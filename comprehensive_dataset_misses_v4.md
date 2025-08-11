# Comprehensive Conversion Dataset - Mismatches Analysis V4 (COMPREHENSIVE FIX)

Generated: 1754930967

## Configuration

- Converter: Restored breakthrough mathematical converter (60.4% baseline)
- Chromatic Adaptation: XYZScaling
- Illuminants tested: C, D65, F7

## Key Fixes in V4:

- **FIX 1**: Python API mapping: 'XYZ Scaling' (not 'XYZScaling')
- **FIX 2**: Expected names use construct_revised_descriptor() logic
- **FIX 3**: ISCC-NBS classification uses revised_descriptor field
- **FIX 4**: Accuracy calculated as matches / (total - errors)
- **FIX 5**: Track Unknown classifications for investigation
- **FIX 6**: Store actual Python error messages for debugging

## W3 Dataset Results

### Overall Statistics

- Total unique colors: 267

### Accuracy by Illuminant (W3) - FIXED Calculation

| Illuminant | Total | Rust Correct | Python Correct | Python Errors | Effective Pop | Rust Accuracy | Python Accuracy | Rust Unknown | Python Unknown |
| ---------- | ----- | ------------ | -------------- | ------------- | ------------- | ------------- | --------------- | ------------ | -------------- |
| C          | 267   | 221          | 172            | 50            | 217           | 82.8%         | 79.3%           | 4            | 2              |
| D65        | 267   | 134          | 127            | 47            | 220           | 50.2%         | 57.7%           | 1            | 1              |
| F7         | 267   | 134          | 125            | 48            | 219           | 50.2%         | 57.1%           | 1            | 1              |

## Centore Dataset Results

### Overall Statistics

- Total unique colors: 260

### Accuracy by Illuminant (Centore) - FIXED Calculation

| Illuminant | Total | Rust Correct | Python Correct | Python Errors | Effective Pop | Rust Accuracy | Python Accuracy | Rust Unknown | Python Unknown |
| ---------- | ----- | ------------ | -------------- | ------------- | ------------- | ------------- | --------------- | ------------ | -------------- |
| C          | 260   | 186          | 177            | 42            | 218           | 71.5%         | 81.2%           | 2            | 2              |
| D65        | 260   | 239          | 205            | 46            | 214           | 91.9%         | 95.8%           | 1            | 1              |
| F7         | 260   | 239          | 206            | 45            | 215           | 91.9%         | 95.8%           | 1            | 1              |

## Python Error Analysis

### Sample Python Errors (First 5 per illuminant)

#### Illuminant C - Python Errors

**W3 - Color: #EAE3E1 - Expected: "pinkish white"**

- Rust: 8.7R 9.1/0.7 → "pinkish white" ✓
- Python Error: `ERROR: "array([ 9.43793462,  9.0551813 ,  0.7188615 ,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #C1B6B3 - Expected: "pinkish gray"**

- Rust: 9.2R 7.4/1.1 → "pinkish gray" ✓
- Python Error: `ERROR: "array([ 9.76980612,  7.41177786,  1.00245538,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #543D3F - Expected: "dark grayish red"**

- Rust: 2.7R 2.8/1.9 → "dark grayish red" ✓
- Python Error: `ERROR: "array([ 2.99032469,  2.80224172,  1.84372743,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #2E1D21 - Expected: "blackish red"**

- Rust: 3.9R 1.3/1.5 → "blackish red" ✓
- Python Error: `ERROR: "array([ 4.03229803,  1.26674496,  1.39799177,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #8F817F - Expected: "reddish gray"**

- Rust: 6.9R 5.4/1.3 → "reddish gray" ✓
- Python Error: `ERROR: "array([ 7.4100523 ,  5.40961079,  1.20988396,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

#### Illuminant D65 - Python Errors

**W3 - Color: #EAD8D7 - Expected: "pale pink"**

- Rust: 8.8YR 8.7/1.1 → "yellowish white" ✗
- Python Error: `ERROR: "array([ 8.89119271,  8.74717951,  1.13746344,  6.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #C4AEAD - Expected: "grayish pink"**

