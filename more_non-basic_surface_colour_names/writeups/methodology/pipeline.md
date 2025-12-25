# Data Pipeline: Screen Colors to Physical Color Space

## Executive Summary

This document describes the end-to-end data pipeline for mapping crowdsourced screen color names (XKCD survey) to physical Munsell color space, detecting systematic biases, and constructing corrected semantic color overlays.

**Key Insight**: Screen color perception differs systematically from physical color measurement. The pipeline quantifies these biases and develops a correction model for accurate semantic overlays.

## Pipeline Architecture

```
Phase 1: Data Collection
    ↓
Phase 2: Entity Matching & Normalization
    ↓
Phase 3: Coordinate Analysis (Pre-Consolidation)
    ↓
Phase 4: Calibration Analysis (Centore Comparison)
    ↓
Phase 5: Consolidation Strategy
    ↓
Phase 6: Convex Hull Construction
    ↓
Phase 7: Bias Correction (Fourier Model)
```

---

## Phase 1: Data Collection

### 1.1 XKCD Color Survey Data

**Source**: XKCD crowdsourced color naming survey (2010)
- **Total responses**: 3.4 million color naming responses
- **Unique names**: 175,844 distinct color names
- **Format**: RGB hex values with user-provided names
- **URL**: https://blog.xkcd.com/2010/05/03/color-survey-results/

**Data structure**:
```json
{
  "color_name": "dusty rose",
  "hex_values": ["#c9a1a1", "#c8a2a0", "#caa0a1"],
  "count": 127
}
```

**Characteristics**:
- Screen colors (RGB, self-luminous)
- Uncalibrated monitors
- Freeform naming (crowd-sourced)
- High sample counts for common colors

### 1.2 Centore Reference Data

**Source**: Color Association of the United States (CAUS) fabric samples
- **Total samples**: 9,261 fabric samples
- **Measurement**: Spectrophotometer-measured Munsell coordinates
- **Categories**: 30 color categories analyzed by Centore (2020)
- **Reference**: JAIC Vol. 25, pp. 24-54

**Data structure**:
```json
{
  "category": "beige",
  "polyhedron_vertices": [
    {"hue": 62.5, "value": 7.2, "chroma": 4.1},
    {"hue": 65.3, "value": 6.8, "chroma": 3.8}
  ],
  "centroid": {"hue": 63.9, "value": 7.0, "chroma": 3.95}
}
```

**Characteristics**:
- Physical colors (reflective, measured under D65)
- Controlled illumination
- Expert-assigned names
- Smaller sample counts per category

### 1.3 Additional Vocabulary Sources

**Purpose**: Expand semantic matching vocabulary

Sources:
- **Meodai Color Names**: 33,000+ color names from multiple sources
- **ColorHexa**: Web color database
- **Color-name.com**: User-contributed color names
- **Wikipedia**: List of colors by name

**Usage**: Build comprehensive reference vocabulary for semantic validation

---

## Phase 2: Entity Matching & Normalization

### 2.1 Semantic Validation

**Goal**: Filter 175,844 XKCD names to retain only valid color descriptions

**Method**: SBERT (Sentence-BERT) semantic similarity

**Model**: `all-MiniLM-L6-v2`

**Reference vocabulary**: 33,000+ known color terms

**Algorithm**:
```python
def validate_color_name(name, reference_vocabulary):
    """Return True if name is semantically similar to any reference color."""
    name_embedding = sbert_model.encode(name)

    for ref_color in reference_vocabulary:
        ref_embedding = sbert_model.encode(ref_color)
        similarity = cosine_similarity(name_embedding, ref_embedding)

        if similarity >= 0.35:
            return True

    return False
```

**Threshold**: 0.35 cosine similarity
- Chosen empirically to balance precision and recall
- Lower threshold: more false positives (non-colors)
- Higher threshold: more false negatives (valid compounds rejected)

**Results**:
| Metric | Value |
|--------|-------|
| Input names | 175,844 |
| Validated names | 137,878 |
| Validation rate | 78.4% |
| Rejected | 37,966 |

**Examples**:

Validated (similarity ≥ 0.35):
- "dusty rose" → 0.82
- "ocean blue" → 0.89
- "brownish purple" → 0.71

Rejected (similarity < 0.35):
- "asdfgh" → 0.08
- "i hate this" → 0.12
- "fedex purple" → 0.29

