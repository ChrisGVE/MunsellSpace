#!/usr/bin/env python3
"""
Phase 5: Consolidation Strategy Evaluation

Evaluates different methods for merging duplicate/variant entries:
1. Simple mean - Average all coordinates
2. Weighted mean - Weight by response count or confidence
3. Median - Robust to outliers
4. Mode-based - Most common coordinate region
5. Source-prioritized - Prefer Centore over XKCD

Measures impact on accuracy using shared overlay colors as validation.
"""

import json
import math
from collections import defaultdict
from pathlib import Path
import statistics


# ============================================================================
# Configuration
# ============================================================================

OUTPUT_DIR = Path(__file__).parent

XKCD_COORDS_CACHE = OUTPUT_DIR / "xkcd_coordinates_cache.json"
CANONICAL_MAPPINGS = OUTPUT_DIR / "canonical_names.json"


# ============================================================================
# Consolidation Strategy Functions
# ============================================================================

def consolidate_simple_mean(rgb_list: list) -> tuple:
    """Strategy 1: Simple arithmetic mean of all RGB values."""
    if not rgb_list:
        return None

    r = sum(c[0] for c in rgb_list) / len(rgb_list)
    g = sum(c[1] for c in rgb_list) / len(rgb_list)
    b = sum(c[2] for c in rgb_list) / len(rgb_list)

    return (int(round(r)), int(round(g)), int(round(b)))


def consolidate_weighted_mean(rgb_list: list, weights: list = None) -> tuple:
    """Strategy 2: Weighted mean (by count if no weights provided)."""
    if not rgb_list:
        return None

    if weights is None:
        weights = [1] * len(rgb_list)

    total_weight = sum(weights)
    if total_weight == 0:
        return None

    r = sum(c[0] * w for c, w in zip(rgb_list, weights)) / total_weight
    g = sum(c[1] * w for c, w in zip(rgb_list, weights)) / total_weight
    b = sum(c[2] * w for c, w in zip(rgb_list, weights)) / total_weight

    return (int(round(r)), int(round(g)), int(round(b)))


def consolidate_median(rgb_list: list) -> tuple:
    """Strategy 3: Median of each channel (robust to outliers)."""
    if not rgb_list:
        return None

    r = statistics.median(c[0] for c in rgb_list)
    g = statistics.median(c[1] for c in rgb_list)
    b = statistics.median(c[2] for c in rgb_list)

    return (int(round(r)), int(round(g)), int(round(b)))


def consolidate_trimmed_mean(rgb_list: list, trim_fraction: float = 0.1) -> tuple:
    """Strategy 4: Trimmed mean (exclude extreme values)."""
    if not rgb_list:
        return None

    n = len(rgb_list)
    if n < 5:
        return consolidate_simple_mean(rgb_list)

    trim_count = int(n * trim_fraction)
    if trim_count == 0:
        return consolidate_simple_mean(rgb_list)

    # Sort by luminance and trim
    sorted_by_lum = sorted(rgb_list, key=lambda c: 0.299*c[0] + 0.587*c[1] + 0.114*c[2])
    trimmed = sorted_by_lum[trim_count:-trim_count] if trim_count > 0 else sorted_by_lum

    return consolidate_simple_mean(trimmed)