- Rust: 5.4YR 7.2/1.5 → "brownish pink" ✗
- Python Error: `ERROR: "array([ 5.37454125,  7.21094898,  1.48735216,  6.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #EAE3E1 - Expected: "pinkish white"**

- Rust: 2.3GY 9.1/0.8 → "yellowish white" ✗
- Python Error: `ERROR: "array([ 2.2962285 ,  9.05538813,  0.83433887,  4.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #C1B6B3 - Expected: "pinkish gray"**

- Rust: 4.2Y 7.4/0.9 → "yellowish gray" ✗
- Python Error: `ERROR: "array([ 4.25367892,  7.41207592,  0.92686117,  5.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #543D3F - Expected: "dark grayish red"**

- Rust: 8.2R 2.8/1.6 → "grayish reddish brown" ✗
- Python Error: `ERROR: "array([ 8.14029075,  2.80094519,  1.64257188,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

#### Illuminant F7 - Python Errors

**W3 - Color: #EAD8D7 - Expected: "pale pink"**

- Rust: 8.9YR 8.7/1.2 → "yellowish white" ✗
- Python Error: `ERROR: "array([ 8.90980652,  8.74722252,  1.15122854,  6.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #C4AEAD - Expected: "grayish pink"**

- Rust: 5.4YR 7.2/1.5 → "brownish pink" ✗
- Python Error: `ERROR: "array([ 5.43319755,  7.21100317,  1.49844129,  6.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #EAE3E1 - Expected: "pinkish white"**

