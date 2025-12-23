# Phase 6: Synthesis and Recommendations

## 1. Executive Summary

This investigation analyzed two color naming datasets to inform the consolidation
of Level 3 semantic overlays for the MunsellSpace library:

### Data Sources

| Source | Type | Samples | Unique Names | Quality |
|--------|------|---------|--------------|---------|
| Centore | Spectrophotometer | ~16,000 CAUS | ~7,584 | High (calibrated) |
| XKCD | Crowdsourced RGB | ~3.4M responses | ~176K | Variable (uncalibrated) |

### Key Findings

1. **Systematic Bias Detected**: XKCD colors appear ~19° bluer and ~1.6 chroma
   units more saturated than Centore spectrophotometer measurements.

2. **Name Standardization Needed**: ~132K canonical mappings identified from
   spelling variants, compound variations, and typos.

3. **High Noise in XKCD**: ~92% of high-variance names are non-color terms
   (names, spam, single letters). Filtering by frequency (n≥100) yields
   1,369 reliable color names.

4. **Consolidation Strategy**: Centroid-weighted mean performs best for
   combining duplicate samples, with mean distance 62.82 RGB units.

## 2. Recommendations for Implementation

### 2.1 Data Pipeline Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Centore Data  │     │   XKCD Data     │
│  (Ground Truth) │     │ (Crowdsourced)  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │ Name Cleaning   │
         │              │ - Lowercase     │
         │              │ - Trim          │
         │              │ - Normalize ws  │
         │              └────────┬────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │ Canonical Map   │
         │              │ - Spelling fix  │
         │              │ - Typo correct  │
         │              │ - US English    │
         │              └────────┬────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │ Filter by n≥100 │
         │              │ Remove noise    │
         │              └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ Munsell Coords  │     │ RGB → Munsell   │
│ (Direct)        │     │ (Converted)     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │ Apply Bias      │
         │              │ Correction      │
         │              │ (Optional)      │
         │              └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Source Priority │
            │ Centore > XKCD  │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Consolidate by  │
            │ Centroid Weight │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Level 3 Output  │
            │ color → Munsell │
            └─────────────────┘
```

### 2.2 Name Standardization Rules

**Priority Order:**
1. Apply canonical spelling mappings (grey→gray, colour→color)
2. Apply typo corrections (confidence ≥0.8)
3. Normalize compounds (light-blue → light blue)
4. Prefer US English spellings

**Implementation:**
```python
# Pseudo-code for name standardization
def standardize_name(raw_name: str) -> str:
    name = raw_name.lower().strip()
    name = re.sub(r'\s+', ' ', name)  # Normalize whitespace

    # Apply canonical mapping
    if name in canonical_map:
        name = canonical_map[name]

    # Apply typo correction if high confidence
    if name in typo_corrections:
        correction = typo_corrections[name]
        if correction['confidence'] >= 0.8:
            name = correction['canonical']

    return name
