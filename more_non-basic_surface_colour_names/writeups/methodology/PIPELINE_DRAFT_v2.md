# Data Pipeline Draft v2

**Date**: 2025-12-25
**Status**: DRAFT - Revised based on discussion
**Purpose**: Refined pipeline incorporating user feedback and open questions

---

## Project Goals (Priority Order)

1. **Add new overlays**: Color categories not in Centore's 30
2. **Validate existing overlays**: Firm up Centore's 30 categories (if possible)
3. **Academic paper**: Side goal (TBD)

**Key Constraint**: Must replicate Centore's exact methodology first, then extend.

**Library Output**: New/validated polyhedra only. NOT the bias correction model.

---

## Critical Question: Raw vs Processed Data

### Centore's Published Data

**Observation**: The polyhedron files contain:
- Color name
- Number of CAUS samples
- Centroid (Munsell and Cartesian)
- Polyhedron vertices (Munsell coordinates)

**Assessment**: This appears to be **PROCESSED data** (the final inner hull vertices), not the raw CAUS samples. The sample counts are mentioned but the original samples are not provided.

**Implication**: We can **verify** Centore's final polyhedra but cannot **replicate** his data cleanup process without raw CAUS data.

### Centore's Data Cleanup (from paper pp. 31-35)

According to user knowledge of the paper, Centore applied two filtering steps:

#### Step 1: Illuminant Filtering (Fluorescent Exclusion)
- **Purpose**: Remove samples measured under non-standard illumination
- **Method**: Exclude fluorescent color samples
- **Relevance to us**: May inform how we handle screen data later

#### Step 2: Color Consistency Filtering
- **Purpose**: Ensure samples genuinely represent the target color
- **Method**: Exclude certain colors (details in paper)
- **Relevance to us**: May be reusable/adaptable for our pipeline

**Action Item**: Document exact filtering criteria from paper for potential reuse.

---

## Data Sources

### Primary Sources

| Source | Type | Size | Use |
|--------|------|------|-----|
| Centore CAUS Polyhedra | Processed (inner hulls) | 30 categories | Reference standard |
| XKCD Color Survey | Screen colors (RGB) | 175,844 names | New color extraction |

### Reference Vocabulary Sources (for semantic validation)

| Source | Size | Use |
|--------|------|-----|
| Centore Color Names | 30 | Reference vocabulary |
| Meodai Color Names | ~32,000 | Reference vocabulary |
| ColorHexa | ~1,400 | Reference vocabulary |
| Wikipedia Colors | ~900 | Reference vocabulary |
| ColorName.com | ~1,300 | Reference vocabulary |
| XKCD Summary (curated) | 954 | Reference vocabulary |

**Note**: The XKCD summary (954 colors) was curated by Randall Munroe and is kept as a reference source, not filtered.

---

## Pipeline Architecture

```
TRACK A: METHODOLOGY VALIDATION (Must complete first)
=======================================================
Phase 0: Centore Polyhedra Verification
    ↓
Checkpoint: Can we parse and reproduce his published polyhedra?
    ↓
Output: Validation tolerance established

TRACK B: SCREEN-TO-PHYSICAL UNDERSTANDING (Critical research)
==============================================================
Phase 1: Reference Vocabulary Construction
    ↓
Phase 2: XKCD Semantic Validation (filter to color names)
    ↓
Phase 3: Calibration Subset Analysis
    ↓
Checkpoint: Can we quantify and correct screen-physical bias?
    ↓
Decision: Proceed with conversion or investigate further

TRACK C: EXTENSION (After Track A + B validated)
=================================================
Phase 4: Full Dataset Conversion
    ↓
Phase 5: Category Extraction
    ↓
Phase 6: Inner Convex Hull Construction
    ↓
Phase 7: Validation & Integration
```

---

## Track A: Methodology Validation

### Phase 0: Centore Polyhedra Verification

**Goal**: Prove we can correctly parse and represent Centore's published polyhedra.

**Input**:
- Centore's polyhedron data files (30 categories)

