#!/usr/bin/env python3
"""
Phase 5.1: Alternative Aggregation Methods

Compare different methods for aggregating loss across families:
- Mean (current baseline)
- Sum (total loss)
- Weighted mean (by sample count)
- Minimax (minimize worst-case loss)
- Trimmed mean (exclude outliers)
- Median (robust to outliers)

The goal is to understand if mean loss hides problematic outlier families.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from scipy.spatial import ConvexHull
from scipy.optimize import minimize

from experiment_logger import ExperimentLogger

BASE_DIR = Path(__file__).parent.parent


@dataclass
class AggregationResult:
    """Results for one aggregation method."""
    method: str
    combined_loss: float
    translation: List[float]
    scaling: List[float]
    per_family_losses: Dict[str, float]
    worst_family: str
    worst_loss: float
    best_family: str
    best_loss: float


def load_polyhedra() -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """Load screen and surface polyhedra."""
    screen_dir = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6"
    surface_dir = BASE_DIR / "datasets/surface_polyhedra"

    screen = {}
    surface = {}

    # Load screen polyhedra
    for f in screen_dir.glob("*_polyhedron.json"):
        name = f.stem.replace("_polyhedron", "")
        with open(f) as file:
            data = json.load(file)
        if "vertices" in data and len(data["vertices"]) >= 4:
            screen[name] = np.array(data["vertices"])

    # Load surface polyhedra (use "points" or "vertices" key)
    for f in surface_dir.glob("*_polyhedron.json"):
        name = f.stem.replace("_polyhedron", "")
        with open(f) as file:
            data = json.load(file)
        vertices_key = "vertices" if "vertices" in data else "points"
        if vertices_key in data and len(data[vertices_key]) >= 4:
            surface[name] = np.array(data[vertices_key])

    return screen, surface


def compute_loss(screen_vertices: np.ndarray,
                 surface_vertices: np.ndarray,
                 translation: np.ndarray,
                 scaling: np.ndarray) -> Tuple[float, float, float]:
    """Compute loss components between transformed screen and surface."""
    # Transform screen vertices
    transformed = screen_vertices * scaling + translation

    # Centroids
    screen_centroid = np.mean(transformed, axis=0)
    surface_centroid = np.mean(surface_vertices, axis=0)
    centroid_dist = np.linalg.norm(screen_centroid - surface_centroid)

    # Normalize centroid by max extent
    max_extent = np.max([
        np.max(transformed) - np.min(transformed),
        np.max(surface_vertices) - np.min(surface_vertices)
    ])
    centroid_loss = centroid_dist / max_extent if max_extent > 0 else 0

    # Volumes
    try:
        screen_hull = ConvexHull(transformed)
        surface_hull = ConvexHull(surface_vertices)
        volume_ratio = screen_hull.volume / surface_hull.volume
        volume_loss = abs(volume_ratio - 1.0)
    except Exception:
        volume_loss = 1.0

    # Hausdorff distance (simplified average)
    from scipy.spatial import cKDTree
    tree_screen = cKDTree(transformed)
    tree_surface = cKDTree(surface_vertices)

    d1, _ = tree_surface.query(transformed)
    d2, _ = tree_screen.query(surface_vertices)

    hausdorff = (np.mean(d1) + np.mean(d2)) / 2
    shape_loss = hausdorff / max_extent if max_extent > 0 else 0

    return centroid_loss, volume_loss, shape_loss


def optimize_for_family(screen: np.ndarray,
                        surface: np.ndarray,
                        loss_weights: Tuple[float, float, float] = (0.4, 0.3, 0.3)) -> Tuple[np.ndarray, np.ndarray, float]:
    """Optimize transformation for a single family."""
    w_c, w_v, w_s = loss_weights

    def objective(params):
        translation = params[:3]
        scaling = params[3:6]
        c, v, s = compute_loss(screen, surface, translation, scaling)
        return w_c * c + w_v * v + w_s * s

    # Initial guess: align centroids, scale to match
    screen_centroid = np.mean(screen, axis=0)
    surface_centroid = np.mean(surface, axis=0)

    screen_extent = np.max(screen, axis=0) - np.min(screen, axis=0)
    surface_extent = np.max(surface, axis=0) - np.min(surface, axis=0)

    initial_translation = surface_centroid - screen_centroid
    initial_scaling = np.ones(3)
    mask = screen_extent > 1e-6
    initial_scaling[mask] = surface_extent[mask] / screen_extent[mask]

    initial_params = np.concatenate([initial_translation, initial_scaling])

    result = minimize(objective, initial_params, method='L-BFGS-B',
                     options={'maxiter': 1000})

    translation = result.x[:3]
    scaling = result.x[3:6]

    return translation, scaling, result.fun


def aggregate_mean(losses: Dict[str, float]) -> float:
    """Standard mean aggregation."""
    return np.mean(list(losses.values()))


def aggregate_sum(losses: Dict[str, float]) -> float:
    """Sum aggregation (total loss)."""
    return np.sum(list(losses.values()))


def aggregate_weighted_mean(losses: Dict[str, float],
                           weights: Dict[str, float]) -> float:
    """Weighted mean aggregation (e.g., by sample count)."""
    total_weight = sum(weights.get(k, 1.0) for k in losses)
    weighted_sum = sum(losses[k] * weights.get(k, 1.0) for k in losses)
    return weighted_sum / total_weight if total_weight > 0 else 0


def aggregate_minimax(losses: Dict[str, float]) -> float:
    """Minimax - worst-case loss."""
    return max(losses.values())


def aggregate_trimmed_mean(losses: Dict[str, float], trim_frac: float = 0.1) -> float:
    """Trimmed mean - exclude extreme values."""
    values = sorted(losses.values())
    n = len(values)
    trim_count = int(n * trim_frac)
    if trim_count * 2 >= n:
        return np.mean(values)
    trimmed = values[trim_count:n - trim_count]
    return np.mean(trimmed)


def aggregate_median(losses: Dict[str, float]) -> float:
    """Median aggregation (robust to outliers)."""
    return np.median(list(losses.values()))


def optimize_global_transformation(
    screen_dict: Dict[str, np.ndarray],
    surface_dict: Dict[str, np.ndarray],
    families: List[str],
    aggregation_fn: Callable[[Dict[str, float]], float],
    loss_weights: Tuple[float, float, float] = (0.4, 0.3, 0.3)
) -> Tuple[np.ndarray, np.ndarray, Dict[str, float]]:
    """Optimize a global transformation using specified aggregation method."""

    w_c, w_v, w_s = loss_weights

    def objective(params):
        translation = params[:3]
        scaling = params[3:6]

        family_losses = {}
        for family in families:
            screen = screen_dict[family]
            surface = surface_dict[family]
            c, v, s = compute_loss(screen, surface, translation, scaling)
            combined = w_c * c + w_v * v + w_s * s
            family_losses[family] = combined

        return aggregation_fn(family_losses)

    # Initialize from average of per-family optima
    translations = []
    scalings = []
    for family in families[:5]:  # Use first 5 for speed
        t, s, _ = optimize_for_family(screen_dict[family], surface_dict[family])
        translations.append(t)
        scalings.append(s)

    initial_translation = np.mean(translations, axis=0)
    initial_scaling = np.mean(scalings, axis=0)
    initial_params = np.concatenate([initial_translation, initial_scaling])

    result = minimize(objective, initial_params, method='L-BFGS-B',
                     options={'maxiter': 1000})

    translation = result.x[:3]
    scaling = result.x[3:6]

    # Compute final per-family losses
    family_losses = {}
    for family in families:
        screen = screen_dict[family]
        surface = surface_dict[family]
        c, v, s = compute_loss(screen, surface, translation, scaling)
        family_losses[family] = w_c * c + w_v * v + w_s * s

    return translation, scaling, family_losses


def get_sample_counts(families: List[str]) -> Dict[str, float]:
    """Get sample counts for each family (for weighted mean)."""
    summary_file = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6_summary.json"

    weights = {}
    if summary_file.exists():
        with open(summary_file) as f:
            data = json.load(f)

        for family in families:
            if family in data.get("families", {}):
                weights[family] = data["families"][family].get("sample_count", 1)
            else:
                weights[family] = 1
    else:
        for family in families:
            weights[family] = 1

    return weights


def main():
    """Run aggregation method comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Phase 5.1: Alternative Aggregation Methods")
    print("=" * 70)

    # Load data
    screen, surface = load_polyhedra()
    families = sorted(set(screen.keys()) & set(surface.keys()))
    print(f"Loaded {len(families)} families with valid polyhedra")

    # Get sample weights
    sample_weights = get_sample_counts(families)

    # Define aggregation methods
    methods = {
        "mean": lambda x: aggregate_mean(x),
        "sum": lambda x: aggregate_sum(x),
        "weighted_mean": lambda x: aggregate_weighted_mean(x, sample_weights),
        "minimax": lambda x: aggregate_minimax(x),
        "trimmed_mean_10": lambda x: aggregate_trimmed_mean(x, 0.1),
        "trimmed_mean_20": lambda x: aggregate_trimmed_mean(x, 0.2),
        "median": lambda x: aggregate_median(x),
    }

    results = []

    for method_name, agg_fn in methods.items():
        print(f"\nOptimizing with {method_name} aggregation...")

        translation, scaling, family_losses = optimize_global_transformation(
            screen, surface, families, agg_fn
        )

        worst_family = max(family_losses, key=family_losses.get)
        best_family = min(family_losses, key=family_losses.get)

        result = AggregationResult(
            method=method_name,
            combined_loss=agg_fn(family_losses),
            translation=translation.tolist(),
            scaling=scaling.tolist(),
            per_family_losses=family_losses,
            worst_family=worst_family,
            worst_loss=family_losses[worst_family],
            best_family=best_family,
            best_loss=family_losses[best_family]
        )
        results.append(result)

        # Also compute mean for comparison
        mean_loss = aggregate_mean(family_losses)

        print(f"  Aggregated loss: {result.combined_loss:.4f}")
        print(f"  Mean loss: {mean_loss:.4f}")
        print(f"  Worst: {worst_family} ({result.worst_loss:.4f})")
        print(f"  Best: {best_family} ({result.best_loss:.4f})")

    # Initialize experiment logger
    logger = ExperimentLogger()

    exp_id = logger.register_experiment(
        name="Aggregation Method Comparison",
        method="aggregation_analysis",
        domain="munsell_cartesian",
        loss_function="combined",
        parameters={
            "n_families": len(families),
            "methods_tested": list(methods.keys())
        },
        tags=["aggregation", "phase5.1", "comparison"]
    )

    logger.log_result(exp_id, {
        "results": [asdict(r) for r in results],
        "sample_weights": sample_weights
    })

    # Save results
    results_file = output_dir / "aggregation_comparison.json"
    results_data = {
        "families": families,
        "sample_weights": sample_weights,
        "results": [asdict(r) for r in results]
    }
    with open(results_file, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, families, sample_weights)
    report_file = output_dir / "aggregation_comparison.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")

    # Summary
    print("\n" + "=" * 70)
    print("AGGREGATION METHOD SUMMARY")
    print("=" * 70)

    print("\n| Method | Aggregated Loss | Mean Loss | Worst Family | Worst Loss |")
    print("|--------|-----------------|-----------|--------------|------------|")

    for r in sorted(results, key=lambda x: aggregate_mean(x.per_family_losses)):
        mean_loss = aggregate_mean(r.per_family_losses)
        print(f"| {r.method} | {r.combined_loss:.4f} | {mean_loss:.4f} | {r.worst_family} | {r.worst_loss:.4f} |")


