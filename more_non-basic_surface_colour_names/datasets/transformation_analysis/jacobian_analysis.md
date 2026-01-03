# Jacobian Analysis: RGB↔Munsell Volume Distortion

Generated: 2026-01-03 18:01

## Overview

The Jacobian determinant |det(J)| represents the local volume scaling factor
when transforming from RGB to Munsell Cartesian space.

- |det(J)| > 1: RGB volumes **expand** in Munsell space
- |det(J)| < 1: RGB volumes **contract** in Munsell space
- |det(J)| ≈ 1: Volume-preserving transformation (locally)

## Sampling Statistics

- Total points sampled: 3375
- Valid Jacobian computations: 3375 (100.0%)

## Jacobian Determinant Statistics

| Statistic | Value |
|-----------|-------|
| Mean | 2054.7010 |
| Std Dev | 32.8340 |
| Median | 2052.5072 |
| Min | 2052.507191 |
| Max | 2546.1147 |
| 5th percentile | 2052.5072 |
| 95th percentile | 2052.5072 |

## Volume Scaling Distribution

- **Expansion (|det(J)| > 1)**: 100.0% of color space
- **Contraction (|det(J)| < 1)**: 0.0% of color space
- **Coefficient of Variation**: 0.02

**Moderate CV suggests reasonably uniform** volume mapping.

## Analysis by Munsell Value (Luminance)

| Value Range | Count | Mean |det(J)| | Std Dev |
|-------------|-------|---------------|---------|
| 0-3 | 64 | 2083.3577 | 119.4833 |
| 3-5 | 448 | 2056.9144 | 46.4328 |
| 5-7 | 819 | 2054.3153 | 29.8197 |
| 7-10 | 2044 | 2053.4732 | 21.8145 |

## Analysis by Munsell Chroma (Saturation)

| Chroma Range | Count | Mean |det(J)| | Std Dev |
|--------------|-------|---------------|---------|
| 0-4 | 735 | 2062.5808 | 69.7921 |
| 4-8 | 1296 | 2052.5072 | 0.0000 |
| 8-12 | 1260 | 2052.5072 | 0.0000 |
| 12-20 | 84 | 2052.5072 | 0.0000 |

## High Distortion Regions

Threshold (95th percentile): |det(J)| > 2052.5072
Number of points: 169

## Key Findings

1. **Overall expansion**: Mean |det(J)| = 2054.70 indicates RGB volumes expand ~2054.7x in Munsell
2. **Non-uniformity**: CV = 0.02 - Moderate spatial variation in volume mapping

## Implications for Transformation Search

- Volume matching in loss function may benefit from Jacobian weighting
- Per-family correction factors can account for local distortion
- High-distortion regions may require special handling
