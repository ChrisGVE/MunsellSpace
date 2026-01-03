# Research Plan: Screen-to-Surface Color Polyhedra Transformation

## 1. Research Objective

**Primary Question:** Can we derive a systematic transformation between screen color polyhedra (crowdsourced RGB) and surface color polyhedra (spectrophotometric Munsell), such that screen color data can be used to predict or approximate surface color behavior?

**Secondary Questions:**
1. Is the transformation global (one function for all colors) or local (hue/value/chroma dependent)?
2. What is the nature of the transformation: linear, affine, polynomial, or requires deep learning?
3. Can we validate the assumption that large sample sizes cancel calibration noise?
4. How does the non-homogeneity of color spaces affect our analysis?

---

## 2. Foundational Assumptions

### Assumption 1: Polyhedra as Semantic Fuzziness
Color names represent fuzzy semantic categories. A polyhedron in Munsell space geometrically bounds the "acceptable" region for a color name. This is a modeling choice, not a physical truth.

### Assumption 2: Large N Cancels Calibration Noise
With sufficient samples, individual calibration differences (monitor variations, lighting conditions, observer differences) average out, revealing the "true" semantic center and extent of a color category.

**Validation Required:**
- Test distribution symmetry around centroids
- Account for non-homogeneous color spaces (Munsell is perceptually uniform but not geometrically uniform)
- Compare results in RGB space (more homogeneous but perceptually non-uniform)

### Assumption 3: Systematic Differences Are Learnable
The differences between screen and surface color perception are not random but systematic, arising from:
- Emissive (screen) vs. reflective (surface) light
- Monitor gamut limitations
- Crowdsourced naming conventions vs. professional color standards

---

## 3. Research Phases

### Phase 1: Literature Review & Methodology Design

#### 1.1 Polyhedron Comparison Metrics
- **Volume comparison**: Ratio, intersection, union (Jaccard index for 3D)
- **Centroid displacement**: Euclidean distance in Munsell Cartesian space
- **Shape similarity**: Hausdorff distance, Fréchet distance
- **Vertex correspondence**: Optimal transport / Wasserstein distance
- **Orientation alignment**: Principal component alignment, Procrustes analysis

#### 1.2 Color Space Transformations
- **Monitor gamut considerations**: sRGB, Adobe RGB, DCI-P3 gamuts
- **Non-linear monitor response**: Gamma correction, ICC profiles
- **Chromatic adaptation**: Bradford transform, von Kries adaptation
- **Munsell ↔ CIELAB ↔ XYZ ↔ RGB conversion chains**

#### 1.3 Non-Uniform Space Metrics
- **Perceptual uniformity**: Munsell is designed for perceptual uniformity
- **Geometric non-uniformity**: Chroma extends further at some hues than others
- **ΔE metrics**: CIEDE2000 vs Euclidean in Munsell Cartesian
- **Local metric tensors**: How "distance" varies across the space

#### 1.4 Noise & Roughness Metrics
- **Surface-to-volume ratio** of convex hulls
- **Convex hull vs. bounding polyhedron comparison**
- **Alpha shapes** for varying levels of detail
- **Fractal dimension** of point cloud boundaries
- **Outlier sensitivity**: Compare hull with/without outlier removal

---

### Phase 2: Data Preparation & Polyhedra Construction

#### 2.1 Augmented Surface Polyhedra
Starting point: Centore's 30 families from CAUS data

**Augmentation strategy:**
1. Load Centore's original polyhedra vertices
2. Add our collected surface data:
   - Golden/Williamsburg (286 native spectrophotometer readings) - HIGH confidence
   - NCS/RAL/RHS (6,036 RGB-derived) - MEDIUM confidence
3. Reconstruct convex hulls with augmented data
4. Compare augmented vs. original Centore polyhedra (should be similar if data is consistent)

#### 2.2 Screen Color Polyhedra
Source: 184K+ crowdsourced color names (XKCD, colorhexa, meodai, etc.)

**Construction strategy:**
1. Use existing family assignments (SBERT-based NLP)
2. Apply confidence thresholds (test multiple: 0.6, 0.7, 0.8, 0.9)
3. Convert RGB → Munsell Cartesian
4. Construct convex hulls per family
5. Document how many families survive each threshold

#### 2.3 Family Matching
- Start with Centore's 30 families as reference
- Match screen families to surface families by name
- If a family has insufficient surface data, drop it from comparison
- Document which families are lost and why

---

### Phase 3: High-Confidence Assignment

#### 3.1 Assignment Quality Criteria
For each color sample to be included:
1. **NLP confidence**: SBERT similarity score to family anchor
2. **Colorimetric consistency**: Munsell hue within expected range for family
3. **Source reliability**: Weight by data source quality

#### 3.2 Threshold Experiments
| Threshold | Expected Effect |
|-----------|-----------------|
| Low (0.5) | More points, more noise, larger polyhedra |
| Medium (0.7) | Balanced trade-off |
| High (0.9) | Fewer points, cleaner polyhedra, may lose families |

Run full analysis at multiple thresholds to understand sensitivity.

---

### Phase 4: Transformation Search

#### 4.1 Loss Function Design

**Primary loss components:**
```
L_total = w1 * L_centroid + w2 * L_volume + w3 * L_shape
```

Where:
- `L_centroid`: Distance between transformed screen centroid and surface centroid
- `L_volume`: Ratio difference |V_screen_transformed / V_surface - 1|
- `L_shape`: Shape similarity metric (Hausdorff, IoU, etc.)

