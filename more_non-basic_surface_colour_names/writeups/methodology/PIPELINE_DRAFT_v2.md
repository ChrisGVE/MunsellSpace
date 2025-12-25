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

**Assessment**: The polyhedron files contain BOTH processed and raw data:
- **Processed**: Polyhedron vertices (inner hull) and faces
- **Raw**: All unique CAUS samples used for that category (with year, season, market, name, Munsell coordinates)

**Implication**: We CAN verify Centore's inner hull methodology by:
1. Starting from the raw samples in each file
2. Computing our own inner convex hull
3. Comparing our vertices to Centore's published vertices

### Centore's Data Cleanup (from JAIC 2020 paper, pp. 30-31)

Centore applied two filtering steps to the raw CAUS data:

#### Step 1: Fluorescent Sample Exclusion
- **Original dataset**: 18,706 lines in spreadsheet
- **Criterion**: Reflectance percentage >100% at one or more wavelengths
- **Excluded**: 2,245 fluorescent samples
- **Reason**: Fluorescent materials re-emit absorbed energy as visible light, making them unsuitable for standard Munsell conversion

#### Step 2: Implausible Name Exclusion
- **Criterion**: Color name that is "completely unsuitable" for the measured Munsell coordinates
- **Example given** (p. 31): "Futurist blue" with Munsell 7.97R 5.64/8.13 - a saturated red, dismissed as "clerical mishap"
- **Excluded**: ~60 samples
- **Final dataset**: ~16,400 non-fluorescent samples with plausible names

**Minimum sample requirement**: Every color name analyzed occurred in at least 25 unique, non-fluorescent samples.

### Raw CAUS Data Availability

**Status**: The full CAUS database (including excluded samples) is only accessible via paid subscription to the Color Association of the United States. We will not pursue this data source.

**What we have**: The polyhedron files contain all samples that passed Centore's filtering. This is sufficient for our Track A verification.

**What we don't have**: The 2,245 fluorescent samples and ~60 implausible name samples that were excluded.

**Historical reference** (for future researchers):
- **Hagley Museum and Library Archives**: https://findingaids.hagley.org/repositories/3/resources/939
  - Contains CAUS historical records (1915-2003)
  - Physical access only (Wilmington, Delaware)

---

## Data Sources

### Primary Sources

| Source | Type | Size | Use |
|--------|------|------|-----|
| Centore CAUS Polyhedra | Processed (inner hulls) | 30 colour names | Reference standard |
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
- Centore's polyhedron data files (30 colour names)

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
- Parsing code verified against 30 colour names
- Tolerance bounds established for centroid matching
- Understanding of what we CAN verify

**Decision Point**: If we cannot accurately parse the data, STOP and investigate format issues.

**Note**: Since we have processed data (not raw), this validates our **parsing** of Centore's results, not our ability to **replicate** his data cleanup.

### Track A Results (2025-12-25)

**Status**: COMPLETED SUCCESSFULLY

All 30 Centore polyhedra verified with comprehensive concordance testing.

**Terminology note**: Centore uses "colour name" (British spelling), not "category".

#### Method
1. Parsed all polyhedron files to extract samples
2. Converted Munsell → Cartesian using Centore's formula: `x = C×cos(H×π/50), y = C×sin(H×π/50), z = V`
3. Computed inner hull via single-layer peeling (scipy ConvexHull)
4. Computed filled-solid centroid via tetrahedron decomposition
5. Matched computed vertices to published vertices using Hungarian algorithm

#### Full Verification Table

