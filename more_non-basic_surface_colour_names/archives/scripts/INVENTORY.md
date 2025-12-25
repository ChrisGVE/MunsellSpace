# Scripts Archive Inventory

This directory contains archived copies of all scripts from the overlay-preprocessing pipeline.
These are reference copies preserved exactly as developed during the research phase.

## Script Summary

| Count | Category |
|-------|----------|
| 4 | Main Pipeline (overlay-preprocessing root) |
| 2 | Vocabulary Collection |
| 8 | Investigation Phases |
| 24 | Semantic Investigation |
| 3 | Root Scripts |
| **41** | **Total** |

---

## Main Pipeline Scripts

### From: overlay-preprocessing/

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `a_priori_extraction.py` | Pattern-based extraction of color words from XKCD data using predefined overlay patterns. High precision but introduces selection bias. | json, re |
| `a_posteriori_extraction.py` | Data-driven extraction of color words by tokenizing all names and classifying by hue variance. Unbiased discovery approach. | json, re, statistics |
| `ml_classification.py` | Random Forest classifier comparing statistical (hue variance) and ML methods for identifying color words. 83% cross-validation accuracy. | json, numpy, sklearn |
| `generate_final_results.py` | Creates final output files: overlay_colors_dataset.csv, overlay_centroids.json, combined_color_dictionary.json, iscc_nbs_contradictions.json. | json, math |

---

## Vocabulary Collection Scripts

### From: overlay-preprocessing/color-vocabularies/

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `collect_vocabularies.py` | Fetches color name data from multiple sources: Centore (20 colors), XKCD (865), meodai/color-names (30K+), Wikipedia, colorhexa.com. | csv, re, urllib |
| `collect_color_name_com.py` | Scrapes colors from color-name.com across 24 color family categories. | csv, re, urllib |

---

## Investigation Phase Scripts

### From: overlay-preprocessing/investigation/

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `phase1_data_inventory.py` | Data inventory and exploration. Analyzes unique color names in Centore and XKCD datasets, documents data quality observations. | json, re, collections |
| `phase2_1_spelling_variants.py` | Spelling variant detection using ensemble approach: rule-based, phonetic (Soundex), edit distance (Levenshtein), dictionary comparison. | json, re, difflib |
| `phase2_2_typo_detection.py` | Typo detection using frequency-based analysis. Low-frequency names similar to high-frequency names are flagged as likely typos. | json, re, difflib |
| `phase2_3_compound_normalization.py` | Compound name standardization: word order, hyphenation, modifier normalization (e.g., "very dark" vs "really dark"). | json, re, collections |
| `phase3_coordinate_analysis.py` | Pre-consolidation coordinate analysis. RGB statistics for XKCD, Munsell statistics for Centore. Identifies high-variance names. | json, math, statistics |
| `phase4_calibration_analysis.py` | Calibration analysis detecting systematic bias between Centore and XKCD data using shared overlay color names as reference points. | json, math, statistics |
| `phase5_consolidation_strategy.py` | Evaluates merging methods: simple mean, weighted mean, median, mode-based, source-prioritized. Measures accuracy impact. | json, math, statistics |
| `phase6_synthesis.py` | Synthesizes findings from Phases 1-5 into actionable recommendations for the color data consolidation pipeline. | json |

---

## Semantic Investigation Scripts

### From: overlay-preprocessing/semantic-investigation/

#### Core Utilities

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `common.py` | Common utilities for semantic experiments: data loading, preprocessing, constants (BASIC_COLORS, COLOR_MODIFIERS). | json, re |

#### ML Experiments (exp1-5)

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `exp1_sbert_similarity.py` | SBERT semantic similarity experiment. Embeds color names and measures similarity to known color vocabulary. | json, numpy, sentence-transformers, sklearn |
| `exp2_bert_tokens.py` | BERT tokenization analysis. Builds color token vocabulary and scores names by token overlap. | json, numpy, transformers |
| `exp3_autoencoder.py` | Semantic autoencoder experiment. Character-level seq2seq autoencoder trained on color vocabulary; high reconstruction loss indicates non-color terms. | json, numpy, torch |
| `exp4_hybrid.py` | Hybrid approach combining SBERT similarity and autoencoder reconstruction loss for improved filtering. | json, numpy, sklearn |
| `exp5_spelling_preprocess.py` | Spelling preprocessing variant. Strips special characters, normalizes whitespace, decodes hex colors before semantic analysis. | json, re, numpy, sentence-transformers |

#### Experiment Infrastructure

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `run_experiments.py` | Master experiment runner. Runs all experiments in sequence with options for small-scale testing or full-scale background execution. | subprocess |
| `analyze_results.py` | Analyzes experiment results against problematic cases, proposes optimal thresholds, builds recommended filtering pipeline. | json, re, numpy |

#### Pipeline and Validation

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `color_name_pipeline.py` | Robust color name processing pipeline. Two-tier validation: master vocabulary lookup (33K+ names) + SBERT semantic similarity for unknown names. | csv, json, re, numpy |
| `full_scale_validation.py` | Full-scale validation on all 175K XKCD names. Analyzes pass/fail rates, similarity score distribution, edge cases. | json, numpy, color_name_pipeline |