**Steps**:
1. Parse Centore's polyhedron files to extract vertices
2. Verify vertex coordinates are correctly interpreted
3. Compute centroid from vertices (compare to published centroid)
4. Compute hull volume from vertices
5. Document parsing format and any ambiguities

**Validation Criteria**:
- Published centroid matches computed centroid (numerical precision)
- Vertex counts match published sample counts logic
- Hull is valid 3D convex polyhedron

**Output**:
- Parsing code verified against 30 categories
- Tolerance bounds established for centroid matching
- Understanding of what we CAN verify

**Decision Point**: If we cannot accurately parse the data, STOP and investigate format issues.

**Note**: Since we have processed data (not raw), this validates our **parsing** of Centore's results, not our ability to **replicate** his data cleanup.

---

## Track B: Screen-to-Physical Understanding

### Phase 1: Reference Vocabulary Construction

**Goal**: Build a merged reference vocabulary for semantic validation.

**Input**:
- Centore's 30 color names
- Non-XKCD vocabulary sources (Meodai, ColorHexa, Wikipedia, ColorName.com)
- XKCD summary (954 curated names)

**Steps**:
1. Merge all sources into single vocabulary
2. Apply name normalization:
   - Lowercase all names
   - Normalize whitespace (collapse multiple spaces, trim)
   - Handle quotes:
     - Remove surrounding `"` or `'` if entire name is quoted
     - Keep `'` in gerundive forms (e.g., "hunter's green")
     - Keep partial quotes as-is
   - Collect all special characters found in dataset (for review)
3. De-duplicate exact matches
4. Document source for each name (for provenance)

**Output**:
- `master_vocabulary.csv`: Unified reference vocabulary (~35,000 unique names)
- `special_characters_found.txt`: List of special characters for review

**Name Cleaning Rules** (to be refined):
```
Original              → Cleaned
"dusty rose"          → dusty rose     (remove surrounding quotes)
'hunter's green'      → hunter's green (keep apostrophe in gerundive)
OCEAN BLUE            → ocean blue     (lowercase)
light  blue           → light blue     (normalize whitespace)
```

---

### Phase 2: XKCD Semantic Validation

**Goal**: Filter XKCD names to retain only valid color descriptions.

**Core Question**: "Is this the name of a color?"

**Input**:
- XKCD 175,844 unique names
- Master reference vocabulary

**Method**: SBERT semantic similarity
- Model: `all-MiniLM-L6-v2` (or evaluate alternatives)
- Compare each XKCD name to reference vocabulary
- Keep if max similarity >= threshold

**Previous Work**:
- Threshold: 0.35 cosine similarity
- Results: 137,878 validated (78.4%)

**Decision Points**:
- Is 0.35 the right threshold? Needs empirical evaluation
- Should we evaluate other tokenization models?
- What is the false positive/negative rate at this threshold?

**Threshold Evaluation Method**:
1. Sample 200 names near threshold (0.30-0.40)
2. Manually classify as valid/invalid color name
3. Compute precision/recall at various thresholds
4. Select threshold balancing both

**Output**:
- `xkcd_validated.json`: Validated XKCD names with RGB
- `xkcd_rejected.json`: Rejected names (for analysis)
- Threshold justification documentation

---

### Phase 3: Calibration Subset Analysis

**Goal**: Understand the relationship between screen colors and physical Munsell space BEFORE converting the full dataset.

**Core Problem**: Screen color perception differs from physical color measurement.

#### Previous Observations (from historical analysis):
| Dimension | Mean Bias | Interpretation |
|-----------|-----------|----------------|
| Value | +0.81 | Screen appears lighter |
| Chroma | +3.82 | Screen appears more saturated |
| Hue | Non-uniform | Category-dependent |

#### The Fundamental Question

When a user names a screen color, they perceive it as brighter and more saturated. Two approaches:

**Approach A: Correct for Observed Bias**
- Measure bias between screen and Centore polyhedra
- Apply correction to "undo" the perceptual difference
- **Assumption**: The bias is a measurement artifact to be corrected

