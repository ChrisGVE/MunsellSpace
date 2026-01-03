# Alternative Loss Metrics Comparison Report

Generated: 2026-01-03 17:32
Families analyzed: 21

## Metric Definitions

| Metric | Description | Range |
|--------|-------------|-------|
| centroid | Normalized centroid distance | [0, ∞) |
| volume | Volume ratio deviation |V_s/V_t - 1| | [0, ∞) |
| hausdorff | Normalized average Hausdorff distance | [0, 1] |
| chamfer | Normalized symmetric Chamfer distance | [0, 1] |
| emd | Normalized Earth Mover's Distance | [0, 1] |
| spectral | Eigenvalue spectrum L2 distance | [0, √3] |
| iou | 1 - Jaccard index (Monte Carlo) | [0, 1] |

## Metric Statistics

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| centroid | 0.9272 | 0.4090 | 0.3698 | 2.0239 |
| volume | 21.3749 | 54.3570 | 0.0544 | 243.0886 |
| hausdorff | 0.2928 | 0.0995 | 0.1316 | 0.5139 |
| chamfer | 0.2822 | 0.1058 | 0.1050 | 0.5135 |
| emd | 0.3891 | 0.1119 | 0.1946 | 0.5851 |
| spectral | 0.2069 | 0.1252 | 0.0343 | 0.5386 |
| iou | 0.9127 | 0.0951 | 0.6531 | 1.0000 |

## Metric Correlations

Pearson correlation coefficients between metrics:

| | centroid | volume | hausdorff | chamfer | emd | spectral | iou |
|-|-|-|-|-|-|-|-|
| centroid | 1.00 | -0.26 | 0.40 | 0.35 | 0.57 | -0.18 | 0.22 |
| volume | -0.26 | 1.00 | 0.49 | 0.50 | 0.45 | -0.19 | 0.31 |
| hausdorff | 0.40 | 0.49 | 1.00 | 0.99 | 0.91 | -0.31 | 0.69 |
| chamfer | 0.35 | 0.50 | 0.99 | 1.00 | 0.91 | -0.33 | 0.70 |
| emd | 0.57 | 0.45 | 0.91 | 0.91 | 1.00 | -0.32 | 0.54 |
| spectral | -0.18 | -0.19 | -0.31 | -0.33 | -0.32 | 1.00 | -0.37 |
| iou | 0.22 | 0.31 | 0.69 | 0.70 | 0.54 | -0.37 | 1.00 |

## Per-Family Results

| Family | Centroid | Volume | Hausdorff | Chamfer | EMD | Spectral | IoU |
|--------|----------|--------|-----------|---------|-----|----------|-----|
| aqua | 1.4644 | 3.4191 | 0.4622 | 0.4584 | 0.5414 | 0.1716 | 1.0000 |
| aquamarine | 0.7744 | 72.7785 | 0.5139 | 0.5135 | 0.5851 | 0.1297 | 0.9990 |
| blue | 0.8865 | 3.2643 | 0.2986 | 0.2925 | 0.3330 | 0.0343 | 0.9326 |
| brown | 1.3917 | 5.5686 | 0.3082 | 0.2942 | 0.4691 | 0.1416 | 0.9839 |
| coral | 1.0835 | 3.9653 | 0.2849 | 0.2761 | 0.4116 | 0.0386 | 0.9552 |
| fuchsia | 0.3977 | 2.5588 | 0.1833 | 0.1850 | 0.2403 | 0.3822 | 0.8345 |
| gold | 0.4054 | 8.5237 | 0.2538 | 0.2458 | 0.3302 | 0.0711 | 0.9555 |
| green | 1.4011 | 0.0544 | 0.2545 | 0.2198 | 0.4022 | 0.3508 | 0.9140 |
| indigo | 1.1304 | 8.6288 | 0.3416 | 0.3523 | 0.4152 | 0.2856 | 0.9851 |
| lime | 0.9179 | 3.8611 | 0.2951 | 0.2507 | 0.3541 | 0.2323 | 0.9523 |
| magenta | 0.7599 | 0.6495 | 0.2252 | 0.2211 | 0.3079 | 0.2318 | 0.8360 |
| mauve | 1.0387 | 1.4428 | 0.2995 | 0.3005 | 0.4718 | 0.2589 | 0.8503 |
| peach | 0.5003 | 243.0886 | 0.4319 | 0.4313 | 0.5391 | 0.0969 | 0.9955 |
| plum | 0.3698 | 0.0570 | 0.1977 | 0.1598 | 0.1946 | 0.5386 | 0.8913 |
| red | 1.1577 | 0.6383 | 0.1316 | 0.1050 | 0.3067 | 0.2122 | 0.6866 |
| rust | 0.4884 | 3.1620 | 0.2036 | 0.2107 | 0.2912 | 0.1546 | 0.9735 |
| tan | 1.0791 | 2.4149 | 0.3071 | 0.3098 | 0.4352 | 0.2298 | 0.8915 |
| teal | 2.0239 | 0.4475 | 0.4295 | 0.4039 | 0.5495 | 0.1282 | 1.0000 |
| violet | 0.8486 | 83.6505 | 0.3548 | 0.3700 | 0.4757 | 0.2832 | 0.9849 |
| wine | 0.7134 | 0.3998 | 0.1761 | 0.1576 | 0.2127 | 0.0429 | 0.8919 |
| yellow | 0.6388 | 0.2989 | 0.1962 | 0.1678 | 0.3048 | 0.3300 | 0.6531 |

## Key Findings

### Highly Correlated Metrics (|r| > 0.7)

- hausdorff ↔ chamfer: r = 0.99
- hausdorff ↔ emd: r = 0.91
- chamfer ↔ emd: r = 0.91
- chamfer ↔ iou: r = 0.70

### Metric Independence

Metrics with low correlation to centroid (potentially capturing different aspects):

- volume: r = -0.26
- hausdorff: r = 0.40
- chamfer: r = 0.35
- spectral: r = -0.18
- iou: r = 0.22

## Recommendations

1. **Primary metrics**: volume + hausdorff (established, interpretable)
2. **Alternative for shape**: chamfer distance (efficient, robust)
3. **For distribution comparison**: EMD (captures spread differences)
4. **For overlap assessment**: IoU (intuitive, but Monte Carlo variance)
5. **For covariance shape**: spectral loss (captures orientation/spread)
