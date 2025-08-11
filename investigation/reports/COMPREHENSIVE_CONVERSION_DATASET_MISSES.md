# Comprehensive Conversion Dataset - Mismatches Analysis

## Configuration
- **Illuminants**: C, D65, F7
- **Adaptations**: XYZScaling, Bradford, CAT02
- **Converter**: Mathematical v1 (Original) only
- **Hue Methods**: Method 1 (IncludeStartExcludeEnd), Method 2 (ExcludeStartIncludeEnd)

## W3 ISCC-NBS Dataset (267 colors)

### Summary Statistics

| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy |
|------------|------------|-------------------|-------------------|
| C | XYZScaling | 47.6% | 53.9% |
| C | Bradford | 47.2% | 51.7% |
| C | CAT02 | 46.4% | 51.3% |
| D65 | XYZScaling | 29.2% | 30.3% |
| D65 | Bradford | 29.2% | 30.3% |
| D65 | CAT02 | 29.2% | 30.3% |
| F7 | XYZScaling | 29.2% | 30.3% |
| F7 | Bradford | 29.2% | 30.3% |
| F7 | CAT02 | 29.6% | 30.7% |

### Detailed Mismatches

#### 1. Expected: vivid pink
Hex: #FFB5BA

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4R 8.0/5.5 | light pink | ❌ | light pink | ❌ | ±0.1 |
| C | Bradford | 5.4R 8.0/5.4 | light pink | ❌ | light pink | ❌ | ±0.1 |
| C | CAT02 | 5.4R 8.0/5.4 | light pink | ❌ | light pink | ❌ | ±0.1 |
| D65 | XYZScaling | 7.0R 8.0/5.3 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 7.0R 8.0/5.3 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 7.0R 8.0/5.3 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 7.0R 8.0/5.3 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 7.0R 8.0/5.3 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 7.0R 8.0/5.3 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |

#### 2. Expected: strong pink
Hex: #EA9399

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.6R 6.9/6.8 | moderate pink | ❌ | moderate pink | ❌ | ±0.1 |
| C | Bradford | 5.6R 6.9/6.7 | moderate pink | ❌ | moderate pink | ❌ | ±0.1 |
| C | CAT02 | 5.6R 6.9/6.6 | moderate pink | ❌ | moderate pink | ❌ | ±0.1 |
| D65 | XYZScaling | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |

#### 3. Expected: deep pink
Hex: #E4717A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.9R 6.0/9.3 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| C | Bradford | 6.0R 6.0/9.1 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| C | CAT02 | 6.0R 6.0/9.0 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| D65 | XYZScaling | 6.7R 6.0/9.0 | moderate reddish orange | ❌ | deep yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 6.7R 6.0/9.0 | moderate reddish orange | ❌ | deep yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 6.7R 6.0/9.0 | moderate reddish orange | ❌ | deep yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 6.8R 6.0/9.0 | moderate reddish orange | ❌ | deep yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 6.8R 6.0/9.0 | moderate reddish orange | ❌ | deep yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 6.8R 6.0/9.0 | moderate reddish orange | ❌ | deep yellowish pink | ❌ | ±0.1 |

#### 4. Expected: light pink
Hex: #F9CCCA

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.3R 8.5/3.5 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 0.8YR 8.5/3.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 0.8YR 8.5/3.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 0.8YR 8.5/3.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 0.9YR 8.5/3.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 0.9YR 8.5/3.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 1.0YR 8.5/3.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |

#### 5. Expected: moderate pink
Hex: #DEA5A4

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.2R 7.2/4.6 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |
| C | Bradford | 6.4R 7.2/4.5 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| C | CAT02 | 6.4R 7.2/4.5 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |
| D65 | Bradford | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |
| D65 | CAT02 | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |
| F7 | XYZScaling | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |
| F7 | Bradford | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |
| F7 | CAT02 | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | moderate yellowish pink | ❌ |  |

#### 6. Expected: dark pink
Hex: #C08081

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.1R 5.9/5.2 | dark yellowish pink | ❌ | dark yellowish pink | ❌ | ±0.1 |
| C | Bradford | 6.3R 5.9/5.1 | dark yellowish pink | ❌ | dark yellowish pink | ❌ | ±0.1 |
| C | CAT02 | 6.3R 5.9/5.1 | dark yellowish pink | ❌ | dark yellowish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 7.6R 5.9/5.0 | grayish reddish orange | ❌ | dark yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 7.6R 5.9/5.0 | grayish reddish orange | ❌ | dark yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 7.6R 5.9/5.0 | grayish reddish orange | ❌ | dark yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 7.7R 5.9/5.0 | grayish reddish orange | ❌ | dark yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 7.7R 5.9/5.0 | grayish reddish orange | ❌ | dark yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 7.7R 5.9/5.0 | grayish reddish orange | ❌ | dark yellowish pink | ❌ | ±0.1 |

#### 7. Expected: pale pink
Hex: #EAD8D7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.4R 8.7/1.8 | pale yellowish pink | ❌ | pale yellowish pink | ❌ |  |
| C | Bradford | 6.6R 8.7/1.7 | pale yellowish pink | ❌ | pale yellowish pink | ❌ |  |
| C | CAT02 | 6.6R 8.7/1.7 | pale yellowish pink | ❌ | pale yellowish pink | ❌ |  |
| D65 | XYZScaling | 1.4Y 8.7/1.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| D65 | Bradford | 1.4Y 8.7/1.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| D65 | CAT02 | 1.4Y 8.7/1.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | XYZScaling | 2.5GY 8.7/1.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | Bradford | 3.0GY 8.7/1.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | CAT02 | 9.1YR 8.7/1.1 | yellowish white | ❌ | yellowish white | ❌ |  |

#### 8. Expected: grayish pink
Hex: #C4AEAD

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.7R 7.2/1.9 | grayish yellowish pink | ❌ | grayish yellowish pink | ❌ | ±0.1 |
| C | Bradford | 6.9R 7.2/1.8 | grayish yellowish pink | ❌ | grayish yellowish pink | ❌ |  |
| C | CAT02 | 6.9R 7.2/1.8 | grayish yellowish pink | ❌ | grayish yellowish pink | ❌ |  |
| D65 | XYZScaling | 8.0YR 7.2/1.3 | brownish pink | ❌ | brownish pink | ❌ |  |
| D65 | Bradford | 8.0YR 7.2/1.3 | brownish pink | ❌ | brownish pink | ❌ |  |
| D65 | CAT02 | 8.0YR 7.2/1.3 | brownish pink | ❌ | brownish pink | ❌ |  |
| F7 | XYZScaling | 8.1YR 7.2/1.3 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| F7 | Bradford | 8.1YR 7.2/1.3 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| F7 | CAT02 | 8.1YR 7.2/1.3 | yellowish gray | ❌ | yellowish gray | ❌ |  |

#### 9. Expected: pinkish white
Hex: #EAE3E1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 9.8Y 9.1/0.8 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| D65 | Bradford | 9.8Y 9.1/0.8 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| D65 | CAT02 | 9.8Y 9.1/0.8 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | XYZScaling | 9.6Y 9.1/0.8 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | Bradford | 9.6Y 9.1/0.8 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | CAT02 | 9.7Y 9.1/0.8 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |

#### 10. Expected: pinkish gray
Hex: #C1B6B3

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.1GY 7.4/1.2 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 7.1GY 7.4/1.2 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 7.1GY 7.4/1.2 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 6.9GY 7.4/1.2 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 6.8GY 7.4/1.2 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 6.3GY 7.4/1.1 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |

#### 11. Expected: vivid red
Hex: #BE0032 - **All configurations matched**

#### 12. Expected: strong red
Hex: #BC3F4A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.7R 4.4/10.3 | dark reddish orange | ❌ | moderate red | ❌ | ±0.1 |
| C | Bradford | 6.8R 4.5/10.0 | dark reddish orange | ❌ | moderate red | ❌ | ±0.1 |
| C | CAT02 | 6.8R 4.4/10.0 | dark reddish orange | ❌ | moderate red | ❌ | ±0.1 |
| D65 | XYZScaling | 7.2R 4.4/10.0 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| D65 | Bradford | 7.2R 4.4/10.0 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| D65 | CAT02 | 7.2R 4.4/10.0 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| F7 | XYZScaling | 7.2R 4.4/10.0 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| F7 | Bradford | 7.2R 4.4/10.1 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| F7 | CAT02 | 7.2R 4.4/10.1 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |

#### 13. Expected: deep red
Hex: #841B2D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.4R 2.9/8.4 | dark red | ❌ | dark red | ❌ | ±0.1 |
| D65 | Bradford | 7.4R 2.9/8.4 | dark red | ❌ | dark red | ❌ | ±0.1 |
| D65 | CAT02 | 7.4R 2.9/8.4 | dark red | ❌ | dark red | ❌ | ±0.1 |
| F7 | XYZScaling | 7.4R 2.9/8.4 | dark red | ❌ | dark red | ❌ | ±0.1 |
| F7 | Bradford | 7.4R 2.9/8.4 | dark red | ❌ | dark red | ❌ | ±0.1 |
| F7 | CAT02 | 7.4R 2.9/8.4 | dark red | ❌ | dark red | ❌ | ±0.1 |

#### 14. Expected: very deep red
Hex: #5C0923 - **All configurations matched**

#### 15. Expected: moderate red
Hex: #AB4E52

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.6R 4.4/7.7 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| C | Bradford | 6.7R 4.4/7.5 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| C | CAT02 | 6.7R 4.4/7.4 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| D65 | XYZScaling | 7.3R 4.4/7.5 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| D65 | Bradford | 7.3R 4.4/7.5 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| D65 | CAT02 | 7.3R 4.4/7.5 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| F7 | XYZScaling | 7.3R 4.4/7.5 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| F7 | Bradford | 7.3R 4.4/7.5 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |
| F7 | CAT02 | 7.3R 4.4/7.5 | dark reddish orange | ❌ | dark reddish orange | ❌ | ±0.1 |

#### 16. Expected: dark red
Hex: #722F37 - **All configurations matched**

#### 17. Expected: very dark red
Hex: #3F1728

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.5R 1.4/4.3 | very dark red | ✅ | very dark purplish red | ❌ | ±0.1 |
| C | Bradford | 0.4R 1.4/4.1 | very dark red | ✅ | very dark purplish red | ❌ | ±0.1 |
| C | CAT02 | 0.5R 1.4/4.1 | very dark red | ✅ | very dark purplish red | ❌ | ±0.1 |

#### 18. Expected: light grayish red
Hex: #AD8884

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.9YR 5.9/2.8 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ |  |
| D65 | Bradford | 1.9YR 5.9/2.8 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ |  |
| D65 | CAT02 | 1.9YR 5.9/2.8 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ |  |
| F7 | XYZScaling | 2.0YR 5.9/2.8 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ |  |
| F7 | Bradford | 2.0YR 5.9/2.8 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ |  |
| F7 | CAT02 | 2.0YR 5.9/2.8 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ |  |

#### 19. Expected: grayish red
Hex: #905D5D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.1R 4.4/4.0 | moderate reddish brown | ❌ | moderate reddish brown | ❌ | ±0.1 |
| D65 | Bradford | 8.1R 4.4/4.0 | moderate reddish brown | ❌ | moderate reddish brown | ❌ | ±0.1 |
| D65 | CAT02 | 8.1R 4.4/4.0 | moderate reddish brown | ❌ | moderate reddish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 8.2R 4.4/4.0 | moderate reddish brown | ❌ | moderate reddish brown | ❌ | ±0.1 |
| F7 | Bradford | 8.2R 4.4/4.0 | moderate reddish brown | ❌ | moderate reddish brown | ❌ | ±0.1 |
| F7 | CAT02 | 8.2R 4.4/4.0 | moderate reddish brown | ❌ | moderate reddish brown | ❌ | ±0.1 |

#### 20. Expected: dark grayish red
Hex: #543D3F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.9R 2.8/1.7 | grayish reddish brown | ❌ | grayish reddish brown | ❌ |  |
| D65 | Bradford | 7.9R 2.8/1.7 | grayish reddish brown | ❌ | grayish reddish brown | ❌ |  |
| D65 | CAT02 | 7.9R 2.8/1.7 | grayish reddish brown | ❌ | grayish reddish brown | ❌ |  |
| F7 | XYZScaling | 8.1R 2.8/1.7 | grayish reddish brown | ❌ | grayish reddish brown | ❌ |  |
| F7 | Bradford | 8.1R 2.8/1.7 | grayish reddish brown | ❌ | grayish reddish brown | ❌ |  |
| F7 | CAT02 | 8.1R 2.8/1.7 | grayish reddish brown | ❌ | grayish reddish brown | ❌ |  |

#### 21. Expected: blackish red
Hex: #2E1D21

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.6R 1.3/1.2 | dark reddish brown | ❌ | dark reddish brown | ❌ |  |
| D65 | Bradford | 7.6R 1.3/1.2 | dark reddish brown | ❌ | dark reddish brown | ❌ |  |
| D65 | CAT02 | 7.6R 1.3/1.2 | dark reddish brown | ❌ | dark reddish brown | ❌ |  |
| F7 | XYZScaling | 7.7R 1.3/1.2 | dark reddish brown | ❌ | dark reddish brown | ❌ |  |
| F7 | Bradford | 7.7R 1.3/1.2 | dark reddish brown | ❌ | dark reddish brown | ❌ |  |
| F7 | CAT02 | 7.7R 1.3/1.2 | dark reddish brown | ❌ | dark reddish brown | ❌ |  |

#### 22. Expected: reddish gray
Hex: #8F817F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.8Y 5.4/0.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| D65 | Bradford | 4.8Y 5.4/0.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| D65 | CAT02 | 4.8Y 5.4/0.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| F7 | XYZScaling | 5.1Y 5.4/0.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| F7 | Bradford | 5.0Y 5.4/0.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| F7 | CAT02 | 5.1Y 5.4/0.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |

#### 23. Expected: dark reddish gray
Hex: #5C504F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 10.0YR 3.5/0.8 | brownish gray | ❌ | brownish gray | ❌ | ±0.1 |
| D65 | Bradford | 10.0YR 3.5/0.8 | brownish gray | ❌ | brownish gray | ❌ | ±0.1 |
| D65 | CAT02 | 10.0YR 3.5/0.8 | brownish gray | ❌ | brownish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 0.2Y 3.5/0.8 | brownish gray | ❌ | brownish gray | ❌ | ±0.1 |
| F7 | Bradford | 0.2Y 3.5/0.8 | brownish gray | ❌ | brownish gray | ❌ | ±0.1 |
| F7 | CAT02 | 0.2Y 3.5/0.8 | brownish gray | ❌ | brownish gray | ❌ | ±0.1 |

#### 24. Expected: reddish black
Hex: #282022 - **All configurations matched**

#### 25. Expected: vivid yellowish pink
Hex: #FFB7A5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.5R 8.0/6.2 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| C | Bradford | 8.7R 8.0/6.1 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| C | CAT02 | 8.7R 8.0/6.0 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 1.9YR 8.0/5.7 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 1.9YR 8.0/5.7 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 1.9YR 8.0/5.7 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 2.0YR 8.0/5.7 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 2.0YR 8.0/5.7 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 2.0YR 8.0/5.7 | light yellowish pink | ❌ | light yellowish pink | ❌ | ±0.1 |

#### 26. Expected: strong yellowish pink
Hex: #F99379 - **All configurations matched**

#### 27. Expected: deep yellowish pink
Hex: #E66721

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.4YR 5.8/13.7 | strong orange | ❌ | vivid reddish orange | ❌ |  |
| C | Bradford | 2.0YR 5.8/13.3 | strong orange | ❌ | vivid reddish orange | ❌ |  |
| C | CAT02 | 2.0YR 5.8/13.3 | strong orange | ❌ | vivid reddish orange | ❌ |  |
| D65 | XYZScaling | 2.6YR 5.8/13.2 | strong orange | ❌ | strong orange | ❌ |  |
| D65 | Bradford | 2.6YR 5.8/13.2 | strong orange | ❌ | strong orange | ❌ |  |
| D65 | CAT02 | 2.6YR 5.8/13.2 | strong orange | ❌ | strong orange | ❌ |  |
| F7 | XYZScaling | 2.6YR 5.8/13.2 | strong orange | ❌ | strong orange | ❌ |  |
| F7 | Bradford | 2.6YR 5.8/13.2 | strong orange | ❌ | strong orange | ❌ |  |
| F7 | CAT02 | 2.6YR 5.8/13.2 | strong orange | ❌ | strong orange | ❌ |  |

#### 28. Expected: light yellowish pink
Hex: #F4C2C2

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.8R 8.2/3.9 | light pink | ❌ | light pink | ❌ |  |
| C | Bradford | 5.9R 8.2/3.8 | light pink | ❌ | light pink | ❌ |  |
| C | CAT02 | 5.9R 8.2/3.8 | light pink | ❌ | light pink | ❌ |  |

#### 29. Expected: moderate yellowish pink
Hex: #D9A6A9

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4R 7.2/4.0 | moderate pink | ❌ | moderate pink | ❌ | ±0.1 |
| C | Bradford | 5.5R 7.2/3.9 | moderate pink | ❌ | moderate pink | ❌ | ±0.1 |
| C | CAT02 | 5.5R 7.2/3.9 | moderate pink | ❌ | moderate pink | ❌ |  |

#### 30. Expected: dark yellowish pink
Hex: #C48379

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9R 6.0/5.8 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |
| C | Bradford | 8.1R 6.0/5.7 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| C | CAT02 | 8.1R 6.0/5.6 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| D65 | XYZScaling | 9.6R 6.0/5.5 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| D65 | Bradford | 9.6R 6.0/5.5 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| D65 | CAT02 | 9.6R 6.0/5.5 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| F7 | XYZScaling | 9.7R 6.0/5.5 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| F7 | Bradford | 9.7R 6.0/5.5 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |
| F7 | CAT02 | 9.7R 6.0/5.5 | grayish reddish orange | ❌ | grayish reddish orange | ❌ | ±0.1 |

#### 31. Expected: pale yellowish pink
Hex: #ECD5C5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.0Y 8.6/2.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| D65 | Bradford | 4.0Y 8.6/2.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| D65 | CAT02 | 4.0Y 8.6/2.0 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | XYZScaling | 5.6Y 8.6/1.9 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| F7 | Bradford | 1.4G 8.6/3.5 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 3.4Y 8.6/2.0 | pale yellow | ❌ | pale yellow | ❌ | ±0.1 |

#### 32. Expected: grayish yellowish pink
Hex: #C7ADA3

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.8Y 7.2/1.9 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| D65 | Bradford | 1.8Y 7.2/1.9 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| D65 | CAT02 | 1.8Y 7.2/1.9 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| F7 | XYZScaling | 1.9Y 7.2/1.9 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| F7 | Bradford | 1.9Y 7.2/1.9 | yellowish gray | ❌ | yellowish gray | ❌ |  |
| F7 | CAT02 | 1.9Y 7.2/1.9 | yellowish gray | ❌ | yellowish gray | ❌ |  |

#### 33. Expected: brownish pink
Hex: #C2AC99

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.7YR 7.1/2.1 | light grayish yellowish brown | ❌ | light grayish yellowish brown | ❌ | ±0.1 |
| C | Bradford | 0.6Y 7.1/2.0 | grayish yellow | ❌ | light grayish yellowish brown | ❌ | ±0.1 |
| C | CAT02 | 0.5Y 7.1/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |
| D65 | XYZScaling | 5.6GY 7.1/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.6GY 7.1/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.6GY 7.1/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.6GY 7.1/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.6GY 7.1/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.6GY 7.1/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |

#### 34. Expected: vivid reddish orange
Hex: #E25822 - **All configurations matched**

#### 35. Expected: strong reddish orange
Hex: #D9603B - **All configurations matched**

#### 36. Expected: deep reddish orange
Hex: #AA381E - **All configurations matched**

#### 37. Expected: moderate reddish orange
Hex: #CB6D51 - **All configurations matched**

#### 38. Expected: dark reddish orange
Hex: #9E4732 - **All configurations matched**

#### 39. Expected: grayish reddish orange
Hex: #B4745E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 3.9YR 5.4/5.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| D65 | Bradford | 3.9YR 5.4/5.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| D65 | CAT02 | 3.9YR 5.4/5.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| F7 | XYZScaling | 3.9YR 5.4/5.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| F7 | Bradford | 3.9YR 5.4/5.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| F7 | CAT02 | 3.9YR 5.4/5.5 | light brown | ❌ | light brown | ❌ | ±0.1 |

#### 40. Expected: strong reddish brown
Hex: #882D17

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ | ±0.1 |
| D65 | Bradford | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ | ±0.1 |
| D65 | CAT02 | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ | ±0.1 |
| F7 | XYZScaling | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ | ±0.1 |
| F7 | Bradford | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ | ±0.1 |
| F7 | CAT02 | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ | ±0.1 |

#### 41. Expected: deep reddish brown
Hex: #56070C - **All configurations matched**

#### 42. Expected: light reddish brown
Hex: #A87C6D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 6.4YR 5.5/3.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| D65 | Bradford | 6.4YR 5.5/3.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| D65 | CAT02 | 6.4YR 5.5/3.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| F7 | XYZScaling | 6.6YR 5.5/3.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| F7 | Bradford | 6.5YR 5.5/3.5 | light brown | ❌ | light brown | ❌ | ±0.1 |
| F7 | CAT02 | 6.6YR 5.5/3.5 | light brown | ❌ | light brown | ❌ | ±0.1 |

#### 43. Expected: moderate reddish brown
Hex: #79443B - **All configurations matched**

#### 44. Expected: dark reddish brown
Hex: #3E1D1E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 9.2R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| C | CAT02 | 9.2R 1.5/2.9 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 9.8R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| D65 | Bradford | 9.8R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| D65 | CAT02 | 9.8R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 9.8R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| F7 | Bradford | 9.8R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| F7 | CAT02 | 9.8R 1.5/3.0 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |

#### 45. Expected: light grayish reddish brown
Hex: #977F73

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 5.9YR 5.4/2.0 | light grayish brown | ❌ | light grayish brown | ❌ | ±0.1 |
| C | CAT02 | 5.9YR 5.4/2.0 | light grayish brown | ❌ | light grayish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 3.2Y 5.4/2.0 | light olive gray | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | Bradford | 3.2Y 5.4/2.0 | light olive gray | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 3.2Y 5.4/2.0 | light olive gray | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 3.3Y 5.4/2.0 | light olive gray | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | Bradford | 3.3Y 5.4/2.0 | light olive gray | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 3.3Y 5.4/2.0 | light olive gray | ❌ | light olive brown | ❌ | ±0.1 |

#### 46. Expected: grayish reddish brown
Hex: #674C47

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.4YR 3.4/2.0 | grayish brown | ❌ | grayish brown | ❌ | ±0.1 |
| D65 | Bradford | 4.4YR 3.4/2.0 | grayish brown | ❌ | grayish brown | ❌ | ±0.1 |
| D65 | CAT02 | 4.4YR 3.4/2.0 | grayish brown | ❌ | grayish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 4.5YR 3.4/2.0 | grayish brown | ❌ | grayish brown | ❌ | ±0.1 |
| F7 | Bradford | 4.4YR 3.4/2.0 | grayish brown | ❌ | grayish brown | ❌ | ±0.1 |
| F7 | CAT02 | 4.5YR 3.4/2.0 | grayish brown | ❌ | grayish brown | ❌ | ±0.1 |

#### 47. Expected: dark grayish reddish brown
Hex: #43302E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.5YR 2.2/1.6 | dark grayish brown | ❌ | dark grayish brown | ❌ | ±0.1 |
| D65 | Bradford | 4.5YR 2.2/1.6 | dark grayish brown | ❌ | dark grayish brown | ❌ | ±0.1 |
| D65 | CAT02 | 4.5YR 2.2/1.6 | dark grayish brown | ❌ | dark grayish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 4.5YR 2.2/1.6 | dark grayish brown | ❌ | dark grayish brown | ❌ | ±0.1 |
| F7 | Bradford | 4.5YR 2.2/1.6 | dark grayish brown | ❌ | dark grayish brown | ❌ | ±0.1 |
| F7 | CAT02 | 4.5YR 2.2/1.6 | dark grayish brown | ❌ | dark grayish brown | ❌ | ±0.1 |

#### 48. Expected: vivid orange
Hex: #F38400

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.6YR 6.5/13.8 | strong orange | ❌ | strong orange | ❌ | ±0.1 |
| C | Bradford | 6.3YR 6.5/13.6 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| C | CAT02 | 6.2YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| D65 | XYZScaling | 7.0YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| D65 | Bradford | 7.0YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| D65 | CAT02 | 7.0YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| F7 | XYZScaling | 7.0YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| F7 | Bradford | 7.0YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| F7 | CAT02 | 7.0YR 6.5/13.5 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |

#### 49. Expected: brilliant orange
Hex: #FD943F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4YR 7.0/11.7 | strong orange | ❌ | strong orange | ❌ | ±0.1 |
| C | Bradford | 6.0YR 7.0/11.5 | strong orange | ❌ | strong orange | ❌ | ±0.1 |
| C | CAT02 | 6.0YR 7.0/11.4 | strong orange | ❌ | strong orange | ❌ | ±0.1 |
| D65 | XYZScaling | 7.0YR 7.0/11.4 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| D65 | Bradford | 7.0YR 7.0/11.4 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| D65 | CAT02 | 7.0YR 7.0/11.4 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| F7 | XYZScaling | 7.0YR 7.0/11.4 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| F7 | Bradford | 7.0YR 7.0/11.4 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |
| F7 | CAT02 | 7.0YR 7.0/11.4 | strong orange yellow | ❌ | strong orange | ❌ | ±0.1 |

#### 50. Expected: strong orange
Hex: #ED872D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 6.3YR 6.5/11.6 | strong orange yellow | ❌ | strong orange | ✅ | ±0.1 |
| C | CAT02 | 6.3YR 6.5/11.5 | strong orange yellow | ❌ | strong orange | ✅ | ±0.1 |
| D65 | XYZScaling | 7.2YR 6.5/11.5 | strong orange yellow | ❌ | strong orange yellow | ❌ | ±0.1 |
| D65 | Bradford | 7.2YR 6.5/11.5 | strong orange yellow | ❌ | strong orange yellow | ❌ | ±0.1 |
| D65 | CAT02 | 7.2YR 6.5/11.5 | strong orange yellow | ❌ | strong orange yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 7.2YR 6.5/11.6 | strong orange yellow | ❌ | strong orange yellow | ❌ | ±0.1 |
| F7 | Bradford | 7.2YR 6.5/11.6 | strong orange yellow | ❌ | strong orange yellow | ❌ | ±0.1 |
| F7 | CAT02 | 7.2YR 6.5/11.6 | strong orange yellow | ❌ | strong orange yellow | ❌ | ±0.1 |

#### 51. Expected: deep orange
Hex: #BE6516 - **All configurations matched**

#### 52. Expected: light orange
Hex: #FAB57F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.2YR 7.8/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| C | Bradford | 7.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| C | CAT02 | 7.6YR 7.8/6.7 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| D65 | XYZScaling | 9.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| D65 | Bradford | 9.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| D65 | CAT02 | 9.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| F7 | XYZScaling | 9.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| F7 | Bradford | 9.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| F7 | CAT02 | 9.7YR 7.8/6.8 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |

#### 53. Expected: moderate orange
Hex: #D99058

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8YR 6.5/7.7 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |
| C | Bradford | 7.3YR 6.5/7.5 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| C | CAT02 | 7.3YR 6.5/7.5 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 8.6YR 6.5/7.6 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| D65 | Bradford | 8.6YR 6.5/7.6 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| D65 | CAT02 | 8.6YR 6.5/7.6 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 8.6YR 6.5/7.6 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| F7 | Bradford | 8.6YR 6.5/7.6 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |
| F7 | CAT02 | 8.6YR 6.5/7.6 | moderate orange yellow | ❌ | moderate orange yellow | ❌ | ±0.1 |

#### 54. Expected: brownish orange
Hex: #AE6938

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.2YR 5.0/7.5 | strong yellowish brown | ❌ | brownish orange | ✅ | ±0.1 |
| C | Bradford | 6.9YR 5.0/7.3 | strong yellowish brown | ❌ | brownish orange | ✅ | ±0.1 |
| C | CAT02 | 6.8YR 5.0/7.2 | strong yellowish brown | ❌ | brownish orange | ✅ | ±0.1 |
| D65 | XYZScaling | 8.0YR 5.0/7.3 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| D65 | Bradford | 8.0YR 5.0/7.3 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| D65 | CAT02 | 8.0YR 5.0/7.3 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 8.0YR 5.0/7.3 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| F7 | Bradford | 8.0YR 5.0/7.3 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| F7 | CAT02 | 8.0YR 5.0/7.3 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |

#### 55. Expected: strong brown
Hex: #80461B - **All configurations matched**

#### 56. Expected: deep brown
Hex: #593319

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.7YR 2.5/4.6 | moderate brown | ❌ | moderate brown | ❌ | ±0.1 |
| C | Bradford | 7.1YR 2.5/4.5 | dark yellowish brown | ❌ | moderate brown | ❌ | ±0.1 |
| C | CAT02 | 7.1YR 2.5/4.4 | dark yellowish brown | ❌ | moderate brown | ❌ | ±0.1 |
| D65 | XYZScaling | 8.1YR 2.5/4.5 | dark yellowish brown | ❌ | dark yellowish brown | ❌ | ±0.1 |
| D65 | Bradford | 8.1YR 2.5/4.5 | dark yellowish brown | ❌ | dark yellowish brown | ❌ | ±0.1 |
| D65 | CAT02 | 8.1YR 2.5/4.5 | dark yellowish brown | ❌ | dark yellowish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 8.1YR 2.5/4.5 | dark yellowish brown | ❌ | dark yellowish brown | ❌ | ±0.1 |
| F7 | Bradford | 8.1YR 2.5/4.5 | dark yellowish brown | ❌ | dark yellowish brown | ❌ | ±0.1 |
| F7 | CAT02 | 8.1YR 2.5/4.5 | dark yellowish brown | ❌ | dark yellowish brown | ❌ | ±0.1 |

#### 57. Expected: light brown
Hex: #A67B5B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.0YR 5.4/4.4 | moderate yellowish brown | ❌ | light brown | ✅ | ±0.1 |
| C | Bradford | 8.4YR 5.4/4.3 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| C | CAT02 | 8.4YR 5.4/4.2 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 1.6Y 5.4/4.2 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | Bradford | 1.6Y 5.4/4.2 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 1.6Y 5.4/4.2 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 1.6Y 5.4/4.2 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | Bradford | 1.6Y 5.4/4.2 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 1.6Y 5.4/4.2 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |

#### 58. Expected: moderate brown
Hex: #6F4E37

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9YR 3.6/3.5 | moderate yellowish brown | ❌ | moderate brown | ✅ | ±0.1 |
| C | Bradford | 8.5YR 3.6/3.4 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| C | CAT02 | 8.5YR 3.6/3.4 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 1.0Y 3.6/3.4 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| D65 | Bradford | 1.0Y 3.6/3.4 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| D65 | CAT02 | 1.0Y 3.6/3.4 | moderate yellowish brown | ❌ | moderate yellowish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 1.1Y 3.6/3.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | Bradford | 1.1Y 3.6/3.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 1.1Y 3.6/3.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |

#### 59. Expected: dark brown
Hex: #422518 - **All configurations matched**

#### 60. Expected: light grayish brown
Hex: #958070

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.3YR 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| C | Bradford | 0.2Y 5.4/1.9 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| C | CAT02 | 0.2Y 5.4/1.9 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 0.3GY 5.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| D65 | Bradford | 0.3GY 5.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| D65 | CAT02 | 0.3GY 5.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| F7 | XYZScaling | 0.4GY 5.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| F7 | Bradford | 0.4GY 5.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| F7 | CAT02 | 0.4GY 5.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |

#### 61. Expected: grayish brown
Hex: #635147

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.0Y 3.5/1.7 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | Bradford | 4.0Y 3.5/1.7 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 4.0Y 3.5/1.7 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 4.1Y 3.5/1.7 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |
| F7 | Bradford | 4.1Y 3.5/1.7 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |
| F7 | CAT02 | 4.1Y 3.5/1.7 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |

#### 62. Expected: dark grayish brown
Hex: #3E322C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 7.2YR 2.2/1.2 | dark grayish yellowish brown | ❌ | dark grayish brown | ✅ |  |
| C | CAT02 | 7.2YR 2.2/1.2 | dark grayish yellowish brown | ❌ | dark grayish brown | ✅ |  |
| D65 | XYZScaling | 1.8Y 2.2/1.3 | dark olive brown | ❌ | dark olive brown | ❌ |  |
| D65 | Bradford | 1.8Y 2.2/1.3 | dark olive brown | ❌ | dark olive brown | ❌ |  |
| D65 | CAT02 | 1.8Y 2.2/1.3 | dark olive brown | ❌ | dark olive brown | ❌ |  |
| F7 | XYZScaling | 1.9Y 2.2/1.3 | dark olive brown | ❌ | dark olive brown | ❌ |  |
| F7 | Bradford | 1.9Y 2.2/1.3 | dark olive brown | ❌ | dark olive brown | ❌ |  |
| F7 | CAT02 | 1.9Y 2.2/1.3 | dark olive brown | ❌ | dark olive brown | ❌ |  |

#### 63. Expected: light brownish gray
Hex: #8E8279

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 2.3GY 5.4/1.5 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | Bradford | 2.3GY 5.4/1.5 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 2.3GY 5.4/1.5 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 2.3GY 5.4/1.5 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | Bradford | 2.3GY 5.4/1.5 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 2.3GY 5.4/1.5 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |

#### 64. Expected: brownish gray
Hex: #5B504F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.2R 3.5/0.9 | dark reddish gray | ❌ | dark reddish gray | ❌ | ±0.1 |
| C | Bradford | 6.9R 3.5/0.8 | dark reddish gray | ❌ | dark reddish gray | ❌ | ±0.1 |
| C | CAT02 | 6.9R 3.5/0.8 | dark reddish gray | ❌ | dark reddish gray | ❌ | ±0.1 |

#### 65. Expected: brownish black
Hex: #28201C - **All configurations matched**

#### 66. Expected: vivid orange yellow
Hex: #F6A600

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.6Y 7.3/12.3 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| C | Bradford | 2.4Y 7.3/12.1 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| C | CAT02 | 2.3Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 3.5Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| D65 | Bradford | 3.5Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| D65 | CAT02 | 3.5Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 3.5Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| F7 | Bradford | 3.5Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |
| F7 | CAT02 | 3.5Y 7.3/12.0 | vivid yellow | ❌ | vivid yellow | ❌ | ±0.1 |

#### 67. Expected: brilliant orange yellow
Hex: #FFC14F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| C | Bradford | 5.0Y 8.1/9.3 | brilliant yellow | ❌ | brilliant yellow | ❌ |  |
| C | CAT02 | 5.0Y 8.1/9.2 | brilliant yellow | ❌ | brilliant yellow | ❌ |  |
| D65 | XYZScaling | 7.5Y 8.1/9.4 | brilliant greenish yellow | ❌ | brilliant greenish yellow | ❌ |  |
| D65 | Bradford | 7.5Y 8.1/9.4 | brilliant greenish yellow | ❌ | brilliant greenish yellow | ❌ |  |
| D65 | CAT02 | 7.5Y 8.1/9.4 | brilliant greenish yellow | ❌ | brilliant greenish yellow | ❌ |  |
| F7 | XYZScaling | 7.5Y 8.1/9.4 | brilliant greenish yellow | ❌ | brilliant greenish yellow | ❌ |  |
| F7 | Bradford | 7.5Y 8.1/9.4 | brilliant greenish yellow | ❌ | brilliant greenish yellow | ❌ |  |
| F7 | CAT02 | 7.5Y 8.1/9.4 | brilliant greenish yellow | ❌ | brilliant greenish yellow | ❌ |  |

#### 68. Expected: strong orange yellow
Hex: #EAA221

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.3Y 7.1/10.9 | strong yellow | ❌ | strong yellow | ❌ | ±0.1 |
| C | Bradford | 3.0Y 7.1/10.8 | strong yellow | ❌ | strong yellow | ❌ | ±0.1 |
| C | CAT02 | 3.0Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 4.2Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ |  |
| D65 | Bradford | 4.2Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ |  |
| D65 | CAT02 | 4.2Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ |  |
| F7 | XYZScaling | 4.2Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ |  |
| F7 | Bradford | 4.2Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ |  |
| F7 | CAT02 | 4.2Y 7.1/10.7 | strong yellow | ❌ | strong yellow | ❌ |  |

#### 69. Expected: deep orange yellow
Hex: #C98500

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.7Y 6.0/10.6 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| C | Bradford | 2.5Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| C | CAT02 | 2.4Y 6.0/10.3 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 3.6Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| D65 | Bradford | 3.6Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| D65 | CAT02 | 3.6Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 3.6Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| F7 | Bradford | 3.6Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| F7 | CAT02 | 3.6Y 6.0/10.4 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |

#### 70. Expected: light orange yellow
Hex: #FBC97F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.7Y 8.3/6.4 | light yellow | ❌ | light yellow | ❌ | ±0.1 |
| C | Bradford | 4.5Y 8.3/6.3 | light yellow | ❌ | light yellow | ❌ |  |
| C | CAT02 | 4.4Y 8.3/6.3 | light yellow | ❌ | light yellow | ❌ |  |
| D65 | XYZScaling | 0.7GY 8.3/6.6 | light greenish yellow | ❌ | light greenish yellow | ❌ |  |
| D65 | Bradford | 0.7GY 8.3/6.6 | light greenish yellow | ❌ | light greenish yellow | ❌ |  |
| D65 | CAT02 | 0.7GY 8.3/6.6 | light greenish yellow | ❌ | light greenish yellow | ❌ |  |
| F7 | XYZScaling | 0.7GY 8.3/6.6 | light greenish yellow | ❌ | light greenish yellow | ❌ |  |
| F7 | Bradford | 0.7GY 8.3/6.6 | light greenish yellow | ❌ | light greenish yellow | ❌ |  |
| F7 | CAT02 | 0.7GY 8.3/6.6 | light greenish yellow | ❌ | light greenish yellow | ❌ |  |

#### 71. Expected: moderate orange yellow
Hex: #E3A857

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.4Y 7.2/7.7 | moderate yellow | ❌ | moderate yellow | ❌ |  |
| C | Bradford | 3.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| C | CAT02 | 3.1Y 7.2/7.5 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 5.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ |  |
| D65 | Bradford | 5.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ |  |
| D65 | CAT02 | 5.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ |  |
| F7 | XYZScaling | 5.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ |  |
| F7 | Bradford | 5.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ |  |
| F7 | CAT02 | 5.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ |  |

#### 72. Expected: dark orange yellow
Hex: #BE8A3D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.2Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| C | Bradford | 4.0Y 6.0/7.1 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| C | CAT02 | 3.9Y 6.0/7.1 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 5.8Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| D65 | Bradford | 5.8Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| D65 | CAT02 | 5.8Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 5.9Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| F7 | Bradford | 5.8Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| F7 | CAT02 | 5.8Y 6.0/7.2 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |

#### 73. Expected: pale orange yellow
Hex: #FAD6A5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.7Y 8.7/4.1 | pale yellow | ❌ | pale yellow | ❌ | ±0.1 |
| C | Bradford | 4.6Y 8.7/4.0 | pale yellow | ❌ | pale yellow | ❌ | ±0.1 |
| C | CAT02 | 4.5Y 8.7/4.0 | pale yellow | ❌ | pale yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 5.2GY 8.7/4.9 | light yellow green | ❌ | light yellow green | ❌ |  |
| D65 | Bradford | 5.2GY 8.7/4.9 | light yellow green | ❌ | light yellow green | ❌ |  |
| D65 | CAT02 | 5.2GY 8.7/4.9 | light yellow green | ❌ | light yellow green | ❌ |  |
| F7 | XYZScaling | 6.2GY 8.7/5.2 | light yellow green | ❌ | light yellow green | ❌ |  |
| F7 | Bradford | 5.3GY 8.7/4.9 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.2GY 8.7/4.9 | light yellow green | ❌ | light yellow green | ❌ |  |

#### 74. Expected: strong yellowish brown
Hex: #996515

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.9Y 4.6/7.8 | light olive brown | ❌ | light olive brown | ❌ |  |
| C | Bradford | 2.6Y 4.6/7.7 | light olive brown | ❌ | light olive brown | ❌ |  |
| C | CAT02 | 2.6Y 4.6/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | XYZScaling | 3.8Y 4.6/7.7 | light olive | ❌ | light olive brown | ❌ |  |
| D65 | Bradford | 3.8Y 4.6/7.7 | light olive | ❌ | light olive brown | ❌ |  |
| D65 | CAT02 | 3.8Y 4.6/7.7 | light olive | ❌ | light olive brown | ❌ |  |
| F7 | XYZScaling | 3.8Y 4.6/7.7 | light olive | ❌ | light olive brown | ❌ |  |
| F7 | Bradford | 3.8Y 4.6/7.7 | light olive | ❌ | light olive brown | ❌ |  |
| F7 | CAT02 | 3.8Y 4.6/7.7 | light olive | ❌ | light olive brown | ❌ |  |

#### 75. Expected: deep yellowish brown
Hex: #654522

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.2Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| C | Bradford | 1.8Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| C | CAT02 | 1.8Y 3.2/4.3 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| D65 | XYZScaling | 3.5Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | Bradford | 3.5Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 3.5Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 3.5Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | Bradford | 3.5Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 3.5Y 3.2/4.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |

#### 76. Expected: light yellowish brown
Hex: #C19A6B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.0Y 6.5/4.6 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| C | Bradford | 3.8Y 6.5/4.5 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| C | CAT02 | 3.8Y 6.5/4.5 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 9.1Y 6.5/4.7 | grayish greenish yellow | ❌ | grayish greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 9.1Y 6.5/4.7 | grayish greenish yellow | ❌ | grayish greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 9.1Y 6.5/4.7 | grayish greenish yellow | ❌ | grayish greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 9.1Y 6.5/4.8 | grayish greenish yellow | ❌ | grayish greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 9.1Y 6.5/4.8 | grayish greenish yellow | ❌ | grayish greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 9.1Y 6.5/4.8 | grayish greenish yellow | ❌ | grayish greenish yellow | ❌ | ±0.1 |

#### 77. Expected: moderate yellowish brown
Hex: #826644

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.1Y 4.4/3.5 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| C | Bradford | 5.0Y 4.4/3.4 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| C | CAT02 | 5.0Y 4.4/3.4 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| D65 | XYZScaling | 8.3Y 4.4/3.7 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| D65 | Bradford | 8.3Y 4.4/3.7 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| D65 | CAT02 | 8.3Y 4.4/3.7 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| F7 | XYZScaling | 8.3Y 4.4/3.7 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| F7 | Bradford | 8.3Y 4.4/3.7 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| F7 | CAT02 | 8.3Y 4.4/3.7 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |

#### 78. Expected: dark yellowish brown
Hex: #4B3621

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 1.4Y 2.4/2.8 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| C | CAT02 | 1.4Y 2.4/2.8 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| D65 | XYZScaling | 3.4Y 2.4/2.9 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| D65 | Bradford | 3.4Y 2.4/2.9 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 3.4Y 2.4/2.9 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 3.4Y 2.4/2.9 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| F7 | Bradford | 3.4Y 2.4/2.9 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 3.4Y 2.4/2.9 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |

#### 79. Expected: light grayish yellowish brown
Hex: #AE9B82

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.4Y 6.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| C | Bradford | 9.9Y 6.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| C | CAT02 | 9.7Y 6.4/2.2 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| D65 | XYZScaling | 2.9GY 6.4/2.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | Bradford | 2.9GY 6.4/2.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 2.9GY 6.4/2.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 2.9GY 6.4/2.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | Bradford | 2.9GY 6.4/2.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 2.9GY 6.4/2.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |

#### 80. Expected: grayish yellowish brown
Hex: #7E6D5A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.7Y 4.6/1.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| C | Bradford | 6.1Y 4.6/1.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| C | CAT02 | 6.0Y 4.6/1.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| D65 | XYZScaling | 0.7GY 4.6/2.4 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| D65 | Bradford | 0.7GY 4.6/2.4 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| D65 | CAT02 | 0.7GY 4.6/2.4 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| F7 | XYZScaling | 0.7GY 4.6/2.4 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| F7 | Bradford | 0.7GY 4.6/2.4 | light grayish olive | ❌ | light grayish olive | ❌ |  |
| F7 | CAT02 | 0.7GY 4.6/2.4 | light grayish olive | ❌ | light grayish olive | ❌ |  |

#### 81. Expected: dark grayish yellowish brown
Hex: #483C32

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.1Y 2.6/1.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| C | Bradford | 1.7Y 2.6/1.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| C | CAT02 | 1.7Y 2.6/1.4 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | XYZScaling | 6.2Y 2.6/1.6 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |
| D65 | Bradford | 6.2Y 2.6/1.6 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |
| D65 | CAT02 | 6.2Y 2.6/1.6 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |
| F7 | XYZScaling | 6.3Y 2.6/1.6 | grayish olive | ❌ | grayish olive | ❌ | ±0.1 |
| F7 | Bradford | 6.3Y 2.6/1.6 | grayish olive | ❌ | grayish olive | ❌ |  |
| F7 | CAT02 | 6.3Y 2.6/1.6 | grayish olive | ❌ | grayish olive | ❌ |  |

#### 82. Expected: vivid yellow
Hex: #F3C300

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.2GY 8.0/11.3 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| C | Bradford | 0.7GY 8.0/11.4 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| C | CAT02 | 0.7GY 8.0/11.3 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 1.7GY 8.0/11.6 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 1.7GY 8.0/11.6 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 1.7GY 8.0/11.6 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 1.7GY 8.0/11.6 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 1.7GY 8.0/11.6 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 1.7GY 8.0/11.6 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |

#### 83. Expected: brilliant yellow
Hex: #FADA5E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.3GY 8.7/8.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | Bradford | 3.8GY 8.7/9.0 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | CAT02 | 3.8GY 8.7/8.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.2GY 8.7/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| D65 | Bradford | 5.2GY 8.7/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| D65 | CAT02 | 5.2GY 8.7/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | XYZScaling | 5.2GY 8.7/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | Bradford | 5.2GY 8.7/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | CAT02 | 5.2GY 8.7/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |

#### 84. Expected: strong yellow
Hex: #D4AF37

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.9GY 7.2/8.8 | strong greenish yellow | ❌ | strong greenish yellow | ❌ |  |
| C | Bradford | 1.3GY 7.2/8.9 | strong yellow green | ❌ | strong greenish yellow | ❌ |  |
| C | CAT02 | 1.3GY 7.2/8.8 | strong yellow green | ❌ | strong greenish yellow | ❌ |  |
| D65 | XYZScaling | 2.3GY 7.2/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | Bradford | 2.3GY 7.2/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | CAT02 | 2.3GY 7.2/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | XYZScaling | 2.4GY 7.2/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | Bradford | 2.3GY 7.2/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | CAT02 | 2.3GY 7.2/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |

#### 85. Expected: deep yellow
Hex: #AF8D13

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.7Y 5.9/8.4 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| C | Bradford | 0.2GY 5.9/8.4 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| C | CAT02 | 0.2GY 5.9/8.4 | deep greenish yellow | ❌ | deep greenish yellow | ❌ |  |
| D65 | XYZScaling | 1.1GY 5.9/8.7 | strong yellow green | ❌ | deep greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 1.1GY 5.9/8.7 | strong yellow green | ❌ | deep greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 1.1GY 5.9/8.7 | strong yellow green | ❌ | deep greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 1.1GY 5.9/8.7 | strong yellow green | ❌ | deep greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 1.1GY 5.9/8.7 | strong yellow green | ❌ | deep greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 1.1GY 5.9/8.7 | strong yellow green | ❌ | deep greenish yellow | ❌ | ±0.1 |

#### 86. Expected: light yellow
Hex: #F8DE7E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.6GY 8.9/7.5 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | Bradford | 5.8GY 8.8/7.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.8GY 8.8/7.5 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.9GY 8.9/8.4 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | Bradford | 6.9GY 8.9/8.4 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 6.9GY 8.9/8.4 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 6.9GY 8.9/8.5 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| F7 | Bradford | 6.8GY 8.9/8.5 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 6.8GY 8.9/8.5 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |

#### 87. Expected: moderate yellow
Hex: #C9AE5D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.2GY 7.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | Bradford | 2.5GY 7.1/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | CAT02 | 2.5GY 7.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 3.7GY 7.1/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | Bradford | 3.7GY 7.1/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | CAT02 | 3.7GY 7.1/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | XYZScaling | 3.7GY 7.1/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | Bradford | 3.7GY 7.1/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | CAT02 | 3.7GY 7.1/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |

#### 88. Expected: dark yellow
Hex: #AB9144

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.1GY 6.0/6.2 | moderate yellow green | ❌ | dark greenish yellow | ❌ | ±0.1 |
| C | Bradford | 1.4GY 6.0/6.2 | moderate yellow green | ❌ | dark greenish yellow | ❌ | ±0.1 |
| C | CAT02 | 1.4GY 6.0/6.2 | moderate yellow green | ❌ | dark greenish yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 2.3GY 6.0/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | Bradford | 2.3GY 6.0/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 2.3GY 6.0/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 2.3GY 6.0/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | Bradford | 2.3GY 6.0/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 2.3GY 6.0/6.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |

#### 89. Expected: pale yellow
Hex: #F3E5AB

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.4GY 9.1/4.0 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| C | Bradford | 3.6GY 9.1/4.0 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| C | CAT02 | 2.5GY 9.1/3.9 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 8.8Y 9.1/4.4 | pale greenish yellow | ❌ | pale greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 8.8Y 9.1/4.4 | pale greenish yellow | ❌ | pale greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 8.8Y 9.1/4.4 | pale greenish yellow | ❌ | pale greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 8.2GY 9.1/5.7 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 0.5GY 9.1/4.4 | pale greenish yellow | ❌ | pale greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 8.9Y 9.1/4.4 | pale greenish yellow | ❌ | pale greenish yellow | ❌ | ±0.1 |

#### 90. Expected: grayish yellow
Hex: #C2B280

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.9GY 7.2/4.2 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| C | Bradford | 4.1GY 7.2/4.2 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| C | CAT02 | 4.1GY 7.2/4.2 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | XYZScaling | 6.5GY 7.2/5.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | Bradford | 6.5GY 7.2/5.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | CAT02 | 6.5GY 7.2/5.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | XYZScaling | 6.5GY 7.2/5.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | Bradford | 6.5GY 7.2/5.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | CAT02 | 6.5GY 7.2/5.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |

#### 91. Expected: dark grayish yellow
Hex: #A18F60

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.8GY 5.9/4.0 | light olive | ❌ | light olive | ❌ | ±0.1 |
| C | Bradford | 1.9GY 5.9/4.0 | light olive | ❌ | light olive | ❌ | ±0.1 |
| C | CAT02 | 1.9GY 5.9/4.0 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | XYZScaling | 3.4GY 5.9/4.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | Bradford | 3.4GY 5.9/4.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 3.4GY 5.9/4.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 3.4GY 5.9/4.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | Bradford | 3.4GY 5.9/4.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 3.4GY 5.9/4.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |

#### 92. Expected: yellowish white
Hex: #F0EAD6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 0.1GY 9.3/1.7 | pale yellow green | ❌ | pale yellow green | ❌ |  |
| D65 | Bradford | 0.1GY 9.3/1.7 | pale yellow green | ❌ | pale yellow green | ❌ |  |
| D65 | CAT02 | 0.1GY 9.3/1.7 | pale yellow green | ❌ | pale yellow green | ❌ |  |
| F7 | XYZScaling | 5.7GY 9.3/2.0 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.7GY 9.3/2.0 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.6GY 9.3/2.0 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |

#### 93. Expected: yellowish gray
Hex: #BFB8A5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.0GY 7.4/1.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | Bradford | 7.0GY 7.4/1.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | CAT02 | 7.0GY 7.4/1.8 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 8.4GY 7.4/2.7 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.4GY 7.4/2.7 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.4GY 7.4/2.7 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 0.1G 7.4/3.0 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 9.9GY 7.4/3.0 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 9.2GY 7.4/2.8 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |

#### 94. Expected: light olive brown
Hex: #967117

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.9Y 4.9/7.2 | light olive | ❌ | light olive | ❌ |  |
| C | Bradford | 7.4Y 4.9/7.2 | light olive | ❌ | light olive | ❌ |  |
| C | CAT02 | 7.4Y 4.9/7.1 | light olive | ❌ | light olive | ❌ |  |
| D65 | XYZScaling | 8.5Y 4.9/7.3 | light olive | ❌ | light olive | ❌ |  |
| D65 | Bradford | 8.5Y 4.9/7.3 | light olive | ❌ | light olive | ❌ |  |
| D65 | CAT02 | 8.5Y 4.9/7.3 | light olive | ❌ | light olive | ❌ |  |
| F7 | XYZScaling | 8.5Y 4.9/7.3 | light olive | ❌ | light olive | ❌ |  |
| F7 | Bradford | 8.5Y 4.9/7.3 | light olive | ❌ | light olive | ❌ |  |
| F7 | CAT02 | 8.5Y 4.9/7.3 | light olive | ❌ | light olive | ❌ |  |

#### 95. Expected: moderate olive brown
Hex: #6C541E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.4Y 3.7/5.0 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| C | Bradford | 7.9Y 3.7/5.0 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| C | CAT02 | 7.8Y 3.6/4.9 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| D65 | XYZScaling | 9.1Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| D65 | Bradford | 9.1Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| D65 | CAT02 | 9.1Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| F7 | XYZScaling | 9.1Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| F7 | Bradford | 9.1Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| F7 | CAT02 | 9.1Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |

#### 96. Expected: dark olive brown
Hex: #3B3121

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.6Y 2.1/2.0 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| C | Bradford | 6.2Y 2.1/2.1 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| C | CAT02 | 6.2Y 2.1/2.0 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| D65 | XYZScaling | 8.6Y 2.1/2.3 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| D65 | Bradford | 8.6Y 2.1/2.3 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| D65 | CAT02 | 8.6Y 2.1/2.3 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| F7 | XYZScaling | 8.6Y 2.1/2.3 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| F7 | Bradford | 8.6Y 2.1/2.3 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |
| F7 | CAT02 | 8.6Y 2.1/2.3 | dark grayish olive | ❌ | dark grayish olive | ❌ | ±0.1 |

#### 97. Expected: vivid greenish yellow
Hex: #DCD300

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.5GY 8.2/11.9 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| C | Bradford | 5.5GY 8.2/12.0 | vivid yellow green | ❌ | vivid yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.5GY 8.2/11.8 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| D65 | XYZScaling | 5.6GY 8.2/12.3 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| D65 | Bradford | 5.6GY 8.2/12.3 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| D65 | CAT02 | 5.6GY 8.2/12.3 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| F7 | XYZScaling | 5.6GY 8.2/12.3 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| F7 | Bradford | 5.6GY 8.2/12.3 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| F7 | CAT02 | 5.6GY 8.2/12.3 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |

#### 98. Expected: brilliant greenish yellow
Hex: #E9E450

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8GY 8.8/10.7 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| C | Bradford | 7.2GY 8.8/10.9 | brilliant yellowish green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | CAT02 | 7.3GY 8.8/10.8 | brilliant yellowish green | ❌ | brilliant yellow green | ❌ |  |
| D65 | XYZScaling | 6.2GY 8.8/10.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | Bradford | 6.2GY 8.8/10.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 6.2GY 8.8/10.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 6.2GY 8.8/10.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| F7 | Bradford | 6.2GY 8.8/10.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 6.2GY 8.8/10.9 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |

#### 99. Expected: strong greenish yellow
Hex: #BEB72E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4GY 7.2/9.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| C | Bradford | 5.5GY 7.2/9.9 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| C | CAT02 | 5.5GY 7.2/9.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | XYZScaling | 5.6GY 7.2/10.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | Bradford | 5.6GY 7.2/10.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | CAT02 | 5.6GY 7.2/10.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | XYZScaling | 5.6GY 7.2/10.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | Bradford | 5.6GY 7.2/10.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | CAT02 | 5.6GY 7.2/10.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |

#### 100. Expected: deep greenish yellow
Hex: #9B9400

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.6GY 5.9/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| C | Bradford | 4.8GY 5.9/9.3 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| C | CAT02 | 4.8GY 5.9/9.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | XYZScaling | 5.2GY 5.9/9.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.2GY 5.9/9.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.2GY 5.9/9.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.2GY 5.9/9.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.2GY 5.9/9.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.2GY 5.9/9.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |

#### 101. Expected: light greenish yellow
Hex: #EAE679

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.5GY 8.9/9.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| C | Bradford | 8.6GY 8.9/9.2 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| C | CAT02 | 8.6GY 8.9/9.2 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | XYZScaling | 8.2GY 8.9/9.5 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.2GY 8.9/9.5 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.2GY 8.9/9.5 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.1GY 8.9/9.5 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.2GY 8.9/9.5 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.2GY 8.9/9.5 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |

#### 102. Expected: moderate greenish yellow
Hex: #B9B459

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.9GY 7.1/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | Bradford | 6.0GY 7.1/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | CAT02 | 6.0GY 7.1/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.2GY 7.1/8.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | Bradford | 6.2GY 7.1/8.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | CAT02 | 6.2GY 7.1/8.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | XYZScaling | 6.2GY 7.1/8.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | Bradford | 6.2GY 7.1/8.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | CAT02 | 6.2GY 7.1/8.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |

#### 103. Expected: dark greenish yellow
Hex: #98943E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.3GY 5.9/7.0 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | Bradford | 5.4GY 5.9/7.0 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.4GY 5.9/7.0 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.7GY 5.9/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.7GY 5.9/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.7GY 5.9/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.7GY 5.9/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.7GY 5.9/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.7GY 5.9/7.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |

#### 104. Expected: pale greenish yellow
Hex: #EBE8A4

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.7GY 9.1/5.4 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| C | CAT02 | 8.1GY 9.1/5.5 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | XYZScaling | 9.5GY 9.1/6.9 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 9.5GY 9.1/6.9 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 9.5GY 9.1/6.9 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 9.4GY 9.1/6.8 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 9.5GY 9.1/6.9 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 9.4GY 9.1/6.8 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |

#### 105. Expected: grayish greenish yellow
Hex: #B9B57D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.6GY 7.2/5.3 | light yellowish green | ❌ | moderate yellow green | ❌ |  |
| C | Bradford | 7.9GY 7.2/5.4 | light yellowish green | ❌ | moderate yellow green | ❌ |  |
| C | CAT02 | 7.9GY 7.2/5.4 | light yellowish green | ❌ | moderate yellow green | ❌ |  |
| D65 | XYZScaling | 7.7GY 7.2/5.9 | light yellowish green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | Bradford | 7.7GY 7.2/5.9 | light yellowish green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 7.7GY 7.2/5.9 | light yellowish green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 7.7GY 7.2/6.0 | light yellowish green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | Bradford | 7.7GY 7.2/6.0 | light yellowish green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 7.7GY 7.2/6.0 | light yellowish green | ❌ | moderate yellow green | ❌ | ±0.1 |

#### 106. Expected: light olive
Hex: #867E36

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.1GY 5.1/6.0 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | Bradford | 4.4GY 5.1/6.1 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | CAT02 | 4.4GY 5.1/6.0 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.1GY 5.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.1GY 5.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.1GY 5.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.1GY 5.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.1GY 5.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.1GY 5.1/6.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |

#### 107. Expected: moderate olive
Hex: #665D1E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.2GY 3.8/5.3 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| C | Bradford | 2.5GY 3.8/5.3 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| C | CAT02 | 2.5GY 3.8/5.3 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| D65 | XYZScaling | 3.6GY 3.8/5.7 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| D65 | Bradford | 3.6GY 3.8/5.7 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| D65 | CAT02 | 3.6GY 3.8/5.7 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| F7 | XYZScaling | 3.6GY 3.8/5.7 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| F7 | Bradford | 3.5GY 3.8/5.7 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| F7 | CAT02 | 3.6GY 3.8/5.7 | moderate olive green | ❌ | moderate olive green | ❌ |  |

#### 108. Expected: dark olive
Hex: #403D21

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.5GY 2.5/3.0 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| C | Bradford | 2.8GY 2.5/3.1 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| C | CAT02 | 2.8GY 2.5/3.1 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.2GY 2.5/3.5 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| D65 | Bradford | 4.2GY 2.5/3.5 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| D65 | CAT02 | 4.2GY 2.5/3.5 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.2GY 2.5/3.5 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| F7 | Bradford | 4.2GY 2.5/3.5 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| F7 | CAT02 | 4.2GY 2.5/3.5 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |

#### 109. Expected: light grayish olive
Hex: #8C8767

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.1GY 5.5/2.9 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | Bradford | 5.2GY 5.5/2.9 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.2GY 5.5/2.9 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.9GY 5.5/3.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.9GY 5.5/3.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.9GY 5.5/3.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.9GY 5.5/3.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.9GY 5.5/3.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.9GY 5.5/3.6 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |

#### 110. Expected: grayish olive
Hex: #5B5842

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.3GY 3.6/2.2 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| C | Bradford | 3.7GY 3.6/2.3 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| C | CAT02 | 3.7GY 3.6/2.2 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| D65 | XYZScaling | 5.4GY 3.6/2.7 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| D65 | Bradford | 5.4GY 3.6/2.7 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| D65 | CAT02 | 5.4GY 3.6/2.7 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| F7 | XYZScaling | 5.4GY 3.6/2.8 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| F7 | Bradford | 5.4GY 3.7/2.8 | grayish olive green | ❌ | grayish olive green | ❌ |  |
| F7 | CAT02 | 5.4GY 3.7/2.8 | grayish olive green | ❌ | grayish olive green | ❌ |  |