**Approach B: Illuminant Transform**
- Find an illuminant under which Munsell coordinates would match LCD response
- Apply chromatic adaptation (e.g., Bradford transform) from that illuminant to D65
- **Assumption**: Screen viewing conditions simulate a different illuminant

**Approach C: Accept the Difference**
- Screen colors represent a different domain than physical colors
- Build separate polyhedra without merging/comparing
- **Assumption**: Cross-domain comparison may not be meaningful

#### Proposed Investigation

**Step 3.1**: Select Calibration Subset
- From non-XKCD, non-Centore vocabulary sources
- Pick colors whose names match Centore's 30 categories
- These become calibration points

**Step 3.2**: Convert Only Calibration Subset to Munsell
- Use MunsellSpace library (ASTM D1535 compliant)
- Standard sRGB → XYZ → Munsell conversion

**Step 3.3**: Compute Bias Analysis
- Compare our polyhedra (from screen sources) to Centore's polyhedra
- Quantify per-dimension bias (H, V, C)
- Analyze whether bias is uniform or category-dependent

**Step 3.4**: Investigate Illuminant Hypothesis
- Can we model the bias as an illuminant transform?
- Check if fluorescent colors (that Centore excluded) provide insight
- Explore Bradford or CIECAM02 chromatic adaptation

**Output**:
- Quantified bias model (or determination that bias is not correctable)
- Decision on how to proceed with full conversion
- Documentation of assumptions made

**Decision Point**: Do not proceed to full conversion until we understand this relationship.

#### Research Questions

1. Is it valid to "correct" for perceptual bias when that bias reflects genuine perception?
2. Could there be an illuminant that resolves the screen-physical mismatch?
3. What assumptions are we making when applying any correction?
4. Could Centore's excluded fluorescent colors help answer this?

---

## Track C: Extension (After Track A + B)

### Phase 4: Full Dataset Conversion

**Goal**: Convert all validated XKCD colors to Munsell space.

**Prerequisites**:
- Track B Phase 3 completed
- Bias model understood (and decision made on correction)

**Input**:
- Validated XKCD names with RGB

**Method**:
- Apply MunsellSpace conversion
- Apply bias correction if determined appropriate in Phase 3

**Output**:
- `munsell_coordinates.json`: Full dataset in Munsell

---

### Phase 5: Category Extraction

**Goal**: Identify candidate color categories for new overlays.

**Method**: Semantic analysis (more sophisticated than substring matching)

**Previous Approaches**:
| Method | Description | Previous Results |
|--------|-------------|------------------|
| A Priori | Pattern matching for color words | 210 candidates |
| A Posteriori | Hue variance analysis | 84 color words |
| ML Classification | Random Forest | 75 high-confidence |

**Refined Approach**:
1. Use semantic clustering (SBERT embeddings)
2. Identify color word clusters (semantic, not just substring)
3. Filter to exclude Centore's 30 categories
4. Curate list before committing

