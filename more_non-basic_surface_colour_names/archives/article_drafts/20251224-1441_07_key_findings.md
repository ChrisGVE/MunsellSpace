# Key Findings: Screen-to-Physical Color Bias Analysis

## Executive Summary

Analysis of 133,359 XKCD screen colors compared against 30 Centore
spectrophotometer-measured physical color categories reveals systematic
biases that vary across color space.

**Main Result**: Linear correction is insufficient. Hue bias is non-uniform
and category-dependent, requiring non-linear modeling.

---

## 1. Universal Biases (Confirmed)

### 1.1 Value Bias: +0.81 Munsell units

| Statistic | Value |
|-----------|-------|
| Mean shift | +0.81 |
| Std dev | ±0.64 |
| Categories lighter | 27/29 (93%) |
| Range | -0.08 to +3.13 |

**Interpretation**: Screen colors appear ~0.8 Munsell Value units **lighter**
than physical colors with the same name.

**Physical Explanation**: Computer monitors are self-luminous (emitting light),
while physical colors are reflective (reflecting ambient light). Self-luminous
colors appear brighter under typical viewing conditions.

### 1.2 Chroma Bias: +3.82 Munsell units

| Statistic | Value |
|-----------|-------|
| Mean shift | +3.82 |
| Std dev | ±1.35 |
| Categories more saturated | 29/29 (100%) |
| Range | +1.50 to +6.63 |

**Interpretation**: Screen colors appear ~3.8 Munsell Chroma units **more
saturated** than physical colors with the same name.

**Physical Explanation**: sRGB monitors can display highly saturated colors
that are difficult to achieve with physical pigments. Additionally, uncalibrated
monitor gamma curves often boost color saturation.

---

## 2. Non-Uniform Hue Bias (Key Finding)

### 2.1 Aggregate Statistics

| Statistic | Value |
|-----------|-------|
| Mean shift | -2.71° |
| Std dev | ±35.94° |
| Near-zero mean | Suggests opposing shifts cancel |

**The high standard deviation (±36°) is the key indicator** that hue bias
is not uniform across color space.

### 2.2 Category-Dependent Patterns

#### Cool Colors Shift Cooler (Toward Blue)

| Category | Δ Hue | XKCD Matches |
|----------|-------|--------------|
| teal | -41.1° | 1,642 |
| turquoise | -39.9° | 857 |
| navy | -27.5° | 610 |
| aqua | -24.7° | 1,097 |
| wine | -15.3° | 270 |
| green | -10.5° | 22,990 |
| pink | -10.5° | 7,469 |

#### Warm Colors Shift Warmer (Toward Yellow/Orange)

| Category | Δ Hue | XKCD Matches |
|----------|-------|--------------|
| white | +38.2° | 1,125 |
| beige | +33.3° | 755 |
| taupe | +31.2° | 196 |
| sand | +30.4° | 441 |
| yellow | +27.8° | 5,483 |
| tan | +26.4° | 1,140 |
| gold | +23.5° | 740 |
| brown | +19.6° | 5,590 |

#### Core Primaries Are Accurate

| Category | Δ Hue | XKCD Matches |
|----------|-------|--------------|
| magenta | -0.8° | 1,099 |
| lavender | +0.9° | 815 |
| red | +3.2° | 5,931 |
| purple | -3.9° | 9,947 |
| fuchsia | -6.2° | 160 |
| violet | -7.1° | 1,567 |
| blue | -9.2° | 18,414 |

### 2.3 Visualization (Hue Shift by Category)

```
         Cooler                    Accurate                    Warmer
    ←─────────────────────────────────┬─────────────────────────────────→

    teal     turquoise    navy    blue purple red    gold    sand    white
   -41.1°     -39.9°    -27.5°  -9.2° -3.9° +3.2°  +23.5° +30.4°  +38.2°

    ●─────────●─────────●────────●────●────●────────●────────●────────●
```

---

## 3. Why Linear Correction Fails

### 3.1 The Mathematical Problem

A linear correction assumes:
```
hue_physical = hue_screen + constant
```

But the data shows:
```
For teal:   hue_physical = hue_screen + 41.1°
For beige:  hue_physical = hue_screen - 33.3°
```

These have **opposite signs** - no single constant can correct both.

### 3.2 The Non-Linear Reality

The correction must be:
```
Δhue = f(hue_screen, value, chroma)
```

Where f is a non-linear function that:
- Returns negative values for cool colors (teal region)
- Returns positive values for warm colors (beige region)
- Returns near-zero for primaries (red, blue, purple)

---

## 4. Statistical Confidence

### 4.1 Sample Sizes

| Metric | Value |
|--------|-------|
| XKCD names validated | 137,878 |
| Successfully converted to Munsell | 133,359 |
| Matched to Centore categories | 101,894 |
| Centore categories analyzed | 30 |

### 4.2 Per-Category Confidence

Categories with >5,000 matches have high statistical power:
- green: 22,990 matches
- blue: 18,414 matches
- purple: 9,947 matches
- pink: 7,469 matches
- gray: 7,104 matches (excluded from hue analysis - neutral)
- red: 5,931 matches
- brown: 5,590 matches
- yellow: 5,483 matches

Categories with <500 matches should be treated with caution:
- coral: 156 matches
- fuchsia: 160 matches
- rust: 182 matches
- taupe: 196 matches
- wine: 270 matches

---

## 5. Implications

### 5.1 For Screen-to-Physical Color Conversion

Any system converting screen colors to physical Munsell coordinates should:
1. Apply universal value correction: subtract ~0.8 units
2. Apply universal chroma correction: subtract ~3.8 units
3. Apply hue-dependent hue correction (non-linear model needed)

### 5.2 For Color Naming Research

The systematic biases suggest:
- People perceive screen colors as lighter and more saturated than physical
- Hue perception on screens diverges from physical in predictable ways
- Cool colors appear cooler on screen; warm colors appear warmer

### 5.3 For Non-Linear Modeling (Next Stage)

Recommended approaches to explore:
1. **Piecewise linear**: Different slopes for different hue regions
2. **Spline interpolation**: Smooth curve through category centroids
3. **Polynomial in cylindrical coords**: Δhue = Σ aᵢⱼₖ · hueⁱ · valueʲ · chromaᵏ
4. **Neural network**: Learn f(h, v, c) → Δh from data
5. **Gaussian Process**: Non-parametric with uncertainty quantification

---

## 6. Data Files Generated

| File | Description |
|------|-------------|
| `munsell_conversions.json` | 133,359 colors with Munsell coords |
| `munsell_conversion_summary.json` | Statistics only |
| `centore_comparison_results.json` | Full comparison with biases |
| `validated_color_names.json` | 137,878 validated names |

---

## 7. Reproducibility

All findings can be reproduced by running:

```bash
# Stage 1: Semantic validation
python semantic-investigation/full_scale_validation.py

# Stage 2: Color wheel consistency (annotation only)
python semantic-investigation/color_wheel_consistency.py

# Stage 3: RGB to Munsell conversion
python semantic-investigation/rgb_to_munsell_conversion.py

# Stage 4: Centore comparison
python semantic-investigation/centore_comparison.py
```

Git commits documenting each stage are available in the repository history.
