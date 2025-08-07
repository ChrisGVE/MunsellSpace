#!/usr/bin/env python3
"""Check if XYZ conversion matches exactly"""

import numpy as np

r, g, b = 34, 17, 119

# Manual Python calculation
srgb = [r/255.0, g/255.0, b/255.0]
print(f"sRGB: {srgb}")
print(f"  R: {srgb[0]:.15f}")
print(f"  G: {srgb[1]:.15f}")  
print(f"  B: {srgb[2]:.15f}")

# Gamma correction (sRGB to linear)
linear = []
for c in srgb:
    if c <= 0.04045:
        linear.append(c / 12.92)
    else:
        linear.append(((c + 0.055) / 1.055) ** 2.4)

print(f"\nLinear RGB:")
print(f"  R: {linear[0]:.15f}")
print(f"  G: {linear[1]:.15f}")
print(f"  B: {linear[2]:.15f}")

# sRGB to XYZ matrix (D65)
xyz = [
    0.4124564 * linear[0] + 0.3575761 * linear[1] + 0.1804375 * linear[2],
    0.2126729 * linear[0] + 0.7151522 * linear[1] + 0.0721750 * linear[2],
    0.0193339 * linear[0] + 0.1191920 * linear[1] + 0.9503041 * linear[2],
]

print(f"\nXYZ:")
print(f"  X: {xyz[0]:.15f}")
print(f"  Y: {xyz[1]:.15f}")
print(f"  Z: {xyz[2]:.15f}")

# XYZ to xyY
sum_xyz = xyz[0] + xyz[1] + xyz[2]
x = xyz[0] / sum_xyz
y = xyz[1] / sum_xyz
Y = xyz[1]

print(f"\nxyY:")
print(f"  x: {x:.15f}")
print(f"  y: {y:.15f}")
print(f"  Y: {Y:.15f}")

# Compare with colour-science
from colour import sRGB_to_XYZ, XYZ_to_xyY

xyz_colour = sRGB_to_XYZ(srgb)
xyy_colour = XYZ_to_xyY(xyz_colour)

print(f"\ncolour-science XYZ:")
print(f"  X: {xyz_colour[0]:.15f}")
print(f"  Y: {xyz_colour[1]:.15f}")
print(f"  Z: {xyz_colour[2]:.15f}")

print(f"\ncolour-science xyY:")
print(f"  x: {xyy_colour[0]:.15f}")
print(f"  y: {xyy_colour[1]:.15f}")
print(f"  Y: {xyy_colour[2]:.15f}")

print(f"\nDifferences:")
print(f"  X diff: {abs(xyz[0] - xyz_colour[0]):.15f}")
print(f"  Y diff: {abs(xyz[1] - xyz_colour[1]):.15f}")
print(f"  Z diff: {abs(xyz[2] - xyz_colour[2]):.15f}")
print(f"  x diff: {abs(x - xyy_colour[0]):.15f}")
print(f"  y diff: {abs(y - xyy_colour[1]):.15f}")