**Output file**: `validated_color_names.json`

### 2.2 Spelling Variant Detection

**Challenge**: Multiple spellings for same color concept
- "gray" vs "grey"
- "lightblue" vs "light blue"
- "purpley" vs "purplish"

**Method**: Levenshtein distance + manual curation

**Examples normalized**:
- "grey", "gray" → "gray"
- "light blue", "lightblue" → "light blue"
- "purpley", "purplish", "purple-ish" → "purplish"

### 2.3 Compound Name Handling

**Compound patterns**:
1. Modifier + Base: "dark blue", "light green"
2. Dual descriptor: "bluish green", "reddish brown"
3. Object reference: "sky blue", "forest green"

**Normalization**:
- Preserve semantic meaning
- Standardize whitespace
- Lowercase conversion

### 2.4 Typo Detection

**Common typos**:
- Character transposition: "pruple" → "purple"
- Missing characters: "geen" → "green"
- Extra characters: "bluue" → "blue"

**Detection**: Edit distance ≤ 2 from known color terms

---

## Phase 3: Coordinate Analysis (Pre-Consolidation)

### 3.1 RGB Averaging

**Problem**: Each XKCD name has multiple RGB values from different responses

**Solution**: Compute mean RGB

```python
def average_rgb(hex_values):
    """Compute mean RGB from list of hex values."""
    r_sum = g_sum = b_sum = 0

    for hex_color in hex_values:
        r, g, b = hex_to_rgb(hex_color)
        r_sum += r
        g_sum += g
        b_sum += b

    n = len(hex_values)
    return (r_sum // n, g_sum // n, b_sum // n)
```

**Example**:
- "dusty rose": ["#c9a1a1", "#c8a2a0", "#caa0a1"]
- Average RGB: (201, 161, 161)

### 3.2 Color Wheel Consistency Check

**Goal**: Annotate colors with consistency flags (not filter)

**Method**: Compare semantic hue expectation vs. actual RGB hue

```python
def compute_color_wheel_consistency(name, rgb):
    """Check if name's semantic hue matches RGB hue."""
    expected_hue = extract_expected_hue(name)  # "blue" → 240°
    actual_hue = rgb_to_hue(rgb)
    deviation = circular_difference(expected_hue, actual_hue)

    return {
        'consistent': deviation < 30,
        'deviation': deviation,
        'expected_hue': expected_hue,
        'actual_hue': actual_hue
    }
```

**Important**: This is annotation only. All colors proceed to next phase.

**Rationale**: Inconsistent colors may reveal systematic biases between screen and physical perception. Filtering would remove the data needed for bias detection.

**Results**:
| Category | Count | Percentage |
|----------|-------|------------|
| Consistent (dev < 30°) | 119,342 | 86.6% |
| Inconsistent (dev ≥ 30°) | 18,536 | 13.4% |

**Output file**: `color_wheel_consistency_results.json`

### 3.3 RGB to Munsell Conversion

**Goal**: Convert all validated XKCD colors to Munsell space

**Method**: ASTM D1535 compliant mathematical conversion via MunsellSpace library

**Conversion pipeline**:
```
sRGB [R, G, B]
    ↓ Gamma correction (ITU-R BT.709)
Linear RGB
    ↓ Color matrix (sRGB D65)
CIE XYZ
    ↓ Chromaticity conversion
CIE xyY
    ↓ Munsell mapping (ASTM D1535)
Munsell [Hue, Value, Chroma]
```

**Implementation**: Rust library with Python orchestration

**Rust converter** (`examples/simple_rgb_to_munsell.rs`):
```rust
fn main() {
    let converter = MunsellConverter::new();

    for line in stdin.lines() {
        let rgb = parse_rgb(&line);
        match converter.rgb_to_munsell(rgb) {
            Ok(munsell) => println!("{}", munsell.to_notation()),
            Err(_) => println!("FAILED"),
        }
    }
}
```

**Hue scale conversion**: Rust outputs hue in 0-40 Munsell scale
```python
# Convert to degrees: 40 → 360
hue_degrees = hue_num * 9.0
```

**Results**:
| Metric | Value |
|--------|-------|
| Input colors | 137,878 |
| Successfully converted | 133,359 |
| Conversion rate | 96.7% |
| Failed (out of gamut) | 4,519 |

