# Bootstrap Sample Size Analysis (Task 100)

Generated: 2026-01-03

## Overview

This analysis determines the minimum sample size needed for stable
convex hull volume estimation using bootstrap resampling.

- Sample sizes tested: [10, 15, 20, 30, 50, 100, 200, 500]
- Bootstrap iterations: 100
- Stability threshold: CV < 0.05

## Summary

- Stable families: 33/35
- Insufficient families: 2

### Minimum Stable Sample Size Distribution

- Mean: 4809.2
- Median: 3385.0
- Range: [500, 21992]

### Insufficient Families

These families have fewer samples than needed for stable volume estimation:

- **brown**: n=5068, min_stable=None
- **purple**: n=10339, min_stable=None

## Per-Family Results

| Family | N Points | Min Stable N | CV @ N | Status |
|--------|----------|--------------|--------|--------|
| aqua | 3015 | 3015 | 0.0236 | stable |
| aquamarine | 2569 | 2569 | 0.0193 | stable |
| beige | 3385 | 3385 | 0.0256 | stable |
| blue | 20982 | 20982 | 0.0176 | stable |
| brown | 5068 | None | 0.0607 | unstable |
| coral | 3782 | 3782 | 0.0189 | stable |
| fuchsia | 4494 | 4494 | 0.0172 | stable |
| gold | 5512 | 5512 | 0.0130 | stable |
| gray | 7546 | 7546 | 0.0168 | stable |
| green | 21992 | 21992 | 0.0153 | stable |
| indigo | 2651 | 2651 | 0.0235 | stable |
| lavender | 3363 | 3363 | 0.0175 | stable |
| lilac | 3606 | 3606 | 0.0215 | stable |
| lime | 4095 | 500 | 0.0079 | stable |
| magenta | 2356 | 2356 | 0.0340 | stable |
| maroon | 1638 | 1638 | 0.0484 | stable |
| mauve | 3125 | 3125 | 0.0153 | stable |
| navy | 1440 | 1440 | 0.0435 | stable |
| orange | 5925 | 5925 | 0.0165 | stable |
| peach | 3744 | 3744 | 0.0208 | stable |
| pink | 8998 | 8998 | 0.0129 | stable |
| plum | 2798 | 2798 | 0.0176 | stable |
| purple | 10339 | None | 0.0552 | unstable |
| red | 5563 | 5563 | 0.0400 | stable |
| rose | 3536 | 3536 | 0.0272 | stable |
| rust | 2527 | 2527 | 0.0186 | stable |
| sand | 5002 | 5002 | 0.0119 | stable |
| tan | 3106 | 3106 | 0.0202 | stable |
| taupe | 2789 | 2789 | 0.0220 | stable |
| teal | 3667 | 3667 | 0.0215 | stable |
| turquoise | 2546 | 2546 | 0.0377 | stable |
| violet | 4168 | 4168 | 0.0360 | stable |
| white | 2671 | 2671 | 0.0209 | stable |
| wine | 2857 | 2857 | 0.0223 | stable |
| yellow | 6851 | 6851 | 0.0145 | stable |

## Implications

1. **Stability threshold (CV < 0.05)**: Ensures volume estimates vary < 5%
2. **Minimum N recommendations**: Use median as guideline for new families
3. **Insufficient families**: May need more samples or alternative methods

## Recommendations

**Excellent stability**: >90% of families have sufficient samples.