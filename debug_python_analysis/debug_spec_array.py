#!/usr/bin/env python3
"""Debug why spec array gives wrong xy values"""

import numpy as np
from colour.notation.munsell import xy_from_renotation_ovoid

# Test what happens with different spec arrays
print("Testing spec array variations:")
print("=" * 80)

# The correct spec for 7.5GY 9/6
spec1 = np.array([7.5, 9, 6, 4])
print(f"Spec: {spec1}")
xy1 = xy_from_renotation_ovoid(spec1)
print(f"Result: xy=({xy1[0]:.6f}, {xy1[1]:.6f})")

# What compare_boundary_values.py was doing
spec2 = np.array([7.5, 9, 6, 9])  # Last element is 9 instead of 4!
print(f"\nSpec with wrong code: {spec2}")
xy2 = xy_from_renotation_ovoid(spec2)
print(f"Result: xy=({xy2[0]:.6f}, {xy2[1]:.6f})")

# Let's understand what the last element means
print("\n\nTesting different hue codes:")
hue_codes = {
    0: "R", 1: "YR", 2: "Y", 3: "GY", 4: "G",
    5: "BG", 6: "B", 7: "PB", 8: "P", 9: "RP"
}

for code, name in hue_codes.items():
    spec = np.array([7.5, 9, 6, code])
    xy = xy_from_renotation_ovoid(spec)
    print(f"Code {code} ({name:2}): xy=({xy[0]:.6f}, {xy[1]:.6f})")

# Check the boundary code issue
print("\n\nBoundary code issue in compare_boundary_values.py:")
print("The script uses int(bounds[0][1]) as the hue code")
print("But bounds[0][1] is the VALUE (9), not the hue code!")
print("This is why it's using code=9 (RP) instead of code=4 (GY)")