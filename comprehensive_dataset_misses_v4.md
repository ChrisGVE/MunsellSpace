# Comprehensive Conversion Dataset - Mismatches Analysis V4

## W3 Dataset

### Summary Statistics

| Illuminant | Total | Rust Correct | Python Correct | Python Errors | Rust Accuracy | Python Accuracy |
| ---------- | ----- | ------------ | -------------- | ------------- | ------------- | --------------- |
| C          | 267   | 221          | 172            | 50            | 82.8%         | 79.3%           |
| D65        | 267   | 134          | 127            | 47            | 50.2%         | 57.7%           |
| F7         | 267   | 134          | 125            | 48            | 50.2%         | 57.1%           |

### Detailed Mismatches (First 5 colors)

**Expected: vivid pink**
Hex: #FFB5BA

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| C          | 0.7R 8.0/6.8 | light pink      | ✗   | 1.0R 8.0/6.6   | moderate pink     | ✗   |

**Expected: very dark red**
Hex: #3F1728

| Illuminant | Rust Munsell | Rust descriptor        | ✓/✗ | Python Munsell | Python descriptor      | ✓/✗ |
| ---------- | ------------ | ---------------------- | --- | -------------- | ---------------------- | --- |
| C          | 1.0R 1.4/4.2 | very dark purplish red | ✗   | 1.0R 1.4/4.0   | very dark purplish red | ✗   |

**Expected: vivid yellowish pink**
Hex: #FFB7A5

| Illuminant | Rust Munsell | Rust descriptor      | ✓/✗ | Python Munsell | Python descriptor    | ✓/✗ |
| ---------- | ------------ | -------------------- | --- | -------------- | -------------------- | --- |
| C          | 7.9R 8.0/6.4 | light yellowish pink | ✗   | 8.4R 8.0/6.1   | light yellowish pink | ✗   |

**Expected: deep yellowish pink**
Hex: #E66721

| Illuminant | Rust Munsell   | Rust descriptor      | ✓/✗ | Python Munsell | Python descriptor    | ✓/✗ |
| ---------- | -------------- | -------------------- | --- | -------------- | -------------------- | --- |
| C          | 0.9YR 5.8/13.8 | vivid reddish orange | ✗   | 1.3YR 5.8/13.4 | vivid reddish orange | ✗   |

**Expected: light yellowish pink**
Hex: #F4C2C2

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| C          | 2.1R 8.2/4.6 | light pink      | ✗   | 2.4R 8.2/4.5   | light pink        | ✗   |

**Expected: vivid pink**
Hex: #FFB5BA

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| D65        | 4.7R 8.0/6.0 | light pink      | ✗   | 4.7R 8.0/6.0   | light pink        | ✗   |

**Expected: strong pink**
Hex: #EA9399

| Illuminant | Rust Munsell | Rust descriptor       | ✓/✗ | Python Munsell | Python descriptor     | ✓/✗ |
| ---------- | ------------ | --------------------- | --- | -------------- | --------------------- | --- |
| D65        | 4.2R 6.9/7.4 | strong yellowish pink | ✗   | 4.2R 6.9/7.4   | strong yellowish pink | ✗   |

**Expected: light pink**
Hex: #F9CCCA

| Illuminant | Rust Munsell  | Rust descriptor      | ✓/✗ | Python Munsell | Python descriptor    | ✓/✗ |
| ---------- | ------------- | -------------------- | --- | -------------- | -------------------- | --- |
| D65        | 0.3YR 8.5/3.3 | light yellowish pink | ✗   | 0.3YR 8.5/3.2  | light yellowish pink | ✗   |

**Expected: moderate pink**
Hex: #DEA5A4

| Illuminant | Rust Munsell | Rust descriptor         | ✓/✗ | Python Munsell | Python descriptor       | ✓/✗ |
| ---------- | ------------ | ----------------------- | --- | -------------- | ----------------------- | --- |
| D65        | 7.7R 7.2/4.5 | moderate yellowish pink | ✗   | 7.7R 7.2/4.5   | moderate yellowish pink | ✗   |

**Expected: dark pink**
Hex: #C08081

| Illuminant | Rust Munsell | Rust descriptor     | ✓/✗ | Python Munsell | Python descriptor   | ✓/✗ |
| ---------- | ------------ | ------------------- | --- | -------------- | ------------------- | --- |
| D65        | 6.2R 5.9/5.4 | dark yellowish pink | ✗   | 6.2R 5.9/5.4   | dark yellowish pink | ✗   |

**Expected: vivid pink**
Hex: #FFB5BA

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| F7         | 4.8R 8.0/6.0 | light pink      | ✗   | 4.8R 8.0/6.0   | light pink        | ✗   |

**Expected: strong pink**
Hex: #EA9399

| Illuminant | Rust Munsell | Rust descriptor       | ✓/✗ | Python Munsell | Python descriptor     | ✓/✗ |
| ---------- | ------------ | --------------------- | --- | -------------- | --------------------- | --- |
| F7         | 4.3R 6.9/7.4 | strong yellowish pink | ✗   | 4.3R 6.9/7.4   | strong yellowish pink | ✗   |