#### 111. Expected: dark grayish olive
Hex: #363527

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.2GY 2.2/1.9 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| C | Bradford | 3.5GY 2.2/2.0 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| C | CAT02 | 3.5GY 2.2/2.0 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.2GY 2.2/2.4 | dark grayish olive green | ❌ | dark grayish olive green | ❌ |  |
| D65 | Bradford | 5.2GY 2.2/2.4 | dark grayish olive green | ❌ | dark grayish olive green | ❌ |  |
| D65 | CAT02 | 5.2GY 2.2/2.4 | dark grayish olive green | ❌ | dark grayish olive green | ❌ |  |
| F7 | XYZScaling | 5.2GY 2.2/2.4 | dark grayish olive green | ❌ | dark grayish olive green | ❌ |  |
| F7 | Bradford | 5.2GY 2.2/2.4 | dark grayish olive green | ❌ | dark grayish olive green | ❌ |  |
| F7 | CAT02 | 5.2GY 2.2/2.4 | dark grayish olive green | ❌ | dark grayish olive green | ❌ |  |

#### 112. Expected: light olive gray
Hex: #8A8776

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.3GY 5.5/1.6 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | Bradford | 5.5GY 5.5/1.6 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.5GY 5.5/1.6 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.4GY 5.5/2.2 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | Bradford | 6.4GY 5.5/2.2 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 6.4GY 5.5/2.2 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 6.4GY 5.5/2.3 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | Bradford | 6.4GY 5.5/2.3 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 6.4GY 5.5/2.3 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |

#### 113. Expected: olive gray
Hex: #57554C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 5.8GY 3.5/1.5 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| D65 | Bradford | 5.8GY 3.5/1.5 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| D65 | CAT02 | 5.8GY 3.5/1.5 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.8GY 3.5/1.5 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| F7 | Bradford | 5.8GY 3.5/1.5 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| F7 | CAT02 | 5.8GY 3.5/1.5 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |

#### 114. Expected: olive black
Hex: #25241D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.5GY 1.4/1.4 | dark olive green | ❌ | dark olive green | ❌ |  |
| D65 | Bradford | 4.5GY 1.4/1.4 | dark olive green | ❌ | dark olive green | ❌ |  |
| D65 | CAT02 | 4.5GY 1.4/1.4 | dark olive green | ❌ | dark olive green | ❌ |  |
| F7 | XYZScaling | 4.5GY 1.4/1.4 | dark olive green | ❌ | dark olive green | ❌ | ±0.1 |
| F7 | Bradford | 4.5GY 1.4/1.4 | dark olive green | ❌ | dark olive green | ❌ | ±0.1 |
| F7 | CAT02 | 4.5GY 1.4/1.4 | dark olive green | ❌ | dark olive green | ❌ | ±0.1 |

#### 115. Expected: vivid yellow green
Hex: #8DB600

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9GY 6.8/12.1 | vivid yellowish green | ❌ | vivid yellow green | ✅ | ±0.1 |
| C | Bradford | 8.0GY 6.8/12.1 | vivid yellowish green | ❌ | vivid yellow green | ✅ |  |
| C | CAT02 | 8.0GY 6.8/12.0 | vivid yellowish green | ❌ | vivid yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.3GY 6.8/12.7 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| D65 | Bradford | 8.3GY 6.8/12.7 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| D65 | CAT02 | 8.3GY 6.8/12.7 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | XYZScaling | 8.3GY 6.8/12.7 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | Bradford | 8.3GY 6.8/12.7 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | CAT02 | 8.3GY 6.8/12.7 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |

#### 116. Expected: brilliant yellow green
Hex: #BDDA57

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.6GY 8.2/10.2 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |  |
| C | Bradford | 7.6GY 8.2/10.3 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |  |
| C | CAT02 | 7.6GY 8.2/10.2 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |  |
| D65 | XYZScaling | 8.1GY 8.2/11.1 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.1GY 8.2/11.1 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.1GY 8.2/11.1 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.1GY 8.2/11.1 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.1GY 8.2/11.1 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.1GY 8.2/11.1 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |

#### 117. Expected: strong yellow green
Hex: #7E9F2E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.1GY 6.0/9.6 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| C | Bradford | 8.1GY 6.0/9.6 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| C | CAT02 | 8.1GY 6.0/9.5 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| D65 | XYZScaling | 8.5GY 6.0/10.3 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.5GY 6.0/10.3 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.5GY 6.0/10.3 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.5GY 6.0/10.3 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.5GY 6.0/10.3 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.5GY 6.0/10.3 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |

#### 118. Expected: deep yellow green
Hex: #467129

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.2GY 4.2/7.4 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| C | Bradford | 9.1GY 4.2/7.4 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| C | CAT02 | 9.2GY 4.2/7.4 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |
| D65 | XYZScaling | 9.1GY 4.2/7.8 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |
| D65 | Bradford | 9.1GY 4.2/7.8 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |
| D65 | CAT02 | 9.1GY 4.2/7.8 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |
| F7 | XYZScaling | 9.1GY 4.2/7.8 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |
| F7 | Bradford | 9.1GY 4.2/7.8 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |
| F7 | CAT02 | 9.1GY 4.2/7.8 | deep yellowish green | ❌ | deep yellowish green | ❌ |  |

#### 119. Expected: light yellow green
Hex: #C9DC89

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.6GY 8.4/7.8 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.6GY 8.4/7.8 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.6GY 8.4/7.8 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.6GY 8.4/7.8 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.5GY 8.4/7.8 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.5GY 8.4/7.8 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |

#### 120. Expected: moderate yellow green
Hex: #8A9A5B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.7GY 6.0/5.9 | moderate yellowish green | ❌ | moderate yellow green | ✅ | ±0.1 |
| C | Bradford | 7.8GY 6.0/5.9 | moderate yellowish green | ❌ | moderate yellow green | ✅ | ±0.1 |
| C | CAT02 | 7.8GY 6.0/5.9 | moderate yellowish green | ❌ | moderate yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.3GY 6.0/6.6 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.3GY 6.0/6.6 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.3GY 6.0/6.6 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.3GY 6.0/6.6 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.3GY 6.0/6.6 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.3GY 6.0/6.6 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |

#### 121. Expected: pale yellow green
Hex: #DADFB7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.1G 8.7/4.4 | very light green | ❌ | very light yellowish green | ❌ |  |
| D65 | XYZScaling | 8.5GY 8.7/4.1 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| D65 | Bradford | 8.5GY 8.7/4.1 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| D65 | CAT02 | 8.5GY 8.7/4.1 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| F7 | XYZScaling | 8.5GY 8.7/4.1 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| F7 | Bradford | 8.5GY 8.7/4.1 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| F7 | CAT02 | 8.5GY 8.7/4.1 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |

#### 122. Expected: grayish yellow green
Hex: #8F9779

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.7GY 6.0/2.8 | moderate yellowish green | ❌ | grayish yellow green | ✅ | ±0.1 |
| C | Bradford | 7.8GY 6.0/2.8 | moderate yellowish green | ❌ | grayish yellow green | ✅ | ±0.1 |
| C | CAT02 | 7.8GY 6.0/2.8 | moderate yellowish green | ❌ | grayish yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.9GY 6.0/3.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.9GY 6.0/3.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.9GY 6.0/3.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.9GY 6.0/3.8 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.9GY 6.0/3.8 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.9GY 6.0/3.8 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |

#### 123. Expected: strong olive green
Hex: #404F00

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.5GY 3.1/6.8 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| C | Bradford | 6.5GY 3.1/6.9 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |
| C | CAT02 | 6.5GY 3.1/6.8 | moderate olive green | ❌ | moderate olive green | ❌ | ±0.1 |

#### 124. Expected: deep olive green
Hex: #232F00

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.9GY 1.7/4.6 | dark olive green | ❌ | dark olive green | ❌ | ±0.1 |
| C | Bradford | 5.9GY 1.7/4.6 | dark olive green | ❌ | dark olive green | ❌ | ±0.1 |
| C | CAT02 | 5.9GY 1.7/4.5 | dark olive green | ❌ | dark olive green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.0GY 1.7/4.7 | dark olive green | ❌ | dark olive green | ❌ |  |
| D65 | Bradford | 6.0GY 1.7/4.7 | dark olive green | ❌ | dark olive green | ❌ |  |
| D65 | CAT02 | 6.0GY 1.7/4.7 | dark olive green | ❌ | dark olive green | ❌ |  |
| F7 | XYZScaling | 6.0GY 1.7/4.7 | dark olive green | ❌ | dark olive green | ❌ |  |
| F7 | Bradford | 6.0GY 1.7/4.7 | dark olive green | ❌ | dark olive green | ❌ |  |
| F7 | CAT02 | 6.0GY 1.7/4.7 | dark olive green | ❌ | dark olive green | ❌ |  |

#### 125. Expected: moderate olive green
Hex: #4A5D23

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.6GY 3.6/5.9 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| C | Bradford | 7.6GY 3.6/5.9 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| C | CAT02 | 7.6GY 3.6/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| D65 | XYZScaling | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| D65 | Bradford | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| D65 | CAT02 | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| F7 | XYZScaling | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| F7 | Bradford | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |  |
| F7 | CAT02 | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |  |

#### 126. Expected: dark olive green
Hex: #2B3D26

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.3GY 2.3/3.5 | very dark yellowish green | ❌ | very dark yellowish green | ❌ | ±0.1 |
| C | Bradford | 9.3GY 2.3/3.5 | very dark yellowish green | ❌ | very dark yellowish green | ❌ | ±0.1 |
| C | CAT02 | 9.3GY 2.3/3.4 | very dark yellowish green | ❌ | very dark yellowish green | ❌ | ±0.1 |
| D65 | XYZScaling | 9.0GY 2.3/3.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| D65 | Bradford | 9.0GY 2.3/3.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| D65 | CAT02 | 9.0GY 2.3/3.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | XYZScaling | 9.0GY 2.3/3.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | Bradford | 9.0GY 2.3/3.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | CAT02 | 9.0GY 2.3/3.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |

#### 127. Expected: grayish olive green
Hex: #515744

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.5GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ | ±0.1 |
| C | Bradford | 7.5GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ | ±0.1 |
| C | CAT02 | 7.5GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.3GY 3.5/2.8 | dark yellowish green | ❌ | dark yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.3GY 3.5/2.8 | dark yellowish green | ❌ | dark yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.3GY 3.5/2.8 | dark yellowish green | ❌ | dark yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.3GY 3.5/2.8 | dark yellowish green | ❌ | dark yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.3GY 3.5/2.8 | dark yellowish green | ❌ | dark yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.3GY 3.5/2.8 | dark yellowish green | ❌ | dark yellowish green | ❌ | ±0.1 |

#### 128. Expected: dark grayish olive green
Hex: #31362B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.2GY 2.2/2.3 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| D65 | Bradford | 8.2GY 2.2/2.3 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| D65 | CAT02 | 8.2GY 2.2/2.3 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | XYZScaling | 8.2GY 2.2/2.3 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | Bradford | 8.2GY 2.2/2.3 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | CAT02 | 8.2GY 2.2/2.3 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |

#### 129. Expected: vivid yellowish green
Hex: #27A64C - **All configurations matched**

#### 130. Expected: brilliant yellowish green
Hex: #83D37D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 2.7G 7.7/11.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| D65 | Bradford | 2.7G 7.7/11.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| D65 | CAT02 | 2.7G 7.7/11.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | XYZScaling | 2.7G 7.7/11.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | Bradford | 2.7G 7.7/11.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | CAT02 | 2.7G 7.7/11.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |

#### 131. Expected: strong yellowish green
Hex: #44944A - **All configurations matched**

#### 132. Expected: deep yellowish green
Hex: #00622D - **All configurations matched**

#### 133. Expected: very deep yellowish green
Hex: #003118

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.3G 1.7/4.6 | very dark green | ❌ | very dark yellowish green | ❌ |  |
| C | Bradford | 2.2G 1.6/4.5 | very dark green | ❌ | very dark yellowish green | ❌ | ±0.1 |
| C | CAT02 | 2.2G 1.6/4.5 | very dark green | ❌ | very dark yellowish green | ❌ | ±0.1 |
| D65 | XYZScaling | 1.8G 1.7/4.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| D65 | Bradford | 1.8G 1.7/4.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| D65 | CAT02 | 1.8G 1.7/4.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | XYZScaling | 1.8G 1.7/4.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | Bradford | 1.8G 1.7/4.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |
| F7 | CAT02 | 1.8G 1.7/4.8 | very dark yellowish green | ❌ | very dark yellowish green | ❌ |  |

#### 134. Expected: very light yellowish green
Hex: #B6E5AF

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.2G 8.6/6.2 | very light green | ❌ | very light green | ❌ |  |
| C | Bradford | 4.1G 8.6/6.2 | very light green | ❌ | very light green | ❌ |  |
| C | CAT02 | 4.1G 8.6/6.1 | very light green | ❌ | very light green | ❌ |  |
| D65 | XYZScaling | 4.0G 8.6/7.5 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| D65 | Bradford | 4.0G 8.6/7.5 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| D65 | CAT02 | 4.0G 8.6/7.5 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.0G 8.6/7.5 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| F7 | Bradford | 4.0G 8.6/7.5 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| F7 | CAT02 | 4.0G 8.6/7.5 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |

#### 135. Expected: light yellowish green
Hex: #93C592

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.0G 7.4/6.6 | light green | ❌ | light green | ❌ | ±0.1 |
| C | Bradford | 4.0G 7.4/6.6 | light green | ❌ | light green | ❌ | ±0.1 |
| C | CAT02 | 4.0G 7.4/6.5 | light green | ❌ | light green | ❌ | ±0.1 |
| D65 | XYZScaling | 3.7G 7.4/7.7 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| D65 | Bradford | 3.7G 7.4/7.7 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| D65 | CAT02 | 3.7G 7.4/7.7 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| F7 | XYZScaling | 3.6G 7.4/7.7 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| F7 | Bradford | 3.6G 7.4/7.7 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| F7 | CAT02 | 3.6G 7.4/7.7 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |

#### 136. Expected: moderate yellowish green
Hex: #679267 - **All configurations matched**

#### 137. Expected: dark yellowish green
Hex: #355E3B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.1G 3.6/5.2 | moderate green | ❌ | dark yellowish green | ✅ | ±0.1 |
| C | CAT02 | 2.1G 3.5/5.1 | moderate green | ❌ | dark yellowish green | ✅ | ±0.1 |

#### 138. Expected: very dark yellowish green
Hex: #173620 - **All configurations matched**

#### 139. Expected: vivid green
Hex: #008856

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.1BG 4.9/10.4 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| C | Bradford | 9.9G 4.9/10.2 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| C | CAT02 | 10.0G 4.9/10.2 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| D65 | XYZScaling | 8.3G 4.9/10.9 | strong green | ❌ | strong green | ❌ | ±0.1 |
| D65 | Bradford | 8.3G 4.9/10.9 | strong green | ❌ | strong green | ❌ | ±0.1 |
| D65 | CAT02 | 8.3G 4.9/10.9 | strong green | ❌ | strong green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.2G 4.9/10.9 | strong green | ❌ | strong green | ❌ | ±0.1 |
| F7 | Bradford | 8.2G 4.9/10.9 | strong green | ❌ | strong green | ❌ | ±0.1 |
| F7 | CAT02 | 8.2G 4.9/10.9 | strong green | ❌ | strong green | ❌ | ±0.1 |

#### 140. Expected: brilliant green
Hex: #3EB489

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.7BG 6.5/8.5 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| C | Bradford | 6.6BG 6.5/8.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| C | CAT02 | 6.7BG 6.5/8.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.3BG 6.5/10.0 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| D65 | Bradford | 5.3BG 6.5/10.0 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 5.3BG 6.5/10.0 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.3BG 6.5/10.1 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| F7 | Bradford | 5.3BG 6.5/10.1 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 5.3BG 6.5/10.1 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |

#### 141. Expected: strong green
Hex: #007959

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.5BG 4.4/7.2 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| C | Bradford | 5.5BG 4.4/7.1 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| C | CAT02 | 5.5BG 4.4/7.0 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.1BG 4.4/8.4 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| D65 | Bradford | 4.1BG 4.4/8.4 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| D65 | CAT02 | 4.1BG 4.4/8.4 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| F7 | XYZScaling | 4.1BG 4.4/8.4 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| F7 | Bradford | 4.1BG 4.4/8.4 | strong bluish green | ❌ | strong bluish green | ❌ |  |
| F7 | CAT02 | 4.1BG 4.4/8.4 | strong bluish green | ❌ | strong bluish green | ❌ |  |

#### 142. Expected: deep green
Hex: #00543D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.9BG 3.1/6.0 | dark bluish green | ❌ | dark bluish green | ❌ | ±0.1 |
| C | Bradford | 3.8BG 3.1/5.9 | dark bluish green | ❌ | dark bluish green | ❌ | ±0.1 |
| C | CAT02 | 3.8BG 3.1/5.8 | dark bluish green | ❌ | dark bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 1.8BG 3.1/7.0 | deep bluish green | ❌ | deep bluish green | ❌ | ±0.1 |
| D65 | Bradford | 1.8BG 3.1/7.0 | deep bluish green | ❌ | deep bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 1.8BG 3.1/7.0 | deep bluish green | ❌ | deep bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 1.8BG 3.1/7.0 | deep bluish green | ❌ | deep bluish green | ❌ | ±0.1 |
| F7 | Bradford | 1.8BG 3.1/7.0 | deep bluish green | ❌ | deep bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 1.8BG 3.1/7.0 | deep bluish green | ❌ | deep bluish green | ❌ | ±0.1 |

#### 143. Expected: very light green
Hex: #8ED1B2

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.0BG 7.8/5.0 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| C | Bradford | 7.9BG 7.8/4.9 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| C | CAT02 | 7.9BG 7.8/4.8 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| D65 | XYZScaling | 5.5BG 7.8/6.6 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| D65 | Bradford | 5.5BG 7.8/6.6 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| D65 | CAT02 | 5.5BG 7.8/6.6 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| F7 | XYZScaling | 5.4BG 7.8/6.7 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| F7 | Bradford | 5.4BG 7.8/6.7 | very light bluish green | ❌ | very light bluish green | ❌ |  |
| F7 | CAT02 | 5.4BG 7.8/6.7 | very light bluish green | ❌ | very light bluish green | ❌ |  |

#### 144. Expected: light green
Hex: #6AAB8E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.7BG 6.4/5.1 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| C | Bradford | 6.6BG 6.4/5.0 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| C | CAT02 | 6.7BG 6.4/4.9 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.3BG 6.4/6.6 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | Bradford | 4.3BG 6.4/6.6 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 4.3BG 6.4/6.6 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.2BG 6.4/6.6 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | Bradford | 4.2BG 6.4/6.6 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 4.2BG 6.4/6.6 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |

#### 145. Expected: moderate green
Hex: #3B7861

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.3BG 4.5/4.7 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | Bradford | 6.3BG 4.5/4.5 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | CAT02 | 6.3BG 4.5/4.5 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.2BG 4.5/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | Bradford | 4.2BG 4.5/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 4.2BG 4.5/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.1BG 4.5/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | Bradford | 4.1BG 4.5/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 4.1BG 4.5/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |

#### 146. Expected: dark green
Hex: #1B4D3E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.8BG 2.9/3.8 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| C | Bradford | 5.8BG 2.9/3.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| C | CAT02 | 5.8BG 2.9/3.6 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| D65 | XYZScaling | 3.8BG 2.9/4.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| D65 | Bradford | 3.8BG 2.9/4.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| D65 | CAT02 | 3.8BG 2.9/4.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| F7 | XYZScaling | 3.7BG 2.9/4.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| F7 | Bradford | 3.7BG 2.9/4.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| F7 | CAT02 | 3.7BG 2.9/4.7 | dark bluish green | ❌ | dark bluish green | ❌ |  |

#### 147. Expected: very dark green
Hex: #1C352D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.1BG 2.0/2.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| C | Bradford | 5.1BG 2.0/2.4 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| C | CAT02 | 5.1BG 2.0/2.4 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 1.5BG 2.0/3.2 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| D65 | Bradford | 1.5BG 2.0/3.2 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 1.5BG 2.0/3.2 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 1.4BG 2.0/3.2 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| F7 | Bradford | 1.4BG 2.0/3.2 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 1.4BG 2.0/3.2 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |

#### 148. Expected: very pale green
Hex: #C7E6D7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.5BG 8.9/2.0 | very pale blue | ❌ | very pale green | ✅ | ±0.1 |
| C | Bradford | 9.4BG 8.8/2.0 | very pale blue | ❌ | very pale green | ✅ | ±0.1 |
| C | CAT02 | 9.4BG 8.8/2.0 | very pale blue | ❌ | very pale green | ✅ | ±0.1 |
| D65 | XYZScaling | 5.2BG 8.9/3.5 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| D65 | Bradford | 5.2BG 8.9/3.5 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 5.2BG 8.9/3.5 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.1BG 8.9/3.5 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| F7 | Bradford | 5.1BG 8.9/3.5 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 5.1BG 8.9/3.5 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |

#### 149. Expected: pale green
Hex: #8DA399

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.8BG 6.4/2.8 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | Bradford | 1.8BG 6.4/2.8 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 1.8BG 6.4/2.8 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 1.5BG 6.4/2.8 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | Bradford | 1.5BG 6.4/2.8 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 1.5BG 6.4/2.8 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |

#### 150. Expected: grayish green
Hex: #5E716A - **All configurations matched**

#### 151. Expected: dark grayish green
Hex: #3A4B47

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.4BG 3.0/1.2 | dark bluish gray | ❌ | dark grayish green | ✅ | ±0.1 |
| C | Bradford | 9.4BG 3.0/1.2 | dark bluish gray | ❌ | dark grayish green | ✅ | ±0.1 |
| C | CAT02 | 9.4BG 3.0/1.2 | dark bluish gray | ❌ | dark grayish green | ✅ | ±0.1 |

#### 152. Expected: blackish green
Hex: #1A2421

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.8BG 1.3/1.0 | greenish black | ❌ | greenish black | ❌ | ±0.1 |
| C | Bradford | 5.8BG 1.3/0.9 | greenish black | ❌ | greenish black | ❌ | ±0.1 |
| C | CAT02 | 5.8BG 1.3/0.9 | greenish black | ❌ | greenish black | ❌ | ±0.1 |

#### 153. Expected: greenish white
Hex: #DFEDE8

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.1B 9.2/0.8 | bluish white | ❌ | bluish white | ❌ |  |
| C | Bradford | 2.1B 9.2/0.8 | bluish white | ❌ | bluish white | ❌ |  |
| C | CAT02 | 2.1B 9.2/0.8 | bluish white | ❌ | bluish white | ❌ |  |
| D65 | XYZScaling | 0.2BG 9.2/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| D65 | Bradford | 0.2BG 9.2/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| D65 | CAT02 | 0.2BG 9.2/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| F7 | XYZScaling | 9.1G 9.2/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| F7 | Bradford | 9.1G 9.2/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| F7 | CAT02 | 9.2G 9.2/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |

#### 154. Expected: light greenish gray
Hex: #B2BEB5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 3.3G 7.5/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| D65 | Bradford | 3.3G 7.5/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| D65 | CAT02 | 3.3G 7.5/2.0 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| F7 | XYZScaling | 3.3G 7.5/2.1 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| F7 | Bradford | 3.3G 7.5/2.1 | very pale green | ❌ | very pale green | ❌ | ±0.1 |
| F7 | CAT02 | 3.3G 7.5/2.1 | very pale green | ❌ | very pale green | ❌ | ±0.1 |

#### 155. Expected: greenish gray
Hex: #7D8984

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.2G 5.5/1.9 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| D65 | Bradford | 8.2G 5.5/1.9 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.2G 5.5/1.9 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| F7 | XYZScaling | 7.9G 5.5/1.9 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| F7 | Bradford | 7.9G 5.5/1.9 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| F7 | CAT02 | 7.9G 5.5/1.9 | grayish green | ❌ | grayish green | ❌ | ±0.1 |

#### 156. Expected: dark greenish gray
Hex: #4E5755

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.4B 3.6/0.6 | dark bluish gray | ❌ | dark bluish gray | ❌ | ±0.1 |
| C | Bradford | 0.5B 3.6/0.6 | dark bluish gray | ❌ | dark bluish gray | ❌ | ±0.1 |
| C | CAT02 | 0.5B 3.6/0.6 | dark bluish gray | ❌ | dark bluish gray | ❌ | ±0.1 |
| D65 | XYZScaling | 1.0BG 3.6/1.4 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| D65 | Bradford | 1.0BG 3.6/1.4 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| D65 | CAT02 | 1.0BG 3.6/1.4 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| F7 | XYZScaling | 0.5BG 3.6/1.4 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| F7 | Bradford | 0.5BG 3.6/1.4 | grayish green | ❌ | grayish green | ❌ | ±0.1 |
| F7 | CAT02 | 0.5BG 3.6/1.4 | grayish green | ❌ | grayish green | ❌ | ±0.1 |

#### 157. Expected: greenish black
Hex: #1E2321

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 2.7G 1.3/1.1 | blackish green | ❌ | blackish green | ❌ | ±0.1 |
| D65 | Bradford | 2.7G 1.3/1.1 | blackish green | ❌ | blackish green | ❌ | ±0.1 |
| D65 | CAT02 | 2.7G 1.3/1.1 | blackish green | ❌ | blackish green | ❌ | ±0.1 |
| F7 | XYZScaling | 2.5G 1.3/1.1 | blackish green | ❌ | blackish green | ❌ | ±0.1 |
| F7 | Bradford | 2.5G 1.3/1.1 | blackish green | ❌ | blackish green | ❌ | ±0.1 |
| F7 | CAT02 | 2.5G 1.3/1.1 | blackish green | ❌ | blackish green | ❌ | ±0.1 |

#### 158. Expected: vivid bluish green
Hex: #008882

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.9BG 5.0/5.8 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | Bradford | 9.8BG 5.0/5.6 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | CAT02 | 9.8BG 5.0/5.6 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 1.3B 5.0/5.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.3B 5.0/5.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.3B 5.0/5.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.4B 5.0/5.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.4B 5.0/5.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.4B 5.0/5.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |

#### 159. Expected: brilliant bluish green
Hex: #00A693

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.6B 6.0/6.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| C | Bradford | 1.7B 6.0/6.1 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| C | CAT02 | 1.7B 6.0/6.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ | ±0.1 |
| D65 | Bradford | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ | ±0.1 |
| D65 | CAT02 | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ | ±0.1 |
| F7 | XYZScaling | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ | ±0.1 |
| F7 | Bradford | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ | ±0.1 |
| F7 | CAT02 | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ | ±0.1 |

#### 160. Expected: strong bluish green
Hex: #007A74

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.8BG 4.5/5.2 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | Bradford | 9.7BG 4.5/5.0 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | CAT02 | 9.7BG 4.5/5.0 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 1.1B 4.5/5.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.1B 4.5/5.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.1B 4.5/5.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.1B 4.5/5.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.1B 4.5/5.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.1B 4.5/5.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |

#### 161. Expected: deep bluish green
Hex: #00443F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.0BG 2.5/3.5 | dark bluish green | ❌ | dark bluish green | ❌ | ±0.1 |
| C | Bradford | 8.9BG 2.5/3.4 | dark bluish green | ❌ | dark bluish green | ❌ | ±0.1 |
| C | CAT02 | 9.0BG 2.5/3.4 | dark bluish green | ❌ | dark bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 9.6BG 2.5/3.5 | dark greenish blue | ❌ | dark bluish green | ❌ | ±0.1 |
| D65 | Bradford | 9.6BG 2.5/3.5 | dark greenish blue | ❌ | dark bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 9.6BG 2.5/3.5 | dark greenish blue | ❌ | dark bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 9.6BG 2.5/3.5 | dark greenish blue | ❌ | dark bluish green | ❌ | ±0.1 |
| F7 | Bradford | 9.6BG 2.5/3.5 | dark greenish blue | ❌ | dark bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 9.6BG 2.5/3.5 | dark greenish blue | ❌ | dark bluish green | ❌ | ±0.1 |

#### 162. Expected: very light bluish green
Hex: #96DED1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.9B 8.3/3.8 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| C | Bradford | 3.9B 8.3/3.6 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| C | CAT02 | 3.9B 8.3/3.6 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| D65 | XYZScaling | 1.5B 8.3/4.4 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| D65 | Bradford | 1.5B 8.3/4.4 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| D65 | CAT02 | 1.5B 8.3/4.4 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| F7 | XYZScaling | 1.5B 8.3/4.4 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| F7 | Bradford | 1.5B 8.3/4.4 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |
| F7 | CAT02 | 1.5B 8.3/4.4 | very light greenish blue | ❌ | very light greenish blue | ❌ |  |

#### 163. Expected: light bluish green
Hex: #66ADA4

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.4B 6.5/3.9 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| C | Bradford | 2.3B 6.5/3.8 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| C | CAT02 | 2.3B 6.5/3.8 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.3B 6.5/4.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.3B 6.5/4.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.3B 6.5/4.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.3B 6.5/4.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.3B 6.5/4.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.3B 6.5/4.3 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |

#### 164. Expected: moderate bluish green
Hex: #317873

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.1B 4.5/4.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.4B 4.5/3.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.4B 4.5/3.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.4B 4.5/3.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.4B 4.5/3.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.4B 4.5/3.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.4B 4.5/3.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |

#### 165. Expected: dark bluish green
Hex: #004B49

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 9.3BG 2.8/3.7 | dark greenish blue | ❌ | dark bluish green | ✅ |  |
| D65 | Bradford | 9.3BG 2.8/3.7 | dark greenish blue | ❌ | dark bluish green | ✅ |  |
| D65 | CAT02 | 9.3BG 2.8/3.7 | dark greenish blue | ❌ | dark bluish green | ✅ |  |
| F7 | XYZScaling | 9.3BG 2.8/3.7 | dark greenish blue | ❌ | dark bluish green | ✅ |  |
| F7 | Bradford | 9.3BG 2.8/3.7 | dark greenish blue | ❌ | dark bluish green | ✅ |  |
| F7 | CAT02 | 9.3BG 2.8/3.7 | dark greenish blue | ❌ | dark bluish green | ✅ |  |

#### 166. Expected: very dark bluish green
Hex: #002A29 - **All configurations matched**

#### 167. Expected: vivid greenish blue
Hex: #0085A1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.5B 5.0/7.6 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| C | Bradford | 2.8B 5.0/7.4 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| C | CAT02 | 2.8B 5.0/7.4 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.5B 5.0/7.2 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.5B 5.0/7.2 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.5B 5.0/7.2 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.4B 5.0/7.2 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.4B 5.0/7.2 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.4B 5.0/7.2 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |

#### 168. Expected: brilliant greenish blue
Hex: #239EBA - **All configurations matched**

