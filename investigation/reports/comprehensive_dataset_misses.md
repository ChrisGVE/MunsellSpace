# Comprehensive Conversion Dataset - Mismatches Analysis

## Configuration

- **Illuminants**: C, D65, F7
- **Adaptations**: XYZScaling, Bradford, CAT02
- **Converter**: Mathematical v1 (Original) only
- **Hue Methods**: Method 1 (IncludeStartExcludeEnd), Method 2 (ExcludeStartIncludeEnd)
- **Python Reference**: colour-science library for ground truth comparison

## W3 ISCC-NBS Dataset (267 colors)

### Summary Statistics

| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy |
| ---------- | ---------- | ----------------- | ----------------- |
| C          | XYZScaling | 46.8%             | 53.9%             |
| C          | Bradford   | 46.4%             | 52.1%             |
| C          | CAT02      | 45.7%             | 51.3%             |
| D65        | XYZScaling | 28.1%             | 30.3%             |
| D65        | Bradford   | 28.1%             | 30.3%             |
| D65        | CAT02      | 28.1%             | 30.3%             |
| F7         | XYZScaling | 28.1%             | 30.3%             |
| F7         | Bradford   | 28.1%             | 30.3%             |
| F7         | CAT02      | 28.5%             | 30.7%             |

### Detailed Mismatches

**Note**: Statistics shown are commented out pending correction

#### 1. Expected: vivid pink

Hex: #FFB5BA

| Illuminant | Adaptation | Munsell      | Py Colour                                                                                           | Method 1             | M1✓ | Method 2             | M2✓ | Boundary |
| ---------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------- | -------------------- | --- | -------------------- | --- | -------- |
| C          | XYZScaling | 5.4R 8.0/5.5 | 1.0R 8.0/6.6                                                                                        | light yellowish pink | ❌  | light pink           | ❌  | 0.10     |
| C          | Bradford   | 5.4R 8.0/5.4 | 1.0R 8.0/6.6                                                                                        | light yellowish pink | ❌  | light pink           | ❌  | 0.10     |
| C          | CAT02      | 5.4R 8.0/5.4 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | light yellowish pink | ❌  | light pink           | ❌  | 0.10     |
| D65        | XYZScaling | 7.0R 8.0/5.3 | 4.7R 8.0/6.0                                                                                        | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 7.0R 8.0/5.3 | 4.7R 8.0/6.0                                                                                        | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 7.0R 8.0/5.3 | 4.7R 8.0/6.0                                                                                        | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 7.0R 8.0/5.3 | 4.8R 8.0/6.0                                                                                        | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 7.0R 8.0/5.3 | 4.8R 8.0/6.0                                                                                        | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 7.0R 8.0/5.3 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |

#### 2. Expected: strong pink

Hex: #EA9399

| Illuminant | Adaptation | Munsell      | Py Colour                                                                                           | Method 1                | M1✓ | Method 2                | M2✓ | Boundary |
| ---------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------- | ----------------------- | --- | ----------------------- | --- | -------- |
| C          | XYZScaling | 5.6R 6.9/6.8 | 1.6R 6.9/8.0                                                                                        | moderate pink           | ❌  | moderate pink           | ❌  | 0.10     |
| C          | Bradford   | 5.6R 6.9/6.7 | 1.6R 6.9/8.0                                                                                        | moderate pink           | ❌  | moderate pink           | ❌  | 0.10     |
| C          | CAT02      | 5.6R 6.9/6.6 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | moderate pink           | ❌  | moderate pink           | ❌  | 0.10     |
| D65        | XYZScaling | 6.9R 6.9/6.6 | 4.2R 6.9/7.4                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 6.9R 6.9/6.6 | 4.2R 6.9/7.4                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 6.9R 6.9/6.6 | 4.2R 6.9/7.4                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 6.9R 6.9/6.6 | 4.3R 6.9/7.4                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 6.9R 6.9/6.6 | 4.3R 6.9/7.4                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 6.9R 6.9/6.6 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |

#### 3. Expected: deep pink

Hex: #E4717A

