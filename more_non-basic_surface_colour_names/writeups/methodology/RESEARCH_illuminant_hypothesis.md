# Research Note: Illuminant Hypothesis for Screen-Physical Color Mismatch

**Date**: 2025-12-25
**Status**: Research question - not validated
**Purpose**: Explore whether the screen-physical color bias can be modeled as an illuminant transform

---

## The Problem

Observed biases between screen (XKCD) and physical (Centore) colors:
| Dimension | Bias | Screen colors appear... |
|-----------|------|-------------------------|
| Value | +0.81 | Lighter |
| Chroma | +3.82 | More saturated |
| Hue | Non-uniform | Category-dependent shifts |

**Question**: Can this be explained by illuminant differences?

---

## Background: Why Screen Colors Look Different

### Self-Luminous vs Reflected Light

**Physical colors (Centore)**:
- Reflective surfaces viewed under controlled illumination (D65 or similar)
- Light source → surface reflection → eye
- Subject to subtractive color mixing

**Screen colors (XKCD)**:
- Self-luminous RGB emitters
- Direct light emission → eye
- Additive color mixing

The perceptual difference is fundamental: self-luminous colors typically appear more saturated and brighter than equivalent reflective colors.

### sRGB Assumptions

The sRGB standard assumes:
- **Reference white**: D65 (6500K daylight)
- **Viewing conditions**: 64 lux ambient, 80 cd/m² display
- **Surround**: 20% reflectance gray

But XKCD survey conditions were:
- **Unknown monitors**: Uncalibrated, varied color temperatures
- **Unknown ambient**: Could be any lighting condition
- **Unknown surround**: Desktop backgrounds varied

---

## Hypothesis A: Effective Illuminant Shift

**Premise**: The bias pattern could be modeled as if screen colors were viewed under a different illuminant than D65.

### Chromatic Adaptation Models

**Bradford Transform** (most common):
```
XYZ_adapted = M_Bradford × XYZ_source
```

Where M_Bradford adapts from source illuminant to destination (D65).

**CIECAM02** (color appearance model):
More comprehensive, accounts for:
- Luminance level
- Surround conditions
- Chromatic adaptation degree

### Testing the Hypothesis

**Method**:
1. Take Centore's centroids as ground truth (physical, D65)
2. Take XKCD centroids as observed (screen, unknown illuminant)
3. Solve for the illuminant that minimizes the difference:
   ```
   Find I such that:
   adapt(XKCD, I → D65) ≈ Centore
   ```
4. If a consistent illuminant emerges, this supports the hypothesis

**Expected Result**:
- If bias is purely an illuminant effect, a single transform should work across all categories
- If bias is non-uniform (which we observe for hue), illuminant alone may not explain it

---

## Hypothesis B: Fluorescent Color Insight

**Premise**: Centore excluded fluorescent colors. These may provide insight.

### Why Fluorescent Colors Are Different

Fluorescent materials:
- Absorb UV/short wavelengths
- Re-emit as visible light
- Appear "enhanced" under UV-rich illumination

**Parallel to screens**: LCD screens are also UV-poor environments (no UV re-emission), but the RGB phosphors/LEDs create similar "enhanced saturation" appearance through direct emission.

### Potential Insight

If Centore's fluorescent exclusion criteria can be understood:
- What made those samples problematic?
- Did they exhibit similar bias patterns to screen colors?
- Could the exclusion logic inform our screen data handling?

---

## Hypothesis C: Hunt Effect

**Premise**: The Hunt effect describes how colorfulness increases with luminance.

**Hunt Effect**: At higher luminance levels, colors appear more saturated.

**Relevance**:
- Screen pixels can be very bright (100+ cd/m²)
- Physical samples under D65 are much dimmer
- Could explain the +3.82 chroma bias

### Testing

Compare XKCD samples taken at different monitor brightnesses (if such metadata exists, which is unlikely).

---

## Hypothesis D: Surround Effect (Helmholtz-Kohlrausch)

**Helmholtz-Kohlrausch Effect**: Saturated colors appear brighter than achromatic colors of the same luminance.

**Relevance**:
- Screen viewing often has dark surrounds
- Physical viewing typically has neutral surrounds
- Could interact with the value bias

---

## Counter-Hypothesis: Domain Mismatch

**Premise**: Screen and physical colors may represent fundamentally different perceptual domains.

### Metamerism

Two colors that match under one illuminant may not match under another. Screen colors are metameric to physical colors - they may match on the display but not in print.

**Implication**: Trying to "correct" screen colors to match physical samples may be fundamentally misguided if the perceptual experience is irreducibly different.

### Separate Domains Approach

Instead of correction:
1. Build screen-based polyhedra from XKCD (represent screen perception)
2. Keep Centore's polyhedra (represent physical perception)
3. Document the relationship but don't merge

---

## Experimental Design

### Calibration Subset Experiment

**Goal**: Determine if illuminant hypothesis holds

**Method**:
1. Select colors from non-XKCD vocabulary sources (Meodai, ColorHexa, etc.)
2. Filter to those matching Centore's 30 categories
3. Convert to Munsell (standard sRGB D65 path)
4. Compare to Centore centroids
5. Fit various models:
   - Global linear correction (baseline)
   - Illuminant transform (Bradford/CIECAM02)
   - Category-specific corrections
   - Fourier hue model (from previous work)
6. Evaluate which model best explains the data

**Success Criteria**:
- If illuminant model fits well (R² > 0.9), we have a principled correction
- If illuminant model fails, we need alternative approach

---

## Literature to Investigate

1. **Color appearance models**: Fairchild (2013) "Color Appearance Models"
2. **Self-luminous colors**: CIE TC 1-77 work on self-luminous color appearance
3. **Display colorimetry**: ICC profiles and monitor color management
4. **Munsell and illumination**: How Munsell notation changes with illuminant
5. **Fluorescent color measurement**: ASTM methods for fluorescent samples

---

## Next Steps

1. Implement Bradford transform and test on calibration subset
2. Review Centore's paper for exact fluorescent exclusion criteria
3. Investigate CIE work on self-luminous color appearance
4. Design rigorous experiment to distinguish between hypotheses

---

**Document Status**: Research note - exploratory
**Author**: Claude Code
**Date**: 2025-12-25
