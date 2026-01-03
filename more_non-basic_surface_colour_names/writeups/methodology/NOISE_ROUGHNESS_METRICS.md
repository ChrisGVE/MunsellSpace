# Noise and Roughness Metrics for Polyhedra Analysis

## Overview

This document describes metrics for assessing the noise and roughness characteristics of polyhedra constructed from color naming data. These metrics help identify calibration issues, outliers, and data quality problems in the semantic color family boundaries.

## 1. Surface-to-Volume Ratio (Isoperimetric Ratio)

### Theory

The surface-to-volume ratio provides a fundamental measure of polyhedron roughness. For a given volume, smooth shapes minimize surface area due to the isoperimetric inequality (Bourke, 2009; Wikipedia contributors, 2025a).

For a 3D shape, we can compute a normalized roughness metric:

```
R = S / V^(2/3)
```

Where:
- `S` = surface area
- `V` = volume
- The exponent 2/3 normalizes for scale (since area scales as length² and volume as length³)

### Reference Values

The sphere achieves the theoretical minimum surface-to-volume ratio:

- **Sphere**: R = 4.84 (for unit sphere: S = 4πr², V = (4/3)πr³)
- **Cube**: R ≈ 6.00
- **Regular tetrahedron**: R ≈ 7.21

Any polyhedron with R > 4.84 exhibits some degree of roughness. Values significantly above theoretical smooth shapes indicate:
- Irregular vertex distribution
- Presence of outliers creating spikes
- Non-uniform data density
- Potential calibration noise

### Application to Color Families

For color family polyhedra:
1. Compute R for each family
2. Compare against theoretical minimum (4.84)
3. Identify families with anomalously high roughness
4. Investigate high-roughness families for data quality issues

### Implementation Considerations

- Surface area: sum of triangle face areas from convex hull
- Volume: computed via divergence theorem or signed tetrahedron volumes
- Sensitivity: metric increases rapidly with surface irregularities

**References:**
- Wikipedia contributors. (2025a). Isoperimetric inequality. https://en.wikipedia.org/wiki/Isoperimetric_inequality
- Wikipedia contributors. (2025b). Surface-area-to-volume ratio. https://en.wikipedia.org/wiki/Surface-area-to-volume_ratio

## 2. Alpha Shapes Analysis

### Theory

Alpha shapes generalize convex hulls by allowing concavities at a scale controlled by parameter α (Edelsbrunner et al., 1983). An alpha shape can be conceptualized as carving out space using a "cookie scoop" of radius 1/α without removing points (Wikipedia contributors, 2025c).

**Key properties:**
- α = 0: convex hull (no concavities)
- α → ∞: individual points (maximum concavity)
- Intermediate α: shape fitting at specific granularity

### Parameter Selection Strategies

Several approaches exist for selecting α (GitHub contributors, 2024; BMC Ecology and Evolution, 2018):

#### 1. Maximum Coverage (Conservative)
Calculate the largest α that includes all data points:
```python
alpha_max = max_distance_to_nearest_neighbor / 2
```

#### 2. Optimization Methods
Minimize number of connected components while including all points (CGAL, 2025).

#### 3. Adaptive/Local Alpha
Define α locally based on point density:
```python
alpha_local(region) = f(point_density(region))
```

This creates tighter fitting in dense regions, looser in sparse regions.

#### 4. Visual/Iterative Selection
- Start with convex hull (α = 0)
- Incrementally increase α
- Stop when shape reasonably fits without losing points

### Multi-Scale Analysis

Computing alpha shapes at multiple α values reveals structure at different scales:

```python
alpha_values = [0, 0.5, 1.0, 2.0, 5.0, 10.0]
shapes = [compute_alpha_shape(points, a) for a in alpha_values]
```

**Interpretation:**
- Rapid volume decrease with α: presence of outliers or sparse regions
- Gradual volume decrease: uniform, dense distribution
- Multiple disconnected components: clustering or gaps in data

### Roughness via Alpha Shape Comparison

Compare volumes at different α levels:

```
hull_ratio(α) = V_alpha / V_convex_hull
```

A smooth distribution shows gradual ratio decrease. Abrupt drops indicate:
- Outliers far from main cluster
- Sparse data regions
- Potential calibration errors

**References:**
- Edelsbrunner, H., Kirkpatrick, D., & Seidel, R. (1983). On the shape of a set of points in the plane. IEEE Transactions on Information Theory, 29(4), 551-559.
- Wikipedia contributors. (2025c). Alpha shape. https://en.wikipedia.org/wiki/Alpha_shape
- BMC Ecology and Evolution. (2018). Alpha shapes: determining 3D shape complexity across morphologically diverse structures. https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-018-1305-z
- GitHub contributors. (2024). panosz/alpha_shapes: A Python library for working with alpha shapes. https://github.com/panosz/alpha_shapes
- CGAL. (2025). 3D Alpha Shapes: User Manual. https://doc.cgal.org/latest/Alpha_shapes_3/index.html