**Expected: light pink**
Hex: #F9CCCA

| Illuminant | Rust Munsell  | Rust descriptor      | ✓/✗ | Python Munsell | Python descriptor    | ✓/✗ |
| ---------- | ------------- | -------------------- | --- | -------------- | -------------------- | --- |
| F7         | 0.3YR 8.5/3.3 | light yellowish pink | ✗   | 0.3YR 8.5/3.3  | light yellowish pink | ✗   |

**Expected: moderate pink**
Hex: #DEA5A4

| Illuminant | Rust Munsell | Rust descriptor         | ✓/✗ | Python Munsell | Python descriptor       | ✓/✗ |
| ---------- | ------------ | ----------------------- | --- | -------------- | ----------------------- | --- |
| F7         | 7.8R 7.2/4.5 | moderate yellowish pink | ✗   | 7.8R 7.2/4.5   | moderate yellowish pink | ✗   |

**Expected: dark pink**
Hex: #C08081

| Illuminant | Rust Munsell | Rust descriptor     | ✓/✗ | Python Munsell | Python descriptor   | ✓/✗ |
| ---------- | ------------ | ------------------- | --- | -------------- | ------------------- | --- |
| F7         | 6.2R 5.9/5.4 | dark yellowish pink | ✗   | 6.3R 5.9/5.4   | dark yellowish pink | ✗   |

## Centore Dataset

### Summary Statistics

| Illuminant | Total | Rust Correct | Python Correct | Python Errors | Rust Accuracy | Python Accuracy |
| ---------- | ----- | ------------ | -------------- | ------------- | ------------- | --------------- |
| C          | 260   | 186          | 176            | 42            | 71.5%         | 80.7%           |
| D65        | 260   | 239          | 205            | 46            | 91.9%         | 95.8%           |
| F7         | 260   | 239          | 206            | 45            | 91.9%         | 95.8%           |

### Detailed Mismatches (First 5 colors)

**Expected: light pink**
Hex: #F8C3CE

| Illuminant | Rust Munsell  | Rust descriptor     | ✓/✗ | Python Munsell | Python descriptor   | ✓/✗ |
| ---------- | ------------- | ------------------- | --- | -------------- | ------------------- | --- |
| C          | 7.1RP 8.3/5.2 | light purplish pink | ✗   | 7.2RP 8.3/5.1  | light purplish pink | ✗   |

**Expected: moderate pink**
Hex: #E2A3AE

| Illuminant | Rust Munsell  | Rust descriptor        | ✓/✗ | Python Munsell | Python descriptor      | ✓/✗ |
| ---------- | ------------- | ---------------------- | --- | -------------- | ---------------------- | --- |
| C          | 8.3RP 7.2/6.3 | moderate purplish pink | ✗   | 8.4RP 7.2/6.0  | moderate purplish pink | ✗   |

**Expected: pale pink**
Hex: #EFD1DC

| Illuminant | Rust Munsell  | Rust descriptor    | ✓/✗ | Python Munsell | Python descriptor  | ✓/✗ |
| ---------- | ------------- | ------------------ | --- | -------------- | ------------------ | --- |
| C          | 4.2RP 8.6/3.7 | pale purplish pink | ✗   | 3.8RP 8.6/3.5  | pale purplish pink | ✗   |

**Expected: grayish pink**
Hex: #CBADB7

| Illuminant | Rust Munsell  | Rust descriptor       | ✓/✗ | Python Munsell | Python descriptor     | ✓/✗ |
| ---------- | ------------- | --------------------- | --- | -------------- | --------------------- | --- |
| C          | 6.6RP 7.3/3.2 | grayish purplish pink | ✗   | 4.5RP 7.3/3.4  | grayish purplish pink | ✗   |

**Expected: pinkish white**
Hex: #EFDDE5

| Illuminant | Rust Munsell  | Rust descriptor    | ✓/✗ | Python Munsell | Python descriptor  | ✓/✗ |
| ---------- | ------------- | ------------------ | --- | -------------- | ------------------ | --- |
| C          | 3.0RP 9.0/2.6 | pale purplish pink | ✗   | 2.6RP 9.0/2.5  | pale purplish pink | ✗   |

**Expected: light grayish red**
Hex: #B4888D

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| D65        | 5.2R 6.0/3.6 | pale red        | ✗   | 5.2R 6.0/3.6   | pale red          | ✗   |

**Expected: light grayish reddish brown**
Hex: #9E7F7A

| Illuminant | Rust Munsell  | Rust descriptor    | ✓/✗ | Python Munsell | Python descriptor  | ✓/✗ |
| ---------- | ------------- | ------------------ | --- | -------------- | ------------------ | --- |
| D65        | 3.0YR 5.5/2.4 | pale reddish brown | ✗   | 3.0YR 5.5/2.4  | pale reddish brown | ✗   |

**Expected: light grayish brown**
Hex: #997F75

