# ISCC-NBS Classification Error Analysis Report

## Overview

This report analyzes classification failures in the MunsellSpace library's ISCC-NBS color naming system.
The analysis is based on the complete MUNSELL_COLOR_SCIENCE dataset containing 260 reference colors.

**Overall Accuracy**: 63.08% (164/260 colors classified correctly)
**Total Failures**: 96 colors (36.92%)

## Error Categories Summary

| Category                    | Count | Percentage | Description                 |
| --------------------------- | ----- | ---------- | --------------------------- |
| Modifier Inconsistencies    | 48    | 18.46%     | Modifier Inconsistencies    |
| Brown Classification Gaps   | 16    | 6.15%      | Brown Classification Gaps   |
| Other Classification Errors | 14    | 5.38%      | Other Classification Errors |
| Hue Family Errors           | 8     | 3.08%      | Hue Family Errors           |
| Red/Purple Confusion        | 6     | 2.31%      | Red/Purple Confusion        |
| Value Classification Errors | 3     | 1.15%      | Value Classification Errors |
| No Classification Found     | 1     | 0.38%      | No Classification Found     |

## Detailed Error Analysis

### Modifier Inconsistencies

**Count**: 48 failures (18.46% of total tests)

**Examples**:

| RGB     | Expected Name     | Actual Name            | Munsell Coordinates | Line |
| ------- | ----------------- | ---------------------- | ------------------- | ---- |
| #EFDDE5 | pinkish white     | pale yellowish pink    | 9.8R 9.1/1.6        | 10   |
| #C7B6BD | pinkish gray      | grayish yellowish pink | 3YR 7.5/1.6         | 11   |
| #5C0625 | very deep red     | very dark purplish red | 6.6RP 1.6/6.3       | 15   |
| #481127 | very dark red     | very dark purplish red | 3.7RP 1.3/4.0       | 18   |
| #B4888D | light grayish red | light reddish brown    | 7.2R 6.0/3.2        | 19   |

**Pattern Analysis**:

- Inconsistent handling of modifiers like 'vivid', 'deep', 'grayish'
- May indicate incorrect polygon boundaries or modifier logic

### Brown Classification Gaps

**Count**: 16 failures (6.15% of total tests)

**Examples**:

| RGB     | Expected Name               | Actual Name            | Munsell Coordinates | Line |
| ------- | --------------------------- | ---------------------- | ------------------- | ---- |
| #8B1C0E | strong reddish brown        | vivid red              | 1.7R 3.1/11.7       | 41   |
| #610F12 | deep reddish brown          | very deep purplish red | 10RP 1.8/8.4        | 42   |
| #7D423B | moderate reddish brown      | grayish red            | 2.6R 3.7/6.1        | 44   |
| #461D1E | dark reddish brown          | very dark purplish red | 10RP 1.5/4.2        | 45   |
| #9E7F7A | light grayish reddish brown | grayish red            | 10R 5.4/2.5         | 46   |

**Pattern Analysis**:

- Brown colors often misclassified as orange, red, or yellow
- Suggests insufficient brown polygon coverage in certain value/chroma ranges

### Other Classification Errors

**Count**: 14 failures (5.38% of total tests)

**Examples**:

| RGB     | Expected Name       | Actual Name           | Munsell Coordinates | Line |
| ------- | ------------------- | --------------------- | ------------------- | ---- |
| #928281 | light brownish gray | light -ish gray brown | 5.4YR 5.4/1.1       | 63   |
| #EEDFDA | yellowish white     | -ish white yellow     | 9.6YR 9.1/1.4       | 91   |
| #C6B9B1 | yellowish gray      | -ish gray yellow      | 2.2Y 7.5/1.7        | 92   |
| #E0E2E5 | greenish white      | -ish white green      | 1.1G 9.1/1.2        | 150  |
| #BABEC1 | light greenish gray | light -ish gray green | 3.1G 7.6/1.2        | 151  |

**Pattern Analysis**:

- Requires further investigation to identify specific patterns

