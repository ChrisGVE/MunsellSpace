# Scripts Inventory

This document provides a comprehensive inventory of all Python scripts in the `overlay-preprocessing/` directory, organized by purpose and execution order.

## Environment Setup

All scripts should be run using the unified Python environment:

```bash
cd overlay-preprocessing
source .venv/bin/activate
```

The environment was created with:
- Python 3.11
- Key dependencies: numpy, scipy, scikit-learn, torch, transformers, sentence-transformers, matplotlib, seaborn, pandas

---

## Directory Structure

```
overlay-preprocessing/
├── color-vocabularies/     # Stage 1: Data collection
├── investigation/          # Stage 2: Data quality analysis
├── semantic-investigation/ # Stage 3-4: ML experiments & bias detection
├── results/                # Aggregated output files
└── *.py                    # High-level pipeline scripts
```

---

## Stage 1: Data Collection

**Location:** `color-vocabularies/`

| Script | Purpose | Output |
|--------|---------|--------|
| `collect_vocabularies.py` | Collects color names from multiple sources (XKCD, Meodai, Wikipedia, ColorHexa) | `*_colors.csv` files |
| `collect_color_name_com.py` | Scrapes additional color names from color-name.com | `color_name_com_colors.csv` |

**Output files:**
- `xkcd_colors.csv` - 954 XKCD survey colors
- `meodai_colors.csv` - Meodai color names dataset
- `wikipedia_colors.csv` - Wikipedia color names
- `colorhexa_colors.csv` - ColorHexa database
- `centore_colors.csv` - Centore's 20 reference overlay centroids
- `master_vocabulary.csv` - Consolidated vocabulary

---

## Stage 2: Data Quality Analysis

**Location:** `investigation/`

Scripts are numbered by execution order:

| Script | Purpose | Output |
|--------|---------|--------|
| `phase1_data_inventory.py` | Initial data audit and statistics | `data_inventory.json` |
| `phase2_1_spelling_variants.py` | Detect spelling variations (color/colour) | `spelling_variants.json` |
| `phase2_2_typo_detection.py` | Identify potential typos using edit distance | `typo_detection.json`, `typo_corrections.json` |
| `phase2_3_compound_normalization.py` | Normalize compound names (light-blue → light blue) | `compound_normalization.json` |
| `phase3_coordinate_analysis.py` | Analyze RGB coordinate distributions | `coordinate_analysis.json` |
| `phase4_calibration_analysis.py` | Cross-source calibration analysis | `calibration_analysis.json` |
| `phase5_consolidation_strategy.py` | Define consolidation rules | `consolidation_strategy.json` |
| `phase6_synthesis.py` | Final synthesis and recommendations | `synthesis_summary.json` |

---

## Stage 3: Semantic Analysis (ML Experiments)

**Location:** `semantic-investigation/`

### Utility Modules

| Script | Purpose |
|--------|---------|
| `common.py` | Shared utilities (file I/O, paths, XKCD data loading) |

### ML Experiments

| Script | Purpose | Model/Method | Output |
|--------|---------|--------------|--------|
| `exp1_sbert_similarity.py` | Semantic similarity using Sentence-BERT | `all-MiniLM-L6-v2` | `exp1_sbert_*.json` |
| `exp2_bert_tokens.py` | Token-level analysis using BERT | `bert-base-uncased` | `exp2_bert_*.json` |
| `exp3_autoencoder.py` | Custom autoencoder for color name embeddings | PyTorch autoencoder | `exp3_autoencoder_*.json`, `*.pt` |
| `exp4_hybrid.py` | Hybrid approach combining methods | Multiple | `exp4_hybrid_results.json` |
| `exp5_spelling_preprocess.py` | Spelling normalization preprocessing | Rule-based | `exp5_*.json` |
| `run_experiments.py` | Master script to run all experiments | - | - |
| `analyze_results.py` | Analyze and compare experiment results | - | - |

### Validation Pipeline

