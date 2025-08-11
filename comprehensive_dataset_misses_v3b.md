# Comprehensive Conversion Dataset - Mismatches Analysis V3b (FIXED)

Generated: 1754927100

## Configuration

- Converter: Restored breakthrough mathematical converter (60.4% baseline)
- Chromatic Adaptation: XYZScaling
- Illuminants tested: C, D65, F7
- **FIX**: Python errors now counted as failures
- **FIX**: Expected names properly parsed
- **FIX**: Statistics based on unique colors, not total tests

## W3 Dataset Results

### Overall Statistics

- Unique colors in dataset: 267

### Accuracy by Illuminant (W3)

| Illuminant | Rust Correct | Python Correct | Python Errors | Rust Unknown | Python Unknown | Rust Accuracy | Python Accuracy |
| ---------- | ------------ | -------------- | ------------- | ------------ | -------------- | ------------- | --------------- |
| C          | 188          | 165            | 50            | 4            | 2              | 70.4%         | 61.8%           |
| D65        | 131          | 126            | 47            | 1            | 1              | 49.1%         | 47.2%           |
| F7         | 131          | 125            | 48            | 1            | 1              | 49.1%         | 46.8%           |

## Centore Dataset Results

### Overall Statistics

- Unique colors in dataset: 260

### Accuracy by Illuminant (Centore)

| Illuminant | Rust Correct | Python Correct | Python Errors | Rust Unknown | Python Unknown | Rust Accuracy | Python Accuracy |
| ---------- | ------------ | -------------- | ------------- | ------------ | -------------- | ------------- | --------------- |
| C          | 190          | 178            | 42            | 2            | 2              | 73.1%         | 68.5%           |
| D65        | 259          | 213            | 46            | 1            | 1              | 99.6%         | 81.9%           |
| F7         | 259          | 214            | 45            | 1            | 1              | 99.6%         | 82.3%           |

## Detailed Mismatch Analysis (First 5 per illuminant)

### W3 Dataset - Detailed Mismatches

#### Illuminant C - W3 Mismatches

**Color: #FFB5BA - Expected: "vivid pink"**

- Rust: 0.7R 8.0/6.8 → "light pink" ✗
- Python: 1.0R 8.0/6.6 → "moderate pink" ✗

**Color: #EAE3E1 - Expected: "-ish white pink"**

- Rust: 8.7R 9.1/0.7 → "pinkish white" ✗
- Python: ERROR → "Error" ERROR

**Color: #C1B6B3 - Expected: "-ish gray pink"**

- Rust: 9.2R 7.4/1.1 → "pinkish gray" ✗
- Python: ERROR → "Error" ERROR

**Color: #3F1728 - Expected: "very dark red"**

- Rust: 1.0R 1.4/4.2 → "very dark purplish red" ✗
- Python: 1.0R 1.4/4.0 → "very dark purplish red" ✗

**Color: #AD8884 - Expected: "pale red"**

- Rust: 5.7R 5.9/3.4 → "light grayish red" ✗
- Python: 6.2R 5.9/3.3 → "light grayish red" ✗

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

**Color: #AD97B3 - Expected: "pale purple"**

- Rust: 6.9P 6.4/3.2 → "Unknown" ✗
- Python: 6.8P 6.4/3.2 → "Unknown" ✗

#### Illuminant F7 - Centore Mismatches

**Color: #AD97B3 - Expected: "pale purple"**

- Rust: 6.9P 6.4/3.2 → "Unknown" ✗
- Python: 6.9P 6.4/3.2 → "Unknown" ✗

## Summary

### Key Findings:

1. Python errors are now properly counted as failures
2. "Unknown" classifications may indicate colors outside ISCC-NBS boundaries
3. Expected names now correctly parsed from W3 dataset
4. Statistics based on unique colors, not total tests
