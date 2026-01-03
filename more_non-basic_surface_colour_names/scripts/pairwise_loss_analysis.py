#!/usr/bin/env python3
"""
Phase 5.1: Pairwise Loss Component Trade-off Analysis

Optimize transformations using pairs of loss components:
- Centroid + Volume (shape free)
- Centroid + Shape (volume free)
- Volume + Shape (centroid free)

Compares against:
- Single-component results (from loss_component_analysis.py)
- Combined loss (all three components)

Outputs trade-off analysis and Pareto-relevant insights.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from scipy.optimize import minimize
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


@dataclass
class PairwiseOptResult:
    """Result of pairwise component optimization."""
    family: str
    pair: str  # "centroid_volume", "centroid_shape", "volume_shape"
    weight_1: float
    weight_2: float
    initial_combined: float
    final_combined: float
    improvement: float
    # Individual component values at optimal point
    centroid_at_optimal: float
    volume_at_optimal: float
    shape_at_optimal: float
    # Pairwise loss (what was optimized)
    pairwise_loss: float
    params: List[float]
    n_iterations: int
    success: bool


class PairwiseLoss:
    """Loss function for pairwise component optimization."""

    PAIRS = {
        "centroid_volume": ("centroid", "volume"),
        "centroid_shape": ("centroid", "shape"),
        "volume_shape": ("volume", "shape"),
    }

    def __init__(self, pair: str, weight_1: float = 0.5, weight_2: float = 0.5):
        """Initialize with pair name and weights.

        Args:
            pair: One of "centroid_volume", "centroid_shape", "volume_shape"
            weight_1: Weight for first component
            weight_2: Weight for second component
        """
        if pair not in self.PAIRS:
            raise ValueError(f"Unknown pair: {pair}. Must be one of {list(self.PAIRS.keys())}")

        self.pair = pair
        self.components = self.PAIRS[pair]
        self.weight_1 = weight_1
        self.weight_2 = weight_2

        # Set up loss functions
        self._loss_fns = {
            "centroid": lambda s, t: centroid_loss(s, t, normalize=True),
            "volume": volume_loss,
            "shape": lambda s, t: hausdorff_loss(s, t, use_average=True),
        }

    def __call__(self, screen_vertices: np.ndarray,
                 surface_vertices: np.ndarray) -> float:
        """Compute pairwise loss."""
        c1, c2 = self.components
        loss_1 = self._loss_fns[c1](screen_vertices, surface_vertices)
        loss_2 = self._loss_fns[c2](screen_vertices, surface_vertices)
        return self.weight_1 * loss_1 + self.weight_2 * loss_2

    def get_excluded_component(self) -> str:
        """Get the component not included in this pair."""
        all_components = {"centroid", "volume", "shape"}
        return (all_components - set(self.components)).pop()


def compute_all_components(screen_vertices: np.ndarray,
                          surface_vertices: np.ndarray) -> Dict[str, float]:
    """Compute all three loss components."""
    return {
        "centroid": centroid_loss(screen_vertices, surface_vertices, normalize=True),
        "volume": volume_loss(screen_vertices, surface_vertices),
        "shape": hausdorff_loss(screen_vertices, surface_vertices, use_average=True)
    }


def compute_combined_loss(components: Dict[str, float]) -> float:
    """Compute standard combined loss with weights 0.4, 0.3, 0.3."""
    return 0.4 * components["centroid"] + 0.3 * components["volume"] + 0.3 * components["shape"]


def optimize_pairwise(transform_class,
                     screen_vertices: np.ndarray,
                     surface_vertices: np.ndarray,
                     pair: str,
                     weight_1: float = 0.5,
                     weight_2: float = 0.5,
                     max_iter: int = 100) -> PairwiseOptResult:
    """Optimize transformation for a pair of loss components.

    Args:
        transform_class: Transformation class to optimize
        screen_vertices: Source polyhedron vertices
        surface_vertices: Target polyhedron vertices
        pair: Which pair to optimize
        weight_1, weight_2: Weights for the two components
        max_iter: Maximum iterations

    Returns:
        PairwiseOptResult with optimization details
    """
    loss_fn = PairwiseLoss(pair, weight_1, weight_2)

    # Get initial parameters
    x0 = transform_class.get_initial_params(screen_vertices, surface_vertices)

    # Compute initial losses
    transformed_init = transform_class.apply(screen_vertices, x0)
    initial_components = compute_all_components(transformed_init, surface_vertices)
    initial_combined = compute_combined_loss(initial_components)

    # Define objective function
    def objective(params):
        transformed = transform_class.apply(screen_vertices, params)
        try:
            return loss_fn(transformed, surface_vertices)
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

    # Compute all components at optimal point
    final_transformed = transform_class.apply(screen_vertices, result.x)
    final_components = compute_all_components(final_transformed, surface_vertices)
    final_combined = compute_combined_loss(final_components)

    pairwise_loss = loss_fn(final_transformed, surface_vertices)
    improvement = (initial_combined - final_combined) / max(initial_combined, 1e-6)

    return PairwiseOptResult(
        family="",  # Set by caller
        pair=pair,
        weight_1=weight_1,
        weight_2=weight_2,
        initial_combined=float(initial_combined),
        final_combined=float(final_combined),
        improvement=float(improvement),
        centroid_at_optimal=float(final_components["centroid"]),
        volume_at_optimal=float(final_components["volume"]),
        shape_at_optimal=float(final_components["shape"]),
        pairwise_loss=float(pairwise_loss),
        params=result.x.tolist(),
        n_iterations=int(result.nit),
        success=bool(result.success)
    )


def run_pairwise_analysis():
    """Run pairwise optimization for all families and pairs."""
    print("Phase 5.1: Pairwise Loss Component Trade-off Analysis")
    print("=" * 70)

    # Load families
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    pairs = ["centroid_volume", "centroid_shape", "volume_shape"]
    results_by_pair: Dict[str, List[PairwiseOptResult]] = {p: [] for p in pairs}

    for family, (screen_vertices, surface_vertices) in families_data.items():
        print(f"\n{family}:")

        for pair in pairs:
            try:
                result = optimize_pairwise(
                    TranslationScalingTransform,
                    screen_vertices,
                    surface_vertices,
                    pair
                )
                result.family = family
                results_by_pair[pair].append(result)

                excluded = PairwiseLoss(pair).get_excluded_component()
                print(f"  {pair}: combined={result.final_combined:.4f}, "
                      f"{excluded}={getattr(result, f'{excluded}_at_optimal'):.4f}")

            except Exception as e:
                print(f"  {pair}: Error - {e}")

    return results_by_pair, families_data


def analyze_pairwise_tradeoffs(results: Dict[str, List[PairwiseOptResult]]) -> Dict:
    """Analyze trade-offs in pairwise optimizations."""
    analysis = {}

    for pair, pair_results in results.items():
        if not pair_results:
            continue

        loss_fn = PairwiseLoss(pair)
        excluded = loss_fn.get_excluded_component()

        # Collect stats
        final_combined = [r.final_combined for r in pair_results]
        pairwise_losses = [r.pairwise_loss for r in pair_results]
        excluded_values = [getattr(r, f"{excluded}_at_optimal") for r in pair_results]

        centroids = [r.centroid_at_optimal for r in pair_results]
        volumes = [r.volume_at_optimal for r in pair_results]
        shapes = [r.shape_at_optimal for r in pair_results]

        analysis[pair] = {
            "n_families": len(pair_results),
            "optimized_pair": loss_fn.components,
            "excluded_component": excluded,
            "combined_loss": {
                "mean": float(np.mean(final_combined)),
                "std": float(np.std(final_combined)),
                "min": float(np.min(final_combined)),
                "max": float(np.max(final_combined)),
            },
            "pairwise_loss": {
                "mean": float(np.mean(pairwise_losses)),
                "std": float(np.std(pairwise_losses)),
            },
            "excluded_component_at_optimal": {
                "mean": float(np.mean(excluded_values)),
                "std": float(np.std(excluded_values)),
                "degradation": excluded_values,  # For Pareto analysis
            },
            "component_values_at_optimal": {
                "mean_centroid": float(np.mean(centroids)),
                "mean_volume": float(np.mean(volumes)),
                "mean_shape": float(np.mean(shapes)),
            }
        }

    return analysis


def compare_with_single_component(pairwise_analysis: Dict) -> Dict:
    """Compare pairwise results with single-component results."""
    # Load single-component results if available
    single_component_file = BASE_DIR / "datasets/transformation_analysis/single_component_analysis.json"

    comparison = {}

    if single_component_file.exists():
        with open(single_component_file) as f:
            single_data = json.load(f)

        single_analysis = single_data.get("analysis", {})

        # Compare each pair to relevant single-component optimizations
        for pair, pair_analysis in pairwise_analysis.items():
            c1, c2 = PairwiseLoss(pair).components
            excluded = PairwiseLoss(pair).get_excluded_component()

            comparison[pair] = {
                "pairwise_combined_loss": pair_analysis["combined_loss"]["mean"],
            }

            # Compare to single-component optimizations
            for comp in [c1, c2]:
                if comp in single_analysis:
                    single_combined = single_analysis[comp]["combined_loss_at_optimal"]["mean"]
                    comparison[pair][f"vs_{comp}_only"] = {
                        "single_combined": single_combined,
                        "difference": pair_analysis["combined_loss"]["mean"] - single_combined,
                    }

    return comparison


def generate_report(results: Dict[str, List[PairwiseOptResult]],
                   analysis: Dict,
                   comparison: Dict,
                   families_data: Dict) -> str:
    """Generate analysis report."""
    report = []
    report.append("# Pairwise Loss Component Trade-off Analysis")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Families analyzed: {len(families_data)}")
    report.append("")

    # Method description
    report.append("## Methodology")
    report.append("")
    report.append("Pairs of loss components optimized together using Translation+Scaling (6 params):")
    report.append("")
    report.append("- **Centroid + Volume**: Shape free to vary")
    report.append("- **Centroid + Shape**: Volume free to vary")
    report.append("- **Volume + Shape**: Centroid free to vary")
    report.append("")
    report.append("Each pair uses equal weights (0.5, 0.5) in the pairwise loss.")
    report.append("")

    # Summary table
    report.append("## Summary Results")
    report.append("")
    report.append("| Pair | Mean Combined | Excluded | Excluded Value |")
    report.append("|------|---------------|----------|----------------|")

    for pair in ["centroid_volume", "centroid_shape", "volume_shape"]:
        if pair in analysis:
            a = analysis[pair]
            excluded = a["excluded_component"]
            excluded_val = a["excluded_component_at_optimal"]["mean"]
            report.append(
                f"| {pair.replace('_', '+')} | {a['combined_loss']['mean']:.4f} | "
                f"{excluded} | {excluded_val:.4f} |"
            )

    report.append("")

    # Comparison with single-component
    if comparison:
        report.append("## Comparison with Single-Component Optimization")
        report.append("")
        report.append("| Pair | Combined Loss | Best Single | Difference |")
        report.append("|------|---------------|-------------|------------|")

        for pair in ["centroid_volume", "centroid_shape", "volume_shape"]:
            if pair in comparison:
                c = comparison[pair]
                pair_loss = c["pairwise_combined_loss"]

                # Find best single-component comparison
                best_single = None
                best_name = ""
                for key in c:
                    if key.startswith("vs_") and key.endswith("_only"):
                        comp_name = key[3:-5]
                        single_loss = c[key]["single_combined"]
                        if best_single is None or single_loss < best_single:
                            best_single = single_loss
                            best_name = comp_name

                if best_single is not None:
                    diff = pair_loss - best_single
                    report.append(
                        f"| {pair.replace('_', '+')} | {pair_loss:.4f} | "
                        f"{best_name}={best_single:.4f} | {diff:+.4f} |"
                    )

        report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    # Find best pair
    best_pair = None
    best_combined = float('inf')
    for pair, pair_analysis in analysis.items():
        combined = pair_analysis["combined_loss"]["mean"]
        if combined < best_combined:
            best_combined = combined
            best_pair = pair

    report.append(f"1. **Best pairwise strategy**: {best_pair.replace('_', '+')}")
    report.append(f"   - Achieves combined loss of {best_combined:.4f}")
    report.append("")

    # Excluded component behavior
    report.append("2. **Excluded component behavior**:")
    for pair, pair_analysis in analysis.items():
        excluded = pair_analysis["excluded_component"]
        excluded_val = pair_analysis["excluded_component_at_optimal"]["mean"]
        status = "acceptable" if excluded_val < 0.3 else "degraded" if excluded_val < 0.6 else "severely degraded"
        report.append(f"   - {pair.replace('_', '+')}: {excluded} = {excluded_val:.4f} ({status})")

    report.append("")

    # Trade-off insights
    report.append("3. **Trade-off insights**:")

    # Check if volume-only still dominates
    volume_only_combined = None
    single_component_file = BASE_DIR / "datasets/transformation_analysis/single_component_analysis.json"
    if single_component_file.exists():
        with open(single_component_file) as f:
            single_data = json.load(f)
        if "analysis" in single_data and "volume" in single_data["analysis"]:
            volume_only_combined = single_data["analysis"]["volume"]["combined_loss_at_optimal"]["mean"]

    if volume_only_combined is not None:
        if best_combined < volume_only_combined:
            report.append(f"   - Pairwise optimization ({best_combined:.4f}) improves on volume-only ({volume_only_combined:.4f})")
        else:
            report.append(f"   - Volume-only ({volume_only_combined:.4f}) still outperforms best pairwise ({best_combined:.4f})")
            report.append("   - This confirms volume matching as the dominant objective")

    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. Proceed with Pareto frontier analysis to find optimal trade-off points")
    report.append("2. Consider adaptive weighting based on family characteristics")
    report.append("3. Volume matching appears critical - ensure it's prioritized in final solution")
    report.append("")

    # Per-family details
    report.append("## Per-Family Results")
    report.append("")

    for pair in ["centroid_volume", "centroid_shape", "volume_shape"]:
        if pair in results and results[pair]:
            excluded = PairwiseLoss(pair).get_excluded_component()
            report.append(f"### {pair.replace('_', ' + ').title()} (excludes {excluded})")
            report.append("")
            report.append("| Family | Combined | Centroid | Volume | Shape |")
            report.append("|--------|----------|----------|--------|-------|")

            for r in sorted(results[pair], key=lambda x: x.final_combined):
                report.append(
                    f"| {r.family} | {r.final_combined:.4f} | "
                    f"{r.centroid_at_optimal:.4f} | {r.volume_at_optimal:.4f} | "
                    f"{r.shape_at_optimal:.4f} |"
                )

            report.append("")

    return "\n".join(report)


def main():
    """Run pairwise loss trade-off analysis."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize experiment logger
    logger = ExperimentLogger()

    # Run analysis
    results, families_data = run_pairwise_analysis()

    # Analyze trade-offs
    analysis = analyze_pairwise_tradeoffs(results)

    # Compare with single-component
    comparison = compare_with_single_component(analysis)

    # Register experiments for each pair
    for pair, pair_results in results.items():
        if pair_results:
            exp_id = logger.register_experiment(
                name=f"Pairwise: {pair.replace('_', '+')}",
                method="translation_scaling",
                domain="munsell_cartesian",
                loss_function=f"{pair}_pairwise",
                parameters={"n_params": 6, "weights": [0.5, 0.5], "optimization": "L-BFGS-B"},
                tags=["pairwise", "phase5.1", pair]
            )

            # Log results
            logger.log_result(exp_id, {
                "mean_combined_loss": analysis[pair]["combined_loss"]["mean"],
                "std_combined_loss": analysis[pair]["combined_loss"]["std"],
                "families_analyzed": len(pair_results),
                "excluded_component": analysis[pair]["excluded_component"],
                "excluded_component_mean": analysis[pair]["excluded_component_at_optimal"]["mean"],
                "per_family_results": [asdict(r) for r in pair_results]
            })

            excluded = analysis[pair]["excluded_component"]
            excluded_val = analysis[pair]["excluded_component_at_optimal"]["mean"]
            logger.log_observation(
                exp_id,
                f"When optimizing {pair.replace('_', '+')}, {excluded} degrades to {excluded_val:.4f}"
            )

    # Save detailed results
    results_file = output_dir / "pairwise_analysis.json"
    results_data = {
        pair: [asdict(r) for r in pair_results]
        for pair, pair_results in results.items()
    }
    results_data["analysis"] = analysis
    results_data["comparison_with_single"] = comparison

    with open(results_file, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, analysis, comparison, families_data)
    report_file = output_dir / "pairwise_analysis.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for pair in ["centroid_volume", "centroid_shape", "volume_shape"]:
        if pair in analysis:
            a = analysis[pair]
            print(f"\n{pair.replace('_', '+').upper()}:")
            print(f"  Combined loss: {a['combined_loss']['mean']:.4f} ± {a['combined_loss']['std']:.4f}")
            print(f"  {a['excluded_component']} at optimal: {a['excluded_component_at_optimal']['mean']:.4f}")


if __name__ == "__main__":
    main()
