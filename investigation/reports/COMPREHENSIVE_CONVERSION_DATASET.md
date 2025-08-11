# Comprehensive Conversion Dataset Analysis

## Illuminant Descriptions

| Code | Illuminant | Description | Mathematical Method |
|------|------------|-------------|---------------------|
| A_v1 | A | Incandescent/Tungsten (2856K) | mathematical.rs (Original) |
| A_v2 | A | Incandescent/Tungsten (2856K) | mathematical_v2.rs (V2) |
| C_v1 | C | Average Daylight (6774K) | mathematical.rs (Original) |
| C_v2 | C | Average Daylight (6774K) | mathematical_v2.rs (V2) |
| D50_v1 | D50 | Horizon Light (5003K) | mathematical.rs (Original) |
| D50_v2 | D50 | Horizon Light (5003K) | mathematical_v2.rs (V2) |
| D55_v1 | D55 | Mid-morning Daylight (5503K) | mathematical.rs (Original) |
| D55_v2 | D55 | Mid-morning Daylight (5503K) | mathematical_v2.rs (V2) |
| D65_v1 | D65 | Noon Daylight (6504K) | mathematical.rs (Original) |
| D65_v2 | D65 | Noon Daylight (6504K) | mathematical_v2.rs (V2) |
| D75_v1 | D75 | North Sky Daylight (7504K) | mathematical.rs (Original) |
| D75_v2 | D75 | North Sky Daylight (7504K) | mathematical_v2.rs (V2) |
| E_v1 | E | Equal Energy | mathematical.rs (Original) |
| E_v2 | E | Equal Energy | mathematical_v2.rs (V2) |
| F2_v1 | F2 | Cool White Fluorescent | mathematical.rs (Original) |
| F2_v2 | F2 | Cool White Fluorescent | mathematical_v2.rs (V2) |
| F7_v1 | F7 | D65 Simulator Fluorescent | mathematical.rs (Original) |
| F7_v2 | F7 | D65 Simulator Fluorescent | mathematical_v2.rs (V2) |
| F11_v1 | F11 | Narrow Band Fluorescent | mathematical.rs (Original) |
| F11_v2 | F11 | Narrow Band Fluorescent | mathematical_v2.rs (V2) |

## W3 ISCC-NBS Dataset (267 colors)

### Summary Statistics

| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy | Total Tested |
|------------|------------|-------------------|-------------------|--------------|
| D50_v2 | CAT02 | 4.1% (11/267) | 5.6% (15/267) | 267 |
| E_v2 | VonKries | 4.9% (13/267) | 6.4% (17/267) | 267 |
| F2_v1 | CAT02 | 10.5% (28/267) | 12.4% (33/267) | 267 |
| D75_v1 | Bradford | 31.5% (84/267) | 31.1% (83/267) | 267 |
| F11_v2 | VonKries | 4.1% (11/267) | 4.9% (13/267) | 267 |
| D75_v1 | VonKries | 31.1% (83/267) | 30.3% (81/267) | 267 |
| A_v1 | CAT02 | 4.1% (11/267) | 3.7% (10/267) | 267 |
| F11_v2 | XYZScaling | 3.4% (9/267) | 4.1% (11/267) | 267 |
| D65_v2 | Bradford | 5.2% (14/267) | 5.6% (15/267) | 267 |
| C_v1 | XYZScaling | 46.4% (124/267) | 52.8% (141/267) | 267 |
| F7_v2 | CAT02 | 5.2% (14/267) | 6.0% (16/267) | 267 |
| A_v2 | XYZScaling | 3.7% (10/267) | 4.5% (12/267) | 267 |
| F11_v1 | VonKries | 13.1% (35/267) | 13.1% (35/267) | 267 |
| D75_v2 | XYZScaling | 4.9% (13/267) | 5.2% (14/267) | 267 |
| E_v2 | XYZScaling | 4.9% (13/267) | 6.4% (17/267) | 267 |
| D50_v1 | XYZScaling | 13.1% (35/267) | 16.1% (43/267) | 267 |
| C_v2 | XYZScaling | 5.6% (15/267) | 6.0% (16/267) | 267 |
| D50_v2 | Bradford | 4.1% (11/267) | 5.6% (15/267) | 267 |
| F2_v1 | XYZScaling | 7.9% (21/267) | 9.7% (26/267) | 267 |
| A_v1 | VonKries | 2.2% (6/267) | 2.2% (6/267) | 267 |
| C_v2 | VonKries | 5.6% (15/267) | 6.0% (16/267) | 267 |
| D55_v2 | XYZScaling | 4.9% (13/267) | 5.6% (15/267) | 267 |
| D75_v2 | CAT02 | 4.5% (12/267) | 4.9% (13/267) | 267 |
| A_v1 | Bradford | 4.1% (11/267) | 3.4% (9/267) | 267 |
| F2_v2 | Bradford | 4.1% (11/267) | 4.5% (12/267) | 267 |
| C_v1 | Bradford | 46.1% (123/267) | 51.7% (138/267) | 267 |
| D50_v1 | VonKries | 16.1% (43/267) | 17.2% (46/267) | 267 |
| D65_v1 | CAT02 | 27.0% (72/267) | 30.0% (80/267) | 267 |
| D50_v1 | CAT02 | 15.4% (41/267) | 17.6% (47/267) | 267 |
| E_v2 | Bradford | 4.9% (13/267) | 6.4% (17/267) | 267 |
| A_v2 | VonKries | 2.2% (6/267) | 3.0% (8/267) | 267 |
| E_v1 | CAT02 | 30.3% (81/267) | 34.5% (92/267) | 267 |
| D65_v1 | VonKries | 27.0% (72/267) | 30.0% (80/267) | 267 |
| D65_v1 | XYZScaling | 27.0% (72/267) | 30.0% (80/267) | 267 |
| D75_v1 | CAT02 | 31.1% (83/267) | 31.1% (83/267) | 267 |
| D55_v1 | Bradford | 17.2% (46/267) | 21.0% (56/267) | 267 |
| C_v2 | Bradford | 5.6% (15/267) | 6.0% (16/267) | 267 |
| D55_v1 | VonKries | 19.5% (52/267) | 21.3% (57/267) | 267 |
| C_v1 | CAT02 | 46.1% (123/267) | 51.3% (137/267) | 267 |
| F11_v1 | CAT02 | 11.2% (30/267) | 12.7% (34/267) | 267 |
| E_v1 | XYZScaling | 28.5% (76/267) | 32.2% (86/267) | 267 |
| A_v2 | CAT02 | 3.0% (8/267) | 3.4% (9/267) | 267 |
| D65_v2 | VonKries | 5.2% (14/267) | 5.6% (15/267) | 267 |
| D65_v2 | XYZScaling | 5.2% (14/267) | 5.6% (15/267) | 267 |
| D75_v1 | XYZScaling | 31.8% (85/267) | 31.8% (85/267) | 267 |
| F7_v2 | VonKries | 5.2% (14/267) | 6.0% (16/267) | 267 |
| A_v2 | Bradford | 3.0% (8/267) | 3.4% (9/267) | 267 |
| F11_v2 | Bradford | 3.7% (10/267) | 4.5% (12/267) | 267 |
| E_v1 | VonKries | 31.5% (84/267) | 37.5% (100/267) | 267 |
| F2_v2 | XYZScaling | 3.7% (10/267) | 4.1% (11/267) | 267 |
| F2_v2 | VonKries | 4.1% (11/267) | 4.5% (12/267) | 267 |
| F2_v1 | VonKries | 13.5% (36/267) | 14.6% (39/267) | 267 |
| F2_v2 | CAT02 | 4.1% (11/267) | 4.5% (12/267) | 267 |
| F7_v1 | Bradford | 27.0% (72/267) | 30.0% (80/267) | 267 |
| F7_v2 | Bradford | 5.2% (14/267) | 6.0% (16/267) | 267 |
| C_v2 | CAT02 | 5.6% (15/267) | 6.0% (16/267) | 267 |
| E_v2 | CAT02 | 4.9% (13/267) | 6.4% (17/267) | 267 |
| C_v1 | VonKries | 43.8% (117/267) | 47.9% (128/267) | 267 |
| F11_v1 | XYZScaling | 9.0% (24/267) | 10.5% (28/267) | 267 |
| D55_v2 | CAT02 | 4.9% (13/267) | 5.6% (15/267) | 267 |
| F7_v1 | VonKries | 27.0% (72/267) | 30.0% (80/267) | 267 |
| F11_v1 | Bradford | 11.6% (31/267) | 12.7% (34/267) | 267 |
| F2_v1 | Bradford | 11.2% (30/267) | 13.5% (36/267) | 267 |
| D55_v2 | Bradford | 4.9% (13/267) | 6.0% (16/267) | 267 |
| D75_v2 | Bradford | 4.5% (12/267) | 4.9% (13/267) | 267 |
| A_v1 | XYZScaling | 8.2% (22/267) | 7.9% (21/267) | 267 |
| D55_v1 | XYZScaling | 16.5% (44/267) | 20.6% (55/267) | 267 |
| F7_v2 | XYZScaling | 5.2% (14/267) | 6.0% (16/267) | 267 |
| D55_v1 | CAT02 | 17.2% (46/267) | 21.3% (57/267) | 267 |
| D55_v2 | VonKries | 4.9% (13/267) | 5.6% (15/267) | 267 |
| D65_v2 | CAT02 | 5.2% (14/267) | 5.6% (15/267) | 267 |
| E_v1 | Bradford | 30.3% (81/267) | 34.1% (91/267) | 267 |
| D75_v2 | VonKries | 4.5% (12/267) | 4.9% (13/267) | 267 |
| F11_v2 | CAT02 | 3.7% (10/267) | 4.5% (12/267) | 267 |
| D65_v1 | Bradford | 27.0% (72/267) | 30.0% (80/267) | 267 |
| D50_v2 | VonKries | 4.1% (11/267) | 5.6% (15/267) | 267 |
| F7_v1 | XYZScaling | 26.6% (71/267) | 30.0% (80/267) | 267 |
| D50_v2 | XYZScaling | 4.1% (11/267) | 5.6% (15/267) | 267 |
| D50_v1 | Bradford | 15.0% (40/267) | 17.2% (46/267) | 267 |
| F7_v1 | CAT02 | 27.3% (73/267) | 30.3% (81/267) | 267 |

### Detailed Results (Showing Matches Only)

#### 1. #FFB5BA - Expected: vivid pink

No matches

#### 2. #EA9399 - Expected: strong pink

No matches

#### 3. #E4717A - Expected: deep pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0R 6.0/9.1 | deep yellowish pink | ❌ | deep pink | ✅ |
| C_v1 | VonKries | 6.0R 6.0/9.1 | deep yellowish pink | ❌ | deep pink | ✅ |
| C_v1 | CAT02 | 6.0R 6.0/9.0 | deep yellowish pink | ❌ | deep pink | ✅ |
| C_v1 | XYZScaling | 5.9R 6.0/9.3 | deep yellowish pink | ❌ | deep pink | ✅ |
| D75_v1 | Bradford | 5.8R 6.0/8.4 | deep yellowish pink | ❌ | deep pink | ✅ |
| D75_v1 | VonKries | 5.9R 6.0/8.4 | deep yellowish pink | ❌ | deep pink | ✅ |
| D75_v1 | CAT02 | 5.9R 6.0/8.4 | deep yellowish pink | ❌ | deep pink | ✅ |
| D75_v1 | XYZScaling | 5.9R 6.0/8.5 | deep yellowish pink | ❌ | deep pink | ✅ |

#### 4. #F9CCCA - Expected: light pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.5R 8.6/3.9 | light pink | ✅ | light pink | ✅ |
| C_v1 | VonKries | 3.5R 8.5/3.9 | light pink | ✅ | light pink | ✅ |
| C_v1 | CAT02 | 3.5R 8.5/3.9 | light pink | ✅ | light pink | ✅ |
| D75_v1 | XYZScaling | 3.3R 8.5/3.1 | light pink | ✅ | light pink | ✅ |

#### 5. #DEA5A4 - Expected: moderate pink

No matches

#### 6. #C08081 - Expected: dark pink

No matches

#### 7. #EAD8D7 - Expected: pale pink

No matches

#### 8. #C4AEAD - Expected: grayish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 10.0RP 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| C_v2 | VonKries | 10.0RP 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| C_v2 | CAT02 | 10.0RP 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| C_v2 | XYZScaling | 10.0RP 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | Bradford | 2.5R 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | VonKries | 2.5R 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | CAT02 | 2.5R 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | XYZScaling | 2.5R 7.2/2.0 | grayish pink | ✅ | grayish pink | ✅ |

#### 9. #EAE3E1 - Expected: pinkish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.4R 9.1/0.7 | pinkish white | ✅ | pinkish white | ✅ |
| C_v1 | VonKries | 9.5R 9.1/0.7 | pinkish white | ✅ | pinkish white | ✅ |
| C_v1 | CAT02 | 9.5R 9.1/0.7 | pinkish white | ✅ | pinkish white | ✅ |
| C_v1 | XYZScaling | 8.9R 9.1/0.7 | pinkish white | ✅ | pinkish white | ✅ |

#### 10. #C1B6B3 - Expected: pinkish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1YR 7.4/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| C_v1 | VonKries | 0.3YR 7.4/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| C_v1 | CAT02 | 0.1YR 7.4/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| C_v1 | XYZScaling | 9.1R 7.4/1.1 | pinkish gray | ✅ | pinkish gray | ✅ |

#### 11. #BE0032 - Expected: vivid red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 8.5R 4.2/17.9 | vivid red | ✅ | vivid red | ✅ |
| A_v1 | VonKries | 8.1R 4.0/18.4 | vivid red | ✅ | vivid red | ✅ |
| A_v1 | CAT02 | 8.5R 4.2/17.9 | vivid red | ✅ | vivid red | ✅ |
| A_v1 | XYZScaling | 8.0R 3.9/18.4 | vivid red | ✅ | vivid red | ✅ |
| C_v1 | Bradford | 7.2R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| C_v1 | VonKries | 7.1R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| C_v1 | CAT02 | 7.2R 3.9/13.3 | vivid red | ✅ | vivid red | ✅ |
| C_v1 | XYZScaling | 7.1R 3.9/13.7 | vivid red | ✅ | vivid red | ✅ |
| D50_v1 | Bradford | 7.7R 4.0/14.8 | vivid red | ✅ | vivid red | ✅ |
| D50_v1 | VonKries | 7.7R 3.9/14.7 | vivid red | ✅ | vivid red | ✅ |
| D50_v1 | CAT02 | 7.7R 4.0/14.8 | vivid red | ✅ | vivid red | ✅ |
| D50_v1 | XYZScaling | 7.7R 3.9/14.4 | vivid red | ✅ | vivid red | ✅ |
| D55_v1 | Bradford | 7.6R 4.0/14.2 | vivid red | ✅ | vivid red | ✅ |
| D55_v1 | VonKries | 7.5R 3.9/14.2 | vivid red | ✅ | vivid red | ✅ |
| D55_v1 | CAT02 | 7.6R 4.0/14.2 | vivid red | ✅ | vivid red | ✅ |
| D55_v1 | XYZScaling | 7.6R 3.9/14.0 | vivid red | ✅ | vivid red | ✅ |
| D65_v1 | Bradford | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| D65_v1 | VonKries | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| D65_v1 | CAT02 | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| D65_v1 | XYZScaling | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| D75_v1 | XYZScaling | 7.1R 3.9/13.1 | vivid red | ✅ | vivid red | ✅ |
| E_v1 | Bradford | 7.5R 4.0/14.4 | vivid red | ✅ | vivid red | ✅ |
| E_v1 | VonKries | 7.4R 3.9/14.3 | vivid red | ✅ | vivid red | ✅ |
| E_v1 | CAT02 | 7.4R 4.0/14.3 | vivid red | ✅ | vivid red | ✅ |
| E_v1 | XYZScaling | 7.3R 3.9/14.6 | vivid red | ✅ | vivid red | ✅ |
| F2_v1 | Bradford | 8.0R 4.1/15.7 | vivid red | ✅ | vivid red | ✅ |
| F2_v1 | VonKries | 7.8R 3.9/15.7 | vivid red | ✅ | vivid red | ✅ |
| F2_v1 | CAT02 | 8.0R 4.0/15.7 | vivid red | ✅ | vivid red | ✅ |
| F2_v1 | XYZScaling | 7.8R 3.9/15.4 | vivid red | ✅ | vivid red | ✅ |
| F7_v1 | Bradford | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| F7_v1 | VonKries | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| F7_v1 | CAT02 | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| F7_v1 | XYZScaling | 7.3R 3.9/13.4 | vivid red | ✅ | vivid red | ✅ |
| F11_v1 | Bradford | 8.1R 4.1/16.0 | vivid red | ✅ | vivid red | ✅ |
| F11_v1 | VonKries | 7.8R 3.9/16.1 | vivid red | ✅ | vivid red | ✅ |
| F11_v1 | CAT02 | 8.0R 4.1/16.0 | vivid red | ✅ | vivid red | ✅ |
| F11_v1 | XYZScaling | 7.8R 3.9/15.8 | vivid red | ✅ | vivid red | ✅ |

#### 12. #BC3F4A - Expected: strong red

No matches

#### 13. #841B2D - Expected: deep red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.2R 2.9/9.6 | deep red | ✅ | deep red | ✅ |
| C_v1 | VonKries | 4.2R 2.9/9.6 | deep red | ✅ | deep red | ✅ |
| C_v1 | CAT02 | 4.2R 2.9/9.6 | deep red | ✅ | deep red | ✅ |
| C_v1 | XYZScaling | 4.0R 2.9/9.9 | deep red | ✅ | deep red | ✅ |
| D50_v1 | Bradford | 8.1R 2.9/9.4 | deep red | ✅ | deep red | ✅ |
| D50_v1 | VonKries | 8.0R 2.9/9.4 | deep red | ✅ | deep red | ✅ |
| D50_v1 | CAT02 | 8.1R 2.9/9.4 | deep red | ✅ | deep red | ✅ |
| D50_v1 | XYZScaling | 8.1R 2.9/9.3 | deep red | ✅ | deep red | ✅ |
| D55_v1 | Bradford | 7.8R 2.9/9.0 | deep red | ✅ | deep red | ✅ |
| D55_v1 | VonKries | 7.8R 2.9/9.0 | deep red | ✅ | deep red | ✅ |
| D55_v1 | CAT02 | 7.8R 2.9/9.0 | deep red | ✅ | deep red | ✅ |
| D75_v1 | Bradford | 4.1R 2.9/9.2 | deep red | ✅ | deep red | ✅ |
| D75_v1 | VonKries | 4.1R 2.9/9.2 | deep red | ✅ | deep red | ✅ |
| D75_v1 | CAT02 | 4.1R 2.9/9.2 | deep red | ✅ | deep red | ✅ |
| D75_v1 | XYZScaling | 4.1R 2.9/9.4 | deep red | ✅ | deep red | ✅ |
| E_v1 | Bradford | 7.5R 2.9/9.1 | deep red | ✅ | deep red | ✅ |
| E_v1 | VonKries | 7.5R 2.9/9.1 | deep red | ✅ | deep red | ✅ |
| E_v1 | CAT02 | 7.5R 2.9/9.0 | deep red | ✅ | deep red | ✅ |
| E_v1 | XYZScaling | 7.4R 2.9/9.2 | deep red | ✅ | deep red | ✅ |
| F2_v1 | Bradford | 8.4R 3.0/10.1 | deep red | ✅ | deep red | ✅ |
| F2_v1 | VonKries | 8.3R 2.9/10.2 | deep red | ✅ | deep red | ✅ |
| F2_v1 | CAT02 | 8.4R 3.0/10.1 | deep red | ✅ | deep red | ✅ |
| F2_v1 | XYZScaling | 8.4R 2.9/10.0 | deep red | ✅ | deep red | ✅ |
| F11_v1 | Bradford | 8.5R 3.0/10.4 | deep red | ✅ | deep red | ✅ |
| F11_v1 | VonKries | 8.3R 2.9/10.4 | deep red | ✅ | deep red | ✅ |
| F11_v1 | CAT02 | 8.5R 3.0/10.4 | deep red | ✅ | deep red | ✅ |
| F11_v1 | XYZScaling | 8.4R 2.9/10.3 | deep red | ✅ | deep red | ✅ |

#### 14. #5C0923 - Expected: very deep red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.0R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| C_v1 | VonKries | 5.0R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| C_v1 | CAT02 | 5.0R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| C_v1 | XYZScaling | 4.9R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | Bradford | 7.6R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | VonKries | 7.4R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | CAT02 | 7.5R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | XYZScaling | 7.5R 1.8/8.0 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | Bradford | 6.9R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | VonKries | 6.8R 1.8/8.0 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | CAT02 | 6.8R 1.8/8.0 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | XYZScaling | 6.8R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | Bradford | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | VonKries | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | CAT02 | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | XYZScaling | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | Bradford | 4.9R 1.8/7.5 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | VonKries | 4.9R 1.8/7.5 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | CAT02 | 4.9R 1.8/7.5 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | XYZScaling | 4.9R 1.8/7.6 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | Bradford | 6.2R 1.9/8.2 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | VonKries | 6.0R 1.8/8.3 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | CAT02 | 6.2R 1.8/8.2 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | XYZScaling | 5.9R 1.8/8.5 | very deep red | ✅ | very deep red | ✅ |
| F2_v1 | Bradford | 8.9R 1.9/8.3 | deep reddish brown | ❌ | very deep red | ✅ |
| F2_v1 | VonKries | 8.4R 1.8/8.5 | deep reddish brown | ❌ | very deep red | ✅ |
| F2_v1 | CAT02 | 8.7R 1.9/8.4 | deep reddish brown | ❌ | very deep red | ✅ |
| F2_v1 | XYZScaling | 8.4R 1.8/8.5 | deep reddish brown | ❌ | very deep red | ✅ |
| F7_v1 | Bradford | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | VonKries | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | CAT02 | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | XYZScaling | 5.6R 1.8/7.8 | very deep red | ✅ | very deep red | ✅ |
| F11_v1 | VonKries | 8.6R 1.8/8.7 | deep reddish brown | ❌ | very deep red | ✅ |
| F11_v1 | CAT02 | 9.0R 1.9/8.5 | deep reddish brown | ❌ | very deep red | ✅ |
| F11_v1 | XYZScaling | 8.6R 1.8/8.7 | deep reddish brown | ❌ | very deep red | ✅ |

#### 15. #AB4E52 - Expected: moderate red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.7R 4.4/7.5 | moderate red | ✅ | moderate red | ✅ |
| C_v1 | VonKries | 6.7R 4.4/7.4 | moderate red | ✅ | moderate red | ✅ |
| C_v1 | CAT02 | 6.7R 4.4/7.4 | moderate red | ✅ | moderate red | ✅ |
| C_v1 | XYZScaling | 6.6R 4.4/7.7 | moderate red | ✅ | moderate red | ✅ |
| D75_v1 | XYZScaling | 6.7R 4.4/7.1 | moderate red | ✅ | moderate red | ✅ |

#### 16. #722F37 - Expected: dark red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.5R 2.9/6.3 | dark red | ✅ | dark red | ✅ |
| C_v1 | VonKries | 3.4R 2.9/6.3 | dark red | ✅ | dark red | ✅ |
| C_v1 | CAT02 | 3.5R 2.9/6.3 | dark red | ✅ | dark red | ✅ |
| C_v1 | XYZScaling | 3.2R 2.9/6.6 | dark red | ✅ | dark red | ✅ |
| D65_v1 | Bradford | 4.3R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| D65_v1 | VonKries | 4.3R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| D65_v1 | CAT02 | 4.3R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| D65_v1 | XYZScaling | 4.3R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| D75_v1 | Bradford | 3.1R 2.9/5.9 | dark red | ✅ | dark red | ✅ |
| D75_v1 | VonKries | 3.3R 2.9/5.9 | dark red | ✅ | dark red | ✅ |
| D75_v1 | CAT02 | 3.1R 2.9/5.9 | dark red | ✅ | dark red | ✅ |
| D75_v1 | XYZScaling | 3.1R 2.9/6.0 | dark red | ✅ | dark red | ✅ |
| F2_v1 | Bradford | 9.0R 2.9/7.3 | dark red | ✅ | dark red | ✅ |
| F2_v1 | VonKries | 8.8R 2.9/7.3 | dark red | ✅ | dark red | ✅ |
| F2_v1 | CAT02 | 9.0R 2.9/7.3 | dark red | ✅ | dark red | ✅ |
| F2_v1 | XYZScaling | 8.9R 2.9/7.1 | dark red | ✅ | dark red | ✅ |
| F7_v1 | Bradford | 4.4R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| F7_v1 | VonKries | 4.4R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| F7_v1 | CAT02 | 4.4R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| F7_v1 | XYZScaling | 4.4R 2.9/6.2 | dark red | ✅ | dark red | ✅ |
| F11_v1 | VonKries | 8.8R 2.9/7.5 | dark red | ✅ | dark red | ✅ |
| F11_v1 | CAT02 | 9.0R 2.9/7.5 | dark red | ✅ | dark red | ✅ |
| F11_v1 | XYZScaling | 8.8R 2.9/7.4 | dark red | ✅ | dark red | ✅ |

#### 17. #3F1728 - Expected: very dark red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.4R 1.4/4.1 | very dark red | ✅ | very dark purplish red | ❌ |
| C_v2 | Bradford | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| C_v1 | VonKries | 0.4R 1.4/4.2 | very dark red | ✅ | very dark purplish red | ❌ |
| C_v2 | VonKries | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| C_v1 | CAT02 | 0.5R 1.4/4.1 | very dark red | ✅ | very dark purplish red | ❌ |
| C_v2 | CAT02 | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| C_v1 | XYZScaling | 0.5R 1.4/4.3 | very dark red | ✅ | very dark purplish red | ❌ |
| C_v2 | XYZScaling | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | Bradford | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | VonKries | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | CAT02 | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v1 | XYZScaling | 5.9R 1.4/4.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | XYZScaling | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | Bradford | 4.7R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D55_v2 | Bradford | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | VonKries | 4.6R 1.4/3.8 | very dark red | ✅ | very dark red | ✅ |
| D55_v2 | VonKries | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | CAT02 | 4.7R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D55_v2 | CAT02 | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | XYZScaling | 4.6R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D55_v2 | XYZScaling | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | Bradford | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | Bradford | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | VonKries | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | VonKries | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | CAT02 | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | CAT02 | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | XYZScaling | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | XYZScaling | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | Bradford | 3.6R 1.4/4.2 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | Bradford | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | VonKries | 3.3R 1.4/4.2 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | VonKries | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | CAT02 | 3.5R 1.4/4.2 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | CAT02 | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | XYZScaling | 3.3R 1.4/4.4 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | XYZScaling | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F2_v2 | Bradford | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F2_v2 | VonKries | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F2_v2 | CAT02 | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F2_v2 | XYZScaling | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | Bradford | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | Bradford | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | VonKries | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | VonKries | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | CAT02 | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | CAT02 | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | XYZScaling | 1.8R 1.4/3.9 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | XYZScaling | 2.5R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |
| F11_v2 | VonKries | 5.0R 1.4/2.0 | very dark red | ✅ | very dark red | ✅ |

#### 18. #AD8884 - Expected: light grayish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.6R 5.9/3.1 | light reddish brown | ❌ | light grayish red | ✅ |
| C_v2 | Bradford | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| C_v1 | VonKries | 7.6R 5.9/3.0 | light reddish brown | ❌ | light grayish red | ✅ |
| C_v2 | VonKries | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| C_v1 | CAT02 | 7.6R 5.9/3.0 | light reddish brown | ❌ | light grayish red | ✅ |
| C_v2 | CAT02 | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| C_v1 | XYZScaling | 7.4R 5.9/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| C_v2 | XYZScaling | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | Bradford | 7.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | VonKries | 7.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | CAT02 | 7.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | XYZScaling | 7.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | Bradford | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | VonKries | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | CAT02 | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | XYZScaling | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v2 | Bradford | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v2 | VonKries | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v2 | CAT02 | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v2 | XYZScaling | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | Bradford | 7.9R 5.9/2.3 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | VonKries | 8.0R 5.9/2.3 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | CAT02 | 7.9R 5.9/2.3 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | XYZScaling | 7.8R 5.9/2.4 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v2 | XYZScaling | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v2 | Bradford | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v2 | VonKries | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v2 | CAT02 | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v2 | XYZScaling | 5.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | Bradford | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | VonKries | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | CAT02 | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | XYZScaling | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v2 | Bradford | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v2 | VonKries | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v2 | CAT02 | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v2 | XYZScaling | 2.5R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | Bradford | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | VonKries | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | CAT02 | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | XYZScaling | 10.0R 5.9/2.0 | light grayish red | ✅ | light grayish red | ✅ |

#### 19. #905D5D - Expected: grayish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.7R 4.4/4.0 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | Bradford | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| C_v1 | VonKries | 6.7R 4.4/4.0 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | VonKries | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| C_v1 | CAT02 | 6.7R 4.4/4.0 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | CAT02 | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| C_v1 | XYZScaling | 6.6R 4.4/4.1 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | XYZScaling | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D50_v2 | Bradford | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D50_v2 | VonKries | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D50_v2 | CAT02 | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D50_v2 | XYZScaling | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D55_v2 | Bradford | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D55_v2 | VonKries | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D55_v2 | CAT02 | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D55_v2 | XYZScaling | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| D65_v2 | Bradford | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | VonKries | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | CAT02 | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | XYZScaling | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | Bradford | 6.6R 4.4/3.4 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | Bradford | 2.5R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | VonKries | 6.7R 4.4/3.4 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | VonKries | 2.5R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | CAT02 | 6.6R 4.4/3.4 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | CAT02 | 2.5R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | XYZScaling | 6.6R 4.4/3.5 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | XYZScaling | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| E_v2 | Bradford | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| E_v2 | VonKries | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| E_v2 | CAT02 | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| E_v1 | XYZScaling | 7.9R 4.4/5.0 | moderate reddish brown | ❌ | grayish red | ✅ |
| E_v2 | XYZScaling | 7.5R 4.4/2.0 | grayish reddish brown | ❌ | grayish red | ✅ |
| F7_v2 | Bradford | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | VonKries | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | CAT02 | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | XYZScaling | 5.0R 4.4/2.0 | grayish red | ✅ | grayish red | ✅ |

#### 20. #543D3F - Expected: dark grayish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.6R 2.8/1.9 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v2 | Bradford | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v1 | VonKries | 2.5R 2.8/1.9 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v2 | VonKries | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v1 | CAT02 | 2.6R 2.8/1.9 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v2 | CAT02 | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v1 | XYZScaling | 2.2R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| C_v2 | XYZScaling | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | Bradford | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | VonKries | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | CAT02 | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | XYZScaling | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | Bradford | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | VonKries | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | CAT02 | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | XYZScaling | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | Bradford | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | VonKries | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | CAT02 | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | XYZScaling | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D75_v1 | Bradford | 1.0R 2.8/1.5 | dark grayish red | ✅ | dark grayish red | ✅ |
| D75_v1 | VonKries | 1.3R 2.8/1.5 | dark grayish red | ✅ | dark grayish red | ✅ |
| D75_v1 | CAT02 | 1.1R 2.8/1.5 | dark grayish red | ✅ | dark grayish red | ✅ |
| D75_v1 | XYZScaling | 1.1R 2.8/1.6 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | Bradford | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | VonKries | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | CAT02 | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | XYZScaling | 5.0R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | Bradford | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | VonKries | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | CAT02 | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | XYZScaling | 2.5R 2.8/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |

#### 21. #2E1D21 - Expected: blackish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.0R 1.3/1.4 | blackish red | ✅ | blackish red | ✅ |
| C_v1 | VonKries | 3.9R 1.3/1.4 | blackish red | ✅ | blackish red | ✅ |
| C_v1 | CAT02 | 4.0R 1.3/1.4 | blackish red | ✅ | blackish red | ✅ |
| C_v1 | XYZScaling | 3.9R 1.3/1.5 | blackish red | ✅ | blackish red | ✅ |
| D75_v1 | Bradford | 2.4R 1.3/1.2 | blackish red | ✅ | blackish red | ✅ |
| D75_v1 | VonKries | 2.5R 1.3/1.2 | blackish red | ✅ | blackish red | ✅ |
| D75_v1 | CAT02 | 2.4R 1.3/1.2 | blackish red | ✅ | blackish red | ✅ |
| D75_v1 | XYZScaling | 2.5R 1.3/1.2 | blackish red | ✅ | blackish red | ✅ |

#### 22. #8F817F - Expected: reddish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.2R 5.4/1.2 | reddish gray | ✅ | reddish gray | ✅ |
| C_v1 | VonKries | 8.2R 5.4/1.2 | reddish gray | ✅ | reddish gray | ✅ |
| C_v1 | CAT02 | 8.2R 5.4/1.2 | reddish gray | ✅ | reddish gray | ✅ |
| C_v1 | XYZScaling | 8.0R 5.4/1.2 | reddish gray | ✅ | reddish gray | ✅ |

#### 23. #5C504F - Expected: dark reddish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.5R 3.5/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| C_v1 | VonKries | 6.5R 3.5/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| C_v1 | CAT02 | 6.5R 3.5/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| C_v1 | XYZScaling | 5.7R 3.5/1.0 | dark reddish gray | ✅ | dark reddish gray | ✅ |

#### 24. #282022 - Expected: reddish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.9R 1.3/0.7 | reddish black | ✅ | reddish black | ✅ |
| C_v1 | VonKries | 2.8R 1.3/0.7 | reddish black | ✅ | reddish black | ✅ |
| C_v1 | CAT02 | 2.9R 1.3/0.7 | reddish black | ✅ | reddish black | ✅ |
| C_v1 | XYZScaling | 2.8R 1.3/0.7 | reddish black | ✅ | reddish black | ✅ |
| D65_v1 | Bradford | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| D65_v1 | VonKries | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| D65_v1 | CAT02 | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| D65_v1 | XYZScaling | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| E_v1 | Bradford | 0.4YR 1.3/1.0 | brownish black | ❌ | reddish black | ✅ |
| E_v1 | VonKries | 0.3YR 1.3/1.0 | brownish black | ❌ | reddish black | ✅ |
| E_v1 | CAT02 | 0.4YR 1.3/1.0 | brownish black | ❌ | reddish black | ✅ |
| E_v1 | XYZScaling | 0.2YR 1.3/1.0 | brownish black | ❌ | reddish black | ✅ |
| F7_v1 | Bradford | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| F7_v1 | VonKries | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| F7_v1 | CAT02 | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |
| F7_v1 | XYZScaling | 0.1YR 1.3/0.5 | brownish black | ❌ | reddish black | ✅ |

#### 25. #FFB7A5 - Expected: vivid yellowish pink

No matches

#### 26. #F99379 - Expected: strong yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.8R 7.0/9.2 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| C_v1 | VonKries | 8.8R 7.0/9.2 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| C_v1 | CAT02 | 8.8R 7.0/9.2 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| C_v1 | XYZScaling | 8.6R 7.0/9.5 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D50_v1 | VonKries | 1.6YR 7.0/10.7 | strong orange | ❌ | strong yellowish pink | ✅ |
| D55_v1 | Bradford | 1.6YR 7.1/9.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D55_v1 | VonKries | 1.2YR 7.0/10.0 | strong orange | ❌ | strong yellowish pink | ✅ |
| D55_v1 | CAT02 | 1.7YR 7.1/9.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D55_v1 | XYZScaling | 1.9YR 7.0/9.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | Bradford | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | VonKries | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | CAT02 | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | XYZScaling | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | Bradford | 9.1R 7.0/8.4 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | VonKries | 9.4R 7.0/8.2 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | CAT02 | 9.1R 7.0/8.4 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | XYZScaling | 9.0R 7.0/8.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | Bradford | 9.5R 7.1/10.5 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | VonKries | 9.2R 7.0/10.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | CAT02 | 9.5R 7.1/10.5 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | XYZScaling | 9.1R 7.0/10.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | Bradford | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | VonKries | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | CAT02 | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | XYZScaling | 0.4YR 7.0/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |

#### 27. #E66721 - Expected: deep yellowish pink

No matches

#### 28. #F4C2C2 - Expected: light yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 5.0YR 8.3/5.1 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D50_v1 | VonKries | 4.7YR 8.2/5.2 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D50_v1 | CAT02 | 5.0YR 8.3/5.1 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D50_v1 | XYZScaling | 5.3YR 8.2/5.0 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D55_v1 | Bradford | 3.2YR 8.2/4.4 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D55_v1 | VonKries | 3.0YR 8.2/4.5 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D55_v1 | CAT02 | 3.2YR 8.2/4.4 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D55_v1 | XYZScaling | 3.3YR 8.2/4.4 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | Bradford | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | VonKries | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | CAT02 | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | XYZScaling | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | Bradford | 8.4R 8.3/5.2 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | VonKries | 8.3R 8.2/5.2 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | CAT02 | 8.4R 8.2/5.2 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | XYZScaling | 8.2R 8.2/5.2 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | Bradford | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | VonKries | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | CAT02 | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | XYZScaling | 8.7R 8.2/3.7 | light yellowish pink | ✅ | light yellowish pink | ✅ |

#### 29. #D9A6A9 - Expected: moderate yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.5R 7.2/3.9 | moderate yellowish pink | ✅ | moderate pink | ❌ |
| C_v1 | VonKries | 5.5R 7.2/3.9 | moderate yellowish pink | ✅ | moderate pink | ❌ |
| C_v1 | CAT02 | 5.5R 7.2/3.9 | moderate yellowish pink | ✅ | moderate pink | ❌ |
| C_v1 | XYZScaling | 5.4R 7.2/4.0 | moderate yellowish pink | ✅ | moderate pink | ❌ |
| D50_v1 | Bradford | 3.1YR 7.2/5.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D50_v1 | VonKries | 2.9YR 7.2/5.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D50_v1 | CAT02 | 3.1YR 7.2/5.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D50_v1 | XYZScaling | 3.3YR 7.2/5.1 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | Bradford | 1.1YR 7.2/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | VonKries | 1.0YR 7.2/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | CAT02 | 1.1YR 7.2/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | XYZScaling | 1.2YR 7.2/4.6 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | Bradford | 7.7R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | VonKries | 7.7R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | CAT02 | 7.7R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | XYZScaling | 7.7R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D75_v1 | VonKries | 5.0R 7.2/3.1 | moderate yellowish pink | ✅ | moderate pink | ❌ |
| E_v1 | Bradford | 7.8R 7.2/5.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | VonKries | 7.7R 7.2/5.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | CAT02 | 7.8R 7.2/5.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | XYZScaling | 7.6R 7.2/5.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | Bradford | 7.8R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | VonKries | 7.8R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | CAT02 | 7.8R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | XYZScaling | 7.8R 7.2/3.8 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |

#### 30. #C48379 - Expected: dark yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 7.9R 6.0/5.8 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |

#### 31. #ECD5C5 - Expected: pale yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| A_v2 | VonKries | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| A_v2 | CAT02 | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| A_v2 | XYZScaling | 5.0YR 8.6/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| C_v1 | Bradford | 6.7YR 8.6/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| C_v1 | VonKries | 6.9YR 8.6/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| C_v1 | CAT02 | 6.6YR 8.6/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| C_v1 | XYZScaling | 6.2YR 8.6/2.1 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| D75_v1 | Bradford | 5.6YR 8.6/1.5 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | Bradford | 2.5YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | VonKries | 2.5YR 8.6/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | CAT02 | 2.5YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |

#### 32. #C7ADA3 - Expected: grayish yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0YR 7.2/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| A_v2 | VonKries | 5.0YR 7.2/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| A_v2 | CAT02 | 5.0YR 7.2/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| A_v2 | XYZScaling | 5.0YR 7.2/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| C_v1 | Bradford | 2.2YR 7.2/2.3 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| C_v1 | VonKries | 2.4YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| C_v1 | CAT02 | 2.1YR 7.2/2.3 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| C_v1 | XYZScaling | 1.5YR 7.2/2.4 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | Bradford | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | VonKries | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | CAT02 | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | Bradford | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | VonKries | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | CAT02 | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | XYZScaling | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |

#### 33. #C2AC99 - Expected: brownish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 7.5YR 7.2/2.0 | brownish pink | ✅ | brownish pink | ✅ |
| A_v2 | VonKries | 7.5YR 7.1/2.0 | brownish pink | ✅ | brownish pink | ✅ |
| A_v2 | CAT02 | 7.5YR 7.2/2.0 | brownish pink | ✅ | brownish pink | ✅ |
| A_v2 | XYZScaling | 7.5YR 7.1/2.0 | brownish pink | ✅ | brownish pink | ✅ |

#### 34. #E25822 - Expected: vivid reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 9.9R 5.7/18.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| A_v1 | VonKries | 9.0R 5.5/19.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| A_v1 | CAT02 | 10.0R 5.7/18.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| A_v1 | XYZScaling | 9.4R 5.4/18.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | Bradford | 0.3YR 5.4/13.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | VonKries | 0.3YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | CAT02 | 0.2YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | XYZScaling | 9.8R 5.4/14.2 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | Bradford | 0.8YR 5.5/15.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | VonKries | 0.4YR 5.4/15.2 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | CAT02 | 0.8YR 5.5/15.2 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | XYZScaling | 1.0YR 5.4/14.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | Bradford | 0.8YR 5.5/14.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | VonKries | 0.5YR 5.4/14.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | CAT02 | 0.8YR 5.5/14.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | XYZScaling | 1.0YR 5.4/14.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | Bradford | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | VonKries | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | CAT02 | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | XYZScaling | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | Bradford | 0.7YR 5.4/13.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | VonKries | 0.9YR 5.4/13.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | CAT02 | 0.6YR 5.4/13.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | XYZScaling | 0.5YR 5.4/13.4 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | Bradford | 0.2YR 5.5/14.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | VonKries | 9.9R 5.4/14.9 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | CAT02 | 0.2YR 5.5/14.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | XYZScaling | 9.8R 5.4/15.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | Bradford | 0.6YR 5.6/16.2 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | VonKries | 9.9R 5.4/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | CAT02 | 0.6YR 5.6/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | XYZScaling | 0.7YR 5.4/15.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | Bradford | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | VonKries | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | CAT02 | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | XYZScaling | 0.8YR 5.4/13.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | Bradford | 0.4YR 5.6/16.5 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | VonKries | 9.7R 5.5/16.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | CAT02 | 0.5YR 5.6/16.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | XYZScaling | 0.3YR 5.4/16.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |

#### 35. #D9603B - Expected: strong reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.7R 5.5/11.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| C_v1 | VonKries | 9.7R 5.4/11.5 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| C_v1 | CAT02 | 9.7R 5.4/11.5 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| C_v1 | XYZScaling | 9.2R 5.4/12.0 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D50_v1 | Bradford | 0.9YR 5.5/12.9 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D50_v1 | VonKries | 0.5YR 5.5/13.0 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D50_v1 | CAT02 | 1.0YR 5.5/12.9 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D50_v1 | XYZScaling | 1.2YR 5.4/12.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | Bradford | 0.8YR 5.5/12.2 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | VonKries | 0.5YR 5.5/12.3 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | CAT02 | 0.8YR 5.5/12.3 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | XYZScaling | 1.0YR 5.4/12.0 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | Bradford | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | VonKries | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | CAT02 | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | XYZScaling | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D75_v1 | XYZScaling | 9.9R 5.4/11.1 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| E_v1 | Bradford | 9.9R 5.5/12.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| E_v1 | VonKries | 9.6R 5.5/12.7 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| E_v1 | CAT02 | 9.9R 5.5/12.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| E_v1 | XYZScaling | 9.5R 5.4/12.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | Bradford | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | VonKries | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | CAT02 | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | XYZScaling | 0.5YR 5.4/11.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |

#### 36. #AA381E - Expected: deep reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.6R 4.0/11.3 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| C_v1 | VonKries | 9.6R 4.0/11.2 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| C_v1 | CAT02 | 9.6R 4.0/11.3 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| C_v1 | XYZScaling | 9.1R 4.0/11.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D50_v1 | Bradford | 0.4YR 4.0/12.2 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D50_v1 | VonKries | 0.1YR 4.0/12.2 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D50_v1 | CAT02 | 0.4YR 4.0/12.2 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D50_v1 | XYZScaling | 0.6YR 4.0/11.8 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | Bradford | 0.3YR 4.0/11.8 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | VonKries | 0.1YR 4.0/11.8 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | CAT02 | 0.3YR 4.0/11.8 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | XYZScaling | 0.5YR 4.0/11.5 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | Bradford | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | VonKries | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | CAT02 | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | XYZScaling | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| E_v1 | Bradford | 9.7R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| E_v1 | VonKries | 9.4R 4.0/12.2 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| E_v1 | CAT02 | 9.7R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| E_v1 | XYZScaling | 9.3R 4.0/12.3 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F2_v1 | Bradford | 0.4YR 4.1/12.9 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F2_v1 | XYZScaling | 0.4YR 4.0/12.6 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | Bradford | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | VonKries | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | CAT02 | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | XYZScaling | 0.2YR 4.0/11.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F11_v1 | XYZScaling | 0.2YR 4.0/12.9 | deep reddish orange | ✅ | deep reddish orange | ✅ |

#### 37. #CB6D51 - Expected: moderate reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.9R 5.5/8.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| C_v1 | VonKries | 9.9R 5.5/8.7 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| C_v1 | CAT02 | 9.8R 5.5/8.7 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| C_v1 | XYZScaling | 9.3R 5.5/9.1 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D50_v1 | VonKries | 1.9YR 5.5/10.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D55_v1 | VonKries | 1.8YR 5.5/9.4 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | Bradford | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | VonKries | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | CAT02 | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | XYZScaling | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | Bradford | 0.5YR 5.5/8.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | VonKries | 0.8YR 5.5/7.9 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | CAT02 | 0.5YR 5.5/8.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | XYZScaling | 0.2YR 5.5/8.3 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | Bradford | 0.4YR 5.6/9.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | VonKries | 0.1YR 5.5/9.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | CAT02 | 0.4YR 5.6/9.7 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | XYZScaling | 9.9R 5.5/9.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | Bradford | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | VonKries | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | CAT02 | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | XYZScaling | 1.4YR 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |

#### 38. #9E4732 - Expected: dark reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.9R 4.1/8.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| C_v1 | VonKries | 9.9R 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| C_v1 | CAT02 | 9.8R 4.0/8.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| C_v1 | XYZScaling | 9.3R 4.0/8.7 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D50_v1 | Bradford | 1.4YR 4.1/9.4 | strong brown | ❌ | dark reddish orange | ✅ |
| D50_v1 | VonKries | 1.1YR 4.1/9.5 | strong brown | ❌ | dark reddish orange | ✅ |
| D50_v1 | CAT02 | 1.4YR 4.1/9.4 | strong brown | ❌ | dark reddish orange | ✅ |
| D50_v1 | XYZScaling | 1.6YR 4.0/9.1 | strong brown | ❌ | dark reddish orange | ✅ |
| D55_v1 | Bradford | 1.3YR 4.1/9.0 | strong brown | ❌ | dark reddish orange | ✅ |
| D55_v1 | VonKries | 1.1YR 4.1/9.0 | strong brown | ❌ | dark reddish orange | ✅ |
| D55_v1 | CAT02 | 1.3YR 4.1/9.0 | strong brown | ❌ | dark reddish orange | ✅ |
| D55_v1 | XYZScaling | 1.4YR 4.0/8.8 | strong brown | ❌ | dark reddish orange | ✅ |
| D65_v1 | Bradford | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | VonKries | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | CAT02 | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | XYZScaling | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | Bradford | 0.2YR 4.0/7.8 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | VonKries | 0.5YR 4.0/7.7 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | CAT02 | 0.2YR 4.0/7.8 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | XYZScaling | 0.0YR 4.0/8.0 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | Bradford | 0.4YR 4.1/9.2 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | VonKries | 0.1YR 4.1/9.2 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | CAT02 | 0.4YR 4.1/9.2 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | XYZScaling | 9.9R 4.0/9.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F2_v1 | Bradford | 1.4YR 4.1/10.3 | strong brown | ❌ | dark reddish orange | ✅ |
| F2_v1 | VonKries | 1.0YR 4.1/10.5 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F2_v1 | CAT02 | 1.5YR 4.1/10.4 | strong brown | ❌ | dark reddish orange | ✅ |
| F2_v1 | XYZScaling | 1.5YR 4.0/10.0 | strong brown | ❌ | dark reddish orange | ✅ |
| F7_v1 | Bradford | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | VonKries | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | CAT02 | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | XYZScaling | 0.9YR 4.0/8.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F11_v1 | Bradford | 1.3YR 4.1/10.7 | strong brown | ❌ | dark reddish orange | ✅ |
| F11_v1 | VonKries | 0.8YR 4.1/10.8 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F11_v1 | CAT02 | 1.4YR 4.1/10.7 | strong brown | ❌ | dark reddish orange | ✅ |
| F11_v1 | XYZScaling | 1.3YR 4.0/10.4 | strong brown | ❌ | dark reddish orange | ✅ |

#### 39. #B4745E - Expected: grayish reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.2YR 5.4/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| C_v1 | VonKries | 1.3YR 5.4/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| C_v1 | CAT02 | 1.1YR 5.4/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| C_v1 | XYZScaling | 0.5YR 5.4/6.0 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | Bradford | 2.6YR 5.4/5.0 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | CAT02 | 2.5YR 5.4/5.0 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | XYZScaling | 2.1YR 5.4/5.2 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| E_v1 | Bradford | 2.3YR 5.4/6.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| E_v1 | VonKries | 1.9YR 5.4/6.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| E_v1 | CAT02 | 2.4YR 5.4/6.7 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| E_v1 | XYZScaling | 1.9YR 5.4/6.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |

#### 40. #882D17 - Expected: strong reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 1.1YR 3.4/12.2 | strong brown | ❌ | strong reddish brown | ✅ |
| A_v1 | VonKries | 0.7YR 3.2/12.4 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| A_v1 | CAT02 | 1.1YR 3.4/12.3 | strong brown | ❌ | strong reddish brown | ✅ |
| A_v1 | XYZScaling | 0.8YR 3.2/12.1 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | Bradford | 0.9YR 3.2/9.0 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | VonKries | 0.9YR 3.2/9.0 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | CAT02 | 0.9YR 3.2/9.0 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | XYZScaling | 0.7YR 3.2/9.2 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D50_v1 | Bradford | 1.2YR 3.2/9.9 | strong brown | ❌ | strong reddish brown | ✅ |
| D50_v1 | VonKries | 1.0YR 3.2/9.9 | strong brown | ❌ | strong reddish brown | ✅ |
| D50_v1 | CAT02 | 1.3YR 3.2/9.9 | strong brown | ❌ | strong reddish brown | ✅ |
| D50_v1 | XYZScaling | 1.3YR 3.2/9.7 | strong brown | ❌ | strong reddish brown | ✅ |
| D55_v1 | Bradford | 1.2YR 3.2/9.6 | strong brown | ❌ | strong reddish brown | ✅ |
| D55_v1 | VonKries | 1.1YR 3.2/9.6 | strong brown | ❌ | strong reddish brown | ✅ |
| D55_v1 | CAT02 | 1.2YR 3.2/9.6 | strong brown | ❌ | strong reddish brown | ✅ |
| D55_v1 | XYZScaling | 1.3YR 3.2/9.4 | strong brown | ❌ | strong reddish brown | ✅ |
| D65_v1 | Bradford | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| D65_v1 | VonKries | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| D65_v1 | CAT02 | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| D65_v1 | XYZScaling | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| D75_v1 | Bradford | 1.0YR 3.2/8.6 | strong brown | ❌ | strong reddish brown | ✅ |
| D75_v1 | VonKries | 1.1YR 3.2/8.6 | strong brown | ❌ | strong reddish brown | ✅ |
| D75_v1 | CAT02 | 1.0YR 3.2/8.6 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D75_v1 | XYZScaling | 1.0YR 3.2/8.8 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | Bradford | 0.9YR 3.2/9.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | VonKries | 0.9YR 3.2/9.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | CAT02 | 0.9YR 3.2/9.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | XYZScaling | 0.8YR 3.2/9.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F2_v1 | Bradford | 1.3YR 3.3/10.5 | strong brown | ❌ | strong reddish brown | ✅ |
| F2_v1 | VonKries | 1.0YR 3.2/10.6 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F2_v1 | CAT02 | 1.3YR 3.3/10.6 | strong brown | ❌ | strong reddish brown | ✅ |
| F2_v1 | XYZScaling | 1.2YR 3.2/10.2 | strong brown | ❌ | strong reddish brown | ✅ |
| F7_v1 | Bradford | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| F7_v1 | VonKries | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| F7_v1 | CAT02 | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| F7_v1 | XYZScaling | 1.1YR 3.2/9.0 | strong brown | ❌ | strong reddish brown | ✅ |
| F11_v1 | Bradford | 1.2YR 3.3/10.7 | strong brown | ❌ | strong reddish brown | ✅ |
| F11_v1 | VonKries | 0.9YR 3.2/10.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F11_v1 | CAT02 | 1.3YR 3.3/10.8 | strong brown | ❌ | strong reddish brown | ✅ |
| F11_v1 | XYZScaling | 1.1YR 3.2/10.5 | strong brown | ❌ | strong reddish brown | ✅ |

#### 41. #56070C - Expected: deep reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 0.2YR 1.8/10.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| A_v1 | VonKries | 0.1YR 1.6/10.6 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| A_v1 | CAT02 | 0.2YR 1.8/10.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| A_v1 | XYZScaling | 0.1YR 1.6/10.6 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | Bradford | 10.0R 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | VonKries | 10.0R 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | CAT02 | 10.0R 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | XYZScaling | 9.9R 1.6/8.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | Bradford | 0.3YR 1.6/8.6 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | VonKries | 0.2YR 1.6/8.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | CAT02 | 0.3YR 1.6/8.6 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | XYZScaling | 0.3YR 1.6/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | Bradford | 0.2YR 1.6/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | VonKries | 0.2YR 1.6/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | CAT02 | 0.2YR 1.6/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | XYZScaling | 0.2YR 1.6/8.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | Bradford | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | VonKries | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | CAT02 | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | XYZScaling | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | Bradford | 10.0R 1.6/7.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | VonKries | 0.0YR 1.6/7.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | CAT02 | 10.0R 1.6/7.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | XYZScaling | 10.0R 1.6/7.8 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | Bradford | 0.1YR 1.6/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | VonKries | 0.0YR 1.6/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | CAT02 | 0.1YR 1.6/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | XYZScaling | 10.0R 1.6/8.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | Bradford | 0.2YR 1.7/9.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | VonKries | 0.2YR 1.6/9.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | CAT02 | 0.2YR 1.7/9.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | XYZScaling | 0.2YR 1.6/9.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | Bradford | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | VonKries | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | CAT02 | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | XYZScaling | 0.1YR 1.6/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | Bradford | 0.2YR 1.7/9.3 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | VonKries | 0.2YR 1.6/9.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | CAT02 | 0.2YR 1.7/9.3 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | XYZScaling | 0.2YR 1.6/9.3 | deep reddish brown | ✅ | deep reddish brown | ✅ |

#### 42. #A87C6D - Expected: light reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.5YR 5.5/3.9 | light reddish brown | ✅ | light reddish brown | ✅ |
| C_v1 | VonKries | 1.6YR 5.5/3.8 | light reddish brown | ✅ | light reddish brown | ✅ |
| C_v1 | CAT02 | 1.4YR 5.5/3.9 | light reddish brown | ✅ | light reddish brown | ✅ |
| C_v1 | XYZScaling | 0.8YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| D75_v1 | XYZScaling | 2.9YR 5.5/3.2 | light reddish brown | ✅ | light reddish brown | ✅ |

#### 43. #79443B - Expected: moderate reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.2R 3.5/4.7 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| C_v1 | VonKries | 9.2R 3.5/4.7 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| C_v1 | CAT02 | 9.1R 3.5/4.7 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| C_v1 | XYZScaling | 8.8R 3.4/4.8 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D55_v1 | XYZScaling | 2.6YR 3.4/5.0 | moderate brown | ❌ | moderate reddish brown | ✅ |
| D65_v1 | Bradford | 1.2YR 3.4/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | VonKries | 1.2YR 3.4/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | CAT02 | 1.2YR 3.4/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | XYZScaling | 1.2YR 3.4/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | Bradford | 9.7R 3.4/4.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | VonKries | 0.1YR 3.4/4.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | CAT02 | 9.7R 3.4/4.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | XYZScaling | 9.4R 3.4/4.3 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | Bradford | 0.9YR 3.5/5.3 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | VonKries | 0.5YR 3.5/5.4 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | CAT02 | 0.9YR 3.5/5.3 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | XYZScaling | 0.3YR 3.4/5.4 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | Bradford | 1.2YR 3.5/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | VonKries | 1.2YR 3.5/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | CAT02 | 1.2YR 3.5/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | XYZScaling | 1.2YR 3.4/4.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |

#### 44. #3E1D1E - Expected: dark reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 9.1R 1.5/3.1 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | Bradford | 0.8YR 1.5/3.7 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | VonKries | 0.7YR 1.5/3.7 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | CAT02 | 0.8YR 1.5/3.7 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | XYZScaling | 0.8YR 1.5/3.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | Bradford | 0.5YR 1.5/3.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | VonKries | 0.4YR 1.5/3.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | CAT02 | 0.5YR 1.5/3.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | XYZScaling | 0.5YR 1.5/3.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | Bradford | 9.9R 1.5/3.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | VonKries | 9.8R 1.5/3.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | CAT02 | 9.9R 1.5/3.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | XYZScaling | 9.8R 1.5/3.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F2_v1 | Bradford | 1.0YR 1.5/4.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F2_v1 | VonKries | 0.9YR 1.5/4.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F2_v1 | CAT02 | 1.0YR 1.5/4.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F2_v1 | XYZScaling | 1.0YR 1.5/4.2 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F11_v1 | Bradford | 1.0YR 1.6/4.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F11_v1 | VonKries | 0.9YR 1.5/4.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F11_v1 | CAT02 | 1.0YR 1.6/4.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F11_v1 | XYZScaling | 0.9YR 1.5/4.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |

#### 45. #977F73 - Expected: light grayish reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 5.5/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| A_v2 | VonKries | 2.5YR 5.4/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| A_v2 | CAT02 | 2.5YR 5.5/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| A_v2 | XYZScaling | 2.5YR 5.4/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| C_v1 | XYZScaling | 4.9YR 5.4/2.1 | light grayish brown | ❌ | light grayish reddish brown | ✅ |

#### 46. #674C47 - Expected: grayish reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 3.5/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| A_v2 | VonKries | 2.5YR 3.5/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| A_v2 | CAT02 | 2.5YR 3.5/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| A_v2 | XYZScaling | 2.5YR 3.4/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| C_v1 | Bradford | 9.7R 3.4/2.1 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| C_v1 | VonKries | 9.8R 3.4/2.1 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| C_v1 | CAT02 | 9.7R 3.4/2.1 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| C_v1 | XYZScaling | 9.0R 3.4/2.2 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D50_v2 | Bradford | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D50_v2 | VonKries | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D50_v2 | CAT02 | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D50_v2 | XYZScaling | 7.5R 3.4/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D55_v2 | Bradford | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D55_v2 | VonKries | 7.5R 3.4/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D55_v2 | CAT02 | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D55_v2 | XYZScaling | 7.5R 3.4/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D75_v1 | Bradford | 1.0YR 3.4/1.7 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D75_v1 | VonKries | 1.2YR 3.4/1.7 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D75_v1 | CAT02 | 0.9YR 3.4/1.7 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D75_v1 | XYZScaling | 0.6YR 3.4/1.7 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| E_v1 | Bradford | 2.7YR 3.5/2.8 | moderate brown | ❌ | grayish reddish brown | ✅ |
| E_v1 | VonKries | 2.4YR 3.5/2.8 | moderate brown | ❌ | grayish reddish brown | ✅ |
| E_v1 | CAT02 | 2.7YR 3.5/2.8 | moderate brown | ❌ | grayish reddish brown | ✅ |
| E_v1 | XYZScaling | 2.3YR 3.4/2.8 | moderate brown | ❌ | grayish reddish brown | ✅ |
| F2_v2 | Bradford | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F2_v2 | VonKries | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F2_v2 | CAT02 | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F2_v2 | XYZScaling | 10.0R 3.4/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | Bradford | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | VonKries | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | CAT02 | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | XYZScaling | 10.0R 3.4/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |

#### 47. #43302E - Expected: dark grayish reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 2.2/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| A_v2 | VonKries | 2.5YR 2.2/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| A_v2 | CAT02 | 2.5YR 2.2/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| A_v2 | XYZScaling | 2.5YR 2.2/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| C_v1 | Bradford | 9.3R 2.2/1.7 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| C_v1 | VonKries | 9.3R 2.2/1.7 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| C_v1 | CAT02 | 9.3R 2.2/1.7 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| C_v1 | XYZScaling | 9.3R 2.2/1.7 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | Bradford | 7.5R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | VonKries | 7.5R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | CAT02 | 7.5R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | XYZScaling | 7.5R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | Bradford | 9.6R 2.2/1.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | VonKries | 9.7R 2.2/1.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | CAT02 | 9.6R 2.2/1.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | XYZScaling | 9.5R 2.2/1.4 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v1 | XYZScaling | 0.6YR 2.2/2.4 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | Bradford | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | VonKries | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | CAT02 | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | XYZScaling | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | Bradford | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | VonKries | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | CAT02 | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | XYZScaling | 10.0R 2.2/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |

#### 48. #F38400 - Expected: vivid orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 2.3YR 6.8/19.7 | vivid orange | ✅ | vivid orange | ✅ |
| A_v1 | CAT02 | 2.5YR 6.8/20.3 | vivid orange | ✅ | vivid orange | ✅ |
| A_v1 | XYZScaling | 2.7YR 6.5/18.8 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | Bradford | 5.9YR 6.6/15.1 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | VonKries | 5.3YR 6.5/15.3 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | CAT02 | 6.1YR 6.6/15.3 | vivid orange yellow | ❌ | vivid orange | ✅ |
| D50_v1 | XYZScaling | 6.8YR 6.5/14.7 | vivid orange yellow | ❌ | vivid orange | ✅ |
| D55_v1 | Bradford | 6.4YR 6.6/14.5 | vivid orange yellow | ❌ | vivid orange | ✅ |
| D55_v1 | VonKries | 6.0YR 6.5/14.6 | vivid orange | ✅ | vivid orange | ✅ |
| D55_v1 | CAT02 | 6.5YR 6.6/14.6 | vivid orange yellow | ❌ | vivid orange | ✅ |
| D55_v1 | XYZScaling | 6.9YR 6.5/14.2 | vivid orange yellow | ❌ | vivid orange | ✅ |
| E_v1 | Bradford | 5.3YR 6.6/14.8 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | VonKries | 5.0YR 6.5/14.8 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | CAT02 | 5.3YR 6.6/14.8 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | XYZScaling | 5.1YR 6.5/14.7 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | Bradford | 4.8YR 6.6/16.4 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | VonKries | 4.0YR 6.5/16.6 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | CAT02 | 5.0YR 6.7/16.8 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | XYZScaling | 5.8YR 6.5/15.7 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | Bradford | 4.3YR 6.7/16.8 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | VonKries | 3.4YR 6.5/17.1 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | CAT02 | 4.5YR 6.7/17.2 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | XYZScaling | 5.2YR 6.5/16.1 | vivid orange | ✅ | vivid orange | ✅ |

#### 49. #FD943F - Expected: brilliant orange

No matches

#### 50. #ED872D - Expected: strong orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.3YR 6.5/11.6 | strong orange | ✅ | strong orange | ✅ |
| C_v1 | VonKries | 6.5YR 6.5/11.5 | strong orange | ✅ | strong orange | ✅ |
| C_v1 | CAT02 | 6.3YR 6.5/11.5 | strong orange | ✅ | strong orange | ✅ |
| C_v1 | XYZScaling | 5.7YR 6.5/11.8 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | Bradford | 6.4YR 6.6/13.2 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | VonKries | 5.8YR 6.5/13.4 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | CAT02 | 6.5YR 6.6/13.4 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | Bradford | 6.7YR 6.6/12.6 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | VonKries | 6.4YR 6.5/12.7 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | CAT02 | 6.8YR 6.6/12.7 | strong orange | ✅ | strong orange | ✅ |
| D75_v1 | XYZScaling | 7.0YR 6.5/11.1 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | Bradford | 5.5YR 6.6/12.9 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | VonKries | 5.2YR 6.5/12.8 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | CAT02 | 5.5YR 6.6/12.9 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | XYZScaling | 5.3YR 6.5/12.8 | strong orange | ✅ | strong orange | ✅ |
| F2_v1 | XYZScaling | 6.3YR 6.5/13.9 | strong orange | ✅ | strong orange | ✅ |

#### 51. #BE6516 - Expected: deep orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.2YR 5.1/10.6 | strong yellowish brown | ❌ | deep orange | ✅ |
| C_v1 | VonKries | 6.4YR 5.1/10.5 | strong yellowish brown | ❌ | deep orange | ✅ |
| C_v1 | CAT02 | 6.2YR 5.1/10.5 | strong yellowish brown | ❌ | deep orange | ✅ |
| C_v1 | XYZScaling | 5.6YR 5.1/10.8 | deep orange | ✅ | deep orange | ✅ |
| D50_v1 | Bradford | 6.1YR 5.2/11.9 | strong yellowish brown | ❌ | deep orange | ✅ |
| D50_v1 | VonKries | 5.5YR 5.1/12.1 | deep orange | ✅ | deep orange | ✅ |
| D50_v1 | CAT02 | 6.2YR 5.2/12.1 | strong yellowish brown | ❌ | deep orange | ✅ |
| D50_v1 | XYZScaling | 6.9YR 5.1/11.6 | strong yellowish brown | ❌ | deep orange | ✅ |
| D55_v1 | Bradford | 6.5YR 5.2/11.4 | strong yellowish brown | ❌ | deep orange | ✅ |
| D55_v1 | VonKries | 6.1YR 5.1/11.5 | strong yellowish brown | ❌ | deep orange | ✅ |
| D55_v1 | CAT02 | 6.6YR 5.2/11.5 | strong yellowish brown | ❌ | deep orange | ✅ |
| D75_v1 | XYZScaling | 6.8YR 5.1/10.2 | strong yellowish brown | ❌ | deep orange | ✅ |
| E_v1 | Bradford | 5.3YR 5.2/11.7 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | VonKries | 5.0YR 5.1/11.7 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | CAT02 | 5.4YR 5.2/11.7 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | XYZScaling | 5.1YR 5.1/11.6 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | Bradford | 5.1YR 5.2/13.1 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | VonKries | 4.2YR 5.1/13.3 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | CAT02 | 5.3YR 5.2/13.3 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | XYZScaling | 6.0YR 5.1/12.5 | strong yellowish brown | ❌ | deep orange | ✅ |
| F11_v1 | Bradford | 4.6YR 5.2/13.4 | deep orange | ✅ | deep orange | ✅ |
| F11_v1 | VonKries | 3.6YR 5.1/13.6 | deep orange | ✅ | deep orange | ✅ |
| F11_v1 | CAT02 | 4.8YR 5.2/13.6 | deep orange | ✅ | deep orange | ✅ |
| F11_v1 | XYZScaling | 5.3YR 5.1/12.9 | deep orange | ✅ | deep orange | ✅ |

#### 52. #FAB57F - Expected: light orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | VonKries | 6.9YR 7.8/8.2 | light orange | ✅ | light orange | ✅ |

#### 53. #D99058 - Expected: moderate orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 6.8YR 6.5/7.7 | moderate orange yellow | ❌ | moderate orange | ✅ |
| E_v1 | Bradford | 6.8YR 6.5/8.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| E_v1 | VonKries | 6.6YR 6.5/8.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| E_v1 | CAT02 | 6.8YR 6.5/8.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| E_v1 | XYZScaling | 6.7YR 6.5/8.7 | moderate orange yellow | ❌ | moderate orange | ✅ |

#### 54. #AE6938 - Expected: brownish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.9YR 5.0/7.3 | strong yellowish brown | ❌ | brownish orange | ✅ |
| C_v1 | CAT02 | 6.8YR 5.0/7.2 | strong yellowish brown | ❌ | brownish orange | ✅ |
| C_v1 | XYZScaling | 6.2YR 5.0/7.5 | strong yellowish brown | ❌ | brownish orange | ✅ |
| E_v1 | Bradford | 6.3YR 5.1/8.3 | strong yellowish brown | ❌ | brownish orange | ✅ |
| E_v1 | VonKries | 6.0YR 5.0/8.3 | strong yellowish brown | ❌ | brownish orange | ✅ |
| E_v1 | CAT02 | 6.3YR 5.0/8.3 | strong yellowish brown | ❌ | brownish orange | ✅ |
| E_v1 | XYZScaling | 6.1YR 5.0/8.3 | strong yellowish brown | ❌ | brownish orange | ✅ |
| F2_v1 | Bradford | 6.8YR 5.1/9.9 | strong yellowish brown | ❌ | brownish orange | ✅ |

#### 55. #80461B - Expected: strong brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.9YR 3.7/10.7 | strong brown | ✅ | strong brown | ✅ |
| A_v1 | VonKries | 2.8YR 3.6/10.8 | strong brown | ✅ | strong brown | ✅ |
| A_v1 | CAT02 | 4.1YR 3.7/10.8 | strong brown | ✅ | strong brown | ✅ |
| A_v1 | XYZScaling | 4.3YR 3.6/10.1 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | Bradford | 6.7YR 3.6/6.8 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | VonKries | 6.8YR 3.6/6.7 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | CAT02 | 6.6YR 3.5/6.7 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | XYZScaling | 6.1YR 3.6/6.9 | strong brown | ✅ | strong brown | ✅ |
| D50_v1 | Bradford | 7.0YR 3.6/7.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| D50_v1 | VonKries | 6.5YR 3.6/7.8 | strong brown | ✅ | strong brown | ✅ |
| D50_v1 | CAT02 | 7.1YR 3.6/7.8 | strong yellowish brown | ❌ | strong brown | ✅ |
| D50_v1 | XYZScaling | 7.7YR 3.6/7.5 | strong yellowish brown | ❌ | strong brown | ✅ |
| D55_v1 | Bradford | 7.3YR 3.6/7.4 | strong yellowish brown | ❌ | strong brown | ✅ |
| D55_v1 | VonKries | 7.0YR 3.6/7.4 | strong brown | ✅ | strong brown | ✅ |
| D55_v1 | CAT02 | 7.4YR 3.6/7.4 | strong yellowish brown | ❌ | strong brown | ✅ |
| D55_v1 | XYZScaling | 7.8YR 3.6/7.2 | strong yellowish brown | ❌ | strong brown | ✅ |
| D65_v1 | Bradford | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| D65_v1 | VonKries | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| D65_v1 | CAT02 | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| D65_v1 | XYZScaling | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| D75_v1 | Bradford | 7.7YR 3.5/6.3 | strong yellowish brown | ❌ | strong brown | ✅ |
| D75_v1 | CAT02 | 7.7YR 3.5/6.3 | strong yellowish brown | ❌ | strong brown | ✅ |
| D75_v1 | XYZScaling | 7.3YR 3.6/6.5 | strong yellowish brown | ❌ | strong brown | ✅ |
| E_v1 | Bradford | 6.1YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | VonKries | 5.8YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | CAT02 | 6.1YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | XYZScaling | 5.8YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | Bradford | 6.2YR 3.6/8.6 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | VonKries | 5.4YR 3.6/8.7 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | CAT02 | 6.4YR 3.6/8.6 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | XYZScaling | 7.0YR 3.6/8.1 | strong yellowish brown | ❌ | strong brown | ✅ |
| F7_v1 | Bradford | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| F7_v1 | VonKries | 7.6YR 3.6/6.8 | strong yellowish brown | ❌ | strong brown | ✅ |
| F7_v1 | CAT02 | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| F7_v1 | XYZScaling | 7.6YR 3.6/6.7 | strong yellowish brown | ❌ | strong brown | ✅ |
| F11_v1 | Bradford | 5.8YR 3.6/8.8 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | VonKries | 4.9YR 3.6/8.9 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | CAT02 | 5.9YR 3.6/8.9 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | XYZScaling | 6.4YR 3.6/8.4 | strong brown | ✅ | strong brown | ✅ |

#### 56. #593319 - Expected: deep brown

No matches

#### 57. #A67B5B - Expected: light brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 8.0YR 5.4/4.4 | moderate yellowish brown | ❌ | light brown | ✅ |
| E_v1 | VonKries | 8.0YR 5.4/5.3 | strong yellowish brown | ❌ | light brown | ✅ |

#### 58. #6F4E37 - Expected: moderate brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 7.9YR 3.6/3.5 | moderate brown | ✅ | moderate brown | ✅ |
| E_v1 | VonKries | 7.9YR 3.6/4.2 | moderate brown | ✅ | moderate brown | ✅ |

#### 59. #422518 - Expected: dark brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| C_v1 | VonKries | 5.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| C_v1 | CAT02 | 5.7YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| C_v1 | XYZScaling | 5.4YR 1.8/3.1 | dark brown | ✅ | dark brown | ✅ |
| D50_v1 | Bradford | 7.1YR 1.8/3.6 | dark yellowish brown | ❌ | dark brown | ✅ |
| D50_v1 | VonKries | 6.8YR 1.8/3.6 | dark brown | ✅ | dark brown | ✅ |
| D50_v1 | CAT02 | 7.1YR 1.8/3.6 | dark yellowish brown | ❌ | dark brown | ✅ |
| D50_v1 | XYZScaling | 7.5YR 1.8/3.4 | dark yellowish brown | ❌ | dark brown | ✅ |
| D55_v1 | Bradford | 7.0YR 1.8/3.4 | dark brown | ✅ | dark brown | ✅ |
| D55_v1 | VonKries | 6.8YR 1.8/3.4 | dark brown | ✅ | dark brown | ✅ |
| D55_v1 | CAT02 | 7.0YR 1.8/3.4 | dark yellowish brown | ❌ | dark brown | ✅ |
| D55_v1 | XYZScaling | 7.3YR 1.8/3.2 | dark yellowish brown | ❌ | dark brown | ✅ |
| D65_v1 | Bradford | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | VonKries | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | CAT02 | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | XYZScaling | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | Bradford | 6.4YR 1.8/2.7 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | VonKries | 6.6YR 1.8/2.7 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | CAT02 | 6.4YR 1.8/2.7 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | XYZScaling | 6.2YR 1.8/2.8 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | Bradford | 5.9YR 1.8/3.5 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | VonKries | 5.7YR 1.8/3.4 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | CAT02 | 5.9YR 1.8/3.4 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | XYZScaling | 5.7YR 1.8/3.4 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | Bradford | 6.8YR 1.8/4.1 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | VonKries | 6.4YR 1.8/4.1 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | CAT02 | 6.9YR 1.8/4.1 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | XYZScaling | 7.3YR 1.8/3.8 | dark yellowish brown | ❌ | dark brown | ✅ |
| F7_v1 | Bradford | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | VonKries | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | CAT02 | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | XYZScaling | 6.8YR 1.8/3.0 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | Bradford | 6.6YR 1.8/4.3 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | VonKries | 6.2YR 1.8/4.3 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | CAT02 | 6.7YR 1.8/4.3 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | XYZScaling | 6.9YR 1.8/4.0 | dark brown | ✅ | dark brown | ✅ |

#### 60. #958070 - Expected: light grayish brown

No matches

#### 61. #635147 - Expected: grayish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 3.6/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| A_v2 | VonKries | 2.5YR 3.5/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| A_v2 | CAT02 | 2.5YR 3.6/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| A_v2 | XYZScaling | 2.5YR 3.5/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| C_v1 | Bradford | 7.9YR 3.5/1.6 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| C_v1 | CAT02 | 7.8YR 3.5/1.6 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| C_v1 | XYZScaling | 7.3YR 3.5/1.6 | grayish yellowish brown | ❌ | grayish brown | ✅ |

#### 62. #3E322C - Expected: dark grayish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 2.2/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| A_v2 | VonKries | 2.5YR 2.2/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| A_v2 | CAT02 | 2.5YR 2.2/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| A_v2 | XYZScaling | 2.5YR 2.2/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| C_v1 | Bradford | 7.2YR 2.2/1.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| C_v1 | VonKries | 7.4YR 2.2/1.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| C_v1 | CAT02 | 7.2YR 2.2/1.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| C_v1 | XYZScaling | 6.8YR 2.2/1.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | Bradford | 8.0YR 2.2/1.8 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | VonKries | 7.8YR 2.2/1.8 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | CAT02 | 8.0YR 2.2/1.8 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | XYZScaling | 7.9YR 2.2/1.8 | dark grayish brown | ✅ | dark grayish brown | ✅ |

#### 63. #8E8279 - Expected: light brownish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.4Y 5.4/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| C_v1 | VonKries | 1.8Y 5.4/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| C_v1 | CAT02 | 1.3Y 5.4/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| C_v1 | XYZScaling | 0.5Y 5.4/1.1 | light brownish gray | ✅ | light brownish gray | ✅ |

#### 64. #5B504F - Expected: brownish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 1.5Y 3.5/0.7 | brownish gray | ✅ | brownish gray | ✅ |
| D65_v1 | VonKries | 1.5Y 3.5/0.7 | brownish gray | ✅ | brownish gray | ✅ |
| D65_v1 | CAT02 | 1.5Y 3.5/0.7 | brownish gray | ✅ | brownish gray | ✅ |
| D65_v1 | XYZScaling | 1.5Y 3.5/0.7 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | Bradford | 1.7Y 3.5/0.8 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | VonKries | 1.7Y 3.5/0.8 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | CAT02 | 1.7Y 3.5/0.8 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | XYZScaling | 1.7Y 3.5/0.8 | brownish gray | ✅ | brownish gray | ✅ |

#### 65. #28201C - Expected: brownish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.0YR 1.3/0.7 | brownish black | ✅ | brownish black | ✅ |
| C_v1 | VonKries | 8.2YR 1.3/0.7 | brownish black | ✅ | brownish black | ✅ |
| C_v1 | CAT02 | 8.0YR 1.3/0.7 | brownish black | ✅ | brownish black | ✅ |
| C_v1 | XYZScaling | 7.4YR 1.3/0.7 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | Bradford | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | VonKries | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | CAT02 | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | XYZScaling | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | Bradford | 1.6Y 1.3/0.5 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | VonKries | 1.9Y 1.3/0.5 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | CAT02 | 1.5Y 1.3/0.5 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | XYZScaling | 0.9Y 1.3/0.5 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | Bradford | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | VonKries | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | CAT02 | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | XYZScaling | 2.9Y 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |

#### 66. #F6A600 - Expected: vivid orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 7.3YR 7.3/18.4 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F2_v1 | Bradford | 9.8YR 7.4/15.2 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F2_v1 | VonKries | 8.7YR 7.3/15.6 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F2_v1 | CAT02 | 10.0YR 7.5/15.7 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F11_v1 | Bradford | 9.0YR 7.5/15.7 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F11_v1 | VonKries | 7.9YR 7.3/16.0 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F11_v1 | CAT02 | 9.2YR 7.5/16.2 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |
| F11_v1 | XYZScaling | 0.8Y 7.3/14.9 | vivid orange yellow | ✅ | vivid orange yellow | ✅ |

#### 67. #FFC14F - Expected: brilliant orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| F2_v1 | VonKries | 0.7Y 8.1/13.2 | vivid yellow | ❌ | brilliant orange yellow | ✅ |
| F11_v1 | Bradford | 1.0Y 8.2/13.4 | vivid yellow | ❌ | brilliant orange yellow | ✅ |
| F11_v1 | VonKries | 9.6YR 8.1/13.7 | brilliant orange yellow | ✅ | brilliant orange yellow | ✅ |

#### 68. #EAA221 - Expected: strong orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | VonKries | 0.9Y 7.1/12.0 | vivid yellow | ❌ | strong orange yellow | ✅ |
| F2_v1 | Bradford | 0.4Y 7.2/13.8 | vivid yellow | ❌ | strong orange yellow | ✅ |

#### 69. #C98500 - Expected: deep orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | VonKries | 0.9Y 6.0/12.1 | vivid yellow | ❌ | deep orange yellow | ✅ |
| E_v1 | Bradford | 0.7Y 6.0/11.6 | vivid yellow | ❌ | deep orange yellow | ✅ |
| E_v1 | VonKries | 0.5Y 6.0/11.6 | vivid yellow | ❌ | deep orange yellow | ✅ |
| E_v1 | CAT02 | 0.8Y 6.0/11.6 | vivid yellow | ❌ | deep orange yellow | ✅ |
| E_v1 | XYZScaling | 0.9Y 6.0/11.5 | vivid yellow | ❌ | deep orange yellow | ✅ |
| F2_v1 | Bradford | 0.0Y 6.1/13.1 | vivid yellow | ❌ | deep orange yellow | ✅ |
| F2_v1 | VonKries | 9.0YR 6.0/13.5 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F2_v1 | CAT02 | 0.3Y 6.1/13.5 | vivid yellow | ❌ | deep orange yellow | ✅ |
| F11_v1 | Bradford | 9.3YR 6.1/13.5 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F11_v1 | VonKries | 8.2YR 6.0/13.9 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F11_v1 | CAT02 | 9.5YR 6.1/13.9 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F11_v1 | XYZScaling | 1.0Y 6.0/12.9 | vivid yellow | ❌ | deep orange yellow | ✅ |

#### 70. #FBC97F - Expected: light orange yellow

No matches

#### 71. #E3A857 - Expected: moderate orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | VonKries | 0.9Y 7.2/9.0 | moderate orange yellow | ✅ | moderate orange yellow | ✅ |

#### 72. #BE8A3D - Expected: dark orange yellow

No matches

#### 73. #FAD6A5 - Expected: pale orange yellow

No matches

#### 74. #996515 - Expected: strong yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 6.8YR 4.8/12.6 | strong yellowish brown | ✅ | deep orange | ❌ |
| A_v1 | CAT02 | 7.1YR 4.8/13.0 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| A_v1 | XYZScaling | 8.5YR 4.6/11.8 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| E_v1 | VonKries | 0.9Y 4.6/8.6 | light olive brown | ❌ | strong yellowish brown | ✅ |
| F2_v1 | Bradford | 0.6Y 4.7/9.8 | light olive brown | ❌ | strong yellowish brown | ✅ |
| F2_v1 | VonKries | 9.7YR 4.6/10.0 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F2_v1 | CAT02 | 0.8Y 4.7/10.0 | light olive brown | ❌ | strong yellowish brown | ✅ |
| F11_v1 | Bradford | 10.0YR 4.7/10.1 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F11_v1 | VonKries | 9.0YR 4.6/10.4 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F11_v1 | CAT02 | 0.2Y 4.7/10.4 | light olive brown | ❌ | strong yellowish brown | ✅ |

#### 75. #654522 - Expected: deep yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 7.5YR 3.3/8.1 | deep yellowish brown | ✅ | strong brown | ❌ |
| A_v1 | CAT02 | 7.7YR 3.3/8.2 | deep yellowish brown | ✅ | strong brown | ❌ |
| A_v1 | XYZScaling | 8.7YR 3.2/7.6 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | Bradford | 0.7Y 3.2/5.0 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | VonKries | 0.5Y 3.2/5.0 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | CAT02 | 0.8Y 3.2/5.0 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | Bradford | 0.8Y 3.2/6.0 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | VonKries | 9.9YR 3.2/6.1 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | CAT02 | 1.0Y 3.2/6.1 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F11_v1 | Bradford | 0.2Y 3.2/6.3 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F11_v1 | VonKries | 9.2YR 3.2/6.4 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F11_v1 | CAT02 | 0.3Y 3.2/6.4 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |

#### 76. #C19A6B - Expected: light yellowish brown

No matches

#### 77. #826644 - Expected: moderate yellowish brown

No matches

#### 78. #4B3621 - Expected: dark yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 0.9Y 2.4/2.9 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | Bradford | 0.5Y 2.4/3.4 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | VonKries | 0.2Y 2.4/3.4 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | CAT02 | 0.5Y 2.4/3.4 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | XYZScaling | 0.5Y 2.4/3.4 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F2_v1 | VonKries | 0.3Y 2.4/4.3 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F11_v1 | Bradford | 0.5Y 2.5/4.4 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F11_v1 | VonKries | 9.6YR 2.4/4.5 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F11_v1 | CAT02 | 0.6Y 2.5/4.5 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |

#### 79. #AE9B82 - Expected: light grayish yellowish brown

No matches

#### 80. #7E6D5A - Expected: grayish yellowish brown

No matches

#### 81. #483C32 - Expected: dark grayish yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 0.9Y 2.6/2.0 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| E_v1 | VonKries | 0.7Y 2.6/2.0 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| E_v1 | CAT02 | 0.9Y 2.6/2.0 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |

#### 82. #F3C300 - Expected: vivid yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 2.6Y 8.0/17.2 | vivid yellow | ✅ | vivid yellow | ✅ |
| F2_v1 | Bradford | 5.1Y 8.1/13.9 | vivid yellow | ✅ | vivid yellow | ✅ |
| F2_v1 | VonKries | 3.8Y 8.0/14.4 | vivid yellow | ✅ | vivid yellow | ✅ |
| F2_v1 | CAT02 | 5.1Y 8.1/14.5 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | Bradford | 4.0Y 8.1/14.4 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | VonKries | 2.9Y 8.0/15.1 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | CAT02 | 4.1Y 8.1/15.1 | vivid yellow | ✅ | vivid yellow | ✅ |

#### 83. #FADA5E - Expected: brilliant yellow

No matches

#### 84. #D4AF37 - Expected: strong yellow

No matches

#### 85. #AF8D13 - Expected: deep yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| F2_v1 | Bradford | 6.5Y 6.0/10.5 | deep greenish yellow | ❌ | deep yellow | ✅ |
| F2_v1 | VonKries | 5.1Y 5.9/10.8 | deep yellow | ✅ | deep yellow | ✅ |
| F2_v1 | CAT02 | 6.5Y 6.0/10.9 | deep greenish yellow | ❌ | deep yellow | ✅ |
| F11_v1 | Bradford | 5.4Y 6.0/10.9 | deep yellow | ✅ | deep yellow | ✅ |

#### 86. #F8DE7E - Expected: light yellow

No matches

#### 87. #C9AE5D - Expected: moderate yellow

No matches

#### 88. #AB9144 - Expected: dark yellow

No matches

#### 89. #F3E5AB - Expected: pale yellow

No matches

#### 90. #C2B280 - Expected: grayish yellow

No matches

#### 91. #A18F60 - Expected: dark grayish yellow

No matches

#### 92. #F0EAD6 - Expected: yellowish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 10.0YR 9.3/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| A_v2 | VonKries | 10.0YR 9.3/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| A_v2 | CAT02 | 10.0YR 9.3/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| A_v2 | XYZScaling | 10.0YR 9.3/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| C_v1 | Bradford | 4.8Y 9.3/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| C_v1 | VonKries | 5.0Y 9.3/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| C_v1 | CAT02 | 4.9Y 9.3/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| C_v1 | XYZScaling | 4.1Y 9.3/1.3 | yellowish white | ✅ | yellowish white | ✅ |

#### 93. #BFB8A5 - Expected: yellowish gray

No matches

#### 94. #967117 - Expected: light olive brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 1.8Y 4.9/11.3 | light olive brown | ✅ | light olive brown | ✅ |
| F2_v1 | VonKries | 3.1Y 4.9/9.5 | light olive brown | ✅ | light olive brown | ✅ |
| F11_v1 | Bradford | 3.4Y 5.0/9.6 | light olive brown | ✅ | light olive brown | ✅ |
| F11_v1 | VonKries | 2.2Y 4.9/9.9 | light olive brown | ✅ | light olive brown | ✅ |
| F11_v1 | CAT02 | 3.5Y 5.0/9.9 | light olive brown | ✅ | light olive brown | ✅ |

#### 95. #6C541E - Expected: moderate olive brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 2.4Y 3.7/7.9 | moderate olive brown | ✅ | moderate olive brown | ✅ |
| F11_v1 | VonKries | 3.1Y 3.7/6.9 | moderate olive | ❌ | moderate olive brown | ✅ |

#### 96. #3B3121 - Expected: dark olive brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 1.7Y 2.1/4.5 | dark olive brown | ✅ | dark olive brown | ✅ |
| E_v1 | VonKries | 3.8Y 2.1/2.5 | dark grayish olive | ❌ | dark olive brown | ✅ |
| F2_v1 | VonKries | 3.8Y 2.1/3.3 | dark olive | ❌ | dark olive brown | ✅ |
| F11_v1 | Bradford | 3.6Y 2.1/3.4 | dark olive | ❌ | dark olive brown | ✅ |
| F11_v1 | VonKries | 2.7Y 2.1/3.4 | dark olive brown | ✅ | dark olive brown | ✅ |
| F11_v1 | CAT02 | 3.7Y 2.1/3.5 | dark olive | ❌ | dark olive brown | ✅ |

#### 97. #DCD300 - Expected: vivid greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 0.6GY 8.2/14.8 | vivid greenish yellow | ✅ | vivid greenish yellow | ✅ |
| F2_v1 | VonKries | 1.6GY 8.2/13.1 | vivid yellow green | ❌ | vivid greenish yellow | ✅ |
| F11_v1 | Bradford | 1.9GY 8.3/13.0 | vivid yellow green | ❌ | vivid greenish yellow | ✅ |
| F11_v1 | VonKries | 0.4GY 8.2/13.4 | vivid greenish yellow | ✅ | vivid greenish yellow | ✅ |
| F11_v1 | CAT02 | 1.9GY 8.3/13.5 | vivid yellow green | ❌ | vivid greenish yellow | ✅ |

#### 98. #E9E450 - Expected: brilliant greenish yellow

No matches

#### 99. #BEB72E - Expected: strong greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| F2_v1 | VonKries | 1.4GY 7.2/11.0 | strong greenish yellow | ✅ | strong greenish yellow | ✅ |

#### 100. #9B9400 - Expected: deep greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| F2_v1 | Bradford | 1.7GY 6.0/10.1 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F2_v1 | VonKries | 0.6GY 5.9/10.2 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F2_v1 | CAT02 | 1.7GY 6.0/10.5 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F11_v1 | Bradford | 0.8GY 6.0/10.2 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F11_v1 | VonKries | 9.6Y 5.9/10.4 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F11_v1 | CAT02 | 0.9GY 6.0/10.7 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |

#### 101. #EAE679 - Expected: light greenish yellow

No matches

#### 102. #B9B459 - Expected: moderate greenish yellow

No matches

#### 103. #98943E - Expected: dark greenish yellow

No matches

#### 104. #EBE8A4 - Expected: pale greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1GY 9.1/4.3 | pale greenish yellow | ✅ | pale greenish yellow | ✅ |

#### 105. #B9B57D - Expected: grayish greenish yellow

No matches

#### 106. #867E36 - Expected: light olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 4.3Y 5.2/9.7 | light olive | ✅ | light olive | ✅ |
| A_v1 | CAT02 | 4.4Y 5.2/10.2 | light olive | ✅ | light olive | ✅ |
| A_v1 | XYZScaling | 7.8Y 5.1/9.1 | light olive | ✅ | light olive | ✅ |
| E_v1 | Bradford | 1.8GY 5.1/6.2 | light olive | ✅ | light olive | ✅ |
| E_v1 | VonKries | 1.7GY 5.1/6.2 | light olive | ✅ | light olive | ✅ |
| E_v1 | CAT02 | 1.8GY 5.1/6.3 | light olive | ✅ | light olive | ✅ |
| F2_v1 | Bradford | 0.8GY 5.2/7.3 | light olive | ✅ | light olive | ✅ |
| F2_v1 | VonKries | 0.0GY 5.1/7.3 | light olive | ✅ | light olive | ✅ |
| F2_v1 | CAT02 | 0.8GY 5.2/7.5 | light olive | ✅ | light olive | ✅ |
| F11_v1 | Bradford | 0.0GY 5.2/7.4 | light olive | ✅ | light olive | ✅ |
| F11_v1 | VonKries | 8.7Y 5.1/7.5 | light olive | ✅ | light olive | ✅ |
| F11_v1 | CAT02 | 0.0GY 5.2/7.6 | light olive | ✅ | light olive | ✅ |
| F11_v1 | XYZScaling | 1.7GY 5.1/7.5 | light olive | ✅ | light olive | ✅ |

#### 107. #665D1E - Expected: moderate olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.8Y 3.9/8.2 | moderate olive | ✅ | moderate olive brown | ❌ |
| A_v1 | CAT02 | 3.8Y 3.9/8.6 | moderate olive | ✅ | moderate olive brown | ❌ |
| A_v1 | XYZScaling | 7.3Y 3.8/7.6 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | Bradford | 1.3GY 3.9/6.1 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | VonKries | 0.7GY 3.8/6.0 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | CAT02 | 1.4GY 3.9/6.2 | moderate olive | ✅ | moderate olive | ✅ |
| D55_v1 | VonKries | 1.8GY 3.8/5.9 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | Bradford | 0.7GY 3.9/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | VonKries | 0.5GY 3.8/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | CAT02 | 0.7GY 3.9/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | XYZScaling | 1.2GY 3.8/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | Bradford | 9.7Y 3.9/6.4 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | VonKries | 8.7Y 3.8/6.5 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | CAT02 | 9.7Y 3.9/6.6 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | XYZScaling | 1.3GY 3.8/6.5 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | Bradford | 8.8Y 3.9/6.6 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | VonKries | 7.7Y 3.8/6.6 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | CAT02 | 8.9Y 3.9/6.8 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | XYZScaling | 0.7GY 3.8/6.6 | moderate olive | ✅ | moderate olive | ✅ |

#### 108. #403D21 - Expected: dark olive

No matches

#### 109. #8C8767 - Expected: light grayish olive

No matches

#### 110. #5B5842 - Expected: grayish olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 0.4GY 3.7/2.7 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | VonKries | 0.3GY 3.7/2.6 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | CAT02 | 0.4GY 3.7/2.7 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | XYZScaling | 0.8GY 3.6/2.7 | grayish olive | ✅ | grayish olive | ✅ |

#### 111. #363527 - Expected: dark grayish olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 1.6GY 2.2/2.7 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| D50_v1 | VonKries | 1.1GY 2.2/2.7 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| D50_v1 | CAT02 | 1.7GY 2.2/2.8 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | Bradford | 0.0GY 2.2/2.2 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | VonKries | 9.9Y 2.2/2.2 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | CAT02 | 0.0GY 2.2/2.2 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | XYZScaling | 0.5GY 2.2/2.2 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| F2_v1 | VonKries | 8.7Y 2.2/3.0 | dark grayish olive | ✅ | dark grayish olive | ✅ |

#### 112. #8A8776 - Expected: light olive gray

No matches

#### 113. #57554C - Expected: olive gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.4GY 3.5/0.9 | olive gray | ✅ | olive gray | ✅ |
| C_v1 | VonKries | 2.9GY 3.5/0.9 | olive gray | ✅ | olive gray | ✅ |
| C_v1 | CAT02 | 2.4GY 3.5/0.9 | olive gray | ✅ | olive gray | ✅ |
| C_v1 | XYZScaling | 2.1GY 3.5/0.9 | olive gray | ✅ | olive gray | ✅ |

#### 114. #25241D - Expected: olive black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.3GY 1.4/0.9 | olive black | ✅ | olive black | ✅ |
| C_v1 | VonKries | 1.6GY 1.4/0.9 | olive black | ✅ | olive black | ✅ |
| C_v1 | CAT02 | 1.3GY 1.4/0.9 | olive black | ✅ | olive black | ✅ |
| C_v1 | XYZScaling | 1.0GY 1.4/0.9 | olive black | ✅ | olive black | ✅ |

#### 115. #8DB600 - Expected: vivid yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 2.5GY 6.8/12.1 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| A_v1 | CAT02 | 2.4GY 6.9/13.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| A_v1 | XYZScaling | 5.3GY 6.8/13.1 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| C_v1 | Bradford | 8.0GY 6.8/12.1 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| C_v1 | CAT02 | 8.0GY 6.8/12.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| C_v1 | XYZScaling | 7.9GY 6.8/12.1 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | Bradford | 7.1GY 6.8/12.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | VonKries | 6.7GY 6.8/12.3 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | CAT02 | 7.0GY 6.8/12.6 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | XYZScaling | 7.8GY 6.8/13.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D55_v1 | Bradford | 7.6GY 6.8/12.5 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D55_v1 | VonKries | 7.3GY 6.8/12.3 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D55_v1 | CAT02 | 7.5GY 6.8/12.6 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | Bradford | 6.9GY 6.8/11.8 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | VonKries | 6.8GY 6.8/11.8 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | CAT02 | 6.8GY 6.8/11.8 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | XYZScaling | 7.4GY 6.8/12.1 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | Bradford | 6.1GY 6.8/12.2 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | VonKries | 5.5GY 6.8/12.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | CAT02 | 6.0GY 6.9/12.6 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | XYZScaling | 7.1GY 6.8/13.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | Bradford | 5.6GY 6.8/12.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | VonKries | 5.2GY 6.8/11.9 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | CAT02 | 5.5GY 6.9/12.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | XYZScaling | 6.8GY 6.8/13.0 | vivid yellow green | ✅ | vivid yellow green | ✅ |

#### 116. #BDDA57 - Expected: brilliant yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.6GY 8.2/10.3 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| C_v1 | VonKries | 7.8GY 8.2/10.4 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| C_v1 | CAT02 | 7.6GY 8.2/10.2 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| C_v1 | XYZScaling | 7.6GY 8.2/10.2 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| E_v1 | Bradford | 6.4GY 8.2/10.4 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| E_v1 | VonKries | 6.4GY 8.2/10.4 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| E_v1 | CAT02 | 6.4GY 8.2/10.4 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| E_v1 | XYZScaling | 6.7GY 8.2/10.6 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |

#### 117. #7E9F2E - Expected: strong yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 7.1GY 6.0/10.1 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D50_v1 | VonKries | 6.7GY 6.0/10.0 | strong yellow green | ✅ | strong yellow green | ✅ |
| D50_v1 | CAT02 | 7.0GY 6.0/10.3 | strong yellow green | ✅ | strong yellow green | ✅ |
| D50_v1 | XYZScaling | 7.7GY 6.0/10.6 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | Bradford | 7.6GY 6.0/10.1 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | VonKries | 7.3GY 6.0/10.0 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | CAT02 | 7.5GY 6.0/10.2 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | XYZScaling | 8.0GY 6.0/10.5 | strong yellowish green | ❌ | strong yellow green | ✅ |
| E_v1 | Bradford | 6.9GY 6.0/9.4 | strong yellow green | ✅ | strong yellow green | ✅ |
| E_v1 | VonKries | 6.8GY 6.0/9.4 | strong yellow green | ✅ | strong yellow green | ✅ |
| E_v1 | CAT02 | 6.8GY 6.0/9.5 | strong yellow green | ✅ | strong yellow green | ✅ |
| E_v1 | XYZScaling | 7.3GY 6.0/9.7 | strong yellowish green | ❌ | strong yellow green | ✅ |
| F2_v1 | Bradford | 6.0GY 6.0/10.1 | strong yellow green | ✅ | strong yellow green | ✅ |
| F2_v1 | VonKries | 5.5GY 6.0/9.9 | strong yellow green | ✅ | strong yellow green | ✅ |
| F2_v1 | CAT02 | 5.9GY 6.1/10.3 | strong yellow green | ✅ | strong yellow green | ✅ |
| F2_v1 | XYZScaling | 6.9GY 6.0/10.8 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | Bradford | 5.5GY 6.0/9.9 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | VonKries | 5.2GY 6.0/9.8 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | CAT02 | 5.5GY 6.1/10.2 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | XYZScaling | 6.6GY 6.0/10.7 | strong yellow green | ✅ | strong yellow green | ✅ |

#### 118. #467129 - Expected: deep yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.8GY 4.2/7.8 | deep yellow green | ✅ | deep yellow green | ✅ |
| A_v1 | VonKries | 2.1GY 4.2/7.8 | deep yellow green | ✅ | deep yellow green | ✅ |
| A_v1 | CAT02 | 3.5GY 4.3/8.2 | deep yellow green | ✅ | deep yellow green | ✅ |
| A_v1 | XYZScaling | 6.2GY 4.2/8.8 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | Bradford | 7.4GY 4.2/7.9 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | VonKries | 6.8GY 4.2/7.8 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | CAT02 | 7.2GY 4.3/8.1 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | XYZScaling | 8.0GY 4.2/8.5 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | Bradford | 6.9GY 4.2/7.8 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | VonKries | 6.4GY 4.2/7.7 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | CAT02 | 6.8GY 4.3/8.0 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | XYZScaling | 7.8GY 4.2/8.4 | deep yellow green | ✅ | deep yellow green | ✅ |

#### 119. #C9DC89 - Expected: light yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.8GY 8.4/6.7 | light yellow green | ✅ | light yellow green | ✅ |
| C_v1 | CAT02 | 7.8GY 8.4/6.7 | light yellow green | ✅ | light yellow green | ✅ |
| C_v1 | XYZScaling | 7.7GY 8.4/6.7 | light yellow green | ✅ | light yellow green | ✅ |

#### 120. #8A9A5B - Expected: moderate yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.8GY 6.0/5.9 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| C_v1 | CAT02 | 7.8GY 6.0/5.9 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| C_v1 | XYZScaling | 7.7GY 6.0/5.9 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| D55_v1 | Bradford | 7.0GY 6.0/6.9 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D55_v1 | VonKries | 6.7GY 6.0/6.8 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D55_v1 | CAT02 | 6.9GY 6.0/6.9 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | Bradford | 6.1GY 6.0/6.2 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | VonKries | 6.1GY 6.0/6.1 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | CAT02 | 6.1GY 6.0/6.2 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | XYZScaling | 6.4GY 6.0/6.3 | moderate yellow green | ✅ | moderate yellow green | ✅ |

#### 121. #DADFB7 - Expected: pale yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | XYZScaling | 10.0Y 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| C_v1 | Bradford | 3.6GY 8.7/2.4 | pale yellow green | ✅ | pale yellow green | ✅ |
| C_v1 | CAT02 | 3.6GY 8.7/2.4 | pale yellow green | ✅ | pale yellow green | ✅ |
| D50_v2 | Bradford | 5.0GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| D50_v2 | VonKries | 5.0GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| D50_v2 | CAT02 | 5.0GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| D50_v2 | XYZScaling | 5.0GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| D55_v2 | Bradford | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | VonKries | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | CAT02 | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | XYZScaling | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| E_v2 | Bradford | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| E_v2 | VonKries | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| E_v2 | CAT02 | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| E_v2 | XYZScaling | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| F2_v2 | Bradford | 5.0GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F2_v2 | VonKries | 2.5GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F2_v2 | CAT02 | 2.5GY 8.8/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F2_v2 | XYZScaling | 5.0GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F7_v2 | Bradford | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| F7_v2 | VonKries | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| F7_v2 | CAT02 | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| F7_v2 | XYZScaling | 7.5GY 8.7/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| F11_v2 | Bradford | 2.5GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | VonKries | 2.5GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | CAT02 | 2.5GY 8.8/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | XYZScaling | 2.5GY 8.7/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |

#### 122. #8F9779 - Expected: grayish yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | XYZScaling | 5.0GY 6.0/2.0 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| C_v1 | Bradford | 7.8GY 6.0/2.8 | moderate yellowish green | ❌ | grayish yellow green | ✅ |
| C_v1 | CAT02 | 7.8GY 6.0/2.8 | moderate yellowish green | ❌ | grayish yellow green | ✅ |
| C_v1 | XYZScaling | 7.7GY 6.0/2.8 | moderate yellowish green | ❌ | grayish yellow green | ✅ |
| D50_v2 | Bradford | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| D50_v2 | VonKries | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| D50_v2 | CAT02 | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| D50_v2 | XYZScaling | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | Bradford | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | VonKries | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | CAT02 | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | XYZScaling | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | Bradford | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | VonKries | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | CAT02 | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | XYZScaling | 7.5GY 6.0/2.0 | pale green | ❌ | grayish yellow green | ✅ |

#### 123. #404F00 - Expected: strong olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 3.7GY 3.1/7.2 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | Bradford | 5.9GY 3.1/7.0 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | CAT02 | 5.8GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | XYZScaling | 6.4GY 3.1/7.3 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | Bradford | 6.2GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | VonKries | 6.0GY 3.1/7.0 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | CAT02 | 6.2GY 3.1/7.2 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | XYZScaling | 6.5GY 3.1/7.3 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | Bradford | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | VonKries | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | CAT02 | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | XYZScaling | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | Bradford | 7.1GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | VonKries | 7.2GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | CAT02 | 7.1GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| F2_v1 | CAT02 | 5.0GY 3.1/7.0 | strong olive green | ✅ | strong olive green | ✅ |
| F2_v1 | XYZScaling | 5.9GY 3.1/7.3 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | Bradford | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | VonKries | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | CAT02 | 6.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | XYZScaling | 6.8GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| F11_v1 | XYZScaling | 5.7GY 3.1/7.3 | strong olive green | ✅ | strong olive green | ✅ |

#### 124. #232F00 - Expected: deep olive green

No matches

#### 125. #4A5D23 - Expected: moderate olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.6GY 3.6/5.9 | dark yellowish green | ❌ | moderate olive green | ✅ |
| C_v1 | VonKries | 7.7GY 3.6/5.9 | dark yellowish green | ❌ | moderate olive green | ✅ |
| C_v1 | CAT02 | 7.6GY 3.6/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ |
| C_v1 | XYZScaling | 7.6GY 3.6/5.9 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D50_v1 | Bradford | 6.6GY 3.6/6.5 | moderate olive green | ✅ | moderate olive green | ✅ |
| D50_v1 | VonKries | 6.2GY 3.6/6.4 | moderate olive green | ✅ | moderate olive green | ✅ |
| D50_v1 | CAT02 | 6.5GY 3.6/6.5 | moderate olive green | ✅ | moderate olive green | ✅ |
| D50_v1 | XYZScaling | 7.1GY 3.6/6.7 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D55_v1 | Bradford | 7.1GY 3.6/6.4 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D55_v1 | VonKries | 6.9GY 3.6/6.3 | moderate olive green | ✅ | moderate olive green | ✅ |
| D55_v1 | CAT02 | 7.0GY 3.6/6.4 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D55_v1 | XYZScaling | 7.4GY 3.6/6.5 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | Bradford | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | VonKries | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | CAT02 | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | XYZScaling | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| E_v1 | Bradford | 6.4GY 3.6/5.9 | moderate olive green | ✅ | moderate olive green | ✅ |
| E_v1 | VonKries | 6.3GY 3.6/5.9 | moderate olive green | ✅ | moderate olive green | ✅ |
| E_v1 | CAT02 | 6.4GY 3.6/5.9 | moderate olive green | ✅ | moderate olive green | ✅ |
| E_v1 | XYZScaling | 6.8GY 3.6/6.1 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | Bradford | 5.5GY 3.6/6.5 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | VonKries | 5.1GY 3.6/6.4 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | CAT02 | 5.5GY 3.6/6.6 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | XYZScaling | 6.3GY 3.6/6.9 | moderate olive green | ✅ | moderate olive green | ✅ |
| F7_v1 | Bradford | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F7_v1 | VonKries | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F7_v1 | CAT02 | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F7_v1 | XYZScaling | 7.9GY 3.6/6.3 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F11_v1 | Bradford | 5.1GY 3.6/6.4 | moderate olive green | ✅ | moderate olive green | ✅ |
| F11_v1 | VonKries | 4.2GY 3.6/6.3 | moderate olive green | ✅ | moderate olive green | ✅ |
| F11_v1 | CAT02 | 5.1GY 3.6/6.6 | moderate olive green | ✅ | moderate olive green | ✅ |
| F11_v1 | XYZScaling | 6.0GY 3.6/6.8 | moderate olive green | ✅ | moderate olive green | ✅ |

#### 126. #2B3D26 - Expected: dark olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 3.4GY 2.3/4.7 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | Bradford | 7.6GY 2.3/4.2 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | VonKries | 7.4GY 2.3/4.1 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | CAT02 | 7.6GY 2.3/4.2 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | XYZScaling | 7.8GY 2.3/4.3 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | Bradford | 7.8GY 2.3/3.6 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | VonKries | 7.7GY 2.3/3.6 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | CAT02 | 7.8GY 2.3/3.6 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | Bradford | 6.3GY 2.3/4.3 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | VonKries | 5.9GY 2.3/4.2 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | CAT02 | 6.2GY 2.4/4.3 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | XYZScaling | 6.9GY 2.3/4.5 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | Bradford | 5.8GY 2.3/4.2 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | VonKries | 5.4GY 2.3/4.2 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | CAT02 | 5.7GY 2.4/4.3 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | XYZScaling | 6.5GY 2.3/4.5 | dark olive green | ✅ | dark olive green | ✅ |

#### 127. #515744 - Expected: grayish olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0GY 3.5/2.0 | grayish olive green | ✅ | grayish olive green | ✅ |
| A_v2 | CAT02 | 5.0GY 3.6/2.0 | grayish olive green | ✅ | grayish olive green | ✅ |
| A_v2 | XYZScaling | 5.0GY 3.5/2.0 | grayish olive green | ✅ | grayish olive green | ✅ |
| C_v1 | Bradford | 7.5GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ |
| C_v1 | VonKries | 7.7GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ |
| C_v1 | CAT02 | 7.5GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ |
| C_v1 | XYZScaling | 7.5GY 3.5/2.3 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | Bradford | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | VonKries | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | CAT02 | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | XYZScaling | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| E_v1 | Bradford | 4.9GY 3.5/2.6 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | VonKries | 4.7GY 3.5/2.6 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | CAT02 | 4.9GY 3.5/2.6 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | XYZScaling | 5.3GY 3.5/2.6 | grayish olive green | ✅ | grayish olive green | ✅ |
| F2_v2 | Bradford | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F2_v2 | VonKries | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F2_v2 | CAT02 | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F2_v2 | XYZScaling | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | Bradford | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | VonKries | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | CAT02 | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | XYZScaling | 7.5GY 3.5/2.0 | grayish green | ❌ | grayish olive green | ✅ |

#### 128. #31362B - Expected: dark grayish olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0GY 2.2/2.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| A_v2 | CAT02 | 5.0GY 2.2/2.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| A_v2 | XYZScaling | 5.0GY 2.2/2.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| C_v1 | Bradford | 7.8GY 2.2/1.9 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| C_v1 | VonKries | 7.9GY 2.2/1.9 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| C_v1 | CAT02 | 7.8GY 2.2/1.9 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| C_v1 | XYZScaling | 7.7GY 2.2/1.9 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| D50_v1 | Bradford | 5.3GY 2.2/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v1 | VonKries | 5.1GY 2.2/2.7 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v1 | CAT02 | 5.3GY 2.2/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v1 | XYZScaling | 5.7GY 2.2/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | Bradford | 6.2GY 2.2/2.6 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | VonKries | 6.1GY 2.2/2.6 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | CAT02 | 6.2GY 2.2/2.6 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | XYZScaling | 6.5GY 2.2/2.6 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | Bradford | 4.6GY 2.2/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | VonKries | 4.4GY 2.2/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | CAT02 | 4.5GY 2.2/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | XYZScaling | 5.2GY 2.2/2.2 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F2_v1 | Bradford | 2.2GY 2.2/2.9 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F2_v2 | Bradford | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F2_v2 | VonKries | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F2_v1 | CAT02 | 2.2GY 2.2/2.9 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F2_v2 | CAT02 | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F2_v2 | XYZScaling | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | Bradford | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | VonKries | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | CAT02 | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | XYZScaling | 7.5GY 2.2/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |

#### 129. #27A64C - Expected: vivid yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 8.6GY 5.9/12.7 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| C_v1 | Bradford | 2.9G 5.9/12.4 | vivid green | ❌ | vivid yellowish green | ✅ |
| C_v1 | CAT02 | 2.9G 5.9/12.3 | vivid green | ❌ | vivid yellowish green | ✅ |
| D50_v1 | Bradford | 0.6G 5.9/11.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | VonKries | 0.2G 5.9/11.4 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | CAT02 | 0.4G 5.9/11.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | XYZScaling | 0.9G 5.9/12.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | Bradford | 1.4G 5.9/12.3 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | VonKries | 1.2G 5.9/12.0 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | CAT02 | 1.3G 5.9/12.3 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | XYZScaling | 1.6G 5.9/12.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D65_v1 | Bradford | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| D65_v1 | VonKries | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| D65_v1 | CAT02 | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| E_v1 | Bradford | 1.1G 5.9/11.1 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| E_v1 | CAT02 | 1.0G 5.9/11.0 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| E_v1 | XYZScaling | 1.6G 5.9/12.0 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | Bradford | 9.8GY 5.9/11.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | VonKries | 9.6GY 5.9/11.3 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | CAT02 | 9.7GY 5.9/11.7 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | XYZScaling | 9.7GY 5.9/12.1 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F7_v1 | Bradford | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| F7_v1 | VonKries | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| F7_v1 | CAT02 | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.8G 5.9/13.2 | vivid green | ❌ | vivid yellowish green | ✅ |
| F11_v1 | Bradford | 9.7GY 5.9/11.3 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | VonKries | 9.3GY 5.9/11.1 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | CAT02 | 9.5GY 5.9/11.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | XYZScaling | 9.7GY 5.9/12.1 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |

#### 130. #83D37D - Expected: brilliant yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.0G 7.7/10.4 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| C_v1 | CAT02 | 3.0G 7.7/10.4 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | Bradford | 1.4G 7.7/10.2 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | VonKries | 1.3G 7.7/10.2 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | CAT02 | 1.4G 7.7/10.2 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | XYZScaling | 1.7G 7.7/10.6 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F2_v1 | Bradford | 9.3GY 7.7/11.0 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F2_v1 | VonKries | 8.5GY 7.7/10.6 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F11_v1 | Bradford | 8.4GY 7.7/10.6 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F11_v1 | VonKries | 7.7GY 7.7/10.2 | brilliant yellowish green | ✅ | brilliant yellow green | ❌ |
| F11_v1 | CAT02 | 8.2GY 7.7/10.7 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |

#### 131. #44944A - Expected: strong yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 7.7GY 5.4/10.5 | strong yellowish green | ✅ | strong yellow green | ❌ |
| C_v1 | Bradford | 1.9G 5.4/9.4 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| C_v1 | VonKries | 2.0G 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| C_v1 | CAT02 | 1.9G 5.4/9.4 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| C_v1 | XYZScaling | 2.0G 5.4/9.5 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | Bradford | 0.1G 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | VonKries | 10.0GY 5.4/9.4 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | CAT02 | 0.0G 5.4/9.7 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | XYZScaling | 0.1G 5.4/9.9 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | Bradford | 0.5G 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | VonKries | 0.4G 5.4/9.5 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | CAT02 | 0.4G 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | XYZScaling | 0.5G 5.4/9.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D65_v1 | Bradford | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D65_v1 | VonKries | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D65_v1 | CAT02 | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D65_v1 | XYZScaling | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D75_v1 | XYZScaling | 2.8G 5.4/10.2 | strong green | ❌ | strong yellowish green | ✅ |
| E_v1 | Bradford | 0.5G 5.4/8.9 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| E_v1 | VonKries | 0.5G 5.4/8.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| E_v1 | CAT02 | 0.5G 5.4/8.9 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| E_v1 | XYZScaling | 0.6G 5.4/9.2 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | Bradford | 9.3GY 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | VonKries | 9.0GY 5.4/9.4 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | CAT02 | 9.2GY 5.4/9.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | XYZScaling | 9.6GY 5.4/10.2 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F7_v1 | Bradford | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F7_v1 | VonKries | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F7_v1 | CAT02 | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F7_v1 | XYZScaling | 1.8G 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | Bradford | 9.0GY 5.4/9.5 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | VonKries | 8.5GY 5.4/9.2 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | CAT02 | 8.9GY 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | XYZScaling | 9.4GY 5.4/10.2 | strong yellowish green | ✅ | strong yellowish green | ✅ |

#### 132. #00622D - Expected: deep yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.5G 3.5/8.5 | strong green | ❌ | deep yellowish green | ✅ |
| C_v1 | VonKries | 2.6G 3.5/8.6 | strong green | ❌ | deep yellowish green | ✅ |
| C_v1 | CAT02 | 2.5G 3.5/8.4 | strong green | ❌ | deep yellowish green | ✅ |
| C_v1 | XYZScaling | 2.6G 3.5/8.6 | strong green | ❌ | deep yellowish green | ✅ |
| D50_v1 | Bradford | 0.4G 3.5/8.2 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | VonKries | 9.9GY 3.5/7.9 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | CAT02 | 0.2G 3.5/8.2 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | XYZScaling | 0.6G 3.5/8.6 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | Bradford | 1.2G 3.5/8.6 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | VonKries | 0.9G 3.5/8.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | CAT02 | 1.1G 3.5/8.5 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | XYZScaling | 1.3G 3.5/8.8 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D65_v1 | Bradford | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| D65_v1 | VonKries | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| D65_v1 | CAT02 | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| E_v1 | Bradford | 0.9G 3.5/7.7 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | VonKries | 0.7G 3.5/7.6 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | CAT02 | 0.8G 3.5/7.7 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | XYZScaling | 1.3G 3.5/8.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F2_v1 | Bradford | 8.7GY 3.5/7.7 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F2_v1 | VonKries | 8.4GY 3.5/7.5 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F2_v1 | CAT02 | 8.4GY 3.5/7.7 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F2_v1 | XYZScaling | 9.4GY 3.5/8.4 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F7_v1 | Bradford | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| F7_v1 | VonKries | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| F7_v1 | CAT02 | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.3G 3.5/9.0 | strong green | ❌ | deep yellowish green | ✅ |
| F11_v1 | Bradford | 8.4GY 3.5/7.5 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F11_v1 | VonKries | 8.3GY 3.5/7.4 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F11_v1 | CAT02 | 8.3GY 3.5/7.6 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F11_v1 | XYZScaling | 9.0GY 3.5/8.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |

#### 133. #003118 - Expected: very deep yellowish green

No matches

#### 134. #B6E5AF - Expected: very light yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 0.2G 8.6/6.0 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| E_v1 | VonKries | 10.0GY 8.6/5.9 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| E_v1 | CAT02 | 0.1G 8.6/5.9 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| E_v1 | XYZScaling | 0.8G 8.6/6.4 | very light yellowish green | ✅ | very light yellowish green | ✅ |

#### 135. #93C592 - Expected: light yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 1.0G 7.4/6.6 | light yellowish green | ✅ | light yellowish green | ✅ |
| E_v1 | VonKries | 0.9G 7.4/6.5 | light yellowish green | ✅ | light yellowish green | ✅ |
| E_v1 | CAT02 | 0.9G 7.4/6.6 | light yellowish green | ✅ | light yellowish green | ✅ |

#### 136. #679267 - Expected: moderate yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.4G 5.5/5.6 | light green | ❌ | moderate yellowish green | ✅ |
| C_v1 | VonKries | 2.5G 5.5/5.7 | light green | ❌ | moderate yellowish green | ✅ |
| C_v1 | CAT02 | 2.4G 5.5/5.5 | light green | ❌ | moderate yellowish green | ✅ |
| C_v1 | XYZScaling | 2.5G 5.5/5.6 | light green | ❌ | moderate yellowish green | ✅ |
| D50_v1 | Bradford | 0.2G 5.5/6.8 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D50_v1 | VonKries | 9.9GY 5.5/6.7 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D50_v1 | CAT02 | 0.1G 5.6/6.9 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | Bradford | 1.0G 5.5/6.7 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | VonKries | 0.9G 5.5/6.6 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | CAT02 | 0.9G 5.6/6.7 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | XYZScaling | 1.1G 5.5/6.8 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D65_v1 | Bradford | 2.3G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| D65_v1 | VonKries | 2.3G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| D65_v1 | CAT02 | 2.3G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.3G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| E_v1 | Bradford | 0.6G 5.5/5.8 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | VonKries | 0.5G 5.5/5.7 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | CAT02 | 0.6G 5.5/5.8 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | XYZScaling | 0.9G 5.5/6.0 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F2_v1 | Bradford | 7.9GY 5.5/6.8 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F2_v1 | VonKries | 7.4GY 5.5/6.6 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F2_v1 | CAT02 | 7.8GY 5.6/6.9 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F7_v1 | Bradford | 2.2G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| F7_v1 | VonKries | 2.2G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| F7_v1 | CAT02 | 2.2G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.2G 5.5/6.4 | light green | ❌ | moderate yellowish green | ✅ |
| F11_v1 | Bradford | 7.1GY 5.5/6.6 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F11_v1 | CAT02 | 7.0GY 5.6/6.8 | moderate yellowish green | ✅ | moderate yellow green | ❌ |

#### 137. #355E3B - Expected: dark yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.0G 3.5/5.2 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| C_v1 | VonKries | 2.1G 3.6/5.2 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| C_v1 | CAT02 | 2.1G 3.5/5.1 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| C_v1 | XYZScaling | 2.1G 3.6/5.2 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | Bradford | 9.5GY 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | VonKries | 9.3GY 3.6/5.6 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | CAT02 | 9.4GY 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | XYZScaling | 9.6GY 3.6/5.8 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | Bradford | 9.9GY 3.6/5.5 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | VonKries | 9.9GY 3.6/5.5 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | CAT02 | 9.9GY 3.6/5.5 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | XYZScaling | 10.0GY 3.6/5.6 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D65_v1 | Bradford | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D65_v1 | VonKries | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D65_v1 | CAT02 | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D65_v1 | XYZScaling | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | Bradford | 9.8GY 3.5/4.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | VonKries | 9.8GY 3.6/4.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | CAT02 | 9.8GY 3.6/4.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | XYZScaling | 0.0G 3.6/5.1 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | Bradford | 8.4GY 3.6/5.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | VonKries | 8.0GY 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | CAT02 | 8.3GY 3.6/5.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | XYZScaling | 8.7GY 3.6/6.1 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F7_v1 | Bradford | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F7_v1 | VonKries | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F7_v1 | CAT02 | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F7_v1 | XYZScaling | 1.8G 3.6/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F11_v1 | Bradford | 7.9GY 3.5/5.8 | dark yellowish green | ✅ | moderate olive green | ❌ |
| F11_v1 | VonKries | 7.4GY 3.6/5.6 | dark yellowish green | ✅ | moderate olive green | ❌ |
| F11_v1 | CAT02 | 7.8GY 3.6/5.8 | dark yellowish green | ✅ | moderate olive green | ❌ |
| F11_v1 | XYZScaling | 8.4GY 3.6/6.1 | dark yellowish green | ✅ | dark yellowish green | ✅ |

#### 138. #173620 - Expected: very dark yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.0G 1.9/4.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| C_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| C_v1 | VonKries | 2.0G 1.9/4.3 | very dark green | ❌ | very dark yellowish green | ✅ |
| C_v2 | VonKries | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| C_v1 | CAT02 | 2.0G 1.9/4.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| C_v2 | CAT02 | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| C_v1 | XYZScaling | 2.0G 1.9/4.3 | very dark green | ❌ | very dark yellowish green | ✅ |
| C_v2 | XYZScaling | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D50_v1 | Bradford | 8.5GY 1.9/4.4 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D50_v1 | VonKries | 8.0GY 1.9/4.3 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D50_v1 | CAT02 | 8.3GY 2.0/4.4 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D50_v1 | XYZScaling | 8.8GY 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | Bradford | 9.7GY 1.9/4.5 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D55_v1 | VonKries | 9.4GY 1.9/4.4 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | CAT02 | 9.6GY 2.0/4.5 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | XYZScaling | 9.9GY 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v1 | Bradford | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D65_v1 | VonKries | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v2 | VonKries | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D65_v1 | CAT02 | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v2 | CAT02 | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D65_v1 | XYZScaling | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v2 | XYZScaling | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v2 | Bradford | 2.5G 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v2 | VonKries | 2.5G 2.0/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v2 | CAT02 | 2.5G 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v1 | XYZScaling | 3.0G 1.9/4.5 | very dark green | ❌ | very dark yellowish green | ✅ |
| D75_v2 | XYZScaling | 2.5G 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| E_v1 | Bradford | 9.3GY 1.9/3.9 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| E_v1 | VonKries | 9.1GY 1.9/3.9 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v2 | VonKries | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| E_v1 | CAT02 | 9.2GY 1.9/3.9 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v2 | CAT02 | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| E_v1 | XYZScaling | 9.7GY 1.9/4.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v2 | XYZScaling | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| F7_v1 | Bradford | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| F7_v1 | VonKries | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v2 | VonKries | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| F7_v1 | CAT02 | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v2 | CAT02 | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| F7_v1 | XYZScaling | 1.6G 1.9/4.6 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v2 | XYZScaling | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |

#### 139. #008856 - Expected: vivid green

No matches

#### 140. #3EB489 - Expected: brilliant green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 5.1G 6.5/10.7 | brilliant green | ✅ | brilliant green | ✅ |
| D50_v1 | VonKries | 4.7G 6.5/10.4 | brilliant green | ✅ | brilliant green | ✅ |
| D50_v1 | CAT02 | 4.9G 6.5/10.7 | brilliant green | ✅ | brilliant green | ✅ |
| D50_v1 | XYZScaling | 5.1G 6.5/10.9 | brilliant green | ✅ | brilliant green | ✅ |
| D55_v1 | VonKries | 8.6G 6.5/10.9 | brilliant green | ✅ | brilliant green | ✅ |

#### 141. #007959 - Expected: strong green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 4.7G 4.4/8.4 | strong green | ✅ | strong green | ✅ |
| D50_v1 | VonKries | 4.4G 4.4/8.2 | strong green | ✅ | strong green | ✅ |
| D50_v1 | CAT02 | 4.6G 4.4/8.4 | strong green | ✅ | strong green | ✅ |
| D50_v1 | XYZScaling | 4.7G 4.4/8.6 | strong green | ✅ | strong green | ✅ |
| D55_v1 | Bradford | 8.5G 4.4/9.0 | strong bluish green | ❌ | strong green | ✅ |
| D55_v1 | VonKries | 7.9G 4.4/8.8 | strong green | ✅ | strong green | ✅ |
| D55_v1 | CAT02 | 8.2G 4.4/9.0 | strong bluish green | ❌ | strong green | ✅ |
| D55_v1 | XYZScaling | 8.4G 4.4/9.1 | strong bluish green | ❌ | strong green | ✅ |
| E_v1 | VonKries | 8.7G 4.4/7.7 | strong bluish green | ❌ | strong green | ✅ |
| F2_v1 | Bradford | 2.1G 4.4/7.9 | strong green | ✅ | deep yellowish green | ❌ |
| F2_v1 | XYZScaling | 2.2G 4.4/8.2 | strong green | ✅ | deep yellowish green | ❌ |

#### 142. #00543D - Expected: deep green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D55_v1 | Bradford | 6.0G 3.1/7.0 | deep green | ✅ | deep green | ✅ |
| D55_v1 | XYZScaling | 5.9G 3.1/7.1 | deep green | ✅ | deep green | ✅ |

#### 143. #8ED1B2 - Expected: very light green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 6.0G 7.8/5.9 | very light green | ✅ | very light green | ✅ |
| E_v1 | VonKries | 5.4G 7.8/5.8 | very light green | ✅ | very light green | ✅ |
| E_v1 | CAT02 | 5.7G 7.8/5.8 | very light green | ✅ | very light green | ✅ |
| E_v1 | XYZScaling | 6.5G 7.8/6.2 | very light green | ✅ | very light green | ✅ |

#### 144. #6AAB8E - Expected: light green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | VonKries | 2.6G 6.4/7.0 | light green | ✅ | moderate yellowish green | ❌ |
| E_v1 | Bradford | 5.5G 6.4/5.7 | light green | ✅ | light green | ✅ |
| E_v1 | VonKries | 4.9G 6.4/5.6 | light green | ✅ | light green | ✅ |
| E_v1 | CAT02 | 5.2G 6.4/5.7 | light green | ✅ | light green | ✅ |
| E_v1 | XYZScaling | 6.2G 6.4/6.1 | light green | ✅ | light green | ✅ |

#### 145. #3B7861 - Expected: moderate green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 3.2G 4.5/6.1 | moderate green | ✅ | moderate green | ✅ |
| D50_v1 | CAT02 | 3.0G 4.5/6.1 | moderate green | ✅ | moderate green | ✅ |
| D50_v1 | XYZScaling | 3.2G 4.5/6.2 | moderate green | ✅ | moderate green | ✅ |
| D55_v1 | Bradford | 5.4G 4.5/6.1 | moderate green | ✅ | moderate green | ✅ |
| D55_v1 | VonKries | 5.0G 4.5/6.0 | moderate green | ✅ | moderate green | ✅ |
| D55_v1 | CAT02 | 5.2G 4.5/6.1 | moderate green | ✅ | moderate green | ✅ |
| D55_v1 | XYZScaling | 5.4G 4.5/6.2 | moderate green | ✅ | moderate green | ✅ |
| E_v1 | Bradford | 6.4G 4.5/5.2 | moderate green | ✅ | moderate green | ✅ |
| E_v1 | VonKries | 5.8G 4.5/5.1 | moderate green | ✅ | moderate green | ✅ |
| E_v1 | CAT02 | 6.1G 4.5/5.1 | moderate green | ✅ | moderate green | ✅ |
| E_v1 | XYZScaling | 6.7G 4.5/5.4 | moderate green | ✅ | moderate green | ✅ |

#### 146. #1B4D3E - Expected: dark green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 3.3G 2.9/5.0 | dark green | ✅ | dark green | ✅ |
| D50_v1 | VonKries | 3.0G 2.9/5.0 | dark green | ✅ | dark green | ✅ |
| D50_v1 | CAT02 | 3.2G 2.9/5.1 | dark green | ✅ | dark green | ✅ |
| D50_v1 | XYZScaling | 3.2G 2.9/5.1 | dark green | ✅ | dark green | ✅ |
| D55_v1 | Bradford | 6.1G 2.9/5.1 | dark green | ✅ | dark green | ✅ |
| D55_v1 | VonKries | 5.5G 2.9/5.0 | dark green | ✅ | dark green | ✅ |
| D55_v1 | CAT02 | 5.8G 2.9/5.1 | dark green | ✅ | dark green | ✅ |
| D55_v1 | XYZScaling | 5.8G 2.9/5.1 | dark green | ✅ | dark green | ✅ |
| E_v1 | Bradford | 7.9G 2.9/4.4 | dark green | ✅ | dark green | ✅ |
| E_v1 | VonKries | 7.1G 2.9/4.3 | dark green | ✅ | dark green | ✅ |
| E_v1 | CAT02 | 7.5G 2.9/4.3 | dark green | ✅ | dark green | ✅ |
| E_v1 | XYZScaling | 8.2G 2.9/4.6 | dark green | ✅ | dark green | ✅ |

#### 147. #1C352D - Expected: very dark green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| C_v2 | VonKries | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| C_v2 | CAT02 | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| C_v2 | XYZScaling | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D55_v1 | Bradford | 3.1G 2.0/3.3 | very dark green | ✅ | very dark green | ✅ |
| D55_v1 | VonKries | 3.0G 2.0/3.3 | very dark green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | CAT02 | 3.1G 2.0/3.3 | very dark green | ✅ | very dark green | ✅ |
| D55_v1 | XYZScaling | 3.1G 2.0/3.3 | very dark green | ✅ | very dark green | ✅ |
| D65_v2 | Bradford | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D65_v2 | VonKries | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D65_v2 | CAT02 | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D65_v2 | XYZScaling | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | Bradford | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | VonKries | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | CAT02 | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | XYZScaling | 7.5G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| E_v1 | Bradford | 3.6G 2.0/2.7 | very dark green | ✅ | very dark green | ✅ |
| E_v2 | Bradford | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| E_v1 | VonKries | 3.3G 2.0/2.7 | very dark green | ✅ | very dark green | ✅ |
| E_v2 | VonKries | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| E_v1 | CAT02 | 3.4G 2.0/2.7 | very dark green | ✅ | very dark green | ✅ |
| E_v2 | CAT02 | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| E_v1 | XYZScaling | 3.8G 2.0/2.8 | very dark green | ✅ | very dark green | ✅ |
| E_v2 | XYZScaling | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | Bradford | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | VonKries | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | CAT02 | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | XYZScaling | 5.0G 2.0/2.0 | blackish green | ❌ | very dark green | ✅ |

#### 148. #C7E6D7 - Expected: very pale green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.4BG 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | Bradford | 7.5G 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v1 | VonKries | 9.4BG 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | VonKries | 7.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v1 | CAT02 | 9.4BG 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | CAT02 | 7.5G 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v1 | XYZScaling | 9.5BG 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | XYZScaling | 7.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | Bradford | 10.0GY 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | VonKries | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | CAT02 | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | XYZScaling | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | Bradford | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | VonKries | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | CAT02 | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | XYZScaling | 10.0GY 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | Bradford | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | VonKries | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | CAT02 | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | XYZScaling | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | Bradford | 7.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | VonKries | 7.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | CAT02 | 7.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | XYZScaling | 7.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | Bradford | 2.5G 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | VonKries | 2.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | CAT02 | 2.5G 8.8/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | XYZScaling | 2.5G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| F2_v2 | Bradford | 7.5GY 8.8/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F2_v2 | VonKries | 7.5GY 8.8/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F2_v2 | CAT02 | 7.5GY 8.8/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F2_v2 | XYZScaling | 7.5GY 8.9/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F7_v2 | Bradford | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | VonKries | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | CAT02 | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | XYZScaling | 5.0G 8.9/2.0 | very pale green | ✅ | very pale green | ✅ |

#### 149. #8DA399 - Expected: pale green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.8BG 6.4/1.5 | pale green | ✅ | pale green | ✅ |
| C_v2 | Bradford | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| C_v1 | VonKries | 7.8BG 6.4/1.5 | pale green | ✅ | pale green | ✅ |
| C_v2 | VonKries | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| C_v1 | CAT02 | 7.9BG 6.4/1.5 | pale green | ✅ | pale green | ✅ |
| C_v2 | CAT02 | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| C_v1 | XYZScaling | 7.9BG 6.4/1.6 | pale green | ✅ | pale green | ✅ |
| C_v2 | XYZScaling | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | Bradford | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | VonKries | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | CAT02 | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | XYZScaling | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | Bradford | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | VonKries | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | CAT02 | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | XYZScaling | 2.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v2 | Bradford | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v2 | VonKries | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v2 | CAT02 | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v2 | XYZScaling | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | Bradford | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | VonKries | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | CAT02 | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | XYZScaling | 7.5G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | Bradford | 9.5GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v2 | Bradford | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | VonKries | 9.3GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v2 | VonKries | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | CAT02 | 9.4GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v2 | CAT02 | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | XYZScaling | 9.9GY 6.4/2.1 | pale green | ✅ | pale green | ✅ |
| E_v2 | XYZScaling | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | Bradford | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | VonKries | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | CAT02 | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | XYZScaling | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v2 | Bradford | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v2 | VonKries | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v2 | CAT02 | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v2 | XYZScaling | 5.0G 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | Bradford | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | VonKries | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | CAT02 | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | XYZScaling | 10.0GY 6.4/2.0 | pale green | ✅ | pale green | ✅ |

#### 150. #5E716A - Expected: grayish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.9BG 4.5/1.3 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| C_v1 | VonKries | 7.9BG 4.5/1.3 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| C_v1 | CAT02 | 7.9BG 4.5/1.3 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| C_v1 | XYZScaling | 7.9BG 4.5/1.4 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | Bradford | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | VonKries | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | CAT02 | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | XYZScaling | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | Bradford | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | VonKries | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | CAT02 | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | XYZScaling | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | Bradford | 2.4BG 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | VonKries | 2.4BG 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | CAT02 | 2.4BG 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | XYZScaling | 2.4BG 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | Bradford | 0.4G 4.5/1.8 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | Bradford | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | VonKries | 0.3G 4.5/1.9 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | VonKries | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | CAT02 | 0.4G 4.5/1.8 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | CAT02 | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | XYZScaling | 0.6G 4.5/1.9 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | XYZScaling | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | Bradford | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | VonKries | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | CAT02 | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | XYZScaling | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | Bradford | 2.1BG 4.5/2.4 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | VonKries | 2.1BG 4.5/2.4 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | CAT02 | 2.1BG 4.5/2.4 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | XYZScaling | 2.1BG 4.5/2.4 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | Bradford | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | VonKries | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | CAT02 | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | XYZScaling | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |

#### 151. #3A4B47 - Expected: dark grayish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v2 | VonKries | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v2 | CAT02 | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v1 | XYZScaling | 9.4BG 3.0/1.2 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v2 | XYZScaling | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | Bradford | 2.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | VonKries | 2.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | CAT02 | 2.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | XYZScaling | 2.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | Bradford | 1.8G 3.0/2.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | Bradford | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | VonKries | 1.6G 3.0/2.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | VonKries | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | CAT02 | 1.7G 3.0/2.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | CAT02 | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | XYZScaling | 1.6G 3.0/2.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | XYZScaling | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | Bradford | 5.3BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | Bradford | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | VonKries | 5.3BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | VonKries | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | CAT02 | 5.3BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | CAT02 | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | XYZScaling | 5.3BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | XYZScaling | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | Bradford | 10.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | VonKries | 10.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | CAT02 | 10.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | XYZScaling | 10.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v1 | Bradford | 1.4G 3.0/1.6 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | Bradford | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v1 | VonKries | 1.1G 3.0/1.6 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | VonKries | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v1 | CAT02 | 1.2G 3.0/1.6 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | CAT02 | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v1 | XYZScaling | 1.6G 3.0/1.6 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | XYZScaling | 5.0G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | Bradford | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | VonKries | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | CAT02 | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | XYZScaling | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | Bradford | 5.2BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | Bradford | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | VonKries | 5.1BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | VonKries | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | CAT02 | 5.2BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | CAT02 | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | XYZScaling | 5.1BG 3.0/1.8 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | XYZScaling | 7.5G 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | Bradford | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | VonKries | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | CAT02 | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | XYZScaling | 10.0GY 3.0/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |

#### 152. #1A2421 - Expected: blackish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| C_v2 | VonKries | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| C_v2 | CAT02 | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| C_v2 | XYZScaling | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| D50_v1 | Bradford | 7.4GY 1.3/1.9 | blackish green | ✅ | dark olive green | ❌ |
| D50_v2 | Bradford | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D50_v1 | VonKries | 7.4GY 1.3/1.9 | blackish green | ✅ | dark olive green | ❌ |
| D50_v2 | VonKries | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D50_v1 | CAT02 | 7.4GY 1.3/1.9 | blackish green | ✅ | dark olive green | ❌ |
| D50_v2 | CAT02 | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D50_v1 | XYZScaling | 7.4GY 1.3/1.9 | blackish green | ✅ | dark olive green | ❌ |
| D50_v2 | XYZScaling | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | Bradford | 9.5GY 1.3/1.8 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | Bradford | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | VonKries | 9.4GY 1.3/1.8 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | VonKries | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | CAT02 | 9.5GY 1.3/1.8 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | CAT02 | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | XYZScaling | 9.5GY 1.3/1.8 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | XYZScaling | 2.5G 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D65_v1 | Bradford | 6.9G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | Bradford | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | VonKries | 6.9G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | VonKries | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | CAT02 | 6.9G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | CAT02 | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | XYZScaling | 6.9G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | XYZScaling | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| D75_v1 | Bradford | 8.4BG 1.3/1.1 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | Bradford | 10.0G 1.3/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D75_v1 | VonKries | 8.5BG 1.3/1.1 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | VonKries | 10.0G 1.3/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D75_v1 | CAT02 | 8.5BG 1.3/1.1 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | CAT02 | 10.0G 1.3/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D75_v1 | XYZScaling | 8.5BG 1.3/1.1 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | XYZScaling | 10.0G 1.3/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| E_v1 | Bradford | 9.0GY 1.3/1.2 | blackish green | ✅ | blackish green | ✅ |
| E_v2 | Bradford | 5.0G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| E_v1 | VonKries | 8.8GY 1.3/1.2 | blackish green | ✅ | blackish green | ✅ |
| E_v2 | VonKries | 5.0G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| E_v1 | CAT02 | 8.9GY 1.3/1.2 | blackish green | ✅ | blackish green | ✅ |
| E_v2 | CAT02 | 5.0G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| E_v1 | XYZScaling | 9.3GY 1.3/1.3 | blackish green | ✅ | blackish green | ✅ |
| E_v2 | XYZScaling | 5.0G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| F2_v2 | Bradford | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F2_v2 | VonKries | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F2_v2 | CAT02 | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F2_v2 | XYZScaling | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F7_v1 | Bradford | 6.6G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | Bradford | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| F7_v1 | VonKries | 6.6G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | VonKries | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| F7_v1 | CAT02 | 6.6G 1.3/1.7 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | CAT02 | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| F7_v1 | XYZScaling | 6.6G 1.3/1.6 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | XYZScaling | 7.5G 1.3/2.0 | blackish green | ✅ | very dark green | ❌ |
| F11_v2 | Bradford | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F11_v2 | VonKries | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F11_v2 | CAT02 | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F11_v2 | XYZScaling | 10.0GY 1.3/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |

#### 153. #DFEDE8 - Expected: greenish white

No matches

#### 154. #B2BEB5 - Expected: light greenish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.4G 7.5/1.1 | light greenish gray | ✅ | light greenish gray | ✅ |
| C_v1 | VonKries | 7.7G 7.5/1.1 | light greenish gray | ✅ | light greenish gray | ✅ |
| C_v1 | CAT02 | 7.5G 7.5/1.1 | light greenish gray | ✅ | light greenish gray | ✅ |
| C_v1 | XYZScaling | 7.9G 7.5/1.1 | light greenish gray | ✅ | light greenish gray | ✅ |

#### 155. #7D8984 - Expected: greenish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.2BG 5.5/0.8 | greenish gray | ✅ | greenish gray | ✅ |
| C_v1 | VonKries | 8.1BG 5.5/0.8 | greenish gray | ✅ | greenish gray | ✅ |
| C_v1 | CAT02 | 8.2BG 5.5/0.8 | greenish gray | ✅ | greenish gray | ✅ |
| C_v1 | XYZScaling | 8.2BG 5.5/0.8 | greenish gray | ✅ | greenish gray | ✅ |

#### 156. #4E5755 - Expected: dark greenish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 9.6BG 3.6/1.1 | dark bluish gray | ❌ | dark greenish gray | ✅ |
| D75_v1 | VonKries | 9.6BG 3.6/1.1 | dark bluish gray | ❌ | dark greenish gray | ✅ |
| D75_v1 | CAT02 | 9.6BG 3.6/1.1 | dark bluish gray | ❌ | dark greenish gray | ✅ |
| D75_v1 | XYZScaling | 9.6BG 3.6/1.1 | dark bluish gray | ❌ | dark greenish gray | ✅ |
| E_v1 | Bradford | 6.4GY 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| E_v1 | VonKries | 6.3GY 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| E_v1 | CAT02 | 6.3GY 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| E_v1 | XYZScaling | 6.6GY 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |

#### 157. #1E2321 - Expected: greenish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.7BG 1.3/0.6 | greenish black | ✅ | greenish black | ✅ |
| C_v1 | VonKries | 1.7BG 1.3/0.6 | greenish black | ✅ | greenish black | ✅ |
| C_v1 | CAT02 | 1.8BG 1.3/0.6 | greenish black | ✅ | greenish black | ✅ |
| C_v1 | XYZScaling | 1.8BG 1.3/0.6 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | Bradford | 8.5BG 1.3/0.7 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | VonKries | 8.5BG 1.3/0.7 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | CAT02 | 8.5BG 1.3/0.7 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | XYZScaling | 8.5BG 1.3/0.7 | greenish black | ✅ | greenish black | ✅ |

#### 158. #008882 - Expected: vivid bluish green

No matches

#### 159. #00A693 - Expected: brilliant bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 5.4BG 6.0/9.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D50_v1 | VonKries | 5.1BG 6.0/9.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D50_v1 | CAT02 | 5.3BG 6.0/9.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D50_v1 | XYZScaling | 5.1BG 6.0/9.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D55_v1 | Bradford | 7.5BG 6.0/8.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D55_v1 | VonKries | 7.4BG 6.0/8.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D55_v1 | CAT02 | 7.5BG 6.0/8.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D55_v1 | XYZScaling | 7.4BG 6.0/8.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D65_v1 | Bradford | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| D65_v1 | VonKries | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| D65_v1 | CAT02 | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| D65_v1 | XYZScaling | 10.0BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| F7_v1 | Bradford | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| F7_v1 | VonKries | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| F7_v1 | CAT02 | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |
| F7_v1 | XYZScaling | 9.9BG 6.0/7.1 | brilliant greenish blue | ❌ | brilliant bluish green | ✅ |

#### 160. #007A74 - Expected: strong bluish green

No matches

#### 161. #00443F - Expected: deep bluish green

No matches

#### 162. #96DED1 - Expected: very light bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D55_v1 | Bradford | 5.2BG 8.3/5.9 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | VonKries | 5.0BG 8.3/6.0 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | CAT02 | 5.2BG 8.3/6.0 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | XYZScaling | 4.8BG 8.3/6.0 | very light bluish green | ✅ | very light bluish green | ✅ |
| E_v1 | Bradford | 7.1BG 8.3/4.0 | very light bluish green | ✅ | very light bluish green | ✅ |
| E_v1 | VonKries | 6.7BG 8.3/4.0 | very light bluish green | ✅ | very light bluish green | ✅ |
| E_v1 | CAT02 | 7.0BG 8.3/4.0 | very light bluish green | ✅ | very light bluish green | ✅ |
| E_v1 | XYZScaling | 7.1BG 8.3/4.1 | very light bluish green | ✅ | very light bluish green | ✅ |

#### 163. #66ADA4 - Expected: light bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 0.3BG 6.5/6.3 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | VonKries | 9.7G 6.5/6.3 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | CAT02 | 0.1BG 6.5/6.3 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | XYZScaling | 9.5G 6.5/6.3 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | Bradford | 6.5BG 6.5/5.2 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | VonKries | 6.3BG 6.5/5.2 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | CAT02 | 6.4BG 6.5/5.2 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | XYZScaling | 6.2BG 6.5/5.2 | light bluish green | ✅ | light bluish green | ✅ |
| E_v1 | Bradford | 8.6BG 6.5/3.5 | light bluish green | ✅ | light bluish green | ✅ |
| E_v1 | VonKries | 8.2BG 6.5/3.6 | light bluish green | ✅ | light bluish green | ✅ |
| E_v1 | CAT02 | 8.5BG 6.5/3.5 | light bluish green | ✅ | light bluish green | ✅ |
| E_v1 | XYZScaling | 8.4BG 6.5/3.7 | light bluish green | ✅ | light bluish green | ✅ |

#### 164. #317873 - Expected: moderate bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 10.0BG 4.5/3.9 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| C_v1 | VonKries | 10.0BG 4.5/3.9 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| C_v1 | CAT02 | 10.0BG 4.5/3.9 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | Bradford | 4.8BG 4.5/5.0 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | VonKries | 4.2BG 4.5/5.2 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | CAT02 | 4.7BG 4.5/5.1 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | XYZScaling | 3.8BG 4.5/5.1 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | Bradford | 7.6BG 4.5/4.3 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | VonKries | 7.5BG 4.5/4.4 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | CAT02 | 7.6BG 4.5/4.4 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | XYZScaling | 7.5BG 4.5/4.3 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | Bradford | 9.5BG 4.5/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | VonKries | 9.5BG 4.5/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | CAT02 | 9.5BG 4.5/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | XYZScaling | 9.5BG 4.5/4.7 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| E_v1 | Bradford | 9.2BG 4.5/3.3 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| E_v1 | VonKries | 8.8BG 4.5/3.3 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| E_v1 | CAT02 | 9.1BG 4.5/3.3 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| E_v1 | XYZScaling | 8.8BG 4.5/3.4 | moderate bluish green | ✅ | moderate bluish green | ✅ |

#### 165. #004B49 - Expected: dark bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.9BG 2.8/3.8 | dark bluish green | ✅ | dark bluish green | ✅ |
| C_v1 | VonKries | 7.9BG 2.8/3.8 | dark bluish green | ✅ | dark bluish green | ✅ |
| C_v1 | CAT02 | 7.9BG 2.8/3.8 | dark bluish green | ✅ | dark bluish green | ✅ |
| C_v1 | XYZScaling | 8.0BG 2.8/3.9 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | Bradford | 5.7BG 2.8/4.1 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | VonKries | 5.5BG 2.8/4.2 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | CAT02 | 5.6BG 2.8/4.1 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | XYZScaling | 5.3BG 2.8/4.0 | dark bluish green | ✅ | dark bluish green | ✅ |
| D55_v1 | Bradford | 8.0BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D55_v1 | VonKries | 7.8BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D55_v1 | CAT02 | 8.0BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D55_v1 | XYZScaling | 7.8BG 2.8/3.6 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | Bradford | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | VonKries | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | CAT02 | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | XYZScaling | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | Bradford | 7.6BG 2.8/4.3 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | VonKries | 7.6BG 2.8/4.4 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | CAT02 | 7.6BG 2.8/4.3 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | XYZScaling | 7.6BG 2.8/4.4 | dark bluish green | ✅ | dark bluish green | ✅ |
| E_v1 | VonKries | 9.8BG 2.8/2.9 | dark grayish blue | ❌ | dark bluish green | ✅ |
| E_v1 | CAT02 | 10.0BG 2.8/2.9 | dark grayish blue | ❌ | dark bluish green | ✅ |
| E_v1 | XYZScaling | 9.7BG 2.8/3.0 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | Bradford | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | VonKries | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | CAT02 | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | XYZScaling | 9.3BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |

#### 166. #002A29 - Expected: very dark bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.6BG 1.4/2.8 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | Bradford | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| C_v1 | VonKries | 6.6BG 1.4/2.8 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | VonKries | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| C_v1 | CAT02 | 6.6BG 1.4/2.8 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | CAT02 | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| C_v1 | XYZScaling | 6.7BG 1.4/2.9 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | XYZScaling | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D50_v1 | Bradford | 2.9BG 1.4/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D50_v1 | VonKries | 2.3BG 1.4/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D50_v1 | CAT02 | 2.8BG 1.4/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D50_v1 | XYZScaling | 1.9BG 1.4/3.0 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v1 | Bradford | 6.9BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v1 | VonKries | 6.7BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v1 | CAT02 | 6.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v1 | XYZScaling | 6.6BG 1.4/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v1 | Bradford | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | Bradford | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | VonKries | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | VonKries | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | CAT02 | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | CAT02 | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | XYZScaling | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | XYZScaling | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | Bradford | 6.4BG 1.4/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | Bradford | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | VonKries | 6.3BG 1.4/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | VonKries | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | CAT02 | 6.4BG 1.4/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | CAT02 | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | XYZScaling | 6.4BG 1.4/3.2 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | XYZScaling | 2.5BG 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v1 | Bradford | 8.6BG 1.4/2.2 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| E_v2 | Bradford | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v1 | VonKries | 8.8BG 1.4/2.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| E_v2 | VonKries | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v1 | CAT02 | 8.6BG 1.4/2.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| E_v2 | CAT02 | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v1 | XYZScaling | 8.8BG 1.4/2.2 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| E_v2 | XYZScaling | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | Bradford | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | Bradford | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | VonKries | 7.9BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | VonKries | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | CAT02 | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | CAT02 | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | XYZScaling | 7.8BG 1.4/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | XYZScaling | 10.0G 1.4/2.0 | blackish green | ❌ | very dark bluish green | ✅ |

#### 167. #0085A1 - Expected: vivid greenish blue

No matches

#### 168. #239EBA - Expected: brilliant greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.8B 5.9/7.8 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| C_v1 | VonKries | 2.9B 5.9/7.7 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| C_v1 | CAT02 | 2.8B 5.9/7.7 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| C_v1 | XYZScaling | 2.5B 5.9/7.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | Bradford | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | VonKries | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | CAT02 | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | XYZScaling | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | Bradford | 2.6B 5.9/8.5 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | VonKries | 2.7B 5.9/8.5 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | CAT02 | 2.6B 5.9/8.5 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | XYZScaling | 2.3B 5.9/8.8 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | Bradford | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | VonKries | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | CAT02 | 1.3B 5.9/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | XYZScaling | 1.3B 5.9/7.5 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |

#### 169. #007791 - Expected: strong greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 2.4B 4.5/7.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | VonKries | 2.5B 4.5/7.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | CAT02 | 2.3B 4.5/7.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | XYZScaling | 2.1B 4.5/7.6 | strong greenish blue | ✅ | strong greenish blue | ✅ |

#### 170. #2E8495 - Expected: deep greenish blue

No matches

#### 171. #9CD1DC - Expected: very light greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.4B 8.0/4.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| C_v1 | VonKries | 2.5B 8.0/4.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| C_v1 | CAT02 | 2.4B 8.0/4.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| C_v1 | XYZScaling | 2.2B 8.0/4.2 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | Bradford | 1.3B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | VonKries | 1.3B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | CAT02 | 1.3B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | XYZScaling | 1.3B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | Bradford | 2.1B 8.0/5.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | VonKries | 2.2B 8.0/5.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | CAT02 | 2.1B 8.0/5.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | XYZScaling | 2.0B 8.0/5.2 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | Bradford | 1.4B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | VonKries | 1.4B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | CAT02 | 1.4B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | XYZScaling | 1.4B 8.0/3.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |

#### 172. #66AABC - Expected: light greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.6B 6.5/5.5 | light greenish blue | ✅ | light greenish blue | ✅ |
| C_v1 | VonKries | 2.7B 6.5/5.4 | light greenish blue | ✅ | light greenish blue | ✅ |
| C_v1 | CAT02 | 2.6B 6.5/5.4 | light greenish blue | ✅ | light greenish blue | ✅ |
| C_v1 | XYZScaling | 2.4B 6.5/5.6 | light greenish blue | ✅ | light greenish blue | ✅ |
| D50_v1 | Bradford | 1.2B 6.5/3.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| D50_v1 | VonKries | 0.9B 6.5/3.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D50_v1 | CAT02 | 1.4B 6.5/3.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| D55_v1 | Bradford | 1.2B 6.5/3.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D55_v1 | VonKries | 1.4B 6.5/3.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D55_v1 | CAT02 | 1.1B 6.5/3.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D55_v1 | XYZScaling | 1.3B 6.5/3.4 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | Bradford | 0.4B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | VonKries | 0.4B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | CAT02 | 0.4B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | XYZScaling | 0.4B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | Bradford | 2.3B 6.5/6.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | VonKries | 2.4B 6.5/6.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | CAT02 | 2.3B 6.5/6.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | XYZScaling | 2.1B 6.5/6.5 | light greenish blue | ✅ | light greenish blue | ✅ |
| E_v1 | Bradford | 0.0B 6.5/3.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| E_v1 | CAT02 | 0.0B 6.5/3.6 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | Bradford | 0.3B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | VonKries | 0.3B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | CAT02 | 0.3B 6.5/5.3 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | XYZScaling | 0.3B 6.5/5.2 | light greenish blue | ✅ | light greenish blue | ✅ |

#### 173. #367588 - Expected: moderate greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.4B 4.5/5.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| C_v1 | VonKries | 2.4B 4.5/5.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| C_v1 | CAT02 | 2.3B 4.5/5.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| C_v1 | XYZScaling | 2.1B 4.5/5.3 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D50_v1 | Bradford | 0.2B 4.5/3.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D50_v1 | VonKries | 0.6B 4.5/3.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D50_v1 | CAT02 | 0.1B 4.5/3.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | Bradford | 0.6B 4.5/5.0 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | VonKries | 0.6B 4.5/5.0 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | CAT02 | 0.6B 4.5/5.0 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | XYZScaling | 0.6B 4.5/5.0 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | Bradford | 2.0B 4.5/5.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | VonKries | 2.2B 4.5/5.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | CAT02 | 2.0B 4.5/5.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | XYZScaling | 1.8B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | Bradford | 0.6B 4.5/3.8 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | VonKries | 0.4B 4.5/3.8 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | CAT02 | 0.6B 4.5/3.8 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | XYZScaling | 0.5B 4.5/3.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | Bradford | 0.5B 4.5/4.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | VonKries | 0.5B 4.5/4.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | CAT02 | 0.5B 4.5/4.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | XYZScaling | 0.5B 4.5/4.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |

#### 174. #004958 - Expected: dark greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.1B 2.8/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| C_v1 | VonKries | 1.1B 2.8/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| C_v1 | CAT02 | 1.0B 2.8/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| C_v1 | XYZScaling | 0.8B 2.8/4.8 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | Bradford | 0.9B 2.8/5.1 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | VonKries | 1.0B 2.8/5.1 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | CAT02 | 0.8B 2.8/5.1 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | XYZScaling | 0.6B 2.8/5.3 | dark greenish blue | ✅ | dark greenish blue | ✅ |

#### 175. #002E3B - Expected: very dark greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.3B 1.7/3.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| C_v1 | VonKries | 1.4B 1.7/3.6 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| C_v1 | CAT02 | 1.3B 1.7/3.6 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| C_v1 | XYZScaling | 1.1B 1.7/3.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | Bradford | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | VonKries | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | CAT02 | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | XYZScaling | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | Bradford | 1.1B 1.7/3.9 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | VonKries | 1.3B 1.7/3.9 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | CAT02 | 1.1B 1.7/3.9 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | XYZScaling | 0.9B 1.7/4.1 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | Bradford | 0.2B 1.6/3.0 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | VonKries | 0.1B 1.7/3.0 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | CAT02 | 0.2B 1.6/3.0 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | XYZScaling | 0.3B 1.7/2.9 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | Bradford | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | VonKries | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | CAT02 | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | XYZScaling | 0.1B 1.7/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |

#### 176. #00A1C2 - Expected: vivid blue

No matches

#### 177. #4997D0 - Expected: brilliant blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.7PB 5.9/9.3 | brilliant blue | ✅ | brilliant blue | ✅ |
| C_v1 | VonKries | 2.1PB 5.9/9.3 | brilliant blue | ✅ | brilliant blue | ✅ |
| C_v1 | CAT02 | 1.6PB 5.9/9.3 | brilliant blue | ✅ | brilliant blue | ✅ |
| C_v1 | XYZScaling | 1.0PB 5.9/9.4 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | Bradford | 0.7PB 5.9/9.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | VonKries | 1.2PB 5.9/9.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | CAT02 | 0.7PB 5.9/9.8 | brilliant blue | ✅ | brilliant blue | ✅ |

#### 178. #0067A5 - Expected: strong blue

No matches

#### 179. #00416A - Expected: deep blue

No matches

#### 180. #A1CAF1 - Expected: very light blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.0PB 7.9/6.1 | very light purplish blue | ❌ | very light blue | ✅ |
| C_v1 | VonKries | 4.4PB 7.9/6.1 | very light purplish blue | ❌ | very light blue | ✅ |
| C_v1 | CAT02 | 4.0PB 7.9/6.1 | very light blue | ✅ | very light blue | ✅ |
| C_v1 | XYZScaling | 3.5PB 7.9/6.1 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | Bradford | 1.6PB 7.9/6.7 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | VonKries | 2.0PB 7.9/6.7 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | CAT02 | 1.6PB 7.9/6.6 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | XYZScaling | 0.8PB 7.9/6.8 | very light blue | ✅ | very light blue | ✅ |

#### 181. #70A3CC - Expected: light blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.0PB 6.4/6.9 | light blue | ✅ | light blue | ✅ |
| C_v1 | VonKries | 2.3PB 6.4/6.9 | light blue | ✅ | light blue | ✅ |
| C_v1 | CAT02 | 1.9PB 6.4/6.9 | light blue | ✅ | light blue | ✅ |
| C_v1 | XYZScaling | 1.4PB 6.4/6.9 | light blue | ✅ | light blue | ✅ |
| D75_v1 | Bradford | 0.4PB 6.4/7.4 | light blue | ✅ | light blue | ✅ |
| D75_v1 | VonKries | 0.8PB 6.4/7.4 | light blue | ✅ | light blue | ✅ |
| D75_v1 | CAT02 | 0.3PB 6.4/7.4 | light blue | ✅ | light blue | ✅ |

#### 182. #436B95 - Expected: moderate blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.6PB 4.3/6.5 | moderate blue | ✅ | moderate blue | ✅ |
| C_v1 | VonKries | 2.7PB 4.3/6.5 | moderate blue | ✅ | moderate blue | ✅ |
| C_v1 | CAT02 | 2.6PB 4.3/6.5 | moderate blue | ✅ | moderate blue | ✅ |
| C_v1 | XYZScaling | 2.3PB 4.3/6.6 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | Bradford | 0.8PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | VonKries | 0.8PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | CAT02 | 0.8PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | XYZScaling | 0.8PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| D75_v1 | Bradford | 1.9PB 4.3/6.9 | moderate blue | ✅ | moderate blue | ✅ |
| D75_v1 | VonKries | 2.1PB 4.3/6.9 | moderate blue | ✅ | moderate blue | ✅ |
| D75_v1 | CAT02 | 1.9PB 4.3/6.9 | moderate blue | ✅ | moderate blue | ✅ |
| D75_v1 | XYZScaling | 1.0PB 4.3/7.1 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | Bradford | 0.7PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | VonKries | 0.7PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | CAT02 | 0.7PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | XYZScaling | 0.7PB 4.3/5.8 | moderate blue | ✅ | moderate blue | ✅ |

#### 183. #00304E - Expected: dark blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| C_v2 | VonKries | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| C_v2 | CAT02 | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| C_v2 | XYZScaling | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D65_v2 | Bradford | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D65_v2 | VonKries | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D65_v2 | CAT02 | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D65_v2 | XYZScaling | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D75_v2 | Bradford | 5.0PB 1.9/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D75_v2 | VonKries | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D75_v2 | CAT02 | 5.0PB 1.9/2.0 | dark blue | ✅ | blackish blue | ❌ |
| D75_v2 | XYZScaling | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| F7_v2 | Bradford | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| F7_v2 | VonKries | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| F7_v2 | CAT02 | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |
| F7_v2 | XYZScaling | 5.0PB 1.8/2.0 | dark blue | ✅ | blackish blue | ❌ |

#### 184. #BCD4E6 - Expected: very pale blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.7PB 8.3/3.4 | very pale blue | ✅ | very pale blue | ✅ |
| C_v1 | VonKries | 4.1PB 8.3/3.4 | very pale blue | ✅ | very pale blue | ✅ |
| C_v1 | CAT02 | 3.6PB 8.3/3.4 | very pale blue | ✅ | very pale blue | ✅ |
| C_v1 | XYZScaling | 2.9PB 8.3/3.4 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | Bradford | 2.2B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | VonKries | 2.2B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | CAT02 | 2.2B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | XYZScaling | 2.2B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | Bradford | 2.1B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | VonKries | 2.1B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | CAT02 | 2.1B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | XYZScaling | 2.1B 8.3/2.6 | very pale blue | ✅ | very pale blue | ✅ |

#### 185. #91A3B0 - Expected: pale blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.4B 6.5/2.6 | pale blue | ✅ | pale blue | ✅ |
| C_v1 | VonKries | 9.0B 6.5/2.6 | pale blue | ✅ | pale blue | ✅ |
| C_v1 | CAT02 | 8.2B 6.5/2.5 | pale blue | ✅ | pale blue | ✅ |
| C_v1 | XYZScaling | 7.2B 6.5/2.6 | pale blue | ✅ | pale blue | ✅ |
| D65_v1 | Bradford | 0.8B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| D65_v1 | VonKries | 0.8B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| D65_v1 | CAT02 | 0.8B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| D65_v1 | XYZScaling | 0.8B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| F7_v1 | Bradford | 0.7B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| F7_v1 | VonKries | 0.7B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| F7_v1 | CAT02 | 0.7B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |
| F7_v1 | XYZScaling | 0.7B 6.5/2.0 | pale blue | ✅ | pale blue | ✅ |

#### 186. #536878 - Expected: grayish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.3PB 4.2/2.9 | grayish blue | ✅ | grayish blue | ✅ |
| C_v1 | VonKries | 0.6PB 4.2/2.9 | grayish blue | ✅ | grayish blue | ✅ |
| C_v1 | CAT02 | 0.3PB 4.2/2.9 | grayish blue | ✅ | grayish blue | ✅ |
| C_v1 | XYZScaling | 4.7B 4.2/3.0 | grayish blue | ✅ | grayish blue | ✅ |
| D65_v1 | Bradford | 2.4B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| D65_v1 | VonKries | 2.4B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| D65_v1 | CAT02 | 2.4B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| D65_v1 | XYZScaling | 2.4B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | Bradford | 3.9B 4.2/1.5 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | VonKries | 3.6B 4.2/1.5 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | CAT02 | 3.9B 4.2/1.5 | grayish blue | ✅ | grayish blue | ✅ |
| F7_v1 | Bradford | 2.3B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| F7_v1 | VonKries | 2.3B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| F7_v1 | CAT02 | 2.3B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |
| F7_v1 | XYZScaling | 2.3B 4.2/2.6 | grayish blue | ✅ | grayish blue | ✅ |

#### 187. #36454F - Expected: dark grayish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.5B 2.8/2.1 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| C_v1 | VonKries | 3.6B 2.8/2.1 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| C_v1 | CAT02 | 3.5B 2.8/2.1 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| C_v1 | XYZScaling | 3.3B 2.8/2.1 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | Bradford | 0.7B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | VonKries | 0.7B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | CAT02 | 0.7B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | XYZScaling | 0.7B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | Bradford | 2.6B 2.8/2.5 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | VonKries | 2.8B 2.8/2.5 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | CAT02 | 2.6B 2.8/2.5 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | XYZScaling | 2.4B 2.8/2.6 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | Bradford | 0.6B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | VonKries | 0.6B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | CAT02 | 0.6B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | XYZScaling | 0.6B 2.8/1.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |

#### 188. #202830 - Expected: blackish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.9B 1.5/1.5 | blackish blue | ✅ | blackish blue | ✅ |
| C_v1 | VonKries | 4.1B 1.5/1.5 | blackish blue | ✅ | blackish blue | ✅ |
| C_v1 | CAT02 | 3.9B 1.5/1.5 | blackish blue | ✅ | blackish blue | ✅ |
| C_v1 | XYZScaling | 3.7B 1.5/1.6 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | Bradford | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | VonKries | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | CAT02 | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | XYZScaling | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| D75_v1 | Bradford | 2.9B 1.5/1.8 | blackish blue | ✅ | blackish blue | ✅ |
| D75_v1 | VonKries | 3.1B 1.5/1.8 | blackish blue | ✅ | blackish blue | ✅ |
| D75_v1 | CAT02 | 2.9B 1.5/1.8 | blackish blue | ✅ | blackish blue | ✅ |
| D75_v1 | XYZScaling | 2.7B 1.5/1.9 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | Bradford | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | VonKries | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | CAT02 | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | XYZScaling | 1.6B 1.5/1.4 | blackish blue | ✅ | blackish blue | ✅ |

#### 189. #E9E9ED - Expected: bluish white

No matches

#### 190. #B4BCC0 - Expected: light bluish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.6B 7.5/1.0 | light bluish gray | ✅ | light bluish gray | ✅ |
| C_v1 | VonKries | 4.7B 7.5/1.0 | light bluish gray | ✅ | light bluish gray | ✅ |
| C_v1 | CAT02 | 4.5B 7.5/1.0 | light bluish gray | ✅ | light bluish gray | ✅ |
| C_v1 | XYZScaling | 4.3B 7.5/1.0 | light bluish gray | ✅ | light bluish gray | ✅ |

#### 191. #81878B - Expected: bluish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.5B 5.5/0.8 | bluish gray | ✅ | bluish gray | ✅ |
| C_v1 | VonKries | 4.7B 5.5/0.8 | bluish gray | ✅ | bluish gray | ✅ |
| C_v1 | CAT02 | 4.5B 5.5/0.8 | bluish gray | ✅ | bluish gray | ✅ |
| C_v1 | XYZScaling | 4.3B 5.5/0.9 | bluish gray | ✅ | bluish gray | ✅ |

#### 192. #51585E - Expected: dark bluish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.2PB 3.6/1.0 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| C_v1 | VonKries | 0.4PB 3.6/1.0 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| C_v1 | CAT02 | 0.1PB 3.6/1.0 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| C_v1 | XYZScaling | 4.3B 3.6/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |

#### 193. #202428 - Expected: bluish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.5B 1.4/0.8 | bluish black | ✅ | bluish black | ✅ |
| C_v1 | VonKries | 3.7B 1.4/0.8 | bluish black | ✅ | bluish black | ✅ |
| C_v1 | CAT02 | 3.5B 1.4/0.8 | bluish black | ✅ | bluish black | ✅ |
| C_v1 | XYZScaling | 3.3B 1.4/0.8 | bluish black | ✅ | bluish black | ✅ |

#### 194. #30267A - Expected: vivid purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | XYZScaling | 6.4PB 2.1/11.1 | vivid purplish blue | ✅ | vivid blue | ❌ |

#### 195. #6C79B8 - Expected: brilliant purplish blue

No matches

#### 196. #545AA7 - Expected: strong purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | XYZScaling | 7.9PB 4.0/11.7 | strong purplish blue | ✅ | strong purplish blue | ✅ |

#### 197. #272458 - Expected: deep purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 7.4PB 1.7/7.1 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D75_v1 | Bradford | 7.0PB 1.7/7.2 | deep purplish blue | ✅ | deep blue | ❌ |
| D75_v1 | CAT02 | 7.0PB 1.7/7.2 | deep purplish blue | ✅ | deep purplish blue | ✅ |

#### 198. #B3BCE2 - Expected: very light purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 7.1PB 7.6/5.9 | very light purplish blue | ✅ | very light purplish blue | ✅ |
| D75_v1 | VonKries | 7.4PB 7.6/5.9 | very light purplish blue | ✅ | very light purplish blue | ✅ |
| D75_v1 | CAT02 | 7.0PB 7.6/5.8 | very light purplish blue | ✅ | very light purplish blue | ✅ |
| D75_v1 | XYZScaling | 6.4PB 7.6/5.9 | very light purplish blue | ✅ | very light purplish blue | ✅ |

#### 199. #8791BF - Expected: light purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.6PB 6.0/6.8 | light violet | ❌ | light purplish blue | ✅ |
| C_v1 | VonKries | 8.7PB 6.0/6.8 | light violet | ❌ | light purplish blue | ✅ |
| C_v1 | CAT02 | 8.6PB 6.0/6.8 | light violet | ❌ | light purplish blue | ✅ |
| C_v1 | XYZScaling | 8.4PB 6.0/6.8 | light violet | ❌ | light purplish blue | ✅ |
| D65_v1 | Bradford | 7.4PB 6.0/5.6 | light purplish blue | ✅ | light purplish blue | ✅ |
| D65_v1 | VonKries | 7.4PB 6.0/5.6 | light purplish blue | ✅ | light purplish blue | ✅ |
| D65_v1 | CAT02 | 7.4PB 6.0/5.6 | light purplish blue | ✅ | light purplish blue | ✅ |
| D65_v1 | XYZScaling | 7.4PB 6.0/5.6 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | Bradford | 7.1PB 6.0/7.1 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | VonKries | 7.5PB 6.0/7.2 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | CAT02 | 7.1PB 6.0/7.1 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | XYZScaling | 6.3PB 6.0/7.1 | light purplish blue | ✅ | light blue | ❌ |
| F7_v1 | Bradford | 7.4PB 6.0/5.5 | light purplish blue | ✅ | light purplish blue | ✅ |
| F7_v1 | VonKries | 7.4PB 6.0/5.5 | light purplish blue | ✅ | light purplish blue | ✅ |
| F7_v1 | CAT02 | 7.4PB 6.0/5.5 | light purplish blue | ✅ | light purplish blue | ✅ |
| F7_v1 | XYZScaling | 7.4PB 6.0/5.5 | light purplish blue | ✅ | light purplish blue | ✅ |

#### 200. #4E5180 - Expected: moderate purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 8.7PB 3.6/6.9 | moderate violet | ❌ | moderate purplish blue | ✅ |
| D75_v1 | CAT02 | 8.6PB 3.6/6.9 | moderate violet | ❌ | moderate purplish blue | ✅ |

#### 201. #252440 - Expected: dark purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 8.4PB 1.5/3.8 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | Bradford | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | VonKries | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | CAT02 | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | XYZScaling | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D75_v1 | Bradford | 7.2PB 1.5/3.9 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D75_v1 | VonKries | 7.6PB 1.5/3.9 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D75_v1 | CAT02 | 7.3PB 1.5/3.9 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D75_v1 | XYZScaling | 5.9PB 1.5/3.8 | dark purplish blue | ✅ | dark blue | ❌ |
| E_v1 | XYZScaling | 6.7PB 1.5/2.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | Bradford | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | VonKries | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | CAT02 | 8.3PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | XYZScaling | 8.4PB 1.5/3.3 | dark purplish blue | ✅ | dark purplish blue | ✅ |

#### 202. #C0C8E1 - Expected: very pale purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 6.3PB 8.0/4.4 | very pale purplish blue | ✅ | very pale purplish blue | ✅ |
| D75_v1 | VonKries | 6.5PB 8.0/4.4 | very pale purplish blue | ✅ | very pale purplish blue | ✅ |
| D75_v1 | CAT02 | 6.2PB 8.0/4.4 | very pale purplish blue | ✅ | very pale purplish blue | ✅ |
| D75_v1 | XYZScaling | 5.7PB 8.0/4.4 | very pale purplish blue | ✅ | very pale purplish blue | ✅ |

#### 203. #8C92AC - Expected: pale purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 6.1PB 6.0/4.4 | pale purplish blue | ✅ | pale purplish blue | ✅ |
| D75_v1 | VonKries | 6.4PB 6.0/4.4 | pale purplish blue | ✅ | pale purplish blue | ✅ |
| D75_v1 | CAT02 | 6.1PB 6.0/4.4 | pale purplish blue | ✅ | pale purplish blue | ✅ |
| D75_v1 | XYZScaling | 5.5PB 6.0/4.4 | pale purplish blue | ✅ | pale purplish blue | ✅ |

#### 204. #4C516D - Expected: grayish purplish blue

No matches

#### 205. #9065CA - Expected: vivid violet

No matches

#### 206. #7E73B8 - Expected: brilliant violet

No matches

#### 207. #604E97 - Expected: strong violet

No matches

#### 208. #32174D - Expected: deep violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.4P 1.4/8.0 | deep violet | ✅ | deep violet | ✅ |
| C_v1 | CAT02 | 2.3P 1.4/7.9 | deep violet | ✅ | deep violet | ✅ |
| C_v1 | XYZScaling | 2.2P 1.4/8.0 | deep violet | ✅ | deep violet | ✅ |
| D75_v1 | Bradford | 0.1P 1.4/7.2 | deep violet | ✅ | deep violet | ✅ |
| D75_v1 | VonKries | 1.5P 1.4/8.0 | deep violet | ✅ | deep violet | ✅ |
| D75_v1 | CAT02 | 0.1P 1.4/7.2 | deep violet | ✅ | deep violet | ✅ |

#### 209. #DCD0FF - Expected: very light violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 1.9P 8.6/6.6 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | VonKries | 2.0P 8.5/6.6 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | CAT02 | 1.9P 8.6/6.6 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | XYZScaling | 1.4P 8.5/6.5 | very light violet | ✅ | very light violet | ✅ |

#### 210. #8C82B6 - Expected: light violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.5PB 5.6/6.8 | light violet | ✅ | light violet | ✅ |
| C_v1 | VonKries | 9.4PB 5.6/6.8 | light violet | ✅ | light violet | ✅ |
| C_v1 | CAT02 | 9.5PB 5.6/6.8 | light violet | ✅ | light violet | ✅ |
| C_v1 | XYZScaling | 9.4PB 5.6/6.8 | light violet | ✅ | light violet | ✅ |
| D65_v1 | Bradford | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| D65_v1 | VonKries | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| D65_v1 | CAT02 | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| D65_v1 | XYZScaling | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| D75_v1 | Bradford | 8.7PB 5.6/7.2 | light violet | ✅ | light purplish blue | ❌ |
| D75_v1 | VonKries | 8.8PB 5.6/7.3 | light violet | ✅ | light purplish blue | ❌ |
| D75_v1 | CAT02 | 8.7PB 5.6/7.2 | light violet | ✅ | light purplish blue | ❌ |
| D75_v1 | XYZScaling | 8.3PB 5.6/7.2 | light violet | ✅ | light purplish blue | ❌ |
| E_v1 | Bradford | 2.8P 5.6/5.3 | light purple | ❌ | light violet | ✅ |
| E_v1 | VonKries | 2.4P 5.6/5.2 | light purple | ❌ | light violet | ✅ |
| E_v1 | CAT02 | 2.6P 5.6/5.3 | light purple | ❌ | light violet | ✅ |
| F7_v1 | Bradford | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| F7_v1 | VonKries | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| F7_v1 | CAT02 | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |
| F7_v1 | XYZScaling | 9.7PB 5.6/5.8 | light violet | ✅ | light violet | ✅ |

#### 211. #604E81 - Expected: moderate violet

No matches

#### 212. #2F2140 - Expected: dark violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.5P 1.6/4.1 | dark violet | ✅ | dark violet | ✅ |
| C_v1 | VonKries | 2.5P 1.5/4.4 | very dark purple | ❌ | dark violet | ✅ |
| C_v1 | CAT02 | 1.5P 1.6/4.0 | dark violet | ✅ | dark violet | ✅ |
| C_v1 | XYZScaling | 1.3P 1.5/4.1 | dark violet | ✅ | dark violet | ✅ |
| D65_v1 | Bradford | 1.9P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| D65_v1 | VonKries | 1.9P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| D65_v1 | CAT02 | 1.9P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| D65_v1 | XYZScaling | 1.9P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| F7_v1 | Bradford | 2.0P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| F7_v1 | VonKries | 2.0P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| F7_v1 | CAT02 | 2.0P 1.5/3.6 | dark violet | ✅ | dark violet | ✅ |
| F7_v1 | XYZScaling | 2.0P 1.5/3.6 | very dark purple | ❌ | dark violet | ✅ |

#### 213. #C4C3DD - Expected: very pale violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.0P 7.9/4.2 | very pale purple | ❌ | very pale violet | ✅ |
| C_v1 | CAT02 | 3.0P 7.9/4.1 | very pale purple | ❌ | very pale violet | ✅ |
| C_v1 | XYZScaling | 2.9P 7.9/4.2 | very pale purple | ❌ | very pale violet | ✅ |
| D75_v1 | Bradford | 8.5PB 7.9/4.4 | very pale violet | ✅ | very pale purplish blue | ❌ |
| D75_v1 | VonKries | 8.8PB 7.9/4.4 | very pale violet | ✅ | very pale purplish blue | ❌ |
| D75_v1 | CAT02 | 8.5PB 7.9/4.3 | very pale violet | ✅ | very pale purplish blue | ❌ |
| D75_v1 | XYZScaling | 8.0PB 7.9/4.3 | very pale violet | ✅ | very pale purplish blue | ❌ |

#### 214. #9690AB - Expected: pale violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.7P 6.0/4.0 | pale violet | ✅ | pale violet | ✅ |
| C_v1 | VonKries | 1.8P 6.0/4.0 | pale violet | ✅ | pale violet | ✅ |
| C_v1 | CAT02 | 1.7P 6.0/4.0 | pale violet | ✅ | pale violet | ✅ |
| C_v1 | XYZScaling | 1.6P 6.0/4.0 | pale violet | ✅ | pale violet | ✅ |
| D75_v1 | Bradford | 9.7PB 6.0/4.3 | pale violet | ✅ | pale violet | ✅ |
| D75_v1 | VonKries | 9.9PB 6.0/4.3 | pale violet | ✅ | pale violet | ✅ |
| D75_v1 | CAT02 | 9.7PB 6.0/4.3 | pale violet | ✅ | pale violet | ✅ |
| D75_v1 | XYZScaling | 9.3PB 6.0/4.3 | pale violet | ✅ | pale violet | ✅ |

#### 215. #554C69 - Expected: grayish violet

No matches

#### 216. #9A4EAE - Expected: vivid purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0P 4.5/13.7 | vivid purple | ✅ | vivid purple | ✅ |
| C_v1 | VonKries | 6.2P 4.5/14.0 | vivid purple | ✅ | vivid purple | ✅ |
| C_v1 | CAT02 | 6.0P 4.6/13.6 | vivid purple | ✅ | vivid purple | ✅ |
| C_v1 | XYZScaling | 6.1P 4.5/13.9 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | Bradford | 5.4P 4.5/13.9 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | VonKries | 5.6P 4.5/14.1 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | CAT02 | 5.4P 4.5/13.8 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | XYZScaling | 5.2P 4.5/13.7 | vivid purple | ✅ | vivid purple | ✅ |
| E_v1 | XYZScaling | 8.3P 4.5/13.1 | vivid purple | ✅ | vivid purple | ✅ |

#### 217. #D399E6 - Expected: brilliant purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.9P 7.0/10.9 | brilliant purple | ✅ | brilliant purple | ✅ |
| C_v1 | VonKries | 6.0P 7.0/11.1 | brilliant purple | ✅ | brilliant purple | ✅ |
| C_v1 | CAT02 | 5.9P 7.0/10.9 | brilliant purple | ✅ | brilliant purple | ✅ |
| C_v1 | XYZScaling | 5.9P 7.0/11.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | Bradford | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | VonKries | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | CAT02 | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | XYZScaling | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | Bradford | 5.0P 7.0/10.8 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | VonKries | 5.1P 7.0/11.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | CAT02 | 5.0P 7.0/10.8 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | XYZScaling | 4.1P 7.0/10.4 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | Bradford | 8.5P 7.0/9.8 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | VonKries | 8.3P 7.0/9.8 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | CAT02 | 8.4P 7.0/9.8 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | XYZScaling | 8.8P 7.0/10.4 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | Bradford | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | VonKries | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | CAT02 | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | XYZScaling | 6.2P 7.0/9.6 | brilliant purple | ✅ | brilliant purple | ✅ |

#### 218. #875692 - Expected: strong purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 6.5P 4.3/9.0 | strong purple | ✅ | strong purple | ✅ |
| D75_v1 | VonKries | 5.7P 4.3/9.0 | strong purple | ✅ | strong purple | ✅ |

#### 219. #602F6B - Expected: deep purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.6P 2.8/8.5 | deep purple | ✅ | deep purple | ✅ |
| C_v1 | VonKries | 6.8P 2.8/8.7 | deep purple | ✅ | deep purple | ✅ |
| C_v1 | CAT02 | 6.6P 2.8/8.5 | deep purple | ✅ | deep purple | ✅ |
| C_v1 | XYZScaling | 6.7P 2.8/8.6 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | Bradford | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | VonKries | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | CAT02 | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | XYZScaling | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | Bradford | 5.9P 2.8/8.7 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | VonKries | 6.1P 2.8/8.8 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | CAT02 | 5.9P 2.8/8.6 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | XYZScaling | 5.6P 2.8/8.6 | deep purple | ✅ | deep purple | ✅ |
| E_v1 | Bradford | 8.9P 2.8/7.7 | deep reddish purple | ❌ | deep purple | ✅ |
| E_v1 | VonKries | 8.7P 2.8/7.7 | deep reddish purple | ❌ | deep purple | ✅ |
| E_v1 | CAT02 | 8.8P 2.8/7.7 | deep reddish purple | ❌ | deep purple | ✅ |
| F7_v1 | Bradford | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| F7_v1 | VonKries | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| F7_v1 | CAT02 | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |
| F7_v1 | XYZScaling | 7.1P 2.8/7.8 | deep purple | ✅ | deep purple | ✅ |

#### 220. #401A4C - Expected: very deep purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.8P 1.7/7.7 | very deep purple | ✅ | very deep purple | ✅ |
| C_v1 | VonKries | 7.0P 1.7/7.8 | very deep purple | ✅ | very deep purple | ✅ |
| C_v1 | CAT02 | 6.8P 1.7/7.7 | very deep purple | ✅ | very deep purple | ✅ |
| C_v1 | XYZScaling | 6.9P 1.7/7.8 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | Bradford | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | VonKries | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | CAT02 | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | XYZScaling | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | Bradford | 6.1P 1.7/7.9 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | VonKries | 6.4P 1.7/8.0 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | CAT02 | 6.1P 1.7/7.8 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | XYZScaling | 5.8P 1.7/7.8 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | Bradford | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | VonKries | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | CAT02 | 7.2P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | XYZScaling | 7.3P 1.7/7.1 | very deep purple | ✅ | very deep purple | ✅ |

#### 221. #D5BADB - Expected: very light purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.5P 7.8/5.3 | very light purple | ✅ | very light purple | ✅ |
| C_v1 | VonKries | 6.6P 7.8/5.4 | very light purple | ✅ | very light purple | ✅ |
| C_v1 | CAT02 | 6.5P 7.8/5.3 | very light purple | ✅ | very light purple | ✅ |
| C_v1 | XYZScaling | 6.5P 7.8/5.3 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | Bradford | 4.4P 7.8/5.1 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | VonKries | 4.5P 7.8/5.1 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | CAT02 | 4.4P 7.8/5.0 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | XYZScaling | 4.3P 7.8/5.0 | very light purple | ✅ | very light purple | ✅ |

#### 222. #B695C0 - Expected: light purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0P 6.5/6.5 | light purple | ✅ | light purple | ✅ |
| C_v1 | VonKries | 6.1P 6.5/6.6 | light purple | ✅ | light purple | ✅ |
| C_v1 | CAT02 | 6.0P 6.5/6.5 | light purple | ✅ | light purple | ✅ |
| C_v1 | XYZScaling | 6.1P 6.5/6.6 | light purple | ✅ | light purple | ✅ |
| D65_v1 | Bradford | 6.4P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| D65_v1 | VonKries | 6.4P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| D65_v1 | CAT02 | 6.4P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| D65_v1 | XYZScaling | 6.4P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| D75_v1 | Bradford | 3.0P 6.5/6.0 | light purple | ✅ | light purple | ✅ |
| D75_v1 | VonKries | 3.7P 6.5/6.2 | light purple | ✅ | light purple | ✅ |
| D75_v1 | CAT02 | 3.1P 6.5/6.0 | light purple | ✅ | light purple | ✅ |
| D75_v1 | XYZScaling | 2.2P 6.5/5.8 | light purple | ✅ | light violet | ❌ |
| F7_v1 | Bradford | 6.5P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| F7_v1 | VonKries | 6.5P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| F7_v1 | CAT02 | 6.4P 6.5/5.2 | light purple | ✅ | light purple | ✅ |
| F7_v1 | XYZScaling | 6.5P 6.5/5.2 | light purple | ✅ | light purple | ✅ |

#### 223. #86608E - Expected: moderate purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.5P 4.5/6.8 | moderate purple | ✅ | moderate purple | ✅ |
| C_v1 | VonKries | 6.6P 4.5/6.9 | moderate purple | ✅ | moderate purple | ✅ |
| C_v1 | CAT02 | 6.5P 4.5/6.8 | moderate purple | ✅ | moderate purple | ✅ |
| C_v1 | XYZScaling | 6.5P 4.5/6.9 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | Bradford | 7.0P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | VonKries | 7.0P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | CAT02 | 7.0P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | XYZScaling | 7.0P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | Bradford | 5.3P 4.5/6.8 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | VonKries | 5.5P 4.5/6.9 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | CAT02 | 5.3P 4.5/6.7 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | XYZScaling | 5.1P 4.5/6.7 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | Bradford | 7.1P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | VonKries | 7.1P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | CAT02 | 7.1P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | XYZScaling | 7.1P 4.5/5.8 | moderate purple | ✅ | moderate purple | ✅ |

#### 224. #563C5C - Expected: dark purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.7P 2.9/4.4 | dark purple | ✅ | dark purple | ✅ |
| C_v1 | VonKries | 6.8P 2.9/4.5 | dark purple | ✅ | dark purple | ✅ |
| C_v1 | CAT02 | 6.7P 2.9/4.4 | dark purple | ✅ | dark purple | ✅ |
| C_v1 | XYZScaling | 6.7P 2.9/4.5 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | Bradford | 7.2P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | VonKries | 7.2P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | CAT02 | 7.2P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | XYZScaling | 7.2P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | Bradford | 5.3P 2.9/4.4 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | VonKries | 5.5P 2.9/4.5 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | CAT02 | 5.3P 2.9/4.4 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | XYZScaling | 5.0P 2.9/4.4 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | Bradford | 7.3P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | VonKries | 7.3P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | CAT02 | 7.3P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | XYZScaling | 7.3P 2.9/3.7 | dark purple | ✅ | dark purple | ✅ |

#### 225. #301934 - Expected: very dark purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.5P 1.3/3.9 | very dark purple | ✅ | very dark purple | ✅ |
| C_v1 | VonKries | 8.6P 1.3/4.0 | very dark purple | ✅ | very dark purple | ✅ |
| C_v1 | CAT02 | 8.4P 1.3/3.9 | very dark purple | ✅ | very dark purple | ✅ |
| C_v1 | XYZScaling | 8.5P 1.3/4.0 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v1 | Bradford | 7.3P 1.3/4.0 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v1 | VonKries | 7.6P 1.3/4.1 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v1 | CAT02 | 7.3P 1.3/4.0 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v1 | XYZScaling | 7.0P 1.3/4.0 | very dark purple | ✅ | very dark purple | ✅ |

#### 226. #D6CADD - Expected: very pale purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.6P 8.2/3.2 | very pale purple | ✅ | very pale purple | ✅ |
| C_v1 | VonKries | 5.7P 8.2/3.2 | very pale purple | ✅ | very pale purple | ✅ |
| C_v1 | CAT02 | 5.6P 8.2/3.2 | very pale purple | ✅ | very pale purple | ✅ |
| C_v1 | XYZScaling | 5.6P 8.2/3.2 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | Bradford | 5.9P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | VonKries | 5.9P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | CAT02 | 5.9P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | XYZScaling | 5.9P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| D75_v1 | Bradford | 2.0P 8.2/3.4 | very pale purple | ✅ | very pale violet | ❌ |
| D75_v1 | VonKries | 2.4P 8.2/3.4 | very pale purple | ✅ | very pale violet | ❌ |
| F7_v1 | Bradford | 6.1P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | VonKries | 6.1P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | CAT02 | 6.1P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | XYZScaling | 6.1P 8.2/1.6 | very pale purple | ✅ | very pale purple | ✅ |

#### 227. #AA98A9 - Expected: pale purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| C_v2 | VonKries | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| C_v2 | CAT02 | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| C_v2 | XYZScaling | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | Bradford | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | VonKries | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | CAT02 | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | XYZScaling | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v1 | Bradford | 0.7RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | Bradford | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v1 | VonKries | 0.7RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | VonKries | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v1 | CAT02 | 0.7RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | CAT02 | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v1 | XYZScaling | 0.7RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | XYZScaling | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v1 | Bradford | 2.6P 6.4/2.6 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | Bradford | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v1 | VonKries | 3.7P 6.4/2.7 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | VonKries | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v1 | CAT02 | 2.6P 6.4/2.6 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | CAT02 | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v1 | XYZScaling | 2.7P 6.4/2.6 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | XYZScaling | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | Bradford | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | VonKries | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | CAT02 | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | XYZScaling | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v1 | Bradford | 0.5RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | Bradford | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v1 | VonKries | 0.5RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | VonKries | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v1 | CAT02 | 0.5RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | CAT02 | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v1 | XYZScaling | 0.5RP 6.4/1.8 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | XYZScaling | 7.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |

#### 228. #796878 - Expected: grayish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.3P 4.5/2.5 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | Bradford | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| C_v1 | VonKries | 8.4P 4.5/2.6 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | VonKries | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| C_v1 | CAT02 | 8.3P 4.5/2.5 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | CAT02 | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| C_v1 | XYZScaling | 8.3P 4.5/2.6 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | Bradford | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | VonKries | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | CAT02 | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | XYZScaling | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | Bradford | 0.3RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | Bradford | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | VonKries | 0.3RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | VonKries | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | CAT02 | 0.3RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | CAT02 | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | XYZScaling | 0.3RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | XYZScaling | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | Bradford | 4.2P 4.5/2.2 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | Bradford | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | VonKries | 5.0P 4.5/2.3 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | VonKries | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | CAT02 | 4.3P 4.5/2.2 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | CAT02 | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | XYZScaling | 3.5P 4.5/2.1 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | XYZScaling | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v1 | Bradford | 4.0RP 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | Bradford | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v1 | VonKries | 3.9RP 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | VonKries | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v1 | CAT02 | 3.9RP 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | CAT02 | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v1 | XYZScaling | 3.9RP 4.5/2.9 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | XYZScaling | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | Bradford | 0.4RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | Bradford | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | VonKries | 0.4RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | VonKries | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | CAT02 | 0.4RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | CAT02 | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | XYZScaling | 0.4RP 4.5/1.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | XYZScaling | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |

#### 229. #50404D - Expected: dark grayish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.0RP 2.9/1.8 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | Bradford | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v1 | VonKries | 0.1RP 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | VonKries | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v1 | CAT02 | 0.0RP 2.9/1.8 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | CAT02 | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v1 | XYZScaling | 0.1RP 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | Bradford | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | VonKries | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | CAT02 | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v1 | XYZScaling | 9.5RP 2.9/1.5 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | XYZScaling | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | Bradford | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | VonKries | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | CAT02 | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | XYZScaling | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | Bradford | 6.9P 2.9/1.7 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | Bradford | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | VonKries | 7.1P 2.9/1.7 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | VonKries | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | CAT02 | 6.9P 2.9/1.7 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | CAT02 | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | XYZScaling | 6.7P 2.9/1.7 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | XYZScaling | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | Bradford | 4.8RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | Bradford | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | VonKries | 4.7RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | VonKries | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | CAT02 | 4.8RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | CAT02 | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | XYZScaling | 4.8RP 2.9/2.1 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | XYZScaling | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | Bradford | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | VonKries | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | CAT02 | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | XYZScaling | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |

#### 230. #291E29 - Expected: blackish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1RP 1.3/1.5 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | Bradford | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| C_v1 | VonKries | 0.2RP 1.3/1.5 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | VonKries | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| C_v1 | CAT02 | 0.0RP 1.3/1.5 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | CAT02 | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| C_v1 | XYZScaling | 0.1RP 1.3/1.5 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v2 | Bradford | 10.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v2 | VonKries | 10.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v2 | CAT02 | 10.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v2 | XYZScaling | 10.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | Bradford | 9.5RP 1.3/1.1 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | Bradford | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | VonKries | 9.4RP 1.3/1.0 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | VonKries | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | CAT02 | 9.3RP 1.3/1.1 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | CAT02 | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | XYZScaling | 9.6RP 1.3/1.1 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | XYZScaling | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | Bradford | 1.4RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | Bradford | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | VonKries | 1.4RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | VonKries | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | CAT02 | 1.4RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | CAT02 | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | XYZScaling | 1.4RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | XYZScaling | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D75_v1 | Bradford | 7.3P 1.3/1.5 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | Bradford | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D75_v1 | VonKries | 7.6P 1.3/1.5 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | VonKries | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D75_v1 | CAT02 | 7.4P 1.3/1.4 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | CAT02 | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D75_v1 | XYZScaling | 7.1P 1.3/1.4 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | XYZScaling | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | Bradford | 6.9RP 1.3/1.3 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | Bradford | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | VonKries | 6.8RP 1.3/1.3 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | VonKries | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | CAT02 | 6.8RP 1.3/1.3 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | CAT02 | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | XYZScaling | 7.1RP 1.3/1.4 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | XYZScaling | 7.5RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | Bradford | 1.5RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | Bradford | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | VonKries | 1.5RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | VonKries | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | CAT02 | 1.5RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | CAT02 | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | XYZScaling | 1.5RP 1.3/1.2 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | XYZScaling | 5.0RP 1.3/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |

#### 231. #E8E3E5 - Expected: purplish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.3RP 9.1/0.8 | purplish white | ✅ | purplish white | ✅ |
| C_v1 | VonKries | 2.9RP 9.1/0.8 | purplish white | ✅ | purplish white | ✅ |
| C_v1 | CAT02 | 1.3RP 9.1/0.8 | purplish white | ✅ | purplish white | ✅ |

#### 232. #BFB9BD - Expected: light purplish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 10.0P 7.5/1.0 | light purplish gray | ✅ | light purplish gray | ✅ |
| C_v1 | VonKries | 10.0P 7.5/1.0 | light purplish gray | ✅ | light purplish gray | ✅ |
| C_v1 | CAT02 | 9.9P 7.5/1.0 | light purplish gray | ✅ | light purplish gray | ✅ |
| C_v1 | XYZScaling | 0.0RP 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |

#### 233. #8B8589 - Expected: purplish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.6RP 5.5/0.8 | purplish gray | ✅ | purplish gray | ✅ |
| C_v1 | VonKries | 0.6RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| C_v1 | CAT02 | 0.5RP 5.5/0.8 | purplish gray | ✅ | purplish gray | ✅ |
| C_v1 | XYZScaling | 0.6RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |

#### 234. #5D555B - Expected: dark purplish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.2RP 3.6/0.9 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| C_v1 | VonKries | 0.3RP 3.6/1.0 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| C_v1 | CAT02 | 0.2RP 3.6/0.9 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| C_v1 | XYZScaling | 0.3RP 3.6/1.0 | dark purplish gray | ✅ | dark purplish gray | ✅ |

#### 235. #242124 - Expected: purplish black

No matches

#### 236. #870074 - Expected: vivid reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.5RP 3.0/13.5 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| C_v1 | VonKries | 0.6RP 3.0/13.7 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| C_v1 | CAT02 | 0.5RP 3.0/13.4 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| C_v1 | XYZScaling | 0.6RP 3.0/13.8 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | Bradford | 2.9RP 3.0/13.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | CAT02 | 2.8RP 3.0/13.2 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | XYZScaling | 2.9RP 3.0/13.7 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D55_v1 | CAT02 | 2.1RP 3.0/13.0 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.2RP 3.0/13.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | Bradford | 1.0RP 3.0/13.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | VonKries | 1.0RP 3.0/13.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | CAT02 | 1.0RP 3.0/13.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.0RP 3.0/13.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | Bradford | 0.1RP 3.0/13.6 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | VonKries | 0.2RP 3.0/13.7 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | CAT02 | 0.1RP 3.0/13.5 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | XYZScaling | 0.0RP 3.0/13.4 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | Bradford | 1.8RP 3.0/13.2 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | VonKries | 1.7RP 3.0/13.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | CAT02 | 1.7RP 3.0/13.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | XYZScaling | 1.9RP 3.0/14.2 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | Bradford | 1.0RP 3.0/13.0 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | VonKries | 1.0RP 3.0/13.0 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | CAT02 | 1.0RP 3.0/13.0 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.0RP 3.0/13.0 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |

#### 237. #9E4F88 - Expected: strong reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8RP 4.4/9.7 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| C_v1 | VonKries | 0.9RP 4.4/9.9 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| C_v1 | CAT02 | 0.8RP 4.4/9.7 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| C_v1 | XYZScaling | 0.9RP 4.4/10.0 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D55_v1 | Bradford | 2.5RP 4.4/9.1 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| D55_v1 | CAT02 | 2.4RP 4.4/9.1 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.5RP 4.4/9.4 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| D75_v1 | Bradford | 10.0P 4.4/9.5 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | VonKries | 0.1RP 4.4/9.6 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | CAT02 | 0.0RP 4.4/9.4 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | XYZScaling | 10.0P 4.4/9.3 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| E_v1 | Bradford | 2.2RP 4.5/9.8 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| E_v1 | VonKries | 2.1RP 4.4/9.8 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| E_v1 | CAT02 | 2.1RP 4.4/9.8 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| E_v1 | XYZScaling | 2.2RP 4.4/10.4 | moderate purplish red | ❌ | strong reddish purple | ✅ |

#### 238. #702963 - Expected: deep reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.5RP 2.9/8.7 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| C_v1 | VonKries | 0.5RP 2.9/8.9 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| C_v1 | CAT02 | 0.5RP 2.9/8.7 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| C_v1 | XYZScaling | 0.6RP 2.9/8.9 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | Bradford | 2.6RP 2.9/8.1 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | VonKries | 2.5RP 2.9/7.9 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | CAT02 | 2.6RP 2.9/8.1 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.7RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | Bradford | 1.0RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | VonKries | 1.0RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | CAT02 | 1.0RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.0RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | Bradford | 9.9P 2.9/8.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | VonKries | 10.0P 2.9/8.7 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | CAT02 | 9.9P 2.9/8.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.8P 2.9/8.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | Bradford | 2.2RP 2.9/8.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | VonKries | 2.1RP 2.9/8.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | CAT02 | 2.1RP 2.9/8.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | XYZScaling | 2.3RP 2.9/9.1 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | Bradford | 1.1RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | VonKries | 1.1RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | CAT02 | 1.1RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.1RP 2.9/8.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |

#### 239. #54194E - Expected: very deep reddish purple

No matches

#### 240. #B784A7 - Expected: light reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.4RP 6.0/6.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| C_v1 | VonKries | 0.4RP 6.0/6.7 | light reddish purple | ✅ | light reddish purple | ✅ |
| C_v1 | CAT02 | 0.4RP 6.0/6.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| C_v1 | XYZScaling | 0.5RP 6.0/6.8 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | Bradford | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | VonKries | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | CAT02 | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| E_v1 | Bradford | 2.5RP 6.0/7.1 | dark purplish pink | ❌ | light reddish purple | ✅ |
| E_v1 | VonKries | 2.4RP 6.0/7.1 | dark purplish pink | ❌ | light reddish purple | ✅ |
| E_v1 | CAT02 | 2.4RP 6.0/7.1 | dark purplish pink | ❌ | light reddish purple | ✅ |
| E_v1 | XYZScaling | 2.4RP 6.0/7.5 | dark purplish pink | ❌ | light reddish purple | ✅ |
| F7_v1 | Bradford | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | VonKries | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | CAT02 | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.2RP 6.0/5.6 | light reddish purple | ✅ | light reddish purple | ✅ |

#### 241. #915C83 - Expected: moderate reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.4RP 4.5/6.7 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| C_v1 | VonKries | 0.4RP 4.5/6.8 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| C_v1 | CAT02 | 0.4RP 4.5/6.7 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| C_v1 | XYZScaling | 0.5RP 4.5/6.9 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D55_v1 | Bradford | 2.8RP 4.5/6.1 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| D55_v1 | VonKries | 2.8RP 4.5/5.9 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| D55_v1 | CAT02 | 2.8RP 4.5/6.1 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.8RP 4.5/6.2 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| D65_v1 | Bradford | 1.3RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D65_v1 | VonKries | 1.3RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D65_v1 | CAT02 | 1.3RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.3RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | Bradford | 9.1P 4.5/6.5 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | VonKries | 9.3P 4.5/6.5 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | CAT02 | 9.2P 4.5/6.4 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.1P 4.5/6.4 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| E_v1 | Bradford | 2.4RP 4.5/6.7 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| E_v1 | VonKries | 2.3RP 4.5/6.7 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| E_v1 | CAT02 | 2.3RP 4.5/6.7 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| E_v1 | XYZScaling | 2.4RP 4.5/7.1 | moderate purplish red | ❌ | moderate reddish purple | ✅ |
| F7_v1 | Bradford | 1.4RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| F7_v1 | VonKries | 1.4RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| F7_v1 | CAT02 | 1.4RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.4RP 4.5/6.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |

#### 242. #5D3954 - Expected: dark reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8RP 2.9/4.3 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| C_v1 | VonKries | 0.9RP 2.9/4.4 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| C_v1 | CAT02 | 0.8RP 2.9/4.3 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| C_v1 | XYZScaling | 0.9RP 2.9/4.4 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | Bradford | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | VonKries | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | CAT02 | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | Bradford | 9.7P 2.9/4.1 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | VonKries | 9.8P 2.9/4.2 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | CAT02 | 9.7P 2.9/4.1 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.6P 2.9/4.1 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | Bradford | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | VonKries | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | CAT02 | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.7RP 2.9/3.8 | dark reddish purple | ✅ | dark reddish purple | ✅ |

#### 243. #341731 - Expected: very dark reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.5RP 1.3/3.9 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| C_v1 | VonKries | 1.6RP 1.3/4.0 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| C_v1 | CAT02 | 1.5RP 1.3/3.9 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| C_v1 | XYZScaling | 1.6RP 1.3/4.0 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | Bradford | 2.3RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | VonKries | 2.3RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | CAT02 | 2.3RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | XYZScaling | 2.3RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | Bradford | 0.3RP 1.3/3.9 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | VonKries | 0.5RP 1.3/4.0 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | CAT02 | 0.4RP 1.3/3.9 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | XYZScaling | 0.1RP 1.3/3.8 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | Bradford | 2.4RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | VonKries | 2.4RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | CAT02 | 2.4RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | XYZScaling | 2.4RP 1.3/3.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |

#### 244. #AA8A9E - Expected: pale reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.7RP 6.0/4.2 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| C_v1 | VonKries | 0.7RP 6.0/4.2 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| C_v1 | CAT02 | 0.7RP 6.0/4.2 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| C_v1 | XYZScaling | 0.7RP 6.0/4.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | Bradford | 1.7RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | VonKries | 1.7RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | CAT02 | 1.7RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.7RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D75_v1 | Bradford | 8.0P 6.0/3.7 | pale reddish purple | ✅ | N/A | ❌ |
| D75_v1 | VonKries | 8.2P 6.0/3.7 | pale reddish purple | ✅ | N/A | ❌ |
| D75_v1 | CAT02 | 8.1P 6.0/3.7 | pale reddish purple | ✅ | N/A | ❌ |
| F7_v1 | Bradford | 1.8RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | VonKries | 1.8RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | CAT02 | 1.8RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.8RP 6.0/3.3 | pale reddish purple | ✅ | pale reddish purple | ✅ |

#### 245. #836479 - Expected: grayish reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8RP 4.5/3.9 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| C_v1 | VonKries | 0.8RP 4.5/3.9 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| C_v1 | CAT02 | 0.8RP 4.5/3.8 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| C_v1 | XYZScaling | 0.9RP 4.5/3.9 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | Bradford | 1.9RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | VonKries | 1.9RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | CAT02 | 1.9RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.9RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | Bradford | 2.0RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | VonKries | 2.0RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | CAT02 | 2.0RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | XYZScaling | 2.0RP 4.5/3.1 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |

#### 246. #FFC8D6 - Expected: brilliant purplish pink

No matches

#### 247. #E68FAC - Expected: strong purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.1RP 6.8/10.1 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| C_v1 | VonKries | 3.1RP 6.8/10.1 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| C_v1 | CAT02 | 3.1RP 6.8/10.0 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| C_v1 | XYZScaling | 3.1RP 6.8/10.4 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | Bradford | 4.2RP 6.8/9.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | VonKries | 4.2RP 6.8/9.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | CAT02 | 4.2RP 6.8/9.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | XYZScaling | 4.2RP 6.8/9.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| E_v1 | VonKries | 5.5RP 6.8/11.4 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | Bradford | 4.3RP 6.8/9.6 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | VonKries | 4.3RP 6.8/9.6 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | CAT02 | 4.3RP 6.8/9.6 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | XYZScaling | 4.3RP 6.8/9.6 | strong purplish pink | ✅ | strong purplish pink | ✅ |

#### 248. #DE6FA1 - Expected: deep purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.3RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| C_v1 | VonKries | 2.2RP 6.0/13.1 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| C_v1 | CAT02 | 2.3RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| C_v1 | XYZScaling | 2.3RP 6.0/13.4 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D50_v1 | Bradford | 6.5RP 6.0/13.8 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D50_v1 | CAT02 | 6.2RP 6.0/14.0 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D50_v1 | XYZScaling | 6.0RP 6.0/14.2 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | Bradford | 4.6RP 6.0/13.7 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | VonKries | 4.5RP 6.0/13.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | CAT02 | 4.5RP 6.0/13.7 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | XYZScaling | 4.5RP 6.0/13.8 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | Bradford | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | VonKries | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | CAT02 | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | XYZScaling | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | Bradford | 1.8RP 6.0/11.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | VonKries | 1.9RP 6.0/12.0 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | CAT02 | 1.9RP 6.0/11.8 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | XYZScaling | 1.9RP 6.0/11.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| E_v1 | Bradford | 3.7RP 6.1/14.5 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| E_v1 | VonKries | 3.6RP 6.0/14.5 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| E_v1 | CAT02 | 3.7RP 6.0/14.4 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | Bradford | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | VonKries | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | CAT02 | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | XYZScaling | 3.0RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |

#### 249. #EFBBCC - Expected: light purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.5RP 8.0/5.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| C_v1 | VonKries | 2.4RP 8.0/5.9 | light purplish pink | ✅ | light purplish pink | ✅ |
| C_v1 | CAT02 | 2.5RP 8.0/5.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| C_v1 | XYZScaling | 2.4RP 8.0/6.0 | light purplish pink | ✅ | light purplish pink | ✅ |
| F7_v1 | CAT02 | 6.1RP 8.0/5.1 | light purplish pink | ✅ | light purplish pink | ✅ |

#### 250. #D597AE - Expected: moderate purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.3RP 6.8/7.0 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| C_v1 | VonKries | 2.3RP 6.8/7.1 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| C_v1 | CAT02 | 2.3RP 6.8/7.0 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| C_v1 | XYZScaling | 2.3RP 6.8/7.2 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | Bradford | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | VonKries | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | CAT02 | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | XYZScaling | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | Bradford | 1.5RP 6.8/5.9 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | VonKries | 1.5RP 6.8/6.0 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | CAT02 | 1.5RP 6.8/5.9 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | XYZScaling | 1.5RP 6.8/6.0 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| E_v1 | Bradford | 6.3RP 6.8/8.3 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| E_v1 | VonKries | 7.5RP 6.8/7.7 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| E_v1 | CAT02 | 6.2RP 6.8/8.3 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| E_v1 | XYZScaling | 5.9RP 6.8/8.6 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | Bradford | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | VonKries | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | CAT02 | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | XYZScaling | 4.2RP 6.8/6.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |

#### 251. #C17E91 - Expected: dark purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.7RP 5.9/7.9 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| C_v1 | VonKries | 3.7RP 5.9/7.9 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| C_v1 | CAT02 | 3.7RP 5.9/7.9 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| C_v1 | XYZScaling | 3.7RP 5.9/8.2 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D65_v1 | Bradford | 6.8RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D65_v1 | VonKries | 6.8RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D65_v1 | CAT02 | 6.8RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D65_v1 | XYZScaling | 6.8RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D75_v1 | Bradford | 3.0RP 5.9/6.8 | dark purplish pink | ✅ | light reddish purple | ❌ |
| D75_v1 | VonKries | 3.0RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D75_v1 | CAT02 | 3.0RP 5.9/6.8 | dark purplish pink | ✅ | light reddish purple | ❌ |
| D75_v1 | XYZScaling | 3.0RP 5.9/6.9 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | Bradford | 7.0RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | VonKries | 7.0RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | CAT02 | 7.0RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | XYZScaling | 7.0RP 5.9/6.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |

#### 252. #E8CCD7 - Expected: pale purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v1 | XYZScaling | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |

#### 253. #C3A6B1 - Expected: grayish purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.8RP 7.0/3.5 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v1 | VonKries | 1.8RP 7.0/3.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v1 | CAT02 | 1.8RP 7.0/3.5 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v1 | XYZScaling | 1.9RP 7.0/3.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v1 | Bradford | 9.9P 7.0/2.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | Bradford | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v1 | VonKries | 0.0RP 7.0/2.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | VonKries | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v1 | CAT02 | 10.0P 7.0/2.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | CAT02 | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v1 | XYZScaling | 0.0RP 7.0/2.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | XYZScaling | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |

#### 254. #CE4676 - Expected: vivid purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.8RP 5.0/16.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| C_v1 | VonKries | 4.7RP 4.9/16.3 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| C_v1 | CAT02 | 4.8RP 5.0/16.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| C_v1 | XYZScaling | 4.7RP 4.9/16.8 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D50_v1 | XYZScaling | 9.9RP 4.9/14.4 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | Bradford | 8.8RP 5.0/14.5 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | VonKries | 8.6RP 5.0/14.5 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | CAT02 | 8.7RP 5.0/14.5 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | XYZScaling | 8.6RP 4.9/14.5 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | Bradford | 6.1RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | VonKries | 6.1RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | CAT02 | 6.1RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | XYZScaling | 6.1RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D75_v1 | Bradford | 4.3RP 4.9/15.3 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D75_v1 | VonKries | 4.4RP 4.9/15.3 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D75_v1 | CAT02 | 4.3RP 4.9/15.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D75_v1 | XYZScaling | 4.4RP 4.9/15.4 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | Bradford | 7.7RP 5.0/15.6 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | VonKries | 7.3RP 5.0/15.9 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | CAT02 | 7.6RP 5.0/15.7 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | XYZScaling | 7.2RP 4.9/16.5 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | Bradford | 6.2RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | VonKries | 6.2RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | CAT02 | 6.2RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | XYZScaling | 6.2RP 4.9/15.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |

#### 255. #B3446C - Expected: strong purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.8RP 4.5/12.9 | strong purplish red | ✅ | strong purplish red | ✅ |
| C_v1 | VonKries | 4.8RP 4.4/12.9 | strong purplish red | ✅ | strong purplish red | ✅ |
| C_v1 | CAT02 | 4.8RP 4.5/12.8 | strong purplish red | ✅ | strong purplish red | ✅ |
| D50_v1 | VonKries | 0.2R 4.5/11.6 | strong purplish red | ✅ | strong purplish red | ✅ |
| D50_v1 | CAT02 | 0.3R 4.5/11.6 | strong purplish red | ✅ | strong purplish red | ✅ |
| D50_v1 | XYZScaling | 0.1R 4.4/11.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| D55_v1 | Bradford | 8.9RP 4.5/11.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| D55_v1 | VonKries | 8.7RP 4.5/11.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| D55_v1 | CAT02 | 8.8RP 4.5/11.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| D55_v1 | XYZScaling | 8.7RP 4.4/11.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| D65_v1 | Bradford | 6.0RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| D65_v1 | VonKries | 6.0RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| D65_v1 | CAT02 | 6.0RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| D65_v1 | XYZScaling | 6.0RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| D75_v1 | Bradford | 4.3RP 4.4/12.2 | strong purplish red | ✅ | strong purplish red | ✅ |
| D75_v1 | VonKries | 4.3RP 4.4/12.2 | strong purplish red | ✅ | strong purplish red | ✅ |
| D75_v1 | CAT02 | 4.3RP 4.4/12.2 | strong purplish red | ✅ | strong purplish red | ✅ |
| D75_v1 | XYZScaling | 4.4RP 4.4/12.3 | strong purplish red | ✅ | strong purplish red | ✅ |
| E_v1 | Bradford | 7.7RP 4.5/12.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| E_v1 | VonKries | 7.3RP 4.5/12.9 | strong purplish red | ✅ | strong purplish red | ✅ |
| E_v1 | CAT02 | 7.5RP 4.5/12.7 | strong purplish red | ✅ | strong purplish red | ✅ |
| F7_v1 | Bradford | 6.1RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| F7_v1 | VonKries | 6.1RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| F7_v1 | CAT02 | 6.1RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |
| F7_v1 | XYZScaling | 6.1RP 4.4/12.1 | strong purplish red | ✅ | strong purplish red | ✅ |

#### 256. #78184A - Expected: deep purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.0RP 2.7/10.5 | deep purplish red | ✅ | deep purplish red | ✅ |
| C_v1 | VonKries | 5.0RP 2.7/10.6 | deep purplish red | ✅ | deep purplish red | ✅ |
| C_v1 | CAT02 | 5.0RP 2.7/10.5 | deep purplish red | ✅ | deep purplish red | ✅ |
| C_v1 | XYZScaling | 5.0RP 2.7/10.9 | deep purplish red | ✅ | deep purplish red | ✅ |
| D50_v1 | Bradford | 9.3RP 2.7/10.0 | deep purplish red | ✅ | deep purplish red | ✅ |
| D50_v1 | VonKries | 9.1RP 2.7/10.0 | deep purplish red | ✅ | deep purplish red | ✅ |
| D50_v1 | CAT02 | 9.2RP 2.7/10.1 | deep purplish red | ✅ | deep purplish red | ✅ |
| D50_v1 | XYZScaling | 9.1RP 2.7/10.2 | deep purplish red | ✅ | deep purplish red | ✅ |
| D55_v1 | Bradford | 7.9RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| D55_v1 | VonKries | 7.7RP 2.7/10.2 | deep purplish red | ✅ | deep purplish red | ✅ |
| D55_v1 | CAT02 | 7.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| D55_v1 | XYZScaling | 7.7RP 2.7/10.4 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | Bradford | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | VonKries | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | CAT02 | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | XYZScaling | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | Bradford | 4.6RP 2.7/10.0 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | VonKries | 4.6RP 2.7/10.1 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | CAT02 | 4.6RP 2.7/10.0 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | XYZScaling | 4.6RP 2.7/10.0 | deep purplish red | ✅ | deep purplish red | ✅ |
| E_v1 | Bradford | 7.0RP 2.7/10.8 | deep purplish red | ✅ | deep purplish red | ✅ |
| E_v1 | VonKries | 6.8RP 2.7/10.9 | deep purplish red | ✅ | deep purplish red | ✅ |
| E_v1 | CAT02 | 6.9RP 2.7/10.8 | deep purplish red | ✅ | deep purplish red | ✅ |
| E_v1 | XYZScaling | 6.9RP 2.7/11.4 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | Bradford | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | VonKries | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | CAT02 | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | XYZScaling | 5.8RP 2.7/10.3 | deep purplish red | ✅ | deep purplish red | ✅ |

#### 257. #54133B - Expected: very deep purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.3RP 1.9/7.6 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| C_v1 | VonKries | 5.3RP 1.8/7.7 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| C_v1 | CAT02 | 5.3RP 1.9/7.5 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| C_v1 | XYZScaling | 5.4RP 1.8/7.8 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D50_v1 | Bradford | 0.3R 1.9/7.3 | very deep red | ❌ | very deep purplish red | ✅ |
| D50_v1 | VonKries | 0.1R 1.8/7.2 | very deep red | ❌ | very deep purplish red | ✅ |
| D50_v1 | CAT02 | 0.1R 1.8/7.4 | very deep red | ❌ | very deep purplish red | ✅ |
| D50_v1 | XYZScaling | 0.1R 1.8/7.5 | very deep red | ❌ | very deep purplish red | ✅ |
| D55_v1 | Bradford | 8.7RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | VonKries | 8.5RP 1.8/7.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | CAT02 | 8.6RP 1.8/7.4 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | XYZScaling | 8.6RP 1.8/7.4 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | Bradford | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | VonKries | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | CAT02 | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | XYZScaling | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | Bradford | 4.6RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | VonKries | 4.7RP 1.8/7.4 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | CAT02 | 4.6RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | XYZScaling | 4.6RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | Bradford | 7.9RP 1.9/7.7 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | VonKries | 7.8RP 1.8/7.7 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | CAT02 | 7.8RP 1.9/7.6 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | XYZScaling | 7.9RP 1.8/8.0 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | Bradford | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | VonKries | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | CAT02 | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | XYZScaling | 6.3RP 1.8/7.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |

#### 258. #A8516E - Expected: moderate purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.6RP 4.5/10.1 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| C_v1 | VonKries | 4.5RP 4.5/10.2 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| C_v1 | CAT02 | 4.6RP 4.5/10.0 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| C_v1 | XYZScaling | 4.5RP 4.5/10.5 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | VonKries | 9.4RP 4.5/9.0 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | CAT02 | 9.5RP 4.5/9.0 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | XYZScaling | 9.4RP 4.5/9.0 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | Bradford | 6.0RP 4.5/9.4 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | VonKries | 6.0RP 4.5/9.4 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | CAT02 | 6.0RP 4.5/9.4 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | XYZScaling | 6.0RP 4.5/9.4 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D75_v1 | Bradford | 3.9RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D75_v1 | VonKries | 4.0RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D75_v1 | CAT02 | 3.9RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D75_v1 | XYZScaling | 4.0RP 4.5/9.4 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| E_v1 | Bradford | 8.0RP 4.6/10.1 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| E_v1 | VonKries | 7.6RP 4.5/10.2 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| E_v1 | CAT02 | 7.9RP 4.5/10.0 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| E_v1 | XYZScaling | 7.5RP 4.5/10.6 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | Bradford | 6.1RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | VonKries | 6.1RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | CAT02 | 6.1RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | XYZScaling | 6.1RP 4.5/9.3 | moderate purplish red | ✅ | moderate purplish red | ✅ |

#### 259. #673147 - Expected: dark purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.0RP 2.8/5.9 | dark purplish red | ✅ | dark purplish red | ✅ |
| C_v1 | VonKries | 5.0RP 2.8/6.0 | dark purplish red | ✅ | dark purplish red | ✅ |
| C_v1 | CAT02 | 5.0RP 2.8/5.9 | dark purplish red | ✅ | dark purplish red | ✅ |
| C_v1 | XYZScaling | 5.0RP 2.8/6.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | Bradford | 9.9RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | VonKries | 9.8RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | CAT02 | 9.8RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | XYZScaling | 9.7RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | Bradford | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | VonKries | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | CAT02 | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | XYZScaling | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | Bradford | 4.4RP 2.8/5.4 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | VonKries | 4.4RP 2.8/5.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | CAT02 | 4.4RP 2.8/5.4 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | XYZScaling | 4.4RP 2.8/5.4 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | Bradford | 8.2RP 2.8/6.3 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | VonKries | 7.9RP 2.8/6.3 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | CAT02 | 8.1RP 2.8/6.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | XYZScaling | 7.9RP 2.8/6.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | Bradford | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | VonKries | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | CAT02 | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | XYZScaling | 6.3RP 2.8/5.6 | dark purplish red | ✅ | dark purplish red | ✅ |

#### 260. #38152C - Expected: very dark purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.4RP 1.3/4.0 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | Bradford | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| C_v1 | VonKries | 5.5RP 1.3/4.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | VonKries | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| C_v1 | CAT02 | 5.5RP 1.3/4.0 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | CAT02 | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| C_v1 | XYZScaling | 5.6RP 1.3/4.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | XYZScaling | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D55_v1 | Bradford | 9.9RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v2 | Bradford | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D55_v1 | VonKries | 9.7RP 1.3/3.6 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v2 | VonKries | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D55_v1 | CAT02 | 9.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v2 | CAT02 | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D55_v1 | XYZScaling | 9.8RP 1.3/3.8 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v2 | XYZScaling | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | Bradford | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | Bradford | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | VonKries | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | VonKries | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | CAT02 | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | CAT02 | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | XYZScaling | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | XYZScaling | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | Bradford | 4.4RP 1.3/3.8 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | Bradford | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | VonKries | 4.5RP 1.3/3.9 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | VonKries | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | CAT02 | 4.4RP 1.3/3.8 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | CAT02 | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | XYZScaling | 4.4RP 1.3/3.8 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | XYZScaling | 7.5RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | Bradford | 8.9RP 1.3/4.0 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | Bradford | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | VonKries | 8.7RP 1.3/4.0 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | VonKries | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | CAT02 | 8.8RP 1.3/4.0 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | CAT02 | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | XYZScaling | 8.9RP 1.3/4.3 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | XYZScaling | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | Bradford | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | Bradford | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | VonKries | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | VonKries | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | CAT02 | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | CAT02 | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | XYZScaling | 6.7RP 1.3/3.7 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | XYZScaling | 10.0RP 1.3/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |

#### 261. #AF868E - Expected: light grayish purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.7RP 5.9/4.8 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| C_v1 | VonKries | 4.6RP 5.9/4.8 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| C_v1 | CAT02 | 4.7RP 5.9/4.8 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| C_v1 | XYZScaling | 4.6RP 5.9/4.9 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D75_v1 | Bradford | 3.2RP 5.9/3.8 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D75_v1 | VonKries | 3.2RP 5.9/3.8 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D75_v1 | CAT02 | 3.2RP 5.9/3.8 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D75_v1 | XYZScaling | 3.2RP 5.9/3.9 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |

#### 262. #915F6D - Expected: grayish purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.6RP 4.5/5.5 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| C_v1 | VonKries | 4.6RP 4.5/5.5 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| C_v1 | CAT02 | 4.6RP 4.5/5.5 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| C_v1 | XYZScaling | 4.6RP 4.5/5.7 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | Bradford | 7.7RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | VonKries | 7.7RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | CAT02 | 7.7RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | XYZScaling | 7.7RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D75_v1 | Bradford | 3.6RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D75_v1 | VonKries | 3.7RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D75_v1 | CAT02 | 3.6RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D75_v1 | XYZScaling | 3.7RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| E_v1 | VonKries | 9.9RP 4.5/5.7 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| E_v1 | XYZScaling | 9.6RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | Bradford | 7.8RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | VonKries | 7.8RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | CAT02 | 7.8RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | XYZScaling | 7.8RP 4.5/4.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |

#### 263. #F2F3F4 - Expected: white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.4PB 9.6/0.2 | white | ✅ | white | ✅ |
| C_v1 | VonKries | 6.9PB 9.6/0.2 | white | ✅ | white | ✅ |
| C_v1 | CAT02 | 5.8PB 9.6/0.2 | white | ✅ | white | ✅ |
| C_v1 | XYZScaling | 5.7PB 9.6/0.2 | white | ✅ | white | ✅ |

#### 264. #B9B8B5 - Expected: light gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 10.0Y 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| C_v1 | VonKries | 4.0GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| C_v1 | CAT02 | 9.2Y 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| C_v1 | XYZScaling | 0.7GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |

#### 265. #848482 - Expected: medium gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.1GY 5.4/0.2 | medium gray | ✅ | medium gray | ✅ |
| C_v1 | VonKries | 6.2GY 5.4/0.2 | medium gray | ✅ | medium gray | ✅ |
| C_v1 | CAT02 | 6.2GY 5.4/0.2 | medium gray | ✅ | medium gray | ✅ |
| C_v1 | XYZScaling | 6.1GY 5.4/0.2 | medium gray | ✅ | medium gray | ✅ |

#### 266. #555555 - Expected: dark gray

No matches

#### 267. #222222 - Expected: black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| D65_v1 | VonKries | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| D65_v1 | CAT02 | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| D65_v1 | XYZScaling | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| D75_v1 | Bradford | 5.9BG 1.3/0.4 | black | ✅ | black | ✅ |
| D75_v1 | VonKries | 5.9BG 1.3/0.4 | black | ✅ | black | ✅ |
| D75_v1 | CAT02 | 5.9BG 1.3/0.4 | black | ✅ | black | ✅ |
| D75_v1 | XYZScaling | 5.9BG 1.3/0.4 | black | ✅ | black | ✅ |
| E_v1 | Bradford | 3.4Y 1.3/0.4 | black | ✅ | black | ✅ |
| E_v1 | VonKries | 3.4Y 1.3/0.4 | black | ✅ | black | ✅ |
| E_v1 | CAT02 | 3.5Y 1.3/0.4 | black | ✅ | black | ✅ |
| E_v1 | XYZScaling | 3.4Y 1.3/0.4 | black | ✅ | black | ✅ |
| F7_v1 | Bradford | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| F7_v1 | VonKries | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| F7_v1 | CAT02 | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |
| F7_v1 | XYZScaling | 7.2GY 1.3/0.4 | black | ✅ | black | ✅ |

## Paul Centore ISCC-NBS Dataset (260 colors)

### Summary Statistics

| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy | Total Tested |
|------------|------------|-------------------|-------------------|--------------|
| A_v1 | Bradford | 4.6% (12/260) | 3.5% (9/260) | 260 |
| D65_v2 | XYZScaling | 5.4% (14/260) | 5.8% (15/260) | 260 |
| A_v1 | CAT02 | 4.6% (12/260) | 3.8% (10/260) | 260 |
| C_v2 | VonKries | 6.2% (16/260) | 6.9% (18/260) | 260 |
| C_v2 | CAT02 | 6.2% (16/260) | 6.9% (18/260) | 260 |
| C_v1 | VonKries | 48.1% (125/260) | 50.0% (130/260) | 260 |
| D50_v2 | XYZScaling | 6.5% (17/260) | 7.3% (19/260) | 260 |
| D55_v1 | CAT02 | 33.5% (87/260) | 38.5% (100/260) | 260 |
| D50_v2 | Bradford | 6.5% (17/260) | 7.3% (19/260) | 260 |
| A_v2 | XYZScaling | 3.5% (9/260) | 3.1% (8/260) | 260 |
| D65_v2 | VonKries | 5.4% (14/260) | 5.8% (15/260) | 260 |
| E_v1 | Bradford | 45.4% (118/260) | 50.8% (132/260) | 260 |
| D75_v1 | Bradford | 40.4% (105/260) | 38.5% (100/260) | 260 |
| D50_v2 | VonKries | 6.5% (17/260) | 7.3% (19/260) | 260 |
| E_v2 | Bradford | 6.2% (16/260) | 6.5% (17/260) | 260 |
| F7_v1 | Bradford | 57.3% (149/260) | 63.1% (164/260) | 260 |
| D75_v2 | CAT02 | 5.4% (14/260) | 5.8% (15/260) | 260 |
| F7_v1 | VonKries | 57.3% (149/260) | 63.1% (164/260) | 260 |
| D55_v1 | Bradford | 32.7% (85/260) | 38.1% (99/260) | 260 |
| D55_v1 | XYZScaling | 30.8% (80/260) | 35.8% (93/260) | 260 |
| F11_v2 | CAT02 | 4.2% (11/260) | 5.0% (13/260) | 260 |
| F2_v2 | XYZScaling | 4.6% (12/260) | 5.0% (13/260) | 260 |
| D75_v2 | Bradford | 5.8% (15/260) | 5.8% (15/260) | 260 |
| C_v1 | CAT02 | 49.6% (129/260) | 52.7% (137/260) | 260 |
| D55_v2 | Bradford | 5.4% (14/260) | 6.2% (16/260) | 260 |
| E_v2 | VonKries | 6.2% (16/260) | 6.2% (16/260) | 260 |
| F7_v2 | VonKries | 5.4% (14/260) | 5.8% (15/260) | 260 |
| D65_v1 | XYZScaling | 56.9% (148/260) | 61.9% (161/260) | 260 |
| E_v1 | VonKries | 46.2% (120/260) | 51.9% (135/260) | 260 |
| F2_v1 | CAT02 | 14.2% (37/260) | 13.8% (36/260) | 260 |
| D75_v2 | VonKries | 5.4% (14/260) | 5.8% (15/260) | 260 |
| D50_v1 | XYZScaling | 22.7% (59/260) | 23.8% (62/260) | 260 |
| F2_v1 | Bradford | 15.8% (41/260) | 15.4% (40/260) | 260 |
| D55_v2 | VonKries | 5.4% (14/260) | 6.2% (16/260) | 260 |
| C_v1 | Bradford | 49.2% (128/260) | 52.7% (137/260) | 260 |
| F2_v1 | VonKries | 15.8% (41/260) | 15.8% (41/260) | 260 |
| C_v1 | XYZScaling | 48.5% (126/260) | 51.5% (134/260) | 260 |
| F2_v2 | VonKries | 4.6% (12/260) | 5.0% (13/260) | 260 |
| E_v2 | XYZScaling | 5.8% (15/260) | 6.2% (16/260) | 260 |
| D75_v1 | VonKries | 38.5% (100/260) | 38.1% (99/260) | 260 |
| D65_v1 | CAT02 | 56.9% (148/260) | 61.9% (161/260) | 260 |
| D75_v2 | XYZScaling | 6.2% (16/260) | 5.8% (15/260) | 260 |
| D75_v1 | XYZScaling | 39.2% (102/260) | 38.1% (99/260) | 260 |
| F2_v2 | CAT02 | 4.6% (12/260) | 5.0% (13/260) | 260 |
| F11_v1 | VonKries | 13.8% (36/260) | 12.7% (33/260) | 260 |
| F7_v2 | Bradford | 5.4% (14/260) | 5.8% (15/260) | 260 |
| F7_v1 | CAT02 | 57.3% (149/260) | 63.1% (164/260) | 260 |
| F7_v1 | XYZScaling | 57.3% (149/260) | 63.1% (164/260) | 260 |
| D65_v1 | Bradford | 56.9% (148/260) | 61.9% (161/260) | 260 |
| D50_v1 | Bradford | 27.7% (72/260) | 29.6% (77/260) | 260 |
| C_v2 | XYZScaling | 6.2% (16/260) | 6.9% (18/260) | 260 |
| F2_v2 | Bradford | 4.6% (12/260) | 5.0% (13/260) | 260 |
| F11_v1 | Bradford | 13.5% (35/260) | 14.2% (37/260) | 260 |
| D50_v2 | CAT02 | 6.5% (17/260) | 7.3% (19/260) | 260 |
| E_v1 | XYZScaling | 40.4% (105/260) | 46.5% (121/260) | 260 |
| F2_v1 | XYZScaling | 13.1% (34/260) | 13.1% (34/260) | 260 |
| F11_v2 | Bradford | 4.2% (11/260) | 5.0% (13/260) | 260 |
| F11_v2 | VonKries | 4.2% (11/260) | 5.0% (13/260) | 260 |
| F7_v2 | XYZScaling | 5.4% (14/260) | 5.8% (15/260) | 260 |
| D55_v2 | CAT02 | 5.4% (14/260) | 6.2% (16/260) | 260 |
| D65_v2 | Bradford | 5.4% (14/260) | 5.8% (15/260) | 260 |
| D65_v1 | VonKries | 56.9% (148/260) | 61.9% (161/260) | 260 |
| D55_v2 | XYZScaling | 5.4% (14/260) | 6.2% (16/260) | 260 |
| D50_v1 | CAT02 | 26.5% (69/260) | 28.8% (75/260) | 260 |
| E_v2 | CAT02 | 6.2% (16/260) | 6.2% (16/260) | 260 |
| F7_v2 | CAT02 | 5.4% (14/260) | 5.8% (15/260) | 260 |
| A_v2 | CAT02 | 3.1% (8/260) | 2.7% (7/260) | 260 |
| F11_v2 | XYZScaling | 4.2% (11/260) | 5.0% (13/260) | 260 |
| A_v2 | VonKries | 2.7% (7/260) | 2.3% (6/260) | 260 |
| D75_v1 | CAT02 | 41.2% (107/260) | 39.6% (103/260) | 260 |
| A_v2 | Bradford | 3.1% (8/260) | 2.7% (7/260) | 260 |
| D55_v1 | VonKries | 36.5% (95/260) | 41.9% (109/260) | 260 |
| D50_v1 | VonKries | 29.6% (77/260) | 33.1% (86/260) | 260 |
| A_v1 | XYZScaling | 7.3% (19/260) | 6.5% (17/260) | 260 |
| D65_v2 | CAT02 | 5.4% (14/260) | 5.8% (15/260) | 260 |
| C_v2 | Bradford | 6.2% (16/260) | 6.9% (18/260) | 260 |
| F11_v1 | CAT02 | 13.5% (35/260) | 14.2% (37/260) | 260 |
| F11_v1 | XYZScaling | 12.3% (32/260) | 13.1% (34/260) | 260 |
| A_v1 | VonKries | 2.3% (6/260) | 1.9% (5/260) | 260 |
| E_v1 | CAT02 | 45.8% (119/260) | 51.5% (134/260) | 260 |

### Detailed Results (Showing Matches Only)

#### 1. #FD7992 - Expected: vivid pink

No matches

#### 2. #F48FA0 - Expected: strong pink

No matches

#### 3. #E66980 - Expected: deep pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.6R 5.9/9.1 | deep yellowish pink | ❌ | deep pink | ✅ |
| C_v1 | VonKries | 8.1RP 5.9/13.6 | deep pink | ✅ | deep purplish pink | ❌ |
| C_v1 | CAT02 | 5.6R 5.9/9.0 | deep yellowish pink | ❌ | deep pink | ✅ |
| C_v1 | XYZScaling | 5.6R 5.9/9.3 | deep yellowish pink | ❌ | deep pink | ✅ |
| D65_v1 | Bradford | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ |
| D65_v1 | VonKries | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ |
| D65_v1 | CAT02 | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ |
| D65_v1 | XYZScaling | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ |
| D75_v1 | VonKries | 8.4RP 5.9/12.2 | deep pink | ✅ | deep purplish pink | ❌ |
| D75_v1 | CAT02 | 8.4RP 5.9/12.2 | deep pink | ✅ | deep purplish pink | ❌ |
| E_v1 | VonKries | 5.9R 5.9/10.4 | deep yellowish pink | ❌ | deep pink | ✅ |
| E_v1 | CAT02 | 6.0R 6.0/10.4 | deep yellowish pink | ❌ | deep pink | ✅ |
| E_v1 | XYZScaling | 5.8R 5.9/10.6 | deep yellowish pink | ❌ | deep pink | ✅ |
| F7_v1 | Bradford | 5.7R 5.9/9.3 | deep yellowish pink | ❌ | deep pink | ✅ |
| F7_v1 | VonKries | 5.7R 5.9/9.3 | deep yellowish pink | ❌ | deep pink | ✅ |
| F7_v1 | CAT02 | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ |
| F7_v1 | XYZScaling | 5.7R 5.9/9.2 | deep yellowish pink | ❌ | deep pink | ✅ |

#### 4. #F8C3CE - Expected: light pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| C_v1 | VonKries | 4.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| C_v1 | CAT02 | 4.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| D65_v1 | Bradford | 5.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| D65_v1 | VonKries | 5.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| D65_v1 | CAT02 | 5.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| D65_v1 | XYZScaling | 5.9R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| E_v1 | VonKries | 3.7R 8.3/5.8 | light pink | ✅ | light pink | ✅ |
| E_v1 | XYZScaling | 3.5R 8.3/5.9 | light pink | ✅ | light pink | ✅ |
| F7_v1 | Bradford | 6.0R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| F7_v1 | VonKries | 6.0R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| F7_v1 | CAT02 | 6.0R 8.3/3.6 | light pink | ✅ | light pink | ✅ |
| F7_v1 | XYZScaling | 6.0R 8.3/3.6 | light pink | ✅ | light pink | ✅ |

#### 5. #E2A3AE - Expected: moderate pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.0R 7.2/4.5 | moderate pink | ✅ | moderate pink | ✅ |
| C_v1 | CAT02 | 5.0R 7.2/4.4 | moderate pink | ✅ | moderate pink | ✅ |
| C_v1 | XYZScaling | 5.0R 7.2/4.6 | moderate pink | ✅ | moderate pink | ✅ |
| D65_v1 | Bradford | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| D65_v1 | VonKries | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| D65_v1 | CAT02 | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| D65_v1 | XYZScaling | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| D75_v1 | VonKries | 5.0R 7.2/3.6 | moderate pink | ✅ | moderate pink | ✅ |
| F7_v1 | Bradford | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| F7_v1 | VonKries | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| F7_v1 | CAT02 | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |
| F7_v1 | XYZScaling | 5.8R 7.2/4.5 | moderate yellowish pink | ❌ | moderate pink | ✅ |

#### 6. #C5808A - Expected: dark pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 4.9R 6.0/5.3 | dark pink | ✅ | dark pink | ✅ |
| D65_v1 | Bradford | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| D65_v1 | VonKries | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| D65_v1 | CAT02 | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| D65_v1 | XYZScaling | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| F7_v1 | Bradford | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| F7_v1 | VonKries | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| F7_v1 | CAT02 | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |
| F7_v1 | XYZScaling | 6.0R 6.0/5.1 | dark yellowish pink | ❌ | dark pink | ✅ |

#### 7. #EFD1DC - Expected: pale pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 10.0RP 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| C_v1 | VonKries | 4.1R 8.6/2.3 | pale pink | ✅ | pale pink | ✅ |
| C_v2 | VonKries | 10.0RP 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| C_v2 | CAT02 | 10.0RP 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| C_v1 | XYZScaling | 4.1R 8.6/2.3 | pale pink | ✅ | pale pink | ✅ |
| C_v2 | XYZScaling | 10.0RP 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| D50_v2 | Bradford | 5.0R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| D50_v2 | VonKries | 5.0R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| D50_v2 | CAT02 | 5.0R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| D50_v2 | XYZScaling | 5.0R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| E_v2 | Bradford | 2.5R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| E_v2 | VonKries | 2.5R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| E_v2 | CAT02 | 2.5R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| E_v2 | XYZScaling | 2.5R 8.6/2.0 | pale pink | ✅ | pale pink | ✅ |
| F7_v1 | Bradford | 3.2R 8.6/2.4 | pale pink | ✅ | pale pink | ✅ |
| F7_v1 | VonKries | 3.2R 8.6/2.4 | pale pink | ✅ | pale pink | ✅ |
| F7_v1 | CAT02 | 3.2R 8.6/2.4 | pale pink | ✅ | pale pink | ✅ |
| F7_v1 | XYZScaling | 3.2R 8.6/2.4 | pale pink | ✅ | pale pink | ✅ |

#### 8. #CBADB7 - Expected: grayish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| C_v2 | VonKries | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| C_v2 | CAT02 | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| C_v2 | XYZScaling | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D50_v2 | Bradford | 5.0R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D50_v2 | VonKries | 5.0R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D50_v2 | CAT02 | 5.0R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D50_v2 | XYZScaling | 5.0R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D55_v2 | Bradford | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D55_v2 | VonKries | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D55_v2 | CAT02 | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D55_v2 | XYZScaling | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v1 | Bradford | 5.8R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v2 | Bradford | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v1 | VonKries | 5.8R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v2 | VonKries | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v1 | CAT02 | 5.8R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v2 | CAT02 | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v1 | XYZScaling | 5.8R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| D65_v2 | XYZScaling | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | Bradford | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | VonKries | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | CAT02 | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| E_v2 | XYZScaling | 2.5R 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v1 | Bradford | 6.0R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v2 | Bradford | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v1 | VonKries | 6.0R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v2 | VonKries | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v1 | CAT02 | 6.0R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v2 | CAT02 | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v1 | XYZScaling | 6.0R 7.3/2.1 | grayish pink | ✅ | grayish pink | ✅ |
| F7_v2 | XYZScaling | 10.0RP 7.3/2.0 | grayish pink | ✅ | grayish pink | ✅ |

#### 9. #EFDDE5 - Expected: pinkish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 1.6YR 9.0/1.0 | pinkish white | ✅ | pinkish white | ✅ |
| D65_v1 | VonKries | 1.6YR 9.0/1.0 | pinkish white | ✅ | pinkish white | ✅ |
| D65_v1 | CAT02 | 1.6YR 9.0/1.0 | pinkish white | ✅ | pinkish white | ✅ |
| D65_v1 | XYZScaling | 1.6YR 9.0/1.0 | pinkish white | ✅ | pinkish white | ✅ |
| F7_v1 | Bradford | 2.4YR 9.0/0.9 | pinkish white | ✅ | pinkish white | ✅ |
| F7_v1 | VonKries | 2.3YR 9.0/0.9 | pinkish white | ✅ | pinkish white | ✅ |
| F7_v1 | CAT02 | 2.4YR 9.0/0.9 | pinkish white | ✅ | pinkish white | ✅ |
| F7_v1 | XYZScaling | 2.4YR 9.0/0.9 | pinkish white | ✅ | pinkish white | ✅ |

#### 10. #C7B6BD - Expected: pinkish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 0.5YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| D65_v1 | VonKries | 0.5YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| D65_v1 | CAT02 | 0.5YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| D65_v1 | XYZScaling | 0.5YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| F7_v1 | Bradford | 1.0YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| F7_v1 | VonKries | 1.0YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| F7_v1 | CAT02 | 1.0YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |
| F7_v1 | XYZScaling | 1.0YR 7.5/1.0 | pinkish gray | ✅ | pinkish gray | ✅ |

#### 11. #D51C3C - Expected: vivid red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 7.0R 4.5/13.4 | vivid red | ✅ | vivid red | ✅ |
| D75_v1 | CAT02 | 7.1R 4.5/13.4 | vivid red | ✅ | vivid red | ✅ |

#### 12. #BF344B - Expected: strong red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 6.9R 4.4/11.6 | deep reddish orange | ❌ | strong red | ✅ |
| E_v1 | VonKries | 6.8R 4.4/11.6 | deep reddish orange | ❌ | strong red | ✅ |
| E_v1 | CAT02 | 6.9R 4.4/11.6 | deep reddish orange | ❌ | strong red | ✅ |
| E_v1 | XYZScaling | 6.7R 4.3/11.8 | deep reddish orange | ❌ | strong red | ✅ |

#### 13. #87122D - Expected: deep red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.0R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| C_v1 | VonKries | 4.0R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| C_v1 | CAT02 | 4.0R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| C_v1 | XYZScaling | 3.9R 2.9/10.6 | deep red | ✅ | deep red | ✅ |
| D50_v1 | Bradford | 8.0R 2.9/9.9 | deep red | ✅ | deep red | ✅ |
| D50_v1 | VonKries | 7.9R 2.9/9.9 | deep red | ✅ | deep red | ✅ |
| D50_v1 | CAT02 | 7.9R 2.9/9.9 | deep red | ✅ | deep red | ✅ |
| D50_v1 | XYZScaling | 7.9R 2.9/9.7 | deep red | ✅ | deep red | ✅ |
| D55_v1 | Bradford | 7.7R 2.9/9.5 | deep red | ✅ | deep red | ✅ |
| D55_v1 | VonKries | 7.6R 2.9/9.5 | deep red | ✅ | deep red | ✅ |
| D55_v1 | CAT02 | 7.7R 2.9/9.5 | deep red | ✅ | deep red | ✅ |
| D55_v1 | XYZScaling | 7.7R 2.9/9.4 | deep red | ✅ | deep red | ✅ |
| D65_v1 | Bradford | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| D65_v1 | VonKries | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| D65_v1 | CAT02 | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| D65_v1 | XYZScaling | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| D75_v1 | Bradford | 3.9R 2.8/9.9 | deep red | ✅ | deep red | ✅ |
| D75_v1 | VonKries | 4.0R 2.8/9.9 | deep red | ✅ | deep red | ✅ |
| D75_v1 | CAT02 | 3.9R 2.8/9.9 | deep red | ✅ | deep red | ✅ |
| D75_v1 | XYZScaling | 3.9R 2.9/10.0 | deep red | ✅ | deep red | ✅ |
| E_v1 | Bradford | 7.4R 2.9/9.5 | deep red | ✅ | deep red | ✅ |
| E_v1 | CAT02 | 7.4R 2.9/9.5 | deep red | ✅ | deep red | ✅ |
| F2_v1 | Bradford | 8.3R 2.9/10.6 | deep red | ✅ | deep red | ✅ |
| F2_v1 | VonKries | 8.2R 2.9/10.6 | deep red | ✅ | deep red | ✅ |
| F2_v1 | CAT02 | 8.3R 2.9/10.6 | deep red | ✅ | deep red | ✅ |
| F2_v1 | XYZScaling | 8.2R 2.9/10.5 | deep red | ✅ | deep red | ✅ |
| F7_v1 | Bradford | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| F7_v1 | VonKries | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| F7_v1 | CAT02 | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| F7_v1 | XYZScaling | 4.3R 2.9/10.3 | deep red | ✅ | deep red | ✅ |
| F11_v1 | Bradford | 8.3R 3.0/10.8 | deep red | ✅ | deep red | ✅ |
| F11_v1 | VonKries | 8.2R 2.9/10.9 | deep red | ✅ | deep red | ✅ |
| F11_v1 | CAT02 | 8.3R 3.0/10.8 | deep red | ✅ | deep red | ✅ |
| F11_v1 | XYZScaling | 8.2R 2.9/10.8 | deep red | ✅ | deep red | ✅ |

#### 14. #5C0625 - Expected: very deep red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.6R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| C_v1 | VonKries | 4.6R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| C_v1 | CAT02 | 4.6R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| C_v1 | XYZScaling | 4.5R 1.8/8.2 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | Bradford | 6.9R 1.8/8.2 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | VonKries | 6.7R 1.8/8.3 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | CAT02 | 6.9R 1.8/8.3 | very deep red | ✅ | very deep red | ✅ |
| D50_v1 | XYZScaling | 6.8R 1.8/8.2 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | Bradford | 6.1R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | VonKries | 6.0R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | CAT02 | 6.1R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D55_v1 | XYZScaling | 6.0R 1.8/8.1 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | Bradford | 4.9R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | VonKries | 4.9R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | CAT02 | 4.9R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| D65_v1 | XYZScaling | 4.9R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | Bradford | 4.2R 1.8/7.7 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | VonKries | 4.3R 1.8/7.7 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | CAT02 | 4.2R 1.8/7.7 | very deep red | ✅ | very deep red | ✅ |
| D75_v1 | XYZScaling | 4.3R 1.8/7.7 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | Bradford | 5.5R 1.8/8.4 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | VonKries | 5.3R 1.8/8.4 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | CAT02 | 5.5R 1.8/8.3 | very deep red | ✅ | very deep red | ✅ |
| E_v1 | XYZScaling | 5.2R 1.8/8.7 | very deep red | ✅ | very deep red | ✅ |
| F2_v1 | Bradford | 8.2R 1.9/8.5 | deep reddish brown | ❌ | very deep red | ✅ |
| F2_v1 | VonKries | 7.8R 1.8/8.6 | very deep red | ✅ | very deep red | ✅ |
| F2_v1 | CAT02 | 8.0R 1.8/8.6 | deep reddish brown | ❌ | very deep red | ✅ |
| F2_v1 | XYZScaling | 7.8R 1.8/8.6 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | Bradford | 5.0R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | VonKries | 5.0R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | CAT02 | 5.0R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| F7_v1 | XYZScaling | 5.0R 1.8/7.9 | very deep red | ✅ | very deep red | ✅ |
| F11_v1 | Bradford | 8.4R 1.9/8.7 | deep reddish brown | ❌ | very deep red | ✅ |
| F11_v1 | VonKries | 8.0R 1.8/8.8 | deep reddish brown | ❌ | very deep red | ✅ |
| F11_v1 | CAT02 | 8.3R 1.9/8.7 | deep reddish brown | ❌ | very deep red | ✅ |
| F11_v1 | XYZScaling | 7.9R 1.8/8.9 | very deep red | ✅ | very deep red | ✅ |

#### 15. #B14955 - Expected: moderate red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.2R 4.5/8.0 | moderate red | ✅ | moderate red | ✅ |
| C_v1 | VonKries | 6.2R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| C_v1 | CAT02 | 6.2R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| C_v1 | XYZScaling | 6.1R 4.4/8.2 | moderate red | ✅ | moderate red | ✅ |
| D65_v1 | Bradford | 6.6R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| D65_v1 | VonKries | 6.6R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| D65_v1 | CAT02 | 6.6R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| D65_v1 | XYZScaling | 6.6R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| D75_v1 | Bradford | 6.1R 4.4/7.5 | moderate red | ✅ | moderate red | ✅ |
| D75_v1 | VonKries | 6.1R 4.4/7.5 | moderate red | ✅ | moderate red | ✅ |
| D75_v1 | CAT02 | 6.1R 4.4/7.4 | moderate red | ✅ | moderate red | ✅ |
| D75_v1 | XYZScaling | 6.1R 4.4/7.6 | moderate red | ✅ | moderate red | ✅ |
| E_v1 | Bradford | 6.9R 4.5/9.0 | moderate red | ✅ | moderate red | ✅ |
| E_v1 | VonKries | 6.8R 4.5/9.0 | moderate red | ✅ | moderate red | ✅ |
| E_v1 | CAT02 | 6.9R 4.5/9.0 | moderate red | ✅ | moderate red | ✅ |
| E_v1 | XYZScaling | 6.7R 4.4/9.2 | moderate red | ✅ | moderate red | ✅ |
| F7_v1 | Bradford | 6.7R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| F7_v1 | VonKries | 6.7R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| F7_v1 | CAT02 | 6.7R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |
| F7_v1 | XYZScaling | 6.7R 4.4/8.0 | moderate red | ✅ | moderate red | ✅ |

#### 16. #742434 - Expected: dark red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.0R 2.7/7.6 | dark red | ✅ | dark red | ✅ |
| C_v1 | VonKries | 2.9R 2.7/7.6 | dark red | ✅ | dark red | ✅ |
| C_v1 | CAT02 | 3.0R 2.7/7.6 | dark red | ✅ | dark red | ✅ |
| C_v1 | XYZScaling | 2.8R 2.7/7.9 | dark red | ✅ | dark red | ✅ |
| D50_v1 | Bradford | 5.8R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| D50_v1 | VonKries | 5.5R 2.7/8.1 | dark red | ✅ | dark red | ✅ |
| D50_v1 | CAT02 | 5.7R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| D50_v1 | XYZScaling | 5.6R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| D55_v1 | Bradford | 4.9R 2.7/7.8 | dark red | ✅ | dark red | ✅ |
| D55_v1 | VonKries | 4.8R 2.7/7.8 | dark red | ✅ | dark red | ✅ |
| D55_v1 | CAT02 | 4.9R 2.7/7.8 | dark red | ✅ | dark red | ✅ |
| D55_v1 | XYZScaling | 4.9R 2.7/7.7 | dark red | ✅ | dark red | ✅ |
| D65_v1 | Bradford | 4.1R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D65_v1 | VonKries | 4.1R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D65_v1 | CAT02 | 4.1R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D65_v1 | XYZScaling | 4.1R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D75_v1 | Bradford | 2.5R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D75_v1 | VonKries | 2.7R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D75_v1 | CAT02 | 2.6R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| D75_v1 | XYZScaling | 2.6R 2.7/7.4 | dark red | ✅ | dark red | ✅ |
| E_v1 | Bradford | 4.4R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| E_v1 | VonKries | 4.3R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| E_v1 | CAT02 | 4.4R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| E_v1 | XYZScaling | 4.2R 2.7/8.2 | dark red | ✅ | dark red | ✅ |
| F2_v1 | Bradford | 8.5R 2.8/8.1 | dark red | ✅ | dark red | ✅ |
| F2_v1 | VonKries | 8.3R 2.7/8.1 | dark red | ✅ | dark red | ✅ |
| F2_v1 | CAT02 | 8.4R 2.8/8.1 | dark red | ✅ | dark red | ✅ |
| F2_v1 | XYZScaling | 8.3R 2.7/8.0 | dark red | ✅ | dark red | ✅ |
| F7_v1 | Bradford | 4.2R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| F7_v1 | VonKries | 4.2R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| F7_v1 | CAT02 | 4.2R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| F7_v1 | XYZScaling | 4.2R 2.7/7.3 | dark red | ✅ | dark red | ✅ |
| F11_v1 | Bradford | 8.5R 2.8/8.3 | dark red | ✅ | dark red | ✅ |
| F11_v1 | VonKries | 8.3R 2.7/8.3 | dark red | ✅ | dark red | ✅ |
| F11_v1 | CAT02 | 8.5R 2.8/8.3 | dark red | ✅ | dark red | ✅ |
| F11_v1 | XYZScaling | 8.3R 2.7/8.3 | dark red | ✅ | dark red | ✅ |

#### 17. #481127 - Expected: very dark red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.2R 1.5/5.6 | very dark red | ✅ | very dark red | ✅ |
| C_v2 | Bradford | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| C_v1 | VonKries | 2.2R 1.5/5.7 | very dark red | ✅ | very dark red | ✅ |
| C_v2 | VonKries | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| C_v1 | CAT02 | 2.2R 1.5/5.6 | very dark red | ✅ | very dark red | ✅ |
| C_v2 | CAT02 | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| C_v1 | XYZScaling | 2.2R 1.5/5.8 | very dark red | ✅ | very dark red | ✅ |
| C_v2 | XYZScaling | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | Bradford | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | VonKries | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | CAT02 | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D50_v2 | XYZScaling | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | Bradford | 5.2R 1.5/5.4 | deep reddish brown | ❌ | very dark red | ✅ |
| D55_v2 | Bradford | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | VonKries | 5.1R 1.5/5.4 | deep reddish brown | ❌ | very dark red | ✅ |
| D55_v2 | VonKries | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | CAT02 | 5.1R 1.5/5.5 | deep reddish brown | ❌ | very dark red | ✅ |
| D55_v2 | CAT02 | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D55_v1 | XYZScaling | 5.1R 1.5/5.4 | deep reddish brown | ❌ | very dark red | ✅ |
| D55_v2 | XYZScaling | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | Bradford | 3.2R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | Bradford | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | VonKries | 3.2R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | VonKries | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | CAT02 | 3.2R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | CAT02 | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D65_v1 | XYZScaling | 3.2R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D65_v2 | XYZScaling | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D75_v1 | Bradford | 1.5R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D75_v2 | Bradford | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D75_v1 | VonKries | 1.6R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D75_v2 | VonKries | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D75_v1 | CAT02 | 1.5R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D75_v2 | CAT02 | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| D75_v1 | XYZScaling | 1.6R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| D75_v2 | XYZScaling | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | Bradford | 4.5R 1.5/5.7 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | Bradford | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | VonKries | 4.3R 1.5/5.7 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | VonKries | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | CAT02 | 4.4R 1.5/5.7 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | CAT02 | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| E_v1 | XYZScaling | 4.2R 1.5/6.0 | very dark red | ✅ | very dark red | ✅ |
| E_v2 | XYZScaling | 5.0R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | Bradford | 3.3R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | Bradford | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | VonKries | 3.3R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | VonKries | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | CAT02 | 3.3R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | CAT02 | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |
| F7_v1 | XYZScaling | 3.3R 1.5/5.4 | very dark red | ✅ | very dark red | ✅ |
| F7_v2 | XYZScaling | 2.5R 1.5/2.0 | very dark red | ✅ | very dark red | ✅ |

#### 18. #B4888D - Expected: light grayish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| C_v2 | VonKries | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| C_v2 | CAT02 | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| C_v1 | XYZScaling | 4.9R 6.0/3.5 | light grayish red | ✅ | light grayish red | ✅ |
| C_v2 | XYZScaling | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | Bradford | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | VonKries | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | CAT02 | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D50_v2 | XYZScaling | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | Bradford | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | VonKries | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | CAT02 | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D55_v2 | XYZScaling | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v1 | Bradford | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| D65_v2 | Bradford | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v1 | VonKries | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| D65_v2 | VonKries | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v1 | CAT02 | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| D65_v2 | CAT02 | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D65_v1 | XYZScaling | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| D65_v2 | XYZScaling | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | Bradford | 5.8R 6.0/2.5 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | VonKries | 4.8R 6.0/2.6 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | CAT02 | 4.8R 6.0/2.6 | light grayish red | ✅ | light grayish red | ✅ |
| D75_v1 | XYZScaling | 4.8R 6.0/2.7 | light grayish red | ✅ | light grayish red | ✅ |
| E_v1 | Bradford | 7.5R 6.0/4.5 | light reddish brown | ❌ | light grayish red | ✅ |
| E_v2 | Bradford | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v1 | VonKries | 7.4R 6.0/4.5 | light reddish brown | ❌ | light grayish red | ✅ |
| E_v2 | VonKries | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v1 | CAT02 | 7.5R 6.0/4.5 | light reddish brown | ❌ | light grayish red | ✅ |
| E_v2 | CAT02 | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| E_v1 | XYZScaling | 7.2R 6.0/4.6 | light reddish brown | ❌ | light grayish red | ✅ |
| E_v2 | XYZScaling | 5.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | Bradford | 7.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | VonKries | 7.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | CAT02 | 7.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F2_v2 | XYZScaling | 7.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v1 | Bradford | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| F7_v2 | Bradford | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v1 | VonKries | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| F7_v2 | VonKries | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v1 | CAT02 | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| F7_v2 | CAT02 | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F7_v1 | XYZScaling | 7.2R 6.0/3.2 | light reddish brown | ❌ | light grayish red | ✅ |
| F7_v2 | XYZScaling | 2.5R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | Bradford | 10.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | VonKries | 10.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | CAT02 | 10.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |
| F11_v2 | XYZScaling | 10.0R 6.0/2.0 | light grayish red | ✅ | light grayish red | ✅ |

#### 19. #985D62 - Expected: grayish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | Bradford | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| C_v1 | VonKries | 5.8R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | VonKries | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| C_v1 | CAT02 | 5.8R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | CAT02 | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| C_v1 | XYZScaling | 5.7R 4.5/4.6 | grayish red | ✅ | grayish red | ✅ |
| C_v2 | XYZScaling | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D50_v2 | Bradford | 7.5R 4.6/2.0 | grayish red | ✅ | grayish red | ✅ |
| D50_v2 | VonKries | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D50_v2 | CAT02 | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D50_v2 | XYZScaling | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D55_v2 | Bradford | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D55_v2 | VonKries | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D55_v2 | CAT02 | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D55_v2 | XYZScaling | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v1 | Bradford | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | Bradford | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v1 | VonKries | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | VonKries | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v1 | CAT02 | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | CAT02 | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D65_v1 | XYZScaling | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| D65_v2 | XYZScaling | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | Bradford | 5.6R 4.5/3.8 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | Bradford | 2.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | VonKries | 5.7R 4.5/3.9 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | VonKries | 2.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | CAT02 | 5.6R 4.5/3.8 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | CAT02 | 2.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| D75_v1 | XYZScaling | 5.7R 4.5/3.9 | grayish red | ✅ | grayish red | ✅ |
| D75_v2 | XYZScaling | 2.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| E_v1 | Bradford | 7.2R 4.6/5.5 | grayish reddish orange | ❌ | grayish red | ✅ |
| E_v2 | Bradford | 7.5R 4.6/2.0 | grayish red | ✅ | grayish red | ✅ |
| E_v1 | VonKries | 7.1R 4.5/5.4 | grayish reddish orange | ❌ | grayish red | ✅ |
| E_v2 | VonKries | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| E_v1 | CAT02 | 7.2R 4.5/5.4 | grayish reddish orange | ❌ | grayish red | ✅ |
| E_v2 | CAT02 | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| E_v1 | XYZScaling | 7.0R 4.5/5.5 | grayish red | ✅ | grayish red | ✅ |
| E_v2 | XYZScaling | 7.5R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F2_v2 | Bradford | 10.0R 4.6/2.0 | grayish red | ✅ | grayish red | ✅ |
| F2_v2 | VonKries | 10.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F2_v2 | CAT02 | 10.0R 4.6/2.0 | grayish red | ✅ | grayish red | ✅ |
| F2_v2 | XYZScaling | 10.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v1 | Bradford | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | Bradford | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v1 | VonKries | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | VonKries | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v1 | CAT02 | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | CAT02 | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F7_v1 | XYZScaling | 6.9R 4.5/4.4 | grayish red | ✅ | grayish red | ✅ |
| F7_v2 | XYZScaling | 5.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F11_v2 | Bradford | 10.0R 4.6/2.0 | grayish red | ✅ | grayish red | ✅ |
| F11_v2 | VonKries | 10.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |
| F11_v2 | CAT02 | 10.0R 4.6/2.0 | grayish red | ✅ | grayish red | ✅ |
| F11_v2 | XYZScaling | 10.0R 4.5/2.0 | grayish red | ✅ | grayish red | ✅ |

#### 20. #53383E - Expected: dark grayish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v2 | Bradford | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | VonKries | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | CAT02 | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D50_v2 | XYZScaling | 5.0R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | Bradford | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | VonKries | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | CAT02 | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D55_v2 | XYZScaling | 5.0R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v1 | Bradford | 3.4R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | Bradford | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v1 | VonKries | 3.4R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | VonKries | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v1 | CAT02 | 3.4R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | CAT02 | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v1 | XYZScaling | 3.4R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| D65_v2 | XYZScaling | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v1 | Bradford | 4.8R 2.7/2.8 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | Bradford | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v1 | VonKries | 4.6R 2.7/2.8 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | VonKries | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v1 | CAT02 | 4.7R 2.7/2.8 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | CAT02 | 5.0R 2.7/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v1 | XYZScaling | 4.5R 2.6/2.8 | dark grayish red | ✅ | dark grayish red | ✅ |
| E_v2 | XYZScaling | 5.0R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v1 | Bradford | 3.6R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | Bradford | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v1 | VonKries | 3.6R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | VonKries | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v1 | CAT02 | 3.6R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | CAT02 | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v1 | XYZScaling | 3.6R 2.6/2.1 | dark grayish red | ✅ | dark grayish red | ✅ |
| F7_v2 | XYZScaling | 2.5R 2.6/2.0 | dark grayish red | ✅ | dark grayish red | ✅ |

#### 21. #332127 - Expected: blackish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8R 1.5/1.6 | blackish red | ✅ | blackish purple | ❌ |
| C_v1 | VonKries | 0.7R 1.5/1.6 | blackish red | ✅ | blackish purple | ❌ |
| C_v1 | CAT02 | 0.8R 1.5/1.6 | blackish red | ✅ | blackish purple | ❌ |
| C_v1 | XYZScaling | 0.7R 1.5/1.6 | blackish red | ✅ | blackish purple | ❌ |
| D65_v1 | Bradford | 4.2R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| D65_v1 | VonKries | 4.2R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| D65_v1 | CAT02 | 4.2R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| D65_v1 | XYZScaling | 4.2R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| F7_v1 | Bradford | 4.3R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| F7_v1 | VonKries | 4.3R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| F7_v1 | CAT02 | 4.3R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |
| F7_v1 | XYZScaling | 4.3R 1.5/1.3 | blackish red | ✅ | blackish red | ✅ |

#### 22. #928186 - Expected: reddish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.4R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| D65_v1 | VonKries | 8.4R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| D65_v1 | CAT02 | 8.4R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| D65_v1 | XYZScaling | 8.4R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| F7_v1 | Bradford | 8.9R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| F7_v1 | VonKries | 8.9R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| F7_v1 | CAT02 | 8.9R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |
| F7_v1 | XYZScaling | 8.9R 5.5/1.1 | reddish gray | ✅ | reddish gray | ✅ |

#### 23. #5D4E53 - Expected: dark reddish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 3.6R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| D65_v1 | VonKries | 3.6R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| D65_v1 | CAT02 | 3.6R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| D65_v1 | XYZScaling | 3.6R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| F7_v1 | Bradford | 3.7R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| F7_v1 | VonKries | 3.7R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| F7_v1 | CAT02 | 3.7R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |
| F7_v1 | XYZScaling | 3.7R 3.4/0.9 | dark reddish gray | ✅ | dark reddish gray | ✅ |

#### 24. #30262B - Expected: reddish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 1.6R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| D65_v1 | VonKries | 1.6R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| D65_v1 | CAT02 | 1.6R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| D65_v1 | XYZScaling | 1.6R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| F7_v1 | Bradford | 1.8R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| F7_v1 | VonKries | 1.8R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| F7_v1 | CAT02 | 1.8R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |
| F7_v1 | XYZScaling | 1.8R 1.6/0.7 | reddish black | ✅ | reddish black | ✅ |

#### 25. #FD7E5D - Expected: vivid yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 0.4YR 6.9/18.6 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| A_v1 | VonKries | 9.4R 6.6/19.0 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| A_v1 | CAT02 | 0.5YR 6.9/18.6 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| A_v1 | XYZScaling | 9.9R 6.6/17.9 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| C_v1 | Bradford | 8.9R 6.6/11.7 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| C_v1 | VonKries | 8.9R 6.6/11.7 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| C_v1 | CAT02 | 8.9R 6.6/11.7 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| C_v1 | XYZScaling | 8.7R 6.6/12.0 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D50_v1 | Bradford | 0.6YR 6.7/13.0 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D50_v1 | VonKries | 0.2YR 6.6/13.1 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D50_v1 | CAT02 | 0.7YR 6.7/13.0 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D50_v1 | XYZScaling | 0.9YR 6.6/12.6 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D55_v1 | Bradford | 0.3YR 6.6/12.4 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D55_v1 | VonKries | 0.0YR 6.6/12.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D55_v1 | CAT02 | 0.4YR 6.6/12.4 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D55_v1 | XYZScaling | 0.5YR 6.6/12.1 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D65_v1 | Bradford | 9.7R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D65_v1 | VonKries | 9.7R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D65_v1 | CAT02 | 9.7R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D65_v1 | XYZScaling | 9.7R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| D75_v1 | XYZScaling | 8.9R 6.6/11.3 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| E_v1 | Bradford | 9.2R 6.7/12.9 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| E_v1 | VonKries | 8.9R 6.6/13.0 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| E_v1 | CAT02 | 9.2R 6.7/12.9 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| E_v1 | XYZScaling | 8.9R 6.6/13.1 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F2_v1 | Bradford | 0.7YR 6.7/14.3 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F2_v1 | VonKries | 0.0YR 6.6/14.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F2_v1 | CAT02 | 0.8YR 6.7/14.3 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F2_v1 | XYZScaling | 0.9YR 6.6/13.8 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F7_v1 | Bradford | 9.8R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F7_v1 | VonKries | 9.7R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F7_v1 | CAT02 | 9.8R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F7_v1 | XYZScaling | 9.8R 6.6/11.5 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F11_v1 | Bradford | 0.5YR 6.7/14.8 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F11_v1 | VonKries | 9.8R 6.6/15.0 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F11_v1 | CAT02 | 0.6YR 6.7/14.8 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |
| F11_v1 | XYZScaling | 0.5YR 6.6/14.3 | vivid yellowish pink | ✅ | vivid yellowish pink | ✅ |

#### 26. #F59080 - Expected: strong yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.1R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| C_v1 | VonKries | 8.1R 6.9/8.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| C_v1 | CAT02 | 8.1R 6.9/8.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| C_v1 | XYZScaling | 7.9R 6.9/8.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D50_v1 | Bradford | 0.7YR 7.0/10.3 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D50_v1 | VonKries | 0.2YR 6.9/10.3 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D50_v1 | CAT02 | 0.8YR 7.0/10.3 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D50_v1 | XYZScaling | 1.0YR 6.9/9.9 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D55_v1 | Bradford | 0.0YR 7.0/9.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D55_v1 | VonKries | 9.7R 6.9/9.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D55_v1 | CAT02 | 0.1YR 7.0/9.6 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D55_v1 | XYZScaling | 0.2YR 6.9/9.3 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | Bradford | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | VonKries | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | CAT02 | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D65_v1 | XYZScaling | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | Bradford | 8.2R 6.9/7.8 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | VonKries | 8.3R 6.9/7.8 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | CAT02 | 8.2R 6.9/7.8 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| D75_v1 | XYZScaling | 8.2R 6.9/8.0 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | Bradford | 8.7R 7.0/10.1 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | VonKries | 8.5R 6.9/10.1 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | CAT02 | 8.7R 7.0/10.1 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| E_v1 | XYZScaling | 8.5R 6.9/10.1 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | Bradford | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | VonKries | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | CAT02 | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |
| F7_v1 | XYZScaling | 8.8R 6.9/8.7 | strong yellowish pink | ✅ | strong yellowish pink | ✅ |

#### 27. #EF6366 - Expected: deep yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.0R 5.9/11.4 | strong reddish orange | ❌ | deep yellowish pink | ✅ |
| C_v1 | VonKries | 6.9R 5.9/11.4 | strong reddish orange | ❌ | deep yellowish pink | ✅ |
| C_v1 | CAT02 | 6.9R 5.9/11.4 | strong reddish orange | ❌ | deep yellowish pink | ✅ |
| C_v1 | XYZScaling | 6.8R 5.9/11.7 | strong reddish orange | ❌ | deep yellowish pink | ✅ |
| D75_v1 | Bradford | 6.9R 5.9/10.7 | moderate reddish orange | ❌ | deep yellowish pink | ✅ |
| D75_v1 | VonKries | 7.0R 5.9/10.7 | moderate reddish orange | ❌ | deep yellowish pink | ✅ |
| D75_v1 | CAT02 | 6.9R 5.9/10.7 | moderate reddish orange | ❌ | deep yellowish pink | ✅ |
| D75_v1 | XYZScaling | 6.9R 5.9/10.9 | moderate reddish orange | ❌ | deep yellowish pink | ✅ |

#### 28. #F8C4B6 - Expected: light yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.9R 8.3/4.3 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| C_v1 | VonKries | 8.9R 8.3/4.3 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| C_v1 | CAT02 | 8.9R 8.3/4.3 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| C_v1 | XYZScaling | 8.7R 8.3/4.4 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D55_v1 | VonKries | 6.9YR 8.3/4.9 | pale orange yellow | ❌ | light yellowish pink | ✅ |
| D65_v1 | Bradford | 4.4YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | VonKries | 4.4YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | CAT02 | 4.4YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D65_v1 | XYZScaling | 4.4YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D75_v1 | Bradford | 1.0YR 8.3/3.3 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D75_v1 | VonKries | 1.2YR 8.3/3.2 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D75_v1 | CAT02 | 0.9YR 8.3/3.3 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| D75_v1 | XYZScaling | 0.4YR 8.3/3.4 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | Bradford | 1.6YR 8.3/5.6 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | VonKries | 1.4YR 8.3/5.6 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | CAT02 | 1.6YR 8.3/5.5 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| E_v1 | XYZScaling | 1.3YR 8.3/5.6 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | Bradford | 4.5YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | VonKries | 4.5YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | CAT02 | 4.5YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |
| F7_v1 | XYZScaling | 4.5YR 8.3/3.8 | light yellowish pink | ✅ | light yellowish pink | ✅ |

#### 29. #E2A698 - Expected: moderate yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.7R 7.3/5.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| C_v1 | VonKries | 8.7R 7.3/5.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| C_v1 | CAT02 | 8.7R 7.3/5.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| C_v1 | XYZScaling | 8.5R 7.3/5.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | Bradford | 4.9YR 7.3/5.6 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | VonKries | 4.6YR 7.3/5.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | CAT02 | 5.0YR 7.3/5.6 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D55_v1 | XYZScaling | 5.5YR 7.3/5.5 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | Bradford | 2.5YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | VonKries | 2.5YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | CAT02 | 2.5YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D65_v1 | XYZScaling | 2.5YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D75_v1 | Bradford | 9.3R 7.2/4.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D75_v1 | VonKries | 9.6R 7.3/4.2 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D75_v1 | CAT02 | 9.3R 7.2/4.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| D75_v1 | XYZScaling | 8.9R 7.3/4.5 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | Bradford | 0.6YR 7.3/6.4 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | VonKries | 0.3YR 7.3/6.4 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | CAT02 | 0.6YR 7.3/6.3 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| E_v1 | XYZScaling | 0.2YR 7.3/6.4 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | Bradford | 2.6YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | VonKries | 2.5YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | CAT02 | 2.6YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |
| F7_v1 | XYZScaling | 2.6YR 7.3/4.7 | moderate yellowish pink | ✅ | moderate yellowish pink | ✅ |

#### 30. #C9807E - Expected: dark yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.8R 6.0/6.0 | dark yellowish pink | ✅ | dark yellowish pink | ✅ |
| C_v1 | VonKries | 6.8R 6.0/6.0 | dark yellowish pink | ✅ | dark yellowish pink | ✅ |
| C_v1 | CAT02 | 6.8R 6.0/6.0 | dark yellowish pink | ✅ | dark yellowish pink | ✅ |
| D65_v1 | Bradford | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| D65_v1 | VonKries | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| D65_v1 | CAT02 | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| D65_v1 | XYZScaling | 7.9R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| D75_v1 | Bradford | 6.8R 6.0/5.2 | dark yellowish pink | ✅ | dark yellowish pink | ✅ |
| D75_v1 | VonKries | 6.9R 6.0/5.2 | dark yellowish pink | ✅ | dark yellowish pink | ✅ |
| D75_v1 | CAT02 | 6.8R 6.0/5.2 | dark yellowish pink | ✅ | dark yellowish pink | ✅ |
| F7_v1 | Bradford | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| F7_v1 | VonKries | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| F7_v1 | CAT02 | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |
| F7_v1 | XYZScaling | 8.0R 6.0/6.0 | grayish reddish orange | ❌ | dark yellowish pink | ✅ |

#### 31. #F1D3D1 - Expected: pale yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| A_v2 | VonKries | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| A_v2 | CAT02 | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| A_v2 | XYZScaling | 5.0YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| D65_v1 | Bradford | 5.6YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| D65_v1 | VonKries | 5.6YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| D65_v1 | CAT02 | 5.6YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| D65_v1 | XYZScaling | 5.6YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| D75_v1 | XYZScaling | 6.9R 8.7/1.6 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F2_v2 | Bradford | 10.0R 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F2_v2 | VonKries | 10.0R 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F2_v2 | CAT02 | 10.0R 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F2_v2 | XYZScaling | 10.0R 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F7_v1 | Bradford | 5.7YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F7_v1 | VonKries | 5.7YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F7_v1 | CAT02 | 5.7YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F7_v1 | XYZScaling | 5.7YR 8.7/1.9 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | Bradford | 2.5YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | VonKries | 2.5YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | CAT02 | 2.5YR 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |
| F11_v2 | XYZScaling | 10.0R 8.7/2.0 | pale yellowish pink | ✅ | pale yellowish pink | ✅ |

#### 32. #CBACAC - Expected: grayish yellowish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0YR 7.3/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| A_v2 | VonKries | 5.0YR 7.2/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| A_v2 | CAT02 | 5.0YR 7.3/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| A_v2 | XYZScaling | 5.0YR 7.2/2.0 | brownish pink | ❌ | grayish yellowish pink | ✅ |
| D50_v2 | Bradford | 7.5R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D50_v2 | VonKries | 7.5R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D50_v2 | CAT02 | 7.5R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D50_v2 | XYZScaling | 7.5R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D65_v1 | Bradford | 1.9YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D65_v1 | VonKries | 1.9YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D65_v1 | CAT02 | 1.9YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| D65_v1 | XYZScaling | 1.9YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | Bradford | 10.0R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | VonKries | 10.0R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | CAT02 | 10.0R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F2_v2 | XYZScaling | 10.0R 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F7_v1 | Bradford | 2.1YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F7_v1 | VonKries | 2.1YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F7_v1 | CAT02 | 2.1YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F7_v1 | XYZScaling | 2.1YR 7.2/2.2 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | Bradford | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | VonKries | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | CAT02 | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |
| F11_v2 | XYZScaling | 2.5YR 7.2/2.0 | grayish yellowish pink | ✅ | grayish yellowish pink | ✅ |

#### 33. #CBAFA7 - Expected: brownish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0YR 7.3/2.0 | brownish pink | ✅ | grayish yellowish pink | ❌ |
| A_v2 | VonKries | 5.0YR 7.3/2.0 | brownish pink | ✅ | grayish yellowish pink | ❌ |
| A_v2 | CAT02 | 5.0YR 7.3/2.0 | brownish pink | ✅ | grayish yellowish pink | ❌ |
| A_v2 | XYZScaling | 5.0YR 7.3/2.0 | brownish pink | ✅ | grayish yellowish pink | ❌ |
| D75_v1 | Bradford | 4.3YR 7.3/1.3 | brownish pink | ✅ | pinkish gray | ❌ |
| D75_v1 | VonKries | 5.1YR 7.3/1.3 | brownish pink | ✅ | brownish pink | ✅ |
| D75_v1 | CAT02 | 4.3YR 7.3/1.3 | brownish pink | ✅ | pinkish gray | ❌ |

#### 34. #E83B1B - Expected: vivid reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 8.9R 5.5/20.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| A_v1 | VonKries | 8.5R 5.2/21.4 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| A_v1 | CAT02 | 8.9R 5.4/20.9 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| A_v1 | XYZScaling | 8.6R 5.1/21.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | Bradford | 8.7R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | VonKries | 8.7R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | CAT02 | 8.7R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| C_v1 | XYZScaling | 8.6R 5.1/16.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | Bradford | 8.9R 5.2/17.5 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | VonKries | 8.8R 5.1/17.6 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | CAT02 | 8.9R 5.2/17.5 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D50_v1 | XYZScaling | 8.9R 5.1/17.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | Bradford | 8.9R 5.2/17.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | VonKries | 8.8R 5.1/17.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | CAT02 | 8.9R 5.2/17.1 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D55_v1 | XYZScaling | 8.9R 5.1/16.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | Bradford | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | VonKries | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | CAT02 | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D65_v1 | XYZScaling | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | Bradford | 8.8R 5.1/15.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | VonKries | 8.8R 5.1/15.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | CAT02 | 8.8R 5.1/15.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| D75_v1 | XYZScaling | 8.7R 5.1/16.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | Bradford | 8.8R 5.2/17.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | VonKries | 8.7R 5.1/17.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | CAT02 | 8.8R 5.2/17.2 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| E_v1 | XYZScaling | 8.6R 5.1/17.5 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | Bradford | 8.9R 5.3/18.4 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | VonKries | 8.7R 5.1/18.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | CAT02 | 9.0R 5.3/18.4 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F2_v1 | XYZScaling | 8.9R 5.1/18.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | Bradford | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | VonKries | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | CAT02 | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F7_v1 | XYZScaling | 8.8R 5.1/16.3 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | Bradford | 8.9R 5.3/18.7 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | VonKries | 8.7R 5.2/19.0 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | CAT02 | 8.9R 5.3/18.8 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |
| F11_v1 | XYZScaling | 8.8R 5.1/18.5 | vivid reddish orange | ✅ | vivid reddish orange | ✅ |

#### 35. #DB5D3B - Expected: strong reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.2R 5.4/12.0 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| C_v1 | VonKries | 9.2R 5.4/11.9 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| C_v1 | CAT02 | 9.2R 5.4/12.0 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| C_v1 | XYZScaling | 8.9R 5.4/12.4 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D50_v1 | XYZScaling | 0.6YR 5.4/12.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | Bradford | 0.3YR 5.5/12.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | VonKries | 10.0R 5.4/12.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | CAT02 | 0.3YR 5.5/12.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D55_v1 | XYZScaling | 0.4YR 5.4/12.3 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | Bradford | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | VonKries | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | CAT02 | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D65_v1 | XYZScaling | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D75_v1 | Bradford | 9.5R 5.4/11.3 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D75_v1 | VonKries | 9.8R 5.4/11.2 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D75_v1 | CAT02 | 9.5R 5.4/11.3 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| D75_v1 | XYZScaling | 9.4R 5.4/11.6 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | Bradford | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | VonKries | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | CAT02 | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |
| F7_v1 | XYZScaling | 9.9R 5.4/11.8 | strong reddish orange | ✅ | strong reddish orange | ✅ |

#### 36. #AF3318 - Expected: deep reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.4R 4.0/12.3 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| C_v1 | VonKries | 9.4R 4.0/12.3 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| C_v1 | CAT02 | 9.3R 4.0/12.3 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| C_v1 | XYZScaling | 9.0R 4.0/12.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D50_v1 | XYZScaling | 0.2YR 4.0/12.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | Bradford | 10.0R 4.0/12.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | VonKries | 9.8R 4.0/12.8 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | CAT02 | 10.0R 4.0/12.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D55_v1 | XYZScaling | 0.1YR 4.0/12.4 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | Bradford | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | VonKries | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | CAT02 | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D65_v1 | XYZScaling | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D75_v1 | Bradford | 9.7R 3.9/11.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D75_v1 | VonKries | 9.8R 4.0/11.6 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D75_v1 | CAT02 | 9.6R 3.9/11.7 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| D75_v1 | XYZScaling | 9.5R 4.0/12.0 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | Bradford | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | VonKries | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | CAT02 | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |
| F7_v1 | XYZScaling | 9.8R 4.0/12.1 | deep reddish orange | ✅ | deep reddish orange | ✅ |

#### 37. #CD6952 - Expected: moderate reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.9R 5.5/9.3 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| C_v1 | VonKries | 8.9R 5.5/9.2 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| C_v1 | CAT02 | 8.8R 5.5/9.2 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| C_v1 | XYZScaling | 8.7R 5.5/9.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D50_v1 | Bradford | 1.2YR 5.5/10.3 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D50_v1 | VonKries | 0.6YR 5.5/10.4 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D50_v1 | CAT02 | 1.2YR 5.5/10.3 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D50_v1 | XYZScaling | 1.5YR 5.5/9.9 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D55_v1 | Bradford | 0.8YR 5.5/9.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D55_v1 | VonKries | 0.4YR 5.5/9.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D55_v1 | CAT02 | 0.8YR 5.5/9.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D55_v1 | XYZScaling | 1.0YR 5.5/9.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | Bradford | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | VonKries | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | CAT02 | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D65_v1 | XYZScaling | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | Bradford | 9.0R 5.4/8.6 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | VonKries | 9.3R 5.5/8.5 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | CAT02 | 9.0R 5.4/8.6 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| D75_v1 | XYZScaling | 8.9R 5.5/8.8 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | Bradford | 9.3R 5.5/10.3 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | VonKries | 9.0R 5.5/10.4 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | CAT02 | 9.3R 5.5/10.3 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| E_v1 | XYZScaling | 9.0R 5.5/10.4 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | Bradford | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | VonKries | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | CAT02 | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |
| F7_v1 | XYZScaling | 9.9R 5.5/9.0 | moderate reddish orange | ✅ | moderate reddish orange | ✅ |

#### 38. #A2402B - Expected: dark reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.4R 4.0/9.6 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| C_v1 | VonKries | 9.5R 4.0/9.5 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| C_v1 | CAT02 | 9.4R 4.0/9.5 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| C_v1 | XYZScaling | 9.0R 4.0/9.9 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D50_v1 | Bradford | 0.8YR 4.0/10.5 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D50_v1 | VonKries | 0.5YR 4.0/10.6 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D50_v1 | CAT02 | 0.9YR 4.0/10.5 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D50_v1 | XYZScaling | 1.0YR 4.0/10.2 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D55_v1 | Bradford | 0.7YR 4.0/10.0 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D55_v1 | VonKries | 0.5YR 4.0/10.1 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D55_v1 | CAT02 | 0.7YR 4.0/10.1 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D55_v1 | XYZScaling | 0.9YR 4.0/9.8 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | Bradford | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | VonKries | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | CAT02 | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D65_v1 | XYZScaling | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | Bradford | 9.8R 3.9/8.9 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | VonKries | 0.1YR 4.0/8.9 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | CAT02 | 9.8R 3.9/8.9 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| D75_v1 | XYZScaling | 9.6R 4.0/9.2 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | Bradford | 9.9R 4.0/10.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | VonKries | 9.5R 4.0/10.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | CAT02 | 9.8R 4.0/10.3 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| E_v1 | XYZScaling | 9.3R 4.0/10.6 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | Bradford | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | VonKries | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | CAT02 | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |
| F7_v1 | XYZScaling | 0.3YR 4.0/9.4 | dark reddish orange | ✅ | dark reddish orange | ✅ |

#### 39. #B97565 - Expected: grayish reddish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.9R 5.5/6.2 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| C_v1 | VonKries | 8.9R 5.5/6.1 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| C_v1 | CAT02 | 8.9R 5.5/6.1 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| C_v1 | XYZScaling | 8.7R 5.5/6.3 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D55_v1 | VonKries | 2.8YR 5.5/6.6 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D65_v1 | Bradford | 1.3YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D65_v1 | VonKries | 1.3YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D65_v1 | CAT02 | 1.3YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D65_v1 | XYZScaling | 1.3YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | Bradford | 9.5R 5.5/5.4 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | VonKries | 9.8R 5.5/5.3 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | CAT02 | 9.5R 5.5/5.4 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| D75_v1 | XYZScaling | 9.2R 5.5/5.6 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| F7_v1 | Bradford | 1.4YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| F7_v1 | VonKries | 1.3YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| F7_v1 | CAT02 | 1.4YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |
| F7_v1 | XYZScaling | 1.4YR 5.5/5.8 | grayish reddish orange | ✅ | grayish reddish orange | ✅ |

#### 40. #8B1C0E - Expected: strong reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 0.7YR 3.2/13.1 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| A_v1 | VonKries | 9.9R 3.0/13.6 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| A_v1 | CAT02 | 0.7YR 3.2/13.2 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| A_v1 | XYZScaling | 0.2YR 3.0/13.3 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | Bradford | 0.3YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | VonKries | 0.3YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | CAT02 | 0.3YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| C_v1 | XYZScaling | 9.6R 3.0/10.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D50_v1 | Bradford | 0.8YR 3.0/11.2 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D50_v1 | VonKries | 0.5YR 3.0/11.3 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D50_v1 | CAT02 | 0.8YR 3.0/11.2 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D50_v1 | XYZScaling | 0.8YR 3.0/11.0 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D55_v1 | Bradford | 0.8YR 3.0/10.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D55_v1 | VonKries | 0.5YR 3.0/11.0 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D55_v1 | CAT02 | 0.8YR 3.0/10.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D55_v1 | XYZScaling | 0.8YR 3.0/10.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D65_v1 | Bradford | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D65_v1 | VonKries | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D65_v1 | CAT02 | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D65_v1 | XYZScaling | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D75_v1 | Bradford | 0.3YR 3.0/10.2 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D75_v1 | VonKries | 0.4YR 3.0/10.1 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D75_v1 | CAT02 | 0.3YR 3.0/10.2 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| D75_v1 | XYZScaling | 0.4YR 3.0/10.3 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | Bradford | 0.4YR 3.1/11.1 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | VonKries | 0.2YR 3.0/11.1 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | CAT02 | 0.3YR 3.0/11.0 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| E_v1 | XYZScaling | 9.8R 3.0/11.3 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F2_v1 | Bradford | 0.8YR 3.1/11.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F2_v1 | VonKries | 0.3YR 3.0/11.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F2_v1 | CAT02 | 0.8YR 3.1/11.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F2_v1 | XYZScaling | 0.8YR 3.0/11.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F7_v1 | Bradford | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F7_v1 | VonKries | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F7_v1 | CAT02 | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F7_v1 | XYZScaling | 0.5YR 3.0/10.5 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F11_v1 | Bradford | 0.8YR 3.1/11.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F11_v1 | VonKries | 0.2YR 3.0/12.1 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F11_v1 | CAT02 | 0.8YR 3.1/11.9 | strong reddish brown | ✅ | strong reddish brown | ✅ |
| F11_v1 | XYZScaling | 0.5YR 3.0/11.7 | strong reddish brown | ✅ | strong reddish brown | ✅ |

#### 41. #610F12 - Expected: deep reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 1.9YR 2.1/9.8 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| A_v1 | VonKries | 9.8R 2.0/11.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| A_v1 | CAT02 | 1.8YR 2.1/9.9 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| A_v1 | XYZScaling | 9.8R 2.0/11.1 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | Bradford | 0.2YR 2.0/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | VonKries | 0.2YR 2.0/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | CAT02 | 0.2YR 2.0/8.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| C_v1 | XYZScaling | 10.0R 2.0/8.3 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | Bradford | 1.1YR 2.0/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | VonKries | 1.0YR 2.0/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | CAT02 | 1.1YR 2.0/8.5 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D50_v1 | XYZScaling | 1.2YR 2.0/8.3 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | Bradford | 1.0YR 2.0/8.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | VonKries | 9.7R 2.0/8.9 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | CAT02 | 1.0YR 2.0/8.2 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D55_v1 | XYZScaling | 9.7R 2.0/8.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | Bradford | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | VonKries | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | CAT02 | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D65_v1 | XYZScaling | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | Bradford | 0.3YR 1.9/7.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | VonKries | 0.4YR 1.9/7.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | CAT02 | 0.3YR 1.9/7.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| D75_v1 | XYZScaling | 0.2YR 2.0/7.8 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | Bradford | 0.6YR 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | VonKries | 0.6YR 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | CAT02 | 0.6YR 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| E_v1 | XYZScaling | 0.5YR 2.0/8.6 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | Bradford | 1.4YR 2.0/8.9 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | VonKries | 1.2YR 2.0/9.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | CAT02 | 1.4YR 2.0/8.9 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F2_v1 | XYZScaling | 1.4YR 2.0/8.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | Bradford | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | VonKries | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | CAT02 | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F7_v1 | XYZScaling | 9.5R 2.0/8.4 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | Bradford | 1.4YR 2.1/9.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | VonKries | 9.8R 2.0/9.9 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | CAT02 | 1.4YR 2.0/9.0 | deep reddish brown | ✅ | deep reddish brown | ✅ |
| F11_v1 | XYZScaling | 9.8R 2.0/9.7 | deep reddish brown | ✅ | deep reddish brown | ✅ |

#### 42. #AC7A73 - Expected: light reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.1R 5.5/4.2 | light reddish brown | ✅ | light reddish brown | ✅ |
| C_v1 | VonKries | 8.1R 5.5/4.2 | light reddish brown | ✅ | light reddish brown | ✅ |
| C_v1 | CAT02 | 8.1R 5.5/4.2 | light reddish brown | ✅ | light reddish brown | ✅ |
| C_v1 | XYZScaling | 7.9R 5.5/4.3 | light reddish brown | ✅ | grayish red | ❌ |
| D65_v1 | Bradford | 0.5YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| D65_v1 | VonKries | 0.5YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| D65_v1 | CAT02 | 0.5YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| D65_v1 | XYZScaling | 0.5YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| D75_v1 | Bradford | 8.4R 5.5/3.5 | light reddish brown | ✅ | light reddish brown | ✅ |
| D75_v1 | VonKries | 8.5R 5.5/3.5 | light reddish brown | ✅ | light reddish brown | ✅ |
| D75_v1 | CAT02 | 8.4R 5.5/3.5 | light reddish brown | ✅ | light reddish brown | ✅ |
| D75_v1 | XYZScaling | 8.3R 5.5/3.6 | light reddish brown | ✅ | light reddish brown | ✅ |
| F7_v1 | Bradford | 0.6YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| F7_v1 | VonKries | 0.6YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| F7_v1 | CAT02 | 0.6YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |
| F7_v1 | XYZScaling | 0.6YR 5.5/4.0 | light reddish brown | ✅ | light reddish brown | ✅ |

#### 43. #7D423B - Expected: moderate reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.6R 3.5/5.2 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| C_v1 | VonKries | 8.6R 3.5/5.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| C_v1 | CAT02 | 8.5R 3.5/5.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| C_v1 | XYZScaling | 8.3R 3.5/5.3 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D50_v1 | Bradford | 1.7YR 3.5/6.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D50_v1 | VonKries | 1.4YR 3.5/6.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D50_v1 | CAT02 | 1.7YR 3.5/6.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D50_v1 | XYZScaling | 1.9YR 3.5/5.8 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D55_v1 | Bradford | 1.2YR 3.5/5.6 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D55_v1 | VonKries | 1.1YR 3.5/5.6 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D55_v1 | CAT02 | 1.2YR 3.5/5.6 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D55_v1 | XYZScaling | 1.3YR 3.5/5.5 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | Bradford | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | VonKries | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | CAT02 | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D65_v1 | XYZScaling | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | Bradford | 8.7R 3.4/4.7 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | VonKries | 8.8R 3.5/4.7 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | CAT02 | 8.6R 3.4/4.7 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| D75_v1 | XYZScaling | 8.6R 3.5/4.8 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | Bradford | 9.5R 3.5/5.9 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | VonKries | 9.1R 3.5/6.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | CAT02 | 9.5R 3.5/5.9 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| E_v1 | XYZScaling | 8.9R 3.5/6.1 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F2_v1 | VonKries | 1.7YR 3.5/7.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | Bradford | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | VonKries | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | CAT02 | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |
| F7_v1 | XYZScaling | 0.1YR 3.5/5.0 | moderate reddish brown | ✅ | moderate reddish brown | ✅ |

#### 44. #461D1E - Expected: dark reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.2R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| C_v1 | VonKries | 9.2R 1.7/3.8 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| C_v1 | CAT02 | 9.2R 1.7/3.8 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| C_v1 | XYZScaling | 9.1R 1.7/4.0 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | Bradford | 0.5YR 1.7/4.7 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | VonKries | 0.4YR 1.7/4.7 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | CAT02 | 0.5YR 1.7/4.7 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D50_v1 | XYZScaling | 0.5YR 1.7/4.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | Bradford | 0.2YR 1.7/4.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | VonKries | 0.1YR 1.7/4.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | CAT02 | 0.2YR 1.7/4.4 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D55_v1 | XYZScaling | 0.2YR 1.7/4.3 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D65_v1 | Bradford | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D65_v1 | VonKries | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D65_v1 | CAT02 | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D65_v1 | XYZScaling | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D75_v1 | Bradford | 9.1R 1.6/3.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D75_v1 | VonKries | 9.2R 1.7/3.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D75_v1 | CAT02 | 9.1R 1.6/3.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| D75_v1 | XYZScaling | 9.1R 1.7/3.6 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | Bradford | 9.8R 1.7/4.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | VonKries | 9.7R 1.7/4.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | CAT02 | 9.7R 1.7/4.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| E_v1 | XYZScaling | 9.6R 1.7/4.5 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F7_v1 | Bradford | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F7_v1 | VonKries | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F7_v1 | CAT02 | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |
| F7_v1 | XYZScaling | 9.7R 1.7/3.9 | dark reddish brown | ✅ | dark reddish brown | ✅ |

#### 45. #9E7F7A - Expected: light grayish reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 5.6/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| A_v2 | VonKries | 2.5YR 5.5/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| A_v2 | CAT02 | 2.5YR 5.5/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| A_v2 | XYZScaling | 2.5YR 5.5/2.0 | light grayish reddish brown | ✅ | light grayish reddish brown | ✅ |
| D65_v1 | Bradford | 4.5YR 5.5/2.3 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| D65_v1 | VonKries | 4.5YR 5.5/2.3 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| D65_v1 | CAT02 | 4.5YR 5.5/2.3 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| D65_v1 | XYZScaling | 4.5YR 5.5/2.3 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| F7_v1 | Bradford | 4.6YR 5.5/2.3 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| F7_v1 | VonKries | 4.6YR 5.5/2.3 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| F7_v1 | CAT02 | 4.7YR 5.5/2.2 | light grayish brown | ❌ | light grayish reddish brown | ✅ |
| F7_v1 | XYZScaling | 4.6YR 5.5/2.2 | light grayish brown | ❌ | light grayish reddish brown | ✅ |

#### 46. #6C4D4B - Expected: grayish reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 3.6/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| A_v2 | VonKries | 2.5YR 3.6/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| A_v2 | CAT02 | 2.5YR 3.6/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| A_v2 | XYZScaling | 2.5YR 3.5/2.0 | grayish brown | ❌ | grayish reddish brown | ✅ |
| C_v1 | Bradford | 7.7R 3.5/2.4 | grayish reddish brown | ✅ | grayish red | ❌ |
| C_v1 | VonKries | 7.7R 3.5/2.4 | grayish reddish brown | ✅ | grayish red | ❌ |
| C_v1 | CAT02 | 7.7R 3.5/2.4 | grayish reddish brown | ✅ | grayish red | ❌ |
| C_v1 | XYZScaling | 7.5R 3.5/2.4 | grayish reddish brown | ✅ | grayish red | ❌ |
| D50_v2 | Bradford | 7.5R 3.6/2.0 | grayish reddish brown | ✅ | grayish red | ❌ |
| D50_v2 | VonKries | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish red | ❌ |
| D50_v2 | CAT02 | 7.5R 3.6/2.0 | grayish reddish brown | ✅ | grayish red | ❌ |
| D50_v2 | XYZScaling | 7.5R 3.5/2.0 | grayish reddish brown | ✅ | grayish red | ❌ |
| D65_v1 | Bradford | 1.0YR 3.5/2.3 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D65_v1 | VonKries | 1.0YR 3.5/2.3 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D65_v1 | CAT02 | 1.0YR 3.5/2.3 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D65_v1 | XYZScaling | 1.0YR 3.5/2.3 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| D75_v1 | Bradford | 7.7R 3.5/1.9 | grayish reddish brown | ✅ | grayish red | ❌ |
| D75_v1 | VonKries | 7.9R 3.5/1.9 | grayish reddish brown | ✅ | grayish red | ❌ |
| D75_v1 | CAT02 | 7.7R 3.5/1.9 | grayish reddish brown | ✅ | grayish red | ❌ |
| D75_v1 | XYZScaling | 7.7R 3.5/2.0 | grayish reddish brown | ✅ | grayish red | ❌ |
| F2_v2 | Bradford | 10.0R 3.6/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F2_v2 | VonKries | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F2_v2 | CAT02 | 10.0R 3.6/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F2_v2 | XYZScaling | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F7_v1 | Bradford | 1.0YR 3.5/2.3 | moderate reddish brown | ❌ | grayish reddish brown | ✅ |
| F7_v1 | VonKries | 1.0YR 3.5/2.3 | moderate reddish brown | ❌ | grayish reddish brown | ✅ |
| F7_v1 | CAT02 | 1.0YR 3.5/2.3 | moderate reddish brown | ❌ | grayish reddish brown | ✅ |
| F7_v1 | XYZScaling | 1.0YR 3.5/2.3 | moderate reddish brown | ❌ | grayish reddish brown | ✅ |
| F11_v2 | Bradford | 10.0R 3.6/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | VonKries | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | CAT02 | 10.0R 3.6/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |
| F11_v2 | XYZScaling | 10.0R 3.5/2.0 | grayish reddish brown | ✅ | grayish reddish brown | ✅ |

#### 47. #43292A - Expected: dark grayish reddish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 2.0/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| A_v2 | VonKries | 2.5YR 2.0/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| A_v2 | CAT02 | 2.5YR 2.0/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| A_v2 | XYZScaling | 2.5YR 2.0/2.0 | dark grayish brown | ❌ | dark grayish reddish brown | ✅ |
| C_v1 | Bradford | 6.9R 2.0/2.4 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| C_v1 | VonKries | 6.9R 2.0/2.4 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| C_v1 | CAT02 | 6.9R 2.0/2.4 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| C_v1 | XYZScaling | 6.5R 2.0/2.5 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | Bradford | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | VonKries | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | CAT02 | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D50_v2 | XYZScaling | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v1 | Bradford | 0.6YR 2.0/2.8 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v2 | Bradford | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v1 | VonKries | 0.5YR 2.0/2.8 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v2 | VonKries | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v1 | CAT02 | 0.6YR 2.0/2.8 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v2 | CAT02 | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v1 | XYZScaling | 0.6YR 2.0/2.8 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D55_v2 | XYZScaling | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D65_v1 | Bradford | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D65_v1 | VonKries | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D65_v1 | CAT02 | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D65_v1 | XYZScaling | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | Bradford | 6.4R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | VonKries | 6.6R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | CAT02 | 6.4R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| D75_v1 | XYZScaling | 6.4R 2.0/2.1 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v1 | Bradford | 9.4R 2.0/2.9 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v2 | Bradford | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v1 | VonKries | 9.4R 2.0/2.9 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v2 | VonKries | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v1 | CAT02 | 9.4R 2.0/2.9 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v2 | CAT02 | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v1 | XYZScaling | 9.3R 2.0/2.9 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| E_v2 | XYZScaling | 7.5R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | Bradford | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | VonKries | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | CAT02 | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F2_v2 | XYZScaling | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F7_v1 | Bradford | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F7_v1 | VonKries | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F7_v1 | CAT02 | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F7_v1 | XYZScaling | 9.3R 2.0/2.3 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | Bradford | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | VonKries | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | CAT02 | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |
| F11_v2 | XYZScaling | 10.0R 2.0/2.0 | dark grayish reddish brown | ✅ | dark grayish reddish brown | ✅ |

#### 48. #F7760B - Expected: vivid orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.5YR 6.3/14.5 | vivid orange | ✅ | vivid orange | ✅ |
| C_v1 | VonKries | 3.6YR 6.3/14.3 | vivid orange | ✅ | vivid orange | ✅ |
| C_v1 | CAT02 | 3.4YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| C_v1 | XYZScaling | 2.8YR 6.3/14.7 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | Bradford | 3.4YR 6.4/15.9 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | VonKries | 2.8YR 6.3/16.0 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | CAT02 | 3.5YR 6.4/16.0 | vivid orange | ✅ | vivid orange | ✅ |
| D50_v1 | XYZScaling | 4.0YR 6.3/15.5 | vivid orange | ✅ | vivid orange | ✅ |
| D55_v1 | Bradford | 3.7YR 6.3/15.3 | vivid orange | ✅ | vivid orange | ✅ |
| D55_v1 | VonKries | 3.3YR 6.3/15.4 | vivid orange | ✅ | vivid orange | ✅ |
| D55_v1 | CAT02 | 3.8YR 6.3/15.4 | vivid orange | ✅ | vivid orange | ✅ |
| D55_v1 | XYZScaling | 4.1YR 6.3/15.0 | vivid orange | ✅ | vivid orange | ✅ |
| D65_v1 | Bradford | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| D65_v1 | VonKries | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| D65_v1 | CAT02 | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| D65_v1 | XYZScaling | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | Bradford | 2.8YR 6.4/15.6 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | VonKries | 2.5YR 6.3/15.6 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | CAT02 | 2.8YR 6.4/15.6 | vivid orange | ✅ | vivid orange | ✅ |
| E_v1 | XYZScaling | 2.5YR 6.3/15.6 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | Bradford | 2.6YR 6.4/17.1 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | CAT02 | 2.8YR 6.4/17.3 | vivid orange | ✅ | vivid orange | ✅ |
| F2_v1 | XYZScaling | 3.2YR 6.3/16.5 | vivid orange | ✅ | vivid orange | ✅ |
| F7_v1 | Bradford | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| F7_v1 | VonKries | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| F7_v1 | CAT02 | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| F7_v1 | XYZScaling | 4.1YR 6.3/14.4 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | Bradford | 2.3YR 6.5/17.5 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | CAT02 | 2.4YR 6.5/17.7 | vivid orange | ✅ | vivid orange | ✅ |
| F11_v1 | XYZScaling | 2.7YR 6.3/16.9 | vivid orange | ✅ | vivid orange | ✅ |

#### 49. #EA8127 - Expected: strong orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| C_v1 | VonKries | 6.0YR 6.3/11.8 | strong orange | ✅ | strong orange | ✅ |
| C_v1 | CAT02 | 5.8YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| C_v1 | XYZScaling | 5.2YR 6.3/12.2 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | Bradford | 5.8YR 6.4/13.5 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | VonKries | 5.3YR 6.4/13.7 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | CAT02 | 5.9YR 6.4/13.7 | strong orange | ✅ | strong orange | ✅ |
| D50_v1 | XYZScaling | 6.6YR 6.3/13.1 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | Bradford | 6.2YR 6.4/12.9 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | VonKries | 5.8YR 6.3/13.0 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | CAT02 | 6.3YR 6.4/13.0 | strong orange | ✅ | strong orange | ✅ |
| D55_v1 | XYZScaling | 6.7YR 6.3/12.6 | strong orange | ✅ | strong orange | ✅ |
| D65_v1 | Bradford | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| D65_v1 | VonKries | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| D65_v1 | CAT02 | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| D65_v1 | XYZScaling | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| D75_v1 | Bradford | 6.9YR 6.3/11.2 | strong orange | ✅ | strong orange | ✅ |
| D75_v1 | CAT02 | 6.9YR 6.3/11.1 | strong orange | ✅ | strong orange | ✅ |
| D75_v1 | XYZScaling | 6.4YR 6.3/11.5 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | Bradford | 5.0YR 6.4/13.2 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | VonKries | 4.7YR 6.4/13.2 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | CAT02 | 5.0YR 6.4/13.2 | strong orange | ✅ | strong orange | ✅ |
| E_v1 | XYZScaling | 4.8YR 6.3/13.1 | strong orange | ✅ | strong orange | ✅ |
| F7_v1 | Bradford | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| F7_v1 | VonKries | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| F7_v1 | CAT02 | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |
| F7_v1 | XYZScaling | 6.7YR 6.3/11.9 | strong orange | ✅ | strong orange | ✅ |

#### 50. #C26012 - Expected: deep orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.8YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| C_v1 | VonKries | 4.9YR 5.1/11.3 | deep orange | ✅ | deep orange | ✅ |
| C_v1 | CAT02 | 4.7YR 5.1/11.3 | deep orange | ✅ | deep orange | ✅ |
| C_v1 | XYZScaling | 4.1YR 5.1/11.6 | deep orange | ✅ | deep orange | ✅ |
| D50_v1 | Bradford | 4.7YR 5.1/12.7 | deep orange | ✅ | deep orange | ✅ |
| D50_v1 | VonKries | 4.1YR 5.1/12.9 | deep orange | ✅ | deep orange | ✅ |
| D50_v1 | CAT02 | 4.8YR 5.1/12.8 | deep orange | ✅ | deep orange | ✅ |
| D50_v1 | XYZScaling | 5.3YR 5.1/12.3 | deep orange | ✅ | deep orange | ✅ |
| D55_v1 | Bradford | 5.0YR 5.1/12.2 | deep orange | ✅ | deep orange | ✅ |
| D55_v1 | VonKries | 4.6YR 5.1/12.3 | deep orange | ✅ | deep orange | ✅ |
| D55_v1 | CAT02 | 5.1YR 5.1/12.2 | deep orange | ✅ | deep orange | ✅ |
| D55_v1 | XYZScaling | 5.5YR 5.1/11.9 | deep orange | ✅ | deep orange | ✅ |
| D65_v1 | Bradford | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| D65_v1 | VonKries | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| D65_v1 | CAT02 | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| D65_v1 | XYZScaling | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| D75_v1 | Bradford | 5.8YR 5.0/10.8 | deep orange | ✅ | deep orange | ✅ |
| D75_v1 | VonKries | 6.1YR 5.1/10.7 | strong yellowish brown | ❌ | deep orange | ✅ |
| D75_v1 | CAT02 | 5.7YR 5.0/10.7 | deep orange | ✅ | deep orange | ✅ |
| D75_v1 | XYZScaling | 5.3YR 5.1/11.0 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | Bradford | 4.0YR 5.1/12.4 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | VonKries | 3.7YR 5.1/12.4 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | CAT02 | 4.0YR 5.1/12.4 | deep orange | ✅ | deep orange | ✅ |
| E_v1 | XYZScaling | 3.7YR 5.1/12.4 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | Bradford | 3.9YR 5.2/13.7 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | VonKries | 3.0YR 5.1/13.9 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | CAT02 | 4.0YR 5.2/13.9 | deep orange | ✅ | deep orange | ✅ |
| F2_v1 | XYZScaling | 4.5YR 5.1/13.2 | deep orange | ✅ | deep orange | ✅ |
| F7_v1 | Bradford | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| F7_v1 | VonKries | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| F7_v1 | CAT02 | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| F7_v1 | XYZScaling | 5.5YR 5.1/11.4 | deep orange | ✅ | deep orange | ✅ |
| F11_v1 | XYZScaling | 3.9YR 5.1/13.6 | deep orange | ✅ | deep orange | ✅ |

#### 51. #FBAF82 - Expected: light orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.1YR 7.7/6.9 | light orange | ✅ | light orange | ✅ |
| C_v1 | VonKries | 5.4YR 7.7/6.8 | light orange | ✅ | light orange | ✅ |
| C_v1 | CAT02 | 5.0YR 7.7/6.9 | light orange | ✅ | light orange | ✅ |
| C_v1 | XYZScaling | 4.3YR 7.7/7.2 | light orange | ✅ | light orange | ✅ |
| D75_v1 | CAT02 | 7.0YR 7.7/6.0 | light orange | ✅ | light orange | ✅ |
| D75_v1 | XYZScaling | 6.5YR 7.7/6.2 | light orange | ✅ | light orange | ✅ |
| E_v1 | Bradford | 4.9YR 7.7/8.4 | light orange | ✅ | light orange | ✅ |
| E_v1 | VonKries | 4.6YR 7.7/8.4 | light orange | ✅ | light orange | ✅ |
| E_v1 | CAT02 | 4.9YR 7.7/8.3 | light orange | ✅ | light orange | ✅ |
| E_v1 | XYZScaling | 4.7YR 7.7/8.3 | light orange | ✅ | light orange | ✅ |

#### 52. #DE8D5C - Expected: moderate orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.3YR 6.5/7.8 | moderate orange | ✅ | moderate orange | ✅ |
| C_v1 | VonKries | 5.5YR 6.5/7.8 | moderate orange | ✅ | moderate orange | ✅ |
| C_v1 | CAT02 | 5.2YR 6.5/7.8 | moderate orange | ✅ | moderate orange | ✅ |
| C_v1 | XYZScaling | 4.5YR 6.5/8.1 | moderate orange | ✅ | moderate orange | ✅ |
| D50_v1 | Bradford | 6.8YR 6.6/9.5 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D50_v1 | VonKries | 6.3YR 6.5/9.6 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D50_v1 | CAT02 | 6.8YR 6.6/9.6 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D55_v1 | Bradford | 6.9YR 6.5/8.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D55_v1 | VonKries | 6.6YR 6.5/8.9 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D55_v1 | CAT02 | 7.0YR 6.5/8.9 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D65_v1 | Bradford | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D65_v1 | VonKries | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D65_v1 | CAT02 | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D65_v1 | XYZScaling | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| D75_v1 | Bradford | 6.7YR 6.5/7.1 | dark orange yellow | ❌ | moderate orange | ✅ |
| D75_v1 | CAT02 | 6.7YR 6.5/7.0 | dark orange yellow | ❌ | moderate orange | ✅ |
| D75_v1 | XYZScaling | 6.3YR 6.5/7.3 | moderate orange yellow | ❌ | moderate orange | ✅ |
| E_v1 | Bradford | 5.0YR 6.5/9.1 | moderate orange | ✅ | moderate orange | ✅ |
| E_v1 | VonKries | 4.7YR 6.5/9.2 | moderate orange | ✅ | moderate orange | ✅ |
| E_v1 | CAT02 | 5.0YR 6.5/9.1 | moderate orange | ✅ | moderate orange | ✅ |
| E_v1 | XYZScaling | 4.8YR 6.5/9.1 | moderate orange | ✅ | moderate orange | ✅ |
| F7_v1 | Bradford | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| F7_v1 | VonKries | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| F7_v1 | CAT02 | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |
| F7_v1 | XYZScaling | 6.9YR 6.5/7.8 | moderate orange yellow | ❌ | moderate orange | ✅ |

#### 53. #B26633 - Expected: brownish orange

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0YR 5.0/8.0 | strong yellowish brown | ❌ | brownish orange | ✅ |
| C_v1 | VonKries | 6.1YR 5.0/7.9 | strong yellowish brown | ❌ | brownish orange | ✅ |
| C_v1 | CAT02 | 6.0YR 5.0/8.0 | brownish orange | ✅ | brownish orange | ✅ |
| C_v1 | XYZScaling | 5.2YR 5.0/8.2 | brownish orange | ✅ | brownish orange | ✅ |
| D50_v1 | Bradford | 6.7YR 5.0/9.5 | strong yellowish brown | ❌ | brownish orange | ✅ |
| D50_v1 | VonKries | 6.1YR 5.0/9.6 | strong yellowish brown | ❌ | brownish orange | ✅ |
| D50_v1 | CAT02 | 6.8YR 5.0/9.5 | strong yellowish brown | ❌ | brownish orange | ✅ |
| D55_v1 | Bradford | 6.9YR 5.0/8.9 | strong yellowish brown | ❌ | brownish orange | ✅ |
| D55_v1 | VonKries | 6.6YR 5.0/9.0 | strong yellowish brown | ❌ | brownish orange | ✅ |
| D55_v1 | CAT02 | 7.0YR 5.0/8.9 | strong yellowish brown | ❌ | brownish orange | ✅ |
| D75_v1 | XYZScaling | 6.6YR 5.0/7.6 | strong yellowish brown | ❌ | brownish orange | ✅ |
| E_v1 | Bradford | 5.5YR 5.0/9.1 | brownish orange | ✅ | brownish orange | ✅ |
| E_v1 | VonKries | 5.1YR 5.0/9.1 | brownish orange | ✅ | brownish orange | ✅ |
| E_v1 | CAT02 | 5.6YR 5.0/9.1 | brownish orange | ✅ | brownish orange | ✅ |
| E_v1 | XYZScaling | 5.2YR 5.0/9.1 | brownish orange | ✅ | brownish orange | ✅ |

#### 54. #8A4416 - Expected: strong brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 2.7YR 3.8/11.8 | strong brown | ✅ | strong brown | ✅ |
| A_v1 | CAT02 | 2.9YR 3.8/12.0 | strong brown | ✅ | strong brown | ✅ |
| A_v1 | XYZScaling | 2.9YR 3.6/11.2 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | Bradford | 5.0YR 3.7/7.9 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | VonKries | 5.1YR 3.7/7.9 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | CAT02 | 4.9YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| C_v1 | XYZScaling | 4.3YR 3.6/8.1 | strong brown | ✅ | strong brown | ✅ |
| D50_v1 | Bradford | 5.2YR 3.7/8.9 | strong brown | ✅ | strong brown | ✅ |
| D50_v1 | VonKries | 4.7YR 3.7/9.0 | strong brown | ✅ | strong brown | ✅ |
| D50_v1 | CAT02 | 5.3YR 3.7/9.0 | strong brown | ✅ | strong brown | ✅ |
| D50_v1 | XYZScaling | 5.8YR 3.6/8.6 | strong brown | ✅ | strong brown | ✅ |
| D55_v1 | Bradford | 5.5YR 3.7/8.5 | strong brown | ✅ | strong brown | ✅ |
| D55_v1 | VonKries | 5.1YR 3.7/8.6 | strong brown | ✅ | strong brown | ✅ |
| D55_v1 | CAT02 | 5.5YR 3.7/8.6 | strong brown | ✅ | strong brown | ✅ |
| D55_v1 | XYZScaling | 5.9YR 3.6/8.3 | strong brown | ✅ | strong brown | ✅ |
| D65_v1 | Bradford | 5.7YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| D65_v1 | VonKries | 5.7YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| D65_v1 | CAT02 | 5.7YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| D65_v1 | XYZScaling | 5.7YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| D75_v1 | Bradford | 5.9YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| D75_v1 | VonKries | 6.2YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| D75_v1 | CAT02 | 5.8YR 3.6/7.5 | strong brown | ✅ | strong brown | ✅ |
| D75_v1 | XYZScaling | 5.5YR 3.6/7.7 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | Bradford | 4.4YR 3.7/8.8 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | VonKries | 4.1YR 3.7/8.7 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | CAT02 | 4.4YR 3.7/8.7 | strong brown | ✅ | strong brown | ✅ |
| E_v1 | XYZScaling | 4.1YR 3.6/8.7 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | Bradford | 4.5YR 3.7/9.7 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | VonKries | 3.7YR 3.7/9.8 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | CAT02 | 4.7YR 3.7/9.8 | strong brown | ✅ | strong brown | ✅ |
| F2_v1 | XYZScaling | 5.1YR 3.6/9.3 | strong brown | ✅ | strong brown | ✅ |
| F7_v1 | Bradford | 5.7YR 3.7/7.9 | strong brown | ✅ | strong brown | ✅ |
| F7_v1 | VonKries | 5.7YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| F7_v1 | CAT02 | 5.7YR 3.7/7.9 | strong brown | ✅ | strong brown | ✅ |
| F7_v1 | XYZScaling | 5.7YR 3.6/7.9 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | Bradford | 4.1YR 3.7/10.0 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | VonKries | 3.3YR 3.7/10.1 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | CAT02 | 4.3YR 3.7/10.1 | strong brown | ✅ | strong brown | ✅ |
| F11_v1 | XYZScaling | 4.6YR 3.6/9.6 | strong brown | ✅ | strong brown | ✅ |

#### 55. #571A07 - Expected: deep brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.4YR 2.1/8.5 | deep brown | ✅ | deep brown | ✅ |
| A_v1 | VonKries | 3.0YR 1.9/8.7 | deep brown | ✅ | deep brown | ✅ |
| A_v1 | CAT02 | 3.4YR 2.0/8.6 | deep brown | ✅ | deep brown | ✅ |
| A_v1 | XYZScaling | 3.3YR 1.9/8.3 | deep brown | ✅ | deep brown | ✅ |
| C_v1 | Bradford | 3.7YR 1.9/6.5 | deep brown | ✅ | deep brown | ✅ |
| C_v1 | VonKries | 3.7YR 1.9/6.5 | deep brown | ✅ | deep brown | ✅ |
| C_v1 | CAT02 | 3.7YR 1.9/6.5 | deep brown | ✅ | deep brown | ✅ |
| C_v1 | XYZScaling | 3.5YR 1.9/6.7 | deep brown | ✅ | deep brown | ✅ |
| D50_v1 | Bradford | 3.8YR 1.9/7.0 | deep brown | ✅ | deep brown | ✅ |
| D50_v1 | VonKries | 3.7YR 1.9/7.0 | deep brown | ✅ | deep brown | ✅ |
| D50_v1 | CAT02 | 3.9YR 1.9/7.0 | deep brown | ✅ | deep brown | ✅ |
| D50_v1 | XYZScaling | 4.0YR 1.9/6.8 | deep brown | ✅ | deep brown | ✅ |
| D55_v1 | Bradford | 3.9YR 1.9/6.8 | deep brown | ✅ | deep brown | ✅ |
| D55_v1 | VonKries | 3.8YR 1.9/6.8 | deep brown | ✅ | deep brown | ✅ |
| D55_v1 | CAT02 | 3.9YR 1.9/6.8 | deep brown | ✅ | deep brown | ✅ |
| D55_v1 | XYZScaling | 3.9YR 1.9/6.6 | deep brown | ✅ | deep brown | ✅ |
| D65_v1 | Bradford | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| D65_v1 | VonKries | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| D65_v1 | CAT02 | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| D65_v1 | XYZScaling | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| D75_v1 | Bradford | 3.8YR 1.9/6.2 | deep brown | ✅ | deep brown | ✅ |
| D75_v1 | VonKries | 3.9YR 1.9/6.2 | deep brown | ✅ | deep brown | ✅ |
| D75_v1 | CAT02 | 3.8YR 1.9/6.2 | deep brown | ✅ | deep brown | ✅ |
| D75_v1 | XYZScaling | 3.7YR 1.9/6.3 | deep brown | ✅ | deep brown | ✅ |
| E_v1 | Bradford | 3.6YR 1.9/6.9 | deep brown | ✅ | deep brown | ✅ |
| E_v1 | VonKries | 3.6YR 1.9/6.9 | deep brown | ✅ | deep brown | ✅ |
| E_v1 | CAT02 | 3.6YR 1.9/6.9 | deep brown | ✅ | deep brown | ✅ |
| E_v1 | XYZScaling | 3.5YR 1.9/6.9 | deep brown | ✅ | deep brown | ✅ |
| F2_v1 | Bradford | 3.7YR 2.0/7.4 | deep brown | ✅ | deep brown | ✅ |
| F2_v1 | VonKries | 3.5YR 1.9/7.4 | deep brown | ✅ | deep brown | ✅ |
| F2_v1 | CAT02 | 3.7YR 2.0/7.5 | deep brown | ✅ | deep brown | ✅ |
| F2_v1 | XYZScaling | 3.8YR 1.9/7.1 | deep brown | ✅ | deep brown | ✅ |
| F7_v1 | Bradford | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| F7_v1 | VonKries | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| F7_v1 | CAT02 | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| F7_v1 | XYZScaling | 3.9YR 1.9/6.4 | deep brown | ✅ | deep brown | ✅ |
| F11_v1 | Bradford | 3.6YR 2.0/7.6 | deep brown | ✅ | deep brown | ✅ |
| F11_v1 | VonKries | 3.4YR 1.9/7.6 | deep brown | ✅ | deep brown | ✅ |
| F11_v1 | CAT02 | 3.6YR 2.0/7.6 | deep brown | ✅ | deep brown | ✅ |
| F11_v1 | XYZScaling | 3.7YR 1.9/7.3 | deep brown | ✅ | deep brown | ✅ |

#### 56. #AD7C63 - Expected: light brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.0YR 5.5/4.4 | light brown | ✅ | light brown | ✅ |
| C_v1 | VonKries | 5.3YR 5.5/4.4 | light brown | ✅ | light brown | ✅ |
| C_v1 | CAT02 | 5.0YR 5.5/4.4 | light brown | ✅ | light brown | ✅ |
| C_v1 | XYZScaling | 4.2YR 5.5/4.6 | light brown | ✅ | light brown | ✅ |
| D75_v1 | Bradford | 7.5YR 5.5/3.7 | light yellowish brown | ❌ | light brown | ✅ |
| D75_v1 | VonKries | 7.7YR 5.5/3.7 | light yellowish brown | ❌ | light brown | ✅ |
| D75_v1 | CAT02 | 7.4YR 5.5/3.7 | light yellowish brown | ❌ | light brown | ✅ |
| D75_v1 | XYZScaling | 6.8YR 5.5/3.9 | light brown | ✅ | light brown | ✅ |
| E_v1 | Bradford | 5.8YR 5.5/5.4 | light brown | ✅ | light brown | ✅ |
| E_v1 | VonKries | 5.3YR 5.5/5.5 | light brown | ✅ | light brown | ✅ |
| E_v1 | CAT02 | 5.8YR 5.5/5.4 | light brown | ✅ | light brown | ✅ |
| E_v1 | XYZScaling | 5.5YR 5.5/5.4 | light brown | ✅ | light brown | ✅ |

#### 57. #724A38 - Expected: moderate brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.8YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| C_v1 | VonKries | 4.9YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| C_v1 | CAT02 | 4.7YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| C_v1 | XYZScaling | 4.1YR 3.5/3.8 | moderate brown | ✅ | moderate brown | ✅ |
| D50_v1 | Bradford | 7.7YR 3.5/4.8 | moderate brown | ✅ | moderate brown | ✅ |
| D50_v1 | VonKries | 7.2YR 3.5/4.8 | dark yellowish brown | ❌ | moderate brown | ✅ |
| D50_v1 | CAT02 | 7.7YR 3.5/4.8 | moderate brown | ✅ | moderate brown | ✅ |
| D55_v1 | Bradford | 7.5YR 3.5/4.3 | moderate brown | ✅ | moderate brown | ✅ |
| D55_v1 | VonKries | 7.2YR 3.5/4.4 | dark yellowish brown | ❌ | moderate brown | ✅ |
| D55_v1 | CAT02 | 7.6YR 3.5/4.4 | moderate brown | ✅ | moderate brown | ✅ |
| D55_v1 | XYZScaling | 7.9YR 3.5/4.2 | dark yellowish brown | ❌ | moderate brown | ✅ |
| D65_v1 | Bradford | 6.9YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| D65_v1 | VonKries | 6.9YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| D65_v1 | CAT02 | 6.9YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| D65_v1 | XYZScaling | 6.9YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| D75_v1 | Bradford | 6.2YR 3.5/3.3 | moderate brown | ✅ | moderate brown | ✅ |
| D75_v1 | VonKries | 6.5YR 3.5/3.2 | moderate brown | ✅ | moderate brown | ✅ |
| D75_v1 | CAT02 | 6.1YR 3.5/3.3 | moderate brown | ✅ | moderate brown | ✅ |
| D75_v1 | XYZScaling | 5.7YR 3.5/3.4 | moderate brown | ✅ | moderate brown | ✅ |
| E_v1 | Bradford | 5.2YR 3.5/4.5 | moderate brown | ✅ | moderate brown | ✅ |
| E_v1 | VonKries | 5.0YR 3.5/4.5 | moderate brown | ✅ | moderate brown | ✅ |
| E_v1 | CAT02 | 5.2YR 3.5/4.5 | moderate brown | ✅ | moderate brown | ✅ |
| E_v1 | XYZScaling | 5.0YR 3.5/4.5 | moderate brown | ✅ | moderate brown | ✅ |
| F7_v1 | Bradford | 7.0YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| F7_v1 | VonKries | 7.0YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| F7_v1 | CAT02 | 7.0YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |
| F7_v1 | XYZScaling | 7.0YR 3.5/3.7 | moderate brown | ✅ | moderate brown | ✅ |

#### 58. #442112 - Expected: dark brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.4YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| C_v1 | VonKries | 5.4YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| C_v1 | CAT02 | 5.3YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| C_v1 | XYZScaling | 5.0YR 1.7/3.6 | dark brown | ✅ | dark brown | ✅ |
| D50_v1 | Bradford | 6.3YR 1.7/4.1 | dark brown | ✅ | dark brown | ✅ |
| D50_v1 | VonKries | 6.0YR 1.7/4.1 | dark brown | ✅ | dark brown | ✅ |
| D50_v1 | CAT02 | 6.3YR 1.7/4.1 | dark brown | ✅ | dark brown | ✅ |
| D50_v1 | XYZScaling | 6.6YR 1.7/3.9 | dark brown | ✅ | dark brown | ✅ |
| D55_v1 | Bradford | 6.2YR 1.7/3.8 | dark brown | ✅ | dark brown | ✅ |
| D55_v1 | VonKries | 6.1YR 1.7/3.8 | dark brown | ✅ | dark brown | ✅ |
| D55_v1 | CAT02 | 6.3YR 1.7/3.8 | dark brown | ✅ | dark brown | ✅ |
| D55_v1 | XYZScaling | 6.5YR 1.7/3.7 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | Bradford | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | VonKries | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | CAT02 | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| D65_v1 | XYZScaling | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | Bradford | 5.9YR 1.7/3.3 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | VonKries | 6.0YR 1.7/3.3 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | CAT02 | 5.8YR 1.7/3.3 | dark brown | ✅ | dark brown | ✅ |
| D75_v1 | XYZScaling | 5.6YR 1.7/3.4 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | Bradford | 5.4YR 1.7/4.0 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | VonKries | 5.2YR 1.7/4.0 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | CAT02 | 5.4YR 1.7/4.0 | dark brown | ✅ | dark brown | ✅ |
| E_v1 | XYZScaling | 5.2YR 1.7/3.9 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | Bradford | 6.1YR 1.7/4.6 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | VonKries | 5.7YR 1.7/4.6 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | CAT02 | 6.1YR 1.7/4.6 | dark brown | ✅ | dark brown | ✅ |
| F2_v1 | XYZScaling | 6.4YR 1.7/4.3 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | Bradford | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | VonKries | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | CAT02 | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| F7_v1 | XYZScaling | 6.1YR 1.7/3.5 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | Bradford | 5.9YR 1.8/4.8 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | VonKries | 5.4YR 1.7/4.8 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | CAT02 | 5.9YR 1.8/4.8 | dark brown | ✅ | dark brown | ✅ |
| F11_v1 | XYZScaling | 6.1YR 1.7/4.5 | dark brown | ✅ | dark brown | ✅ |

#### 59. #997F75 - Expected: light grayish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | XYZScaling | 7.5YR 5.4/1.5 | light grayish brown | ✅ | light grayish brown | ✅ |

#### 60. #674F48 - Expected: grayish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 3.6/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| A_v2 | VonKries | 2.5YR 3.5/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| A_v2 | CAT02 | 2.5YR 3.6/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| A_v2 | XYZScaling | 2.5YR 3.5/2.0 | grayish brown | ✅ | grayish reddish brown | ❌ |
| C_v1 | Bradford | 2.1YR 3.5/1.9 | grayish brown | ✅ | grayish reddish brown | ❌ |
| C_v1 | VonKries | 2.2YR 3.5/1.9 | grayish brown | ✅ | grayish reddish brown | ❌ |
| C_v1 | CAT02 | 2.1YR 3.5/1.9 | grayish brown | ✅ | grayish reddish brown | ❌ |
| D65_v1 | Bradford | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| D65_v1 | VonKries | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| D65_v1 | CAT02 | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| D65_v1 | XYZScaling | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| D75_v1 | Bradford | 4.4YR 3.5/1.5 | grayish brown | ✅ | brownish gray | ❌ |
| D75_v1 | VonKries | 4.9YR 3.5/1.4 | grayish brown | ✅ | brownish gray | ❌ |
| D75_v1 | CAT02 | 4.4YR 3.5/1.4 | grayish brown | ✅ | brownish gray | ❌ |
| D75_v1 | XYZScaling | 3.8YR 3.5/1.5 | grayish brown | ✅ | grayish brown | ✅ |
| F7_v1 | Bradford | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| F7_v1 | VonKries | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| F7_v1 | CAT02 | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |
| F7_v1 | XYZScaling | 7.5YR 3.5/1.9 | grayish yellowish brown | ❌ | grayish brown | ✅ |

#### 61. #3E2C28 - Expected: dark grayish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 2.5YR 2.0/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| A_v2 | VonKries | 2.5YR 2.0/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| A_v2 | CAT02 | 2.5YR 2.0/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| A_v2 | XYZScaling | 2.5YR 2.0/2.0 | dark grayish brown | ✅ | dark grayish reddish brown | ❌ |
| D50_v1 | Bradford | 7.8YR 2.0/2.5 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D50_v1 | VonKries | 7.5YR 2.0/2.5 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D50_v1 | CAT02 | 7.8YR 2.0/2.5 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D55_v1 | Bradford | 7.3YR 2.0/2.1 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D55_v1 | VonKries | 7.1YR 2.0/2.1 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D55_v1 | CAT02 | 7.3YR 2.0/2.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D55_v1 | XYZScaling | 7.5YR 2.0/2.1 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D65_v1 | Bradford | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D65_v1 | VonKries | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D65_v1 | CAT02 | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| D65_v1 | XYZScaling | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | Bradford | 4.8YR 2.0/2.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | VonKries | 4.6YR 2.0/2.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | CAT02 | 4.8YR 2.0/2.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| E_v1 | XYZScaling | 4.6YR 2.0/2.2 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| F7_v1 | Bradford | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| F7_v1 | VonKries | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| F7_v1 | CAT02 | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |
| F7_v1 | XYZScaling | 5.9YR 2.0/1.7 | dark grayish brown | ✅ | dark grayish brown | ✅ |

#### 62. #928281 - Expected: light brownish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 0.8Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| D65_v1 | VonKries | 0.8Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| D65_v1 | CAT02 | 0.8Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| D65_v1 | XYZScaling | 0.8Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| F7_v1 | Bradford | 1.1Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| F7_v1 | VonKries | 1.0Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| F7_v1 | CAT02 | 1.1Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |
| F7_v1 | XYZScaling | 1.1Y 5.5/1.0 | light brownish gray | ✅ | light brownish gray | ✅ |

#### 63. #605251 - Expected: brownish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.1YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| D65_v1 | VonKries | 8.1YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| D65_v1 | CAT02 | 8.1YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| D65_v1 | XYZScaling | 8.1YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | Bradford | 8.2YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | VonKries | 8.2YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | CAT02 | 8.3YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |
| F7_v1 | XYZScaling | 8.2YR 3.6/0.9 | brownish gray | ✅ | brownish gray | ✅ |

#### 64. #2B211E - Expected: brownish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.6YR 1.3/1.0 | brownish black | ✅ | brownish black | ✅ |
| C_v1 | VonKries | 1.7YR 1.3/1.0 | brownish black | ✅ | brownish black | ✅ |
| C_v1 | CAT02 | 1.6YR 1.3/1.0 | brownish black | ✅ | brownish black | ✅ |
| C_v1 | XYZScaling | 1.5YR 1.3/1.0 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | Bradford | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | VonKries | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | CAT02 | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D65_v1 | XYZScaling | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | Bradford | 6.8YR 1.3/0.6 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | VonKries | 2.6YR 1.3/0.7 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | CAT02 | 6.8YR 1.3/0.6 | brownish black | ✅ | brownish black | ✅ |
| D75_v1 | XYZScaling | 6.4YR 1.3/0.6 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | Bradford | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | VonKries | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | CAT02 | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |
| F7_v1 | XYZScaling | 9.5YR 1.3/0.8 | brownish black | ✅ | brownish black | ✅ |

#### 65. #FFBE50 - Expected: brilliant orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| F2_v1 | VonKries | 9.9YR 8.1/13.2 | brilliant orange yellow | ✅ | brilliant orange yellow | ✅ |
| F11_v1 | Bradford | 0.3Y 8.2/13.4 | vivid yellow | ❌ | brilliant orange yellow | ✅ |
| F11_v1 | VonKries | 9.0YR 8.1/13.8 | brilliant orange yellow | ✅ | brilliant orange yellow | ✅ |
| F11_v1 | CAT02 | 0.6Y 8.2/13.7 | vivid yellow | ❌ | brilliant orange yellow | ✅ |

#### 66. #F0A121 - Expected: strong orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 0.9Y 7.1/11.4 | vivid yellow | ❌ | strong orange yellow | ✅ |
| D50_v1 | VonKries | 0.3Y 7.2/13.1 | vivid yellow | ❌ | strong orange yellow | ✅ |
| E_v1 | Bradford | 9.9YR 7.2/12.5 | strong orange yellow | ✅ | strong orange yellow | ✅ |
| E_v1 | VonKries | 9.7YR 7.2/12.5 | strong orange yellow | ✅ | strong orange yellow | ✅ |
| E_v1 | CAT02 | 10.0YR 7.2/12.5 | strong orange yellow | ✅ | strong orange yellow | ✅ |
| E_v1 | XYZScaling | 0.1Y 7.1/12.3 | vivid yellow | ❌ | strong orange yellow | ✅ |
| F11_v1 | XYZScaling | 0.4Y 7.1/14.0 | vivid yellow | ❌ | strong orange yellow | ✅ |

#### 67. #D08511 - Expected: deep orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8Y 6.1/10.6 | deep yellow | ❌ | deep orange yellow | ✅ |
| C_v1 | CAT02 | 0.7Y 6.1/10.5 | deep yellow | ❌ | deep orange yellow | ✅ |
| C_v1 | XYZScaling | 0.1Y 6.1/10.8 | deep yellow | ❌ | deep orange yellow | ✅ |
| D50_v1 | Bradford | 0.3Y 6.1/12.0 | vivid yellow | ❌ | deep orange yellow | ✅ |
| D50_v1 | VonKries | 9.6YR 6.1/12.3 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| D50_v1 | CAT02 | 0.4Y 6.1/12.3 | vivid yellow | ❌ | deep orange yellow | ✅ |
| D55_v1 | Bradford | 1.0Y 6.1/11.5 | vivid yellow | ❌ | deep orange yellow | ✅ |
| D55_v1 | VonKries | 0.5Y 6.1/11.6 | vivid yellow | ❌ | deep orange yellow | ✅ |
| E_v1 | Bradford | 9.4YR 6.1/11.7 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| E_v1 | VonKries | 9.1YR 6.1/11.7 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| E_v1 | CAT02 | 9.4YR 6.1/11.8 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| E_v1 | XYZScaling | 9.4YR 6.1/11.6 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F2_v1 | Bradford | 8.9YR 6.2/13.3 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F2_v1 | VonKries | 7.9YR 6.1/13.7 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F2_v1 | CAT02 | 9.1YR 6.2/13.7 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F2_v1 | XYZScaling | 0.4Y 6.1/12.7 | vivid yellow | ❌ | deep orange yellow | ✅ |
| F11_v1 | Bradford | 8.2YR 6.2/13.8 | deep orange yellow | ✅ | deep orange yellow | ✅ |
| F11_v1 | XYZScaling | 9.6YR 6.1/13.1 | deep orange yellow | ✅ | deep orange yellow | ✅ |

#### 68. #FCC27C - Expected: light orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 0.5Y 8.2/8.1 | light orange yellow | ✅ | light orange yellow | ✅ |
| E_v1 | VonKries | 0.2Y 8.2/8.1 | light orange yellow | ✅ | light orange yellow | ✅ |
| E_v1 | CAT02 | 0.5Y 8.2/8.1 | light orange yellow | ✅ | light orange yellow | ✅ |
| E_v1 | XYZScaling | 0.8Y 8.2/8.0 | light orange yellow | ✅ | light orange yellow | ✅ |

#### 69. #E7A75D - Expected: moderate orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 0.2Y 7.2/7.7 | moderate yellow | ❌ | moderate orange yellow | ✅ |
| D50_v1 | VonKries | 0.8Y 7.2/9.6 | moderate orange yellow | ✅ | moderate orange yellow | ✅ |
| E_v1 | Bradford | 9.6YR 7.3/9.0 | moderate orange yellow | ✅ | moderate orange yellow | ✅ |
| E_v1 | VonKries | 9.2YR 7.2/9.0 | moderate orange yellow | ✅ | moderate orange yellow | ✅ |
| E_v1 | CAT02 | 9.6YR 7.3/9.0 | moderate orange yellow | ✅ | moderate orange yellow | ✅ |
| E_v1 | XYZScaling | 9.7YR 7.2/8.8 | moderate orange yellow | ✅ | moderate orange yellow | ✅ |

#### 70. #C38639 - Expected: dark orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | XYZScaling | 0.8Y 6.0/8.0 | dark yellow | ❌ | dark orange yellow | ✅ |
| D50_v1 | VonKries | 0.8Y 6.0/9.5 | deep yellow | ❌ | dark orange yellow | ✅ |
| E_v1 | Bradford | 0.1Y 6.0/9.0 | deep yellow | ❌ | dark orange yellow | ✅ |
| E_v1 | VonKries | 9.8YR 6.0/9.0 | dark orange yellow | ✅ | dark orange yellow | ✅ |
| E_v1 | CAT02 | 0.1Y 6.0/9.0 | deep yellow | ❌ | dark orange yellow | ✅ |
| E_v1 | XYZScaling | 0.2Y 6.0/8.9 | deep yellow | ❌ | dark orange yellow | ✅ |

#### 71. #EEC6A6 - Expected: pale orange yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 7.5YR 8.3/2.0 | pale orange yellow | ✅ | pale yellowish pink | ❌ |
| A_v2 | VonKries | 7.5YR 8.2/2.0 | pale orange yellow | ✅ | pale yellowish pink | ❌ |
| A_v2 | CAT02 | 7.5YR 8.3/2.0 | pale orange yellow | ✅ | pale yellowish pink | ❌ |
| A_v2 | XYZScaling | 7.5YR 8.2/2.0 | pale orange yellow | ✅ | pale yellowish pink | ❌ |
| C_v1 | Bradford | 8.3YR 8.2/3.7 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| C_v1 | VonKries | 8.6YR 8.2/3.6 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| C_v1 | CAT02 | 8.3YR 8.2/3.7 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| C_v1 | XYZScaling | 7.8YR 8.2/3.8 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| E_v1 | Bradford | 8.3YR 8.2/5.2 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| E_v1 | VonKries | 8.1YR 8.2/5.2 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| E_v1 | CAT02 | 8.3YR 8.2/5.2 | pale orange yellow | ✅ | pale orange yellow | ✅ |
| E_v1 | XYZScaling | 8.4YR 8.2/5.1 | pale orange yellow | ✅ | pale orange yellow | ✅ |

#### 72. #9E671D - Expected: strong yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 6.3YR 4.9/12.9 | strong yellowish brown | ✅ | deep orange | ❌ |
| A_v1 | CAT02 | 6.6YR 4.9/13.3 | strong yellowish brown | ✅ | deep orange | ❌ |
| A_v1 | XYZScaling | 7.8YR 4.7/12.0 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| D50_v1 | VonKries | 0.7Y 4.7/9.0 | light olive brown | ❌ | strong yellowish brown | ✅ |
| E_v1 | Bradford | 0.4Y 4.8/8.5 | light olive brown | ❌ | strong yellowish brown | ✅ |
| E_v1 | VonKries | 0.1Y 4.7/8.5 | light olive brown | ❌ | strong yellowish brown | ✅ |
| E_v1 | CAT02 | 0.4Y 4.8/8.5 | light olive brown | ❌ | strong yellowish brown | ✅ |
| E_v1 | XYZScaling | 0.5Y 4.7/8.4 | light olive brown | ❌ | strong yellowish brown | ✅ |
| F2_v1 | Bradford | 0.1Y 4.8/9.8 | light olive brown | ❌ | strong yellowish brown | ✅ |
| F2_v1 | VonKries | 9.1YR 4.7/10.1 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F2_v1 | CAT02 | 0.2Y 4.8/10.1 | light olive brown | ❌ | strong yellowish brown | ✅ |
| F11_v1 | Bradford | 9.4YR 4.8/10.2 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F11_v1 | VonKries | 8.4YR 4.7/10.5 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F11_v1 | CAT02 | 9.6YR 4.8/10.5 | strong yellowish brown | ✅ | strong yellowish brown | ✅ |
| F11_v1 | XYZScaling | 0.7Y 4.7/9.7 | light olive brown | ❌ | strong yellowish brown | ✅ |

#### 73. #673F0B - Expected: deep yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 7.3YR 3.0/8.5 | deep yellowish brown | ✅ | strong brown | ❌ |
| C_v1 | Bradford | 0.9Y 3.0/6.0 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| C_v1 | CAT02 | 0.9Y 3.0/6.0 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| C_v1 | XYZScaling | 0.4Y 3.0/6.1 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| D50_v1 | Bradford | 0.6Y 3.0/6.8 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| D50_v1 | VonKries | 0.0Y 3.0/6.9 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| D50_v1 | CAT02 | 0.7Y 3.1/6.9 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| D55_v1 | VonKries | 0.7Y 3.0/6.5 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | Bradford | 9.8YR 3.0/6.6 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | VonKries | 9.6YR 3.0/6.6 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | CAT02 | 9.8YR 3.0/6.6 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| E_v1 | XYZScaling | 9.8YR 3.0/6.6 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | Bradford | 9.4YR 3.1/7.4 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | VonKries | 8.6YR 3.0/7.5 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | CAT02 | 9.6YR 3.1/7.5 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F2_v1 | XYZScaling | 0.6Y 3.0/7.1 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F11_v1 | Bradford | 8.9YR 3.1/7.6 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F11_v1 | VonKries | 7.9YR 3.0/7.7 | deep yellowish brown | ✅ | strong brown | ❌ |
| F11_v1 | CAT02 | 9.0YR 3.1/7.7 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |
| F11_v1 | XYZScaling | 10.0YR 3.0/7.3 | deep yellowish brown | ✅ | deep yellowish brown | ✅ |

#### 74. #C49A74 - Expected: light yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.2Y 6.6/4.3 | grayish yellow | ❌ | light yellowish brown | ✅ |
| C_v1 | VonKries | 0.6Y 6.6/4.2 | grayish yellow | ❌ | light yellowish brown | ✅ |
| C_v1 | CAT02 | 0.1Y 6.6/4.2 | grayish yellow | ❌ | light yellowish brown | ✅ |
| C_v1 | XYZScaling | 9.4YR 6.6/4.4 | light yellowish brown | ✅ | light yellowish brown | ✅ |

#### 75. #886648 - Expected: moderate yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8Y 4.5/3.6 | light olive brown | ❌ | moderate yellowish brown | ✅ |
| C_v1 | CAT02 | 0.8Y 4.5/3.5 | moderate yellowish brown | ✅ | moderate yellowish brown | ✅ |
| C_v1 | XYZScaling | 0.0Y 4.5/3.6 | light olive brown | ❌ | moderate yellowish brown | ✅ |
| E_v1 | Bradford | 10.0YR 4.5/4.5 | moderate yellowish brown | ✅ | moderate yellowish brown | ✅ |
| E_v1 | VonKries | 9.6YR 4.5/4.5 | moderate yellowish brown | ✅ | moderate yellowish brown | ✅ |
| E_v1 | CAT02 | 10.0YR 4.5/4.5 | moderate yellowish brown | ✅ | moderate yellowish brown | ✅ |
| E_v1 | XYZScaling | 0.0Y 4.5/4.4 | light olive brown | ❌ | moderate yellowish brown | ✅ |

#### 76. #50341A - Expected: dark yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.9YR 2.4/3.7 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| C_v1 | VonKries | 0.1Y 2.4/3.6 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| C_v1 | CAT02 | 9.8YR 2.4/3.7 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| C_v1 | XYZScaling | 9.3YR 2.4/3.7 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D50_v1 | Bradford | 0.5Y 2.4/4.4 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D50_v1 | VonKries | 9.9YR 2.4/4.5 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D50_v1 | CAT02 | 0.6Y 2.4/4.5 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D55_v1 | Bradford | 0.8Y 2.4/4.1 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D55_v1 | VonKries | 0.4Y 2.4/4.2 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D55_v1 | CAT02 | 0.9Y 2.4/4.2 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| D75_v1 | XYZScaling | 0.8Y 2.4/3.5 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | Bradford | 9.0YR 2.4/4.2 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | VonKries | 8.8YR 2.4/4.2 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | CAT02 | 9.1YR 2.4/4.2 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| E_v1 | XYZScaling | 9.0YR 2.4/4.2 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F2_v1 | Bradford | 9.5YR 2.5/5.0 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F2_v1 | XYZScaling | 0.5Y 2.4/4.7 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |
| F11_v1 | XYZScaling | 9.9YR 2.4/4.9 | dark yellowish brown | ✅ | dark yellowish brown | ✅ |

#### 77. #B49B8D - Expected: light grayish yellowish brown

No matches

#### 78. #7E695D - Expected: grayish yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 8.0YR 4.5/1.8 | grayish yellowish brown | ✅ | grayish yellowish brown | ✅ |
| E_v1 | Bradford | 8.3YR 4.5/2.7 | grayish yellowish brown | ✅ | grayish yellowish brown | ✅ |
| E_v1 | VonKries | 8.1YR 4.5/2.7 | grayish yellowish brown | ✅ | grayish yellowish brown | ✅ |
| E_v1 | CAT02 | 8.3YR 4.5/2.7 | grayish yellowish brown | ✅ | grayish yellowish brown | ✅ |
| E_v1 | XYZScaling | 8.3YR 4.5/2.7 | grayish yellowish brown | ✅ | grayish yellowish brown | ✅ |

#### 79. #4D3D33 - Expected: dark grayish yellowish brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.8YR 2.7/1.6 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| C_v1 | VonKries | 9.0YR 2.7/1.6 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| C_v1 | CAT02 | 8.7YR 2.7/1.6 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| C_v1 | XYZScaling | 8.1YR 2.7/1.7 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| E_v1 | Bradford | 8.9YR 2.7/2.3 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| E_v1 | VonKries | 8.7YR 2.7/2.3 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| E_v1 | CAT02 | 9.0YR 2.7/2.3 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |
| E_v1 | XYZScaling | 8.9YR 2.7/2.3 | dark grayish yellowish brown | ✅ | dark grayish yellowish brown | ✅ |

#### 80. #F1BF15 - Expected: vivid yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 2.1Y 7.9/16.9 | vivid yellow | ✅ | vivid yellow | ✅ |
| D50_v1 | VonKries | 6.8Y 7.9/12.5 | vivid yellow | ✅ | vivid yellow | ✅ |
| E_v1 | Bradford | 6.8Y 7.9/11.9 | vivid yellow | ✅ | vivid yellow | ✅ |
| E_v1 | VonKries | 6.5Y 7.9/11.9 | vivid yellow | ✅ | vivid yellow | ✅ |
| E_v1 | CAT02 | 6.8Y 7.9/11.9 | vivid yellow | ✅ | vivid yellow | ✅ |
| F2_v1 | Bradford | 4.7Y 8.0/13.6 | vivid yellow | ✅ | vivid yellow | ✅ |
| F2_v1 | VonKries | 3.5Y 7.9/14.1 | vivid yellow | ✅ | vivid yellow | ✅ |
| F2_v1 | CAT02 | 4.7Y 8.0/14.1 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | Bradford | 3.7Y 8.0/14.2 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | VonKries | 2.5Y 7.9/14.7 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | CAT02 | 3.8Y 8.0/14.8 | vivid yellow | ✅ | vivid yellow | ✅ |
| F11_v1 | XYZScaling | 6.7Y 7.9/13.4 | vivid yellow | ✅ | vivid yellow | ✅ |

#### 81. #F7CE50 - Expected: brilliant yellow

No matches

#### 82. #D9AE2F - Expected: strong yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 6.9Y 7.3/10.1 | strong greenish yellow | ❌ | strong yellow | ✅ |
| E_v1 | VonKries | 6.6Y 7.2/10.1 | strong greenish yellow | ❌ | strong yellow | ✅ |
| E_v1 | CAT02 | 6.9Y 7.3/10.1 | strong greenish yellow | ❌ | strong yellow | ✅ |

#### 83. #B88F16 - Expected: deep yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | VonKries | 6.5Y 6.1/10.0 | deep greenish yellow | ❌ | deep yellow | ✅ |
| E_v1 | Bradford | 6.3Y 6.1/9.5 | deep greenish yellow | ❌ | deep yellow | ✅ |
| E_v1 | VonKries | 6.1Y 6.1/9.5 | deep greenish yellow | ❌ | deep yellow | ✅ |
| E_v1 | CAT02 | 6.3Y 6.1/9.5 | deep greenish yellow | ❌ | deep yellow | ✅ |
| E_v1 | XYZScaling | 6.9Y 6.1/9.4 | deep greenish yellow | ❌ | deep yellow | ✅ |
| F2_v1 | Bradford | 5.1Y 6.1/11.0 | deep yellow | ✅ | deep yellow | ✅ |
| F11_v1 | XYZScaling | 6.5Y 6.1/10.8 | deep greenish yellow | ❌ | deep yellow | ✅ |

#### 84. #F4D284 - Expected: light yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | VonKries | 6.5Y 8.5/7.0 | light yellow | ✅ | light yellow | ✅ |

#### 85. #D2AF63 - Expected: moderate yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 6.9Y 7.2/7.1 | moderate greenish yellow | ❌ | moderate yellow | ✅ |
| E_v1 | VonKries | 6.4Y 7.2/7.1 | moderate greenish yellow | ❌ | moderate yellow | ✅ |
| E_v1 | CAT02 | 6.9Y 7.2/7.1 | moderate greenish yellow | ❌ | moderate yellow | ✅ |

#### 86. #B08F42 - Expected: dark yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | VonKries | 6.9Y 6.0/7.0 | dark greenish yellow | ❌ | dark yellow | ✅ |

#### 87. #EFD7B2 - Expected: pale yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | XYZScaling | 6.6Y 8.7/2.4 | pale yellow | ✅ | pale yellow | ✅ |
| E_v1 | Bradford | 3.6Y 8.7/4.3 | pale yellow | ✅ | pale yellow | ✅ |
| E_v1 | VonKries | 3.3Y 8.7/4.3 | pale yellow | ✅ | pale yellow | ✅ |
| E_v1 | CAT02 | 3.6Y 8.7/4.3 | pale yellow | ✅ | pale yellow | ✅ |
| E_v1 | XYZScaling | 4.1Y 8.7/4.2 | pale yellow | ✅ | pale yellow | ✅ |

#### 88. #C8B18B - Expected: grayish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 5.0Y 7.3/4.3 | grayish yellow | ✅ | grayish yellow | ✅ |
| E_v1 | VonKries | 4.7Y 7.3/4.3 | grayish yellow | ✅ | grayish yellow | ✅ |
| E_v1 | CAT02 | 5.1Y 7.3/4.3 | grayish yellow | ✅ | grayish yellow | ✅ |
| E_v1 | XYZScaling | 6.4Y 7.2/4.2 | grayish yellow | ✅ | grayish yellow | ✅ |

#### 89. #A99066 - Expected: dark grayish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 6.2Y 6.0/4.6 | light olive | ❌ | dark grayish yellow | ✅ |
| E_v1 | VonKries | 5.7Y 6.0/4.6 | dark grayish yellow | ✅ | dark grayish yellow | ✅ |
| E_v1 | CAT02 | 6.2Y 6.0/4.6 | light olive | ❌ | dark grayish yellow | ✅ |

#### 90. #EEDFDA - Expected: yellowish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 10.0YR 9.0/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| A_v2 | VonKries | 10.0YR 9.0/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| A_v2 | CAT02 | 10.0YR 9.0/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| A_v2 | XYZScaling | 10.0YR 9.0/2.0 | yellowish white | ✅ | yellowish white | ✅ |
| D65_v1 | Bradford | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| D65_v1 | VonKries | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| D65_v1 | CAT02 | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| D65_v1 | XYZScaling | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| F7_v1 | Bradford | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| F7_v1 | VonKries | 2.8Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| F7_v1 | CAT02 | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |
| F7_v1 | XYZScaling | 2.7Y 9.0/1.2 | yellowish white | ✅ | yellowish white | ✅ |

#### 91. #C6B9B1 - Expected: yellowish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.5YR 7.5/1.1 | yellowish gray | ✅ | yellowish gray | ✅ |
| C_v1 | VonKries | 7.6YR 7.5/1.0 | yellowish gray | ✅ | yellowish gray | ✅ |
| C_v1 | CAT02 | 7.5YR 7.5/1.0 | yellowish gray | ✅ | yellowish gray | ✅ |
| C_v1 | XYZScaling | 7.0YR 7.5/1.1 | yellowish gray | ✅ | pinkish gray | ❌ |

#### 92. #997736 - Expected: light olive brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 1.8Y 5.1/10.5 | light olive brown | ✅ | light olive brown | ✅ |
| F2_v1 | VonKries | 3.4Y 5.1/8.1 | light olive brown | ✅ | light olive brown | ✅ |
| F11_v1 | Bradford | 3.6Y 5.2/8.3 | light olive brown | ✅ | light olive brown | ✅ |
| F11_v1 | VonKries | 2.4Y 5.1/8.5 | light olive brown | ✅ | light olive brown | ✅ |
| F11_v1 | CAT02 | 3.7Y 5.2/8.5 | light olive brown | ✅ | light olive brown | ✅ |

#### 93. #705420 - Expected: moderate olive brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 1.4Y 3.7/8.2 | moderate olive brown | ✅ | moderate olive brown | ✅ |
| F2_v1 | VonKries | 2.9Y 3.7/6.8 | moderate olive brown | ✅ | moderate olive brown | ✅ |
| F11_v1 | Bradford | 3.1Y 3.8/6.9 | moderate olive | ❌ | moderate olive brown | ✅ |
| F11_v1 | VonKries | 2.0Y 3.7/7.1 | moderate olive brown | ✅ | moderate olive brown | ✅ |
| F11_v1 | CAT02 | 3.3Y 3.8/7.1 | moderate olive | ❌ | moderate olive brown | ✅ |

#### 94. #3F2C10 - Expected: dark olive brown

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.5Y 1.9/3.3 | dark olive | ❌ | dark olive brown | ✅ |
| C_v1 | VonKries | 3.8Y 1.9/3.2 | dark olive | ❌ | dark olive brown | ✅ |
| C_v1 | CAT02 | 3.5Y 1.9/3.2 | dark olive | ❌ | dark olive brown | ✅ |
| C_v1 | XYZScaling | 2.9Y 1.9/3.3 | dark olive brown | ✅ | dark olive brown | ✅ |
| D50_v1 | Bradford | 3.7Y 2.0/3.8 | dark olive | ❌ | dark olive brown | ✅ |
| D50_v1 | VonKries | 3.2Y 1.9/3.8 | dark olive | ❌ | dark olive brown | ✅ |
| D50_v1 | CAT02 | 3.8Y 2.0/3.9 | dark olive | ❌ | dark olive brown | ✅ |
| D55_v1 | VonKries | 3.9Y 1.9/3.6 | dark olive | ❌ | dark olive brown | ✅ |
| E_v1 | Bradford | 2.2Y 2.0/3.7 | dark olive brown | ✅ | dark olive brown | ✅ |
| E_v1 | VonKries | 2.0Y 1.9/3.6 | dark olive brown | ✅ | dark olive brown | ✅ |
| E_v1 | CAT02 | 2.2Y 2.0/3.7 | dark olive brown | ✅ | dark olive brown | ✅ |
| E_v1 | XYZScaling | 2.5Y 1.9/3.6 | dark olive brown | ✅ | dark olive brown | ✅ |
| F2_v1 | Bradford | 2.0Y 2.0/4.3 | dark olive brown | ✅ | dark olive brown | ✅ |
| F2_v1 | VonKries | 1.3Y 1.9/4.3 | dark olive brown | ✅ | dark olive brown | ✅ |
| F2_v1 | CAT02 | 2.1Y 2.0/4.4 | dark olive brown | ✅ | dark olive brown | ✅ |
| F11_v1 | Bradford | 1.2Y 2.0/4.5 | dark olive brown | ✅ | dark olive brown | ✅ |
| F11_v1 | CAT02 | 1.4Y 2.0/4.6 | dark olive brown | ✅ | dark olive brown | ✅ |
| F11_v1 | XYZScaling | 3.3Y 1.9/4.1 | dark olive | ❌ | dark olive brown | ✅ |

#### 95. #EBDD21 - Expected: vivid greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 9.7Y 8.6/15.3 | vivid greenish yellow | ✅ | vivid greenish yellow | ✅ |
| F2_v1 | VonKries | 1.1GY 8.6/13.2 | vivid yellow green | ❌ | vivid greenish yellow | ✅ |
| F11_v1 | Bradford | 1.4GY 8.7/13.2 | vivid yellow green | ❌ | vivid greenish yellow | ✅ |
| F11_v1 | VonKries | 9.7Y 8.6/13.5 | vivid greenish yellow | ✅ | vivid greenish yellow | ✅ |
| F11_v1 | CAT02 | 1.4GY 8.8/13.7 | vivid yellow green | ❌ | vivid greenish yellow | ✅ |

#### 96. #E9DC55 - Expected: brilliant greenish yellow

No matches

#### 97. #C4B827 - Expected: strong greenish yellow

No matches

#### 98. #A29812 - Expected: deep greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| F2_v1 | Bradford | 1.3GY 6.1/10.1 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F2_v1 | VonKries | 0.3GY 6.1/10.2 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F2_v1 | CAT02 | 1.3GY 6.2/10.5 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F11_v1 | Bradford | 0.5GY 6.1/10.2 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F11_v1 | VonKries | 9.1Y 6.1/10.4 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |
| F11_v1 | CAT02 | 0.5GY 6.2/10.7 | deep greenish yellow | ✅ | deep greenish yellow | ✅ |

#### 99. #E9DD8A - Expected: light greenish yellow

No matches

#### 100. #C0B55E - Expected: moderate greenish yellow

No matches

#### 101. #9E953C - Expected: dark greenish yellow

No matches

#### 102. #E6DCAB - Expected: pale greenish yellow

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 1.4GY 8.7/3.3 | light yellow green | ❌ | pale greenish yellow | ✅ |

#### 103. #BEB584 - Expected: grayish greenish yellow

No matches

#### 104. #8B7D2E - Expected: light olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 6.6Y 5.1/9.7 | light olive | ✅ | light olive | ✅ |
| D50_v1 | Bradford | 1.5GY 5.1/7.3 | light olive | ✅ | light olive | ✅ |
| D50_v1 | VonKries | 1.0GY 5.1/7.2 | light olive | ✅ | light olive | ✅ |
| D50_v1 | CAT02 | 1.5GY 5.2/7.4 | light olive | ✅ | light olive | ✅ |
| D55_v1 | VonKries | 1.9GY 5.1/7.0 | light olive | ✅ | light olive | ✅ |
| E_v1 | Bradford | 0.9GY 5.1/6.7 | light olive | ✅ | light olive | ✅ |
| E_v1 | VonKries | 0.8GY 5.1/6.7 | light olive | ✅ | light olive | ✅ |
| E_v1 | CAT02 | 0.9GY 5.1/6.7 | light olive | ✅ | light olive | ✅ |
| E_v1 | XYZScaling | 1.4GY 5.1/6.7 | light olive | ✅ | light olive | ✅ |
| F2_v1 | Bradford | 9.8Y 5.2/7.7 | light olive | ✅ | light olive | ✅ |
| F2_v1 | VonKries | 8.5Y 5.1/7.8 | light olive | ✅ | light olive | ✅ |
| F2_v1 | CAT02 | 9.8Y 5.2/8.0 | light olive | ✅ | light olive | ✅ |
| F2_v1 | XYZScaling | 1.4GY 5.1/7.8 | light olive | ✅ | light olive | ✅ |
| F11_v1 | Bradford | 8.6Y 5.2/7.9 | light olive | ✅ | light olive | ✅ |
| F11_v1 | VonKries | 7.3Y 5.1/8.0 | light olive | ✅ | light olive | ✅ |
| F11_v1 | CAT02 | 8.6Y 5.2/8.1 | light olive | ✅ | light olive | ✅ |
| F11_v1 | XYZScaling | 0.8GY 5.1/7.9 | light olive | ✅ | light olive | ✅ |

#### 105. #64591A - Expected: moderate olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.2Y 3.8/8.1 | moderate olive | ✅ | moderate olive brown | ❌ |
| A_v1 | CAT02 | 3.2Y 3.8/8.4 | moderate olive | ✅ | moderate olive brown | ❌ |
| A_v1 | XYZScaling | 6.7Y 3.7/7.5 | moderate olive | ✅ | moderate olive | ✅ |
| C_v1 | Bradford | 1.8GY 3.7/5.3 | moderate olive | ✅ | moderate olive | ✅ |
| C_v1 | CAT02 | 1.8GY 3.7/5.3 | moderate olive | ✅ | moderate olive | ✅ |
| C_v1 | XYZScaling | 1.5GY 3.7/5.3 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | Bradford | 0.7GY 3.7/6.0 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | VonKries | 0.2GY 3.7/6.0 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | CAT02 | 0.8GY 3.7/6.1 | moderate olive | ✅ | moderate olive | ✅ |
| D50_v1 | XYZScaling | 1.9GY 3.7/6.1 | moderate olive | ✅ | moderate olive | ✅ |
| D55_v1 | Bradford | 1.5GY 3.7/5.8 | moderate olive | ✅ | moderate olive | ✅ |
| D55_v1 | VonKries | 1.1GY 3.7/5.8 | moderate olive | ✅ | moderate olive | ✅ |
| D55_v1 | CAT02 | 1.6GY 3.7/5.9 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | Bradford | 0.1GY 3.7/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | VonKries | 0.0GY 3.7/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | CAT02 | 0.1GY 3.7/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| E_v1 | XYZScaling | 0.6GY 3.7/5.6 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | Bradford | 9.0Y 3.7/6.4 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | VonKries | 8.0Y 3.7/6.4 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | CAT02 | 9.1Y 3.8/6.6 | moderate olive | ✅ | moderate olive | ✅ |
| F2_v1 | XYZScaling | 0.8GY 3.7/6.4 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | Bradford | 8.2Y 3.7/6.5 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | VonKries | 7.0Y 3.7/6.6 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | CAT02 | 8.2Y 3.8/6.7 | moderate olive | ✅ | moderate olive | ✅ |
| F11_v1 | XYZScaling | 0.2GY 3.7/6.4 | moderate olive | ✅ | moderate olive | ✅ |

#### 106. #352E0A - Expected: dark olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.8Y 1.9/4.6 | dark olive | ✅ | dark olive brown | ❌ |
| A_v1 | CAT02 | 4.0Y 1.9/4.8 | dark olive | ✅ | dark olive | ✅ |
| A_v1 | XYZScaling | 3.4Y 1.9/4.4 | dark olive | ✅ | dark olive brown | ❌ |
| C_v1 | Bradford | 0.3GY 1.9/3.4 | dark olive | ✅ | dark olive | ✅ |
| C_v1 | VonKries | 0.6GY 1.9/3.4 | dark olive | ✅ | dark olive | ✅ |
| C_v1 | CAT02 | 0.3GY 1.9/3.4 | dark olive | ✅ | dark olive | ✅ |
| C_v1 | XYZScaling | 0.0GY 1.9/3.4 | dark olive | ✅ | dark olive | ✅ |
| D50_v1 | Bradford | 8.5Y 1.9/3.7 | dark olive | ✅ | dark olive | ✅ |
| D50_v1 | VonKries | 7.6Y 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| D50_v1 | CAT02 | 8.1Y 1.9/3.7 | dark olive | ✅ | dark olive | ✅ |
| D50_v1 | XYZScaling | 0.2GY 1.9/3.7 | dark olive | ✅ | dark olive | ✅ |
| D55_v1 | Bradford | 0.2GY 1.9/3.7 | dark olive | ✅ | dark olive | ✅ |
| D55_v1 | VonKries | 9.8Y 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| D55_v1 | CAT02 | 0.2GY 1.9/3.7 | dark olive | ✅ | dark olive | ✅ |
| D55_v1 | XYZScaling | 0.9GY 1.9/3.7 | dark olive | ✅ | dark olive | ✅ |
| D65_v1 | Bradford | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| D65_v1 | VonKries | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| D65_v1 | CAT02 | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| D65_v1 | XYZScaling | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| D75_v1 | XYZScaling | 1.4GY 1.9/3.5 | dark olive | ✅ | dark olive | ✅ |
| E_v1 | Bradford | 8.6Y 1.9/3.5 | dark olive | ✅ | dark olive | ✅ |
| E_v1 | VonKries | 8.4Y 1.9/3.5 | dark olive | ✅ | dark olive | ✅ |
| E_v1 | CAT02 | 8.6Y 1.9/3.5 | dark olive | ✅ | dark olive | ✅ |
| E_v1 | XYZScaling | 9.1Y 1.9/3.5 | dark olive | ✅ | dark olive | ✅ |
| F2_v1 | Bradford | 5.4Y 1.9/3.9 | dark olive | ✅ | dark olive | ✅ |
| F2_v1 | VonKries | 5.3Y 1.9/3.8 | dark olive | ✅ | dark olive | ✅ |
| F2_v1 | CAT02 | 4.6Y 1.9/4.0 | dark olive | ✅ | dark olive | ✅ |
| F2_v1 | XYZScaling | 7.0Y 1.9/3.8 | dark olive | ✅ | dark olive | ✅ |
| F7_v1 | Bradford | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| F7_v1 | VonKries | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| F7_v1 | CAT02 | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| F7_v1 | XYZScaling | 1.3GY 1.9/3.6 | dark olive | ✅ | dark olive | ✅ |
| F11_v1 | Bradford | 5.6Y 1.9/3.9 | dark olive | ✅ | dark olive | ✅ |
| F11_v1 | VonKries | 6.0Y 1.9/3.9 | dark olive | ✅ | dark olive | ✅ |
| F11_v1 | CAT02 | 5.3Y 1.9/4.0 | dark olive | ✅ | dark olive | ✅ |
| F11_v1 | XYZScaling | 5.8Y 1.9/3.8 | dark olive | ✅ | dark olive | ✅ |

#### 107. #8E856F - Expected: light grayish olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | VonKries | 1.2GY 5.5/2.9 | light grayish olive | ✅ | light grayish olive | ✅ |
| E_v1 | XYZScaling | 1.5GY 5.5/2.9 | light grayish olive | ✅ | light grayish olive | ✅ |

#### 108. #5D553F - Expected: grayish olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.4GY 3.6/2.2 | grayish olive | ✅ | grayish olive | ✅ |
| C_v1 | VonKries | 0.6GY 3.6/2.2 | grayish olive | ✅ | grayish olive | ✅ |
| C_v1 | CAT02 | 0.4GY 3.6/2.2 | grayish olive | ✅ | grayish olive | ✅ |
| C_v1 | XYZScaling | 0.2GY 3.6/2.2 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | Bradford | 8.7Y 3.6/2.8 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | VonKries | 8.5Y 3.6/2.7 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | CAT02 | 8.7Y 3.6/2.8 | grayish olive | ✅ | grayish olive | ✅ |
| E_v1 | XYZScaling | 9.1Y 3.6/2.7 | grayish olive | ✅ | grayish olive | ✅ |

#### 109. #35301C - Expected: dark grayish olive

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.3GY 2.0/2.4 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| C_v1 | VonKries | 0.7GY 2.0/2.4 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| C_v1 | CAT02 | 0.3GY 2.0/2.4 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| C_v1 | XYZScaling | 0.1GY 2.0/2.4 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| D55_v1 | Bradford | 0.6GY 2.0/2.9 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| D55_v1 | VonKries | 0.2GY 2.0/2.9 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| D55_v1 | CAT02 | 0.6GY 2.0/3.0 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| D55_v1 | XYZScaling | 1.3GY 2.0/3.0 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | Bradford | 8.4Y 2.0/2.7 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | VonKries | 8.2Y 2.0/2.6 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | CAT02 | 8.4Y 2.0/2.7 | dark grayish olive | ✅ | dark grayish olive | ✅ |
| E_v1 | XYZScaling | 8.9Y 2.0/2.7 | dark grayish olive | ✅ | dark grayish olive | ✅ |

#### 110. #8F877F - Expected: light olive gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8Y 5.6/0.8 | light olive gray | ✅ | light olive gray | ✅ |
| C_v1 | VonKries | 7.1Y 5.6/0.8 | light olive gray | ✅ | light olive gray | ✅ |
| C_v1 | CAT02 | 5.8Y 5.6/0.8 | light olive gray | ✅ | light olive gray | ✅ |
| C_v1 | XYZScaling | 4.4Y 5.6/0.8 | light olive gray | ✅ | light olive gray | ✅ |

#### 111. #58514A - Expected: olive gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.3Y 3.4/0.8 | olive gray | ✅ | olive gray | ✅ |
| C_v1 | VonKries | 6.9Y 3.4/0.8 | olive gray | ✅ | olive gray | ✅ |
| C_v1 | CAT02 | 6.2Y 3.4/0.8 | olive gray | ✅ | olive gray | ✅ |
| C_v1 | XYZScaling | 5.1Y 3.4/0.8 | olive gray | ✅ | olive gray | ✅ |
| D65_v1 | Bradford | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| D65_v1 | VonKries | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| D65_v1 | CAT02 | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| D65_v1 | XYZScaling | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| D75_v1 | Bradford | 3.7GY 3.4/0.7 | olive gray | ✅ | olive gray | ✅ |
| D75_v1 | CAT02 | 3.8GY 3.4/0.7 | olive gray | ✅ | olive gray | ✅ |
| D75_v1 | XYZScaling | 2.3GY 3.4/0.7 | olive gray | ✅ | olive gray | ✅ |
| F7_v1 | Bradford | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| F7_v1 | VonKries | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| F7_v1 | CAT02 | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |
| F7_v1 | XYZScaling | 0.7GY 3.4/1.2 | olive gray | ✅ | olive gray | ✅ |

#### 112. #23211C - Expected: olive black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.9Y 1.2/0.6 | olive black | ✅ | olive black | ✅ |
| C_v1 | VonKries | 8.2Y 1.2/0.6 | olive black | ✅ | olive black | ✅ |
| C_v1 | CAT02 | 7.9Y 1.2/0.6 | olive black | ✅ | olive black | ✅ |
| C_v1 | XYZScaling | 7.5Y 1.2/0.5 | olive black | ✅ | olive black | ✅ |
| D65_v1 | Bradford | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| D65_v1 | VonKries | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| D65_v1 | CAT02 | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| D65_v1 | XYZScaling | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| E_v1 | Bradford | 5.5Y 1.2/0.9 | olive black | ✅ | olive black | ✅ |
| E_v1 | VonKries | 5.5Y 1.2/0.9 | olive black | ✅ | olive black | ✅ |
| E_v1 | CAT02 | 5.5Y 1.2/0.9 | olive black | ✅ | olive black | ✅ |
| E_v1 | XYZScaling | 5.7Y 1.2/0.9 | olive black | ✅ | olive black | ✅ |
| F7_v1 | Bradford | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| F7_v1 | VonKries | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| F7_v1 | CAT02 | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |
| F7_v1 | XYZScaling | 2.3GY 1.2/1.0 | olive black | ✅ | olive black | ✅ |

#### 113. #A7DC26 - Expected: vivid yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 3.6GY 8.2/13.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| A_v1 | VonKries | 1.4GY 8.1/13.9 | vivid yellow green | ✅ | vivid greenish yellow | ❌ |
| A_v1 | CAT02 | 3.4GY 8.2/14.3 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| A_v1 | XYZScaling | 5.4GY 8.1/14.5 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | Bradford | 7.6GY 8.1/13.6 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | VonKries | 7.1GY 8.1/13.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D50_v1 | CAT02 | 7.5GY 8.2/13.8 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| D55_v1 | VonKries | 7.8GY 8.1/13.6 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | Bradford | 7.3GY 8.1/12.9 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | VonKries | 7.2GY 8.1/12.8 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | CAT02 | 7.3GY 8.1/12.9 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| E_v1 | XYZScaling | 7.9GY 8.1/13.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | Bradford | 6.4GY 8.1/13.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | VonKries | 5.7GY 8.1/13.2 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | CAT02 | 6.2GY 8.2/13.8 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F2_v1 | XYZScaling | 7.6GY 8.1/14.4 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | Bradford | 5.8GY 8.1/13.2 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | VonKries | 5.6GY 8.1/13.1 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | CAT02 | 5.7GY 8.2/13.6 | vivid yellow green | ✅ | vivid yellow green | ✅ |
| F11_v1 | XYZScaling | 7.2GY 8.1/14.3 | vivid yellow green | ✅ | vivid yellow green | ✅ |

#### 114. #C3DF69 - Expected: brilliant yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.9GY 8.4/9.4 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| C_v1 | CAT02 | 7.9GY 8.4/9.3 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| C_v1 | XYZScaling | 7.8GY 8.4/9.3 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| D50_v1 | Bradford | 6.5GY 8.5/10.6 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| D50_v1 | VonKries | 6.4GY 8.4/10.5 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| D50_v1 | CAT02 | 6.5GY 8.5/10.7 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| D55_v1 | Bradford | 7.2GY 8.4/10.4 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| D55_v1 | VonKries | 6.9GY 8.4/10.3 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| D55_v1 | CAT02 | 7.1GY 8.5/10.5 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| D55_v1 | XYZScaling | 7.6GY 8.4/10.7 | brilliant yellowish green | ❌ | brilliant yellow green | ✅ |
| E_v1 | Bradford | 6.6GY 8.4/9.6 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| E_v1 | VonKries | 6.6GY 8.4/9.6 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| E_v1 | CAT02 | 6.6GY 8.4/9.7 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| E_v1 | XYZScaling | 6.7GY 8.4/9.8 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| F2_v1 | VonKries | 5.7GY 8.4/11.0 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |
| F11_v1 | VonKries | 5.3GY 8.4/11.0 | brilliant yellow green | ✅ | brilliant yellow green | ✅ |

#### 115. #82A12B - Expected: strong yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.8GY 6.1/9.7 | strong yellowish green | ❌ | strong yellow green | ✅ |
| C_v1 | CAT02 | 7.8GY 6.1/9.6 | strong yellowish green | ❌ | strong yellow green | ✅ |
| C_v1 | XYZScaling | 7.8GY 6.1/9.7 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D50_v1 | Bradford | 6.9GY 6.1/10.3 | strong yellow green | ✅ | strong yellow green | ✅ |
| D50_v1 | VonKries | 6.5GY 6.1/10.2 | strong yellow green | ✅ | strong yellow green | ✅ |
| D50_v1 | CAT02 | 6.8GY 6.1/10.5 | strong yellow green | ✅ | strong yellow green | ✅ |
| D50_v1 | XYZScaling | 7.5GY 6.1/10.7 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | Bradford | 7.4GY 6.1/10.2 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | VonKries | 7.1GY 6.1/10.2 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | CAT02 | 7.3GY 6.1/10.4 | strong yellowish green | ❌ | strong yellow green | ✅ |
| D55_v1 | XYZScaling | 7.8GY 6.1/10.6 | strong yellowish green | ❌ | strong yellow green | ✅ |
| E_v1 | Bradford | 6.7GY 6.1/9.6 | strong yellow green | ✅ | strong yellow green | ✅ |
| E_v1 | VonKries | 6.6GY 6.1/9.6 | strong yellow green | ✅ | strong yellow green | ✅ |
| E_v1 | CAT02 | 6.6GY 6.1/9.6 | strong yellow green | ✅ | strong yellow green | ✅ |
| E_v1 | XYZScaling | 7.1GY 6.1/9.9 | strong yellowish green | ❌ | strong yellow green | ✅ |
| F2_v1 | Bradford | 5.8GY 6.1/10.2 | strong yellow green | ✅ | strong yellow green | ✅ |
| F2_v1 | VonKries | 5.4GY 6.1/10.0 | strong yellow green | ✅ | strong yellow green | ✅ |
| F2_v1 | CAT02 | 5.7GY 6.1/10.5 | strong yellow green | ✅ | strong yellow green | ✅ |
| F2_v1 | XYZScaling | 6.8GY 6.1/10.9 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | Bradford | 5.4GY 6.1/10.1 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | VonKries | 5.0GY 6.1/9.9 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | CAT02 | 5.3GY 6.2/10.4 | strong yellow green | ✅ | strong yellow green | ✅ |
| F11_v1 | XYZScaling | 6.5GY 6.1/10.9 | strong yellow green | ✅ | strong yellow green | ✅ |

#### 116. #486C0E - Expected: deep yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 2.8GY 4.1/8.1 | deep yellow green | ✅ | deep yellow green | ✅ |
| A_v1 | CAT02 | 2.5GY 4.1/8.6 | deep yellow green | ✅ | deep yellow green | ✅ |
| A_v1 | XYZScaling | 5.9GY 4.1/9.1 | deep yellow green | ✅ | deep yellow green | ✅ |
| D50_v1 | Bradford | 7.5GY 4.1/8.5 | deep yellow green | ✅ | deep yellow green | ✅ |
| D50_v1 | VonKries | 7.2GY 4.1/8.4 | deep yellow green | ✅ | deep yellow green | ✅ |
| D50_v1 | CAT02 | 7.4GY 4.1/8.7 | deep yellow green | ✅ | deep yellow green | ✅ |
| D50_v1 | XYZScaling | 7.6GY 4.1/8.8 | deep yellow green | ✅ | deep yellow green | ✅ |
| D55_v1 | Bradford | 7.7GY 4.1/8.5 | deep yellow green | ✅ | deep yellow green | ✅ |
| D55_v1 | VonKries | 7.6GY 4.1/8.5 | deep yellow green | ✅ | deep yellow green | ✅ |
| D55_v1 | CAT02 | 7.7GY 4.1/8.6 | deep yellow green | ✅ | deep yellow green | ✅ |
| D55_v1 | XYZScaling | 7.8GY 4.1/8.7 | deep yellow green | ✅ | deep yellow green | ✅ |
| E_v1 | Bradford | 7.4GY 4.1/8.1 | deep yellow green | ✅ | deep yellow green | ✅ |
| E_v1 | VonKries | 7.3GY 4.1/8.0 | deep yellow green | ✅ | deep yellow green | ✅ |
| E_v1 | CAT02 | 7.3GY 4.1/8.1 | deep yellow green | ✅ | deep yellow green | ✅ |
| E_v1 | XYZScaling | 7.7GY 4.1/8.3 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | Bradford | 6.6GY 4.1/8.4 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | VonKries | 6.1GY 4.1/8.3 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | CAT02 | 6.5GY 4.1/8.7 | deep yellow green | ✅ | deep yellow green | ✅ |
| F2_v1 | XYZScaling | 7.4GY 4.1/9.0 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | Bradford | 6.2GY 4.1/8.3 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | VonKries | 5.7GY 4.1/8.2 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | CAT02 | 6.1GY 4.1/8.6 | deep yellow green | ✅ | deep yellow green | ✅ |
| F11_v1 | XYZScaling | 7.2GY 4.1/8.9 | deep yellow green | ✅ | deep yellow green | ✅ |

#### 117. #CEDB9F - Expected: light yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.0GY 8.5/4.9 | light yellow green | ✅ | light yellow green | ✅ |
| C_v1 | CAT02 | 8.0GY 8.5/4.8 | light yellow green | ✅ | light yellow green | ✅ |
| C_v1 | XYZScaling | 7.9GY 8.5/4.9 | light yellow green | ✅ | light yellow green | ✅ |
| D55_v1 | Bradford | 7.5GY 8.5/6.7 | light yellow green | ✅ | light yellow green | ✅ |
| D55_v1 | VonKries | 7.8GY 8.5/6.8 | light yellow green | ✅ | light yellow green | ✅ |
| D55_v1 | CAT02 | 7.5GY 8.5/6.8 | light yellow green | ✅ | light yellow green | ✅ |
| D55_v1 | XYZScaling | 7.4GY 8.5/6.7 | light yellow green | ✅ | light yellow green | ✅ |
| E_v1 | Bradford | 7.7GY 8.5/6.1 | light yellow green | ✅ | light yellow green | ✅ |
| E_v1 | CAT02 | 7.5GY 8.5/6.1 | light yellow green | ✅ | light yellow green | ✅ |

#### 118. #8B9A5F - Expected: moderate yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.8GY 6.0/5.5 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| C_v1 | CAT02 | 7.8GY 6.0/5.5 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| C_v1 | XYZScaling | 7.7GY 6.0/5.5 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| D50_v1 | Bradford | 6.3GY 6.0/6.8 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D50_v1 | VonKries | 6.0GY 6.0/6.8 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D50_v1 | CAT02 | 6.2GY 6.0/6.9 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D55_v1 | Bradford | 6.9GY 6.0/6.6 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D55_v1 | VonKries | 6.7GY 6.0/6.5 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D55_v1 | CAT02 | 6.9GY 6.0/6.6 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| D55_v1 | XYZScaling | 7.3GY 6.0/6.8 | moderate yellowish green | ❌ | moderate yellow green | ✅ |
| E_v1 | Bradford | 6.1GY 6.0/5.9 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | VonKries | 6.0GY 6.0/5.8 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | CAT02 | 6.1GY 6.0/5.9 | moderate yellow green | ✅ | moderate yellow green | ✅ |
| E_v1 | XYZScaling | 6.4GY 6.0/6.0 | moderate yellow green | ✅ | moderate yellow green | ✅ |

#### 119. #D7D7C1 - Expected: pale yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 5.3GY 8.5/1.5 | pale yellow green | ✅ | pale yellow green | ✅ |
| D50_v2 | Bradford | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D50_v2 | VonKries | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D50_v2 | CAT02 | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D50_v2 | XYZScaling | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | Bradford | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | VonKries | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | CAT02 | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| D55_v2 | XYZScaling | 7.5GY 8.5/2.0 | very pale green | ❌ | pale yellow green | ✅ |
| F2_v2 | Bradford | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F2_v2 | VonKries | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F2_v2 | CAT02 | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F2_v2 | XYZScaling | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | Bradford | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | VonKries | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | CAT02 | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |
| F11_v2 | XYZScaling | 5.0GY 8.5/2.0 | pale yellow green | ✅ | pale yellow green | ✅ |

#### 120. #979A85 - Expected: grayish yellow green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.9GY 6.2/1.8 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| C_v1 | VonKries | 7.1GY 6.2/1.9 | pale green | ❌ | grayish yellow green | ✅ |
| C_v1 | CAT02 | 6.9GY 6.2/1.8 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| C_v1 | XYZScaling | 6.9GY 6.2/1.8 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| E_v1 | Bradford | 3.8GY 6.2/2.6 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| E_v1 | VonKries | 3.5GY 6.2/2.6 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| E_v1 | CAT02 | 3.7GY 6.2/2.7 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| E_v1 | XYZScaling | 4.8GY 6.2/2.7 | grayish yellow green | ✅ | grayish yellow green | ✅ |
| F2_v2 | Bradford | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | VonKries | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | CAT02 | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F2_v2 | XYZScaling | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | Bradford | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | VonKries | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | CAT02 | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |
| F11_v2 | XYZScaling | 7.5GY 6.2/2.0 | pale green | ❌ | grayish yellow green | ✅ |

#### 121. #2C5506 - Expected: strong olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | Bradford | 4.7GY 3.1/7.1 | strong olive green | ✅ | strong olive green | ✅ |
| A_v1 | CAT02 | 4.3GY 3.2/7.4 | strong olive green | ✅ | strong olive green | ✅ |
| A_v1 | XYZScaling | 6.0GY 3.1/8.0 | strong olive green | ✅ | strong olive green | ✅ |
| C_v1 | Bradford | 7.6GY 3.1/7.5 | strong olive green | ✅ | strong olive green | ✅ |
| C_v1 | VonKries | 7.7GY 3.1/7.6 | strong olive green | ✅ | strong olive green | ✅ |
| C_v1 | CAT02 | 7.7GY 3.1/7.5 | strong olive green | ✅ | strong olive green | ✅ |
| C_v1 | XYZScaling | 7.7GY 3.1/7.5 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | Bradford | 7.2GY 3.2/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | VonKries | 7.1GY 3.1/7.7 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | CAT02 | 7.1GY 3.2/7.9 | strong olive green | ✅ | strong olive green | ✅ |
| D50_v1 | XYZScaling | 7.3GY 3.1/8.1 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | Bradford | 7.4GY 3.2/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | VonKries | 7.3GY 3.1/7.7 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | CAT02 | 7.3GY 3.2/7.9 | strong olive green | ✅ | strong olive green | ✅ |
| D55_v1 | XYZScaling | 7.4GY 3.1/8.0 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | Bradford | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | VonKries | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | CAT02 | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D65_v1 | XYZScaling | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | Bradford | 7.7GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | VonKries | 7.9GY 3.1/7.9 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | CAT02 | 7.8GY 3.1/7.7 | strong olive green | ✅ | strong olive green | ✅ |
| D75_v1 | XYZScaling | 7.8GY 3.1/7.6 | strong olive green | ✅ | strong olive green | ✅ |
| E_v1 | Bradford | 7.3GY 3.1/7.5 | strong olive green | ✅ | strong olive green | ✅ |
| E_v1 | VonKries | 7.3GY 3.1/7.4 | strong olive green | ✅ | strong olive green | ✅ |
| E_v1 | CAT02 | 7.3GY 3.1/7.5 | strong olive green | ✅ | strong olive green | ✅ |
| E_v1 | XYZScaling | 7.4GY 3.1/7.7 | strong olive green | ✅ | strong olive green | ✅ |
| F2_v1 | Bradford | 7.0GY 3.2/7.7 | strong olive green | ✅ | strong olive green | ✅ |
| F2_v1 | VonKries | 6.8GY 3.1/7.6 | strong olive green | ✅ | strong olive green | ✅ |
| F2_v1 | CAT02 | 6.9GY 3.2/7.9 | strong olive green | ✅ | strong olive green | ✅ |
| F2_v1 | XYZScaling | 7.0GY 3.1/8.2 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | Bradford | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | VonKries | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | CAT02 | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| F7_v1 | XYZScaling | 7.6GY 3.1/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| F11_v1 | Bradford | 6.9GY 3.2/7.6 | strong olive green | ✅ | strong olive green | ✅ |
| F11_v1 | VonKries | 6.4GY 3.1/7.5 | strong olive green | ✅ | strong olive green | ✅ |
| F11_v1 | CAT02 | 6.8GY 3.2/7.8 | strong olive green | ✅ | strong olive green | ✅ |
| F11_v1 | XYZScaling | 7.0GY 3.1/8.1 | strong olive green | ✅ | strong olive green | ✅ |

#### 122. #495B22 - Expected: moderate olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.5GY 3.5/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ |
| C_v1 | VonKries | 7.6GY 3.5/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ |
| C_v1 | CAT02 | 7.5GY 3.5/5.7 | dark yellowish green | ❌ | moderate olive green | ✅ |
| C_v1 | XYZScaling | 7.4GY 3.5/5.8 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D50_v1 | Bradford | 6.5GY 3.6/6.4 | moderate olive green | ✅ | moderate olive green | ✅ |
| D50_v1 | VonKries | 6.2GY 3.5/6.3 | moderate olive green | ✅ | moderate olive green | ✅ |
| D50_v1 | CAT02 | 6.4GY 3.6/6.5 | moderate olive green | ✅ | moderate olive green | ✅ |
| D50_v1 | XYZScaling | 7.0GY 3.5/6.6 | moderate olive green | ✅ | moderate olive green | ✅ |
| D55_v1 | Bradford | 7.0GY 3.6/6.3 | moderate olive green | ✅ | moderate olive green | ✅ |
| D55_v1 | VonKries | 6.8GY 3.5/6.2 | moderate olive green | ✅ | moderate olive green | ✅ |
| D55_v1 | CAT02 | 6.9GY 3.6/6.4 | moderate olive green | ✅ | moderate olive green | ✅ |
| D55_v1 | XYZScaling | 7.3GY 3.5/6.4 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | Bradford | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | VonKries | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | CAT02 | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| D65_v1 | XYZScaling | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| E_v1 | Bradford | 6.3GY 3.5/5.8 | moderate olive green | ✅ | moderate olive green | ✅ |
| E_v1 | VonKries | 6.2GY 3.5/5.8 | moderate olive green | ✅ | moderate olive green | ✅ |
| E_v1 | CAT02 | 6.3GY 3.5/5.8 | moderate olive green | ✅ | moderate olive green | ✅ |
| E_v1 | XYZScaling | 6.7GY 3.5/6.0 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | Bradford | 5.5GY 3.6/6.4 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | VonKries | 5.0GY 3.5/6.3 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | CAT02 | 5.4GY 3.6/6.5 | moderate olive green | ✅ | moderate olive green | ✅ |
| F2_v1 | XYZScaling | 6.3GY 3.5/6.8 | moderate olive green | ✅ | moderate olive green | ✅ |
| F7_v1 | Bradford | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F7_v1 | VonKries | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F7_v1 | CAT02 | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F7_v1 | XYZScaling | 7.8GY 3.5/6.2 | dark yellowish green | ❌ | moderate olive green | ✅ |
| F11_v1 | Bradford | 5.0GY 3.6/6.3 | moderate olive green | ✅ | moderate olive green | ✅ |
| F11_v1 | VonKries | 4.0GY 3.5/6.2 | moderate olive green | ✅ | moderate olive green | ✅ |
| F11_v1 | CAT02 | 5.0GY 3.6/6.5 | moderate olive green | ✅ | moderate olive green | ✅ |
| F11_v1 | XYZScaling | 6.0GY 3.5/6.8 | moderate olive green | ✅ | moderate olive green | ✅ |

#### 123. #20340B - Expected: dark olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v1 | XYZScaling | 3.3GY 1.9/4.9 | dark olive green | ✅ | dark olive green | ✅ |
| C_v1 | Bradford | 6.9GY 1.9/4.7 | dark olive green | ✅ | dark olive green | ✅ |
| C_v1 | VonKries | 7.0GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| C_v1 | CAT02 | 6.9GY 1.9/4.7 | dark olive green | ✅ | dark olive green | ✅ |
| C_v1 | XYZScaling | 7.0GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | Bradford | 6.5GY 1.9/5.1 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | VonKries | 6.3GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | CAT02 | 6.4GY 1.9/5.1 | dark olive green | ✅ | dark olive green | ✅ |
| D50_v1 | XYZScaling | 6.6GY 1.9/5.2 | dark olive green | ✅ | dark olive green | ✅ |
| D55_v1 | Bradford | 6.7GY 1.9/5.1 | dark olive green | ✅ | dark olive green | ✅ |
| D55_v1 | VonKries | 6.6GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| D55_v1 | CAT02 | 6.7GY 1.9/5.1 | dark olive green | ✅ | dark olive green | ✅ |
| D55_v1 | XYZScaling | 6.8GY 1.9/5.2 | dark olive green | ✅ | dark olive green | ✅ |
| D65_v1 | Bradford | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| D65_v1 | VonKries | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| D65_v1 | CAT02 | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| D65_v1 | XYZScaling | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| D75_v1 | Bradford | 7.2GY 1.9/4.9 | dark olive green | ✅ | dark olive green | ✅ |
| D75_v1 | VonKries | 7.2GY 1.9/4.9 | dark olive green | ✅ | dark olive green | ✅ |
| D75_v1 | CAT02 | 7.2GY 1.9/4.9 | dark olive green | ✅ | dark olive green | ✅ |
| D75_v1 | XYZScaling | 7.2GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | Bradford | 6.6GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | VonKries | 6.5GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | CAT02 | 6.6GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| E_v1 | XYZScaling | 6.7GY 1.9/4.9 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | Bradford | 5.7GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | VonKries | 5.2GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | CAT02 | 5.5GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| F2_v1 | XYZScaling | 6.1GY 1.9/5.2 | dark olive green | ✅ | dark olive green | ✅ |
| F7_v1 | Bradford | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| F7_v1 | VonKries | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| F7_v1 | CAT02 | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| F7_v1 | XYZScaling | 7.0GY 1.9/5.0 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | Bradford | 5.3GY 1.9/4.8 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | VonKries | 4.7GY 1.9/4.7 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | CAT02 | 5.1GY 1.9/4.9 | dark olive green | ✅ | dark olive green | ✅ |
| F11_v1 | XYZScaling | 5.9GY 1.9/5.2 | dark olive green | ✅ | dark olive green | ✅ |

#### 124. #545947 - Expected: grayish olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | XYZScaling | 5.0GY 3.6/2.0 | grayish olive green | ✅ | grayish olive green | ✅ |
| C_v1 | Bradford | 7.3GY 3.6/2.1 | grayish green | ❌ | grayish olive green | ✅ |
| C_v1 | VonKries | 7.5GY 3.6/2.2 | grayish green | ❌ | grayish olive green | ✅ |
| C_v1 | CAT02 | 7.3GY 3.6/2.1 | grayish green | ❌ | grayish olive green | ✅ |
| C_v1 | XYZScaling | 7.2GY 3.6/2.1 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | Bradford | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | VonKries | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | CAT02 | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D50_v2 | XYZScaling | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| D55_v1 | VonKries | 5.9GY 3.6/3.0 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | Bradford | 4.3GY 3.6/2.4 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | VonKries | 4.1GY 3.6/2.4 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | CAT02 | 4.2GY 3.6/2.4 | grayish olive green | ✅ | grayish olive green | ✅ |
| E_v1 | XYZScaling | 5.1GY 3.6/2.5 | grayish olive green | ✅ | grayish olive green | ✅ |
| F2_v2 | Bradford | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F2_v2 | VonKries | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F2_v2 | CAT02 | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F2_v2 | XYZScaling | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | Bradford | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | VonKries | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | CAT02 | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |
| F11_v2 | XYZScaling | 7.5GY 3.6/2.0 | grayish green | ❌ | grayish olive green | ✅ |

#### 125. #2F3326 - Expected: dark grayish olive green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| A_v2 | Bradford | 5.0GY 2.0/2.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| A_v2 | CAT02 | 5.0GY 2.0/2.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| A_v2 | XYZScaling | 5.0GY 2.0/2.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| C_v1 | Bradford | 6.8GY 2.0/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| C_v1 | VonKries | 6.9GY 2.0/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| C_v1 | CAT02 | 6.8GY 2.0/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| C_v1 | XYZScaling | 6.7GY 2.0/2.1 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v1 | Bradford | 5.0GY 2.0/3.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v2 | Bradford | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| D50_v1 | VonKries | 4.5GY 2.0/2.9 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v2 | VonKries | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| D50_v1 | CAT02 | 5.0GY 2.0/3.0 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D50_v2 | CAT02 | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| D50_v2 | XYZScaling | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| D55_v1 | Bradford | 5.8GY 2.0/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | VonKries | 5.6GY 2.0/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | CAT02 | 5.8GY 2.0/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D55_v1 | XYZScaling | 6.0GY 2.0/2.8 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D65_v1 | Bradford | 7.4GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D65_v1 | VonKries | 7.4GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D65_v1 | CAT02 | 7.4GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| D65_v1 | XYZScaling | 7.4GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | Bradford | 3.8GY 2.0/2.3 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | VonKries | 3.6GY 2.0/2.3 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | CAT02 | 3.7GY 2.0/2.3 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| E_v1 | XYZScaling | 4.5GY 2.0/2.4 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F2_v2 | Bradford | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F2_v2 | VonKries | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F2_v2 | CAT02 | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F2_v2 | XYZScaling | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F7_v1 | Bradford | 7.3GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F7_v1 | VonKries | 7.3GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F7_v1 | CAT02 | 7.3GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F7_v1 | XYZScaling | 7.3GY 2.0/2.5 | dark grayish olive green | ✅ | dark grayish olive green | ✅ |
| F11_v2 | Bradford | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | VonKries | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | CAT02 | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |
| F11_v2 | XYZScaling | 7.5GY 2.0/2.0 | dark grayish green | ❌ | dark grayish olive green | ✅ |

#### 126. #3FD740 - Expected: vivid yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.2G 7.5/15.6 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| C_v1 | VonKries | 1.3G 7.5/15.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| C_v1 | CAT02 | 1.2G 7.5/15.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| C_v1 | XYZScaling | 1.3G 7.5/15.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | Bradford | 0.2G 7.5/15.7 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | VonKries | 0.1G 7.5/15.4 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | CAT02 | 0.1G 7.6/15.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D50_v1 | XYZScaling | 0.1G 7.5/16.2 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | Bradford | 0.4G 7.5/15.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | VonKries | 0.3G 7.5/15.6 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | CAT02 | 0.3G 7.6/15.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D55_v1 | XYZScaling | 0.5G 7.5/16.3 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D65_v1 | Bradford | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D65_v1 | VonKries | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D65_v1 | CAT02 | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D65_v1 | XYZScaling | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D75_v1 | Bradford | 1.9G 7.5/17.0 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D75_v1 | VonKries | 2.1G 7.5/17.4 | vivid green | ❌ | vivid yellowish green | ✅ |
| D75_v1 | CAT02 | 2.0G 7.5/17.1 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| D75_v1 | XYZScaling | 1.7G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| E_v1 | Bradford | 0.4G 7.5/14.9 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| E_v1 | VonKries | 0.4G 7.5/14.8 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| E_v1 | CAT02 | 0.4G 7.5/14.9 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| E_v1 | XYZScaling | 0.5G 7.5/15.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | Bradford | 9.9GY 7.5/15.4 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | VonKries | 9.5GY 7.5/15.0 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | CAT02 | 9.7GY 7.6/15.7 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F2_v1 | XYZScaling | 9.6GY 7.5/16.3 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F7_v1 | Bradford | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F7_v1 | VonKries | 1.2G 7.5/16.4 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F7_v1 | CAT02 | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F7_v1 | XYZScaling | 1.2G 7.5/16.5 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | Bradford | 9.6GY 7.5/15.1 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | VonKries | 9.2GY 7.5/14.7 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | CAT02 | 9.4GY 7.6/15.4 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |
| F11_v1 | XYZScaling | 9.5GY 7.5/16.2 | vivid yellowish green | ✅ | vivid yellowish green | ✅ |

#### 127. #87D989 - Expected: brilliant yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 1.9G 7.9/10.0 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | VonKries | 1.8G 7.9/10.0 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | CAT02 | 1.9G 7.9/10.0 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| E_v1 | XYZScaling | 2.2G 7.9/10.4 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F2_v1 | Bradford | 9.5GY 7.9/10.8 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F2_v1 | VonKries | 8.8GY 7.9/10.4 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F2_v1 | CAT02 | 9.4GY 8.0/10.9 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F11_v1 | Bradford | 8.6GY 7.9/10.4 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |
| F11_v1 | VonKries | 7.9GY 7.9/10.1 | brilliant yellowish green | ✅ | brilliant yellow green | ❌ |
| F11_v1 | CAT02 | 8.4GY 8.0/10.6 | brilliant yellowish green | ✅ | brilliant yellowish green | ✅ |

#### 128. #39964A - Expected: strong yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.5G 5.4/10.2 | strong green | ❌ | strong yellowish green | ✅ |
| C_v1 | VonKries | 2.6G 5.4/10.4 | strong green | ❌ | strong yellowish green | ✅ |
| C_v1 | CAT02 | 2.5G 5.4/10.2 | strong green | ❌ | strong yellowish green | ✅ |
| C_v1 | XYZScaling | 2.6G 5.4/10.4 | strong green | ❌ | strong yellowish green | ✅ |
| D50_v1 | Bradford | 0.2G 5.4/10.0 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | VonKries | 0.1G 5.4/9.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | CAT02 | 0.1G 5.4/10.0 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D50_v1 | XYZScaling | 0.3G 5.4/10.3 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | Bradford | 0.8G 5.4/10.2 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | VonKries | 0.5G 5.4/9.9 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | CAT02 | 0.7G 5.4/10.2 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D55_v1 | XYZScaling | 1.1G 5.4/10.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| D65_v1 | Bradford | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| D65_v1 | VonKries | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| D65_v1 | CAT02 | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| E_v1 | Bradford | 0.7G 5.4/9.3 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| E_v1 | VonKries | 0.6G 5.4/9.3 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| E_v1 | CAT02 | 0.6G 5.4/9.3 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| E_v1 | XYZScaling | 0.9G 5.4/9.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | Bradford | 9.6GY 5.4/10.0 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | VonKries | 9.3GY 5.4/9.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | CAT02 | 9.4GY 5.4/10.1 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F2_v1 | XYZScaling | 9.6GY 5.4/10.5 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F7_v1 | Bradford | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| F7_v1 | VonKries | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| F7_v1 | CAT02 | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.3G 5.4/10.9 | strong green | ❌ | strong yellowish green | ✅ |
| F11_v1 | Bradford | 9.3GY 5.4/9.8 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | VonKries | 9.0GY 5.4/9.6 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | CAT02 | 9.1GY 5.4/10.0 | strong yellowish green | ✅ | strong yellowish green | ✅ |
| F11_v1 | XYZScaling | 9.5GY 5.4/10.5 | strong yellowish green | ✅ | strong yellowish green | ✅ |

#### 129. #176A1E - Expected: deep yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 10.0GY 3.8/8.7 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| C_v1 | VonKries | 0.1G 3.8/8.8 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| C_v1 | CAT02 | 0.0G 3.8/8.6 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| C_v1 | XYZScaling | 0.1G 3.8/8.8 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | Bradford | 8.5GY 3.8/8.9 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | VonKries | 8.2GY 3.8/8.6 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | CAT02 | 8.4GY 3.8/8.9 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D50_v1 | XYZScaling | 8.9GY 3.8/9.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | Bradford | 9.1GY 3.8/9.0 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | VonKries | 8.9GY 3.8/8.8 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | CAT02 | 9.0GY 3.8/9.0 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D55_v1 | XYZScaling | 9.3GY 3.8/9.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D65_v1 | Bradford | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D65_v1 | VonKries | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D65_v1 | CAT02 | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D65_v1 | XYZScaling | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D75_v1 | Bradford | 0.7G 3.8/9.5 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D75_v1 | VonKries | 0.9G 3.8/9.7 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D75_v1 | CAT02 | 0.8G 3.8/9.5 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| D75_v1 | XYZScaling | 0.6G 3.8/9.2 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | Bradford | 8.7GY 3.8/8.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | VonKries | 8.5GY 3.8/8.2 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | CAT02 | 8.6GY 3.8/8.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| E_v1 | XYZScaling | 9.2GY 3.8/8.8 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F2_v1 | XYZScaling | 8.1GY 3.8/9.3 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F7_v1 | Bradford | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F7_v1 | VonKries | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F7_v1 | CAT02 | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |
| F7_v1 | XYZScaling | 0.0G 3.8/9.1 | deep yellowish green | ✅ | deep yellowish green | ✅ |

#### 130. #054208 - Expected: very deep yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.9GY 2.3/7.2 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| C_v1 | VonKries | 9.1GY 2.3/7.3 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| C_v1 | CAT02 | 9.0GY 2.3/7.2 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| C_v1 | XYZScaling | 9.0GY 2.3/7.3 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D50_v1 | XYZScaling | 8.3GY 2.3/7.6 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D55_v1 | Bradford | 8.4GY 2.3/7.3 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D55_v1 | VonKries | 8.1GY 2.3/7.2 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D55_v1 | CAT02 | 8.3GY 2.3/7.3 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D55_v1 | XYZScaling | 8.6GY 2.3/7.6 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D65_v1 | Bradford | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D65_v1 | VonKries | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D65_v1 | CAT02 | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D65_v1 | XYZScaling | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D75_v1 | Bradford | 9.6GY 2.3/7.7 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D75_v1 | VonKries | 9.8GY 2.3/7.8 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D75_v1 | CAT02 | 9.7GY 2.3/7.6 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| D75_v1 | XYZScaling | 9.4GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| E_v1 | XYZScaling | 8.4GY 2.3/7.2 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| F7_v1 | Bradford | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| F7_v1 | VonKries | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| F7_v1 | CAT02 | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |
| F7_v1 | XYZScaling | 9.1GY 2.3/7.5 | very deep yellowish green | ✅ | very deep yellowish green | ✅ |

#### 131. #C5EDC4 - Expected: very light yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.0G 9.0/3.9 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| C_v1 | VonKries | 2.2G 9.0/4.0 | very light green | ❌ | very light yellowish green | ✅ |
| C_v1 | CAT02 | 2.0G 9.0/3.9 | very light green | ❌ | very light yellowish green | ✅ |
| C_v1 | XYZScaling | 2.1G 9.0/4.0 | very light green | ❌ | very light yellowish green | ✅ |
| D50_v1 | Bradford | 9.4GY 9.0/6.4 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| D50_v1 | VonKries | 9.0GY 9.0/6.2 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| D50_v1 | CAT02 | 9.4GY 9.0/6.4 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| D50_v1 | XYZScaling | 9.9GY 9.0/6.6 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| D55_v1 | Bradford | 2.3G 9.0/6.8 | very light green | ❌ | very light yellowish green | ✅ |
| D55_v1 | VonKries | 1.6G 9.0/6.4 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| D55_v1 | CAT02 | 2.1G 9.0/6.8 | very light green | ❌ | very light yellowish green | ✅ |
| D65_v1 | Bradford | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| D65_v1 | VonKries | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| D65_v1 | CAT02 | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.2G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| E_v1 | Bradford | 9.9GY 9.0/4.7 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| E_v1 | VonKries | 9.7GY 9.0/4.6 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| E_v1 | CAT02 | 9.8GY 9.0/4.7 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| E_v1 | XYZScaling | 0.5G 9.0/5.0 | very light yellowish green | ✅ | very light yellowish green | ✅ |
| F7_v1 | Bradford | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| F7_v1 | VonKries | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| F7_v1 | CAT02 | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.1G 9.0/5.1 | very light green | ❌ | very light yellowish green | ✅ |

#### 132. #9CC69C - Expected: light yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 0.0G 7.5/7.0 | light yellowish green | ✅ | light yellowish green | ✅ |
| D50_v1 | VonKries | 9.6GY 7.5/6.8 | light yellowish green | ✅ | light yellowish green | ✅ |
| D55_v1 | VonKries | 1.5G 7.5/6.9 | light yellowish green | ✅ | light yellowish green | ✅ |
| E_v1 | Bradford | 0.6G 7.5/5.4 | light yellowish green | ✅ | light yellowish green | ✅ |
| E_v1 | VonKries | 0.4G 7.5/5.4 | light yellowish green | ✅ | light yellowish green | ✅ |
| E_v1 | CAT02 | 0.5G 7.5/5.4 | light yellowish green | ✅ | light yellowish green | ✅ |
| E_v1 | XYZScaling | 1.1G 7.5/5.8 | light yellowish green | ✅ | light yellowish green | ✅ |

#### 133. #669069 - Expected: moderate yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 0.3G 5.5/6.5 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D50_v1 | VonKries | 0.1G 5.5/6.4 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D50_v1 | CAT02 | 0.2G 5.5/6.6 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D50_v1 | XYZScaling | 0.5G 5.5/6.7 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | Bradford | 1.1G 5.5/6.4 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | VonKries | 1.0G 5.5/6.3 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | CAT02 | 1.1G 5.5/6.4 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D55_v1 | XYZScaling | 1.2G 5.5/6.5 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D65_v1 | Bradford | 2.8G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D65_v1 | VonKries | 2.8G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D65_v1 | CAT02 | 2.8G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.8G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | Bradford | 0.8G 5.5/5.4 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | VonKries | 0.7G 5.5/5.4 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | CAT02 | 0.7G 5.5/5.4 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| E_v1 | XYZScaling | 1.0G 5.5/5.6 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F2_v1 | Bradford | 8.0GY 5.5/6.5 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F2_v1 | VonKries | 7.4GY 5.5/6.3 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F2_v1 | CAT02 | 7.9GY 5.5/6.6 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F2_v1 | XYZScaling | 8.7GY 5.5/6.9 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F7_v1 | Bradford | 2.7G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F7_v1 | VonKries | 2.7G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F7_v1 | CAT02 | 2.7G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.7G 5.5/6.1 | moderate yellowish green | ✅ | moderate yellowish green | ✅ |
| F11_v1 | Bradford | 7.1GY 5.5/6.4 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F11_v1 | CAT02 | 7.1GY 5.5/6.5 | moderate yellowish green | ✅ | moderate yellow green | ❌ |
| F11_v1 | XYZScaling | 8.0GY 5.5/6.8 | moderate yellowish green | ✅ | moderate yellow green | ❌ |

#### 134. #2F5D3A - Expected: dark yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.7G 3.5/5.5 | dark green | ❌ | dark yellowish green | ✅ |
| C_v1 | VonKries | 2.8G 3.5/5.6 | dark green | ❌ | dark yellowish green | ✅ |
| C_v1 | CAT02 | 2.7G 3.5/5.5 | dark green | ❌ | dark yellowish green | ✅ |
| C_v1 | XYZScaling | 2.8G 3.5/5.6 | dark green | ❌ | dark yellowish green | ✅ |
| D50_v1 | Bradford | 9.7GY 3.5/5.8 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | VonKries | 9.5GY 3.5/5.7 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | CAT02 | 9.6GY 3.5/5.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D50_v1 | XYZScaling | 9.7GY 3.5/5.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | Bradford | 0.4G 3.5/5.8 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | VonKries | 0.1G 3.5/5.6 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | CAT02 | 0.3G 3.5/5.8 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D55_v1 | XYZScaling | 0.6G 3.5/6.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| D65_v1 | Bradford | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| D65_v1 | VonKries | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| D65_v1 | CAT02 | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| D65_v1 | XYZScaling | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| E_v1 | Bradford | 0.0G 3.5/5.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | VonKries | 10.0GY 3.5/5.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | CAT02 | 0.0G 3.5/5.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| E_v1 | XYZScaling | 0.4G 3.5/5.3 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | Bradford | 8.6GY 3.5/6.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | VonKries | 8.4GY 3.5/5.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | CAT02 | 8.5GY 3.5/6.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F2_v1 | XYZScaling | 8.8GY 3.5/6.2 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F7_v1 | Bradford | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| F7_v1 | VonKries | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| F7_v1 | CAT02 | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| F7_v1 | XYZScaling | 2.4G 3.5/6.1 | dark green | ❌ | dark yellowish green | ✅ |
| F11_v1 | Bradford | 8.3GY 3.5/5.9 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F11_v1 | VonKries | 7.9GY 3.5/5.8 | dark yellowish green | ✅ | moderate olive green | ❌ |
| F11_v1 | CAT02 | 8.2GY 3.5/6.0 | dark yellowish green | ✅ | dark yellowish green | ✅ |
| F11_v1 | XYZScaling | 8.6GY 3.5/6.2 | dark yellowish green | ✅ | dark yellowish green | ✅ |

#### 135. #10361A - Expected: very dark yellowish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.9G 1.9/4.8 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| C_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| C_v1 | VonKries | 1.0G 1.9/4.9 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| C_v2 | VonKries | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| C_v1 | CAT02 | 0.9G 1.9/4.8 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| C_v2 | CAT02 | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| C_v1 | XYZScaling | 1.0G 1.9/4.9 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| C_v2 | XYZScaling | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D50_v1 | Bradford | 8.5GY 1.9/5.0 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D50_v1 | VonKries | 8.1GY 1.9/4.8 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D50_v1 | CAT02 | 8.4GY 1.9/5.0 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D50_v1 | XYZScaling | 8.9GY 1.9/5.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | Bradford | 9.4GY 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | VonKries | 9.1GY 1.9/5.0 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | CAT02 | 9.3GY 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D55_v1 | XYZScaling | 9.6GY 1.9/5.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v1 | Bradford | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v1 | VonKries | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v1 | CAT02 | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D65_v1 | XYZScaling | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D75_v1 | Bradford | 1.8G 1.9/5.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D75_v2 | Bradford | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v1 | VonKries | 1.9G 1.9/5.3 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D75_v2 | VonKries | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v1 | CAT02 | 1.8G 1.9/5.2 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D75_v2 | CAT02 | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| D75_v1 | XYZScaling | 1.7G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| D75_v2 | XYZScaling | 10.0GY 1.9/2.0 | blackish green | ❌ | very dark yellowish green | ✅ |
| E_v1 | Bradford | 9.0GY 1.9/4.5 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v1 | VonKries | 8.8GY 1.9/4.5 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v1 | CAT02 | 8.8GY 1.9/4.5 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| E_v1 | XYZScaling | 9.4GY 1.9/4.8 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v1 | Bradford | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v1 | VonKries | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v1 | CAT02 | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |
| F7_v1 | XYZScaling | 0.8G 1.9/5.1 | very dark yellowish green | ✅ | very dark yellowish green | ✅ |

#### 136. #23EAA5 - Expected: vivid green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 6.7G 8.2/15.5 | vivid green | ✅ | vivid green | ✅ |
| D50_v1 | VonKries | 5.7G 8.2/14.9 | vivid green | ✅ | vivid green | ✅ |
| D50_v1 | CAT02 | 6.2G 8.2/15.5 | vivid green | ✅ | vivid green | ✅ |
| D50_v1 | XYZScaling | 6.8G 8.2/16.0 | vivid green | ✅ | vivid green | ✅ |
| F2_v1 | Bradford | 3.1G 8.2/13.8 | vivid green | ✅ | vivid green | ✅ |
| F2_v1 | VonKries | 2.6G 8.2/13.3 | vivid green | ✅ | vivid yellowish green | ❌ |
| F2_v1 | CAT02 | 2.8G 8.2/13.8 | vivid green | ✅ | vivid yellowish green | ❌ |
| F2_v1 | XYZScaling | 3.3G 8.2/14.7 | vivid green | ✅ | vivid green | ✅ |
| F11_v1 | Bradford | 2.5G 8.2/13.3 | vivid green | ✅ | vivid yellowish green | ❌ |
| F11_v1 | VonKries | 2.1G 8.2/12.8 | vivid green | ✅ | vivid yellowish green | ❌ |
| F11_v1 | CAT02 | 2.3G 8.2/13.3 | vivid green | ✅ | vivid yellowish green | ❌ |
| F11_v1 | XYZScaling | 2.7G 8.2/14.2 | vivid green | ✅ | vivid yellowish green | ❌ |

#### 137. #49D0A3 - Expected: brilliant green

No matches

#### 138. #158A66 - Expected: strong green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 4.8G 5.0/9.4 | strong green | ✅ | strong green | ✅ |
| D50_v1 | VonKries | 4.5G 5.0/9.1 | strong green | ✅ | strong green | ✅ |
| D50_v1 | CAT02 | 4.7G 5.0/9.4 | strong green | ✅ | strong green | ✅ |
| D50_v1 | XYZScaling | 4.8G 5.0/9.6 | strong green | ✅ | strong green | ✅ |
| D55_v1 | Bradford | 8.6G 5.0/9.9 | strong bluish green | ❌ | strong green | ✅ |
| D55_v1 | VonKries | 8.0G 5.0/9.7 | strong bluish green | ❌ | strong green | ✅ |
| D55_v1 | CAT02 | 8.3G 5.0/9.9 | strong bluish green | ❌ | strong green | ✅ |
| D55_v1 | XYZScaling | 8.5G 5.0/10.0 | strong bluish green | ❌ | strong green | ✅ |
| E_v1 | VonKries | 8.8G 5.0/8.4 | strong bluish green | ❌ | strong green | ✅ |
| F2_v1 | Bradford | 2.0G 5.0/8.6 | strong green | ✅ | strong yellowish green | ❌ |
| F2_v1 | XYZScaling | 2.2G 5.0/9.1 | strong green | ✅ | strong yellowish green | ❌ |

#### 139. #A6E2CA - Expected: very light green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 3.5G 8.5/6.8 | very light green | ✅ | very light green | ✅ |
| D50_v1 | VonKries | 3.3G 8.5/6.7 | very light green | ✅ | very light green | ✅ |
| D50_v1 | CAT02 | 3.4G 8.5/6.8 | very light green | ✅ | very light green | ✅ |
| D50_v1 | XYZScaling | 3.5G 8.5/6.9 | very light green | ✅ | very light green | ✅ |
| D55_v1 | Bradford | 5.5G 8.5/6.3 | very light green | ✅ | very light green | ✅ |
| D55_v1 | VonKries | 5.7G 8.5/6.3 | very light green | ✅ | very light green | ✅ |
| D55_v1 | CAT02 | 5.7G 8.5/6.3 | very light green | ✅ | very light green | ✅ |
| D55_v1 | XYZScaling | 5.7G 8.5/6.3 | very light green | ✅ | very light green | ✅ |
| E_v1 | Bradford | 2.9G 8.5/4.1 | very light green | ✅ | light yellowish green | ❌ |
| E_v1 | VonKries | 2.6G 8.5/4.1 | very light green | ✅ | very light yellowish green | ❌ |
| E_v1 | CAT02 | 2.7G 8.5/4.1 | very light green | ✅ | light yellowish green | ❌ |
| E_v1 | XYZScaling | 3.4G 8.5/4.4 | very light green | ✅ | very light green | ✅ |

#### 140. #6FAC95 - Expected: light green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 3.1G 6.5/6.5 | light green | ✅ | light green | ✅ |
| D50_v1 | VonKries | 3.0G 6.5/6.4 | light green | ✅ | moderate yellowish green | ❌ |
| D50_v1 | CAT02 | 3.1G 6.5/6.5 | light green | ✅ | light green | ✅ |
| D50_v1 | XYZScaling | 3.1G 6.5/6.6 | light green | ✅ | light green | ✅ |
| D55_v1 | Bradford | 6.9G 6.5/6.6 | light green | ✅ | light green | ✅ |
| D55_v1 | VonKries | 6.5G 6.5/6.5 | light green | ✅ | light green | ✅ |
| D55_v1 | CAT02 | 6.8G 6.5/6.7 | light green | ✅ | light green | ✅ |
| D55_v1 | XYZScaling | 6.8G 6.5/6.7 | light green | ✅ | light green | ✅ |
| E_v1 | Bradford | 7.9G 6.5/5.1 | light green | ✅ | light green | ✅ |
| E_v1 | VonKries | 7.2G 6.5/5.1 | light green | ✅ | light green | ✅ |
| E_v1 | CAT02 | 7.5G 6.5/5.1 | light green | ✅ | light green | ✅ |
| E_v1 | XYZScaling | 8.3G 6.5/5.4 | light green | ✅ | light green | ✅ |

#### 141. #337762 - Expected: moderate green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 4.4G 4.4/6.3 | moderate green | ✅ | moderate green | ✅ |
| D50_v1 | VonKries | 4.0G 4.4/6.2 | moderate green | ✅ | moderate green | ✅ |
| D50_v1 | CAT02 | 4.2G 4.4/6.3 | moderate green | ✅ | moderate green | ✅ |
| D50_v1 | XYZScaling | 4.3G 4.4/6.4 | moderate green | ✅ | moderate green | ✅ |
| D55_v1 | Bradford | 8.5G 4.4/6.5 | moderate bluish green | ❌ | moderate green | ✅ |
| D55_v1 | VonKries | 7.9G 4.4/6.4 | moderate green | ✅ | moderate green | ✅ |
| D55_v1 | CAT02 | 8.3G 4.4/6.5 | moderate bluish green | ❌ | moderate green | ✅ |
| D55_v1 | XYZScaling | 8.3G 4.4/6.6 | moderate bluish green | ❌ | moderate green | ✅ |

#### 142. #164E3D - Expected: dark green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 3.4G 2.9/5.4 | dark green | ✅ | dark green | ✅ |
| D50_v1 | VonKries | 3.1G 2.9/5.3 | dark green | ✅ | dark green | ✅ |
| D50_v1 | CAT02 | 3.3G 2.9/5.5 | dark green | ✅ | dark green | ✅ |
| D50_v1 | XYZScaling | 3.3G 2.9/5.5 | dark green | ✅ | dark green | ✅ |
| D55_v1 | Bradford | 5.8G 2.9/5.5 | dark green | ✅ | dark green | ✅ |
| D55_v1 | VonKries | 5.3G 2.9/5.4 | dark green | ✅ | dark green | ✅ |
| D55_v1 | CAT02 | 5.6G 2.9/5.5 | dark green | ✅ | dark green | ✅ |
| D55_v1 | XYZScaling | 5.7G 2.9/5.6 | dark green | ✅ | dark green | ✅ |
| E_v1 | Bradford | 7.6G 2.9/4.8 | dark green | ✅ | dark green | ✅ |
| E_v1 | VonKries | 6.8G 2.9/4.7 | dark green | ✅ | dark green | ✅ |
| E_v1 | CAT02 | 7.2G 2.9/4.8 | dark green | ✅ | dark green | ✅ |
| E_v1 | XYZScaling | 7.8G 2.9/5.0 | dark green | ✅ | dark green | ✅ |

#### 143. #0C2E24 - Expected: very dark green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| C_v2 | VonKries | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| C_v2 | CAT02 | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| C_v2 | XYZScaling | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D50_v1 | Bradford | 2.0G 1.6/3.4 | very dark green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | Bradford | 3.9G 1.6/3.4 | very dark green | ✅ | very dark green | ✅ |
| D55_v1 | VonKries | 3.7G 1.6/3.4 | very dark green | ✅ | very dark green | ✅ |
| D55_v1 | CAT02 | 3.8G 1.6/3.4 | very dark green | ✅ | very dark green | ✅ |
| D55_v1 | XYZScaling | 3.8G 1.6/3.4 | very dark green | ✅ | very dark green | ✅ |
| D65_v2 | Bradford | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D65_v2 | VonKries | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D65_v2 | CAT02 | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D65_v2 | XYZScaling | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | Bradford | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | VonKries | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | CAT02 | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| D75_v2 | XYZScaling | 7.5G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| E_v1 | Bradford | 4.3G 1.6/3.0 | very dark green | ✅ | very dark green | ✅ |
| E_v2 | Bradford | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| E_v1 | VonKries | 4.1G 1.6/3.0 | very dark green | ✅ | very dark green | ✅ |
| E_v1 | CAT02 | 4.2G 1.6/3.0 | very dark green | ✅ | very dark green | ✅ |
| E_v1 | XYZScaling | 4.4G 1.6/3.1 | very dark green | ✅ | very dark green | ✅ |
| F7_v2 | Bradford | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | VonKries | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | CAT02 | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |
| F7_v2 | XYZScaling | 5.0G 1.6/2.0 | blackish green | ❌ | very dark green | ✅ |

#### 144. #C7D9D6 - Expected: very pale green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | VonKries | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | CAT02 | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| C_v2 | XYZScaling | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | Bradford | 10.0GY 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | VonKries | 10.0GY 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | CAT02 | 10.0GY 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D50_v2 | XYZScaling | 10.0GY 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | Bradford | 2.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | VonKries | 2.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | CAT02 | 2.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D55_v2 | XYZScaling | 2.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v1 | Bradford | 7.4BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | Bradford | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v1 | VonKries | 7.4BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | VonKries | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v1 | CAT02 | 7.4BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | CAT02 | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D65_v1 | XYZScaling | 7.4BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| D65_v2 | XYZScaling | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | Bradford | 10.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | VonKries | 10.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | CAT02 | 10.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| D75_v2 | XYZScaling | 10.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | Bradford | 5.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | VonKries | 5.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v1 | CAT02 | 9.6GY 8.5/1.6 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | CAT02 | 5.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| E_v2 | XYZScaling | 5.0G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| F2_v2 | Bradford | 7.5GY 8.5/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F2_v2 | VonKries | 7.5GY 8.5/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F2_v2 | CAT02 | 7.5GY 8.5/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F2_v2 | XYZScaling | 7.5GY 8.5/2.0 | very pale green | ✅ | pale yellow green | ❌ |
| F7_v1 | Bradford | 7.1BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | Bradford | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| F7_v1 | VonKries | 7.1BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | VonKries | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| F7_v1 | CAT02 | 7.1BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | CAT02 | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |
| F7_v1 | XYZScaling | 7.1BG 8.5/1.9 | very pale green | ✅ | very pale green | ✅ |
| F7_v2 | XYZScaling | 7.5G 8.5/2.0 | very pale green | ✅ | very pale green | ✅ |

#### 145. #94A6A3 - Expected: pale green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| C_v2 | VonKries | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| C_v2 | CAT02 | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| C_v2 | XYZScaling | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | Bradford | 2.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | VonKries | 2.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | CAT02 | 2.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D50_v2 | XYZScaling | 2.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | Bradford | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | VonKries | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | CAT02 | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D55_v2 | XYZScaling | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v1 | Bradford | 7.1BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| D65_v2 | Bradford | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v1 | VonKries | 7.1BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| D65_v2 | VonKries | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v1 | CAT02 | 7.1BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| D65_v2 | CAT02 | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D65_v1 | XYZScaling | 7.1BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| D65_v2 | XYZScaling | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | Bradford | 10.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | VonKries | 10.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | CAT02 | 10.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| D75_v2 | XYZScaling | 10.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | Bradford | 8.4GY 6.6/1.3 | pale green | ✅ | pale green | ✅ |
| E_v2 | Bradford | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | VonKries | 8.3GY 6.6/1.3 | pale green | ✅ | pale green | ✅ |
| E_v2 | VonKries | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | CAT02 | 8.3GY 6.6/1.3 | pale green | ✅ | pale green | ✅ |
| E_v2 | CAT02 | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| E_v1 | XYZScaling | 8.7GY 6.6/1.4 | pale green | ✅ | pale green | ✅ |
| E_v2 | XYZScaling | 5.0G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | Bradford | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | VonKries | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | CAT02 | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F2_v2 | XYZScaling | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v1 | Bradford | 6.9BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| F7_v2 | Bradford | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v1 | VonKries | 6.9BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| F7_v2 | VonKries | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v1 | CAT02 | 6.9BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| F7_v2 | CAT02 | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F7_v1 | XYZScaling | 6.9BG 6.6/1.8 | pale green | ✅ | pale green | ✅ |
| F7_v2 | XYZScaling | 7.5G 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | Bradford | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | VonKries | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | CAT02 | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |
| F11_v2 | XYZScaling | 10.0GY 6.6/2.0 | pale green | ✅ | pale green | ✅ |

#### 146. #61716E - Expected: grayish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| C_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | Bradford | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | VonKries | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | CAT02 | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D50_v2 | XYZScaling | 2.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v1 | Bradford | 1.0G 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | Bradford | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v1 | VonKries | 1.0G 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | VonKries | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v1 | CAT02 | 1.0G 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | CAT02 | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D55_v1 | XYZScaling | 1.0G 4.5/2.3 | grayish green | ✅ | grayish green | ✅ |
| D55_v2 | XYZScaling | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | Bradford | 6.3BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | VonKries | 6.3BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | CAT02 | 6.3BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D65_v1 | XYZScaling | 6.3BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| D65_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | Bradford | 10.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | VonKries | 10.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | CAT02 | 10.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| D75_v2 | XYZScaling | 10.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | Bradford | 0.1G 4.5/1.3 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | Bradford | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | VonKries | 10.0GY 4.5/1.3 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | VonKries | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | CAT02 | 0.0G 4.5/1.3 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | CAT02 | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| E_v1 | XYZScaling | 0.3G 4.5/1.4 | grayish green | ✅ | grayish green | ✅ |
| E_v2 | XYZScaling | 5.0G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | Bradford | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | VonKries | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | CAT02 | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F2_v2 | XYZScaling | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | Bradford | 6.1BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | Bradford | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | VonKries | 6.1BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | VonKries | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | CAT02 | 6.1BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | CAT02 | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F7_v1 | XYZScaling | 6.1BG 4.5/1.6 | grayish green | ✅ | grayish green | ✅ |
| F7_v2 | XYZScaling | 7.5G 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | Bradford | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | VonKries | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | CAT02 | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |
| F11_v2 | XYZScaling | 10.0GY 4.5/2.0 | grayish green | ✅ | grayish green | ✅ |

#### 147. #394746 - Expected: dark grayish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v2 | VonKries | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v2 | CAT02 | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| C_v2 | XYZScaling | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v1 | Bradford | 9.3GY 2.9/2.2 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | Bradford | 2.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v1 | VonKries | 9.2GY 2.9/2.2 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | VonKries | 2.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v1 | CAT02 | 9.3GY 2.9/2.2 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | CAT02 | 2.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v1 | XYZScaling | 9.1GY 2.9/2.2 | dark grayish green | ✅ | dark grayish green | ✅ |
| D50_v2 | XYZScaling | 2.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | Bradford | 2.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | Bradford | 5.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | VonKries | 1.9G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | VonKries | 5.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | CAT02 | 2.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | CAT02 | 5.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v1 | XYZScaling | 1.8G 2.9/1.9 | dark grayish green | ✅ | dark grayish green | ✅ |
| D55_v2 | XYZScaling | 5.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | Bradford | 7.4BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | Bradford | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | VonKries | 7.4BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | VonKries | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | CAT02 | 7.4BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | CAT02 | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v1 | XYZScaling | 7.4BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| D65_v2 | XYZScaling | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v1 | Bradford | 7.9BG 2.9/1.7 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | Bradford | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v1 | VonKries | 7.9BG 2.9/1.7 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | VonKries | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v1 | CAT02 | 7.9BG 2.9/1.7 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | CAT02 | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v1 | XYZScaling | 7.9BG 2.9/1.7 | dark grayish green | ✅ | dark grayish green | ✅ |
| D75_v2 | XYZScaling | 10.0G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | Bradford | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | VonKries | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | CAT02 | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| E_v2 | XYZScaling | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | Bradford | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | VonKries | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | CAT02 | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F2_v2 | XYZScaling | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | Bradford | 7.2BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | Bradford | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | VonKries | 7.2BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | VonKries | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | CAT02 | 7.2BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | CAT02 | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v1 | XYZScaling | 7.2BG 2.9/1.3 | dark grayish green | ✅ | dark grayish green | ✅ |
| F7_v2 | XYZScaling | 7.5G 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | Bradford | 10.0GY 2.8/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | VonKries | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | CAT02 | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |
| F11_v2 | XYZScaling | 10.0GY 2.9/2.0 | dark grayish green | ✅ | dark grayish green | ✅ |

#### 148. #1F2A2A - Expected: blackish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.1BG 1.6/1.1 | blackish green | ✅ | blackish green | ✅ |
| C_v2 | Bradford | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| C_v1 | VonKries | 6.1BG 1.6/1.1 | blackish green | ✅ | blackish green | ✅ |
| C_v2 | VonKries | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| C_v1 | CAT02 | 6.1BG 1.6/1.1 | blackish green | ✅ | blackish green | ✅ |
| C_v2 | CAT02 | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| C_v1 | XYZScaling | 6.3BG 1.6/1.2 | blackish green | ✅ | blackish green | ✅ |
| C_v2 | XYZScaling | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D50_v1 | Bradford | 8.4GY 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D50_v2 | Bradford | 2.5G 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D50_v1 | VonKries | 8.3GY 1.6/1.7 | blackish green | ✅ | blackish green | ✅ |
| D50_v2 | VonKries | 2.5G 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D50_v1 | CAT02 | 8.4GY 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D50_v2 | CAT02 | 2.5G 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D50_v1 | XYZScaling | 8.2GY 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D50_v2 | XYZScaling | 2.5G 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| D55_v1 | Bradford | 2.7G 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | Bradford | 5.0G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D55_v1 | VonKries | 2.6G 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | VonKries | 5.0G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D55_v1 | CAT02 | 2.7G 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | CAT02 | 5.0G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D55_v1 | XYZScaling | 2.3G 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D55_v2 | XYZScaling | 5.0G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | Bradford | 8.6BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | Bradford | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | VonKries | 8.6BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | VonKries | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | CAT02 | 8.6BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | CAT02 | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D65_v1 | XYZScaling | 8.6BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| D65_v2 | XYZScaling | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| D75_v1 | Bradford | 5.9BG 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | Bradford | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D75_v1 | VonKries | 5.9BG 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | VonKries | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D75_v1 | CAT02 | 5.9BG 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | CAT02 | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| D75_v1 | XYZScaling | 5.9BG 1.6/1.6 | blackish green | ✅ | blackish green | ✅ |
| D75_v2 | XYZScaling | 10.0G 1.6/2.0 | blackish green | ✅ | very dark bluish green | ❌ |
| E_v2 | Bradford | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| E_v2 | VonKries | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| E_v2 | CAT02 | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| E_v2 | XYZScaling | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| F2_v2 | Bradford | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F2_v2 | VonKries | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F2_v2 | CAT02 | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F2_v2 | XYZScaling | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F7_v1 | Bradford | 8.4BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | Bradford | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| F7_v1 | VonKries | 8.4BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | VonKries | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| F7_v1 | CAT02 | 8.4BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | CAT02 | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| F7_v1 | XYZScaling | 8.4BG 1.6/1.0 | blackish green | ✅ | blackish green | ✅ |
| F7_v2 | XYZScaling | 7.5G 1.6/2.0 | blackish green | ✅ | very dark green | ❌ |
| F11_v2 | Bradford | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F11_v2 | VonKries | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F11_v2 | CAT02 | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |
| F11_v2 | XYZScaling | 10.0GY 1.6/2.0 | blackish green | ✅ | very dark yellowish green | ❌ |

#### 149. #E0E2E5 - Expected: greenish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 3.9G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| D65_v1 | VonKries | 3.9G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| D65_v1 | CAT02 | 3.9G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| D65_v1 | XYZScaling | 3.9G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| F7_v1 | Bradford | 3.4G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| F7_v1 | VonKries | 3.4G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| F7_v1 | CAT02 | 3.4G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |
| F7_v1 | XYZScaling | 3.4G 9.0/0.9 | greenish white | ✅ | greenish white | ✅ |

#### 150. #BABEC1 - Expected: light greenish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 1.5BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| D65_v1 | VonKries | 1.5BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| D65_v1 | CAT02 | 1.5BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| D65_v1 | XYZScaling | 1.5BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| F7_v1 | Bradford | 0.3BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| F7_v1 | VonKries | 0.3BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| F7_v1 | CAT02 | 0.4BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |
| F7_v1 | XYZScaling | 0.3BG 7.6/1.0 | light greenish gray | ✅ | light greenish gray | ✅ |

#### 151. #848888 - Expected: greenish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 4.9G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| D65_v1 | VonKries | 4.9G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| D65_v1 | CAT02 | 4.9G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| D65_v1 | XYZScaling | 4.9G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| D75_v1 | Bradford | 8.6BG 5.5/1.1 | greenish gray | ✅ | greenish gray | ✅ |
| D75_v1 | VonKries | 8.6BG 5.5/1.1 | greenish gray | ✅ | greenish gray | ✅ |
| D75_v1 | CAT02 | 8.6BG 5.5/1.1 | greenish gray | ✅ | greenish gray | ✅ |
| D75_v1 | XYZScaling | 8.6BG 5.5/1.1 | greenish gray | ✅ | greenish gray | ✅ |
| F7_v1 | Bradford | 4.6G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| F7_v1 | VonKries | 4.6G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| F7_v1 | CAT02 | 4.6G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |
| F7_v1 | XYZScaling | 4.6G 5.5/1.0 | greenish gray | ✅ | greenish gray | ✅ |

#### 152. #545858 - Expected: dark greenish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 5.4G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D65_v1 | VonKries | 5.4G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D65_v1 | CAT02 | 5.4G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D65_v1 | XYZScaling | 5.4G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D75_v1 | Bradford | 7.4BG 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D75_v1 | VonKries | 7.4BG 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D75_v1 | CAT02 | 7.5BG 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| D75_v1 | XYZScaling | 7.5BG 3.6/1.0 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| F7_v1 | Bradford | 4.9G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| F7_v1 | VonKries | 4.9G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| F7_v1 | CAT02 | 4.9G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |
| F7_v1 | XYZScaling | 4.9G 3.6/0.9 | dark greenish gray | ✅ | dark greenish gray | ✅ |

#### 153. #212626 - Expected: greenish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0BG 1.4/0.6 | greenish black | ✅ | greenish black | ✅ |
| C_v1 | VonKries | 6.0BG 1.4/0.5 | greenish black | ✅ | greenish black | ✅ |
| C_v1 | CAT02 | 6.0BG 1.4/0.5 | greenish black | ✅ | greenish black | ✅ |
| C_v1 | XYZScaling | 6.1BG 1.4/0.6 | greenish black | ✅ | greenish black | ✅ |
| D65_v1 | Bradford | 2.8BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| D65_v1 | VonKries | 2.8BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| D65_v1 | CAT02 | 2.8BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| D65_v1 | XYZScaling | 2.8BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | Bradford | 5.7BG 1.4/1.0 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | VonKries | 5.7BG 1.4/1.0 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | CAT02 | 5.7BG 1.4/1.0 | greenish black | ✅ | greenish black | ✅ |
| D75_v1 | XYZScaling | 5.7BG 1.4/1.0 | greenish black | ✅ | greenish black | ✅ |
| F7_v1 | Bradford | 2.3BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| F7_v1 | VonKries | 2.3BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| F7_v1 | CAT02 | 2.3BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |
| F7_v1 | XYZScaling | 2.3BG 1.4/0.8 | greenish black | ✅ | greenish black | ✅ |

#### 154. #13FCD5 - Expected: vivid bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 5.5BG 8.9/12.7 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D50_v1 | VonKries | 5.2BG 8.9/12.7 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D50_v1 | CAT02 | 5.4BG 8.9/12.8 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D50_v1 | XYZScaling | 5.3BG 8.9/12.9 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D55_v1 | Bradford | 7.8BG 8.9/11.5 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D55_v1 | VonKries | 7.6BG 8.9/11.4 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D55_v1 | CAT02 | 7.7BG 8.9/11.5 | vivid bluish green | ✅ | vivid bluish green | ✅ |
| D55_v1 | XYZScaling | 7.6BG 8.9/11.5 | vivid bluish green | ✅ | vivid bluish green | ✅ |

#### 155. #35D7CE - Expected: brilliant bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 8.8BG 7.7/8.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D50_v1 | VonKries | 8.5BG 7.8/8.2 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D50_v1 | CAT02 | 8.7BG 7.7/8.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| D50_v1 | XYZScaling | 8.3BG 7.8/8.0 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| F2_v1 | Bradford | 1.5BG 7.7/10.2 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| F2_v1 | VonKries | 0.6BG 7.8/10.3 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| F2_v1 | CAT02 | 1.3BG 7.7/10.2 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |
| F2_v1 | XYZScaling | 0.1BG 7.8/10.1 | brilliant bluish green | ✅ | brilliant bluish green | ✅ |

#### 156. #0D8F82 - Expected: strong bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 5.3BG 5.2/7.5 | strong bluish green | ✅ | strong bluish green | ✅ |
| D50_v1 | VonKries | 5.0BG 5.2/7.5 | strong bluish green | ✅ | strong bluish green | ✅ |
| D50_v1 | CAT02 | 5.3BG 5.2/7.6 | strong bluish green | ✅ | strong bluish green | ✅ |
| D50_v1 | XYZScaling | 4.9BG 5.2/7.5 | strong bluish green | ✅ | strong bluish green | ✅ |

#### 157. #98E1E0 - Expected: very light bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 0.6BG 8.4/5.6 | very light bluish green | ✅ | very light bluish green | ✅ |
| D50_v1 | VonKries | 9.8G 8.5/5.7 | very light bluish green | ✅ | very light bluish green | ✅ |
| D50_v1 | CAT02 | 0.6BG 8.4/5.6 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | Bradford | 9.4BG 8.4/4.3 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | VonKries | 9.2BG 8.5/4.4 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | CAT02 | 9.4BG 8.4/4.3 | very light bluish green | ✅ | very light bluish green | ✅ |
| D55_v1 | XYZScaling | 9.1BG 8.5/4.3 | very light bluish green | ✅ | very light bluish green | ✅ |

#### 158. #5FABAB - Expected: light bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 10.0BG 6.4/4.7 | light bluish green | ✅ | light bluish green | ✅ |
| C_v1 | VonKries | 10.0BG 6.4/4.6 | light bluish green | ✅ | light bluish green | ✅ |
| C_v1 | CAT02 | 10.0BG 6.4/4.6 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | Bradford | 6.1BG 6.4/5.1 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | VonKries | 5.8BG 6.4/5.2 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | CAT02 | 6.1BG 6.4/5.1 | light bluish green | ✅ | light bluish green | ✅ |
| D50_v1 | XYZScaling | 5.5BG 6.4/5.0 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | Bradford | 9.8BG 6.4/4.2 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | VonKries | 9.7BG 6.4/4.3 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | CAT02 | 9.8BG 6.4/4.2 | light bluish green | ✅ | light bluish green | ✅ |
| D55_v1 | XYZScaling | 9.6BG 6.4/4.1 | light bluish green | ✅ | light bluish green | ✅ |
| D75_v1 | Bradford | 9.6BG 6.4/5.6 | light bluish green | ✅ | light bluish green | ✅ |
| D75_v1 | VonKries | 9.6BG 6.4/5.6 | light bluish green | ✅ | light bluish green | ✅ |
| D75_v1 | CAT02 | 9.6BG 6.4/5.6 | light bluish green | ✅ | light bluish green | ✅ |
| D75_v1 | XYZScaling | 9.6BG 6.4/5.7 | light bluish green | ✅ | light bluish green | ✅ |

#### 159. #297A7B - Expected: moderate bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.2BG 4.6/4.9 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| C_v1 | VonKries | 8.2BG 4.6/4.8 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| C_v1 | CAT02 | 8.2BG 4.6/4.9 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| C_v1 | XYZScaling | 8.3BG 4.6/5.0 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | Bradford | 7.5BG 4.6/4.4 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | VonKries | 7.3BG 4.6/4.5 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | CAT02 | 7.5BG 4.6/4.4 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D50_v1 | XYZScaling | 7.2BG 4.6/4.3 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | Bradford | 9.9BG 4.6/4.1 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | VonKries | 9.7BG 4.6/4.1 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | CAT02 | 9.9BG 4.6/4.1 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D55_v1 | XYZScaling | 9.7BG 4.6/4.0 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D65_v1 | Bradford | 9.8BG 4.6/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D65_v1 | VonKries | 9.8BG 4.6/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D65_v1 | CAT02 | 9.8BG 4.6/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D65_v1 | XYZScaling | 9.8BG 4.6/4.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | Bradford | 8.0BG 4.6/5.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | VonKries | 7.9BG 4.6/5.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | CAT02 | 8.0BG 4.6/5.6 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| D75_v1 | XYZScaling | 8.0BG 4.6/5.7 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| F2_v1 | Bradford | 8.1G 4.5/5.5 | moderate bluish green | ✅ | moderate green | ❌ |
| F2_v1 | CAT02 | 8.0G 4.5/5.4 | moderate bluish green | ✅ | moderate green | ❌ |
| F7_v1 | Bradford | 9.9BG 4.6/4.5 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| F7_v1 | VonKries | 9.9BG 4.6/4.5 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| F7_v1 | CAT02 | 9.9BG 4.6/4.5 | moderate bluish green | ✅ | moderate bluish green | ✅ |
| F7_v1 | XYZScaling | 9.9BG 4.6/4.5 | moderate bluish green | ✅ | moderate bluish green | ✅ |

#### 160. #154B4D - Expected: dark bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.9BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| C_v1 | VonKries | 6.9BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| C_v1 | CAT02 | 6.9BG 2.8/3.7 | dark bluish green | ✅ | dark bluish green | ✅ |
| C_v1 | XYZScaling | 6.7BG 2.8/3.8 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | Bradford | 6.4BG 2.8/3.2 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | VonKries | 6.2BG 2.8/3.3 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | CAT02 | 6.4BG 2.8/3.2 | dark bluish green | ✅ | dark bluish green | ✅ |
| D50_v1 | XYZScaling | 6.0BG 2.8/3.1 | dark bluish green | ✅ | dark bluish green | ✅ |
| D55_v1 | Bradford | 9.4BG 2.8/2.9 | dark grayish blue | ❌ | dark bluish green | ✅ |
| D55_v1 | VonKries | 9.3BG 2.8/2.9 | dark grayish blue | ❌ | dark bluish green | ✅ |
| D55_v1 | CAT02 | 9.4BG 2.8/2.9 | dark grayish blue | ❌ | dark bluish green | ✅ |
| D55_v1 | XYZScaling | 9.2BG 2.8/2.8 | dark grayish blue | ❌ | dark bluish green | ✅ |
| D65_v1 | Bradford | 8.2BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | VonKries | 8.2BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | CAT02 | 8.2BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| D65_v1 | XYZScaling | 8.2BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | Bradford | 6.9BG 2.8/4.2 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | VonKries | 7.0BG 2.8/4.2 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | CAT02 | 6.9BG 2.8/4.2 | dark bluish green | ✅ | dark bluish green | ✅ |
| D75_v1 | XYZScaling | 6.9BG 2.8/4.3 | dark bluish green | ✅ | dark bluish green | ✅ |
| E_v1 | Bradford | 9.2BG 2.8/2.6 | dark grayish blue | ❌ | dark bluish green | ✅ |
| E_v1 | VonKries | 9.4BG 2.8/2.6 | dark grayish blue | ❌ | dark bluish green | ✅ |
| E_v1 | CAT02 | 9.3BG 2.8/2.6 | dark grayish blue | ❌ | dark bluish green | ✅ |
| E_v1 | XYZScaling | 9.5BG 2.8/2.6 | dark grayish blue | ❌ | dark bluish green | ✅ |
| F7_v1 | Bradford | 8.3BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | VonKries | 8.3BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | CAT02 | 8.3BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |
| F7_v1 | XYZScaling | 8.3BG 2.8/3.5 | dark bluish green | ✅ | dark bluish green | ✅ |

#### 161. #0A2D2E - Expected: very dark bluish green

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.9BG 1.6/2.8 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | Bradford | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| C_v1 | VonKries | 5.9BG 1.6/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | VonKries | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| C_v1 | CAT02 | 5.9BG 1.6/2.8 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | CAT02 | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| C_v1 | XYZScaling | 5.8BG 1.6/2.8 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| C_v2 | XYZScaling | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D50_v1 | Bradford | 3.7BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D50_v1 | VonKries | 3.2BG 1.6/2.7 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D50_v1 | CAT02 | 3.7BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D50_v1 | XYZScaling | 2.7BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v1 | Bradford | 7.9BG 1.6/2.3 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v2 | Bradford | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D55_v1 | VonKries | 7.7BG 1.6/2.3 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v2 | VonKries | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D55_v1 | CAT02 | 7.9BG 1.6/2.3 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v2 | CAT02 | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D55_v1 | XYZScaling | 7.7BG 1.6/2.2 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D55_v2 | XYZScaling | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | Bradford | 7.3BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | Bradford | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | VonKries | 7.3BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | VonKries | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | CAT02 | 7.3BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | CAT02 | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D65_v1 | XYZScaling | 7.3BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D65_v2 | XYZScaling | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | Bradford | 6.0BG 1.6/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | Bradford | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | VonKries | 6.1BG 1.6/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | VonKries | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | CAT02 | 6.0BG 1.6/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | CAT02 | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| D75_v1 | XYZScaling | 6.0BG 1.6/3.1 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| D75_v2 | XYZScaling | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v2 | Bradford | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v2 | VonKries | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v2 | CAT02 | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| E_v2 | XYZScaling | 10.0G 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | Bradford | 7.4BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | Bradford | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | VonKries | 7.4BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | VonKries | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | CAT02 | 7.4BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | CAT02 | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |
| F7_v1 | XYZScaling | 7.4BG 1.6/2.6 | very dark bluish green | ✅ | very dark bluish green | ✅ |
| F7_v2 | XYZScaling | 2.5BG 1.6/2.0 | blackish green | ❌ | very dark bluish green | ✅ |

#### 162. #2DBCE2 - Expected: brilliant greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.9B 7.0/9.2 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| C_v1 | VonKries | 4.0B 7.0/9.2 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| C_v1 | CAT02 | 3.9B 7.0/9.2 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| C_v1 | XYZScaling | 3.7B 7.0/9.5 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D55_v1 | Bradford | 0.4B 7.0/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D55_v1 | VonKries | 0.1B 7.0/7.7 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D55_v1 | CAT02 | 0.4B 7.0/7.6 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D55_v1 | XYZScaling | 0.7B 7.0/7.1 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | Bradford | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | VonKries | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | CAT02 | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D65_v1 | XYZScaling | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | Bradford | 3.7B 7.0/10.0 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | VonKries | 3.8B 7.0/9.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | CAT02 | 3.7B 7.0/9.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| D75_v1 | XYZScaling | 3.4B 7.0/10.3 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| E_v1 | Bradford | 2.6B 7.0/7.4 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| E_v1 | VonKries | 2.4B 7.0/7.3 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| E_v1 | CAT02 | 2.6B 7.0/7.4 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| E_v1 | XYZScaling | 2.6B 7.0/7.2 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | Bradford | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | VonKries | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | CAT02 | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |
| F7_v1 | XYZScaling | 2.5B 7.0/8.9 | brilliant greenish blue | ✅ | brilliant greenish blue | ✅ |

#### 163. #1385AF - Expected: strong greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.3B 5.1/8.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| C_v1 | VonKries | 4.5B 5.1/8.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| C_v1 | CAT02 | 4.3B 5.1/8.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| C_v1 | XYZScaling | 4.1B 5.1/8.5 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D65_v1 | Bradford | 3.4B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D65_v1 | VonKries | 3.4B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D65_v1 | CAT02 | 3.4B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D65_v1 | XYZScaling | 3.4B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | Bradford | 4.1B 5.1/8.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | VonKries | 4.2B 5.1/8.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | CAT02 | 4.1B 5.1/8.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| D75_v1 | XYZScaling | 3.8B 5.1/9.3 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| F7_v1 | Bradford | 3.3B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| F7_v1 | VonKries | 3.3B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| F7_v1 | CAT02 | 3.3B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |
| F7_v1 | XYZScaling | 3.4B 5.1/7.9 | strong greenish blue | ✅ | strong greenish blue | ✅ |

#### 164. #94D6EF - Expected: very light greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.5B 8.2/5.7 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| C_v1 | VonKries | 4.6B 8.2/5.6 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| C_v1 | CAT02 | 4.5B 8.2/5.6 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| C_v1 | XYZScaling | 4.3B 8.2/5.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D50_v1 | VonKries | 1.5B 8.2/3.1 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D55_v1 | Bradford | 1.5B 8.2/3.5 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D55_v1 | VonKries | 1.8B 8.2/3.6 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D55_v1 | CAT02 | 1.4B 8.1/3.6 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D55_v1 | XYZScaling | 1.5B 8.2/3.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | Bradford | 2.2B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | VonKries | 2.2B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | CAT02 | 2.2B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D65_v1 | XYZScaling | 2.2B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | Bradford | 4.0B 8.2/6.6 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | VonKries | 4.1B 8.2/6.5 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | CAT02 | 4.0B 8.2/6.5 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| D75_v1 | XYZScaling | 3.8B 8.2/6.8 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| E_v1 | Bradford | 2.1B 8.1/3.5 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| E_v1 | VonKries | 1.9B 8.2/3.5 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| E_v1 | CAT02 | 2.1B 8.1/3.5 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| E_v1 | XYZScaling | 2.1B 8.2/3.4 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | Bradford | 2.1B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | VonKries | 2.1B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | CAT02 | 2.1B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |
| F7_v1 | XYZScaling | 2.1B 8.2/5.3 | very light greenish blue | ✅ | very light greenish blue | ✅ |

#### 165. #65A8C3 - Expected: light greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.1B 6.5/6.1 | light greenish blue | ✅ | light greenish blue | ✅ |
| C_v1 | VonKries | 4.2B 6.5/6.1 | light greenish blue | ✅ | light greenish blue | ✅ |
| C_v1 | CAT02 | 4.1B 6.5/6.1 | light greenish blue | ✅ | light greenish blue | ✅ |
| C_v1 | XYZScaling | 3.9B 6.5/6.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| D50_v1 | Bradford | 1.6B 6.4/3.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| D50_v1 | VonKries | 2.1B 6.4/3.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| D50_v1 | CAT02 | 1.4B 6.4/3.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | Bradford | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | VonKries | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | CAT02 | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D65_v1 | XYZScaling | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | Bradford | 3.7B 6.5/6.9 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | VonKries | 3.8B 6.5/6.9 | light greenish blue | ✅ | light greenish blue | ✅ |
| D75_v1 | CAT02 | 3.7B 6.5/6.9 | light greenish blue | ✅ | light greenish blue | ✅ |
| E_v1 | Bradford | 2.5B 6.4/4.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| E_v1 | VonKries | 2.3B 6.4/4.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| E_v1 | CAT02 | 2.5B 6.4/4.2 | light greenish blue | ✅ | light greenish blue | ✅ |
| E_v1 | XYZScaling | 2.5B 6.5/4.0 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | Bradford | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | VonKries | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | CAT02 | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |
| F7_v1 | XYZScaling | 2.2B 6.5/5.7 | light greenish blue | ✅ | light greenish blue | ✅ |

#### 166. #2A7691 - Expected: moderate greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.3B 4.5/6.2 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| C_v1 | VonKries | 3.4B 4.5/6.1 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| C_v1 | CAT02 | 3.3B 4.5/6.2 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| C_v1 | XYZScaling | 3.0B 4.5/6.3 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D55_v1 | XYZScaling | 0.1B 4.5/4.5 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | Bradford | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | VonKries | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | CAT02 | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D65_v1 | XYZScaling | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | Bradford | 3.0B 4.6/6.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | VonKries | 3.1B 4.5/6.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | CAT02 | 3.0B 4.6/6.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| D75_v1 | XYZScaling | 2.7B 4.5/7.0 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | Bradford | 2.0B 4.5/4.8 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | VonKries | 1.9B 4.5/4.7 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | CAT02 | 2.1B 4.5/4.8 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| E_v1 | XYZScaling | 2.1B 4.5/4.6 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | Bradford | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | VonKries | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | CAT02 | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |
| F7_v1 | XYZScaling | 1.9B 4.5/5.9 | moderate greenish blue | ✅ | moderate greenish blue | ✅ |

#### 167. #134A60 - Expected: dark greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.9B 2.9/4.8 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| C_v1 | VonKries | 3.0B 2.9/4.7 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| C_v1 | CAT02 | 2.9B 2.9/4.8 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| C_v1 | XYZScaling | 2.6B 2.9/4.9 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D55_v1 | CAT02 | 0.1B 2.9/3.8 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D55_v1 | XYZScaling | 0.5B 2.9/3.5 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D65_v1 | Bradford | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D65_v1 | VonKries | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D65_v1 | CAT02 | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D65_v1 | XYZScaling | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | Bradford | 2.6B 2.9/5.2 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | VonKries | 2.8B 2.9/5.2 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | CAT02 | 2.6B 2.9/5.2 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| D75_v1 | XYZScaling | 2.3B 2.9/5.4 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| E_v1 | Bradford | 2.0B 2.9/3.8 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| E_v1 | VonKries | 1.8B 2.9/3.7 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| E_v1 | CAT02 | 2.0B 2.9/3.8 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| E_v1 | XYZScaling | 2.1B 2.9/3.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| F7_v1 | Bradford | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| F7_v1 | VonKries | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| F7_v1 | CAT02 | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |
| F7_v1 | XYZScaling | 1.7B 2.9/4.6 | dark greenish blue | ✅ | dark greenish blue | ✅ |

#### 168. #0B2C3B - Expected: very dark greenish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.5B 1.6/3.4 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| C_v1 | VonKries | 2.6B 1.6/3.4 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| C_v1 | CAT02 | 2.5B 1.6/3.4 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| C_v1 | XYZScaling | 2.3B 1.6/3.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D55_v1 | Bradford | 9.8BG 1.6/2.7 | very dark greenish blue | ✅ | very dark bluish green | ❌ |
| D55_v1 | VonKries | 9.5BG 1.6/2.8 | very dark greenish blue | ✅ | very dark bluish green | ❌ |
| D55_v1 | CAT02 | 9.9BG 1.6/2.7 | very dark greenish blue | ✅ | very dark bluish green | ❌ |
| D55_v1 | XYZScaling | 0.2B 1.6/2.5 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | Bradford | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | VonKries | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | CAT02 | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D65_v1 | XYZScaling | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | Bradford | 2.2B 1.6/3.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | VonKries | 2.4B 1.6/3.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | CAT02 | 2.2B 1.6/3.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| D75_v1 | XYZScaling | 1.9B 1.6/3.8 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | Bradford | 1.8B 1.6/2.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | VonKries | 1.6B 1.6/2.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | CAT02 | 1.8B 1.6/2.7 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| E_v1 | XYZScaling | 1.9B 1.6/2.6 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | Bradford | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | VonKries | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | CAT02 | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |
| F7_v1 | XYZScaling | 1.4B 1.6/3.3 | very dark greenish blue | ✅ | very dark greenish blue | ✅ |

#### 169. #1B5CD7 - Expected: vivid blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.5B 4.2/14.0 | vivid blue | ✅ | vivid blue | ✅ |
| C_v1 | CAT02 | 9.5B 4.2/13.9 | vivid blue | ✅ | vivid blue | ✅ |
| C_v1 | XYZScaling | 8.7B 4.2/14.1 | vivid blue | ✅ | vivid greenish blue | ❌ |
| D65_v1 | Bradford | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| D65_v1 | VonKries | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| D65_v1 | CAT02 | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| D65_v1 | XYZScaling | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| D75_v1 | Bradford | 9.0B 4.2/14.3 | vivid blue | ✅ | vivid greenish blue | ❌ |
| D75_v1 | VonKries | 9.3B 4.2/14.3 | vivid blue | ✅ | vivid blue | ✅ |
| D75_v1 | CAT02 | 9.1B 4.2/14.2 | vivid blue | ✅ | vivid blue | ✅ |
| F7_v1 | Bradford | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| F7_v1 | VonKries | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| F7_v1 | CAT02 | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |
| F7_v1 | XYZScaling | 9.3B 4.2/13.3 | vivid blue | ✅ | vivid blue | ✅ |

#### 170. #419DED - Expected: brilliant blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.9PB 6.2/11.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| C_v1 | VonKries | 4.3PB 6.2/11.9 | brilliant blue | ✅ | brilliant blue | ✅ |
| C_v1 | CAT02 | 3.8PB 6.2/11.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| C_v1 | XYZScaling | 3.3PB 6.2/11.9 | brilliant blue | ✅ | brilliant blue | ✅ |
| D65_v1 | Bradford | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| D65_v1 | VonKries | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| D65_v1 | CAT02 | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| D65_v1 | XYZScaling | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | Bradford | 3.1PB 6.2/12.3 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | VonKries | 3.7PB 6.2/12.4 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | CAT02 | 3.1PB 6.2/12.2 | brilliant blue | ✅ | brilliant blue | ✅ |
| D75_v1 | XYZScaling | 2.1PB 6.2/12.5 | brilliant blue | ✅ | brilliant blue | ✅ |
| E_v1 | Bradford | 3.2PB 6.1/9.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| E_v1 | VonKries | 2.9PB 6.2/9.7 | brilliant blue | ✅ | brilliant blue | ✅ |
| E_v1 | CAT02 | 3.2PB 6.1/9.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| E_v1 | XYZScaling | 4.3PB 6.2/9.6 | brilliant blue | ✅ | brilliant blue | ✅ |
| F7_v1 | Bradford | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| F7_v1 | VonKries | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| F7_v1 | CAT02 | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |
| F7_v1 | XYZScaling | 2.0PB 6.2/10.8 | brilliant blue | ✅ | brilliant blue | ✅ |

#### 171. #276CBD - Expected: strong blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.7PB 4.5/10.9 | strong blue | ✅ | strong blue | ✅ |
| C_v1 | VonKries | 1.1PB 4.5/10.9 | strong blue | ✅ | strong blue | ✅ |
| C_v1 | CAT02 | 0.7PB 4.5/10.9 | strong blue | ✅ | strong blue | ✅ |
| C_v1 | XYZScaling | 1.5PB 4.5/11.3 | strong blue | ✅ | strong blue | ✅ |
| D65_v1 | Bradford | 9.9B 4.5/10.2 | strong blue | ✅ | strong blue | ✅ |
| D65_v1 | VonKries | 9.9B 4.5/10.2 | strong blue | ✅ | strong blue | ✅ |
| D65_v1 | CAT02 | 9.9B 4.5/10.2 | strong blue | ✅ | strong blue | ✅ |
| D65_v1 | XYZScaling | 9.9B 4.5/10.2 | strong blue | ✅ | strong blue | ✅ |
| D75_v1 | Bradford | 1.5PB 4.5/11.6 | strong blue | ✅ | strong blue | ✅ |
| D75_v1 | VonKries | 0.3PB 4.5/11.3 | strong blue | ✅ | strong blue | ✅ |
| D75_v1 | CAT02 | 1.5PB 4.5/11.5 | strong blue | ✅ | strong blue | ✅ |
| D75_v1 | XYZScaling | 9.6B 4.5/11.6 | strong blue | ✅ | strong blue | ✅ |
| E_v1 | Bradford | 2.7PB 4.4/9.5 | strong blue | ✅ | strong blue | ✅ |
| E_v1 | VonKries | 0.3PB 4.4/9.2 | strong blue | ✅ | strong blue | ✅ |
| E_v1 | CAT02 | 0.7PB 4.4/9.3 | strong blue | ✅ | strong blue | ✅ |
| F7_v1 | Bradford | 9.9B 4.5/10.1 | strong blue | ✅ | strong blue | ✅ |
| F7_v1 | VonKries | 9.9B 4.5/10.1 | strong blue | ✅ | strong blue | ✅ |
| F7_v1 | CAT02 | 9.9B 4.5/10.1 | strong blue | ✅ | strong blue | ✅ |
| F7_v1 | XYZScaling | 9.9B 4.5/10.1 | strong blue | ✅ | strong blue | ✅ |

#### 172. #113074 - Expected: deep blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.7PB 2.2/8.8 | deep blue | ✅ | deep blue | ✅ |
| C_v1 | VonKries | 4.5PB 2.2/9.0 | deep blue | ✅ | deep blue | ✅ |
| C_v1 | CAT02 | 3.6PB 2.2/8.8 | deep blue | ✅ | deep blue | ✅ |
| C_v1 | XYZScaling | 2.8PB 2.2/8.8 | deep blue | ✅ | deep blue | ✅ |
| D55_v1 | Bradford | 2.9PB 2.1/7.2 | deep blue | ✅ | deep blue | ✅ |
| D55_v1 | VonKries | 1.3PB 2.2/7.1 | deep blue | ✅ | deep blue | ✅ |
| D55_v1 | CAT02 | 2.8PB 2.1/7.3 | deep blue | ✅ | deep blue | ✅ |
| D55_v1 | XYZScaling | 6.1PB 2.2/7.5 | deep purplish blue | ❌ | deep blue | ✅ |
| D65_v1 | Bradford | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| D65_v1 | VonKries | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| D65_v1 | CAT02 | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| D65_v1 | XYZScaling | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| D75_v1 | Bradford | 3.0PB 2.2/9.0 | deep blue | ✅ | deep blue | ✅ |
| D75_v1 | VonKries | 3.9PB 2.2/9.2 | deep blue | ✅ | deep blue | ✅ |
| D75_v1 | CAT02 | 3.0PB 2.2/8.9 | deep blue | ✅ | deep blue | ✅ |
| E_v1 | Bradford | 4.2PB 2.1/7.8 | deep blue | ✅ | deep blue | ✅ |
| E_v1 | VonKries | 3.7PB 2.2/7.7 | deep blue | ✅ | deep blue | ✅ |
| E_v1 | CAT02 | 4.0PB 2.1/7.8 | deep blue | ✅ | deep blue | ✅ |
| E_v1 | XYZScaling | 6.4PB 2.2/8.2 | deep purplish blue | ❌ | deep blue | ✅ |
| F7_v1 | Bradford | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| F7_v1 | VonKries | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| F7_v1 | CAT02 | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |
| F7_v1 | XYZScaling | 2.9PB 2.2/8.2 | deep blue | ✅ | deep blue | ✅ |

#### 173. #99C6F9 - Expected: very light blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.7PB 7.8/7.4 | very light blue | ✅ | very light blue | ✅ |
| C_v1 | VonKries | 5.1PB 7.8/7.4 | very light blue | ✅ | very light blue | ✅ |
| C_v1 | CAT02 | 4.7PB 7.8/7.4 | very light blue | ✅ | very light blue | ✅ |
| C_v1 | XYZScaling | 4.2PB 7.8/7.5 | very light blue | ✅ | very light blue | ✅ |
| D65_v1 | Bradford | 2.0PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| D65_v1 | VonKries | 2.0PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| D65_v1 | CAT02 | 2.0PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| D65_v1 | XYZScaling | 2.0PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | Bradford | 2.9PB 7.8/7.9 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | VonKries | 3.3PB 7.8/8.0 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | CAT02 | 2.9PB 7.8/7.9 | very light blue | ✅ | very light blue | ✅ |
| D75_v1 | XYZScaling | 2.1PB 7.8/8.0 | very light blue | ✅ | very light blue | ✅ |
| F7_v1 | Bradford | 1.9PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| F7_v1 | VonKries | 1.9PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| F7_v1 | CAT02 | 1.9PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |
| F7_v1 | XYZScaling | 1.9PB 7.8/6.4 | very light blue | ✅ | very light blue | ✅ |

#### 174. #73A4DC - Expected: light blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.1PB 6.5/8.5 | light blue | ✅ | light blue | ✅ |
| C_v1 | VonKries | 4.5PB 6.5/8.5 | light blue | ✅ | light blue | ✅ |
| C_v1 | CAT02 | 4.1PB 6.5/8.4 | light blue | ✅ | light blue | ✅ |
| C_v1 | XYZScaling | 3.6PB 6.5/8.5 | light blue | ✅ | light blue | ✅ |
| D55_v1 | XYZScaling | 2.6PB 6.5/5.3 | light blue | ✅ | light blue | ✅ |
| D65_v1 | Bradford | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| D65_v1 | VonKries | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| D65_v1 | CAT02 | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| D65_v1 | XYZScaling | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| D75_v1 | Bradford | 2.7PB 6.5/8.9 | light blue | ✅ | light blue | ✅ |
| D75_v1 | CAT02 | 2.7PB 6.5/8.9 | light blue | ✅ | light blue | ✅ |
| E_v1 | Bradford | 4.5PB 6.5/6.4 | light blue | ✅ | light blue | ✅ |
| E_v1 | VonKries | 4.3PB 6.5/6.3 | light blue | ✅ | light blue | ✅ |
| E_v1 | CAT02 | 4.5PB 6.5/6.4 | light blue | ✅ | light blue | ✅ |
| F7_v1 | Bradford | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| F7_v1 | VonKries | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| F7_v1 | CAT02 | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |
| F7_v1 | XYZScaling | 2.0PB 6.5/7.5 | light blue | ✅ | light blue | ✅ |

#### 175. #34689E - Expected: moderate blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.3PB 4.2/8.0 | moderate blue | ✅ | moderate blue | ✅ |
| C_v1 | VonKries | 0.4PB 4.2/7.9 | moderate blue | ✅ | moderate blue | ✅ |
| C_v1 | CAT02 | 0.3PB 4.2/7.9 | moderate blue | ✅ | moderate blue | ✅ |
| C_v1 | XYZScaling | 9.1B 4.2/8.0 | moderate blue | ✅ | moderate blue | ✅ |
| D55_v1 | Bradford | 0.4PB 4.2/5.9 | moderate blue | ✅ | moderate blue | ✅ |
| D55_v1 | CAT02 | 0.5PB 4.2/6.0 | moderate blue | ✅ | moderate blue | ✅ |
| D55_v1 | XYZScaling | 2.3PB 4.2/5.7 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | Bradford | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | VonKries | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | CAT02 | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| D65_v1 | XYZScaling | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| D75_v1 | VonKries | 9.4B 4.2/8.3 | moderate blue | ✅ | moderate blue | ✅ |
| E_v1 | Bradford | 2.2PB 4.2/6.5 | moderate blue | ✅ | moderate blue | ✅ |
| E_v1 | VonKries | 2.2PB 4.2/6.5 | moderate blue | ✅ | moderate blue | ✅ |
| E_v1 | CAT02 | 2.1PB 4.2/6.5 | moderate blue | ✅ | moderate blue | ✅ |
| E_v1 | XYZScaling | 2.6PB 4.2/6.3 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | Bradford | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | VonKries | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | CAT02 | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |
| F7_v1 | XYZScaling | 0.8PB 4.2/7.3 | moderate blue | ✅ | moderate blue | ✅ |

#### 176. #173459 - Expected: dark blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 0.2PB 2.1/5.4 | dark blue | ✅ | dark blue | ✅ |
| D50_v1 | XYZScaling | 1.3PB 2.1/3.3 | dark blue | ✅ | dark blue | ✅ |
| E_v1 | XYZScaling | 1.7PB 2.1/4.4 | dark blue | ✅ | dark blue | ✅ |

#### 177. #C2D2EC - Expected: very pale blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.8B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | VonKries | 8.8B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | CAT02 | 8.8B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| D65_v1 | XYZScaling | 8.8B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| D75_v1 | Bradford | 4.7PB 8.3/4.6 | very pale blue | ✅ | very pale blue | ✅ |
| D75_v1 | CAT02 | 4.6PB 8.3/4.6 | very pale blue | ✅ | very pale blue | ✅ |
| D75_v1 | XYZScaling | 4.0PB 8.3/4.6 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | Bradford | 8.4B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | VonKries | 8.4B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | CAT02 | 8.4B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |
| F7_v1 | XYZScaling | 8.5B 8.3/2.8 | very pale blue | ✅ | very pale blue | ✅ |

#### 178. #91A2BB - Expected: pale blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 3.2PB 6.5/4.6 | pale blue | ✅ | pale blue | ✅ |
| D75_v1 | VonKries | 3.6PB 6.5/4.6 | pale blue | ✅ | pale blue | ✅ |
| D75_v1 | CAT02 | 3.2PB 6.5/4.6 | pale blue | ✅ | pale blue | ✅ |
| D75_v1 | XYZScaling | 2.5PB 6.5/4.7 | pale blue | ✅ | pale blue | ✅ |

#### 179. #54687F - Expected: grayish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.8PB 4.2/3.6 | grayish blue | ✅ | grayish blue | ✅ |
| C_v1 | VonKries | 3.1PB 4.2/3.6 | grayish blue | ✅ | grayish blue | ✅ |
| C_v1 | CAT02 | 2.7PB 4.2/3.6 | grayish blue | ✅ | grayish blue | ✅ |
| C_v1 | XYZScaling | 2.3PB 4.2/3.7 | grayish blue | ✅ | grayish blue | ✅ |
| D55_v1 | Bradford | 2.2B 4.2/1.9 | grayish blue | ✅ | grayish blue | ✅ |
| D55_v1 | VonKries | 1.7B 4.2/1.9 | grayish blue | ✅ | grayish blue | ✅ |
| D55_v1 | CAT02 | 2.3B 4.2/1.9 | grayish blue | ✅ | grayish blue | ✅ |
| D55_v1 | XYZScaling | 3.0B 4.2/1.7 | grayish blue | ✅ | grayish blue | ✅ |
| D75_v1 | Bradford | 0.7PB 4.3/4.0 | grayish blue | ✅ | grayish blue | ✅ |
| D75_v1 | VonKries | 1.1PB 4.2/4.1 | grayish blue | ✅ | grayish blue | ✅ |
| D75_v1 | CAT02 | 0.6PB 4.3/4.0 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | Bradford | 3.6PB 4.2/2.2 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | VonKries | 3.3PB 4.2/2.1 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | CAT02 | 3.6PB 4.2/2.2 | grayish blue | ✅ | grayish blue | ✅ |
| E_v1 | XYZScaling | 4.4PB 4.2/2.1 | grayish blue | ✅ | grayish blue | ✅ |

#### 180. #323F4E - Expected: dark grayish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0B 2.6/2.5 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| C_v1 | VonKries | 6.6B 2.6/2.4 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| C_v1 | CAT02 | 5.9B 2.6/2.5 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| C_v1 | XYZScaling | 5.2B 2.6/2.5 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | Bradford | 3.5B 2.6/2.3 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | VonKries | 3.5B 2.6/2.3 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | CAT02 | 3.5B 2.6/2.3 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D65_v1 | XYZScaling | 3.5B 2.6/2.3 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | Bradford | 4.3B 2.6/2.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | VonKries | 4.5B 2.6/2.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | CAT02 | 4.3B 2.6/2.9 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| D75_v1 | XYZScaling | 4.0B 2.6/3.0 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | Bradford | 3.5B 2.6/2.2 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | VonKries | 3.5B 2.6/2.2 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | CAT02 | 3.5B 2.6/2.2 | dark grayish blue | ✅ | dark grayish blue | ✅ |
| F7_v1 | XYZScaling | 3.5B 2.6/2.2 | dark grayish blue | ✅ | dark grayish blue | ✅ |

#### 181. #1E2531 - Expected: blackish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.8B 1.4/1.8 | blackish blue | ✅ | blackish blue | ✅ |
| C_v1 | VonKries | 7.5B 1.4/1.8 | blackish blue | ✅ | blackish blue | ✅ |
| C_v1 | CAT02 | 6.7B 1.4/1.8 | blackish blue | ✅ | blackish blue | ✅ |
| C_v1 | XYZScaling | 6.0B 1.4/1.9 | blackish blue | ✅ | blackish blue | ✅ |
| D55_v1 | Bradford | 2.9B 1.4/1.0 | blackish blue | ✅ | blackish blue | ✅ |
| D55_v1 | VonKries | 2.4B 1.4/1.1 | blackish blue | ✅ | blackish blue | ✅ |
| D55_v1 | CAT02 | 3.0B 1.4/1.1 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | Bradford | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | VonKries | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | CAT02 | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| D65_v1 | XYZScaling | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| E_v1 | Bradford | 1.9PB 1.4/1.1 | blackish blue | ✅ | blackish blue | ✅ |
| E_v1 | VonKries | 1.3PB 1.4/1.1 | blackish blue | ✅ | blackish blue | ✅ |
| E_v1 | CAT02 | 1.8PB 1.4/1.1 | blackish blue | ✅ | blackish blue | ✅ |
| E_v1 | XYZScaling | 4.8PB 1.4/1.1 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | Bradford | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | VonKries | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | CAT02 | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |
| F7_v1 | XYZScaling | 4.0B 1.4/1.7 | blackish blue | ✅ | blackish blue | ✅ |

#### 182. #E1E1F1 - Expected: bluish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 4.8B 9.0/0.9 | bluish white | ✅ | bluish white | ✅ |
| D65_v1 | VonKries | 4.8B 9.0/0.9 | bluish white | ✅ | bluish white | ✅ |
| D65_v1 | CAT02 | 4.8B 9.0/0.9 | bluish white | ✅ | bluish white | ✅ |
| D65_v1 | XYZScaling | 4.8B 9.0/0.9 | bluish white | ✅ | bluish white | ✅ |
| F7_v1 | Bradford | 4.4B 9.0/0.8 | bluish white | ✅ | bluish white | ✅ |
| F7_v1 | VonKries | 4.4B 9.0/0.8 | bluish white | ✅ | bluish white | ✅ |
| F7_v1 | CAT02 | 4.4B 9.0/0.8 | bluish white | ✅ | bluish white | ✅ |
| F7_v1 | XYZScaling | 4.4B 9.0/0.8 | bluish white | ✅ | bluish white | ✅ |

#### 183. #B7B8C6 - Expected: light bluish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 4.4B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| D65_v1 | VonKries | 4.4B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| D65_v1 | CAT02 | 4.4B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| D65_v1 | XYZScaling | 4.4B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| F7_v1 | Bradford | 4.2B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| F7_v1 | VonKries | 4.2B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| F7_v1 | CAT02 | 4.2B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |
| F7_v1 | XYZScaling | 4.2B 7.4/0.9 | light bluish gray | ✅ | light bluish gray | ✅ |

#### 184. #838793 - Expected: bluish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 3.3B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| D65_v1 | VonKries | 3.3B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| D65_v1 | CAT02 | 3.3B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| D65_v1 | XYZScaling | 3.3B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| F7_v1 | Bradford | 3.1B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| F7_v1 | VonKries | 3.1B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| F7_v1 | CAT02 | 3.1B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |
| F7_v1 | XYZScaling | 3.1B 5.5/1.0 | bluish gray | ✅ | bluish gray | ✅ |

#### 185. #50545F - Expected: dark bluish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.4PB 3.5/1.4 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| C_v1 | VonKries | 3.5PB 3.5/1.4 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| C_v1 | CAT02 | 3.4PB 3.5/1.4 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| C_v1 | XYZScaling | 3.2PB 3.5/1.4 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| D65_v1 | Bradford | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| D65_v1 | VonKries | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| D65_v1 | CAT02 | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| D65_v1 | XYZScaling | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| F7_v1 | Bradford | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| F7_v1 | VonKries | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| F7_v1 | CAT02 | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |
| F7_v1 | XYZScaling | 4.1B 3.5/1.1 | dark bluish gray | ✅ | dark bluish gray | ✅ |

#### 186. #24272E - Expected: bluish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.0PB 1.5/1.0 | bluish black | ✅ | bluish black | ✅ |
| C_v1 | VonKries | 1.8PB 1.5/1.0 | bluish black | ✅ | bluish black | ✅ |
| C_v1 | CAT02 | 0.8PB 1.5/1.0 | bluish black | ✅ | bluish black | ✅ |
| D65_v1 | Bradford | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| D65_v1 | VonKries | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| D65_v1 | CAT02 | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| D65_v1 | XYZScaling | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| F7_v1 | Bradford | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| F7_v1 | VonKries | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| F7_v1 | CAT02 | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |
| F7_v1 | XYZScaling | 3.1B 1.5/0.9 | bluish black | ✅ | bluish black | ✅ |

#### 187. #4436D1 - Expected: vivid purplish blue

No matches

#### 188. #8088E2 - Expected: brilliant purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.8PB 5.9/11.4 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| C_v1 | VonKries | 6.7PB 5.9/11.4 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| C_v1 | CAT02 | 6.9PB 5.9/11.4 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| C_v1 | XYZScaling | 6.7PB 5.9/11.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D65_v1 | Bradford | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D65_v1 | VonKries | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D65_v1 | CAT02 | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D65_v1 | XYZScaling | 6.9PB 5.9/10.6 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D75_v1 | Bradford | 6.2PB 5.9/11.8 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D75_v1 | VonKries | 6.3PB 5.9/11.8 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| D75_v1 | CAT02 | 6.3PB 5.9/11.7 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| E_v1 | Bradford | 8.1PB 5.8/9.7 | brilliant violet | ❌ | brilliant purplish blue | ✅ |
| E_v1 | VonKries | 8.2PB 5.9/9.7 | brilliant violet | ❌ | brilliant purplish blue | ✅ |
| E_v1 | CAT02 | 8.1PB 5.8/9.7 | brilliant violet | ❌ | brilliant purplish blue | ✅ |
| E_v1 | XYZScaling | 8.4PB 5.9/9.6 | brilliant violet | ❌ | brilliant purplish blue | ✅ |
| F7_v1 | Bradford | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| F7_v1 | VonKries | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| F7_v1 | CAT02 | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ |
| F7_v1 | XYZScaling | 7.0PB 5.9/10.5 | brilliant purplish blue | ✅ | brilliant blue | ❌ |

#### 189. #5359B5 - Expected: strong purplish blue

No matches

#### 190. #2A286F - Expected: deep purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.7PB 2.1/10.1 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| C_v1 | CAT02 | 7.6PB 2.1/10.0 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| C_v1 | XYZScaling | 7.2PB 2.0/9.9 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D50_v1 | VonKries | 7.9PB 2.0/7.0 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D55_v1 | VonKries | 7.7PB 2.0/7.9 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D65_v1 | Bradford | 7.6PB 2.0/9.4 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D65_v1 | VonKries | 7.6PB 2.0/9.4 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D65_v1 | CAT02 | 7.6PB 2.0/9.4 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D65_v1 | XYZScaling | 7.6PB 2.0/9.4 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D75_v1 | Bradford | 6.9PB 2.1/10.0 | deep purplish blue | ✅ | deep blue | ❌ |
| D75_v1 | VonKries | 7.6PB 2.0/10.6 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| D75_v1 | CAT02 | 7.0PB 2.1/9.9 | deep purplish blue | ✅ | deep blue | ❌ |
| F7_v1 | Bradford | 7.6PB 2.0/9.3 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| F7_v1 | VonKries | 7.5PB 2.0/9.3 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| F7_v1 | CAT02 | 7.6PB 2.0/9.3 | deep purplish blue | ✅ | deep purplish blue | ✅ |
| F7_v1 | XYZScaling | 7.6PB 2.0/9.4 | deep purplish blue | ✅ | deep purplish blue | ✅ |

#### 191. #B7C0F8 - Expected: very light purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| D65_v1 | VonKries | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| D65_v1 | CAT02 | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| D65_v1 | XYZScaling | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| D75_v1 | Bradford | 8.2PB 7.8/7.8 | very light violet | ❌ | very light purplish blue | ✅ |
| D75_v1 | VonKries | 8.6PB 7.8/7.9 | very light violet | ❌ | very light purplish blue | ✅ |
| D75_v1 | CAT02 | 8.2PB 7.8/7.7 | very light violet | ❌ | very light purplish blue | ✅ |
| D75_v1 | XYZScaling | 7.4PB 7.8/7.7 | very light purplish blue | ✅ | very light purplish blue | ✅ |
| F7_v1 | Bradford | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| F7_v1 | VonKries | 8.7PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| F7_v1 | CAT02 | 8.7PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |
| F7_v1 | XYZScaling | 8.8PB 7.8/6.3 | very light violet | ❌ | very light purplish blue | ✅ |

#### 192. #8991CB - Expected: light purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.4PB 6.1/8.2 | light violet | ❌ | light purplish blue | ✅ |
| C_v1 | VonKries | 8.6PB 6.1/8.3 | light violet | ❌ | light purplish blue | ✅ |
| C_v1 | CAT02 | 8.4PB 6.1/8.2 | light violet | ❌ | light purplish blue | ✅ |
| C_v1 | XYZScaling | 8.2PB 6.1/8.3 | light violet | ❌ | light purplish blue | ✅ |
| D65_v1 | Bradford | 8.3PB 6.1/7.2 | light violet | ❌ | light purplish blue | ✅ |
| D65_v1 | VonKries | 8.3PB 6.1/7.2 | light violet | ❌ | light purplish blue | ✅ |
| D65_v1 | CAT02 | 8.3PB 6.1/7.2 | light violet | ❌ | light purplish blue | ✅ |
| D65_v1 | XYZScaling | 8.3PB 6.1/7.2 | light violet | ❌ | light purplish blue | ✅ |
| D75_v1 | Bradford | 7.7PB 6.1/8.7 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | VonKries | 7.8PB 6.1/8.8 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | CAT02 | 7.7PB 6.1/8.7 | light purplish blue | ✅ | light purplish blue | ✅ |
| D75_v1 | XYZScaling | 7.3PB 6.1/8.7 | light purplish blue | ✅ | light purplish blue | ✅ |
| F7_v1 | Bradford | 8.3PB 6.1/7.1 | light violet | ❌ | light purplish blue | ✅ |
| F7_v1 | VonKries | 8.3PB 6.1/7.1 | light violet | ❌ | light purplish blue | ✅ |
| F7_v1 | CAT02 | 8.3PB 6.1/7.1 | light violet | ❌ | light purplish blue | ✅ |
| F7_v1 | XYZScaling | 8.3PB 6.1/7.1 | light violet | ❌ | light purplish blue | ✅ |

#### 193. #4D4E87 - Expected: moderate purplish blue

No matches

#### 194. #222248 - Expected: dark purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.2PB 1.5/5.1 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| C_v1 | CAT02 | 7.2PB 1.5/5.1 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D50_v1 | VonKries | 8.2PB 1.5/3.2 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D50_v1 | XYZScaling | 8.4PB 1.5/3.0 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D55_v1 | VonKries | 7.6PB 1.5/3.7 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | Bradford | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | VonKries | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | CAT02 | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D65_v1 | XYZScaling | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| D75_v2 | Bradford | 7.5PB 1.5/2.0 | dark purplish blue | ✅ | blackish blue | ❌ |
| D75_v2 | XYZScaling | 7.5PB 1.5/2.0 | dark purplish blue | ✅ | blackish blue | ❌ |
| F2_v1 | Bradford | 8.5PB 1.4/2.1 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F2_v1 | CAT02 | 7.3PB 1.4/2.2 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | Bradford | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | VonKries | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | CAT02 | 6.9PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |
| F7_v1 | XYZScaling | 7.0PB 1.5/4.6 | dark purplish blue | ✅ | dark purplish blue | ✅ |

#### 195. #C5C9F0 - Expected: very pale purplish blue

No matches

#### 196. #8E92B7 - Expected: pale purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| D65_v1 | VonKries | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| D65_v1 | CAT02 | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| D65_v1 | XYZScaling | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| F7_v1 | Bradford | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| F7_v1 | VonKries | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| F7_v1 | CAT02 | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |
| F7_v1 | XYZScaling | 8.4PB 6.0/4.4 | pale violet | ❌ | pale purplish blue | ✅ |

#### 197. #494D71 - Expected: grayish purplish blue

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D75_v1 | Bradford | 6.7PB 3.3/5.0 | grayish purplish blue | ✅ | grayish purplish blue | ✅ |
| D75_v1 | CAT02 | 6.7PB 3.3/4.9 | grayish purplish blue | ✅ | grayish purplish blue | ✅ |

#### 198. #7931D3 - Expected: vivid violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 1.6P 3.8/15.3 | vivid violet | ✅ | vivid violet | ✅ |
| D50_v1 | CAT02 | 1.2P 3.7/15.3 | vivid violet | ✅ | vivid violet | ✅ |
| D55_v1 | Bradford | 9.5PB 3.8/14.7 | vivid violet | ✅ | vivid violet | ✅ |
| D55_v1 | CAT02 | 9.3PB 3.8/14.8 | vivid violet | ✅ | vivid violet | ✅ |
| D55_v1 | XYZScaling | 1.9P 3.9/17.2 | vivid violet | ✅ | vivid violet | ✅ |
| E_v1 | Bradford | 9.1PB 3.9/15.4 | vivid violet | ✅ | vivid violet | ✅ |
| E_v1 | XYZScaling | 1.5P 3.9/18.2 | vivid violet | ✅ | vivid violet | ✅ |

#### 199. #987FDC - Expected: brilliant violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| E_v1 | Bradford | 0.6P 5.8/9.6 | brilliant violet | ✅ | brilliant violet | ✅ |
| E_v1 | VonKries | 0.1P 5.8/9.4 | brilliant violet | ✅ | brilliant violet | ✅ |
| E_v1 | CAT02 | 0.3P 5.8/9.5 | brilliant violet | ✅ | brilliant violet | ✅ |
| E_v1 | XYZScaling | 2.8P 5.8/10.5 | brilliant violet | ✅ | brilliant violet | ✅ |

#### 200. #61419C - Expected: strong violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D55_v1 | XYZScaling | 2.1P 3.5/9.4 | strong violet | ✅ | strong violet | ✅ |
| E_v1 | Bradford | 9.6PB 3.5/9.1 | strong violet | ✅ | strong violet | ✅ |
| E_v1 | CAT02 | 9.4PB 3.5/9.1 | strong violet | ✅ | strong violet | ✅ |
| E_v1 | XYZScaling | 2.1P 3.5/10.5 | strong violet | ✅ | strong violet | ✅ |

#### 201. #3C1668 - Expected: deep violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | VonKries | 9.3PB 1.8/10.0 | deep violet | ✅ | deep violet | ✅ |
| D50_v1 | VonKries | 2.5P 1.8/8.5 | deep violet | ✅ | deep violet | ✅ |
| D55_v1 | Bradford | 2.9P 1.7/10.1 | deep violet | ✅ | deep violet | ✅ |
| D55_v1 | VonKries | 0.9P 1.8/8.7 | deep violet | ✅ | deep violet | ✅ |
| D55_v1 | CAT02 | 2.8P 1.7/10.2 | deep violet | ✅ | deep violet | ✅ |
| E_v1 | Bradford | 2.3P 1.8/10.6 | deep violet | ✅ | deep violet | ✅ |
| E_v1 | VonKries | 1.6P 1.8/10.0 | deep violet | ✅ | deep violet | ✅ |
| E_v1 | CAT02 | 2.0P 1.8/10.4 | deep violet | ✅ | deep violet | ✅ |
| F7_v1 | Bradford | 9.0PB 1.8/9.1 | deep violet | ✅ | deep violet | ✅ |
| F7_v1 | VonKries | 9.0PB 1.8/9.1 | deep violet | ✅ | deep violet | ✅ |
| F7_v1 | CAT02 | 9.0PB 1.8/9.1 | deep violet | ✅ | deep violet | ✅ |
| F7_v1 | XYZScaling | 9.1PB 1.8/9.1 | deep violet | ✅ | deep violet | ✅ |

#### 202. #C9BAF8 - Expected: very light violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.5P 7.8/8.2 | very light violet | ✅ | very light violet | ✅ |
| C_v1 | VonKries | 2.7P 7.8/8.3 | very light violet | ✅ | very light violet | ✅ |
| C_v1 | CAT02 | 2.5P 7.8/8.1 | very light violet | ✅ | very light violet | ✅ |
| C_v1 | XYZScaling | 2.4P 7.8/8.2 | very light violet | ✅ | very light violet | ✅ |
| D65_v1 | Bradford | 2.6P 7.8/7.0 | very light violet | ✅ | very light violet | ✅ |
| D65_v1 | VonKries | 2.6P 7.8/7.0 | very light violet | ✅ | very light violet | ✅ |
| D65_v1 | CAT02 | 2.6P 7.8/7.0 | very light violet | ✅ | very light violet | ✅ |
| D65_v1 | XYZScaling | 2.6P 7.8/7.0 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | Bradford | 1.0P 7.8/8.3 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | VonKries | 1.3P 7.8/8.4 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | CAT02 | 1.0P 7.8/8.3 | very light violet | ✅ | very light violet | ✅ |
| D75_v1 | XYZScaling | 0.7P 7.8/8.3 | very light violet | ✅ | very light violet | ✅ |
| F7_v1 | Bradford | 2.6P 7.8/6.9 | very light violet | ✅ | very light violet | ✅ |
| F7_v1 | VonKries | 2.6P 7.8/6.9 | very light violet | ✅ | very light violet | ✅ |
| F7_v1 | CAT02 | 2.6P 7.8/6.9 | very light violet | ✅ | very light violet | ✅ |
| F7_v1 | XYZScaling | 2.6P 7.8/6.9 | very light violet | ✅ | very light violet | ✅ |

#### 203. #9B8CCA - Expected: light violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1P 6.1/8.2 | light violet | ✅ | light violet | ✅ |
| C_v1 | VonKries | 0.1P 6.1/8.2 | light violet | ✅ | light violet | ✅ |
| C_v1 | CAT02 | 0.2P 6.1/8.2 | light violet | ✅ | light violet | ✅ |
| C_v1 | XYZScaling | 0.1P 6.1/8.3 | light violet | ✅ | light violet | ✅ |
| D55_v1 | Bradford | 1.8P 6.0/5.0 | light violet | ✅ | light violet | ✅ |
| D55_v1 | CAT02 | 1.6P 6.0/5.1 | light violet | ✅ | light violet | ✅ |
| D65_v1 | Bradford | 0.6P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| D65_v1 | VonKries | 0.6P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| D65_v1 | CAT02 | 0.6P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| D65_v1 | XYZScaling | 0.6P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| D75_v1 | Bradford | 9.5PB 6.1/8.7 | light violet | ✅ | light violet | ✅ |
| D75_v1 | VonKries | 9.6PB 6.1/8.7 | light violet | ✅ | light violet | ✅ |
| D75_v1 | CAT02 | 9.5PB 6.1/8.6 | light violet | ✅ | light violet | ✅ |
| D75_v1 | XYZScaling | 9.1PB 6.1/8.7 | light violet | ✅ | light violet | ✅ |
| F7_v1 | Bradford | 0.7P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| F7_v1 | VonKries | 0.7P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| F7_v1 | CAT02 | 0.6P 6.1/7.2 | light violet | ✅ | light violet | ✅ |
| F7_v1 | XYZScaling | 0.7P 6.1/7.2 | light violet | ✅ | light violet | ✅ |

#### 204. #5C4985 - Expected: moderate violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D55_v1 | Bradford | 0.5P 3.5/5.1 | moderate violet | ✅ | moderate violet | ✅ |
| D55_v1 | CAT02 | 0.3P 3.5/5.2 | moderate violet | ✅ | moderate violet | ✅ |
| E_v1 | Bradford | 1.3P 3.5/6.1 | moderate violet | ✅ | moderate violet | ✅ |
| E_v1 | VonKries | 0.8P 3.5/5.9 | moderate violet | ✅ | moderate violet | ✅ |
| E_v1 | CAT02 | 1.0P 3.5/6.0 | moderate violet | ✅ | moderate violet | ✅ |

#### 205. #34254D - Expected: dark violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D55_v1 | VonKries | 2.0P 1.8/3.9 | very dark purple | ❌ | dark violet | ✅ |

#### 206. #D0C6EF - Expected: very pale violet

No matches

#### 207. #9A90B5 - Expected: pale violet

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 1.4P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| D65_v1 | VonKries | 1.4P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| D65_v1 | CAT02 | 1.4P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| D65_v1 | XYZScaling | 1.4P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| F7_v1 | Bradford | 1.5P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| F7_v1 | VonKries | 1.5P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| F7_v1 | CAT02 | 1.5P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |
| F7_v1 | XYZScaling | 1.5P 6.1/4.1 | pale violet | ✅ | pale violet | ✅ |

#### 208. #584E72 - Expected: grayish violet

No matches

#### 209. #B935D5 - Expected: vivid purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.1P 4.9/21.1 | vivid purple | ✅ | vivid purple | ✅ |
| C_v1 | VonKries | 6.2P 4.8/21.5 | vivid purple | ✅ | vivid purple | ✅ |
| C_v1 | CAT02 | 6.0P 4.9/21.0 | vivid purple | ✅ | vivid purple | ✅ |
| C_v1 | XYZScaling | 6.1P 4.8/21.4 | vivid purple | ✅ | vivid purple | ✅ |
| D50_v1 | Bradford | 8.9P 4.8/17.4 | vivid purple | ✅ | vivid purple | ✅ |
| D50_v1 | VonKries | 8.4P 4.8/16.6 | vivid purple | ✅ | vivid purple | ✅ |
| D50_v1 | CAT02 | 8.7P 4.7/17.7 | vivid purple | ✅ | vivid purple | ✅ |
| D55_v1 | Bradford | 7.8P 4.8/18.4 | vivid purple | ✅ | vivid purple | ✅ |
| D55_v1 | VonKries | 7.5P 4.8/17.9 | vivid purple | ✅ | vivid purple | ✅ |
| D55_v1 | CAT02 | 7.7P 4.8/18.6 | vivid purple | ✅ | vivid purple | ✅ |
| D55_v1 | XYZScaling | 8.2P 4.8/18.8 | vivid purple | ✅ | vivid purple | ✅ |
| D65_v1 | Bradford | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| D65_v1 | VonKries | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| D65_v1 | CAT02 | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| D65_v1 | XYZScaling | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | Bradford | 5.6P 4.8/21.4 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | VonKries | 5.8P 4.8/21.8 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | CAT02 | 5.6P 4.9/21.2 | vivid purple | ✅ | vivid purple | ✅ |
| D75_v1 | XYZScaling | 5.3P 4.8/21.2 | vivid purple | ✅ | vivid purple | ✅ |
| E_v1 | Bradford | 7.4P 4.8/19.5 | vivid purple | ✅ | vivid purple | ✅ |
| E_v1 | VonKries | 7.3P 4.8/19.4 | vivid purple | ✅ | vivid purple | ✅ |
| E_v1 | CAT02 | 7.4P 4.8/19.5 | vivid purple | ✅ | vivid purple | ✅ |
| E_v1 | XYZScaling | 7.9P 4.8/20.4 | vivid purple | ✅ | vivid purple | ✅ |
| F7_v1 | Bradford | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| F7_v1 | VonKries | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| F7_v1 | CAT02 | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |
| F7_v1 | XYZScaling | 6.4P 4.8/19.9 | vivid purple | ✅ | vivid purple | ✅ |

#### 210. #CE8CE3 - Expected: brilliant purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.9P 6.7/12.2 | brilliant purple | ✅ | brilliant purple | ✅ |
| C_v1 | VonKries | 6.0P 6.7/12.4 | brilliant purple | ✅ | brilliant purple | ✅ |
| C_v1 | CAT02 | 5.9P 6.7/12.2 | brilliant purple | ✅ | brilliant purple | ✅ |
| C_v1 | XYZScaling | 5.9P 6.7/12.3 | brilliant purple | ✅ | brilliant purple | ✅ |
| D55_v1 | Bradford | 8.6P 6.7/9.7 | brilliant purple | ✅ | brilliant purple | ✅ |
| D55_v1 | VonKries | 8.3P 6.7/9.4 | brilliant purple | ✅ | brilliant purple | ✅ |
| D55_v1 | CAT02 | 8.5P 6.6/9.8 | brilliant purple | ✅ | brilliant purple | ✅ |
| D55_v1 | XYZScaling | 8.9P 6.7/10.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | Bradford | 6.2P 6.7/11.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | VonKries | 6.2P 6.7/11.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | CAT02 | 6.2P 6.7/11.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D65_v1 | XYZScaling | 6.2P 6.7/11.0 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | Bradford | 5.1P 6.7/12.3 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | VonKries | 5.2P 6.7/12.4 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | CAT02 | 5.1P 6.7/12.2 | brilliant purple | ✅ | brilliant purple | ✅ |
| D75_v1 | XYZScaling | 4.5P 6.7/11.9 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | Bradford | 8.2P 6.7/11.1 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | VonKries | 8.0P 6.7/11.1 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | CAT02 | 8.1P 6.7/11.1 | brilliant purple | ✅ | brilliant purple | ✅ |
| E_v1 | XYZScaling | 8.6P 6.7/11.7 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | Bradford | 6.2P 6.7/10.9 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | VonKries | 6.2P 6.7/10.9 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | CAT02 | 6.2P 6.7/10.9 | brilliant purple | ✅ | brilliant purple | ✅ |
| F7_v1 | XYZScaling | 6.2P 6.7/10.9 | brilliant purple | ✅ | brilliant purple | ✅ |

#### 211. #9352A8 - Expected: strong purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8P 4.5/12.4 | strong purple | ✅ | strong purple | ✅ |
| C_v1 | VonKries | 5.9P 4.5/12.6 | strong purple | ✅ | strong purple | ✅ |
| C_v1 | CAT02 | 5.8P 4.5/12.3 | strong purple | ✅ | strong purple | ✅ |
| C_v1 | XYZScaling | 5.8P 4.5/12.5 | strong purple | ✅ | strong purple | ✅ |
| D55_v1 | Bradford | 8.1P 4.5/10.0 | strong purple | ✅ | strong purple | ✅ |
| D55_v1 | VonKries | 7.8P 4.5/9.7 | strong purple | ✅ | strong purple | ✅ |
| D55_v1 | CAT02 | 8.0P 4.5/10.1 | strong purple | ✅ | strong purple | ✅ |
| D55_v1 | XYZScaling | 8.5P 4.5/10.4 | strong purple | ✅ | strong purple | ✅ |
| D65_v1 | Bradford | 6.2P 4.5/11.4 | strong purple | ✅ | strong purple | ✅ |
| D65_v1 | VonKries | 6.2P 4.5/11.4 | strong purple | ✅ | strong purple | ✅ |
| D65_v1 | CAT02 | 6.2P 4.5/11.4 | strong purple | ✅ | strong purple | ✅ |
| D65_v1 | XYZScaling | 6.2P 4.5/11.4 | strong purple | ✅ | strong purple | ✅ |
| D75_v1 | Bradford | 5.1P 4.5/12.6 | strong purple | ✅ | strong purple | ✅ |
| D75_v1 | VonKries | 5.3P 4.5/12.8 | strong purple | ✅ | strong purple | ✅ |
| D75_v1 | CAT02 | 5.1P 4.5/12.5 | strong purple | ✅ | strong purple | ✅ |
| D75_v1 | XYZScaling | 4.5P 4.5/12.2 | strong purple | ✅ | strong purple | ✅ |
| E_v1 | Bradford | 7.7P 4.5/11.1 | strong purple | ✅ | strong purple | ✅ |
| E_v1 | VonKries | 7.6P 4.5/11.1 | strong purple | ✅ | strong purple | ✅ |
| E_v1 | CAT02 | 7.6P 4.5/11.2 | strong purple | ✅ | strong purple | ✅ |
| E_v1 | XYZScaling | 8.2P 4.5/11.7 | strong purple | ✅ | strong purple | ✅ |
| F7_v1 | Bradford | 6.2P 4.5/11.3 | strong purple | ✅ | strong purple | ✅ |
| F7_v1 | VonKries | 6.2P 4.5/11.3 | strong purple | ✅ | strong purple | ✅ |
| F7_v1 | CAT02 | 6.2P 4.5/11.3 | strong purple | ✅ | strong purple | ✅ |
| F7_v1 | XYZScaling | 6.2P 4.5/11.3 | strong purple | ✅ | strong purple | ✅ |

#### 212. #652277 - Expected: deep purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.2P 2.7/11.8 | deep purple | ✅ | deep purple | ✅ |
| C_v1 | VonKries | 6.4P 2.7/12.0 | deep purple | ✅ | deep purple | ✅ |
| C_v1 | CAT02 | 6.2P 2.7/11.7 | deep purple | ✅ | deep purple | ✅ |
| C_v1 | XYZScaling | 6.3P 2.7/11.9 | deep purple | ✅ | deep purple | ✅ |
| D55_v1 | Bradford | 8.3P 2.7/9.8 | deep reddish purple | ❌ | deep purple | ✅ |
| D55_v1 | VonKries | 8.0P 2.7/9.5 | deep purple | ✅ | deep purple | ✅ |
| D55_v1 | CAT02 | 8.3P 2.7/9.9 | deep reddish purple | ❌ | deep purple | ✅ |
| D55_v1 | XYZScaling | 8.8P 2.7/10.1 | deep reddish purple | ❌ | deep purple | ✅ |
| D65_v1 | Bradford | 6.6P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | VonKries | 6.6P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | CAT02 | 6.6P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| D65_v1 | XYZScaling | 6.6P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | Bradford | 5.7P 2.7/12.1 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | VonKries | 5.9P 2.7/12.2 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | CAT02 | 5.7P 2.7/11.9 | deep purple | ✅ | deep purple | ✅ |
| D75_v1 | XYZScaling | 5.4P 2.7/12.0 | deep purple | ✅ | deep purple | ✅ |
| E_v1 | Bradford | 7.9P 2.7/10.5 | deep purple | ✅ | deep purple | ✅ |
| E_v1 | VonKries | 7.8P 2.7/10.5 | deep purple | ✅ | deep purple | ✅ |
| E_v1 | CAT02 | 7.8P 2.7/10.6 | deep purple | ✅ | deep purple | ✅ |
| E_v1 | XYZScaling | 8.5P 2.7/11.1 | deep reddish purple | ❌ | deep purple | ✅ |
| F7_v1 | Bradford | 6.7P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| F7_v1 | VonKries | 6.6P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| F7_v1 | CAT02 | 6.6P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |
| F7_v1 | XYZScaling | 6.7P 2.7/11.0 | deep purple | ✅ | deep purple | ✅ |

#### 213. #460A55 - Expected: very deep purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 7.0P 1.6/10.7 | very deep purple | ✅ | very deep purple | ✅ |
| C_v1 | VonKries | 7.2P 1.6/10.9 | very deep purple | ✅ | very deep purple | ✅ |
| C_v1 | CAT02 | 7.0P 1.6/10.7 | very deep purple | ✅ | very deep purple | ✅ |
| C_v1 | XYZScaling | 7.0P 1.6/10.9 | very deep purple | ✅ | very deep purple | ✅ |
| D55_v1 | Bradford | 9.0P 1.6/8.8 | very deep reddish purple | ❌ | very deep purple | ✅ |
| D55_v1 | VonKries | 8.6P 1.6/8.6 | very deep reddish purple | ❌ | very deep purple | ✅ |
| D55_v1 | CAT02 | 8.9P 1.6/9.0 | very deep reddish purple | ❌ | very deep purple | ✅ |
| D65_v1 | Bradford | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | VonKries | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | CAT02 | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| D65_v1 | XYZScaling | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | Bradford | 6.5P 1.6/11.1 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | VonKries | 6.8P 1.6/11.2 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | CAT02 | 6.6P 1.6/11.0 | very deep purple | ✅ | very deep purple | ✅ |
| D75_v1 | XYZScaling | 6.2P 1.6/11.0 | very deep purple | ✅ | very deep purple | ✅ |
| E_v1 | Bradford | 8.5P 1.6/9.4 | very deep reddish purple | ❌ | very deep purple | ✅ |
| E_v1 | VonKries | 8.4P 1.6/9.4 | very deep reddish purple | ❌ | very deep purple | ✅ |
| E_v1 | CAT02 | 8.4P 1.6/9.5 | very deep reddish purple | ❌ | very deep purple | ✅ |
| F7_v1 | Bradford | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | VonKries | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | CAT02 | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |
| F7_v1 | XYZScaling | 7.4P 1.6/10.0 | very deep purple | ✅ | very deep purple | ✅ |

#### 214. #E4B9F3 - Expected: very light purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.0P 8.0/8.2 | very light purple | ✅ | very light purple | ✅ |
| C_v1 | VonKries | 6.1P 8.0/8.3 | very light purple | ✅ | very light purple | ✅ |
| C_v1 | CAT02 | 6.0P 8.0/8.1 | very light purple | ✅ | very light purple | ✅ |
| C_v1 | XYZScaling | 6.0P 8.0/8.2 | very light purple | ✅ | very light purple | ✅ |
| D65_v1 | Bradford | 6.3P 8.0/6.9 | very light purple | ✅ | very light purple | ✅ |
| D65_v1 | VonKries | 6.3P 8.0/6.9 | very light purple | ✅ | very light purple | ✅ |
| D65_v1 | CAT02 | 6.3P 8.0/6.9 | very light purple | ✅ | very light purple | ✅ |
| D65_v1 | XYZScaling | 6.3P 8.0/6.9 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | Bradford | 3.9P 8.0/7.7 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | VonKries | 4.6P 8.0/7.9 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | CAT02 | 4.0P 8.0/7.7 | very light purple | ✅ | very light purple | ✅ |
| D75_v1 | XYZScaling | 4.0P 8.0/7.7 | very light purple | ✅ | very light purple | ✅ |
| F7_v1 | Bradford | 6.3P 8.0/6.8 | very light purple | ✅ | very light purple | ✅ |
| F7_v1 | VonKries | 6.3P 8.0/6.8 | very light purple | ✅ | very light purple | ✅ |
| F7_v1 | CAT02 | 6.3P 8.0/6.8 | very light purple | ✅ | very light purple | ✅ |
| F7_v1 | XYZScaling | 6.4P 8.0/6.8 | very light purple | ✅ | very light purple | ✅ |

#### 215. #BC93CC - Expected: light purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.7P 6.6/8.4 | light purple | ✅ | light purple | ✅ |
| C_v1 | VonKries | 5.8P 6.5/8.5 | light purple | ✅ | light purple | ✅ |
| C_v1 | CAT02 | 5.7P 6.6/8.3 | light purple | ✅ | light purple | ✅ |
| C_v1 | XYZScaling | 5.7P 6.5/8.4 | light purple | ✅ | light purple | ✅ |
| D65_v1 | Bradford | 6.0P 6.5/7.1 | light purple | ✅ | light purple | ✅ |
| D65_v1 | VonKries | 6.0P 6.5/7.1 | light purple | ✅ | light purple | ✅ |
| D65_v1 | CAT02 | 6.0P 6.5/7.1 | light purple | ✅ | light purple | ✅ |
| D65_v1 | XYZScaling | 6.0P 6.5/7.1 | light purple | ✅ | light purple | ✅ |
| D75_v1 | Bradford | 3.2P 6.6/7.8 | light purple | ✅ | light purple | ✅ |
| D75_v1 | VonKries | 3.8P 6.5/8.1 | light purple | ✅ | light purple | ✅ |
| D75_v1 | CAT02 | 3.2P 6.6/7.8 | light purple | ✅ | light purple | ✅ |
| D75_v1 | XYZScaling | 2.3P 6.5/7.5 | light purple | ✅ | light violet | ❌ |
| E_v1 | VonKries | 8.9P 6.6/7.3 | light purple | ✅ | light purple | ✅ |
| E_v1 | CAT02 | 9.0P 6.5/7.4 | light purple | ✅ | light purple | ✅ |
| F7_v1 | Bradford | 6.1P 6.5/7.0 | light purple | ✅ | light purple | ✅ |
| F7_v1 | VonKries | 6.1P 6.5/7.0 | light purple | ✅ | light purple | ✅ |
| F7_v1 | CAT02 | 6.1P 6.5/7.0 | light purple | ✅ | light purple | ✅ |
| F7_v1 | XYZScaling | 6.1P 6.5/7.0 | light purple | ✅ | light purple | ✅ |

#### 216. #875E96 - Expected: moderate purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8P 4.5/8.2 | moderate purple | ✅ | moderate purple | ✅ |
| C_v1 | VonKries | 5.9P 4.5/8.3 | moderate purple | ✅ | moderate purple | ✅ |
| C_v1 | CAT02 | 5.8P 4.5/8.1 | moderate purple | ✅ | moderate purple | ✅ |
| C_v1 | XYZScaling | 5.8P 4.5/8.2 | moderate purple | ✅ | moderate purple | ✅ |
| D55_v1 | Bradford | 9.0P 4.5/6.0 | moderate reddish purple | ❌ | moderate purple | ✅ |
| D55_v1 | VonKries | 8.7P 4.5/5.9 | moderate reddish purple | ❌ | moderate purple | ✅ |
| D55_v1 | CAT02 | 8.8P 4.5/6.1 | moderate reddish purple | ❌ | moderate purple | ✅ |
| D65_v1 | Bradford | 6.1P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | VonKries | 6.1P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | CAT02 | 6.1P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| D65_v1 | XYZScaling | 6.1P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | Bradford | 4.1P 4.5/7.9 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | VonKries | 4.8P 4.5/8.3 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | CAT02 | 4.2P 4.5/7.9 | moderate purple | ✅ | moderate purple | ✅ |
| D75_v1 | XYZScaling | 3.1P 4.5/7.5 | moderate purple | ✅ | moderate purple | ✅ |
| E_v1 | Bradford | 8.5P 4.5/7.2 | moderate reddish purple | ❌ | moderate purple | ✅ |
| E_v1 | VonKries | 8.4P 4.5/7.1 | moderate reddish purple | ❌ | moderate purple | ✅ |
| E_v1 | CAT02 | 8.4P 4.5/7.2 | moderate reddish purple | ❌ | moderate purple | ✅ |
| E_v1 | XYZScaling | 8.9P 4.5/7.6 | moderate reddish purple | ❌ | moderate purple | ✅ |
| F7_v1 | Bradford | 6.2P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | VonKries | 6.2P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | CAT02 | 6.2P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |
| F7_v1 | XYZScaling | 6.2P 4.5/7.1 | moderate purple | ✅ | moderate purple | ✅ |

#### 217. #563762 - Expected: dark purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8P 2.8/6.2 | dark purple | ✅ | dark purple | ✅ |
| C_v1 | VonKries | 6.0P 2.8/6.3 | dark purple | ✅ | dark purple | ✅ |
| C_v1 | CAT02 | 5.8P 2.8/6.1 | dark purple | ✅ | dark purple | ✅ |
| C_v1 | XYZScaling | 5.9P 2.8/6.2 | dark purple | ✅ | dark purple | ✅ |
| D55_v1 | VonKries | 8.7P 2.8/4.3 | dark purple | ✅ | dark purple | ✅ |
| D55_v1 | CAT02 | 8.9P 2.8/4.6 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | Bradford | 6.2P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | VonKries | 6.2P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | CAT02 | 6.2P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| D65_v1 | XYZScaling | 6.2P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | Bradford | 4.5P 2.8/6.1 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | VonKries | 5.1P 2.8/6.4 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | CAT02 | 4.6P 2.8/6.1 | dark purple | ✅ | dark purple | ✅ |
| D75_v1 | XYZScaling | 3.4P 2.8/5.8 | dark purple | ✅ | dark purple | ✅ |
| E_v1 | Bradford | 8.6P 2.8/5.3 | dark purple | ✅ | dark purple | ✅ |
| E_v1 | VonKries | 8.4P 2.8/5.3 | dark purple | ✅ | dark purple | ✅ |
| E_v1 | CAT02 | 8.5P 2.8/5.3 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | Bradford | 6.3P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | VonKries | 6.3P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | CAT02 | 6.3P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |
| F7_v1 | XYZScaling | 6.3P 2.8/5.4 | dark purple | ✅ | dark purple | ✅ |

#### 218. #371B41 - Expected: very dark purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.9P 1.5/5.9 | very dark purple | ✅ | very dark purple | ✅ |
| C_v1 | VonKries | 7.1P 1.5/6.0 | very dark purple | ✅ | very dark purple | ✅ |
| C_v1 | CAT02 | 6.9P 1.5/5.9 | very dark purple | ✅ | very dark purple | ✅ |
| C_v1 | XYZScaling | 6.9P 1.5/6.0 | very dark purple | ✅ | very dark purple | ✅ |
| D65_v1 | Bradford | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| D65_v1 | VonKries | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| D65_v1 | CAT02 | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| D65_v1 | XYZScaling | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v1 | Bradford | 6.1P 1.5/6.1 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v2 | Bradford | 7.5P 1.5/2.0 | very dark purple | ✅ | blackish purple | ❌ |
| D75_v1 | VonKries | 6.3P 1.5/6.2 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v2 | VonKries | 7.5P 1.5/2.0 | very dark purple | ✅ | blackish purple | ❌ |
| D75_v1 | CAT02 | 6.1P 1.5/6.0 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v2 | CAT02 | 7.5P 1.5/2.0 | very dark purple | ✅ | blackish purple | ❌ |
| D75_v1 | XYZScaling | 5.7P 1.5/6.0 | very dark purple | ✅ | very dark purple | ✅ |
| D75_v2 | XYZScaling | 5.0P 1.5/2.0 | very dark purple | ✅ | blackish purple | ❌ |
| F7_v1 | Bradford | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| F7_v1 | VonKries | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| F7_v1 | CAT02 | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |
| F7_v1 | XYZScaling | 7.3P 1.5/5.3 | very dark purple | ✅ | very dark purple | ✅ |

#### 219. #E0CBEB - Expected: very pale purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.7P 8.4/4.8 | very pale purple | ✅ | very pale purple | ✅ |
| C_v1 | VonKries | 5.8P 8.4/4.9 | very pale purple | ✅ | very pale purple | ✅ |
| C_v1 | CAT02 | 5.7P 8.4/4.8 | very pale purple | ✅ | very pale purple | ✅ |
| C_v1 | XYZScaling | 5.7P 8.4/4.8 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | Bradford | 6.0P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | VonKries | 6.0P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | CAT02 | 6.0P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| D65_v1 | XYZScaling | 6.0P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| D75_v1 | Bradford | 3.9P 8.4/4.9 | very pale purple | ✅ | very pale purple | ✅ |
| D75_v1 | VonKries | 4.2P 8.4/5.0 | very pale purple | ✅ | very pale purple | ✅ |
| D75_v1 | CAT02 | 3.9P 8.4/4.9 | very pale purple | ✅ | very pale purple | ✅ |
| D75_v1 | XYZScaling | 3.5P 8.4/4.9 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | Bradford | 6.1P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | VonKries | 6.1P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | CAT02 | 6.1P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |
| F7_v1 | XYZScaling | 6.1P 8.4/3.3 | very pale purple | ✅ | very pale purple | ✅ |

#### 220. #AD97B3 - Expected: pale purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v2 | Bradford | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| C_v2 | VonKries | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| C_v2 | CAT02 | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D50_v2 | Bradford | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D50_v2 | VonKries | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D50_v2 | CAT02 | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D50_v2 | XYZScaling | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | Bradford | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | VonKries | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | CAT02 | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D55_v2 | XYZScaling | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | Bradford | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | VonKries | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | CAT02 | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D65_v2 | XYZScaling | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | Bradford | 2.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | VonKries | 2.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | CAT02 | 2.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| D75_v2 | XYZScaling | 2.5RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | Bradford | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | VonKries | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | CAT02 | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| E_v2 | XYZScaling | 10.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | Bradford | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | VonKries | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | CAT02 | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |
| F7_v2 | XYZScaling | 5.0RP 6.4/2.0 | pale purple | ✅ | pale purple | ✅ |

#### 221. #7B667E - Expected: grayish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 6.9P 4.5/3.6 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | Bradford | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| C_v1 | VonKries | 7.0P 4.5/3.6 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | VonKries | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| C_v1 | CAT02 | 6.9P 4.5/3.6 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | CAT02 | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| C_v1 | XYZScaling | 7.0P 4.5/3.6 | grayish purple | ✅ | grayish purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D50_v2 | Bradford | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D50_v2 | VonKries | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D50_v2 | CAT02 | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D50_v2 | XYZScaling | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v1 | Bradford | 3.2RP 4.5/2.4 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | Bradford | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v1 | VonKries | 3.1RP 4.5/2.3 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | VonKries | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v1 | CAT02 | 3.0RP 4.5/2.4 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | CAT02 | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v1 | XYZScaling | 3.2RP 4.5/2.6 | grayish purple | ✅ | grayish purple | ✅ |
| D55_v2 | XYZScaling | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | Bradford | 7.9P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | Bradford | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | VonKries | 7.9P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | VonKries | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | CAT02 | 7.9P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | CAT02 | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v1 | XYZScaling | 7.9P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| D65_v2 | XYZScaling | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | Bradford | 3.6P 4.5/3.3 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | Bradford | 2.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | VonKries | 4.3P 4.5/3.4 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | VonKries | 2.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | CAT02 | 3.7P 4.5/3.3 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v2 | CAT02 | 2.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| D75_v1 | XYZScaling | 2.7P 4.5/3.2 | grayish purple | ✅ | pale violet | ❌ |
| D75_v2 | XYZScaling | 2.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | Bradford | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | VonKries | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | CAT02 | 7.5RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| E_v2 | XYZScaling | 10.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | Bradford | 8.0P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | Bradford | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | VonKries | 7.9P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | VonKries | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | CAT02 | 7.9P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | CAT02 | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v1 | XYZScaling | 8.0P 4.5/2.7 | grayish purple | ✅ | grayish purple | ✅ |
| F7_v2 | XYZScaling | 5.0RP 4.5/2.0 | grayish purple | ✅ | grayish purple | ✅ |

#### 222. #513F51 - Expected: dark grayish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.3P 2.9/2.5 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | Bradford | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v1 | VonKries | 8.4P 2.9/2.5 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | VonKries | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v1 | CAT02 | 8.3P 2.9/2.4 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | CAT02 | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v1 | XYZScaling | 8.4P 2.9/2.5 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v1 | Bradford | 9.9RP 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v2 | Bradford | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v1 | VonKries | 0.1R 2.9/1.8 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v2 | VonKries | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v1 | CAT02 | 9.4RP 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v2 | CAT02 | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v1 | XYZScaling | 9.4RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D50_v2 | XYZScaling | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v1 | Bradford | 4.4RP 2.9/1.8 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | Bradford | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v1 | VonKries | 4.3RP 2.9/1.7 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | VonKries | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v1 | CAT02 | 4.3RP 2.9/1.8 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | CAT02 | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v1 | XYZScaling | 4.4RP 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D55_v2 | XYZScaling | 10.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v1 | Bradford | 9.6P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | Bradford | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v1 | VonKries | 9.6P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | VonKries | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v1 | CAT02 | 9.6P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | CAT02 | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v1 | XYZScaling | 9.6P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D65_v2 | XYZScaling | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | Bradford | 5.9P 2.9/2.3 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | Bradford | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | VonKries | 6.1P 2.9/2.4 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | VonKries | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | CAT02 | 5.9P 2.9/2.3 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | CAT02 | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v1 | XYZScaling | 5.7P 2.9/2.3 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| D75_v2 | XYZScaling | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | Bradford | 3.1RP 2.9/2.3 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | Bradford | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | VonKries | 3.0RP 2.9/2.3 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | VonKries | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | CAT02 | 3.0RP 2.9/2.3 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | CAT02 | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v1 | XYZScaling | 3.1RP 2.9/2.5 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| E_v2 | XYZScaling | 7.5RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v1 | Bradford | 9.7P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | Bradford | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v1 | VonKries | 9.7P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | VonKries | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v1 | CAT02 | 9.7P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | CAT02 | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v1 | XYZScaling | 9.7P 2.9/1.9 | dark grayish purple | ✅ | dark grayish purple | ✅ |
| F7_v2 | XYZScaling | 5.0RP 2.9/2.0 | dark grayish purple | ✅ | dark grayish purple | ✅ |

#### 223. #2F2231 - Expected: blackish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 8.3P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | Bradford | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| C_v1 | VonKries | 8.5P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | VonKries | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| C_v1 | CAT02 | 8.3P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | CAT02 | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| C_v1 | XYZScaling | 8.4P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| C_v2 | XYZScaling | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v1 | Bradford | 0.5R 1.5/1.3 | blackish red | ❌ | blackish purple | ✅ |
| D50_v2 | Bradford | 10.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v1 | VonKries | 0.4R 1.5/1.3 | blackish red | ❌ | blackish purple | ✅ |
| D50_v2 | VonKries | 10.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v1 | CAT02 | 0.1R 1.5/1.3 | blackish red | ❌ | blackish purple | ✅ |
| D50_v2 | CAT02 | 10.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D50_v1 | XYZScaling | 0.5R 1.5/1.4 | blackish red | ❌ | blackish purple | ✅ |
| D50_v2 | XYZScaling | 10.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | Bradford | 5.4RP 1.5/1.3 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | Bradford | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | VonKries | 5.1RP 1.5/1.3 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | VonKries | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | CAT02 | 5.1RP 1.5/1.4 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | CAT02 | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D55_v1 | XYZScaling | 5.7RP 1.5/1.4 | blackish purple | ✅ | blackish purple | ✅ |
| D55_v2 | XYZScaling | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | Bradford | 9.2P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | Bradford | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | VonKries | 9.2P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | VonKries | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | CAT02 | 9.2P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | CAT02 | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D65_v1 | XYZScaling | 9.2P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| D65_v2 | XYZScaling | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| D75_v1 | Bradford | 6.3P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | Bradford | 2.5RP 1.5/2.0 | very dark reddish purple | ❌ | blackish purple | ✅ |
| D75_v1 | VonKries | 6.5P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | VonKries | 2.5RP 1.5/2.0 | very dark reddish purple | ❌ | blackish purple | ✅ |
| D75_v1 | CAT02 | 6.3P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | CAT02 | 2.5RP 1.5/2.0 | very dark reddish purple | ❌ | blackish purple | ✅ |
| D75_v1 | XYZScaling | 6.0P 1.5/1.9 | blackish purple | ✅ | blackish purple | ✅ |
| D75_v2 | XYZScaling | 2.5RP 1.5/2.0 | very dark reddish purple | ❌ | blackish purple | ✅ |
| E_v1 | Bradford | 3.8RP 1.5/1.7 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | Bradford | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | VonKries | 3.7RP 1.5/1.7 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | VonKries | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | CAT02 | 3.7RP 1.5/1.7 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | CAT02 | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| E_v1 | XYZScaling | 4.1RP 1.5/1.8 | blackish purple | ✅ | blackish purple | ✅ |
| E_v2 | XYZScaling | 7.5RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | Bradford | 9.3P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | Bradford | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | VonKries | 9.3P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | VonKries | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | CAT02 | 9.3P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | CAT02 | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |
| F7_v1 | XYZScaling | 9.3P 1.5/1.6 | blackish purple | ✅ | blackish purple | ✅ |
| F7_v2 | XYZScaling | 5.0RP 1.5/2.0 | very dark purplish red | ❌ | blackish purple | ✅ |

#### 224. #EBDFEF - Expected: purplish white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.4P 9.0/1.0 | purplish white | ✅ | purplish white | ✅ |
| D65_v1 | VonKries | 8.4P 9.0/1.0 | purplish white | ✅ | purplish white | ✅ |
| D65_v1 | CAT02 | 8.4P 9.0/1.0 | purplish white | ✅ | purplish white | ✅ |
| D65_v1 | XYZScaling | 8.4P 9.0/1.0 | purplish white | ✅ | purplish white | ✅ |
| F7_v1 | Bradford | 9.1P 9.0/0.9 | purplish white | ✅ | purplish white | ✅ |
| F7_v1 | VonKries | 9.1P 9.0/0.9 | purplish white | ✅ | purplish white | ✅ |
| F7_v1 | CAT02 | 9.0P 9.0/0.9 | purplish white | ✅ | purplish white | ✅ |
| F7_v1 | XYZScaling | 9.1P 9.0/0.9 | purplish white | ✅ | purplish white | ✅ |

#### 225. #C3B7C6 - Expected: light purplish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.6P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| D65_v1 | VonKries | 8.6P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| D65_v1 | CAT02 | 8.6P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| D65_v1 | XYZScaling | 8.6P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| F7_v1 | Bradford | 9.0P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| F7_v1 | VonKries | 9.0P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| F7_v1 | CAT02 | 9.0P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |
| F7_v1 | XYZScaling | 9.0P 7.5/1.1 | light purplish gray | ✅ | light purplish gray | ✅ |

#### 226. #8F8490 - Expected: purplish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| D65_v1 | VonKries | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| D65_v1 | CAT02 | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| D65_v1 | XYZScaling | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| F7_v1 | Bradford | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| F7_v1 | VonKries | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| F7_v1 | CAT02 | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |
| F7_v1 | XYZScaling | 0.5RP 5.5/0.9 | purplish gray | ✅ | purplish gray | ✅ |

#### 227. #5C525E - Expected: dark purplish gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.3P 3.6/1.0 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| D65_v1 | VonKries | 8.3P 3.6/1.0 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| D65_v1 | CAT02 | 8.3P 3.6/1.0 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| D65_v1 | XYZScaling | 8.3P 3.6/1.0 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| F7_v1 | Bradford | 8.5P 3.6/0.9 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| F7_v1 | VonKries | 8.5P 3.6/0.9 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| F7_v1 | CAT02 | 8.5P 3.6/0.9 | dark purplish gray | ✅ | dark purplish gray | ✅ |
| F7_v1 | XYZScaling | 8.5P 3.6/0.9 | dark purplish gray | ✅ | dark purplish gray | ✅ |

#### 228. #2B2630 - Expected: purplish black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D55_v1 | Bradford | 6.4RP 1.6/0.6 | purplish black | ✅ | purplish black | ✅ |
| D55_v1 | VonKries | 6.1RP 1.6/0.5 | purplish black | ✅ | purplish black | ✅ |
| D55_v1 | CAT02 | 6.0RP 1.6/0.6 | purplish black | ✅ | purplish black | ✅ |
| D55_v1 | XYZScaling | 6.9RP 1.6/0.6 | purplish black | ✅ | purplish black | ✅ |
| D65_v1 | Bradford | 4.2P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| D65_v1 | VonKries | 4.2P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| D65_v1 | CAT02 | 4.2P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| D65_v1 | XYZScaling | 4.2P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| E_v1 | Bradford | 3.1RP 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| E_v1 | VonKries | 2.9RP 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| E_v1 | CAT02 | 3.0RP 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| F7_v1 | Bradford | 4.4P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| F7_v1 | VonKries | 4.4P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| F7_v1 | CAT02 | 4.4P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |
| F7_v1 | XYZScaling | 4.5P 1.6/0.9 | purplish black | ✅ | purplish black | ✅ |

#### 229. #D429B9 - Expected: vivid reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.8P 5.0/19.7 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| C_v1 | VonKries | 9.8P 5.0/20.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| C_v1 | CAT02 | 9.8P 5.0/19.6 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| C_v1 | XYZScaling | 9.8P 5.0/20.2 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | Bradford | 1.5RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | VonKries | 1.4RP 5.0/18.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | CAT02 | 1.4RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D50_v1 | XYZScaling | 1.5RP 5.0/19.8 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D55_v1 | Bradford | 1.1RP 5.0/18.4 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D55_v1 | VonKries | 1.1RP 5.0/18.0 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D55_v1 | CAT02 | 1.1RP 5.0/18.5 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D55_v1 | XYZScaling | 1.1RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | Bradford | 0.2RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | VonKries | 0.2RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | CAT02 | 0.2RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D65_v1 | XYZScaling | 0.2RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | Bradford | 9.3P 5.0/19.6 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | VonKries | 9.4P 5.0/19.8 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | CAT02 | 9.3P 5.0/19.4 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.2P 5.0/19.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | Bradford | 1.0RP 5.0/19.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | VonKries | 1.0RP 5.0/19.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | CAT02 | 1.0RP 5.0/19.1 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| E_v1 | XYZScaling | 1.0RP 5.0/20.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F2_v1 | Bradford | 2.6RP 5.0/21.2 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F2_v1 | VonKries | 2.4RP 5.0/19.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F2_v1 | CAT02 | 2.4RP 5.0/21.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F2_v1 | XYZScaling | 2.6RP 5.0/23.3 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | Bradford | 0.3RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | VonKries | 0.3RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | CAT02 | 0.3RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F7_v1 | XYZScaling | 0.3RP 5.0/18.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F11_v1 | Bradford | 3.0RP 5.0/21.8 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F11_v1 | VonKries | 2.7RP 5.0/20.5 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F11_v1 | CAT02 | 2.7RP 5.0/21.9 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |
| F11_v1 | XYZScaling | 2.9RP 5.0/24.4 | vivid reddish purple | ✅ | vivid reddish purple | ✅ |

#### 230. #A74994 - Expected: strong reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1RP 4.5/12.0 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| C_v1 | VonKries | 0.1RP 4.5/12.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| C_v1 | CAT02 | 0.1RP 4.5/11.9 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| C_v1 | XYZScaling | 0.1RP 4.5/12.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D50_v1 | Bradford | 2.5RP 4.5/11.4 | strong purplish red | ❌ | strong reddish purple | ✅ |
| D50_v1 | VonKries | 2.4RP 4.5/10.9 | moderate purplish red | ❌ | strong reddish purple | ✅ |
| D50_v1 | CAT02 | 2.4RP 4.5/11.4 | strong purplish red | ❌ | strong reddish purple | ✅ |
| D50_v1 | XYZScaling | 2.5RP 4.5/11.9 | strong purplish red | ❌ | strong reddish purple | ✅ |
| D55_v1 | Bradford | 1.9RP 4.5/11.0 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D55_v1 | VonKries | 1.8RP 4.5/10.7 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D55_v1 | CAT02 | 1.8RP 4.5/11.0 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D55_v1 | XYZScaling | 1.9RP 4.5/11.3 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D65_v1 | Bradford | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D65_v1 | VonKries | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D65_v1 | CAT02 | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D65_v1 | XYZScaling | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | Bradford | 9.3P 4.5/11.8 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | VonKries | 9.5P 4.5/12.0 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | CAT02 | 9.4P 4.5/11.8 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.3P 4.5/11.7 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| E_v1 | Bradford | 1.6RP 4.5/11.7 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| E_v1 | VonKries | 1.5RP 4.5/11.7 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| E_v1 | CAT02 | 1.5RP 4.5/11.6 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| E_v1 | XYZScaling | 1.6RP 4.5/12.3 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| F7_v1 | Bradford | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| F7_v1 | VonKries | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| F7_v1 | CAT02 | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |
| F7_v1 | XYZScaling | 0.7RP 4.5/11.2 | strong reddish purple | ✅ | strong reddish purple | ✅ |

#### 231. #761A6A - Expected: deep reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1RP 2.8/10.9 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| C_v1 | VonKries | 0.2RP 2.8/11.2 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| C_v1 | CAT02 | 0.1RP 2.8/10.9 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| C_v1 | XYZScaling | 0.2RP 2.8/11.2 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D50_v1 | VonKries | 2.8RP 2.8/9.8 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D50_v1 | CAT02 | 2.9RP 2.8/10.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | Bradford | 2.0RP 2.8/10.2 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | VonKries | 1.9RP 2.8/10.0 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | CAT02 | 2.0RP 2.8/10.3 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.1RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | Bradford | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | VonKries | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | CAT02 | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D65_v1 | XYZScaling | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | Bradford | 9.6P 2.8/11.0 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | VonKries | 9.7P 2.8/11.1 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | CAT02 | 9.6P 2.8/10.9 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.5P 2.8/10.8 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | Bradford | 1.6RP 2.8/10.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | VonKries | 1.5RP 2.8/10.7 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | CAT02 | 1.6RP 2.8/10.6 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| E_v1 | XYZScaling | 1.8RP 2.8/11.4 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | Bradford | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | VonKries | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | CAT02 | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |
| F7_v1 | XYZScaling | 0.6RP 2.8/10.5 | deep reddish purple | ✅ | deep reddish purple | ✅ |

#### 232. #4F094A - Expected: very deep reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.5RP 1.7/8.9 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| C_v1 | VonKries | 0.6RP 1.7/9.1 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| C_v1 | CAT02 | 0.5RP 1.7/8.9 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| C_v1 | XYZScaling | 0.6RP 1.7/9.1 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D55_v1 | VonKries | 3.0RP 1.7/8.0 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D65_v1 | Bradford | 1.1RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D65_v1 | VonKries | 1.1RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D65_v1 | CAT02 | 1.1RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.1RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D75_v1 | Bradford | 9.8P 1.7/8.9 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D75_v1 | VonKries | 10.0P 1.7/9.0 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D75_v1 | CAT02 | 9.8P 1.7/8.9 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.7P 1.7/8.8 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| E_v1 | Bradford | 2.6RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| E_v1 | VonKries | 2.4RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| E_v1 | CAT02 | 2.5RP 1.7/8.6 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| E_v1 | XYZScaling | 3.0RP 1.7/9.1 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| F7_v1 | Bradford | 1.2RP 1.7/8.5 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| F7_v1 | VonKries | 1.2RP 1.7/8.5 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| F7_v1 | CAT02 | 1.2RP 1.7/8.5 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.2RP 1.7/8.5 | very deep reddish purple | ✅ | very deep reddish purple | ✅ |

#### 233. #BD80AE - Expected: light reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.9P 6.0/8.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| C_v1 | VonKries | 9.9P 6.0/8.3 | light reddish purple | ✅ | light reddish purple | ✅ |
| C_v1 | CAT02 | 9.9P 6.0/8.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| C_v1 | XYZScaling | 9.9P 6.0/8.4 | light reddish purple | ✅ | light reddish purple | ✅ |
| D55_v1 | Bradford | 2.4RP 6.0/7.4 | dark purplish pink | ❌ | light reddish purple | ✅ |
| D55_v1 | VonKries | 2.4RP 6.0/7.2 | dark purplish pink | ❌ | light reddish purple | ✅ |
| D55_v1 | CAT02 | 2.4RP 6.0/7.4 | dark purplish pink | ❌ | light reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.4RP 6.0/7.6 | dark purplish pink | ❌ | light reddish purple | ✅ |
| D65_v1 | Bradford | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | VonKries | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | CAT02 | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| E_v1 | Bradford | 1.7RP 6.0/8.3 | light reddish purple | ✅ | light reddish purple | ✅ |
| E_v1 | VonKries | 1.7RP 6.0/8.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| E_v1 | CAT02 | 1.7RP 6.0/8.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| E_v1 | XYZScaling | 1.7RP 6.0/8.8 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | Bradford | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | VonKries | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | CAT02 | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.2RP 6.0/7.2 | light reddish purple | ✅ | light reddish purple | ✅ |

#### 234. #965888 - Expected: moderate reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1RP 4.5/8.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| C_v1 | VonKries | 0.1RP 4.5/8.1 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| C_v1 | CAT02 | 0.1RP 4.5/8.0 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| C_v1 | XYZScaling | 0.1RP 4.5/8.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D55_v1 | Bradford | 2.4RP 4.5/7.1 | moderate purplish red | ❌ | moderate reddish purple | ✅ |
| D55_v1 | VonKries | 2.4RP 4.5/6.9 | grayish purplish red | ❌ | moderate reddish purple | ✅ |
| D55_v1 | CAT02 | 2.4RP 4.5/7.1 | moderate purplish red | ❌ | moderate reddish purple | ✅ |
| D55_v1 | XYZScaling | 2.4RP 4.5/7.3 | moderate purplish red | ❌ | moderate reddish purple | ✅ |
| D65_v1 | Bradford | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D65_v1 | VonKries | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D65_v1 | CAT02 | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D65_v1 | XYZScaling | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | Bradford | 9.0P 4.5/7.8 | moderate reddish purple | ✅ | moderate purple | ❌ |
| D75_v1 | VonKries | 9.1P 4.5/7.9 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | CAT02 | 9.0P 4.5/7.8 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| D75_v1 | XYZScaling | 8.9P 4.5/7.7 | moderate reddish purple | ✅ | moderate purple | ❌ |
| E_v1 | Bradford | 2.0RP 4.5/7.8 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| E_v1 | VonKries | 1.9RP 4.5/7.8 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| E_v1 | CAT02 | 2.0RP 4.5/7.8 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| E_v1 | XYZScaling | 2.0RP 4.5/8.3 | moderate purplish red | ❌ | moderate reddish purple | ✅ |
| F7_v1 | Bradford | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| F7_v1 | VonKries | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| F7_v1 | CAT02 | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |
| F7_v1 | XYZScaling | 0.9RP 4.5/7.2 | moderate reddish purple | ✅ | moderate reddish purple | ✅ |

#### 235. #5F3458 - Expected: dark reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.1RP 2.8/5.6 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| C_v1 | VonKries | 0.1RP 2.8/5.7 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| C_v1 | CAT02 | 0.1RP 2.8/5.6 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| C_v1 | XYZScaling | 0.2RP 2.8/5.7 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | Bradford | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | VonKries | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | CAT02 | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D65_v1 | XYZScaling | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | Bradford | 9.1P 2.8/5.5 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | VonKries | 9.3P 2.8/5.6 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| D75_v1 | CAT02 | 9.1P 2.8/5.5 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| E_v1 | Bradford | 2.5RP 2.8/5.4 | dark purplish red | ❌ | dark reddish purple | ✅ |
| E_v1 | VonKries | 2.3RP 2.8/5.4 | dark purplish red | ❌ | dark reddish purple | ✅ |
| E_v1 | CAT02 | 2.4RP 2.8/5.4 | dark purplish red | ❌ | dark reddish purple | ✅ |
| E_v1 | XYZScaling | 2.6RP 2.8/5.8 | dark purplish red | ❌ | dark reddish purple | ✅ |
| F7_v1 | Bradford | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | VonKries | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | CAT02 | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |
| F7_v1 | XYZScaling | 0.8RP 2.8/5.0 | dark reddish purple | ✅ | dark reddish purple | ✅ |

#### 236. #3F183C - Expected: very dark reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.7RP 1.5/5.6 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| C_v1 | VonKries | 0.8RP 1.5/5.7 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| C_v1 | CAT02 | 0.7RP 1.5/5.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| C_v1 | XYZScaling | 0.8RP 1.5/5.7 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | Bradford | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | VonKries | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | CAT02 | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | Bradford | 9.7P 1.5/5.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | VonKries | 9.9P 1.5/5.6 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | CAT02 | 9.7P 1.5/5.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v1 | XYZScaling | 9.5P 1.5/5.5 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| D75_v2 | XYZScaling | 2.5RP 1.5/2.0 | very dark reddish purple | ✅ | blackish purple | ❌ |
| F7_v1 | Bradford | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | VonKries | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | CAT02 | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.5RP 1.5/5.1 | very dark reddish purple | ✅ | very dark reddish purple | ✅ |

#### 237. #AD89A5 - Expected: pale reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 0.7RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | VonKries | 0.7RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | CAT02 | 0.7RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| D65_v1 | XYZScaling | 0.7RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | Bradford | 0.8RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | VonKries | 0.8RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | CAT02 | 0.8RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |
| F7_v1 | XYZScaling | 0.8RP 6.0/4.1 | pale reddish purple | ✅ | pale reddish purple | ✅ |

#### 238. #86627E - Expected: grayish reddish purple

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.8P 4.5/4.8 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| C_v1 | VonKries | 9.9P 4.5/4.8 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| C_v1 | CAT02 | 9.8P 4.5/4.7 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| C_v1 | XYZScaling | 9.9P 4.5/4.9 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | Bradford | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | VonKries | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | CAT02 | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| D65_v1 | XYZScaling | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| E_v1 | Bradford | 2.6RP 4.5/4.8 | grayish purplish red | ❌ | grayish reddish purple | ✅ |
| E_v1 | VonKries | 2.5RP 4.5/4.8 | grayish purplish red | ❌ | grayish reddish purple | ✅ |
| E_v1 | CAT02 | 2.5RP 4.5/4.8 | grayish purplish red | ❌ | grayish reddish purple | ✅ |
| F7_v1 | Bradford | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | VonKries | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | CAT02 | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |
| F7_v1 | XYZScaling | 1.1RP 4.5/4.0 | grayish reddish purple | ✅ | grayish reddish purple | ✅ |

#### 239. #FCA1E7 - Expected: brilliant purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.4P 7.7/11.2 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| C_v1 | VonKries | 9.4P 7.7/11.4 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| C_v1 | CAT02 | 9.4P 7.7/11.2 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| C_v1 | XYZScaling | 9.5P 7.7/11.4 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D50_v1 | Bradford | 3.2RP 7.7/10.9 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D50_v1 | VonKries | 3.1RP 7.7/10.5 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D50_v1 | CAT02 | 3.1RP 7.7/10.9 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D50_v1 | XYZScaling | 3.1RP 7.7/11.3 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D55_v1 | Bradford | 1.6RP 7.7/10.2 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D55_v1 | VonKries | 1.6RP 7.7/10.0 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D55_v1 | CAT02 | 1.6RP 7.7/10.2 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D55_v1 | XYZScaling | 1.6RP 7.7/10.4 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D65_v1 | Bradford | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D65_v1 | VonKries | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D65_v1 | CAT02 | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| D65_v1 | XYZScaling | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| E_v1 | Bradford | 1.1RP 7.7/11.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| E_v1 | VonKries | 1.0RP 7.7/11.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| E_v1 | CAT02 | 1.0RP 7.7/11.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| E_v1 | XYZScaling | 1.1RP 7.7/11.7 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| F2_v1 | XYZScaling | 8.4RP 7.7/11.4 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| F7_v1 | Bradford | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| F7_v1 | VonKries | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| F7_v1 | CAT02 | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |
| F7_v1 | XYZScaling | 0.0RP 7.7/10.1 | brilliant purplish pink | ✅ | brilliant purplish pink | ✅ |

#### 240. #F483CD - Expected: strong purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.8RP 6.9/13.1 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| C_v1 | VonKries | 0.8RP 6.8/13.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| C_v1 | CAT02 | 0.8RP 6.9/13.0 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| C_v1 | XYZScaling | 0.8RP 6.8/13.4 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D50_v1 | Bradford | 3.1RP 6.9/14.0 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D50_v1 | VonKries | 3.2RP 6.9/13.6 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D50_v1 | CAT02 | 6.3RP 6.8/11.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D50_v1 | XYZScaling | 3.1RP 6.8/14.4 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D55_v1 | Bradford | 2.3RP 6.9/13.1 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D55_v1 | VonKries | 2.2RP 6.9/12.8 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D55_v1 | CAT02 | 2.2RP 6.8/13.1 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D55_v1 | XYZScaling | 2.3RP 6.8/13.3 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | Bradford | 1.0RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | VonKries | 1.0RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | CAT02 | 1.0RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D65_v1 | XYZScaling | 1.0RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D75_v1 | Bradford | 0.1RP 6.8/12.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D75_v1 | VonKries | 0.2RP 6.8/12.8 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D75_v1 | CAT02 | 0.1RP 6.9/12.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| D75_v1 | XYZScaling | 0.1RP 6.8/12.6 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| E_v1 | Bradford | 1.7RP 6.9/13.8 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| E_v1 | VonKries | 1.6RP 6.9/13.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| E_v1 | CAT02 | 1.6RP 6.9/13.7 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| E_v1 | XYZScaling | 1.7RP 6.8/14.5 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F2_v1 | Bradford | 5.9RP 6.9/15.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | Bradford | 1.1RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | VonKries | 1.1RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | CAT02 | 1.1RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F7_v1 | XYZScaling | 1.1RP 6.8/12.2 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F11_v1 | VonKries | 9.0RP 6.9/12.9 | strong purplish pink | ✅ | strong purplish pink | ✅ |
| F11_v1 | CAT02 | 6.1RP 6.9/15.8 | strong purplish pink | ✅ | strong purplish pink | ✅ |

#### 241. #DF6AAC - Expected: deep purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.4RP 6.0/13.3 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| C_v1 | VonKries | 1.4RP 6.0/13.4 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| C_v1 | CAT02 | 1.4RP 6.0/13.2 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| C_v1 | XYZScaling | 1.4RP 6.0/13.7 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D50_v1 | Bradford | 4.1RP 6.0/15.0 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D50_v1 | VonKries | 4.0RP 6.0/14.7 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | Bradford | 3.2RP 6.0/14.1 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | VonKries | 3.2RP 6.0/13.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | CAT02 | 3.2RP 6.0/14.1 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D55_v1 | XYZScaling | 3.2RP 6.0/14.2 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | Bradford | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | VonKries | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | CAT02 | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D65_v1 | XYZScaling | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | Bradford | 1.2RP 6.0/12.6 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | VonKries | 1.2RP 6.0/12.7 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | CAT02 | 1.2RP 6.0/12.5 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| D75_v1 | XYZScaling | 1.2RP 6.0/12.5 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| E_v1 | Bradford | 2.7RP 6.0/14.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| E_v1 | VonKries | 2.5RP 6.0/15.0 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| E_v1 | CAT02 | 2.6RP 6.0/14.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F2_v1 | VonKries | 8.1RP 6.0/14.1 | deep pink | ❌ | deep purplish pink | ✅ |
| F7_v1 | Bradford | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | VonKries | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | CAT02 | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |
| F7_v1 | XYZScaling | 1.8RP 6.0/12.9 | deep purplish pink | ✅ | deep purplish pink | ✅ |

#### 242. #F5B2DB - Expected: light purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.3RP 7.9/7.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| C_v1 | VonKries | 0.3RP 7.9/7.9 | light purplish pink | ✅ | light purplish pink | ✅ |
| C_v1 | CAT02 | 0.3RP 7.9/7.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| C_v1 | XYZScaling | 0.4RP 7.9/8.0 | light purplish pink | ✅ | light purplish pink | ✅ |
| D55_v1 | VonKries | 4.8RP 7.9/7.4 | light purplish pink | ✅ | light purplish pink | ✅ |
| D55_v1 | CAT02 | 4.7RP 7.9/7.6 | light purplish pink | ✅ | light purplish pink | ✅ |
| D55_v1 | XYZScaling | 4.7RP 7.9/7.7 | light purplish pink | ✅ | light purplish pink | ✅ |
| D65_v1 | Bradford | 1.1RP 7.9/6.9 | light purplish pink | ✅ | light purplish pink | ✅ |
| D65_v1 | VonKries | 1.1RP 7.9/6.9 | light purplish pink | ✅ | light purplish pink | ✅ |
| D65_v1 | CAT02 | 1.1RP 7.9/6.9 | light purplish pink | ✅ | light purplish pink | ✅ |
| D65_v1 | XYZScaling | 1.1RP 7.9/6.9 | light purplish pink | ✅ | light purplish pink | ✅ |
| D75_v1 | Bradford | 9.2P 7.9/7.3 | light purplish pink | ✅ | light purplish pink | ✅ |
| D75_v1 | VonKries | 9.3P 7.9/7.3 | light purplish pink | ✅ | light purplish pink | ✅ |
| D75_v1 | CAT02 | 9.2P 7.9/7.2 | light purplish pink | ✅ | light purplish pink | ✅ |
| D75_v1 | XYZScaling | 9.2P 7.9/7.2 | light purplish pink | ✅ | light purplish pink | ✅ |
| E_v1 | Bradford | 2.9RP 7.9/8.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| E_v1 | VonKries | 2.8RP 7.9/8.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| E_v1 | CAT02 | 2.8RP 7.9/8.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| F7_v1 | Bradford | 1.1RP 7.9/6.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| F7_v1 | VonKries | 1.1RP 7.9/6.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| F7_v1 | CAT02 | 1.1RP 7.9/6.8 | light purplish pink | ✅ | light purplish pink | ✅ |
| F7_v1 | XYZScaling | 1.1RP 7.9/6.8 | light purplish pink | ✅ | light purplish pink | ✅ |

#### 243. #DE98BF - Expected: moderate purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 1.0RP 7.0/8.1 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| C_v1 | VonKries | 1.0RP 7.0/8.2 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| C_v1 | CAT02 | 1.0RP 7.0/8.1 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| C_v1 | XYZScaling | 1.1RP 7.0/8.3 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D55_v1 | VonKries | 5.3RP 7.0/7.9 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | Bradford | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | VonKries | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | CAT02 | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D65_v1 | XYZScaling | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | Bradford | 0.2RP 7.0/7.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | VonKries | 0.3RP 7.0/7.6 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | CAT02 | 0.2RP 7.0/7.5 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| D75_v1 | XYZScaling | 0.2RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | Bradford | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | VonKries | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | CAT02 | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |
| F7_v1 | XYZScaling | 1.6RP 7.0/7.4 | moderate purplish pink | ✅ | moderate purplish pink | ✅ |

#### 244. #C67D9D - Expected: dark purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.0RP 6.0/8.5 | dark purplish pink | ✅ | light reddish purple | ❌ |
| C_v1 | VonKries | 2.0RP 6.0/8.6 | dark purplish pink | ✅ | light reddish purple | ❌ |
| C_v1 | CAT02 | 2.0RP 6.0/8.5 | dark purplish pink | ✅ | light reddish purple | ❌ |
| C_v1 | XYZScaling | 2.0RP 6.0/8.8 | dark purplish pink | ✅ | light reddish purple | ❌ |
| D55_v1 | Bradford | 6.4RP 6.0/8.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D55_v1 | XYZScaling | 6.3RP 6.0/8.8 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| D65_v1 | Bradford | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | light reddish purple | ❌ |
| D65_v1 | VonKries | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | light reddish purple | ❌ |
| D65_v1 | CAT02 | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | light reddish purple | ❌ |
| D65_v1 | XYZScaling | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | light reddish purple | ❌ |
| F7_v1 | Bradford | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | VonKries | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | CAT02 | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | dark purplish pink | ✅ |
| F7_v1 | XYZScaling | 3.0RP 6.0/8.1 | dark purplish pink | ✅ | dark purplish pink | ✅ |

#### 245. #EBC8DF - Expected: pale purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.8P 8.4/4.6 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v2 | Bradford | 7.5RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v1 | VonKries | 9.8P 8.4/4.6 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v2 | VonKries | 7.5RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v1 | CAT02 | 9.8P 8.4/4.6 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v2 | CAT02 | 7.5RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v1 | XYZScaling | 9.8P 8.4/4.7 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| C_v2 | XYZScaling | 7.5RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D65_v1 | Bradford | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D65_v1 | VonKries | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D65_v1 | CAT02 | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D65_v1 | XYZScaling | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D75_v2 | Bradford | 5.0RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D75_v2 | VonKries | 5.0RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D75_v2 | CAT02 | 5.0RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| D75_v2 | XYZScaling | 5.0RP 8.4/2.0 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| F7_v1 | Bradford | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| F7_v1 | VonKries | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| F7_v1 | CAT02 | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |
| F7_v1 | XYZScaling | 1.5RP 8.4/3.5 | pale purplish pink | ✅ | pale purplish pink | ✅ |

#### 246. #C7A3B9 - Expected: grayish purplish pink

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 0.5RP 7.0/4.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v2 | Bradford | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v1 | VonKries | 0.5RP 7.0/4.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v2 | VonKries | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v1 | CAT02 | 0.5RP 7.0/4.6 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v2 | CAT02 | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v1 | XYZScaling | 0.5RP 7.0/4.8 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| C_v2 | XYZScaling | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D65_v1 | Bradford | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D65_v1 | VonKries | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D65_v1 | CAT02 | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D65_v1 | XYZScaling | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | Bradford | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | VonKries | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | CAT02 | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| D75_v2 | XYZScaling | 7.5RP 7.0/2.0 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| F7_v1 | Bradford | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| F7_v1 | VonKries | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| F7_v1 | CAT02 | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |
| F7_v1 | XYZScaling | 1.7RP 7.0/3.7 | grayish purplish pink | ✅ | grayish purplish pink | ✅ |

#### 247. #DD2388 - Expected: vivid purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 6.2RP 4.9/21.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D50_v1 | VonKries | 5.9RP 4.9/21.3 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D50_v1 | CAT02 | 6.0RP 4.9/21.5 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D50_v1 | XYZScaling | 5.9RP 4.9/22.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | Bradford | 4.6RP 4.9/22.7 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | VonKries | 4.6RP 4.9/22.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | CAT02 | 4.6RP 4.9/22.6 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D55_v1 | XYZScaling | 4.6RP 4.9/22.6 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | Bradford | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | VonKries | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | CAT02 | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| D65_v1 | XYZScaling | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | Bradford | 4.2RP 5.0/22.9 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | VonKries | 4.1RP 4.9/23.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | CAT02 | 4.2RP 4.9/22.9 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| E_v1 | XYZScaling | 4.1RP 4.9/24.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F2_v1 | Bradford | 8.7RP 5.0/19.7 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F2_v1 | VonKries | 8.2RP 4.9/20.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F2_v1 | CAT02 | 8.3RP 5.0/20.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F2_v1 | XYZScaling | 8.0RP 4.9/21.9 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | Bradford | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | VonKries | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | CAT02 | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F7_v1 | XYZScaling | 3.3RP 4.9/21.1 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F11_v1 | Bradford | 9.2RP 5.0/19.6 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F11_v1 | VonKries | 8.6RP 4.9/20.2 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F11_v1 | CAT02 | 8.8RP 5.0/20.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |
| F11_v1 | XYZScaling | 9.7RP 4.9/36.0 | vivid purplish red | ✅ | vivid purplish red | ✅ |

#### 248. #B83773 - Expected: strong purplish red

No matches

#### 249. #881055 - Expected: deep purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 3.9RP 3.0/12.6 | deep purplish red | ✅ | deep purplish red | ✅ |
| C_v1 | VonKries | 3.9RP 3.0/12.8 | deep purplish red | ✅ | deep purplish red | ✅ |
| C_v1 | CAT02 | 3.9RP 3.0/12.6 | deep purplish red | ✅ | deep purplish red | ✅ |
| D50_v1 | Bradford | 7.0RP 3.0/12.9 | deep purplish red | ✅ | deep purplish red | ✅ |
| D50_v1 | VonKries | 6.8RP 3.0/12.9 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | Bradford | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | VonKries | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | CAT02 | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| D65_v1 | XYZScaling | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | Bradford | 3.6RP 3.0/12.1 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | VonKries | 3.7RP 3.0/12.2 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | CAT02 | 3.7RP 3.0/12.0 | deep purplish red | ✅ | deep purplish red | ✅ |
| D75_v1 | XYZScaling | 3.7RP 3.0/12.1 | deep purplish red | ✅ | deep purplish red | ✅ |
| F2_v1 | Bradford | 9.3RP 3.0/12.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| F2_v1 | VonKries | 8.9RP 3.0/12.4 | deep purplish red | ✅ | deep purplish red | ✅ |
| F2_v1 | CAT02 | 8.9RP 3.0/12.5 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | Bradford | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | VonKries | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | CAT02 | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| F7_v1 | XYZScaling | 4.3RP 3.0/12.7 | deep purplish red | ✅ | deep purplish red | ✅ |
| F11_v1 | Bradford | 9.8RP 3.1/12.3 | deep purplish red | ✅ | deep purplish red | ✅ |
| F11_v1 | VonKries | 9.3RP 3.0/12.5 | deep purplish red | ✅ | deep purplish red | ✅ |
| F11_v1 | CAT02 | 9.4RP 3.0/12.5 | deep purplish red | ✅ | deep purplish red | ✅ |

#### 250. #54063C - Expected: very deep purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.0RP 1.7/8.5 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| C_v1 | VonKries | 5.1RP 1.7/8.6 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| C_v1 | CAT02 | 5.1RP 1.7/8.4 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| C_v1 | XYZScaling | 5.2RP 1.7/8.7 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D50_v1 | Bradford | 9.5RP 1.7/8.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D50_v1 | VonKries | 9.3RP 1.7/8.1 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D50_v1 | CAT02 | 9.3RP 1.7/8.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D50_v1 | XYZScaling | 9.4RP 1.7/8.5 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | Bradford | 8.2RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | VonKries | 8.1RP 1.7/8.1 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | CAT02 | 8.1RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D55_v1 | XYZScaling | 8.2RP 1.7/8.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | Bradford | 5.9RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | VonKries | 5.9RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | CAT02 | 5.9RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D65_v1 | XYZScaling | 5.9RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | Bradford | 4.5RP 1.7/8.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | VonKries | 4.6RP 1.7/8.4 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | CAT02 | 4.5RP 1.7/8.3 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| D75_v1 | XYZScaling | 4.5RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | Bradford | 7.4RP 1.7/8.5 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | VonKries | 7.3RP 1.7/8.5 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | CAT02 | 7.4RP 1.7/8.5 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| E_v1 | XYZScaling | 7.5RP 1.7/9.0 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | Bradford | 6.0RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | VonKries | 6.0RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | CAT02 | 6.0RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |
| F7_v1 | XYZScaling | 6.0RP 1.7/8.2 | very deep purplish red | ✅ | very deep purplish red | ✅ |

#### 251. #AB4B74 - Expected: moderate purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D50_v1 | Bradford | 9.0RP 4.5/10.5 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D50_v1 | VonKries | 8.7RP 4.5/10.5 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D50_v1 | CAT02 | 8.8RP 4.5/10.6 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D50_v1 | XYZScaling | 8.6RP 4.5/10.7 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | Bradford | 7.0RP 4.5/10.8 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | VonKries | 6.8RP 4.5/10.7 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | CAT02 | 6.8RP 4.5/10.8 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D55_v1 | XYZScaling | 6.8RP 4.5/10.8 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | Bradford | 4.1RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | VonKries | 4.1RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | CAT02 | 4.1RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D65_v1 | XYZScaling | 4.1RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| D75_v1 | Bradford | 2.8RP 4.5/10.4 | moderate purplish red | ✅ | strong reddish purple | ❌ |
| D75_v1 | VonKries | 2.8RP 4.5/10.5 | moderate purplish red | ✅ | strong reddish purple | ❌ |
| D75_v1 | CAT02 | 2.8RP 4.5/10.4 | moderate purplish red | ✅ | strong reddish purple | ❌ |
| D75_v1 | XYZScaling | 2.8RP 4.5/10.4 | moderate purplish red | ✅ | strong reddish purple | ❌ |
| F7_v1 | Bradford | 4.2RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | VonKries | 4.2RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | CAT02 | 4.2RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |
| F7_v1 | XYZScaling | 4.2RP 4.5/10.9 | moderate purplish red | ✅ | moderate purplish red | ✅ |

#### 252. #6E294C - Expected: dark purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 4.2RP 2.8/7.7 | dark purplish red | ✅ | dark purplish red | ✅ |
| C_v1 | VonKries | 4.2RP 2.8/7.8 | dark purplish red | ✅ | dark purplish red | ✅ |
| C_v1 | CAT02 | 4.2RP 2.8/7.7 | dark purplish red | ✅ | dark purplish red | ✅ |
| C_v1 | XYZScaling | 4.2RP 2.8/7.9 | dark purplish red | ✅ | dark purplish red | ✅ |
| D50_v1 | Bradford | 9.1RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D50_v1 | VonKries | 8.9RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D50_v1 | CAT02 | 8.9RP 2.8/7.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D50_v1 | XYZScaling | 8.9RP 2.8/7.7 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | Bradford | 7.2RP 2.8/7.7 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | VonKries | 7.1RP 2.8/7.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | CAT02 | 7.1RP 2.8/7.7 | dark purplish red | ✅ | dark purplish red | ✅ |
| D55_v1 | XYZScaling | 7.1RP 2.8/7.8 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | Bradford | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | VonKries | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | CAT02 | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D65_v1 | XYZScaling | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | Bradford | 3.7RP 2.8/7.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | VonKries | 3.7RP 2.8/7.3 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | CAT02 | 3.7RP 2.8/7.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| D75_v1 | XYZScaling | 3.7RP 2.8/7.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | Bradford | 6.1RP 2.8/8.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | VonKries | 6.0RP 2.8/8.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | CAT02 | 6.0RP 2.8/8.2 | dark purplish red | ✅ | dark purplish red | ✅ |
| E_v1 | XYZScaling | 6.0RP 2.8/8.6 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | Bradford | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | VonKries | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | CAT02 | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |
| F7_v1 | XYZScaling | 4.8RP 2.8/7.5 | dark purplish red | ✅ | dark purplish red | ✅ |

#### 253. #431432 - Expected: very dark purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 5.8RP 1.5/5.4 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | Bradford | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| C_v1 | VonKries | 5.8RP 1.5/5.5 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | VonKries | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| C_v1 | CAT02 | 5.8RP 1.5/5.4 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | CAT02 | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| C_v1 | XYZScaling | 5.9RP 1.5/5.6 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| C_v2 | XYZScaling | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D55_v1 | Bradford | 9.5RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v1 | VonKries | 9.4RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v1 | CAT02 | 9.4RP 1.5/5.2 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D55_v1 | XYZScaling | 9.5RP 1.5/5.2 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v1 | Bradford | 6.8RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | Bradford | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | VonKries | 6.8RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | VonKries | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | CAT02 | 6.8RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | CAT02 | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D65_v1 | XYZScaling | 6.8RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D65_v2 | XYZScaling | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | Bradford | 4.8RP 1.5/5.3 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | Bradford | 7.5RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | VonKries | 4.9RP 1.5/5.3 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | VonKries | 7.5RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | CAT02 | 4.8RP 1.5/5.2 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | CAT02 | 7.5RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| D75_v1 | XYZScaling | 4.8RP 1.5/5.2 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| D75_v2 | XYZScaling | 7.5RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | Bradford | 8.7RP 1.5/5.5 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | Bradford | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | VonKries | 8.6RP 1.5/5.5 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | VonKries | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | CAT02 | 8.6RP 1.5/5.5 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| E_v2 | CAT02 | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| E_v1 | XYZScaling | 8.7RP 1.5/5.8 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v1 | Bradford | 6.9RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | Bradford | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | VonKries | 6.9RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | VonKries | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | CAT02 | 6.9RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | CAT02 | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |
| F7_v1 | XYZScaling | 6.9RP 1.5/5.1 | very dark purplish red | ✅ | very dark purplish red | ✅ |
| F7_v2 | XYZScaling | 10.0RP 1.5/2.0 | very dark purplish red | ✅ | blackish purple | ❌ |

#### 254. #B2879B - Expected: light grayish purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 3.0RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D65_v1 | VonKries | 3.0RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D65_v1 | CAT02 | 3.0RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| D65_v1 | XYZScaling | 3.0RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| F7_v1 | Bradford | 3.1RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| F7_v1 | VonKries | 3.1RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| F7_v1 | CAT02 | 3.1RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |
| F7_v1 | XYZScaling | 3.1RP 6.0/4.5 | light grayish purplish red | ✅ | light grayish purplish red | ✅ |

#### 255. #945C73 - Expected: grayish purplish red

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 2.8RP 4.5/6.2 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| C_v1 | VonKries | 2.8RP 4.5/6.3 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| C_v1 | CAT02 | 2.8RP 4.5/6.2 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| C_v1 | XYZScaling | 2.8RP 4.5/6.4 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| D55_v1 | Bradford | 9.2RP 4.5/5.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D55_v1 | VonKries | 9.0RP 4.5/5.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D55_v1 | CAT02 | 9.0RP 4.5/5.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D55_v1 | XYZScaling | 8.9RP 4.5/5.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | Bradford | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | VonKries | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | CAT02 | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D65_v1 | XYZScaling | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| D75_v1 | Bradford | 2.4RP 4.5/5.5 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| D75_v1 | VonKries | 2.4RP 4.5/5.5 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| D75_v1 | CAT02 | 2.4RP 4.5/5.5 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| D75_v1 | XYZScaling | 2.4RP 4.5/5.5 | grayish purplish red | ✅ | moderate reddish purple | ❌ |
| E_v1 | Bradford | 6.4RP 4.5/6.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| E_v1 | VonKries | 6.1RP 4.5/6.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| E_v1 | CAT02 | 6.3RP 4.5/6.8 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | Bradford | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | VonKries | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | CAT02 | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |
| F7_v1 | XYZScaling | 4.1RP 4.5/5.9 | grayish purplish red | ✅ | grayish purplish red | ✅ |

#### 256. #E7E1E9 - Expected: white

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 2.1G 9.0/0.4 | white | ✅ | white | ✅ |
| D65_v1 | VonKries | 2.1G 9.0/0.4 | white | ✅ | white | ✅ |
| D65_v1 | CAT02 | 2.1G 9.0/0.4 | white | ✅ | white | ✅ |
| D65_v1 | XYZScaling | 2.1G 9.0/0.4 | white | ✅ | white | ✅ |
| F7_v1 | Bradford | 1.7G 9.0/0.4 | white | ✅ | white | ✅ |
| F7_v1 | VonKries | 1.7G 9.0/0.4 | white | ✅ | white | ✅ |
| F7_v1 | CAT02 | 1.8G 9.0/0.4 | white | ✅ | white | ✅ |
| F7_v1 | XYZScaling | 1.7G 9.0/0.4 | white | ✅ | white | ✅ |

#### 257. #BDB7BF - Expected: light gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| D65_v1 | VonKries | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| D65_v1 | CAT02 | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| D65_v1 | XYZScaling | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| F7_v1 | Bradford | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| F7_v1 | VonKries | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| F7_v1 | CAT02 | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |
| F7_v1 | XYZScaling | 9.5GY 7.4/0.2 | light gray | ✅ | light gray | ✅ |

#### 258. #8A8489 - Expected: medium gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 2.3GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| D65_v1 | VonKries | 2.3GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| D65_v1 | CAT02 | 2.3GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| D65_v1 | XYZScaling | 2.3GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| F7_v1 | Bradford | 2.4GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| F7_v1 | VonKries | 2.4GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| F7_v1 | CAT02 | 2.4GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |
| F7_v1 | XYZScaling | 2.4GY 5.5/0.2 | medium gray | ✅ | medium gray | ✅ |

#### 259. #585458 - Expected: dark gray

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| D65_v1 | Bradford | 8.7Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| D65_v1 | VonKries | 8.7Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| D65_v1 | CAT02 | 8.7Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| D65_v1 | XYZScaling | 8.7Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| F7_v1 | Bradford | 9.0Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| F7_v1 | VonKries | 9.0Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| F7_v1 | CAT02 | 9.1Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |
| F7_v1 | XYZScaling | 9.0Y 3.6/0.1 | dark gray | ✅ | dark gray | ✅ |

#### 260. #2B292B - Expected: black

| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |
|------------|------------|---------|----------|-----|----------|-----|
| C_v1 | Bradford | 9.4P 1.7/0.3 | black | ✅ | black | ✅ |
| C_v1 | VonKries | 9.5P 1.7/0.3 | black | ✅ | black | ✅ |
| C_v1 | CAT02 | 9.3P 1.7/0.3 | black | ✅ | black | ✅ |
| C_v1 | XYZScaling | 9.4P 1.7/0.3 | black | ✅ | black | ✅ |
| D65_v1 | Bradford | 0.1GY 1.7/0.1 | black | ✅ | black | ✅ |
| D65_v1 | VonKries | 0.1GY 1.7/0.1 | black | ✅ | black | ✅ |
| D65_v1 | CAT02 | 0.1GY 1.7/0.1 | black | ✅ | black | ✅ |
| D65_v1 | XYZScaling | 0.1GY 1.7/0.1 | black | ✅ | black | ✅ |
| D75_v1 | Bradford | 4.6B 1.7/0.4 | black | ✅ | black | ✅ |
| D75_v1 | VonKries | 4.7B 1.7/0.4 | black | ✅ | black | ✅ |
| D75_v1 | CAT02 | 4.5B 1.7/0.4 | black | ✅ | black | ✅ |
| D75_v1 | XYZScaling | 4.4B 1.7/0.4 | black | ✅ | black | ✅ |
| F7_v1 | Bradford | 0.2GY 1.7/0.1 | black | ✅ | black | ✅ |
| F7_v1 | VonKries | 0.2GY 1.7/0.1 | black | ✅ | black | ✅ |
| F7_v1 | CAT02 | 0.4GY 1.7/0.1 | black | ✅ | black | ✅ |
| F7_v1 | XYZScaling | 0.2GY 1.7/0.1 | black | ✅ | black | ✅ |

