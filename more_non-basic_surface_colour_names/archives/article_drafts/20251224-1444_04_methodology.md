# Methodology: Four-Stage Pipeline

## Overview

The research follows a four-stage pipeline that progressively transforms raw
crowdsourced color data into quantified screen-to-physical color biases.

```
Stage 1: Semantic Validation
    ↓
Stage 2: Color Wheel Consistency (Annotation)
    ↓
Stage 3: RGB to Munsell Conversion
    ↓
Stage 4: Centore Comparison & Bias Detection
```

---

## Stage 1: Semantic Validation

### Goal

Filter the 175,844 XKCD color names to retain only those that are semantically
valid color descriptions.

### Approach: SBERT Sentence Embeddings

We use Sentence-BERT (SBERT) to compute semantic similarity between each XKCD
name and a reference set of known color terms.

### Reference Vocabulary

```python
reference_colors = [
    "red", "orange", "yellow", "green", "blue", "purple", "pink", "brown",
    "black", "white", "gray", "grey", "cyan", "magenta", "violet", "indigo",
    "maroon", "navy", "olive", "teal", "aqua", "coral", "salmon", "tan",
    "beige", "ivory", "cream", "gold", "silver", "bronze", "copper",
    "crimson", "scarlet", "burgundy", "lavender", "lilac", "plum",
    "turquoise", "chartreuse", "lime", "mint", "forest", "emerald",
    "azure", "sapphire", "cobalt", "cerulean", "periwinkle", "mauve",
    "fuchsia", "rose", "blush", "peach", "apricot", "rust", "sienna",
    "umber", "ochre", "khaki", "taupe", "sand", "buff", "ecru"
]
```

### Similarity Computation

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def validate_color_name(name):
    """Return True if name is semantically similar to any reference color."""
    name_embedding = model.encode(name)

    for ref_color in reference_colors:
        ref_embedding = model.encode(ref_color)
        similarity = cosine_similarity(name_embedding, ref_embedding)
        if similarity >= 0.35:
            return True

    return False
```

### Threshold Selection

The 0.35 similarity threshold was chosen empirically:

| Threshold | Validated Names | False Negatives | False Positives |
|-----------|-----------------|-----------------|-----------------|
| 0.50 | 89,234 | High (valid compounds rejected) | Low |
| 0.40 | 121,456 | Moderate | Low |
| **0.35** | **137,878** | Low | Low |
| 0.30 | 152,891 | Low | Moderate |
| 0.25 | 168,234 | Low | High |

### Results

| Metric | Value |
|--------|-------|
| Input names | 175,844 |
| Validated names | 137,878 |
| Validation rate | 78.4% |
| Rejected as non-color | 37,966 |

### Examples

**Validated (similarity ≥ 0.35)**:
- "dusty rose" → 0.82 (similar to "rose")
- "ocean blue" → 0.89 (similar to "blue")
- "brownish purple" → 0.71 (similar to "brown", "purple")

**Rejected (similarity < 0.35)**:
- "asdfgh" → 0.08
- "i hate this" → 0.12
- "fedex purple" → 0.29 (borderline, brand name)

---

## Stage 2: Color Wheel Consistency (Annotation Only)

### Goal

Annotate each validated color with its consistency against theoretical color
wheel positions.

### Important Design Decision

This stage does **not filter** colors. Consistency flags are annotations only.

**Rationale**: Screen colors may systematically deviate from color wheel
positions due to monitor characteristics, gamma curves, and perception
differences. Filtering would remove the data needed to detect these biases.

### Computation

```python
def compute_color_wheel_consistency(name, rgb):
    """
    Check if the name's semantic hue matches the RGB hue.
    Returns consistency flag and hue deviation.
    """
    # Extract semantic hue expectation from name
    expected_hue = extract_expected_hue(name)  # e.g., "blue" → 240°

    # Compute actual RGB hue
    actual_hue = rgb_to_hue(rgb)  # e.g., (0, 0, 255) → 240°

    # Compute deviation
    deviation = circular_difference(expected_hue, actual_hue)

    # Annotate (but do not filter)
    return {
        'consistent': deviation < 30,
        'deviation': deviation,
        'expected_hue': expected_hue,
        'actual_hue': actual_hue
    }
