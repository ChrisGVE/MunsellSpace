#!/usr/bin/env python3
"""Debug how Python handles low-chroma interpolation internally"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.notation.munsell import _munsell_specification_to_xyY
from colour import sRGB_to_XYZ, XYZ_to_xyY

def trace_interpolation(spec):
    """Trace the interpolation process for a specification"""
    print(f"\nTracing spec: {spec}")
    
    # This is what Python does internally
    hue, value, chroma, code = spec
    
    if chroma < 2.0:
        print(f"  Low chroma case: {chroma:.3f} < 2.0")
        print(f"  Will interpolate between grey and chroma 2")
        
        # Try to get xy at chroma 2
        spec_chroma2 = [hue, value, 2.0, code]
        print(f"  Attempting to get xy at spec: {spec_chroma2}")
        
        try:
            xy_chroma2 = _munsell_specification_to_xyY(spec_chroma2)
            print(f"  Success! xy at chroma 2: ({xy_chroma2[0]:.6f}, {xy_chroma2[1]:.6f})")
        except Exception as e:
            print(f"  Failed: {e}")
            # Python would handle the failure here
            print(f"  Python must have a fallback for value {value:.3f}")
    
    # Get the actual result
    try:
        result = _munsell_specification_to_xyY(spec)
        print(f"  Final xy: ({result[0]:.6f}, {result[1]:.6f}, {result[2]:.6f})")
        return result
    except Exception as e:
        print(f"  Final conversion failed: {e}")
        return None

# Test the problematic grey color
rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"RGB: {rgb * 255}")
print(f"xyY: ({xyy[0]:.10f}, {xyy[1]:.10f}, {xyy[2]:.10f})")

# Get the specification from xyY
spec = xyY_to_munsell_specification(xyy)
print(f"\nPython result:")
print(f"  Spec: [{spec[0]:.10f}, {spec[1]:.10f}, {spec[2]:.10f}, {int(spec[3])}]")
print(f"  Munsell: {spec[0]:.1f}G {spec[1]:.1f}/{spec[2]:.1f}")

# Now trace what happens for different test cases
test_specs = [
    [7.123, 9.277, 2.084, 3],  # The correct spec
    [7.123, 9.277, 1.541, 3],  # What Rust gets  
    [7.123, 9.0, 2.0, 3],       # Integer value at chroma 2
    [7.123, 9.277, 2.0, 3],     # Non-integer value at chroma 2
]

for test_spec in test_specs:
    trace_interpolation(test_spec)

print("\n=== KEY INSIGHT ===")
print("For non-integer values with chroma < 2.0:")
print("Python can handle [hue, 9.277, 2.0, code] directly")
print("Our code may be failing to get xy at chroma 2 for non-integer values")
print("This causes us to use a fallback that produces different results")