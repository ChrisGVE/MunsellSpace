#!/usr/bin/env python3
"""Test how Python handles value > 9 with chroma < 2."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import (
    xy_from_renotation_ovoid,
    munsell_specification_to_xy,
    normalise_munsell_specification
)

# Test high values with low chromas
test_specs = [
    [9.96, 9.54, 1.96, 6.0],  # Python's result for RGB(255,238,238)
    [9.96, 9.54, 1.0, 6.0],   # Lower chroma test
    [9.96, 9.54, 0.5, 6.0],   # Very low chroma test
]

print("Testing high value (>9) with low chroma (<2):")
print("=" * 60)

for spec in test_specs:
    print(f"\nSpec: hue={spec[0]:.2f}, value={spec[1]:.2f}, chroma={spec[2]:.2f}, code={spec[3]}")
    
    # Normalize
    spec_norm = normalise_munsell_specification(spec)
    
    # Test with munsell_specification_to_xy
    try:
        # This requires integer values, so we need to handle it differently
        # Let's manually test the logic we think Python uses
        
        # For value > 9, we expect Python to interpolate between value=9 result
        # and illuminant C based on luminance
        
        # Get result at value=9 with same chroma
        spec_9 = [spec[0], 9.0, spec[2], spec[3]]
        xy_9 = munsell_specification_to_xy(spec_9)
        print(f"  At value=9.0: x={xy_9[0]:.6f}, y={xy_9[1]:.6f}")
        
        # Illuminant C
        illuminant_c = [0.31006, 0.31616]
        print(f"  Illuminant C: x={illuminant_c[0]:.6f}, y={illuminant_c[1]:.6f}")
        
        # What would linear interpolation give?
        t = (spec[1] - 9.0) / (10.0 - 9.0)
        x_linear = xy_9[0] + t * (illuminant_c[0] - xy_9[0])
        y_linear = xy_9[1] + t * (illuminant_c[1] - xy_9[1])
        print(f"  Linear interp (t={t:.3f}): x={x_linear:.6f}, y={y_linear:.6f}")
        
    except Exception as e:
        print(f"  Error: {e}")

# Now test what Python actually produces for these colors
print("\n" + "=" * 60)
print("Checking actual Python results for high-value colors:")

# We need to use integer values for the actual function
test_integer_specs = [
    [9.96, 9.0, 1.96, 6.0],  # Rounded to integer value
    [9.96, 9.0, 1.0, 6.0],   
    [9.96, 9.0, 0.5, 6.0],   
]

for spec in test_integer_specs:
    xy = munsell_specification_to_xy(spec)
    print(f"Value={spec[1]:.1f}, Chroma={spec[2]:.2f}: x={xy[0]:.6f}, y={xy[1]:.6f}")