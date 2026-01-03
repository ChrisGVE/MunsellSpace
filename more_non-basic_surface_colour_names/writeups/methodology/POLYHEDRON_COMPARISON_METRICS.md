# Polyhedron Comparison Metrics for Color Space Analysis

## Executive Summary

This document reviews metrics for comparing 3D polyhedra in Munsell color space, specifically for assessing transformations between screen-color-derived and surface-color-derived semantic color family regions. These metrics support the search for optimal transformations (Task 64) and validation of transformation quality (Task 65).

## 1. Volume-Based Metrics

### 1.1 Volume Ratio

The most basic comparison metric is the ratio of polyhedron volumes:

```
Volume Ratio = V₁ / V₂
```

**Properties:**
- Simple to compute from convex hull volume
- Scale-dependent: sensitive to overall region size
- Does not capture shape similarity or spatial alignment
- Ratio > 1 indicates first polyhedron is larger

**Applications:**
- Quick sanity check for extreme size mismatches
- Screening transformations that produce unrealistic volume changes
- Combined with other metrics for comprehensive assessment

**Implementation:** Available via `scipy.spatial.ConvexHull.volume` attribute.

### 1.2 Jaccard Index (3D Intersection over Union)

The [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index), also known as Intersection over Union (IoU), measures overlap between volumes:

