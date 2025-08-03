# Investigation Summary - Mathematical Munsell Conversion

## Key Finding
The accuracy regression from 61% to 3.57% cannot be resolved through individual fixes. The algorithm appears to require a holistic approach where all corrections work together correctly.

## Critical Discovery
**The achromatic detection was fundamentally wrong**: We were checking achromatic relative to D65 illuminant, but Python checks relative to the value-specific achromatic center (which uses Illuminant C). This is a major architectural difference.

## Fixes Attempted

### 1. Achromatic Center Fix (Latest)
- **Issue**: Using D65 for achromatic detection instead of value-specific center
- **Fix**: Calculate rho_input relative to achromatic center for the specific value
- **Result**: No improvement (still 3.57% accuracy)

### 2. Previous Fixes (All Reverted)
- Achromatic threshold: 1e-3 (Python value) vs 1e-6
- Hue==0 normalization with family increment
- Chroma==0 returning achromatic
- Extrapolation after 2 points vs 4
- LinearInterpolator for chroma (no extrapolation)

## Why Individual Fixes Failed

The algorithm is highly interconnected:
1. The achromatic detection affects initial conditions
2. The initial guess affects convergence
3. The interpolation methods affect refinement
4. The normalization affects final output

Changing one part without adjusting the others breaks the delicate balance.

## Fundamental Issues Identified

1. **Illuminant Confusion**: Mixed use of D65 and Illuminant C coordinates
2. **Achromatic Detection**: Was checking wrong point (D65 instead of value-specific)
3. **Convergence Sensitivity**: Small changes cause massive accuracy swings
4. **Implementation Details**: Python has many subtle normalization rules

## Next Steps Required

1. **Start Fresh**: Go back to a known working state (if possible)
2. **Systematic Approach**: Apply ALL fixes together, not individually
3. **Deep Debugging**: Trace through specific colors to understand divergence
4. **Test Incrementally**: Verify each step matches Python exactly

## Conclusion

The mathematical Munsell conversion is extremely sensitive to implementation details. The Python colour-science implementation has many subtle behaviors that must ALL be replicated exactly. Individual fixes without understanding the complete system architecture lead to regression rather than improvement.

The 3.57% accuracy suggests the algorithm is fundamentally broken in its current state, not just missing small tweaks.