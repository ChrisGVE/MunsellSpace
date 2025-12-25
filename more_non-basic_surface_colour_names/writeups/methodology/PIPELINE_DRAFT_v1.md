# Data Pipeline Draft v1

**Date**: 2025-12-25
**Status**: DRAFT - For discussion
**Purpose**: First synthesis of inferred pipeline from existing documentation

---

## Project Goals (Priority Order)

1. **Add new overlays**: Color categories not in Centore's 30
2. **Validate existing overlays**: Firm up Centore's 30 categories (if possible)
3. **Academic paper**: Side goal (TBD)

**Key Constraint**: Must replicate Centore's exact methodology first, then extend.

**Library Output**: New/validated polyhedra only. NOT the bias correction model.

---

## Data Sources

### Primary Sources

| Source | Type | Size | Use |
|--------|------|------|-----|
| Centore CAUS Polyhedra | Spectrophotometer-measured | 30 categories | Reference standard |
| XKCD Color Survey | Screen colors (RGB) | 175,844 names | New color extraction |

### Secondary Sources (Vocabulary)

| Source | Size | Use |
|--------|------|-----|
| Meodai Color Names | ~32,000 | Semantic validation reference |
| ColorHexa | ~1,400 | Semantic validation reference |
| Wikipedia Colors | ~900 | Semantic validation reference |
| ColorName.com | ~1,300 | Semantic validation reference |

---

## Pipeline Architecture

```
TRACK A: REPLICATION (Must do first)
=========================================
Phase 0: Centore Methodology Validation
    ↓
Checkpoint: Can we reproduce Centore's polyhedra?

TRACK B: EXTENSION (After Track A validated)
=========================================
Phase 1: XKCD Data Preparation
    ↓
Phase 2: Semantic Validation
    ↓
Phase 3: RGB → Munsell Conversion
    ↓
Phase 4: Category Extraction
    ↓
Phase 5: Inner Convex Hull Construction
    ↓
Phase 6: Validation & Integration
```

---

## Track A: Centore Replication

### Phase 0: Methodology Validation

**Goal**: Prove we can reproduce Centore's exact results using his methodology.

**Input**:
- Centore's polyhedron data files (30 categories)
- Centore's methodology (JAIC 2020, pp. 31-35)

**Steps**:
1. Parse Centore's polyhedron files to extract vertices
2. Apply inner convex hull algorithm to Centore's raw vertices
3. Compare our computed hull to Centore's published hull
4. Verify: vertices match, centroid matches, volume matches

**Validation Criteria**:
- Vertex count matches for each category
- Centroid within numerical precision
- Hull volume within 1% tolerance

**Decision Point**: If we cannot reproduce Centore's results, STOP and investigate.

**Reference**: `writeups/methodology/centore_inner_hull.md`

---

## Track B: Extension

### Phase 1: XKCD Data Preparation

**Goal**: Extract and clean XKCD color survey data.

**Input**:
- XKCD SQL dump (3.4M responses, 175,844 unique names)

**Steps**:
1. Parse SQL dump to extract (name, RGB) pairs
2. Aggregate by name: compute mean RGB, count responses
3. Basic cleaning: lowercase, normalize whitespace
4. Build master vocabulary from secondary sources

**Output**:
- `xkcd_aggregated.json`: {name, mean_rgb, count, hex_values}
- `master_vocabulary.csv`: Combined reference color names

**Decision Point**: Minimum response count threshold? (Previous work used varying thresholds)

---

### Phase 2: Semantic Validation

**Goal**: Filter to retain only valid color descriptions.

**Input**:
- Aggregated XKCD names
- Master reference vocabulary

**Method**: SBERT semantic similarity
- Model: `all-MiniLM-L6-v2`
- Compare each XKCD name to reference vocabulary
- Keep if max similarity >= threshold

**Previous Work**:
- Threshold: 0.35 cosine similarity
- Results: 137,878 validated (78.4%)
- Rejected: 37,966 (21.6%)

**Decision Points**:
- Is 0.35 the right threshold? (Empirical, needs evaluation)
- Should we use different model? (all-MiniLM-L6-v2 was chosen for speed)

**Output**: `validated_names.json`

---

