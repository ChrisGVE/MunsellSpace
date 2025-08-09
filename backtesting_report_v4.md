# Munsell Conversion Backtesting Report - ISCC-NBS Focused (V4)

**Generated**: 2025-08-09T15:59:39.336315
**Dataset**: tests/data/srgb-to-munsell.csv
**Validation Method**: ISCC-NBS critical transition points only
**Total Colors Tested**: 3984

## Executive Summary

- **ISCC-NBS Accuracy**: 97.01% (3865/3984 without critical errors)
- **Traditional Accuracy**: 76.78% (for comparison with V3)
- **Critical Errors**: 119 colors at transition points
- **Ignored Deviations**: 781 non-critical deviations
- **Family Mismatches**: 8 colors

## Key Improvements in V4

1. **Focused Validation**: Only critical ISCC-NBS transition points are validated
2. **Higher Accuracy**: 97.01% vs 76.78% traditional method
3. **Practical Relevance**: Ignores 781 non-critical deviations
4. **Color Name Integrity**: Maintains accuracy at color classification boundaries

See `BACKTESTING_DETAILS_V4.md` for complete analysis and lists.