## 3. Convex Hull vs. Bounding Polyhedron

### Comparative Analysis

Comparing different bounding representations reveals distribution characteristics:

1. **Convex Hull**: Minimal convex container
2. **Oriented Bounding Box (OBB)**: Minimal volume box aligned to principal axes
3. **Axis-Aligned Bounding Box (AABB)**: Box aligned to coordinate axes
4. **Minimum Volume Ellipsoid (MVE)**: Smoothest approximation

**Useful ratios:**
```
compactness = V_convex_hull / V_bounding_box
sphericity = V_convex_hull / V_bounding_sphere
```

Values near 1.0 indicate compact, regular distributions. Lower values suggest elongated or sparse distributions.

**References:**
- GitHub contributors. (2024). gabyx/ApproxMVBB: Fast algorithms to compute an approximation of the minimal volume oriented bounding box. https://github.com/gabyx/ApproxMVBB

## 4. Fractal Dimension

### Box-Counting Dimension

The box-counting (Minkowski-Bouligand) dimension quantifies how point distribution scales with resolution (Bourke, 2009; Wikipedia contributors, 2025d).

**Algorithm:**
1. Cover point set with grid of boxes of size s
2. Count number of non-empty boxes N(s)
3. Repeat for decreasing box sizes: s₁ > s₂ > s₃ > ...
4. Plot log(N(s)) vs log(1/s)
5. Fractal dimension D = slope of linear fit

**Expected dimensions:**
- **D ≈ 2.0**: Points lie on a smooth surface
- **2.0 < D < 3.0**: Points fill space with fractal structure
- **D ≈ 3.0**: Points densely fill 3D volume

**Implementation notes:**
- Use logarithmic spacing for box sizes: s = 2^(-k) for k = 1, 2, 3, ...
- Typical range: max_extent/2 down to min_point_separation
- Require at least 5-10 different box sizes for reliable slope
- Remove edge effects by extending grid slightly beyond data bounds

**References:**
- Wikipedia contributors. (2025d). Box counting. https://en.wikipedia.org/wiki/Box_counting
- Bourke, P. (2009). Estimating fractal dimension of point datasets. https://paulbourke.net/fractals/fdpoints/
- Moisy, F. (2008). Computing a fractal dimension with Matlab: 1D, 2D and 3D Box-counting. http://www.fast.u-psud.fr/~moisy/ml/boxcount/html/demo.html

### Correlation Dimension

Alternative to box-counting, based on correlation integral:

```
C(r) = (1/N²) × Σᵢⱼ Θ(r - |xᵢ - xⱼ|)
```

Where Θ is the Heaviside step function. Correlation dimension:

```
D₂ = lim(r→0) [d log C(r) / d log r]
```

**Advantages over box-counting:**
- Less sensitive to edge effects
- More statistically robust for small datasets
- Better for point clouds vs. solid objects

**Application:**
- Compare D₂ across color families
- Families with higher dimensions may have more complex/noisy boundaries
- Significant deviations suggest outliers or multiple sub-clusters

**References:**
- Grassberger, P., & Procaccia, I. (1983). Measuring the strangeness of strange attractors. Physica D: Nonlinear Phenomena, 9(1-2), 189-208.
- Eckmann, J. P., & Ruelle, D. (1985). Ergodic theory of chaos and strange attractors. Reviews of Modern Physics, 57(3), 617-656.

### Relevance to Calibration Noise

Fractal dimension helps distinguish:

**Clean data (D ≈ 2.0-2.3):**
- Points lie near smooth boundary surface
- Consistent naming patterns
- Reliable semantic boundaries

**Noisy data (D > 2.5):**
- Points scattered throughout volume
- Inconsistent color naming
- Potential RGB-to-Munsell conversion artifacts
- Outliers from annotation errors

**Under-sampled data (D < 2.0):**
- Insufficient data points
- Gaps in coverage
- May miss true boundary extent

## 5. Outlier Sensitivity Analysis

### Methodology

Assess how polyhedron properties change when potential outliers are removed:

1. Compute baseline metrics (volume, surface area, centroid)
2. Identify potential outliers using robust statistics
3. Iteratively remove outliers at different thresholds
4. Track metric changes

**Sensitivity score:**
```
sensitivity = (metric_original - metric_filtered) / metric_original
```

High sensitivity indicates:
- Outliers significantly influence boundary
- Possible data quality issues
- Need for manual review of extreme points

### Statistical Distances for Outlier Detection

**Mahalanobis Distance:**
```
D_M(x) = sqrt((x - μ)ᵀ Σ⁻¹ (x - μ))
```

