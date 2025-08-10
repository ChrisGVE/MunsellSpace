# Original Mathematical Converter Illuminant Comparison Report

## Executive Summary

This report analyzes the Original mathematical converter with different
illuminant matrix configurations on precision test colors to identify
optimal settings and assess practical impact through ISCC-NBS classification.

- **Test Colors**: 8 precision test colors
- **Illuminants Tested**: 10 illuminant configurations
- **Colors with Meaningful Differences**: 8/8
- **Total Meaningful Differences**: 356

## Color-by-Color Analysis

### Pinkish White (#EFDDE5)

**Description**: Light pinkish color showing chroma precision issue
**Expected Munsell**: 5R 9/1.5
**Known Issue**: Chroma precision (expected 1.5, often gets 1.6)

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 7.6YR 9.0/10.3 | brilliant orange orange |
| Average Daylight (Munsell) | C | 1.0RP 9.0/2.4 | pale pink pink |
| Daylight 5000K | D50 | 1.4Y 9.0/2.8 | pale yellow yellow |
| Mid-morning Daylight | D55 | 9.7YR 9.0/1.9 | pale pink pink |
| Daylight 6500K (sRGB) | D65 | 1.6YR 9.0/1.0 | pinkish white pink |
| North Sky Daylight | D75 | 4.5P 9.0/1.8 | pale pink pink |
| Equal Energy | E | 8.5R 9.0/2.9 | pale yellowish pink yellowish pink |
| Cool White Fluorescent | F2 | 0.9Y 9.0/4.5 | pale greenish yellow greenish yellow |
| Daylight Fluorescent | F7 | 2.4YR 9.0/0.9 | pinkish white pink |
| Narrow Band Fluorescent | F11 | 9.3YR 9.0/5.2 | pale orange yellow orange yellow |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 13.330
- A vs D50: 13.423
- A vs D55: 10.579
- A vs D65: 13.403
- A vs D75: 13.575
- A vs E: 10.359
- A vs F2: 11.143
- A vs F7: 14.177
- A vs F11: 6.936
- C vs D50: 2.712
- C vs D55: 3.774
- C vs D65: 4.073
- C vs D75: 6.130
- C vs E: 4.971
- C vs F2: 4.187
- C vs F7: 4.848
- C vs F11: 6.394
- D50 vs D55: 4.485
- D50 vs D65: 3.981
- D50 vs D75: 6.037
- D50 vs E: 5.063
- D50 vs F2: 2.279
- D50 vs F7: 4.755
- D50 vs F11: 6.487
- D55 vs D65: 2.824
- D55 vs D75: 6.881
- D55 vs E: 4.220
- D55 vs F2: 5.752
- D55 vs F7: 3.599
- D55 vs F11: 3.643
- D65 vs D75: 5.768
- D65 vs E: 7.044
- D65 vs F2: 6.260
- D65 vs F7: 0.774
- D65 vs F11: 6.467
- D75 vs E: 7.056
- D75 vs F2: 8.317
- D75 vs F7: 5.058
- D75 vs F11: 10.164
- E vs F2: 6.029
- E vs F7: 7.818
- E vs F11: 5.108
- F2 vs F7: 7.034
- F2 vs F11: 4.207
- F7 vs F11: 7.242

### Very Dark Red (#5C0625)