| Illuminant | Adaptation | Munsell      | Py Colour                                                                                           | Method 1            | M1✓ | Method 2            | M2✓ | Boundary |
| ---------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------- | ------------------- | --- | ------------------- | --- | -------- |
| C          | XYZScaling | 5.9R 6.0/9.3 | 2.5R 6.0/10.7                                                                                       | deep yellowish pink | ❌  | deep pink           | ✅  | 0.10     |
| C          | Bradford   | 6.0R 6.0/9.1 | 2.5R 6.0/10.7                                                                                       | deep yellowish pink | ❌  | deep pink           | ✅  | 0.10     |
| C          | CAT02      | 6.0R 6.0/9.0 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | deep yellowish pink | ❌  | deep pink           | ✅  | 0.10     |
| D65        | XYZScaling | 6.7R 6.0/9.0 | 4.0R 6.0/10.3                                                                                       | deep yellowish pink | ❌  | deep yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 6.7R 6.0/9.0 | 4.0R 6.0/10.3                                                                                       | deep yellowish pink | ❌  | deep yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 6.7R 6.0/9.0 | 4.0R 6.0/10.3                                                                                       | deep yellowish pink | ❌  | deep yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 6.8R 6.0/9.0 | 4.0R 6.0/10.3                                                                                       | deep yellowish pink | ❌  | deep yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 6.8R 6.0/9.0 | 4.0R 6.0/10.3                                                                                       | deep yellowish pink | ❌  | deep yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 6.8R 6.0/9.0 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | deep yellowish pink | ❌  | deep yellowish pink | ❌  | 0.10     |

#### 4. Expected: light pink

Hex: #F9CCCA

| Illuminant | Adaptation | Munsell       | Py Colour                                                                                           | Method 1             | M1✓ | Method 2             | M2✓ | Boundary |
| ---------- | ---------- | ------------- | --------------------------------------------------------------------------------------------------- | -------------------- | --- | -------------------- | --- | -------- |
| C          | XYZScaling | 6.3R 8.5/3.5  | 3.4R 8.5/3.9                                                                                        | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| D65        | XYZScaling | 0.8YR 8.5/3.2 | 0.3YR 8.5/3.2                                                                                       | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 0.8YR 8.5/3.2 | 0.3YR 8.5/3.2                                                                                       | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 0.8YR 8.5/3.2 | 0.3YR 8.5/3.2                                                                                       | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 0.9YR 8.5/3.2 | 0.3YR 8.5/3.3                                                                                       | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 0.9YR 8.5/3.2 | 0.3YR 8.5/3.3                                                                                       | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 1.0YR 8.5/3.2 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | light yellowish pink | ❌  | light yellowish pink | ❌  | 0.10     |

#### 5. Expected: moderate pink

Hex: #DEA5A4

| Illuminant | Adaptation | Munsell      | Py Colour                                                                                           | Method 1                | M1✓ | Method 2                | M2✓ | Boundary |
| ---------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------- | ----------------------- | --- | ----------------------- | --- | -------- |
| C          | XYZScaling | 6.2R 7.2/4.6 | 3.3R 7.2/5.2                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| C          | Bradford   | 6.4R 7.2/4.5 | 3.3R 7.2/5.2                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| C          | CAT02      | 6.4R 7.2/4.5 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| D65        | XYZScaling | 8.4R 7.2/4.4 | 7.7R 7.2/4.5                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 8.4R 7.2/4.4 | 7.7R 7.2/4.5                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 8.4R 7.2/4.4 | 7.7R 7.2/4.5                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 8.4R 7.2/4.4 | 7.8R 7.2/4.5                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 8.4R 7.2/4.4 | 7.8R 7.2/4.5                                                                                        | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 8.4R 7.2/4.4 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | moderate yellowish pink | ❌  | moderate yellowish pink | ❌  | 0.10     |

## Paul Centore Dataset (260 colors)

### Summary Statistics

| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy |
| ---------- | ---------- | ----------------- | ----------------- |
| C          | XYZScaling | 51.2%             | 52.3%             |
| C          | Bradford   | 51.5%             | 53.1%             |
| C          | CAT02      | 51.9%             | 53.5%             |
| D65        | XYZScaling | 57.3%             | 61.9%             |
| D65        | Bradford   | 57.3%             | 61.9%             |
| D65        | CAT02      | 57.3%             | 61.9%             |
| F7         | XYZScaling | 58.5%             | 63.1%             |
| F7         | Bradford   | 58.1%             | 62.7%             |
| F7         | CAT02      | 58.1%             | 62.7%             |

