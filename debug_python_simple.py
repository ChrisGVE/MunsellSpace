#!/usr/bin/env python3
"""Simple Python script to get exact Munsell conversion for RGB(255,0,0)."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

# Test pure red
rgb = np.array([1.0, 0.0, 0.0])  # Normalized RGB
print(f"Input RGB: {rgb}")

# Get XYZ and xyY
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ (D65): {xyz}")

xyy = XYZ_to_xyY(xyz)
print(f"xyY (D65): x={xyy[0]:.6f}, y={xyy[1]:.6f}, Y={xyy[2]:.6f}")

# Convert to Munsell
munsell = xyY_to_munsell_colour(xyy)
print(f"Final Munsell: {munsell}")

# Also test the other RGB primaries and secondaries
test_colors = [
    ([1.0, 0.0, 0.0], "Red"),
    ([0.0, 1.0, 0.0], "Green"),
    ([0.0, 0.0, 1.0], "Blue"),
    ([1.0, 1.0, 0.0], "Yellow"),
    ([1.0, 0.0, 1.0], "Magenta"),
    ([0.0, 1.0, 1.0], "Cyan")
]

print("\n=== All test colors ===")
for rgb_val, name in test_colors:
    rgb_np = np.array(rgb_val)
    xyz = sRGB_to_XYZ(rgb_np)
    xyy = XYZ_to_xyY(xyz)
    munsell = xyY_to_munsell_colour(xyy)
    print(f"{name}: RGB{[int(c*255) for c in rgb_val]} → {munsell}")