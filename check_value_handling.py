#!/usr/bin/env python3
"""Check how Python handles value > 9 in interpolation"""

import numpy as np
from colour.notation import munsell

# Check if Python's xy_from_renotation_ovoid accepts value > 9
print("Testing value handling in Python's xy_from_renotation_ovoid:")

test_specs = [
    [7.1, 9.0, 2.0, 3],    # Valid
    [7.1, 9.2, 2.0, 3],    # Value > 9
    [7.1, 9.27, 2.0, 3],   # Value > 9
    [7.1, 9.3, 2.0, 3],    # Value > 9 (reference uses this)
]

for spec in test_specs:
    try:
        xy = munsell.xy_from_renotation_ovoid(spec)
        print(f"  Spec {spec} -> xy=[{xy[0]:.6f}, {xy[1]:.6f}]")
    except AssertionError as e:
        print(f"  Spec {spec} -> ERROR: {e}")

print("\n--- Checking internal functions ---")

# Check what functions are available for handling value > 9
print("Available functions in munsell module:")
funcs = [f for f in dir(munsell) if 'interpolat' in f.lower()]
for f in funcs:
    print(f"  {f}")

# Try the extended version
print("\n--- Testing xy_from_renotation_ovoid_interpolated (if exists) ---")
if hasattr(munsell, 'xy_from_renotation_ovoid_interpolated'):
    for spec in test_specs:
        try:
            xy = munsell.xy_from_renotation_ovoid_interpolated(spec)
            print(f"  Spec {spec} -> xy=[{xy[0]:.6f}, {xy[1]:.6f}]")
        except Exception as e:
            print(f"  Spec {spec} -> ERROR: {e}")
else:
    print("  Function not found in Python module")

# Check how convergence handles this internally
print("\n--- Checking convergence algorithm ---")
from colour import sRGB_to_XYZ

rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

print(f"Input xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")

# Run convergence
spec = munsell.xyY_to_munsell_specification(xyy)
print(f"Final spec: {spec}")
print(f"  Value in spec: {spec[1]:.6f}")

# The convergence must handle value > 9 internally somehow
# Let's check if it clamps or uses a different function
print("\n--- Checking Python's internal handling ---")

# Look for the actual function used in convergence
import inspect

# Get source of _munsell_specification_to_xyY
if hasattr(munsell, '_munsell_specification_to_xyY'):
    print("Found _munsell_specification_to_xyY (internal function)")
    # This is the function used during convergence
    # It might handle value > 9 differently