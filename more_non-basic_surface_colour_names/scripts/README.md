# Color Research Scripts

This directory contains Python scripts for color data preprocessing and analysis for the MunsellSpace research project.

## Setup

Use [uv](https://docs.astral.sh/uv/) to manage the Python environment:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
cd more_non-basic_surface_colour_names/scripts
uv sync

# Run a script
uv run python src/semantic/centore_comparison.py
```

## Directory Structure

```
scripts/
├── pyproject.toml       # Package configuration and dependencies
├── README.md            # This file
└── src/
    ├── __init__.py
    ├── a_posteriori_extraction.py    # A posteriori color extraction
    ├── a_priori_extraction.py        # A priori color extraction
    ├── generate_final_results.py     # Final result generation
    ├── ml_classification.py          # ML-based classification
    ├── excluded_colors.txt           # List of excluded color names
    ├── investigation/                # Phase 1-6 investigation scripts
    │   ├── __init__.py
    │   ├── phase1_data_inventory.py
    │   ├── phase2_1_spelling_variants.py
    │   ├── phase2_2_typo_detection.py
    │   ├── phase2_3_compound_normalization.py
    │   ├── phase3_coordinate_analysis.py
    │   ├── phase4_calibration_analysis.py
    │   ├── phase5_consolidation_strategy.py
    │   └── phase6_synthesis.py
    └── semantic/                     # Semantic analysis scripts
        ├── __init__.py
        ├── common.py                 # Shared utilities
        ├── centore_comparison.py     # Compare with Centore data
        ├── color_wheel_consistency.py
        ├── exp1_sbert_similarity.py  # SBERT similarity experiment
        ├── exp2_bert_tokens.py       # BERT tokenization experiment
        ├── exp3_autoencoder.py       # Autoencoder experiment
        ├── exp4_hybrid.py            # Hybrid approach experiment
        ├── exp5_spelling_preprocess.py
        ├── build_convex_hulls.py     # Convex hull construction
        ├── fit_fourier_correction.py # Fourier correction model
        ├── full_scale_validation.py  # Full validation
        └── ...
```

## Key Scripts

### Data Pipeline
- `common.py` - Shared utilities, data loading, coordinate caching
- `centore_comparison.py` - Compare XKCD data with Centore polyhedra
- `build_convex_hulls.py` - Construct convex hulls for color categories

### Experiments
- `exp1_sbert_similarity.py` - SBERT semantic similarity validation
- `exp2_bert_tokens.py` - BERT tokenization for spelling variants
- `exp3_autoencoder.py` - Character-level autoencoder for typos
- `exp4_hybrid.py` - Hybrid SBERT + autoencoder approach
- `exp5_spelling_preprocess.py` - Spelling preprocessing

### Bias Correction
- `fit_fourier_correction.py` - Fit Fourier hue correction model
- `hypothesis_tests.py` - Statistical hypothesis testing
- `model_analysis.py` - Model selection analysis

## Data Dependencies

Scripts expect data files in:
- `../datasets/collected/` - Color vocabulary CSVs
- `../datasets/centore/` - Centore polyhedron files
- `../../assets/xkcd/` - XKCD survey data (large, not tracked)

## Note

These scripts are research tools for developing new color overlays. The validated polyhedra will eventually be integrated into the MunsellSpace library.

---

**Last updated:** 2025-12-25
