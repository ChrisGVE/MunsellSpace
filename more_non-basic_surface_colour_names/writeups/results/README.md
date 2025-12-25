# Results Directory Index

This directory contains all experimental results, analysis outputs, and documentation for the color research project.

**Result files are now stored in**: `writeups/results/data/`

**Scripts to regenerate results**: `scripts/src/semantic/`

---

## Experimental Results (JSON)

### Phase 2: Semantic Validation

**File**: `validated_color_names.json`
- **Size**: ~25 MB (145,042 validated names with metadata)
- **Content**: XKCD color names that passed SBERT semantic validation
- **Format**: JSON array of objects
- **Fields**: name, hex_values, count, validation_score, closest_reference
- **Creation**: `full_scale_validation.py`

**File**: `full_scale_validation_summary.json`
- **Size**: ~9 KB
- **Content**: Summary statistics for semantic validation
- **Metrics**:
  - Total names processed: 175,844
  - Validated names: 137,878 (78.4%)
  - Rejected names: 37,966 (21.6%)
  - Threshold: 0.35 cosine similarity
- **Creation**: `full_scale_validation.py`

**File**: `color_wheel_consistency_results.json`
- **Size**: ~24 KB
- **Content**: Color wheel consistency annotations (not filtering)
- **Metrics**:
  - Consistent (deviation < 30°): 119,342 (86.6%)
  - Inconsistent (deviation ≥ 30°): 18,536 (13.4%)
  - Per-color deviation scores
- **Creation**: `color_wheel_consistency.py`

### Phase 3: RGB to Munsell Conversion

**File**: `munsell_conversions.json`
- **Size**: ~48 MB (133,359 converted colors)
- **Content**: Complete RGB to Munsell conversion results
- **Format**: JSON array of objects
- **Fields**: name, rgb, munsell_notation, hue_num, value, chroma, x, y
- **Creation**: `rgb_to_munsell_conversion.py` (Rust + Python)

**File**: `munsell_conversion_summary.json`
- **Size**: ~551 bytes
- **Content**: Conversion statistics
- **Metrics**:
  - Input colors: 137,878
  - Successfully converted: 133,359 (96.7%)
  - Failed (out of gamut): 4,519 (3.3%)
- **Creation**: `rgb_to_munsell_conversion.py`

**File**: `xkcd_coordinates_cache.json`
- **Size**: ~21 MB
- **Content**: Cached Munsell coordinates for fast lookup
- **Purpose**: Speed up repeated analyses without re-converting
- **Creation**: `common.py` (lazy initialization)

### Phase 4: Calibration Analysis

**File**: `centore_comparison_results.json`
- **Size**: ~27 KB
- **Content**: Per-category bias analysis comparing XKCD to Centore
- **Structure**:
  - 30 categories analyzed
  - Per-category: n_matches, mean_hue_bias, mean_value_bias, mean_chroma_bias
  - Global statistics: overall means and standard deviations
- **Key findings**:
  - Value bias: +0.81 (screen appears lighter)
  - Chroma bias: +3.82 (screen appears more saturated)
  - Hue bias: -2.71° ± 35.94° (non-uniform)
- **Creation**: `centore_comparison.py`

**File**: `hue_bias_analysis.json`
- **Size**: ~5 KB
- **Content**: Detailed hue bias breakdown by category
- **Fields**: category, n, mean_hue_bias, std_hue_bias, category_hue_position
- **Notable categories**:
  - teal: -41.1° (shift toward blue)
  - aqua: -38.7° (shift toward blue)
  - beige: +33.3° (shift toward yellow)
  - tan: +29.8° (shift toward yellow)
- **Creation**: `polyhedra_bias_analysis.py`

**File**: `distribution_comparison_results.json`
- **Size**: ~51 KB
- **Content**: Distribution comparison between XKCD and Centore polyhedra
- **Metrics**: Centroid distance, volume ratio, vertex count comparison
- **Creation**: `distribution_comparison_methods.py`

**File**: `polyhedra_bias_results.json`
- **Size**: ~26 KB (if exists)
- **Content**: Polyhedra-level bias analysis
- **Creation**: `polyhedra_bias_analysis.py`

### Phase 6: Convex Hull Construction

**File**: `convex_hull_results.json`
- **Size**: ~11 KB
- **Content**: Polyhedra constructed for 30 Centore categories
- **Structure**:
  - Per-category: vertices (Cartesian coordinates), faces, centroid
  - Outlier removal statistics (outer vs inner hull)
- **Method**: Centore inner convex hull (single-layer vertex removal)
- **Creation**: `build_convex_hulls.py`

### Phase 7: Bias Correction Model

**File**: `fourier_correction_model.json`
- **Size**: ~3.4 KB
- **Content**: Fourier 4 harmonic model coefficients
- **Structure**:
  ```json
  {
    "model_type": "fourier_4_harmonics",
    "coefficients": {
      "a0": -2.931,
      "a1": 6.501, "b1": 15.949,
      "a2": -7.675, "b2": 6.927,
      "a3": 9.248, "b3": -17.937,
      "a4": -10.873, "b4": 7.078
    },
    "performance": {
      "train_mae": 5.06,
      "cv_mae": 7.41,
      "weighted_mae": 7.16,
      "max_error": 16.2
    }
  }
  ```
