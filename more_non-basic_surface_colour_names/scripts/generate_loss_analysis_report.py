#!/usr/bin/env python3
"""
Phase 5.1: Comprehensive Loss Analysis Report Generator

Synthesizes findings from all Phase 5.1 experiments:
- Task 92: Single-component optimization
- Task 93: Pairwise optimization
- Task 94: Pareto frontier analysis
- Task 95: Aggregation methods
- Task 96: Alternative metrics

Generates a comprehensive markdown report for research documentation.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).parent.parent
ANALYSIS_DIR = BASE_DIR / "datasets/transformation_analysis"


def load_json(filepath: Path) -> Optional[Dict]:
    """Load JSON file if it exists."""
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def load_all_results() -> Dict[str, Any]:
    """Load all Phase 5.1 analysis results."""
    results = {}

    # Single component analysis
    results["single_component"] = load_json(ANALYSIS_DIR / "single_component_analysis.json")

    # Pairwise analysis
    results["pairwise"] = load_json(ANALYSIS_DIR / "pairwise_analysis.json")

    # Pareto analysis
    results["pareto"] = load_json(ANALYSIS_DIR / "pareto_analysis.json")

    # Aggregation comparison
    results["aggregation"] = load_json(ANALYSIS_DIR / "aggregation_comparison.json")

    # Alternative metrics
    results["metrics"] = load_json(ANALYSIS_DIR / "alternative_metrics.json")

    # Experiment registry
    results["experiments"] = load_json(ANALYSIS_DIR / "experiment_registry.json")

    return results


def generate_executive_summary(results: Dict[str, Any]) -> List[str]:
    """Generate executive summary section."""
    lines = []
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("This report synthesizes Phase 5.1 Loss Function Analysis findings from 21 experiments ")
    lines.append("(EXP-001 through EXP-021) investigating optimal loss function design for screen-to-surface ")
    lines.append("color polyhedron transformation.")
    lines.append("")

    lines.append("### Key Findings")
    lines.append("")
    lines.append("1. **Volume matching is the dominant objective**: Volume-only optimization achieves 0.054 combined loss,")
    lines.append("   nearly identical to full combined optimization (0.0535). Centroid and shape contribute minimally.")
    lines.append("")
    lines.append("2. **Shape preservation is fundamentally limited**: Across all tested weight combinations,")
    lines.append("   shape loss varies only 5% (0.13 to 0.18). This is a constraint of the transformation approach,")
    lines.append("   not the loss function.")
    lines.append("")
    lines.append("3. **Chamfer distance can replace Hausdorff**: Correlation r=0.99 between the two metrics.")
    lines.append("   Chamfer is computationally faster (O(n log n) vs O(n²)).")
    lines.append("")
    lines.append("4. **Mean aggregation is optimal**: Alternative methods (minimax, trimmed mean, median)")
    lines.append("   either trade too much performance or fail catastrophically on outlier families.")
    lines.append("")
    lines.append("5. **All Pareto strategies are optimal**: The 6 tested weight configurations occupy different")
    lines.append("   regions of the Pareto frontier with genuine trade-offs between objectives.")
    lines.append("")

    return lines


def generate_methodology_section() -> List[str]:
    """Generate methodology section."""
    lines = []
    lines.append("## Methodology")
    lines.append("")
    lines.append("### Loss Function Components")
    lines.append("")
    lines.append("| Component | Formula | Description |")
    lines.append("|-----------|---------|-------------|")
    lines.append("| Centroid | ‖c_screen - c_surface‖ / max_extent | Normalized position difference |")
    lines.append("| Volume | |V_screen/V_surface - 1| | Volume ratio deviation |")
    lines.append("| Shape | Hausdorff(S, T) / max_extent | Normalized surface distance |")
    lines.append("")
    lines.append("### Combined Loss Function")
    lines.append("")
    lines.append("```")
    lines.append("L_total = w_c × L_centroid + w_v × L_volume + w_s × L_shape")
    lines.append("```")
    lines.append("")
    lines.append("Default weights: (w_c, w_v, w_s) = (0.4, 0.3, 0.3)")
    lines.append("")
    lines.append("### Dataset")
    lines.append("")
    lines.append("- **Screen polyhedra**: 35 families from 184K crowdsourced RGB colors (threshold 0.6)")
    lines.append("- **Surface polyhedra**: 24 families from Centore's surface color dataset")
    lines.append("- **Valid overlap**: 21 families with 3D extent in both datasets")
    lines.append("")

    return lines


def generate_single_component_section(results: Dict[str, Any]) -> List[str]:
    """Generate single-component analysis section."""
    lines = []
    lines.append("## Single-Component Optimization (Task 92)")
    lines.append("")

    sc = results.get("single_component", {})
    if not sc:
        lines.append("*Data not available*")
        return lines

    analysis = sc.get("analysis", {})

    lines.append("Isolated optimization of each loss component to understand their individual impact:")
    lines.append("")
    lines.append("| Strategy | Optimized Loss | Combined Loss | Rank |")
    lines.append("|----------|----------------|---------------|------|")

    if "volume" in analysis:
        v = analysis["volume"]
        lines.append(f"| Volume-only | {v['target_component']['mean_final']:.4f} | {v['combined_loss_at_optimal']['mean']:.4f} | 1 |")

    if "centroid" in analysis:
        c = analysis["centroid"]
        lines.append(f"| Centroid-only | {c['target_component']['mean_final']:.4f} | {c['combined_loss_at_optimal']['mean']:.4f} | 2 |")

    if "shape" in analysis:
        s = analysis["shape"]
        lines.append(f"| Shape-only | {s['target_component']['mean_final']:.4f} | {s['combined_loss_at_optimal']['mean']:.4f} | 3 |")

    lines.append("")
    lines.append("**Critical insight**: Volume-only achieves 0.054 combined loss, nearly identical to the")
    lines.append("full weighted combination. This confirms volume matching is the dominant objective.")
    lines.append("")

    return lines


def generate_pairwise_section(results: Dict[str, Any]) -> List[str]:
    """Generate pairwise analysis section."""
    lines = []
    lines.append("## Pairwise Component Trade-offs (Task 93)")
    lines.append("")

    pw = results.get("pairwise", {})
    if not pw:
        lines.append("*Data not available*")
        return lines

    analysis = pw.get("analysis", {})

    lines.append("Optimization of component pairs to understand interactions:")
    lines.append("")
    lines.append("| Pair | Combined Loss | Excluded Component at Optimal |")
    lines.append("|------|---------------|-------------------------------|")

    pairs = [
        ("centroid_volume", "shape"),
        ("centroid_shape", "volume"),
        ("volume_shape", "centroid")
    ]

    for pair_name, excluded in pairs:
        if pair_name in analysis:
            p = analysis[pair_name]
            comp_values = p.get("component_values_at_optimal", {})
            excluded_val = comp_values.get(f"mean_{excluded}", 0)
            lines.append(f"| {pair_name.replace('_', ' + ')} | {p['combined_loss']['mean']:.4f} | {excluded}: {excluded_val:.4f} |")

    lines.append("")
    lines.append("**Finding**: Volume-only (0.054) still outperforms the best pairwise combination (0.056).")
    lines.append("Adding centroid or shape objectives provides marginal benefit at best.")
    lines.append("")

    return lines


def generate_pareto_section(results: Dict[str, Any]) -> List[str]:
    """Generate Pareto analysis section."""
    lines = []
    lines.append("## Pareto Frontier Analysis (Task 94)")
    lines.append("")

    pareto = results.get("pareto", {})
    if not pareto:
        lines.append("*Data not available*")
        return lines

    analysis = pareto.get("analysis", {})
    all_points = pareto.get("all_points", [])

    lines.append("All 6 tested strategies are Pareto-optimal (none dominates another):")
    lines.append("")
    lines.append("| Strategy | Centroid | Volume | Shape | Combined |")
    lines.append("|----------|----------|--------|-------|----------|")

    for p in sorted(all_points, key=lambda x: x.get("combined", 0)):
        lines.append(f"| {p['name']} | {p['centroid']:.4f} | {p['volume']:.4f} | {p['shape']:.4f} | {p['combined']:.4f} |")

    lines.append("")

    # Trade-off ranges
    if "trade_off_ranges" in analysis:
        ranges = analysis["trade_off_ranges"]
        lines.append("### Trade-off Ranges")
        lines.append("")
        lines.append("| Objective | Min Achievable | Max Achievable | Range |")
        lines.append("|-----------|----------------|----------------|-------|")

        for obj in ["centroid", "volume", "shape"]:
            if obj in ranges:
                min_v, max_v = ranges[obj]
                lines.append(f"| {obj} | {min_v:.4f} | {max_v:.4f} | {max_v - min_v:.4f} |")

        lines.append("")

    lines.append("**Critical observation**: Shape varies only 0.05 (0.13 to 0.18) across ALL strategies.")
    lines.append("Shape preservation is limited by the transformation approach, not the loss weights.")
    lines.append("")

    return lines


def generate_aggregation_section(results: Dict[str, Any]) -> List[str]:
    """Generate aggregation comparison section."""
    lines = []
    lines.append("## Aggregation Method Comparison (Task 95)")
    lines.append("")

    agg = results.get("aggregation", {})
    if not agg:
        lines.append("*Data not available*")
        return lines

    agg_results = agg.get("results", [])

    lines.append("Comparison of methods for combining losses across families:")
    lines.append("")
    lines.append("| Method | Aggregated Loss | Mean Loss | Worst Family | Worst Loss |")
    lines.append("|--------|-----------------|-----------|--------------|------------|")

    for r in sorted(agg_results, key=lambda x: sum(x.get("per_family_losses", {}).values()) / max(len(x.get("per_family_losses", {})), 1)):
        losses = r.get("per_family_losses", {})
        mean_loss = sum(losses.values()) / len(losses) if losses else 0
        lines.append(f"| {r['method']} | {r['combined_loss']:.4f} | {mean_loss:.4f} | {r['worst_family']} | {r['worst_loss']:.4f} |")

    lines.append("")
    lines.append("**Warning**: Trimmed mean and median methods cause catastrophic failures on outlier families.")
    lines.append("Mean aggregation is most stable and recommended for general use.")
    lines.append("")

    return lines


def generate_metrics_section(results: Dict[str, Any]) -> List[str]:
    """Generate alternative metrics section."""
    lines = []
    lines.append("## Alternative Loss Metrics (Task 96)")
    lines.append("")

    metrics = results.get("metrics", {})
    if not metrics:
        lines.append("*Data not available*")
        return lines

    # Statistics are nested under analysis
    analysis = metrics.get("analysis", {})
    stats = analysis.get("statistics", {})

    lines.append("Comparison of shape distance metrics:")
    lines.append("")
    lines.append("| Metric | Mean | Std | Description |")
    lines.append("|--------|------|-----|-------------|")
    lines.append(f"| Hausdorff | {stats.get('hausdorff', {}).get('mean', 0):.4f} | {stats.get('hausdorff', {}).get('std', 0):.4f} | Surface-to-surface distance |")
    lines.append(f"| Chamfer | {stats.get('chamfer', {}).get('mean', 0):.4f} | {stats.get('chamfer', {}).get('std', 0):.4f} | Symmetric nearest-neighbor |")
    lines.append(f"| EMD | {stats.get('emd', {}).get('mean', 0):.4f} | {stats.get('emd', {}).get('std', 0):.4f} | Earth Mover's Distance |")
    lines.append(f"| Spectral | {stats.get('spectral', {}).get('mean', 0):.4f} | {stats.get('spectral', {}).get('std', 0):.4f} | Covariance eigenvalue comparison |")
    lines.append(f"| IoU | {stats.get('iou', {}).get('mean', 0):.4f} | {stats.get('iou', {}).get('std', 0):.4f} | 1 - Jaccard overlap |")
    lines.append("")

    # Correlations (nested under analysis as matrix with metrics list)
    corr_matrix = analysis.get("correlation_matrix", [])
    metric_names = analysis.get("metrics", [])

    if corr_matrix and metric_names:
        lines.append("### Key Correlations")
        lines.append("")
        lines.append("| Metric Pair | Correlation |")
        lines.append("|-------------|-------------|")

        # Create index lookup
        metric_idx = {m: i for i, m in enumerate(metric_names)}

        high_corr = [
            ("hausdorff", "chamfer"),
            ("hausdorff", "emd"),
            ("chamfer", "emd"),
            ("chamfer", "iou")
        ]

        for m1, m2 in high_corr:
            if m1 in metric_idx and m2 in metric_idx:
                i, j = metric_idx[m1], metric_idx[m2]
                r = corr_matrix[i][j]
                lines.append(f"| {m1} ↔ {m2} | {r:.2f} |")

        lines.append("")

    lines.append("**Recommendation**: Replace Hausdorff with Chamfer (r=0.99, faster computation).")
    lines.append("Consider adding spectral loss to capture orientation/spread not in shape metrics.")
    lines.append("")

    return lines


def generate_recommendations() -> List[str]:
    """Generate recommendations section."""
    lines = []
    lines.append("## Recommendations")
    lines.append("")
    lines.append("### Loss Function Design")
    lines.append("")
    lines.append("1. **Use volume-only optimization** for best results")
    lines.append("   - Achieves 0.054 combined loss (near-optimal)")
    lines.append("   - Simpler, faster, more interpretable")
    lines.append("")
    lines.append("2. **Replace Hausdorff with Chamfer distance**")
    lines.append("   - Correlation r=0.99 (equivalent information)")
    lines.append("   - O(n log n) vs O(n²) computational complexity")
    lines.append("")
    lines.append("3. **Use mean aggregation across families**")
    lines.append("   - Most stable and consistent")
    lines.append("   - Minimax possible for worst-case guarantees (5% improvement at 10% mean cost)")
    lines.append("")
    lines.append("### Future Work")
    lines.append("")
    lines.append("1. **Shape preservation remains at ~0.13-0.18** regardless of weights")
    lines.append("   - Investigate non-linear transformations (RBF, TPS)")
    lines.append("   - Consider per-family transformations for problematic cases")
    lines.append("")
    lines.append("2. **Problematic families identified**: peach, lime, coral, gray")
    lines.append("   - Investigate why these families have high transformation error")
    lines.append("   - May require special handling or exclusion")
    lines.append("")
    lines.append("3. **Spectral loss captures different information**")
    lines.append("   - Negative correlation with shape metrics")
    lines.append("   - Could complement current loss function for covariance matching")
    lines.append("")

    return lines


def generate_experiment_summary(results: Dict[str, Any]) -> List[str]:
    """Generate experiment summary section."""
    lines = []
    lines.append("## Experiment Registry")
    lines.append("")

    exp = results.get("experiments", {})
    if not exp:
        lines.append("*Data not available*")
        return lines

    experiments = exp.get("experiments", [])

    lines.append(f"Total experiments: {len(experiments)}")
    lines.append("")
    lines.append("| ID | Name | Method | Tags |")
    lines.append("|----|------|--------|------|")

    for e in sorted(experiments, key=lambda x: x.get("experiment_id", "")):
        tags = ", ".join(e.get("tags", []))
        lines.append(f"| {e.get('experiment_id', '')} | {e.get('name', '')} | {e.get('method', '')} | {tags} |")

    lines.append("")

    return lines


def main():
    """Generate comprehensive loss analysis report."""
    print("Phase 5.1: Comprehensive Loss Analysis Report")
    print("=" * 70)

    # Load all results
    results = load_all_results()
    print(f"Loaded data from {sum(1 for v in results.values() if v is not None)} sources")

    # Generate report
    report = []

    # Header
    report.append("# Phase 5.1: Comprehensive Loss Function Analysis Report")
    report.append("")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    report.append("**Tasks Covered**: 92 (Single-component), 93 (Pairwise), 94 (Pareto), ")
    report.append("95 (Aggregation), 96 (Alternative Metrics)")
    report.append("")
    report.append("**Experiments**: EXP-001 through EXP-021")
    report.append("")
    report.append("---")
    report.append("")

    # Sections
    report.extend(generate_executive_summary(results))
    report.append("---")
    report.append("")
    report.extend(generate_methodology_section())
    report.append("---")
    report.append("")
    report.extend(generate_single_component_section(results))
    report.append("---")
    report.append("")
    report.extend(generate_pairwise_section(results))
    report.append("---")
    report.append("")
    report.extend(generate_pareto_section(results))
    report.append("---")
    report.append("")
    report.extend(generate_aggregation_section(results))
    report.append("---")
    report.append("")
    report.extend(generate_metrics_section(results))
    report.append("---")
    report.append("")
    report.extend(generate_recommendations())
    report.append("---")
    report.append("")
    report.extend(generate_experiment_summary(results))

    # Write report
    report_text = "\n".join(report)
    report_file = ANALYSIS_DIR / "PHASE_5.1_LOSS_ANALYSIS_REPORT.md"

    with open(report_file, "w") as f:
        f.write(report_text)

    print(f"\nSaved: {report_file}")
    print(f"Report length: {len(report_text)} characters")

    # Summary stats
    print("\n" + "=" * 70)
    print("REPORT GENERATED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