**Category Criteria**:
- Must be a recognizable color category (not modifier or compound)
- Must have sufficient samples (use Centore's minimum as threshold)
- Must show spatial coherence in Munsell space

**Output**:
- Curated list of new category candidates
- Justification for each candidate

---

### Phase 6: Inner Convex Hull Construction

**Goal**: Build polyhedra for new categories using Centore's exact methodology.

**Input**:
- XKCD samples for each new category
- Validated methodology from Track A

**Method**: Centore's inner convex hull (JAIC 2020)
1. Collect samples matching category name
2. Convert to Cartesian coordinates (Centore's formula)
3. Compute outer convex hull
4. Discard boundary vertices (single-layer peeling per Centore)
5. Compute inner convex hull
6. Calculate filled-solid centroid

**Minimum Samples**: Use Centore's minimum as threshold

**Output**: Polyhedra for new categories

---

### Phase 7: Validation & Integration

**Goal**: Validate new polyhedra and add to MunsellSpace.

**Quality Criteria** (to be refined):
1. **Locality**: Polyhedron should be localized, not global (similar to Centore's)
2. **Non-degenerate**: Valid 3D hull with meaningful volume
3. **Consistent**: Multiple samples from different sources agree
4. **Distinct**: Not overlapping excessively with existing categories

**Steps**:
1. Check each polyhedron against quality criteria
2. For categories overlapping Centore's 30: compare carefully
   - Do NOT "bastardize" Centore's polyhedra
   - Keep extension data separate if uncertain
3. Document assumptions and limitations
4. Format for library integration
5. Add to MunsellSpace (version TBD)

---

## Additional Requirement: Color Name Collection

**Goal**: Maintain a collection of color names with coordinates and vicinity.

**Sources**:
- Centore's categories
- Our datasets (non-XKCD)
- XKCD validated names

**Exclusion Filter**: Remove names containing offensive words
- Examples: pee, puke, poop, etc.
- Compile list of excluded terms
- Apply filter before final collection

**Output**:
- `color_name_collection.json`: Curated color names with:
  - Name
  - Coordinate (Munsell)
  - Vicinity (polyhedron or uncertainty bounds)
  - Source

---

## Resolved Questions

Based on discussion:

| Question | Resolution |
|----------|------------|
| Sample count minimum | Use Centore's minimum; quantity controlled by category count |
| Outlier removal | Adopt Centore's single-layer peeling (apples to apples) |
| New categories | Generate from semantic analysis, curate before committing |
| Centore validation | Use exclusively Centore's for methodology; evaluate extension separately |
| Quality threshold | Polyhedra should be localized; may find criteria from geometry literature |

---

## Open Questions Requiring Further Research

### Illuminant and Perception

1. **Illuminant resolution**: Is there an illuminant under which LCD colors would match Centore's Munsell coordinates? Could chromatic adaptation (Bradford, CIECAM02) provide a principled correction?

2. **Fluorescent colors**: Could Centore's excluded fluorescent samples provide insight into the illuminant question? (Fluorescent materials exhibit enhanced appearance under certain illuminants.)

3. **Perceptual validity**: When users name screen colors perceived as brighter/more saturated, is it correct to "correct" for this? Or does the perception itself matter?

### Methodological

4. **Centore raw data access**: Can we obtain the raw CAUS data (before Centore's filtering)? This would enable true replication.

5. **Color consistency filtering**: What exactly did Centore exclude for "color consistency"? Can we adapt this for our pipeline?

6. **Quality criteria from literature**: What criteria exist in geometry/convex set literature for polyhedron quality? Locality, volume, stability?

---

## Appendix: Centore Methodology Reference

From `writeups/methodology/centore_inner_hull.md`:

### Inner Convex Hull Algorithm

1. **Collect samples** for category (color name matching)
2. **Convert to Cartesian**:
   ```
   x = C × cos(H × π/50)
   y = C × sin(H × π/50)
   z = V
   ```
   Where H is on 0-100 scale (100 = 360°)

3. **Compute outer hull** H of sample set S
4. **Extract vertices** V of H (minimal generating set)
5. **Remove vertices** to get S−V (outlier removal)
6. **Compute inner hull** Γ of S−V (final polyhedron)
7. **Compute centroid** (filled-solid method, equations 6-8)

### Limitations Acknowledged by Centore

1. Uncontrolled viewing illumination for CAUS naming
2. Fanciful/distinctive name bias (marketing names)
3. Fashion industry domain
4. Specialized color terminology
5. Unknown subject demographics
6. Possible sample fading
7. English language only

---

## Next Steps

1. **Track A Phase 0**: Parse Centore polyhedra, verify interpretation
2. **Track B Phase 1**: Build reference vocabulary with proper normalization
3. **Track B Phase 3**: Design calibration subset experiment
4. **Research**: Investigate illuminant hypothesis (literature review)
5. **Documentation**: Extract Centore's filtering criteria from paper

---

**Document Status**: Draft v2 - Incorporating user feedback
**Author**: Claude Code
**Date**: 2025-12-25