#### Color Science Analysis

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `color_wheel_consistency.py` | Color wheel consistency check. Verifies that color names semantically match their RGB coordinates (e.g., "blue" should have hue ~240). | csv, json, colorsys, numpy |
| `rgb_to_munsell_conversion.py` | RGB to Munsell conversion using MunsellSpace Rust library. Converts validated names from RGB to Munsell space via subprocess. | csv, json, subprocess, statistics |
| `centore_comparison.py` | Centore reference comparison. Compares XKCD-derived Munsell positions with Centore reference overlays to detect systematic biases. | json, re, math, statistics |
| `distribution_comparison_methods.py` | Statistical distribution comparison methods: Sliced Wasserstein Distance, Circular Statistics, Procrustes Analysis, GMM + KL Divergence. | json, numpy, scipy (optional) |

#### Correction Model Development

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `correction_model.py` | Correction model development for screen-to-physical color conversion. Models value bias (+0.81), chroma bias (+3.82), and non-uniform hue bias. | json, numpy, scipy (optional) |
| `fit_fourier_correction.py` | Fits Fourier harmonic model for hue correction using circular statistics results from distribution comparison. | json, numpy |
| `model_analysis.py` | Detailed model analysis with overfitting diagnostics and model selection rationale. | json, numpy |
| `extended_model_analysis.py` | Extended model selection criteria: AIC/BIC, nested F-tests, bootstrap coefficient stability, analysis of non-improving overlays. | json, numpy |
| `hypothesis_tests.py` | Hypothesis testing for model selection. Tests bias existence, non-uniformity, Fourier 4 vs simpler models, signal vs noise. Uses permutation tests and bootstrap methods. | json, numpy |
| `rigorous_validation.py` | Rigorous methodology validation: model selection, hypothesis testing, bootstrap confidence intervals, cross-validation. | json, numpy |

#### Geometry and Visualization

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `build_convex_hulls.py` | Builds convex hull polyhedra for color names following Centore's methodology. Outputs vertices, faces, and centroids. | json, numpy, scipy.spatial |
| `polyhedra_bias_analysis.py` | Polyhedra-based bias analysis comparing XKCD and Centore convex hull centroids for robust outlier-excluding comparison. | json, math, statistics |
| `visualize_correction_model.py` | Visualizes Fourier hue correction model: continuous curve, data points vs predictions, residuals analysis. | json, numpy, matplotlib |
| `visualize_hue_bias.py` | Visualizes hue-dependent bias pattern between Centore reference and XKCD screen data. | json, numpy, matplotlib |

---

## Root Scripts

### From: scripts/

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `extract_xkcd_colors.py` | Parses XKCD color survey SQL dump, extracts color name to RGB mappings, outputs aggregated statistics and candidate overlay colors. | json, re, statistics |
| `extract_color_words.py` | A posteriori color word extraction by tokenizing all names, aggregating colors, computing statistics to identify potential color terms. | json, re, statistics, math |
| `classify_color_words.py` | Compares statistical (hue variance threshold) and ML (Random Forest) methods for identifying color words. Training data: Centore overlays + ISCC-NBS terms. | json, numpy, sklearn |

---

## Execution Order (Recommended)

### Phase 1: Data Collection
1. `collect_vocabularies.py` - Gather reference vocabularies
2. `collect_color_name_com.py` - Additional vocabulary source
3. `extract_xkcd_colors.py` - Parse XKCD survey data

### Phase 2: Initial Analysis
4. `a_priori_extraction.py` - Pattern-based extraction (baseline)
5. `a_posteriori_extraction.py` - Data-driven extraction
6. `extract_color_words.py` - Word tokenization analysis

### Phase 3: Investigation Pipeline
7. `phase1_data_inventory.py`
8. `phase2_1_spelling_variants.py`
9. `phase2_2_typo_detection.py`
10. `phase2_3_compound_normalization.py`
11. `phase3_coordinate_analysis.py`
12. `phase4_calibration_analysis.py`
13. `phase5_consolidation_strategy.py`
14. `phase6_synthesis.py`

### Phase 4: Semantic Investigation
15. `run_experiments.py` - Runs exp1-5 in sequence
16. `analyze_results.py`
17. `color_name_pipeline.py`
18. `full_scale_validation.py`

### Phase 5: Color Science Analysis
19. `color_wheel_consistency.py`
20. `rgb_to_munsell_conversion.py`
21. `centore_comparison.py`
22. `distribution_comparison_methods.py`
23. `build_convex_hulls.py`
24. `polyhedra_bias_analysis.py`

### Phase 6: Model Development
25. `correction_model.py`
26. `fit_fourier_correction.py`
27. `model_analysis.py`
28. `extended_model_analysis.py`
29. `hypothesis_tests.py`
30. `rigorous_validation.py`

### Phase 7: Visualization
31. `visualize_correction_model.py`
32. `visualize_hue_bias.py`

### Phase 8: Classification Comparison
33. `ml_classification.py`
34. `classify_color_words.py`

### Phase 9: Final Output
35. `generate_final_results.py`

---

## Notes

- All scripts are Python 3.x compatible
- Heavy dependencies: numpy, scipy, sklearn, torch, sentence-transformers, matplotlib
- Scripts depend on data files in `assets/`, `overlay-preprocessing/results/`, and `overlay-preprocessing/investigation/`
- Some scripts cache intermediate results as JSON files
- The MunsellSpace Rust library is required for RGB to Munsell conversion
