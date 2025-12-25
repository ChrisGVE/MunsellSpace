# Project Inventory: more_non-basic_surface_colour_names

This document provides a complete inventory of the `more_non-basic_surface_colour_names/` folder, which contains all research files related to extending Centore's paper "Beige, aqua, fuchsia, etc.: Definitions for some non-basic colour names."

**Last updated**: 2025-12-25
**Total files**: ~226
**Total directories**: ~25

---

## Folder Structure Overview

```
more_non-basic_surface_colour_names/
├── archives/              # Historical files and archived scripts
├── datasets/              # All color data sources (tracked)
├── literature/            # Academic papers (PDFs local only, not tracked)
├── memory/                # Claude context preservation
├── scripts/               # Active Python scripts (unified uv environment)
├── writeups/              # Documentation and paper drafts
└── inventory.md           # This file
```

---

## 1. Archives (`archives/`)

Contains historical analysis files and original scripts, preserved for reference.

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

Research notes that became the foundation for the academic paper.

### 1.3 Scripts Archive (`archives/scripts/`, ~42 files)

Original Python scripts from overlay-preprocessing. See `archives/scripts/INVENTORY.md` for detailed descriptions.

---

## 2. Datasets (`datasets/`)

All color data sources organized by origin. **Data files NOT tracked in git** - download from sources documented in `datasets/SOURCES.md`.

### 2.1 Centore Data (`datasets/centore/`, 60 files)

- `PolyhedronFiles/` - Full polyhedron data for 30 color categories
- `PolyhedronFilesJustNames/` - Simplified name-only versions

**Source:** Centore, P. (2020) "Beige, aqua, fuchsia, etc." - JAIC Vol. 25, pp. 24-54

### 2.2 Collected Vocabularies (`datasets/collected/`, 7 files)

| File | Source | Records |
|------|--------|---------|
| `centore_colors.csv` | 30 Centore color categories | 30 |
| `xkcd_colors.csv` | XKCD survey color names | 949 |
| `meodai_colors.csv` | Meodai color names collection | ~33,000 |
| `colorhexa_colors.csv` | ColorHexa web database | ~1,400 |
| `color_name_com_colors.csv` | color-name.com user colors | ~1,300 |
| `wikipedia_colors.csv` | Wikipedia list of colors | ~900 |
| `master_vocabulary.csv` | Merged reference vocabulary | ~33,000 |

### 2.3 XKCD Color Survey (`datasets/xkcd/`, 4 files)

| File | Size | Tracked | Description |
|------|------|---------|-------------|
| `xkcd_color_survey.txt` | 19 KB | Yes | Summary of 949 most common color names |
| `mainsurvey_sqldump.txt` | 295 MB | No | Full survey responses |
| `satfaces_sqldump.txt` | 159 MB | No | Saturation/faces data |
| `colorsurvey.tar.gz` | 84 MB | No | Compressed archive |

**Source:** Munroe, R. (2010). XKCD Color Survey. https://blog.xkcd.com/2010/05/03/color-survey-results/

### 2.4 Source Documentation

- `datasets/SOURCES.md` - Complete documentation with URLs and collection dates

---

## 3. Literature (`literature/`)

Academic papers and reference materials. **PDFs stored locally but NOT tracked in git.**

| File | Citation | Tracked |
|------|----------|---------|
| `jaic_v25_03.pdf` | Centore (2020) | No (.gitignore) |
| `convex-sets-and-their-applications.pdf` | Lay (2007) | No (.gitignore) |
| `SOURCES.md` | Citations with download URLs | Yes |

---

## 4. Memory (`memory/`)

Context preservation for Claude sessions.

| File | Description |
|------|-------------|
| `README.md` | Instructions for context preservation |
| `20251224-2240_context_project-state.md` | Project state snapshot |
| `20251225-0930_context_project-goals.md` | Project goals and constraints |
| `critical_decisions.md` | Key decisions with rationale |

---

## 5. Scripts (`scripts/`)

Consolidated Python environment with all analysis scripts.

```
scripts/
├── pyproject.toml       # Unified uv configuration
├── README.md            # Script documentation
└── src/
    ├── __init__.py
    ├── a_posteriori_extraction.py
    ├── a_priori_extraction.py
    ├── generate_final_results.py
    ├── ml_classification.py
    ├── excluded_colors.txt
    ├── investigation/   # Phase 1-6 investigation scripts
    └── semantic/        # Semantic analysis scripts
```

**Usage:**
```bash
cd more_non-basic_surface_colour_names/scripts
uv sync
uv run python src/semantic/centore_comparison.py
```

---

## 6. Writeups (`writeups/`)

Documentation, references, and paper drafts.

### 6.1 Methodology (`writeups/methodology/`)

| File | Description |
|------|-------------|
| `pipeline.md` | Complete 7-phase data pipeline documentation (~25 KB) |

### 6.2 References (`writeups/references/`)

| File | Description |
|------|-------------|
| `REFERENCES.md` | Original references file |
| `reference_collection.md` | Comprehensive bibliography |
| `active_references.md` | Only references actually used |

### 6.3 Results (`writeups/results/`)

| File | Description |
|------|-------------|
| `README.md` | Index of all result files |
| `data/` | Migrated result files (JSON, CSV) |

**Result files in `data/`:**
- Phase 2: `validated_color_names.json`, `color_wheel_consistency_results.json`
- Phase 3: Conversion results
- Phase 4: `calibration_analysis.json`, `centore_comparison_results.json`
- Phase 5: `consolidation_strategy.json`
- Phase 6: `convex_hull_results.json`
- Various experiment results

### 6.4 Drafts (`writeups/drafts/`)

| File | Description |
|------|-------------|
| `README.md` | Academic paper outline and planning |

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
- **XKCD raw data?** → `datasets/xkcd/`

### Finding Scripts
- **Active scripts?** → `scripts/src/`
- **Archived scripts?** → `archives/scripts/`

### Finding Context
- **Key decisions?** → `memory/critical_decisions.md`
- **Project goals?** → `memory/20251225-0930_context_project-goals.md`

---

## Migration Summary (2025-12-25)

The second cleanup pass completed the following:

1. **Literature**: PDFs kept locally but not tracked (via .gitignore)
2. **Datasets**: All tracked with SOURCES.md documentation
3. **Scripts**: Consolidated under unified uv environment in `scripts/`
4. **overlay-preprocessing/**: Completely removed
5. **Root duplicates**: Removed (PolyhedronFiles/, scripts/, literature/)
6. **tmp/**: Emptied (scratchpad ready for use)

All tracked files were migrated using `git mv` to preserve history.

---

**Document version**: 2.0
**Created**: 2024-12-24
**Updated**: 2025-12-25
**Maintained by**: MunsellSpace Color Research Project