**Alternative formulation (separated):**
```
L_centroid_only: Optimize centroid alignment ignoring volume
L_volume_only: Optimize volume match ignoring centroid
L_joint: Multi-objective optimization
```

#### 4.2 Transformation Classes

**Linear transformations:**
- Translation only: T(x) = x + b
- Scaling only: T(x) = Ax (diagonal A)
- Affine: T(x) = Ax + b
- Per-family affine: T_f(x) = A_f * x + b_f

**Non-linear transformations:**
- Polynomial: T(x) = Σ a_ijk * x^i * y^j * z^k
- Radial basis functions
- Thin-plate splines
- B-spline deformations

**Learned transformations:**
- MLP (multi-layer perceptron)
- Residual networks
- Variational approaches

#### 4.3 Transformation Domains

Test transformations in different spaces:
1. **Munsell Cartesian**: Direct transformation
2. **RGB before conversion**: Transform RGB, then convert to Munsell
3. **CIELAB intermediate**: RGB → LAB → transform → Munsell
4. **Hue-dependent**: Different transformations for different hue sectors

---

### Phase 5: Assumption Validation

#### 5.1 Large N Cancels Noise (Munsell Space)

For each color family with N samples:
```
1. Calculate centroid C = mean(samples)
2. Calculate residuals R_i = sample_i - C
3. Analyze residual distribution:
   - Covariance matrix Σ
   - Principal components
   - Test for symmetry (skewness in each PC direction)
   - Test for uniformity (chi-square test on angular distribution)
```

**Expected result for random calibration noise:**
- Residuals form ellipsoid (not sphere - space is non-homogeneous)
- Ellipsoid orientation should align with local Munsell geometry
- No systematic skewness

**Expected result for systematic bias:**
- Residuals show consistent skewness
- Direction of skewness reveals nature of bias

#### 5.2 Non-Homogeneity Considerations

Munsell space is perceptually uniform but geometrically non-uniform:
- Chroma extends further for some hues (yellow) than others (blue)
- Value scale is non-linear in physical luminance

**Approach:**
- Fit ellipsoid to each family's point cloud
- Compare ellipsoid orientation to expected local Munsell geometry
- Normalize residuals by local metric before symmetry tests

#### 5.3 RGB Space Validation

Complementary analysis in RGB space:
- More geometrically homogeneous (cubic)
- But perceptually non-uniform
- Gamut limitations (some colors unrepresentable)

Compare:
- Residual distributions in RGB vs Munsell
- Ellipsoid orientations
- Systematic biases

---

### Phase 6: Noise & Roughness Analysis

#### 6.1 Polyhedron Roughness Metrics

**Surface-to-volume ratio:**
```
Roughness = Surface_area / Volume^(2/3)
```
Higher values indicate more complex/jagged shapes.

**Hull comparison:**
- Compute convex hull (removes all concavities)
- Compute alpha shape (preserves some concavities)
- Compare volumes: V_alpha / V_hull
- Ratio near 1 = smooth; ratio << 1 = rough/jagged

**Outlier sensitivity:**
- Compute hull with all points
- Compute hull with outliers removed (e.g., 95th percentile)
- Compare: how much does hull shrink?

#### 6.2 Screen vs Surface Roughness Comparison

Hypothesis: Screen color polyhedra may be "rougher" due to:
- Individual calibration noise
- Naming inconsistencies
- Gamut edge effects

Test:
- Compare roughness metrics between screen and surface polyhedra for same families
- Is roughness correlated with sample size?
- Is roughness correlated with family (some colors more consistently named?)

---

### Phase 7: Synthesis & Research Directions

#### 7.1 Summary Deliverables
1. Best-fit transformation(s) with confidence intervals
2. Validation results for large-N assumption
3. Roughness comparison report
4. Recommendations for practical application

#### 7.2 Potential Research Extensions
- **Temporal analysis**: Do color semantics drift over time?
- **Cross-cultural comparison**: Different language color naming
- **Application-specific transformations**: Print vs. web vs. product design
- **Uncertainty quantification**: Probabilistic polyhedra

---

## 4. Success Criteria

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Transformation accuracy | Centroid error < 1.5 Munsell units | Mean across families |
| Family coverage | ≥ 25 of 30 families | Families with sufficient data |
| Assumption validation | p > 0.05 for symmetry tests | Statistical significance |
| Reproducibility | Consistent across threshold choices | Variance analysis |

---

## 5. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Insufficient surface data | Can't compute reliable surface polyhedra | Use conservative thresholds; document uncertainty |
| No learnable transformation exists | Research question answered negatively | Still valuable finding; document limitations |
| Non-homogeneity breaks assumptions | Invalid statistical tests | Use local metrics; transform to more uniform space |
| Overfitting to available data | Transformation doesn't generalize | Cross-validation; held-out test families |

---

## 6. Timeline & Dependencies

```
Phase 1 (Literature) ──┬──► Phase 2 (Data Prep) ──► Phase 3 (Assignment)
                       │                                    │
                       │                                    ▼
                       │                           Phase 4 (Transformation)
                       │                                    │
                       └──────────────────────────────────► │
                                                           ▼
                                              Phase 5 (Assumption Validation)
                                                           │
                                                           ▼
                                              Phase 6 (Noise Analysis)
                                                           │
                                                           ▼
                                              Phase 7 (Synthesis)
```

---

*Research plan created: 2026-01-03*
*Version: 1.0*
