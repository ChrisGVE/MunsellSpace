# Reference Test Colors for Validation

This is our standard test set for quickly validating changes to the mathematical conversion algorithm.

## Test Set (12 colors)

| RGB | Description | Expected Python | Current Rust | Status |
|-----|-------------|-----------------|--------------|--------|
| [255,0,0] | R high chroma | 7.9R 5.2/20.4 | 7.9R 5.2/20.4 | ✓ Exact |
| [255,128,0] | YR high chroma | 3.7YR 6.6/14.7 | 3.7YR 6.6/14.7 | ✓ Exact |
| [0,255,0] | G high chroma | 9.9GY 8.7/19.4 | 9.9GY 8.7/19.4 | ✓ Exact |
| [0,0,255] | B high chroma | (Python error) | 6.9PB 3.2/28.4 | N/A |
| [128,0,128] | P high chroma | 9.3P 2.9/13.8 | 9.2P 2.9/13.7 | ~0.1 diff |
| [150,100,100] | R medium | 7.4R 4.7/4.0 | 7.4R 4.7/4.0 | ✓ Exact |
| [100,150,100] | G medium | 0.3G 5.6/6.2 | 0.3G 5.6/6.3 | ~0.1 chroma |
| [160,120,120] | Low chroma R | 8.4R 5.3/3.1 | 8.4R 5.3/3.1 | ✓ Exact |
| [120,140,160] | Low chroma B | 8.0B 5.6/2.7 | 8.0B 5.6/2.7 | ✓ Exact |
| [100,50,50] | Dark red | 8.3R 2.7/4.4 | 8.2R 2.7/4.4 | ~0.1 hue |
| [200,160,160] | Light red | 9.2R 6.9/3.0 | 9.1R 6.9/3.1 | ~0.1 diff |
| [238,0,85] | Test case R | 3.0R 4.9/17.6 | 2.6R 5.0/18.1 | Oscillation |

## Summary Statistics
- **Exact matches**: 6/12 (50%)
- **Family matches**: 11/12 (92% excluding Python error)
- **Within 0.1 tolerance**: 10/12 (83%)
- **Problem cases**: 1 (oscillation on [238,0,85])

## Usage
Run `python3 test_colors.py` to check current accuracy against this reference set.

## Notes
- Python cannot handle pure blue [0,0,255] - outside Munsell renotation dataset
- Python requires chroma >= 2.0
- Most differences are ~0.1 in hue or chroma
- Main issue is oscillation/convergence for [238,0,85]