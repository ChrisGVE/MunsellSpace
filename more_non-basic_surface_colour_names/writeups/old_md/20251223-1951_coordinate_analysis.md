# Phase 3: Pre-Consolidation Coordinate Analysis Report

## 1. Executive Summary

| Dataset | Names | Total Samples | Coordinate System |
|---------|-------|---------------|-------------------|
| XKCD | 175,844 | 3,393,725 | RGB (0-255) |
| Centore | 30 | 9,251 | Munsell (HVC) |

## 2. XKCD RGB Distribution Summary

| Metric | Value |
|--------|-------|
| Min samples per name | 1 |
| Max samples per name | 314,172 |
| Mean samples per name | 19.3 |
| Median samples per name | 1.0 |
| Min RGB std | 0.0 |
| Max RGB std | 242.6 |
| Mean RGB std | 15.0 |

### 2.1 Interpretation

- **Low variance**: Consistent color naming (same name = same color)
- **High variance**: Inconsistent naming or broad color category
- Typical RGB std < 30 indicates good naming consistency

## 3. Centore Munsell Distribution Summary

| Overlay | Samples | Value Std | Chroma Std | Hue Std |
|---------|---------|-----------|------------|---------|
| aqua | 119 | 1.19 | 1.70 | 26.0 |
| beige | 277 | 0.97 | 1.03 | 10.6 |
| blue | 1671 | 1.69 | 2.49 | 25.2 |
| brown | 536 | 1.13 | 1.53 | 14.9 |
| coral | 215 | 1.10 | 2.77 | 12.7 |
| fuchsia | 45 | 0.72 | 2.36 | 10.1 |
| gold | 362 | 1.11 | 2.25 | 10.3 |
| gray | 482 | 1.54 | 0.72 | 82.3 |
| green | 1296 | 1.72 | 2.35 | 33.9 |
| lavender | 47 | 1.20 | 2.04 | 23.3 |
| lilac | 78 | 1.10 | 1.87 | 22.9 |
| magenta | 25 | 0.90 | 2.42 | 11.3 |
| mauve | 181 | 1.37 | 1.95 | 35.7 |
| navy | 100 | 0.43 | 1.54 | 6.2 |
| orange | 377 | 1.19 | 2.61 | 14.8 |
| peach | 102 | 0.93 | 1.81 | 14.0 |
| pink | 594 | 1.25 | 3.39 | 23.3 |
| purple | 226 | 1.00 | 2.45 | 19.1 |
| red | 661 | 0.87 | 3.05 | 9.7 |
| rose | 467 | 1.33 | 3.32 | 20.7 |
| rust | 93 | 0.89 | 1.68 | 9.5 |
| sand | 123 | 1.16 | 1.33 | 15.1 |
| tan | 129 | 1.06 | 1.55 | 11.9 |
| taupe | 76 | 1.30 | 0.59 | 23.7 |
| teal | 43 | 0.73 | 1.49 | 19.6 |
| turquoise | 120 | 1.08 | 2.10 | 18.1 |
| violet | 178 | 1.27 | 2.56 | 18.4 |
| white | 151 | 0.84 | 0.84 | 21.1 |
| wine | 83 | 0.96 | 2.12 | 16.5 |
| yellow | 394 | 0.86 | 2.64 | 10.8 |

### 3.1 Interpretation

- **Value std**: Variation in lightness (0=dark, 10=light)
- **Chroma std**: Variation in saturation
- **Hue std**: Variation in hue angle (circular)
- Higher std = broader color category

## 4. High-Variance Names (Potential Issues)

Names with RGB std >= 40 and count >= 100:
These may indicate inconsistent color naming or overly broad categories.

