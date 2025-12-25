# Academic Paper Drafts

This directory is reserved for academic paper drafts based on the color research project.

---

## Potential Paper: Screen Colors to Physical Color Space

### Working Title

**"Bridging Screen and Physical Color Perception: Systematic Bias Detection Between Crowdsourced RGB and Spectrophotometer-Measured Munsell Colors"**

Alternative titles:
- "From Screens to Surfaces: Mapping Crowdsourced Color Names to Physical Munsell Space"
- "Systematic Biases in Screen Color Perception: A Data-Driven Analysis"
- "Correcting Screen-to-Physical Color Bias for Semantic Color Overlays"

---

## Target Venues

### Primary Targets

**Journal of the International Colour Association (JAIC)**
- Centore (2020) published here (same methodology lineage)
- Open access, peer-reviewed
- Audience: Color scientists, researchers
- Impact: Moderate (specialized field)

**Color Research & Application**
- Wiley journal, peer-reviewed
- Broader color science audience
- Impact factor: ~1.5
- Publishes methodology and application papers

**ACM Transactions on Graphics (TOG)**
- If emphasizing computational aspects
- High impact (IF ~6.5)
- Requires strong graphics/visualization component

### Secondary Targets

**Vision Research**
- If emphasizing perception aspects
- High impact (IF ~2.5)
- Requires strong psychophysical component

**PLoS ONE**
- Open access, broad audience
- Accepts computational/data science papers
- Moderate impact (IF ~3.2)

**arXiv Preprint** (initial)
- Post preprint before submission
- Category: cs.CV (Computer Vision) or cs.HC (Human-Computer Interaction)
- Get early feedback

---

## Paper Structure Outline

### Abstract (250 words)

**Problem**: Mapping crowdsourced screen color names to physical Munsell space is challenging due to systematic biases between screen and physical color perception.

**Approach**: We present a 7-phase data pipeline that processes 175,844 crowdsourced RGB color names (XKCD survey), validates them semantically, converts to Munsell space, and detects biases against spectrophotometer-measured reference data (Centore 2020).

**Key Finding**: Screen colors exhibit systematic biases: +0.81 in value (appear lighter), +3.82 in chroma (appear more saturated), and non-uniform hue bias (cool colors shift ~40° toward blue, warm colors shift ~30° toward yellow).

**Contribution**: We develop a Fourier 4-harmonic correction model that reduces hue error from 11.2° to 7.2° (35% improvement) and demonstrate that linear correction is insufficient for opposite-direction hue biases.

**Implications**: Our pipeline and correction model enable accurate semantic color overlays for color naming systems, bridging the gap between screen-based crowdsourcing and physical color measurement.

---

### 1. Introduction (2 pages)

**Section 1.1: Motivation**
- Color naming is fundamental to human communication about color
- Two paradigms: expert-measured (Munsell, ISCC-NBS) vs. crowdsourced (XKCD)
- Challenge: Screen colors (RGB, self-luminous) ≠ physical colors (reflective, D65)

**Section 1.2: Problem Statement**
- Goal: Create semantic color overlays in Munsell space using crowdsourced data
- Obstacles:
  - Semantic noise (gibberish, sentences, brand names)
  - Coordinate bias (screen vs. physical perception)
  - Outlier handling (crowd data is noisy)

**Section 1.3: Research Questions**
1. Can crowdsourced screen color names be validated semantically?
2. What systematic biases exist between screen and physical color perception?
3. Is linear correction sufficient, or do we need non-linear models?
4. How can we construct outlier-robust semantic color regions?

**Section 1.4: Contributions**
- 7-phase data pipeline for screen-to-physical color mapping
- Quantification of systematic biases (value, chroma, hue)
- Non-uniform hue bias model (Fourier 4 harmonics)
- Validation against Centore (2020) reference dataset

**Section 1.5: Paper Organization**
- Section 2: Related work
- Section 3: Methodology (7-phase pipeline)
- Section 4: Results
- Section 5: Discussion
- Section 6: Conclusion and future work

---

### 2. Related Work (3 pages)

