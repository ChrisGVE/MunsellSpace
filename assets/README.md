# MunsellSpace Assets

This directory contains reference datasets used for color conversion and classification.

## Directory Structure

```
assets/
├── iscc-nbs/          # ISCC-NBS color classification data
├── xkcd/              # XKCD color survey data
├── centore/           # Centore semantic overlay reference
└── README.md          # This file
```

## Data Sources

### ISCC-NBS (`iscc-nbs/`)

The Inter-Society Color Council - National Bureau of Standards color naming system.

| File | Description |
|------|-------------|
| `ISCC-NBS-Colors.csv` | 267 color categories with representative Munsell values |
| `ISCC-NBS-Definitions.csv` | Color name definitions and boundaries |
| `ISCC-NBS-Definitions_Master.csv` | Extended definitions with polygon coordinates |

**Source:** Kelly, Kenneth L. & Judd, Deane B. (1976). *Color: Universal Language and Dictionary of Names*. NBS Special Publication 440.

**License:** Public domain (U.S. Government work)

### XKCD Color Survey (`xkcd/`)

Randall Munroe's 2010 web-based color naming survey with ~3.4 million responses.

| File | Description | Size | Included |
|------|-------------|------|----------|
| `xkcd_color_survey.txt` | 949 named colors with consensus hex values | 19 KB | Yes |
| `mainsurvey_sqldump.txt` | Full survey data (3.4M responses) | 295 MB | **No** |
| `satfaces_sqldump.txt` | Saturation perception experiment | 159 MB | **No** |
| `colorsurvey.tar.gz` | Original compressed archive | 84 MB | **No** |

**Source:** https://blog.xkcd.com/2010/05/03/color-survey-results/

**License:** CC0 Public Domain

**Downloading Large Files:**

The SQL dump files are too large for GitHub. To download them:

```bash
cd assets/xkcd/
curl -O https://xkcd.com/color/colorsurvey.tar.gz
tar -xzf colorsurvey.tar.gz
```

**Data Format (mainsurvey_sqldump.txt):**
```sql
INSERT INTO "answers" VALUES(id, user_id, datestamp, r, g, b, 'colorname');
```

### Centore Semantic Overlays (`centore/`)

Paul Centore's polyhedron definitions for 30 semantic color names, derived from CAUS fabric samples.

| File | Description |
|------|-------------|
| `DATA_SOURCE.md` | Documentation of the original data source |

**Note:** The actual polyhedron vertex/face data is compiled into the Rust source code at `src/constants/centore_polyhedra.rs`. The original data was extracted from `PolyhedronFiles.zip` distributed with Centore's 2020 paper.

**Source:** Centore, P. (2020). "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names". *Journal of the International Colour Association*, 25, 24-54.

**License:** Academic use permitted; see paper for terms.

## Usage in Code

These datasets are **not loaded at runtime**. They have been converted to static Rust constants:

- ISCC-NBS data → `src/constants/iscc_nbs_*.rs`
- Centore polyhedra → `src/constants/centore_polyhedra.rs`

The raw files are retained for:
- Reference and validation
- Regenerating constants if needed
- Research and analysis scripts

## Data Processing Scripts

Preprocessing scripts for these datasets are in `overlay-preprocessing/`:

- `a_priori_extraction.py` - Pattern-based color extraction
- `a_posteriori_extraction.py` - Data-driven word classification
- `ml_classification.py` - Machine learning classifier

See `overlay-preprocessing/METHODOLOGY.md` for methodology documentation.
