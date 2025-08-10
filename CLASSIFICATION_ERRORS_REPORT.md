# ISCC-NBS Classification Error Analysis Report

## Overview

This report analyzes classification failures in the MunsellSpace library's ISCC-NBS color naming system.
The analysis is based on the complete MUNSELL_COLOR_SCIENCE dataset containing 260 reference colors.

**Overall Accuracy**: 69.23% (180/260 colors classified correctly)
**Total Failures**: 80 colors (30.77%)

## Error Categories Summary

| Category | Count | Percentage | Description |
|----------|-------|------------|-------------|
| Modifier Inconsistencies | 44 | 16.92% | Modifier Inconsistencies |
| Brown Classification Gaps | 16 | 6.15% | Brown Classification Gaps |
| Hue Family Errors | 8 | 3.08% | Hue Family Errors |
| Red/Purple Confusion | 4 | 1.54% | Red/Purple Confusion |
| Other Classification Errors | 4 | 1.54% | Other Classification Errors |
| Value Classification Errors | 3 | 1.15% | Value Classification Errors |
| No Classification Found | 1 | 0.38% | No Classification Found |

## Detailed Error Analysis

### Modifier Inconsistencies

**Count**: 44 failures (16.92% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #EFDDE5 | pinkish white | pale yellowish pink | 9.8R 9.1/1.6 | 10 |
| #C7B6BD | pinkish gray | grayish yellowish pink | 3YR 7.5/1.6 | 11 |
| #5C0625 | very deep red | very dark purplish red | 6.6RP 1.6/6.3 | 15 |
| #481127 | very dark red | very dark purplish red | 3.7RP 1.3/4.0 | 18 |
| #928186 | reddish gray | light brownish gray | 8.4YR 5.4/1.0 | 23 |

**Pattern Analysis**:
- Inconsistent handling of modifiers like 'vivid', 'deep', 'grayish'
- May indicate incorrect polygon boundaries or modifier logic

### Brown Classification Gaps

**Count**: 16 failures (6.15% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #8B1C0E | strong reddish brown | vivid red | 1.7R 3.1/11.7 | 41 |
| #610F12 | deep reddish brown | very deep purplish red | 10RP 1.8/8.4 | 42 |
| #7D423B | moderate reddish brown | grayish red | 2.6R 3.7/6.1 | 44 |
| #461D1E | dark reddish brown | very dark purplish red | 10RP 1.5/4.2 | 45 |
| #9E7F7A | light grayish reddish brown | grayish red | 10R 5.4/2.5 | 46 |

**Pattern Analysis**:
- Brown colors often misclassified as orange, red, or yellow
- Suggests insufficient brown polygon coverage in certain value/chroma ranges

### Hue Family Errors

**Count**: 8 failures (3.08% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #5D4E53 | dark reddish gray | dark purplish gray | 1.6RP 3.7/0.8 | 24 |
| #30262B | reddish black | purplish black | 6.6P 1.5/0.7 | 25 |
| #20340B | dark olive green | dark olive brown | 3Y 1.7/5.8 | 124 |
| #2F3326 | dark grayish olive green | dark grayish yellowish brown | 10YR 1.8/1.9 | 126 |
| #2A7691 | moderate greenish blue | moderate bluish green | 9.8BG 4.6/6.0 | 167 |

**Pattern Analysis**:
- Requires further investigation to identify specific patterns

### Red/Purple Confusion

**Count**: 4 failures (1.54% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #53383E | dark grayish red | dark grayish purple | 5.8RP 2.7/2.0 | 21 |
| #332127 | blackish red | blackish purple | 2.5RP 1.4/1.4 | 22 |
| #54063C | very deep purplish red | very dark purple | 5.7P 1.5/4.4 | 251 |
| #431432 | very dark purplish red | very dark purple | 5.5P 1.3/3.2 | 254 |

**Pattern Analysis**:
- Common in colors at hue boundary between red and purple families
- May indicate incorrect hue boundary definitions in ISCC-NBS polygons

### Other Classification Errors

**Count**: 4 failures (1.54% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #2A286F | deep purplish blue | deep greenish blue | 7.4B 1.9/7.2 | 191 |
| #34254D | dark violet | dark blue | 9.6B 1.6/4.4 | 206 |
| #584E72 | grayish violet | grayish blue | 9.2B 3.8/4.2 | 209 |
| #5C525E | dark purplish gray | dark bluish gray | 4.9PB 3.8/1.1 | 228 |

**Pattern Analysis**:
- Requires further investigation to identify specific patterns

### Value Classification Errors

**Count**: 3 failures (1.15% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #1F2A2A | blackish green | greenish black | 1BG 1.4/0.7 | 149 |
| #24272E | bluish black | blackish blue | 4.7B 1.4/1.0 | 187 |
| #2B2630 | purplish black | blackish blue | 1.3PB 1.4/1.1 | 229 |

**Pattern Analysis**:
- Requires further investigation to identify specific patterns

### No Classification Found

**Count**: 1 failures (0.38% of total tests)

**Examples**:

| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |
|-----|---------------|-------------|-------------------|------|
| #AD97B3 | pale purple | No classification | 7.9P 6.4/3.9 | 221 |

**Pattern Analysis**:
- Colors fall outside all defined ISCC-NBS polygon regions
- Indicates gaps in color space coverage

## Complete Failure List

All 80 classification failures with complete details:

| # | RGB | Expected | Actual | Munsell | Error | Category |
|---|-----|----------|--------|---------|--------|----------|
| 1 | #EFDDE5 | pinkish white | pale yellowish pink | 9.8R 9.1/1.6 | Classification mismatch | Modifier Inconsistencies |
| 2 | #C7B6BD | pinkish gray | grayish yellowish pink | 3YR 7.5/1.6 | Classification mismatch | Modifier Inconsistencies |
| 3 | #5C0625 | very deep red | very dark purplish red | 6.6RP 1.6/6.3 | Classification mismatch | Modifier Inconsistencies |
| 4 | #481127 | very dark red | very dark purplish red | 3.7RP 1.3/4.0 | Classification mismatch | Modifier Inconsistencies |
| 5 | #53383E | dark grayish red | dark grayish purple | 5.8RP 2.7/2.0 | Classification mismatch | Red/Purple Confusion |
| 6 | #332127 | blackish red | blackish purple | 2.5RP 1.4/1.4 | Classification mismatch | Red/Purple Confusion |
| 7 | #928186 | reddish gray | light brownish gray | 8.4YR 5.4/1.0 | Classification mismatch | Modifier Inconsistencies |
| 8 | #5D4E53 | dark reddish gray | dark purplish gray | 1.6RP 3.7/0.8 | Classification mismatch | Hue Family Errors |
| 9 | #30262B | reddish black | purplish black | 6.6P 1.5/0.7 | Classification mismatch | Hue Family Errors |
| 10 | #8B1C0E | strong reddish brown | vivid red | 1.7R 3.1/11.7 | Classification mismatch | Brown Classification Gaps |
| 11 | #610F12 | deep reddish brown | very deep purplish red | 10RP 1.8/8.4 | Classification mismatch | Brown Classification Gaps |
| 12 | #7D423B | moderate reddish brown | grayish red | 2.6R 3.7/6.1 | Classification mismatch | Brown Classification Gaps |
| 13 | #461D1E | dark reddish brown | very dark purplish red | 10RP 1.5/4.2 | Classification mismatch | Brown Classification Gaps |
| 14 | #9E7F7A | light grayish reddish brown | grayish red | 10R 5.4/2.5 | Classification mismatch | Brown Classification Gaps |
| 15 | #43292A | dark grayish reddish brown | very dark purplish red | 10RP 1.8/2.4 | Classification mismatch | Brown Classification Gaps |
| 16 | #8A4416 | strong brown | moderate red | 5.8R 3.8/10.3 | Classification mismatch | Brown Classification Gaps |
| 17 | #571A07 | deep brown | very deep red | 3.1R 1.7/8.0 | Classification mismatch | Brown Classification Gaps |
| 18 | #AD7C63 | light brown | dark yellowish pink | 7.2R 5.5/6.3 | Classification mismatch | Brown Classification Gaps |
| 19 | #724A38 | moderate brown | grayish red | 6.3R 3.8/5.4 | Classification mismatch | Brown Classification Gaps |
| 20 | #442112 | dark brown | very dark red | 5.3R 1.5/5.2 | Classification mismatch | Brown Classification Gaps |
| 21 | #997F75 | light grayish brown | grayish yellowish brown | 9.1YR 5.4/2.3 | Classification mismatch | Modifier Inconsistencies |
| 22 | #3E2C28 | dark grayish brown | very dark red | 4.6R 1.8/2.1 | Classification mismatch | Brown Classification Gaps |
| 23 | #605251 | brownish gray | dark reddish gray | 2.5R 3.8/1.0 | Classification mismatch | Brown Classification Gaps |
| 24 | #2B211E | brownish black | blackish red | 5.8R 1.2/1.1 | Classification mismatch | Brown Classification Gaps |
| 25 | #FFBE50 | brilliant orange yellow | light orange yellow | 10YR 8.2/9.9 | Classification mismatch | Modifier Inconsistencies |
| 26 | #673F0B | deep yellowish brown | strong brown | 7.4YR 3.1/6.8 | Classification mismatch | Modifier Inconsistencies |
| 27 | #886648 | moderate yellowish brown | grayish reddish orange | 9.5R 4.5/6.0 | Classification mismatch | Brown Classification Gaps |
| 28 | #50341A | dark yellowish brown | deep reddish brown | 8.9R 2.3/5.5 | Classification mismatch | Modifier Inconsistencies |
| 29 | #B49B8D | light grayish yellowish brown | light olive brown | 2.1Y 6.5/2.2 | Classification mismatch | Modifier Inconsistencies |
| 30 | #7E695D | grayish yellowish brown | light olive brown | 2.6Y 4.5/2.1 | Classification mismatch | Modifier Inconsistencies |
| 31 | #4D3D33 | dark grayish yellowish brown | grayish reddish brown | 8.6R 2.7/2.5 | Classification mismatch | Modifier Inconsistencies |
| 32 | #997736 | light olive brown | moderate reddish orange | 2YR 5.1/9.5 | Classification mismatch | Brown Classification Gaps |
| 33 | #3F2C10 | dark olive brown | deep reddish brown | 10R 1.8/5.1 | Classification mismatch | Modifier Inconsistencies |
| 34 | #64591A | moderate olive | strong brown | 5.2YR 3.7/8.2 | Classification mismatch | Modifier Inconsistencies |
| 35 | #352E0A | dark olive | deep brown | 5YR 1.7/5.3 | Classification mismatch | Modifier Inconsistencies |
| 36 | #8E856F | light grayish olive | light olive brown | 2.8Y 5.4/2.0 | Classification mismatch | Modifier Inconsistencies |
| 37 | #5D553F | grayish olive | moderate brown | 4.3YR 3.8/3.5 | Classification mismatch | Modifier Inconsistencies |
| 38 | #35301C | dark grayish olive | dark brown | 5YR 1.8/3.3 | Classification mismatch | Modifier Inconsistencies |
| 39 | #8F877F | light olive gray | grayish yellowish brown | 10YR 5.5/1.3 | Classification mismatch | Modifier Inconsistencies |
| 40 | #58514A | olive gray | brownish gray | 1.2YR 3.7/1.1 | Classification mismatch | Modifier Inconsistencies |
| 41 | #23211C | olive black | brownish black | 4.3YR 1.1/0.8 | Classification mismatch | Modifier Inconsistencies |
| 42 | #2C5506 | strong olive green | moderate olive brown | 4Y 3.3/9.6 | Classification mismatch | Modifier Inconsistencies |
| 43 | #495B22 | moderate olive green | strong yellowish brown | 10YR 3.8/7.4 | Classification mismatch | Modifier Inconsistencies |
| 44 | #20340B | dark olive green | dark olive brown | 3Y 1.7/5.8 | Classification mismatch | Hue Family Errors |
| 45 | #2F3326 | dark grayish olive green | dark grayish yellowish brown | 10YR 1.8/1.9 | Classification mismatch | Hue Family Errors |
| 46 | #054208 | very deep yellowish green | dark olive | 6.9Y 2.1/8.5 | Classification mismatch | Modifier Inconsistencies |
| 47 | #2F5D3A | dark yellowish green | moderate olive | 8.8Y 3.8/5.0 | Classification mismatch | Modifier Inconsistencies |
| 48 | #10361A | very dark yellowish green | dark olive | 8.7Y 1.7/4.5 | Classification mismatch | Modifier Inconsistencies |
| 49 | #0C2E24 | very dark green | very dark yellowish green | 8.4GY 1.5/2.2 | Classification mismatch | Modifier Inconsistencies |
| 50 | #1F2A2A | blackish green | greenish black | 1BG 1.4/0.7 | Classification mismatch | Value Classification Errors |
| 51 | #545858 | dark greenish gray | dark gray | 7.2GY 3.8/0.5 | Classification mismatch | Modifier Inconsistencies |
| 52 | #212626 | greenish black | black | 1BG 1.3/0.4 | Classification mismatch | Modifier Inconsistencies |
| 53 | #2A7691 | moderate greenish blue | moderate bluish green | 9.8BG 4.6/6.0 | Classification mismatch | Hue Family Errors |
| 54 | #323F4E | dark grayish blue | dark blue | 10B 2.5/2.2 | Classification mismatch | Modifier Inconsistencies |
| 55 | #1E2531 | blackish blue | very dark greenish blue | 4.3B 1.3/2.1 | Classification mismatch | Modifier Inconsistencies |
| 56 | #838793 | bluish gray | pale blue | 6.3PB 5.5/1.5 | Classification mismatch | Modifier Inconsistencies |
| 57 | #24272E | bluish black | blackish blue | 4.7B 1.4/1.0 | Classification mismatch | Value Classification Errors |
| 58 | #2A286F | deep purplish blue | deep greenish blue | 7.4B 1.9/7.2 | Classification mismatch | Other Classification Errors |
| 59 | #222248 | dark purplish blue | very dark greenish blue | 7.3B 1.4/4.7 | Classification mismatch | Modifier Inconsistencies |
| 60 | #3C1668 | deep violet | dark blue | 9.6B 1.6/6.7 | Classification mismatch | Modifier Inconsistencies |
| 61 | #34254D | dark violet | dark blue | 9.6B 1.6/4.4 | Classification mismatch | Other Classification Errors |
| 62 | #584E72 | grayish violet | grayish blue | 9.2B 3.8/4.2 | Classification mismatch | Other Classification Errors |
| 63 | #563762 | dark purple | dark blue | 3.1PB 2.8/4.3 | Classification mismatch | Hue Family Errors |
| 64 | #371B41 | very dark purple | dark blue | 3.1PB 1.4/3.7 | Classification mismatch | Modifier Inconsistencies |
| 65 | #AD97B3 | pale purple | None | 7.9P 6.4/3.9 | No ISCC-NBS classification found | No Classification Found |
| 66 | #513F51 | dark grayish purple | dark grayish blue | 6.7PB 2.9/1.7 | Classification mismatch | Hue Family Errors |
| 67 | #2F2231 | blackish purple | blackish blue | 5.1PB 1.4/1.8 | Classification mismatch | Hue Family Errors |
| 68 | #EBDFEF | purplish white | pale purplish pink | 9.6P 9.1/1.6 | Classification mismatch | Modifier Inconsistencies |
| 69 | #C3B7C6 | light purplish gray | grayish purplish pink | 9.3P 7.5/1.8 | Classification mismatch | Modifier Inconsistencies |
| 70 | #8F8490 | purplish gray | pale purple | 8.5P 5.5/1.8 | Classification mismatch | Modifier Inconsistencies |
| 71 | #5C525E | dark purplish gray | dark bluish gray | 4.9PB 3.8/1.1 | Classification mismatch | Other Classification Errors |
| 72 | #2B2630 | purplish black | blackish blue | 1.3PB 1.4/1.1 | Classification mismatch | Value Classification Errors |
| 73 | #4F094A | very deep reddish purple | dark purplish blue | 8.2PB 1.5/4.6 | Classification mismatch | Modifier Inconsistencies |
| 74 | #965888 | moderate reddish purple | grayish violet | 10PB 4.5/4.5 | Classification mismatch | Modifier Inconsistencies |
| 75 | #5F3458 | dark reddish purple | grayish violet | 9.4PB 2.8/3.5 | Classification mismatch | Modifier Inconsistencies |
| 76 | #54063C | very deep purplish red | very dark purple | 5.7P 1.5/4.4 | Classification mismatch | Red/Purple Confusion |
| 77 | #431432 | very dark purplish red | very dark purple | 5.5P 1.3/3.2 | Classification mismatch | Red/Purple Confusion |
| 78 | #E7E1E9 | white | very pale green | 8.4GY 9.1/1.4 | Classification mismatch | Modifier Inconsistencies |
| 79 | #BDB7BF | light gray | light purplish gray | 5.2P 7.5/1.4 | Classification mismatch | Modifier Inconsistencies |
| 80 | #8A8489 | medium gray | greenish gray | 7.1GY 5.4/0.9 | Classification mismatch | Modifier Inconsistencies |

## Recommendations

### Modifier Inconsistencies (44 failures)
1. Standardize modifier application logic
2. Review value/chroma thresholds for modifiers like 'vivid', 'deep'
3. Ensure consistent polygon boundary rules

### Brown Classification Gaps (16 failures)
1. Expand brown polygon coverage in low-chroma, medium-value regions
2. Review brown vs orange/yellow boundary definitions
3. Add more brown polygon regions for comprehensive coverage

### Hue Family Errors (8 failures)
1. Investigate specific failure patterns
2. Review relevant polygon definitions and boundaries
3. Consider algorithm improvements for this category

---
Report generated by MunsellSpace Classification Accuracy Analysis Tool