**Section 2.1: Color Naming Studies**
- Berlin & Kay (1969): Universal basic color terms
- XKCD survey (Munroe 2010): Crowdsourced color naming
- Monroe et al. (2016): Lab vs. online color naming
- Key insight: Crowdsourced data is viable but noisy

**Section 2.2: Color Space Conversions**
- ASTM D1535: Munsell standard
- ITU-R BT.709: sRGB standard
- Centore methodology: RGB to Munsell mathematical conversion
- Challenge: Screen RGB ≠ physical reflectance

**Section 2.3: Semantic Similarity**
- Word embeddings (Word2Vec, GloVe)
- Sentence embeddings (SBERT, Sentence-BERT)
- Application: Filtering crowdsourced text for semantic validity
- Reimers & Gurevych (2019): SBERT for similarity

**Section 2.4: Convex Hull Methods**
- Lay (2007): Convex sets and minimal generating sets
- Centore (2020): Inner convex hull for outlier removal
- Eddy (1982): Convex hull peeling
- Application: Define color regions robustly

**Section 2.5: Color Perception Bias**
- Monitor calibration effects
- Surround effects (dark room vs. ambient light)
- Adaptation effects
- Existing work: Limited quantification of screen-to-physical bias

**Section 2.6: Gap in Literature**
- No prior work systematically quantifies screen-to-physical color bias
- No prior work applies non-linear correction to crowdsourced color data
- Our contribution: Data-driven bias detection and correction

---

### 3. Methodology (6 pages)

**Section 3.1: Overview**
- 7-phase pipeline diagram
- Data flow: 175,844 names → 137,878 validated → 133,359 converted → 101,894 matched

**Section 3.2: Phase 1 - Data Collection**
- XKCD dataset: 3.4M responses, 175,844 unique names
- Centore dataset: 9,261 CAUS samples, 30 categories
- Data characteristics and limitations

**Section 3.3: Phase 2 - Entity Matching & Normalization**
- Semantic validation with SBERT (threshold 0.35)
- Spelling variant detection (Levenshtein distance)
- Typo correction
- Results: 78.4% validation rate

**Section 3.4: Phase 3 - Coordinate Analysis**
- RGB averaging for multi-response colors
- Color wheel consistency check (annotation only)
- RGB to Munsell conversion (ASTM D1535)
- Results: 96.7% conversion success

**Section 3.5: Phase 4 - Calibration Analysis**
- Category matching (substring matching)
- Centore centroid calculation (circular mean for hue)
- Bias computation (circular difference for hue)
- Results: Value +0.81, Chroma +3.82, Hue non-uniform

**Section 3.6: Phase 6 - Convex Hull Construction**
- Centore inner hull algorithm
- Outlier removal (single-layer vertex removal)
- Degenerate case handling
- Results: 30 polyhedra constructed

**Section 3.7: Phase 7 - Bias Correction**
- Model selection (linear, piecewise, Fourier, spline)
- Cross-validation (leave-one-out)
- Fourier 4 harmonics: optimal complexity
- Results: 35% improvement in hue error

---

### 4. Results (4 pages)

**Section 4.1: Semantic Validation Results**
- 137,878 / 175,844 names validated (78.4%)
- Top rejected categories: gibberish, sentences, brands
- Validation examples (validated vs. rejected)

**Section 4.2: Conversion Results**
- 133,359 / 137,878 colors converted (96.7%)
- Out-of-gamut failures: 4,519 (3.3%)
- Conversion accuracy (spot checks)

**Section 4.3: Bias Detection Results**
- Universal biases: Table of value, chroma, hue
- Category-specific hue biases: Figure (scatter plot)
- Non-uniformity: Cool colors shift blue, warm shift yellow

**Section 4.4: Correction Model Performance**
- Model comparison table (linear, piecewise, Fourier 1-6)
- Cross-validation results
- Fourier 4 selection rationale

**Section 4.5: Hypothesis Testing**
- 6 hypothesis tests (Table)
- Interpretation: Non-uniform bias confirmed, model captures real signal