**Description**: Very dark red with red/purple confusion
**Expected Munsell**: 5R 1.5/6
**Known Issue**: Hue family (expected R, often classified as RP)

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 0.7YR 2.0/9.5 | deep reddish brown reddish brown |
| Average Daylight (Munsell) | C | 4.6R 1.8/7.9 | very deep red red |
| Daylight 5000K | D50 | 6.9R 1.8/8.2 | very deep red red |
| Mid-morning Daylight | D55 | 6.1R 1.8/8.1 | very deep red red |
| Daylight 6500K (sRGB) | D65 | 4.9R 1.8/7.9 | very deep red red |
| North Sky Daylight | D75 | 4.2R 1.8/7.7 | very deep red red |
| Equal Energy | E | 5.5R 1.8/8.4 | very deep red red |
| Cool White Fluorescent | F2 | 8.2R 1.9/8.5 | very deep red red |
| Daylight Fluorescent | F7 | 5.0R 1.8/7.9 | very deep red red |
| Narrow Band Fluorescent | F11 | 8.4R 1.9/8.7 | very deep red red |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 7.667
- A vs D50: 7.066
- A vs D55: 8.002
- A vs D65: 8.053
- A vs D75: 7.515
- A vs E: 8.082
- A vs F2: 5.491
- A vs F7: 8.057
- A vs F11: 5.106
- C vs D50: 2.735
- C vs D55: 1.798
- C vs D65: 0.386
- C vs D75: 0.597
- C vs E: 1.416
- C vs F2: 4.309
- C vs F7: 0.390
- C vs F11: 4.694
- D50 vs D55: 0.937
- D50 vs D65: 2.390
- D50 vs D75: 3.332
- D50 vs E: 1.562
- D50 vs F2: 1.574
- D50 vs F7: 2.377
- D50 vs F11: 1.960
- D55 vs D65: 1.454
- D55 vs D75: 2.395
- D55 vs E: 0.906
- D55 vs F2: 2.511
- D55 vs F7: 1.440
- D55 vs F11: 2.896
- D65 vs D75: 0.942
- D65 vs E: 1.072
- D65 vs F2: 3.965
- D65 vs F11: 4.350
- D75 vs E: 2.013
- D75 vs F2: 4.906
- D75 vs F7: 0.955
- D75 vs F11: 5.292
- E vs F2: 2.893
- E vs F7: 1.058
- E vs F11: 3.278
- F2 vs F7: 3.951
- F2 vs F11: 0.385
- F7 vs F11: 4.336

### Pinkish Gray (#C7B6BD)

**Description**: Pinkish gray with family classification issue
**Expected Munsell**: 5R 7.5/1.5
**Known Issue**: Chroma precision and family classification

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 8.1YR 7.5/9.1 | moderate orange yellow orange yellow |
| Average Daylight (Munsell) | C | 1.5RP 7.5/2.3 | grayish pink pink |
| Daylight 5000K | D50 | 1.9Y 7.5/2.5 | grayish pink pink |
| Mid-morning Daylight | D55 | 0.3Y 7.5/1.8 | yellowish gray yellow |
| Daylight 6500K (sRGB) | D65 | 0.5YR 7.5/1.0 | pinkish gray pink |
| North Sky Daylight | D75 | 5.2P 7.5/1.5 | light purplish gray purple |
| Equal Energy | E | 8.5R 7.5/2.7 | grayish yellowish pink yellowish pink |
| Cool White Fluorescent | F2 | 1.1Y 7.5/4.1 | grayish greenish yellow greenish yellow |
| Daylight Fluorescent | F7 | 1.0YR 7.5/1.0 | yellowish gray yellow |
| Narrow Band Fluorescent | F11 | 9.6YR 7.5/4.7 | pale orange yellow orange yellow |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 12.187
- A vs D50: 12.426
- A vs D55: 11.547
- A vs D65: 10.561
- A vs D75: 12.591
- A vs E: 8.803
- A vs F2: 9.926
- A vs F7: 11.066
- A vs F11: 5.875
- C vs D50: 2.685
- C vs D55: 3.661
- C vs D65: 4.293
- C vs D75: 6.601
- C vs E: 5.383
- C vs F2: 4.261
- C vs F7: 3.806
- C vs F11: 6.312
- D50 vs D55: 2.345
- D50 vs D65: 4.977
- D50 vs D75: 6.362
- D50 vs E: 5.622
- D50 vs F2: 2.500
- D50 vs F7: 4.491
- D50 vs F11: 6.551
- D55 vs D65: 3.014
- D55 vs D75: 7.240
- D55 vs E: 4.744
- D55 vs F2: 3.082
- D55 vs F7: 3.519
- D55 vs F11: 5.673
- D65 vs D75: 7.204
- D65 vs E: 5.758
- D65 vs F2: 5.714
- D65 vs F7: 0.505
- D65 vs F11: 4.687
- D75 vs E: 6.532
- D75 vs F2: 8.862
- D75 vs F7: 6.717
- D75 vs F11: 9.600
- E vs F2: 5.981
- E vs F7: 6.263
- E vs F11: 5.068
- F2 vs F7: 5.228
- F2 vs F11: 4.051
- F7 vs F11: 5.192

### Very Dark Burgundy (#481127)

