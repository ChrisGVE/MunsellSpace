# Phase 1: Data Exploration Report

## 1. Executive Summary

This report documents the initial exploration of color naming data from the XKCD color survey.

### Key Findings

| Metric | Value |
|--------|-------|
| Total unique color names | 23,598 |
| Total survey responses | 3,227,010 |
| Single-word names | 7,031 (29.8%) |
| Multi-word names | 16,567 (70.2%) |
| Names with hyphens | 1,782 |
| Names with digits | 245 |

## 2. Dataset Overview

### 2.1 XKCD Color Survey

The XKCD color survey collected ~3.4 million color naming responses from internet users in 2010.
Each response consists of an RGB color value and a user-provided color name.

**Data Source**: `assets/xkcd/mainsurvey_sqldump.txt`

**Response Distribution**:

| Response Count | Number of Names | Interpretation |
|----------------|-----------------|----------------|
| 1 | 0 | Unique/rare names |
| 2-10 | 16,467 | Uncommon names |
| 11-100 | 5,794 | Moderately common |
| 101-1000 | 1,095 | Common names |
| 1001-10000 | 195 | Very common names |
| 10001+ | 47 | Highly popular names |

### 2.2 Centore Dataset

The Centore dataset consists of ~16,000 CAUS (Color Association of the United States) fabric samples
measured with spectrophotometers. We have access to:

- 20 semantic overlay color names (aqua, beige, coral, etc.)
- 11 basic ISCC-NBS color names

**Note**: Individual CAUS sample names are not directly available in our dataset.
The polyhedron data represents aggregate boundaries, not individual samples.

## 3. Name Characteristics Analysis

### 3.1 Name Length Distribution

| Metric | Characters | Words |
|--------|------------|-------|
| Minimum | 1 | 1 |
| Maximum | 47 | 10 |
| Mean | 11.6 | 2.0 |
| Median | 11 | 2 |

### 3.2 Name Structure Categories

| Category | Count | Percentage |
|----------|-------|------------|
| two_word | 11,850 | 50.2% |
| single_word | 7,031 | 29.8% |
| three_word | 3,937 | 16.7% |
| phrase | 780 | 3.3% |

### 3.3 Top 20 Words (Weighted by Response Count)

| Rank | Word | Weighted Frequency |
|------|------|-------------------|
| 1 | green | 705,139 |
| 2 | blue | 593,832 |
| 3 | purple | 370,207 |
| 4 | light | 218,443 |
| 5 | pink | 209,773 |
| 6 | dark | 147,887 |
| 7 | brown | 126,987 |
| 8 | red | 121,277 |
| 9 | gray | 120,633 |
| 10 | yellow | 98,419 |
| 11 | orange | 91,880 |
| 12 | teal | 72,027 |
| 13 | bright | 51,279 |
| 14 | magenta | 49,657 |
| 15 | lime | 48,726 |
| 16 | violet | 45,546 |
| 17 | pale | 44,489 |
| 18 | sky | 40,421 |
| 19 | olive | 38,926 |
| 20 | turquoise | 32,546 |

## 4. Data Quality Observations

### 4.1 Potential Issues Identified

#### Very Long Names (>30 characters)

These may be sentences, descriptions, or data entry errors:

| Name | Length | Count |
|------|--------|-------|
| i dont think this survey ever ends | 34 | 71 |
| all work and no play makes jack a dull b... | 42 | 32 |
| light blue with a hint of green | 31 | 24 |
| light green with a hint of blue | 31 | 16 |
| what would you call this color? | 31 | 14 |
| i said i am done being the guinea pig | 37 | 11 |
| i see everything mmmmmmmmmmmmmmmmmmmm | 37 | 9 |
| somewhere between blue and purple | 33 | 7 |
| ass colorass colorass colorass color | 36 | 7 |
| a hooker cause it needs to get laaaaaaid | 40 | 6 |

#### Names Containing Numbers

