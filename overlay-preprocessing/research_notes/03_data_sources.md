# Data Sources

## Overview

This research combines two fundamentally different color datasets:

1. **XKCD Color Survey** - Crowdsourced screen color names from web users
2. **Centore Polyhedron Data** - Spectrophotometer-measured physical color samples

The systematic differences between these sources reveal the biases between screen
and physical color perception.

---

## 1. XKCD Color Survey

### Origin

In 2010, Randall Munroe (creator of xkcd.com) conducted a large-scale online
color naming survey. Participants were shown randomly-generated RGB colors on
their computer screens and asked to name them.

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total color names collected | 175,844 |
| Total survey responses | ~3.4 million |
| Unique RGB values | 137,878 (after validation) |
| Collection period | 2010 |

### Data Structure

Each entry contains:
- `name`: Freeform color name entered by user
- `n`: Number of times this name was submitted
- `colors`: List of RGB hex values associated with this name

### Example Entry

```json
{
  "name": "dusty rose",
  "n": 847,
  "colors": ["#c9a1a1", "#c9a1a2", "#d4a5a5", ...]
}
```

### Key Characteristics

1. **Screen-based perception**: All colors were self-luminous (backlit LCD/CRT)
2. **Uncontrolled viewing conditions**: Varied monitor calibrations, ambient lighting
3. **Freeform naming**: No constraints on vocabulary (includes compounds, brands, jokes)
4. **Population bias**: English-speaking web users, skewed toward tech-savvy demographics
5. **Temporal snapshot**: Single time period, reflects 2010 color vocabulary

### Preprocessing Required

1. **Semantic validation**: Filter nonsense entries ("asdfgh", profanity, non-color terms)
2. **RGB averaging**: Multiple RGB values per name require averaging
3. **Character encoding**: Handle non-ASCII characters (Cyrillic, CJK, etc.)

---

## 2. Centore Polyhedron Data

### Origin

Paul Centore's "Real Colour Wheel" project provides spectrophotometer-measured
color samples organized into a 3D polyhedron structure in Munsell space.

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Color categories | 30 |
| Measurement method | Spectrophotometer |
| Color space | Munsell (H V/C) |
| Data format | Text files with polygon vertices |

### Data Structure

Each category file contains:
- Munsell coordinates for polygon vertices
- Category name (e.g., "blue", "teal", "beige")
- Polygon boundaries in Munsell space

### Categories Analyzed

**Core Colors (13)**:
red, orange, yellow, green, blue, purple, violet, pink, magenta, fuchsia, brown, gray, white

**Extended Colors (17)**:
aqua, beige, coral, gold, lavender, maroon, navy, olive, rust, salmon, sand, tan, taupe, teal, turquoise, wine, black

### Key Characteristics

1. **Physical samples**: Measured reflectance, not self-luminous
2. **Controlled conditions**: D65 illuminant, standardized geometry
3. **Munsell-native**: Coordinates directly in Munsell space
4. **Categorical boundaries**: Polygons define regions, not point estimates
5. **Expert-curated**: Based on color science expertise

### Centroid Calculation

For comparison with XKCD data, we compute category centroids:

```python
def compute_centroid(vertices):
    """Compute Munsell centroid of polygon vertices."""
    # Circular mean for hue (degrees)
    hue_angles = [v['hue'] * math.pi / 180 for v in vertices]
    mean_sin = sum(math.sin(a) for a in hue_angles) / len(hue_angles)
    mean_cos = sum(math.cos(a) for a in hue_angles) / len(hue_angles)
    mean_hue = math.atan2(mean_sin, mean_cos) * 180 / math.pi

    # Arithmetic mean for value and chroma
    mean_value = sum(v['value'] for v in vertices) / len(vertices)
    mean_chroma = sum(v['chroma'] for v in vertices) / len(vertices)

    return {'hue': mean_hue, 'value': mean_value, 'chroma': mean_chroma}
```

---

## 3. Fundamental Differences

### Perception Mode

| Aspect | XKCD | Centore |
|--------|------|---------|
| Light source | Emissive (screen) | Reflective (pigment) |
| Viewing condition | Self-luminous | Illuminated by ambient |
| Gamut | sRGB (limited) | Physical pigments |
| Adaptation | Dark-adapted typical | D65 standard |

### Measurement Quality

| Aspect | XKCD | Centore |
|--------|------|---------|
| Precision | Variable (user devices) | High (spectrophotometer) |
| Calibration | Uncalibrated | Standardized |
| Color space | RGB (device-dependent) | Munsell (perceptually uniform) |
| Uncertainty | High (crowd variance) | Low (instrument precision) |

### Semantic Scope

| Aspect | XKCD | Centore |
|--------|------|---------|
| Vocabulary | Open (freeform) | Fixed (30 categories) |
| Granularity | Fine (175K names) | Coarse (30 regions) |
| Coverage | Uneven (popular colors over-represented) | Systematic (color wheel coverage) |

---

## 4. Data Pipeline Integration

### Matching Strategy

To compare XKCD screen colors with Centore physical references:

1. **Convert XKCD RGB to Munsell**: Use mathematical conversion (ASTM D1535)
2. **Match to Centore categories**: Find category whose name matches XKCD name semantically
3. **Compute biases**: Compare XKCD Munsell position with Centore centroid

### Matching Criteria

A match occurs when:
- XKCD color name contains Centore category name (case-insensitive)
- OR Centore category name contains XKCD color name
- Examples: "light blue" matches "blue", "teal green" matches both "teal" and "green"

### Matched Data Volume

| Stage | Colors |
|-------|--------|
| XKCD validated names | 137,878 |
| Successfully converted to Munsell | 133,359 |
| Matched to Centore categories | 101,894 |

---

## 5. Data Quality Considerations

### XKCD Limitations

1. **Monitor variability**: Same RGB looks different on different screens
2. **Naming consistency**: Same color may have multiple names
3. **Cultural bias**: English-centric vocabulary
4. **Temporal bias**: 2010 color trends

### Centore Limitations

1. **Category coarseness**: 30 categories for entire color space
2. **Boundary ambiguity**: Polygon edges are arbitrary
3. **Physical substrate**: Specific pigments may not match mental prototypes

### Mitigations

1. **Large sample sizes**: Statistical power from 100K+ matched colors
2. **Semantic validation**: SBERT filtering removes noise
3. **Aggregate analysis**: Focus on category-level biases, not individual colors
4. **Multiple validation**: Cross-check with color science literature

---

## 6. File Locations

| File | Description |
|------|-------------|
| `xkcd_color_survey_data.json` | Original XKCD survey data |
| `validated_color_names.json` | 137,878 semantically validated names |
| `munsell_conversions.json` | 133,359 RGB→Munsell conversions |
| `centore_*.txt` | 30 Centore polygon files |
| `centore_comparison_results.json` | Matched colors with biases |

