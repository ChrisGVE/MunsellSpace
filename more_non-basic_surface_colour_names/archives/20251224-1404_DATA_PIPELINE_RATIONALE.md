# Color Data Pipeline Rationale

## Data Sources

### 1. XKCD Color Survey (Crowdsourced Screen Colors)
- **Nature**: RGB/hex values displayed on computer monitors
- **Collection**: Users named colors they saw on their screens
- **175,844 unique names** from 3.4M responses
- **Limitation**: Screen colors, not physical colors; no illuminant control

### 2. Centore Reference Data (Measured Physical Colors)
- **Nature**: Spectrophotometer measurements of physical color samples
- **Collection**: Controlled laboratory conditions with known illuminant
- **Reference quality**: Ground truth for Munsell notation
- **Limitation**: Limited to measured samples only

## Pipeline Philosophy

### Why No Color Wheel Filtering

The color wheel consistency check compares color names against a theoretical HSL
color wheel (red=0°, green=120°, blue=240°). Initial implementation filtered out
"inconsistent" colors, but this was removed for important reasons:

1. **Perceptual vs. Theoretical**: XKCD data represents how people *perceive and
   name* screen colors, not where colors "should" be on a theoretical wheel.

2. **Screen vs. Physical Colors**: There may be systematic biases between:
   - How colors appear on screens (RGB/hex)
   - How physical colors are measured (spectrophotometer)

3. **Bias Detection Opportunity**: Colors that appear "inconsistent" (e.g., people
   calling cyan "blue") may reveal systematic perceptual shifts that are valuable
   for calibration.

4. **Future Correction**: By comparing XKCD-derived overlays with Centore reference
   overlays, we aim to:
   - Detect systematic biases between screen and physical color perception
   - Develop a correction/conversion from screen colors to physical color space
   - Apply this calibration to improve overlay accuracy

### Assumptions and Limitations

**First-order approximation**: This approach assumes that systematic biases between
screen color perception and physical color measurement can be detected and corrected.
This is a simplification that does NOT account for:

- **Illuminant differences**: Screen colors are self-luminous; physical colors are
  reflective under various light sources
- **Monitor calibration**: Different monitors display colors differently
- **Individual perception**: Color perception varies between individuals
- **Metamerism**: Colors that match on screen may not match physically

Despite these limitations, comparing crowdsourced screen color naming with
spectrophotometer-measured physical colors provides a reasonable starting point
for building semantic color overlays.

## Pipeline Stages

### Stage 1: Semantic Validation ✓
- **Input**: 175,844 raw XKCD color names
- **Method**: SBERT semantic similarity + 33K master vocabulary
- **Output**: 145,042 validated color names (82.5%)
- **Filter**: Yes - removes gibberish, sentences, non-color terms

### Stage 2: Color Wheel Consistency (Analysis Only) ✓
- **Input**: 145,042 validated names with RGB coordinates
- **Method**: Compare name semantics against HSL hue position
- **Output**: Consistency annotations (86.6% consistent, 13.4% flagged)
- **Filter**: NO - all colors retained; flags are informational only

### Stage 3: RGB → Munsell Conversion (Pending)
- **Input**: All 145,042 validated names with RGB
- **Method**: MunsellSpace library conversion
- **Output**: Color names with Munsell notation (H V/C)
- **Filter**: No

### Stage 4: Centore Comparison & Bias Detection (Pending)
- **Input**: XKCD-derived Munsell positions + Centore reference overlays
- **Method**: Compare centroid positions for overlapping color categories
- **Output**: Systematic bias vectors/corrections
- **Filter**: No - analysis only

### Stage 5: Calibration & Final Overlays (Pending)
- **Input**: Bias-corrected color positions
- **Method**: Apply calibration, build final overlay regions
- **Output**: Production semantic overlays for MunsellSpace

## Key Files

| File | Purpose |
|------|---------|
| `color_name_pipeline.py` | Stage 1: Semantic validation |
| `color_wheel_consistency.py` | Stage 2: Consistency analysis (no filter) |
| `validated_color_names.json` | 145K validated names with metadata |
| `full_scale_validation_summary.json` | Validation statistics |
| `color_wheel_consistency_results.json` | Consistency annotations |

## References

- XKCD Color Survey: https://blog.xkcd.com/2010/05/03/color-survey-results/
- Centore Polyhedron Data: Spectrophotometer measurements
- MunsellSpace: ASTM D1535 compliant RGB→Munsell conversion