Where μ is mean and Σ is covariance matrix. Points with D_M > threshold are outliers.

**Isolation Forest:**
Uses tree-based anomaly detection. Points requiring few splits to isolate are outliers.

**Local Outlier Factor (LOF):**
Compares local density of point to neighbors. Isolated points have high LOF scores.

**References:**
- Mahalanobis, P. C. (1936). On the generalized distance in statistics. Proceedings of the National Institute of Sciences of India, 2, 49-55.
- Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation forest. IEEE International Conference on Data Mining, 413-422.

## 6. Robust Statistics for Outlier Detection

### Median Absolute Deviation (MAD)

MAD is a robust alternative to standard deviation:

```
MAD = median(|xᵢ - median(x)|)
```

**Modified Z-score:**
```
M = 0.6745 × (x - median(x)) / MAD
```

**Outlier criterion:**
- |M| > 3.5: potential outlier (conservative)
- |M| > 2.5: liberal outlier threshold

**Advantages:**
- Not affected by extreme values (breakdown point = 50%)
- Works well with small samples
- Computationally simple

### Interquartile Range (IQR)

IQR measures spread of middle 50% of data:

```
IQR = Q₃ - Q₁
```

**Outlier fences:**
- Lower fence: Q₁ - 1.5 × IQR
- Upper fence: Q₃ + 1.5 × IQR
- Extreme outliers: Q₁ - 3.0 × IQR or Q₃ + 3.0 × IQR

**Multivariate extension:**
Use coordinate-wise IQR or leverage bagplot concept (Rousseeuw et al., 1999).

### Bagplot for Multivariate Outliers

Extension of boxplot to 2D/3D using depth contours and convex hulls:

1. Compute depth of each point (how central it is)
2. Bag = central 50% by depth (analogous to IQR)
3. Fence = inflated bag by factor (typically 3.0)
4. Outliers = points outside fence

**References:**
- Rousseeuw, P. J., Ruts, I., & Tukey, J. W. (1999). The bagplot: a bivariate boxplot. The American Statistician, 53(4), 382-387.
- Medium. (2024). Outlier Detection and Treatment: Z-score, IQR, and Robust Methods. https://medium.com/@aakash013/outlier-detection-treatment-z-score-iqr-and-robust-methods-398c99450ff3

### Convex Hull Peeling (Onion Peeling)

Iterative algorithm for identifying multivariate outliers:

1. Compute convex hull of all points
2. Flag hull vertices as potential outliers
3. Remove hull vertices
4. Repeat on remaining points
5. Stop after k layers (typically 1-3 for outlier detection)

**Interpretation:**
- Points in outer layers are peripheral
- Consistent with geometric definition of outliers
- Naturally handles multivariate distributions

**References:**
- Eddy, W. F. (1982). Convex hull peeling. In COMPSTAT 1982 5th Symposium held at Toulouse 1982 (pp. 42-47).
- arXiv. (2018). Onion-Peeling Outlier Detection in 2-D data Sets. https://arxiv.org/pdf/1803.04964

### Application Strategy

For color family polyhedra:

1. **Compute MAD** for each Munsell coordinate (H, V, C separately)
2. **Compute multivariate distance** (Mahalanobis or convex hull layers)
3. **Cross-validate** outliers using multiple methods
4. **Manual inspection** of flagged points
5. **Document** decisions about inclusion/exclusion

## 7. Integration: Complete Analysis Pipeline

### Recommended Workflow

For each color family polyhedron:

**Step 1: Initial Metrics**
- Compute S/V ratio → roughness baseline
- Calculate fractal dimension → distributional complexity

**Step 2: Multi-Scale Analysis**
- Generate alpha shapes at 5-7 α values
- Plot volume ratio vs. α
- Identify abrupt transitions (outlier signatures)

**Step 3: Outlier Detection**
- Apply MAD/IQR per coordinate
- Compute Mahalanobis distance
- Perform convex hull peeling (2-3 layers)
- Create consensus outlier list

**Step 4: Sensitivity Analysis**
- Compute metrics with all points
- Remove top 5%, 10%, 15% outliers (by distance)
- Track relative changes in:
  - Volume
  - Surface area
  - Centroid location
  - Fractal dimension

**Step 5: Decision Making**
```
if sensitivity > 20% or fractal_dim > 2.5:
    flag for manual review
if S/V_ratio > 7.0:
    investigate for spikes/outliers
if alpha_shape_ratio drops > 30% for small α increase:
    examine peripheral points
```

### Quality Thresholds

Based on Phase 6 baseline analysis (see quality_assessment.json):

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| S/V Ratio | 4.8-6.0 | 6.0-7.0 | > 7.0 |
| Fractal Dim | 2.0-2.3 | 2.3-2.6 | > 2.6 |
| Outlier % | < 5% | 5-10% | > 10% |
| Volume Sensitivity | < 10% | 10-20% | > 20% |

