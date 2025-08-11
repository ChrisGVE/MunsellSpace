# Comprehensive Conversion Dataset - Mismatches Analysis V2

## Configuration
- **Illuminants**: C, D65, F7
- **Adaptation**: XYZScaling (winner across datasets)
- **Hue Method**: Method 2 (ExcludeStartIncludeEnd) - systematically better
- **Python Reference**: colour-science library with ISCC-NBS classification

## W3 ISCC-NBS Dataset (267 colors)

### Summary Statistics

| Illuminant | Rust Accuracy | Python Accuracy | Python Errors |
|------------|---------------|-----------------|---------------|
| C | 53.9% | 67.4% | 50 |
| D65 | 30.3% | 51.3% | 47 |
| F7 | 30.3% | 50.9% | 48 |

### Detailed Mismatches (First 5)

Total colors with mismatches: 120 (44.9%)

#### 1. Expected: vivid pink
Hex: #FFB5BA

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 5.4R 8.0/5.5 | light pink | ❌ | 1.0R 8.0/6.6 | light pink | ❌ |
| D65 | 7.0R 8.0/5.3 | light yellowish pink | ❌ | 4.7R 8.0/6.0 | light pink | ❌ |
| F7 | 7.0R 8.0/5.3 | light yellowish pink | ❌ | 4.8R 8.0/6.0 | light pink | ❌ |

#### 2. Expected: strong pink
Hex: #EA9399

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 5.6R 6.9/6.8 | moderate pink | ❌ | 1.6R 6.9/8.0 | strong pink | ✅ |
| D65 | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | 4.2R 6.9/7.4 | strong yellowish pink | ❌ |
| F7 | 6.9R 6.9/6.6 | moderate yellowish pink | ❌ | 4.3R 6.9/7.4 | strong yellowish pink | ❌ |

#### 3. Expected: deep pink
Hex: #E4717A

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 5.9R 6.0/9.3 | deep pink | ✅ | 2.5R 6.0/10.7 | deep pink | ✅ |
| D65 | 6.7R 6.0/9.0 | deep yellowish pink | ❌ | 4.0R 6.0/10.3 | deep pink | ✅ |
| F7 | 6.8R 6.0/9.0 | deep yellowish pink | ❌ | 4.0R 6.0/10.3 | deep pink | ✅ |

#### 4. Expected: light pink
Hex: #F9CCCA

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 6.3R 8.5/3.5 | light yellowish pink | ❌ | 3.4R 8.5/3.9 | light pink | ✅ |
| D65 | 0.8YR 8.5/3.2 | light yellowish pink | ❌ | 0.3YR 8.5/3.2 | light yellowish pink | ❌ |
| F7 | 0.9YR 8.5/3.2 | light yellowish pink | ❌ | 0.3YR 8.5/3.3 | light yellowish pink | ❌ |

#### 5. Expected: moderate pink
Hex: #DEA5A4

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 6.2R 7.2/4.6 | moderate yellowish pink | ❌ | 3.3R 7.2/5.2 | moderate pink | ✅ |
| D65 | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | 7.7R 7.2/4.5 | moderate yellowish pink | ❌ |
| F7 | 8.4R 7.2/4.4 | moderate yellowish pink | ❌ | 7.8R 7.2/4.5 | moderate yellowish pink | ❌ |

## Paul Centore Dataset (260 colors)

### Summary Statistics

| Illuminant | Rust Accuracy | Python Accuracy | Python Errors |
|------------|---------------|-----------------|---------------|
| C | 52.3% | 68.8% | 42 |
| D65 | 61.9% | 81.9% | 46 |
| F7 | 63.1% | 82.3% | 45 |

### Detailed Mismatches (First 5)

Total colors with mismatches: 95 (36.5%)

#### 1. Expected: vivid pink
Hex: #FD7992

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 6.0RP 6.6/15.9 | strong purplish pink | ❌ | 9.9RP 6.6/12.1 | vivid pink | ✅ |
| D65 | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | 1.2R 6.6/11.7 | vivid pink | ✅ |
| F7 | 5.6R 6.6/9.5 | strong yellowish pink | ❌ | 1.2R 6.6/11.7 | vivid pink | ✅ |

#### 2. Expected: strong pink
Hex: #F48FA0

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 5.6RP 7.0/12.0 | strong purplish pink | ❌ | 9.4RP 7.0/9.5 | strong pink | ✅ |
| D65 | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | 1.4R 7.0/8.9 | strong pink | ✅ |
| F7 | 5.6R 7.0/7.3 | strong yellowish pink | ❌ | 1.4R 7.0/8.9 | strong pink | ✅ |

#### 4. Expected: light pink
Hex: #F8C3CE

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 4.2RP 8.3/6.0 | light purplish pink | ❌ | 7.2RP 8.3/5.1 | light purplish pink | ❌ |
| D65 | 5.9R 8.3/3.6 | light pink | ✅ | 2.4R 8.3/4.2 | light pink | ✅ |
| F7 | 6.0R 8.3/3.6 | light pink | ✅ | 2.5R 8.3/4.2 | light pink | ✅ |

#### 7. Expected: pale pink
Hex: #EFD1DC

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 4.1R 8.6/2.3 | pale pink | ✅ | 3.8RP 8.6/3.5 | pale purplish pink | ❌ |
| D65 | 6.2R 8.6/2.1 | pale yellowish pink | ❌ | 2.9R 8.6/2.4 | pale pink | ✅ |
| F7 | 3.2R 8.6/2.4 | pale pink | ✅ | 3.1R 8.6/2.4 | pale pink | ✅ |

#### 8. Expected: grayish pink
Hex: #CBADB7

| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |
|------------|--------------|-----------|----|--------------|-----------|----|
| C | 2.3RP 7.3/3.7 | grayish purplish pink | ❌ | 4.5RP 7.3/3.4 | grayish purplish pink | ❌ |
| D65 | 5.8R 7.3/2.1 | grayish pink | ✅ | 2.2R 7.3/2.4 | grayish pink | ✅ |
| F7 | 6.0R 7.3/2.1 | grayish pink | ✅ | 2.3R 7.3/2.4 | grayish pink | ✅ |

## Summary

### Key Findings
- **Method 2** (ExcludeStartIncludeEnd) is systematically better across both datasets
- **XYZScaling** adaptation performs best overall
- **W3 Dataset**: Best with Illuminant C (53.9% accuracy)
- **Centore Dataset**: F7 slightly better than D65

### Performance Comparison
- W3: 267 total colors, 120 with mismatches (44.9%)
- Centore: 260 total colors, 95 with mismatches (36.5%)