| Name | Count | Total Std | R Std | G Std | B Std | R Range | G Range | B Range |
|------|-------|-----------|-------|-------|-------|---------|---------|---------|
| megan | 158 | 134.1 | 78.0 | 76.8 | 77.5 | 253 | 255 | 254 |
| hiccup | 108 | 133.4 | 79.9 | 77.6 | 73.5 | 255 | 250 | 252 |
| sal | 104 | 131.9 | 76.8 | 73.8 | 77.7 | 255 | 255 | 251 |
| ian | 100 | 131.6 | 76.6 | 71.1 | 80.0 | 252 | 253 | 254 |
| k | 458 | 130.9 | 76.6 | 74.7 | 75.4 | 255 | 255 | 255 |
| fd | 100 | 130.7 | 77.0 | 76.6 | 72.7 | 250 | 251 | 246 |
| m | 218 | 130.6 | 74.7 | 76.1 | 75.4 | 255 | 254 | 249 |
| . | 186 | 129.9 | 77.1 | 72.5 | 75.3 | 254 | 255 | 253 |
| q | 176 | 129.9 | 74.4 | 78.1 | 72.3 | 254 | 253 | 253 |
| o | 154 | 129.8 | 79.0 | 71.8 | 73.8 | 254 | 252 | 255 |
| eric is faggot | 213 | 129.7 | 72.7 | 73.9 | 77.9 | 255 | 255 | 254 |
| r | 387 | 129.5 | 75.1 | 75.0 | 74.1 | 255 | 255 | 255 |
| aids | 504 | 129.3 | 73.6 | 76.0 | 74.3 | 255 | 254 | 255 |
| no | 211 | 129.2 | 74.8 | 75.7 | 73.4 | 254 | 253 | 252 |
| n | 200 | 129.0 | 73.1 | 74.9 | 75.4 | 254 | 254 | 254 |
| löä | 116 | 128.9 | 73.3 | 76.1 | 73.7 | 251 | 252 | 252 |
| y | 233 | 128.8 | 73.1 | 74.3 | 75.6 | 255 | 251 | 253 |
| h | 697 | 128.7 | 72.8 | 75.2 | 74.9 | 255 | 255 | 255 |
| fag | 131 | 128.5 | 76.3 | 75.0 | 71.2 | 255 | 253 | 255 |
| s | 1,315 | 128.5 | 74.9 | 73.0 | 74.7 | 255 | 255 | 255 |
| rick astley | 179 | 128.5 | 73.8 | 75.2 | 73.6 | 255 | 253 | 254 |
| l | 296 | 128.2 | 72.9 | 73.3 | 75.8 | 252 | 255 | 255 |
| sd | 221 | 128.1 | 75.2 | 72.7 | 74.1 | 252 | 255 | 254 |
| x | 248 | 128.1 | 72.1 | 75.4 | 74.4 | 253 | 255 | 252 |
| nigger | 3,838 | 128.0 | 73.8 | 74.2 | 73.7 | 255 | 255 | 255 |
| this | 123 | 127.7 | 74.9 | 74.0 | 72.3 | 251 | 254 | 249 |
| as | 136 | 127.7 | 73.3 | 73.9 | 74.0 | 253 | 248 | 255 |
| f | 2,446 | 127.6 | 74.7 | 73.6 | 72.8 | 255 | 255 | 255 |
| sex | 125 | 127.4 | 76.6 | 73.7 | 70.2 | 248 | 250 | 250 |
| j | 338 | 127.2 | 71.0 | 73.1 | 76.1 | 255 | 254 | 254 |
| 3 | 105 | 127.2 | 71.5 | 75.4 | 73.3 | 251 | 254 | 254 |
| josh | 642 | 127.1 | 72.4 | 74.2 | 73.6 | 255 | 255 | 255 |
| g | 1,147 | 127.1 | 72.8 | 74.2 | 73.2 | 254 | 255 | 255 |
| a | 2,420 | 127.0 | 73.3 | 73.9 | 72.7 | 255 | 255 | 255 |
| df | 290 | 126.9 | 72.1 | 75.1 | 72.6 | 255 | 255 | 254 |
| e | 469 | 126.9 | 71.5 | 73.1 | 75.1 | 255 | 255 | 255 |
| w | 478 | 126.9 | 75.9 | 71.9 | 71.9 | 255 | 255 | 255 |
| everlasting cocksucker | 268 | 126.9 | 74.6 | 73.2 | 72.0 | 255 | 249 | 255 |
| 1 | 815 | 126.8 | 73.7 | 72.5 | 73.5 | 255 | 255 | 255 |
| d | 2,270 | 126.8 | 72.9 | 73.0 | 73.7 | 255 | 255 | 255 |
| penis | 1,325 | 126.7 | 74.1 | 72.3 | 73.0 | 255 | 255 | 255 |
| xkcd | 117 | 126.6 | 73.8 | 71.7 | 73.6 | 243 | 245 | 255 |
| v | 502 | 126.6 | 73.0 | 72.1 | 74.1 | 255 | 255 | 255 |
| u | 225 | 126.4 | 75.2 | 72.8 | 70.9 | 255 | 254 | 255 |
| your mom | 606 | 126.3 | 73.4 | 72.0 | 73.3 | 255 | 255 | 255 |
| ass color | 100 | 126.2 | 76.4 | 71.9 | 70.2 | 251 | 253 | 252 |
| dicks | 226 | 126.1 | 74.0 | 73.4 | 71.0 | 253 | 255 | 254 |
| lol | 100 | 126.1 | 70.8 | 75.5 | 72.0 | 252 | 245 | 250 |
| c | 167 | 126.0 | 71.1 | 74.2 | 72.8 | 253 | 251 | 254 |
| 5 | 122 | 126.0 | 76.2 | 70.9 | 70.9 | 251 | 254 | 252 |

## 5. Coordinate System Comparison

### 5.1 Challenge
XKCD and Centore use different coordinate systems:
- **XKCD**: RGB (device-dependent, uncalibrated monitors)
- **Centore**: Munsell (perceptually uniform, spectrophotometer)

### 5.2 Implication
Direct coordinate comparison requires transformation.
Phase 4 will address this using shared overlay colors as calibration points.

## 6. Recommendations

### 6.1 For High-Variance Names
1. Review if the name represents a broad category vs specific color
2. Consider splitting into sub-categories if meaningful
3. Use median instead of mean for robust centroid estimation

### 6.2 For Consolidation
1. Weight by sample count when merging duplicate names
2. Use robust statistics (median, IQR) for outlier handling
3. Document variance for uncertainty quantification

---

*Generated by Phase 3: Pre-Consolidation Coordinate Analysis*