### Phase 3: RGB → Munsell Conversion

**Goal**: Convert validated colors to Munsell space.

**Input**:
- Validated names with RGB coordinates

**Method**: MunsellSpace library (ASTM D1535 compliant)

**Steps**:
1. Convert mean RGB to Munsell (H, V, C)
2. Convert to Cartesian coordinates for hull computation
3. Flag out-of-gamut colors

**Previous Results**:
- Successfully converted: 133,359 (96.7%)
- Failed (out of gamut): 4,519 (3.3%)

**Output**: `munsell_coordinates.json`

---

### Phase 4: Category Extraction

**Goal**: Identify candidate color categories for new overlays.

**Method Options** (from previous work):

| Method | Approach | Previous Results |
|--------|----------|------------------|
| A Priori | Pattern matching | 210 candidates |
| A Posteriori | Hue variance analysis | 84 color words |
| ML Classification | Random Forest | 75 high-confidence |

**Decision Points**:
- Which extraction method?
- What constitutes a "category" vs "modifier"?
- Which categories are NOT in Centore's 30?

**Output**: List of candidate categories for new overlays

---

### Phase 5: Inner Convex Hull Construction

**Goal**: Build polyhedra for new categories using Centore's methodology.

**Input**:
- XKCD samples for each new category
- Validated methodology from Phase 0

**Method**: Centore's inner convex hull (JAIC 2020)
1. Collect samples matching category name
2. Convert to Cartesian coordinates
3. Compute outer convex hull
4. Discard boundary vertices (outlier removal)
5. Compute inner convex hull
6. Calculate centroid

**Minimum Samples**: Need >= 4 points for 3D hull

**Output**: Polyhedra for new categories

---

### Phase 6: Validation & Integration

**Goal**: Validate new polyhedra and add to MunsellSpace.

**Steps**:
1. Compare new polyhedra to any Centore overlap
2. Check for degenerate cases (too few samples, flat hulls)
3. Document assumptions and limitations
4. Format for library integration
5. Add to MunsellSpace v1.2

---

## Open Questions for Discussion

### Methodology Questions

1. **Centore Replication**: Do we have enough data to reproduce Centore's polyhedra, or only his final results?

2. **XKCD Reliability**: Can screen color data (uncalibrated monitors) produce reliable polyhedra for physical color space?

3. **Bias Correction**: Should we apply corrections for screen-vs-physical differences? (Fourier model is unconfirmed)

### Threshold Questions

4. **Semantic Threshold**: Is 0.35 cosine similarity appropriate? How was it chosen?

5. **Sample Count**: Minimum samples per category? (Centore had 25-1673; XKCD has 100-20,000+)

6. **Outlier Removal**: Single-layer peeling (Centore) or multi-layer (more aggressive)?

### Scope Questions

7. **New Categories**: Which specific categories should we add? (Need list)

8. **Centore Validation**: Should we use XKCD to validate/extend Centore's 30, or keep them separate?

9. **Quality Threshold**: When is a polyhedron "good enough" for the library?

---

## Appendix: What Was Tried (Historical Reference)

From `writeups/old_md/`:

### Semantic Validation Experiments

| Experiment | Method | Outcome |
|------------|--------|---------|
| Exp 1: SBERT | Semantic similarity | **Selected** |
| Exp 2: BERT tokens | Tokenization | Rejected (spelling variants failed) |
| Exp 3: Autoencoder | Character-level | Rejected (non-ASCII failed) |
| Exp 4: Hybrid | SBERT + autoencoder | Rejected (SBERT alone sufficient) |

### Bias Detection (Research Only)

Previous analysis found:
- Value bias: +0.81 (screen appears lighter)
- Chroma bias: +3.82 (screen appears more saturated)
- Hue bias: Non-uniform, category-dependent

**Status**: Unconfirmed. Do not use for library integration.

---

## Next Steps

1. **Discuss this draft**: Clarify scope and decisions
2. **Phase 0 first**: Validate Centore replication before proceeding
3. **Define categories**: Agree on which new overlays to add
4. **Implement rigorously**: Each phase with tests and validation

---

**Document Status**: Draft v1 - For discussion
**Author**: Claude Code
**Date**: 2025-12-25