## 8. Citations and References

### Academic Literature

1. Edelsbrunner, H., Kirkpatrick, D., & Seidel, R. (1983). On the shape of a set of points in the plane. *IEEE Transactions on Information Theory*, 29(4), 551-559.

2. Grassberger, P., & Procaccia, I. (1983). Measuring the strangeness of strange attractors. *Physica D: Nonlinear Phenomena*, 9(1-2), 189-208.

3. Eckmann, J. P., & Ruelle, D. (1985). Ergodic theory of chaos and strange attractors. *Reviews of Modern Physics*, 57(3), 617-656.

4. Rousseeuw, P. J., Ruts, I., & Tukey, J. W. (1999). The bagplot: a bivariate boxplot. *The American Statistician*, 53(4), 382-387.

5. Mahalanobis, P. C. (1936). On the generalized distance in statistics. *Proceedings of the National Institute of Sciences of India*, 2, 49-55.

6. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation forest. *IEEE International Conference on Data Mining*, 413-422.

7. Eddy, W. F. (1982). Convex hull peeling. In *COMPSTAT 1982 5th Symposium held at Toulouse 1982* (pp. 42-47).

### Online Resources

8. Wikipedia contributors. (2025a). Isoperimetric inequality. Retrieved January 3, 2026, from https://en.wikipedia.org/wiki/Isoperimetric_inequality

9. Wikipedia contributors. (2025b). Surface-area-to-volume ratio. Retrieved January 3, 2026, from https://en.wikipedia.org/wiki/Surface-area-to-volume_ratio

10. Wikipedia contributors. (2025c). Alpha shape. Retrieved January 3, 2026, from https://en.wikipedia.org/wiki/Alpha_shape

11. Wikipedia contributors. (2025d). Box counting. Retrieved January 3, 2026, from https://en.wikipedia.org/wiki/Box_counting

12. Bourke, P. (2009). Estimating fractal dimension of point datasets. Retrieved January 3, 2026, from https://paulbourke.net/fractals/fdpoints/

13. Bourke, P. (2009). Box counting fractal dimension of volumetric data. Retrieved January 3, 2026, from https://paulbourke.net/fractals/cubecount/

14. Moisy, F. (2008). Computing a fractal dimension with Matlab: 1D, 2D and 3D Box-counting. Retrieved January 3, 2026, from http://www.fast.u-psud.fr/~moisy/ml/boxcount/html/demo.html

### Software and Tools

15. BMC Ecology and Evolution. (2018). Alpha shapes: determining 3D shape complexity across morphologically diverse structures. Retrieved January 3, 2026, from https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-018-1305-z

16. GitHub contributors. (2024). panosz/alpha_shapes: A Python library for working with alpha shapes. Retrieved January 3, 2026, from https://github.com/panosz/alpha_shapes

17. GitHub contributors. (2024). Jon-Ting/fastbc: Fast computation of box-counting dimension for 3D binary images. Retrieved January 3, 2026, from https://github.com/jon-ting/fastbc

18. GitHub contributors. (2024). gabyx/ApproxMVBB: Fast algorithms to compute minimal volume oriented bounding box. Retrieved January 3, 2026, from https://github.com/gabyx/ApproxMVBB

19. CGAL. (2025). 3D Alpha Shapes: User Manual. Retrieved January 3, 2026, from https://doc.cgal.org/latest/Alpha_shapes_3/index.html

20. Alpha Shape Toolbox. (2024). Alpha Shape Toolbox Documentation. Retrieved January 3, 2026, from https://alphashape.readthedocs.io/en/latest/readme.html

21. Medium. (2024). Outlier Detection and Treatment: Z-score, IQR, and Robust Methods. Retrieved January 3, 2026, from https://medium.com/@aakash013/outlier-detection-treatment-z-score-iqr-and-robust-methods-398c99450ff3

22. arXiv. (2018). Onion-Peeling Outlier Detection in 2-D data Sets. Retrieved January 3, 2026, from https://arxiv.org/pdf/1803.04964

23. arXiv. (2011). Estimators of Fractal Dimension: Assessing the Roughness. Retrieved January 3, 2026, from https://arxiv.org/pdf/1101.1444

24. Frontiers in Physics. (2022). Anomaly Detection Based on Convex Analysis: A Survey. Retrieved January 3, 2026, from https://www.frontiersin.org/articles/10.3389/fphy.2022.873848/full

## Conclusion

These metrics provide a comprehensive toolkit for assessing polyhedron quality in the color naming project. By combining geometric measures (S/V ratio), topological analysis (alpha shapes), fractal characterization (box-counting), and robust statistics (MAD/IQR), we can systematically identify and address data quality issues, calibration noise, and outliers in semantic color boundaries.