**Description**: Very dark burgundy with hue family confusion
**Expected Munsell**: 5R 1/5
**Known Issue**: Hue family (expected R, often classified as RP)

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 0.0YR 1.6/7.4 | deep reddish brown reddish brown |
| Average Daylight (Munsell) | C | 2.2R 1.5/5.6 | very dark red red |
| Daylight 5000K | D50 | 6.4R 1.5/5.5 | very dark red red |
| Mid-morning Daylight | D55 | 5.2R 1.5/5.4 | very dark red red |
| Daylight 6500K (sRGB) | D65 | 3.2R 1.5/5.4 | very dark red red |
| North Sky Daylight | D75 | 1.5R 1.5/5.4 | very dark red red |
| Equal Energy | E | 4.5R 1.5/5.7 | very dark red red |
| Cool White Fluorescent | F2 | 8.3R 1.5/5.8 | deep reddish brown reddish brown |
| Daylight Fluorescent | F7 | 3.3R 1.5/5.4 | very dark red red |
| Narrow Band Fluorescent | F11 | 8.6R 1.5/5.9 | deep reddish brown reddish brown |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 6.087
- A vs D50: 7.644
- A vs D55: 8.942
- A vs D65: 7.388
- A vs D75: 5.549
- A vs E: 8.323
- A vs F2: 5.450
- A vs F7: 7.424
- A vs F11: 4.970
- C vs D50: 4.264
- C vs D55: 3.158
- C vs D65: 1.301
- C vs D75: 0.934
- C vs E: 2.367
- C vs F2: 4.103
- C vs F7: 1.337
- C vs F11: 3.916
- D50 vs D55: 1.297
- D50 vs D65: 3.345
- D50 vs D75: 5.049
- D50 vs E: 2.002
- D50 vs F2: 2.194
- D50 vs F7: 3.315
- D50 vs F11: 2.674
- D55 vs D65: 2.048
- D55 vs D75: 3.752
- D55 vs E: 0.914
- D55 vs F2: 3.491
- D55 vs F7: 2.018
- D55 vs F11: 3.971
- D65 vs D75: 1.856
- D65 vs E: 1.596
- D65 vs F2: 5.404
- D65 vs F11: 5.217
- D75 vs E: 3.300
- D75 vs F2: 3.565
- D75 vs F7: 1.892
- D75 vs F11: 3.378
- E vs F2: 3.943
- E vs F7: 1.567
- E vs F11: 4.423
- F2 vs F7: 5.439
- F2 vs F11: 0.480
- F7 vs F11: 5.253

### Dusty Rose (#BC8F8F)

**Description**: Desaturated red showing subtle illuminant effects
**Expected Munsell**: 5R 6/4
**Known Issue**: Subtle illuminant sensitivity

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 5.3YR 6.3/10.2 | strong orange orange |
| Average Daylight (Munsell) | C | 6.3R 6.3/3.5 | light grayish red red |
| Daylight 5000K | D50 | 4.4YR 6.3/4.7 | light brown brown |
| Mid-morning Daylight | D55 | 2.5YR 6.3/4.2 | light reddish brown reddish brown |
| Daylight 6500K (sRGB) | D65 | 8.6R 6.3/3.4 | light grayish red red |
| North Sky Daylight | D75 | 6.1R 6.3/2.8 | light grayish red red |
| Equal Energy | E | 8.4R 6.3/4.8 | light grayish red red |
| Cool White Fluorescent | F2 | 5.7YR 6.3/5.9 | light brown brown |
| Daylight Fluorescent | F7 | 8.6R 6.3/3.5 | light grayish red red |
| Narrow Band Fluorescent | F11 | 5.1YR 6.3/6.4 | moderate orange orange |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 9.792
- A vs D50: 6.431
- A vs D55: 8.842
- A vs D65: 12.098
- A vs D75: 10.293
- A vs E: 10.586
- A vs F2: 4.683
- A vs F7: 12.129
- A vs F11: 4.036
- C vs D50: 5.069
- C vs D55: 6.440
- C vs D65: 2.306
- C vs D75: 1.018
- C vs E: 3.360
- C vs F2: 5.109
- C vs F7: 2.337
- C vs F11: 6.227
- D50 vs D55: 2.411
- D50 vs D65: 7.375
- D50 vs D75: 5.569
- D50 vs E: 6.113
- D50 vs F2: 2.477
- D50 vs F7: 7.406
- D50 vs F11: 2.395
- D55 vs D65: 6.726
- D55 vs D75: 6.941
- D55 vs E: 6.766
- D55 vs F2: 4.888
- D55 vs F7: 6.675
- D55 vs F11: 4.806
- D65 vs D75: 3.128
- D65 vs E: 1.512
- D65 vs F2: 7.415
- D65 vs F7: 0.051
- D65 vs F11: 8.533
- D75 vs E: 4.378
- D75 vs F2: 5.609
- D75 vs F7: 3.179
- D75 vs F11: 6.728
- E vs F2: 5.903
- E vs F7: 1.543
- E vs F11: 7.021
- F2 vs F7: 7.446
- F2 vs F11: 1.118
- F7 vs F11: 8.564