**Output file**: `munsell_conversions.json`

---

## Phase 4: Calibration Analysis (Centore Comparison)

### 4.1 Category Matching

**Goal**: Match XKCD names to Centore's 30 reference categories

**Method**: Substring matching (bidirectional)

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

**Example matches**:
- "dusty rose" → "rose"
- "ocean blue" → "blue"
- "light teal" → "teal"

**Results**:
| Metric | Value |
|--------|-------|
| XKCD colors processed | 133,359 |
| Matched to categories | 101,894 |
| Match rate | 76.4% |
| Unmatched | 31,465 |

### 4.2 Centore Centroid Calculation

**Goal**: Compute reference centroid for each Centore category

**Method**: Circular mean for hue, arithmetic mean for value/chroma

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

### 4.3 Bias Detection

**Goal**: Quantify systematic differences between XKCD and Centore

**Method**: Compute per-color bias in each Munsell dimension

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

### 4.4 Aggregate Statistics

**Goal**: Identify universal vs. category-specific biases

**Method**: Aggregate by category, compute global statistics

**Results**:

**Universal biases** (across all categories):
| Dimension | Mean Bias | Std Dev | Interpretation |
|-----------|-----------|---------|----------------|
| Value | +0.81 | ±0.92 | Screen colors appear lighter |
| Chroma | +3.82 | ±2.14 | Screen colors appear more saturated |
| Hue | -2.71° | ±35.94° | Non-uniform (category-dependent) |

**Category-specific hue biases** (selected):
| Category | n | Hue Bias | Interpretation |
|----------|---|----------|----------------|
| teal | 1,642 | -41.1° | Shifts strongly toward blue |
| aqua | 987 | -38.7° | Shifts toward blue |
| beige | 755 | +33.3° | Shifts toward yellow |
| tan | 612 | +29.8° | Shifts toward yellow |
| green | 22,990 | -10.5° | Slight shift toward cyan |
| blue | 18,414 | -9.2° | Slight shift toward cyan |

**Key finding**: Hue bias is non-uniform and opposite for cool vs. warm colors.

**Output file**: `centore_comparison_results.json`

---

## Phase 5: Consolidation Strategy

### 5.1 Duplicate Detection

**Goal**: Identify multiple XKCD names referring to same color region

**Method**: Cluster colors with similar Munsell coordinates

**Clustering criteria**:
- ΔE (Munsell distance) < 2.0
- Same semantic category
- Overlapping name components

**Example duplicates**:
- "light blue", "lightblue", "pale blue" → Consolidate
- "forest green", "dark green" → Keep separate (different value)

### 5.2 Merging Strategy

**Decision tree**:
1. Exact semantic match + ΔE < 1.0 → Merge
2. Spelling variant + ΔE < 2.0 → Merge
3. Modifier difference + ΔE < 2.0 → Keep separate
4. ΔE ≥ 2.0 → Always keep separate

**Merge operation**:
```python
def merge_colors(color_list):
    """Merge duplicate colors, keeping highest sample count."""
    # Sort by sample count (descending)
    sorted_colors = sorted(color_list, key=lambda c: c['count'], reverse=True)

    # Keep primary name (highest count)
    primary = sorted_colors[0]

    # Combine samples
    total_count = sum(c['count'] for c in sorted_colors)

    # Recompute mean Munsell (weighted by count)
    weighted_hue = circular_weighted_mean([c['hue'] for c in sorted_colors],
                                          [c['count'] for c in sorted_colors])
    weighted_value = weighted_mean([c['value'] for c in sorted_colors],
                                   [c['count'] for c in sorted_colors])
    weighted_chroma = weighted_mean([c['chroma'] for c in sorted_colors],
                                    [c['count'] for c in sorted_colors])

    return {
        'name': primary['name'],
        'count': total_count,
        'hue': weighted_hue,
        'value': weighted_value,
        'chroma': weighted_chroma,
        'merged_from': [c['name'] for c in sorted_colors[1:]]
    }
```

---

## Phase 6: Convex Hull Construction

### 6.1 Centore Inner Hull Methodology

**Goal**: Build outlier-robust polyhedra for each color category

**Method**: Centore's inner convex hull algorithm (JAIC 2020)

**Rationale**: Single-layer vertex removal eliminates boundary outliers while preserving core distribution

