# Pairwise Loss Component Trade-off Analysis

Generated: 2026-01-03 14:51
Families analyzed: 21

## Methodology

Pairs of loss components optimized together using Translation+Scaling (6 params):

- **Centroid + Volume**: Shape free to vary
- **Centroid + Shape**: Volume free to vary
- **Volume + Shape**: Centroid free to vary

Each pair uses equal weights (0.5, 0.5) in the pairwise loss.

## Summary Results

| Pair | Mean Combined | Excluded | Excluded Value |
|------|---------------|----------|----------------|
| centroid+volume | 0.0561 | shape | 0.1799 |
| centroid+shape | 0.1580 | volume | 0.3566 |
| volume+shape | 0.0789 | centroid | 0.0692 |

## Comparison with Single-Component Optimization

| Pair | Combined Loss | Best Single | Difference |
|------|---------------|-------------|------------|
| centroid+volume | 0.0561 | volume=0.0540 | +0.0021 |
| centroid+shape | 0.1580 | centroid=0.1580 | +0.0000 |
| volume+shape | 0.0789 | volume=0.0540 | +0.0249 |

## Key Findings

1. **Best pairwise strategy**: centroid+volume
   - Achieves combined loss of 0.0561

2. **Excluded component behavior**:
   - centroid+volume: shape = 0.1799 (acceptable)
   - centroid+shape: volume = 0.3566 (degraded)
   - volume+shape: centroid = 0.0692 (acceptable)

3. **Trade-off insights**:
   - Volume-only (0.0540) still outperforms best pairwise (0.0561)
   - This confirms volume matching as the dominant objective

## Recommendations

1. Proceed with Pareto frontier analysis to find optimal trade-off points
2. Consider adaptive weighting based on family characteristics
3. Volume matching appears critical - ensure it's prioritized in final solution

## Per-Family Results

### Centroid + Volume (excludes shape)

| Family | Combined | Centroid | Volume | Shape |
|--------|----------|----------|--------|-------|
| wine | 0.0326 | 0.0013 | 0.0000 | 0.1069 |
| violet | 0.0382 | 0.0005 | 0.0000 | 0.1266 |
| fuchsia | 0.0424 | 0.0000 | 0.0000 | 0.1413 |
| peach | 0.0452 | 0.0000 | 0.0000 | 0.1506 |
| brown | 0.0496 | 0.0000 | 0.0000 | 0.1652 |
| plum | 0.0507 | 0.0000 | 0.0000 | 0.1689 |
| aquamarine | 0.0512 | 0.0068 | 0.0000 | 0.1616 |
| red | 0.0526 | 0.0083 | 0.0000 | 0.1644 |
| yellow | 0.0534 | 0.0281 | 0.0000 | 0.1403 |
| rust | 0.0545 | 0.0000 | 0.0000 | 0.1817 |
| green | 0.0555 | 0.0000 | 0.0000 | 0.1850 |
| magenta | 0.0561 | 0.0006 | 0.0000 | 0.1861 |
| gold | 0.0569 | 0.0063 | 0.0000 | 0.1814 |
| tan | 0.0595 | 0.0000 | 0.0000 | 0.1984 |
| teal | 0.0601 | 0.0000 | 0.0000 | 0.2003 |
| coral | 0.0618 | 0.0011 | 0.0000 | 0.2047 |
| indigo | 0.0644 | 0.0087 | 0.0000 | 0.2030 |
| blue | 0.0662 | 0.0139 | 0.0000 | 0.2022 |
| lime | 0.0749 | 0.0000 | 0.0000 | 0.2496 |
| mauve | 0.0753 | 0.0235 | 0.0000 | 0.2196 |
| aqua | 0.0778 | 0.0150 | 0.0000 | 0.2395 |

### Centroid + Shape (excludes volume)

| Family | Combined | Centroid | Volume | Shape |
|--------|----------|----------|--------|-------|
| indigo | 0.0682 | 0.0000 | 0.1094 | 0.1180 |
| wine | 0.0811 | 0.0000 | 0.1627 | 0.1077 |
| brown | 0.0898 | 0.0000 | 0.1352 | 0.1640 |
| coral | 0.0927 | 0.0000 | 0.1090 | 0.2001 |
| green | 0.0962 | 0.0000 | 0.1363 | 0.1845 |
| peach | 0.1052 | 0.0000 | 0.1990 | 0.1517 |
| blue | 0.1138 | 0.0000 | 0.2399 | 0.1395 |
| red | 0.1331 | 0.0000 | 0.2820 | 0.1619 |
| rust | 0.1334 | 0.0000 | 0.2618 | 0.1827 |
| teal | 0.1383 | 0.0000 | 0.2704 | 0.1906 |
| magenta | 0.1430 | 0.0000 | 0.2979 | 0.1788 |
| aquamarine | 0.1807 | 0.0000 | 0.4458 | 0.1567 |
| aqua | 0.1854 | 0.0000 | 0.3824 | 0.2357 |
| lime | 0.1891 | 0.0000 | 0.3732 | 0.2570 |
| tan | 0.1911 | 0.0000 | 0.4534 | 0.1837 |
| gold | 0.1939 | 0.0000 | 0.4857 | 0.1608 |
| fuchsia | 0.2138 | 0.0000 | 0.5712 | 0.1413 |
| yellow | 0.2174 | 0.0000 | 0.5820 | 0.1427 |
| plum | 0.2193 | 0.0000 | 0.5633 | 0.1676 |
| mauve | 0.2599 | 0.0000 | 0.6534 | 0.2130 |
| violet | 0.2715 | 0.0000 | 0.7755 | 0.1295 |

### Volume + Shape (excludes centroid)

| Family | Combined | Centroid | Volume | Shape |
|--------|----------|----------|--------|-------|
| wine | 0.0320 | 0.0001 | 0.0000 | 0.1065 |
| indigo | 0.0349 | 0.0000 | 0.0000 | 0.1164 |
| violet | 0.0380 | 0.0000 | 0.0000 | 0.1266 |
| yellow | 0.0418 | 0.0004 | 0.0000 | 0.1390 |
| fuchsia | 0.0426 | 0.0003 | 0.0000 | 0.1415 |
| peach | 0.0451 | 0.0000 | 0.0000 | 0.1502 |
| aquamarine | 0.0484 | 0.0002 | 0.0000 | 0.1612 |
| brown | 0.0496 | 0.0002 | 0.0000 | 0.1652 |
| plum | 0.0506 | 0.0000 | 0.0000 | 0.1688 |
| green | 0.0555 | 0.0002 | 0.0000 | 0.1849 |
| tan | 0.0598 | 0.0007 | 0.0000 | 0.1983 |
| teal | 0.0599 | 0.0003 | 0.0000 | 0.1992 |
| blue | 0.0606 | 0.0003 | 0.0000 | 0.2017 |
| coral | 0.0613 | 0.0001 | 0.0000 | 0.2044 |
| mauve | 0.0664 | 0.0010 | 0.0000 | 0.2198 |
| aqua | 0.0723 | 0.0001 | 0.0000 | 0.2408 |
| lime | 0.0749 | 0.0005 | 0.0000 | 0.2491 |
| magenta | 0.1518 | 0.2559 | 0.0000 | 0.1648 |
| rust | 0.1633 | 0.2876 | 0.0000 | 0.1609 |
| gold | 0.1941 | 0.3756 | 0.0000 | 0.1464 |
| red | 0.2541 | 0.5305 | 0.0000 | 0.1395 |
