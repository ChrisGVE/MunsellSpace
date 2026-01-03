# Transformation Domain Comparison Report

Generated: 2026-01-03

Families analyzed: 21 (valid polyhedra with 3D extent)

## Domain Descriptions

| Domain | Description | Pros | Cons |
|--------|-------------|------|------|
| Munsell Cartesian | Direct transform in (x, y, z) | Preserves perceptual uniformity | Non-uniform geometry |
| RGB | Transform in RGB, convert back | Uniform geometry | Perceptually non-uniform |
| CIELAB | RGB → LAB → transform → Munsell | Perceptually uniform | Error accumulation |

## Summary Results

| Domain | Mean Loss | Std Loss | Ratio vs Best |
|--------|-----------|----------|---------------|
| Munsell Cartesian | 0.0535 | 0.0123 | 1.0x (baseline) |
| RGB | 1.4235 | 0.9419 | 26.6x worse |
| CIELAB | 1.6004 | 1.0120 | 29.9x worse |

## Key Findings

1. **Munsell Cartesian domain is dramatically better**
   - 27x lower loss than RGB domain
   - 30x lower loss than CIELAB domain
   - This is a decisive result

2. **RGB domain degrades accuracy**
   - Approximate Munsell→RGB→Munsell conversion introduces significant errors
   - Even uniform RGB geometry cannot compensate for conversion loss

3. **CIELAB domain is worst**
   - Two conversion steps (Munsell→RGB→LAB and LAB→Munsell)
   - Error accumulation outweighs any perceptual benefits

4. **Conversion errors dominate**
   - The approximate color space conversions introduce errors
   - These errors are larger than any optimization improvement

## Analysis

The dramatic difference (27-30x) between domains indicates that:

1. **Optimization in the target space is essential**
   - Transformations should be learned and applied in Munsell Cartesian
   - Any conversion step introduces unrecoverable errors

2. **Approximate conversions are inadequate**
   - RGB↔Munsell and LAB↔Munsell require full Munsell renotation data
   - Simple approximations are not suitable for precision work

3. **Perceptual uniformity is preserved**
   - Staying in Munsell Cartesian maintains perceptual meaning
   - The "non-uniform geometry" concern is not relevant for this task

## Recommendations

1. **Use Munsell Cartesian domain exclusively**
   - All transformations should be computed in native Munsell Cartesian space
   - The Translation+Scaling (6 params) approach with 0.053 mean loss is optimal

2. **Avoid intermediate conversions**
   - Do not convert to RGB or CIELAB for transformation
   - Conversion errors are prohibitive

3. **Hue-dependent transforms not needed**
   - Given Munsell Cartesian's strong performance, per-sector optimization adds
     complexity without benefit
   - Global Translation+Scaling is sufficient

4. **Practical implementation**
   - Input: Munsell Cartesian (x, y, z) screen coordinates
   - Transform: Scale + translate (6 parameters)
   - Output: Munsell Cartesian (x, y, z) surface-corrected coordinates

## Conclusion

The domain comparison definitively shows that **direct transformation in Munsell
Cartesian space is the only viable approach**. RGB and CIELAB domains introduce
conversion errors that are 27-30x larger than the transformation optimization can
correct. This finding simplifies the overall system design - we can confidently
use the Translation+Scaling transformation in native Munsell Cartesian coordinates.