| Colour Name | Centroid Err | V(ours) | V(Centore) | E(ours) | E(Centore) | F(ours) | F(Centore) | Mean V Err | Max V Err |
|-------------|--------------|---------|------------|---------|------------|---------|------------|------------|-----------|
| aqua        | 0.0023       | 28      | 28         | 78      | 78         | 52      | 52         | 0.0037     | 0.0058    |
| beige       | 0.0033       | 32      | 32         | 90      | 90         | 60      | 60         | 0.0041     | 0.0063    |
| blue        | 0.0052       | 66      | 66         | 192     | 192        | 128     | 128        | 0.0038     | 0.0067    |
| brown       | 0.0051       | 33      | 33         | 93      | 93         | 62      | 62         | 0.0039     | 0.0065    |
| coral       | 0.0062       | 34      | 34         | 96      | 96         | 64      | 64         | 0.0038     | 0.0063    |
| fuchsia     | 0.0049       | 18      | 18         | 48      | 48         | 32      | 32         | 0.0032     | 0.0066    |
| gold        | 0.0046       | 47      | 47         | 135     | 135        | 90      | 90         | 0.0035     | 0.0067    |
| gray        | 0.0038       | 39      | 39         | 111     | 111        | 74      | 74         | 0.0035     | 0.0062    |
| green       | 0.0067       | 66      | 66         | 192     | 192        | 128     | 128        | 0.0039     | 0.0065    |
| lavender    | 0.0047       | 15      | 15         | 39      | 39         | 26      | 26         | 0.0039     | 0.0062    |
| lilac       | 0.0011       | 20      | 20         | 54      | 54         | 36      | 36         | 0.0042     | 0.0064    |
| magenta     | 0.0046       | 7       | 7          | 15      | 15         | 10      | 10         | 0.0043     | 0.0060    |
| mauve       | 0.0064       | 44      | 44         | 126     | 126        | 84      | 84         | 0.0035     | 0.0054    |
| navy        | 0.0029       | 24      | 24         | 66      | 66         | 44      | 44         | 0.0040     | 0.0064    |
| orange      | 0.0050       | 46      | 46         | 132     | 132        | 88      | 88         | 0.0040     | 0.0066    |
| peach       | 0.0018       | 28      | 28         | 78      | 78         | 52      | 52         | 0.0041     | 0.0062    |
| pink        | 0.0035       | 55      | 55         | 159     | 159        | 106     | 106        | 0.0037     | 0.0068    |
| purple      | 0.0040       | 45      | 45         | 129     | 129        | 86      | 86         | 0.0037     | 0.0065    |
| red         | 0.0042       | 39      | 39         | 111     | 111        | 74      | 74         | 0.0038     | 0.0059    |
| rose        | 0.0051       | 51      | 51         | 147     | 147        | 98      | 98         | 0.0039     | 0.0061    |
| rust        | 0.0046       | 24      | 24         | 66      | 66         | 44      | 44         | 0.0039     | 0.0067    |
| sand        | 0.0054       | 24      | 24         | 66      | 66         | 44      | 44         | 0.0036     | 0.0055    |
| tan         | 0.0058       | 27      | 27         | 75      | 75         | 50      | 50         | 0.0035     | 0.0055    |
| taupe       | 0.0063       | 23      | 23         | 63      | 63         | 42      | 42         | 0.0038     | 0.0057    |
| teal        | 0.0053       | 15      | 15         | 39      | 39         | 26      | 26         | 0.0034     | 0.0055    |
| turquoise   | 0.0044       | 26      | 26         | 72      | 72         | 48      | 48         | 0.0042     | 0.0062    |
| violet      | 0.0026       | 31      | 31         | 87      | 87         | 58      | 58         | 0.0041     | 0.0066    |
| white       | 0.0034       | 24      | 24         | 66      | 66         | 44      | 44         | 0.0039     | 0.0069    |
| wine        | 0.0066       | 21      | 21         | 57      | 57         | 38      | 38         | 0.0037     | 0.0062    |
| yellow      | 0.0037       | 35      | 35         | 99      | 99         | 66      | 66         | 0.0043     | 0.0070    |
| **MEAN**    | **0.0045**   |         |            |         |            |         |            | **0.0038** | **0.0063**|
| **MAX**     | **0.0067**   |         |            |         |            |         |            | **0.0043** | **0.0070**|

#### Summary Statistics

| Metric | Value |
|--------|-------|
| Exact vertex count match | 30/30 (100%) |
| Vertex count discrepancy | None |
| Mean centroid error | 0.0045 Munsell units |
| Max centroid error | 0.0067 (green) |
| Mean vertex coordinate error | 0.0038 Munsell units |
| Max vertex coordinate error | 0.0070 Munsell units |

**Interpretation**: Perfect concordance achieved for all 30 colour names. All errors are below 0.01 Munsell units, representing sub-percentage agreement well within numerical precision bounds.

**Technical Note**: Initial verification showed a discrepancy for "white" (23 vs 24 vertices) caused by a parsing issue. The white polyhedron includes a neutral sample (N9.02 - "Purplish White") which uses the Munsell neutral notation `N{value}` rather than the chromatic pattern `{hue}{letter} {value}/{chroma}`. After adding neutral color parsing, all 30 colour names matched exactly.

**Verification scripts**:
- `scripts/src/track_a_verification.py` (centroid-only)
- `scripts/src/track_a_full_verification.py` (comprehensive)

**Detailed results**: `writeups/results/track_a_full_verification.json`

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

## Critical Insight: Screen vs Surface Colors (from Centore's paper, p. 28)

Centore explicitly addresses the screen-physical color problem:

> "The Munsell system applies only to surface colours, and not to coloured lights... it is not clear how to convert between RGBs and Munsell coordinates. This paper, however, relies only on spectrophotometrically measured surface colours."