### Detailed Mismatches

#### 1. Expected: vivid pink

Hex: #FD7992

| Illuminant | Adaptation | Munsell        | Py Colour                                                                                           | Method 1              | M1✓ | Method 2              | M2✓ | Boundary |
| ---------- | ---------- | -------------- | --------------------------------------------------------------------------------------------------- | --------------------- | --- | --------------------- | --- | -------- |
| C          | XYZScaling | 6.0RP 6.6/15.9 | 9.9RP 6.6/12.1                                                                                      | strong purplish pink  | ❌  | strong purplish pink  | ❌  | 0.10     |
| C          | Bradford   | 6.2RP 6.6/15.3 | 9.9RP 6.6/12.1                                                                                      | strong purplish pink  | ❌  | strong purplish pink  | ❌  | 0.10     |
| C          | CAT02      | 6.2RP 6.6/15.2 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | strong purplish pink  | ❌  | strong purplish pink  | ❌  | 0.10     |
| D65        | XYZScaling | 5.6R 6.6/9.5   | 1.2R 6.6/11.7                                                                                       | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 5.6R 6.6/9.5   | 1.2R 6.6/11.7                                                                                       | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 5.6R 6.6/9.5   | 1.2R 6.6/11.7                                                                                       | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 5.6R 6.6/9.5   | 1.2R 6.6/11.7                                                                                       | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 5.6R 6.6/9.5   | 1.2R 6.6/11.7                                                                                       | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 5.6R 6.6/9.5   | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |

#### 2. Expected: strong pink

Hex: #F48FA0

| Illuminant | Adaptation | Munsell        | Py Colour                                                                                           | Method 1              | M1✓ | Method 2              | M2✓ | Boundary |
| ---------- | ---------- | -------------- | --------------------------------------------------------------------------------------------------- | --------------------- | --- | --------------------- | --- | -------- |
| C          | XYZScaling | 5.6RP 7.0/12.0 | 9.4RP 7.0/9.5                                                                                       | strong purplish pink  | ❌  | strong purplish pink  | ❌  | 0.10     |
| C          | Bradford   | 4.9R 7.0/7.3   | 9.4RP 7.0/9.5                                                                                       | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| C          | CAT02      | 4.9R 7.0/7.3   | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| D65        | XYZScaling | 5.6R 7.0/7.3   | 1.4R 7.0/8.9                                                                                        | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| D65        | Bradford   | 5.6R 7.0/7.3   | 1.4R 7.0/8.9                                                                                        | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| D65        | CAT02      | 5.6R 7.0/7.3   | 1.4R 7.0/8.9                                                                                        | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| F7         | XYZScaling | 5.6R 7.0/7.3   | 1.4R 7.0/8.9                                                                                        | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| F7         | Bradford   | 5.6R 7.0/7.3   | 1.4R 7.0/8.9                                                                                        | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |
| F7         | CAT02      | 5.6R 7.0/7.3   | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | strong yellowish pink | ❌  | strong yellowish pink | ❌  | 0.10     |

#### 3. Expected: deep pink

Hex: #E66980

| Illuminant | Adaptation | Munsell      | Py Colour                                                                                           | Method 1            | M1✓ | Method 2  | M2✓ | Boundary |
| ---------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------- | ------------------- | --- | --------- | --- | -------- |
| C          | XYZScaling | 5.6R 5.9/9.3 | 0.3R 5.9/11.8                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| C          | Bradford   | 5.6R 5.9/9.1 | 0.3R 5.9/11.8                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| C          | CAT02      | 5.6R 5.9/9.0 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| D65        | XYZScaling | 5.7R 5.9/9.2 | 1.6R 5.9/11.3                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| D65        | Bradford   | 5.7R 5.9/9.2 | 1.6R 5.9/11.3                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| D65        | CAT02      | 5.7R 5.9/9.2 | 1.6R 5.9/11.3                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| F7         | XYZScaling | 5.7R 5.9/9.2 | 1.6R 5.9/11.3                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| F7         | Bradford   | 5.7R 5.9/9.3 | 1.6R 5.9/11.3                                                                                       | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |
| F7         | CAT02      | 5.7R 5.9/9.2 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | deep yellowish pink | ❌  | deep pink | ✅  | 0.10     |

