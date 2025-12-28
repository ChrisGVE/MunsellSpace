# New Overlay Candidates Report

**Date**: 2025-12-28
**Phase**: Phase 5 - Category Extraction (Track C)
**Method**: SBERT Semantic Clustering + RGB Spatial Coherence Analysis

---

## Executive Summary

After analyzing 3,000 color names via SBERT semantic clustering and validating against Centore's 30 reference categories, we identified **5 strong candidates** for new semantic overlays:

| Rank | Candidate | Frequency | Coherence | Combined Score | Status |
|------|-----------|-----------|-----------|----------------|--------|
| 1 | **INDIGO** | 11 variants | 0.960 | 0.593 | RECOMMEND |
| 2 | **MAROON** | 9 variants | 0.967 | 0.539 | RECOMMEND |
| 3 | **LIME** | 7 variants | 0.998 | 0.482 | CONSIDER |
| 4 | **PLUM** | 5 variants | 0.974 | 0.403 | CONSIDER |
| 5 | **AQUAMARINE** | 5 variants | 0.919 | 0.391 | CONSIDER |

---

## Methodology

### 1. Semantic Clustering (SBERT)
- Used `all-MiniLM-L6-v2` sentence embeddings
- K-means clustering into 20 families
- Validated against Centore anchor families: 57.6% purity, 69.4% recall

### 2. Candidate Extraction
- Identified base color words in each cluster
- Filtered out Centore's existing 30 categories
- Required minimum 5 variants per candidate
- Excluded offensive terms (puke, vomit, etc.)

### 3. Spatial Coherence Analysis
- Computed RGB centroid and standard deviation for each candidate
- Coherence score = 1 - (volume / max_volume)
- Higher coherence = more compact color space distribution

### 4. Combined Ranking
- Combined score = √(frequency_norm × coherence)
- Frequency normalized against max observed (30)

---

## Recommended Candidates

### 1. INDIGO

**Status**: RECOMMEND
**Combined Score**: 0.593

| Metric | Value |
|--------|-------|
| Frequency | 11 variants |
| Spatial Coherence | 0.960 (EXCELLENT) |
| RGB Centroid | (70.8, 58.8, 154.0) |
| Hex Centroid | #463a9a |
| Source Cluster | magenta |

**Variants Found**:
- indigo, dark indigo, persian indigo, electric indigo
- light indigo, lavender indigo, indigo dye
- bright indigo, deep indigo, mood indigo, ultra violet

**Justification**:
- Distinct from Centore's `violet` and `purple` - occupies blue-purple transition
- Strong semantic coherence (all variants contain "indigo")
- Excellent spatial coherence in RGB space
- Historically significant pigment (natural dye)

**Recommendation**: Include in new overlay set

---

### 2. MAROON

**Status**: RECOMMEND
**Combined Score**: 0.539

| Metric | Value |
|--------|-------|
| Frequency | 9 variants |
| Spatial Coherence | 0.967 (EXCELLENT) |
| RGB Centroid | (148.8, 48.8, 76.5) |
| Hex Centroid | #94304c |
| Source Cluster | maroon |

**Variants Found**:
- maroon, dark maroon, light maroon, bright maroon
- up maroon, deep maroon, rich maroon, royal maroon, mystic maroon

**Justification**:
- Not in Centore's 30 (distinct from burgundy, wine, crimson)
- High frequency in XKCD data
- Excellent spatial coherence
- Named its own SBERT cluster (strong semantic identity)

**Recommendation**: Include in new overlay set

---

### 3. LIME

**Status**: CONSIDER
**Combined Score**: 0.482

| Metric | Value |
|--------|-------|
| Frequency | 7 variants |
| Spatial Coherence | 0.998 (EXCELLENT) |
| RGB Centroid | (178.3, 252.3, 58.4) |
| Hex Centroid | #b2fc3a |
| Source Cluster | peach |

**Variants Found**:
- lime, electric lime, lemon lime, key lime
- bright lime, light lime, pale lime

