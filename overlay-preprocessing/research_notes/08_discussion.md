# Discussion: Why Linear Correction Fails

## The Central Problem

The aggregate statistics present a misleading picture:

| Dimension | Mean Bias |
|-----------|-----------|
| Value | +0.81 |
| Chroma | +3.82 |
| Hue | -2.71° |

The near-zero mean hue bias (-2.71°) suggests hue might need only minor
correction. However, the standard deviation (±35.94°) reveals the truth:
**hue bias is highly non-uniform across color space**.

---

## 1. The Cancellation Effect

### Opposite Biases Cancel Out

| Color Region | Mean Hue Bias | n |
|--------------|---------------|---|
| Cool colors (teal, aqua, turquoise) | -35.2° | 3,596 |
| Warm earth tones (beige, tan, sand) | +30.3° | 2,336 |
| Core primaries (red, blue, purple) | -3.3° | 34,292 |

When aggregated, the cool-shift and warm-shift populations cancel, producing
a misleading near-zero mean.

### Mathematical Demonstration

```
True biases:
  teal: -41.1° (n=1,642)
  beige: +33.3° (n=755)

Weighted mean:
  (-41.1 × 1642 + 33.3 × 755) / (1642 + 755)
  = (-67,485 + 25,142) / 2,397
  = -17.7°
```

This weighted mean (-17.7°) tells us nothing useful about how to correct
either teal or beige.

---

## 2. Why Linear Correction Fails

### The Linear Model

A linear correction assumes:

```
hue_corrected = hue_screen + constant
```

For this to work, all categories must have the same hue bias. They don't:

| Category | Required Correction |
|----------|---------------------|
| teal | +41.1° |
| turquoise | +39.9° |
| beige | -33.3° |
| white | -38.2° |

### The Impossibility

No single constant can correct both:
- Cool colors (need **positive** correction)
- Warm colors (need **negative** correction)

Applying the aggregate correction (-2.71°) to all colors:
- Improves primaries slightly (already near zero)
- Worsens cool colors (-41° becomes -44°)
- Worsens warm colors (+38° becomes +35°)

---

## 3. Physical Explanations for Non-Uniform Bias

### 3.1 sRGB Gamut Limitations

The sRGB color space has a limited gamut compared to human vision:

| Region | sRGB Coverage | Effect |
|--------|---------------|--------|
| Saturated cyans | Poor | Colors pushed toward blue |
| Saturated teals | Poor | Colors pushed toward blue |
| Earth tones | Good | Colors rendered accurately |
| Saturated yellows | Moderate | Some shift toward orange |

**Result**: Cool colors (teal, cyan, turquoise) are systematically shifted
toward blue because sRGB cannot represent their true cyan hue.

### 3.2 Monitor White Point

Consumer monitors typically have:
- Color temperature: 6500K-9300K
- Slight blue bias compared to D50/D55 daylight

This blue bias:
- Makes warm colors appear relatively warmer (yellow-shifted)
- Makes cool colors appear cooler (blue-shifted)

### 3.3 Gamma Curve Effects

sRGB gamma (approximately 2.2) affects perception non-uniformly:

| Value Range | Gamma Effect |
|-------------|--------------|
| Dark colors | Compressed, less distinguishable |
| Midtones | Expanded, more distinguishable |
| Light colors | Slightly compressed |

Near-neutral colors (beige, tan, taupe) in the light-to-mid range may
experience more noticeable hue shifts due to gamma-induced saturation changes.

### 3.4 Chromatic Adaptation

Viewing self-luminous colors (monitors) differs from reflective colors (objects):

| Adaptation State | Effect |
|------------------|--------|
| Dark-adapted (typical screen viewing) | Higher sensitivity, colors appear more saturated |
| Light-adapted (viewing objects) | Normalized sensitivity |

This explains the universal chroma bias (+3.82): screen colors appear more
saturated than physical colors with the same coordinates.

---

## 4. The Non-Linear Reality

### Required Model

The correction must be a function of position in color space:

```
Δhue = f(hue, value, chroma)
```

