# Quality Scoring Threshold Sensitivity Analysis

Generated: 2026-01-03 11:11:03

## Methodology

Quality score combines three components:
- **NLP Confidence (40%)**: SBERT similarity score for family assignment
- **Colorimetric Consistency (40%)**: Hue within expected family range
- **Source Reliability (20%)**: Data source quality weighting

## Screen Color Data

Total samples: 184296

| Threshold | Samples | Percentage | Families |
|-----------|---------|------------|----------|
| 0.5 | 137007 | 74.3% | 35 |
| 0.6 | 122961 | 66.7% | 35 |
| 0.7 | 92239 | 50.0% | 35 |
| 0.8 | 21876 | 11.9% | 35 |

### Per-Family Quality Summary (Threshold 0.6)

| Family | Total | Pass (≥0.6) | Pass Rate | Avg Score |
|--------|-------|-------------|-----------|-----------|
| aqua | 3082 | 1593 | 51.7% | 0.564 |
| aquamarine | 2625 | 1227 | 46.7% | 0.542 |
| beige | 3540 | 2088 | 59.0% | 0.602 |
| blue | 22103 | 18778 | 85.0% | 0.706 |
| brown | 5248 | 4299 | 81.9% | 0.689 |
| coral | 3840 | 738 | 19.2% | 0.406 |
| fuchsia | 4591 | 1501 | 32.7% | 0.463 |
| gold | 5709 | 1441 | 25.2% | 0.414 |
| gray | 7839 | 7578 | 96.7% | 0.742 |
| green | 23090 | 21816 | 94.5% | 0.742 |
| indigo | 2693 | 902 | 33.5% | 0.464 |
| lavender | 3475 | 1359 | 39.1% | 0.503 |
| lilac | 3709 | 1183 | 31.9% | 0.455 |
| lime | 4186 | 2399 | 57.3% | 0.568 |
| magenta | 2444 | 1492 | 61.0% | 0.612 |
| maroon | 1685 | 727 | 43.1% | 0.520 |
| mauve | 3195 | 1344 | 42.1% | 0.510 |
| navy | 1492 | 600 | 40.2% | 0.495 |
| orange | 6109 | 4392 | 71.9% | 0.653 |
| peach | 3813 | 1612 | 42.3% | 0.515 |
| pink | 9438 | 8341 | 88.4% | 0.733 |
| plum | 2849 | 678 | 23.8% | 0.420 |
| purple | 10944 | 9720 | 88.8% | 0.733 |
| red | 5808 | 4859 | 83.7% | 0.698 |
| rose | 3580 | 1310 | 36.6% | 0.486 |
| rust | 2586 | 807 | 31.2% | 0.450 |
| sand | 5067 | 2304 | 45.5% | 0.526 |
| tan | 3163 | 2038 | 64.4% | 0.608 |
| taupe | 2848 | 1119 | 39.3% | 0.532 |
| teal | 3822 | 1788 | 46.8% | 0.534 |
| turquoise | 2674 | 1606 | 60.1% | 0.601 |
| violet | 4239 | 2086 | 49.2% | 0.546 |
| white | 2745 | 2607 | 95.0% | 0.690 |
| wine | 2910 | 792 | 27.2% | 0.443 |
| yellow | 7155 | 5837 | 81.6% | 0.689 |

## Surface Color Data

Total samples: 10172

| Threshold | Samples | Percentage | Families |
|-----------|---------|------------|----------|
| 0.5 | 10172 | 100.0% | 62 |
| 0.6 | 8805 | 86.6% | 62 |
| 0.7 | 3771 | 37.1% | 49 |
| 0.8 | 1973 | 19.4% | 13 |

## Source Reliability Weights

| Source | Weight | Category |
|--------|--------|----------|
| Golden Artist Colors | 1.0 | Spectrophotometer |
| Williamsburg | 1.0 | Spectrophotometer |
| NCS | 0.9 | Spectrophotometer |
| Pantone TCX Textile | 0.9 | Spectrophotometer |
| Pantone PMS Solid Coated | 0.85 | Surface Standard |
| Pantone Mixed | 0.85 | Surface Standard |
| RAL Classic | 0.85 | Surface Standard |
| RHS Colour Chart | 0.8 | Surface Standard |
| Copic | 0.75 | Surface Standard |
| Ohuhu | 0.75 | Surface Standard |
| Gemological estimates | 0.6 | Research |
| xkcd_curated | 0.55 | Screen/Web |
| wikipedia | 0.55 | Screen/Web |
| xkcd_survey | 0.5 | Screen/Web |
| colorhexa | 0.5 | Screen/Web |
| meodai | 0.5 | Screen/Web |
| colorname_com | 0.5 | Screen/Web |

## Recommendations

Based on the sensitivity analysis:

**Recommended threshold: 0.7**

- Retains 92239 screen samples (50.0%)
- Covers 35 color families
