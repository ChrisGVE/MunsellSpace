# Dataset Sources

This directory contains datasets for color name research and analysis. All scraped/derived datasets are tracked in git with source documentation.

---

## Directory Structure

```
datasets/
├── centore/              # Paul Centore's JAIC 2020 polyhedron data
│   ├── PolyhedronFiles/       # Full data with vertices and coordinates
│   └── PolyhedronFilesJustNames/  # Simplified version with names only
├── collected/            # Color vocabulary datasets from various sources
└── SOURCES.md            # This file
```

**Note:** XKCD raw survey data (175,844 unique names, 3.4M responses) is stored separately in `assets/xkcd/` and is not duplicated here.

---

## Centore Data (Essential Reference)

**Citation:**
Centore, P. (2020). Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names. *Journal of the International Colour Association*, 25, 24-54.

**Download URL:**
https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf
(Supplementary materials available from same source)

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

## Collected Vocabularies (Scraped/Derived)

Color vocabulary datasets collected from various online sources for research purposes.

| File | Source | URL | Entries | Collected | License |
|------|--------|-----|---------|-----------|---------|
| `xkcd_colors.csv` | XKCD Color Survey | https://xkcd.com/color/rgb/ | 949 | 2024-12 | CC0 |
| `meodai_colors.csv` | Meodai Color Names | https://github.com/meodai/color-names | 31,852 | 2024-12 | MIT |
| `colorhexa_colors.csv` | ColorHexa | https://www.colorhexa.com/ | 1,421 | 2024-12 | Fair use |
| `wikipedia_colors.csv` | Wikipedia Color Lists | https://en.wikipedia.org/wiki/Lists_of_colors | 900 | 2024-12 | CC BY-SA |
| `color_name_com_colors.csv` | ColorName.com | https://colorname.com/ | 1,313 | 2024-12 | Fair use |
| `centore_colors.csv` | Derived from Centore JAIC 2020 | (see above) | 30 | 2024-12 | Academic |
| `master_vocabulary.csv` | Consolidated from all sources | - | 33,208 | 2024-12 | Mixed |

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
5. **XKCD full data:** The raw XKCD survey (~295 MB SQL dump) is in `assets/xkcd/` and not tracked in git.

---

## Related Files

- `assets/xkcd/` - Full XKCD color survey data (not tracked, download separately)
- `more_non-basic_surface_colour_names/scripts/` - Analysis scripts (TBD)
- `more_non-basic_surface_colour_names/literature/SOURCES.md` - Literature references

---

**Last updated:** 2025-12-25
