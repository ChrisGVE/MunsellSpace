#!/usr/bin/env python3
"""
Phase 4.1: Loss Functions for Polyhedra Transformation

Design and implement loss functions for optimizing screen-to-surface
polyhedra transformation. Uses polyhedron_metrics.py for core calculations.

Loss components:
1. L_centroid: Centroid alignment (Euclidean distance)
2. L_volume: Volume matching (ratio deviation from 1.0)
3. L_shape: Shape similarity (Hausdorff or Procrustes distance)

Combined loss:
L_total = w1 * L_centroid + w2 * L_volume + w3 * L_shape
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from scipy.spatial import ConvexHull
import sys

# Import the existing metrics module
from polyhedron_metrics import PolyhedronMetrics

BASE_DIR = Path(__file__).parent.parent


@dataclass
class TransformationParams:
    """Parameters for affine transformation."""
    translation: np.ndarray  # 3D translation vector
    scale: np.ndarray       # 3D scale factors (or scalar)
    rotation: np.ndarray    # 3x3 rotation matrix


@dataclass
class LossComponents:
    """Individual loss components."""
    centroid_loss: float
    volume_loss: float
    shape_loss: float
    total_loss: float
    weights: Tuple[float, float, float]


def apply_transformation(vertices: np.ndarray, params: TransformationParams) -> np.ndarray:
    """Apply affine transformation to vertices.

    Args:
        vertices: Nx3 array of vertex coordinates
        params: TransformationParams with translation, scale, rotation

    Returns:
        Transformed Nx3 vertex array
    """
    # Apply scale
    if params.scale.shape == ():
        scaled = vertices * params.scale
    else:
        scaled = vertices * params.scale

    # Apply rotation
    rotated = scaled @ params.rotation.T

    # Apply translation
    translated = rotated + params.translation

    return translated


def centroid_loss(screen_vertices: np.ndarray, surface_vertices: np.ndarray,
                  normalize: bool = True) -> float:
    """Compute centroid alignment loss.

    Args:
        screen_vertices: Transformed screen polyhedron vertices
        surface_vertices: Target surface polyhedron vertices
        normalize: If True, normalize by average polyhedron radius

    Returns:
        Normalized Euclidean distance between centroids
    """
    screen_centroid = np.mean(screen_vertices, axis=0)
    surface_centroid = np.mean(surface_vertices, axis=0)

    distance = np.linalg.norm(screen_centroid - surface_centroid)

    if normalize:
        # Normalize by average "radius" (mean distance from centroid)
        screen_radius = np.mean(np.linalg.norm(screen_vertices - screen_centroid, axis=1))
        surface_radius = np.mean(np.linalg.norm(surface_vertices - surface_centroid, axis=1))
        avg_radius = (screen_radius + surface_radius) / 2

        if avg_radius > 0:
            distance = distance / avg_radius

    return distance


def volume_loss(screen_vertices: np.ndarray, surface_vertices: np.ndarray) -> float:
    """Compute volume matching loss.

    Loss = |V_screen / V_surface - 1|

    Penalizes both over and under estimation of volume.

    Args:
        screen_vertices: Transformed screen polyhedron vertices
        surface_vertices: Target surface polyhedron vertices

    Returns:
        Absolute deviation of volume ratio from 1.0
    """
    try:
        screen_hull = ConvexHull(screen_vertices)
        surface_hull = ConvexHull(surface_vertices)

        screen_volume = screen_hull.volume
        surface_volume = surface_hull.volume

        if surface_volume > 0:
            ratio = screen_volume / surface_volume
            return abs(ratio - 1.0)
        else:
            return float('inf')
    except Exception:
        return float('inf')


def hausdorff_loss(screen_vertices: np.ndarray, surface_vertices: np.ndarray,
                   use_average: bool = True) -> float:
    """Compute shape similarity loss using Hausdorff distance.

    Args:
        screen_vertices: Transformed screen polyhedron vertices
        surface_vertices: Target surface polyhedron vertices
        use_average: If True, use average Hausdorff (more stable)

    Returns:
        Normalized Hausdorff distance
    """
    metrics = PolyhedronMetrics(screen_vertices, surface_vertices)
    hausdorff = metrics.calculate_hausdorff_distance()

    if use_average:
        distance = hausdorff.average_hausdorff
    else:
        distance = hausdorff.hausdorff_distance

    # Normalize by average polyhedron diameter
    screen_diameter = np.max(np.linalg.norm(
        screen_vertices[:, np.newaxis] - screen_vertices, axis=2))
    surface_diameter = np.max(np.linalg.norm(
        surface_vertices[:, np.newaxis] - surface_vertices, axis=2))
    avg_diameter = (screen_diameter + surface_diameter) / 2

    if avg_diameter > 0:
        return distance / avg_diameter
    return distance


def procrustes_loss(screen_vertices: np.ndarray, surface_vertices: np.ndarray) -> float:
    """Compute shape similarity loss using Procrustes distance.

    Measures shape difference after optimal alignment.

    Args:
        screen_vertices: Transformed screen polyhedron vertices
        surface_vertices: Target surface polyhedron vertices

    Returns:
        Procrustes distance (0 = identical shape)
    """
    metrics = PolyhedronMetrics(screen_vertices, surface_vertices)
    procrustes = metrics.calculate_procrustes_distance()
    return procrustes.procrustes_distance


def iou_loss(screen_vertices: np.ndarray, surface_vertices: np.ndarray) -> float:
    """Compute IoU-based loss (1 - Jaccard index).

    IoU = Intersection / Union
    Loss = 1 - IoU

    Args:
        screen_vertices: Transformed screen polyhedron vertices
        surface_vertices: Target surface polyhedron vertices

    Returns:
        1 - Jaccard index (0 = perfect overlap, 1 = no overlap)
    """
    metrics = PolyhedronMetrics(screen_vertices, surface_vertices)
    volume_metrics = metrics.calculate_volume_metrics()

    if volume_metrics.jaccard_index is not None:
        return 1.0 - volume_metrics.jaccard_index
    else:
        # If intersection computation failed, use volume ratio as proxy
        return abs(volume_metrics.volume_ratio - 1.0)


class TransformationLoss:
    """Combined loss function for polyhedra transformation optimization."""

    def __init__(self,
                 w_centroid: float = 0.4,
                 w_volume: float = 0.3,
                 w_shape: float = 0.3,
                 shape_metric: str = "hausdorff"):
        """Initialize loss function with weights.

        Args:
            w_centroid: Weight for centroid alignment loss (default 0.4)
            w_volume: Weight for volume matching loss (default 0.3)
            w_shape: Weight for shape similarity loss (default 0.3)
            shape_metric: "hausdorff", "procrustes", or "iou"
        """
        # Normalize weights
        total = w_centroid + w_volume + w_shape
        self.w_centroid = w_centroid / total
        self.w_volume = w_volume / total
        self.w_shape = w_shape / total

        self.shape_metric = shape_metric

        if shape_metric == "hausdorff":
            self.shape_fn = hausdorff_loss
        elif shape_metric == "procrustes":
            self.shape_fn = procrustes_loss
        elif shape_metric == "iou":
            self.shape_fn = iou_loss
        else:
            raise ValueError(f"Unknown shape metric: {shape_metric}")

    def __call__(self, screen_vertices: np.ndarray,
                 surface_vertices: np.ndarray) -> LossComponents:
        """Compute combined loss.

        Args:
            screen_vertices: Transformed screen polyhedron vertices
            surface_vertices: Target surface polyhedron vertices

        Returns:
            LossComponents with individual and total losses
        """
        l_centroid = centroid_loss(screen_vertices, surface_vertices)
        l_volume = volume_loss(screen_vertices, surface_vertices)
        l_shape = self.shape_fn(screen_vertices, surface_vertices)

        l_total = (self.w_centroid * l_centroid +
                   self.w_volume * l_volume +
                   self.w_shape * l_shape)

        return LossComponents(
            centroid_loss=l_centroid,
            volume_loss=l_volume,
            shape_loss=l_shape,
            total_loss=l_total,
            weights=(self.w_centroid, self.w_volume, self.w_shape)
        )


def load_polyhedron(filepath: Path) -> np.ndarray:
    """Load polyhedron vertices from JSON file."""
    with open(filepath) as f:
        data = json.load(f)

    if "vertices" in data:
        return np.array(data["vertices"])
    elif "points" in data:
        return np.array(data["points"])
    else:
        raise ValueError(f"No vertices found in {filepath}")


def analyze_matched_families():
    """Analyze loss components for all matched screen-surface family pairs."""
    matched_file = BASE_DIR / "datasets/matched_families/included_families.json"
    screen_dir = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6"
    surface_dir = BASE_DIR / "datasets/surface_polyhedra"

    with open(matched_file) as f:
        matched = json.load(f)

    results = []
    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    print(f"Analyzing {len(matched)} matched families...")
    print()

    for family_info in matched:
        family = family_info["family"]

        screen_file = screen_dir / f"{family}_polyhedron.json"
        surface_file = surface_dir / f"{family}_polyhedron.json"

        if not screen_file.exists() or not surface_file.exists():
            print(f"  {family}: Missing polyhedron file, skipping")
            continue

        try:
            screen_vertices = load_polyhedron(screen_file)
            surface_vertices = load_polyhedron(surface_file)

            # Compute loss without any transformation (baseline)
            loss = loss_fn(screen_vertices, surface_vertices)

            results.append({
                "family": family,
                "category": family_info["category"],
                "screen_samples": family_info["screen_samples"],
                "surface_samples": family_info["surface_samples"],
                "centroid_loss": loss.centroid_loss,
                "volume_loss": loss.volume_loss,
                "shape_loss": loss.shape_loss,
                "total_loss": loss.total_loss
            })

            print(f"  {family}: L_total={loss.total_loss:.4f} "
                  f"(centroid={loss.centroid_loss:.3f}, "
                  f"volume={loss.volume_loss:.3f}, "
                  f"shape={loss.shape_loss:.3f})")

        except Exception as e:
            print(f"  {family}: Error - {e}")

    return results


def weight_sensitivity_analysis():
    """Analyze sensitivity to weight choices."""
    matched_file = BASE_DIR / "datasets/matched_families/included_families.json"
    screen_dir = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6"
    surface_dir = BASE_DIR / "datasets/surface_polyhedra"

    with open(matched_file) as f:
        matched = json.load(f)

    # Weight configurations to test
    weight_configs = [
        (1.0, 0.0, 0.0, "centroid_only"),
        (0.0, 1.0, 0.0, "volume_only"),
        (0.0, 0.0, 1.0, "shape_only"),
        (0.5, 0.5, 0.0, "centroid_volume"),
        (0.5, 0.0, 0.5, "centroid_shape"),
        (0.0, 0.5, 0.5, "volume_shape"),
        (0.33, 0.33, 0.34, "equal"),
        (0.4, 0.3, 0.3, "centroid_emphasis"),
        (0.3, 0.4, 0.3, "volume_emphasis"),
        (0.3, 0.3, 0.4, "shape_emphasis"),
    ]

    results = {name: [] for _, _, _, name in weight_configs}

    for family_info in matched:
        family = family_info["family"]

        screen_file = screen_dir / f"{family}_polyhedron.json"
        surface_file = surface_dir / f"{family}_polyhedron.json"

        if not screen_file.exists() or not surface_file.exists():
            continue

        try:
            screen_vertices = load_polyhedron(screen_file)
            surface_vertices = load_polyhedron(surface_file)

            for w_c, w_v, w_s, name in weight_configs:
                loss_fn = TransformationLoss(w_centroid=w_c, w_volume=w_v, w_shape=w_s)
                loss = loss_fn(screen_vertices, surface_vertices)
                results[name].append(loss.total_loss)

        except Exception:
            pass

    # Compute statistics
    print("\nWeight Sensitivity Analysis")
    print("=" * 60)
    print(f"{'Config':<20} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10}")
    print("-" * 60)

    for w_c, w_v, w_s, name in weight_configs:
        losses = results[name]
        if losses:
            mean_loss = np.mean(losses)
            std_loss = np.std(losses)
            min_loss = np.min(losses)
            max_loss = np.max(losses)
            print(f"{name:<20} {mean_loss:>10.4f} {std_loss:>10.4f} "
                  f"{min_loss:>10.4f} {max_loss:>10.4f}")

    return results


def generate_report(family_results, weight_results):
    """Generate analysis report."""
    report = []
    report.append("# Loss Functions Analysis Report")
    report.append("")
    report.append("## Loss Function Design")
    report.append("")
    report.append("Combined loss: `L_total = w1 * L_centroid + w2 * L_volume + w3 * L_shape`")
    report.append("")
    report.append("### Component Definitions")
    report.append("")
    report.append("1. **L_centroid**: Normalized Euclidean distance between centroids")
    report.append("   - Normalized by average polyhedron radius")
    report.append("   - Range: [0, inf), 0 = perfect alignment")
    report.append("")
    report.append("2. **L_volume**: Volume ratio deviation")
    report.append("   - `|V_screen / V_surface - 1|`")
    report.append("   - Range: [0, inf), 0 = equal volumes")
    report.append("")
    report.append("3. **L_shape**: Normalized Hausdorff distance")
    report.append("   - Average bidirectional Hausdorff")
    report.append("   - Normalized by average diameter")
    report.append("   - Range: [0, 1], 0 = identical shape")
    report.append("")

    # Family results
    report.append("## Baseline Loss by Family (No Transformation)")
    report.append("")
    report.append("| Family | Category | L_centroid | L_volume | L_shape | L_total |")
    report.append("|--------|----------|------------|----------|---------|---------|")

    for r in sorted(family_results, key=lambda x: x["total_loss"]):
        report.append(f"| {r['family']} | {r['category']} | "
                     f"{r['centroid_loss']:.3f} | {r['volume_loss']:.3f} | "
                     f"{r['shape_loss']:.3f} | {r['total_loss']:.3f} |")

    report.append("")

    # Statistics
    if family_results:
        losses = [r["total_loss"] for r in family_results]
        report.append("### Summary Statistics")
        report.append("")
        report.append(f"- Mean total loss: {np.mean(losses):.4f}")
        report.append(f"- Std total loss: {np.std(losses):.4f}")
        report.append(f"- Min total loss: {np.min(losses):.4f} ({min(family_results, key=lambda x: x['total_loss'])['family']})")
        report.append(f"- Max total loss: {np.max(losses):.4f} ({max(family_results, key=lambda x: x['total_loss'])['family']})")
        report.append("")

    # Weight sensitivity
    report.append("## Weight Sensitivity Analysis")
    report.append("")
    report.append("| Configuration | w_centroid | w_volume | w_shape | Mean Loss |")
    report.append("|---------------|------------|----------|---------|-----------|")

    weight_configs = [
        (1.0, 0.0, 0.0, "centroid_only"),
        (0.0, 1.0, 0.0, "volume_only"),
        (0.0, 0.0, 1.0, "shape_only"),
        (0.33, 0.33, 0.34, "equal"),
        (0.4, 0.3, 0.3, "centroid_emphasis"),
    ]

    for w_c, w_v, w_s, name in weight_configs:
        if name in weight_results and weight_results[name]:
            mean_loss = np.mean(weight_results[name])
            report.append(f"| {name} | {w_c:.2f} | {w_v:.2f} | {w_s:.2f} | {mean_loss:.4f} |")

    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. **Default weights**: w_centroid=0.4, w_volume=0.3, w_shape=0.3")
    report.append("   - Emphasizes centroid alignment as primary objective")
    report.append("   - Balances volume and shape preservation")
    report.append("")
    report.append("2. **For optimization**:")
    report.append("   - Start with centroid-only for fast initial alignment")
    report.append("   - Refine with full loss for final optimization")
    report.append("")

    return "\n".join(report)


def main():
    """Run loss function analysis."""
    print("Phase 4.1: Loss Functions for Polyhedra Transformation")
    print("=" * 60)

    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Analyze matched families
    print("\n1. Baseline Loss Analysis")
    print("-" * 40)
    family_results = analyze_matched_families()

    # Save family results
    family_output = output_dir / "baseline_losses.json"
    with open(family_output, "w") as f:
        json.dump(family_results, f, indent=2)
    print(f"\nSaved: {family_output}")

    # Weight sensitivity
    print("\n2. Weight Sensitivity Analysis")
    print("-" * 40)
    weight_results = weight_sensitivity_analysis()

    # Generate report
    print("\n3. Generating Report")
    print("-" * 40)
    report = generate_report(family_results, weight_results)
    report_path = output_dir / "loss_functions_analysis.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved: {report_path}")


if __name__ == "__main__":
    main()
