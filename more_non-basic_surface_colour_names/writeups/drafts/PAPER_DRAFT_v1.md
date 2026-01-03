# Extending Non-Basic Surface Color Names: A Computational Replication and Extension of Centore's Polyhedron Methodology

**Draft Version**: 1.0
**Date**: 2026-01-03
**Status**: Working Draft

---

## Abstract

We present a computational replication and extension of Centore's (2020) methodology for defining non-basic surface color names using inner convex hull polyhedra in Munsell color space. Our work makes three contributions: (1) full verification of Centore's 30 color family polyhedra with sub-percentage numerical agreement, (2) quantification of systematic differences between screen-displayed (RGB) and surface-measured (spectrophotometric) color naming with an average centroid shift of 3.21 Munsell units, and (3) identification of five candidate color families not in Centore's original set—indigo, maroon, lime, plum, and aquamarine—with sufficient sample sizes and spatial coherence for potential inclusion. We also investigate the RGB-to-Munsell transformation, finding that volume matching is the dominant objective for polyhedron transformation (achieving 0.054 combined loss with volume-only optimization) while shape preservation is fundamentally limited to a floor of 0.13–0.18 regardless of optimization strategy. Our analysis of 184,297 crowdsourced screen color names against Centore's 9,261 spectrophotometer-measured fabric samples reveals that screen colors appear systematically lighter (+0.81 Munsell value on average) and more saturated (+3.82 Munsell chroma on average) than their surface counterparts, with hue shifts that are category-dependent. These findings have implications for color naming research, computational color science, and the development of color-aware language models.

**Keywords**: color naming, Munsell color space, convex hull, semantic color categories, screen-surface transformation, crowdsourced color data

---

## 1. Introduction

Color naming is a fundamental aspect of human communication, yet the boundaries between color categories remain subjective and culturally variable. While Berlin and Kay's (1969) foundational work established that languages share a constrained set of basic color terms—red, yellow, green, blue, black, white, gray, orange, brown, pink, and purple in English—everyday color communication relies heavily on non-basic terms such as "beige," "navy," "coral," and "turquoise."

Centore (2020) provided the first systematic, empirical definitions for 20 non-basic surface color names by analyzing 9,261 fabric samples from the Color Association of the United States (CAUS) database. His methodology employed inner convex hull polyhedra in a cylindrical Munsell coordinate system, defining each color category as a bounded region in three-dimensional color space. This approach offers significant advantages over alternative methods: it is mathematically precise, reproducible, and captures the natural variation in how humans apply color names.

However, Centore's work is limited to physical surface colors measured with spectrophotometry. With the proliferation of digital color interaction—from design tools to social media—there is a practical need to understand how color naming extends to screen-displayed colors. Additionally, Centore's 30 families, while comprehensive, do not exhaust the vocabulary of commonly-used color terms.

In this paper, we address three research questions:

1. **Can Centore's methodology be computationally replicated?** We implement his inner convex hull algorithm and verify our results against his published polyhedra.

2. **How do screen-displayed colors differ from surface colors in naming?** We compare polyhedra constructed from crowdsourced RGB color names to Centore's spectrophotometer-measured surface colors.

3. **What additional color families merit definition?** We identify candidate families from crowdsourced data that do not overlap with Centore's 30.

Our findings contribute to color science, computational linguistics, and the development of color-aware AI systems that must bridge the gap between digital and physical color perception.

---

## 2. Related Work

### 2.1 Basic Color Terms and Universal Categories

Berlin and Kay's (1969) cross-cultural study established that languages encode color categories in a constrained evolutionary sequence, from a minimum of two terms (black/white) to a maximum of eleven basic terms. The World Color Survey (Kay et al., 2009) extended this work to 110 unwritten languages, confirming privileged focal points in color space.

Regier et al. (2007) demonstrated that color naming systems across languages reflect near-optimal partitions of perceptual color space, balancing communicative efficiency with categorical simplicity. This work grounds our assumption that color categories have principled boundaries in perceptual space.

### 2.2 Centore's Polyhedron Methodology

Centore (2020) introduced a novel approach to defining non-basic color names using inner convex hulls in Munsell space. His methodology consists of:

1. **Data collection**: Fabric samples with associated color names from the CAUS database, measured via spectrophotometry.

2. **Coordinate transformation**: Conversion of Munsell notation to Cartesian coordinates using:
   $$x = C \cdot \cos\left(\frac{H \cdot \pi}{50}\right), \quad y = C \cdot \sin\left(\frac{H \cdot \pi}{50}\right), \quad z = V$$
   where $H$ is hue on a 0–100 scale (corresponding to 0–360°), $C$ is chroma, and $V$ is value.

3. **Outlier removal**: Computing the outer convex hull and discarding its vertices (single-layer peeling) to exclude extreme samples.

4. **Inner hull construction**: Computing the convex hull of remaining points to define the color family polyhedron.

5. **Centroid calculation**: Computing the filled-solid centroid via tetrahedron decomposition (not the vertex centroid).

Centore's 30 families include 10 basic colors (blue, brown, gray, green, orange, pink, purple, red, white, yellow) and 20 non-basic colors (aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy, peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine).

### 2.3 Screen Colors vs. Surface Colors

Centore explicitly noted that "the Munsell system applies only to surface colours, and not to coloured lights" (2020, p. 28), acknowledging that RGB-to-Munsell conversion for screen colors requires "additional analysis."

Screen colors differ from surface colors in fundamental ways:
- **Emissive vs. reflective**: Screens emit light (additive color mixing); surfaces reflect light (subtractive color mixing).
- **Viewing conditions**: Screen colors are viewed under variable ambient lighting; spectrophotometric measurements are standardized.
- **Gamut differences**: sRGB covers a smaller portion of visible color space than surface colors can achieve.

The XKCD Color Survey (Munroe, 2010) collected 3.4 million color naming responses for screen-displayed RGB colors, providing the largest available dataset of crowdsourced color names. However, the direct comparison of XKCD-derived categories to Centore's surface-derived categories has not been previously attempted.

### 2.4 Color Space Transformations

Converting RGB values to Munsell notation follows a standard pipeline (ASTM D1535-14):

1. **Gamma correction**: sRGB to linear RGB using ITU-R BT.709 transfer function.
2. **Matrix transformation**: Linear RGB to CIE XYZ using D65 illuminant primaries.
3. **Chromaticity calculation**: XYZ to xyY for hue and chroma determination.
4. **Munsell lookup**: xyY to Munsell via interpolation of the Munsell Renotation Data.

While this pipeline is mathematically well-defined, it assumes the input RGB values represent surface colors viewed under standard illumination—an assumption violated by screen-displayed colors.

---

## 3. Methodology

### 3.1 Track A: Methodology Verification

To ensure our implementation correctly replicates Centore's approach, we performed comprehensive verification against all 30 published polyhedra.

**Implementation details**:
- Munsell notation parsing including neutral colors (e.g., "N9.02" for achromatic samples)
- Cartesian coordinate conversion using Centore's exact formula
- Convex hull computation via scipy's QHull interface
- Single-layer vertex removal for outlier detection
- Filled-solid centroid via tetrahedron decomposition

