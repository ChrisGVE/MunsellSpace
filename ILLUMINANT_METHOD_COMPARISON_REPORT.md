# Illuminant Method Comparison Report

## Executive Summary

This report compares the original mathematical converter with the new
illuminant-aware mathematical_v2 converter across all available illuminants.

- **Test Colors**: 15
- **Illuminants Tested**: 10 (D65, C, A, D50, D55, D75, F2, F7, F11, E)
- **Total Conversions**: 165

## Color-by-Color Analysis

### Pure Red (#FF0000)

**Description**: Pure red - maximum saturation
**Expected Munsell**: 5R 5/20

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 8.5R 5.2/20.0 | ✅ |
| V2 | D65 (Daylight 6500K) | 2.5YR 5.2/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 2.5YR 5.2/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 2.5YR 5.7/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 2.5YR 5.3/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 2.5YR 5.3/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 2.5YR 5.2/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 2.5YR 5.4/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 2.5YR 5.2/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 2.5YR 5.5/2.0 | ✅ |
| V2 | E (Equal Energy) | 2.5YR 5.3/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 0.45
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 0.10
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 0.19
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 0.23
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 0.11
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 0.43
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 0.17
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 0.21
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 0.34
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 0.38
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 0.49
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 0.25
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 0.45
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 0.22
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 0.34
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 0.15
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 0.10
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 0.13
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 0.11
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 0.13
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 0.17
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 0.24
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 0.27
- D75 (North sky daylight) vs E (Equal Energy): Difference score 0.15
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 0.19
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 0.23
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 0.11
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 0.12

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 24.04
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 24.06
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 24.48
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 24.14
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 24.10
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 24.08
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 24.23
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 24.04
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 24.27
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 24.15


### Pure Green (#00FF00)

**Description**: Pure green - maximum saturation
**Expected Munsell**: 5G 8/20

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 6.7GY 8.7/18.5 | ✅ |
| V2 | D65 (Daylight 6500K) | 7.5GY 8.7/4.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5GY 8.7/4.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 10.0Y 8.7/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5GY 8.8/4.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 7.5GY 8.8/4.0 | ✅ |
| V2 | D75 (North sky daylight) | 7.5GY 8.7/4.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 7.5GY 8.7/4.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 7.5GY 8.7/4.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 7.5GY 8.7/4.0 | ✅ |
| V2 | E (Equal Energy) | 7.5GY 8.7/4.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 6.56
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 6.53
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 6.57
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 6.57
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 6.55
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 6.56
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 6.56
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 6.55
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 6.53

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 15.31
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 15.34
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 21.87
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 15.32
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 15.32
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 15.32
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 15.31
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 15.31
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 15.33
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 15.34


### Pure Blue (#0000FF)

**Description**: Pure blue - maximum saturation
**Expected Munsell**: 5B 3/20

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 9.9RP 3.2/30.0 | ✅ |
| V2 | D65 (Daylight 6500K) | 7.5PB 3.2/6.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5PB 3.3/6.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 10.0PB 2.4/4.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5PB 2.9/6.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 7.5PB 3.0/6.0 | ✅ |
| V2 | D75 (North sky daylight) | 7.5PB 3.3/6.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 7.5PB 2.8/6.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 7.5PB 3.2/6.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 7.5PB 2.7/6.0 | ✅ |
| V2 | E (Equal Energy) | 7.5PB 3.1/6.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 5.33
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 0.26
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 0.16
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 0.13
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 0.43
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 0.46
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 5.42
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 0.35
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 0.25
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 0.52
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 0.55
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 0.17
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 5.06
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 5.16
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 5.45
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.89
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 5.32
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.86
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 5.24
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 0.10
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 0.39
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 0.17
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 0.26
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 0.20
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 0.18
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 0.29
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 0.27
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 0.16
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 0.30
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 0.56
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 0.13
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 0.59
- D75 (North sky daylight) vs E (Equal Energy): Difference score 0.21
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 0.43
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 0.35
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 0.46
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 0.38

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 28.38
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 28.47
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 28.95
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 28.64
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 28.54
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 28.51
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 28.81
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 28.38
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 28.84
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 28.46


### Pinkish White (#EFDDE5)