**Algorithm**:

**Step 1**: Collect color samples for category
```python
samples = get_samples_for_category("beige")
```

**Step 2**: Convert to Cartesian coordinates
```python
def munsell_to_cartesian(hue_100, value, chroma):
    """Convert Munsell cylindrical to Cartesian."""
    hue_rad = hue_100 * math.pi / 50.0
    x = chroma * math.cos(hue_rad)
    y = chroma * math.sin(hue_rad)
    z = value
    return (x, y, z)

S = [munsell_to_cartesian(h, v, c) for h, v, c in samples]
```

**Step 3**: Compute outer convex hull
```python
from scipy.spatial import ConvexHull

H = ConvexHull(S)
V = S[H.vertices]  # Outer hull vertices
```

**Step 4**: Remove outer vertices (outlier removal)
```python
vertex_indices = set(H.vertices)
S_minus_V = [S[i] for i in range(len(S)) if i not in vertex_indices]
```

**Step 5**: Compute inner convex hull (final polyhedron)
```python
Gamma = ConvexHull(S_minus_V)
vertices = S_minus_V[Gamma.vertices]
faces = Gamma.simplices
```

**Step 6**: Compute centroid
```python
centroid = compute_filled_solid_centroid(vertices, faces)
```

### 6.2 Centroid Calculation

**Method**: Filled-solid centroid (Centore equations 6-8)

**Approximation** (for implementation):
```python
def compute_centroid_simple(vertices):
    """Simple centroid as mean of vertices."""
    return np.mean(vertices, axis=0)
```

**Note**: This differs from Centore's exact filled-solid centroid but provides reasonable approximation.

### 6.3 Degenerate Case Handling

**Cases**:
1. Fewer than 4 samples → Skip category
2. All samples coplanar → Use 2D hull
3. Inner hull has fewer than 4 points → Fall back to outer hull

**Output file**: `convex_hull_results.json`

---

## Phase 7: Bias Correction (Fourier Model)

### 7.1 Model Selection Rationale

**Goal**: Correct non-uniform hue bias while avoiding overfitting

**Challenge**: Cool colors shift ~40° toward blue; warm colors shift ~30° toward yellow. Opposite directions require non-linear model.

**Models evaluated**:
1. Global linear (1 parameter) - baseline
2. Piecewise linear (4/6/12 regions)
3. Fourier series (1-6 harmonics)
4. Spline interpolation
5. Gaussian process regression

**Selection criteria**:
- Leave-one-out cross-validation error
- Train-CV ratio < 1.5x (overfitting threshold)
- Physical interpretability
- Smooth interpolation

**Selected model**: Fourier 4 harmonics

**Rationale**:
- Lowest CV weighted MAE: 7.16°
- Train-CV ratio: 1.47x (below threshold)
- Physically interpretable harmonics
- Smooth interpolation (no discontinuities)

**Evidence against overfitting**:
- Fourier 5 increases CV error by 74% (classic overfitting)
- 20 residual degrees of freedom (29 samples - 9 parameters)
- Bootstrap 95% CI: [4.7°, 9.6°]

### 7.2 Fourier 4 Model

**Formula**:
```
hue_correction(θ) = a₀ + a₁cos(θ) + b₁sin(θ) + a₂cos(2θ) + b₂sin(2θ)
                       + a₃cos(3θ) + b₃sin(3θ) + a₄cos(4θ) + b₄sin(4θ)

where θ = hue in radians
```

**Fitted coefficients**:
```python
coefficients = {
    'a0': -2.931,
    'a1': +6.501,  'b1': +15.949,
    'a2': -7.675,  'b2': +6.927,
    'a3': +9.248,  'b3': -17.937,
    'a4': -10.873, 'b4': +7.078
}
```

**Physical interpretation**:
| Harmonic | Period | Physical Effect |
|----------|--------|-----------------|
| k=1 | 360° | Overall warm-cool asymmetry |
| k=2 | 180° | Opposite quadrant effects (teal vs beige) |
| k=3 | 120° | RGB primary spacing effects |
| k=4 | 90° | Quadrant boundary refinement |

### 7.3 Model Application

