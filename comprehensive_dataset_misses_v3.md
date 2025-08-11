# Comprehensive Conversion Dataset - Mismatches Analysis V3

Generated: 1754925613

## Configuration

- Converter: Restored breakthrough mathematical converter (60.4% baseline)
- Hue Range Method: ExcludeStartIncludeEnd (Method 2)
- Chromatic Adaptation: XYZScaling
- Illuminants tested: C, D65, F7

## W3 Dataset Results

### Overall Statistics

- Unique colors: 267
- Total tests: 801 (3 illuminants × 267 colors)
- Colors with at least one mismatch: 354/801 (44.2%)

### Accuracy by Illuminant (W3)

| Illuminant | Rust Matches | Python Matches | Python Errors | Rust Accuracy | Python Accuracy |
| ---------- | ------------ | -------------- | ------------- | ------------- | --------------- |
| C          | 187          | 166            | 0             | 70.0%         | 62.2%           |
| D65        | 130          | 124            | 0             | 48.7%         | 46.4%           |
| F7         | 130          | 123            | 0             | 48.7%         | 46.1%           |

## Centore Dataset Results

### Overall Statistics

- Unique colors: 260
- Total tests: 780 (3 illuminants × 260 colors)
- Colors with at least one mismatch: 72/780 (9.2%)

### Accuracy by Illuminant (Centore)

| Illuminant | Rust Matches | Python Matches | Python Errors | Rust Accuracy | Python Accuracy |
| ---------- | ------------ | -------------- | ------------- | ------------- | --------------- |
| C          | 190          | 177            | 0             | 73.1%         | 68.1%           |
| D65        | 259          | 213            | 0             | 99.6%         | 81.9%           |
| F7         | 259          | 214            | 0             | 99.6%         | 82.3%           |

## Sample Mismatches (First 5 per illuminant)

### W3 Dataset Mismatches

#### Illuminant C

| RGB     | Expected        | Rust Result  | Rust ISCC              | Python Result                                                                                                         | Python ISCC            |
| ------- | --------------- | ------------ | ---------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| #FFB5BA | vivid pink      | 0.7R 8.0/6.8 | light pink             | 1.0R 8.0/6.6                                                                                                          | light pink             |
| #EAE3E1 | -ish white pink | 8.7R 9.1/0.7 | pinkish white          | ERROR: "array([ 9.43793462, 9.0551813 , 0.7188615 , 7. ])" specification chroma must be normalised to domain [2, 50]! | Unknown                |
| #C1B6B3 | -ish gray pink  | 9.2R 7.4/1.1 | pinkish gray           | ERROR: "array([ 9.76980612, 7.41177786, 1.00245538, 7. ])" specification chroma must be normalised to domain [2, 50]! | Unknown                |
| #3F1728 | very dark red   | 1.0R 1.4/4.2 | very dark purplish red | 1.0R 1.4/4.0                                                                                                          | very dark purplish red |
| #AD8884 | pale red        | 5.7R 5.9/3.4 | light grayish red      | 6.2R 5.9/3.3                                                                                                          | light grayish red      |

#### Illuminant D65

| RGB     | Expected      | Rust Result   | Rust ISCC               | Python Result | Python ISCC             |
| ------- | ------------- | ------------- | ----------------------- | ------------- | ----------------------- |
| #FFB5BA | vivid pink    | 4.7R 8.0/6.0  | light pink              | 4.7R 8.0/6.0  | light pink              |
| #EA9399 | strong pink   | 4.2R 6.9/7.4  | strong yellowish pink   | 4.2R 6.9/7.4  | strong yellowish pink   |
| #F9CCCA | light pink    | 0.3YR 8.5/3.3 | light yellowish pink    | 0.3YR 8.5/3.2 | light yellowish pink    |
| #DEA5A4 | moderate pink | 7.7R 7.2/4.5  | moderate yellowish pink | 7.7R 7.2/4.5  | moderate yellowish pink |
| #C08081 | dark pink     | 6.2R 5.9/5.4  | dark yellowish pink     | 6.2R 5.9/5.4  | dark yellowish pink     |

#### Illuminant F7

| RGB     | Expected      | Rust Result   | Rust ISCC               | Python Result | Python ISCC             |
| ------- | ------------- | ------------- | ----------------------- | ------------- | ----------------------- |
| #FFB5BA | vivid pink    | 4.8R 8.0/6.0  | light pink              | 4.8R 8.0/6.0  | light pink              |
| #EA9399 | strong pink   | 4.3R 6.9/7.4  | strong yellowish pink   | 4.3R 6.9/7.4  | strong yellowish pink   |
| #F9CCCA | light pink    | 0.3YR 8.5/3.3 | light yellowish pink    | 0.3YR 8.5/3.3 | light yellowish pink    |
| #DEA5A4 | moderate pink | 7.8R 7.2/4.5  | moderate yellowish pink | 7.8R 7.2/4.5  | moderate yellowish pink |
| #C08081 | dark pink     | 6.2R 5.9/5.4  | dark yellowish pink     | 6.3R 5.9/5.4  | dark yellowish pink     |

### Centore Dataset Mismatches

#### Illuminant C

| RGB     | Expected      | Rust Result   | Rust ISCC              | Python Result | Python ISCC            |
| ------- | ------------- | ------------- | ---------------------- | ------------- | ---------------------- |
| #F8C3CE | light pink    | 7.1RP 8.3/5.2 | light purplish pink    | 7.2RP 8.3/5.1 | light purplish pink    |
| #E2A3AE | moderate pink | 8.3RP 7.2/6.3 | moderate purplish pink | 8.4RP 7.2/6.0 | moderate purplish pink |
| #EFD1DC | pale pink     | 4.2RP 8.6/3.7 | pale purplish pink     | 3.8RP 8.6/3.5 | pale purplish pink     |
| #CBADB7 | grayish pink  | 6.6RP 7.3/3.2 | grayish purplish pink  | 4.5RP 7.3/3.4 | grayish purplish pink  |
| #EFDDE5 | pinkish white | 3.0RP 9.0/2.6 | pale purplish pink     | 2.6RP 9.0/2.5 | pale purplish pink     |

#### Illuminant D65

| RGB     | Expected    | Rust Result  | Rust ISCC | Python Result | Python ISCC |
| ------- | ----------- | ------------ | --------- | ------------- | ----------- |
| #AD97B3 | pale purple | 6.9P 6.4/3.2 | Unknown   | 6.8P 6.4/3.2  | Unknown     |

#### Illuminant F7

| RGB     | Expected    | Rust Result  | Rust ISCC | Python Result | Python ISCC |
| ------- | ----------- | ------------ | --------- | ------------- | ----------- |
| #AD97B3 | pale purple | 6.9P 6.4/3.2 | Unknown   | 6.9P 6.4/3.2  | Unknown     |

## Comparison with V2 Results

### V2 Results (mathematical_v2 converter):

- W3 Dataset: Best 53.9% with Illuminant C
- Centore Dataset: Best 63.8% with F7
- Python accuracy: 82.3% on Centore with F7

### V3 Results (breakthrough mathematical converter):

- Using restored 60.4% accuracy baseline version
- Added illuminant configurability with chromatic adaptation
- See accuracy tables above for detailed comparison
