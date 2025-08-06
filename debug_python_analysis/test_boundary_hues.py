#!/usr/bin/env python3
"""Test boundary hue interpolation for 8.548GY"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY
from colour.notation.munsell import bounding_hues_from_renotation

# Get the boundary hues for 8.548GY
# The bounding_hues_from_renotation function returns the hues that bracket the given hue
hue = 8.548
code = 4  # GY

# Test what the standard hues are
print("Testing boundary hues for 8.548GY:")
print("Standard hues in GY family: 2.5GY, 5.0GY, 7.5GY, 10.0GY")
print(f"8.548 falls between 7.5GY and 10.0GY")

# Test the exact values at the boundaries
for test_hue in [7.5, 10.0]:
    for chroma in [6.0, 8.0]:
        spec = np.array([test_hue, 9.0, chroma, 4])
        xyY = munsell_specification_to_xyY(spec)
        print(f"  {test_hue}GY 9.0/{chroma}: xy=({xyY[0]:.6f}, {xyY[1]:.6f})")

# Now let's verify the interpolation
print("\nInterpolation test:")
# 8.548 is 43.2% of the way from 7.5 to 10.0
t = (8.548 - 7.5) / (10.0 - 7.5)
print(f"t = {t:.3f} (fraction from 7.5 to 10.0)")

# Get values at boundaries
spec_75_6 = np.array([7.5, 9.0, 6.0, 4])
spec_100_6 = np.array([10.0, 9.0, 6.0, 4])
xy_75_6 = munsell_specification_to_xyY(spec_75_6)
xy_100_6 = munsell_specification_to_xyY(spec_100_6)

x_interp_6 = xy_75_6[0] + t * (xy_100_6[0] - xy_75_6[0])
y_interp_6 = xy_75_6[1] + t * (xy_100_6[1] - xy_75_6[1])

print(f"\nManual interpolation for chroma=6.0:")
print(f"  Expected: ({x_interp_6:.6f}, {y_interp_6:.6f})")
print(f"  Python gives: (0.326241, 0.407311)")
print(f"  Rust claims: (0.326800, 0.406782)")