### Hue Family Errors

**Count**: 8 failures (3.08% of total tests)

**Examples**:

| RGB     | Expected Name            | Actual Name                  | Munsell Coordinates | Line |
| ------- | ------------------------ | ---------------------------- | ------------------- | ---- |
| #20340B | dark olive green         | dark olive brown             | 3Y 1.7/5.8          | 124  |
| #2F3326 | dark grayish olive green | dark grayish yellowish brown | 10YR 1.8/1.9        | 126  |
| #2A7691 | moderate greenish blue   | moderate bluish green        | 9.8BG 4.6/6.0       | 167  |
| #563762 | dark purple              | dark blue                    | 3.1PB 2.8/4.3       | 218  |
| #513F51 | dark grayish purple      | dark grayish blue            | 6.7PB 2.9/1.7       | 223  |

**Pattern Analysis**:

- Requires further investigation to identify specific patterns

### Red/Purple Confusion

**Count**: 6 failures (2.31% of total tests)

**Examples**:

| RGB     | Expected Name          | Actual Name           | Munsell Coordinates | Line |
| ------- | ---------------------- | --------------------- | ------------------- | ---- |
| #53383E | dark grayish red       | dark grayish purple   | 5.8RP 2.7/2.0       | 21   |
| #332127 | blackish red           | blackish purple       | 2.5RP 1.4/1.4       | 22   |
| #5D4E53 | dark reddish gray      | dark -ish gray purple | 1.6RP 3.7/0.8       | 24   |
| #30262B | reddish black          | -ish black purple     | 6.6P 1.5/0.7        | 25   |
| #54063C | very deep purplish red | very dark purple      | 5.7P 1.5/4.4        | 251  |

**Pattern Analysis**:

- Common in colors at hue boundary between red and purple families
- May indicate incorrect hue boundary definitions in ISCC-NBS polygons

### Value Classification Errors

**Count**: 3 failures (1.15% of total tests)

**Examples**:

| RGB     | Expected Name  | Actual Name      | Munsell Coordinates | Line |
| ------- | -------------- | ---------------- | ------------------- | ---- |
| #1F2A2A | blackish green | -ish black green | 1BG 1.4/0.7         | 149  |
| #24272E | bluish black   | blackish blue    | 4.7B 1.4/1.0        | 187  |
| #2B2630 | purplish black | blackish blue    | 1.3PB 1.4/1.1       | 229  |

**Pattern Analysis**:

- Requires further investigation to identify specific patterns

### No Classification Found

**Count**: 1 failures (0.38% of total tests)

**Examples**:

| RGB     | Expected Name | Actual Name       | Munsell Coordinates | Line |
| ------- | ------------- | ----------------- | ------------------- | ---- |
| #AD97B3 | pale purple   | No classification | 7.9P 6.4/3.9        | 221  |

**Pattern Analysis**:

- Colors fall outside all defined ISCC-NBS polygon regions
- Indicates gaps in color space coverage

## Complete Failure List

All 96 classification failures with complete details:

