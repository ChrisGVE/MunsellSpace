# Munsell Conversion Backtesting Report

**Generated**: 2025-08-07T19:37:57.677076
**Dataset**: tests/data/srgb-to-munsell.csv
**Total Colors Tested**: 3,744

## Executive Summary

- **Overall Accuracy**: 78.79% (2,950/3,744 within 0.1 tolerance)
- **Family Mismatches**: 0.13% (5 colors)
- **Hue Accuracy**: 97.38% within tolerance
- **Value Accuracy**: 99.89% within tolerance
- **Chroma Accuracy**: 80.32% within tolerance

## Family Mismatches

**Total**: 5 (0.13%)

### Top Transitions

| From → To | Count | Percentage |
|-----------|-------|------------|
| PB→Unknown | 2 | 40.0% |
| R→RP | 1 | 20.0% |
| RP→P | 1 | 20.0% |
| YR→R | 1 | 20.0% |

## Hue Differences

### Summary Statistics

- **Median**: 0.000000
- **Mean**: 0.007292
- **Std Dev**: 0.027691
- **Min**: 0.000000
- **Max**: 0.300000
- **Above 0.1**: 98 (2.62%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.000000 | ✓ Median - typical error |
|  90.0% | 0.000000 | ✓ 90% of colors below this |
|  95.0% | 0.100000 | ✓ 95% of colors below this |
|  96.0% | 0.100000 | ✓ 96% of colors below this |
|  97.0% | 0.100000 | ✓ 97% of colors below this |
|  98.0% | 0.100000 | ⚠️ 98% of colors below this |
|  99.0% | 0.100000 | ⚠️ 99% of colors below this |
|  99.5% | 0.100000 | ⚠️ 99.5% of colors below this |
| 100.0% | 0.300000 | ⚠️ Maximum error |

## Value Differences

### Summary Statistics

- **Median**: 0.000000
- **Mean**: 0.000294
- **Std Dev**: 0.005412
- **Min**: 0.000000
- **Max**: 0.100000
- **Above 0.1**: 4 (0.11%)

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
| 100.0% | 0.100000 | ⚠️ Maximum error |

## Chroma Differences

### Summary Statistics

- **Median**: 0.000000
- **Mean**: 0.048371
- **Std Dev**: 0.067760
- **Min**: 0.000000
- **Max**: 0.600000
- **Above 0.1**: 737 (19.68%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.000000 | ✓ Median - typical error |
|  90.0% | 0.100000 | ⚠️ 90% of colors below this |
|  95.0% | 0.200000 | ⚠️ 95% of colors below this |
|  96.0% | 0.200000 | ⚠️ 96% of colors below this |
|  97.0% | 0.200000 | ⚠️ 97% of colors below this |
|  98.0% | 0.200000 | ⚠️ 98% of colors below this |
|  99.0% | 0.300000 | ⚠️ 99% of colors below this |
|  99.5% | 0.300000 | ⚠️ 99.5% of colors below this |
| 100.0% | 0.600000 | ⚠️ Maximum error |

## Most Problematic Colors

**Total problematic colors**: 794 (showing top 20)

| Hex | RGB | Python | Rust | ΔH | ΔV | ΔC | Family |
|-----|-----|--------|------|----|----|----|---------|
| #ddeeee | (221, 238, 238) | 7.1G 9.3/2.1 | 7.1G 9.3/1.5 | 0.000 | 0.000 | 0.600 | ✓ |
| #4400bb | (68, 0, 187) | 8.3PB 2.6/20.7 | 8.3PB 2.6/21.1 | 0.000 | 0.000 | 0.400 | ✓ |
| #221177 | (34, 17, 119) | 7.4PB 1.6/13.1 | 7.5PB 1.6/13.5 | 0.100 | 0.000 | 0.400 | ✓ |
| #330077 | (51, 0, 119) | 9.0PB 1.5/14.2 | 9.0PB 1.5/14.6 | 0.000 | 0.000 | 0.400 | ✓ |
| #440066 | (68, 0, 102) | 2.5P 1.6/11.9 | 2.5P 1.6/12.3 | 0.000 | 0.000 | 0.400 | ✓ |
| #330088 | (51, 0, 136) | 8.3PB 1.8/16.0 | 8.4PB 1.8/16.4 | 0.100 | 0.000 | 0.400 | ✓ |
| #3311bb | (51, 17, 187) | 7.5PB 2.6/20.3 | 7.5PB 2.6/20.7 | 0.000 | 0.000 | 0.400 | ✓ |
| #220077 | (34, 0, 119) | 7.4PB 1.3/14.6 | 7.4PB 1.3/14.9 | 0.000 | 0.000 | 0.300 | ✓ |
| #221166 | (34, 17, 102) | 7.9PB 1.3/11.1 | 7.9PB 1.3/11.4 | 0.000 | 0.000 | 0.300 | ✓ |
| #3300bb | (51, 0, 187) | 7.4PB 2.4/21.2 | 7.5PB 2.4/21.5 | 0.100 | 0.000 | 0.300 | ✓ |
| #3333dd | (51, 51, 221) | 7.4PB 3.4/20.9 | 7.4PB 3.4/21.2 | 0.000 | 0.000 | 0.300 | ✓ |
| #3333ee | (51, 51, 238) | 7.3PB 3.6/22.8 | 7.3PB 3.6/23.1 | 0.000 | 0.000 | 0.300 | ✓ |
| #3322bb | (51, 34, 187) | 7.5PB 2.8/18.9 | 7.5PB 2.8/19.2 | 0.000 | 0.000 | 0.300 | ✓ |
| #4422ff | (68, 34, 255) | 7.6PB 3.6/25.9 | 7.6PB 3.6/26.2 | 0.000 | 0.000 | 0.300 | ✓ |
| #440055 | (68, 0, 85) | 5.4P 1.5/10.2 | 5.4P 1.5/10.5 | 0.000 | 0.000 | 0.300 | ✓ |
| #4400cc | (68, 0, 204) | 8.0PB 2.8/22.4 | 8.0PB 2.8/22.7 | 0.000 | 0.000 | 0.300 | ✓ |
| #4433dd | (68, 51, 221) | 7.8PB 3.5/20.7 | 7.8PB 3.5/21.0 | 0.000 | 0.000 | 0.300 | ✓ |
| #4433ee | (68, 51, 238) | 7.7PB 3.7/22.7 | 7.7PB 3.7/23.0 | 0.000 | 0.000 | 0.300 | ✓ |
| #4411bb | (68, 17, 187) | 8.3PB 2.7/20.0 | 8.3PB 2.7/20.3 | 0.000 | 0.000 | 0.300 | ✓ |
| #4411ee | (68, 17, 238) | 7.7PB 3.3/25.2 | 7.7PB 3.3/25.5 | 0.000 | 0.000 | 0.300 | ✓ |

## Analysis and Conclusions

### Primary Issues

- **Chroma**: 19.7% exceed tolerance

### Strengths

- **Value calculation**: Near perfect accuracy
- **Hue calculation**: Excellent accuracy
- **Family assignment**: Very accurate

### Target vs Actual

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Overall Accuracy | 99.98% | 78.79% | Need improvement
| Hue within 0.1 | 100% | 97.38% | Need improvement
| Value within 0.1 | 100% | 99.89% | Need improvement
| Chroma within 0.1 | 100% | 80.32% | Need improvement