**Section 4.6: Visualizations**
- Figure 1: Pipeline architecture diagram
- Figure 2: Hue bias scatter plot (category vs. bias)
- Figure 3: Fourier 4 model curve with data points
- Figure 4: Before/after correction comparison

---

### 5. Discussion (3 pages)

**Section 5.1: Why Linear Correction Fails**
- Opposite-direction biases (cool vs. warm colors)
- Physical explanation: Monitor gamma, surround effects, adaptation

**Section 5.2: Fourier Model Interpretation**
- Harmonic 1: Warm-cool asymmetry
- Harmonic 2: Opposite quadrant effects (180°)
- Harmonic 3: RGB primary spacing (120°)
- Harmonic 4: Quadrant boundaries (90°)

**Section 5.3: Physical Explanations**
- Screen self-luminance vs. reflective surfaces
- Monitor calibration variability
- Surround and adaptation effects
- Metamerism (screen matches ≠ physical matches)

**Section 5.4: Limitations**
- First-order approximation
- Category matching (substring only)
- Sample size variation (some categories n < 200)
- Convex hull approximation (simple centroid)

**Section 5.5: Implications for Color Systems**
- Semantic overlays: Need correction for screen data
- ISCC-NBS alternative: Crowdsourced + corrected
- Color naming applications: Games, design tools, accessibility

**Section 5.6: Generalizability**
- Other crowdsourced datasets (e.g., OSF color survey)
- Other color spaces (CIELAB, CIECAM02)
- Other languages (multilingual color naming)

---

### 6. Conclusion and Future Work (2 pages)

**Section 6.1: Summary of Contributions**
- 7-phase pipeline for screen-to-physical color mapping
- Quantification of systematic biases
- Fourier 4 correction model (35% improvement)
- Open-source implementation

**Section 6.2: Key Findings**
1. Crowdsourced color data is viable with semantic validation
2. Screen colors are systematically lighter (+0.81) and more saturated (+3.82)
3. Hue bias is non-uniform (requires non-linear correction)
4. Fourier 4 harmonics provide optimal bias correction

**Section 6.3: Future Work**
- Perceptual color spaces (CIELAB, CIEDE2000)
- Category-specific corrections
- Uncertainty quantification (bootstrap CIs)
- Independent validation dataset
- Multidimensional correction (joint hue-value-chroma)
- Multilingual color naming
- User study: Validate corrected overlays with human subjects

**Section 6.4: Open Science**
- Code: GitHub repository
- Data: XKCD (public), Centore (supplementary materials)
- Results: JSON files available
- Reproducibility: Full pipeline documented

---

## Supplementary Materials

### Appendix A: Data Pipeline Details
- Complete algorithm pseudocode
- Circular statistics formulas
- Munsell distance metric

### Appendix B: Model Selection
- Full model comparison table (12 models)
- Cross-validation details
- Bootstrap confidence intervals

### Appendix C: Hypothesis Testing
- 6 hypothesis tests (detailed methodology)
- Permutation test implementations
- Statistical significance interpretation

### Appendix D: Category-Level Results
- Table: All 30 categories with n, biases, CIs
- Per-category scatter plots (optional)

### Appendix E: Code Availability
- GitHub repository URL
- Installation instructions
- Reproduction instructions

---

## Figures (Planned)

**Figure 1**: Pipeline architecture diagram
- 7 phases with data flow
- Sample sizes at each stage
- Key algorithms highlighted

**Figure 2**: Hue bias scatter plot
- X-axis: Category hue position (0-360°)
- Y-axis: Hue bias (degrees)
- Points sized by sample count
- Color-coded by bias direction

**Figure 3**: Fourier 4 model visualization
- X-axis: Hue (0-360°)
- Y-axis: Hue correction (degrees)
- Solid line: Fourier 4 model
- Scatter: Actual category biases
- Shaded: ±1 SD envelope

**Figure 4**: Before/after correction
- Side-by-side comparison
- Example categories (teal, beige)
- Show error reduction