| #   | RGB     | Expected                      | Actual                       | Munsell        | Error                            | Category                    |
| --- | ------- | ----------------------------- | ---------------------------- | -------------- | -------------------------------- | --------------------------- |
| 1   | #EFDDE5 | pinkish white                 | pale yellowish pink          | 9.8R 9.1/1.6   | Classification mismatch          | Modifier Inconsistencies    |
| 2   | #C7B6BD | pinkish gray                  | grayish yellowish pink       | 3YR 7.5/1.6    | Classification mismatch          | Modifier Inconsistencies    |
| 3   | #5C0625 | very deep red                 | very dark purplish red       | 6.6RP 1.6/6.3  | Classification mismatch          | Modifier Inconsistencies    |
| 4   | #481127 | very dark red                 | very dark purplish red       | 3.7RP 1.3/4.0  | Classification mismatch          | Modifier Inconsistencies    |
| 5   | #B4888D | light grayish red             | light reddish brown          | 7.2R 6.0/3.2   | Classification mismatch          | Modifier Inconsistencies    |
| 6   | #53383E | dark grayish red              | dark grayish purple          | 5.8RP 2.7/2.0  | Classification mismatch          | Red/Purple Confusion        |
| 7   | #332127 | blackish red                  | blackish purple              | 2.5RP 1.4/1.4  | Classification mismatch          | Red/Purple Confusion        |
| 8   | #928186 | reddish gray                  | light -ish gray brown        | 8.4YR 5.4/1.0  | Classification mismatch          | Modifier Inconsistencies    |
| 9   | #5D4E53 | dark reddish gray             | dark -ish gray purple        | 1.6RP 3.7/0.8  | Classification mismatch          | Red/Purple Confusion        |
| 10  | #30262B | reddish black                 | -ish black purple            | 6.6P 1.5/0.7   | Classification mismatch          | Red/Purple Confusion        |
| 11  | #8B1C0E | strong reddish brown          | vivid red                    | 1.7R 3.1/11.7  | Classification mismatch          | Brown Classification Gaps   |
| 12  | #610F12 | deep reddish brown            | very deep purplish red       | 10RP 1.8/8.4   | Classification mismatch          | Brown Classification Gaps   |
| 13  | #7D423B | moderate reddish brown        | grayish red                  | 2.6R 3.7/6.1   | Classification mismatch          | Brown Classification Gaps   |
| 14  | #461D1E | dark reddish brown            | very dark purplish red       | 10RP 1.5/4.2   | Classification mismatch          | Brown Classification Gaps   |
| 15  | #9E7F7A | light grayish reddish brown   | grayish red                  | 10R 5.4/2.5    | Classification mismatch          | Brown Classification Gaps   |
| 16  | #43292A | dark grayish reddish brown    | very dark purplish red       | 10RP 1.8/2.4   | Classification mismatch          | Brown Classification Gaps   |
| 17  | #8A4416 | strong brown                  | moderate red                 | 5.8R 3.8/10.3  | Classification mismatch          | Brown Classification Gaps   |
| 18  | #571A07 | deep brown                    | very deep red                | 3.1R 1.7/8.0   | Classification mismatch          | Brown Classification Gaps   |
| 19  | #AD7C63 | light brown                   | grayish reddish orange       | 7.2R 5.5/6.3   | Classification mismatch          | Brown Classification Gaps   |
| 20  | #724A38 | moderate brown                | grayish red                  | 6.3R 3.8/5.4   | Classification mismatch          | Brown Classification Gaps   |
| 21  | #442112 | dark brown                    | very dark red                | 5.3R 1.5/5.2   | Classification mismatch          | Brown Classification Gaps   |
| 22  | #997F75 | light grayish brown           | grayish yellowish brown      | 9.1YR 5.4/2.3  | Classification mismatch          | Modifier Inconsistencies    |
| 23  | #3E2C28 | dark grayish brown            | very dark red                | 4.6R 1.8/2.1   | Classification mismatch          | Brown Classification Gaps   |
| 24  | #928281 | light brownish gray           | light -ish gray brown        | 5.4YR 5.4/1.1  | Classification mismatch          | Other Classification Errors |
| 25  | #605251 | brownish gray                 | dark -ish gray red           | 2.5R 3.8/1.0   | Classification mismatch          | Brown Classification Gaps   |
| 26  | #2B211E | brownish black                | blackish red                 | 5.8R 1.2/1.1   | Classification mismatch          | Brown Classification Gaps   |
| 27  | #FFBE50 | brilliant orange yellow       | light orange yellow          | 10YR 8.2/9.9   | Classification mismatch          | Modifier Inconsistencies    |
| 28  | #673F0B | deep yellowish brown          | strong brown                 | 7.4YR 3.1/6.8  | Classification mismatch          | Modifier Inconsistencies    |
| 29  | #886648 | moderate yellowish brown      | grayish reddish orange       | 9.5R 4.5/6.0   | Classification mismatch          | Brown Classification Gaps   |
| 30  | #50341A | dark yellowish brown          | deep reddish brown           | 8.9R 2.3/5.5   | Classification mismatch          | Modifier Inconsistencies    |
| 31  | #B49B8D | light grayish yellowish brown | grayish yellow               | 2.1Y 6.5/2.2   | Classification mismatch          | Brown Classification Gaps   |
| 32  | #7E695D | grayish yellowish brown       | moderate olive brown         | 2.6Y 4.5/2.1   | Classification mismatch          | Modifier Inconsistencies    |
| 33  | #4D3D33 | dark grayish yellowish brown  | grayish reddish brown        | 8.6R 2.7/2.5   | Classification mismatch          | Modifier Inconsistencies    |
| 34  | #EEDFDA | yellowish white               | -ish white yellow            | 9.6YR 9.1/1.4  | Classification mismatch          | Other Classification Errors |
| 35  | #C6B9B1 | yellowish gray                | -ish gray yellow             | 2.2Y 7.5/1.7   | Classification mismatch          | Other Classification Errors |
| 36  | #997736 | light olive brown             | brownish orange              | 2YR 5.1/9.5    | Classification mismatch          | Modifier Inconsistencies    |
| 37  | #3F2C10 | dark olive brown              | deep reddish brown           | 10R 1.8/5.1    | Classification mismatch          | Modifier Inconsistencies    |
| 38  | #64591A | moderate olive                | strong brown                 | 5.2YR 3.7/8.2  | Classification mismatch          | Modifier Inconsistencies    |
| 39  | #352E0A | dark olive                    | deep brown                   | 5YR 1.7/5.3    | Classification mismatch          | Modifier Inconsistencies    |
| 40  | #8E856F | light grayish olive           | light olive brown            | 2.8Y 5.4/2.0   | Classification mismatch          | Modifier Inconsistencies    |
| 41  | #5D553F | grayish olive                 | moderate brown               | 4.3YR 3.8/3.5  | Classification mismatch          | Modifier Inconsistencies    |
| 42  | #35301C | dark grayish olive            | dark brown                   | 5YR 1.8/3.3    | Classification mismatch          | Modifier Inconsistencies    |
| 43  | #8F877F | light olive gray              | pale yellowish brown         | 10YR 5.5/1.3   | Classification mismatch          | Modifier Inconsistencies    |
| 44  | #58514A | olive gray                    | -ish gray brown              | 1.2YR 3.7/1.1  | Classification mismatch          | Modifier Inconsistencies    |
| 45  | #23211C | olive black                   | -ish black brown             | 4.3YR 1.1/0.8  | Classification mismatch          | Modifier Inconsistencies    |
| 46  | #2C5506 | strong olive green            | moderate olive brown         | 4Y 3.3/9.6     | Classification mismatch          | Modifier Inconsistencies    |
| 47  | #495B22 | moderate olive green          | strong yellowish brown       | 10YR 3.8/7.4   | Classification mismatch          | Modifier Inconsistencies    |
| 48  | #20340B | dark olive green              | dark olive brown             | 3Y 1.7/5.8     | Classification mismatch          | Hue Family Errors           |
| 49  | #2F3326 | dark grayish olive green      | dark grayish yellowish brown | 10YR 1.8/1.9   | Classification mismatch          | Hue Family Errors           |
| 50  | #054208 | very deep yellowish green     | dark olive                   | 6.9Y 2.1/8.5   | Classification mismatch          | Modifier Inconsistencies    |
| 51  | #2F5D3A | dark yellowish green          | moderate olive               | 8.8Y 3.8/5.0   | Classification mismatch          | Modifier Inconsistencies    |
| 52  | #10361A | very dark yellowish green     | dark olive                   | 8.7Y 1.7/4.5   | Classification mismatch          | Modifier Inconsistencies    |
| 53  | #0C2E24 | very dark green               | very dark yellowish green    | 8.4GY 1.5/2.2  | Classification mismatch          | Modifier Inconsistencies    |
| 54  | #1F2A2A | blackish green                | -ish black green             | 1BG 1.4/0.7    | Classification mismatch          | Value Classification Errors |
| 55  | #E0E2E5 | greenish white                | -ish white green             | 1.1G 9.1/1.2   | Classification mismatch          | Other Classification Errors |
| 56  | #BABEC1 | light greenish gray           | light -ish gray green        | 3.1G 7.6/1.2   | Classification mismatch          | Other Classification Errors |
| 57  | #848888 | greenish gray                 | -ish gray green              | 8.8GY 5.5/0.8  | Classification mismatch          | Other Classification Errors |
| 58  | #545858 | dark greenish gray            | dark -ish gray green         | 7.2GY 3.8/0.5  | Classification mismatch          | Other Classification Errors |
| 59  | #212626 | greenish black                | black                        | 1BG 1.3/0.4    | Classification mismatch          | Modifier Inconsistencies    |
| 60  | #2A7691 | moderate greenish blue        | moderate bluish green        | 9.8BG 4.6/6.0  | Classification mismatch          | Hue Family Errors           |
| 61  | #1B5CD7 | vivid blue                    | vivid purplish blue          | 6.5PB 4.2/16.3 | Classification mismatch          | Modifier Inconsistencies    |
| 62  | #323F4E | dark grayish blue             | dark blue                    | 10B 2.5/2.2    | Classification mismatch          | Modifier Inconsistencies    |
| 63  | #1E2531 | blackish blue                 | very dark greenish blue      | 4.3B 1.3/2.1   | Classification mismatch          | Modifier Inconsistencies    |
| 64  | #E1E1F1 | bluish white                  | -ish white blue              | 1.4PB 9.1/1.3  | Classification mismatch          | Other Classification Errors |
| 65  | #B7B8C6 | light bluish gray             | light -ish gray blue         | 4.5PB 7.5/1.4  | Classification mismatch          | Other Classification Errors |
| 66  | #838793 | bluish gray                   | grayish blue                 | 6.3PB 5.5/1.5  | Classification mismatch          | Modifier Inconsistencies    |
| 67  | #50545F | dark bluish gray              | grayish blue                 | 5.9PB 3.8/1.5  | Classification mismatch          | Modifier Inconsistencies    |
| 68  | #24272E | bluish black                  | blackish blue                | 4.7B 1.4/1.0   | Classification mismatch          | Value Classification Errors |
| 69  | #2A286F | deep purplish blue            | deep greenish blue           | 7.4B 1.9/7.2   | Classification mismatch          | Other Classification Errors |
| 70  | #222248 | dark purplish blue            | very dark greenish blue      | 7.3B 1.4/4.7   | Classification mismatch          | Modifier Inconsistencies    |
| 71  | #3C1668 | deep violet                   | dark blue                    | 9.6B 1.6/6.7   | Classification mismatch          | Modifier Inconsistencies    |
| 72  | #34254D | dark violet                   | dark blue                    | 9.6B 1.6/4.4   | Classification mismatch          | Other Classification Errors |
| 73  | #584E72 | grayish violet                | grayish blue                 | 9.2B 3.8/4.2   | Classification mismatch          | Other Classification Errors |
| 74  | #563762 | dark purple                   | dark blue                    | 3.1PB 2.8/4.3  | Classification mismatch          | Hue Family Errors           |
| 75  | #371B41 | very dark purple              | dark blue                    | 3.1PB 1.4/3.7  | Classification mismatch          | Modifier Inconsistencies    |
| 76  | #AD97B3 | pale purple                   | None                         | 7.9P 6.4/3.9   | No ISCC-NBS classification found | No Classification Found     |
| 77  | #513F51 | dark grayish purple           | dark grayish blue            | 6.7PB 2.9/1.7  | Classification mismatch          | Hue Family Errors           |
| 78  | #2F2231 | blackish purple               | blackish blue                | 5.1PB 1.4/1.8  | Classification mismatch          | Hue Family Errors           |
| 79  | #EBDFEF | purplish white                | pale purplish pink           | 9.6P 9.1/1.6   | Classification mismatch          | Modifier Inconsistencies    |
| 80  | #C3B7C6 | light purplish gray           | pale purplish pink           | 9.3P 7.5/1.8   | Classification mismatch          | Modifier Inconsistencies    |
| 81  | #8F8490 | purplish gray                 | pale purple                  | 8.5P 5.5/1.8   | Classification mismatch          | Modifier Inconsistencies    |
| 82  | #5C525E | dark purplish gray            | dark -ish gray blue          | 4.9PB 3.8/1.1  | Classification mismatch          | Other Classification Errors |
| 83  | #2B2630 | purplish black                | blackish blue                | 1.3PB 1.4/1.1  | Classification mismatch          | Value Classification Errors |
| 84  | #4F094A | very deep reddish purple      | dark violet                  | 8.2PB 1.5/4.6  | Classification mismatch          | Modifier Inconsistencies    |
| 85  | #965888 | moderate reddish purple       | grayish violet               | 10PB 4.5/4.5   | Classification mismatch          | Modifier Inconsistencies    |
| 86  | #5F3458 | dark reddish purple           | grayish violet               | 9.4PB 2.8/3.5  | Classification mismatch          | Modifier Inconsistencies    |
| 87  | #DD2388 | vivid purplish red            | vivid purplish pink          | 5.9RP 4.9/16.7 | Classification mismatch          | Hue Family Errors           |
| 88  | #B83773 | strong purplish red           | strong purplish pink         | 6.7RP 4.4/12.1 | Classification mismatch          | Hue Family Errors           |
| 89  | #54063C | very deep purplish red        | very dark purple             | 5.7P 1.5/4.4   | Classification mismatch          | Red/Purple Confusion        |
| 90  | #431432 | very dark purplish red        | very dark purple             | 5.5P 1.3/3.2   | Classification mismatch          | Red/Purple Confusion        |
| 91  | #B2879B | light grayish purplish red    | pale purplish red            | 6RP 6.0/3.9    | Classification mismatch          | Modifier Inconsistencies    |
| 92  | #E7E1E9 | white                         | very pale green              | 8.4GY 9.1/1.4  | Classification mismatch          | Modifier Inconsistencies    |
| 93  | #BDB7BF | light gray                    | light -ish gray purple       | 5.2P 7.5/1.4   | Classification mismatch          | Modifier Inconsistencies    |
| 94  | #8A8489 | medium gray                   | -ish gray green              | 7.1GY 5.4/0.9  | Classification mismatch          | Modifier Inconsistencies    |
| 95  | #585458 | dark gray                     | dark -ish gray green         | 7.2GY 3.8/0.5  | Classification mismatch          | Modifier Inconsistencies    |
| 96  | #2B292B | black                         | black                        | 6.7PB 1.5/0.1  | Classification mismatch          | Other Classification Errors |

## Recommendations

### Modifier Inconsistencies (48 failures)

1. Standardize modifier application logic
2. Review value/chroma thresholds for modifiers like 'vivid', 'deep'
3. Ensure consistent polygon boundary rules

### Brown Classification Gaps (16 failures)

1. Expand brown polygon coverage in low-chroma, medium-value regions
2. Review brown vs orange/yellow boundary definitions
3. Add more brown polygon regions for comprehensive coverage

### Other Classification Errors (14 failures)

1. Investigate specific failure patterns
2. Review relevant polygon definitions and boundaries
3. Consider algorithm improvements for this category

### Hue Family Errors (8 failures)

1. Investigate specific failure patterns
2. Review relevant polygon definitions and boundaries
3. Consider algorithm improvements for this category

### Red/Purple Confusion (6 failures)

1. Review hue boundary definitions between R, RP, and P families
2. Check polygon overlap at red-purple transition zones
3. Verify mechanical wedge system hue angle calculations

---

Report generated by MunsellSpace Classification Accuracy Analysis Tool
