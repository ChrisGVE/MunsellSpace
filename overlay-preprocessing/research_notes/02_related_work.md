# Related Work

## Overview

This research intersects several domains: color naming and categorization,
crowdsourced color data, RGB-to-Munsell conversion, and sentence embedding
methods for semantic similarity. This section reviews the foundational work
in each area.

---

## 1. Color Naming and Categorization

### 1.1 Berlin & Kay (1969)

The seminal work on cross-cultural color naming. Berlin and Kay proposed that
all languages share a universal inventory of basic color terms, acquired in
a predictable order:

```
Stage I:   black, white
Stage II:  + red
Stage III: + green OR yellow
Stage IV:  + green AND yellow
Stage V:   + blue
Stage VI:  + brown
Stage VII: + purple, pink, orange, gray
```

**Relevance**: Our 30 Centore categories include all basic color terms plus
extended vocabulary (teal, turquoise, beige). The high-agreement categories
(red, blue, green) align with Berlin & Kay's focal colors.

### 1.2 Regier, Kay & Khetarpal (2007)

Extended Berlin & Kay's work with computational modeling, showing that color
naming systems optimize for communicative efficiency. Languages carve color
space into regions that maximize discriminability while minimizing cognitive
load.

**Relevance**: Explains why color category boundaries are fuzzy and why
transitional colors (teal, turquoise) show high variance.

### 1.3 Monroe et al. (2008)

Analyzed online color naming data from an earlier web survey, finding:
- English speakers use fine-grained color vocabulary
- Color boundaries vary by context and speaker
- Agreement is highest for focal colors

**Relevance**: The XKCD survey replicates these findings at larger scale.

---

## 2. Crowdsourced Color Data

### 2.1 XKCD Color Survey (Munroe, 2010)

The data source for our screen color analysis. Randall Munroe collected
~3.4 million responses from web users who named randomly-generated RGB colors.

Key characteristics:
- Freeform text entry (no vocabulary constraints)
- Colors displayed on user's own monitor (uncalibrated)
- English-speaking, tech-savvy demographic
- Includes noise (profanity, jokes, random strings)

**Relevance**: Largest available color naming dataset; requires semantic
filtering before use.

### 2.2 Moroney (2003)

Proposed methods for aggregating color naming data from multiple observers.
Key insight: inter-observer variability is substantial; large sample sizes
are needed for reliable category boundaries.

**Relevance**: Justifies our focus on category-level bias rather than
individual color bias.

### 2.3 Lindner & Süsstrunk (2017)

Analyzed color naming consistency across languages using online surveys.
Found that basic color terms have high cross-linguistic agreement, but
extended vocabulary diverges significantly.

**Relevance**: Our English-only analysis may not generalize to other
languages for non-basic colors.

---

## 3. RGB to Munsell Conversion

### 3.1 Munsell Renotation Data (Newhall et al., 1943)

The original empirical dataset mapping Munsell notations to CIE coordinates.
Collected through extensive psychophysical experiments with human observers.

**Relevance**: Foundation for all Munsell conversion algorithms.

### 3.2 ASTM D1535 Standard

The American Society for Testing and Materials standard for Munsell color
notation. Specifies:
- Conversion algorithms from CIE coordinates to Munsell
- Precision requirements
- Edge case handling

**Relevance**: Our MunsellSpace library implements ASTM D1535 for accurate
RGB-to-Munsell conversion.

### 3.3 Centore (2012)

Paul Centore's "An Algorithm for Interpolation in Munsell Space" provides
a practical implementation of Munsell conversion. His "Real Colour Wheel"
project includes spectrophotometer-measured physical samples organized into
color categories.

**Relevance**: Primary physical reference for our bias analysis.

### 3.4 colour-science Library

Open-source Python library implementing color science algorithms, including
RGB-to-Munsell conversion. Our Rust implementation was validated against this
reference.

**Relevance**: Validation reference for conversion accuracy.

---

## 4. Sentence Embeddings for Semantic Similarity

### 4.1 Word2Vec (Mikolov et al., 2013)

Pioneered distributed word representations. Words with similar meanings have
similar vectors. However, single-word embeddings cannot capture compound
color names like "dusty rose."

**Relevance**: Insufficient for our use case; need sentence/phrase embeddings.

### 4.2 BERT (Devlin et al., 2019)

Bidirectional Transformer for language understanding. Produces contextual
embeddings. However, raw BERT embeddings are not optimized for semantic
similarity at the sentence level.

**Relevance**: BERT tokenization failed for color name validation due to
spelling variant sensitivity (gray ≠ grey).

### 4.3 Sentence-BERT (Reimers & Gurevych, 2019)

Fine-tunes BERT for sentence similarity tasks. Produces embeddings where
similar sentences have high cosine similarity.

**Relevance**: Core method for our semantic validation. SBERT similarity
≥ 0.35 effectively filters non-color terms.

### 4.4 all-MiniLM-L6-v2

Distilled SBERT model optimized for speed while maintaining quality. Trained
on over 1 billion sentence pairs.

**Relevance**: Specific model used in our validation pipeline.

---

## 5. Screen vs Physical Color Perception

### 5.1 Hunt Effect (Hunt, 1952)

Chromatic adaptation depends on luminance level. Colors appear more saturated
at higher luminance (self-luminous displays) compared to lower luminance
(reflected surfaces).

**Relevance**: Partially explains our +3.82 chroma bias (screen colors more
saturated).

### 5.2 Stevens Effect (Stevens, 1961)

Perceived contrast increases with luminance. Dark colors appear darker and
light colors appear lighter on brighter displays.

**Relevance**: May contribute to value perception differences.

### 5.3 Fairchild (2013)

"Color Appearance Models" provides comprehensive treatment of how viewing
conditions affect color perception. Key factors:
- Adaptation state
- Background luminance
- Chromatic adaptation to illuminant
- Self-luminous vs reflective observation

**Relevance**: Theoretical framework for understanding screen-physical
color differences.

### 5.4 sRGB Gamut Limitations (Stokes et al., 1996)

The sRGB color space cannot represent highly saturated cyans and teals.
Colors outside the gamut are clipped or compressed.

**Relevance**: Explains why teal and turquoise show the largest hue shifts
(-40°): they are pushed toward blue because sRGB cannot represent their true
hue.

---

## 6. Non-Linear Color Correction

### 6.1 Polynomial Color Correction (Finlayson et al., 1998)

Uses polynomial models to correct color between devices. Demonstrated that
higher-order terms improve accuracy for non-linear color responses.

**Relevance**: Supports our polynomial approach for hue correction.

### 6.2 Radial Basis Functions for Color (Vrhel & Trussell, 1992)

Applied RBF interpolation to color matching. Smooth interpolation through
known points.

**Relevance**: Basis for our spline interpolation approach.

### 6.3 Neural Networks for Color (Stiles & Burch, 2007)

Neural networks can learn complex color transformations from data.

**Relevance**: Supports neural network approach, though small training set
is a concern.

---

## 7. Gap in Literature

Prior work has addressed:
- Color naming patterns (Berlin & Kay, Monroe et al.)
- Crowdsourced color data collection (XKCD, Moroney)
- RGB to Munsell conversion (ASTM, Centore)
- Screen color perception (Hunt, Fairchild)

**What is missing**: Systematic quantification of screen-to-physical color
bias using crowdsourced data, and discovery that hue bias is non-uniform
(category-dependent).

This research fills that gap by:
1. Connecting crowdsourced screen colors to physical references
2. Quantifying bias in each Munsell dimension
3. Discovering the non-linear nature of hue bias
4. Proposing correction approaches

