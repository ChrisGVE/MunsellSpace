# Munsell Conversion Backtesting Report

**Generated**: 2025-08-08T05:49:30.685279
**Dataset**: tests/data/srgb-to-munsell.csv
**Total Colors Tested**: 3841

## Executive Summary

- **Overall Accuracy**: 75.81% (2912/3841 within 0.1 tolerance)
- **Family Mismatches**: 11 colors
- **Hue Accuracy**: 96.09% within tolerance
- **Value Accuracy**: 97.27% within tolerance
- **Chroma Accuracy**: 80.50% within tolerance

## Key Issues Identified

1. **Low Chroma Colors (<2.0)**: 12 problematic colors
2. **High Chroma Colors (>15.0)**: 414 problematic colors
3. **Edge Cases (Value ≥9.0)**: 6 problematic colors
4. **Wrong Family Assignments**: 11 colors

See `BACKTESTING_DETAILS.md` for complete lists and detailed analysis.
