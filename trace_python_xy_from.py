#!/usr/bin/env python3
"""Trace Python's xy_from_renotation_ovoid for high values"""

import sys
import os
import numpy as np

# Test what Python does with value > 9 in xy_from_renotation_ovoid
# We need to patch colour-science to trace this
print("Testing xy_from_renotation_ovoid with value > 9")

# First, let's check if Python clamps or extrapolates
from colour.notation.munsell import munsell_specification_to_munsell_colour
from colour.models import XYZ_to_xyY
from colour import sRGB_to_XYZ

# RGB(187,255,153) gives value 9.35
rgb = np.array([187, 255, 153]) / 255.0
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"RGB {[187, 255, 153]}:")
print(f"  xyY: {xyy}")

# Now test the conversion
from colour.notation.munsell import xyY_to_munsell_specification
munsell = xyY_to_munsell_specification(xyy)
print(f"  Munsell spec: {munsell}")
print(f"  Value: {munsell[1]:.3f}, Chroma: {munsell[2]:.3f}")

# Test what happens if we manually call xy_from_renotation_ovoid with high value
print("\nManually testing xy_from_renotation_ovoid:")
try:
    # Import the internal function
    import colour.notation.munsell as mn
    
    # Check if the function exists
    if hasattr(mn, 'xy_from_renotation_ovoid'):
        # Test with a high-value specification
        test_spec = np.array([8.5, 9.35, 12.8, 4])  # 8.5GY 9.35/12.8
        print(f"Input spec: {test_spec}")
        
        try:
            xy = mn.xy_from_renotation_ovoid(test_spec)
            print(f"Output xy: {xy}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("xy_from_renotation_ovoid not found in colour.notation.munsell")
        
        # Try to find it elsewhere
        import colour
        for attr in dir(colour.notation):
            if 'xy_from' in attr.lower():
                print(f"  Found: {attr}")
                
except Exception as e:
    print(f"Import error: {e}")