```

### 2.3 Coordinate Consolidation Strategy

**For XKCD-only colors:**
- Use centroid-weighted mean of RGB samples
- Convert to Munsell using MunsellSpace library
- Document sample count as confidence metric

**For Centore-only colors:**
- Use Centore Munsell coordinates directly
- No conversion needed (already calibrated)

**For colors in both datasets:**
- **Recommended**: Use Centore as ground truth
- Centore is spectrophotometer-calibrated; XKCD has systematic bias
- Optional: Weight Centore 3:1 vs XKCD if blending desired

### 2.4 Bias Correction (If Blending)

If choosing to blend XKCD with Centore, apply these corrections:

| Dimension | Correction | Notes |
|-----------|------------|-------|
| Hue | +19.3° | XKCD appears bluer |
| Value | None | No systematic bias |
| Chroma | -1.58 | XKCD appears more saturated |

**Caution**: These corrections are approximations based on 30 calibration
points. Full colorimetric transformation (D65→C illuminant) would be
more rigorous.

### 2.5 Quality Filtering Criteria

**Minimum requirements for inclusion:**
- Sample count n ≥ 100 (for XKCD)
- RGB standard deviation < 100 (filter noisy colors)
- Not in spam/noise list (names, single letters, etc.)

**Confidence scoring:**
```
confidence = min(1.0, log10(n) / 3)  # n=1000 → confidence=1.0
```

## 3. Output Artifacts for Implementation

### 3.1 Files to Use

| File | Purpose | Format |
|------|---------|--------|
| `canonical_names.json` | Spelling variant mappings | `{variant: canonical}` |
| `typo_corrections.json` | Typo corrections with confidence | `{typo: {canonical, confidence}}` |
| `xkcd_coordinates_cache.json` | Pre-computed XKCD centroids | `{name: {r, g, b, n, std}}` |

### 3.2 Files for Reference Only

| File | Purpose |
|------|---------|
| `calibration_analysis.json` | Bias measurements |
| `consolidation_strategy.json` | Strategy comparison |
| `coordinate_analysis.json` | Distribution analysis |

## 4. Uncertainty Budget

### 4.1 Sources of Uncertainty

| Source | Impact | Mitigation |
|--------|--------|------------|
| Uncalibrated monitors | ±19° hue, ±1.6 chroma | Use Centore as ground truth |
| RGB→Munsell conversion | ±0.5 value, ±1 chroma | Use library's validated conversion |
| Crowdsourced naming | High variance | Filter n<100, use centroid weight |
| Typo detection | ~80% precision | Manual review of corrections |

### 4.2 Confidence Levels

| Scenario | Confidence | Recommendation |
|----------|------------|----------------|
| Centore data | High | Use directly |
| XKCD n≥1000 | Medium-High | Use with filtering |
| XKCD 100≤n<1000 | Medium | Use with caution |
| XKCD n<100 | Low | Exclude |

## 5. Future Work

### 5.1 Recommended Enhancements

1. **Full Colorimetric Pipeline**: Implement D65→C chromatic adaptation
   for rigorous XKCD→Munsell conversion.

2. **Cross-Validation**: Hold out some Centore colors to validate
   bias corrections.

3. **Hierarchical Taxonomy**: Link Level 3 (individual) colors to
   Level 2 (compound) and Level 1 (basic) categories.

4. **Perceptual Clustering**: Group similar colors using Munsell
   distance metrics rather than RGB.

### 5.2 Data Quality Improvements

1. Review high-frequency typo corrections manually
2. Build whitelist of valid color names
3. Consider user weighting (frequent contributors may be more reliable)

## 6. Summary Metrics

### 6.1 Final Numbers

| Metric | Value |
|--------|-------|
| Centore unique names | ~7,584 |
| XKCD unique names (filtered) | ~1,369 |
| Canonical mappings | 132,418 |
| Detected typos | 18,702 |
| Calibration points | 30 |
| Hue bias | -19.3° |
| Chroma bias | +1.58 |
| Best strategy | centroid_weighted |
| Strategy distance | 62.82 RGB |

### 6.2 Investigation Statistics

| Phase | Duration | Key Output |
|-------|----------|------------|
| Phase 1: Data Inventory | - | 176K XKCD, 7.6K Centore |
| Phase 2.1: Spelling | - | 132K canonical mappings |
| Phase 2.2: Typos | - | 18.7K corrections |
| Phase 2.3: Compounds | - | 5K hyphen, 7.5K order variants |
| Phase 3: Coordinates | - | Distribution analysis |
| Phase 4: Calibration | - | Bias detection |
| Phase 5: Strategy | - | centroid_weighted wins |
| Phase 6: Synthesis | - | This report |

---

## Appendix A: Quick Start Implementation

```python
# Quick start pseudo-code for consolidation

import json
from pathlib import Path

# Load mappings
with open("canonical_names.json") as f:
    canonical = json.load(f)

with open("typo_corrections.json") as f:
    typos = json.load(f)

with open("xkcd_coordinates_cache.json") as f:
    xkcd = json.load(f)

def get_color_coordinate(name: str, centore_data: dict) -> dict:
    '''Get Munsell coordinate for a color name.'''
    # Standardize name
    std_name = name.lower().strip()
    if std_name in canonical:
        std_name = canonical[std_name]

    # Priority 1: Centore (ground truth)
    if std_name in centore_data:
        return {
            "source": "centore",
            "munsell": centore_data[std_name],
            "confidence": "high"
        }

    # Priority 2: XKCD (crowdsourced)
    if std_name in xkcd:
        entry = xkcd[std_name]
        if entry.get("n", 0) >= 100:
            return {
                "source": "xkcd",
                "rgb": (entry["r"], entry["g"], entry["b"]),
                "n": entry["n"],
                "confidence": "medium" if entry["n"] >= 1000 else "low"
            }

    return None
```

---

*Generated by Phase 6: Synthesis and Recommendations*
*Color Data Investigation Complete*
