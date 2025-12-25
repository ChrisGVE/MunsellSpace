# Conclusion

## Summary of Contributions

This research presents a comprehensive pipeline for analyzing the relationship
between crowdsourced screen color names and physical color references. Through
four stages of processing - semantic validation, color wheel annotation,
RGB-to-Munsell conversion, and Centore comparison - we have quantified the
systematic biases that exist between screen and physical color perception.

### Key Contributions

1. **Semantic Validation Methodology**

   We demonstrated that sentence embeddings (SBERT) effectively filter
   freeform color naming data, retaining 137,878 valid names (78.4%) from
   the 175,844 XKCD entries. This approach outperforms string-matching,
   sample-count filtering, and character-level autoencoders.

2. **Universal Bias Quantification**

   Screen colors systematically differ from physical references:
   - **Value**: +0.81 units lighter (self-luminous vs reflective)
   - **Chroma**: +3.82 units more saturated (gamut and adaptation effects)

   These biases are consistent across categories and amenable to linear
   correction.

3. **Non-Uniform Hue Bias Discovery**

   The central finding: hue bias varies dramatically by color category.
   - Cool colors shift toward blue (-25° to -41°)
   - Warm earth tones shift toward yellow (+25° to +38°)
   - Core primaries are relatively accurate (±10°)

   This non-uniformity means **linear correction is fundamentally insufficient**.

4. **Framework for Non-Linear Modeling**

   We establish the requirements for non-linear hue correction and propose
   five modeling approaches: piecewise linear, polynomial, Gaussian Process,
   neural network, and spline interpolation.

---

## Implications

### For Color Science

The screen-physical color gap is not merely a calibration issue. Even with
perfect monitor calibration, fundamental differences in perception persist
due to:
- Self-luminous vs reflective light
- sRGB gamut limitations
- Chromatic adaptation states

Color naming studies using screen-displayed colors must account for these
systematic biases when generalizing to physical color perception.

### For Digital Design

Designers selecting colors on screen for physical production (print, paint,
textiles) should expect:
- Physical colors to appear darker than screen previews
- Physical colors to appear less saturated
- Warm and cool colors to shift in opposite hue directions

The correction factors quantified here provide a basis for more accurate
screen-to-physical color prediction.

### For Color Retrieval Systems

Systems that retrieve images by color name should consider:
- User color vocabulary reflects screen experience
- Named colors may not match physical expectations
- Category boundaries differ between screen and physical contexts

### For Semantic Overlay Construction

Building semantic color overlays from crowdsourced data requires:
- Semantic validation (not just frequency filtering)
- Bias correction if physical color targets are intended
- Acknowledgment that screen-based categories may not transfer to physical

---

## Limitations and Future Directions

### Current Limitations

1. **Temporal Snapshot**: XKCD data from 2010; monitor technology has evolved
2. **Language Bias**: English-only vocabulary; may not generalize cross-culturally
3. **Coarse Physical Reference**: Only 30 Centore categories; finer granularity possible
4. **No Individual Variation**: Aggregate analysis; individual differences not modeled

### Future Directions

1. **Non-Linear Hue Correction**: Implement and validate proposed modeling approaches
2. **Physical Validation**: Print corrected colors; measure with spectrophotometer
3. **Perceptual Validation**: User studies to confirm corrected colors "feel right"
4. **Modern Data Collection**: Replicate with contemporary color naming survey
5. **Cross-Linguistic Extension**: Analyze non-English color naming data

---

## Closing Remarks

The relationship between screen colors and physical colors is more complex
than a simple offset. Our discovery that hue bias is non-uniform - cool colors
shift cooler, warm colors shift warmer, while primaries remain stable -
reveals a structured pattern that can be modeled and corrected.

This work provides the foundation for building accurate semantic color overlays
that bridge the digital and physical worlds. By understanding and correcting
the systematic biases in crowdsourced screen color data, we can create tools
that better translate human color vocabulary into physical color reality.

The data, code, and detailed methodology are available for replication and
extension. We hope this work contributes to the ongoing effort to formalize
human color perception and enable more accurate color communication across
media.

---

## Reproducibility

All findings can be reproduced with the following pipeline:

```bash
# Stage 1: Semantic validation
python semantic-investigation/full_scale_validation.py

# Stage 2: Color wheel consistency
python semantic-investigation/color_wheel_consistency.py

# Stage 3: RGB to Munsell conversion
python semantic-investigation/rgb_to_munsell_conversion.py

# Stage 4: Centore comparison
python semantic-investigation/centore_comparison.py
```

Data files and intermediate results are available in the repository.

