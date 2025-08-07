#!/usr/bin/env python3
"""Trace the convergence for RGB(221, 238, 238) in Python"""

from colour.notation.munsell import xyY_to_munsell_colour
from colour.models import RGB_to_XYZ, XYZ_to_xyY
import numpy as np

# Test color
rgb = np.array([221, 238, 238]) / 255.0

# Convert to xyY
XYZ = RGB_to_XYZ(rgb, illuminant_XYZ=np.array([0.98074, 1.00000, 1.18232]),
                 illuminant_xy=np.array([0.31270, 0.32900]),
                 matrix=np.array([
                     [0.4124564, 0.3575761, 0.1804375],
                     [0.2126729, 0.7151522, 0.0721750],
                     [0.0193339, 0.1191920, 0.9503041]
                 ]))
xyY = XYZ_to_xyY(XYZ)

print(f"RGB: {rgb * 255}")
print(f"XYZ: {XYZ}")
print(f"xyY: {xyY}")
print(f"Expected Munsell: {xyY_to_munsell_colour(xyY)}")
print()

# Now trace the convergence manually
from colour.notation.munsell import xyY_to_munsell_specification

# Enable debugging in the source if possible
import colour.notation.munsell as munsell_module

# Try to monkey-patch the function to add debug output
original_func = munsell_module.xyY_to_munsell_specification

def traced_xyY_to_munsell_specification(xyY):
    """Wrapper to trace execution"""
    print("=== PYTHON CONVERGENCE TRACE ===")
    print(f"Input xyY: {xyY}")
    
    # We can't easily trace internals, but we can run it
    result = original_func(xyY)
    
    print(f"Output specification: {result}")
    return result

# Run the traced version
spec = traced_xyY_to_munsell_specification(xyY)
print(f"\nFinal spec: hue={spec[0]:.3f}, value={spec[1]:.3f}, chroma={spec[2]:.3f}, code={spec[3]}")

# Let's also test what happens if we try different chroma values
print("\n=== Testing different chroma values ===")
from colour.notation.munsell import _munsell_specification_to_xyY

test_chromas = [1.5, 1.6, 1.8, 2.0, 2.1, 2.084]
for chroma in test_chromas:
    test_spec = [spec[0], spec[1], chroma, spec[3]]
    try:
        xy_result = _munsell_specification_to_xyY(test_spec)
        distance = np.sqrt((xy_result[0] - xyY[0])**2 + (xy_result[1] - xyY[1])**2)
        print(f"Chroma {chroma:.3f}: xy=({xy_result[0]:.6f}, {xy_result[1]:.6f}), distance={distance:.9f}")
    except Exception as e:
        print(f"Chroma {chroma:.3f}: FAILED - {e}")