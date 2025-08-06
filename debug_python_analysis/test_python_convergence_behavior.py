#!/usr/bin/env python3
"""Test Python's convergence behavior for the problematic green color"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import munsell_colour_to_munsell_specification
from colour.notation.munsell import munsell_specification_to_xyY

# Test case
r, g, b = 204, 255, 170
rgb_norm = [r/255.0, g/255.0, b/255.0]
XYZ = sRGB_to_XYZ(rgb_norm)
xyY = XYZ_to_xyY(XYZ)

print(f"Testing RGB({r}, {g}, {b}):")
print(f"Target xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")

# Try different Munsell specifications to see which ones are close to target
test_specs = [
    (8.5, 9.5, 7.1, 4),   # Rust result
    (8.0, 9.5, 12.7, 4),  # Python result
    (8.5, 9.5, 12.0, 4),  # Higher chroma variant
    (8.0, 9.5, 7.0, 4),   # Lower chroma variant
]

print("\nTesting different specifications:")
for hue, value, chroma, code in test_specs:
    spec = np.array([hue, value, chroma, code])
    test_xyY = munsell_specification_to_xyY(spec)
    dist = np.sqrt((xyY[0] - test_xyY[0])**2 + (xyY[1] - test_xyY[1])**2)
    print(f"{hue:3.1f}GY {value}/{chroma:4.1f} -> xy=({test_xyY[0]:.6f}, {test_xyY[1]:.6f}), dist={dist:.6f}")

# Let's trace through the algorithm manually
print("\nUnderstanding the convergence:")
print("The issue is that multiple Munsell specifications can map to similar xy coordinates.")
print("The algorithm needs to explore the full chroma range to find the best match.")