May indicate specific color codes or measurement artifacts:

| Name | Count |
|------|-------|
| 1 | 815 |
| 2 | 191 |
| 5 | 122 |
| over 9000 | 111 |
| 4 | 106 |
| 3 | 105 |
| 42 | 97 |
| 6 | 74 |
| 7 | 71 |
| 1st april, huh? | 70 |

### 4.2 Spelling Variants Detected

#### Gray vs Grey

Found 1,291 names containing either "gray" or "grey".

#### Known Misspelling Patterns


**fuchsia** - Found 91 variant(s):
- `fuschia` (13154 responses)
- `fushia` (2697 responses)
- `fuchia` (475 responses)
- `fusia` (471 responses)
- `dark fuschia` (341 responses)

**turquoise** - Found 214 variant(s):
- `turquoise` (26313 responses)
- `turqoise` (2722 responses)
- `dark turquoise` (1714 responses)
- `light turquoise` (1544 responses)
- `turqouise` (810 responses)

**lavender** - Found 48 variant(s):
- `lavendar` (4381 responses)
- `lavander` (736 responses)
- `dark lavendar` (210 responses)
- `light lavendar` (120 responses)
- `pale lavendar` (79 responses)

**burgundy** - Found 13 variant(s):
- `burgandy` (1404 responses)
- `light burgandy` (48 responses)
- `dark burgandy` (25 responses)
- `pale burgandy` (12 responses)
- `deep burgandy` (8 responses)

**chartreuse** - Found 12 variant(s):
- `chartruse` (692 responses)
- `chartruese` (389 responses)
- `chartruese` (389 responses)
- `dark chartruse` (11 responses)
- `light chartruse` (10 responses)

**magenta** - Found 5 variant(s):
- `megenta` (74 responses)
- `magents` (20 responses)
- `dark megenta` (5 responses)
- `dark magents` (4 responses)
- `mageta` (3 responses)

**beige** - Found 164 variant(s):
- `beige` (14322 responses)
- `dark beige` (896 responses)
- `biege` (276 responses)
- `light beige` (244 responses)
- `greenish beige` (120 responses)

**cyan** - Found 3 variant(s):
- `cyaan` (10 responses)
- `syan` (7 responses)
- `cayan` (5 responses)

## 5. Methodology Notes

### 5.1 Tokenization Approach

For this initial exploration, we used simple whitespace/punctuation tokenization:
- Split on spaces, hyphens, underscores
- Preserve case for analysis (normalize to lowercase for counting)

**Limitation**: Does not handle compound words like "bluegreen" vs "blue green"

### 5.2 N-gram Analysis

Generated character bigrams for future typo detection. The most common bigrams
provide a baseline for identifying unusual character sequences that may indicate typos.

## 6. Uncertainty Considerations

### 6.1 Known Uncertainties

1. **Single-response names**: 0 names have only 1 response. These could be:
   - Legitimate rare color names
   - Typos or misspellings
   - Nonsense entries

2. **Monitor calibration**: All RGB values are from uncalibrated consumer monitors.
   Systematic bias cannot be assessed without reference data.

3. **Centore sample names**: We lack the individual CAUS sample names, limiting
   direct comparison at the individual color name level.

### 6.2 Suggestions for Uncertainty Reduction

1. **Cross-reference with dictionaries**: Compare against color name dictionaries
   (e.g., X11 colors, CSS colors) to identify likely valid names.

2. **Frequency thresholds**: Consider filtering names with very low response counts
   before entity matching to reduce noise.

3. **Manual review**: High-frequency unusual names should be manually reviewed
   before automated correction.

**Note**: These are suggestions only. No corrections have been applied.

## 7. Files Generated

| File | Description |
|------|-------------|
| `data_inventory.json` | Raw statistics and analysis data |
| `data_exploration.md` | This report |

---

*Generated by Phase 1: Data Inventory and Exploration*