**Description**: Light pinkish color - chroma precision issue
**Expected Munsell**: 5R 9/1.5

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 1.6YR 9.0/1.0 | ✅ |
| V2 | D65 (Daylight 6500K) | 7.5G 9.0/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5G 9.0/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 5.0YR 9.0/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 10.0GY 9.0/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 2.5G 9.0/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 10.0G 9.0/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 2.5GY 9.0/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 7.5G 9.0/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 2.5GY 9.0/2.0 | ✅ |
| V2 | E (Equal Energy) | 2.5R 9.0/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 4.52
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 4.50
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 5.00
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 2.50
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 7.01
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 7.01
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 4.52
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 5.00
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 2.50
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 7.00
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 7.00
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 7.02
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 4.52
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 7.02
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.51
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 4.52
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.51
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 4.50
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 2.00
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.50
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 4.50
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 2.51
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 4.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 2.50
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 2.01
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 5.00
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 2.01
- D55 (Mid-morning/afternoon) vs E (Equal Energy): Difference score 2.00
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 2.50
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs E (Equal Energy): Difference score 4.51
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 7.01
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 2.00
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 7.01
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.00

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 7.14
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 7.14
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 4.43
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 4.64
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 3.92
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 4.64
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 3.92
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 7.14
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 3.92
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 3.92


### Very Dark Red (#5C0625)

**Description**: Very dark red - red/purple confusion
**Expected Munsell**: 5R 1.5/6

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 4.9R 1.8/7.9 | ✅ |
| V2 | D65 (Daylight 6500K) | 7.5R 1.8/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5R 1.8/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 2.5YR 2.0/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 10.0R 1.8/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 7.5R 1.8/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 7.5R 1.8/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 10.0R 1.9/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 7.5R 1.8/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 10.0R 1.9/2.0 | ✅ |
| V2 | E (Equal Energy) | 7.5R 1.8/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 7.18
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 2.54
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 2.57
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 2.59
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 7.17
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 2.53
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 2.56
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 2.58
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 4.64
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 7.16
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 7.19
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.60
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 7.18
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.59
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 7.13
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 2.52
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 2.55
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 2.54
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.51
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 2.55
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 2.57
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 2.59
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.60
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 2.57
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 2.53
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.59
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.54

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 8.43
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 8.44
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 10.51
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 10.87
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 8.45
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 8.45
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 10.90
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 8.43
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 10.92
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 8.48


### Pinkish Gray (#C7B6BD)

