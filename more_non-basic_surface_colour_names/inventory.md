# Project Inventory: more_non-basic_surface_colour_names

This document provides a complete inventory of the `more_non-basic_surface_colour_names/` folder, which contains all research files related to extending Centore's paper "Beige, aqua, fuchsia, etc.: Definitions for some non-basic colour names."

**Last updated**: 2024-12-24
**Total files**: 150
**Total directories**: 19

---

## Folder Structure Overview

```
more_non-basic_surface_colour_names/
├── archives/              # Historical files being replaced
├── datasets/              # All color data sources
├── literature/            # Academic papers and references
├── memory/                # Claude context preservation
├── scripts/               # Active Python scripts (future consolidation)
├── writeups/              # Documentation and paper drafts
└── inventory.md           # This file
```

---

## 1. Archives (`archives/`)

Contains historical analysis files and original scripts, preserved for reference.

**Total files**: 57 (15 .md files + 42 scripts)

### 1.1 Analysis Documents (15 files)

| File | Original Location | Description |
|------|-------------------|-------------|
| `20250815-2247_CONVERSION_ANALYSIS_SUMMARY.md` | Root | Early RGB to Munsell conversion analysis |
| `20250815-2247_find_munsell_references.md` | Root | Reference finding for Munsell data |
| `20251223-1550_METHODOLOGY.md` | overlay-preprocessing/ | Overall methodology document |
| `20251223-1641_data_exploration.md` | investigation/ | Phase 1 data exploration |
| `20251223-1938_spelling_variants.md` | investigation/ | Phase 2.1 spelling variant analysis |
| `20251223-1946_typo_detection.md` | investigation/ | Phase 2.2 typo detection results |
| `20251223-1949_compound_normalization.md` | investigation/ | Phase 2.3 compound name handling |
| `20251223-1951_coordinate_analysis.md` | investigation/ | Phase 3 coordinate analysis |
| `20251223-1953_calibration_analysis.md` | investigation/ | Phase 4 Centore calibration |
| `20251223-1957_consolidation_strategy.md` | investigation/ | Phase 5 consolidation |
| `20251223-1958_synthesis_report.md` | investigation/ | Phase 6 synthesis |
| `20251223-2200_research_summary.md` | investigation/ | Overall research summary |
| `20251224-1404_DATA_PIPELINE_RATIONALE.md` | semantic-investigation/ | Pipeline rationale |
| `20251224-1812_SCRIPTS_INVENTORY.md` | overlay-preprocessing/ | Original scripts inventory |
| `20251224-2103_POLYHEDRON_METHODOLOGY.md` | semantic-investigation/ | Inner convex hull methodology |

### 1.2 Article Drafts (`archives/article_drafts/`, 13 files)

Research notes that became the foundation for the academic paper:

| File | Description |
|------|-------------|
| `20251224-1509_00_ARTICLE_STRUCTURE.md` | Paper outline |
| `20251224-1448_01_introduction.md` | Introduction draft |
| `20251224-1449_02_related_work.md` | Related work section |
| `20251224-1443_03_data_sources.md` | Data sources documentation |
| `20251224-1444_04_methodology.md` | Methodology section |
| `20251224-1440_05_failed_approaches.md` | What didn't work |
| `20251224-1445_06_results.md` | Results section |
| `20251224-1441_07_key_findings.md` | Key findings summary |
| `20251224-1446_08_discussion.md` | Discussion section |
| `20251224-1447_09_future_work.md` | Future work ideas |
| `20251224-1448_10_conclusion.md` | Conclusion draft |
| `20251224-1520_appendix_model_selection.md` | Model selection appendix |
| `20251224-1526_AIC_SUBMISSION_REQUIREMENTS.md` | Journal submission requirements |

### 1.3 Scripts Archive (`archives/scripts/`, 42 files)

Original Python scripts from overlay-preprocessing. See `archives/scripts/INVENTORY.md` for detailed descriptions.

**Categories**:
- **Core pipeline**: `a_priori_extraction.py`, `a_posteriori_extraction.py`, `ml_classification.py`, `generate_final_results.py`
- **Experiments 1-5**: `exp1_sbert_similarity.py`, `exp2_bert_tokens.py`, `exp3_autoencoder.py`, `exp4_hybrid.py`, `exp5_spelling_preprocess.py`
- **Investigation phases**: `phase1_data_inventory.py` through `phase6_synthesis.py`
- **Semantic analysis**: `full_scale_validation.py`, `centore_comparison.py`, `build_convex_hulls.py`
- **Bias correction**: `fit_fourier_correction.py`, `extended_model_analysis.py`, `visualize_hue_bias.py`
- **Vocabularies**: `collect_vocabularies.py`, `collect_color_name_com.py`
- **Utilities**: `common.py`, `run_experiments.py`, `analyze_results.py`