#### 169. Expected: strong greenish blue
Hex: #007791

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.3B 4.5/6.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| C | Bradford | 2.6B 4.5/6.8 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| C | CAT02 | 2.5B 4.5/6.7 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.2B 4.5/6.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.2B 4.5/6.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.2B 4.5/6.6 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.2B 4.5/6.5 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.2B 4.5/6.5 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.2B 4.5/6.5 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |

#### 170. Expected: deep greenish blue
Hex: #2E8495

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.3B 5.0/6.2 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| C | Bradford | 1.5B 5.0/6.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| C | CAT02 | 1.5B 5.0/6.0 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 9.6BG 5.0/5.9 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | Bradford | 9.6BG 5.0/5.9 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 9.6BG 5.0/5.9 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 9.6BG 5.0/5.9 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | Bradford | 9.6BG 5.0/5.9 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 9.6BG 5.0/5.9 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |

#### 171. Expected: very light greenish blue
Hex: #9CD1DC - **All configurations matched**

#### 172. Expected: light greenish blue
Hex: #66AABC - **All configurations matched**

#### 173. Expected: moderate greenish blue
Hex: #367588 - **All configurations matched**

#### 174. Expected: dark greenish blue
Hex: #004958

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 9.6BG 2.8/4.6 | dark greenish blue | ✅ | dark bluish green | ❌ | ±0.1 |
| D65 | Bradford | 9.6BG 2.8/4.6 | dark greenish blue | ✅ | dark bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 9.6BG 2.8/4.6 | dark greenish blue | ✅ | dark bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 9.6BG 2.8/4.6 | dark greenish blue | ✅ | dark bluish green | ❌ | ±0.1 |
| F7 | Bradford | 9.6BG 2.8/4.6 | dark greenish blue | ✅ | dark bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 9.6BG 2.8/4.6 | dark greenish blue | ✅ | dark bluish green | ❌ | ±0.1 |

#### 175. Expected: very dark greenish blue
Hex: #002E3B - **All configurations matched**

#### 176. Expected: vivid blue
Hex: #00A1C2

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.9B 6.0/8.8 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| C | Bradford | 3.2B 6.0/8.6 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| C | CAT02 | 3.2B 6.0/8.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.8B 6.0/8.3 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.8B 6.0/8.3 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.8B 6.0/8.3 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.8B 6.0/8.3 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.8B 6.0/8.3 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.8B 6.0/8.3 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |

#### 177. Expected: brilliant blue
Hex: #4997D0

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 6.1B 5.9/8.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| D65 | Bradford | 6.1B 5.9/8.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| D65 | CAT02 | 6.1B 5.9/8.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| F7 | XYZScaling | 6.1B 5.9/8.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| F7 | Bradford | 6.1B 5.9/8.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| F7 | CAT02 | 6.1B 5.9/8.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |

#### 178. Expected: strong blue
Hex: #0067A5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.2B 4.1/9.5 | strong greenish blue | ❌ | strong greenish blue | ❌ | ±0.1 |
| C | Bradford | 8.1B 4.1/9.4 | strong blue | ✅ | strong greenish blue | ❌ |  |
| C | CAT02 | 8.1B 4.1/9.3 | strong blue | ✅ | strong greenish blue | ❌ |  |
| D65 | XYZScaling | 6.0B 4.1/8.8 | strong greenish blue | ❌ | strong greenish blue | ❌ |  |
| D65 | Bradford | 6.0B 4.1/8.8 | strong greenish blue | ❌ | strong greenish blue | ❌ |  |
| D65 | CAT02 | 6.0B 4.1/8.8 | strong greenish blue | ❌ | strong greenish blue | ❌ |  |
| F7 | XYZScaling | 6.0B 4.1/8.7 | strong greenish blue | ❌ | strong greenish blue | ❌ |  |
| F7 | Bradford | 6.0B 4.1/8.7 | strong greenish blue | ❌ | strong greenish blue | ❌ |  |
| F7 | CAT02 | 6.0B 4.1/8.7 | strong greenish blue | ❌ | strong greenish blue | ❌ |  |

#### 179. Expected: deep blue
Hex: #00416A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.7B 2.6/6.6 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| C | Bradford | 4.9B 2.6/6.5 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| C | CAT02 | 4.9B 2.6/6.5 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 4.4B 2.6/6.2 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 4.4B 2.6/6.2 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 4.4B 2.6/6.2 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 4.4B 2.6/6.2 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 4.4B 2.6/6.2 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 4.4B 2.6/6.2 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |

#### 180. Expected: very light blue
Hex: #A1CAF1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.1B 7.9/5.2 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 8.1B 7.9/5.2 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 8.1B 7.9/5.2 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 7.9B 7.9/5.1 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 7.9B 7.9/5.1 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 7.9B 7.9/5.1 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |

#### 181. Expected: light blue
Hex: #70A3CC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 5.0B 6.4/6.1 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 5.0B 6.4/6.1 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 5.0B 6.4/6.1 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 5.0B 6.4/6.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 5.0B 6.4/6.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 5.0B 6.4/6.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |

#### 182. Expected: moderate blue
Hex: #436B95 - **All configurations matched**

#### 183. Expected: dark blue
Hex: #00304E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.1B 1.8/5.4 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| C | Bradford | 4.3B 1.8/5.3 | very dark greenish blue | ❌ | very dark greenish blue | ❌ |  |
| C | CAT02 | 4.3B 1.8/5.3 | very dark greenish blue | ❌ | very dark greenish blue | ❌ |  |
| D65 | XYZScaling | 3.7B 1.8/5.1 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 3.7B 1.8/5.1 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 3.7B 1.8/5.1 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 3.7B 1.8/5.0 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 3.7B 1.8/5.0 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 3.7B 1.8/5.0 | very dark greenish blue | ❌ | very dark greenish blue | ❌ | ±0.1 |

#### 184. Expected: very pale blue
Hex: #BCD4E6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 3.7PB 8.3/3.4 | very pale purplish blue | ❌ | very pale blue | ✅ | ±0.1 |
| C | CAT02 | 3.6PB 8.3/3.4 | very pale purplish blue | ❌ | very pale blue | ✅ |  |

#### 185. Expected: pale blue
Hex: #91A3B0 - **All configurations matched**

#### 186. Expected: grayish blue
Hex: #536878 - **All configurations matched**

#### 187. Expected: dark grayish blue
Hex: #36454F - **All configurations matched**

#### 188. Expected: blackish blue
Hex: #202830 - **All configurations matched**

#### 189. Expected: bluish white
Hex: #E9E9ED

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.6P 9.2/0.8 | purplish white | ❌ | purplish white | ❌ |  |
| C | Bradford | 3.8P 9.2/0.9 | purplish white | ❌ | purplish white | ❌ |  |
| C | CAT02 | 3.7P 9.2/0.8 | purplish white | ❌ | purplish white | ❌ |  |
| D65 | XYZScaling | 1.9G 9.2/0.7 | greenish white | ❌ | greenish white | ❌ |  |
| D65 | Bradford | 1.9G 9.2/0.7 | greenish white | ❌ | greenish white | ❌ |  |
| D65 | CAT02 | 1.9G 9.2/0.7 | greenish white | ❌ | greenish white | ❌ |  |
| F7 | XYZScaling | 1.5G 9.2/0.7 | greenish white | ❌ | greenish white | ❌ |  |
| F7 | Bradford | 1.5G 9.2/0.7 | greenish white | ❌ | greenish white | ❌ |  |
| F7 | CAT02 | 1.5G 9.2/0.7 | greenish white | ❌ | greenish white | ❌ |  |

#### 190. Expected: light bluish gray
Hex: #B4BCC0

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 9.8BG 7.5/0.9 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 9.8BG 7.5/0.9 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 9.8BG 7.5/0.9 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 9.4BG 7.5/1.0 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 9.4BG 7.5/1.0 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 9.5BG 7.5/1.0 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |

#### 191. Expected: bluish gray
Hex: #81878B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 9.6BG 5.5/0.7 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 9.6BG 5.5/0.7 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 9.6BG 5.5/0.7 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 9.4BG 5.5/0.7 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 9.4BG 5.5/0.7 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 9.4BG 5.5/0.7 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |

#### 192. Expected: dark bluish gray
Hex: #51585E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.6BG 3.6/0.9 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 7.6BG 3.6/0.9 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 7.6BG 3.6/0.9 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 7.4BG 3.6/0.9 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 7.4BG 3.6/0.9 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 7.4BG 3.6/0.9 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |

#### 193. Expected: bluish black
Hex: #202428

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.8BG 1.4/0.7 | greenish black | ❌ | greenish black | ❌ |  |
| D65 | Bradford | 8.8BG 1.4/0.7 | greenish black | ❌ | greenish black | ❌ |  |
| D65 | CAT02 | 8.8BG 1.4/0.7 | greenish black | ❌ | greenish black | ❌ |  |
| F7 | XYZScaling | 8.6BG 1.4/0.7 | greenish black | ❌ | greenish black | ❌ |  |
| F7 | Bradford | 8.6BG 1.4/0.7 | greenish black | ❌ | greenish black | ❌ |  |
| F7 | CAT02 | 8.6BG 1.4/0.7 | greenish black | ❌ | greenish black | ❌ |  |

#### 194. Expected: vivid purplish blue
Hex: #30267A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.4B 2.1/8.7 | deep greenish blue | ❌ | deep greenish blue | ❌ |  |
| C | Bradford | 9.7B 2.2/8.4 | deep blue | ❌ | deep blue | ❌ |  |
| C | CAT02 | 9.7B 2.2/8.3 | deep blue | ❌ | deep blue | ❌ |  |
| D65 | XYZScaling | 9.5B 2.1/8.0 | deep blue | ❌ | deep blue | ❌ | ±0.1 |
| D65 | Bradford | 9.5B 2.1/8.0 | deep blue | ❌ | deep blue | ❌ | ±0.1 |
| D65 | CAT02 | 9.5B 2.1/8.0 | deep blue | ❌ | deep blue | ❌ | ±0.1 |
| F7 | XYZScaling | 9.6B 2.1/8.0 | deep blue | ❌ | deep blue | ❌ | ±0.1 |
| F7 | Bradford | 9.5B 2.1/8.0 | deep blue | ❌ | deep blue | ❌ | ±0.1 |
| F7 | CAT02 | 9.5B 2.1/8.0 | deep blue | ❌ | deep blue | ❌ | ±0.1 |

#### 195. Expected: brilliant purplish blue
Hex: #6C79B8

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.9PB 5.1/8.5 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| C | Bradford | 6.1PB 5.1/8.5 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| C | CAT02 | 6.1PB 5.1/8.4 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | XYZScaling | 6.1PB 5.1/7.6 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | Bradford | 6.1PB 5.1/7.6 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | CAT02 | 6.1PB 5.1/7.6 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | XYZScaling | 6.1PB 5.1/7.5 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | Bradford | 6.1PB 5.1/7.5 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | CAT02 | 6.1PB 5.1/7.5 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |

#### 196. Expected: strong purplish blue
Hex: #545AA7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.8P 4.0/13.1 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| C | Bradford | 1.5P 4.1/13.6 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| C | CAT02 | 1.4P 4.1/13.4 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| D65 | XYZScaling | 2.5PB 4.0/8.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | Bradford | 2.5PB 4.0/8.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | CAT02 | 2.5PB 4.0/8.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | XYZScaling | 2.6PB 4.0/8.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | Bradford | 2.6PB 4.0/8.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | CAT02 | 2.6PB 4.0/8.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |

#### 197. Expected: deep purplish blue
Hex: #272458

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 9.5B 1.7/5.8 | dark blue | ❌ | dark blue | ❌ |  |
| C | CAT02 | 9.5B 1.7/5.8 | dark blue | ❌ | dark blue | ❌ |  |
| D65 | XYZScaling | 7.6PB 1.7/6.6 | dark purplish blue | ❌ | dark purplish blue | ❌ | ±0.1 |
| D65 | Bradford | 7.6PB 1.7/6.6 | dark purplish blue | ❌ | dark purplish blue | ❌ | ±0.1 |
| D65 | CAT02 | 7.6PB 1.7/6.6 | dark purplish blue | ❌ | dark purplish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 9.0B 1.7/5.4 | dark blue | ❌ | very dark greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 7.6PB 1.7/6.5 | dark purplish blue | ❌ | dark purplish blue | ❌ | ±0.1 |
| F7 | CAT02 | 7.6PB 1.7/6.5 | dark purplish blue | ❌ | dark purplish blue | ❌ | ±0.1 |

#### 198. Expected: very light purplish blue
Hex: #B3BCE2

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.6PB 7.6/5.6 | very light violet | ❌ | very light violet | ❌ |  |
| C | Bradford | 10.0PB 7.6/5.6 | very light violet | ❌ | very light violet | ❌ |  |
| C | CAT02 | 9.9PB 7.6/5.6 | very light violet | ❌ | very light violet | ❌ |  |
| D65 | XYZScaling | 7.6PB 7.6/4.3 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |
| D65 | Bradford | 7.6PB 7.6/4.3 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |
| D65 | CAT02 | 7.6PB 7.6/4.3 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |
| F7 | XYZScaling | 7.6PB 7.6/4.3 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |
| F7 | Bradford | 7.6PB 7.6/4.3 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |
| F7 | CAT02 | 7.6PB 7.6/4.3 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |

#### 199. Expected: light purplish blue
Hex: #8791BF - **All configurations matched**

#### 200. Expected: moderate purplish blue
Hex: #4E5180

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.8P 3.6/7.2 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |
| C | Bradford | 2.3PB 3.6/5.5 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| C | CAT02 | 2.4PB 3.6/5.5 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | XYZScaling | 2.4PB 3.6/4.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | Bradford | 2.4PB 3.6/4.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | CAT02 | 2.4PB 3.6/4.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 2.4PB 3.6/4.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | Bradford | 2.4PB 3.6/4.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | CAT02 | 2.4PB 3.6/4.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |

#### 201. Expected: dark purplish blue
Hex: #252440

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 9.2B 1.5/3.3 | dark blue | ❌ | dark blue | ❌ | ±0.1 |
| C | CAT02 | 9.1B 1.5/3.3 | dark blue | ❌ | dark blue | ❌ | ±0.1 |

#### 202. Expected: very pale purplish blue
Hex: #C0C8E1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.6PB 8.0/4.1 | very pale violet | ❌ | very pale violet | ❌ | ±0.1 |
| C | Bradford | 9.8PB 8.0/4.1 | very pale violet | ❌ | very pale violet | ❌ | ±0.1 |
| C | CAT02 | 9.8PB 8.0/4.0 | very pale violet | ❌ | very pale violet | ❌ | ±0.1 |
| D65 | XYZScaling | 5.4PB 8.0/2.7 | very pale blue | ❌ | very pale blue | ❌ | ±0.1 |
| D65 | Bradford | 5.4PB 8.0/2.7 | very pale blue | ❌ | very pale blue | ❌ | ±0.1 |
| D65 | CAT02 | 5.4PB 8.0/2.7 | very pale blue | ❌ | very pale blue | ❌ | ±0.1 |
| F7 | XYZScaling | 5.3PB 8.0/2.7 | very pale blue | ❌ | very pale blue | ❌ | ±0.1 |
| F7 | Bradford | 5.2PB 8.0/2.7 | very pale blue | ❌ | very pale blue | ❌ | ±0.1 |
| F7 | CAT02 | 5.2PB 8.0/2.7 | very pale blue | ❌ | very pale blue | ❌ | ±0.1 |

#### 203. Expected: pale purplish blue
Hex: #8C92AC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.0PB 6.0/4.1 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |
| C | Bradford | 9.3PB 6.0/4.1 | pale violet | ❌ | pale violet | ❌ | ±0.1 |
| C | CAT02 | 9.3PB 6.0/4.1 | pale violet | ❌ | pale violet | ❌ | ±0.1 |
| D65 | XYZScaling | 6.6PB 6.0/3.0 | pale blue | ❌ | pale blue | ❌ | ±0.1 |
| D65 | Bradford | 6.6PB 6.0/3.0 | pale blue | ❌ | pale blue | ❌ | ±0.1 |
| D65 | CAT02 | 6.6PB 6.0/3.0 | pale blue | ❌ | pale blue | ❌ | ±0.1 |
| F7 | XYZScaling | 6.5PB 6.0/3.0 | pale blue | ❌ | pale blue | ❌ | ±0.1 |
| F7 | Bradford | 6.5PB 6.0/3.0 | pale blue | ❌ | pale blue | ❌ | ±0.1 |
| F7 | CAT02 | 6.5PB 6.0/3.0 | pale blue | ❌ | pale blue | ❌ | ±0.1 |

#### 204. Expected: grayish purplish blue
Hex: #4C516D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.8PB 3.5/3.4 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| C | Bradford | 0.9PB 3.5/3.4 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| C | CAT02 | 1.0PB 3.5/3.4 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.4PB 3.5/2.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.4PB 3.5/2.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.4PB 3.5/2.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.5PB 3.5/2.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.5PB 3.5/2.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.5PB 3.5/2.9 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |

#### 205. Expected: vivid violet
Hex: #9065CA

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.3PB 5.0/11.4 | strong purplish blue | ❌ | strong purplish blue | ❌ | ±0.1 |
| C | Bradford | 8.5PB 5.1/11.4 | strong purplish blue | ❌ | strong purplish blue | ❌ | ±0.1 |
| C | CAT02 | 8.5PB 5.1/11.3 | strong purplish blue | ❌ | strong purplish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 8.9PB 5.0/10.6 | brilliant violet | ❌ | brilliant purplish blue | ❌ | ±0.1 |
| D65 | Bradford | 8.9PB 5.0/10.6 | brilliant violet | ❌ | brilliant purplish blue | ❌ | ±0.1 |
| D65 | CAT02 | 8.9PB 5.0/10.6 | brilliant violet | ❌ | brilliant purplish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 9.0PB 5.0/10.6 | brilliant violet | ❌ | brilliant purplish blue | ❌ | ±0.1 |
| F7 | Bradford | 9.0PB 5.0/10.6 | brilliant violet | ❌ | brilliant purplish blue | ❌ | ±0.1 |
| F7 | CAT02 | 8.9PB 5.0/10.6 | brilliant violet | ❌ | brilliant purplish blue | ❌ | ±0.1 |

#### 206. Expected: brilliant violet
Hex: #7E73B8

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8PB 5.1/8.4 | light purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| C | Bradford | 6.8PB 5.1/8.3 | light purplish blue | ❌ | moderate blue | ❌ |  |
| C | CAT02 | 6.9PB 5.1/8.3 | light purplish blue | ❌ | moderate blue | ❌ |  |
| D65 | XYZScaling | 7.4PB 5.1/7.5 | light purplish blue | ❌ | light purplish blue | ❌ | ±0.1 |
| D65 | Bradford | 7.4PB 5.1/7.5 | light purplish blue | ❌ | light purplish blue | ❌ | ±0.1 |
| D65 | CAT02 | 7.4PB 5.1/7.5 | light purplish blue | ❌ | light purplish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 7.4PB 5.1/7.5 | light purplish blue | ❌ | light purplish blue | ❌ | ±0.1 |
| F7 | Bradford | 7.4PB 5.1/7.5 | light purplish blue | ❌ | light purplish blue | ❌ | ±0.1 |
| F7 | CAT02 | 7.4PB 5.1/7.5 | light purplish blue | ❌ | light purplish blue | ❌ | ±0.1 |

#### 207. Expected: strong violet
Hex: #604E97

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.0PB 3.7/7.7 | moderate blue | ❌ | moderate blue | ❌ |  |
| C | Bradford | 4.4PB 3.8/7.7 | moderate blue | ❌ | moderate blue | ❌ |  |
| C | CAT02 | 4.4PB 3.8/7.7 | moderate blue | ❌ | moderate blue | ❌ |  |
| D65 | XYZScaling | 4.2PB 3.7/7.0 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | Bradford | 4.2PB 3.7/7.0 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | CAT02 | 4.2PB 3.7/7.0 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | XYZScaling | 4.2PB 3.7/7.0 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | Bradford | 4.2PB 3.7/7.0 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | CAT02 | 4.2PB 3.7/7.0 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |

#### 208. Expected: deep violet
Hex: #32174D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 3.2P 1.4/7.7 | very deep purple | ❌ | very deep purple | ❌ | ±0.1 |
| D65 | Bradford | 3.2P 1.4/7.7 | very deep purple | ❌ | very deep purple | ❌ | ±0.1 |
| D65 | CAT02 | 3.2P 1.4/7.7 | very deep purple | ❌ | very deep purple | ❌ | ±0.1 |
| F7 | XYZScaling | 3.3P 1.4/7.7 | very deep purple | ❌ | very deep purple | ❌ | ±0.1 |
| F7 | Bradford | 3.3P 1.4/7.7 | very deep purple | ❌ | very deep purple | ❌ | ±0.1 |
| F7 | CAT02 | 3.3P 1.4/7.7 | very deep purple | ❌ | very deep purple | ❌ | ±0.1 |

#### 209. Expected: very light violet
Hex: #DCD0FF

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.1P 8.5/6.5 | very light purple | ❌ | very light purple | ❌ | ±0.1 |
| C | Bradford | 4.3P 8.6/6.5 | very light purple | ❌ | very light purple | ❌ | ±0.1 |
| C | CAT02 | 4.2P 8.6/6.5 | very light purple | ❌ | very light purple | ❌ | ±0.1 |
| D65 | XYZScaling | 3.3P 8.5/5.0 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| D65 | Bradford | 3.3P 8.5/5.0 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| D65 | CAT02 | 3.3P 8.5/5.0 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | XYZScaling | 3.3P 8.5/4.9 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | Bradford | 3.3P 8.5/4.9 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | CAT02 | 3.3P 8.5/4.9 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 210. Expected: light violet
Hex: #8C82B6 - **All configurations matched**

#### 211. Expected: moderate violet
Hex: #604E81

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.1PB 3.6/5.6 | moderate purplish blue | ❌ | moderate purplish blue | ❌ |  |
| C | Bradford | 7.3PB 3.6/5.6 | moderate purplish blue | ❌ | moderate purplish blue | ❌ |  |
| C | CAT02 | 7.3PB 3.7/5.6 | moderate purplish blue | ❌ | moderate purplish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 7.1PB 3.6/4.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| D65 | Bradford | 7.1PB 3.6/4.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| D65 | CAT02 | 7.1PB 3.6/4.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 7.2PB 3.6/4.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| F7 | Bradford | 7.2PB 3.6/4.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| F7 | CAT02 | 7.2PB 3.6/4.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ |  |

#### 212. Expected: dark violet
Hex: #2F2140 - **All configurations matched**

#### 213. Expected: very pale violet
Hex: #C4C3DD

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 9.8PB 7.9/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| D65 | Bradford | 9.8PB 7.9/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| D65 | CAT02 | 9.8PB 7.9/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | XYZScaling | 9.8PB 7.9/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | Bradford | 9.8PB 7.9/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | CAT02 | 9.8PB 7.9/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 214. Expected: pale violet
Hex: #9690AB

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 0.9P 6.0/2.8 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| D65 | Bradford | 0.9P 6.0/2.8 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| D65 | CAT02 | 0.9P 6.0/2.8 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| F7 | XYZScaling | 0.9P 6.0/2.8 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| F7 | Bradford | 0.9P 6.0/2.8 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| F7 | CAT02 | 0.9P 6.0/2.8 | pale purple | ❌ | pale purple | ❌ | ±0.1 |

#### 215. Expected: grayish violet
Hex: #554C69

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.3PB 3.4/3.1 | grayish purplish blue | ❌ | grayish purplish blue | ❌ |  |
| C | Bradford | 6.6PB 3.4/3.1 | grayish purplish blue | ❌ | grayish purplish blue | ❌ |  |
| C | CAT02 | 6.5PB 3.4/3.1 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 5.5PB 3.4/2.5 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | Bradford | 5.5PB 3.4/2.5 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | CAT02 | 5.5PB 3.4/2.5 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 5.6PB 3.4/2.5 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | Bradford | 5.5PB 3.4/2.5 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | CAT02 | 5.5PB 3.4/2.5 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |

#### 216. Expected: vivid purple
Hex: #9A4EAE

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 6.4P 4.5/12.7 | strong purple | ❌ | strong purple | ❌ | ±0.1 |
| D65 | Bradford | 6.4P 4.5/12.7 | strong purple | ❌ | strong purple | ❌ | ±0.1 |
| D65 | CAT02 | 6.4P 4.5/12.7 | strong purple | ❌ | strong purple | ❌ | ±0.1 |
| F7 | XYZScaling | 6.4P 4.5/12.6 | strong purple | ❌ | strong purple | ❌ | ±0.1 |
| F7 | Bradford | 6.4P 4.5/12.6 | strong purple | ❌ | strong purple | ❌ | ±0.1 |
| F7 | CAT02 | 6.4P 4.5/12.6 | strong purple | ❌ | strong purple | ❌ | ±0.1 |

#### 217. Expected: brilliant purple
Hex: #D399E6 - **All configurations matched**

#### 218. Expected: strong purple
Hex: #875692

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.5P 4.3/9.0 | moderate purple | ❌ | moderate purple | ❌ | ±0.1 |
| C | Bradford | 6.4P 4.3/8.9 | moderate purple | ❌ | moderate purple | ❌ |  |
| C | CAT02 | 6.4P 4.3/8.8 | moderate purple | ❌ | moderate purple | ❌ |  |
| D65 | XYZScaling | 6.9P 4.3/7.9 | moderate purple | ❌ | moderate purple | ❌ |  |
| D65 | Bradford | 6.9P 4.3/7.9 | moderate purple | ❌ | moderate purple | ❌ |  |
| D65 | CAT02 | 6.9P 4.3/7.9 | moderate purple | ❌ | moderate purple | ❌ |  |
| F7 | XYZScaling | 6.9P 4.3/7.9 | moderate purple | ❌ | moderate purple | ❌ |  |
| F7 | Bradford | 6.9P 4.3/7.9 | moderate purple | ❌ | moderate purple | ❌ |  |
| F7 | CAT02 | 6.9P 4.3/7.9 | moderate purple | ❌ | moderate purple | ❌ |  |

#### 219. Expected: deep purple
Hex: #602F6B - **All configurations matched**

#### 220. Expected: very deep purple
Hex: #401A4C - **All configurations matched**

#### 221. Expected: very light purple
Hex: #D5BADB

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 6.8P 7.8/3.8 | very pale purple | ❌ | very pale purple | ❌ |  |
| D65 | Bradford | 6.8P 7.8/3.8 | very pale purple | ❌ | very pale purple | ❌ |  |
| D65 | CAT02 | 6.8P 7.8/3.8 | very pale purple | ❌ | very pale purple | ❌ |  |
| F7 | XYZScaling | 6.9P 7.8/3.7 | very pale purple | ❌ | very pale purple | ❌ |  |
| F7 | Bradford | 6.9P 7.8/3.7 | very pale purple | ❌ | very pale purple | ❌ |  |
| F7 | CAT02 | 6.9P 7.8/3.7 | very pale purple | ❌ | very pale purple | ❌ |  |

#### 222. Expected: light purple
Hex: #B695C0 - **All configurations matched**

#### 223. Expected: moderate purple
Hex: #86608E - **All configurations matched**

#### 224. Expected: dark purple
Hex: #563C5C - **All configurations matched**

#### 225. Expected: very dark purple
Hex: #301934

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.5P 1.3/4.0 | very dark reddish purple | ❌ | very dark purple | ✅ | ±0.1 |
| C | Bradford | 8.5P 1.3/3.9 | very dark reddish purple | ❌ | very dark purple | ✅ | ±0.1 |
| C | CAT02 | 8.4P 1.3/3.9 | very dark reddish purple | ❌ | very dark purple | ✅ | ±0.1 |
| D65 | XYZScaling | 9.1P 1.3/3.5 | very dark reddish purple | ❌ | very dark reddish purple | ❌ | ±0.1 |
| D65 | Bradford | 9.1P 1.3/3.5 | very dark reddish purple | ❌ | very dark reddish purple | ❌ | ±0.1 |
| D65 | CAT02 | 9.1P 1.3/3.5 | very dark reddish purple | ❌ | very dark reddish purple | ❌ | ±0.1 |
| F7 | XYZScaling | 9.1P 1.3/3.5 | very dark reddish purple | ❌ | very dark reddish purple | ❌ | ±0.1 |
| F7 | Bradford | 9.1P 1.3/3.5 | very dark reddish purple | ❌ | very dark reddish purple | ❌ | ±0.1 |
| F7 | CAT02 | 9.1P 1.3/3.5 | very dark reddish purple | ❌ | very dark reddish purple | ❌ | ±0.1 |

#### 226. Expected: very pale purple
Hex: #D6CADD - **All configurations matched**

#### 227. Expected: pale purple
Hex: #AA98A9

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.7P 6.4/3.1 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | Bradford | 7.7P 6.4/3.1 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | CAT02 | 7.7P 6.4/3.0 | N/A | ❌ | N/A | ❌ | ±0.1 |

#### 228. Expected: grayish purple
Hex: #796878 - **All configurations matched**

#### 229. Expected: dark grayish purple
Hex: #50404D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.6RP 2.9/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| D65 | Bradford | 1.6RP 2.9/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| D65 | CAT02 | 1.6RP 2.9/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 1.7RP 2.9/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| F7 | Bradford | 1.7RP 2.9/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| F7 | CAT02 | 1.7RP 2.9/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |

#### 230. Expected: blackish purple
Hex: #291E29 - **All configurations matched**

#### 231. Expected: purplish white
Hex: #E8E3E5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.7R 9.0/0.5 | white | ❌ | white | ❌ | ±0.1 |
| D65 | XYZScaling | 2.2G 9.0/1.0 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| D65 | Bradford | 2.2G 9.0/1.0 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| D65 | CAT02 | 2.2G 9.0/1.0 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| F7 | XYZScaling | 2.4G 9.0/1.0 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| F7 | Bradford | 2.4G 9.0/1.0 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| F7 | CAT02 | 2.3G 9.0/1.0 | greenish white | ❌ | greenish white | ❌ | ±0.1 |

#### 232. Expected: light purplish gray
Hex: #BFB9BD

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.6GY 7.5/0.5 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 8.6GY 7.5/0.5 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 8.6GY 7.5/0.5 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 9.5GY 7.5/0.6 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 9.6GY 7.5/0.6 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 9.9GY 7.5/0.6 | light greenish gray | ❌ | light greenish gray | ❌ | ±0.1 |

#### 233. Expected: purplish gray
Hex: #8B8589

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 3.0GY 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| D65 | Bradford | 3.0GY 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| D65 | CAT02 | 3.0GY 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| F7 | XYZScaling | 3.2GY 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| F7 | Bradford | 3.2GY 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| F7 | CAT02 | 3.3GY 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |

#### 234. Expected: dark purplish gray
Hex: #5D555B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.1RP 3.6/0.4 | dark gray | ❌ | dark gray | ❌ | ±0.1 |
| D65 | Bradford | 7.1RP 3.6/0.4 | dark gray | ❌ | dark gray | ❌ | ±0.1 |
| D65 | CAT02 | 7.1RP 3.6/0.4 | dark gray | ❌ | dark gray | ❌ | ±0.1 |
| F7 | XYZScaling | 8.0RP 3.6/0.4 | dark gray | ❌ | dark gray | ❌ | ±0.1 |
| F7 | Bradford | 8.0RP 3.6/0.4 | dark gray | ❌ | dark gray | ❌ | ±0.1 |
| F7 | CAT02 | 8.0RP 3.6/0.4 | dark gray | ❌ | dark gray | ❌ | ±0.1 |