Where f is non-linear and:
- Returns negative values (cool→cooler correction) for teal region
- Returns positive values (warm→warmer correction) for beige region
- Returns near-zero for primaries (red, blue, purple)

### Visualization

```
                    Hue Correction Required

    -40° ─────────────────┬───────────────────── +40°
                          │
    teal     cyan     blue│purple    red    beige
    ━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━
    Need +40°        Near 0°              Need -40°
    (toward cyan)                    (toward yellow)
```

---

## 5. Implications for Value and Chroma

### Value Bias: Possibly Linear

The value bias is more uniform (+0.81 ± 0.64):

| Finding | Implication |
|---------|-------------|
| 27/29 categories lighter | Consistent direction |
| Small std dev (0.64) | Low variance |
| Physical explanation clear | Self-luminous vs reflective |

**Linear correction may work**: Subtract ~0.8 from screen value.

### Chroma Bias: Possibly Linear

The chroma bias is also relatively uniform (+3.82 ± 1.35):

| Finding | Implication |
|---------|-------------|
| 29/29 categories more saturated | Perfectly consistent |
| Moderate std dev (1.35) | Some variance by category |
| Physical explanation clear | Gamut and adaptation |

**Linear correction may work**: Subtract ~3.8 from screen chroma.

### Hue Bias: Definitely Non-Linear

The hue bias requires non-linear treatment:

| Finding | Implication |
|---------|-------------|
| Mean near zero | Cancellation effect |
| High std dev (35.94°) | Extreme variance |
| Opposite signs by region | Cannot use single constant |
| Range spans 80° | Massive variation |

**Non-linear correction required**: Model must vary by hue region.

---

## 6. Comparison with Prior Work

### Monroe et al. (2008)

The XKCD survey replicates findings from Monroe et al.:
- English color vocabulary is fine-grained
- Color boundaries vary by context
- Agreement increases for focal colors

### Berlin & Kay (1969)

The category structure aligns with basic color terms:
- High-agreement categories (red, blue, green) are focal colors
- Low-agreement categories (teal, turquoise) are boundary regions

### Our Contribution

This work adds:
- Quantification of screen-to-physical bias
- Discovery of non-uniform hue bias pattern
- Evidence that linear correction is insufficient

---

## 7. Limitations

### 7.1 Data Limitations

| Limitation | Impact |
|------------|--------|
| XKCD data from 2010 | May not reflect current monitor technology |
| Uncontrolled viewing | Cannot account for individual monitor calibration |
| English-only vocabulary | May not generalize to other languages |
| Single survey | No temporal validation |

### 7.2 Methodology Limitations

| Limitation | Impact |
|------------|--------|
| Categorical matching | May miss nuanced semantic relationships |
| Centroid approximation | Polygons have internal structure |
| Circular statistics | Assumes unimodal hue distribution |
| No out-of-gamut handling | Conversion failures discarded |

### 7.3 Statistical Limitations

| Limitation | Impact |
|------------|--------|
| Unequal category sizes | Statistical power varies |
| Non-independent observations | Same users may have provided multiple colors |
| Potential confounds | Age, gender, color experience not controlled |

---

## 8. The Path Forward

### What Works

1. **Semantic validation via SBERT** - Effective for filtering noise
2. **RGB to Munsell conversion** - Mathematical approach is sound
3. **Categorical bias detection** - Reveals systematic patterns
4. **Separate treatment of dimensions** - Value/chroma may be linear

### What's Needed

1. **Non-linear hue model** - Must vary by position in color space
2. **Validation dataset** - Independent color names to test corrections
3. **Uncertainty quantification** - Per-category confidence intervals
4. **Physical verification** - Compare corrected colors to physical samples

### Proposed Next Stage

Stage 5: Non-Linear Hue Correction Modeling

Options to explore:
1. Piecewise linear by hue region
2. Polynomial in cylindrical coordinates
3. Gaussian Process regression
4. Neural network function approximation
5. Spline interpolation through category centroids

See `09_future_work.md` for detailed proposals.

