# Munsell Conversion Backtesting Report

**Generated**: 2025-08-09T12:42:56.004276
**Dataset**: tests/data/srgb-to-munsell.csv
**Total Colors Tested**: 3984

## Executive Summary

- **Overall Accuracy**: 76.78% (3059/3984 within 0.1 tolerance)
- **Family Mismatches**: 10 colors
- **Hue Accuracy**: 96.23% within tolerance
- **Value Accuracy**: 97.36% within tolerance
- **Chroma Accuracy**: 81.35% within tolerance

## Key Issues Identified

1. **Low Chroma Colors (<2.0)**: 10 problematic colors
2. **High Chroma Colors (>15.0)**: 412 problematic colors
3. **Edge Cases (Value ≥9.0)**: 4 problematic colors
4. **Wrong Family Assignments**: 10 colors

See `BACKTESTING_DETAILS.md` for complete lists and detailed analysis.
