# Color Word Extraction Methodology

This document describes the three methods used to extract color words from the XKCD color survey dataset for potential inclusion in MunsellSpace's semantic overlay system.

## Overview

The goal is to identify words that refer to specific colors (like "salmon", "teal") versus words that are modifiers (like "light", "dark") or non-color terms.

| Method | Approach | Pros | Cons |
|--------|----------|------|------|
| A Priori | Pattern matching | High precision, fast | Selection bias |
| A Posteriori | Hue variance classification | Unbiased, data-driven | Threshold sensitivity |
| ML Classification | Random Forest on features | Handles edge cases | Requires training data |

## Dataset

**XKCD Color Survey (2010)**
- ~3.4 million color naming responses
- 171,780 unique color names
- Each response: RGB value + user-provided color name
- Source: https://blog.xkcd.com/2010/05/03/color-survey-results/

## Method 1: A Priori Extraction

### Approach
Pre-define a list of expected color names and search for matches in the dataset.

```python
OVERLAY_PATTERNS = [
    "salmon", "seafoam", "burgundy", "maroon", "cream", ...
]

# Match color names containing any pattern
for name in color_names:
    for pattern in OVERLAY_PATTERNS:
        if pattern in name:
            candidates.append(name)
```

### Pros
- **High precision**: Known color terms are reliably identified
- **Fast**: Simple string matching
- **Interpretable**: Clear criteria for inclusion

### Cons
- **Selection bias**: Only finds colors we already know about
- **Limited coverage**: Misses novel or unexpected color terms
- **Subjective**: Pattern list is manually curated

### Results
- **210 candidates** found
- **16% coverage** of total responses
- **84% ignored** - potentially valid colors missed

### Files
- Script: `a_priori_extraction.py`
- Output: `results/xkcd_overlay_candidates_apriori.csv`

---

## Method 2: A Posteriori Extraction

### Approach
Data-driven classification using hue variance as the discriminating feature.

**Intuition**: A true color word (like "blue") should consistently refer to colors in a narrow hue range. A modifier (like "dark") appears with many different hues.

```python
# Tokenize all color names into words
words = tokenize_all_color_names(dataset)

# For each word, compute hue statistics
for word in words:
    colors = get_colors_containing(word)
    hue_std = circular_std([rgb_to_hue(c) for c in colors])

    if hue_std < 40°:
        classify_as_color_word(word)
    elif hue_std > 60°:
        classify_as_modifier(word)
    else:
        classify_as_ambiguous(word)
```

### Statistical Foundation

**Circular Statistics**: Hue is a circular variable (0° = 360°), requiring circular mean and standard deviation formulas.

```
circular_mean = atan2(Σsin(θ), Σcos(θ))
circular_std = √(-2 * ln(R))  where R = |Σe^(iθ)| / n
```

### Classification Thresholds

| Hue Std | Classification | Interpretation |
|---------|---------------|----------------|
| < 40° | Color word | Refers to specific hue region |
| > 60° | Modifier | Applies across hue spectrum |
| 40-60° | Ambiguous | Needs manual review |

### Pros
- **Unbiased**: No pre-conceived list of colors
- **Data-driven**: Classification emerges from the data
- **Discovers unknown**: Can find color terms we didn't expect

### Cons
- **Threshold sensitivity**: Results depend on 40°/60° cutoffs
- **Achromatic handling**: Gray/black/white need special treatment
- **Compound names**: "Army green" may classify "army" incorrectly

### Results
- **84 color words** identified
- **66 modifiers** identified
- **13 ambiguous** words

### Files
- Script: `a_posteriori_extraction.py`
- Output: `results/xkcd_word_analysis.json`, `results/xkcd_word_candidates.csv`

---

## Method 3: ML Classification

### Approach
Train a Random Forest classifier on labeled examples, then predict on unlabeled words.

**Training Data**:
- **Positive (color terms)**: Centore 20 overlays + ISCC-NBS basic terms + known colors
- **Negative (modifiers)**: light, dark, bright, pale, -ish suffixes, etc.

**Features**:
```python
features = [
    hue_std,      # Circular hue standard deviation
    sat_mean,     # Mean saturation
    sat_std,      # Saturation standard deviation
    val_mean,     # Mean value (brightness)
    val_std,      # Value standard deviation
    num_colors,   # Number of color variants
    word_len      # Word length in characters
]
```

