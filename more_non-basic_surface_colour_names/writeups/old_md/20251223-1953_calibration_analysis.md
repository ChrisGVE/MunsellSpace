# Phase 4: Calibration Analysis Report

## 1. Executive Summary

This analysis compares XKCD (RGB) and Centore (Munsell) color coordinates
using shared overlay color names as calibration reference points.

| Metric | Value |
|--------|-------|
| Shared overlay colors | 20 |
| Shared basic colors | 10 |
| Total comparisons | 30 |

## 2. Methodology

### 2.1 Coordinate Systems
- **XKCD**: RGB (0-255), from uncalibrated consumer monitors
- **Centore**: Munsell HVC, from spectrophotometer measurements

### 2.2 Comparison Approach
1. Compute XKCD RGB centroid for each shared color name
2. Extract Centore Munsell centroid from polyhedron data
3. Convert RGB to approximate Munsell-comparable metrics:
   - **Hue**: RGB → HSV → Hue angle (0-360°)
   - **Value**: RGB luminance → approximate Munsell Value (0-10)
   - **Chroma**: HSV saturation → approximate Munsell Chroma
4. Compute differences and test for systematic bias

### 2.3 Limitations
- RGB-to-Munsell conversion is approximate
- XKCD monitors were uncalibrated (random viewing conditions)
- Centore uses illuminant C; sRGB assumes D65
- Full analysis requires proper colorimetric conversion

## 3. Calibration Point Comparison

| Color | XKCD RGB | Centore Munsell | Hue Δ | Value Δ | Chroma Δ | XKCD n |
|-------|----------|-----------------|-------|---------|----------|--------|
| aqua | (62,206,189) | 7.44BG 6.18/3.37 | -33.8° | 0.64 | 5.03 | 23,317 |
| beige | (211,192,133) | 6.66YR 6.15/3.40 | -14.5° | 1.39 | 1.06 | 14,322 |
| blue | (55,97,198) | 0.56PB 4.69/4.64 | -31.6° | -0.95 | 4.01 | 288,015 |
| brown | (136,90,44) | 2.84YR 3.95/3.70 | -16.4° | -0.17 | 4.46 | 75,812 |
| coral | (230,100,92) | 6.53R 5.84/8.28 | -20.2° | -0.85 | -1.11 | 2,260 |
| fuchsia | (209,46,168) | 4.78RP 4.09/10.33 | -26.1° | -0.60 | -0.94 | 3,471 |
| gold | (207,176,40) | 9.79YR 6.39/7.35 | -22.1° | 0.39 | 2.35 | 6,265 |
| gray | (143,147,143) | 9.62P 5.25/0.55 | 157.5° | 0.47 | -0.19 | 18,241 |
| green | (74,185,68) | 2.04G 5.33/4.75 | -34.7° | 0.68 | 2.86 | 314,172 |
| lavender | (177,126,208) | 5.61P 5.37/4.79 | -31.2° | 0.24 | -0.08 | 25,800 |
| lilac | (179,123,209) | 7.75P 5.61/4.83 | -36.9° | -0.09 | 0.11 | 15,703 |
| magenta | (200,39,152) | 3.82RP 3.37/9.39 | -19.9° | -0.17 | 0.26 | 43,724 |
| mauve | (167,94,142) | 1.19RP 5.15/3.85 | -7.5° | -0.71 | 1.35 | 19,149 |
| navy | (32,45,104) | 7.26PB 2.11/3.61 | -49.0° | -0.30 | 4.71 | 7,213 |
| orange | (228,122,38) | 2.50YR 5.69/8.86 | -18.4° | -0.25 | 1.16 | 52,200 |
| peach | (238,165,119) | 2.89YR 7.03/5.86 | -23.0° | -0.07 | 0.11 | 12,023 |
| pink | (227,91,169) | 0.70R 5.76/7.88 | -36.8° | -0.83 | -0.71 | 131,013 |
| purple | (142,53,173) | 6.81P 3.53/6.45 | -28.1° | -0.37 | 1.87 | 249,199 |
| red | (204,38,44) | 4.27R 3.79/8.82 | -17.6° | -0.90 | 0.94 | 69,928 |
| rose | (213,98,129) | 0.47R 4.99/7.69 | -18.0° | -0.11 | -1.21 | 8,810 |
| rust | (172,73,37) | 9.42R 3.95/7.37 | -18.2° | -0.37 | 2.03 | 3,170 |
| sand | (211,187,107) | 7.60YR 6.26/3.19 | -16.8° | 1.06 | 2.74 | 3,685 |
| tan | (203,172,103) | 6.30YR 5.23/4.07 | -17.2° | 1.59 | 1.83 | 23,977 |
| taupe | (175,156,115) | 3.25YR 4.68/1.42 | -6.2° | 1.48 | 2.72 | 4,210 |
| teal | (57,179,159) | 1.56B 3.32/4.53 | -51.4° | 2.63 | 3.67 | 57,128 |
| turquoise | (54,195,178) | 1.61B 5.45/5.92 | -48.9° | 0.97 | 2.77 | 26,313 |
| violet | (143,60,181) | 7.00P 3.80/6.16 | -32.0° | -0.40 | 1.85 | 32,806 |
| white | (225,227,218) | 2.07Y 8.01/2.02 | -5.5° | 0.84 | -1.57 | 2,427 |
| wine | (134,32,69) | 2.69R 2.98/4.85 | -31.6° | -0.77 | 4.30 | 1,559 |
| yellow | (227,221,54) | 2.64Y 7.44/7.98 | -23.3° | 0.81 | 1.16 | 44,073 |

## 4. Systematic Bias Analysis

### 4.1 Test for Systematic Differences

| Dimension | n | Mean Δ | Std | t-stat | Systematic? |
|-----------|---|--------|-----|--------|-------------|
| Hue | 30 | -19.31 | 35.44 | 2.98 | **YES** |
| Value | 30 | 0.18 | 0.88 | 1.09 | no |
| Chroma | 30 | 1.58 | 1.89 | 4.59 | **YES** |

### 4.2 Interpretation

**Hue**: Systematic bias detected. XKCD colors appear bluer 
than Centore by ~19.3° on average.

**Value**: No significant systematic bias. Differences appear random.

**Chroma**: Systematic bias detected. XKCD colors appear more saturated 
than Centore by ~1.58 Chroma units.

## 5. Recommendations

### 5.1 If Systematic Bias Found
1. Consider applying a global correction transformation
2. Use regression analysis to fit correction parameters
3. Validate correction on held-out colors

### 5.2 If No Systematic Bias
1. Differences may be due to random monitor variation
2. Consider using robust statistics (median) for aggregation
3. Document uncertainty without applying corrections

### 5.3 For Full Analysis
1. Install MunsellSpace Python library for accurate RGB→Munsell conversion
2. Use colorimetric transforms (sRGB → XYZ → Munsell)
3. Account for illuminant differences (D65 vs C)

## 6. Uncertainty Budget

| Source | Impact | Mitigation |
|--------|--------|------------|
| Uncalibrated monitors | High | Use large sample sizes |
| RGB-Munsell approximation | Medium | Use proper conversion |
| Illuminant difference | Low-Medium | Apply chromatic adaptation |
| Sample size variation | Low | Weight by sample count |

---

*Generated by Phase 4: Calibration Analysis*