```

### Results

All 137,878 validated colors proceed to Stage 3, annotated with consistency flags.

---

## Stage 3: RGB to Munsell Conversion

### Goal

Convert all validated XKCD RGB colors to Munsell color space coordinates.

### Approach: Mathematical Conversion (ASTM D1535)

We use the MunsellSpace Rust library, which implements the ASTM D1535 standard
for RGB-to-Munsell conversion.

### Conversion Pipeline

```
sRGB [R,G,B]
    ↓ Gamma correction (ITU-R BT.709)
Linear RGB
    ↓ Color matrix (sRGB D65)
CIE XYZ
    ↓ Chromaticity conversion
CIE xyY
    ↓ Munsell mapping (ASTM D1535)
Munsell [H V/C]
```

### Implementation

**Rust Converter** (`examples/simple_rgb_to_munsell.rs`):
```rust
fn main() {
    let converter = MunsellConverter::new();

    // Read RGB, output Munsell
    for line in stdin.lines() {
        let rgb = parse_rgb(&line);
        match converter.rgb_to_munsell(rgb) {
            Ok(munsell) => println!("{}", munsell.to_notation()),
            Err(_) => println!("FAILED"),
        }
    }
}
```

**Python Orchestrator** (`rgb_to_munsell_conversion.py`):
```python
def convert_batch(colors):
    """Convert batch of RGB colors to Munsell via Rust subprocess."""
    process = subprocess.Popen(
        ['cargo', 'run', '--release', '--example', 'simple_rgb_to_munsell'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    # Write RGB values, read Munsell notations
    for name, r, g, b in colors:
        process.stdin.write(f"{name},{r},{g},{b}\n")

    return parse_output(process.stdout)
```

### RGB Averaging

Each XKCD name has multiple associated RGB values (from different survey
responses). We compute the mean:

```python
def average_rgb(rgb_list):
    """Compute mean RGB from list of hex values."""
    r_sum = g_sum = b_sum = 0
    for hex_color in rgb_list:
        r, g, b = hex_to_rgb(hex_color)
        r_sum += r
        g_sum += g
        b_sum += b

    n = len(rgb_list)
    return (r_sum // n, g_sum // n, b_sum // n)
```

### Results

| Metric | Value |
|--------|-------|
| Input validated names | 137,878 |
| Successfully converted | 133,359 |
| Conversion rate | 96.7% |
| Failed (out of gamut) | 4,519 |

### Output Format

```json
{
  "name": "dusty rose",
  "rgb": [201, 161, 161],
  "munsell_notation": "2.5R 7/4",
  "hue_letter": "R",
  "hue_num": 2.5,
  "value": 7.0,
  "chroma": 4.0,
  "x": 3.46,
  "y": 1.41
}
```

---

## Stage 4: Centore Comparison & Bias Detection

### Goal

Compare XKCD-derived Munsell positions with Centore physical reference centroids
to detect systematic biases.

### Matching Algorithm

```python
def match_to_centore(xkcd_name, centore_categories):
    """Find matching Centore category for XKCD name."""
    name_lower = xkcd_name.lower()

    for category in centore_categories:
        cat_lower = category.lower()
        # Match if either contains the other
        if cat_lower in name_lower or name_lower in cat_lower:
            return category

    return None
```

### Centroid Calculation

For each Centore category, compute the centroid of its polygon vertices:

```python
def compute_centroid(vertices):
    """Compute Munsell centroid using circular mean for hue."""
    # Circular mean for hue (hue is angular)
    hue_rads = [v['hue'] * math.pi / 180 for v in vertices]
    mean_sin = sum(math.sin(h) for h in hue_rads) / len(vertices)
    mean_cos = sum(math.cos(h) for h in hue_rads) / len(vertices)
    mean_hue = math.atan2(mean_sin, mean_cos) * 180 / math.pi

    # Arithmetic mean for value and chroma
    mean_value = sum(v['value'] for v in vertices) / len(vertices)
    mean_chroma = sum(v['chroma'] for v in vertices) / len(vertices)

    return {
        'hue': mean_hue % 360,
        'value': mean_value,
        'chroma': mean_chroma
    }
```

### Bias Computation

For each matched color, compute the deviation from Centore centroid:

```python
def compute_bias(xkcd_munsell, centore_centroid):
    """Compute bias in each Munsell dimension."""
    # Hue bias (circular difference)
    delta_hue = circular_difference(
        xkcd_munsell['hue'],
        centore_centroid['hue']
    )

    # Value bias
    delta_value = xkcd_munsell['value'] - centore_centroid['value']

    # Chroma bias
    delta_chroma = xkcd_munsell['chroma'] - centore_centroid['chroma']

    return {
        'delta_hue': delta_hue,
        'delta_value': delta_value,
        'delta_chroma': delta_chroma
    }
```

### Hue Scale Conversion (Critical)

**Important**: The Rust converter outputs hue in 0-40 Munsell scale, not 0-360
degrees. Conversion is required:

```python
# Rust outputs hue_num in 0-40 Munsell scale
# Convert to degrees: 40 → 360
hue_degrees = hue_num * 9.0
```

### Aggregation by Category

For each Centore category, aggregate all matched XKCD colors:

```python
def aggregate_category(matches):
    """Compute mean bias for a Centore category."""
    # Circular mean for hue bias
    hue_biases = [m['delta_hue'] for m in matches]
    mean_hue_bias = circular_mean(hue_biases)

    # Arithmetic mean for value/chroma bias
    mean_value_bias = sum(m['delta_value'] for m in matches) / len(matches)
    mean_chroma_bias = sum(m['delta_chroma'] for m in matches) / len(matches)

    return {
        'category': matches[0]['category'],
        'n_matches': len(matches),
        'mean_hue_bias': mean_hue_bias,
        'mean_value_bias': mean_value_bias,
        'mean_chroma_bias': mean_chroma_bias
    }
```

### Results

| Metric | Value |
|--------|-------|
| Colors matched to categories | 101,894 |
| Categories analyzed | 30 |
| Mean value bias | +0.81 |
| Mean chroma bias | +3.82 |
| Mean hue bias | -2.71° |
| Hue bias std dev | ±35.94° |

---

## Pipeline Execution

### Complete Workflow

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

### Data Flow

```
xkcd_color_survey_data.json (175,844 names)
    ↓ Stage 1
validated_color_names.json (137,878 names)
    ↓ Stage 2 (annotation only)
validated_color_names.json (with consistency flags)
    ↓ Stage 3
munsell_conversions.json (133,359 colors)
    ↓ Stage 4
centore_comparison_results.json (101,894 matched, 30 categories)
```

---

## Statistical Methods

### Circular Statistics for Hue

Hue is an angular quantity (0-360°). Standard arithmetic mean fails at wrap-around:

```
Wrong: mean(355°, 5°) = 180°
Right: mean(355°, 5°) = 0° (using circular mean)
```

**Circular Mean Implementation**:

```python
def circular_mean(angles_degrees):
    """Compute circular mean of angles in degrees."""
    angles_rad = [a * math.pi / 180 for a in angles_degrees]
    mean_sin = sum(math.sin(a) for a in angles_rad) / len(angles_rad)
    mean_cos = sum(math.cos(a) for a in angles_rad) / len(angles_rad)
    mean_rad = math.atan2(mean_sin, mean_cos)
    return mean_rad * 180 / math.pi
```

### Confidence Intervals

For categories with sufficient sample size, we compute 95% confidence intervals:

```python
def confidence_interval(values, confidence=0.95):
    """Compute confidence interval for mean."""
    n = len(values)
    mean = sum(values) / n
    std = (sum((v - mean)**2 for v in values) / (n - 1)) ** 0.5
    margin = 1.96 * std / (n ** 0.5)  # z=1.96 for 95% CI
    return (mean - margin, mean + margin)
```

### Distance Metric

Overall color distance uses Euclidean distance in Cartesian Munsell space:

```python
def munsell_distance(color1, color2):
    """Compute distance in Munsell space."""
    # Convert to Cartesian (x, y from hue/chroma)
    x1 = color1['chroma'] * math.cos(color1['hue'] * math.pi / 180)
    y1 = color1['chroma'] * math.sin(color1['hue'] * math.pi / 180)
    x2 = color2['chroma'] * math.cos(color2['hue'] * math.pi / 180)
    y2 = color2['chroma'] * math.sin(color2['hue'] * math.pi / 180)

    # Euclidean distance including value
    return math.sqrt(
        (x1 - x2)**2 +
        (y1 - y2)**2 +
        (color1['value'] - color2['value'])**2
    )
```

