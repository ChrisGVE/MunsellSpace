# ISCC-NBS Classification Error Analysis Report

## Overview

This report analyzes classification failures in the MunsellSpace library's ISCC-NBS color naming system.
The analysis is based on the complete MUNSELL_COLOR_SCIENCE dataset containing 260 reference colors.

**Overall Accuracy**: 57.69% (150/260 colors classified correctly)
**Total Failures**: 110 colors (42.31%)

## Error Categories Summary

| Category | Count | Percentage | Description |
|----------|-------|------------|-------------|
| Modifier Inconsistencies | 54 | 20.77% | Modifier Inconsistencies |
| Hue Family Errors | 17 | 6.54% | Hue Family Errors |
| No Classification Found | 17 | 6.54% | No Classification Found |
| Brown Classification Gaps | 13 | 5.00% | Brown Classification Gaps |
| Red/Purple Confusion | 4 | 1.54% | Red/Purple Confusion |
| Other Classification Errors | 3 | 1.15% | Other Classification Errors |
| Value Classification Errors | 2 | 0.77% | Value Classification Errors |

## Detailed Error Analysis

### Modifier Inconsistencies

**Count**: 54 failures (20.77% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [239, 221, 229] | pinkish white | pale yellowish pink | 9.8R 9.1/1.6 | 10 |
| [199, 182, 189] | pinkish gray | grayish yellowish pink | 3YR 7.5/1.6 | 11 |
| [92, 6, 37] | very deep red | very dark purplish red | 6.6RP 1.6/6.3 | 15 |
| [72, 17, 39] | very dark red | very dark purplish red | 3.7RP 1.3/4.0 | 18 |
| [180, 136, 141] | light grayish red | pale red | 7.2R 6.0/3.2 | 19 |

**Pattern Analysis**:
- Inconsistent handling of modifiers like 'vivid', 'deep', 'grayish'
- May indicate incorrect polygon boundaries or modifier logic

### Hue Family Errors

**Count**: 17 failures (6.54% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [93, 78, 83] | dark reddish gray | dark purplish gray | 1.6RP 3.7/0.8 | 24 |
| [48, 38, 43] | reddish black | purplish black | 6.6P 1.5/0.7 | 25 |
| [167, 220, 38] | vivid yellow green | vivid chartreuse | 6.1GY 8.2/12.8 | 114 |
| [195, 223, 105] | brilliant yellow green | brilliant chartreuse | 5.6GY 8.6/9.2 | 115 |
| [130, 161, 43] | strong yellow green | strong chartreuse | 5.7GY 6.1/9.4 | 116 |

**Pattern Analysis**:
- Requires further investigation to identify specific patterns

### No Classification Found

**Count**: 17 failures (6.54% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [136, 102, 72] | moderate yellowish brown | No classification | 9.5R 4.5/6.0 | 76 |
| [180, 155, 141] | light grayish yellowish brown | No classification | 2.1Y 6.5/2.2 | 78 |
| [126, 105, 93] | grayish yellowish brown | No classification | 2.6Y 4.5/2.1 | 79 |
| [143, 135, 127] | light olive gray | No classification | 10YR 5.5/1.3 | 111 |
| [224, 226, 229] | greenish white | No classification | 1.1G 9.1/1.2 | 150 |

**Pattern Analysis**:
- Colors fall outside all defined ISCC-NBS polygon regions
- Indicates gaps in color space coverage

### Brown Classification Gaps

**Count**: 13 failures (5.00% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [139, 28, 14] | strong reddish brown | vivid red | 1.7R 3.1/11.7 | 41 |
| [97, 15, 18] | deep reddish brown | very deep purplish red | 10RP 1.8/8.4 | 42 |
| [125, 66, 59] | moderate reddish brown | grayish red | 2.6R 3.7/6.1 | 44 |
| [70, 29, 30] | dark reddish brown | very dark purplish red | 10RP 1.5/4.2 | 45 |
| [158, 127, 122] | light grayish reddish brown | grayish red | 10R 5.4/2.5 | 46 |

**Pattern Analysis**:
- Brown colors often misclassified as orange, red, or yellow
- Suggests insufficient brown polygon coverage in certain value/chroma ranges

### Red/Purple Confusion

**Count**: 4 failures (1.54% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [83, 56, 62] | dark grayish red | dark grayish purple | 5.8RP 2.7/2.0 | 21 |
| [51, 33, 39] | blackish red | blackish purple | 2.5RP 1.4/1.4 | 22 |
| [84, 6, 60] | very deep purplish red | very dark purple | 5.7P 1.5/4.4 | 251 |
| [67, 20, 50] | very dark purplish red | very dark purple | 5.5P 1.3/3.2 | 254 |

**Pattern Analysis**:
- Common in colors at hue boundary between red and purple families
- May indicate incorrect hue boundary definitions in ISCC-NBS polygons

### Other Classification Errors

**Count**: 3 failures (1.15% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [52, 37, 77] | dark violet | dark blue | 9.6B 1.6/4.4 | 206 |
| [88, 78, 114] | grayish violet | grayish blue | 9.2B 3.8/4.2 | 209 |
| [92, 82, 94] | dark purplish gray | dark bluish gray | 4.9PB 3.8/1.1 | 228 |

**Pattern Analysis**:
- Requires further investigation to identify specific patterns

### Value Classification Errors

**Count**: 2 failures (0.77% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| [31, 42, 42] | blackish green | greenish black | 1BG 1.4/0.7 | 149 |
| [43, 38, 48] | purplish black | blackish blue | 1.3PB 1.4/1.1 | 229 |

**Pattern Analysis**:
- Requires further investigation to identify specific patterns

## Complete Failure List

All 110 classification failures with complete details:

| # | RGB | Expected | Actual | Munsell | Error | Category |
|---|-----|----------|--------|---------|--------|----------|
| 1 | [239,221,229] | pinkish white | pale yellowish pink | 9.8R 9.1/1.6 | Classification mismatch | Modifier Inconsistencies |
| 2 | [199,182,189] | pinkish gray | grayish yellowish pink | 3YR 7.5/1.6 | Classification mismatch | Modifier Inconsistencies |
| 3 | [92,6,37] | very deep red | very dark purplish red | 6.6RP 1.6/6.3 | Classification mismatch | Modifier Inconsistencies |
| 4 | [72,17,39] | very dark red | very dark purplish red | 3.7RP 1.3/4.0 | Classification mismatch | Modifier Inconsistencies |
| 5 | [180,136,141] | light grayish red | pale red | 7.2R 6.0/3.2 | Classification mismatch | Modifier Inconsistencies |
| 6 | [83,56,62] | dark grayish red | dark grayish purple | 5.8RP 2.7/2.0 | Classification mismatch | Red/Purple Confusion |
| 7 | [51,33,39] | blackish red | blackish purple | 2.5RP 1.4/1.4 | Classification mismatch | Red/Purple Confusion |
| 8 | [146,129,134] | reddish gray | light brownish gray | 8.4YR 5.4/1.0 | Classification mismatch | Modifier Inconsistencies |
| 9 | [93,78,83] | dark reddish gray | dark purplish gray | 1.6RP 3.7/0.8 | Classification mismatch | Hue Family Errors |
| 10 | [48,38,43] | reddish black | purplish black | 6.6P 1.5/0.7 | Classification mismatch | Hue Family Errors |
| 11 | [139,28,14] | strong reddish brown | vivid red | 1.7R 3.1/11.7 | Classification mismatch | Brown Classification Gaps |
| 12 | [97,15,18] | deep reddish brown | very deep purplish red | 10RP 1.8/8.4 | Classification mismatch | Brown Classification Gaps |
| 13 | [125,66,59] | moderate reddish brown | grayish red | 2.6R 3.7/6.1 | Classification mismatch | Brown Classification Gaps |
| 14 | [70,29,30] | dark reddish brown | very dark purplish red | 10RP 1.5/4.2 | Classification mismatch | Brown Classification Gaps |
| 15 | [158,127,122] | light grayish reddish brown | grayish red | 10R 5.4/2.5 | Classification mismatch | Brown Classification Gaps |
| 16 | [67,41,42] | dark grayish reddish brown | very dark purplish red | 10RP 1.8/2.4 | Classification mismatch | Brown Classification Gaps |
| 17 | [138,68,22] | strong brown | moderate red | 5.8R 3.8/10.3 | Classification mismatch | Brown Classification Gaps |
| 18 | [87,26,7] | deep brown | very deep red | 3.1R 1.7/8.0 | Classification mismatch | Brown Classification Gaps |
| 19 | [173,124,99] | light brown | grayish reddish orange | 7.2R 5.5/6.3 | Classification mismatch | Brown Classification Gaps |
| 20 | [114,74,56] | moderate brown | grayish red | 6.3R 3.8/5.4 | Classification mismatch | Brown Classification Gaps |
| 21 | [68,33,18] | dark brown | deep reddish brown | 5.3R 1.5/5.2 | Classification mismatch | Modifier Inconsistencies |
| 22 | [153,127,117] | light grayish brown | grayish yellowish brown | 9.1YR 5.4/2.3 | Classification mismatch | Modifier Inconsistencies |
| 23 | [62,44,40] | dark grayish brown | very dark red | 4.6R 1.8/2.1 | Classification mismatch | Brown Classification Gaps |
| 24 | [96,82,81] | brownish gray | dark reddish gray | 2.5R 3.8/1.0 | Classification mismatch | Brown Classification Gaps |
| 25 | [43,33,30] | brownish black | blackish red | 5.8R 1.2/1.1 | Classification mismatch | Brown Classification Gaps |
| 26 | [255,190,80] | brilliant orange yellow | light orange yellow | 10YR 8.2/9.9 | Classification mismatch | Modifier Inconsistencies |
| 27 | [136,102,72] | moderate yellowish brown | None | 9.5R 4.5/6.0 | No ISCC-NBS classification found | No Classification Found |
| 28 | [80,52,26] | dark yellowish brown | deep reddish brown | 8.9R 2.3/5.5 | Classification mismatch | Modifier Inconsistencies |
| 29 | [180,155,141] | light grayish yellowish brown | None | 2.1Y 6.5/2.2 | No ISCC-NBS classification found | No Classification Found |
| 30 | [126,105,93] | grayish yellowish brown | None | 2.6Y 4.5/2.1 | No ISCC-NBS classification found | No Classification Found |
| 31 | [77,61,51] | dark grayish yellowish brown | grayish reddish brown | 8.6R 2.7/2.5 | Classification mismatch | Modifier Inconsistencies |
| 32 | [153,119,54] | light olive brown | brownish orange | 2YR 5.1/9.5 | Classification mismatch | Modifier Inconsistencies |
| 33 | [63,44,16] | dark olive brown | deep reddish brown | 10R 1.8/5.1 | Classification mismatch | Modifier Inconsistencies |
| 34 | [100,89,26] | moderate olive | strong brown | 5.2YR 3.7/8.2 | Classification mismatch | Modifier Inconsistencies |
| 35 | [53,46,10] | dark olive | deep brown | 5YR 1.7/5.3 | Classification mismatch | Modifier Inconsistencies |
| 36 | [142,133,111] | light grayish olive | light olive brown | 2.8Y 5.4/2.0 | Classification mismatch | Modifier Inconsistencies |
| 37 | [93,85,63] | grayish olive | moderate brown | 4.3YR 3.8/3.5 | Classification mismatch | Modifier Inconsistencies |
| 38 | [53,48,28] | dark grayish olive | dark brown | 5YR 1.8/3.3 | Classification mismatch | Modifier Inconsistencies |
| 39 | [143,135,127] | light olive gray | None | 10YR 5.5/1.3 | No ISCC-NBS classification found | No Classification Found |
| 40 | [88,81,74] | olive gray | brownish gray | 1.2YR 3.7/1.1 | Classification mismatch | Modifier Inconsistencies |
| 41 | [35,33,28] | olive black | brownish black | 4.3YR 1.1/0.8 | Classification mismatch | Modifier Inconsistencies |
| 42 | [167,220,38] | vivid yellow green | vivid chartreuse | 6.1GY 8.2/12.8 | Classification mismatch | Hue Family Errors |
| 43 | [195,223,105] | brilliant yellow green | brilliant chartreuse | 5.6GY 8.6/9.2 | Classification mismatch | Hue Family Errors |
| 44 | [130,161,43] | strong yellow green | strong chartreuse | 5.7GY 6.1/9.4 | Classification mismatch | Hue Family Errors |
| 45 | [72,108,14] | deep yellow green | deep chartreuse | 6.2GY 4.1/7.9 | Classification mismatch | Hue Family Errors |
| 46 | [206,219,159] | light yellow green | light chartreuse | 5.5GY 8.6/5.1 | Classification mismatch | Hue Family Errors |
| 47 | [139,154,95] | moderate yellow green | moderate chartreuse | 6.1GY 6.0/5.6 | Classification mismatch | Hue Family Errors |
| 48 | [215,215,193] | pale yellow green | pale chartreuse | 1.3GY 8.6/2.0 | Classification mismatch | Hue Family Errors |
| 49 | [151,154,133] | grayish yellow green | grayish chartreuse | 3.6GY 6.2/1.9 | Classification mismatch | Hue Family Errors |
| 50 | [44,85,6] | strong olive green | moderate olive brown | 4Y 3.3/9.6 | Classification mismatch | Modifier Inconsistencies |
| 51 | [73,91,34] | moderate olive green | strong yellowish brown | 10YR 3.8/7.4 | Classification mismatch | Modifier Inconsistencies |
| 52 | [32,52,11] | dark olive green | dark olive brown | 3Y 1.7/5.8 | Classification mismatch | Hue Family Errors |
| 53 | [47,51,38] | dark grayish olive green | dark grayish yellowish brown | 10YR 1.8/1.9 | Classification mismatch | Hue Family Errors |
| 54 | [5,66,8] | very deep yellowish green | dark olive | 6.9Y 2.1/8.5 | Classification mismatch | Modifier Inconsistencies |
| 55 | [47,93,58] | dark yellowish green | moderate olive | 8.8Y 3.8/5.0 | Classification mismatch | Modifier Inconsistencies |
| 56 | [16,54,26] | very dark yellowish green | dark olive | 8.7Y 1.7/4.5 | Classification mismatch | Modifier Inconsistencies |
| 57 | [12,46,36] | very dark green | very dark yellowish green | 8.4GY 1.5/2.2 | Classification mismatch | Modifier Inconsistencies |
| 58 | [31,42,42] | blackish green | greenish black | 1BG 1.4/0.7 | Classification mismatch | Value Classification Errors |
| 59 | [224,226,229] | greenish white | None | 1.1G 9.1/1.2 | No ISCC-NBS classification found | No Classification Found |
| 60 | [186,190,193] | light greenish gray | None | 3.1G 7.6/1.2 | No ISCC-NBS classification found | No Classification Found |
| 61 | [84,88,88] | dark greenish gray | None | 7.2GY 3.8/0.5 | No ISCC-NBS classification found | No Classification Found |
| 62 | [33,38,38] | greenish black | black | 1BG 1.3/0.4 | Classification mismatch | Modifier Inconsistencies |
| 63 | [19,252,213] | vivid bluish green | vivid turquoise | 10G 9.0/11.1 | Classification mismatch | Modifier Inconsistencies |
| 64 | [53,215,206] | brilliant bluish green | brilliant turquoise | 2.9BG 7.8/9.9 | Classification mismatch | Modifier Inconsistencies |
| 65 | [13,143,130] | strong bluish green | strong turquoise | 10G 5.2/7.7 | Classification mismatch | Modifier Inconsistencies |
| 66 | [152,225,224] | very light bluish green | very light turquoise | 5.3BG 8.6/4.9 | Classification mismatch | Modifier Inconsistencies |
| 67 | [95,171,171] | light bluish green | light turquoise | 4.9BG 6.5/5.6 | Classification mismatch | Modifier Inconsistencies |
| 68 | [41,122,123] | moderate bluish green | moderate turquoise | 4.5BG 4.6/5.6 | Classification mismatch | Modifier Inconsistencies |
| 69 | [21,75,77] | dark bluish green | dark turquoise | 3.8BG 2.9/4.4 | Classification mismatch | Modifier Inconsistencies |
| 70 | [10,45,46] | very dark bluish green | very dark turquoise | 3.2BG 1.4/3.3 | Classification mismatch | Modifier Inconsistencies |
| 71 | [45,188,226] | brilliant greenish blue | brilliant teal | 3.2B 7.1/8.6 | Classification mismatch | Modifier Inconsistencies |
| 72 | [19,133,175] | strong greenish blue | strong teal | 1B 5.1/8.0 | Classification mismatch | Modifier Inconsistencies |
| 73 | [148,214,239] | very light greenish blue | very light teal | 3.8B 8.3/5.2 | Classification mismatch | Modifier Inconsistencies |
| 74 | [101,168,195] | light greenish blue | light teal | 6.2B 6.5/5.7 | Classification mismatch | Modifier Inconsistencies |
| 75 | [42,118,145] | moderate greenish blue | moderate teal | 9.8BG 4.6/6.0 | Classification mismatch | Modifier Inconsistencies |
| 76 | [19,74,96] | dark greenish blue | dark teal | 2.6B 2.9/4.0 | Classification mismatch | Modifier Inconsistencies |
| 77 | [11,44,59] | very dark greenish blue | very dark teal | 5.6B 1.5/3.4 | Classification mismatch | Modifier Inconsistencies |
| 78 | [50,63,78] | dark grayish blue | None | 10B 2.5/2.2 | No ISCC-NBS classification found | No Classification Found |
| 79 | [30,37,49] | blackish blue | very dark teal | 4.3B 1.3/2.1 | Classification mismatch | Modifier Inconsistencies |
| 80 | [131,135,147] | bluish gray | None | 6.3PB 5.5/1.5 | No ISCC-NBS classification found | No Classification Found |
| 81 | [80,84,95] | dark bluish gray | None | 5.9PB 3.8/1.5 | No ISCC-NBS classification found | No Classification Found |
| 82 | [36,39,46] | bluish black | None | 4.7B 1.4/1.0 | No ISCC-NBS classification found | No Classification Found |
| 83 | [42,40,111] | deep purplish blue | deep teal | 7.4B 1.9/7.2 | Classification mismatch | Modifier Inconsistencies |
| 84 | [34,34,72] | dark purplish blue | very dark teal | 7.3B 1.4/4.7 | Classification mismatch | Modifier Inconsistencies |
| 85 | [60,22,104] | deep violet | dark blue | 9.6B 1.6/6.7 | Classification mismatch | Modifier Inconsistencies |
| 86 | [52,37,77] | dark violet | dark blue | 9.6B 1.6/4.4 | Classification mismatch | Other Classification Errors |
| 87 | [88,78,114] | grayish violet | grayish blue | 9.2B 3.8/4.2 | Classification mismatch | Other Classification Errors |
| 88 | [86,55,98] | dark purple | dark blue | 3.1PB 2.8/4.3 | Classification mismatch | Hue Family Errors |
| 89 | [55,27,65] | very dark purple | dark blue | 3.1PB 1.4/3.7 | Classification mismatch | Modifier Inconsistencies |
| 90 | [173,151,179] | pale purple | None | 7.9P 6.4/3.9 | No ISCC-NBS classification found | No Classification Found |
| 91 | [81,63,81] | dark grayish purple | dark grayish blue | 6.7PB 2.9/1.7 | Classification mismatch | Hue Family Errors |
| 92 | [47,34,49] | blackish purple | blackish blue | 5.1PB 1.4/1.8 | Classification mismatch | Hue Family Errors |
| 93 | [235,223,239] | purplish white | pale purplish pink | 9.6P 9.1/1.6 | Classification mismatch | Modifier Inconsistencies |
| 94 | [195,183,198] | light purplish gray | None | 9.3P 7.5/1.8 | No ISCC-NBS classification found | No Classification Found |
| 95 | [143,132,144] | purplish gray | None | 8.5P 5.5/1.8 | No ISCC-NBS classification found | No Classification Found |
| 96 | [92,82,94] | dark purplish gray | dark bluish gray | 4.9PB 3.8/1.1 | Classification mismatch | Other Classification Errors |
| 97 | [43,38,48] | purplish black | blackish blue | 1.3PB 1.4/1.1 | Classification mismatch | Value Classification Errors |
| 98 | [79,9,74] | very deep reddish purple | dark purplish blue | 8.2PB 1.5/4.6 | Classification mismatch | Modifier Inconsistencies |
| 99 | [150,88,136] | moderate reddish purple | None | 10PB 4.5/4.5 | No ISCC-NBS classification found | No Classification Found |
| 100 | [95,52,88] | dark reddish purple | grayish violet | 9.4PB 2.8/3.5 | Classification mismatch | Modifier Inconsistencies |
| 101 | [134,98,126] | grayish reddish purple | None | 10P 4.5/5.0 | No ISCC-NBS classification found | No Classification Found |
| 102 | [221,35,136] | vivid purplish red | vivid purplish pink | 5.9RP 4.9/16.7 | Classification mismatch | Hue Family Errors |
| 103 | [184,55,115] | strong purplish red | strong purplish pink | 6.7RP 4.4/12.1 | Classification mismatch | Hue Family Errors |
| 104 | [84,6,60] | very deep purplish red | very dark purple | 5.7P 1.5/4.4 | Classification mismatch | Red/Purple Confusion |
| 105 | [67,20,50] | very dark purplish red | very dark purple | 5.5P 1.3/3.2 | Classification mismatch | Red/Purple Confusion |
| 106 | [178,135,155] | light grayish purplish red | pale purplish red | 6RP 6.0/3.9 | Classification mismatch | Modifier Inconsistencies |
| 107 | [231,225,233] | white | very pale green | 8.4GY 9.1/1.4 | Classification mismatch | Modifier Inconsistencies |
| 108 | [189,183,191] | light gray | light purplish gray | 5.2P 7.5/1.4 | Classification mismatch | Modifier Inconsistencies |
| 109 | [138,132,137] | medium gray | greenish gray | 7.1GY 5.4/0.9 | Classification mismatch | Modifier Inconsistencies |
| 110 | [88,84,88] | dark gray | None | 7.2GY 3.8/0.5 | No ISCC-NBS classification found | No Classification Found |

## Recommendations

### Modifier Inconsistencies (54 failures)
1. Standardize modifier application logic
2. Review value/chroma thresholds for modifiers like 'vivid', 'deep'
3. Ensure consistent polygon boundary rules

### Hue Family Errors (17 failures)
1. Investigate specific failure patterns
2. Review relevant polygon definitions and boundaries
3. Consider algorithm improvements for this category

### No Classification Found (17 failures)
1. Identify gaps in ISCC-NBS color space coverage
2. Add missing polygon regions for unclassified colors
3. Review if gaps are intentional or require new definitions

### Brown Classification Gaps (13 failures)
1. Expand brown polygon coverage in low-chroma, medium-value regions
2. Review brown vs orange/yellow boundary definitions
3. Add more brown polygon regions for comprehensive coverage

---
Report generated by MunsellSpace Classification Accuracy Analysis Tool