| Script | Purpose | Output |
|--------|---------|--------|
| `color_name_pipeline.py` | Complete pipeline: SBERT → validation → classification | Validated color names |
| `full_scale_validation.py` | Run pipeline on full dataset | `full_scale_validation_summary.json`, `validated_color_names.json` |
| `color_wheel_consistency.py` | Validate color names against color wheel position | `color_wheel_consistency_results.json` |
| `rgb_to_munsell_conversion.py` | Convert RGB to Munsell coordinates | `munsell_conversions.json` |

---

## Stage 4: Bias Detection & Correction

**Location:** `semantic-investigation/`

| Script | Purpose | Output |
|--------|---------|--------|
| `centore_comparison.py` | Compare XKCD centroids with Centore reference | `centore_comparison_results.json` |
| `distribution_comparison_methods.py` | **Four statistical methods for distribution comparison** | `distribution_comparison_results.json` |
| `correction_model.py` | Fourier harmonic model for hue correction | Screen correction parameters |
| `model_analysis.py` | Model selection and overfitting analysis | Model comparison metrics |
| `hypothesis_tests.py` | Statistical hypothesis tests for model validation | Test results |

### Distribution Comparison Methods (`distribution_comparison_methods.py`)

This is the key script implementing four approaches:

1. **Sliced Wasserstein Distance (with hue unfolding)**
   - Handles circular hue via point triplication at θ, θ-360°, θ+360°
   - Permutation test for p-values

2. **Circular Statistics (Watson's U²)**
   - von Mises-based analysis for hue dimension
   - Mann-Whitney U for value and chroma

3. **Procrustes Analysis**
   - Rigid transformation alignment
   - PROTEST permutation test

4. **GMM + KL Divergence**
   - Gaussian Mixture Model fitting
   - Bootstrap confidence intervals

---

## High-Level Pipeline Scripts

**Location:** Root of `overlay-preprocessing/`

| Script | Purpose |
|--------|---------|
| `a_priori_extraction.py` | Extract overlay names using predefined patterns |
| `a_posteriori_extraction.py` | Extract overlay names using ML predictions |
| `ml_classification.py` | Train ML classifier for color name categorization |
| `generate_final_results.py` | Generate final consolidated results |

---

## Execution Order for Full Pipeline

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Data collection (if needed)
python color-vocabularies/collect_vocabularies.py

# 3. Data investigation (run in order)
python investigation/phase1_data_inventory.py
python investigation/phase2_1_spelling_variants.py
# ... through phase6

# 4. Semantic experiments
python semantic-investigation/run_experiments.py

# 5. Validation pipeline
python semantic-investigation/full_scale_validation.py
python semantic-investigation/rgb_to_munsell_conversion.py

# 6. Bias detection
python semantic-investigation/centore_comparison.py
python semantic-investigation/distribution_comparison_methods.py
```

---

## Key Output Files

| File | Location | Description |
|------|----------|-------------|
| `validated_color_names.json` | `semantic-investigation/` | 137,878 validated color names with RGB |
| `munsell_conversions.json` | `semantic-investigation/` | 133,359 colors with Munsell coordinates |
| `centore_comparison_results.json` | `semantic-investigation/` | Per-overlay bias analysis (30 categories) |
| `distribution_comparison_results.json` | `semantic-investigation/` | Four-method statistical comparison |
| `master_vocabulary.csv` | `color-vocabularies/` | Consolidated color vocabulary |

---

## Dependencies

See `pyproject.toml` for full list. Key packages:
- **numpy** (1.26.4) - Numerical computing
- **scipy** (1.16.3) - Scientific computing (Procrustes, statistics)
- **scikit-learn** (1.8.0) - Machine learning (GMM, classifiers)
- **torch** (2.1.2) - Deep learning
- **transformers** (4.49.0) - BERT/Hugging Face models
- **sentence-transformers** (5.2.0) - SBERT embeddings
- **matplotlib** (3.10.8) - Visualization
- **seaborn** (0.13.2) - Statistical visualization
- **pandas** (2.3.3) - Data manipulation