#### 235. Expected: purplish black
Hex: #242124

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.1RP 1.3/0.4 | black | ❌ | black | ❌ | ±0.1 |
| C | Bradford | 0.0RP 1.3/0.4 | black | ❌ | black | ❌ | ±0.1 |
| C | CAT02 | 0.0RP 1.3/0.4 | black | ❌ | black | ❌ | ±0.1 |
| D65 | XYZScaling | 9.6RP 1.3/0.1 | black | ❌ | black | ❌ |  |
| D65 | Bradford | 9.6RP 1.3/0.1 | black | ❌ | black | ❌ |  |
| D65 | CAT02 | 9.6RP 1.3/0.1 | black | ❌ | black | ❌ |  |
| F7 | XYZScaling | 0.6R 1.3/0.1 | black | ❌ | black | ❌ |  |
| F7 | Bradford | 0.6R 1.3/0.1 | black | ❌ | black | ❌ |  |
| F7 | CAT02 | 0.6R 1.3/0.1 | black | ❌ | black | ❌ |  |

#### 236. Expected: vivid reddish purple
Hex: #870074 - **All configurations matched**

#### 237. Expected: strong reddish purple
Hex: #9E4F88

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.4RP 4.4/9.0 | moderate reddish purple | ❌ | moderate reddish purple | ❌ | ±0.1 |
| D65 | Bradford | 1.4RP 4.4/9.0 | moderate reddish purple | ❌ | moderate reddish purple | ❌ | ±0.1 |
| D65 | CAT02 | 1.4RP 4.4/9.0 | moderate reddish purple | ❌ | moderate reddish purple | ❌ | ±0.1 |
| F7 | XYZScaling | 1.4RP 4.4/9.0 | moderate reddish purple | ❌ | moderate reddish purple | ❌ | ±0.1 |
| F7 | Bradford | 1.4RP 4.4/9.0 | moderate reddish purple | ❌ | moderate reddish purple | ❌ | ±0.1 |
| F7 | CAT02 | 1.4RP 4.4/9.0 | moderate reddish purple | ❌ | moderate reddish purple | ❌ | ±0.1 |

#### 238. Expected: deep reddish purple
Hex: #702963 - **All configurations matched**

#### 239. Expected: very deep reddish purple
Hex: #54194E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.9P 2.0/8.3 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| C | Bradford | 9.8P 2.0/8.1 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| C | CAT02 | 9.8P 2.0/8.1 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| D65 | XYZScaling | 0.4RP 2.0/7.7 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| D65 | Bradford | 0.4RP 2.0/7.7 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| D65 | CAT02 | 0.4RP 2.0/7.7 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| F7 | XYZScaling | 0.4RP 2.0/7.7 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| F7 | Bradford | 0.4RP 2.0/7.7 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |
| F7 | CAT02 | 0.4RP 2.0/7.7 | deep reddish purple | ❌ | deep reddish purple | ❌ | ±0.1 |

#### 240. Expected: light reddish purple
Hex: #B784A7 - **All configurations matched**

#### 241. Expected: moderate reddish purple
Hex: #915C83 - **All configurations matched**

#### 242. Expected: dark reddish purple
Hex: #5D3954 - **All configurations matched**

#### 243. Expected: very dark reddish purple
Hex: #341731 - **All configurations matched**

#### 244. Expected: pale reddish purple
Hex: #AA8A9E - **All configurations matched**

#### 245. Expected: grayish reddish purple
Hex: #836479 - **All configurations matched**

#### 246. Expected: brilliant purplish pink
Hex: #FFC8D6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.8R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| C | Bradford | 4.8R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| C | CAT02 | 4.8R 8.5/3.5 | light pink | ❌ | light pink | ❌ | ±0.1 |
| D65 | XYZScaling | 5.4R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| D65 | Bradford | 5.4R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| D65 | CAT02 | 5.4R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| F7 | XYZScaling | 5.4R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| F7 | Bradford | 5.4R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |
| F7 | CAT02 | 5.4R 8.5/3.6 | light pink | ❌ | light pink | ❌ | ±0.1 |

#### 247. Expected: strong purplish pink
Hex: #E68FAC - **All configurations matched**

#### 248. Expected: deep purplish pink
Hex: #DE6FA1 - **All configurations matched**

#### 249. Expected: light purplish pink
Hex: #EFBBCC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 5.0R 8.0/3.4 | light pink | ❌ | light pink | ❌ | ±0.1 |
| D65 | Bradford | 5.0R 8.0/3.4 | light pink | ❌ | light pink | ❌ | ±0.1 |
| D65 | CAT02 | 5.0R 8.0/3.4 | light pink | ❌ | light pink | ❌ | ±0.1 |
| F7 | XYZScaling | 6.7RP 8.0/5.0 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |
| F7 | Bradford | 6.7RP 8.0/5.0 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |

#### 250. Expected: moderate purplish pink
Hex: #D597AE - **All configurations matched**

#### 251. Expected: dark purplish pink
Hex: #C17E91 - **All configurations matched**

#### 252. Expected: pale purplish pink
Hex: #E8CCD7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 3.9R 8.4/2.2 | pale pink | ❌ | pale pink | ❌ | ±0.1 |
| C | CAT02 | 3.9R 8.4/2.2 | pale pink | ❌ | pale pink | ❌ | ±0.1 |
| D65 | XYZScaling | 6.1R 8.4/2.0 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 6.1R 8.4/2.0 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 6.1R 8.4/2.0 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 6.3R 8.4/2.0 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 6.3R 8.4/2.0 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 6.3R 8.4/2.0 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |

#### 253. Expected: grayish purplish pink
Hex: #C3A6B1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 5.1R 7.0/1.9 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |
| D65 | Bradford | 5.1R 7.0/1.9 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |
| D65 | CAT02 | 5.1R 7.0/1.9 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 5.2R 7.0/1.9 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |
| F7 | Bradford | 5.2R 7.0/1.9 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |
| F7 | CAT02 | 5.2R 7.0/1.9 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |

#### 254. Expected: vivid purplish red
Hex: #CE4676 - **All configurations matched**

#### 255. Expected: strong purplish red
Hex: #B3446C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.8RP 4.4/13.3 | vivid purplish red | ❌ | vivid purplish red | ❌ | ±0.1 |

#### 256. Expected: deep purplish red
Hex: #78184A - **All configurations matched**

#### 257. Expected: very deep purplish red
Hex: #54133B - **All configurations matched**

#### 258. Expected: moderate purplish red
Hex: #A8516E - **All configurations matched**

#### 259. Expected: dark purplish red
Hex: #673147 - **All configurations matched**

#### 260. Expected: very dark purplish red
Hex: #38152C - **All configurations matched**

#### 261. Expected: light grayish purplish red
Hex: #AF868E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 3.1R 5.9/3.4 | light grayish red | ❌ | light grayish red | ❌ |  |
| D65 | Bradford | 3.1R 5.9/3.4 | light grayish red | ❌ | light grayish red | ❌ |  |
| D65 | CAT02 | 3.1R 5.9/3.4 | light grayish red | ❌ | light grayish red | ❌ |  |
| F7 | XYZScaling | 3.3R 5.9/3.4 | light grayish red | ❌ | light grayish red | ❌ |  |
| F7 | Bradford | 3.3R 5.9/3.4 | light grayish red | ❌ | light grayish red | ❌ |  |
| F7 | CAT02 | 3.3R 5.9/3.4 | light grayish red | ❌ | light grayish red | ❌ |  |

#### 262. Expected: grayish purplish red
Hex: #915F6D - **All configurations matched**

#### 263. Expected: white
Hex: #F2F3F4

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 0.7G 9.6/0.9 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| D65 | Bradford | 0.7G 9.6/0.9 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| D65 | CAT02 | 0.7G 9.6/0.9 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| F7 | XYZScaling | 0.6G 9.6/0.9 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| F7 | Bradford | 0.6G 9.6/0.9 | greenish white | ❌ | greenish white | ❌ | ±0.1 |
| F7 | CAT02 | 0.6G 9.6/0.9 | greenish white | ❌ | greenish white | ❌ | ±0.1 |

#### 264. Expected: light gray
Hex: #B9B8B5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 0.5G 7.4/1.2 | pale green | ❌ | pale green | ❌ | ±0.1 |
| D65 | Bradford | 0.5G 7.4/1.2 | pale green | ❌ | pale green | ❌ | ±0.1 |
| D65 | CAT02 | 0.5G 7.4/1.2 | pale green | ❌ | pale green | ❌ | ±0.1 |
| F7 | XYZScaling | 0.3G 7.4/1.2 | pale green | ❌ | pale green | ❌ | ±0.1 |
| F7 | Bradford | 0.3G 7.4/1.2 | pale green | ❌ | pale green | ❌ | ±0.1 |
| F7 | CAT02 | 0.4G 7.4/1.2 | pale green | ❌ | pale green | ❌ | ±0.1 |

#### 265. Expected: medium gray
Hex: #848482

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 0.0G 5.4/1.0 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 0.0G 5.4/1.0 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 0.0G 5.4/1.0 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 9.9GY 5.4/1.0 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 9.9GY 5.4/1.0 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 9.9GY 5.4/1.0 | greenish gray | ❌ | greenish gray | ❌ | ±0.1 |

#### 266. Expected: dark gray
Hex: #555555

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.0N 3.6/0.0 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | Bradford | 0.0N 3.6/0.0 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | CAT02 | 0.0N 3.6/0.0 | N/A | ❌ | N/A | ❌ | ±0.1 |
| D65 | XYZScaling | 9.8GY 3.6/0.6 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| D65 | Bradford | 9.8GY 3.6/0.6 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| D65 | CAT02 | 9.8GY 3.6/0.6 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 9.8GY 3.6/0.7 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| F7 | Bradford | 9.8GY 3.6/0.7 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |
| F7 | CAT02 | 9.8GY 3.6/0.7 | dark greenish gray | ❌ | dark greenish gray | ❌ | ±0.1 |

#### 267. Expected: black
Hex: #222222

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.0N 1.3/0.0 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | Bradford | 0.0N 1.3/0.0 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | CAT02 | 0.0N 1.3/0.0 | N/A | ❌ | N/A | ❌ | ±0.1 |

## Paul Centore Dataset (260 colors)

### Summary Statistics

| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy |
|------------|------------|-------------------|-------------------|
| C | XYZScaling | 48.5% | 52.3% |
| C | Bradford | 50.0% | 53.1% |
| C | CAT02 | 50.0% | 53.5% |
| D65 | XYZScaling | 58.5% | 61.9% |
| D65 | Bradford | 58.5% | 61.9% |
| D65 | CAT02 | 58.5% | 61.9% |
| F7 | XYZScaling | 59.2% | 63.1% |
| F7 | Bradford | 59.2% | 62.7% |
| F7 | CAT02 | 59.2% | 62.7% |

### Detailed Mismatches

#### 1. Expected: vivid pink
Hex: #FD7992

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.0RP 6.6/15.9 | strong purplish pink | ❌ | strong purplish pink | ❌ |  |
| C | Bradford | 6.2RP 6.6/15.3 | strong purplish pink | ❌ | strong purplish pink | ❌ |  |
| C | CAT02 | 6.2RP 6.6/15.2 | strong purplish pink | ❌ | strong purplish pink | ❌ |  |
| D65 | XYZScaling | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |

#### 2. Expected: strong pink
Hex: #F48FA0

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.6RP 7.0/12.0 | strong purplish pink | ❌ | strong purplish pink | ❌ | ±0.1 |
| C | Bradford | 4.9R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| C | CAT02 | 4.9R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| F7 | XYZScaling | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| F7 | Bradford | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |
| F7 | CAT02 | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | strong yellowish pink | ❌ | ±0.1 |

#### 3. Expected: deep pink
Hex: #E66980

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.6R 5.9/9.3 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| C | Bradford | 5.6R 5.9/9.1 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| C | CAT02 | 5.6R 5.9/9.0 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| D65 | XYZScaling | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| D65 | Bradford | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| D65 | CAT02 | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| F7 | XYZScaling | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| F7 | Bradford | 5.7R 5.9/9.3 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |
| F7 | CAT02 | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ | ±0.1 |

#### 4. Expected: light pink
Hex: #F8C3CE

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.2RP 8.3/6.0 | light purplish pink | ❌ | light purplish pink | ❌ | ±0.1 |

#### 5. Expected: moderate pink
Hex: #E2A3AE - **All configurations matched**

#### 6. Expected: dark pink
Hex: #C5808A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 6.7RP 6.0/8.0 | dark purplish pink | ❌ | dark purplish pink | ❌ | ±0.1 |
| C | CAT02 | 6.7RP 6.0/7.9 | dark purplish pink | ❌ | dark purplish pink | ❌ | ±0.1 |

#### 7. Expected: pale pink
Hex: #EFD1DC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 1.7RP 8.6/3.6 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |
| C | CAT02 | 1.7RP 8.6/3.6 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 6.2R 8.6/2.1 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| D65 | Bradford | 6.2R 8.6/2.1 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| D65 | CAT02 | 6.2R 8.6/2.1 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |

#### 8. Expected: grayish pink
Hex: #CBADB7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.3RP 7.3/3.7 | grayish purplish pink | ❌ | grayish purplish pink | ❌ |  |
| C | Bradford | 2.3RP 7.3/3.6 | grayish purplish pink | ❌ | grayish purplish pink | ❌ |  |
| C | CAT02 | 2.3RP 7.3/3.6 | grayish purplish pink | ❌ | grayish purplish pink | ❌ |  |

#### 9. Expected: pinkish white
Hex: #EFDDE5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.0RP 9.0/2.5 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |
| C | Bradford | 1.0RP 9.0/2.4 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |
| C | CAT02 | 1.0RP 9.0/2.4 | pale purplish pink | ❌ | pale purplish pink | ❌ | ±0.1 |

#### 10. Expected: pinkish gray
Hex: #C7B6BD

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.5RP 7.5/2.3 | grayish purplish pink | ❌ | grayish purplish pink | ❌ | ±0.1 |
| C | Bradford | 1.5RP 7.5/2.3 | grayish purplish pink | ❌ | grayish purplish pink | ❌ | ±0.1 |
| C | CAT02 | 1.5RP 7.5/2.3 | grayish purplish pink | ❌ | grayish purplish pink | ❌ | ±0.1 |

#### 11. Expected: vivid red
Hex: #D51C3C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 7.1R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| C | CAT02 | 7.1R 4.5/13.9 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| D65 | XYZScaling | 7.3R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| D65 | Bradford | 7.3R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| D65 | CAT02 | 7.3R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| F7 | XYZScaling | 7.3R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| F7 | Bradford | 7.3R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |
| F7 | CAT02 | 7.3R 4.5/14.0 | vivid reddish orange | ❌ | vivid reddish orange | ❌ | ±0.1 |

#### 12. Expected: strong red
Hex: #BF344B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.3R 4.3/10.9 | dark reddish orange | ❌ | moderate red | ❌ |  |
| C | Bradford | 6.4R 4.4/10.6 | dark reddish orange | ❌ | moderate red | ❌ | ±0.1 |
| C | CAT02 | 6.4R 4.4/10.6 | dark reddish orange | ❌ | moderate red | ❌ | ±0.1 |
| D65 | XYZScaling | 6.7R 4.3/10.7 | dark reddish orange | ❌ | moderate red | ❌ |  |
| D65 | Bradford | 6.7R 4.3/10.7 | dark reddish orange | ❌ | moderate red | ❌ |  |
| D65 | CAT02 | 6.7R 4.3/10.7 | dark reddish orange | ❌ | moderate red | ❌ |  |
| F7 | XYZScaling | 6.7R 4.3/10.7 | dark reddish orange | ❌ | moderate red | ❌ |  |
| F7 | Bradford | 6.7R 4.3/10.7 | dark reddish orange | ❌ | moderate red | ❌ |  |
| F7 | CAT02 | 6.7R 4.3/10.7 | dark reddish orange | ❌ | moderate red | ❌ |  |

#### 13. Expected: deep red
Hex: #87122D - **All configurations matched**

#### 14. Expected: very deep red
Hex: #5C0625 - **All configurations matched**

#### 15. Expected: moderate red
Hex: #B14955

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.1R 4.4/8.2 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| C | Bradford | 6.2R 4.5/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| C | CAT02 | 6.2R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| D65 | XYZScaling | 6.6R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| D65 | Bradford | 6.6R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| D65 | CAT02 | 6.6R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| F7 | XYZScaling | 6.7R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| F7 | Bradford | 6.7R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |
| F7 | CAT02 | 6.7R 4.4/8.0 | dark reddish orange | ❌ | moderate red | ✅ | ±0.1 |

#### 16. Expected: dark red
Hex: #742434 - **All configurations matched**

#### 17. Expected: very dark red
Hex: #481127 - **All configurations matched**

#### 18. Expected: light grayish red
Hex: #B4888D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 6.9RP 6.0/5.0 | light grayish purplish red | ❌ | light grayish purplish red | ❌ | ±0.1 |
| C | CAT02 | 6.9RP 6.0/4.9 | light grayish purplish red | ❌ | light grayish purplish red | ❌ | ±0.1 |

#### 19. Expected: grayish red
Hex: #985D62 - **All configurations matched**

#### 20. Expected: dark grayish red
Hex: #53383E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.6RP 2.6/2.7 | dark grayish purple | ❌ | dark grayish purple | ❌ |  |
| C | Bradford | 8.8RP 2.7/2.5 | dark grayish purple | ❌ | dark grayish purple | ❌ | ±0.1 |
| C | CAT02 | 8.8RP 2.7/2.5 | dark grayish purple | ❌ | dark grayish purple | ❌ | ±0.1 |

#### 21. Expected: blackish red
Hex: #332127

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.7R 1.5/1.6 | blackish purple | ❌ | blackish purple | ❌ | ±0.1 |
| C | Bradford | 0.8R 1.5/1.6 | blackish purple | ❌ | blackish purple | ❌ | ±0.1 |
| C | CAT02 | 0.8R 1.5/1.6 | blackish purple | ❌ | blackish purple | ❌ | ±0.1 |

#### 22. Expected: reddish gray
Hex: #928186

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.0RP 5.5/2.1 | grayish purple | ❌ | grayish purple | ❌ | ±0.1 |
| C | Bradford | 3.0RP 5.5/2.0 | grayish purple | ❌ | grayish purple | ❌ | ±0.1 |
| C | CAT02 | 3.0RP 5.5/2.0 | grayish purple | ❌ | grayish purple | ❌ | ±0.1 |

#### 23. Expected: dark reddish gray
Hex: #5D4E53

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.0RP 3.4/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| C | Bradford | 4.0RP 3.4/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| C | CAT02 | 4.0RP 3.4/1.4 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |

#### 24. Expected: reddish black
Hex: #30262B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.1RP 1.6/1.0 | purplish black | ❌ | purplish black | ❌ | ±0.1 |
| C | Bradford | 6.0RP 1.6/1.0 | purplish black | ❌ | purplish black | ❌ | ±0.1 |
| C | CAT02 | 6.0RP 1.6/1.0 | purplish black | ❌ | purplish black | ❌ | ±0.1 |

#### 25. Expected: vivid yellowish pink
Hex: #FD7E5D - **All configurations matched**

#### 26. Expected: strong yellowish pink
Hex: #F59080 - **All configurations matched**

#### 27. Expected: deep yellowish pink
Hex: #EF6366

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8R 5.9/11.7 | strong reddish orange | ❌ | deep yellowish pink | ✅ | ±0.1 |
| C | Bradford | 7.0R 5.9/11.4 | strong reddish orange | ❌ | deep yellowish pink | ✅ | ±0.1 |
| C | CAT02 | 6.9R 5.9/11.4 | strong reddish orange | ❌ | deep yellowish pink | ✅ | ±0.1 |
| D65 | XYZScaling | 7.4R 5.9/11.4 | strong reddish orange | ❌ | strong reddish orange | ❌ | ±0.1 |
| D65 | Bradford | 7.4R 5.9/11.4 | strong reddish orange | ❌ | strong reddish orange | ❌ | ±0.1 |
| D65 | CAT02 | 7.4R 5.9/11.4 | strong reddish orange | ❌ | strong reddish orange | ❌ | ±0.1 |
| F7 | XYZScaling | 7.4R 5.9/11.4 | strong reddish orange | ❌ | strong reddish orange | ❌ | ±0.1 |
| F7 | Bradford | 7.4R 5.9/11.4 | strong reddish orange | ❌ | strong reddish orange | ❌ | ±0.1 |
| F7 | CAT02 | 7.4R 5.9/11.4 | strong reddish orange | ❌ | strong reddish orange | ❌ | ±0.1 |

#### 28. Expected: light yellowish pink
Hex: #F8C4B6 - **All configurations matched**

#### 29. Expected: moderate yellowish pink
Hex: #E2A698 - **All configurations matched**

#### 30. Expected: dark yellowish pink
Hex: #C9807E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.9R 6.0/7.0 | deep pink | ❌ | deep pink | ❌ | ±0.1 |
| D65 | XYZScaling | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |
| D65 | Bradford | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |
| D65 | CAT02 | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |
| F7 | XYZScaling | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |
| F7 | Bradford | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |
| F7 | CAT02 | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ | ±0.1 |

#### 31. Expected: pale yellowish pink
Hex: #F1D3D1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.6R 8.7/2.9 | pale pink | ❌ | pale pink | ❌ | ±0.1 |
| C | Bradford | 4.0R 8.7/2.8 | pale pink | ❌ | pale pink | ❌ |  |
| C | CAT02 | 4.0R 8.7/2.8 | pale pink | ❌ | pale pink | ❌ |  |

#### 32. Expected: grayish yellowish pink
Hex: #CBACAC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.8R 7.2/2.6 | grayish pink | ❌ | grayish pink | ❌ |  |
| C | Bradford | 6.0R 7.2/2.5 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |
| C | CAT02 | 6.0R 7.2/2.5 | grayish pink | ❌ | grayish pink | ❌ | ±0.1 |

#### 33. Expected: brownish pink
Hex: #CBAFA7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.2R 7.3/2.6 | grayish yellowish pink | ❌ | grayish yellowish pink | ❌ |  |
| C | Bradford | 0.0YR 7.3/2.5 | grayish yellowish pink | ❌ | grayish yellowish pink | ❌ | ±0.1 |
| C | CAT02 | 0.0YR 7.3/2.5 | grayish yellowish pink | ❌ | grayish yellowish pink | ❌ | ±0.1 |
| D65 | XYZScaling | 9.2YR 7.3/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |
| D65 | Bradford | 9.2YR 7.3/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |
| D65 | CAT02 | 9.2YR 7.3/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |
| F7 | XYZScaling | 9.3YR 7.3/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |
| F7 | Bradford | 9.3YR 7.3/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |
| F7 | CAT02 | 9.3YR 7.3/2.0 | yellowish gray | ❌ | yellowish gray | ❌ | ±0.1 |

#### 34. Expected: vivid reddish orange
Hex: #E83B1B - **All configurations matched**

#### 35. Expected: strong reddish orange
Hex: #DB5D3B - **All configurations matched**

#### 36. Expected: deep reddish orange
Hex: #AF3318 - **All configurations matched**

#### 37. Expected: moderate reddish orange
Hex: #CD6952 - **All configurations matched**

#### 38. Expected: dark reddish orange
Hex: #A2402B - **All configurations matched**

#### 39. Expected: grayish reddish orange
Hex: #B97565 - **All configurations matched**

#### 40. Expected: strong reddish brown
Hex: #8B1C0E - **All configurations matched**

#### 41. Expected: deep reddish brown
Hex: #610F12 - **All configurations matched**

#### 42. Expected: light reddish brown
Hex: #AC7A73

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9R 5.5/4.3 | grayish red | ❌ | grayish red | ❌ | ±0.1 |

#### 43. Expected: moderate reddish brown
Hex: #7D423B - **All configurations matched**

#### 44. Expected: dark reddish brown
Hex: #461D1E - **All configurations matched**

#### 45. Expected: light grayish reddish brown
Hex: #9E7F7A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.2R 5.5/2.7 | grayish red | ❌ | grayish red | ❌ | ±0.1 |
| C | Bradford | 8.4R 5.5/2.6 | grayish red | ❌ | grayish red | ❌ | ±0.1 |
| C | CAT02 | 8.4R 5.5/2.6 | grayish red | ❌ | grayish red | ❌ | ±0.1 |

#### 46. Expected: grayish reddish brown
Hex: #6C4D4B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.5R 3.5/2.4 | grayish red | ❌ | grayish red | ❌ | ±0.1 |
| C | Bradford | 7.7R 3.5/2.4 | grayish red | ❌ | grayish red | ❌ | ±0.1 |
| C | CAT02 | 7.7R 3.5/2.4 | grayish red | ❌ | grayish red | ❌ | ±0.1 |

#### 47. Expected: dark grayish reddish brown
Hex: #43292A - **All configurations matched**

#### 48. Expected: vivid orange
Hex: #F7760B - **All configurations matched**

#### 49. Expected: strong orange
Hex: #EA8127 - **All configurations matched**

#### 50. Expected: deep orange
Hex: #C26012 - **All configurations matched**

#### 51. Expected: light orange
Hex: #FBAF82

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.5YR 7.7/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| D65 | Bradford | 7.5YR 7.7/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| D65 | CAT02 | 7.5YR 7.7/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| F7 | XYZScaling | 7.5YR 7.7/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| F7 | Bradford | 7.5YR 7.7/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |
| F7 | CAT02 | 7.5YR 7.7/6.9 | moderate orange yellow | ❌ | moderate orange yellow | ❌ |  |

#### 52. Expected: moderate orange
Hex: #DE8D5C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |
| D65 | Bradford | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |
| D65 | CAT02 | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |
| F7 | XYZScaling | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |
| F7 | Bradford | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |
| F7 | CAT02 | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ | ±0.1 |

#### 53. Expected: brownish orange
Hex: #B26633

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 7.1YR 5.0/8.0 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| D65 | Bradford | 7.1YR 5.0/8.0 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| D65 | CAT02 | 7.1YR 5.0/8.0 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 7.1YR 5.0/8.0 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| F7 | Bradford | 7.1YR 5.0/8.0 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |
| F7 | CAT02 | 7.1YR 5.0/8.0 | strong yellowish brown | ❌ | strong yellowish brown | ❌ | ±0.1 |

#### 54. Expected: strong brown
Hex: #8A4416 - **All configurations matched**

#### 55. Expected: deep brown
Hex: #571A07 - **All configurations matched**

#### 56. Expected: light brown
Hex: #AD7C63 - **All configurations matched**

#### 57. Expected: moderate brown
Hex: #724A38 - **All configurations matched**

#### 58. Expected: dark brown
Hex: #442112 - **All configurations matched**

#### 59. Expected: light grayish brown
Hex: #997F75

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.1YR 5.4/2.3 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ | ±0.1 |
| C | Bradford | 2.8YR 5.4/2.2 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ | ±0.1 |
| C | CAT02 | 2.8YR 5.4/2.2 | light grayish reddish brown | ❌ | light grayish reddish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 0.4Y 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| D65 | Bradford | 0.4Y 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| D65 | CAT02 | 0.4Y 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| F7 | XYZScaling | 0.5Y 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| F7 | Bradford | 0.5Y 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |
| F7 | CAT02 | 0.5Y 5.4/2.0 | grayish yellowish brown | ❌ | grayish yellowish brown | ❌ | ±0.1 |

#### 60. Expected: grayish brown
Hex: #674F48

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.5YR 3.5/2.0 | moderate reddish brown | ❌ | grayish reddish brown | ❌ | ±0.1 |
| C | Bradford | 2.1YR 3.5/1.9 | grayish brown | ✅ | grayish reddish brown | ❌ | ±0.1 |
| C | CAT02 | 2.1YR 3.5/1.9 | grayish brown | ✅ | grayish reddish brown | ❌ | ±0.1 |

#### 61. Expected: dark grayish brown
Hex: #3E2C28

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.4YR 2.0/1.8 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| C | Bradford | 0.6YR 2.0/1.8 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |
| C | CAT02 | 0.6YR 2.0/1.8 | dark grayish reddish brown | ❌ | dark grayish reddish brown | ❌ | ±0.1 |

#### 62. Expected: light brownish gray
Hex: #928281

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.0R 5.5/1.3 | reddish gray | ❌ | reddish gray | ❌ | ±0.1 |
| C | Bradford | 7.2R 5.5/1.3 | reddish gray | ❌ | reddish gray | ❌ | ±0.1 |
| C | CAT02 | 7.2R 5.5/1.3 | reddish gray | ❌ | reddish gray | ❌ | ±0.1 |

#### 63. Expected: brownish gray
Hex: #605251

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.7R 3.6/1.1 | dark reddish gray | ❌ | dark reddish gray | ❌ | ±0.1 |
| C | Bradford | 5.7R 3.6/1.1 | dark reddish gray | ❌ | dark reddish gray | ❌ | ±0.1 |
| C | CAT02 | 5.6R 3.6/1.1 | dark reddish gray | ❌ | dark reddish gray | ❌ | ±0.1 |

#### 64. Expected: brownish black
Hex: #2B211E - **All configurations matched**

#### 65. Expected: brilliant orange yellow
Hex: #FFBE50

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.6Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| C | Bradford | 4.3Y 8.1/9.3 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| C | CAT02 | 4.2Y 8.0/9.2 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 6.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| D65 | Bradford | 6.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| D65 | CAT02 | 6.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 6.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| F7 | Bradford | 6.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |
| F7 | CAT02 | 6.3Y 8.1/9.4 | brilliant yellow | ❌ | brilliant yellow | ❌ | ±0.1 |

#### 66. Expected: strong orange yellow
Hex: #F0A121

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 1.7Y 7.1/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| C | CAT02 | 1.6Y 7.1/11.1 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| D65 | XYZScaling | 3.0Y 7.1/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| D65 | Bradford | 3.0Y 7.1/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| D65 | CAT02 | 3.0Y 7.1/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| F7 | XYZScaling | 3.0Y 7.1/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| F7 | Bradford | 3.0Y 7.2/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |
| F7 | CAT02 | 3.0Y 7.2/11.2 | vivid yellow | ❌ | vivid yellow | ❌ |  |

#### 67. Expected: deep orange yellow
Hex: #D08511

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 2.0Y 6.1/10.5 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| D65 | Bradford | 2.0Y 6.1/10.5 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| D65 | CAT02 | 2.0Y 6.1/10.5 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 2.0Y 6.1/10.5 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| F7 | Bradford | 2.0Y 6.1/10.5 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |
| F7 | CAT02 | 2.0Y 6.1/10.5 | deep yellow | ❌ | deep yellow | ❌ | ±0.1 |