**Correction function**:
```python
def apply_hue_correction(hue_degrees, model):
    """Apply Fourier correction to observed hue."""
    theta = hue_degrees * math.pi / 180.0

    correction = model['a0']
    for k in range(1, 5):
        correction += model[f'a{k}'] * math.cos(k * theta)
        correction += model[f'b{k}'] * math.sin(k * theta)

    corrected_hue = (hue_degrees - correction) % 360
    return corrected_hue
```

**Expected performance**:
| Metric | Value |
|--------|-------|
| Mean Absolute Error | 5.1° (training), 7.4° (CV) |
| Weighted MAE | 7.2° |
| Maximum Error | ~16° (unusual categories) |

**Output file**: `fourier_correction_model.json`

### 7.4 Hypothesis Testing

**Tests conducted** (permutation methods, bootstrap resampling):

| Test | Null Hypothesis | p-value | Decision |
|------|-----------------|---------|----------|
| Mean bias = 0 | H₀: μ = 0 | 0.50 | Fail to reject (expected) |
| Bias is uniform | H₀: σ² = 0 | <0.001 | **Reject** (confirms non-uniformity) |
| Fourier 4 = Linear | H₀: SSE_F4 = SSE_linear | <0.001 | **Reject** (93.9% reduction) |
| Fourier 4 = Fourier 3 | H₀: SSE_F4 = SSE_F3 | 0.10 | Marginal (CV favors F4) |
| Model vs noise | H₀: MAE = random | <0.001 | **Reject** (captures real signal) |
| Paired improvement | H₀: no improvement | <0.001 | **Reject** (26/29 improved) |

**Interpretation**:
- Hue bias is non-uniform (justifies correction)
- Fourier 4 significantly outperforms linear baseline
- Model captures real signal, not noise
- Systematic improvement across categories

---

## Pipeline Outputs

### Summary of Key Files

| Phase | Output File | Description |
|-------|-------------|-------------|
| 2.1 | `validated_color_names.json` | 137,878 validated XKCD names |
| 2.2 | `color_wheel_consistency_results.json` | Consistency annotations |
| 3.3 | `munsell_conversions.json` | 133,359 RGB→Munsell conversions |
| 3.3 | `munsell_conversion_summary.json` | Conversion statistics |
| 4.4 | `centore_comparison_results.json` | 101,894 matched colors, bias stats |
| 4.4 | `hue_bias_analysis.json` | Per-category hue bias analysis |
| 6.3 | `convex_hull_results.json` | Polyhedra for 30 categories |
| 7.3 | `fourier_correction_model.json` | Fourier 4 model coefficients |
| 7.4 | `extended_model_analysis_results.json` | Hypothesis testing results |

### Visualization Outputs

| File | Description |
|------|-------------|
| `hue_bias_analysis.png` | Scatter plot: category hue bias vs. hue position |
| `correction_model_visualization.png` | Fourier model curve with data points |

---

## Pipeline Execution

### Complete Workflow

**Prerequisites**:
```bash
pip install sentence-transformers numpy scipy
cargo build --release
```

**Execution sequence**:
```bash
# Phase 2: Semantic validation
cd overlay-preprocessing/semantic-investigation
python full_scale_validation.py

# Phase 3: Coordinate analysis
python color_wheel_consistency.py
python rgb_to_munsell_conversion.py

# Phase 4: Calibration analysis
python centore_comparison.py
python polyhedra_bias_analysis.py

# Phase 6: Convex hull construction
python build_convex_hulls.py

# Phase 7: Bias correction
python fit_fourier_correction.py
python extended_model_analysis.py
python visualize_hue_bias.py
python visualize_correction_model.py
```

### Data Flow Diagram

```
xkcd_color_survey_data.json (175,844 names)
    ↓
validated_color_names.json (137,878 names, 78.4%)
    ↓
munsell_conversions.json (133,359 colors, 96.7%)
    ↓
centore_comparison_results.json (101,894 matched, 76.4%)
    ↓
convex_hull_results.json (30 polyhedra)
    ↓
fourier_correction_model.json (Fourier 4)
```

---

## Key Findings

### Universal Biases

1. **Value bias**: +0.81 (screen colors appear lighter)
2. **Chroma bias**: +3.82 (screen colors appear more saturated)

### Non-Uniform Hue Bias

**Cool colors** (teal, aqua): Shift ~40° toward blue (cooler)

**Warm colors** (beige, tan): Shift ~30° toward yellow (warmer)

**Implication**: Linear correction cannot fix opposite-direction biases

