#!/usr/bin/env python3
"""
Phase 5.1: Alternative Loss Metrics

Implement alternative loss metrics for polyhedra comparison:
1. Chamfer Distance - symmetric average nearest-neighbor
2. Earth Mover's Distance - optimal transport (Wasserstein)
3. Spectral Loss - eigenvalue comparison of covariance matrices
4. IoU Loss - 1 - Jaccard index (via Monte Carlo sampling)

Compare against existing metrics (centroid, volume, Hausdorff).
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from scipy.spatial import ConvexHull, KDTree, Delaunay
from scipy.stats import wasserstein_distance
from datetime import datetime, timezone
import warnings

from loss_functions import (
    centroid_loss, volume_loss, hausdorff_loss, load_polyhedron
)
from linear_transformations import (
    TranslationScalingTransform, load_matched_families
)
from experiment_logger import ExperimentLogger

BASE_DIR = Path(__file__).parent.parent


def chamfer_distance(points_a: np.ndarray, points_b: np.ndarray,
                    normalize: bool = True) -> float:
    """Compute symmetric Chamfer distance between two point sets.

    Chamfer distance is the average of:
    - mean distance from each point in A to its nearest neighbor in B
    - mean distance from each point in B to its nearest neighbor in A

    Args:
        points_a: Nx3 array of points
        points_b: Mx3 array of points
        normalize: If True, normalize by average diameter

    Returns:
        Chamfer distance (lower is better, 0 = identical)
    """
    # Build KD-trees for efficient nearest neighbor queries
    tree_a = KDTree(points_a)
    tree_b = KDTree(points_b)

    # A -> B: for each point in A, find nearest in B
    distances_a_to_b, _ = tree_b.query(points_a)
    mean_a_to_b = np.mean(distances_a_to_b)

    # B -> A: for each point in B, find nearest in A
    distances_b_to_a, _ = tree_a.query(points_b)
    mean_b_to_a = np.mean(distances_b_to_a)

    # Symmetric Chamfer distance
    chamfer = (mean_a_to_b + mean_b_to_a) / 2

    if normalize:
        # Normalize by average diameter
        diameter_a = np.max(np.linalg.norm(
            points_a[:, np.newaxis] - points_a, axis=2))
        diameter_b = np.max(np.linalg.norm(
            points_b[:, np.newaxis] - points_b, axis=2))
        avg_diameter = (diameter_a + diameter_b) / 2

        if avg_diameter > 0:
            chamfer = chamfer / avg_diameter

    return float(chamfer)


def earth_movers_distance(points_a: np.ndarray, points_b: np.ndarray,
                          normalize: bool = True) -> float:
    """Compute Earth Mover's Distance (Wasserstein) between point distributions.

    Uses 1D Wasserstein on each axis and combines with L2 norm.
    Full 3D optimal transport is expensive; this is an approximation.

    Args:
        points_a: Nx3 array of points
        points_b: Mx3 array of points
        normalize: If True, normalize by average diameter

    Returns:
        EMD (lower is better, 0 = identical distributions)
    """
    # Compute 1D Wasserstein distance per axis and combine
    emd_per_axis = []
    for axis in range(3):
        w_dist = wasserstein_distance(points_a[:, axis], points_b[:, axis])
        emd_per_axis.append(w_dist)

    # Combine with L2 norm
    emd = np.sqrt(sum(w**2 for w in emd_per_axis))

    if normalize:
        # Normalize by average diameter
        diameter_a = np.max(np.linalg.norm(
            points_a[:, np.newaxis] - points_a, axis=2))
        diameter_b = np.max(np.linalg.norm(
            points_b[:, np.newaxis] - points_b, axis=2))
        avg_diameter = (diameter_a + diameter_b) / 2

        if avg_diameter > 0:
            emd = emd / avg_diameter

    return float(emd)


def spectral_loss(points_a: np.ndarray, points_b: np.ndarray) -> float:
    """Compute spectral loss based on covariance matrix eigenvalues.

    Compares the shape of point distributions by comparing
    eigenvalue spectra of their covariance matrices.

    Args:
        points_a: Nx3 array of points
        points_b: Mx3 array of points

    Returns:
        Spectral loss (lower is better, 0 = identical shape)
    """
    # Center the points
    centered_a = points_a - np.mean(points_a, axis=0)
    centered_b = points_b - np.mean(points_b, axis=0)

    # Compute covariance matrices
    cov_a = np.cov(centered_a.T)
    cov_b = np.cov(centered_b.T)

    # Compute eigenvalues (sorted in descending order)
    eigenvalues_a = np.sort(np.linalg.eigvalsh(cov_a))[::-1]
    eigenvalues_b = np.sort(np.linalg.eigvalsh(cov_b))[::-1]

    # Normalize eigenvalues to sum to 1
    eigenvalues_a = eigenvalues_a / np.sum(eigenvalues_a)
    eigenvalues_b = eigenvalues_b / np.sum(eigenvalues_b)

    # Compute L2 distance between normalized spectra
    spectral_dist = np.linalg.norm(eigenvalues_a - eigenvalues_b)

    return float(spectral_dist)


def point_in_hull(points: np.ndarray, hull: ConvexHull) -> np.ndarray:
    """Check if points are inside a convex hull.

    Uses the fact that a point is inside the hull if it satisfies
    all halfspace inequalities: Ax + b <= 0 for all (A, b) in equations.

    Args:
        points: Nx3 array of query points
        hull: ConvexHull object

    Returns:
        Boolean array indicating whether each point is inside
    """
    A = hull.equations[:, :-1]
    b = hull.equations[:, -1]

    # Point is inside if A @ point + b <= 0 for all equations
    # Add small tolerance for numerical stability
    return np.all(points @ A.T + b <= 1e-12, axis=1)


def iou_loss(points_a: np.ndarray, points_b: np.ndarray,
             n_samples: int = 10000) -> float:
    """Compute IoU loss (1 - Jaccard index) via Monte Carlo sampling.

    IoU = |A ∩ B| / |A ∪ B|
    Loss = 1 - IoU

    Args:
        points_a: Nx3 array of points defining polyhedron A
        points_b: Mx3 array of points defining polyhedron B
        n_samples: Number of Monte Carlo samples

    Returns:
        IoU loss (0 = perfect overlap, 1 = no overlap)
    """
    try:
        hull_a = ConvexHull(points_a)
        hull_b = ConvexHull(points_b)
    except Exception:
        return 1.0  # If hull construction fails, return max loss

    # Combined bounding box
    all_points = np.vstack([points_a, points_b])
    min_bound = np.min(all_points, axis=0)
    max_bound = np.max(all_points, axis=0)

    # Sample uniformly in bounding box
    samples = np.random.uniform(min_bound, max_bound, size=(n_samples, 3))

    # Check which samples are in each hull
    in_a = point_in_hull(samples, hull_a)
    in_b = point_in_hull(samples, hull_b)

    # Compute intersection and union counts
    intersection = np.sum(in_a & in_b)
    union = np.sum(in_a | in_b)

    if union == 0:
        return 1.0  # No overlap possible

    iou = intersection / union
    return float(1.0 - iou)


@dataclass
class MetricResult:
    """Result of computing a metric for a family."""
    family: str
    metric: str
    value: float
    normalized: bool


def compute_all_metrics(screen_vertices: np.ndarray,
                       surface_vertices: np.ndarray) -> Dict[str, float]:
    """Compute all loss metrics between screen and surface polyhedra."""
    metrics = {}

    # Existing metrics
    metrics["centroid"] = centroid_loss(screen_vertices, surface_vertices, normalize=True)
    metrics["volume"] = volume_loss(screen_vertices, surface_vertices)
    metrics["hausdorff"] = hausdorff_loss(screen_vertices, surface_vertices, use_average=True)

    # New metrics
    metrics["chamfer"] = chamfer_distance(screen_vertices, surface_vertices, normalize=True)
    metrics["emd"] = earth_movers_distance(screen_vertices, surface_vertices, normalize=True)
    metrics["spectral"] = spectral_loss(screen_vertices, surface_vertices)
    metrics["iou"] = iou_loss(screen_vertices, surface_vertices, n_samples=5000)

    return metrics


def run_metric_comparison():
    """Run comparison of all metrics across families."""
    print("Phase 5.1: Alternative Loss Metrics Comparison")
    print("=" * 70)

    # Load families
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    # Compute all metrics for each family
    results: Dict[str, Dict[str, float]] = {}

    for family, (screen_vertices, surface_vertices) in families_data.items():
        print(f"\n{family}:")

        try:
            metrics = compute_all_metrics(screen_vertices, surface_vertices)
            results[family] = metrics

            print(f"  centroid: {metrics['centroid']:.4f}, volume: {metrics['volume']:.4f}, "
                  f"hausdorff: {metrics['hausdorff']:.4f}")
            print(f"  chamfer: {metrics['chamfer']:.4f}, emd: {metrics['emd']:.4f}, "
                  f"spectral: {metrics['spectral']:.4f}, iou: {metrics['iou']:.4f}")

        except Exception as e:
            print(f"  Error: {e}")

    return results, families_data


def analyze_metric_correlations(results: Dict[str, Dict[str, float]]) -> Dict:
    """Analyze correlations between different metrics."""
    if not results:
        return {}

    # Extract metric arrays
    metrics_list = list(next(iter(results.values())).keys())
    n_families = len(results)

    metric_arrays = {m: np.zeros(n_families) for m in metrics_list}
    for i, (family, metrics) in enumerate(results.items()):
        for m, v in metrics.items():
            metric_arrays[m][i] = v

    # Compute correlation matrix
    n_metrics = len(metrics_list)
    corr_matrix = np.zeros((n_metrics, n_metrics))

    for i, m1 in enumerate(metrics_list):
        for j, m2 in enumerate(metrics_list):
            corr_matrix[i, j] = np.corrcoef(metric_arrays[m1], metric_arrays[m2])[0, 1]

    # Statistics per metric
    stats = {}
    for m in metrics_list:
        arr = metric_arrays[m]
        stats[m] = {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
        }

    return {
        "metrics": metrics_list,
        "correlation_matrix": corr_matrix.tolist(),
        "statistics": stats
    }


def generate_report(results: Dict[str, Dict[str, float]],
                   analysis: Dict) -> str:
    """Generate comparison report."""
    report = []
    report.append("# Alternative Loss Metrics Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Families analyzed: {len(results)}")
    report.append("")

    # Metric descriptions
    report.append("## Metric Definitions")
    report.append("")
    report.append("| Metric | Description | Range |")
    report.append("|--------|-------------|-------|")
    report.append("| centroid | Normalized centroid distance | [0, ∞) |")
    report.append("| volume | Volume ratio deviation |V_s/V_t - 1| | [0, ∞) |")
    report.append("| hausdorff | Normalized average Hausdorff distance | [0, 1] |")
    report.append("| chamfer | Normalized symmetric Chamfer distance | [0, 1] |")
    report.append("| emd | Normalized Earth Mover's Distance | [0, 1] |")
    report.append("| spectral | Eigenvalue spectrum L2 distance | [0, √3] |")
    report.append("| iou | 1 - Jaccard index (Monte Carlo) | [0, 1] |")
    report.append("")

    # Statistics
    if analysis.get("statistics"):
        report.append("## Metric Statistics")
        report.append("")
        report.append("| Metric | Mean | Std | Min | Max |")
        report.append("|--------|------|-----|-----|-----|")

        for m in analysis["metrics"]:
            s = analysis["statistics"][m]
            report.append(f"| {m} | {s['mean']:.4f} | {s['std']:.4f} | "
                         f"{s['min']:.4f} | {s['max']:.4f} |")

        report.append("")

    # Correlation matrix
    if analysis.get("correlation_matrix"):
        report.append("## Metric Correlations")
        report.append("")
        report.append("Pearson correlation coefficients between metrics:")
        report.append("")

        metrics = analysis["metrics"]
        header = "| | " + " | ".join(metrics) + " |"
        report.append(header)
        report.append("|" + "-|" * (len(metrics) + 1))

        for i, m1 in enumerate(metrics):
            row = f"| {m1} |"
            for j, m2 in enumerate(metrics):
                corr = analysis["correlation_matrix"][i][j]
                row += f" {corr:.2f} |"
            report.append(row)

        report.append("")

    # Per-family results
    report.append("## Per-Family Results")
    report.append("")
    report.append("| Family | Centroid | Volume | Hausdorff | Chamfer | EMD | Spectral | IoU |")
    report.append("|--------|----------|--------|-----------|---------|-----|----------|-----|")

    for family in sorted(results.keys()):
        m = results[family]
        report.append(
            f"| {family} | {m['centroid']:.4f} | {m['volume']:.4f} | "
            f"{m['hausdorff']:.4f} | {m['chamfer']:.4f} | {m['emd']:.4f} | "
            f"{m['spectral']:.4f} | {m['iou']:.4f} |"
        )

    report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    if analysis.get("correlation_matrix") and analysis.get("metrics"):
        metrics = analysis["metrics"]
        corr = np.array(analysis["correlation_matrix"])

        # Find highly correlated pairs
        report.append("### Highly Correlated Metrics (|r| > 0.7)")
        report.append("")

        found_high_corr = False
        for i in range(len(metrics)):
            for j in range(i + 1, len(metrics)):
                if abs(corr[i, j]) > 0.7:
                    found_high_corr = True
                    report.append(f"- {metrics[i]} ↔ {metrics[j]}: r = {corr[i, j]:.2f}")

        if not found_high_corr:
            report.append("- No pairs with |r| > 0.7 found")

        report.append("")

        # Find low correlation with combined loss proxy
        report.append("### Metric Independence")
        report.append("")
        report.append("Metrics with low correlation to centroid (potentially capturing different aspects):")
        report.append("")

        centroid_idx = metrics.index("centroid") if "centroid" in metrics else 0
        for i, m in enumerate(metrics):
            if i != centroid_idx and abs(corr[centroid_idx, i]) < 0.5:
                report.append(f"- {m}: r = {corr[centroid_idx, i]:.2f}")

        report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. **Primary metrics**: volume + hausdorff (established, interpretable)")
    report.append("2. **Alternative for shape**: chamfer distance (efficient, robust)")
    report.append("3. **For distribution comparison**: EMD (captures spread differences)")
    report.append("4. **For overlap assessment**: IoU (intuitive, but Monte Carlo variance)")
    report.append("5. **For covariance shape**: spectral loss (captures orientation/spread)")
    report.append("")

    return "\n".join(report)


def main():
    """Run alternative loss metrics comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set random seed for reproducibility (IoU uses Monte Carlo)
    np.random.seed(42)

    # Initialize experiment logger
    logger = ExperimentLogger()

    # Run comparison
    results, families_data = run_metric_comparison()

    # Analyze correlations
    analysis = analyze_metric_correlations(results)

    # Register experiment
    exp_id = logger.register_experiment(
        name="Alternative Loss Metrics Comparison",
        method="metric_comparison",
        domain="munsell_cartesian",
        loss_function="multiple",
        parameters={
            "metrics": ["centroid", "volume", "hausdorff", "chamfer", "emd", "spectral", "iou"],
            "iou_samples": 5000,
            "normalized": True
        },
        tags=["metrics", "phase5.1", "comparison"]
    )

    # Log results
    logger.log_result(exp_id, {
        "per_family_metrics": results,
        "correlation_analysis": analysis
    })

    # Log key observation
    if analysis.get("statistics"):
        chamfer_mean = analysis["statistics"]["chamfer"]["mean"]
        hausdorff_mean = analysis["statistics"]["hausdorff"]["mean"]
        logger.log_observation(
            exp_id,
            f"Chamfer distance (mean={chamfer_mean:.4f}) vs Hausdorff (mean={hausdorff_mean:.4f})"
        )

    # Save results
    results_file = output_dir / "alternative_metrics.json"
    with open(results_file, "w") as f:
        json.dump({
            "per_family": results,
            "analysis": analysis
        }, f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, analysis)
    report_file = output_dir / "alternative_metrics.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")

    # Summary
    print("\n" + "=" * 70)
    print("METRIC COMPARISON SUMMARY")
    print("=" * 70)

    if analysis.get("statistics"):
        print("\nMean values across families:")
        for m in analysis["metrics"]:
            print(f"  {m}: {analysis['statistics'][m]['mean']:.4f}")


if __name__ == "__main__":
    main()