### Model
- **Algorithm**: Random Forest (100 trees, max_depth=5)
- **Preprocessing**: StandardScaler normalization
- **Validation**: 5-fold cross-validation

### Feature Importance

| Feature | Importance | Interpretation |
|---------|------------|----------------|
| hue_std | 48.0% | Most discriminative feature |
| val_std | 14.9% | Value consistency matters |
| sat_mean | 9.9% | Saturation level relevant |
| sat_std | 9.5% | Saturation consistency |
| val_mean | 7.0% | Brightness level |
| num_colors | 6.6% | Usage frequency |
| word_len | 4.2% | Longer words slightly more likely modifiers |

### Pros
- **Handles edge cases**: Learns complex decision boundaries
- **Non-linear relationships**: Can capture feature interactions
- **Quantified confidence**: Provides probability scores

### Cons
- **Requires labeled data**: Performance limited by training set quality
- **Overfitting risk**: May memorize training examples
- **Less interpretable**: "Black box" compared to threshold method

### Results
- **83.33% cross-validation accuracy**
- **75 words** both methods agree are COLOR
- **62 words** both methods agree are MODIFIER
- **40 high-confidence** new overlay candidates

### Files
- Script: `ml_classification.py`
- Output: `results/classification_comparison.json`

---

## Comparison of Methods

### Agreement Analysis

| Agreement | Count | Description |
|-----------|-------|-------------|
| Both COLOR | 75 | High-confidence color terms |
| Both MODIFIER | 62 | High-confidence modifiers |
| Statistical only | ~5 | Statistical says color, ML disagrees |
| ML only | ~8 | ML says color, statistical disagrees |
| Disagreements | ~13 | Methods disagree |

### Key Insight

The ML classifier **validates** the statistical approach:
- hue_std is the most important feature (48%)
- The 40°/60° thresholds are approximately what the ML learns
- Disagreements are primarily edge cases (-ish suffixes, compound modifiers)

### Recommendation: Ensemble Approach

Use **both methods** for final classification:
1. Run statistical method (fast, interpretable)
2. Run ML method (handles edge cases)
3. Accept words where **both agree** as high-confidence
4. Manual review where they disagree

---

## Bayesian vs Frequentist Note

**Q: Is the a posteriori method Bayesian?**

No, it's more **frequentist**:
- Uses observed frequencies without prior beliefs
- Classification based on threshold rules, not probability distributions
- No updating of beliefs as data is processed

A true **Bayesian approach** would:
1. Start with prior probabilities (e.g., P(color) = 0.3)
2. Update based on evidence (hue clustering)
3. Produce posterior probabilities P(color|features)
4. Allow incorporation of expert knowledge as priors

The ML method is closer to Bayesian in spirit (produces probabilities) but is still fundamentally frequentist (no priors).

---

## Excluded Terms

Certain words are excluded from final results regardless of classification:

**Offensive terms** (user requested):
- puke, vomit, poop, poo, shit

**See**: `excluded_colors.txt` for full list with rationale.

---

## Usage

```bash
# Run all preprocessing (in order)
cd overlay-preprocessing

# 1. A priori extraction (creates aggregates)
python a_priori_extraction.py

# 2. A posteriori extraction (requires aggregates)
python a_posteriori_extraction.py

# 3. ML classification (requires word analysis)
python ml_classification.py
```

**Requirements**:
```bash
pip install scikit-learn numpy
```

---

## Output Files

| File | Description |
|------|-------------|
| `results/xkcd_color_aggregates.json` | Full XKCD color statistics |
| `results/xkcd_overlay_candidates_apriori.csv` | A priori candidates |
| `results/xkcd_word_analysis.json` | A posteriori classification |
| `results/xkcd_word_candidates.csv` | A posteriori color words |
| `results/classification_comparison.json` | ML comparison results |
| `excluded_colors.txt` | Filtered terms |

---

## References

1. Centore, P. (2020). "Beige, aqua, fuchsia, etc." *J. Int. Colour Assoc.*, 25, 24-54.
2. Munroe, R. (2010). "Color Survey Results." https://blog.xkcd.com/
3. Fisher, N.I. (1993). *Statistical Analysis of Circular Data*. Cambridge University Press.