```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

**Properties:**
- Range: [0, 1] where 1 indicates perfect overlap
- Symmetric: Jaccard(A, B) = Jaccard(B, A)
- Translation and rotation invariant
- Captures both size and alignment simultaneously

**Computational Challenges:**
- Computing 3D volume intersection requires halfspace intersection
- Union volume: |A ∪ B| = |A| + |B| - |A ∩ B|
- Intersection requires combining halfspace representations

**Extensions:**

[Generalized Intersection over Union (GIoU)](https://giou.stanford.edu/GIoU.pdf) addresses limitations when shapes don't intersect:

```
GIoU(A, B) = IoU(A, B) - |C \ (A ∪ B)| / |C|
```

where C is the smallest convex hull enclosing both A and B. GIoU maintains gradients even when IoU = 0, making it superior for optimization tasks.

**Research Applications:**
- [3D object comparison research](https://www.researchgate.net/publication/314691464_3D_Objects_Comparison_Using_New_Approach_Based_Similarity_Index) demonstrates Jaccard similarity for meshes and polyhedra
- Widely used in computer vision for bounding box and segmentation comparison

**Implementation:** Requires halfspace intersection via `scipy.spatial.HalfspaceIntersection`.

### 1.3 Volume Intersection Calculation

Given two convex polyhedra P₁ and P₂:

1. Convert each polyhedron to halfspace representation (Ax ≤ b)
2. Combine halfspaces: intersection satisfies all constraints from both
3. Find feasible interior point for `HalfspaceIntersection`
4. Compute convex hull of intersection vertices
5. Extract volume from resulting hull

**Halfspace Representation:**
Each facet of a convex hull defines a halfspace. [SciPy's ConvexHull](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html) provides this via the `equations` attribute: `[normal_x, normal_y, normal_z, offset]` where `normal · x + offset = 0` on the facet and `normal · x + offset ≤ 0` inside the hull.

**Interior Point Selection:**
[SciPy's HalfspaceIntersection](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.HalfspaceIntersection.html) requires a feasible interior point. For convex hulls, the centroid of either polyhedron is typically feasible if the polyhedra overlap. Otherwise, linear programming can find a feasible point, or use the midpoint between centroids.

## 2. Centroid-Based Metrics

### 2.1 Centroid Displacement

Euclidean distance between polyhedron centroids in Munsell Cartesian space:

```
Δcentroid = ||c₁ - c₂||₂ = √[(x₁-x₂)² + (y₁-y₂)² + (z₁-z₂)²]
```

**Properties:**
- Intuitive interpretation: "how far did the region move?"
- Translation-variant by design (measures translation)
- Independent of shape and volume
- Units: Munsell units in Cartesian space

**Applications:**
- Assess global shifts in hue/chroma/value
- Identify systematic biases (e.g., "all colors shifted brighter")
- Combined with volume metrics for comprehensive assessment

**Benchmarks from Centore (2020) comparison:**
- Average centroid shift: 3.21 Munsell units
- Range: 0.5 (lime) to 7.44 (purple)
- Most families shifted lighter (23 of 27 analyzed)

**Implementation:** Direct calculation from polyhedron centroid coordinates.

### 2.2 Centroid as Representative Point

The centroid serves as a single representative point for complex regions. For convex polyhedra:

```
centroid = (1/n) ∑ vᵢ
```

where vᵢ are vertices in Munsell Cartesian coordinates [x, y, z].

**Alternative:** For non-uniformly distributed samples, the median center or weighted centroid may be more robust to outliers.

## 3. Shape Similarity Metrics

### 3.1 Hausdorff Distance

The [Hausdorff distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance) measures maximum deviation between two sets:

```
dₕ(A, B) = max(h(A, B), h(B, A))
```

where the directed Hausdorff distance is:

```
h(A, B) = max_{a∈A} min_{b∈B} ||a - b||
```

**Properties:**
- Measures worst-case mismatch between surfaces
- Asymmetric in directed form: h(A, B) ≠ h(B, A)
- Symmetric in standard form: dₕ(A, B) = dₕ(B, A)
- Sensitive to outliers (single far vertex dominates)

**Computational Complexity:**
- Naive: O(|A| × |B|) for finite point sets
- [Efficient algorithms exist](https://link.springer.com/article/10.1007/s00454-023-00562-5) for special cases
- For polyhedra: typically computed on vertex sets or surface points

**Applications:**
- Quality assessment for point cloud registration
- [Shape matching and pattern recognition](https://link.springer.com/chapter/10.1007/978-3-642-55566-4_4)
- Surface deviation analysis in manufacturing

**Limitations for Color Space:**
- Single outlier vertex can skew results
- Does not capture interior structure or volume
- May not reflect perceptual color region similarity

**Recent Research:**
- [Generalized Hausdorff distance for point cloud quality](https://arxiv.org/abs/2003.13669) (2020)
- Work on budgeted and directed Hausdorff distance approximations (2026)

**Implementation:** Iterate over vertices of each polyhedron to find max-min distances.

### 3.2 Average Hausdorff Distance

A more robust variant:

```
d_avg(A, B) = (1/2)[avg_{a∈A} min_{b∈B} ||a - b|| + avg_{b∈B} min_{a∈A} ||a - b||]
```

**Advantages:**
- Reduces sensitivity to outliers
- Better represents typical surface deviation
- More stable for optimization

### 3.3 Bidirectional Surface Distance

For dense surface representations, compute distances from sampled points on each polyhedron's surface:

1. Sample points uniformly on each facet
2. For each point on P₁, find nearest point on P₂ surface
3. Compute mean, median, and percentile distances
4. Repeat in reverse direction

**Metrics:**
- Mean surface distance
- Median surface distance
- 95th percentile distance (robust outlier measure)
- Root mean square (RMS) distance

## 4. Vertex Correspondence Metrics

### 4.1 Optimal Transport and Wasserstein Distance

The Wasserstein distance measures the minimum cost to transform one probability distribution into another. For discrete point clouds representing polyhedra vertices:

```
W₂(μ, ν) = min_{π∈Π(μ,ν)} [∫∫ ||x - y||² dπ(x,y)]^(1/2)
```

where π is a transport plan (coupling) between distributions μ and ν.

**Properties:**
- Accounts for point-to-point correspondence
- Sensitive to both position and density
- Computationally expensive for large point sets
- Requires solving linear programming problem

**Applications in Shape Analysis:**
- [Point cloud alignment and comparison](https://arxiv.org/html/2503.06838)
- Measures geometric similarity while allowing deformation
- Foundation for modern shape matching algorithms

**Computational Methods:**
- Exact: linear programming solvers (O(n³ log n))
- Approximate: Sinkhorn iterations (faster, regularized)
- Python: `scipy.stats.wasserstein_distance` (1D), `POT` library (multi-D)

### 4.2 Procrustes-Wasserstein Distance

[Recent research (2025)](https://arxiv.org/abs/2507.00894) introduced Procrustes-Wasserstein (PW) distance, combining optimal transport with geometric alignment:

```
PW(μ, ν) = min_{R,t} W₂(μ, R(ν) + t)
```

where R is an orthogonal transformation (rotation/reflection) and t is translation.

**Key Properties:**
- Invariant to rigid transformations
- True metric (satisfies triangle inequality)
- Combines benefits of Procrustes and Wasserstein
- Suitable for comparing point clouds in different orientations

**Advantages over Standard Wasserstein:**
- Naturally handles rotated/mirrored shapes
- Recovers rigid transformation as byproduct
- More robust to pose variation

**Applications:**
- [Shape clustering and tracking](https://openreview.net/forum?id=bp975dIAjt)
- Archaeological applications (bone morphology evolution)
- 2D/3D point cloud comparison

**Relation to Gromov-Wasserstein:**
PW shares rotational invariance with Gromov-Wasserstein but is computationally simpler and provides explicit transformation recovery.

## 5. Optimal Alignment Metrics

### 5.1 Procrustes Analysis

[Procrustes analysis](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance) finds the optimal rigid transformation (rotation, translation, optionally scaling) to align two point sets:

```
min_{R,t,s} ∑ᵢ ||sR·xᵢ + t - yᵢ||²
```

**Solution via SVD:**

1. Center both point sets (subtract centroids)
2. Compute cross-covariance matrix: H = X^T Y
3. SVD: H = U Σ V^T
4. Optimal rotation: R = V U^T
5. Handle reflection: if det(R) < 0, flip last column of V
6. Optimal translation: t = ȳ - R·x̄
7. Optimal scale: s = tr(Σ) / tr(X^T X)

**Procrustes Distance:**
After optimal alignment, the residual error:

```
d_Procrustes = √[∑ᵢ ||R·xᵢ + t - yᵢ||²]
```

**Properties:**
- Removes pose variation to focus on shape difference
- Provides interpretable transformation parameters
- [SciPy implementation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.procrustes.html): `scipy.spatial.procrustes`
- Requires point correspondence (same number of points)

**Applications:**
- [3D point cloud registration](https://www.daniellowengrub.com/blog/2019/05/14/point-cloud-alignment)
- Shape morphometrics
- Medical imaging alignment
- [Archaeological artifact comparison](https://github.com/bmershon/procrustes)

**For Unequal Point Sets:**
Use Iterative Closest Point (ICP) to establish correspondence:

1. Find nearest neighbors between point sets
2. Compute Procrustes alignment on correspondences
3. Iterate until convergence

### 5.2 PCA-Based Alignment

[Principal Component Analysis alignment](https://www.algosome.com/articles/pca-three-dimensions-point-cloud.html) provides a canonical orientation:

**Algorithm:**

1. Center point cloud at origin
2. Compute covariance matrix C = (1/n) X^T X
3. Eigendecomposition: C = V Λ V^T
4. Align to principal axes: X' = X V

**Properties:**
- Fast: O(n) for covariance, O(1) for eigendecomposition (3×3 matrix)
- Provides unique orientation (up to reflection ambiguity)
- Basis for rotation-invariant features
- Used for [initial rough alignment](https://www.researchgate.net/publication/313542364_3D_point_cloud_matching_based_on_principal_component_analysis_and_iterative_closest_point_algorithm)

**Limitations:**
- Sign ambiguity in eigenvectors (reflection)
- Fails for spherical/symmetric distributions
- Less robust than Procrustes for point correspondence

**Combined Approach:**
1. PCA alignment for initial rough orientation
2. ICP for fine-tuning correspondence
3. Procrustes for final rigid transformation

### 5.3 Kabsch Algorithm

Special case of Procrustes without scaling, commonly used in molecular biology:

[Finding optimal rotation and translation](https://nghiaho.com/?page_id=671):

1. Center both point sets
2. Compute H = ∑ᵢ (xᵢ - x̄)(yᵢ - ȳ)^T
3. SVD: H = U S V^T
4. Compute rotation: R = V U^T
5. Correct for reflection: if det(R) = -1, flip sign of last column of V

**Guaranteed to find optimal rotation matrix** (det(R) = 1, R^T R = I).

## 6. Fréchet Distance (Limited Applicability)

The [Fréchet distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance) is primarily defined for curves (1D manifolds):

```
δ_F(P, Q) = inf_{α,β} max_{t∈[0,1]} d(P(α(t)), Q(β(t)))
```

where α and β are continuous, non-decreasing reparametrizations.

**Intuition:** The "dog leash" distance - minimum leash length needed for a person and dog to traverse separate paths.

**Applications:**
- [Polygonal curve similarity](https://www.semanticscholar.org/paper/Computing-Discrete-Fr%C3%A9chet-Distance-%E2%88%97-Eiter-Mannila/3642e114b0329edca7f1731339103af4c1feca98)
- [3D polygonal chain simplification](https://link.springer.com/chapter/10.1007/978-3-540-78773-0_54)
- Trajectory similarity
- Handwriting recognition

**Discrete Fréchet Distance:**
For polygonal curves with vertices:
```
δ_dF(P, Q) = min_L max_{(p,q)∈L} d(p, q)
```
over all valid couplings L. [Computable in O(mn) time](http://cgm.cs.mcgill.ca/~athens/cs507/Projects/2002/StephanePelletier/) via dynamic programming.

**Extensions to Surfaces:**
- [Fréchet distance on polyhedral surfaces](https://link.springer.com/article/10.1007/s00453-012-9723-6) exists but is computationally expensive
- O(M⁶ log² M) for convex surfaces
- O(M⁷ log² M) for non-convex surfaces

**Limitations for Color Space Polyhedra:**
- Designed for 1D curves, not 3D volumes
- No standard definition for arbitrary polyhedra comparison
- Surface-based variants are computationally prohibitive
- Hausdorff or Wasserstein distances are more appropriate

**Note:** While Fréchet distance appears in image generation metrics (Fréchet Inception Distance), that usage measures distributional similarity in feature space, not geometric shape comparison.

## 7. Recommended Metrics for Color Space Transformation

Based on the literature review and computational tractability, the recommended metric suite for comparing screen vs. surface color polyhedra:

### Primary Metrics (Fast, Intuitive)

1. **Centroid Displacement** - Global translation assessment
2. **Volume Ratio** - Scale change assessment
3. **Jaccard Index (IoU)** - Overlap quality (if computable)

### Secondary Metrics (Shape Quality)

4. **Hausdorff Distance** - Maximum surface deviation
5. **Average Surface Distance** - Typical surface deviation

### Advanced Metrics (If Needed)

6. **Procrustes Distance** - After optimal alignment
7. **Wasserstein Distance** - Vertex distribution similarity

### Implementation Priority

**Phase 1 (Essential):**
- Centroid displacement ✓
- Volume ratio ✓
- Average Hausdorff distance ✓

**Phase 2 (Enhanced):**
- Jaccard index (requires halfspace intersection)
- Procrustes alignment and distance

**Phase 3 (Research):**
- Wasserstein/Procrustes-Wasserstein distance
- GIoU for non-overlapping cases

## 8. Computational Considerations

### SciPy/NumPy Stack

**Available:**
- `scipy.spatial.ConvexHull` - Volume, vertices, equations, facets
- `scipy.spatial.HalfspaceIntersection` - Volume intersection
- `scipy.spatial.procrustes` - Procrustes alignment
- `scipy.stats.wasserstein_distance` - 1D Wasserstein (not suitable for 3D)
- `numpy.linalg` - SVD, eigendecomposition

**External Libraries:**
- [POT (Python Optimal Transport)](https://pythonot.github.io/) - Multi-dimensional Wasserstein
- [frechetdist](https://pypi.org/project/frechetdist/) - Discrete Fréchet for curves
- [Polyhedra.jl](http://juliapolyhedra.github.io/Polyhedra.jl/stable/generated/Convex%20hull%20and%20intersection/) (Julia) - Reference implementation

### Computational Complexity

| Metric | Complexity | Notes |
|--------|-----------|-------|
| Centroid displacement | O(n) | n = vertex count |
| Volume ratio | O(1) | From precomputed hulls |
| Hausdorff distance | O(nm) | n, m = vertex counts |
| Jaccard index | O((n+m)³) | Halfspace intersection |
| Procrustes | O(n) | After centering, O(1) SVD (3×3) |
| Wasserstein | O(n³ log n) | Exact optimal transport |

## 9. References and Citations

### Primary Literature

1. Jaccard Index: [Wikipedia - Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index)

2. Generalized IoU: Rezatofighi et al. (2019). [Generalized Intersection over Union](https://giou.stanford.edu/GIoU.pdf). CVPR 2019.

3. Hausdorff Distance: [Wikipedia - Hausdorff Distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance)

4. Computing Hausdorff Distance: Alt et al. (1995). [Computing the Hausdorff Distance of Geometric Patterns and Shapes](https://link.springer.com/chapter/10.1007/978-3-642-55566-4_4). Springer.

5. Generalized Hausdorff Distance: Alexiou et al. (2020). [A Generalized Hausdorff Distance Based Quality Metric for Point Cloud Geometry](https://arxiv.org/abs/2003.13669). IEEE QoMEX 2020.

6. Procrustes-Wasserstein Distance: Delon et al. (2025). [An in depth look at the Procrustes-Wasserstein distance: properties and barycenters](https://arxiv.org/abs/2507.00894). ICML 2025.

7. Wasserstein Alignment: Grave et al. (2018). [Unsupervised Alignment of Embeddings with Wasserstein Procrustes](https://www.researchgate.net/publication/325439455_Unsupervised_Alignment_of_Embeddings_with_Wasserstein_Procrustes).

8. Fréchet Distance: [Wikipedia - Fréchet Distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance)

9. Discrete Fréchet Distance: Eiter & Mannila (1994). [Computing Discrete Fréchet Distance](https://www.semanticscholar.org/paper/Computing-Discrete-Fr%C3%A9chet-Distance-%E2%88%97-Eiter-Mannila/3642e114b0329edca7f1731339103af4c1feca98).

10. 3D Polygonal Chains: Bereg & Wang (2008). [Simplifying 3D Polygonal Chains Under the Discrete Fréchet Distance](https://link.springer.com/chapter/10.1007/978-3-540-78773-0_54). LATIN 2008.

### Computational Geometry Resources

11. SciPy ConvexHull: [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html)

12. SciPy HalfspaceIntersection: [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.HalfspaceIntersection.html)

13. SciPy Procrustes: [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.procrustes.html)

14. Qhull Library: [Qhull Documentation](http://www.qhull.org/) - Underlying convex hull implementation

### Applied Research

15. 3D Object Comparison: Ben Haj Yahia et al. (2017). [3D Objects Comparison Using New Approach Based Similarity Index](https://www.researchgate.net/publication/314691464_3D_Objects_Comparison_Using_New_Approach_Based_Similarity_Index).

16. Point Cloud Registration: [Point Cloud Alignment Tutorial](https://www.daniellowengrub.com/blog/2019/05/14/point-cloud-alignment)

17. PCA for Point Clouds: [PCA for 3-Dimensional Point Cloud](https://www.algosome.com/articles/pca-three-dimensions-point-cloud.html)

18. Optimal Rotation: [Finding Optimal Rotation and Translation](https://nghiaho.com/?page_id=671) - Kabsch algorithm tutorial

19. PCA + ICP Alignment: Zhang (2016). [3D point cloud matching based on PCA and ICP](https://www.researchgate.net/publication/313542364_3D_point_cloud_matching_based_on_principal_component_analysis_and_iterative_closest_point_algorithm).

### Color Space Context

20. Centore, P. (2020). An Open-Source Inversion Algorithm for the Munsell Renotation. *Color Research & Application*, 45(5), 858-873. (Provides benchmark for centroid displacement)

---

**Document Version:** 1.0
**Last Updated:** 2026-01-03
**Related Tasks:** Task 63 (Literature Review), Task 64 (Transformation Search), Task 65 (Validation)
**Author:** Research Analyst Agent
