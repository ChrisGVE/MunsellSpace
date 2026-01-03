# Per-Family Volume Ratio Analysis (Task 99)

Generated: 2026-01-03

## Overview

This analysis examines how the RGB→Munsell volume mapping varies within each
color family's polyhedron. Using Monte Carlo sampling within convex hulls,
we compute per-family Jacobian statistics and correction factors.

## Reference: Global Jacobian Statistics

From Task 98 analysis (3375 sample points across RGB space):
- Mean |det(J)|: 2054.70
- CV (coefficient of variation): 0.0200

## Summary

- Valid families analyzed: 35
- Mean correction factor: 0.9989
- Correction factor std: 0.0000
- Range: [0.9989, 0.9989]
- Max deviation from global: 0.11%

## Per-Family Results

| Family | Mean |det(J)| | CV | Correction Factor | Deviation (%) |
|--------|----------------|------|-------------------|---------------|
| aqua | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| aquamarine | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| beige | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| blue | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| brown | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| coral | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| fuchsia | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| gold | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| gray | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| green | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| indigo | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| lavender | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| lilac | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| lime | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| magenta | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| maroon | 2052.52 | 0.0000 | 0.9989 | -0.11 |
| mauve | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| navy | 2052.52 | 0.0000 | 0.9989 | -0.11 |
| orange | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| peach | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| pink | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| plum | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| purple | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| red | 2052.52 | 0.0000 | 0.9989 | -0.11 |
| rose | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| rust | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| sand | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| tan | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| taupe | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| teal | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| turquoise | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| violet | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| white | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| wine | 2052.51 | 0.0000 | 0.9989 | -0.11 |
| yellow | 2052.51 | 0.0000 | 0.9989 | -0.11 |

## Implications

1. **Correction factors near 1.0**: Volume mapping is uniform across families
2. **Low per-family CV**: Jacobian is consistent within each polyhedron
3. **Max deviation indicates**: Whether per-family corrections are needed

## Recommendation

**No per-family correction needed**: Max deviation < 5%, use global scaling.