#### 68. Expected: light orange yellow
Hex: #FCC27C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.2Y 8.2/6.8 | light yellow | ❌ | light yellow | ❌ |  |
| C | Bradford | 2.1Y 8.2/6.7 | light yellow | ❌ | light yellow | ❌ |  |
| C | CAT02 | 2.0Y 8.2/6.6 | light yellow | ❌ | light yellow | ❌ |  |
| D65 | XYZScaling | 4.7Y 8.2/6.7 | light yellow | ❌ | light yellow | ❌ |  |
| D65 | Bradford | 4.7Y 8.2/6.7 | light yellow | ❌ | light yellow | ❌ |  |
| D65 | CAT02 | 4.7Y 8.2/6.7 | light yellow | ❌ | light yellow | ❌ |  |
| F7 | XYZScaling | 4.8Y 8.2/6.7 | light yellow | ❌ | light yellow | ❌ |  |
| F7 | Bradford | 4.8Y 8.2/6.8 | light yellow | ❌ | light yellow | ❌ |  |
| F7 | CAT02 | 4.8Y 8.2/6.8 | light yellow | ❌ | light yellow | ❌ |  |

#### 69. Expected: moderate orange yellow
Hex: #E7A75D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 1.1Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 3.3Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| D65 | Bradford | 3.3Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| D65 | CAT02 | 3.3Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 3.3Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| F7 | Bradford | 3.3Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |
| F7 | CAT02 | 3.3Y 7.2/7.6 | moderate yellow | ❌ | moderate yellow | ❌ | ±0.1 |

#### 70. Expected: dark orange yellow
Hex: #C38639

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.8Y 6.0/8.0 | dark yellow | ❌ | dark orange yellow | ✅ | ±0.1 |
| C | Bradford | 1.6Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| C | CAT02 | 1.6Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 3.2Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| D65 | Bradford | 3.2Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| D65 | CAT02 | 3.2Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 3.3Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| F7 | Bradford | 3.2Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |
| F7 | CAT02 | 3.2Y 6.0/7.8 | dark yellow | ❌ | dark yellow | ❌ | ±0.1 |

#### 71. Expected: pale orange yellow
Hex: #EEC6A6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.0Y 8.2/3.7 | pale yellow | ❌ | pale yellow | ❌ |  |
| D65 | Bradford | 4.0Y 8.2/3.7 | pale yellow | ❌ | pale yellow | ❌ |  |
| D65 | CAT02 | 4.0Y 8.2/3.7 | pale yellow | ❌ | pale yellow | ❌ |  |
| F7 | XYZScaling | 4.0Y 8.2/3.7 | pale yellow | ❌ | pale yellow | ❌ |  |
| F7 | Bradford | 4.0Y 8.2/3.7 | pale yellow | ❌ | pale yellow | ❌ |  |
| F7 | CAT02 | 4.0Y 8.2/3.7 | pale yellow | ❌ | pale yellow | ❌ |  |

#### 72. Expected: strong yellowish brown
Hex: #9E671D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.1Y 4.7/7.7 | light olive brown | ❌ | light olive brown | ❌ |  |
| C | Bradford | 1.7Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| C | CAT02 | 1.7Y 4.7/7.5 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | XYZScaling | 3.0Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | Bradford | 3.0Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 3.0Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 3.0Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | Bradford | 3.0Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 3.0Y 4.7/7.6 | light olive brown | ❌ | light olive brown | ❌ | ±0.1 |

#### 73. Expected: deep yellowish brown
Hex: #673F0B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.4Y 3.0/6.1 | moderate olive brown | ❌ | deep yellowish brown | ✅ | ±0.1 |
| C | Bradford | 0.9Y 3.0/6.0 | moderate olive brown | ❌ | deep yellowish brown | ✅ | ±0.1 |
| C | CAT02 | 0.9Y 3.0/6.0 | moderate olive brown | ❌ | deep yellowish brown | ✅ | ±0.1 |
| D65 | XYZScaling | 1.9Y 3.0/6.0 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | Bradford | 1.9Y 3.0/6.0 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 1.9Y 3.0/6.0 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 1.9Y 3.0/6.0 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | Bradford | 1.9Y 3.0/6.0 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 1.9Y 3.0/6.0 | moderate olive brown | ❌ | moderate olive brown | ❌ | ±0.1 |

#### 74. Expected: light yellowish brown
Hex: #C49A74

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | Bradford | 0.2Y 6.6/4.3 | grayish yellow | ❌ | light yellowish brown | ✅ | ±0.1 |
| C | CAT02 | 0.1Y 6.6/4.2 | grayish yellow | ❌ | light yellowish brown | ✅ | ±0.1 |
| D65 | XYZScaling | 4.2Y 6.6/4.3 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| D65 | Bradford | 4.2Y 6.6/4.3 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 4.2Y 6.6/4.3 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 4.3Y 6.6/4.3 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| F7 | Bradford | 4.3Y 6.6/4.3 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 4.3Y 6.6/4.3 | grayish yellow | ❌ | grayish yellow | ❌ | ±0.1 |

#### 75. Expected: moderate yellowish brown
Hex: #886648

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.1Y 4.5/3.6 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | Bradford | 4.1Y 4.5/3.6 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | CAT02 | 4.1Y 4.5/3.6 | light olive | ❌ | light olive | ❌ | ±0.1 |
| F7 | XYZScaling | 4.2Y 4.5/3.6 | light olive | ❌ | light olive | ❌ | ±0.1 |
| F7 | Bradford | 4.2Y 4.5/3.6 | light olive | ❌ | light olive | ❌ | ±0.1 |
| F7 | CAT02 | 4.2Y 4.5/3.6 | light olive | ❌ | light olive | ❌ | ±0.1 |

#### 76. Expected: dark yellowish brown
Hex: #50341A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.2Y 2.4/3.7 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| D65 | Bradford | 1.2Y 2.4/3.7 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| D65 | CAT02 | 1.2Y 2.4/3.7 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| F7 | XYZScaling | 1.2Y 2.4/3.7 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| F7 | Bradford | 1.2Y 2.4/3.7 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |
| F7 | CAT02 | 1.2Y 2.4/3.7 | dark olive brown | ❌ | dark olive brown | ❌ | ±0.1 |

#### 77. Expected: light grayish yellowish brown
Hex: #B49B8D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.9YR 6.5/2.2 | light grayish brown | ❌ | light grayish brown | ❌ | ±0.1 |
| C | Bradford | 6.8YR 6.5/2.1 | light grayish brown | ❌ | light grayish brown | ❌ | ±0.1 |
| C | CAT02 | 6.8YR 6.5/2.1 | light grayish brown | ❌ | light grayish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 4.9Y 6.5/2.0 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| D65 | Bradford | 4.9Y 6.5/2.0 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| D65 | CAT02 | 4.9Y 6.5/2.0 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| F7 | XYZScaling | 5.0Y 6.5/2.0 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| F7 | Bradford | 5.0Y 6.5/2.0 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |
| F7 | CAT02 | 5.1Y 6.5/2.0 | light grayish olive | ❌ | light grayish olive | ❌ | ±0.1 |

#### 78. Expected: grayish yellowish brown
Hex: #7E695D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.3YR 4.5/1.8 | grayish yellowish brown | ✅ | light grayish brown | ❌ | ±0.1 |
| C | Bradford | 7.9YR 4.5/1.8 | grayish yellowish brown | ✅ | light grayish brown | ❌ | ±0.1 |
| C | CAT02 | 7.9YR 4.5/1.8 | grayish yellowish brown | ✅ | light grayish brown | ❌ | ±0.1 |
| D65 | XYZScaling | 4.5Y 4.5/1.8 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| D65 | Bradford | 4.5Y 4.5/1.8 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| D65 | CAT02 | 4.5Y 4.5/1.8 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| F7 | XYZScaling | 4.6Y 4.5/1.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| F7 | Bradford | 4.6Y 4.5/1.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |
| F7 | CAT02 | 4.6Y 4.5/1.9 | light olive gray | ❌ | light olive gray | ❌ | ±0.1 |

#### 79. Expected: dark grayish yellowish brown
Hex: #4D3D33

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 3.2Y 2.7/1.8 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| D65 | Bradford | 3.2Y 2.7/1.8 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| D65 | CAT02 | 3.2Y 2.7/1.8 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| F7 | XYZScaling | 3.2Y 2.7/1.8 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| F7 | Bradford | 3.2Y 2.7/1.8 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |
| F7 | CAT02 | 3.2Y 2.7/1.8 | moderate olive brown | ❌ | moderate olive brown | ❌ |  |

#### 80. Expected: vivid yellow
Hex: #F1BF15

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.3Y 7.9/11.0 | strong greenish yellow | ❌ | strong greenish yellow | ❌ | ±0.1 |
| C | Bradford | 0.2GY 7.9/11.0 | strong greenish yellow | ❌ | strong greenish yellow | ❌ | ±0.1 |
| C | CAT02 | 0.1GY 7.9/10.8 | strong greenish yellow | ❌ | strong greenish yellow | ❌ |  |
| D65 | XYZScaling | 1.2GY 7.9/11.2 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 1.2GY 7.9/11.2 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 1.2GY 7.9/11.2 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 1.2GY 7.9/11.2 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 1.2GY 7.9/11.2 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 1.2GY 7.9/11.2 | vivid greenish yellow | ❌ | vivid greenish yellow | ❌ | ±0.1 |

#### 81. Expected: brilliant yellow
Hex: #F7CE50

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.3GY 8.4/9.1 | brilliant yellow green | ❌ | brilliant greenish yellow | ❌ |  |
| C | Bradford | 1.8GY 8.4/9.2 | brilliant yellow green | ❌ | brilliant greenish yellow | ❌ |  |
| C | CAT02 | 1.8GY 8.4/9.1 | brilliant yellow green | ❌ | brilliant greenish yellow | ❌ |  |
| D65 | XYZScaling | 3.0GY 8.4/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| D65 | Bradford | 3.0GY 8.4/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| D65 | CAT02 | 3.0GY 8.4/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | XYZScaling | 3.0GY 8.4/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | Bradford | 3.0GY 8.4/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | CAT02 | 3.0GY 8.4/9.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |

#### 82. Expected: strong yellow
Hex: #D9AE2F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.6Y 7.2/9.2 | strong greenish yellow | ❌ | strong greenish yellow | ❌ |  |
| C | Bradford | 0.3GY 7.2/9.2 | strong greenish yellow | ❌ | strong greenish yellow | ❌ |  |
| C | CAT02 | 0.3GY 7.2/9.1 | strong greenish yellow | ❌ | strong greenish yellow | ❌ |  |
| D65 | XYZScaling | 1.3GY 7.2/9.5 | strong yellow green | ❌ | strong greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 1.3GY 7.2/9.5 | strong yellow green | ❌ | strong greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 1.3GY 7.2/9.5 | strong yellow green | ❌ | strong greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 1.3GY 7.2/9.5 | strong yellow green | ❌ | strong greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 1.3GY 7.2/9.5 | strong yellow green | ❌ | strong greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 1.3GY 7.2/9.5 | strong yellow green | ❌ | strong greenish yellow | ❌ | ±0.1 |

#### 83. Expected: deep yellow
Hex: #B88F16

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.0Y 6.1/8.7 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| C | Bradford | 8.7Y 6.0/8.7 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| C | CAT02 | 8.6Y 6.0/8.6 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 0.1GY 6.1/8.8 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 0.1GY 6.1/8.8 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 0.1GY 6.1/8.8 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 0.1GY 6.1/8.8 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 0.1GY 6.1/8.8 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 0.1GY 6.1/8.8 | deep greenish yellow | ❌ | deep greenish yellow | ❌ | ±0.1 |

#### 84. Expected: light yellow
Hex: #F4D284

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.6GY 8.5/6.1 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| C | Bradford | 3.2GY 8.5/6.2 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| C | CAT02 | 3.2GY 8.5/6.1 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.8GY 8.5/6.8 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| D65 | Bradford | 4.8GY 8.5/6.8 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 4.8GY 8.5/6.8 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.8GY 8.5/6.8 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| F7 | Bradford | 4.8GY 8.5/6.8 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 4.8GY 8.5/6.8 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |

#### 85. Expected: moderate yellow
Hex: #D2AF63

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.7GY 7.2/6.2 | moderate greenish yellow | ❌ | moderate greenish yellow | ❌ |  |
| C | Bradford | 1.1GY 7.2/6.3 | moderate yellow green | ❌ | moderate greenish yellow | ❌ |  |
| C | CAT02 | 1.1GY 7.2/6.2 | moderate yellow green | ❌ | moderate greenish yellow | ❌ |  |
| D65 | XYZScaling | 2.3GY 7.2/6.7 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | Bradford | 2.3GY 7.2/6.7 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | CAT02 | 2.3GY 7.2/6.7 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | XYZScaling | 2.3GY 7.2/6.7 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | Bradford | 2.3GY 7.2/6.7 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | CAT02 | 2.3GY 7.2/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |

#### 86. Expected: dark yellow
Hex: #B08F42

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.5Y 6.0/6.3 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| C | Bradford | 0.1GY 6.0/6.3 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| C | CAT02 | 0.1GY 6.0/6.2 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| D65 | XYZScaling | 1.0GY 6.0/6.7 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| D65 | Bradford | 1.0GY 6.0/6.7 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| D65 | CAT02 | 1.0GY 6.0/6.7 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| F7 | XYZScaling | 1.1GY 6.0/6.7 | moderate yellow green | ❌ | dark greenish yellow | ❌ | ±0.1 |
| F7 | Bradford | 1.0GY 6.0/6.7 | dark greenish yellow | ❌ | dark greenish yellow | ❌ | ±0.1 |
| F7 | CAT02 | 1.1GY 6.0/6.7 | moderate yellow green | ❌ | dark greenish yellow | ❌ | ±0.1 |

#### 87. Expected: pale yellow
Hex: #EFD7B2

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.6GY 8.7/3.0 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| C | Bradford | 6.0GY 8.7/3.3 | light yellow green | ❌ | light yellow green | ❌ |  |
| C | CAT02 | 5.9GY 8.7/3.3 | light yellow green | ❌ | light yellow green | ❌ |  |
| D65 | XYZScaling | 8.5GY 8.7/4.6 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.5GY 8.7/4.6 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.5GY 8.7/4.6 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.4GY 8.7/4.6 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.4GY 8.7/4.6 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.4GY 8.7/4.6 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |

#### 88. Expected: grayish yellow
Hex: #C8B18B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.7GY 7.2/3.3 | moderate yellow green | ❌ | grayish greenish yellow | ❌ |  |
| C | Bradford | 2.6GY 7.2/3.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| C | CAT02 | 2.5GY 7.2/3.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | XYZScaling | 4.1GY 7.2/3.9 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | Bradford | 4.1GY 7.2/3.9 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 4.1GY 7.2/3.9 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.1GY 7.2/4.0 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | Bradford | 4.1GY 7.2/4.0 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 4.1GY 7.2/4.0 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |

#### 89. Expected: dark grayish yellow
Hex: #A99066

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.3GY 6.0/3.8 | light olive | ❌ | light olive | ❌ | ±0.1 |
| C | Bradford | 1.3GY 6.0/3.8 | light olive | ❌ | light olive | ❌ | ±0.1 |
| C | CAT02 | 1.3GY 6.0/3.8 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | XYZScaling | 1.8GY 6.0/4.2 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | Bradford | 1.8GY 6.0/4.2 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | CAT02 | 1.8GY 6.0/4.2 | light olive | ❌ | light olive | ❌ | ±0.1 |
| F7 | XYZScaling | 1.8GY 6.0/4.2 | light olive | ❌ | light olive | ❌ | ±0.1 |
| F7 | Bradford | 1.8GY 6.0/4.2 | light olive | ❌ | light olive | ❌ | ±0.1 |
| F7 | CAT02 | 1.8GY 6.0/4.2 | light olive | ❌ | light olive | ❌ | ±0.1 |

#### 90. Expected: yellowish white
Hex: #EEDFDA

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.7R 9.0/1.6 | pale yellowish pink | ❌ | pale yellowish pink | ❌ | ±0.1 |
| C | Bradford | 0.9YR 9.0/1.4 | pinkish white | ❌ | pinkish white | ❌ | ±0.1 |
| C | CAT02 | 0.9YR 9.0/1.4 | pinkish white | ❌ | pinkish white | ❌ | ±0.1 |

#### 91. Expected: yellowish gray
Hex: #C6B9B1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.0YR 7.5/1.1 | yellowish gray | ✅ | pinkish gray | ❌ | ±0.1 |
| D65 | XYZScaling | 6.7GY 7.5/1.6 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| D65 | Bradford | 6.7GY 7.5/1.6 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 6.7GY 7.5/1.6 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.6GY 7.5/1.5 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.6GY 7.5/1.5 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 6.7GY 7.5/1.6 | pale yellow green | ❌ | pale yellow green | ❌ | ±0.1 |

#### 92. Expected: light olive brown
Hex: #997736

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.6Y 5.1/5.6 | light olive | ❌ | light olive | ❌ |  |
| C | Bradford | 8.1Y 5.1/5.6 | light olive | ❌ | light olive | ❌ |  |
| C | CAT02 | 8.1Y 5.1/5.6 | light olive | ❌ | light olive | ❌ | ±0.1 |
| D65 | XYZScaling | 9.4Y 5.1/5.9 | light olive | ❌ | light olive | ❌ |  |
| D65 | Bradford | 9.4Y 5.1/5.9 | light olive | ❌ | light olive | ❌ |  |
| D65 | CAT02 | 9.4Y 5.1/5.9 | light olive | ❌ | light olive | ❌ |  |
| F7 | XYZScaling | 9.4Y 5.1/5.9 | light olive | ❌ | light olive | ❌ |  |
| F7 | Bradford | 9.4Y 5.1/5.9 | light olive | ❌ | light olive | ❌ |  |
| F7 | CAT02 | 9.4Y 5.1/5.9 | light olive | ❌ | light olive | ❌ |  |

#### 93. Expected: moderate olive brown
Hex: #705420

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.1Y 3.7/5.0 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| C | Bradford | 6.6Y 3.7/5.0 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| C | CAT02 | 6.5Y 3.7/4.9 | moderate olive | ❌ | moderate olive | ❌ | ±0.1 |
| D65 | XYZScaling | 7.8Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| D65 | Bradford | 7.8Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| D65 | CAT02 | 7.8Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| F7 | XYZScaling | 7.8Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| F7 | Bradford | 7.8Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |
| F7 | CAT02 | 7.8Y 3.7/5.1 | moderate olive | ❌ | moderate olive | ❌ |  |

#### 94. Expected: dark olive brown
Hex: #3F2C10

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 5.2Y 1.9/3.3 | dark olive | ❌ | dark olive | ❌ | ±0.1 |
| D65 | Bradford | 5.2Y 1.9/3.3 | dark olive | ❌ | dark olive | ❌ | ±0.1 |
| D65 | CAT02 | 5.2Y 1.9/3.3 | dark olive | ❌ | dark olive | ❌ | ±0.1 |
| F7 | XYZScaling | 5.2Y 1.9/3.3 | dark olive | ❌ | dark olive | ❌ | ±0.1 |
| F7 | Bradford | 5.2Y 1.9/3.3 | dark olive | ❌ | dark olive | ❌ | ±0.1 |
| F7 | CAT02 | 5.2Y 1.9/3.3 | dark olive | ❌ | dark olive | ❌ | ±0.1 |

#### 95. Expected: vivid greenish yellow
Hex: #EBDD21

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4GY 8.6/11.7 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| C | Bradford | 5.5GY 8.6/11.8 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| C | CAT02 | 5.5GY 8.6/11.7 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| D65 | XYZScaling | 5.7GY 8.6/12.2 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| D65 | Bradford | 5.7GY 8.6/12.2 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| D65 | CAT02 | 5.7GY 8.6/12.2 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| F7 | XYZScaling | 5.7GY 8.6/12.2 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| F7 | Bradford | 5.7GY 8.6/12.2 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |
| F7 | CAT02 | 5.7GY 8.6/12.2 | vivid yellow green | ❌ | vivid yellow green | ❌ |  |

#### 96. Expected: brilliant greenish yellow
Hex: #E9DC55

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.4GY 8.6/10.1 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | Bradford | 6.6GY 8.6/10.2 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| C | CAT02 | 6.6GY 8.6/10.1 | brilliant yellow green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.7GY 8.6/10.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| D65 | Bradford | 6.7GY 8.6/10.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| D65 | CAT02 | 6.7GY 8.6/10.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | XYZScaling | 6.7GY 8.6/10.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | Bradford | 6.7GY 8.6/10.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |
| F7 | CAT02 | 6.7GY 8.6/10.6 | brilliant yellow green | ❌ | brilliant yellow green | ❌ |  |

#### 97. Expected: strong greenish yellow
Hex: #C4B827

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.1GY 7.3/10.0 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | Bradford | 5.2GY 7.3/10.1 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.2GY 7.3/10.0 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.4GY 7.3/10.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.4GY 7.3/10.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.4GY 7.3/10.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.4GY 7.3/10.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.4GY 7.3/10.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.4GY 7.3/10.5 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |

#### 98. Expected: deep greenish yellow
Hex: #A29812

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.4GY 6.1/9.0 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | Bradford | 4.6GY 6.1/9.1 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | CAT02 | 4.6GY 6.1/9.0 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.1GY 6.1/9.4 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.1GY 6.1/9.4 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.1GY 6.1/9.4 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.1GY 6.1/9.4 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.1GY 6.1/9.4 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.1GY 6.1/9.4 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |

#### 99. Expected: light greenish yellow
Hex: #E9DD8A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.5GY 8.7/7.0 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| C | Bradford | 7.7GY 8.7/7.1 | brilliant yellowish green | ❌ | brilliant yellow green | ❌ | ±0.1 |
| C | CAT02 | 7.7GY 8.7/7.0 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 8.5GY 8.7/8.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.5GY 8.7/8.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.5GY 8.7/8.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.5GY 8.7/8.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ |  |
| F7 | Bradford | 8.5GY 8.7/8.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ |  |
| F7 | CAT02 | 8.5GY 8.7/8.1 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ |  |

#### 100. Expected: moderate greenish yellow
Hex: #C0B55E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4GY 7.2/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| C | Bradford | 5.5GY 7.2/7.2 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| C | CAT02 | 5.5GY 7.2/7.1 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | XYZScaling | 6.0GY 7.2/7.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | Bradford | 6.0GY 7.2/7.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| D65 | CAT02 | 6.0GY 7.2/7.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | XYZScaling | 6.0GY 7.2/7.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | Bradford | 6.0GY 7.2/7.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |
| F7 | CAT02 | 6.0GY 7.2/7.8 | strong yellow green | ❌ | strong yellow green | ❌ |  |

#### 101. Expected: dark greenish yellow
Hex: #9E953C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.8GY 6.0/7.1 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | Bradford | 5.0GY 6.0/7.2 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| C | CAT02 | 5.0GY 6.0/7.1 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.4GY 6.0/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.4GY 6.0/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.4GY 6.0/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.4GY 6.0/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.4GY 6.0/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.4GY 6.0/7.6 | strong yellow green | ❌ | strong yellow green | ❌ | ±0.1 |

#### 102. Expected: pale greenish yellow
Hex: #E6DCAB

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.4G 8.7/5.1 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| C | Bradford | 6.1Y 8.7/3.2 | pale greenish yellow | ✅ | pale yellow | ❌ |  |
| C | CAT02 | 9.3GY 8.7/4.7 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| D65 | XYZScaling | 5.1GY 8.7/4.1 | light yellow green | ❌ | light yellow green | ❌ |  |
| D65 | Bradford | 5.1GY 8.7/4.1 | light yellow green | ❌ | light yellow green | ❌ |  |
| D65 | CAT02 | 5.1GY 8.7/4.1 | light yellow green | ❌ | light yellow green | ❌ |  |
| F7 | XYZScaling | 3.3GY 8.7/4.0 | light yellow green | ❌ | light yellow green | ❌ | ±0.1 |
| F7 | Bradford | 0.3G 8.7/5.8 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |
| F7 | CAT02 | 8.9GY 8.7/5.3 | very light yellowish green | ❌ | very light yellowish green | ❌ |  |

#### 103. Expected: grayish greenish yellow
Hex: #BEB584

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.4GY 7.3/4.4 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | Bradford | 6.7GY 7.2/4.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| C | CAT02 | 6.7GY 7.2/4.5 | moderate yellow green | ❌ | moderate yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 8.2GY 7.3/5.6 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.2GY 7.3/5.6 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.2GY 7.3/5.6 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.2GY 7.3/5.6 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.1GY 7.3/5.6 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.2GY 7.3/5.6 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |

#### 104. Expected: light olive
Hex: #8B7D2E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.4GY 5.1/6.2 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| C | Bradford | 2.8GY 5.1/6.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| C | CAT02 | 2.8GY 5.1/6.3 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | XYZScaling | 3.9GY 5.1/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | Bradford | 3.9GY 5.1/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| D65 | CAT02 | 3.9GY 5.1/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | XYZScaling | 3.9GY 5.1/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | Bradford | 3.8GY 5.1/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |
| F7 | CAT02 | 3.8GY 5.1/6.8 | moderate yellow green | ❌ | moderate yellow green | ❌ |  |

#### 105. Expected: moderate olive
Hex: #64591A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.5GY 3.7/5.3 | moderate olive green | ❌ | moderate olive | ✅ |  |
| C | Bradford | 1.8GY 3.7/5.3 | moderate olive green | ❌ | moderate olive | ✅ |  |
| C | CAT02 | 1.8GY 3.7/5.3 | moderate olive green | ❌ | moderate olive | ✅ |  |
| D65 | XYZScaling | 2.8GY 3.7/5.6 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| D65 | Bradford | 2.8GY 3.7/5.6 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| D65 | CAT02 | 2.8GY 3.7/5.6 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| F7 | XYZScaling | 2.8GY 3.7/5.6 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| F7 | Bradford | 2.8GY 3.7/5.6 | moderate olive green | ❌ | moderate olive green | ❌ |  |
| F7 | CAT02 | 2.8GY 3.7/5.6 | moderate olive green | ❌ | moderate olive green | ❌ |  |

#### 106. Expected: dark olive
Hex: #352E0A

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 1.3GY 1.9/3.6 | dark olive green | ❌ | dark olive | ✅ | ±0.1 |
| D65 | Bradford | 1.3GY 1.9/3.6 | dark olive green | ❌ | dark olive | ✅ | ±0.1 |
| D65 | CAT02 | 1.3GY 1.9/3.6 | dark olive green | ❌ | dark olive | ✅ | ±0.1 |
| F7 | XYZScaling | 1.3GY 1.9/3.6 | dark olive green | ❌ | dark olive | ✅ | ±0.1 |
| F7 | Bradford | 1.3GY 1.9/3.6 | dark olive green | ❌ | dark olive | ✅ | ±0.1 |
| F7 | CAT02 | 1.3GY 1.9/3.6 | dark olive green | ❌ | dark olive | ✅ | ±0.1 |

#### 107. Expected: light grayish olive
Hex: #8E856F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.3GY 5.5/2.0 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | Bradford | 2.4GY 5.5/2.0 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| C | CAT02 | 2.4GY 5.5/2.0 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.3GY 5.5/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.3GY 5.5/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.3GY 5.5/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.3GY 5.5/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.3GY 5.5/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.3GY 5.5/2.7 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |

#### 108. Expected: grayish olive
Hex: #5D553F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 2.6GY 3.6/2.6 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| D65 | Bradford | 2.6GY 3.6/2.6 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| D65 | CAT02 | 2.6GY 3.6/2.6 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| F7 | XYZScaling | 2.6GY 3.6/2.6 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| F7 | Bradford | 2.6GY 3.6/2.6 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |
| F7 | CAT02 | 2.6GY 3.6/2.6 | grayish olive green | ❌ | grayish olive green | ❌ | ±0.1 |

#### 109. Expected: dark grayish olive
Hex: #35301C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 2.1GY 2.0/2.7 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| D65 | Bradford | 2.1GY 2.0/2.7 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| D65 | CAT02 | 2.1GY 2.0/2.7 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| F7 | XYZScaling | 2.1GY 2.0/2.7 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| F7 | Bradford | 2.1GY 2.0/2.7 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |
| F7 | CAT02 | 2.1GY 2.0/2.7 | dark grayish olive green | ❌ | dark grayish olive green | ❌ | ±0.1 |

#### 110. Expected: light olive gray
Hex: #8F877F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 5.3GY 5.6/1.4 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | Bradford | 5.3GY 5.6/1.4 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| D65 | CAT02 | 5.3GY 5.6/1.4 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.3GY 5.6/1.4 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | Bradford | 5.3GY 5.6/1.4 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |
| F7 | CAT02 | 5.3GY 5.6/1.4 | grayish yellow green | ❌ | grayish yellow green | ❌ | ±0.1 |

#### 111. Expected: olive gray
Hex: #58514A - **All configurations matched**

#### 112. Expected: olive black
Hex: #23211C - **All configurations matched**

#### 113. Expected: vivid yellow green
Hex: #A7DC26

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.6GY 8.1/13.4 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| C | Bradford | 8.6GY 8.1/13.4 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| C | CAT02 | 8.6GY 8.1/13.3 | vivid yellowish green | ❌ | vivid yellowish green | ❌ | ±0.1 |
| D65 | XYZScaling | 9.0GY 8.1/14.2 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| D65 | Bradford | 9.0GY 8.1/14.2 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| D65 | CAT02 | 9.0GY 8.1/14.2 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | XYZScaling | 9.0GY 8.1/14.2 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | Bradford | 9.0GY 8.1/14.2 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |
| F7 | CAT02 | 9.0GY 8.1/14.2 | vivid yellowish green | ❌ | vivid yellowish green | ❌ |  |

#### 114. Expected: brilliant yellow green
Hex: #C3DF69

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.8GY 8.4/9.3 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ | ±0.1 |
| C | Bradford | 7.9GY 8.4/9.4 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ | ±0.1 |
| C | CAT02 | 7.9GY 8.4/9.3 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.4GY 8.4/10.3 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.4GY 8.4/10.3 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.4GY 8.4/10.3 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.4GY 8.4/10.3 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.4GY 8.4/10.3 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.4GY 8.4/10.3 | brilliant yellowish green | ❌ | brilliant yellowish green | ❌ | ±0.1 |

#### 115. Expected: strong yellow green
Hex: #82A12B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.8GY 6.1/9.7 | strong yellowish green | ❌ | strong yellow green | ✅ | ±0.1 |
| C | Bradford | 7.8GY 6.1/9.7 | strong yellowish green | ❌ | strong yellow green | ✅ | ±0.1 |
| C | CAT02 | 7.8GY 6.1/9.6 | strong yellowish green | ❌ | strong yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.2GY 6.1/10.4 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.2GY 6.1/10.4 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.2GY 6.1/10.4 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.2GY 6.1/10.4 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.2GY 6.1/10.4 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.2GY 6.1/10.4 | strong yellowish green | ❌ | strong yellowish green | ❌ | ±0.1 |