### Correction Model Performance

**Fourier 4 harmonics**:
- Reduces hue error from 11.2° (linear) to 7.2° (corrected)
- 35% improvement in weighted MAE
- Generalizes well (CV ratio 1.47x)

---

## Limitations

### Data Source Limitations

1. **Screen vs. physical colors**: Fundamental measurement difference
2. **Monitor calibration**: Uncalibrated, varied displays
3. **Illuminant differences**: Self-luminous vs. reflective D65
4. **Individual perception**: Color naming varies by person
5. **Metamerism**: Screen-matched colors may not match physically

### Methodological Limitations

1. **First-order approximation**: Assumes systematic biases are correctable
2. **Category matching**: Substring matching may miss nuanced relationships
3. **Sample size variation**: Some categories have few matches (n < 200)
4. **Convex hull approximation**: Simple centroid vs. filled-solid centroid
5. **Model generalization**: Fourier 4 validated on 29 categories only

### Future Improvements

1. **Perceptual color space**: Use CIELAB or CIEDE2000 for better uniformity
2. **Category-specific corrections**: Per-category non-linear models
3. **Uncertainty quantification**: Bootstrap confidence intervals
4. **Validation dataset**: Independent test set from different color study
5. **Multidimensional correction**: Joint hue-value-chroma modeling

---

## References

### Primary Sources

1. **Centore, P. (2020)** "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names" - JAIC Vol. 25, pp. 24-54
   - PDF: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf

2. **Munroe, R. (2010)** "XKCD Color Survey Results"
   - URL: https://blog.xkcd.com/2010/05/03/color-survey-results/

### Supporting References

3. **Lay, S.R. (2007)** "Convex Sets and Their Applications" - Dover Publications
   - Defines minimal generating set (convex hull vertices)

4. **ASTM D1535** "Standard Practice for Specifying Color by the Munsell System"
   - Munsell color space specification

5. **ITU-R BT.709** "Parameter values for the HDTV standards"
   - sRGB standard and gamma correction

### Computational Methods

6. **Reimers & Gurevych (2019)** "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
   - Semantic similarity computation

7. **Fisher, N.I. (1993)** "Statistical Analysis of Circular Data" - Cambridge University Press
   - Circular statistics for hue analysis

---

## Appendices

### Appendix A: Circular Statistics

**Circular mean**:
```python
def circular_mean(angles_degrees):
    angles_rad = [a * math.pi / 180 for a in angles_degrees]
    mean_sin = sum(math.sin(a) for a in angles_rad) / len(angles_rad)
    mean_cos = sum(math.cos(a) for a in angles_rad) / len(angles_rad)
    return math.atan2(mean_sin, mean_cos) * 180 / math.pi
```

**Circular difference**:
```python
def circular_difference(angle1, angle2):
    """Compute shortest angular difference (returns -180 to +180)."""
    diff = (angle1 - angle2) % 360
    if diff > 180:
        diff -= 360
    return diff
```

### Appendix B: Munsell Distance

**Euclidean distance in Cartesian Munsell space**:
```python
def munsell_distance(color1, color2):
    x1 = color1['chroma'] * math.cos(color1['hue'] * math.pi / 180)
    y1 = color1['chroma'] * math.sin(color1['hue'] * math.pi / 180)
    x2 = color2['chroma'] * math.cos(color2['hue'] * math.pi / 180)
    y2 = color2['chroma'] * math.sin(color2['hue'] * math.pi / 180)

    return math.sqrt(
        (x1 - x2)**2 +
        (y1 - y2)**2 +
        (color1['value'] - color2['value'])**2
    )
```

### Appendix C: Weighted Statistics

**Weighted mean**:
```python
def weighted_mean(values, weights):
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)
```

**Weighted circular mean**:
```python
def circular_weighted_mean(angles_degrees, weights):
    angles_rad = [a * math.pi / 180 for a in angles_degrees]
    mean_sin = sum(w * math.sin(a) for a, w in zip(angles_rad, weights)) / sum(weights)
    mean_cos = sum(w * math.cos(a) for a, w in zip(angles_rad, weights)) / sum(weights)
    return math.atan2(mean_sin, mean_cos) * 180 / math.pi
```

---

**Document version**: 1.0
**Last updated**: 2024-12-24
**Author**: MunsellSpace Color Research Project