| Illuminant | Rust Munsell  | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------- | --------------- | --- | -------------- | ----------------- | --- |
| D65        | 7.3YR 5.4/2.2 | pale brown      | ✗   | 7.3YR 5.4/2.2  | pale brown        | ✗   |

**Expected: light grayish yellowish brown**
Hex: #B49B8D

| Illuminant | Rust Munsell  | Rust descriptor      | ✓/✗ | Python Munsell | Python descriptor    | ✓/✗ |
| ---------- | ------------- | -------------------- | --- | -------------- | -------------------- | --- |
| D65        | 9.3YR 6.5/2.3 | pale yellowish brown | ✗   | 9.3YR 6.5/2.3  | pale yellowish brown | ✗   |

**Expected: light grayish olive**
Hex: #8E856F

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| D65        | 8.2Y 5.5/2.2 | pale olive      | ✗   | 8.2Y 5.5/2.2   | pale olive        | ✗   |

**Expected: light grayish red**
Hex: #B4888D

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| F7         | 5.3R 6.0/3.6 | pale red        | ✗   | 5.3R 6.0/3.6   | pale red          | ✗   |

**Expected: light grayish reddish brown**
Hex: #9E7F7A

| Illuminant | Rust Munsell  | Rust descriptor    | ✓/✗ | Python Munsell | Python descriptor  | ✓/✗ |
| ---------- | ------------- | ------------------ | --- | -------------- | ------------------ | --- |
| F7         | 3.0YR 5.5/2.4 | pale reddish brown | ✗   | 3.0YR 5.5/2.4  | pale reddish brown | ✗   |

**Expected: light grayish brown**
Hex: #997F75

| Illuminant | Rust Munsell  | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------- | --------------- | --- | -------------- | ----------------- | --- |
| F7         | 7.3YR 5.4/2.2 | pale brown      | ✗   | 7.3YR 5.4/2.2  | pale brown        | ✗   |

**Expected: light grayish yellowish brown**
Hex: #B49B8D

| Illuminant | Rust Munsell  | Rust descriptor      | ✓/✗ | Python Munsell | Python descriptor    | ✓/✗ |
| ---------- | ------------- | -------------------- | --- | -------------- | -------------------- | --- |
| F7         | 9.3YR 6.5/2.3 | pale yellowish brown | ✗   | 9.3YR 6.5/2.3  | pale yellowish brown | ✗   |

**Expected: light grayish olive**
Hex: #8E856F

| Illuminant | Rust Munsell | Rust descriptor | ✓/✗ | Python Munsell | Python descriptor | ✓/✗ |
| ---------- | ------------ | --------------- | --- | -------------- | ----------------- | --- |
| F7         | 8.2Y 5.5/2.2 | pale olive      | ✗   | 8.2Y 5.5/2.2   | pale olive        | ✗   |

## Python Errors

### First 5 errors per dataset

#### W3 Dataset Python Errors

| Descriptor       | Hex     | Returned Python Error                                                                                                 |
| ---------------- | ------- | --------------------------------------------------------------------------------------------------------------------- |
| pinkish white    | #EAE3E1 | ERROR: "array([ 9.43793462, 9.0551813 , 0.7188615 , 7. ])" specification chroma must be normalised to domain [2, 50]! |
| pinkish gray     | #C1B6B3 | ERROR: "array([ 9.76980612, 7.41177786, 1.00245538, 7. ])" specification chroma must be normalised to domain [2, 50]! |
| dark grayish red | #543D3F | ERROR: "array([ 2.99032469, 2.80224172, 1.84372743, 7. ])" specification chroma must be normalised to domain [2, 50]! |
| blackish red     | #2E1D21 | ERROR: "array([ 4.03229803, 1.26674496, 1.39799177, 7. ])" specification chroma must be normalised to domain [2, 50]! |
| reddish gray     | #8F817F | ERROR: "array([ 7.4100523 , 5.40961079, 1.20988396, 7. ])" specification chroma must be normalised to domain [2, 50]! |

#### Centore Dataset Python Errors

| Descriptor         | Hex     | Returned Python Error                                                                                                 |
| ------------------ | ------- | --------------------------------------------------------------------------------------------------------------------- |
| blackish red       | #332127 | ERROR: "array([ 1.19199824, 1.48442643, 1.5378845 , 7. ])" specification chroma must be normalised to domain [2, 50]! |
| reddish gray       | #928186 | ERROR: "array([ 5.44787417, 5.45794177, 1.8388855 , 8. ])" specification chroma must be normalised to domain [2, 50]! |
| dark reddish gray  | #5D4E53 | ERROR: "array([ 5.88772911, 3.42928413, 1.32505296, 8. ])" specification chroma must be normalised to domain [2, 50]! |
| reddish black      | #30262B | ERROR: "array([ 6.3657322 , 1.61643972, 0.96025915, 8. ])" specification chroma must be normalised to domain [2, 50]! |
| dark grayish brown | #3E2C28 | ERROR: "array([ 2.41100042, 1.97183673, 1.68372951, 6. ])" specification chroma must be normalised to domain [2, 50]! |
