# Dataset Sources

This directory contains datasets for color name research and analysis.

**Note:** Data files are NOT tracked in git. Download from sources below and place in appropriate folders.

---

## Directory Structure

```
datasets/
├── centore/              # Paul Centore's JAIC 2020 polyhedron data
│   ├── PolyhedronFiles/       # Full data with vertices and coordinates
│   └── PolyhedronFilesJustNames/  # Simplified version with names only
├── collected/            # Color vocabulary datasets from various sources
├── xkcd/                 # XKCD Color Survey raw data
└── SOURCES.md            # This file
```

---

## Centore Data (Essential Reference)

**Citation:**
Centore, P. (2020). Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names. *Journal of the International Colour Association*, 25, 24-54.

**Download URLs:**
- Paper: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf
- Polyhedron Data: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/PolyhedronFiles.zip
- Polyhedron Names Only: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/PolyhedronFilesJustNames.zip

**Setup:**
```bash
cd datasets/centore/
curl -O https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/PolyhedronFiles.zip
curl -O https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/PolyhedronFilesJustNames.zip
unzip PolyhedronFiles.zip
unzip PolyhedronFilesJustNames.zip
rm *.zip
```

**Format:** Text files containing convex hull polyhedra for 30 non-basic color terms in Munsell color space. Each file includes:
- Color name
- Number of CAUS samples (Color Association of the US)
- Centroid in Munsell and Cartesian coordinates
- Polyhedron vertices in Munsell coordinates

**Colors (30):** aqua, beige, blue, brown, coral, fuchsia, gold, gray, green, lavender, lilac, magenta, mauve, navy, orange, peach, pink, purple, red, rose, rust, sand, tan, taupe, teal, turquoise, violet, white, wine, yellow

**License:** Academic use; contact author for commercial licensing.

### PolyhedronFiles/
Full polyhedron data with Munsell vertex coordinates, centroids, and sample counts.

### PolyhedronFilesJustNames/
Simplified version containing vertex names without additional metadata.

---

## XKCD Color Survey (Primary Data Source)

**Citation:**
Munroe, R. (2010). Color Survey Results. *XKCD*. https://blog.xkcd.com/2010/05/03/color-survey-results/

**Download URL:**
https://xkcd.com/color/rgb.txt (summary)
Full data: Contact author or use archived version

**Description:**
Large-scale crowd-sourced color naming survey with ~3.4 million responses from ~222,500 participants naming RGB colors displayed on screen.

**Files:**

| File | Size | Tracked | Description |
|------|------|---------|-------------|
| `xkcd_color_survey.txt` | 19 KB | Yes | Summary of 949 most common color names with hex values |
| `mainsurvey_sqldump.txt` | 295 MB | No | Full survey responses (download separately) |
| `satfaces_sqldump.txt` | 159 MB | No | Saturation/faces data (download separately) |
| `colorsurvey.tar.gz` | 84 MB | No | Compressed archive of survey data |

**Key Statistics:**
- Total unique color names: 175,844
- Validated names (after semantic filtering): 137,878
- Survey responses: ~3.4 million

**License:** Data released by Randall Munroe; academic/research use permitted.

**Note:** Large files (SQL dumps) are excluded from git tracking. Download separately from the XKCD archives if needed.

---

## Collected Vocabularies (Scraped/Derived)

Color vocabulary datasets collected from various online sources for research purposes.

| File | Source | URL | Entries | License |
|------|--------|-----|---------|---------|
| `xkcd_colors.csv` | XKCD Color Survey | https://xkcd.com/color/rgb.txt | 949 | CC0 |
| `meodai_colors.csv` | Meodai Color Names | https://github.com/meodai/color-names | 31,852 | MIT |
| `colorhexa_colors.csv` | ColorHexa | https://www.colorhexa.com/ | 1,421 | Fair use |
| `wikipedia_colors.csv` | Wikipedia Color Lists | https://en.wikipedia.org/wiki/Lists_of_colors | 900 | CC BY-SA |
| `color_name_com_colors.csv` | ColorName.com | https://colorname.com/ | 1,313 | Fair use |
| `centore_colors.csv` | Derived from Centore JAIC 2020 | (see above) | 30 | Academic |
| `master_vocabulary.csv` | Consolidated from all sources | - | 33,208 | Mixed |

**Setup (direct downloads):**
```bash
cd datasets/collected/

# XKCD colors (direct download)
curl -o xkcd_colors.csv https://xkcd.com/color/rgb.txt

# Meodai colors (from GitHub)
curl -o meodai_colors.csv https://raw.githubusercontent.com/meodai/color-names/master/dist/colornames.csv
```

**Note:** ColorHexa, Wikipedia, and ColorName.com require web scraping. Use scripts in `../scripts/src/` to regenerate.

### CSV Format

Most collected datasets use the format:
```csv
name,coordinates
cloudy blue,#acc2d9
```

Where `coordinates` is typically a hex color value (`#RRGGBB`).

The `centore_colors.csv` uses Munsell notation:
```csv
name,coordinates
aqua,7.4BG 6.2/3.4
```

### master_vocabulary.csv

A consolidated vocabulary of unique color names from all sources. Contains only the `name` column (no coordinates) for vocabulary analysis purposes.

---

## Usage Notes

1. **Coordinate systems vary:** Centore data uses Munsell notation; collected data uses hex RGB.
2. **Duplicates exist:** The collected sources may contain overlapping color names.
3. **Quality varies:** XKCD data is crowd-sourced; Centore data is expert-curated.
4. **Case sensitivity:** Color names may have inconsistent capitalization across sources.
5. **Large files excluded:** XKCD SQL dumps (~450 MB total) are in `datasets/xkcd/` but not tracked in git.

---

## Related Files

- `../scripts/` - Analysis scripts using these datasets
- `../literature/SOURCES.md` - Literature references and academic papers

---

**Last updated:** 2025-12-25