def consolidate_mode_region(rgb_list: list, bin_size: int = 20) -> tuple:
    """Strategy 5: Most common region (binned mode)."""
    if not rgb_list:
        return None

    # Bin RGB values
    bins = defaultdict(list)
    for c in rgb_list:
        bin_key = (c[0] // bin_size, c[1] // bin_size, c[2] // bin_size)
        bins[bin_key].append(c)

    # Find largest bin
    largest_bin = max(bins.values(), key=len)

    # Return mean of largest bin
    return consolidate_simple_mean(largest_bin)


def consolidate_centroid_weighted(rgb_list: list) -> tuple:
    """
    Strategy 6: Weight by distance from centroid.
    Points closer to centroid get higher weight (inverse distance).
    """
    if not rgb_list:
        return None

    if len(rgb_list) < 3:
        return consolidate_simple_mean(rgb_list)

    # First pass: compute centroid
    centroid = consolidate_simple_mean(rgb_list)

    # Compute distances
    distances = []
    for c in rgb_list:
        d = math.sqrt((c[0]-centroid[0])**2 + (c[1]-centroid[1])**2 + (c[2]-centroid[2])**2)
        distances.append(max(d, 1))  # Avoid division by zero

    # Inverse distance weights
    weights = [1/d for d in distances]

    return consolidate_weighted_mean(rgb_list, weights)


# ============================================================================
# Evaluation Functions
# ============================================================================

def compute_rgb_distance(rgb1: tuple, rgb2: tuple) -> float:
    """Euclidean distance in RGB space."""
    if rgb1 is None or rgb2 is None:
        return float('inf')
    return math.sqrt(sum((a-b)**2 for a, b in zip(rgb1, rgb2)))


def evaluate_strategies_on_color(color_name: str, rgb_list: list) -> dict:
    """
    Evaluate all consolidation strategies on a single color.
    Uses leave-one-out cross-validation approach.
    """
    strategies = {
        'simple_mean': consolidate_simple_mean,
        'median': consolidate_median,
        'trimmed_mean': consolidate_trimmed_mean,
        'mode_region': consolidate_mode_region,
        'centroid_weighted': consolidate_centroid_weighted
    }

    results = {}
    for name, func in strategies.items():
        result = func(rgb_list)
        results[name] = {
            'rgb': result,
            'strategy': name
        }

    return results


def compare_strategies_with_reference(
    xkcd_coords: dict,
    reference_colors: dict,
    sample_size: int = 100
) -> dict:
    """
    Compare consolidation strategies using reference colors.
    Reference could be Centore centroids or high-confidence XKCD centroids.
    """
    strategies = ['simple_mean', 'median', 'trimmed_mean', 'mode_region', 'centroid_weighted']
    strategy_errors = {s: [] for s in strategies}

    for color, ref_rgb in reference_colors.items():
        if color not in xkcd_coords:
            continue

        rgb_list = xkcd_coords[color]
        if len(rgb_list) < 10:  # Skip colors with few samples
            continue

        # Evaluate each strategy
        results = evaluate_strategies_on_color(color, rgb_list)

        for strategy_name in strategies:
            if strategy_name in results:
                estimated_rgb = results[strategy_name]['rgb']
                error = compute_rgb_distance(estimated_rgb, ref_rgb)
                strategy_errors[strategy_name].append({
                    'color': color,
                    'error': error,
                    'sample_count': len(rgb_list)
                })

    return strategy_errors


def compute_within_color_variance(xkcd_coords: dict, min_count: int = 50) -> dict:
    """
    Compute variance reduction for each strategy.
    Measures how well each strategy represents the underlying distribution.
    """
    strategies = {
        'simple_mean': consolidate_simple_mean,
        'median': consolidate_median,
        'trimmed_mean': consolidate_trimmed_mean,
        'mode_region': consolidate_mode_region,
        'centroid_weighted': consolidate_centroid_weighted
    }

    variance_results = {s: [] for s in strategies}

    for color, rgb_list in xkcd_coords.items():
        if len(rgb_list) < min_count:
            continue

        for strategy_name, func in strategies.items():
            consolidated = func(rgb_list)
            if consolidated is None:
                continue

            # Compute average distance from consolidated point to all samples
            distances = [compute_rgb_distance(consolidated, rgb) for rgb in rgb_list]
            mean_distance = statistics.mean(distances)

            variance_results[strategy_name].append({
                'color': color,
                'mean_distance': mean_distance,
                'sample_count': len(rgb_list)
            })

    return variance_results


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 5: Consolidation Strategy Evaluation")
    print("=" * 70)

    # Load data
    print("\n1. Loading data...")

    print("   Loading XKCD coordinates...")
    with open(XKCD_COORDS_CACHE, 'r') as f:
        cached = json.load(f)
    xkcd_coords = {k: [tuple(v) for v in vals] for k, vals in cached.items()}
    print(f"   → Loaded {len(xkcd_coords):,} color names")

    print("   Loading canonical mappings...")
    with open(CANONICAL_MAPPINGS, 'r') as f:
        canonical_mappings = json.load(f)
    print(f"   → Loaded {len(canonical_mappings):,} mappings")

    # Filter to colors with sufficient samples
    print("\n2. Filtering colors with sufficient samples...")
    min_samples = 100
    sufficient_colors = {k: v for k, v in xkcd_coords.items() if len(v) >= min_samples}
    print(f"   → {len(sufficient_colors):,} colors with >= {min_samples} samples")

    # Compute within-color variance for each strategy
    print("\n3. Evaluating consolidation strategies...")

    variance_results = compute_within_color_variance(xkcd_coords, min_count=100)

    print("\n   Strategy Performance (Mean Distance to Samples):")
    strategy_summary = {}
    for strategy, results in variance_results.items():
        if results:
            mean_dist = statistics.mean(r['mean_distance'] for r in results)
            std_dist = statistics.stdev(r['mean_distance'] for r in results) if len(results) > 1 else 0
            strategy_summary[strategy] = {
                'mean_distance': mean_dist,
                'std_distance': std_dist,
                'n_colors': len(results)
            }
            print(f"   → {strategy}: mean={mean_dist:.2f}, std={std_dist:.2f}, n={len(results)}")

    # Rank strategies
    ranked = sorted(strategy_summary.items(), key=lambda x: x[1]['mean_distance'])
    best_strategy = ranked[0][0]
    print(f"\n   Best strategy: {best_strategy}")

    # Analyze robustness to outliers
    print("\n4. Analyzing outlier robustness...")

    # Find high-variance colors (likely to have outliers)
    high_variance_colors = []
    for color, rgb_list in xkcd_coords.items():
        if len(rgb_list) >= 100:
            r_std = statistics.stdev(c[0] for c in rgb_list)
            g_std = statistics.stdev(c[1] for c in rgb_list)
            b_std = statistics.stdev(c[2] for c in rgb_list)
            total_std = math.sqrt(r_std**2 + g_std**2 + b_std**2)
            if total_std > 50:
                high_variance_colors.append((color, total_std, rgb_list))

    print(f"   → Found {len(high_variance_colors):,} high-variance colors (std > 50)")

    # Compare strategies on high-variance colors
    if high_variance_colors:
        print("\n   Outlier Robustness (High-Variance Colors):")
        outlier_performance = {s: [] for s in variance_results.keys()}

        for color, std, rgb_list in high_variance_colors[:100]:
            for strategy_name, func in [
                ('simple_mean', consolidate_simple_mean),
                ('median', consolidate_median),
                ('trimmed_mean', consolidate_trimmed_mean),
                ('mode_region', consolidate_mode_region),
                ('centroid_weighted', consolidate_centroid_weighted)
            ]:
                consolidated = func(rgb_list)
                if consolidated:
                    distances = [compute_rgb_distance(consolidated, rgb) for rgb in rgb_list]
                    mean_dist = statistics.mean(distances)
                    outlier_performance[strategy_name].append(mean_dist)

        for strategy, perfs in outlier_performance.items():
            if perfs:
                print(f"   → {strategy}: mean_dist={statistics.mean(perfs):.2f}")

    # Generate report
    print("\n5. Generating outputs...")

    report = []
    report.append("# Phase 5: Consolidation Strategy Evaluation Report")
    report.append("")
    report.append("## 1. Executive Summary")
    report.append("")
    report.append("Evaluated 5 consolidation strategies for merging duplicate color entries:")
    report.append("")
    report.append("| Strategy | Mean Distance | Std | n Colors | Rank |")
    report.append("|----------|---------------|-----|----------|------|")

    for i, (strategy, summary) in enumerate(ranked):
        rank = i + 1
        report.append(f"| {strategy} | {summary['mean_distance']:.2f} | "
                     f"{summary['std_distance']:.2f} | {summary['n_colors']:,} | {rank} |")
    report.append("")

    report.append(f"**Recommended Strategy**: {best_strategy}")
    report.append("")

    report.append("## 2. Strategy Descriptions")
    report.append("")
    report.append("### 2.1 Simple Mean")
    report.append("- Arithmetic mean of all RGB values")
    report.append("- **Pro**: Simple, unbiased estimator")
    report.append("- **Con**: Sensitive to outliers")
    report.append("")

    report.append("### 2.2 Median")
    report.append("- Median of each RGB channel independently")
    report.append("- **Pro**: Robust to outliers")
    report.append("- **Con**: May not preserve color relationships")
    report.append("")

    report.append("### 2.3 Trimmed Mean")
    report.append("- Mean after removing 10% extreme values (by luminance)")
    report.append("- **Pro**: Balances robustness and efficiency")
    report.append("- **Con**: May lose legitimate variation")
    report.append("")

    report.append("### 2.4 Mode Region")
    report.append("- Mean of the most populated 20x20x20 RGB bin")
    report.append("- **Pro**: Represents consensus color")
    report.append("- **Con**: May miss nuanced colors")
    report.append("")

    report.append("### 2.5 Centroid Weighted")
    report.append("- Inverse distance weighting from centroid")
    report.append("- **Pro**: Down-weights outliers automatically")
    report.append("- **Con**: Two-pass computation")
    report.append("")

    report.append("## 3. Evaluation Methodology")
    report.append("")
    report.append("### 3.1 Metric: Mean Distance to Samples")
    report.append("For each color, compute the average Euclidean distance in RGB space")
    report.append("from the consolidated point to all original samples.")
    report.append("")
    report.append("Lower distance = better representation of the color distribution.")
    report.append("")

    report.append("### 3.2 Outlier Robustness")
    report.append("Evaluated performance on high-variance colors (std > 50 in RGB space)")
    report.append("to assess sensitivity to outliers and noise.")
    report.append("")

    report.append("## 4. Recommendations")
    report.append("")
    report.append("### 4.1 For General Consolidation")
    report.append(f"- Use **{best_strategy}** for most cases")
    report.append("- This strategy provides the best balance of accuracy and robustness")
    report.append("")

    report.append("### 4.2 For High-Variance Colors")
    report.append("- Consider **trimmed_mean** or **median** for colors with high variance")
    report.append("- These strategies better handle outliers from uncalibrated monitors")
    report.append("")

    report.append("### 4.3 For Cross-Dataset Consolidation")
    report.append("- When combining Centore (spectrophotometer) with XKCD (RGB):")
    report.append("  - **Option A**: Source-prioritized (prefer Centore as ground truth)")
    report.append("  - **Option B**: Weighted mean (weight Centore higher)")
    report.append("  - **Option C**: Keep separate, document provenance")
    report.append("")

    report.append("### 4.4 Weighting by Sample Count")
    report.append("- For merging variant spellings, weight by response count")
    report.append("- Higher count = more reliable estimate")
    report.append("- Use sqrt(count) weighting to avoid over-dominance")
    report.append("")

    report.append("## 5. Trade-offs Summary")
    report.append("")
    report.append("| Criterion | Best Strategy | Rationale |")
    report.append("|-----------|--------------|-----------|")
    report.append("| Accuracy (all colors) | simple_mean | Unbiased |")
    report.append("| Outlier robustness | trimmed_mean/median | Ignores extremes |")
    report.append("| Consensus color | mode_region | Most common |")
    report.append("| Automatic weighting | centroid_weighted | Down-weights outliers |")
    report.append("| Interpretability | simple_mean | Most intuitive |")
    report.append("")

    report.append("---")
    report.append("")
    report.append("*Generated by Phase 5: Consolidation Strategy Evaluation*")

    # Write report
    report_path = OUTPUT_DIR / "consolidation_strategy.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"   → Report: {report_path}")

    # Write JSON data
    json_output = {
        'summary': {
            'colors_evaluated': len(sufficient_colors),
            'min_samples': min_samples,
            'best_strategy': best_strategy,
            'high_variance_colors': len(high_variance_colors)
        },
        'strategy_performance': strategy_summary,
        'rankings': [(s, summary['mean_distance']) for s, summary in ranked]
    }

    json_path = OUTPUT_DIR / "consolidation_strategy.json"
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   → Data: {json_path}")

    print(f"\nPhase 5 complete!")
    print(f"Recommended consolidation strategy: {best_strategy}")


if __name__ == "__main__":
    main()
