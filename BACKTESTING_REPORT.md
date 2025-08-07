# Munsell Conversion Backtesting Report

**Generated**: 2025-08-07T14:21:54.486538
**Dataset**: tests/data/srgb-to-munsell.csv
**Total Colors Tested**: 48

## Executive Summary

- **Overall Accuracy**: 66.67% (32/48 within 0.1 tolerance)
- **Family Mismatches**: 0.00% (0 colors)
- **Hue Accuracy**: 97.92% within tolerance
- **Value Accuracy**: 100.00% within tolerance
- **Chroma Accuracy**: 68.75% within tolerance

## Family Mismatches

**Total**: 0 (0.00%)

## Hue Differences

### Summary Statistics

- **Median**: 0.000000
- **Mean**: 0.008333
- **Std Dev**: 0.027639
- **Min**: 0.000000
- **Max**: 0.100000
- **Above 0.1**: 1 (2.08%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.000000 | ✓ Median - typical error |
|  90.0% | 0.000000 | ✓ 90% of colors below this |
|  95.0% | 0.100000 | ✓ 95% of colors below this |
|  96.0% | 0.100000 | ✓ 96% of colors below this |
|  97.0% | 0.100000 | ✓ 97% of colors below this |
|  98.0% | 0.100000 | ✓ 98% of colors below this |
|  99.0% | 0.100000 | ⚠️ 99% of colors below this |
|  99.5% | 0.100000 | ⚠️ 99.5% of colors below this |
| 100.0% | 0.100000 | ⚠️ Maximum error |

## Value Differences

### Summary Statistics

- **Median**: 0.000000
- **Mean**: 0.000000
- **Std Dev**: 0.000000
- **Min**: 0.000000
- **Max**: 0.000000
- **Above 0.1**: 0 (0.00%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.000000 | ✓ Median - typical error |
|  90.0% | 0.000000 | ✓ 90% of colors below this |
|  95.0% | 0.000000 | ✓ 95% of colors below this |
|  96.0% | 0.000000 | ✓ 96% of colors below this |
|  97.0% | 0.000000 | ✓ 97% of colors below this |
|  98.0% | 0.000000 | ✓ 98% of colors below this |
|  99.0% | 0.000000 | ✓ 99% of colors below this |
|  99.5% | 0.000000 | ✓ 99.5% of colors below this |
| 100.0% | 0.000000 | ✓ Maximum error |

## Chroma Differences

### Summary Statistics

- **Median**: 0.100000
- **Mean**: 0.079167
- **Std Dev**: 0.067572
- **Min**: 0.000000
- **Max**: 0.200000
- **Above 0.1**: 15 (31.25%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.100000 | ✓ Median - typical error |
|  90.0% | 0.200000 | ⚠️ 90% of colors below this |
|  95.0% | 0.200000 | ⚠️ 95% of colors below this |
|  96.0% | 0.200000 | ⚠️ 96% of colors below this |
|  97.0% | 0.200000 | ⚠️ 97% of colors below this |
|  98.0% | 0.200000 | ⚠️ 98% of colors below this |
|  99.0% | 0.200000 | ⚠️ 99% of colors below this |
|  99.5% | 0.200000 | ⚠️ 99.5% of colors below this |
| 100.0% | 0.200000 | ⚠️ Maximum error |

## Most Problematic Colors

**Total problematic colors**: 16 (showing top 16)

| Hex | RGB | Python | Rust | ΔH | ΔV | ΔC | Family |
|-----|-----|--------|------|----|----|----|---------|
| #0044bb | (0, 68, 187) | 6.5PB 3.3/15.2 | 6.5PB 3.3/15.4 | 0.000 | 0.000 | 0.200 | ✓ |
| #002266 | (0, 34, 102) | 6.1PB 1.6/9.1 | 6.1PB 1.6/9.3 | 0.000 | 0.000 | 0.200 | ✓ |
| #002255 | (0, 34, 85) | 5.5PB 1.4/7.0 | 5.6PB 1.4/7.2 | 0.100 | 0.000 | 0.200 | ✓ |
| #0044cc | (0, 68, 204) | 6.7PB 3.4/17.2 | 6.7PB 3.4/17.4 | 0.000 | 0.000 | 0.200 | ✓ |
| #0044dd | (0, 68, 221) | 6.8PB 3.6/19.2 | 6.8PB 3.6/19.4 | 0.000 | 0.000 | 0.200 | ✓ |
| #002277 | (0, 34, 119) | 6.4PB 1.8/11.3 | 6.4PB 1.8/11.5 | 0.000 | 0.000 | 0.200 | ✓ |
| #003311 | (0, 51, 17) | 9.6GY 1.7/5.4 | 9.7GY 1.7/5.6 | 0.100 | 0.000 | 0.200 | ✓ |
| #0044ee | (0, 68, 238) | 6.9PB 3.8/21.2 | 6.9PB 3.8/21.3 | 0.000 | 0.000 | 0.100 | ✓ |
| #0066ff | (0, 102, 255) | 6.6PB 4.7/19.0 | 6.6PB 4.7/19.1 | 0.000 | 0.000 | 0.100 | ✓ |
| #007711 | (0, 119, 17) | 9.6GY 4.2/10.7 | 9.6GY 4.2/10.8 | 0.000 | 0.000 | 0.100 | ✓ |
| #005533 | (0, 85, 51) | 2.3G 3.1/6.8 | 2.3G 3.1/6.9 | 0.000 | 0.000 | 0.100 | ✓ |
| #005577 | (0, 85, 119) | 7.4B 3.3/5.6 | 7.4B 3.3/5.7 | 0.000 | 0.000 | 0.100 | ✓ |
| #002222 | (0, 34, 34) | 3.0BG 1.1/3.0 | 3.1BG 1.1/3.0 | 0.100 | 0.000 | 0.000 | ✓ |
| #002233 | (0, 34, 51) | 6.6B 1.1/3.1 | 6.6B 1.1/3.2 | 0.000 | 0.000 | 0.100 | ✓ |
| #003333 | (0, 51, 51) | 3.4BG 1.8/3.8 | 3.4BG 1.8/3.9 | 0.000 | 0.000 | 0.100 | ✓ |
| #003344 | (0, 51, 68) | 4.0B 1.9/3.8 | 4.0B 1.9/3.9 | 0.000 | 0.000 | 0.100 | ✓ |

## Analysis and Conclusions

### Primary Issues

- **Chroma**: 31.2% exceed tolerance

### Strengths

- **Value calculation**: Near perfect accuracy
- **Hue calculation**: Excellent accuracy
- **Family assignment**: Very accurate

### Target vs Actual

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Overall Accuracy | 99.98% | 66.67% | Need improvement
| Hue within 0.1 | 100% | 97.92% | Need improvement
| Value within 0.1 | 100% | 100.00% | ✓
| Chroma within 0.1 | 100% | 68.75% | Need improvement