---

## 2. Datasets (`datasets/`)

All color data sources organized by origin.

**Total files**: 69 (60 Centore + 7 CSV + 1 README)

### 2.1 Centore Data (`datasets/centore/`)

#### PolyhedronFiles/ (30 files)
Complete polyhedron data for 30 color categories from Centore (2020).
Contains vertices, faces, and centroid data in Munsell space.

**Colors**: aqua, beige, blue, brown, coral, fuchsia, gold, gray, green, lavender, lilac, magenta, mauve, navy, orange, peach, pink, purple, red, rose, rust, sand, tan, taupe, teal, turquoise, violet, white, wine, yellow

**Format**: Text files with Munsell coordinates (Hue, Value, Chroma)

#### PolyhedronFilesJustNames/ (30 files)
Name-only versions of polyhedron files (without coordinate data).

**Source**: Centore, P. (2020) "Beige, aqua, fuchsia, etc." - JAIC Vol. 25, pp. 24-54

### 2.2 Collected Vocabularies (`datasets/collected/`, 7 files)

| File | Description | Records |
|------|-------------|---------|
| `centore_colors.csv` | 30 Centore color categories | 30 |
| `xkcd_colors.csv` | XKCD survey color names | 954 |
| `meodai_colors.csv` | Meodai color names collection | ~33,000 |
| `colorhexa_colors.csv` | ColorHexa web database | Variable |
| `color_name_com_colors.csv` | color-name.com user colors | Variable |
| `wikipedia_colors.csv` | Wikipedia list of colors | ~1,500 |
| `master_vocabulary.csv` | Merged reference vocabulary | ~35,000 |

### 2.3 XKCD Data (`datasets/xkcd/`)

**Status**: Placeholder for XKCD survey SQL dump
**Required file**: `mainsurvey_sqldump.txt` (~295 MB)
**Download**: https://xkcd.com/color/rgb.txt (954 most common) or full dump

---

## 3. Literature (`literature/`)

Academic papers and reference materials.

**Total files**: 3 (2 PDFs + 1 README)

| File | Citation | Description |
|------|----------|-------------|
| `jaic_v25_03.pdf` | Centore (2020) | Primary methodology paper |
| `convex-sets-and-their-applications.pdf` | Lay (2007) | Convex hull theory reference |
| `README.md` | - | Literature citations and licenses |

---

## 4. Memory (`memory/`)

Context preservation for Claude sessions.

**Total files**: 3

| File | Description |
|------|-------------|
| `README.md` | Instructions for context preservation |
| `20251224-2240_context_project-state.md` | Current project state snapshot |
| `critical_decisions.md` | 7 key decisions with rationale |

**Key decisions documented**:
1. SBERT vs BERT for semantic validation
2. 0.35 similarity threshold selection
3. Fourier 4 over higher-order models
4. Inner convex hull methodology
5. Circular statistics for hue
6. Leave-one-out cross-validation
7. Annotation vs filtering for consistency

---

## 5. Scripts (`scripts/`)

**Status**: Empty - reserved for future consolidated Python environment

**Planned contents**:
- Consolidated `pyproject.toml` with uv
- Merged scripts from `archives/scripts/`
- Single virtual environment

**Migration pending**: Scripts currently in `archives/scripts/` will be consolidated here with updated import paths.

---

## 6. Writeups (`writeups/`)

Documentation, references, and paper drafts.

**Total files**: 5

### 6.1 Methodology (`writeups/methodology/`, 1 file)

| File | Size | Description |
|------|------|-------------|
| `pipeline.md` | ~25 KB | Complete 7-phase data pipeline documentation |

**Contents**:
- Phase 1: Data Collection
- Phase 2: Entity Matching & Normalization
- Phase 3: Coordinate Analysis
- Phase 4: Calibration Analysis
- Phase 5: Consolidation Strategy
- Phase 6: Convex Hull Construction
- Phase 7: Bias Correction (Fourier Model)
- Algorithms, formulas, code examples
- References and appendices

### 6.2 References (`writeups/references/`, 2 files)

