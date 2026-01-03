# Aggregation Method Comparison Report

Generated: 2026-01-03 17:37
Families analyzed: 23

## Aggregation Methods

| Method | Description |
|--------|-------------|
| mean | Arithmetic mean of family losses |
| sum | Total sum of family losses |
| weighted_mean | Mean weighted by sample count |
| minimax | Worst-case (maximum) loss |
| trimmed_mean_10 | Mean with 10% trimmed from each end |
| trimmed_mean_20 | Mean with 20% trimmed from each end |
| median | Median loss (robust to outliers) |

## Results Summary

| Method | Aggregated Loss | Mean Loss | Worst Family | Worst Loss |
|--------|-----------------|-----------|--------------|------------|
| mean | 0.4228 | 0.4228 | lime | 0.5708 |
| sum | 9.7238 | 0.4228 | lime | 0.5707 |
| trimmed_mean_10 | 0.4036 | 0.4260 | peach | 1.0551 |
| weighted_mean | 0.4224 | 0.4328 | coral | 0.6071 |
| minimax | 0.5417 | 0.4628 | gray | 0.5417 |
| trimmed_mean_20 | 0.3093 | 1.3021 | peach | 14.7544 |
| median | 0.3327 | 1.7685 | peach | 20.7072 |

## Outlier Analysis

Families appearing as worst across methods:

- **peach**: 3/7 methods
- **lime**: 2/7 methods
- **coral**: 1/7 methods
- **gray**: 1/7 methods

## Per-Family Loss Distribution (Mean Aggregation)

| Rank | Family | Loss | Weight |
|------|--------|------|--------|
| 1 | peach | 0.0984 | 36 |
| 2 | aquamarine | 0.3099 | 12 |
| 3 | violet | 0.3355 | 27 |
| 4 | gold | 0.3652 | 17 |
| 5 | fuchsia | 0.3705 | 16 |
| 6 | blue | 0.3811 | 121 |
| 7 | yellow | 0.3891 | 58 |
| 8 | plum | 0.4044 | 14 |
| 9 | tan | 0.4150 | 19 |
| 10 | wine | 0.4210 | 20 |
| 11 | mauve | 0.4235 | 14 |
| 12 | magenta | 0.4297 | 14 |
| 13 | white | 0.4339 | 14 |
| 14 | green | 0.4476 | 169 |
| 15 | gray | 0.4529 | 34 |
| 16 | aqua | 0.4612 | 14 |
| 17 | brown | 0.4640 | 37 |
| 18 | rust | 0.4669 | 15 |
| 19 | indigo | 0.4851 | 19 |
| 20 | teal | 0.5030 | 19 |
| 21 | red | 0.5371 | 34 |
| 22 | coral | 0.5579 | 23 |
| 23 | lime | 0.5708 | 28 |

## Key Findings

1. **Minimax vs Mean**: Worst-case loss improved by 5.1%
   - Mean method worst: 0.5708
   - Minimax method worst: 0.5417

2. **Loss distribution**: CV = 0.22 (std/mean)
   - Moderate variability, outliers not dominant

## Recommendations

1. **For general use**: Mean aggregation provides good balance
2. **For worst-case guarantees**: Use minimax optimization
3. **For robustness**: Consider trimmed mean or median