**Figure 5**: Convex hull example
- 3D Munsell space (x, y, z)
- Outer hull (dashed)
- Inner hull (solid)
- Centroid (marked)

**Figure 6**: Model selection curve
- X-axis: Model complexity (parameters)
- Y-axis: Cross-validation error
- Show elbow at Fourier 4

---

## Tables (Planned)

**Table 1**: Dataset statistics
- XKCD: 175,844 names, 3.4M responses
- Centore: 9,261 samples, 30 categories
- Validation: 137,878 (78.4%)
- Conversion: 133,359 (96.7%)

**Table 2**: Global bias statistics
- Value: +0.81 ± 0.92
- Chroma: +3.82 ± 2.14
- Hue: -2.71° ± 35.94°

**Table 3**: Category-specific hue biases (selected)
- Top 5 cool (negative bias)
- Top 5 warm (positive bias)
- Neutral (near-zero bias)

**Table 4**: Model comparison
- Linear, piecewise (4/6/12), Fourier (1-6)
- Train MAE, CV MAE, CV ratio
- Parameters, residual DoF

**Table 5**: Hypothesis test results
- 6 tests with null hypothesis, statistic, p-value, decision

---

## Writing Guidelines

### Target Length
- Conference paper: 8-10 pages (e.g., ACM CHI, SIGGRAPH)
- Journal paper: 15-20 pages (e.g., JAIC, Color Research & Application)

### Style
- Active voice preferred
- Past tense for methodology
- Present tense for results/implications
- First person plural ("we") acceptable

### Technical Level
- Assume color science background
- Define specialized terms (circular statistics, convex hull)
- Equations in mathematical notation
- Code listings minimal (pseudocode in appendix)

### Citation Style
- APA or numbered (venue-dependent)
- Centore (2020) cited prominently
- XKCD dataset credited properly
- All dependencies cited (SBERT, scipy, etc.)

---

## Draft Status

**Current status**: Outline only (this README)

**Next steps**:
1. Write Introduction draft
2. Write Methodology draft (draw from `pipeline.md`)
3. Generate figures (run visualization scripts)
4. Compile results tables
5. Write Discussion and Conclusion
6. Compile supplementary materials
7. Internal review
8. Submit to preprint (arXiv)
9. Submit to journal

**Estimated timeline**:
- Draft 1: 2-3 weeks
- Internal review: 1 week
- Revision: 1 week
- Submission: Month 2

---

## Resources for Writing

### Documentation Sources
- `/writeups/methodology/pipeline.md` - Complete methodology
- `/writeups/references/active_references.md` - All citations
- `/writeups/results/README.md` - All result files
- `overlay-preprocessing/research_notes/` - Section drafts

### Existing Draft Sections (research_notes/)
- `00_ARTICLE_STRUCTURE.md` - Article outline
- `01_introduction.md` - Introduction draft
- `02_related_work.md` - Related work draft
- `03_data_sources.md` - Data sources section
- `04_methodology.md` - Methodology draft
- `05_failed_approaches.md` - What didn't work
- `06_results.md` - Results draft
- `07_key_findings.md` - Key findings
- `08_discussion.md` - Discussion draft
- `09_future_work.md` - Future work
- `10_conclusion.md` - Conclusion draft
- `appendix_model_selection.md` - Model selection appendix

**Note**: These drafts can be compiled and refined into the final paper.

---

## Collaboration

**Primary author**: MunsellSpace Research Team

**Potential co-authors**:
- Methodology contributors
- Code contributors
- Dataset curators (Munroe for XKCD, Centore for reference data)

**Acknowledgments**:
- XKCD community for crowdsourced data
- Centore for reference methodology and data
- Open-source library maintainers (SBERT, scipy, etc.)

---

## License for Drafts

**Draft license**: All rights reserved (until publication)

**Post-publication**:
- If open access: CC BY 4.0
- If paywalled: Copyright transferred to publisher (retain preprint rights)

---

**Document version**: 1.0 (outline only)
**Last updated**: 2024-12-24
**Status**: Planning stage, no draft written yet
**Maintained by**: MunsellSpace Color Research Project
