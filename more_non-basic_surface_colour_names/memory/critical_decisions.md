# Critical Decisions Log

This document records key technical and methodological decisions made during the semantic overlay investigation, with rationale for each.

---

## Decision 1: Fourier 4 Harmonics (Not 3 or 5)

### Context
Needed to model the systematic hue-dependent bias between Centore and XKCD color coordinates.

### Decision
Use 4-harmonic Fourier series for hue bias correction.

### Rationale

**Why not 3 harmonics:**
- Leave-one-out cross-validation showed higher error with 3 harmonics
- Missed important structure in the warm hue region
- Statistical tests showed significant improvement from 3 to 4

**Why not 5 harmonics:**
- Cross-validation error INCREASED with 5 harmonics (classic overfitting signal)
- 74% CV error increase compared to 4 harmonics
- Additional parameters did not capture real signal, just noise

**Why 4 harmonics is optimal:**
- Train-CV ratio = 1.47x (below 1.5x overfitting threshold)
- Each harmonic has physical interpretation:
  - k=1: Warm-cool asymmetry (largest amplitude)
  - k=2: Opposite quadrant effects
  - k=3: RGB primary spacing
  - k=4: Quadrant boundary refinement
- Bootstrap 95% CI for MAE: [4.7 deg, 9.6 deg]
- 20 residual degrees of freedom (adequate for 9 parameters)

### Supporting Evidence
- Model comparison in `extended_model_analysis_results.json`
- Hypothesis testing in appendix documentation
- SSE reduction: 93.9% compared to linear model

---

## Decision 2: Outlier-Robust Inner Convex Hull

### Context
Need to construct polyhedra from color samples that may contain outliers (especially XKCD crowd-sourced data).

### Decision
Use Centore's inner convex hull method: compute outer hull, discard boundary vertices, compute hull of remaining points.

### Rationale

**Why inner convex hull (not raw convex hull):**
- Outliers by definition lie on the boundary of the convex hull
- Single layer of vertex removal is mathematically principled
- Matches Centore's published methodology exactly

**Why single-layer peeling (not multi-layer):**
- Enables apples-to-apples comparison with Centore's polyhedra
- Centore's paper explicitly uses single layer (JAIC 2020, p. 33)
- Multi-layer would be more aggressive but less comparable

**Why not statistical outlier detection (IQR, z-score):**
- Convex hull method is distribution-free
- Works in 3D Cartesian space directly
- No assumptions about point distribution required

### Alternative Considered
Multi-layer peeling (Eddy 1982) - more aggressive outlier removal. Documented as Option B in methodology for future investigation, but not used for primary comparison.

### Reference
Centore (2020): "Any potential outlier is likely in the set V, so we will discard all points in V"

---

## Decision 3: Centore as Reference (Not XKCD)

### Context
When comparing color coordinates between datasets, needed to choose which dataset to treat as "ground truth".

### Decision
Treat Centore's spectrophotometer-measured coordinates as the reference standard.

### Rationale

**Measurement quality:**
- Centore: Spectrophotometer under controlled D65 illumination
- XKCD: Uncalibrated consumer monitors with unknown settings

**Calibration:**
- Centore: Known, repeatable measurement conditions
- XKCD: Each participant's monitor is different, gamma varies, ambient light unknown

**Noise levels:**
- Centore: Low noise, professional measurement
- XKCD: High noise, crowd-sourced perceptual responses

**Sample curation:**
- Centore: Expert-assigned color names from CAUS fabric samples
- XKCD: Freeform user input, includes typos, jokes, creative names

### Implication
The Fourier bias model corrects XKCD toward Centore, not vice versa. This assumes spectrophotometer measurement is closer to "true" Munsell coordinates.

### Caveat
Centore's data has its own biases (fashion industry terminology, English-only, unknown subject demographics). Documented in `POLYHEDRON_METHODOLOGY.md`.

---

## Decision 4: Entity Matching Methodology

### Context
Need to match color names between Centore (20 overlays) and XKCD (954 color names) for calibration.

### Decision
Use exact case-insensitive string matching for the 20 Centore overlay names.

### Rationale

**Why exact match (not fuzzy):**
- Centore's 20 names are well-defined, common English color terms
- All 20 have direct matches in XKCD data
- No ambiguity in matching

**Why case-insensitive:**
- XKCD data is lowercase
- Centore paper uses title case
- Semantic meaning is identical

**20 matched overlays:**
aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy, peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine

### Not Matched
Basic colors (red, blue, green, etc.) were included in convex hull analysis but excluded from bias correction since they have different semantic boundaries in each dataset.

---

## Decision 5: Hue as Primary Bias Dimension

### Context
Systematic differences between datasets could manifest in hue, value, chroma, or combinations.

### Decision
Model hue bias as primary, with constant offsets for value and chroma.

### Rationale

**Empirical observation:**
- Hue differences varied systematically by hue angle (periodic pattern)
- Value and chroma differences were relatively constant across hue

**Physical explanation:**
- Monitor colorimetry differs from spectrophotometer in hue rendering
- RGB primaries have fixed positions on monitors
- D65 simulation varies by monitor quality

**Model structure:**
- Hue: Fourier series (captures periodic variation)
- Value: Constant offset (+1.15)
- Chroma: Constant offset (+3.86)

### Supporting Evidence
- `hue_bias_analysis.json` - Per-overlay hue differences
- Residual analysis showed no remaining hue-dependent structure
- Value/chroma residuals showed no systematic pattern

---

## Decision 6: Leave-One-Out Cross-Validation

### Context
Need to validate model without overfitting, but only have 20 calibration points.

### Decision
Use leave-one-out cross-validation (LOOCV) for model selection.

### Rationale

**Small sample size:**
- Only 20 overlays shared between Centore and XKCD
- K-fold CV with K<20 would waste data
- LOOCV uses maximum training data per fold

**Unbiased estimate:**
- Each point serves as test set exactly once
- No data leakage between folds
- Provides per-overlay error estimates

**Alternative considered:**
Bootstrap validation - used for confidence intervals but not primary model selection

### Implementation
For each overlay i:
1. Fit model on remaining 19 overlays
2. Predict hue for overlay i
3. Record prediction error
4. Report mean absolute error across all 20 folds

---

## Decision 7: Coordinate System Alignment

### Context
Centore uses hue on 0-100 scale (100 = 360 degrees), library uses 0-40 scale (40 = 360 degrees).

### Decision
Convert all coordinates to consistent scale before analysis, store results in degrees for interpretability.

### Rationale

**Centore's formula** (JAIC 2020, p. 32):
- x = C * cos(H * pi/50)
- y = C * sin(H * pi/50)
- Where H is 0-100 scale

**Library convention**:
- Hue number 0-40 (40 steps = full circle)
- Each step = 9 degrees

**Conversion:**
- hue_degrees = hue_40 * 9
- hue_100 = hue_40 * 2.5

**Storage format:**
- Results files use degrees for human readability
- Fourier model operates in degrees (0-360 range)

---

## Summary Table

| Decision | Choice | Key Reason |
|----------|--------|------------|
| Fourier harmonics | 4 | CV error increases at 5, Train-CV ratio < 1.5 |
| Outlier method | Inner convex hull | Matches Centore, distribution-free |
| Reference dataset | Centore | Spectrophotometer > monitors |
| Entity matching | Exact, case-insensitive | 20 names unambiguous |
| Bias dimension | Hue primary | Periodic pattern observed |
| Cross-validation | Leave-one-out | Small sample (n=20) |
| Coordinates | Degrees | Interpretability |
