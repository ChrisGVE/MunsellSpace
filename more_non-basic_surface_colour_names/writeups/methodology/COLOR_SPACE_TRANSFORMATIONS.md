# Color Space Transformations for Screen-to-Surface Color Mapping

**Research Component**: Phase 1.2 - Color Space Transformation Literature Review
**Date**: 2026-01-03
**Purpose**: Comprehensive review of color space transformations relevant to screen color (emissive RGB) to surface color (reflective Munsell) conversion

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Monitor Gamut Considerations](#2-monitor-gamut-considerations)
3. [Gamma Correction and Non-Linear Monitor Response](#3-gamma-correction-and-non-linear-monitor-response)
4. [Chromatic Adaptation Transforms](#4-chromatic-adaptation-transforms)
5. [Conversion Chains: RGB ↔ XYZ ↔ CIELAB ↔ Munsell](#5-conversion-chains-rgb--xyz--cielab--munsell)
6. [Gamut Mapping Algorithms](#6-gamut-mapping-algorithms)
7. [Error Accumulation Analysis](#7-error-accumulation-analysis)
8. [Practical Implications for Screen-to-Surface Transformation](#8-practical-implications-for-screen-to-surface-transformation)
9. [References](#9-references)

---

## 1. Introduction

### 1.1 The Screen vs. Surface Color Problem

Screen colors (emissive displays) and surface colors (reflective materials) differ fundamentally:

- **Emissive light**: Monitors emit light directly via RGB LEDs/phosphors
- **Reflective light**: Surface colors reflect ambient illumination
- **Gamut differences**: Monitors have limited gamut compared to spectral reflectance
- **Viewing conditions**: Displays are self-luminous; surfaces depend on illuminant
- **Color appearance**: Same RGB values can produce different perceptions depending on context

Converting crowdsourced RGB color names to surface color polyhedra in Munsell space requires understanding these differences and the transformation pipeline.

### 1.2 The Conversion Pipeline

The general conversion chain for screen-to-surface color mapping follows:

```
sRGB [R,G,B]
  → Gamma Correction
  → Linear RGB
  → XYZ (via 3×3 matrix)
  → Chromatic Adaptation (if needed)
  → CIELAB
  → Munsell HVC
```

Each step introduces potential errors and assumptions that accumulate through the chain.

---

## 2. Monitor Gamut Considerations

### 2.1 Color Space Gamut Comparison

Modern monitors support various RGB color spaces with different gamuts:

#### sRGB (Standard RGB)
- **Coverage**: ~35% of visible spectrum
- **Standard**: Default for web, digital content, and most monitors
- **White point**: D65 (6500K)
- **Primaries**: ITU-R BT.709 primaries
- **Use case**: Universal compatibility

**Source**: [sRGB - Wikipedia](https://en.wikipedia.org/wiki/SRGB), [W3C sRGB Specification](https://www.w3.org/Graphics/Color/sRGB.html)

#### Adobe RGB (1998)
- **Coverage**: ~50% of visible spectrum (~35% wider than sRGB)
- **Gamut bias**: Extended cyan-green range for print workflows
- **Primaries**: Same red/blue as sRGB, deeper green primary
- **Use case**: Professional photography, print preparation

**Source**: [Adobe RGB vs DCI-P3 vs sRGB](https://mobilepixels.us/blogs/blog/adobe-rgb-vs-dci-p3-vs-srgb)

#### DCI-P3 (Digital Cinema Initiative)
- **Coverage**: ~45-50% of visible spectrum (25% larger area than sRGB)
- **Gamut bias**: More evenly distributed across red, green, and blue
- **Standard**: Digital cinema, modern wide-gamut displays (Apple, modern monitors)
- **Use case**: HDR content, digital cinema, modern multimedia

**Display P3 variant**: Apple's implementation for consumer displays, using D65 white point instead of DCI's theater white point.

**Source**: [DCI-P3 - Wikipedia](https://en.wikipedia.org/wiki/DCI-P3), [Color gamuts explained: sRGB, DCI-P3, Rec 2020](https://www.androidauthority.com/color-gamuts-guide-3035782/)

### 2.2 Gamut Implications for Color Naming

**Key insight**: Crowdsourced color naming data comes from diverse monitors with varying gamuts:

- **sRGB monitors**: Most common, limited gamut
- **Wide-gamut displays**: P3 or Adobe RGB capable
- **Uncalibrated displays**: Unknown actual gamut

**Impact on data quality**:
- Same hex color displays differently on different monitors
- Highly saturated colors may be clipped on sRGB displays
- User perception influenced by their specific monitor's capabilities

**Source**: [Explaining Monitor Colour Gamut and Improving Measurement Accuracy](https://tftcentral.co.uk/articles/colour_gamut)

### 2.3 Out-of-Gamut Colors

Many surface colors have spectral reflectances that cannot be reproduced on any RGB display:

- **Fluorescent colors**: Emit more light than reflected
- **High-chroma colors**: Exceed monitor primaries
- **Surface texture effects**: Iridescence, metallic sheen

When mapping surface colors to screen RGB, out-of-gamut colors require gamut mapping (see Section 6).

---

## 3. Gamma Correction and Non-Linear Monitor Response

### 3.1 The Gamma Encoding Problem

Computer graphics systems use **gamma encoding** to optimize limited bit depth for human perception:

- **Human perception**: Logarithmic (Weber-Fechner law) - more sensitive to dark tones
- **Digital encoding**: Linear (equal steps in binary values)
- **Gamma correction**: Non-linear encoding that allocates more bits to darker values

**Source**: [Gamma correction - Wikipedia](https://en.wikipedia.org/wiki/Gamma_correction)

### 3.2 sRGB Transfer Function

The sRGB standard defines a **piecewise transfer function** (not pure gamma 2.2):

```
Encoding (linear → sRGB):
  C_srgb = 12.92 * C_linear                    if C_linear ≤ 0.0031308
  C_srgb = 1.055 * C_linear^(1/2.4) - 0.055    if C_linear > 0.0031308

Decoding (sRGB → linear):
  C_linear = C_srgb / 12.92                          if C_srgb ≤ 0.04045
  C_linear = ((C_srgb + 0.055) / 1.055)^2.4          if C_srgb > 0.04045
```

**Approximation**: The sRGB curve approximates **gamma 2.2** but has a linear segment near black to avoid infinite slope at zero.

**Source**: [sRGB - Wikipedia](https://en.wikipedia.org/wiki/SRGB), [A Standard Default Color Space for the Internet - sRGB](https://www.w3.org/Graphics/Color/sRGB.html)

### 3.3 ICC Profiles and Color Management

**ICC (International Color Consortium) profiles** describe device color behavior:

- **Tone Response Curve (TRC)**: Describes the gamma/transfer function
- **Chromatic adaptation**: Transforms between different white points
- **Look-Up Tables (LUTs)**: For complex non-linear transformations

Modern operating systems use ICC profiles to ensure consistent color across devices:

- **Windows**: Display Color Calibration (dccw.exe) creates ICC profiles
- **macOS**: ColorSync framework manages ICC profiles
- **Linux**: Various tools (DisplayCAL, Argyll CMS)

**Hardware calibration**: Colorimeters (X-Rite, Datacolor) measure actual display output and generate accurate ICC profiles.

**Source**: [Using ICC Profiles in Windows](https://pcmonitors.info/articles/using-icc-profiles-in-windows/), [Gamma and Linear - Krita Manual](https://docs.krita.org/en/general_concepts/colors/linear_and_gamma.html)

### 3.4 Practical Considerations

**For crowdsourced data**:
- Most users do NOT have calibrated monitors
- Assumption: sRGB gamma 2.2 approximation is reasonable default
- Reality: Individual monitors may deviate significantly
- Mitigation: Large sample sizes may average out calibration variations

**For color science research**:
- Always work in **linear RGB** for mathematical operations
- Apply gamma correction only for display or storage
- Document assumed transfer function explicitly

**Source**: [Gamma correction and Precision Color](http://www.libpng.org/pub/png/book/chapter10.html)

---

## 4. Chromatic Adaptation Transforms

### 4.1 The Chromatic Adaptation Problem

Human vision adapts to ambient illumination - a white sheet of paper appears white under both daylight (D65, ~6500K) and incandescent light (A, ~2856K), even though the physical light spectra differ dramatically.

**Color conversion problem**:
- Munsell colors were measured under **Illuminant C** (average daylight, ~6774K)
- Modern color spaces use **Illuminant D65** (standard daylight, ~6504K)
- sRGB uses **D65** as white point

**Solution**: Chromatic adaptation transforms (CATs) convert color appearance between different illuminants.

### 4.2 Von Kries Transform

The **von Kries hypothesis** (1902) proposed that chromatic adaptation occurs via independent gain control in the three cone types (L, M, S).

**Mathematical form**:
```
1. Convert XYZ to cone response space: ρ = M_adapt * XYZ
2. Apply diagonal scaling:          ρ' = D * ρ
3. Convert back to XYZ:             XYZ' = M_adapt^(-1) * ρ'

Where D is a diagonal matrix:
D = diag(ρ_dest / ρ_src)
```

**Key properties**:
- **Symmetric**: Forward and reverse transformations are reciprocal
- **Transitive**: Adapting A→B→C equals A→C
- **Diagonal assumption**: Cones adapt independently (biologically questionable but works well)

**Source**: [The von Kries chromatic adaptation transform and its generalization](https://opg.optica.org/col/abstract.cfm?URI=col-18-3-033301), [Chromatic adaptation - Wikipedia](https://en.wikipedia.org/wiki/Chromatic_adaptation)

### 4.3 Common Chromatic Adaptation Matrices

Different CATs use different "cone response" spaces (not actual cone sensitivities):

#### Bradford Transform
- **Matrix**: Calculated from 58 pairs of corresponding colors
- **Performance**: Best overall for most applications
- **Characteristics**: "Sharpened" cone responses with less overlap

```
M_Bradford =
[[ 0.8951,  0.2664, -0.1614],
 [-0.7502,  1.7135,  0.0367],
 [ 0.0389, -0.0685,  1.0296]]
```

**Source**: [Chromatic adaptation • Color.js](https://colorjs.io/docs/adaptation)

#### CAT02
- **Origin**: Part of CIECAM02 color appearance model
- **Matrix**: Slightly different from Bradford
- **Usage**: Widely used in modern color appearance models

```
M_CAT02 =
[[ 0.7328,  0.4296, -0.1624],
 [-0.7036,  1.6975,  0.0061],
 [ 0.0030,  0.0136,  0.9834]]
```

**Source**: [colour.adaptation.cat Module — Colour 0.3.0 documentation](https://www.colour-science.org/api/0.3.0/html/colour.adaptation.cat.html)

#### CAT16
- **Origin**: Part of CAM16 (successor to CIECAM02)
- **Improvements**: Fixes gamut issues in CAT02, ensures symmetry and transitivity
- **Two-step process**: Ensures mathematical properties are preserved
- **Issue**: Standalone CAT16 can cause inconsistencies; best used within CAM16

**Source**: [Some concerns regarding the CAT16 chromatic adaptation transform](https://www.researchgate.net/publication/337354547_Some_concerns_regarding_the_CAT16_chromatic_adaptation_transform)

#### Von Kries (Original)
- **Matrix**: Based on Hunt-Pointer-Estevez cone fundamentals
- **Performance**: Works well for similar daylight illuminants, poor for very different sources

### 4.4 Performance Comparison

**Empirical findings** (from generalized von Kries research):

- **CAT02**: Slightly outperforms CAT16 on most datasets due to sharpened sensor space
- **Bradford**: Most widely used, excellent practical performance
- **CAT16**: Best for avoiding negative tristimulus values, maintains symmetry/transitivity

**Recommendation for Munsell conversion**:
- Use **Bradford** for general-purpose C→D65 adaptation
- Use **CAT02** for consistency with CIECAM02-based workflows
- Document which transform is used

**Source**: [The von Kries chromatic adaptation transform and its generalization](https://www.researchgate.net/publication/339727107_The_von_Kries_chromatic_adaptation_transform_and_its_generalization)

### 4.5 Practical Implementation

**Python example using colour-science library**:
```python
import colour

# XYZ under Illuminant C
XYZ_C = [0.20, 0.30, 0.40]

# Adapt to D65 using Bradford
XYZ_D65 = colour.adaptation.chromatic_adaptation_VonKries(
    XYZ=XYZ_C,
    XYZ_w=colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C'],
    XYZ_wr=colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'],
    transform='Bradford'
)
```

**Source**: [colour.adaptation.chromatic_adaptation_VonKries](https://colour.readthedocs.io/en/develop/generated/colour.adaptation.chromatic_adaptation_VonKries.html)

---

## 5. Conversion Chains: RGB ↔ XYZ ↔ CIELAB ↔ Munsell

### 5.1 RGB to XYZ Conversion

**For sRGB with D65 white point**:

```
Step 1: Gamma correction (sRGB → linear RGB)
  R_linear = ((R_srgb + 0.055) / 1.055)^2.4  [if R_srgb > 0.04045]
  (similar for G and B)

Step 2: Matrix multiplication (linear RGB → XYZ)
  [X]   [ 0.4124564  0.3575761  0.1804375 ] [R_linear]
  [Y] = [ 0.2126729  0.7151522  0.0721750 ] [G_linear]
  [Z]   [ 0.0193339  0.1191920  0.9503041 ] [B_linear]
```

**Inverse (XYZ → sRGB)**:
```
Step 1: Matrix multiplication (XYZ → linear RGB)
  [R_linear]   [  3.2404542 -1.5371385 -0.4985314 ] [X]
  [G_linear] = [ -0.9692660  1.8760108  0.0415560 ] [Y]
  [B_linear]   [  0.0556434 -0.2040259  1.0572252 ] [Z]

Step 2: Gamma encoding (linear RGB → sRGB)
  R_srgb = 1.055 * R_linear^(1/2.4) - 0.055  [if R_linear > 0.0031308]
```

**Notes**:
- Matrix values derived from sRGB primaries and D65 white point
- Matrix is **exact** for the defined primaries
- Precision matters - use full precision values, round only for display

**Source**: [Rec. 709 - Wikipedia](https://en.wikipedia.org/wiki/Rec._709), [Understanding Color Space Conversions in Display](https://www.synopsys.com/blogs/chip-design/color-space-conversions-display.html)

### 5.2 XYZ to CIELAB Conversion

**CIELAB** is a perceptually uniform color space with:
- **L***: Lightness (0 = black, 100 = white)
- **a***: Green-red axis (negative = green, positive = red)
- **b***: Blue-yellow axis (negative = blue, positive = yellow)

**Conversion** (assuming D65 white point):
```
X_n = 95.047  (D65 white point, Y = 100)
Y_n = 100.000
Z_n = 108.883

f(t) = t^(1/3)                if t > (6/29)^3
     = (1/3) * (29/6)^2 * t + 4/29    otherwise

L* = 116 * f(Y / Y_n) - 16
a* = 500 * [f(X / X_n) - f(Y / Y_n)]
b* = 200 * [f(Y / Y_n) - f(Z / Z_n)]
```

**Inverse** (CIELAB → XYZ):
```
f_y = (L* + 16) / 116
f_x = a* / 500 + f_y
f_z = f_y - b* / 200

f_inv(t) = t^3                     if t > 6/29
         = 3 * (6/29)^2 * (t - 4/29)    otherwise

X = X_n * f_inv(f_x)
Y = Y_n * f_inv(f_y)
Z = Z_n * f_inv(f_z)
```

**Source**: [colour.RGB_Colourspace](https://colour.readthedocs.io/en/develop/generated/colour.RGB_Colourspace.html)

### 5.3 XYZ/CIELAB to Munsell Conversion

**The Munsell Renotation Problem**:

Munsell notation (HVC: Hue, Value, Chroma) was developed empirically. The **1943 Munsell Renotation** provides a lookup table relating 2,734 Munsell chips to CIE xyY coordinates (Illuminant C, 2° observer).

**Forward conversion (Munsell → CIE)**:
- **Direct lookup**: If Munsell specification matches a renotation entry
- **Interpolation**: For intermediate values, interpolate between nearby chips
- **Extrapolation**: For out-of-renotation-range colors (use cautiously)

**Inverse conversion (CIE → Munsell)**:
- **Nearest neighbor**: Find closest Munsell chip by ΔE
- **Iterative search**: Search Munsell space for minimum distance
- **Interpolation**: Interpolate between adjacent chips for sub-chip precision

**Accuracy considerations**:
- **Renotation data limitations**: Only 2,734 chips, extrapolated regions less reliable
- **Illuminant C vs D65**: Requires chromatic adaptation (typically Bradford)
- **Gamut boundaries**: Not all colors have valid Munsell notations

**Software implementations**:
- **munsellinterpol** (R): Interpolates Munsell renotation data
- **colour-science** (Python): Provides Munsell conversion utilities
- **MunsellSpace** (Rust, this project): ASTM D1535 mathematical converter

**Sources**:
- [Munsell Color Conversion • aqp](https://ncss-tech.github.io/aqp/articles/Munsell-color-conversion.html)
- [MunsellToLab in munsellinterpol](https://rdrr.io/cran/munsellinterpol/man/MunsellToLab.html)
- [Interpolate Munsell Renotation Data](https://cran.r-project.org/web/packages/munsellinterpol/munsellinterpol.pdf)

### 5.4 Complete Conversion Chain Example

**RGB → Munsell**:
```
1. sRGB [206, 123, 89] (web color)
2. Gamma correction → Linear RGB [0.5849, 0.2190, 0.1034]
3. Matrix mult → XYZ_D65 [0.3015, 0.2473, 0.1156]
4. (Optional) Adapt D65→C → XYZ_C [0.3085, 0.2473, 0.1065]
5. XYZ → LAB [56.42, 27.18, 28.03]
6. Munsell lookup/interpolation → 5.2YR 5.6/5.8
```

**Munsell → RGB**:
```
1. Munsell 5R 5/10 (red surface color)
2. Interpolate renotation → xyY_C [0.456, 0.345, 24.5]
3. xyY → XYZ_C [0.324, 0.245, 0.086]
4. Adapt C→D65 → XYZ_D65 [0.317, 0.245, 0.094]
5. XYZ → Linear RGB [0.692, 0.189, 0.098]
6. Check gamut (may need clipping)
7. Gamma encode → sRGB [210, 103, 80]
```

**Source**: [Munsell Color Conversion](https://cran.r-project.org/web/packages/aqp/vignettes/Munsell-color-conversion.html)

---

## 6. Gamut Mapping Algorithms

### 6.1 The Gamut Mapping Problem

**Definition**: Converting colors outside a target gamut to valid in-gamut colors while preserving appearance as much as possible.

**Arises when**:
- Converting wide-gamut surface colors to narrow-gamut display RGB
- Converting between different RGB spaces (Adobe RGB → sRGB)
- Converting spectral colors to any RGB space

**Source**: [Gamut Mapping - ColorAide Documentation](https://facelessuser.github.io/coloraide/gamut/)

### 6.2 Clipping vs. Compression

**Simple clipping**: Set out-of-gamut component values to 0 or 1
- **Pros**: Fast, preserves in-gamut colors exactly
- **Cons**: Hue and saturation shifts, harsh artifacts at gamut boundary

**Compression**: Gradually reduce colorfulness of all colors
- **Pros**: Smooth transitions, preserves relative relationships
- **Cons**: Reduces colorfulness of in-gamut colors unnecessarily

**Source**: [Colour gamut mapping between small and large colour gamuts](https://www.researchgate.net/publication/324614038_Colour_gamut_mapping_between_small_and_large_colour_gamuts_Part_I_gamut_compression)

### 6.3 Perceptual Gamut Mapping Strategies

#### Chroma Reduction
- **Method**: Reduce chroma in polar color space (e.g., LCh) until in-gamut
- **Preserves**: Hue and lightness
- **Cost**: Reduced saturation/colorfulness

**Algorithm** (CSS Color Level 4 approach):
```
1. Convert to Oklch (perceptual hue-chroma-lightness space)
2. Binary search for chroma value where:
   - Color is just inside gamut
   - ΔE (difference from clipped version) < JND (just noticeable difference)
3. Use deltaEOK for difference metric
```

**Source**: [Gamut mapping • Color.js](https://colorjs.io/docs/gamut-mapping), [sRGB gamut clipping](https://bottosson.github.io/posts/gamutclipping/)

#### MINDE (Minimum Delta E)
- **Method**: Find in-gamut color with shortest perceptual distance (ΔE) to out-of-gamut color
- **Preserves**: Best perceptual match
- **Cost**: May allow more hue shift than chroma reduction, computationally expensive

**Source**: [Gamut Mapping - ColorAide Documentation](https://facelessuser.github.io/coloraide/gamut/)

#### HPMINDE (Hue Preserving Minimum ΔE)
- **Method**: Clip to gamut boundary along constant hue lines
- **Preserves**: Hue (strictly)
- **Cost**: May sacrifice lightness or chroma

**Algorithm**:
1. Convert to perceptual polar space (e.g., CIELAB → LCh_ab)
2. Hold hue constant
3. Search along L-C plane for minimum ΔE point on gamut boundary

**Source**: [Hue Preserving Minimum Color Difference Gamut Clipping (HPMINDE)](https://shankhya.github.io/musings/hpminde.pdf), [Gamut Mapping through Perceptually-Based Contrast Reduction](https://www.researchgate.net/publication/263301749_Gamut_Mapping_through_Perceptually-Based_Contrast_Reduction)

### 6.4 Rendering Intents (ICC Standard)

**Perceptual**:
- Compress entire color space to fit in gamut
- Maintains relationships between colors
- Best for photographic images

**Relative Colorimetric**:
- Clip out-of-gamut colors to boundary
- Preserve in-gamut colors exactly
- Best for logos, spot colors

**Saturation**:
- Maximize saturation/vividness
- Allow hue shifts
- Best for business graphics

**Absolute Colorimetric**:
- Preserve absolute color appearance (including white point)
- Rare use case

**Source**: [Improve gamut mapping of Color Management System](https://www.researchgate.net/publication/252322606_Improve_gamut_mapping_of_Color_Management_System_by_perceptual_quality-oriented_analysis)

### 6.5 Recommended Approaches

**For surface color → screen conversion**:
1. Check if in sRGB gamut after conversion
2. If not, use **chroma reduction** with constant hue/lightness
3. Work in perceptually uniform space (Oklch or LCh_ab)
4. Document % of colors requiring gamut mapping

**For screen color → surface analysis**:
- Most screen colors are within surface color gamut
- Gamut mapping rarely needed
- Exception: Highly saturated blues/cyans near sRGB gamut boundary

---

## 7. Error Accumulation Analysis

### 7.1 Sources of Error in Conversion Chains

Each step in the conversion pipeline introduces potential errors:

| Conversion Step | Error Source | Magnitude |
|----------------|--------------|-----------|
| RGB → Linear RGB | Gamma function approximation | < 0.5% |
| Linear RGB → XYZ | Rounding in matrix values | < 0.1% |
| XYZ_D65 → XYZ_C | Chromatic adaptation accuracy | ~1-2% (ΔE) |
| XYZ → CIELAB | Cube root approximation near black | Variable |
| CIELAB → Munsell | Interpolation/lookup errors | 0.5-3 ΔE units |
| **Total chain** | **Cumulative** | **1.5-5 ΔE units** |

**Source**: [Conversion between CIELAB and Munsell Hue](https://www.researchgate.net/publication/234005891_Conversion_between_CIELAB_and_Munsell_Hue)

### 7.2 Munsell Conversion Accuracy

**Best-case accuracy** (distance-weighted LUT with CIEDE2000):
- **Root mean square error**: ~1 Munsell hue unit
- **Transformation accuracy**: 88.4% (basic matrix), 96.6% (with residual correction)

**Polynomial methods** (predicting Munsell from CIELAB):
- Generally poor performance (~70-80% accuracy)
- No one-to-one mapping between L*C*h and Munsell HVC

**Source**:
- [Conversion between CIELAB and Munsell Hue](https://www.researchgate.net/publication/234005891_Conversion_between_CIELAB_and_Munsell_Hue)
- [Different transformation methods between CIELAB coordinates and Munsell hue](https://www.researchgate.net/publication/230428930_Different_transformation_methods_between_CIELAB_coordinates_and_Munsell_hue)

### 7.3 Round-Trip Errors

**Ideal**: HVC → xyY → HVC should recover original Munsell specification

**Reality** (munsellinterpol package):
- Most colors: < 0.1 Munsell units error
- Very dark samples (V < 1): Potentially larger errors
- Out-of-renotation colors: Errors increase with extrapolation distance

**Source**: [munsellinterpol User Guide](https://cran.r-project.org/web//packages//munsellinterpol/vignettes/munsellinterpol-guide.html)

### 7.4 Systematic vs. Random Errors

**Random errors** (average out with large N):
- Rounding in calculations
- Interpolation noise
- Individual monitor calibration variations

**Systematic errors** (do NOT average out):
- Wrong chromatic adaptation method
- Incorrect gamma assumption
- Gamut mapping bias
- Illuminant mismatch

**Implication for research**:
- Large sample sizes help with random errors
- Systematic errors require careful methodological choices
- Document all assumptions explicitly

### 7.5 Practical Error Mitigation

**Best practices**:
1. Use high-precision arithmetic (64-bit float minimum)
2. Document all transformation matrices and parameters
3. Use validated libraries (colour-science, MunsellSpace)
4. Validate round-trip conversions on known test colors
5. Report error estimates with all derived data
6. Use perceptually uniform spaces (CIELAB, Oklch) for distance metrics

**Validation test suite**:
- Known Munsell renotation chips
- Macbeth ColorChecker patches
- sRGB primary/secondary colors
- Achromatic series (black-gray-white)

---

## 8. Practical Implications for Screen-to-Surface Transformation

### 8.1 Key Challenges

**Fundamental differences**:
1. **Emissive vs. reflective**: Monitors emit light; surfaces reflect it
2. **Self-luminous vs. illuminant-dependent**: Screens don't depend on ambient light
3. **Gamut mismatch**: sRGB ⊂ surface color gamut (mostly)
4. **Uncalibrated data**: Crowdsourced color names from diverse, uncalibrated displays

### 8.2 Assumptions for Large-N Data

**Hypothesis**: With sufficient samples, individual calibration noise averages out, revealing "true" color category centers.

**Required validations**:
- Test distribution symmetry around centroids (Section 5, Phase 5)
- Account for non-homogeneous Munsell space (ellipsoid fitting)
- Compare systematic vs. random error components
- Analyze residual distributions

### 8.3 Recommended Conversion Pipeline

**For crowdsourced RGB → Munsell**:
```
1. Assume sRGB color space (most common)
2. Apply sRGB gamma correction → linear RGB
3. Linear RGB → XYZ_D65 (ITU-R BT.709 matrix)
4. (Optional) Chromatic adapt D65 → C using Bradford
5. XYZ → CIELAB
6. CIELAB → Munsell using validated interpolation (MunsellSpace Rust library)
7. Document conversion parameters
```

**Error budget**:
- Gamma assumption: ~1-2% (uncalibrated monitors vary)
- Chromatic adaptation: ~1 ΔE unit
- Munsell interpolation: ~0.5-1.5 ΔE units
- **Total expected error**: ~2-4 ΔE units per color

**Mitigation with large samples**:
- Random errors average out across thousands of samples
- Systematic errors remain (document and account for)

### 8.4 Open Research Questions

1. **Is there a learnable transformation** between screen and surface color polyhedra?
2. **How much error is acceptable** for semantic color categories?
3. **Do different color families** require different transformation parameters?
4. **Can we validate** the large-N averaging hypothesis empirically?

These questions will be addressed in subsequent research phases.

---

## 9. References

### Chromatic Adaptation
- [Chromatic adaptation - Wikipedia](https://en.wikipedia.org/wiki/Chromatic_adaptation)
- [The von Kries chromatic adaptation transform and its generalization](https://opg.optica.org/col/abstract.cfm?URI=col-18-3-033301)
- [Chromatic adaptation • Color.js](https://colorjs.io/docs/adaptation)
- [colour.adaptation.cat Module — Colour 0.3.0 documentation](https://www.colour-science.org/api/0.3.0/html/colour.adaptation.cat.html)
- [Some concerns regarding the CAT16 chromatic adaptation transform](https://www.researchgate.net/publication/337354547_Some_concerns_regarding_the_CAT16_chromatic_adaptation_transform)

### Monitor Gamuts
- [sRGB - Wikipedia](https://en.wikipedia.org/wiki/SRGB)
- [DCI-P3 - Wikipedia](https://en.wikipedia.org/wiki/DCI-P3)
- [Color gamuts explained: sRGB, DCI-P3, Rec 2020](https://www.androidauthority.com/color-gamuts-guide-3035782/)
- [Adobe RGB vs DCI-P3 vs sRGB](https://mobilepixels.us/blogs/blog/adobe-rgb-vs-dci-p3-vs-srgb)
- [Explaining Monitor Colour Gamut and Improving Measurement Accuracy](https://tftcentral.co.uk/articles/colour_gamut)

### Gamma Correction
- [Gamma correction - Wikipedia](https://en.wikipedia.org/wiki/Gamma_correction)
- [A Standard Default Color Space for the Internet - sRGB](https://www.w3.org/Graphics/Color/sRGB.html)
- [Gamma and Linear - Krita Manual](https://docs.krita.org/en/general_concepts/colors/linear_and_gamma.html)
- [Gamma correction and Precision Color](http://www.libpng.org/pub/png/book/chapter10.html)
- [Using ICC Profiles in Windows](https://pcmonitors.info/articles/using-icc-profiles-in-windows/)

### Color Space Conversions
- [Rec. 709 - Wikipedia](https://en.wikipedia.org/wiki/Rec._709)
- [Understanding Color Space Conversions in Display](https://www.synopsys.com/blogs/chip-design/color-space-conversions-display.html)
- [colour.RGB_Colourspace](https://colour.readthedocs.io/en/develop/generated/colour.RGB_Colourspace.html)

### Munsell Conversions
- [Munsell Color Conversion • aqp](https://ncss-tech.github.io/aqp/articles/Munsell-color-conversion.html)
- [MunsellToLab in munsellinterpol](https://rdrr.io/cran/munsellinterpol/man/MunsellToLab.html)
- [Interpolate Munsell Renotation Data](https://cran.r-project.org/web/packages/munsellinterpol/munsellinterpol.pdf)
- [Conversion between CIELAB and Munsell Hue](https://www.researchgate.net/publication/234005891_Conversion_between_CIELAB_and_Munsell_Hue)

### Gamut Mapping
- [Gamut Mapping - ColorAide Documentation](https://facelessuser.github.io/coloraide/gamut/)
- [Gamut mapping • Color.js](https://colorjs.io/docs/gamut-mapping)
- [sRGB gamut clipping](https://bottosson.github.io/posts/gamutclipping/)
- [Hue Preserving Minimum Color Difference Gamut Clipping (HPMINDE)](https://shankhya.github.io/musings/hpminde.pdf)
- [Gamut Mapping through Perceptually-Based Contrast Reduction](https://www.researchgate.net/publication/263301749_Gamut_Mapping_through_Perceptually-Based_Contrast_Reduction)
- [Improve gamut mapping of Color Management System](https://www.researchgate.net/publication/252322606_Improve_gamut_mapping_of_Color_Management_System_by_perceptual_quality-oriented_analysis)

### Error Analysis
- [Conversion between CIELAB and Munsell Hue](https://www.researchgate.net/publication/234005891_Conversion_between_CIELAB_and_Munsell_Hue)
- [Different transformation methods between CIELAB coordinates and Munsell hue](https://www.researchgate.net/publication/230428930_Different_transformation_methods_between_CIELAB_coordinates_and_Munsell_hue)
- [munsellinterpol User Guide](https://cran.r-project.org/web//packages//munsellinterpol/vignettes/munsellinterpol-guide.html)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-03
**Next Steps**: Implement color transformation functions (Phase 1.2, Deliverable 2)
