# Phase 5.1: Comprehensive Loss Function Analysis Report

**Generated**: 2026-01-03 17:42

**Tasks Covered**: 92 (Single-component), 93 (Pairwise), 94 (Pareto), 
95 (Aggregation), 96 (Alternative Metrics)

**Experiments**: EXP-001 through EXP-021

---

## Executive Summary

This report synthesizes Phase 5.1 Loss Function Analysis findings from 21 experiments 
(EXP-001 through EXP-021) investigating optimal loss function design for screen-to-surface 
color polyhedron transformation.

### Key Findings

1. **Volume matching is the dominant objective**: Volume-only optimization achieves 0.054 combined loss,
   nearly identical to full combined optimization (0.0535). Centroid and shape contribute minimally.

2. **Shape preservation is fundamentally limited**: Across all tested weight combinations,
   shape loss varies only 5% (0.13 to 0.18). This is a constraint of the transformation approach,
   not the loss function.

3. **Chamfer distance can replace Hausdorff**: Correlation r=0.99 between the two metrics.
   Chamfer is computationally faster (O(n log n) vs O(n²)).

4. **Mean aggregation is optimal**: Alternative methods (minimax, trimmed mean, median)
   either trade too much performance or fail catastrophically on outlier families.

5. **All Pareto strategies are optimal**: The 6 tested weight configurations occupy different
   regions of the Pareto frontier with genuine trade-offs between objectives.

---

## Methodology

### Loss Function Components

| Component | Formula | Description |
|-----------|---------|-------------|
| Centroid | ‖c_screen - c_surface‖ / max_extent | Normalized position difference |
| Volume | |V_screen/V_surface - 1| | Volume ratio deviation |
| Shape | Hausdorff(S, T) / max_extent | Normalized surface distance |

### Combined Loss Function

```
L_total = w_c × L_centroid + w_v × L_volume + w_s × L_shape
```

Default weights: (w_c, w_v, w_s) = (0.4, 0.3, 0.3)

### Dataset

- **Screen polyhedra**: 35 families from 184K crowdsourced RGB colors (threshold 0.6)
- **Surface polyhedra**: 24 families from Centore's surface color dataset
- **Valid overlap**: 21 families with 3D extent in both datasets

---

## Single-Component Optimization (Task 92)

Isolated optimization of each loss component to understand their individual impact:

| Strategy | Optimized Loss | Combined Loss | Rank |
|----------|----------------|---------------|------|
| Volume-only | 0.0000 | 0.0540 | 1 |
| Centroid-only | 0.0000 | 0.1580 | 2 |
| Shape-only | 0.1304 | 0.3076 | 3 |

**Critical insight**: Volume-only achieves 0.054 combined loss, nearly identical to the
full weighted combination. This confirms volume matching is the dominant objective.

---

## Pairwise Component Trade-offs (Task 93)

Optimization of component pairs to understand interactions:

| Pair | Combined Loss | Excluded Component at Optimal |
|------|---------------|-------------------------------|
| centroid + volume | 0.0561 | shape: 0.1799 |
| centroid + shape | 0.1580 | volume: 0.3566 |
| volume + shape | 0.0789 | centroid: 0.0692 |

**Finding**: Volume-only (0.054) still outperforms the best pairwise combination (0.056).
Adding centroid or shape objectives provides marginal benefit at best.

---

## Pareto Frontier Analysis (Task 94)

All 6 tested strategies are Pareto-optimal (none dominates another):

| Strategy | Centroid | Volume | Shape | Combined |
|----------|----------|--------|-------|----------|
| volume_only | 0.0000 | 0.0000 | 0.1800 | 0.0540 |
| centroid_volume | 0.0054 | 0.0000 | 0.1799 | 0.0561 |
| volume_shape | 0.0692 | 0.0000 | 0.1707 | 0.0789 |
| centroid_only | 0.0000 | 0.3566 | 0.1699 | 0.1580 |
| centroid_shape | 0.0000 | 0.3566 | 0.1699 | 0.1580 |
| shape_only | 0.2557 | 0.5540 | 0.1304 | 0.3076 |

### Trade-off Ranges

| Objective | Min Achievable | Max Achievable | Range |
|-----------|----------------|----------------|-------|
| centroid | 0.0000 | 0.2557 | 0.2557 |
| volume | 0.0000 | 0.5540 | 0.5540 |
| shape | 0.1304 | 0.1800 | 0.0495 |

**Critical observation**: Shape varies only 0.05 (0.13 to 0.18) across ALL strategies.
Shape preservation is limited by the transformation approach, not the loss weights.

---

## Aggregation Method Comparison (Task 95)

Comparison of methods for combining losses across families:

