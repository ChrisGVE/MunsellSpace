#!/usr/bin/env python3
"""Test how Python handles extrapolation for high chromas"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xy
from colour.utilities import domain_range_scale

# Test a specification with high chroma that doesn't exist
# Red: hue=0.0, value=5.0, chroma=24.0, code=6
spec = np.array([0.0, 5.0, 24.0, 6.0])

print(f"Testing specification: {spec}")
print(f"  hue={spec[0]}, value={spec[1]}, chroma={spec[2]}, code={spec[3]}")

# Try the function that handles interpolation
try:
    with domain_range_scale("ignore"):
        xy = munsell_specification_to_xy(spec)
    print(f"\nmunsell_specification_to_xy result: {xy}")
except Exception as e:
    print(f"\nmunsell_specification_to_xy error: {e}")

# Try extrapolating between chromas
print("\n\nTesting extrapolation approach:")
# Find the highest available chroma
for max_chroma in range(20, 0, -2):
    spec_test = np.array([0.0, 5.0, float(max_chroma), 6.0])
    try:
        with domain_range_scale("ignore"):
            xy_max = munsell_specification_to_xy(spec_test)
        print(f"  Max available chroma: {max_chroma}, xy={xy_max}")
        
        # Now try one step lower
        spec_lower = np.array([0.0, 5.0, float(max_chroma - 2), 6.0])
        with domain_range_scale("ignore"):
            xy_lower = munsell_specification_to_xy(spec_lower)
        print(f"  Lower chroma: {max_chroma - 2}, xy={xy_lower}")
        
        # Linear extrapolation to chroma 24
        t = (24.0 - max_chroma) / 2.0  # Steps to extrapolate
        x_extrap = xy_max[0] + t * (xy_max[0] - xy_lower[0])
        y_extrap = xy_max[1] + t * (xy_max[1] - xy_lower[1])
        print(f"  Extrapolated to chroma 24: xy=[{x_extrap:.6f}, {y_extrap:.6f}]")
        break
    except:
        continue