- **Creation**: `fit_fourier_correction.py`

**File**: `extended_model_analysis_results.json`
- **Size**: ~863 bytes
- **Content**: Hypothesis testing and model selection validation
- **Tests included**:
  - Mean bias = 0 (p=0.50, fail to reject)
  - Bias is uniform (p<0.001, reject - confirms non-uniformity)
  - Fourier 4 vs Linear (p<0.001, reject - 93.9% SSE reduction)
  - Fourier 4 vs Fourier 3 (p=0.10, marginal)
  - Model vs noise (p<0.001, reject - captures real signal)
  - Paired improvement (p<0.001, reject - 26/29 improved)
- **Creation**: `extended_model_analysis.py`

---

## Visualization Outputs (PNG)

### Phase 4: Bias Analysis

**File**: `hue_bias_analysis.png`
- **Dimensions**: Typically 1200×800 pixels
- **Content**: Scatter plot showing hue bias by category vs. category hue position
- **X-axis**: Category hue position (0-360°)
- **Y-axis**: Hue bias (degrees, negative = cooler, positive = warmer)
- **Key features**:
  - Points sized by sample count
  - Color-coded by bias direction
  - Shows non-uniform bias pattern (cool colors shift blue, warm shift yellow)
- **Creation**: `visualize_hue_bias.py`

### Phase 7: Correction Model

**File**: `correction_model_visualization.png`
- **Dimensions**: Typically 1200×800 pixels
- **Content**: Fourier 4 model curve with actual bias data points
- **X-axis**: Hue position (0-360°)
- **Y-axis**: Hue correction (degrees)
- **Curves shown**:
  - Fourier 4 model (solid line)
  - Actual category biases (scatter points)
  - ±1 standard deviation envelope (shaded region)
- **Creation**: `visualize_correction_model.py`

---

## Experiment Results (Legacy/Exploratory)

These files document experiments that were explored but not used in final pipeline:

**File**: `exp1_sbert_full_results.json` (21 MB)
- **Experiment**: Full-scale SBERT semantic validation
- **Outcome**: Selected approach (Phase 2.1)

**File**: `exp2_bert_full_results.json` (8 KB)
- **Experiment**: BERT tokenization for spelling variants
- **Outcome**: Rejected (failed on spelling variants)

**File**: `exp3_autoencoder_full_results.json` (10 KB)
- **Experiment**: Character-level autoencoder for typo detection
- **Outcome**: Rejected (failed on non-ASCII characters)

**File**: `exp4_hybrid_results.json` (27 KB)
- **Experiment**: Hybrid SBERT + autoencoder approach
- **Outcome**: Rejected (SBERT alone sufficient)

**File**: `exp5_preprocessing_results.json` (595 bytes)
- **Experiment**: Preprocessing pipeline statistics
- **Outcome**: Informational only

---

## Model Training Artifacts

**File**: `exp3_autoencoder_model.pt`
- **Size**: Variable (PyTorch model weights)
- **Content**: Trained autoencoder model (not used in final pipeline)
- **Format**: PyTorch state_dict
- **Note**: Exploratory only

---

## Result File Locations

### Primary Location
All result files are stored in:
```
more_non-basic_surface_colour_names/writeups/results/data/
```

### Scripts Location
Scripts that generate these results are in:
```
more_non-basic_surface_colour_names/scripts/src/semantic/
```

### Organized by Phase

**Phase 2 outputs**:
- `validated_color_names.json`
- `full_scale_validation_summary.json`
- `color_wheel_consistency_results.json`

**Phase 3 outputs**:
- `munsell_conversions.json`
- `munsell_conversion_summary.json`
- `xkcd_coordinates_cache.json`

**Phase 4 outputs**:
- `centore_comparison_results.json`
- `hue_bias_analysis.json`
- `distribution_comparison_results.json`
- `hue_bias_analysis.png`

**Phase 6 outputs**:
- `convex_hull_results.json`

**Phase 7 outputs**:
- `fourier_correction_model.json`
- `extended_model_analysis_results.json`
- `correction_model_visualization.png`

---

## Accessing Results

### Command-Line

**View summary statistics**:
```bash
cd more_non-basic_surface_colour_names/writeups/results/data

# Phase 2 summary
jq '.summary' full_scale_validation_summary.json

# Phase 3 summary
jq '.' munsell_conversion_summary.json

# Phase 4 global statistics
jq '.global_statistics' centore_comparison_results.json

# Phase 7 model performance
jq '.performance' fourier_correction_model.json
```

**Count entries**:
```bash
# Validated names
jq 'length' validated_color_names.json

# Converted colors
jq 'length' munsell_conversions.json

# Categories analyzed
jq '.categories | length' centore_comparison_results.json
```

### Python

