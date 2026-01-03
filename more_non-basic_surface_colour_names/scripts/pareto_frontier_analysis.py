#!/usr/bin/env python3
"""
Phase 5.1: Pareto Frontier Analysis for Loss Component Trade-offs

Explores the weight space to find Pareto-optimal solutions:
- Samples weight combinations (w_centroid, w_volume, w_shape)
- Identifies non-dominated solutions
- Visualizes the trade-off frontier
- Recommends optimal weight configurations

Key concepts:
- Pareto optimal: No other solution is better in all objectives
- Pareto frontier: Set of all Pareto optimal solutions
- Trade-off: Improving one objective necessarily worsens another
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, field
from scipy.optimize import minimize
from datetime import datetime, timezone
import warnings
import itertools

from loss_functions import (
    centroid_loss, volume_loss, hausdorff_loss, load_polyhedron
)
from linear_transformations import (
    TranslationScalingTransform, load_matched_families
)
from experiment_logger import ExperimentLogger

BASE_DIR = Path(__file__).parent.parent


@dataclass
class WeightedOptResult:
    """Result of weighted optimization at a specific weight configuration."""
    weights: Tuple[float, float, float]  # (centroid, volume, shape)
    mean_combined_loss: float
    mean_centroid: float
    mean_volume: float
    mean_shape: float
    n_families: int
    is_pareto_optimal: bool = False


@dataclass
class ParetoPoint:
    """A point on the Pareto frontier."""
    weights: Tuple[float, float, float]
    objectives: Tuple[float, float, float]  # (centroid, volume, shape)
    combined_loss: float
    dominated_by: List[int] = field(default_factory=list)


def compute_all_components(screen_vertices: np.ndarray,
                          surface_vertices: np.ndarray) -> Dict[str, float]:
    """Compute all three loss components."""
    return {
        "centroid": centroid_loss(screen_vertices, surface_vertices, normalize=True),
        "volume": volume_loss(screen_vertices, surface_vertices),
        "shape": hausdorff_loss(screen_vertices, surface_vertices, use_average=True)
    }


def weighted_loss(components: Dict[str, float],
                  weights: Tuple[float, float, float]) -> float:
    """Compute weighted loss from components."""
    return (weights[0] * components["centroid"] +
            weights[1] * components["volume"] +
            weights[2] * components["shape"])


def optimize_with_weights(transform_class,
                         screen_vertices: np.ndarray,
                         surface_vertices: np.ndarray,
                         weights: Tuple[float, float, float],
                         max_iter: int = 50) -> Dict[str, float]:
    """Optimize transformation with specific weights.

    Returns dict with centroid, volume, shape, and combined loss at optimal.
    """
    w_c, w_v, w_s = weights

    # Get initial parameters
    x0 = transform_class.get_initial_params(screen_vertices, surface_vertices)

    # Define objective function
    def objective(params):
        transformed = transform_class.apply(screen_vertices, params)
        try:
            c = centroid_loss(transformed, surface_vertices, normalize=True)
            v = volume_loss(transformed, surface_vertices)
            s = hausdorff_loss(transformed, surface_vertices, use_average=True)
            return w_c * c + w_v * v + w_s * s
        except Exception:
            return 1e6

    # Optimize
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = minimize(
            objective,
            x0,
            method='L-BFGS-B',
            options={'maxiter': max_iter, 'disp': False}
        )

    # Compute all components at optimal
    final_transformed = transform_class.apply(screen_vertices, result.x)
    components = compute_all_components(final_transformed, surface_vertices)
    components["combined"] = weighted_loss(components, weights)

    return components


def generate_weight_grid(n_steps: int = 11) -> List[Tuple[float, float, float]]:
    """Generate grid of weight combinations that sum to 1.

    Uses barycentric coordinates on simplex.
    """
    weights = []
    step = 1.0 / (n_steps - 1)

    for i in range(n_steps):
        for j in range(n_steps - i):
            w_c = i * step
            w_v = j * step
            w_s = 1.0 - w_c - w_v
            if w_s >= -1e-10:  # Allow small numerical error
                w_s = max(0, w_s)
                weights.append((w_c, w_v, w_s))

    return weights


def is_dominated(point: Tuple[float, float, float],
                 other: Tuple[float, float, float]) -> bool:
    """Check if point is dominated by other.

    A point is dominated if other is <= in all objectives and < in at least one.
    (Lower is better for all loss components.)
    """
    all_leq = all(o <= p for o, p in zip(other, point))
    some_lt = any(o < p for o, p in zip(other, point))
    return all_leq and some_lt


def find_pareto_frontier(results: List[WeightedOptResult]) -> List[WeightedOptResult]:
    """Find Pareto-optimal solutions from all results.

    A solution is Pareto-optimal if no other solution dominates it
    (i.e., is better in all objectives).
    """
    pareto_optimal = []

    for i, r1 in enumerate(results):
        obj1 = (r1.mean_centroid, r1.mean_volume, r1.mean_shape)

        dominated = False
        for j, r2 in enumerate(results):
            if i == j:
                continue
            obj2 = (r2.mean_centroid, r2.mean_volume, r2.mean_shape)

            if is_dominated(obj1, obj2):
                dominated = True
                break

        if not dominated:
            r1.is_pareto_optimal = True
            pareto_optimal.append(r1)

    return pareto_optimal


def run_pareto_analysis(n_weight_steps: int = 6):
    """Run Pareto frontier analysis across weight space."""
    print("Phase 5.1: Pareto Frontier Analysis")
    print("=" * 70)

    # Load families
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    # Generate weight grid
    weight_configs = generate_weight_grid(n_weight_steps)
    print(f"Testing {len(weight_configs)} weight configurations")

    results: List[WeightedOptResult] = []

    for idx, weights in enumerate(weight_configs):
        if idx % 10 == 0:
            print(f"  Progress: {idx}/{len(weight_configs)} ({100*idx/len(weight_configs):.0f}%)")

        # Optimize each family with these weights
        family_results = []
        for family, (screen_vertices, surface_vertices) in families_data.items():
            try:
                components = optimize_with_weights(
                    TranslationScalingTransform,
                    screen_vertices,
                    surface_vertices,
                    weights
                )
                family_results.append(components)
            except Exception:
                pass

        if family_results:
            # Aggregate across families
            mean_centroid = np.mean([r["centroid"] for r in family_results])
            mean_volume = np.mean([r["volume"] for r in family_results])
            mean_shape = np.mean([r["shape"] for r in family_results])
            mean_combined = np.mean([r["combined"] for r in family_results])

            results.append(WeightedOptResult(
                weights=weights,
                mean_combined_loss=float(mean_combined),
                mean_centroid=float(mean_centroid),
                mean_volume=float(mean_volume),
                mean_shape=float(mean_shape),
                n_families=len(family_results)
            ))

    print(f"Completed optimization for {len(results)} weight configurations")

    # Find Pareto frontier
    pareto_optimal = find_pareto_frontier(results)
    print(f"Found {len(pareto_optimal)} Pareto-optimal solutions")

    return results, pareto_optimal, families_data


def analyze_pareto_frontier(pareto_optimal: List[WeightedOptResult]) -> Dict:
    """Analyze the Pareto frontier characteristics."""
    if not pareto_optimal:
        return {}

    # Find extreme points
    best_centroid = min(pareto_optimal, key=lambda r: r.mean_centroid)
    best_volume = min(pareto_optimal, key=lambda r: r.mean_volume)
    best_shape = min(pareto_optimal, key=lambda r: r.mean_shape)
    best_combined = min(pareto_optimal, key=lambda r: r.mean_combined_loss)

    # Analyze weight distribution on frontier
    frontier_weights = [r.weights for r in pareto_optimal]
    avg_w_centroid = np.mean([w[0] for w in frontier_weights])
    avg_w_volume = np.mean([w[1] for w in frontier_weights])
    avg_w_shape = np.mean([w[2] for w in frontier_weights])

    analysis = {
        "n_pareto_points": len(pareto_optimal),
        "extreme_points": {
            "best_centroid": {
                "weights": best_centroid.weights,
                "centroid": best_centroid.mean_centroid,
                "volume": best_centroid.mean_volume,
                "shape": best_centroid.mean_shape,
            },
            "best_volume": {
                "weights": best_volume.weights,
                "centroid": best_volume.mean_centroid,
                "volume": best_volume.mean_volume,
                "shape": best_volume.mean_shape,
            },
            "best_shape": {
                "weights": best_shape.weights,
                "centroid": best_shape.mean_centroid,
                "volume": best_shape.mean_volume,
                "shape": best_shape.mean_shape,
            },
            "best_combined": {
                "weights": best_combined.weights,
                "combined": best_combined.mean_combined_loss,
                "centroid": best_combined.mean_centroid,
                "volume": best_combined.mean_volume,
                "shape": best_combined.mean_shape,
            }
        },
        "frontier_weight_averages": {
            "centroid": avg_w_centroid,
            "volume": avg_w_volume,
            "shape": avg_w_shape,
        },
        "trade_off_range": {
            "centroid": (min(r.mean_centroid for r in pareto_optimal),
                        max(r.mean_centroid for r in pareto_optimal)),
            "volume": (min(r.mean_volume for r in pareto_optimal),
                      max(r.mean_volume for r in pareto_optimal)),
            "shape": (min(r.mean_shape for r in pareto_optimal),
                     max(r.mean_shape for r in pareto_optimal)),
        }
    }

    return analysis


def generate_report(results: List[WeightedOptResult],
                   pareto_optimal: List[WeightedOptResult],
                   analysis: Dict) -> str:
    """Generate Pareto analysis report."""
    report = []
    report.append("# Pareto Frontier Analysis Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Weight configurations tested: {len(results)}")
    report.append(f"Pareto-optimal solutions: {len(pareto_optimal)}")
    report.append("")

    # Methodology
    report.append("## Methodology")
    report.append("")
    report.append("1. Sample weight space (w_centroid + w_volume + w_shape = 1)")
    report.append("2. Optimize transformation for each weight configuration")
    report.append("3. Identify non-dominated (Pareto-optimal) solutions")
    report.append("4. Analyze trade-offs on the frontier")
    report.append("")

    # Extreme points
    report.append("## Extreme Points on Frontier")
    report.append("")

    if analysis.get("extreme_points"):
        ep = analysis["extreme_points"]

        report.append("### Best Centroid Alignment")
        bc = ep["best_centroid"]
        report.append(f"- Weights: centroid={bc['weights'][0]:.2f}, volume={bc['weights'][1]:.2f}, shape={bc['weights'][2]:.2f}")
        report.append(f"- Centroid: {bc['centroid']:.4f}, Volume: {bc['volume']:.4f}, Shape: {bc['shape']:.4f}")
        report.append("")

        report.append("### Best Volume Matching")
        bv = ep["best_volume"]
        report.append(f"- Weights: centroid={bv['weights'][0]:.2f}, volume={bv['weights'][1]:.2f}, shape={bv['weights'][2]:.2f}")
        report.append(f"- Centroid: {bv['centroid']:.4f}, Volume: {bv['volume']:.4f}, Shape: {bv['shape']:.4f}")
        report.append("")

        report.append("### Best Shape Preservation")
        bs = ep["best_shape"]
        report.append(f"- Weights: centroid={bs['weights'][0]:.2f}, volume={bs['weights'][1]:.2f}, shape={bs['weights'][2]:.2f}")
        report.append(f"- Centroid: {bs['centroid']:.4f}, Volume: {bs['volume']:.4f}, Shape: {bs['shape']:.4f}")
        report.append("")

        report.append("### Best Combined Loss")
        bcom = ep["best_combined"]
        report.append(f"- Weights: centroid={bcom['weights'][0]:.2f}, volume={bcom['weights'][1]:.2f}, shape={bcom['weights'][2]:.2f}")
        report.append(f"- Combined: {bcom['combined']:.4f}")
        report.append(f"- Centroid: {bcom['centroid']:.4f}, Volume: {bcom['volume']:.4f}, Shape: {bcom['shape']:.4f}")
        report.append("")

    # Trade-off ranges
    report.append("## Trade-off Ranges")
    report.append("")
    if analysis.get("trade_off_range"):
        tr = analysis["trade_off_range"]
        report.append("| Component | Min | Max | Range |")
        report.append("|-----------|-----|-----|-------|")
        for comp in ["centroid", "volume", "shape"]:
            min_v, max_v = tr[comp]
            report.append(f"| {comp} | {min_v:.4f} | {max_v:.4f} | {max_v - min_v:.4f} |")
        report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    if analysis.get("extreme_points"):
        ep = analysis["extreme_points"]

        # Check if volume dominates
        bv = ep["best_volume"]
        bc = ep["best_centroid"]
        bs = ep["best_shape"]

        if bv["volume"] < 0.01 and bv["centroid"] < 0.1:
            report.append("1. **Volume-focused weights achieve near-zero volume error with acceptable centroid**")

        if bs["shape"] - bv["shape"] < 0.1:
            report.append("2. **Shape preservation varies little across the frontier** - shape may be inherently limited")

        # Check frontier weight distribution
        if analysis.get("frontier_weight_averages"):
            fw = analysis["frontier_weight_averages"]
            dominant = max(fw.items(), key=lambda x: x[1])
            report.append(f"3. **Average Pareto weight for {dominant[0]}: {dominant[1]:.2f}** - suggests importance")

    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. For best combined performance, use weights near the 'Best Combined' point")
    report.append("2. For applications prioritizing volume accuracy, increase volume weight")
    report.append("3. The Pareto frontier reveals inherent trade-offs that cannot be eliminated")
    report.append("")

    # Full Pareto frontier table
    report.append("## Pareto Frontier Points")
    report.append("")
    report.append("| w_c | w_v | w_s | Centroid | Volume | Shape | Combined |")
    report.append("|-----|-----|-----|----------|--------|-------|----------|")

    for r in sorted(pareto_optimal, key=lambda x: x.mean_combined_loss):
        report.append(
            f"| {r.weights[0]:.2f} | {r.weights[1]:.2f} | {r.weights[2]:.2f} | "
            f"{r.mean_centroid:.4f} | {r.mean_volume:.4f} | {r.mean_shape:.4f} | "
            f"{r.mean_combined_loss:.4f} |"
        )

    report.append("")

    return "\n".join(report)


def main():
    """Run Pareto frontier analysis."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize experiment logger
    logger = ExperimentLogger()

    # Run analysis with 6-step grid (21 weight configs)
    results, pareto_optimal, families_data = run_pareto_analysis(n_weight_steps=6)

    # Analyze frontier
    analysis = analyze_pareto_frontier(pareto_optimal)

    # Register experiment
    exp_id = logger.register_experiment(
        name="Pareto Frontier Analysis",
        method="translation_scaling",
        domain="munsell_cartesian",
        loss_function="variable_weighted",
        parameters={
            "n_params": 6,
            "weight_steps": 6,
            "n_weight_configs": len(results),
            "optimization": "L-BFGS-B"
        },
        tags=["pareto", "phase5.1", "multi_objective"]
    )

    # Log results
    logger.log_result(exp_id, {
        "n_pareto_optimal": len(pareto_optimal),
        "extreme_points": analysis.get("extreme_points", {}),
        "trade_off_ranges": analysis.get("trade_off_range", {}),
        "frontier_weights": [asdict(r) for r in pareto_optimal]
    })

    # Log key observation
    if analysis.get("extreme_points"):
        best_combined = analysis["extreme_points"]["best_combined"]
        logger.log_observation(
            exp_id,
            f"Best combined loss {best_combined['combined']:.4f} at weights "
            f"({best_combined['weights'][0]:.2f}, {best_combined['weights'][1]:.2f}, {best_combined['weights'][2]:.2f})"
        )

    # Save detailed results
    results_file = output_dir / "pareto_analysis.json"
    results_data = {
        "all_results": [asdict(r) for r in results],
        "pareto_optimal": [asdict(r) for r in pareto_optimal],
        "analysis": analysis
    }

    with open(results_file, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, pareto_optimal, analysis)
    report_file = output_dir / "pareto_analysis.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")

    # Print summary
    print("\n" + "=" * 70)
    print("PARETO FRONTIER SUMMARY")
    print("=" * 70)

    print(f"\nWeight configurations tested: {len(results)}")
    print(f"Pareto-optimal solutions: {len(pareto_optimal)}")

    if analysis.get("extreme_points"):
        ep = analysis["extreme_points"]
        print("\nExtreme points:")
        print(f"  Best centroid: {ep['best_centroid']['centroid']:.4f} at weights {ep['best_centroid']['weights']}")
        print(f"  Best volume: {ep['best_volume']['volume']:.4f} at weights {ep['best_volume']['weights']}")
        print(f"  Best shape: {ep['best_shape']['shape']:.4f} at weights {ep['best_shape']['weights']}")
        print(f"  Best combined: {ep['best_combined']['combined']:.4f} at weights {ep['best_combined']['weights']}")


if __name__ == "__main__":
    main()