**Implication for our work**: Centore's CAUS data consists of physical fabric samples measured with a spectrophotometer. Our XKCD data consists of screen colors (self-luminous RGB). Centore himself states the conversion between these domains is unclear without "additional analysis."

This validates our Track B approach: we must investigate the screen-physical relationship before proceeding with full conversion.

---

## Open Questions Requiring Further Research

### Illuminant and Perception

1. **Illuminant resolution**: Is there an illuminant under which LCD colors would match Centore's Munsell coordinates? Could chromatic adaptation (Bradford, CIECAM02) provide a principled correction?

2. **Perceptual validity**: When users name screen colors perceived as brighter/more saturated, is it correct to "correct" for this? Or does the perception itself matter?

### Methodological

3. **Quality criteria from literature**: What criteria exist in geometry/convex set literature for polyhedron quality? Locality, volume, stability?

### Resolved Questions (via paper extraction)

| Question | Resolution |
|----------|------------|
| Centore raw data access | Not feasible - CAUS requires paid subscription. Polyhedron files contain sufficient samples for verification. |
| Fluorescent exclusion criteria | Reflectance >100% at any wavelength (2,245 samples excluded) |
| Implausible name criteria | Color name "completely unsuitable" for measured coordinates (~60 samples excluded) |
| Minimum sample count | 25 unique, non-fluorescent samples per category |

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

## Appendix: Script Inventory

### Location

All scripts are in `scripts/src/`.

### Reusable Core Components

These functions from `track_a_full_verification.py` are validated against Centore's methodology and **safe for reuse** in Track C:

| Component | Function | Description |
|-----------|----------|-------------|
| `MunsellCoord` | dataclass | Munsell coordinate with chromatic and neutral support |
| `parse_munsell()` | function | Parse Munsell notation including neutral colors (N{value}) |
| `MunsellCoord.to_cartesian()` | method | Convert to Centore's Cartesian: x=C×cos(H×π/50), y=C×sin(H×π/50), z=V |
| `compute_inner_hull()` | function | Single-layer peeling algorithm (scipy ConvexHull) |
| `compute_filled_solid_centroid()` | function | Tetrahedron decomposition for filled-solid centroid |

**Important**: These functions have been validated against all 30 Centore polyhedra with 100% concordance. They implement the exact methodology from Centore (2020) JAIC paper.

### Track A Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `track_a_full_verification.py` | Comprehensive verification (V, E, F, coordinates, centroid) | ✅ Production |
| `track_a_verification.py` | Centroid-only verification (deprecated by full version) | ⚠️ Superseded |

### Diagnosis Scripts (One-Off)

| Script | Purpose | Status |
|--------|---------|--------|
| `diagnose_white.py` | Initial diagnosis of white vertex discrepancy | 📋 Investigation |
| `diagnose_white_detailed.py` | Deep analysis confirming neutral color parsing issue | 📋 Investigation |

These scripts documented the investigation process and are kept for reference only.

### Legacy Scripts (Pre-Track A)

These scripts exist from earlier work and have **not been validated** against Centore's methodology:

| Script | Purpose | Status |
|--------|---------|--------|
| `a_priori_extraction.py` | Pattern matching for color words | ⚠️ Unvalidated |
| `a_posteriori_extraction.py` | Hue variance analysis | ⚠️ Unvalidated |
| `ml_classification.py` | Random Forest classification | ⚠️ Unvalidated |
| `generate_final_results.py` | Results generation | ⚠️ Unvalidated |

**Warning**: Do not use legacy scripts without first validating their methodology against Track A results.

### Recommended Refactoring for Track C

Before proceeding to Track C, consider extracting the reusable core components into a shared module:

```
scripts/src/
├── core/
│   ├── __init__.py
│   ├── munsell.py          # MunsellCoord, parse_munsell()
│   ├── geometry.py         # compute_inner_hull(), compute_filled_solid_centroid()
│   └── centore_parser.py   # parse_polyhedron_file()
├── track_a/
│   └── verification.py     # Track A specific code
└── track_c/
    └── (future extension scripts)
```

---

## Next Steps

1. ~~**Track A Phase 0**: Parse Centore polyhedra, verify interpretation~~ ✅ COMPLETED
2. **Track B Phase 1**: Build reference vocabulary with proper normalization
3. **Track B Phase 2**: XKCD semantic validation
4. **Track B Phase 3**: Design calibration subset experiment
5. **Research**: Investigate illuminant hypothesis (literature review)

---

**Document Status**: Draft v2.2 - Track A complete with 100% verification
**Author**: Claude Code
**Date**: 2025-12-25
