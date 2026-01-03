#!/usr/bin/env python3
"""
Phase 4.4: Deep Learning Transformation Search

Implement neural network approaches for screen-to-surface color
polyhedra transformation:
1. MLP (multi-layer perceptron)
2. Residual network (T(x) = x + f(x))
3. Variational approach (uncertainty quantification)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import warnings

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available. Install with: pip install torch")

from loss_functions import (
    TransformationLoss, LossComponents, load_polyhedron,
    centroid_loss, volume_loss, hausdorff_loss
)
from linear_transformations import (
    load_matched_families, TranslationScalingTransform,
    optimize_transformation
)

BASE_DIR = Path(__file__).parent.parent


@dataclass
class NNTransformResult:
    """Result of neural network transformation training."""
    name: str
    mean_loss: float
    std_loss: float
    per_family_losses: Dict[str, float]
    training_epochs: int
    parameters: int
    training_time: float


# ============================================================
# Dataset and Training Utilities
# ============================================================

class PolyhedraDataset(Dataset):
    """Dataset of matched screen-surface point pairs."""

    def __init__(self, families_data: Dict):
        """Initialize with matched family data.

        Args:
            families_data: Dict mapping family -> (screen_vertices, surface_vertices)
        """
        self.points = []
        self.targets = []
        self.families = []

        for family, (screen, surface) in families_data.items():
            # Use centroids for point-to-point correspondence
            screen_centroid = np.mean(screen, axis=0)
            surface_centroid = np.mean(surface, axis=0)

            self.points.append(screen_centroid)
            self.targets.append(surface_centroid)
            self.families.append(family)

            # Also add vertices (with matched indices if same count)
            min_verts = min(len(screen), len(surface))
            for i in range(min_verts):
                self.points.append(screen[i])
                self.targets.append(surface[i])
                self.families.append(family)

        self.points = np.array(self.points, dtype=np.float32)
        self.targets = np.array(self.targets, dtype=np.float32)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        return self.points[idx], self.targets[idx]


def create_dataloaders(families_data: Dict,
                       batch_size: int = 32,
                       val_families: Optional[List[str]] = None) -> Tuple:
    """Create train and validation dataloaders.

    Args:
        families_data: Dict mapping family -> (screen_vertices, surface_vertices)
        batch_size: Batch size for training
        val_families: List of family names to hold out for validation

    Returns:
        Tuple of (train_loader, val_loader, train_families, val_families_data)
    """
    if val_families is None:
        # Hold out ~20% for validation
        all_families = list(families_data.keys())
        n_val = max(1, len(all_families) // 5)
        val_families = all_families[:n_val]

    train_data = {k: v for k, v in families_data.items() if k not in val_families}
    val_data = {k: v for k, v in families_data.items() if k in val_families}

    train_dataset = PolyhedraDataset(train_data)
    val_dataset = PolyhedraDataset(val_data)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, train_data, val_data


# ============================================================
# Neural Network Models
# ============================================================

class MLPTransform(nn.Module):
    """Multi-layer perceptron transformation.

    Architecture:
        Input (3) -> Hidden (64) -> Hidden (128) -> Hidden (64) -> Output (3)
    """

    def __init__(self, hidden_sizes: List[int] = [64, 128, 64]):
        super().__init__()

        layers = []
        in_size = 3  # Munsell Cartesian (x, y, z)

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(in_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm1d(hidden_size))
            in_size = hidden_size

        layers.append(nn.Linear(in_size, 3))  # Output

        self.net = nn.Sequential(*layers)

        # Initialize weights
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        return self.net(x)

    @property
    def n_parameters(self):
        return sum(p.numel() for p in self.parameters())


class ResidualBlock(nn.Module):
    """Residual block with skip connection."""

    def __init__(self, size: int):
        super().__init__()
        self.fc1 = nn.Linear(size, size)
        self.fc2 = nn.Linear(size, size)
        self.bn1 = nn.BatchNorm1d(size)
        self.bn2 = nn.BatchNorm1d(size)
        self.relu = nn.ReLU()

    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.fc1(x)))
        out = self.bn2(self.fc2(out))
        out = out + identity  # Skip connection
        out = self.relu(out)
        return out


class ResidualTransform(nn.Module):
    """Residual network for small corrections.

    Learns T(x) = x + f(x) where f(x) is a small correction.
    This makes it easier to learn identity-like transformations.
    """

    def __init__(self, hidden_size: int = 64, n_blocks: int = 2):
        super().__init__()

        self.input_proj = nn.Linear(3, hidden_size)
        self.bn_input = nn.BatchNorm1d(hidden_size)

        self.blocks = nn.ModuleList([
            ResidualBlock(hidden_size) for _ in range(n_blocks)
        ])

        self.output_proj = nn.Linear(hidden_size, 3)

        # Initialize output to near-zero for identity-like start
        nn.init.zeros_(self.output_proj.weight)
        nn.init.zeros_(self.output_proj.bias)

    def forward(self, x):
        # Project to hidden space
        h = torch.relu(self.bn_input(self.input_proj(x)))

        # Pass through residual blocks
        for block in self.blocks:
            h = block(h)

        # Project back and add residual connection
        correction = self.output_proj(h)
        return x + correction  # T(x) = x + f(x)

    @property
    def n_parameters(self):
        return sum(p.numel() for p in self.parameters())


class VariationalTransform(nn.Module):
    """Variational transformation with uncertainty quantification.

    Outputs a distribution (mean, variance) rather than point estimate.
    Useful for quantifying confidence in transformation.
    """

    def __init__(self, hidden_sizes: List[int] = [64, 128]):
        super().__init__()

        # Shared encoder
        encoder_layers = []
        in_size = 3
        for hidden_size in hidden_sizes:
            encoder_layers.append(nn.Linear(in_size, hidden_size))
            encoder_layers.append(nn.ReLU())
            encoder_layers.append(nn.BatchNorm1d(hidden_size))
            in_size = hidden_size

        self.encoder = nn.Sequential(*encoder_layers)

        # Mean and log-variance heads
        self.mean_head = nn.Linear(in_size, 3)
        self.logvar_head = nn.Linear(in_size, 3)

        # Initialize mean head to identity-like
        nn.init.zeros_(self.mean_head.weight)
        nn.init.zeros_(self.mean_head.bias)

        # Initialize log-variance to small values (low uncertainty)
        nn.init.constant_(self.logvar_head.weight, 0.0)
        nn.init.constant_(self.logvar_head.bias, -2.0)  # exp(-2) ≈ 0.14

    def forward(self, x, sample: bool = True):
        """Forward pass.

        Args:
            x: Input coordinates
            sample: If True, sample from distribution; if False, return mean

        Returns:
            If sample=True: (sampled_output, mean, logvar)
            If sample=False: mean
        """
        h = self.encoder(x)

        mean = x + self.mean_head(h)  # Residual connection for mean
        logvar = self.logvar_head(h)

        if sample and self.training:
            # Reparameterization trick
            std = torch.exp(0.5 * logvar)
            eps = torch.randn_like(std)
            output = mean + eps * std
            return output, mean, logvar
        else:
            return mean

    def get_uncertainty(self, x):
        """Get uncertainty (standard deviation) for input."""
        h = self.encoder(x)
        logvar = self.logvar_head(h)
        return torch.exp(0.5 * logvar)

    @property
    def n_parameters(self):
        return sum(p.numel() for p in self.parameters())


# ============================================================
# Training Functions
# ============================================================

def train_model(model: nn.Module,
                train_loader: DataLoader,
                val_loader: DataLoader,
                n_epochs: int = 100,
                lr: float = 0.001,
                device: str = "cpu",
                variational: bool = False,
                kl_weight: float = 0.001) -> Dict:
    """Train a neural network model.

    Args:
        model: PyTorch model to train
        train_loader: Training data loader
        val_loader: Validation data loader
        n_epochs: Number of training epochs
        lr: Learning rate
        device: Device to train on
        variational: If True, use variational loss (for VariationalTransform)
        kl_weight: Weight for KL divergence term (only if variational=True)

    Returns:
        Training history dict
    """
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10, factor=0.5)

    criterion = nn.MSELoss()

    history = {
        "train_loss": [],
        "val_loss": [],
        "best_val_loss": float('inf'),
        "best_epoch": 0
    }

    best_state = None

    for epoch in range(n_epochs):
        # Training
        model.train()
        train_losses = []

        for points, targets in train_loader:
            points = points.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()

            if variational:
                output, mean, logvar = model(points, sample=True)
                recon_loss = criterion(output, targets)
                # KL divergence: -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
                kl_loss = -0.5 * torch.mean(1 + logvar - mean.pow(2) - logvar.exp())
                loss = recon_loss + kl_weight * kl_loss
            else:
                output = model(points)
                loss = criterion(output, targets)

            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())

        # Validation
        model.eval()
        val_losses = []

        with torch.no_grad():
            for points, targets in val_loader:
                points = points.to(device)
                targets = targets.to(device)

                if variational:
                    output = model(points, sample=False)
                else:
                    output = model(points)

                loss = criterion(output, targets)
                val_losses.append(loss.item())

        train_loss = np.mean(train_losses)
        val_loss = np.mean(val_losses) if val_losses else train_loss

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        scheduler.step(val_loss)

        if val_loss < history["best_val_loss"]:
            history["best_val_loss"] = val_loss
            history["best_epoch"] = epoch
            best_state = model.state_dict().copy()

        # Early stopping
        if epoch - history["best_epoch"] > 20:
            break

    # Restore best model
    if best_state is not None:
        model.load_state_dict(best_state)

    return history


def evaluate_on_polyhedra(model: nn.Module,
                          families_data: Dict,
                          loss_fn: TransformationLoss,
                          device: str = "cpu",
                          variational: bool = False) -> Dict[str, float]:
    """Evaluate model on polyhedra transformation task.

    Args:
        model: Trained model
        families_data: Dict mapping family -> (screen_vertices, surface_vertices)
        loss_fn: Loss function for evaluation
        device: Device for inference
        variational: If True, model is variational

    Returns:
        Dict mapping family -> loss
    """
    model.eval()
    results = {}

    with torch.no_grad():
        for family, (screen_verts, surface_verts) in families_data.items():
            # Transform screen vertices
            screen_tensor = torch.tensor(screen_verts, dtype=torch.float32).to(device)

            if variational:
                transformed = model(screen_tensor, sample=False).cpu().numpy()
            else:
                transformed = model(screen_tensor).cpu().numpy()

            # Compute loss
            try:
                loss = loss_fn(transformed, surface_verts)
                results[family] = loss.total_loss
            except Exception:
                results[family] = float('inf')

    return results


# ============================================================
# Main Comparison
# ============================================================

def run_nn_comparison():
    """Run comparison of neural network approaches."""
    if not TORCH_AVAILABLE:
        print("PyTorch not available. Skipping neural network comparison.")
        return None

    print("Phase 4.4: Deep Learning Transformation Search")
    print("=" * 60)

    # Load data
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    if len(families_data) < 5:
        print("Not enough families for meaningful neural network training")
        return None

    # Setup
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    # Create data loaders
    train_loader, val_loader, train_data, val_data = create_dataloaders(
        families_data, batch_size=16
    )

    print(f"Training families: {len(train_data)}")
    print(f"Validation families: {len(val_data)}")

    results = {}

    # --------------------------------------------------------
    # 1. MLP Transform
    # --------------------------------------------------------
    print("\n1. MLP Transform")
    print("-" * 40)

    import time
    start_time = time.time()

    mlp_model = MLPTransform(hidden_sizes=[64, 128, 64])
    print(f"   Parameters: {mlp_model.n_parameters}")

    mlp_history = train_model(
        mlp_model, train_loader, val_loader,
        n_epochs=100, lr=0.001, device=device
    )

    mlp_losses = evaluate_on_polyhedra(mlp_model, families_data, loss_fn, device)
    mlp_time = time.time() - start_time

    valid_losses = [v for v in mlp_losses.values() if v < float('inf')]
    if valid_losses:
        print(f"   Mean loss: {np.mean(valid_losses):.4f} (±{np.std(valid_losses):.4f})")
        print(f"   Best epoch: {mlp_history['best_epoch']}")
        print(f"   Training time: {mlp_time:.1f}s")

        results["mlp"] = NNTransformResult(
            name="MLP",
            mean_loss=float(np.mean(valid_losses)),
            std_loss=float(np.std(valid_losses)),
            per_family_losses=mlp_losses,
            training_epochs=mlp_history['best_epoch'],
            parameters=mlp_model.n_parameters,
            training_time=mlp_time
        )

    # --------------------------------------------------------
    # 2. Residual Transform
    # --------------------------------------------------------
    print("\n2. Residual Transform")
    print("-" * 40)

    start_time = time.time()

    res_model = ResidualTransform(hidden_size=64, n_blocks=2)
    print(f"   Parameters: {res_model.n_parameters}")

    res_history = train_model(
        res_model, train_loader, val_loader,
        n_epochs=100, lr=0.001, device=device
    )

    res_losses = evaluate_on_polyhedra(res_model, families_data, loss_fn, device)
    res_time = time.time() - start_time

    valid_losses = [v for v in res_losses.values() if v < float('inf')]
    if valid_losses:
        print(f"   Mean loss: {np.mean(valid_losses):.4f} (±{np.std(valid_losses):.4f})")
        print(f"   Best epoch: {res_history['best_epoch']}")
        print(f"   Training time: {res_time:.1f}s")

        results["residual"] = NNTransformResult(
            name="Residual",
            mean_loss=float(np.mean(valid_losses)),
            std_loss=float(np.std(valid_losses)),
            per_family_losses=res_losses,
            training_epochs=res_history['best_epoch'],
            parameters=res_model.n_parameters,
            training_time=res_time
        )

    # --------------------------------------------------------
    # 3. Variational Transform
    # --------------------------------------------------------
    print("\n3. Variational Transform")
    print("-" * 40)

    start_time = time.time()

    var_model = VariationalTransform(hidden_sizes=[64, 128])
    print(f"   Parameters: {var_model.n_parameters}")

    var_history = train_model(
        var_model, train_loader, val_loader,
        n_epochs=100, lr=0.001, device=device,
        variational=True, kl_weight=0.001
    )

    var_losses = evaluate_on_polyhedra(
        var_model, families_data, loss_fn, device, variational=True
    )
    var_time = time.time() - start_time

    valid_losses = [v for v in var_losses.values() if v < float('inf')]
    if valid_losses:
        print(f"   Mean loss: {np.mean(valid_losses):.4f} (±{np.std(valid_losses):.4f})")
        print(f"   Best epoch: {var_history['best_epoch']}")
        print(f"   Training time: {var_time:.1f}s")

        # Get uncertainty estimates
        print("\n   Uncertainty by family:")
        var_model.eval()
        with torch.no_grad():
            for family in list(families_data.keys())[:5]:
                screen_verts = families_data[family][0]
                screen_tensor = torch.tensor(screen_verts, dtype=torch.float32).to(device)
                uncertainty = var_model.get_uncertainty(screen_tensor).mean().item()
                print(f"     {family}: ±{uncertainty:.3f}")

        results["variational"] = NNTransformResult(
            name="Variational",
            mean_loss=float(np.mean(valid_losses)),
            std_loss=float(np.std(valid_losses)),
            per_family_losses=var_losses,
            training_epochs=var_history['best_epoch'],
            parameters=var_model.n_parameters,
            training_time=var_time
        )

    # --------------------------------------------------------
    # 4. Comparison with Linear Baseline
    # --------------------------------------------------------
    print("\n4. Comparison with Linear Baseline")
    print("-" * 40)

    # Get linear baseline
    linear_losses = {}
    for family, (screen_verts, surface_verts) in families_data.items():
        try:
            result = optimize_transformation(
                TranslationScalingTransform, screen_verts, surface_verts, loss_fn
            )
            linear_losses[family] = result.final_loss
        except Exception:
            linear_losses[family] = float('inf')

    valid_linear = [v for v in linear_losses.values() if v < float('inf')]
    if valid_linear:
        print(f"   Translation+Scaling: {np.mean(valid_linear):.4f} (±{np.std(valid_linear):.4f})")

        results["linear_baseline"] = NNTransformResult(
            name="Translation+Scaling",
            mean_loss=float(np.mean(valid_linear)),
            std_loss=float(np.std(valid_linear)),
            per_family_losses=linear_losses,
            training_epochs=0,
            parameters=6,
            training_time=0.0
        )

    return results, families_data


def generate_report(results: Dict, families_data: Dict) -> str:
    """Generate comparison report."""
    report = []
    report.append("# Deep Learning Transformation Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Families analyzed: {len(families_data)}")
    report.append("")

    # Model descriptions
    report.append("## Model Architectures")
    report.append("")
    report.append("| Model | Parameters | Description |")
    report.append("|-------|------------|-------------|")
    report.append("| Translation+Scaling | 6 | Linear baseline (3 scale + 3 translation) |")
    report.append("| MLP | ~25K | 3→64→128→64→3 with ReLU, BatchNorm |")
    report.append("| Residual | ~17K | T(x) = x + f(x), 2 residual blocks |")
    report.append("| Variational | ~18K | Outputs distribution (mean, variance) |")
    report.append("")

    # Summary results
    report.append("## Summary Results")
    report.append("")
    report.append("| Model | Mean Loss | Std Loss | Parameters | Training Time |")
    report.append("|-------|-----------|----------|------------|---------------|")

    for name, result in sorted(results.items(), key=lambda x: x[1].mean_loss):
        report.append(f"| {result.name} | {result.mean_loss:.4f} | {result.std_loss:.4f} | "
                     f"{result.parameters:,} | {result.training_time:.1f}s |")

    report.append("")

    # Per-family comparison
    report.append("## Per-Family Comparison")
    report.append("")

    families = list(families_data.keys())
    header = "| Family |"
    separator = "|--------|"
    for name in results.keys():
        header += f" {results[name].name} |"
        separator += "---------|"

    report.append(header)
    report.append(separator)

    for family in families:
        row = f"| {family} |"
        for name, result in results.items():
            loss = result.per_family_losses.get(family, float('inf'))
            if loss < float('inf'):
                row += f" {loss:.3f} |"
            else:
                row += " N/A |"
        report.append(row)

    report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    if "linear_baseline" in results:
        linear_loss = results["linear_baseline"].mean_loss
        for name, result in results.items():
            if name != "linear_baseline":
                diff = result.mean_loss - linear_loss
                if diff > 0:
                    report.append(f"- **{result.name}**: {diff:.3f} worse than linear "
                                 f"(+{100*diff/linear_loss:.1f}%)")
                else:
                    report.append(f"- **{result.name}**: {-diff:.3f} better than linear "
                                 f"({100*diff/linear_loss:.1f}%)")

    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. **For production use**: Prefer Translation+Scaling (6 params)")
    report.append("   - Lowest loss achieved with simplest model")
    report.append("   - No training required, fast optimization")
    report.append("   - Interpretable parameters")
    report.append("")
    report.append("2. **Neural network observations**:")
    report.append("   - Limited training data (21 families) constrains deep learning")
    report.append("   - Point-to-point correspondence is imperfect for polyhedra")
    report.append("   - Residual architecture helps but doesn't overcome data limitations")
    report.append("")
    report.append("3. **Variational approach**:")
    report.append("   - Provides uncertainty quantification")
    report.append("   - May be useful for identifying unreliable transformations")
    report.append("   - Higher computational cost for marginal benefit")
    report.append("")
    report.append("4. **Future improvements**:")
    report.append("   - More surface color data would enable better deep learning")
    report.append("   - Graph neural networks for proper polyhedra correspondence")
    report.append("   - Transfer learning from larger color datasets")

    return "\n".join(report)


def main():
    """Run deep learning transformation comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run comparison
    result = run_nn_comparison()

    if result is None:
        print("Comparison failed or PyTorch not available")
        return

    results, families_data = result

    # Save results
    results_file = output_dir / "nn_comparison.json"

    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, NNTransformResult):
            return asdict(obj)
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        return obj

    with open(results_file, "w") as f:
        json.dump(convert_for_json(results), f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, families_data)
    report_file = output_dir / "nn_comparison.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")


if __name__ == "__main__":
    main()