**Load results**:
```python
import json

# Load validated names
with open('validated_color_names.json') as f:
    validated = json.load(f)

# Load bias analysis
with open('centore_comparison_results.json') as f:
    bias_analysis = json.load(f)

# Load correction model
with open('fourier_correction_model.json') as f:
    model = json.load(f)

print(f"Validated names: {len(validated)}")
print(f"Global value bias: {bias_analysis['global_statistics']['mean_value_bias']}")
print(f"Model CV MAE: {model['performance']['cv_mae']}°")
```

---

## Result File Schemas

### validated_color_names.json
```json
[
  {
    "name": "dusty rose",
    "hex_values": ["#c9a1a1", "#c8a2a0"],
    "count": 127,
    "validation_score": 0.82,
    "closest_reference": "rose",
    "consistent": true,
    "hue_deviation": 3.2
  }
]
```

### munsell_conversions.json
```json
[
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
]
```

### centore_comparison_results.json
```json
{
  "categories": [
    {
      "category": "beige",
      "n_matches": 755,
      "mean_hue_bias": 33.3,
      "mean_value_bias": 0.92,
      "mean_chroma_bias": 4.15,
      "centore_centroid": {"hue": 63.9, "value": 7.0, "chroma": 3.95}
    }
  ],
  "global_statistics": {
    "mean_value_bias": 0.81,
    "mean_chroma_bias": 3.82,
    "mean_hue_bias": -2.71,
    "hue_bias_std": 35.94
  }
}
```

### fourier_correction_model.json
```json
{
  "model_type": "fourier_4_harmonics",
  "coefficients": {
    "a0": -2.931,
    "a1": 6.501,
    "b1": 15.949,
    "a2": -7.675,
    "b2": 6.927,
    "a3": 9.248,
    "b3": -17.937,
    "a4": -10.873,
    "b4": 7.078
  },
  "performance": {
    "train_mae": 5.06,
    "cv_mae": 7.41,
    "weighted_mae": 7.16,
    "cv_ratio": 1.47,
    "max_error": 16.2
  },
  "metadata": {
    "n_categories": 29,
    "parameters": 9,
    "residual_dof": 20,
    "bootstrap_ci_95": [4.7, 9.6]
  }
}
```

---

## Reproducing Results

### Complete Pipeline Execution

```bash
cd more_non-basic_surface_colour_names/scripts

# Phase 2: Semantic validation (produces validated_color_names.json)
uv run python src/semantic/full_scale_validation.py

# Phase 2: Color wheel consistency (annotates validated_color_names.json)
uv run python src/semantic/color_wheel_consistency.py

# Phase 3: RGB to Munsell (produces munsell_conversions.json)
uv run python src/semantic/rgb_to_munsell_conversion.py

# Phase 4: Calibration analysis (produces centore_comparison_results.json)
uv run python src/semantic/centore_comparison.py
uv run python src/semantic/polyhedra_bias_analysis.py

# Phase 6: Convex hulls (produces convex_hull_results.json)
uv run python src/semantic/build_convex_hulls.py

# Phase 7: Correction model (produces fourier_correction_model.json)
uv run python src/semantic/fit_fourier_correction.py
uv run python src/semantic/extended_model_analysis.py

# Visualizations
uv run python src/semantic/visualize_hue_bias.py
uv run python src/semantic/visualize_correction_model.py
```

**Total execution time**: ~15 minutes (with caching)

**Prerequisites**:
- sentence-transformers (SBERT model)
- numpy, scipy (numerical/spatial operations)
- matplotlib (visualizations)
- Rust toolchain (Munsell converter)

---

## Result File Statistics

| File | Size | Format | Phase | Records |
|------|------|--------|-------|---------|
| validated_color_names.json | 25 MB | JSON | 2 | 137,878 |
| munsell_conversions.json | 48 MB | JSON | 3 | 133,359 |
| centore_comparison_results.json | 27 KB | JSON | 4 | 30 categories |
| convex_hull_results.json | 11 KB | JSON | 6 | 30 polyhedra |
| fourier_correction_model.json | 3.4 KB | JSON | 7 | 1 model |
| hue_bias_analysis.png | ~200 KB | PNG | 4 | Visualization |
| correction_model_visualization.png | ~180 KB | PNG | 7 | Visualization |

**Total result size**: ~73 MB (excluding exploratory experiments)

---

## Archival and Version Control

**Version control status**:
- Result files are **not** committed to git (too large, regenerable)
- Excluded via `.gitignore`
- Scripts to regenerate results **are** version-controlled

**Archival location** (if backing up):
- Cloud: Store in project backup
- Local: Keep in `more_non-basic_surface_colour_names/writeups/results/data/`

**Recommended backup**:
```bash
# Create tarball of all results
cd more_non-basic_surface_colour_names/writeups/results/data
tar -czf color_research_results_$(date +%Y%m%d).tar.gz \
  validated_color_names.json \
  munsell_conversions.json \
  centore_comparison_results.json \
  convex_hull_results.json \
  fourier_correction_model.json \
  *.png
```

---

**Document version**: 2.0
**Last updated**: 2025-12-25
**Maintained by**: MunsellSpace Color Research Project