#### 116. Expected: deep yellow green
Hex: #486C0E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.0GY 4.1/8.2 | deep yellowish green | ❌ | deep yellow green | ✅ | ±0.1 |
| C | Bradford | 8.0GY 4.1/8.2 | deep yellowish green | ❌ | deep yellow green | ✅ | ±0.1 |
| C | CAT02 | 8.0GY 4.1/8.1 | deep yellowish green | ❌ | deep yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.1GY 4.1/8.5 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.1GY 4.1/8.5 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.1GY 4.1/8.5 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.1GY 4.1/8.5 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.1GY 4.1/8.5 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.1GY 4.1/8.5 | deep yellowish green | ❌ | deep yellowish green | ❌ | ±0.1 |

#### 117. Expected: light yellow green
Hex: #CEDB9F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.7GY 8.5/5.9 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.7GY 8.5/5.9 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.7GY 8.5/5.9 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.7GY 8.5/5.9 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.6GY 8.5/5.9 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.7GY 8.5/5.9 | light yellowish green | ❌ | light yellowish green | ❌ | ±0.1 |

#### 118. Expected: moderate yellow green
Hex: #8B9A5F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.7GY 6.0/5.5 | moderate yellowish green | ❌ | moderate yellow green | ✅ | ±0.1 |
| C | Bradford | 7.8GY 6.0/5.5 | moderate yellowish green | ❌ | moderate yellow green | ✅ | ±0.1 |
| C | CAT02 | 7.8GY 6.0/5.5 | moderate yellowish green | ❌ | moderate yellow green | ✅ | ±0.1 |
| D65 | XYZScaling | 8.4GY 6.0/6.3 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 8.4GY 6.0/6.3 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 8.4GY 6.0/6.3 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 8.4GY 6.0/6.3 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 8.4GY 6.0/6.3 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 8.4GY 6.0/6.3 | moderate yellowish green | ❌ | moderate yellowish green | ❌ | ±0.1 |

#### 119. Expected: pale yellow green
Hex: #D7D7C1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.4Y 8.5/1.3 | yellowish white | ❌ | yellowish white | ❌ | ±0.1 |
| C | Bradford | 8.3G 8.5/3.2 | very light green | ❌ | very light green | ❌ | ±0.1 |
| C | CAT02 | 4.5G 8.5/2.8 | very light green | ❌ | very light green | ❌ | ±0.1 |
| D65 | XYZScaling | 1.5G 8.5/3.3 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | Bradford | 1.5G 8.5/3.3 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| D65 | CAT02 | 1.5G 8.5/3.3 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | XYZScaling | 1.4G 8.5/3.4 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | Bradford | 1.4G 8.5/3.4 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |
| F7 | CAT02 | 1.4G 8.5/3.4 | very light yellowish green | ❌ | very light yellowish green | ❌ | ±0.1 |

#### 120. Expected: grayish yellow green
Hex: #979A85

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 8.3GY 6.2/2.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ |  |
| D65 | Bradford | 8.3GY 6.2/2.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ |  |
| D65 | CAT02 | 8.3GY 6.2/2.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ |  |
| F7 | XYZScaling | 8.2GY 6.2/2.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ |  |
| F7 | Bradford | 8.2GY 6.2/2.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ |  |
| F7 | CAT02 | 8.2GY 6.2/2.7 | moderate yellowish green | ❌ | moderate yellowish green | ❌ |  |

#### 121. Expected: strong olive green
Hex: #2C5506

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.7GY 3.1/7.5 | deep yellowish green | ❌ | strong olive green | ✅ | ±0.1 |
| C | Bradford | 7.6GY 3.1/7.5 | deep yellowish green | ❌ | strong olive green | ✅ | ±0.1 |
| C | CAT02 | 7.7GY 3.1/7.5 | deep yellowish green | ❌ | strong olive green | ✅ | ±0.1 |
| D65 | XYZScaling | 7.6GY 3.1/7.8 | deep yellowish green | ❌ | strong olive green | ✅ |  |
| D65 | Bradford | 7.6GY 3.1/7.8 | deep yellowish green | ❌ | strong olive green | ✅ |  |
| D65 | CAT02 | 7.6GY 3.1/7.8 | deep yellowish green | ❌ | strong olive green | ✅ |  |
| F7 | XYZScaling | 7.6GY 3.1/7.8 | deep yellowish green | ❌ | strong olive green | ✅ |  |
| F7 | Bradford | 7.6GY 3.1/7.8 | deep yellowish green | ❌ | strong olive green | ✅ |  |
| F7 | CAT02 | 7.6GY 3.1/7.8 | deep yellowish green | ❌ | strong olive green | ✅ |  |

#### 122. Expected: moderate olive green
Hex: #495B22

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.4GY 3.5/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| C | Bradford | 7.5GY 3.5/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| C | CAT02 | 7.5GY 3.5/5.7 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| D65 | XYZScaling | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| D65 | Bradford | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| D65 | CAT02 | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| F7 | XYZScaling | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| F7 | Bradford | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |
| F7 | CAT02 | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ | ±0.1 |

#### 123. Expected: dark olive green
Hex: #20340B - **All configurations matched**

#### 124. Expected: grayish olive green
Hex: #545947

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.2GY 3.6/2.1 | grayish green | ❌ | grayish olive green | ✅ |  |
| C | Bradford | 7.3GY 3.6/2.1 | grayish green | ❌ | grayish olive green | ✅ |  |
| C | CAT02 | 7.3GY 3.6/2.1 | grayish green | ❌ | grayish olive green | ✅ |  |
| D65 | XYZScaling | 8.1GY 3.6/2.7 | dark yellowish green | ❌ | dark yellowish green | ❌ |  |
| D65 | Bradford | 8.1GY 3.6/2.7 | dark yellowish green | ❌ | dark yellowish green | ❌ |  |
| D65 | CAT02 | 8.1GY 3.6/2.7 | dark yellowish green | ❌ | dark yellowish green | ❌ |  |
| F7 | XYZScaling | 8.1GY 3.6/2.7 | dark yellowish green | ❌ | dark yellowish green | ❌ |  |
| F7 | Bradford | 8.1GY 3.6/2.7 | dark yellowish green | ❌ | dark yellowish green | ❌ |  |
| F7 | CAT02 | 8.1GY 3.6/2.7 | dark yellowish green | ❌ | dark yellowish green | ❌ |  |

#### 125. Expected: dark grayish olive green
Hex: #2F3326 - **All configurations matched**

#### 126. Expected: vivid yellowish green
Hex: #3FD740 - **All configurations matched**

#### 127. Expected: brilliant yellowish green
Hex: #87D989

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.9G 7.9/10.4 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| C | Bradford | 3.8G 7.9/10.3 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| C | CAT02 | 3.8G 7.9/10.2 | brilliant green | ❌ | brilliant green | ❌ | ±0.1 |
| D65 | XYZScaling | 3.5G 7.9/11.2 | vivid green | ❌ | vivid green | ❌ | ±0.1 |
| D65 | Bradford | 3.5G 7.9/11.2 | vivid green | ❌ | vivid green | ❌ | ±0.1 |
| D65 | CAT02 | 3.5G 7.9/11.2 | vivid green | ❌ | vivid green | ❌ | ±0.1 |
| F7 | XYZScaling | 3.5G 7.9/11.2 | vivid green | ❌ | vivid green | ❌ | ±0.1 |
| F7 | Bradford | 3.5G 7.9/11.2 | vivid green | ❌ | vivid green | ❌ | ±0.1 |
| F7 | CAT02 | 3.5G 7.9/11.2 | vivid green | ❌ | vivid green | ❌ | ±0.1 |

#### 128. Expected: strong yellowish green
Hex: #39964A - **All configurations matched**

#### 129. Expected: deep yellowish green
Hex: #176A1E - **All configurations matched**

#### 130. Expected: very deep yellowish green
Hex: #054208 - **All configurations matched**

#### 131. Expected: very light yellowish green
Hex: #C5EDC4

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.1G 9.0/4.0 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |
| D65 | XYZScaling | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |
| D65 | Bradford | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |
| D65 | CAT02 | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |
| F7 | XYZScaling | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |
| F7 | Bradford | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |
| F7 | CAT02 | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ | ±0.1 |

#### 132. Expected: light yellowish green
Hex: #9CC69C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.6G 7.5/5.5 | very light green | ❌ | very light green | ❌ | ±0.1 |
| C | Bradford | 4.6G 7.5/5.4 | very light green | ❌ | very light green | ❌ | ±0.1 |
| C | CAT02 | 4.6G 7.5/5.4 | very light green | ❌ | very light green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.1G 7.5/6.5 | very light green | ❌ | very light green | ❌ | ±0.1 |
| D65 | Bradford | 4.1G 7.5/6.5 | very light green | ❌ | very light green | ❌ | ±0.1 |
| D65 | CAT02 | 4.1G 7.5/6.5 | very light green | ❌ | very light green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.0G 7.5/6.6 | very light green | ❌ | very light green | ❌ | ±0.1 |
| F7 | Bradford | 4.0G 7.5/6.6 | very light green | ❌ | very light green | ❌ | ±0.1 |
| F7 | CAT02 | 4.0G 7.5/6.6 | very light green | ❌ | very light green | ❌ | ±0.1 |

#### 133. Expected: moderate yellowish green
Hex: #669069

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.2G 5.5/5.4 | moderate green | ❌ | moderate green | ❌ | ±0.1 |
| C | Bradford | 3.1G 5.5/5.3 | moderate green | ❌ | moderate green | ❌ | ±0.1 |
| C | CAT02 | 3.1G 5.5/5.3 | moderate green | ❌ | moderate green | ❌ | ±0.1 |

#### 134. Expected: dark yellowish green
Hex: #2F5D3A - **All configurations matched**

#### 135. Expected: very dark yellowish green
Hex: #10361A - **All configurations matched**

#### 136. Expected: vivid green
Hex: #23EAA5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.4BG 8.2/12.9 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| C | Bradford | 6.3BG 8.2/12.7 | vivid bluish green | ❌ | vivid bluish green | ❌ |  |
| C | CAT02 | 6.3BG 8.2/12.6 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.2BG 8.2/15.0 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| D65 | Bradford | 5.2BG 8.2/15.0 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 5.2BG 8.2/15.0 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.2BG 8.2/15.1 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| F7 | Bradford | 5.2BG 8.2/15.1 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 5.2BG 8.2/15.1 | vivid bluish green | ❌ | vivid bluish green | ❌ | ±0.1 |

#### 137. Expected: brilliant green
Hex: #49D0A3

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.4BG 7.5/8.6 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| C | Bradford | 8.3BG 7.5/8.4 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| C | CAT02 | 8.4BG 7.5/8.4 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.8BG 7.5/10.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| D65 | Bradford | 6.8BG 7.5/10.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 6.8BG 7.5/10.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 6.8BG 7.5/10.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| F7 | Bradford | 6.8BG 7.5/10.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 6.8BG 7.5/10.3 | brilliant bluish green | ❌ | brilliant bluish green | ❌ | ±0.1 |

#### 138. Expected: strong green
Hex: #158A66

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.7BG 5.0/7.9 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| C | Bradford | 5.7BG 5.0/7.8 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| C | CAT02 | 5.7BG 5.0/7.7 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 4.3BG 5.0/9.2 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| D65 | Bradford | 4.3BG 5.0/9.2 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 4.3BG 5.0/9.2 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 4.2BG 5.0/9.2 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| F7 | Bradford | 4.2BG 5.0/9.2 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 4.2BG 5.0/9.2 | strong bluish green | ❌ | strong bluish green | ❌ | ±0.1 |

#### 139. Expected: very light green
Hex: #A6E2CA

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.4B 8.5/3.7 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| C | Bradford | 0.3B 8.5/3.6 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| C | CAT02 | 0.3B 8.5/3.6 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 7.4BG 8.5/5.1 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| D65 | Bradford | 7.4BG 8.5/5.1 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 7.4BG 8.5/5.1 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 7.3BG 8.5/5.1 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| F7 | Bradford | 7.3BG 8.5/5.1 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 7.3BG 8.5/5.1 | very light bluish green | ❌ | very light bluish green | ❌ | ±0.1 |

#### 140. Expected: light green
Hex: #6FAC95

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.7BG 6.5/4.1 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| C | Bradford | 8.6BG 6.5/4.0 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| C | CAT02 | 8.6BG 6.5/4.0 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 6.3BG 6.5/5.4 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | Bradford | 6.3BG 6.5/5.4 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 6.3BG 6.5/5.4 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 6.2BG 6.5/5.5 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | Bradford | 6.2BG 6.5/5.5 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 6.2BG 6.5/5.5 | light bluish green | ❌ | light bluish green | ❌ | ±0.1 |

#### 141. Expected: moderate green
Hex: #337762

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.3BG 4.4/4.6 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | Bradford | 7.4BG 4.4/4.5 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| C | CAT02 | 7.4BG 4.4/4.4 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 5.8BG 4.4/5.5 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | Bradford | 5.8BG 4.4/5.5 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 5.8BG 4.4/5.5 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 5.8BG 4.4/5.6 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | Bradford | 5.8BG 4.4/5.6 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 5.8BG 4.4/5.6 | moderate bluish green | ❌ | moderate bluish green | ❌ | ±0.1 |

#### 142. Expected: dark green
Hex: #164E3D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4BG 2.9/4.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| C | Bradford | 5.4BG 2.9/4.1 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| C | CAT02 | 5.4BG 2.9/4.1 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| D65 | XYZScaling | 3.0BG 2.9/5.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| D65 | Bradford | 3.0BG 2.9/5.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| D65 | CAT02 | 3.0BG 2.9/5.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| F7 | XYZScaling | 2.9BG 2.9/5.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| F7 | Bradford | 2.9BG 2.9/5.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |
| F7 | CAT02 | 2.9BG 2.9/5.3 | dark bluish green | ❌ | dark bluish green | ❌ |  |

#### 143. Expected: very dark green
Hex: #0C2E24

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.0BG 1.6/3.1 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| C | Bradford | 2.9BG 1.6/3.0 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| C | CAT02 | 2.9BG 1.6/3.0 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| D65 | XYZScaling | 9.7G 1.6/3.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| D65 | Bradford | 9.7G 1.6/3.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| D65 | CAT02 | 9.7G 1.6/3.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| F7 | XYZScaling | 9.6G 1.6/3.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| F7 | Bradford | 9.6G 1.6/3.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |
| F7 | CAT02 | 9.6G 1.6/3.5 | very dark bluish green | ❌ | very dark bluish green | ❌ | ±0.1 |

#### 144. Expected: very pale green
Hex: #C7D9D6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.8B 8.5/1.1 | light bluish gray | ❌ | light bluish gray | ❌ | ±0.1 |
| C | Bradford | 3.7B 8.5/1.1 | light bluish gray | ❌ | light bluish gray | ❌ | ±0.1 |
| C | CAT02 | 3.7B 8.5/1.1 | light bluish gray | ❌ | light bluish gray | ❌ | ±0.1 |

#### 145. Expected: pale green
Hex: #94A6A3

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.8B 6.6/1.1 | light bluish gray | ❌ | light bluish gray | ❌ | ±0.1 |
| C | Bradford | 2.7B 6.6/1.1 | light bluish gray | ❌ | light bluish gray | ❌ | ±0.1 |
| C | CAT02 | 2.7B 6.6/1.1 | light bluish gray | ❌ | light bluish gray | ❌ | ±0.1 |

#### 146. Expected: grayish green
Hex: #61716E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.8B 4.5/1.0 | bluish gray | ❌ | bluish gray | ❌ | ±0.1 |
| C | Bradford | 1.8B 4.5/1.0 | bluish gray | ❌ | bluish gray | ❌ | ±0.1 |
| C | CAT02 | 1.8B 4.5/1.0 | bluish gray | ❌ | bluish gray | ❌ | ±0.1 |

#### 147. Expected: dark grayish green
Hex: #394746

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.7BG 2.9/1.1 | dark greenish gray | ❌ | dark greenish gray | ❌ |  |
| C | Bradford | 8.6BG 2.9/1.1 | dark greenish gray | ❌ | dark greenish gray | ❌ |  |
| C | CAT02 | 8.6BG 2.9/1.1 | dark greenish gray | ❌ | dark greenish gray | ❌ |  |

#### 148. Expected: blackish green
Hex: #1F2A2A - **All configurations matched**

#### 149. Expected: greenish white
Hex: #E0E2E5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.1PB 9.0/0.7 | purplish white | ❌ | purplish white | ❌ | ±0.1 |
| C | Bradford | 9.4PB 9.0/0.7 | purplish white | ❌ | purplish white | ❌ | ±0.1 |
| C | CAT02 | 9.3PB 9.0/0.7 | purplish white | ❌ | purplish white | ❌ | ±0.1 |

#### 150. Expected: light greenish gray
Hex: #BABEC1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.7B 7.6/0.6 | light bluish gray | ❌ | light bluish gray | ❌ |  |
| C | Bradford | 9.8B 7.6/0.6 | light bluish gray | ❌ | light bluish gray | ❌ |  |
| C | CAT02 | 9.5B 7.6/0.6 | light bluish gray | ❌ | light bluish gray | ❌ |  |

#### 151. Expected: greenish gray
Hex: #848888

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.7BG 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| C | Bradford | 9.4BG 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |
| C | CAT02 | 9.5BG 5.5/0.3 | medium gray | ❌ | medium gray | ❌ | ±0.1 |

#### 152. Expected: dark greenish gray
Hex: #545858

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.1BG 3.6/0.4 | dark gray | ❌ | dark gray | ❌ |  |
| C | Bradford | 7.9BG 3.6/0.3 | dark gray | ❌ | dark gray | ❌ |  |
| C | CAT02 | 7.9BG 3.6/0.3 | dark gray | ❌ | dark gray | ❌ |  |

#### 153. Expected: greenish black
Hex: #212626 - **All configurations matched**

#### 154. Expected: vivid bluish green
Hex: #13FCD5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.9B 8.9/8.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| C | Bradford | 1.9B 8.9/8.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| C | CAT02 | 1.9B 8.9/8.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 1.1B 8.9/9.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.1B 8.9/9.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.1B 8.9/9.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.1B 8.9/9.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.1B 8.9/9.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.1B 8.9/9.5 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |

#### 155. Expected: brilliant bluish green
Hex: #35D7CE

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.3B 7.8/7.4 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| C | Bradford | 1.2B 7.8/7.2 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| C | CAT02 | 1.2B 7.8/7.2 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ |  |
| D65 | XYZScaling | 3.1B 7.8/7.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 3.1B 7.8/7.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 3.1B 7.8/7.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 3.1B 7.8/7.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 3.1B 7.8/7.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 3.1B 7.8/7.1 | brilliant greenish blue | ❌ | brilliant greenish blue | ❌ | ±0.1 |

#### 156. Expected: strong bluish green
Hex: #0D8F82

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.6B 5.2/5.5 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| C | Bradford | 1.6B 5.2/5.3 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| C | CAT02 | 1.6B 5.2/5.3 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| D65 | XYZScaling | 0.3B 5.2/5.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| D65 | Bradford | 0.3B 5.2/5.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| D65 | CAT02 | 0.3B 5.2/5.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| F7 | XYZScaling | 0.3B 5.2/5.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 0.3B 5.2/5.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 0.3B 5.2/5.9 | moderate greenish blue | ❌ | moderate greenish blue | ❌ | ±0.1 |

#### 157. Expected: very light bluish green
Hex: #98E1E0

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.5B 8.5/4.3 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| C | Bradford | 1.5B 8.5/4.2 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| C | CAT02 | 1.5B 8.5/4.2 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 4.2B 8.5/4.1 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 4.2B 8.5/4.1 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 4.2B 8.5/4.1 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 4.3B 8.5/4.0 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 4.3B 8.5/4.0 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 4.3B 8.5/4.0 | very light greenish blue | ❌ | very light greenish blue | ❌ | ±0.1 |

#### 158. Expected: light bluish green
Hex: #5FABAB

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.2B 6.4/4.8 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| C | Bradford | 10.0BG 6.4/4.7 | light greenish blue | ❌ | light bluish green | ✅ | ±0.1 |
| C | CAT02 | 10.0BG 6.4/4.6 | light greenish blue | ❌ | light bluish green | ✅ | ±0.1 |
| D65 | XYZScaling | 1.8B 6.4/4.5 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 1.8B 6.4/4.5 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 1.8B 6.4/4.5 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 1.8B 6.4/4.5 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 1.8B 6.4/4.5 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 1.8B 6.4/4.5 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |

#### 159. Expected: moderate bluish green
Hex: #297A7B - **All configurations matched**

#### 160. Expected: dark bluish green
Hex: #154B4D - **All configurations matched**

#### 161. Expected: very dark bluish green
Hex: #0A2D2E - **All configurations matched**

#### 162. Expected: brilliant greenish blue
Hex: #2DBCE2 - **All configurations matched**

#### 163. Expected: strong greenish blue
Hex: #1385AF - **All configurations matched**

#### 164. Expected: very light greenish blue
Hex: #94D6EF - **All configurations matched**

#### 165. Expected: light greenish blue
Hex: #65A8C3 - **All configurations matched**

#### 166. Expected: moderate greenish blue
Hex: #2A7691 - **All configurations matched**

#### 167. Expected: dark greenish blue
Hex: #134A60 - **All configurations matched**

#### 168. Expected: very dark greenish blue
Hex: #0B2C3B - **All configurations matched**

#### 169. Expected: vivid blue
Hex: #1B5CD7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.7B 4.2/14.1 | vivid greenish blue | ❌ | vivid greenish blue | ❌ | ±0.1 |

#### 170. Expected: brilliant blue
Hex: #419DED - **All configurations matched**

#### 171. Expected: strong blue
Hex: #276CBD - **All configurations matched**

#### 172. Expected: deep blue
Hex: #113074 - **All configurations matched**

#### 173. Expected: very light blue
Hex: #99C6F9 - **All configurations matched**

#### 174. Expected: light blue
Hex: #73A4DC - **All configurations matched**

#### 175. Expected: moderate blue
Hex: #34689E - **All configurations matched**

#### 176. Expected: dark blue
Hex: #173459

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.9B 2.1/5.6 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| C | Bradford | 7.7B 2.1/5.5 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| C | CAT02 | 7.6B 2.1/5.5 | dark greenish blue | ❌ | dark greenish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 5.8B 2.1/5.2 | dark greenish blue | ❌ | dark greenish blue | ❌ |  |
| D65 | Bradford | 5.8B 2.1/5.2 | dark greenish blue | ❌ | dark greenish blue | ❌ |  |
| D65 | CAT02 | 5.8B 2.1/5.2 | dark greenish blue | ❌ | dark greenish blue | ❌ |  |
| F7 | XYZScaling | 5.8B 2.1/5.2 | dark greenish blue | ❌ | dark greenish blue | ❌ |  |
| F7 | Bradford | 5.8B 2.1/5.2 | dark greenish blue | ❌ | dark greenish blue | ❌ |  |
| F7 | CAT02 | 5.8B 2.1/5.2 | dark greenish blue | ❌ | dark greenish blue | ❌ |  |

#### 177. Expected: very pale blue
Hex: #C2D2EC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9PB 8.3/4.2 | very pale purplish blue | ❌ | very pale purplish blue | ❌ |  |
| C | Bradford | 8.2PB 8.3/4.2 | very pale violet | ❌ | very pale purplish blue | ❌ |  |
| C | CAT02 | 8.2PB 8.3/4.2 | very pale violet | ❌ | very pale purplish blue | ❌ |  |

#### 178. Expected: pale blue
Hex: #91A2BB

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.9PB 6.5/4.2 | pale purplish blue | ❌ | pale purplish blue | ❌ | ±0.1 |
| C | Bradford | 6.3PB 6.5/4.2 | pale purplish blue | ❌ | pale purplish blue | ❌ | ±0.1 |
| C | CAT02 | 6.2PB 6.5/4.1 | pale purplish blue | ❌ | pale purplish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 7.6B 6.5/3.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | Bradford | 7.6B 6.5/3.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| D65 | CAT02 | 7.6B 6.5/3.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 7.4B 6.5/3.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | Bradford | 7.4B 6.5/3.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |
| F7 | CAT02 | 7.4B 6.5/3.0 | light greenish blue | ❌ | light greenish blue | ❌ | ±0.1 |

#### 179. Expected: grayish blue
Hex: #54687F

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| D65 | XYZScaling | 4.6B 4.2/3.1 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| D65 | Bradford | 4.6B 4.2/3.1 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| D65 | CAT02 | 4.6B 4.2/3.1 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| F7 | XYZScaling | 4.6B 4.2/3.1 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| F7 | Bradford | 4.6B 4.2/3.1 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |
| F7 | CAT02 | 4.6B 4.2/3.1 | moderate greenish blue | ❌ | moderate greenish blue | ❌ |  |

#### 180. Expected: dark grayish blue
Hex: #323F4E - **All configurations matched**

#### 181. Expected: blackish blue
Hex: #1E2531 - **All configurations matched**

#### 182. Expected: bluish white
Hex: #E1E1F1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.1P 9.0/2.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | Bradford | 3.3P 9.0/2.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | CAT02 | 3.2P 9.0/2.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 183. Expected: light bluish gray
Hex: #B7B8C6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.9P 7.4/2.5 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| C | Bradford | 2.1P 7.4/2.5 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| C | CAT02 | 2.0P 7.4/2.5 | pale purple | ❌ | pale purple | ❌ | ±0.1 |

#### 184. Expected: bluish gray
Hex: #838793

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.2PB 5.5/1.9 | pale purple | ❌ | pale blue | ❌ | ±0.1 |
| C | Bradford | 8.4PB 5.5/1.9 | pale purple | ❌ | pale blue | ❌ | ±0.1 |
| C | CAT02 | 8.4PB 5.5/1.9 | pale purple | ❌ | pale blue | ❌ | ±0.1 |

#### 185. Expected: dark bluish gray
Hex: #50545F - **All configurations matched**

#### 186. Expected: bluish black
Hex: #24272E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9B 1.5/1.0 | blackish blue | ❌ | blackish blue | ❌ | ±0.1 |

#### 187. Expected: vivid purplish blue
Hex: #4436D1

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.0P 3.4/27.7 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| C | Bradford | 0.3PB 3.5/13.9 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| C | CAT02 | 0.2PB 3.5/13.8 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| D65 | XYZScaling | 0.2PB 3.4/13.3 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| D65 | Bradford | 0.2PB 3.4/13.3 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| D65 | CAT02 | 0.2PB 3.4/13.3 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| F7 | XYZScaling | 0.2PB 3.4/13.3 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| F7 | Bradford | 0.2PB 3.4/13.3 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |
| F7 | CAT02 | 0.2PB 3.4/13.3 | vivid blue | ❌ | vivid blue | ❌ | ±0.1 |

#### 188. Expected: brilliant purplish blue
Hex: #8088E2

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.7PB 5.9/11.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| C | Bradford | 6.8PB 5.9/11.4 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| C | CAT02 | 6.9PB 5.9/11.4 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| D65 | XYZScaling | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| D65 | Bradford | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| D65 | CAT02 | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| F7 | XYZScaling | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| F7 | Bradford | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |
| F7 | CAT02 | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ | ±0.1 |

#### 189. Expected: strong purplish blue
Hex: #5359B5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.7P 4.1/15.9 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| C | Bradford | 1.4P 4.1/16.5 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| C | CAT02 | 1.4P 4.1/16.3 | vivid violet | ❌ | vivid violet | ❌ |  |
| D65 | XYZScaling | 0.8P 4.1/14.4 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| D65 | Bradford | 0.8P 4.1/14.4 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| D65 | CAT02 | 0.8P 4.1/14.4 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| F7 | XYZScaling | 0.8P 4.1/14.4 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| F7 | Bradford | 0.8P 4.1/14.3 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |
| F7 | CAT02 | 0.8P 4.1/14.3 | vivid violet | ❌ | vivid violet | ❌ | ±0.1 |

#### 190. Expected: deep purplish blue
Hex: #2A286F - **All configurations matched**

#### 191. Expected: very light purplish blue
Hex: #B7C0F8

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 0.2P 7.8/7.7 | very light violet | ❌ | very light violet | ❌ |  |
| C | Bradford | 0.6P 7.8/7.7 | very light violet | ❌ | very light violet | ❌ |  |
| C | CAT02 | 0.5P 7.8/7.7 | very light violet | ❌ | very light violet | ❌ |  |
| D65 | XYZScaling | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |  |
| D65 | Bradford | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |  |
| D65 | CAT02 | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |  |
| F7 | XYZScaling | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |  |
| F7 | Bradford | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |  |
| F7 | CAT02 | 8.7PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |  |

#### 192. Expected: light purplish blue
Hex: #8991CB - **All configurations matched**

#### 193. Expected: moderate purplish blue
Hex: #4D4E87

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.2P 3.5/9.2 | strong violet | ❌ | strong violet | ❌ | ±0.1 |
| C | Bradford | 1.9P 3.5/9.4 | strong violet | ❌ | strong violet | ❌ | ±0.1 |
| C | CAT02 | 1.8P 3.5/9.4 | strong violet | ❌ | strong violet | ❌ | ±0.1 |
| D65 | XYZScaling | 1.1P 3.5/8.0 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |
| D65 | Bradford | 1.1P 3.5/8.0 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |
| D65 | CAT02 | 1.1P 3.5/8.0 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |
| F7 | XYZScaling | 1.1P 3.5/7.9 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |
| F7 | Bradford | 1.1P 3.5/7.9 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |
| F7 | CAT02 | 1.0P 3.5/7.9 | moderate violet | ❌ | moderate violet | ❌ | ±0.1 |

#### 194. Expected: dark purplish blue
Hex: #222248

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8PB 1.5/5.1 | dark blue | ❌ | dark blue | ❌ | ±0.1 |

#### 195. Expected: very pale purplish blue
Hex: #C5C9F0

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.3P 8.1/5.7 | very light violet | ❌ | very light violet | ❌ |  |
| C | Bradford | 1.5P 8.1/5.7 | very light violet | ❌ | very light violet | ❌ |  |
| C | CAT02 | 1.5P 8.1/5.7 | very light violet | ❌ | very light violet | ❌ |  |
| D65 | XYZScaling | 9.2PB 8.1/4.3 | very pale violet | ❌ | very pale violet | ❌ |  |
| D65 | Bradford | 9.2PB 8.1/4.3 | very pale violet | ❌ | very pale violet | ❌ |  |
| D65 | CAT02 | 9.2PB 8.1/4.3 | very pale violet | ❌ | very pale violet | ❌ |  |
| F7 | XYZScaling | 9.2PB 8.1/4.3 | very pale violet | ❌ | very pale violet | ❌ |  |
| F7 | Bradford | 9.2PB 8.1/4.3 | very pale violet | ❌ | very pale violet | ❌ |  |
| F7 | CAT02 | 9.2PB 8.1/4.3 | very pale violet | ❌ | very pale violet | ❌ |  |