- Rust: 2.2GY 9.1/0.8 → "yellowish white" ✗
- Python Error: `ERROR: "array([ 2.10814781,  9.05541097,  0.8455287 ,  4.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #C1B6B3 - Expected: "pinkish gray"**

- Rust: 4.3Y 7.4/0.9 → "yellowish gray" ✗
- Python Error: `ERROR: "array([ 4.21101266,  7.41211292,  0.93906721,  5.        ])" specification chroma must be normalised to domain [2, 50]!`

**W3 - Color: #543D3F - Expected: "dark grayish red"**

- Rust: 8.2R 2.8/1.6 → "grayish reddish brown" ✗
- Python Error: `ERROR: "array([ 8.20490786,  2.80099829,  1.646625  ,  7.        ])" specification chroma must be normalised to domain [2, 50]!`

## Unknown Classification Analysis

### Colors Classified as "Unknown" (First 5 per illuminant)

These may be outside ISCC-NBS polygon boundaries or neutral colors.

#### Illuminant C - Unknown Classifications

**W3 - Color: #C19A6B - Expected: "light yellowish brown"**

- Rust: 8.7YR 6.5/5.0 → "Unknown" ✗ (UNKNOWN)
- Python: 9.1YR 6.5/4.9 → "light yellowish brown" ✓

**W3 - Color: #AA98A9 - Expected: "pale purple"**

- Rust: 7.8P 6.4/3.1 → "Unknown" ✗ (UNKNOWN)
- Python: 7.8P 6.4/3.0 → "pale purple" ✓

**W3 - Color: #555555 - Expected: "dark grey"**

- Rust: 0.0N 3.6/0.0 → "Unknown" ✗ (UNKNOWN)
- Python: N3.6 → "Unknown" ✗ (UNKNOWN)

**W3 - Color: #222222 - Expected: "black"**

- Rust: 0.0N 1.3/0.0 → "Unknown" ✗ (UNKNOWN)
- Python: N1.3 → "Unknown" ✗ (UNKNOWN)

**Centore - Color: #B4888D - Expected: "light grayish red"**

- Rust: 9.8RP 6.0/4.4 → "Unknown" ✗ (UNKNOWN)
- Python: 10.0RP 6.0/4.2 → "Unknown" ✗ (UNKNOWN)

#### Illuminant D65 - Unknown Classifications

**W3 - Color: #C19A6B - Expected: "light yellowish brown"**

- Rust: 1.0Y 6.5/5.1 → "Unknown" ✗ (UNKNOWN)
- Python: 1.0Y 6.5/5.1 → "Unknown" ✗ (UNKNOWN)

**Centore - Color: #AD97B3 - Expected: "pale purple"**

- Rust: 6.9P 6.4/3.2 → "Unknown" ✗ (UNKNOWN)
- Python: 6.8P 6.4/3.2 → "Unknown" ✗ (UNKNOWN)

#### Illuminant F7 - Unknown Classifications

**W3 - Color: #C19A6B - Expected: "light yellowish brown"**

- Rust: 1.0Y 6.5/5.1 → "Unknown" ✗ (UNKNOWN)
- Python: 1.0Y 6.5/5.1 → "Unknown" ✗ (UNKNOWN)

**Centore - Color: #AD97B3 - Expected: "pale purple"**

- Rust: 6.9P 6.4/3.2 → "Unknown" ✗ (UNKNOWN)
- Python: 6.9P 6.4/3.2 → "Unknown" ✗ (UNKNOWN)

## Detailed Mismatch Analysis (First 5 per illuminant)

Excludes Python errors and Unknown classifications for focus on actual classification differences.

### W3 Dataset - Detailed Mismatches

#### Illuminant C - W3 Mismatches

**Color: #FFB5BA - Expected: "vivid pink"**

- Rust: 0.7R 8.0/6.8 → "light pink" ✗
- Python: 1.0R 8.0/6.6 → "moderate pink" ✗

**Color: #3F1728 - Expected: "very dark red"**

- Rust: 1.0R 1.4/4.2 → "very dark purplish red" ✗
- Python: 1.0R 1.4/4.0 → "very dark purplish red" ✗

**Color: #FFB7A5 - Expected: "vivid yellowish pink"**

- Rust: 7.9R 8.0/6.4 → "light yellowish pink" ✗
- Python: 8.4R 8.0/6.1 → "light yellowish pink" ✗

**Color: #E66721 - Expected: "deep yellowish pink"**

- Rust: 0.9YR 5.8/13.8 → "vivid reddish orange" ✗
- Python: 1.3YR 5.8/13.4 → "vivid reddish orange" ✗

**Color: #F4C2C2 - Expected: "light yellowish pink"**

- Rust: 2.1R 8.2/4.6 → "light pink" ✗
- Python: 2.4R 8.2/4.5 → "light pink" ✗

#### Illuminant D65 - W3 Mismatches

**Color: #FFB5BA - Expected: "vivid pink"**

- Rust: 4.7R 8.0/6.0 → "light pink" ✗
- Python: 4.7R 8.0/6.0 → "light pink" ✗

**Color: #EA9399 - Expected: "strong pink"**

- Rust: 4.2R 6.9/7.4 → "strong yellowish pink" ✗
- Python: 4.2R 6.9/7.4 → "strong yellowish pink" ✗

**Color: #F9CCCA - Expected: "light pink"**

- Rust: 0.3YR 8.5/3.3 → "light yellowish pink" ✗
- Python: 0.3YR 8.5/3.2 → "light yellowish pink" ✗

**Color: #DEA5A4 - Expected: "moderate pink"**

- Rust: 7.7R 7.2/4.5 → "moderate yellowish pink" ✗
- Python: 7.7R 7.2/4.5 → "moderate yellowish pink" ✗

**Color: #C08081 - Expected: "dark pink"**

- Rust: 6.2R 5.9/5.4 → "dark yellowish pink" ✗
- Python: 6.2R 5.9/5.4 → "dark yellowish pink" ✗

#### Illuminant F7 - W3 Mismatches

**Color: #FFB5BA - Expected: "vivid pink"**

- Rust: 4.8R 8.0/6.0 → "light pink" ✗
- Python: 4.8R 8.0/6.0 → "light pink" ✗

**Color: #EA9399 - Expected: "strong pink"**

- Rust: 4.3R 6.9/7.4 → "strong yellowish pink" ✗
- Python: 4.3R 6.9/7.4 → "strong yellowish pink" ✗

**Color: #F9CCCA - Expected: "light pink"**

- Rust: 0.3YR 8.5/3.3 → "light yellowish pink" ✗
- Python: 0.3YR 8.5/3.3 → "light yellowish pink" ✗

**Color: #DEA5A4 - Expected: "moderate pink"**

- Rust: 7.8R 7.2/4.5 → "moderate yellowish pink" ✗
- Python: 7.8R 7.2/4.5 → "moderate yellowish pink" ✗

**Color: #C08081 - Expected: "dark pink"**

- Rust: 6.2R 5.9/5.4 → "dark yellowish pink" ✗
- Python: 6.3R 5.9/5.4 → "dark yellowish pink" ✗

### Centore Dataset - Detailed Mismatches

#### Illuminant C - Centore Mismatches

**Color: #F8C3CE - Expected: "light pink"**

- Rust: 7.1RP 8.3/5.2 → "light purplish pink" ✗
- Python: 7.2RP 8.3/5.1 → "light purplish pink" ✗

**Color: #E2A3AE - Expected: "moderate pink"**

- Rust: 8.3RP 7.2/6.3 → "moderate purplish pink" ✗
- Python: 8.4RP 7.2/6.0 → "moderate purplish pink" ✗

**Color: #EFD1DC - Expected: "pale pink"**

- Rust: 4.2RP 8.6/3.7 → "pale purplish pink" ✗
- Python: 3.8RP 8.6/3.5 → "pale purplish pink" ✗

**Color: #CBADB7 - Expected: "grayish pink"**

- Rust: 6.6RP 7.3/3.2 → "grayish purplish pink" ✗
- Python: 4.5RP 7.3/3.4 → "grayish purplish pink" ✗

**Color: #EFDDE5 - Expected: "pinkish white"**

- Rust: 3.0RP 9.0/2.6 → "pale purplish pink" ✗
- Python: 2.6RP 9.0/2.5 → "pale purplish pink" ✗

#### Illuminant D65 - Centore Mismatches

**Color: #B4888D - Expected: "light grayish red"**

- Rust: 5.2R 6.0/3.6 → "pale red" ✗
- Python: 5.2R 6.0/3.6 → "pale red" ✗

**Color: #9E7F7A - Expected: "light grayish reddish brown"**

- Rust: 3.0YR 5.5/2.4 → "pale reddish brown" ✗
- Python: 3.0YR 5.5/2.4 → "pale reddish brown" ✗

**Color: #997F75 - Expected: "light grayish brown"**

- Rust: 7.3YR 5.4/2.2 → "pale brown" ✗
- Python: 7.3YR 5.4/2.2 → "pale brown" ✗

**Color: #B49B8D - Expected: "light grayish yellowish brown"**

- Rust: 9.3YR 6.5/2.3 → "pale yellowish brown" ✗
- Python: 9.3YR 6.5/2.3 → "pale yellowish brown" ✗

**Color: #8E856F - Expected: "light grayish olive"**

- Rust: 8.2Y 5.5/2.2 → "pale olive" ✗
- Python: 8.2Y 5.5/2.2 → "pale olive" ✗

#### Illuminant F7 - Centore Mismatches

**Color: #B4888D - Expected: "light grayish red"**

- Rust: 5.3R 6.0/3.6 → "pale red" ✗
- Python: 5.3R 6.0/3.6 → "pale red" ✗

**Color: #9E7F7A - Expected: "light grayish reddish brown"**

- Rust: 3.0YR 5.5/2.4 → "pale reddish brown" ✗
- Python: 3.0YR 5.5/2.4 → "pale reddish brown" ✗

**Color: #997F75 - Expected: "light grayish brown"**

- Rust: 7.3YR 5.4/2.2 → "pale brown" ✗
- Python: 7.3YR 5.4/2.2 → "pale brown" ✗

**Color: #B49B8D - Expected: "light grayish yellowish brown"**

- Rust: 9.3YR 6.5/2.3 → "pale yellowish brown" ✗
- Python: 9.3YR 6.5/2.3 → "pale yellowish brown" ✗

**Color: #8E856F - Expected: "light grayish olive"**

- Rust: 8.2Y 5.5/2.2 → "pale olive" ✗
- Python: 8.2Y 5.5/2.2 → "pale olive" ✗

## Summary

### V4 Comprehensive Fixes Applied:

1. **Python API Fix**: Used 'XYZ Scaling' instead of 'XYZScaling'
2. **ISCC-NBS Fix**: Used revised_descriptor field from construct_revised_descriptor()
3. **Accuracy Fix**: Calculate as matches / (total - errors)
4. **Error Tracking**: Store actual Python error messages for debugging
5. **Unknown Analysis**: Track colors outside ISCC-NBS boundaries
6. **Expected Names**: Apply construct_revised_descriptor() logic to ground truth