### Warm Beige (#F5F5DC)

**Description**: Warm beige with subtle yellow cast
**Expected Munsell**: 5Y 9.5/2
**Known Issue**: Subtle illuminant sensitivity

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 1.7Y 9.6/10.5 | brilliant orange yellow orange yellow |
| Average Daylight (Munsell) | C | 5.1GY 9.6/1.4 | pale yellow green yellow green |
| Daylight 5000K | D50 | 6.8Y 9.6/4.0 | pale yellow yellow |
| Mid-morning Daylight | D55 | 2.3GY 9.6/3.2 | light yellow green yellow green |
| Daylight 6500K (sRGB) | D65 | 5.3GY 9.6/2.1 | pale pink pink |
| North Sky Daylight | D75 | 3.7G 9.6/2.2 | very pale green green |
| Equal Energy | E | 7.5Y 9.6/2.6 | pale yellow yellow |
| Cool White Fluorescent | F2 | 6.1GY 9.6/6.2 | light yellow green yellow green |
| Daylight Fluorescent | F7 | 5.3GY 9.6/2.1 | pale pink pink |
| Narrow Band Fluorescent | F11 | 2.9GY 9.6/6.0 | light yellow green yellow green |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 14.520
- A vs D50: 11.443
- A vs D55: 9.976
- A vs D65: 14.073
- A vs D75: 12.270
- A vs E: 12.039
- A vs F2: 10.686
- A vs F7: 14.033
- A vs F11: 7.681
- C vs D50: 6.192
- C vs D55: 4.544
- C vs D65: 0.824
- C vs D75: 4.253
- C vs E: 5.596
- C vs F2: 5.757
- C vs F7: 0.817
- C vs F11: 6.839
- D50 vs D55: 7.187
- D50 vs D65: 5.368
- D50 vs D75: 6.843
- D50 vs E: 2.131
- D50 vs F2: 4.983
- D50 vs F7: 5.375
- D50 vs F11: 7.987
- D55 vs D65: 4.097
- D55 vs D75: 4.294
- D55 vs E: 7.409
- D55 vs F2: 6.752
- D55 vs F7: 4.057
- D55 vs F11: 3.330
- D65 vs D75: 3.813
- D65 vs E: 4.772
- D65 vs F2: 4.933
- D65 vs F11: 6.391
- D75 vs E: 6.247
- D75 vs F2: 8.408
- D75 vs F7: 3.774
- D75 vs F11: 6.588
- E vs F2: 7.114
- E vs F7: 4.779
- E vs F11: 10.118
- F2 vs F7: 4.940
- F2 vs F11: 3.424
- F7 vs F11: 6.352

### Cool Gray (#C8C8D2)

**Description**: Cool gray with subtle blue cast
**Expected Munsell**: 5B 8/1
**Known Issue**: Subtle illuminant sensitivity

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 0.7Y 8.0/8.4 | light orange yellow orange yellow |
| Average Daylight (Munsell) | C | 3.4P 8.0/2.1 | pale pink pink |
| Daylight 5000K | D50 | 6.9GY 8.0/2.4 | pale pink pink |
| Mid-morning Daylight | D55 | 6.6Y 8.0/1.1 | yellowish gray yellow |
| Daylight 6500K (sRGB) | D65 | 2.9B 8.0/0.4 | light gray gray |
| North Sky Daylight | D75 | 3.9PB 8.0/2.4 | pale pink pink |
| Equal Energy | E | 0.5YR 8.0/1.5 | pale pink pink |
| Cool White Fluorescent | F2 | 1.7GY 8.0/3.5 | pale greenish yellow greenish yellow |
| Daylight Fluorescent | F7 | 3.9B 8.0/0.4 | light gray gray |
| Narrow Band Fluorescent | F11 | 4.4Y 8.0/3.8 | pale yellow yellow |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 11.091
- A vs D50: 11.827
- A vs D55: 11.381
- A vs D65: 12.176
- A vs D75: 11.284
- A vs E: 9.060
- A vs F2: 7.941
- A vs F7: 13.229
- A vs F11: 8.355
- C vs D50: 5.700
- C vs D55: 6.207
- C vs D65: 4.249
- C vs D75: 2.700
- C vs E: 5.539
- C vs F2: 5.150
- C vs F7: 4.141
- C vs F11: 4.734
- D50 vs D55: 3.554
- D50 vs D65: 7.945
- D50 vs D75: 5.022
- D50 vs E: 6.433
- D50 vs F2: 5.913
- D50 vs F7: 6.908
- D50 vs F11: 5.938
- D55 vs D65: 6.391
- D55 vs D75: 6.015
- D55 vs E: 6.324
- D55 vs F2: 9.348
- D55 vs F7: 5.353
- D55 vs F11: 4.934
- D65 vs D75: 4.949
- D65 vs E: 5.451
- D65 vs F2: 6.235
- D65 vs F7: 1.053
- D65 vs F11: 6.979
- D75 vs E: 6.239
- D75 vs F2: 5.343
- D75 vs F7: 3.949
- D75 vs F11: 4.035
- E vs F2: 5.146
- E vs F7: 6.503
- E vs F11: 8.267
- F2 vs F7: 7.288
- F2 vs F11: 5.121
- F7 vs F11: 5.942

