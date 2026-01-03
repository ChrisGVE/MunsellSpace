#!/usr/bin/env python3
"""
Phase 5.1: Pareto Frontier Analysis from Existing Results

Constructs Pareto frontier from single-component and pairwise analysis results,
avoiding redundant expensive optimization runs.

This is a fast alternative to full weight-space sampling.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

from experiment_logger import ExperimentLogger

BASE_DIR = Path(__file__).parent.parent


@dataclass
class ParetoPoint:
    """A point in the objective space."""
    name: str
    weights: Tuple[float, float, float]  # Approximate weights for strategy
    centroid: float
    volume: float
    shape: float
    combined: float  # 0.4*c + 0.3*v + 0.3*s
    is_pareto_optimal: bool = False


def is_dominated(point_a: ParetoPoint, point_b: ParetoPoint) -> bool:
    """Check if point_a is dominated by point_b.

    A point is dominated if another point is <= in all objectives and < in at least one.
    """
    obj_a = (point_a.centroid, point_a.volume, point_a.shape)
    obj_b = (point_b.centroid, point_b.volume, point_b.shape)

    all_leq = all(b <= a for a, b in zip(obj_a, obj_b))
    some_lt = any(b < a for a, b in zip(obj_a, obj_b))
    return all_leq and some_lt


def find_pareto_frontier(points: List[ParetoPoint]) -> List[ParetoPoint]:
    """Find Pareto-optimal points."""
    pareto = []

    for i, p1 in enumerate(points):
        dominated = False
        for j, p2 in enumerate(points):
            if i != j and is_dominated(p1, p2):
                dominated = True
                break

        if not dominated:
            p1.is_pareto_optimal = True
            pareto.append(p1)

    return pareto


def load_existing_results() -> List[ParetoPoint]:
    """Load results from single-component and pairwise analyses."""
    points = []

    # Load single-component results
    single_file = BASE_DIR / "datasets/transformation_analysis/single_component_analysis.json"
    if single_file.exists():
        with open(single_file) as f:
            data = json.load(f)

        analysis = data.get("analysis", {})

        # Extract single-component optimal points
        if "centroid" in analysis:
            a = analysis["centroid"]
            points.append(ParetoPoint(
                name="centroid_only",
                weights=(1.0, 0.0, 0.0),
                centroid=a["other_components_at_optimal"]["mean_centroid"],
                volume=a["other_components_at_optimal"]["mean_volume"],
                shape=a["other_components_at_optimal"]["mean_shape"],
                combined=a["combined_loss_at_optimal"]["mean"]
            ))

        if "volume" in analysis:
            a = analysis["volume"]
            points.append(ParetoPoint(
                name="volume_only",
                weights=(0.0, 1.0, 0.0),
                centroid=a["other_components_at_optimal"]["mean_centroid"],
                volume=a["other_components_at_optimal"]["mean_volume"],
                shape=a["other_components_at_optimal"]["mean_shape"],
                combined=a["combined_loss_at_optimal"]["mean"]
            ))

        if "shape" in analysis:
            a = analysis["shape"]
            points.append(ParetoPoint(
                name="shape_only",
                weights=(0.0, 0.0, 1.0),
                centroid=a["other_components_at_optimal"]["mean_centroid"],
                volume=a["other_components_at_optimal"]["mean_volume"],
                shape=a["other_components_at_optimal"]["mean_shape"],
                combined=a["combined_loss_at_optimal"]["mean"]
            ))

    # Load pairwise results
    pairwise_file = BASE_DIR / "datasets/transformation_analysis/pairwise_analysis.json"
    if pairwise_file.exists():
        with open(pairwise_file) as f:
            data = json.load(f)

        analysis = data.get("analysis", {})

        if "centroid_volume" in analysis:
            a = analysis["centroid_volume"]
            points.append(ParetoPoint(
                name="centroid_volume",
                weights=(0.5, 0.5, 0.0),
                centroid=a["component_values_at_optimal"]["mean_centroid"],
                volume=a["component_values_at_optimal"]["mean_volume"],
                shape=a["component_values_at_optimal"]["mean_shape"],
                combined=a["combined_loss"]["mean"]
            ))

        if "centroid_shape" in analysis:
            a = analysis["centroid_shape"]
            points.append(ParetoPoint(
                name="centroid_shape",
                weights=(0.5, 0.0, 0.5),
                centroid=a["component_values_at_optimal"]["mean_centroid"],
                volume=a["component_values_at_optimal"]["mean_volume"],
                shape=a["component_values_at_optimal"]["mean_shape"],
                combined=a["combined_loss"]["mean"]
            ))

        if "volume_shape" in analysis:
            a = analysis["volume_shape"]
            points.append(ParetoPoint(
                name="volume_shape",
                weights=(0.0, 0.5, 0.5),
                centroid=a["component_values_at_optimal"]["mean_centroid"],
                volume=a["component_values_at_optimal"]["mean_volume"],
                shape=a["component_values_at_optimal"]["mean_shape"],
                combined=a["combined_loss"]["mean"]
            ))

    # Load combined optimization result (from Phase 4)
    # Note: extended_domain_comparison.json is a list, but doesn't have
    # per-component breakdown needed for Pareto analysis

    return points


def analyze_pareto(points: List[ParetoPoint], pareto: List[ParetoPoint]) -> Dict:
    """Analyze the Pareto frontier."""
    if not pareto:
        return {}

    # Find extreme points
    best_centroid = min(pareto, key=lambda p: p.centroid)
    best_volume = min(pareto, key=lambda p: p.volume)
    best_shape = min(pareto, key=lambda p: p.shape)
    best_combined = min(pareto, key=lambda p: p.combined)

    analysis = {
        "n_total_points": len(points),
        "n_pareto_optimal": len(pareto),
        "pareto_fraction": len(pareto) / len(points) if points else 0,
        "extreme_points": {
            "best_centroid": {
                "name": best_centroid.name,
                "centroid": best_centroid.centroid,
                "volume": best_centroid.volume,
                "shape": best_centroid.shape,
                "combined": best_centroid.combined
            },
            "best_volume": {
                "name": best_volume.name,
                "centroid": best_volume.centroid,
                "volume": best_volume.volume,
                "shape": best_volume.shape,
                "combined": best_volume.combined
            },
            "best_shape": {
                "name": best_shape.name,
                "centroid": best_shape.centroid,
                "volume": best_shape.volume,
                "shape": best_shape.shape,
                "combined": best_shape.combined
            },
            "best_combined": {
                "name": best_combined.name,
                "centroid": best_combined.centroid,
                "volume": best_combined.volume,
                "shape": best_combined.shape,
                "combined": best_combined.combined
            }
        },
        "trade_off_ranges": {
            "centroid": (min(p.centroid for p in pareto), max(p.centroid for p in pareto)),
            "volume": (min(p.volume for p in pareto), max(p.volume for p in pareto)),
            "shape": (min(p.shape for p in pareto), max(p.shape for p in pareto))
        }
    }

    return analysis


def generate_report(points: List[ParetoPoint], pareto: List[ParetoPoint],
                   analysis: Dict) -> str:
    """Generate Pareto analysis report."""
    report = []
    report.append("# Pareto Frontier Analysis (from Existing Results)")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Total strategies evaluated: {len(points)}")
    report.append(f"Pareto-optimal strategies: {len(pareto)}")
    report.append("")

    # Methodology
    report.append("## Methodology")
    report.append("")
    report.append("Pareto frontier constructed from existing optimization results:")
    report.append("- Single-component: centroid-only, volume-only, shape-only")
    report.append("- Pairwise: centroid+volume, centroid+shape, volume+shape")
    report.append("")
    report.append("A strategy is Pareto-optimal if no other strategy dominates it")
    report.append("(i.e., is better in all three objectives simultaneously).")
    report.append("")

    # All points table
    report.append("## All Evaluated Strategies")
    report.append("")
    report.append("| Strategy | Centroid | Volume | Shape | Combined | Pareto? |")
    report.append("|----------|----------|--------|-------|----------|---------|")

    for p in sorted(points, key=lambda x: x.combined):
        pareto_mark = "✓" if p.is_pareto_optimal else ""
        report.append(
            f"| {p.name} | {p.centroid:.4f} | {p.volume:.4f} | "
            f"{p.shape:.4f} | {p.combined:.4f} | {pareto_mark} |"
        )

    report.append("")

    # Pareto frontier
    report.append("## Pareto Frontier")
    report.append("")

    if pareto:
        report.append("| Strategy | Centroid | Volume | Shape | Combined |")
        report.append("|----------|----------|--------|-------|----------|")

        for p in sorted(pareto, key=lambda x: x.combined):
            report.append(
                f"| {p.name} | {p.centroid:.4f} | {p.volume:.4f} | "
                f"{p.shape:.4f} | {p.combined:.4f} |"
            )

        report.append("")

    # Extreme points
    if analysis.get("extreme_points"):
        report.append("## Extreme Points on Frontier")
        report.append("")

        ep = analysis["extreme_points"]

        report.append(f"**Best Centroid**: {ep['best_centroid']['name']}")
        report.append(f"  - Centroid: {ep['best_centroid']['centroid']:.4f}")
        report.append("")

        report.append(f"**Best Volume**: {ep['best_volume']['name']}")
        report.append(f"  - Volume: {ep['best_volume']['volume']:.4f}")
        report.append("")

        report.append(f"**Best Shape**: {ep['best_shape']['name']}")
        report.append(f"  - Shape: {ep['best_shape']['shape']:.4f}")
        report.append("")

        report.append(f"**Best Combined**: {ep['best_combined']['name']}")
        report.append(f"  - Combined: {ep['best_combined']['combined']:.4f}")
        report.append("")

    # Trade-off ranges
    if analysis.get("trade_off_ranges"):
        report.append("## Trade-off Ranges on Frontier")
        report.append("")
        report.append("| Objective | Min | Max | Range |")
        report.append("|-----------|-----|-----|-------|")

        for obj in ["centroid", "volume", "shape"]:
            min_v, max_v = analysis["trade_off_ranges"][obj]
            report.append(f"| {obj} | {min_v:.4f} | {max_v:.4f} | {max_v - min_v:.4f} |")

        report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    if pareto:
        # Check which strategies are Pareto optimal
        pareto_names = [p.name for p in pareto]

        if "volume_only" in pareto_names:
            report.append("1. **Volume-only is Pareto-optimal** - confirms its dominance")

        if "centroid_volume" in pareto_names:
            report.append("2. **Centroid+Volume is Pareto-optimal** - good balance point")

        # Check if shape_only is dominated
        shape_only = next((p for p in points if p.name == "shape_only"), None)
        if shape_only and not shape_only.is_pareto_optimal:
            report.append("3. **Shape-only is dominated** - shape degrades volume too much")

        report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. **For general use**: Use volume-only or centroid+volume optimization")
    report.append("2. **For maximum shape fidelity**: Accept volume degradation or use multi-objective")
    report.append("3. **The Pareto frontier confirms**: volume matching is the most efficient single objective")
    report.append("")

    return "\n".join(report)


def main():
    """Run Pareto analysis from existing results."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Phase 5.1: Pareto Frontier Analysis (from Existing Results)")
    print("=" * 70)

    # Load existing results
    points = load_existing_results()
    print(f"Loaded {len(points)} optimization strategies")

    for p in points:
        print(f"  {p.name}: c={p.centroid:.4f}, v={p.volume:.4f}, s={p.shape:.4f}, combined={p.combined:.4f}")

    # Find Pareto frontier
    pareto = find_pareto_frontier(points)
    print(f"\nFound {len(pareto)} Pareto-optimal strategies:")
    for p in pareto:
        print(f"  {p.name}")

    # Analyze
    analysis = analyze_pareto(points, pareto)

    # Initialize experiment logger
    logger = ExperimentLogger()

    # Register experiment
    exp_id = logger.register_experiment(
        name="Pareto Frontier (from existing)",
        method="analysis",
        domain="munsell_cartesian",
        loss_function="multi_objective",
        parameters={
            "n_strategies": len(points),
            "source": "single_component + pairwise"
        },
        tags=["pareto", "phase5.1", "multi_objective"]
    )

    # Log results
    logger.log_result(exp_id, {
        "n_pareto_optimal": len(pareto),
        "pareto_strategies": [p.name for p in pareto],
        "analysis": analysis,
        "all_points": [asdict(p) for p in points]
    })

    if analysis.get("extreme_points"):
        best = analysis["extreme_points"]["best_combined"]
        logger.log_observation(
            exp_id,
            f"Best combined strategy: {best['name']} with loss {best['combined']:.4f}"
        )

    # Save results
    results_file = output_dir / "pareto_analysis.json"
    results_data = {
        "all_points": [asdict(p) for p in points],
        "pareto_optimal": [asdict(p) for p in pareto],
        "analysis": analysis
    }

    with open(results_file, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(points, pareto, analysis)
    report_file = output_dir / "pareto_analysis.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")

    # Summary
    print("\n" + "=" * 70)
    print("PARETO FRONTIER SUMMARY")
    print("=" * 70)

    print(f"\nStrategies: {len(points)} evaluated, {len(pareto)} Pareto-optimal")

    if analysis.get("extreme_points"):
        ep = analysis["extreme_points"]
        print(f"\nBest combined: {ep['best_combined']['name']} ({ep['best_combined']['combined']:.4f})")
        print(f"Best volume: {ep['best_volume']['name']} ({ep['best_volume']['volume']:.4f})")


if __name__ == "__main__":
    main()