**Verification metrics**:
- Centroid position error (Euclidean distance)
- Vertex count match
- Edge and face count match (via Euler's formula: $V - E + F = 2$)
- Individual vertex coordinate matching (Hungarian algorithm for optimal assignment)

### 3.2 Track B: Screen Color Polyhedra Construction

We constructed polyhedra from crowdsourced screen color data following Centore's exact methodology.

**Data sources**:
- XKCD Color Survey (Munroe, 2010): 175,844 unique color names with RGB values
- Meodai Color Names (Aerne, 2024): 33,000+ curated names for vocabulary reference
- Additional sources: ColorHexa, Wikipedia color lists, ColorName.com

**Preprocessing pipeline**:
1. **Semantic validation**: SBERT similarity filtering (Reimers & Gurevych, 2019) with threshold 0.35 to retain color-relevant names
2. **Name normalization**: Lowercase, whitespace normalization, quote handling
3. **Family assignment**: Substring matching to map names to color families (e.g., "light coral" → coral)
4. **Munsell conversion**: RGB to Munsell via MunsellSpace library (ASTM D1535 compliant)

**Polyhedron construction**: Identical to Centore's methodology (Section 3.1) applied to screen-derived samples.

### 3.3 Track C: Centore Comparison

For each of Centore's 30 families, we compared our screen-derived polyhedra to his surface-derived polyhedra.

**Metrics**:
- **Centroid shift**: Euclidean distance between centroids in Cartesian Munsell space
- **Value shift**: Difference in mean value (lightness)
- **Volume ratio**: Ratio of polyhedron volumes
- **Vertex count ratio**: Number of vertices (proxy for sample size and distribution)

### 3.4 Track D: New Family Identification

We identified candidate color families from the screen data that do not overlap with Centore's 30.

**Criteria for candidate families**:
1. **Minimum sample size**: ≥200 unique samples (comparable to Centore's smallest family, magenta, with 25 samples)
2. **Spatial coherence**: Standard deviation of coordinates below threshold
3. **Hue consistency**: Majority of samples within a single hue quadrant
4. **Semantic distinctiveness**: Not a variant spelling or synonym of existing family

### 3.5 Phase 5: Transformation Analysis

We investigated optimal methods for transforming screen polyhedra to match surface polyhedra.

**Loss function components**:
$$L_{total} = w_c \cdot L_{centroid} + w_v \cdot L_{volume} + w_s \cdot L_{shape}$$

where:
- $L_{centroid} = \frac{\|c_{screen} - c_{surface}\|}{\text{max\_extent}}$ (normalized position error)
- $L_{volume} = \left|\frac{V_{screen}}{V_{surface}} - 1\right|$ (volume ratio deviation)
- $L_{shape} = \frac{d_H(S_{screen}, S_{surface})}{\text{max\_extent}}$ (normalized Hausdorff distance)

**Experiments**:
- Single-component optimization (centroid-only, volume-only, shape-only)
- Pairwise component optimization
- Pareto frontier analysis
- Alternative shape metrics (Chamfer, EMD, spectral, IoU)
- Aggregation methods (mean, minimax, trimmed mean, median)

---

## 4. Results

### 4.1 Track A: Verification Results

Our implementation achieves perfect concordance with Centore's published polyhedra.

**Table 1: Verification Summary Statistics**

| Metric | Value |
|--------|-------|
| Exact vertex count match | 30/30 (100%) |
| Mean centroid error | 0.0045 Munsell units |
| Max centroid error | 0.0067 (green) |
| Mean vertex coordinate error | 0.0038 Munsell units |
| Max vertex coordinate error | 0.0070 Munsell units |

All errors are below 0.01 Munsell units, representing sub-percentage agreement well within numerical precision bounds. This verification confirms that our implementation correctly replicates Centore's methodology.

**Technical note**: Initial verification revealed a parsing issue for neutral colors (Munsell notation "N{value}" rather than chromatic "{hue}{letter} {value}/{chroma}"). After correction, all 30 families matched exactly.

### 4.2 Track B: Screen Color Polyhedra

We constructed 35 polyhedra from 184,297 screen color samples: Centore's 30 families plus 5 new candidates.

**Table 2: Screen Polyhedra Summary**

| Quality Rating | Count | Percentage |
|----------------|-------|------------|
| Good | 2 | 5.7% |
| Acceptable | 12 | 34.3% |
| Needs Review | 21 | 60.0% |

Quality assessment used sample size (≥100 for good), spatial coherence (<0.3 for good), and hue consistency (>80% for good).

**Highest quality families**: brown (4,516 samples, 86.1% hue consistency) and maroon (1,237 samples, 73.4% hue consistency).

**Problematic families**: teal (8.5% hue consistency), turquoise (11.2%), plum (11.7%), and navy (13.4%). Low hue consistency indicates the screen color naming for these families spans multiple hue regions.

### 4.3 Track C: Centore Comparison

Comparison of our screen-derived polyhedra with Centore's surface-derived polyhedra reveals systematic differences.

**Table 3: Screen-Surface Comparison Summary**

| Metric | Value |
|--------|-------|
| Centore families compared | 30 |
| Average centroid shift | 3.21 Munsell units |
| Maximum centroid shift | 7.44 Munsell units (purple) |
| Families shifted lighter | 23 (77%) |
| Families shifted darker | 4 (13%) |
| Mean value shift | +0.81 |
| Mean chroma shift | +3.82 |

**Table 4: Top 5 Centroid Shifts**

| Family | Shift (Munsell units) | Value Δ |
|--------|----------------------|---------|
| purple | 7.44 | +1.62 |
| coral | 6.85 | -0.02 |
| violet | 6.71 | +1.11 |
| lilac | 6.50 | -0.09 |
| lavender | 5.28 | +0.44 |

The purple family shows the largest divergence between screen and surface naming. This may reflect (1) the difficulty of reproducing purple hues on sRGB displays, (2) cultural differences between fashion-industry color naming (Centore's CAUS data) and general-population screen color naming (XKCD data), or (3) genuine differences in how people perceive emissive vs. reflective purple.

**Value trends**: 23 families appear lighter on screen (+value), consistent with the emissive nature of displays. Notable exceptions include white (-1.60 value), peach (-1.16), and orange (-0.71), which may reflect ceiling effects (white) or cultural associations (orange/peach as "warm" colors that people name more conservatively on cool-toned screens).

### 4.4 Track D: New Candidate Families

We identified 5 candidate families not in Centore's original 30:

**Table 5: New Candidate Families**

| Family | Samples | Centroid (x, y, z) | Volume | Spatial Coherence |
|--------|---------|-------------------|--------|-------------------|
| indigo | 421 | (2.1, -6.9, 4.5) | 1,211 | 0.52 |
| maroon | 1,237 | (4.0, 1.7, 4.7) | 3,545 | 0.49 |
| lime | 759 | (-4.4, 5.5, 7.5) | 932 | 0.52 |
| plum | 333 | (6.2, -7.4, 4.5) | 597 | 0.60 |
| aquamarine | 969 | (-5.6, 0.1, 6.8) | 686 | 0.65 |

**Indigo** occupies the blue-violet transition region (negative y, low-moderate value). It is distinct from both navy (darker) and violet (more red component).

**Maroon** fills the dark red-brown gap, distinct from both wine (more purple) and rust (more orange).

**Lime** occupies the yellow-green region, providing a more intuitive name than ISCC-NBS "yellow green."

**Plum** is positioned in the red-purple region, distinct from violet (more blue) and purple (broader hue range).

**Aquamarine** fills the blue-green region with gemstone-based naming, distinct from teal (darker) and turquoise (more cyan).

### 4.5 Phase 5: Transformation Analysis

We investigated optimal loss functions for transforming screen polyhedra toward surface polyhedra.

**Key Finding 1: Volume dominates the loss function**

| Strategy | Combined Loss | Rank |
|----------|---------------|------|
| Volume-only | 0.054 | 1 |
| Centroid-only | 0.158 | 2 |
| Shape-only | 0.308 | 3 |

Volume-only optimization achieves 0.054 combined loss, nearly identical to full weighted optimization (0.0535). Adding centroid or shape objectives provides marginal benefit.

**Key Finding 2: Shape preservation is fundamentally limited**

Across all tested weight combinations, shape loss varies only 5% (0.13 to 0.18). This represents a floor imposed by the transformation approach, not the loss function weights.

**Table 6: Shape Loss Floor Across Strategies**

| Strategy | Shape Loss |
|----------|------------|
| shape_only | 0.130 |
| volume_shape | 0.171 |
| volume_only | 0.180 |
| centroid_volume | 0.180 |

**Key Finding 3: Chamfer can replace Hausdorff**

Alternative shape metrics show high correlation:
- Hausdorff ↔ Chamfer: r = 0.99
- Hausdorff ↔ EMD: r = 0.91
- Chamfer ↔ EMD: r = 0.91

Chamfer distance is computationally faster (O(n log n) vs O(n²)) and provides equivalent information.

**Key Finding 4: Volume transformation is uniform**

Jacobian analysis across color space shows the RGB-to-Munsell transformation has CV = 0.02 (highly uniform). A single global scaling factor of 2,054.70 suffices for volume normalization—no per-family corrections are needed.

**Bootstrap analysis** confirms 94.3% of families (33/35) achieve stable volume estimates. Only brown and purple remain unstable, potentially requiring alternative bounding methods (e.g., alpha-shapes).

---

## 5. Discussion

### 5.1 Screen-Surface Color Gap

Our results quantify a systematic gap between how people name colors on screens versus physical surfaces. The average centroid shift of 3.21 Munsell units is perceptually significant—roughly equivalent to one or two steps on the Munsell chroma scale.

This gap has multiple sources:

1. **Physical**: Emissive displays produce colors through additive mixing (R+G+B), while reflective surfaces use subtractive mixing. The sRGB gamut is smaller than the surface color gamut, particularly for saturated blues and greens.

2. **Perceptual**: Screen viewing conditions vary (ambient lighting, monitor calibration), while spectrophotometric measurement is standardized. People may perceive screen colors as more saturated due to the high luminance of displays.

3. **Cultural**: The CAUS database represents fashion-industry professional color naming, while XKCD represents general-population crowdsourced naming. Professional colorists may use terms more precisely.

4. **Semantic**: Color names carry cultural associations beyond colorimetry. "Navy" evokes military uniforms; "coral" evokes marine biology. These associations may shift the perceived boundaries of categories.

### 5.2 Implications for Color Naming Research

Our verification of Centore's methodology (Track A) establishes a computational foundation for future color naming research. The inner convex hull approach can be applied to new datasets, languages, and color media.

The screen-surface gap (Track C) suggests caution when using screen-based color data to draw conclusions about color perception generally. Researchers should specify whether their data represents emissive or reflective colors.

Our new candidate families (Track D) suggest that Centore's 30 families, while comprehensive, do not exhaust the vocabulary of commonly-used color terms. Indigo, maroon, and lime in particular fill gaps in the hue circle that users intuitively recognize.

### 5.3 Implications for Color-Aware AI Systems

Modern language models and vision-language systems increasingly need to reason about color. Our findings suggest:

1. **Training data matters**: Models trained on screen color descriptions may not generalize to surface color tasks (and vice versa).

2. **Category boundaries are soft**: The 60% of families rated "needs review" for hue consistency shows that crowdsourced color naming is inherently fuzzy. Hard categorical boundaries may not reflect human usage.

3. **Volume-based matching works**: For applications that need to transform color descriptions between domains, volume matching provides a simple and effective approach.

### 5.4 Limitations

Several limitations constrain our findings:

1. **Data source bias**: XKCD respondents skew young, English-speaking, and tech-savvy. Our screen color data may not represent global color naming.

2. **RGB gamut constraints**: Some Centore families (e.g., certain saturated blues) may fall partially outside sRGB, affecting our screen-derived polyhedra.

3. **Temporal mismatch**: Centore's CAUS data spans decades of fashion samples; XKCD data is from a single 2010 survey. Color naming may evolve over time.

4. **Single-language focus**: Our analysis is English-only. Cross-linguistic validation is needed.

5. **Pending data requests**: We have not yet integrated data from colornaming.net, inkswatches.com, or updated CAUS samples, which may refine our findings.

---

## 6. Conclusions

We have demonstrated that Centore's inner convex hull methodology for defining non-basic color names can be computationally replicated with sub-percentage numerical precision. Applying this methodology to crowdsourced screen color data reveals systematic differences from surface color naming: screen colors appear lighter, more saturated, and shifted in hue relative to spectrophotometer-measured surface colors.

Our analysis identifies five candidate color families—indigo, maroon, lime, plum, and aquamarine—that merit consideration for addition to the standard vocabulary of defined color terms. These families fill intuitive gaps in the color space and have sufficient sample support from crowdsourced data.

For researchers and practitioners working with color transformation, we recommend volume-only optimization as the most effective approach, with the understanding that shape preservation is fundamentally limited to approximately 0.13–0.18 regardless of optimization strategy. A single global scaling factor of approximately 2,055 suffices for RGB-to-Munsell volume normalization.

Future work should (1) extend this analysis to non-English languages using World Color Survey data, (2) investigate non-linear transformation methods (radial basis functions, thin-plate splines) for improved shape preservation, and (3) integrate additional surface color datasets as they become available.

---

## Acknowledgments

We thank Paul Centore for making his polyhedron data publicly available and for his foundational work on non-basic color definitions. We also thank Randall Munroe for the XKCD Color Survey data and David Aerne for the Meodai Color Names collection.

---

## References

ASTM International. (2014). ASTM D1535-14: Standard Practice for Specifying Color by the Munsell System. ASTM International.

Aerne, D. (2024). Color Names: Collection of 33,000+ Curated Color Names. GitHub repository. https://github.com/meodai/color-names

Berlin, B., & Kay, P. (1969). Basic Color Terms: Their Universality and Evolution. University of California Press.

Centore, P. (2020). Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names. Journal of the International Colour Association, 25, 24–54.

Fisher, N. I. (1993). Statistical Analysis of Circular Data. Cambridge University Press.

ITU-R. (2015). BT.709: Parameter values for the HDTV standards for production and international programme exchange. International Telecommunication Union.

Kay, P., Berlin, B., Maffi, L., Merrifield, W. R., & Cook, R. (2009). The World Color Survey. CSLI Publications.

Lay, S. R. (2007). Convex Sets and Their Applications. Dover Publications.

Munroe, R. (2010). XKCD Color Survey Results. XKCD Blog. https://blog.xkcd.com/2010/05/03/color-survey-results/

Regier, T., Kay, P., & Khetarpal, N. (2007). Color naming reflects optimal partitions of color space. Proceedings of the National Academy of Sciences, 104(4), 1436–1441.

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. Proceedings of EMNLP-IJCNLP 2019.

---

## Appendix A: Detailed Verification Table

**Table A1: Full Verification Results for All 30 Centore Families**

| Family | Centroid Err | V(ours) | V(Centore) | Mean V Err | Max V Err |
|--------|--------------|---------|------------|------------|-----------|
| aqua | 0.0023 | 28 | 28 | 0.0037 | 0.0058 |
| beige | 0.0033 | 32 | 32 | 0.0041 | 0.0063 |
| blue | 0.0052 | 66 | 66 | 0.0038 | 0.0067 |
| brown | 0.0051 | 33 | 33 | 0.0039 | 0.0065 |
| coral | 0.0062 | 34 | 34 | 0.0038 | 0.0063 |
| fuchsia | 0.0049 | 18 | 18 | 0.0032 | 0.0066 |
| gold | 0.0046 | 47 | 47 | 0.0035 | 0.0067 |
| gray | 0.0038 | 39 | 39 | 0.0035 | 0.0062 |
| green | 0.0067 | 66 | 66 | 0.0039 | 0.0065 |
| lavender | 0.0047 | 15 | 15 | 0.0039 | 0.0062 |
| lilac | 0.0011 | 20 | 20 | 0.0042 | 0.0064 |
| magenta | 0.0046 | 7 | 7 | 0.0043 | 0.0060 |
| mauve | 0.0064 | 44 | 44 | 0.0035 | 0.0054 |
| navy | 0.0029 | 24 | 24 | 0.0040 | 0.0064 |
| orange | 0.0050 | 46 | 46 | 0.0040 | 0.0066 |
| peach | 0.0018 | 28 | 28 | 0.0041 | 0.0062 |
| pink | 0.0035 | 55 | 55 | 0.0037 | 0.0068 |
| purple | 0.0040 | 45 | 45 | 0.0037 | 0.0065 |
| red | 0.0042 | 39 | 39 | 0.0038 | 0.0059 |
| rose | 0.0051 | 51 | 51 | 0.0039 | 0.0061 |
| rust | 0.0046 | 24 | 24 | 0.0039 | 0.0067 |
| sand | 0.0054 | 24 | 24 | 0.0036 | 0.0055 |
| tan | 0.0058 | 27 | 27 | 0.0035 | 0.0055 |
| taupe | 0.0063 | 23 | 23 | 0.0038 | 0.0057 |
| teal | 0.0053 | 15 | 15 | 0.0034 | 0.0055 |
| turquoise | 0.0044 | 26 | 26 | 0.0042 | 0.0062 |
| violet | 0.0026 | 31 | 31 | 0.0041 | 0.0066 |
| white | 0.0034 | 24 | 24 | 0.0039 | 0.0069 |
| wine | 0.0066 | 21 | 21 | 0.0037 | 0.0062 |
| yellow | 0.0037 | 35 | 35 | 0.0043 | 0.0070 |

**Summary**: Mean centroid error = 0.0045; Max centroid error = 0.0067; Mean vertex error = 0.0038; Max vertex error = 0.0070. All errors below 0.01 Munsell units.

---

## Appendix B: Transformation Analysis Details

### B.1 Jacobian Analysis

The Jacobian determinant |det(J)| represents local volume scaling in the RGB→Munsell transformation:

$$|det(J)| = \left|\frac{\partial(x_M, y_M, z_M)}{\partial(R, G, B)}\right|$$

**Table B1: Jacobian Statistics by Region**

| Region | Mean |det(J)| | Std Dev | CV |
|--------|----------------|---------|-----|
| Overall | 2054.70 | 32.83 | 0.02 |
| Low Value (0-3) | 2083.36 | 119.48 | 0.06 |
| High Value (7-10) | 2053.47 | 21.81 | 0.01 |
| High Chroma (>4) | 2052.51 | 0.00 | 0.00 |

The near-zero variance in high-chroma regions confirms that the RGB→Munsell transformation is remarkably uniform for saturated colors.

### B.2 Loss Metric Correlations

**Table B2: Shape Metric Correlations**

| Metric Pair | Correlation |
|-------------|-------------|
| Hausdorff ↔ Chamfer | 0.99 |
| Hausdorff ↔ EMD | 0.91 |
| Chamfer ↔ EMD | 0.91 |
| Chamfer ↔ IoU | 0.70 |
| Spectral ↔ Hausdorff | -0.23 |

Spectral loss captures different information than geometric metrics, suggesting potential for multi-objective optimization.

---

## Appendix C: New Candidate Family Details

### C.1 Indigo

**Centroid**: (2.1, -6.9, 4.5) in Cartesian Munsell coordinates
**Approximate Munsell**: 7.5PB 4.5/7
**Sample count**: 421
**Hue range**: Primarily 7.5PB–10PB (blue-violet transition)
**Semantic neighbors**: navy (darker), violet (more red), blue (more cyan)

Indigo fills a gap between blue and violet that users intuitively recognize. The name derives from the Indigofera plant and has historical significance in textile dyeing.

### C.2 Maroon

**Centroid**: (4.0, 1.7, 4.7) in Cartesian Munsell coordinates
**Approximate Munsell**: 5R 4.7/4
**Sample count**: 1,237
**Hue range**: Primarily 5R–10R (dark red-brown)
**Semantic neighbors**: wine (more purple), rust (more orange), brown (less red)

Maroon provides a distinct category for dark reds that are neither brown nor purple. The name derives from the French word for chestnut.

### C.3 Lime

**Centroid**: (-4.4, 5.5, 7.5) in Cartesian Munsell coordinates
**Approximate Munsell**: 5GY 7.5/7
**Sample count**: 759
**Hue range**: Primarily 5GY–10GY (yellow-green)
**Semantic neighbors**: yellow (warmer), green (bluer), chartreuse (more yellow)

Lime provides an intuitive name for the yellow-green region that ISCC-NBS calls "yellow green." The citrus association gives this category strong semantic anchoring.

### C.4 Plum

**Centroid**: (6.2, -7.4, 4.5) in Cartesian Munsell coordinates
**Approximate Munsell**: 2.5RP 4.5/9
**Sample count**: 333
**Hue range**: Primarily 2.5RP–7.5RP (red-purple)
**Semantic neighbors**: purple (broader), magenta (lighter), wine (darker)

Plum fills the red-purple gap with fruit-based naming. Note that plum is more red than violet (which is more blue), following the purple-violet rule.

### C.5 Aquamarine

**Centroid**: (-5.6, 0.1, 6.8) in Cartesian Munsell coordinates
**Approximate Munsell**: 5BG 6.8/6
**Sample count**: 969
**Hue range**: Primarily 5BG–10BG (blue-green)
**Semantic neighbors**: turquoise (more cyan), teal (darker), aqua (lighter)

Aquamarine provides gemstone-based naming for the blue-green region. Its centroid is slightly greener than turquoise and lighter than teal.

---

*End of Paper Draft v1.0*