**Justification**:
- Near-perfect spatial coherence (0.998)
- Distinct yellow-green category
- Clear fruit-based naming pattern
- May overlap with Centore's `yellow` edge cases

**Recommendation**: Include if sample threshold met (≥25)

---

### 4. PLUM

**Status**: CONSIDER
**Combined Score**: 0.403

| Metric | Value |
|--------|-------|
| Frequency | 5 variants |
| Spatial Coherence | 0.974 (EXCELLENT) |
| RGB Centroid | (123.8, 52.6, 90.6) |
| Hex Centroid | #7b345a |
| Source Cluster | peach |

**Variants Found**:
- plum, light plum, dark plum, persian plum, sugar plum

**Justification**:
- Excellent spatial coherence
- Distinct from Centore's `purple` and `mauve`
- Fruit-based naming (like lime)
- Borderline frequency (5 variants)

**Recommendation**: Include if XKCD full sample count ≥25

---

### 5. AQUAMARINE

**Status**: CONSIDER
**Combined Score**: 0.391

| Metric | Value |
|--------|-------|
| Frequency | 5 variants |
| Spatial Coherence | 0.919 (GOOD) |
| RGB Centroid | (81.3, 195.7, 179.3) |
| Hex Centroid | #51c3b3 |
| Source Cluster | aqua |

**Variants Found**:
- aquamarine, dark aquamarine, light aquamarine
- medium aquamarine, deep aquamarine

**Justification**:
- Good spatial coherence
- Related to but distinct from Centore's `aqua`
- Gemstone-based naming
- May be considered sub-category of aqua

**Recommendation**: Evaluate overlap with `aqua` polyhedron before including

---

## Excluded Candidates

### GREY (Excluded)

**Reason**: British spelling variant of `gray`, which is already in Centore's basic 10.

| Metric | Value |
|--------|-------|
| Frequency | 20 variants (highest) |
| Spatial Coherence | 0.963 |

**Decision**: EXCLUDE - Not a new category, just spelling variant.

---

### BLACK (Needs Investigation)

**Status**: INVESTIGATE

| Metric | Value |
|--------|-------|
| Frequency | 9 variants |
| Spatial Coherence | 0.999 (EXCELLENT) |
| RGB Centroid | (11.3, 13.3, 13.3) |
| Hex Centroid | #0b0d0d |

**Observation**: Centore's 30 includes `white` but NOT `black`. This is notable because both are achromatic endpoints of the Munsell value axis.

**Possible explanations**:
1. Intentional omission (fashion industry uses "black" as exact, not named)
2. Statistical coincidence (not enough "black" samples met Centore's criteria)
3. Oversight in the original study

**Recommendation**: Research Centore's paper for rationale before including. If unexplained, consider adding as neutral endpoint complement to `white`.

---

### SILVER (Insufficient Data)

**Status**: DEFER

Only 14 variants found in SBERT clusters, but fewer than 3 matched in colornames dataset.

**Note**: Silver is a metallic color that may not have good RGB representation. Consider for future work with spectral data.

---

### CARMINE (Insufficient Data)

**Status**: DEFER

7 variants found in SBERT clusters, but fewer than 3 matched in colornames dataset.

**Note**: Historical pigment name, may warrant inclusion if more samples available.

---

## Next Steps (Phase 6)

For each recommended candidate:

1. **Extract XKCD samples** matching the candidate name
2. **Convert to Munsell coordinates** using MunsellSpace library
3. **Build inner convex hull** using Centore's validated methodology
4. **Verify sample count** ≥25 (Centore's minimum)
5. **Check overlap** with existing Centore polyhedra
6. **Generate polyhedron JSON** for library integration

---

## Appendix: Centore's 30 Categories

### Basic Colors (10)
blue, brown, gray, green, orange, pink, purple, red, white, yellow

### Non-Basic Colors (20)
aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy, peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine

---

*Generated by Phase 5 Category Extraction pipeline*
