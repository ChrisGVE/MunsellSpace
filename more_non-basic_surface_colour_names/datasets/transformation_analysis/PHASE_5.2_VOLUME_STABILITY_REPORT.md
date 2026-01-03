# Phase 5.2: Volume Stability Report

**Generated**: 2026-01-03

**Tasks Covered**: 98 (Jacobian), 99 (Per-Family Ratios), 100 (Bootstrap), 101 (Synthesis)

---

## Executive Summary

Phase 5.2 investigated the stability and reliability of volume measurements in RGB→Munsell
color space transformation. Three complementary analyses were conducted:

1. **Jacobian Analysis** (Task 98): Measures local volume distortion across color space
2. **Per-Family Volume Ratios** (Task 99): Validates uniformity within each color family
3. **Bootstrap Sample Size** (Task 100): Determines minimum samples for stable volume estimates

### Key Findings

| Analysis | Key Metric | Value | Implication |
|----------|------------|-------|-------------|
| Jacobian | CV (spatial) | 0.02 | Volume mapping is uniform |
| Per-Family | Max deviation | 0.11% | No family-specific corrections needed |
| Bootstrap | Stable families | 94.3% | Sample sizes are adequate |

**Bottom Line**: Volume matching is reliable for 33/35 families with no position-dependent
corrections required. Use a single global scaling factor (~2054) for all transformations.

---

## 1. Jacobian Analysis Summary

### Spatial Distortion Patterns

The Jacobian determinant |det(J)| represents local volume scaling in the RGB→Munsell transformation.

| Region | Mean |det(J)| | Std Dev | Notes |
|--------|----------------|---------|-------|
| Overall | 2054.70 | 32.83 | Uniform expansion |
| Low Value (0-3) | 2083.36 | 119.48 | Slightly higher variance |
| Mid Value (3-5) | 2056.91 | 46.43 | Stable |
| High Value (7-10) | 2053.47 | 21.81 | Most stable |
| Low Chroma (0-4) | 2062.58 | 69.79 | Moderate variance |
| High Chroma (4+) | 2052.51 | 0.00 | Perfectly uniform |

**Key Insight**: The transformation expands RGB volumes by ~2000x uniformly. High-chroma
colors show zero variance in volume scaling.

### Per-Family Correction Factors

Monte Carlo sampling within each family's polyhedron (500 samples × 35 families):

| Metric | Value |
|--------|-------|
| Correction factor (all families) | 0.9989 |
| Correction factor std | 0.0000 |
| Per-family CV | 0.0000 |
| Max deviation from global | 0.11% |

**Conclusion**: All 35 families exhibit identical volume behavior. No per-family corrections needed.

---

## 2. Sample Size Requirements

### Bootstrap Analysis Results

Analyzed 177,706 samples across 35 families with 100 bootstrap iterations.

| Category | Count | Families |
|----------|-------|----------|
| Stable (CV < 0.05) | 33 | All except brown, purple |
| Unstable | 2 | brown, purple |

### Minimum Stable Sample Sizes

| Statistic | N_min |
|-----------|-------|
| Mean | 4,809 |
| Median | 3,385 |
| Min | 500 (lime) |
| Max | 21,992 (green) |

### Flagged Families

| Family | N Samples | Status | Issue |
|--------|-----------|--------|-------|
| brown | 5,068 | Unstable | Diffuse distribution |
| purple | 10,339 | Unstable | Irregularly shaped region |

These families may benefit from:
- Alpha-shape boundaries instead of convex hulls
- Robust volume estimation methods
- Exclusion from volume-based metrics

---

## 3. Volume Normalization Recommendations

### Convex Hull vs Alpha-Shape

| Method | Pros | Cons | Recommended For |
|--------|------|------|-----------------|
| Convex Hull | Simple, fast | Sensitive to outliers | 33 stable families |
| Alpha-Shape | Robust to outliers | Requires α tuning | brown, purple |

### Correction Factor Application

**Recommended Approach**: Single global scaling factor

```
V_munsell_normalized = V_rgb × 2054.70
```

Rationale:
- Per-family deviation is only 0.11%
- Computational simplicity
- No risk of overfitting to training data

**NOT Recommended**: Per-family correction factors

- Adds complexity without benefit
- Risk of overfitting
- Inconsistent with uniform Jacobian findings

---

## 4. Implications for Transformation

### When to Use Volume Loss

Volume matching should be included in the loss function when:

1. **Screen→Surface transformation**: Core use case
2. **Shape is secondary**: Phase 5.1 showed shape loss varies only 5% regardless of weights
3. **Families are stable**: 33/35 families qualify

### When to Discount Volume Loss

Consider reducing or excluding volume loss when:

1. **Processing brown or purple**: These families show unstable volume estimates
2. **Very small sample sizes**: < 500 samples (use centroid-only)
3. **Extreme outliers present**: Consider alpha-shape first

### Weight Recommendations

Based on Phase 5.1 and 5.2 findings:

| Scenario | Centroid | Volume | Shape |
|----------|----------|--------|-------|
| Standard (stable) | 0.2 | 0.6 | 0.2 |
| Unstable families | 0.6 | 0.1 | 0.3 |
| Minimal samples | 1.0 | 0.0 | 0.0 |

---

## 5. Actionable Recommendations

### For Phase 5.3+ Implementation

1. **Use volume-only optimization** for best overall results (Task 92 finding)

2. **Apply global scaling factor** (2054.70) for volume normalization

3. **Flag brown and purple** as problematic - consider:
   - Downweighting volume loss
   - Using alternative bounding methods
   - Manual review of transformation quality

4. **Minimum sample threshold**: Require ≥3,000 samples for new families

5. **Monitor CV during bootstrap**: If CV > 0.05, flag for review

### For Visualization Development (Task 114)

Priority visualizations based on this analysis:

1. **Jacobian heatmap**: 2D projection showing spatial uniformity
2. **Volume convergence curves**: CV vs N for each family
3. **Correction factor distribution**: Histogram (should be extremely narrow)
4. **Problem family scatter**: brown and purple sample distributions

---

## 6. Summary Statistics

### Phase 5.2 Experiment Registry

| ID | Task | Method | Key Finding |
|----|------|--------|-------------|
| EXP-022 | 98 | Jacobian computation | CV = 0.02, uniform |
| EXP-023 | 99 | Per-family Monte Carlo | All identical |
| EXP-024 | 100 | Bootstrap resampling | 94.3% stable |

### Files Generated

| File | Description |
|------|-------------|
| jacobian_analysis.json | Spatial Jacobian statistics |
| jacobian_map.json | 3375-point spatial distribution |
| per_family_volume_ratios.json | Per-family correction factors |
| sample_size_analysis.json | Bootstrap results |
| research_observations.md | Detailed experiment logs |

---

## Conclusion

Phase 5.2 establishes that volume matching is reliable and straightforward:

1. **Uniform transformation**: CV = 0.02 across color space
2. **No family-specific corrections**: Max deviation 0.11%
3. **Adequate sampling**: 94.3% of families are stable
4. **Simple implementation**: Single global scaling factor

The RGB→Munsell volume transformation is remarkably well-behaved, enabling robust volume-based
loss functions for screen-to-surface color transformation.

**Next Phase**: 5.3 (Shape-Statistical Methods) for improved shape preservation beyond the
current 0.13-0.18 shape loss floor identified in Phase 5.1.
