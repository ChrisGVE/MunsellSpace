# Munsell Conversion Backtesting Report

**Generated**: 2025-08-09T07:20:57.416690
**Dataset**: tests/data/srgb-to-munsell.csv
**Total Colors Tested**: 3984

## Executive Summary

- **Overall Accuracy**: 73.34% (2922/3984 within 0.1 tolerance)
- **Family Mismatches**: 13 colors
- **Hue Accuracy**: 93.90% within tolerance
- **Value Accuracy**: 97.36% within tolerance
- **Chroma Accuracy**: 77.89% within tolerance

## Key Issues Identified

1. **Low Chroma Colors (<2.0)**: 12 problematic colors
2. **High Chroma Colors (>15.0)**: 430 problematic colors
3. **Edge Cases (Value ≥9.0)**: 141 problematic colors
4. **Wrong Family Assignments**: 13 colors

See `BACKTESTING_DETAILS.md` for complete lists and detailed analysis.