#### 196. Expected: pale purplish blue
Hex: #8E92B7

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.4PB 6.0/5.5 | light violet | ❌ | light violet | ❌ | ±0.1 |
| C | Bradford | 9.5PB 6.0/5.5 | light violet | ❌ | light violet | ❌ | ±0.1 |
| C | CAT02 | 9.6PB 6.0/5.4 | light violet | ❌ | light violet | ❌ | ±0.1 |
| D65 | XYZScaling | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |
| D65 | Bradford | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |
| D65 | CAT02 | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |
| F7 | XYZScaling | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |
| F7 | Bradford | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |
| F7 | CAT02 | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ | ±0.1 |

#### 197. Expected: grayish purplish blue
Hex: #494D71

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.0PB 3.3/4.3 | grayish blue | ❌ | grayish blue | ❌ |  |
| C | Bradford | 2.3PB 3.3/4.2 | grayish blue | ❌ | grayish blue | ❌ |  |
| C | CAT02 | 2.3PB 3.3/4.2 | grayish blue | ❌ | grayish blue | ❌ |  |
| D65 | XYZScaling | 2.0PB 3.3/3.7 | grayish blue | ❌ | grayish blue | ❌ |  |
| D65 | Bradford | 2.0PB 3.3/3.7 | grayish blue | ❌ | grayish blue | ❌ |  |
| D65 | CAT02 | 2.0PB 3.3/3.7 | grayish blue | ❌ | grayish blue | ❌ |  |
| F7 | XYZScaling | 2.1PB 3.3/3.7 | grayish blue | ❌ | grayish blue | ❌ |  |
| F7 | Bradford | 2.0PB 3.3/3.7 | grayish blue | ❌ | grayish blue | ❌ |  |
| F7 | CAT02 | 2.0PB 3.3/3.7 | grayish blue | ❌ | grayish blue | ❌ |  |

#### 198. Expected: vivid violet
Hex: #7931D3

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.2PB 3.9/14.9 | vivid purplish blue | ❌ | vivid blue | ❌ | ±0.1 |
| C | Bradford | 6.4PB 3.9/15.1 | vivid purplish blue | ❌ | vivid blue | ❌ | ±0.1 |
| C | CAT02 | 6.4PB 3.9/15.0 | vivid purplish blue | ❌ | vivid blue | ❌ | ±0.1 |
| D65 | XYZScaling | 6.9PB 3.9/14.6 | vivid purplish blue | ❌ | vivid blue | ❌ |  |
| D65 | Bradford | 6.9PB 3.9/14.6 | vivid purplish blue | ❌ | vivid blue | ❌ |  |
| D65 | CAT02 | 6.9PB 3.9/14.6 | vivid purplish blue | ❌ | vivid blue | ❌ |  |
| F7 | XYZScaling | 7.0PB 3.9/14.7 | vivid purplish blue | ❌ | vivid blue | ❌ |  |
| F7 | Bradford | 7.0PB 3.9/14.6 | vivid purplish blue | ❌ | vivid blue | ❌ |  |
| F7 | CAT02 | 7.0PB 3.9/14.6 | vivid purplish blue | ❌ | vivid blue | ❌ |  |

#### 199. Expected: brilliant violet
Hex: #987FDC

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8PB 5.8/10.6 | brilliant purplish blue | ❌ | brilliant blue | ❌ | ±0.1 |
| C | Bradford | 6.9PB 5.8/10.5 | brilliant purplish blue | ❌ | brilliant blue | ❌ | ±0.1 |
| C | CAT02 | 7.0PB 5.8/10.5 | brilliant purplish blue | ❌ | brilliant blue | ❌ | ±0.1 |
| D65 | XYZScaling | 7.6PB 5.8/9.8 | brilliant purplish blue | ❌ | brilliant purplish blue | ❌ |  |
| D65 | Bradford | 7.6PB 5.8/9.8 | brilliant purplish blue | ❌ | brilliant purplish blue | ❌ |  |
| D65 | CAT02 | 7.6PB 5.8/9.8 | brilliant purplish blue | ❌ | brilliant purplish blue | ❌ |  |
| F7 | XYZScaling | 7.7PB 5.8/9.8 | brilliant purplish blue | ❌ | brilliant purplish blue | ❌ |  |
| F7 | Bradford | 7.7PB 5.8/9.8 | brilliant purplish blue | ❌ | brilliant purplish blue | ❌ |  |
| F7 | CAT02 | 7.7PB 5.8/9.8 | brilliant purplish blue | ❌ | brilliant purplish blue | ❌ |  |

#### 200. Expected: strong violet
Hex: #61419C

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.7PB 3.5/9.3 | strong blue | ❌ | strong blue | ❌ | ±0.1 |
| C | Bradford | 6.0PB 3.5/9.3 | strong blue | ❌ | strong blue | ❌ | ±0.1 |
| C | CAT02 | 6.0PB 3.5/9.3 | strong blue | ❌ | strong blue | ❌ | ±0.1 |
| D65 | XYZScaling | 6.3PB 3.5/8.7 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | Bradford | 6.3PB 3.5/8.7 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | CAT02 | 6.3PB 3.5/8.7 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | XYZScaling | 6.4PB 3.5/8.7 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | Bradford | 6.3PB 3.5/8.7 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | CAT02 | 6.3PB 3.5/8.7 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |

#### 201. Expected: deep violet
Hex: #3C1668

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.9PB 1.8/9.1 | deep purplish blue | ❌ | deep purplish blue | ❌ | ±0.1 |
| C | Bradford | 8.2PB 1.8/9.2 | deep violet | ✅ | deep purplish blue | ❌ |  |
| C | CAT02 | 8.1PB 1.8/9.0 | deep violet | ✅ | deep purplish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 9.0PB 1.8/9.1 | deep violet | ✅ | deep purplish blue | ❌ | ±0.1 |
| D65 | Bradford | 9.0PB 1.8/9.1 | deep violet | ✅ | deep purplish blue | ❌ | ±0.1 |
| D65 | CAT02 | 9.0PB 1.8/9.1 | deep violet | ✅ | deep purplish blue | ❌ | ±0.1 |
| F7 | Bradford | 9.0PB 1.8/9.1 | deep violet | ✅ | deep purplish blue | ❌ | ±0.1 |
| F7 | CAT02 | 9.0PB 1.8/9.1 | deep violet | ✅ | deep purplish blue | ❌ | ±0.1 |

#### 202. Expected: very light violet
Hex: #C9BAF8

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.4P 7.8/8.2 | very light purple | ❌ | very light violet | ✅ |  |
| C | Bradford | 2.5P 7.8/8.2 | very light purple | ❌ | very light violet | ✅ |  |
| C | CAT02 | 2.5P 7.8/8.1 | very light purple | ❌ | very light violet | ✅ |  |
| D65 | XYZScaling | 2.6P 7.8/7.0 | very light purple | ❌ | very light violet | ✅ | ±0.1 |
| D65 | Bradford | 2.6P 7.8/7.0 | very light purple | ❌ | very light violet | ✅ | ±0.1 |
| D65 | CAT02 | 2.6P 7.8/7.0 | very light purple | ❌ | very light violet | ✅ | ±0.1 |
| F7 | XYZScaling | 2.6P 7.8/6.9 | very light purple | ❌ | very light violet | ✅ | ±0.1 |
| F7 | Bradford | 2.6P 7.8/6.9 | very light purple | ❌ | very light violet | ✅ | ±0.1 |
| F7 | CAT02 | 2.6P 7.8/6.9 | very light purple | ❌ | very light violet | ✅ | ±0.1 |

#### 203. Expected: light violet
Hex: #9B8CCA - **All configurations matched**

#### 204. Expected: moderate violet
Hex: #5C4985

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.8PB 3.5/6.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| C | Bradford | 6.1PB 3.5/6.4 | moderate purplish blue | ❌ | moderate blue | ❌ | ±0.1 |
| C | CAT02 | 6.0PB 3.5/6.4 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | XYZScaling | 5.9PB 3.5/5.7 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | Bradford | 5.9PB 3.5/5.7 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| D65 | CAT02 | 5.9PB 3.5/5.7 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | XYZScaling | 6.0PB 3.5/5.7 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | Bradford | 6.0PB 3.5/5.7 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |
| F7 | CAT02 | 6.0PB 3.5/5.7 | moderate blue | ❌ | moderate blue | ❌ | ±0.1 |

#### 205. Expected: dark violet
Hex: #34254D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 7.5PB 1.8/4.6 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| C | Bradford | 7.8PB 1.8/4.7 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| C | CAT02 | 7.7PB 1.8/4.6 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| D65 | XYZScaling | 7.9PB 1.8/4.2 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| D65 | Bradford | 7.9PB 1.8/4.2 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| D65 | CAT02 | 7.9PB 1.8/4.2 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| F7 | XYZScaling | 8.0PB 1.8/4.2 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| F7 | Bradford | 7.9PB 1.8/4.2 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |
| F7 | CAT02 | 7.9PB 1.8/4.2 | dark purplish blue | ❌ | dark purplish blue | ❌ |  |

#### 206. Expected: very pale violet
Hex: #D0C6EF

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.7P 8.1/6.0 | very light purple | ❌ | very light purple | ❌ | ±0.1 |
| C | Bradford | 3.8P 8.1/5.9 | very light purple | ❌ | very light purple | ❌ | ±0.1 |
| C | CAT02 | 3.8P 8.1/5.9 | very light purple | ❌ | very light purple | ❌ | ±0.1 |
| D65 | XYZScaling | 3.2P 8.1/4.5 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| D65 | Bradford | 3.2P 8.1/4.5 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| D65 | CAT02 | 3.2P 8.1/4.5 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | XYZScaling | 3.2P 8.1/4.4 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | Bradford | 3.2P 8.1/4.4 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| F7 | CAT02 | 3.2P 8.1/4.4 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 207. Expected: pale violet
Hex: #9A90B5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.5P 6.1/5.2 | light violet | ❌ | light violet | ❌ | ±0.1 |
| C | Bradford | 1.6P 6.1/5.2 | light violet | ❌ | light violet | ❌ | ±0.1 |
| C | CAT02 | 1.6P 6.1/5.2 | light violet | ❌ | light violet | ❌ | ±0.1 |

#### 208. Expected: grayish violet
Hex: #584E72

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 5.4PB 3.5/3.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| C | Bradford | 5.7PB 3.5/3.9 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| C | CAT02 | 5.6PB 3.5/3.8 | grayish purplish blue | ❌ | grayish purplish blue | ❌ | ±0.1 |
| D65 | XYZScaling | 4.8PB 3.5/3.2 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | Bradford | 4.8PB 3.5/3.2 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| D65 | CAT02 | 4.8PB 3.5/3.2 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | XYZScaling | 4.8PB 3.5/3.2 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | Bradford | 4.8PB 3.5/3.2 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |
| F7 | CAT02 | 4.8PB 3.5/3.2 | grayish blue | ❌ | grayish blue | ❌ | ±0.1 |

#### 209. Expected: vivid purple
Hex: #B935D5 - **All configurations matched**

#### 210. Expected: brilliant purple
Hex: #CE8CE3 - **All configurations matched**

#### 211. Expected: strong purple
Hex: #9352A8 - **All configurations matched**

#### 212. Expected: deep purple
Hex: #652277 - **All configurations matched**

#### 213. Expected: very deep purple
Hex: #460A55 - **All configurations matched**

#### 214. Expected: very light purple
Hex: #E4B9F3 - **All configurations matched**

#### 215. Expected: light purple
Hex: #BC93CC - **All configurations matched**

#### 216. Expected: moderate purple
Hex: #875E96 - **All configurations matched**

#### 217. Expected: dark purple
Hex: #563762 - **All configurations matched**

#### 218. Expected: very dark purple
Hex: #371B41 - **All configurations matched**

#### 219. Expected: very pale purple
Hex: #E0CBEB - **All configurations matched**

#### 220. Expected: pale purple
Hex: #AD97B3

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.2P 6.4/4.5 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | Bradford | 6.1P 6.4/4.4 | N/A | ❌ | N/A | ❌ | ±0.1 |
| C | CAT02 | 6.1P 6.4/4.4 | N/A | ❌ | N/A | ❌ | ±0.1 |
| D65 | XYZScaling | 6.7P 6.4/3.2 | N/A | ❌ | N/A | ❌ | ±0.1 |
| D65 | Bradford | 6.7P 6.4/3.2 | N/A | ❌ | N/A | ❌ | ±0.1 |
| D65 | CAT02 | 6.7P 6.4/3.2 | N/A | ❌ | N/A | ❌ | ±0.1 |
| F7 | XYZScaling | 6.7P 6.4/3.1 | N/A | ❌ | N/A | ❌ | ±0.1 |
| F7 | Bradford | 6.7P 6.4/3.1 | N/A | ❌ | N/A | ❌ | ±0.1 |
| F7 | CAT02 | 6.7P 6.4/3.1 | N/A | ❌ | N/A | ❌ | ±0.1 |

#### 221. Expected: grayish purple
Hex: #7B667E - **All configurations matched**

#### 222. Expected: dark grayish purple
Hex: #513F51 - **All configurations matched**

#### 223. Expected: blackish purple
Hex: #2F2231 - **All configurations matched**

#### 224. Expected: purplish white
Hex: #EBDFEF

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.3P 9.0/2.9 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | Bradford | 6.3P 9.0/2.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | CAT02 | 6.3P 9.0/2.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 225. Expected: light purplish gray
Hex: #C3B7C6

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.4P 7.5/2.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | Bradford | 6.4P 7.5/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | CAT02 | 6.4P 7.5/2.7 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 226. Expected: purplish gray
Hex: #8F8490

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.9P 5.5/2.0 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| C | Bradford | 6.9P 5.5/2.0 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| C | CAT02 | 6.9P 5.5/2.0 | pale purple | ❌ | pale purple | ❌ | ±0.1 |

#### 227. Expected: dark purplish gray
Hex: #5C525E

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.8P 3.6/1.6 | grayish purple | ❌ | grayish purple | ❌ | ±0.1 |
| C | Bradford | 6.8P 3.6/1.5 | grayish purple | ❌ | grayish purple | ❌ | ±0.1 |
| C | CAT02 | 6.8P 3.6/1.5 | grayish purple | ❌ | grayish purple | ❌ | ±0.1 |

#### 228. Expected: purplish black
Hex: #2B2630

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.6P 1.6/1.3 | blackish purple | ❌ | blackish purple | ❌ | ±0.1 |
| C | Bradford | 4.8P 1.6/1.3 | blackish purple | ❌ | blackish purple | ❌ | ±0.1 |
| C | CAT02 | 4.7P 1.6/1.3 | blackish purple | ❌ | blackish purple | ❌ | ±0.1 |

#### 229. Expected: vivid reddish purple
Hex: #D429B9 - **All configurations matched**

#### 230. Expected: strong reddish purple
Hex: #A74994 - **All configurations matched**

#### 231. Expected: deep reddish purple
Hex: #761A6A - **All configurations matched**

#### 232. Expected: very deep reddish purple
Hex: #4F094A - **All configurations matched**

#### 233. Expected: light reddish purple
Hex: #BD80AE - **All configurations matched**

#### 234. Expected: moderate reddish purple
Hex: #965888 - **All configurations matched**

#### 235. Expected: dark reddish purple
Hex: #5F3458 - **All configurations matched**

#### 236. Expected: very dark reddish purple
Hex: #3F183C - **All configurations matched**

#### 237. Expected: pale reddish purple
Hex: #AD89A5

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 9.6P 6.0/5.2 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| C | Bradford | 9.5P 6.0/5.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| C | CAT02 | 9.5P 6.0/5.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |

#### 238. Expected: grayish reddish purple
Hex: #86627E - **All configurations matched**

#### 239. Expected: brilliant purplish pink
Hex: #FCA1E7 - **All configurations matched**

#### 240. Expected: strong purplish pink
Hex: #F483CD - **All configurations matched**

#### 241. Expected: deep purplish pink
Hex: #DF6AAC - **All configurations matched**

#### 242. Expected: light purplish pink
Hex: #F5B2DB - **All configurations matched**

#### 243. Expected: moderate purplish pink
Hex: #DE98BF - **All configurations matched**

#### 244. Expected: dark purplish pink
Hex: #C67D9D

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.0RP 6.0/8.8 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| C | Bradford | 2.0RP 6.0/8.5 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| C | CAT02 | 2.0RP 6.0/8.5 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| D65 | XYZScaling | 3.0RP 6.0/8.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| D65 | Bradford | 3.0RP 6.0/8.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| D65 | CAT02 | 3.0RP 6.0/8.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| F7 | XYZScaling | 3.0RP 6.0/8.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| F7 | Bradford | 3.0RP 6.0/8.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| F7 | CAT02 | 3.0RP 6.0/8.1 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |

#### 245. Expected: pale purplish pink
Hex: #EBC8DF - **All configurations matched**

#### 246. Expected: grayish purplish pink
Hex: #C7A3B9 - **All configurations matched**

#### 247. Expected: vivid purplish red
Hex: #DD2388

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.8RP 4.9/22.1 | vivid purplish red | ✅ | vivid reddish purple | ❌ | ±0.1 |
| C | Bradford | 2.8RP 4.9/21.3 | vivid purplish red | ✅ | vivid reddish purple | ❌ | ±0.1 |
| C | CAT02 | 2.8RP 4.9/21.2 | vivid purplish red | ✅ | vivid reddish purple | ❌ | ±0.1 |

#### 248. Expected: strong purplish red
Hex: #B83773

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.5RP 4.4/15.5 | vivid purplish red | ❌ | vivid purplish red | ❌ | ±0.1 |
| C | Bradford | 3.5RP 4.4/14.9 | vivid purplish red | ❌ | vivid purplish red | ❌ | ±0.1 |
| C | CAT02 | 3.5RP 4.4/14.8 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |
| D65 | XYZScaling | 4.2RP 4.4/14.6 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |
| D65 | Bradford | 4.2RP 4.4/14.6 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |
| D65 | CAT02 | 4.2RP 4.4/14.6 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |
| F7 | XYZScaling | 4.2RP 4.4/14.6 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |
| F7 | Bradford | 4.2RP 4.4/14.6 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |
| F7 | CAT02 | 4.2RP 4.4/14.6 | vivid purplish red | ❌ | vivid purplish red | ❌ |  |

#### 249. Expected: deep purplish red
Hex: #881055

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 4.0RP 3.0/13.1 | vivid purplish red | ❌ | vivid purplish red | ❌ | ±0.1 |

#### 250. Expected: very deep purplish red
Hex: #54063C - **All configurations matched**

#### 251. Expected: moderate purplish red
Hex: #AB4B74

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 3.3RP 4.5/11.6 | strong purplish red | ❌ | strong purplish red | ❌ | ±0.1 |
| C | Bradford | 3.3RP 4.5/11.2 | strong purplish red | ❌ | strong purplish red | ❌ | ±0.1 |
| C | CAT02 | 3.3RP 4.5/11.2 | strong purplish red | ❌ | strong purplish red | ❌ | ±0.1 |

#### 252. Expected: dark purplish red
Hex: #6E294C - **All configurations matched**

#### 253. Expected: very dark purplish red
Hex: #431432 - **All configurations matched**

#### 254. Expected: light grayish purplish red
Hex: #B2879B

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 1.6RP 6.0/5.2 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| C | Bradford | 1.6RP 6.0/5.0 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| C | CAT02 | 1.6RP 6.0/5.0 | light reddish purple | ❌ | light reddish purple | ❌ | ±0.1 |
| D65 | XYZScaling | 3.0RP 6.0/4.5 | pale reddish purple | ❌ | pale reddish purple | ❌ | ±0.1 |
| D65 | Bradford | 3.0RP 6.0/4.5 | pale reddish purple | ❌ | pale reddish purple | ❌ | ±0.1 |
| D65 | CAT02 | 3.0RP 6.0/4.5 | pale reddish purple | ❌ | pale reddish purple | ❌ | ±0.1 |

#### 255. Expected: grayish purplish red
Hex: #945C73

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 2.8RP 4.5/6.4 | grayish purplish red | ✅ | moderate reddish purple | ❌ | ±0.1 |
| C | Bradford | 2.8RP 4.5/6.2 | grayish purplish red | ✅ | moderate reddish purple | ❌ | ±0.1 |
| C | CAT02 | 2.8RP 4.5/6.2 | grayish purplish red | ✅ | moderate reddish purple | ❌ | ±0.1 |

#### 256. Expected: white
Hex: #E7E1E9

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.3P 9.0/1.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | Bradford | 6.3P 9.0/1.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |
| C | CAT02 | 6.3P 9.0/1.8 | very pale purple | ❌ | very pale purple | ❌ | ±0.1 |

#### 257. Expected: light gray
Hex: #BDB7BF

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 6.2P 7.4/1.6 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| C | Bradford | 6.1P 7.4/1.6 | pale purple | ❌ | pale purple | ❌ | ±0.1 |
| C | CAT02 | 6.1P 7.4/1.6 | pale purple | ❌ | pale purple | ❌ | ±0.1 |

#### 258. Expected: medium gray
Hex: #8A8489

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.9P 5.5/1.0 | purplish gray | ❌ | purplish gray | ❌ | ±0.1 |
| C | Bradford | 8.8P 5.5/0.9 | purplish gray | ❌ | purplish gray | ❌ | ±0.1 |
| C | CAT02 | 8.8P 5.5/0.9 | purplish gray | ❌ | purplish gray | ❌ | ±0.1 |

#### 259. Expected: dark gray
Hex: #585458

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ | Boundary |
|------------|------------|---------|----------|-----|----------|-----|----------|
| C | XYZScaling | 8.2P 3.6/0.6 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| C | Bradford | 8.1P 3.6/0.6 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |
| C | CAT02 | 8.1P 3.6/0.6 | dark purplish gray | ❌ | dark purplish gray | ❌ | ±0.1 |

#### 260. Expected: black
Hex: #2B292B - **All configurations matched**

## Pattern Analysis

### W3 Dataset Patterns

#### Boundary Analysis
- Total mismatches: 1568
- Near boundary (±0.1): 1140 (72.7%)

#### Family Analysis

| Family | Expected Count | Found Count | Accuracy |
|--------|---------------|-------------|----------|
| PB | 169 | 0 | 0.0% |
| P | 156 | 96 | 0.0% |
| R | 266 | 102 | 0.0% |
| Y | 235 | 344 | 0.0% |
| YR | 250 | 162 | 0.0% |
| BG | 204 | 249 | 0.0% |
| RP | 259 | 45 | 0.0% |
| G | 158 | 603 | 0.0% |
| GY | 467 | 703 | 0.0% |
| B | 233 | 224 | 0.0% |
| N | 6 | 0 | 0.0% |

#### Modifier Analysis

| Modifier | Expected Count | Correct Count | Accuracy |
|----------|---------------|---------------|----------|
| strong | 207 | 248 | 119.8% |
| -ish white | 45 | 0 | 0.0% |
| grayish | 180 | 225 | 125.0% |
| strong yellowish | 9 | 0 | 0.0% |
| very deep | 45 | 0 | 0.0% |
| blackish | 36 | 54 | 150.0% |
| -ish black | 54 | 0 | 0.0% |
| brilliant | 126 | 150 | 119.0% |
| -ish gray | 72 | 0 | 0.0% |
| light -ish gray | 45 | 0 | 0.0% |
| dark | 225 | 332 | 147.6% |
| very light | 72 | 0 | 0.0% |
| vivid | 171 | 168 | 98.2% |
| pale | 171 | 144 | 84.2% |
| light | 207 | 279 | 134.8% |
| dark -ish gray | 36 | 0 | 0.0% |
| very dark | 72 | 0 | 0.0% |
| very pale | 45 | 0 | 0.0% |
| dark grayish | 90 | 0 | 0.0% |
| medium | 9 | 6 | 66.7% |
| moderate | 234 | 390 | 166.7% |
| deep | 216 | 230 | 106.5% |
| brownish | 18 | 3 | 16.7% |

#### Color Name Analysis

| Color | Expected Count | Correct Count | Accuracy |
|-------|---------------|---------------|----------|
| violet | 99 | 60 | 60.6% |
| brown | 99 | 162 | 163.6% |
| white | 9 | 18 | 200.0% |
| pink | 99 | 126 | 127.3% |
| bluish green | 81 | 64 | 79.0% |
| blue | 162 | 234 | 144.4% |
| green | 180 | 342 | 190.0% |
| purplish red | 63 | 114 | 181.0% |
| yellowish brown | 72 | 2 | 2.8% |
| greenish yellow | 81 | 2 | 2.5% |
| greenish blue | 81 | 144 | 177.8% |
| purple | 171 | 252 | 147.4% |
| olive green | 54 | 54 | 100.0% |
| purplish black | 9 | 0 | 0.0% |
| grey | 9 | 0 | 0.0% |
| orange yellow | 72 | 0 | 0.0% |
| red | 126 | 228 | 181.0% |
| olive brown | 27 | 0 | 0.0% |
| olive | 81 | 108 | 133.3% |
| gray | 18 | 24 | 133.3% |
| yellowish green | 81 | 121 | 149.4% |
| reddish purple | 90 | 180 | 200.0% |
| purplish pink | 90 | 92 | 102.2% |
| yellow | 108 | 210 | 194.4% |
| reddish orange | 54 | 96 | 177.8% |
| reddish brown | 72 | 86 | 119.4% |
| orange | 63 | 111 | 176.2% |
| chartreuse | 72 | 0 | 0.0% |
| black | 9 | 12 | 133.3% |
| yellowish pink | 72 | 73 | 101.4% |
| purplish blue | 99 | 65 | 65.7% |

### Centore Dataset Patterns

#### Boundary Analysis
- Total mismatches: 1065
- Near boundary (±0.1): 787 (73.9%)

#### Family Analysis

| Family | Expected Count | Found Count | Accuracy |
|--------|---------------|-------------|----------|
| R | 308 | 81 | 0.0% |
| P | 274 | 102 | 0.0% |
| PB | 204 | 0 | 0.0% |
| BG | 149 | 138 | 0.0% |
| G | 120 | 245 | 0.0% |
| RP | 263 | 42 | 0.0% |
| YR | 246 | 73 | 0.0% |
| Y | 187 | 211 | 0.0% |
| GY | 376 | 526 | 0.0% |
| B | 213 | 177 | 0.0% |

#### Modifier Analysis

| Modifier | Expected Count | Correct Count | Accuracy |
|----------|---------------|---------------|----------|
| moderate | 234 | 408 | 174.4% |
| medium | 9 | 12 | 133.3% |
| reddish | 18 | 24 | 133.3% |
| blackish | 36 | 72 | 200.0% |
| deep | 180 | 310 | 172.2% |
| bluish | 27 | 40 | 148.1% |
| pinkish | 18 | 24 | 133.3% |
| vivid | 153 | 264 | 172.5% |
| pale | 117 | 130 | 111.1% |
| light | 306 | 456 | 149.0% |
| dark | 351 | 620 | 176.6% |
| brilliant | 117 | 222 | 189.7% |
| grayish | 180 | 264 | 146.7% |
| purplish | 27 | 36 | 133.3% |
| strong | 216 | 305 | 141.2% |
| yellowish | 18 | 17 | 94.4% |
| greenish | 27 | 42 | 155.6% |
| very | 234 | 462 | 197.4% |
| brownish | 36 | 36 | 100.0% |
| olive | 18 | 36 | 200.0% |

#### Color Name Analysis

| Color | Expected Count | Correct Count | Accuracy |
|-------|---------------|---------------|----------|
| grayish reddish brown | 18 | 30 | 166.7% |
| dark greenish blue | 9 | 18 | 200.0% |
| deep purplish red | 9 | 18 | 200.0% |
| brownish gray | 9 | 12 | 133.3% |
| white | 54 | 82 | 151.9% |
| pale purplish blue | 9 | 0 | 0.0% |
| light violet | 9 | 9 | 100.0% |
| grayish red | 18 | 26 | 144.4% |
| yellowish pink | 72 | 109 | 151.4% |
| yellowish green | 63 | 84 | 133.3% |
| dark purple | 9 | 18 | 200.0% |
| yellowish brown | 54 | 22 | 40.7% |
| olive brown | 27 | 6 | 22.2% |
| light purplish blue | 9 | 6 | 66.7% |
| blue | 90 | 180 | 200.0% |
| brown | 54 | 108 | 200.0% |
| deep yellowish green | 9 | 18 | 200.0% |
| light purple | 9 | 18 | 200.0% |
| grayish brown | 18 | 12 | 66.7% |
| pale blue | 9 | 12 | 133.3% |
| red | 63 | 120 | 190.5% |
| greenish gray | 18 | 24 | 133.3% |
| pale green | 9 | 12 | 133.3% |
| olive gray | 9 | 6 | 66.7% |
| grayish green | 9 | 12 | 133.3% |
| greenish blue | 45 | 90 | 200.0% |
| grayish olive | 18 | 18 | 100.0% |
| orange | 54 | 96 | 177.8% |
| green | 81 | 150 | 185.2% |
| black | 63 | 126 | 200.0% |
| dark bluish green | 9 | 18 | 200.0% |
| purplish red | 54 | 102 | 188.9% |
| light bluish green | 9 | 0 | 0.0% |
| dark red | 9 | 18 | 200.0% |
| reddish brown | 54 | 100 | 185.2% |
| orange yellow | 63 | 19 | 30.2% |
| deep purple | 9 | 18 | 200.0% |
| grayish blue | 9 | 18 | 200.0% |
| gray | 99 | 168 | 169.7% |
| pink | 81 | 150 | 185.2% |
| light green | 9 | 6 | 66.7% |
| greenish yellow | 81 | 1 | 1.2% |
| violet | 81 | 45 | 55.6% |
| reddish gray | 9 | 12 | 133.3% |
| dark purplish red | 9 | 18 | 200.0% |
| reddish purple | 72 | 144 | 200.0% |
| grayish olive green | 9 | 18 | 200.0% |
| dark green | 9 | 0 | 0.0% |
| grayish purplish red | 9 | 6 | 66.7% |
| purplish blue | 81 | 67 | 82.7% |
| bluish gray | 18 | 30 | 166.7% |
| yellow green | 72 | 24 | 33.3% |
| pale purple | 9 | 18 | 200.0% |
| yellow | 81 | 162 | 200.0% |
| light blue | 9 | 18 | 200.0% |
| purplish gray | 18 | 24 | 133.3% |
| deep reddish purple | 9 | 18 | 200.0% |
| purplish pink | 72 | 126 | 175.0% |
| pale violet | 9 | 0 | 0.0% |
| grayish purple | 9 | 18 | 200.0% |
| olive green | 36 | 39 | 108.3% |
| deep red | 9 | 18 | 200.0% |
| grayish yellow | 9 | 0 | 0.0% |
| light yellowish green | 9 | 11 | 122.2% |
| purple | 90 | 162 | 180.0% |
| light greenish blue | 9 | 18 | 200.0% |
| grayish yellowish brown | 18 | 6 | 33.3% |
| olive | 36 | 54 | 150.0% |
| reddish orange | 54 | 108 | 200.0% |
| dark reddish purple | 9 | 18 | 200.0% |
| bluish green | 54 | 38 | 70.4% |
| dark yellowish green | 9 | 18 | 200.0% |

