# Munsell Conversion Backtesting Report

**Generated**: 2025-08-07T14:17:26.156426
**Dataset**: tests/data/srgb-to-munsell.csv
**Total Colors Tested**: 482

## Executive Summary

- **Overall Accuracy**: 82.78% (399/482 within 0.1 tolerance)
- **Family Mismatches**: 1.66% (8 colors)
- **Hue Accuracy**: 98.34% within tolerance
- **Value Accuracy**: 100.00% within tolerance
- **Chroma Accuracy**: 84.44% within tolerance

## Family Mismatches

**Total**: 8 (1.66%)

### Top Transitions

| From → To | Count | Percentage |
|-----------|-------|------------|
| G→GY | 6 | 75.0% |
| B→BG | 1 | 12.5% |
| BG→G | 1 | 12.5% |

## Hue Differences

### Summary Statistics

- **Median**: 0.024560
- **Mean**: 0.190675
- **Std Dev**: 1.270905
- **Min**: 0.000045
- **Max**: 9.994371
- **Above 0.1**: 8 (1.66%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.024560 | ✓ Median - typical error |
|  90.0% | 0.047842 | ✓ 90% of colors below this |
|  95.0% | 0.053273 | ✓ 95% of colors below this |
|  96.0% | 0.054316 | ✓ 96% of colors below this |
|  97.0% | 0.058835 | ✓ 97% of colors below this |
|  98.0% | 0.067358 | ✓ 98% of colors below this |
|  99.0% | 9.961002 | ⚠️ 99% of colors below this |
|  99.5% | 9.977337 | ⚠️ 99.5% of colors below this |
| 100.0% | 9.994371 | ⚠️ Maximum error |

## Value Differences

### Summary Statistics

- **Median**: 0.025801
- **Mean**: 0.025086
- **Std Dev**: 0.014421
- **Min**: 0.000178
- **Max**: 0.050169
- **Above 0.1**: 0 (0.00%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.025801 | ✓ Median - typical error |
|  90.0% | 0.044976 | ✓ 90% of colors below this |
|  95.0% | 0.047291 | ✓ 95% of colors below this |
|  96.0% | 0.047623 | ✓ 96% of colors below this |
|  97.0% | 0.047995 | ✓ 97% of colors below this |
|  98.0% | 0.048745 | ✓ 98% of colors below this |
|  99.0% | 0.049220 | ✓ 99% of colors below this |
|  99.5% | 0.049724 | ✓ 99.5% of colors below this |
| 100.0% | 0.050169 | ✓ Maximum error |

## Chroma Differences

### Summary Statistics

- **Median**: 0.039132
- **Mean**: 0.056253
- **Std Dev**: 0.055904
- **Min**: 0.000003
- **Max**: 0.366607
- **Above 0.1**: 75 (15.56%)

### Percentile Distribution

| Percentile | Value | Analysis |
|------------|-------|----------|
|  50.0% | 0.039132 | ✓ Median - typical error |
|  90.0% | 0.130236 | ⚠️ 90% of colors below this |
|  95.0% | 0.183458 | ⚠️ 95% of colors below this |
|  96.0% | 0.197966 | ⚠️ 96% of colors below this |
|  97.0% | 0.207300 | ⚠️ 97% of colors below this |
|  98.0% | 0.220028 | ⚠️ 98% of colors below this |
|  99.0% | 0.241321 | ⚠️ 99% of colors below this |
|  99.5% | 0.269097 | ⚠️ 99.5% of colors below this |
| 100.0% | 0.366607 | ⚠️ Maximum error |

## Most Problematic Colors

**Total problematic colors**: 83 (showing top 20)

| Hex | RGB | Python | Rust | ΔH | ΔV | ΔC | Family |
|-----|-----|--------|------|----|----|----|---------|
| #11cc22 | (17, 204, 34) | 0.0G 7.1/16.2 | 0.0G 7.1/16.2 | 9.994 | 0.001 | 0.011 | ✗ |
| #11dd22 | (17, 221, 34) | 0.0G 7.7/17.2 | 0.0G 7.7/17.2 | 9.990 | 0.040 | 0.024 | ✗ |
| #007788 | (0, 119, 136) | 0.0B 4.5/6.0 | 0.0B 4.5/6.0 | 9.977 | 0.029 | 0.010 | ✗ |
| #118877 | (17, 136, 119) | 0.0BG 5.0/7.2 | 0.0BG 5.0/7.2 | 9.977 | 0.024 | 0.016 | ✗ |
| #00bb22 | (0, 187, 34) | 0.0G 6.5/15.1 | 0.0G 6.5/15.1 | 9.962 | 0.028 | 0.016 | ✗ |
| #117722 | (17, 119, 34) | 0.0G 4.3/9.9 | 0.0G 4.3/9.9 | 9.961 | 0.042 | 0.014 | ✗ |
| #11ee22 | (17, 238, 34) | 0.0G 8.2/18.1 | 0.0G 8.2/18.1 | 9.960 | 0.014 | 0.008 | ✗ |
| #11ff22 | (17, 255, 34) | 0.0G 8.8/18.8 | 0.0G 8.8/18.9 | 9.959 | 0.041 | 0.053 | ✗ |
| #221177 | (34, 17, 119) | 7.4PB 1.6/13.1 | 7.5PB 1.6/13.5 | 0.059 | 0.045 | 0.367 | ✓ |
| #221166 | (34, 17, 102) | 7.9PB 1.3/11.1 | 7.9PB 1.3/11.4 | 0.050 | 0.045 | 0.281 | ✓ |
| #220077 | (34, 0, 119) | 7.4PB 1.3/14.6 | 7.4PB 1.3/14.9 | 0.013 | 0.028 | 0.281 | ✓ |
| #112266 | (17, 34, 102) | 6.6PB 1.6/8.9 | 6.6PB 1.6/9.2 | 0.027 | 0.032 | 0.251 | ✓ |
| #223388 | (34, 51, 136) | 6.9PB 2.5/10.9 | 6.9PB 2.5/11.1 | 0.027 | 0.004 | 0.248 | ✓ |
| #1133dd | (17, 51, 221) | 6.9PB 3.3/21.2 | 7.0PB 3.3/21.4 | 0.052 | 0.011 | 0.240 | ✓ |
| #1144cc | (17, 68, 204) | 6.8PB 3.5/17.2 | 6.8PB 3.5/17.4 | 0.038 | 0.031 | 0.236 | ✓ |
| #002266 | (0, 34, 102) | 6.1PB 1.6/9.1 | 6.1PB 1.6/9.3 | 0.007 | 0.029 | 0.235 | ✓ |
| #112255 | (17, 34, 85) | 6.2PB 1.5/6.8 | 6.2PB 1.5/7.0 | 0.021 | 0.028 | 0.222 | ✓ |
| #003311 | (0, 51, 17) | 9.6GY 1.7/5.4 | 9.7GY 1.7/5.6 | 0.052 | 0.022 | 0.222 | ✓ |
| #222255 | (34, 34, 85) | 7.6PB 1.6/6.5 | 7.6PB 1.6/6.7 | 0.003 | 0.010 | 0.219 | ✓ |
| #0033aa | (0, 51, 170) | 6.6PB 2.7/15.2 | 6.6PB 2.7/15.4 | 0.012 | 0.019 | 0.217 | ✓ |

## Analysis and Conclusions

### Primary Issues

- **Chroma**: 15.6% exceed tolerance

### Strengths

- **Value calculation**: Near perfect accuracy
- **Hue calculation**: Excellent accuracy
- **Family assignment**: Very accurate

### Target vs Actual

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Overall Accuracy | 99.98% | 82.78% | Need improvement
| Hue within 0.1 | 100% | 98.34% | Need improvement
| Value within 0.1 | 100% | 100.00% | ✓
| Chroma within 0.1 | 100% | 84.44% | Need improvement