#### 4. Expected: light pink

Hex: #F8C3CE

| Illuminant | Adaptation | Munsell       | Py Colour                                                                                           | Method 1             | M1✓ | Method 2            | M2✓ | Boundary |
| ---------- | ---------- | ------------- | --------------------------------------------------------------------------------------------------- | -------------------- | --- | ------------------- | --- | -------- |
| C          | XYZScaling | 4.2RP 8.3/6.0 | 7.2RP 8.3/5.1                                                                                       | light purplish pink  | ❌  | light purplish pink | ❌  | 0.10     |
| D65        | XYZScaling | 5.9R 8.3/3.6  | 2.4R 8.3/4.2                                                                                        | light yellowish pink | ❌  | light pink          | ✅  | 0.10     |
| D65        | Bradford   | 5.9R 8.3/3.6  | 2.4R 8.3/4.2                                                                                        | light yellowish pink | ❌  | light pink          | ✅  | 0.10     |
| D65        | CAT02      | 5.9R 8.3/3.6  | 2.4R 8.3/4.2                                                                                        | light yellowish pink | ❌  | light pink          | ✅  | 0.10     |
| F7         | XYZScaling | 6.0R 8.3/3.6  | 2.5R 8.3/4.2                                                                                        | light yellowish pink | ❌  | light pink          | ✅  | 0.10     |
| F7         | Bradford   | 6.0R 8.3/3.6  | 2.5R 8.3/4.2                                                                                        | light yellowish pink | ❌  | light pink          | ✅  | 0.10     |
| F7         | CAT02      | 6.0R 8.3/3.6  | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | light yellowish pink | ❌  | light pink          | ✅  | 0.10     |

#### 6. Expected: dark pink

Hex: #C5808A

| Illuminant | Adaptation | Munsell       | Py Colour                                                                                           | Method 1            | M1✓ | Method 2           | M2✓ | Boundary |
| ---------- | ---------- | ------------- | --------------------------------------------------------------------------------------------------- | ------------------- | --- | ------------------ | --- | -------- |
| C          | Bradford   | 6.7RP 6.0/8.0 | 9.8RP 6.0/6.6                                                                                       | dark purplish pink  | ❌  | dark purplish pink | ❌  | 0.10     |
| C          | CAT02      | 6.7RP 6.0/7.9 | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | dark purplish pink  | ❌  | dark purplish pink | ❌  | 0.10     |
| D65        | XYZScaling | 6.0R 6.0/5.1  | 2.5R 6.0/6.0                                                                                        | dark yellowish pink | ❌  | dark pink          | ✅  | 0.10     |
| D65        | Bradford   | 6.0R 6.0/5.1  | 2.5R 6.0/6.0                                                                                        | dark yellowish pink | ❌  | dark pink          | ✅  | 0.10     |
| D65        | CAT02      | 6.0R 6.0/5.1  | 2.5R 6.0/6.0                                                                                        | dark yellowish pink | ❌  | dark pink          | ✅  | 0.10     |
| F7         | XYZScaling | 6.0R 6.0/5.1  | 2.6R 6.0/6.0                                                                                        | dark yellowish pink | ❌  | dark pink          | ✅  | 0.10     |
| F7         | Bradford   | 6.0R 6.0/5.1  | 2.6R 6.0/6.0                                                                                        | dark yellowish pink | ❌  | dark pink          | ✅  | 0.10     |
| F7         | CAT02      | 6.0R 6.0/5.1  | ERROR: chromatic_adaptation_CMCCAT2000() missing 2 required positional arguments: 'L_A1' and 'L_A2' | dark yellowish pink | ❌  | dark pink          | ✅  | 0.10     |

## Summary

### Dataset Characteristics

- W3 dataset: 267 colors, 208 with mismatches (77.9%)
- Centore dataset: 260 colors, 161 with mismatches (61.9%)

### Notes

- Python reference values from colour-science library using same illuminant/adaptation
- Boundary distance shows minimum distance to the correct ISCC-NBS polygon in Munsell space
- Statistics corrected to count per-color rather than per-configuration