### Medium Orange (#FFA500)

**Description**: Orange showing yellow-red transition effects
**Expected Munsell**: 2.5YR 7/14
**Known Issue**: Illuminant impact on hue transition

| Illuminant | Short | Munsell Result | ISCC-NBS Classification |
|------------|-------|----------------|-------------------------|
| Tungsten Incandescent | A | 4.7YR 7.7/20.4 | vivid orange orange |
| Average Daylight (Munsell) | C | 0.6Y 7.4/12.9 | strong orange yellow orange yellow |
| Daylight 5000K | D50 | 10.0YR 7.5/14.5 | vivid orange yellow orange yellow |
| Mid-morning Daylight | D55 | 0.7Y 7.5/13.8 | strong orange yellow orange yellow |
| Daylight 6500K (sRGB) | D65 | 1.8Y 7.4/12.8 | strong orange yellow orange yellow |
| North Sky Daylight | D75 | 2.6Y 7.4/12.0 | vivid yellow yellow |
| Equal Energy | E | 9.0YR 7.5/14.1 | vivid orange yellow orange yellow |
| Cool White Fluorescent | F2 | 8.4YR 7.5/15.9 | vivid orange yellow orange yellow |
| Daylight Fluorescent | F7 | 1.8Y 7.4/12.8 | strong orange yellow orange yellow |
| Narrow Band Fluorescent | F11 | 7.7YR 7.6/16.4 | vivid orange yellow orange yellow |

**Illuminant Differences** (difference score > 0.05):
- A vs C: 13.953
- A vs D50: 10.852
- A vs D55: 12.907
- A vs D65: 12.833
- A vs D75: 12.850
- A vs E: 10.742
- A vs F2: 8.314
- A vs F7: 12.822
- A vs F11: 7.025
- C vs D50: 4.303
- C vs D55: 1.046
- C vs D65: 1.318
- C vs D75: 2.930
- C vs E: 4.817
- C vs F2: 7.245
- C vs F7: 1.309
- C vs F11: 8.534
- D50 vs D55: 3.454
- D50 vs D65: 5.615
- D50 vs D75: 7.234
- D50 vs E: 1.300
- D50 vs F2: 2.942
- D50 vs F7: 5.606
- D50 vs F11: 4.231
- D55 vs D65: 2.162
- D55 vs D75: 3.780
- D55 vs E: 3.967
- D55 vs F2: 6.396
- D55 vs F7: 2.152
- D55 vs F11: 7.685
- D65 vs D75: 1.618
- D65 vs E: 6.129
- D65 vs F2: 8.558
- D65 vs F11: 9.846
- D75 vs E: 7.747
- D75 vs F2: 10.176
- D75 vs F7: 1.627
- D75 vs F11: 11.464
- E vs F2: 2.429
- E vs F7: 6.120
- E vs F11: 3.717
- F2 vs F7: 8.549
- F2 vs F11: 1.288
- F7 vs F11: 9.837

## Summary and Conclusions

✅ **Illuminant Configuration Impact Detected**

- 8/8 colors show meaningful differences across illuminants
- 356 total meaningful differences detected
- Different illuminant matrices can resolve some precision issues

**Recommendation**: Consider implementing illuminant-configurable
matrix selection in the Original mathematical converter.

---
Report generated by MunsellSpace Original Illuminant Comparison Tool