**Description**: Pinkish gray - family classification issue
**Expected Munsell**: 5R 7.5/1.5

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 0.5YR 7.5/1.0 | ✅ |
| V2 | D65 (Daylight 6500K) | 7.5G 7.5/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5RP 7.5/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 5.0YR 7.5/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 10.0GY 7.5/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 10.0GY 7.5/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 10.0G 7.5/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 5.0GY 7.5/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 7.5G 7.5/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 10.0R 7.5/2.0 | ✅ |
| V2 | E (Equal Energy) | 2.5R 7.5/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs C (Average Daylight - Munsell Standard): Difference score 2.00
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 4.52
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 4.50
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 4.50
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 2.50
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 4.51
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 7.01
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 4.52
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 4.51
- C (Average Daylight - Munsell Standard) vs F7 (Daylight Fluorescent): Difference score 2.00
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 7.00
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 7.02
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 7.02
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 7.02
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 2.01
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 4.52
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.52
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 2.00
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 5.00
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 4.50
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 2.01
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 4.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 2.00
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 5.01
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 4.50
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 2.01
- D55 (Mid-morning/afternoon) vs E (Equal Energy): Difference score 4.50
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 7.01
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 2.50
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.01
- D75 (North sky daylight) vs E (Equal Energy): Difference score 4.51
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 4.51
- F2 (Cool White Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 7.00
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 4.50
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 7.01
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.50

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 6.05
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 6.05
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 5.54
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 3.55
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 3.55
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 3.55
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 7.53
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 6.05
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 3.56
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 5.03


### Pure Black (#000000)

**Description**: Pure black - achromatic test
**Expected Munsell**: N 0

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 0.0N 0.0/0.0 | ✅ |
| V2 | D65 (Daylight 6500K) | 0.0N 0.0/0.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 0.0N 0.0/0.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 0.0N 0.0/0.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 0.0N 0.0/0.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 0.0N 0.0/0.0 | ✅ |
| V2 | D75 (North sky daylight) | 0.0N 0.0/0.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 0.0N 0.0/0.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 0.0N 0.0/0.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 0.0N 0.0/0.0 | ✅ |
| V2 | E (Equal Energy) | 0.0N 0.0/0.0 | ✅ |


### Pure White (#FFFFFF)

**Description**: Pure white - achromatic test
**Expected Munsell**: N 10

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 8.5GY 10.0/0.8 | ✅ |
| V2 | D65 (Daylight 6500K) | 5.0G 10.0/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 10.0G 10.0/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 10.0YR 10.0/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5GY 10.0/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 10.0GY 10.0/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 10.0G 10.0/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 5.0GY 10.0/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 5.0G 10.0/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 2.5GY 10.0/2.0 | ✅ |
| V2 | E (Equal Energy) | 10.0GY 10.0/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs C (Average Daylight - Munsell Standard): Difference score 5.00
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 7.00
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 4.50
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 7.00
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 5.00
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 2.00
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 7.00
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 2.00
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 2.00
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 7.00
- C (Average Daylight - Munsell Standard) vs F7 (Daylight Fluorescent): Difference score 5.00
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 2.00
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 4.50
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 2.00
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 2.00
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 7.00
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 7.00
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 2.00
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 2.50
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 4.50
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.50
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 4.50
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 5.00
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 2.00
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 5.00
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 7.00
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 2.50
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 7.00
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 5.00
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- D75 (North sky daylight) vs E (Equal Energy): Difference score 2.00
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 2.00
- F2 (Cool White Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.50
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 5.00
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 7.00
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.50

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 6.73
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 4.70
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 4.70
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 2.23
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 2.70
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 4.70
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 4.73
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 6.73
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 5.20
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 2.70


### Medium Gray (#808080)

**Description**: Medium gray - neutral reference
**Expected Munsell**: N 5

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 1.0G 5.3/0.8 | ✅ |
| V2 | D65 (Daylight 6500K) | 7.5G 5.3/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5G 5.3/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 2.5YR 5.3/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 2.5G 5.3/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 2.5G 5.3/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 10.0G 5.3/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 10.0GY 5.3/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 7.5G 5.3/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 10.0GY 5.3/2.0 | ✅ |
| V2 | E (Equal Energy) | 5.0G 5.3/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 7.00
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 5.00
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 5.00
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 2.50
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 4.50
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 2.50
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 7.00
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 5.00
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 5.00
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 2.50
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 2.50
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 2.00
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 2.00
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 4.50
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.50
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 7.00
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.50
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 2.50
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 4.50
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 5.00
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 2.50
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 4.50
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 5.00
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- D55 (Mid-morning/afternoon) vs E (Equal Energy): Difference score 2.50
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 2.00
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 2.50
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.00
- D75 (North sky daylight) vs E (Equal Energy): Difference score 5.00
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 4.50
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 7.00
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 4.50
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 2.50
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 7.00

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 4.67
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 4.67
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 4.69
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 2.69
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 2.69
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 2.17
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 4.17
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 4.67
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 4.17
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 5.19


### Orange (#FFA500)

**Description**: Orange - yellow-red transition
**Expected Munsell**: 2.5YR 7/14

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 1.8Y 7.4/12.8 | ✅ |
| V2 | D65 (Daylight 6500K) | 10.0YR 7.4/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 7.5YR 7.4/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 5.0YR 7.7/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 10.0YR 7.5/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 10.0YR 7.5/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 7.5YR 7.4/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 10.0YR 7.5/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 10.0YR 7.4/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 10.0YR 7.6/2.0 | ✅ |
| V2 | E (Equal Energy) | 7.5YR 7.5/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs C (Average Daylight - Munsell Standard): Difference score 2.50
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 5.25
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 2.53
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 0.12
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 0.14
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 2.55
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 2.75
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 2.57
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 2.54
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 2.62
- C (Average Daylight - Munsell Standard) vs F7 (Daylight Fluorescent): Difference score 2.50
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 2.64
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 5.18
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 5.21
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 2.78
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 5.13
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 5.25
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 5.12
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 2.70
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 2.60
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.52
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 2.57
- D55 (Mid-morning/afternoon) vs E (Equal Energy): Difference score 2.51
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 2.65
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 2.53
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.67
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 0.12
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 2.57
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 0.13
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 2.55
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.58

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 14.53
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 17.03
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 16.24
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 14.60
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 14.57
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 17.06
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 14.65
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 14.53
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 14.66
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 17.08


### Purple (#800080)

**Description**: Purple - red-blue transition
**Expected Munsell**: 5P 3/10

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 9.1P 2.9/14.0 | ✅ |
| V2 | D65 (Daylight 6500K) | 2.5RP 2.9/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 2.5RP 3.0/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 5.0R 3.0/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5RP 2.9/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 5.0RP 2.9/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 10.0P 3.0/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 10.0RP 2.9/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 2.5RP 2.9/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 10.0RP 3.0/2.0 | ✅ |
| V2 | E (Equal Energy) | 5.0RP 3.0/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 4.56
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 5.01
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 2.51
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 4.51
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 2.50
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 2.51
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 2.53
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 4.53
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 5.04
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 2.54
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 4.52
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 2.53
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 2.52
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 2.50
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 4.57
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 2.07
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 7.05
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 7.06
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 4.56
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 7.05
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 2.03
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 2.50
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 4.52
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.51
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 5.01
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 2.52
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.54
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 7.02
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 5.01
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 2.51
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 5.02
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 2.01
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.00
- D75 (North sky daylight) vs E (Equal Energy): Difference score 7.02
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 2.50
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 5.03
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.51
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 2.53
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 5.02

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 17.33
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 17.36
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 18.18
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 15.63
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 18.13
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 12.84
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 14.83
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 17.33
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 14.84
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 18.15


### Teal (#008080)

**Description**: Teal - blue-green transition
**Expected Munsell**: 5BG 4/8

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 9.8BG 4.7/5.5 | ✅ |
| V2 | D65 (Daylight 6500K) | 2.5BG 4.7/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 2.5BG 4.7/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 7.5GY 4.6/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5G 4.7/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 10.0G 4.7/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 2.5BG 4.7/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 5.0G 4.7/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 2.5BG 4.7/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 2.5G 4.7/2.0 | ✅ |
| V2 | E (Equal Energy) | 10.0G 4.7/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 7.12
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 7.03
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 4.52
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 4.55
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 2.06
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 4.53
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 7.11
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 7.02
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 4.51
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 4.54
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 2.05
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 4.52
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 2.09
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 4.60
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 7.13
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.57
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 7.12
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 7.06
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.59
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 2.51
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 7.04
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.52
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 7.03
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 5.03
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 4.53
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 5.03
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 4.52
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 2.54
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 4.56
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.07
- D75 (North sky daylight) vs E (Equal Energy): Difference score 4.54
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 4.55
- F2 (Cool White Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.51
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 5.02
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.06
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 4.53
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.53

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 6.16
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 6.16
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 7.95
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 7.86
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 5.68
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 6.17
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 10.38
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 6.16
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 8.22
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 5.69


### Warm Beige (#F5F5DC)

**Description**: Warm beige - subtle yellow cast
**Expected Munsell**: 5Y 9.5/2

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 2.5G 9.6/3.7 | ✅ |
| V2 | D65 (Daylight 6500K) | 10.0GY 9.6/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 10.0GY 9.6/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 10.0YR 9.6/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 5.0GY 9.6/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 7.5GY 9.6/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 2.5G 9.6/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 2.5GY 9.6/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 10.0GY 9.6/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 2.5GY 9.6/2.0 | ✅ |
| V2 | E (Equal Energy) | 7.5GY 9.6/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 2.03
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 5.01
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 2.51
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 4.51
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 2.52
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 2.52
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 2.50
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 2.03
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 5.01
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 2.51
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 2.52
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 2.52
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 2.51
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 7.02
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 4.52
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 4.53
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.51
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 2.03
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.52
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 2.50
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 4.51
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.51
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 5.01
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 2.51
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.51
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 7.01
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 5.01
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 2.51
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 5.01
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 2.02
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.02
- D75 (North sky daylight) vs E (Equal Energy): Difference score 7.01
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 2.52
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 5.01
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.52
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 2.50
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 5.01

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 6.14
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 6.14
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 6.17
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 6.20
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 8.65
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 1.70
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 3.71
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 6.14
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 3.71
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 8.64


### Cool Beige (#F0F8FF)

**Description**: Cool beige - subtle blue cast
**Expected Munsell**: 5B 9.8/1

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 1.9B 9.7/0.9 | ✅ |
| V2 | D65 (Daylight 6500K) | 10.0G 9.7/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 10.0G 9.7/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 7.5YR 9.7/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5GY 9.7/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 2.5G 9.7/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 2.5BG 9.7/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 5.0GY 9.7/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 10.0G 9.7/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 5.0GY 9.7/2.0 | ✅ |
| V2 | E (Equal Energy) | 5.0G 9.7/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 4.52
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 4.51
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 2.50
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 4.50
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 7.01
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 5.00
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 4.52
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 4.51
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 2.50
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 4.50
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 7.01
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 5.00
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 2.01
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 7.02
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 7.02
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.51
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 4.52
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.52
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 7.00
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 7.01
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.50
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 4.51
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 2.51
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 4.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 2.01
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 4.51
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 2.50
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- D55 (Mid-morning/afternoon) vs E (Equal Energy): Difference score 2.50
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 4.50
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs E (Equal Energy): Difference score 4.51
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 7.01
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 2.01
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 7.01
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 5.00
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 2.01

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 4.97
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 4.97
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 7.49
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 7.48
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 3.73
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 3.73
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 6.23
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 4.97
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 6.23
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 6.23


### Dusty Rose (#BC8F8F)

**Description**: Dusty rose - desaturated red
**Expected Munsell**: 5R 6/4

| Method | Illuminant | Munsell Result | Success |
|--------|------------|----------------|---------|
| Original | D65 (Fixed) | 8.6R 6.3/3.4 | ✅ |
| V2 | D65 (Daylight 6500K) | 2.5R 6.3/2.0 | ✅ |
| V2 | C (Average Daylight - Munsell Standard) | 2.5R 6.3/2.0 | ✅ |
| V2 | A (Tungsten Incandescent) | 2.5YR 6.3/2.0 | ✅ |
| V2 | D50 (Daylight 5000K) | 7.5R 6.3/2.0 | ✅ |
| V2 | D55 (Mid-morning/afternoon) | 5.0R 6.3/2.0 | ✅ |
| V2 | D75 (North sky daylight) | 10.0RP 6.3/2.0 | ✅ |
| V2 | F2 (Cool White Fluorescent) | 10.0R 6.3/2.0 | ✅ |
| V2 | F7 (Daylight Fluorescent) | 2.5R 6.3/2.0 | ✅ |
| V2 | F11 (Narrow Band Fluorescent) | 10.0R 6.3/2.0 | ✅ |
| V2 | E (Equal Energy) | 5.0R 6.3/2.0 | ✅ |

**Illuminant Differences**:
- D65 (Daylight 6500K) vs A (Tungsten Incandescent): Difference score 2.08
- D65 (Daylight 6500K) vs D50 (Daylight 5000K): Difference score 5.02
- D65 (Daylight 6500K) vs D55 (Mid-morning/afternoon): Difference score 2.51
- D65 (Daylight 6500K) vs D75 (North sky daylight): Difference score 4.51
- D65 (Daylight 6500K) vs F2 (Cool White Fluorescent): Difference score 2.53
- D65 (Daylight 6500K) vs F11 (Narrow Band Fluorescent): Difference score 2.54
- D65 (Daylight 6500K) vs E (Equal Energy): Difference score 2.52
- C (Average Daylight - Munsell Standard) vs A (Tungsten Incandescent): Difference score 2.08
- C (Average Daylight - Munsell Standard) vs D50 (Daylight 5000K): Difference score 5.02
- C (Average Daylight - Munsell Standard) vs D55 (Mid-morning/afternoon): Difference score 2.51
- C (Average Daylight - Munsell Standard) vs D75 (North sky daylight): Difference score 4.51
- C (Average Daylight - Munsell Standard) vs F2 (Cool White Fluorescent): Difference score 2.53
- C (Average Daylight - Munsell Standard) vs F11 (Narrow Band Fluorescent): Difference score 2.54
- C (Average Daylight - Munsell Standard) vs E (Equal Energy): Difference score 2.52
- A (Tungsten Incandescent) vs D50 (Daylight 5000K): Difference score 7.06
- A (Tungsten Incandescent) vs D55 (Mid-morning/afternoon): Difference score 4.57
- A (Tungsten Incandescent) vs D75 (North sky daylight): Difference score 4.59
- A (Tungsten Incandescent) vs F2 (Cool White Fluorescent): Difference score 4.55
- A (Tungsten Incandescent) vs F7 (Daylight Fluorescent): Difference score 2.08
- A (Tungsten Incandescent) vs F11 (Narrow Band Fluorescent): Difference score 4.54
- A (Tungsten Incandescent) vs E (Equal Energy): Difference score 4.56
- D50 (Daylight 5000K) vs D55 (Mid-morning/afternoon): Difference score 2.51
- D50 (Daylight 5000K) vs D75 (North sky daylight): Difference score 4.53
- D50 (Daylight 5000K) vs F2 (Cool White Fluorescent): Difference score 2.52
- D50 (Daylight 5000K) vs F7 (Daylight Fluorescent): Difference score 5.02
- D50 (Daylight 5000K) vs F11 (Narrow Band Fluorescent): Difference score 2.52
- D50 (Daylight 5000K) vs E (Equal Energy): Difference score 2.50
- D55 (Mid-morning/afternoon) vs D75 (North sky daylight): Difference score 7.02
- D55 (Mid-morning/afternoon) vs F2 (Cool White Fluorescent): Difference score 5.02
- D55 (Mid-morning/afternoon) vs F7 (Daylight Fluorescent): Difference score 2.51
- D55 (Mid-morning/afternoon) vs F11 (Narrow Band Fluorescent): Difference score 5.03
- D75 (North sky daylight) vs F2 (Cool White Fluorescent): Difference score 2.04
- D75 (North sky daylight) vs F7 (Daylight Fluorescent): Difference score 4.51
- D75 (North sky daylight) vs F11 (Narrow Band Fluorescent): Difference score 2.05
- D75 (North sky daylight) vs E (Equal Energy): Difference score 7.03
- F2 (Cool White Fluorescent) vs F7 (Daylight Fluorescent): Difference score 2.53
- F2 (Cool White Fluorescent) vs E (Equal Energy): Difference score 5.02
- F7 (Daylight Fluorescent) vs F11 (Narrow Band Fluorescent): Difference score 2.54
- F7 (Daylight Fluorescent) vs E (Equal Energy): Difference score 2.52
- F11 (Narrow Band Fluorescent) vs E (Equal Energy): Difference score 5.02

**Method Differences**:
- Original (D65 (Fixed)) vs V2 (D65 (Daylight 6500K)): Difference score 5.39
- Original (D65 (Fixed)) vs V2 (C (Average Daylight - Munsell Standard)): Difference score 5.39
- Original (D65 (Fixed)) vs V2 (A (Tungsten Incandescent)): Difference score 7.47
- Original (D65 (Fixed)) vs V2 (D50 (Daylight 5000K)): Difference score 2.52
- Original (D65 (Fixed)) vs V2 (D55 (Mid-morning/afternoon)): Difference score 5.01
- Original (D65 (Fixed)) vs V2 (D75 (North sky daylight)): Difference score 4.90
- Original (D65 (Fixed)) vs V2 (F2 (Cool White Fluorescent)): Difference score 2.93
- Original (D65 (Fixed)) vs V2 (F7 (Daylight Fluorescent)): Difference score 5.39
- Original (D65 (Fixed)) vs V2 (F11 (Narrow Band Fluorescent)): Difference score 2.93
- Original (D65 (Fixed)) vs V2 (E (Equal Energy)): Difference score 5.02


## Summary of Findings

### Illuminant Impact Analysis

- **Colors showing illuminant differences**: 14/15
- **Total illuminant differences detected**: 497

### Method Impact Analysis

- **Colors showing method differences**: 14/15
- **Total method differences detected**: 140

## Conclusions

✅ **Illuminant changes DO produce different results** for some colors.
The illuminant-aware V2 converter shows measurable differences
compared to the fixed D65 original converter.

---
Report generated by MunsellSpace Illuminant Method Comparison Tool