def generate_report(results: List[AggregationResult],
                   families: List[str],
                   sample_weights: Dict[str, float]) -> str:
    """Generate aggregation comparison report."""
    report = []
    report.append("# Aggregation Method Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Families analyzed: {len(families)}")
    report.append("")

    # Method definitions
    report.append("## Aggregation Methods")
    report.append("")
    report.append("| Method | Description |")
    report.append("|--------|-------------|")
    report.append("| mean | Arithmetic mean of family losses |")
    report.append("| sum | Total sum of family losses |")
    report.append("| weighted_mean | Mean weighted by sample count |")
    report.append("| minimax | Worst-case (maximum) loss |")
    report.append("| trimmed_mean_10 | Mean with 10% trimmed from each end |")
    report.append("| trimmed_mean_20 | Mean with 20% trimmed from each end |")
    report.append("| median | Median loss (robust to outliers) |")
    report.append("")

    # Results summary
    report.append("## Results Summary")
    report.append("")
    report.append("| Method | Aggregated Loss | Mean Loss | Worst Family | Worst Loss |")
    report.append("|--------|-----------------|-----------|--------------|------------|")

    for r in sorted(results, key=lambda x: aggregate_mean(x.per_family_losses)):
        mean_loss = aggregate_mean(r.per_family_losses)
        report.append(f"| {r.method} | {r.combined_loss:.4f} | {mean_loss:.4f} | {r.worst_family} | {r.worst_loss:.4f} |")

    report.append("")

    # Outlier analysis
    report.append("## Outlier Analysis")
    report.append("")

    # Find consistent outliers across methods
    worst_counts = {}
    for r in results:
        if r.worst_family not in worst_counts:
            worst_counts[r.worst_family] = 0
        worst_counts[r.worst_family] += 1

    report.append("Families appearing as worst across methods:")
    report.append("")
    for family, count in sorted(worst_counts.items(), key=lambda x: -x[1]):
        report.append(f"- **{family}**: {count}/{len(results)} methods")

    report.append("")

    # Per-family loss distribution
    report.append("## Per-Family Loss Distribution (Mean Aggregation)")
    report.append("")

    mean_result = next((r for r in results if r.method == "mean"), results[0])
    sorted_families = sorted(mean_result.per_family_losses.items(), key=lambda x: x[1])

    report.append("| Rank | Family | Loss | Weight |")
    report.append("|------|--------|------|--------|")

    for i, (family, loss) in enumerate(sorted_families, 1):
        weight = sample_weights.get(family, 1)
        report.append(f"| {i} | {family} | {loss:.4f} | {weight:.0f} |")

    report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    # Check if minimax and mean give same transformation
    mean_result = next((r for r in results if r.method == "mean"), None)
    minimax_result = next((r for r in results if r.method == "minimax"), None)

    if mean_result and minimax_result:
        mean_worst = mean_result.worst_loss
        minimax_worst = minimax_result.worst_loss
        improvement = (mean_worst - minimax_worst) / mean_worst * 100

        report.append(f"1. **Minimax vs Mean**: Worst-case loss improved by {improvement:.1f}%")
        report.append(f"   - Mean method worst: {mean_worst:.4f}")
        report.append(f"   - Minimax method worst: {minimax_worst:.4f}")
        report.append("")

    # Check if outliers dominate
    losses = list(mean_result.per_family_losses.values())
    std = np.std(losses)
    mean = np.mean(losses)
    cv = std / mean if mean > 0 else 0

    report.append(f"2. **Loss distribution**: CV = {cv:.2f} (std/mean)")
    if cv > 0.5:
        report.append("   - High variability suggests outliers are significant")
    else:
        report.append("   - Moderate variability, outliers not dominant")

    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. **For general use**: Mean aggregation provides good balance")
    report.append("2. **For worst-case guarantees**: Use minimax optimization")
    report.append("3. **For robustness**: Consider trimmed mean or median")
    report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    main()
