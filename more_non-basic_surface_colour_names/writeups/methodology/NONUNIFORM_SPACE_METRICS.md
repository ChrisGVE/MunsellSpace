# Non-Uniform Space Metrics for Munsell Color Analysis

**Date**: 2026-01-03
**Status**: Research documentation for Phase 1.3
**Purpose**: Understanding perceptual uniformity, local metric tensors, and ΔE metrics for polyhedra comparison in non-homogeneous Munsell space

---

## Table of Contents

1. [Introduction](#introduction)
2. [Munsell Design Principles](#munsell-design-principles)
3. [MacAdam Ellipses and Just-Noticeable Differences](#macadam-ellipses-and-just-noticeable-differences)
4. [Color Discrimination Thresholds](#color-discrimination-thresholds)
5. [Geometric Non-Uniformity of Munsell Space](#geometric-non-uniformity-of-munsell-space)
6. [Value Scale Non-Linearity](#value-scale-non-linearity)
7. [ΔE Color Difference Metrics](#δe-color-difference-metrics)
8. [Local Metric Tensors and Distance Variations](#local-metric-tensors-and-distance-variations)
9. [Geodesic vs Euclidean Distance](#geodesic-vs-euclidean-distance)
10. [Application to Polyhedra Comparison](#application-to-polyhedra-comparison)
11. [References](#references)

---

## Introduction

Color spaces present a fundamental challenge: representing three-dimensional perceptual relationships in mathematical coordinate systems. While the goal is to create a perceptually uniform space where equal distances correspond to equal perceived color differences, achieving this ideal has proven impossible within standard Euclidean geometry.

This document examines the perceptual non-uniformities inherent in color spaces, particularly the Munsell system, and explores the metrics available for measuring color differences in this non-homogeneous space. These concepts are critical for comparing color polyhedra constructed from different data sources and for validating semantic overlay boundaries.

---

## Munsell Design Principles

### The Quest for Perceptual Uniformity

Albert H. Munsell, an American artist and educator working in the late 1800s and early 1900s, initially conceived of a three-dimensional color sphere as the basis for his color order system. However, through systematic experiments with human subjects studying color sensitivities of the visual system, he came to a revolutionary conclusion:

> **A color space based on human perception would not be naturally geometrically regular.**

### From Sphere to Tree

Munsell's human subject experiments revealed that people with normal color vision can differentiate between more variances in red than blue-green. This perceptual asymmetry forced Munsell to abandon the aesthetically pleasing sphere concept in favor of a three-dimensional "color tree" model with uneven branches based on equally perceived color differences.

As Munsell himself explained:
> "Desire to fit a chosen contour, such as the pyramid, cone, cylinder or cube, coupled with a lack of proper tests, has led to many distorted statements of color relations, and it becomes evident, when physical measurement of pigment values and chromas is studied, that no regular contour will serve."

### Three-Dimensional Structure

The Munsell system consists of three independent perceptually-based dimensions:

- **Hue (H)**: Measured along the circumference of horizontal circles (0-100 scale, where 100 = 360°)
- **Value (V)**: Vertical axis from 0 (black) to 10 (white), representing perceived lightness
- **Chroma (C)**: Radial distance from the neutral axis, representing color purity/saturation

These form cylindrical coordinates on an irregular color solid where, in each dimension, colors are as close to perceptually uniform as Munsell could make them through careful measurement of human visual responses.

**Sources**: [Nightingale - Perceptual Uniform Color](https://nightingaledvs.com/color-in-a-perceptual-uniform-way/), [Wikipedia - Munsell Color System](https://en.wikipedia.org/wiki/Munsell_color_system)

---

## MacAdam Ellipses and Just-Noticeable Differences

### MacAdam's 1942 Experiments

In 1942, David MacAdam at the University of Rochester performed landmark color matching experiments where observers tried to match pairs of colors (one fixed, one variable). The ellipse parameters derived from statistical variations in the matching are closely related to Just Noticeable Differences (JND).

MacAdam studied 25 colors and showed that the CIE XYZ color space is **not isotropic**. Instead of circles of perceived unit differences, the space contains ellipses in the xy chromaticity diagram that are elongated in chroma with respect to hue.

### The JND Concept

Colors inside each MacAdam ellipse are perceived as the same as the color at the center of the ellipse. The contour of the ellipse shows the just noticeable differences (JND) in the color space.

**Key Finding**: To make MacAdam ellipses more like circles, perceptually uniform color spaces are required. These ellipses are often interpreted as defining the local metric tensor at their centers.

### Implications for Color Science

MacAdam's work demonstrated conclusively that color perception is fundamentally non-uniform. This observation led to decades of research attempting to develop more perceptually uniform color spaces, including:

- CIE L\*u\*v\* (1976)
- CIE L\*a\*b\* (1976)
- More recent systems like CAM16-UCS and Jzazbz

However, even in these refined spaces, the MacAdam JND ellipses are still not rendered perfectly circular, as would be the case for a perfect uniform color space.

**Sources**: [Imatest - Color Difference Ellipses](https://www.imatest.com/2015/09/color-difference-ellipses/), [ResearchGate - MacAdam Ellipses](https://www.researchgate.net/figure/MacAdam-ellipses-plotted-on-the-CIE-1931-xy-chromaticity-diagram-9-The-ellipses-show_fig1_246546517)

---

## Color Discrimination Thresholds

### The Impossibility of a Perfect Euclidean Color Space

Researchers including Judd, Schrödinger, and Silberstein concluded through theoretical analysis that **no ideal color space, especially no three-dimensional Euclidean space**, supports geometrical properties where MacAdam ellipses (perceived unit differences of color) can lie on unit circles.

Judd termed this fundamental property of color perception the **"Super-importance of hue differences"** - the fact that small changes in hue are perceptually more significant than equivalent metric changes in other dimensions.

### Perceptual Threshold Values

Modern research on color difference thresholds has established approximate values for just noticeable differences:

- **ΔE ≈ 1.0**: Widely cited JND threshold in CIELAB
- **ΔE < 2.0**: Generally considered imperceptible under normal viewing conditions (CIEDE2000)
- **ΔE < 0.5**: Stringent tolerance for automotive coatings (CMC)

These thresholds vary depending on:
- The color difference formula used
- Viewing conditions
- Surface texture (smooth vs rough)
- Observer training and expectations

**Sources**: [Techkon - CIEDE2000 Formula](https://techkonusa.com/demystifying-the-cie-delta-e-2000-formula/), [Wikipedia - Color Difference](https://en.wikipedia.org/wiki/Color_difference)

---

## Geometric Non-Uniformity of Munsell Space

### Asymmetric Chroma Extent

One of the most striking features of the Munsell system is that **different areas of the color space have different maximal chroma coordinates**. This asymmetry arises from the nature of human vision and the physics of color stimuli.

#### Yellow vs Blue Asymmetry

- **Light yellow colors**: Considerably more potential chroma than light purples
- **Blue and purple**: Bulge outward at low values (darker tones)
- **Yellow**: Bulges outward at high values (lighter tones)

#### Quantitative Examples

At **Value 4**:
- Hues 10RP and 5R: Extend to chroma /14
- Hues 5Y and 10Y: Maximum chroma only /6

At **Value 8**:
- Hue 10YR: Extends to chroma /14
- Hues 10PB and 5P: Reach only /4

### Historical Development Insight

In 1898, Munsell painted a child's globe in subtly shifting shades, only to discover that the globe's perfect symmetry could not sufficiently map the differences in chroma strength between colors. By 1905, in his publication "A Color Notation," Munsell had moved to a tree as the conceptual model, since its unequal length branches could accommodate different hues, chroma, and value relationships.

### Documented Irregularities

Analysis of the Munsell renotation data has revealed several specific irregularities:

1. **Exaggerated chroma spacing**: Into yellow and yellow-green hues
2. **Hue displacement**: Lines of constant hue shift as lightness increases (especially in blue-greens)
3. **Curved hue lines**: Constant violet and green hues form curves rather than radial lines
4. **Wide hue gaps**: Particularly in green colors

These irregularities are not defects but rather accurate representations of human perceptual space.

**Sources**: [Wikipedia - Munsell Color System](https://en.wikipedia.org/wiki/Munsell_color_system), [Nightingale - Perceptual Uniform Color](https://nightingaledvs.com/color-in-a-perceptual-uniform-way/), [ResearchGate - Munsell Cylindrical Coordinates](https://www.researchgate.net/figure/a-The-Munsell-color-system-represented-in-cylindrical-coordinates-b-Illustration-of-the_fig1_393230475)

---

## Value Scale Non-Linearity

### Perceptual vs Physical Lightness

The Munsell value scale is intentionally designed to be **non-linear** with respect to physical luminance (Y) or reflectance. This non-linearity accounts for human perception of lightness, which does not scale linearly with the amount of light reflected.

### Mathematical Relationships

#### Original Square Root Function

To account for this perceptual non-linearity, the value was originally taken as the square root of the luminance:

```
V ∝ √Y
```

Although this was later redefined with more sophisticated functions to improve accuracy.

#### Judd's Fifth-Degree Polynomial

The modern Munsell value (V) scale is related to CIE luminance factor (Y) by a complex **fifth-degree polynomial equation** called Judd's polynomial. This equation was devised with measurements based on magnesium oxide, assigned an absolute reflectance of 1.026 for 45°/0° illumination and viewing.

### Cube Root Transformation

Research on transforming physical reflectance spectra into perceptual space has shown that different transformations yield different uniformity characteristics:

- **Original reflectance scale**: Spectra neither parallel nor equally spaced
- **Log scale**: Spectra parallel but not equally spaced
- **Cube root scale**: Spectra both parallel AND equally spaced

Quantitative models using human cone sensitivity functions include **nonlinear cube root functions** to transform cone activations into Munsell color space coordinates, providing quantitative estimates of opponent process weights.

### Complexity of CIE-Munsell Conversion

The relations between Munsell and CIE variables are very complex:

- Lines of constant Munsell hue are **curved** in the CIE chromaticity diagram
- Hue locations **change with Munsell value**
- **No analytical expressions exist** to convert between CIE and Munsell systems
- Only lookup table programs can perform these conversions

**Sources**: [PMC - Munsell Reflectance Model](https://pmc.ncbi.nlm.nih.gov/articles/PMC156363/), [OSA JOSA - Neutral Value Scales](https://opg.optica.org/josa/abstract.cfm?uri=josa-23-11-394), [ScienceDirect - Munsell System](https://www.sciencedirect.com/topics/engineering/munsell-system)

---

## ΔE Color Difference Metrics

### Overview of CIELAB-Based Formulas

Color difference formulas attempt to quantify perceptual color differences through mathematical expressions. All modern formulas build on the CIE L\*a\*b\* color space but apply different corrections for perceptual non-uniformities.

### CIELAB ΔE\*ab (1976)

The simplest metric is Euclidean distance in CIELAB space:

```
ΔE*ab = √[(ΔL*)² + (Δa*)² + (Δb*)²]
```

**Advantages**:
- Simple to compute
- Widely understood
- Reasonable for large color differences

**Limitations**:
- Does not account for perceptual non-uniformities
- Particularly poor in blue region
- Overestimates gray differences near the neutral axis

### CIE94 ΔE\*94 (1995)

The CIE94 formula was introduced to address perceptual non-uniformities while retaining the CIELAB color space. It uses application-specific parametric weighting factors:

```
ΔE*94 = √[(ΔL*/kL·SL)² + (ΔC*/kC·SC)² + (ΔH*/kH·SH)²]
```

Where:
- **SL = 1** (constant)
- **SC = 1 + 0.045·Cab\*** (linear function of chroma)
- **SH = 1 + 0.015·Cab\*** (linear function of chroma)
- **kL, kC, kH**: Application-specific parametric factors

**Standard values**:
- For smooth surfaces (paint, plastic): kL = kC = kH = 1
- For rough surfaces (textiles): kL = 2, kC = kH = 1

**Advantages**:
- Simpler than CMC
- Better performance than CIELAB
- Industry-standard before CIEDE2000

**Limitations**:
- Chromatic discrimination ellipses are radially oriented (no rotation)
- Does not account for ellipse rotation in a\*b\* plane

**Sources**: [Wikipedia - Color Difference](https://en.wikipedia.org/wiki/Color_difference), [ResearchGate - Testing CIELAB Formulas](https://www.researchgate.net/publication/285259959_Testing_CIELAB-based_color-difference_formulas)

### CMC(l:c) (1984)

Developed by the Colour Measurement Committee of the Society of Dyers and Colourists, CMC is based on the CIE L\*C\*h\* color model with two user-adjustable parameters:

```
ΔE*CMC = √[(ΔL*/l·SL)² + (ΔC*/c·SC)² + (ΔH*/SH)²]
```

Where l and c allow users to weight the difference based on application requirements.

**Common parameter values**:
- **CMC(2:1)**: For acceptability decisions (doubles tolerance for lightness vs chroma)
- **CMC(1:1)**: For imperceptibility threshold

**Advantages**:
- Developed from visual evaluation of textile samples
- Reflects human vision sensitivity in lightness and chroma
- Well-suited for pass/fail production decisions
- Once a tolerance is established, same value applicable across colors under similar conditions

**Limitations**:
- More complex weighting functions than CIE94
- Does not account for ellipse rotation

**Industry Applications**:
- Automotive: ΔE\*CMC < 0.5 under D65/10° (very stringent)
- Textiles: CMC(2:1) most common
- Research suggests CMC(2:1) best conforms to average human observer

**Sources**: [Wikipedia - Color Difference](https://en.wikipedia.org/wiki/Color_difference), [ScienceDirect - Color Difference Formula](https://www.sciencedirect.com/topics/engineering/color-difference-formula)

### CIEDE2000 ΔE\*00 (2001)

CIEDE2000 is the most sophisticated color difference formula, published by the CIE in 2001 as the current standard. It adds five corrections to address remaining perceptual uniformity issues:

**Key improvements**:
1. **Hue rotation term (RT)**: Addresses problematic blue region
2. **Compensation for neutral colors**: Better handling near gray axis
3. **Lightness weighting**: Improved SL function
4. **Chroma weighting**: Improved SC function
5. **Hue weighting**: Improved SH function

**Formula structure** (highly complex):
```
ΔE*00 = √[(ΔL'/kL·SL)² + (ΔC'/kC·SC)² + (ΔH'/kH·SH)² + RT·(ΔC'/kC·SC)·(ΔH'/kH·SH)]
```

The full formula involves multiple intermediate calculations and is considerably more computationally intensive than predecessors.

**Implementation Challenges**:

The formula is complex enough that several implementations distributed on the Internet (including from reputable sources) have been found to contain errors. The authoritative implementation notes by Sharma, Wu, and Dalal (2005) provide:

- Supplemental test data for comprehensive validation
- Documentation of discontinuities in the formula
- Microsoft Excel spreadsheets and MATLAB scripts
- Identification of implementation pitfalls

**Advantages**:
- Most accurate for human perception
- Industry standard since 2001
- Statistically superior to CIE94 and CMC at 95% confidence level
- Accounts for hue rotation in a\*b\* plane

**Limitations**:
- Computationally expensive
- Not reliable below 1 cd/m² or above 100 cd/m² (designed for standard viewing)
- Underpredicts error in BT.709 blue primary region
- Three independent sources of mathematical discontinuities

**Perceptual Thresholds**:
- ΔE00 < 1.0: Just noticeable difference
- ΔE00 < 2.0: Generally imperceptible under normal viewing

**Sources**: [Sharma et al. 2005 - Implementation Notes](https://hajim.rochester.edu/ece/sites/gsharma/papers/CIEDE2000CRNAFeb05.pdf), [Techkon - CIEDE2000 Formula](https://techkonusa.com/demystifying-the-cie-delta-e-2000-formula/), [Color Research & Application](https://onlinelibrary.wiley.com/doi/10.1002/col.20070)

### Euclidean Distance in Munsell Cartesian Space

Given Munsell coordinates in Cartesian representation using Centore's formula:

```
x = C × cos(H × π/50)
y = C × sin(H × π/50)
z = V
```

Standard Euclidean distance can be computed:

```
d = √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]
```

**Advantages**:
- Simple to compute
- Preserves geometric relationships in Cartesian space
- Appropriate for convex hull algorithms

**Limitations**:
- Does not account for perceptual non-uniformities in Munsell space
- Hue, value, and chroma are not perceptually equivalent units
- May overweight chroma differences relative to hue or value

**When to Use**:
- Geometric polyhedra calculations
- Spatial clustering in Munsell coordinates
- Situations where computational simplicity is paramount

### Comparative Performance

Research comparing these formulas across multiple datasets has shown:

1. **CIEDE2000** performs best overall, followed by **CIE94** and **CMC**
2. **CMC** and **CIEDE2000** differences statistically significant at 95% confidence
3. **CMC** and **CIE94** differences NOT statistically significant
4. **CIE94** performs best across all viewing conditions
5. **CIELAB** and **BFD** perform worst
6. **CMC** gives highest color differences when computing near the gray point

**Sources**: [ResearchGate - Testing CIELAB Formulas](https://www.researchgate.net/publication/285259959_Testing_CIELAB-based_color-difference_formulas), [ArXiv - Color Difference Formula Evaluation](https://arxiv.org/pdf/1904.11293)

---

## Local Metric Tensors and Distance Variations

### The Metric Tensor Concept

In differential geometry, a **metric tensor** is an additional structure on a manifold (such as a surface or color space) that allows defining distances and angles. Color space can be viewed as a real vector space, but the challenge is that **no matter what inner product is applied, the resulting Euclidean distance does not correspond to human perception** of difference between colors.

### MacAdam Ellipses as Metric Tensors

MacAdam's 1942 experiments on color matching provide the empirical foundation for understanding the local metric structure of color space. The MacAdam ellipses are often **interpreted as defining the metric tensor at their centers**.

At each point in color space, the local metric tensor describes how perceptual distance stretches differently in different directions:

- Ellipses elongated in one direction indicate that changes in that direction are less perceptually significant
- The inverse of the ellipse dimensions defines the local metric for computing perceptual distances

### Riemannian Color Space

Many color difference formulas implicitly treat color space as a **Riemannian manifold** - a curved space where distances are measured along the manifold surface rather than through straight lines.

**Key properties**:
- Color space has **curvilinear nature** rather than flat Euclidean structure
- Small color difference calculations using Euclidean distance **do not agree sufficiently** with perceptual color difference
- The metric tensor varies across the space, making it **non-homogeneous**

### Line Element Theory

The beauty of line element theory for assessing color differences is that it can deal with **Euclidean as well as non-Euclidean** color perception space simultaneously, whereas color difference formulas in nearly every case assume that color space is Euclidean.

Line element theory uses the local metric tensor G to compute distances:

```
ds² = Σᵢⱼ gᵢⱼ dxᵢ dxⱼ
```

Where gᵢⱼ are components of the metric tensor that vary across the space.

**Sources**: [DTU Research - Metric of Colour Space](https://orbit.dtu.dk/en/publications/the-metric-of-colour-space), [HAL Archives - Line Element Methods](https://theses.hal.science/tel-00981484/document)

---

## Geodesic vs Euclidean Distance

### Definitions

**Euclidean Distance**: The straight-line distance between two points in coordinate space, computed using the Pythagorean theorem.

**Geodesic Distance**: The shortest path between two points measured along the surface of the manifold (curved space). In flat Euclidean space, geodesics are straight lines, but in Riemannian space they are generally curved.

### Color Space Implications

The shortest length path in color space is called a **geodesic**, which is used to evaluate the magnitude of perceptual color differences. When color space is treated as a Riemannian manifold with a non-trivial metric tensor:

```
Geodesic distance ≠ Euclidean distance
```

### When They Coincide

**Flat manifold condition**: When the Riemannian metric tensor is proportional to the identity matrix (G ∝ I), the Euclidean distance in the latent space corresponds to the geodesic distance. A manifold with this property is called a **flat manifold**.

For most color spaces, including Munsell and CIELAB, the metric tensor is **not** proportional to identity, meaning:

- Geodesic paths curve through the space
- Perceptual distance must account for this curvature
- Euclidean distance is only an approximation

### Computational Considerations

**Geodesic distance advantages**:
- More accurate representation of perceptual differences
- Accounts for the curvilinear structure of color space
- Enables higher structure sensitivity

**Euclidean distance advantages**:
- Computationally simple
- Works well for convex hull algorithms
- Adequate for large-scale geometric comparisons

**Practical compromise**: For polyhedra comparison, Euclidean distance in Munsell Cartesian space provides geometric clarity, while CIEDE2000 provides perceptual accuracy. Use both metrics to characterize different aspects of color relationships.

**Sources**: [Wikipedia - Geodesic](https://en.wikipedia.org/wiki/Geodesic), [ResearchGate - Geodesic vs Euclidean](https://www.researchgate.net/figure/Geodesic-distance-vs-Euclidean-distance-Image-contents-in-between-could-provide-a_fig1_221111355)

---

## Application to Polyhedra Comparison

### Multi-Metric Approach

When comparing color polyhedra constructed from different data sources (e.g., Centore's CAUS data vs XKCD screen colors), no single metric captures all relevant aspects. A comprehensive comparison requires multiple metrics:

#### 1. Geometric Metrics (Munsell Cartesian Space)

**Euclidean centroid distance**:
```python
d_centroid = np.linalg.norm(centroid_A - centroid_B)
```

**Applications**:
- Comparing overall polyhedron positions
- Detecting systematic bias between datasets
- Spatial clustering analysis

**Interpretation**: Values in Munsell units (approximate perceptual scale)

#### 2. Perceptual Metrics (CIELAB)

Convert Munsell centroids to CIELAB and compute CIEDE2000:

**Applications**:
- Assessing whether differences are perceptually significant
- Validating that polyhedra represent distinct color categories
- Quality control for overlay boundaries

**Interpretation**:
- ΔE00 < 1.0: Indistinguishable
- ΔE00 < 2.0: Just noticeable
- ΔE00 > 5.0: Clear perceptual difference

#### 3. Volume and Shape Metrics

**Volume ratio**:
```python
volume_ratio = volume_A / volume_B
```

**Hausdorff distance**: Maximum distance from any point in one polyhedron to the nearest point in the other

**Applications**:
- Detecting over/under-saturation in datasets
- Identifying shape distortions
- Quantifying extent differences

#### 4. Overlap Metrics

**Intersection over union (IoU)**:
```python
IoU = volume(A ∩ B) / volume(A ∪ B)
```

**Applications**:
- Quantifying semantic category agreement
- Validating consistency between datasets
- Identifying boundary ambiguities

### Validation Criteria for Polyhedra

Based on the research above, proposed criteria for polyhedra quality:

1. **Perceptual distinctness**: Centroids separated by ΔE00 > 5.0 from existing categories
2. **Spatial coherence**: Low internal variance relative to inter-category distance
3. **Geometric validity**: Convex hull with V - E + F = 2 (Euler characteristic)
4. **Statistical support**: Minimum 25 samples (Centore's threshold)
5. **Localization**: Limited extent in Munsell space (not global spread)

### Recommended Workflow

For comparing polyhedra from different sources:

```python
# 1. Geometric comparison in Munsell Cartesian
centroid_distance_munsell = euclidean(centroid_A, centroid_B)

# 2. Perceptual comparison in CIELAB
centroid_A_lab = munsell_to_lab(centroid_A)
centroid_B_lab = munsell_to_lab(centroid_B)
delta_e_2000 = ciede2000(centroid_A_lab, centroid_B_lab)

# 3. Shape comparison
volume_ratio = volume_A / volume_B
hausdorff_dist = compute_hausdorff(vertices_A, vertices_B)

# 4. Overlap analysis
intersection_volume = compute_intersection(poly_A, poly_B)
union_volume = volume_A + volume_B - intersection_volume
iou = intersection_volume / union_volume
```

### Interpretation Guidelines

| Metric | Threshold | Interpretation |
|--------|-----------|----------------|
| Centroid ΔE00 | < 2.0 | Same perceptual category |
| Centroid ΔE00 | 2.0-5.0 | Related but distinguishable |
| Centroid ΔE00 | > 5.0 | Distinct categories |
| Volume ratio | 0.8-1.2 | Similar extent |
| Volume ratio | < 0.5 or > 2.0 | Significant size difference |
| IoU | > 0.7 | High overlap |
| IoU | 0.3-0.7 | Moderate overlap |
| IoU | < 0.3 | Low overlap |

### Special Considerations

**Screen vs Surface Colors**: When comparing screen-derived polyhedra (XKCD) to surface-measured polyhedra (Centore CAUS), systematic bias is expected due to:

1. Self-luminous vs reflective viewing conditions
2. Different viewing environments
3. Perceptual adaptation differences

**Recommendation**: Document bias separately before applying corrections. Use Track B Phase 3 calibration subset to quantify and characterize this bias.

---

## References

### Perceptual Uniformity and MacAdam Ellipses

- [Nightingale - Color in a Perceptual Uniform Way](https://nightingaledvs.com/color-in-a-perceptual-uniform-way/)
- [Imatest - Color Difference Ellipses](https://www.imatest.com/2015/09/color-difference-ellipses/)
- [ResearchGate - MacAdam Ellipses Diagram](https://www.researchgate.net/figure/MacAdam-ellipses-plotted-on-the-CIE-1931-xy-chromaticity-diagram-9-The-ellipses-show_fig1_246546517)

### Munsell System Structure

- [Wikipedia - Munsell Color System](https://en.wikipedia.org/wiki/Munsell_color_system)
- [ScienceDirect - Munsell System Overview](https://www.sciencedirect.com/topics/engineering/munsell-system)
- [ResearchGate - Munsell Cylindrical Coordinates](https://www.researchgate.net/figure/a-The-Munsell-color-system-represented-in-cylindrical-coordinates-b-Illustration-of-the_fig1_393230475)

### Value Scale Non-Linearity

- [PMC - Munsell Reflectance Transformation](https://pmc.ncbi.nlm.nih.gov/articles/PMC156363/)
- [OSA JOSA - Neutral Value Scales](https://opg.optica.org/josa/abstract.cfm?uri=josa-23-11-394)
- [SPIE - Munsell System](https://spie.org/publications/pm105_53_munsell_system)

### Color Difference Formulas

- [Wikipedia - Color Difference](https://en.wikipedia.org/wiki/Color_difference)
- [Techkon - CIEDE2000 Formula](https://techkonusa.com/demystifying-the-cie-delta-e-2000-formula/)
- [Sharma et al. 2005 - CIEDE2000 Implementation Notes](https://hajim.rochester.edu/ece/sites/gsharma/papers/CIEDE2000CRNAFeb05.pdf)
- [Color Research & Application - CIEDE2000 Paper](https://onlinelibrary.wiley.com/doi/10.1002/col.20070)
- [ResearchGate - Testing CIELAB-based Formulas](https://www.researchgate.net/publication/285259959_Testing_CIELAB-based_color-difference_formulas)
- [ScienceDirect - Color Difference Formula Overview](https://www.sciencedirect.com/topics/engineering/color-difference-formula)

### Metric Tensors and Geodesic Distance

- [DTU Research - The Metric of Colour Space](https://orbit.dtu.dk/en/publications/the-metric-of-colour-space)
- [HAL Archives - Line Element and Variational Methods](https://theses.hal.science/tel-00981484/document)
- [Wikipedia - Geodesic](https://en.wikipedia.org/wiki/Geodesic)
- [Wikipedia - Metric Tensor](https://en.wikipedia.org/wiki/Metric_tensor)
- [ResearchGate - Geodesic vs Euclidean Distance](https://www.researchgate.net/figure/Geodesic-distance-vs-Euclidean-distance-Image-contents-in-between-could-provide-a_fig1_221111355)

---

**Document Status**: Complete
**Author**: Research Analyst (Claude Code)
**Date**: 2026-01-03
**Next Phase**: Implement delta_e_metrics.py with formulas documented above