| File | Size | Description |
|------|------|-------------|
| `reference_collection.md` | ~15 KB | Comprehensive bibliography |
| `active_references.md` | ~10 KB | Only references actually used |

**Reference count**: 8 primary references actively cited

### 6.3 Results (`writeups/results/`, 1 file)

| File | Size | Description |
|------|------|-------------|
| `README.md` | ~13 KB | Index of all result files |

**Documented results** (in overlay-preprocessing/semantic-investigation/):
- Phase 2: `validated_color_names.json` (137,878 names)
- Phase 3: `munsell_conversions.json` (133,359 colors)
- Phase 4: `centore_comparison_results.json`, `hue_bias_analysis.json`
- Phase 6: `convex_hull_results.json` (30 polyhedra)
- Phase 7: `fourier_correction_model.json`

### 6.4 Research Notes (`writeups/research_notes/`)

**Status**: Empty - placeholder for dated research findings

**Naming convention**: `YYYYMMDD_HHMM_{name}.md`

### 6.5 Drafts (`writeups/drafts/`, 1 file)

| File | Size | Description |
|------|------|-------------|
| `README.md` | ~15 KB | Academic paper outline and planning |

**Contents**:
- Working title and alternatives
- Target venues (JAIC, Color Research & Application)
- Complete paper structure (6 sections)
- Planned figures and tables
- Writing guidelines

---

## File Statistics

### By Type

| Type | Count | Size |
|------|-------|------|
| Python scripts | 42 | ~250 KB |
| Markdown (.md) | 38 | ~180 KB |
| CSV data | 7 | ~5 MB |
| PDF documents | 2 | ~15 MB |
| Text data | 60 | ~500 KB |
| **Total** | **150** | **~21 MB** |

### By Directory

| Directory | Files | Subdirs | Description |
|-----------|-------|---------|-------------|
| `archives/` | 57 | 2 | Historical files |
| `datasets/` | 69 | 4 | Color data |
| `literature/` | 3 | 0 | Papers |
| `memory/` | 3 | 0 | Context |
| `scripts/` | 0 | 0 | Future consolidated scripts |
| `writeups/` | 5 | 5 | Documentation |
| **Total** | **150** | **19** | |

---

## Key Result Files (External)

Result files are stored in `overlay-preprocessing/semantic-investigation/` (not migrated to avoid duplication).

| File | Size | Description |
|------|------|-------------|
| `validated_color_names.json` | 25 MB | 137,878 validated XKCD names |
| `munsell_conversions.json` | 48 MB | 133,359 RGB→Munsell conversions |
| `centore_comparison_results.json` | 27 KB | 30 category bias analysis |
| `convex_hull_results.json` | 11 KB | 30 constructed polyhedra |
| `fourier_correction_model.json` | 3.4 KB | Fourier 4 correction coefficients |
| `hue_bias_analysis.png` | ~200 KB | Bias visualization |
| `correction_model_visualization.png` | ~180 KB | Fourier model plot |

**Total external results**: ~73 MB

---

## Quick Reference

### Finding Documentation
- **How does the pipeline work?** → `writeups/methodology/pipeline.md`
- **What references are used?** → `writeups/references/active_references.md`
- **Where are results?** → `writeups/results/README.md`
- **Paper outline?** → `writeups/drafts/README.md`

### Finding Data
- **Centore polyhedra?** → `datasets/centore/PolyhedronFiles/`
- **Color vocabularies?** → `datasets/collected/`
- **XKCD raw data?** → `datasets/xkcd/` (download required)

### Finding Scripts
- **Original scripts?** → `archives/scripts/`
- **Script descriptions?** → `archives/scripts/INVENTORY.md`

### Finding Context
- **Key decisions?** → `memory/critical_decisions.md`
- **Project state?** → `memory/20251224-2240_context_project-state.md`

---

## Maintenance

### Adding New Files
1. Follow naming conventions (YYYYMMDD-HHMM prefix for dated files)
2. Update this inventory
3. Add to appropriate subdirectory
4. Update `memory/` if significant decision

### Reorganization Rules
1. Never delete files without archiving first
2. Preserve original timestamps in filenames
3. Update cross-references in documentation
4. Test any script moves for import path issues

### Version Control
- This folder is NOT fully version-controlled (large result files)
- Scripts and documentation ARE version-controlled
- Use `.gitignore` for generated results

---

**Document version**: 1.0
**Created**: 2024-12-24
**Maintained by**: MunsellSpace Color Research Project