| Method | Aggregated Loss | Mean Loss | Worst Family | Worst Loss |
|--------|-----------------|-----------|--------------|------------|
| mean | 0.4228 | 0.4228 | lime | 0.5708 |
| sum | 9.7238 | 0.4228 | lime | 0.5707 |
| trimmed_mean_10 | 0.4036 | 0.4260 | peach | 1.0551 |
| weighted_mean | 0.4224 | 0.4328 | coral | 0.6071 |
| minimax | 0.5417 | 0.4628 | gray | 0.5417 |
| trimmed_mean_20 | 0.3093 | 1.3021 | peach | 14.7544 |
| median | 0.3327 | 1.7685 | peach | 20.7072 |

**Warning**: Trimmed mean and median methods cause catastrophic failures on outlier families.
Mean aggregation is most stable and recommended for general use.

---

## Alternative Loss Metrics (Task 96)

Comparison of shape distance metrics:

| Metric | Mean | Std | Description |
|--------|------|-----|-------------|
| Hausdorff | 0.2928 | 0.0995 | Surface-to-surface distance |
| Chamfer | 0.2822 | 0.1058 | Symmetric nearest-neighbor |
| EMD | 0.3891 | 0.1119 | Earth Mover's Distance |
| Spectral | 0.2069 | 0.1252 | Covariance eigenvalue comparison |
| IoU | 0.9127 | 0.0951 | 1 - Jaccard overlap |

### Key Correlations

| Metric Pair | Correlation |
|-------------|-------------|
| hausdorff ↔ chamfer | 0.99 |
| hausdorff ↔ emd | 0.91 |
| chamfer ↔ emd | 0.91 |
| chamfer ↔ iou | 0.70 |

**Recommendation**: Replace Hausdorff with Chamfer (r=0.99, faster computation).
Consider adding spectral loss to capture orientation/spread not in shape metrics.

---

## Recommendations

### Loss Function Design

1. **Use volume-only optimization** for best results
   - Achieves 0.054 combined loss (near-optimal)
   - Simpler, faster, more interpretable

2. **Replace Hausdorff with Chamfer distance**
   - Correlation r=0.99 (equivalent information)
   - O(n log n) vs O(n²) computational complexity

3. **Use mean aggregation across families**
   - Most stable and consistent
   - Minimax possible for worst-case guarantees (5% improvement at 10% mean cost)

### Future Work

1. **Shape preservation remains at ~0.13-0.18** regardless of weights
   - Investigate non-linear transformations (RBF, TPS)
   - Consider per-family transformations for problematic cases

2. **Problematic families identified**: peach, lime, coral, gray
   - Investigate why these families have high transformation error
   - May require special handling or exclusion

3. **Spectral loss captures different information**
   - Negative correlation with shape metrics
   - Could complement current loss function for covariance matching

---

## Experiment Registry

Total experiments: 21

| ID | Name | Method | Tags |
|----|------|--------|------|
|  | Translation+Scaling Baseline | translation_scaling | baseline, linear, phase4 |
|  | Nonlinear: polynomial_deg2 | polynomial_deg2 | nonlinear, phase4 |
|  | Nonlinear: polynomial_deg3 | polynomial_deg3 | nonlinear, phase4 |
|  | Nonlinear: rbf_multiquadric | rbf_multiquadric | nonlinear, phase4 |
|  | Nonlinear: rbf_gaussian | rbf_gaussian | nonlinear, phase4 |
|  | Nonlinear: thin_plate_spline | thin_plate_spline | nonlinear, phase4 |
|  | Domain: Munsell Cartesian | translation_scaling | domain_comparison, phase4 |
|  | Domain: RGB | translation_scaling | domain_comparison, phase4 |
|  | Domain: CIELAB | translation_scaling | domain_comparison, phase4 |
|  | Translation+Scaling in Munsell | translation_scaling | extended_domain, phase4 |
|  | Translation+Scaling in RGB | translation_scaling | extended_domain, phase4 |
|  | Affine in Munsell | affine | extended_domain, phase4 |
|  | Single-Component: Centroid-only | translation_scaling | single_component, phase5.1, centroid |
|  | Single-Component: Volume-only | translation_scaling | single_component, phase5.1, volume |
|  | Single-Component: Shape-only | translation_scaling | single_component, phase5.1, shape |
|  | Pairwise: centroid+volume | translation_scaling | pairwise, phase5.1, centroid_volume |
|  | Pairwise: centroid+shape | translation_scaling | pairwise, phase5.1, centroid_shape |
|  | Pairwise: volume+shape | translation_scaling | pairwise, phase5.1, volume_shape |
|  | Pareto Frontier (from existing) | analysis | pareto, phase5.1, multi_objective |
|  | Alternative Loss Metrics Comparison | metric_comparison | metrics, phase5.1, comparison |
|  | Aggregation Method Comparison | aggregation_analysis | aggregation, phase5.1, comparison |
