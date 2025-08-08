#!/usr/bin/env python3
"""Verify XYZ to xyY conversion differences"""

import numpy as np
from colour import sRGB_to_XYZ

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
print(f"RGB normalized: {rgb}")

# Get XYZ from colour library
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ from colour: {xyz}")
print(f"  X={xyz[0]:.10f}")
print(f"  Y={xyz[1]:.10f}")
print(f"  Z={xyz[2]:.10f}")

# Convert to xyY the standard way
total = xyz[0] + xyz[1] + xyz[2]
print(f"Sum(XYZ): {total:.10f}")

x = xyz[0] / total
y = xyz[1] / total
Y = xyz[1]

print(f"\nxyY conversion:")
print(f"  x = X/sum = {xyz[0]:.10f} / {total:.10f} = {x:.10f}")
print(f"  y = Y/sum = {xyz[1]:.10f} / {total:.10f} = {y:.10f}")
print(f"  Y = {Y:.10f}")

print(f"\nFinal xyY: [{x:.10f}, {y:.10f}, {Y:.10f}]")

# Compare with what Rust gets
print("\n--- Comparison ---")
print(f"Python: x={x:.6f}, y={y:.6f}, Y={Y:.6f}")
print(f"Rust:   x=0.301656, y=0.328990, Y=0.919160")
print(f"Diff:   x={x-0.301656:.6f}, y={y-0.328990:.6f}, Y={Y-0.919160:.6f}")

# Now check if munsell module does something different
import munsell
spec = munsell.xyY_to_munsell_specification(np.array([x, y, Y]))
print(f"\nMunsell spec from Python: {spec}")

# Check intermediate XYZ values
print("\n--- Checking intermediate XYZ ---")
# Manual sRGB to linear
rgb_linear = np.zeros(3)
for i in range(3):
    c = rgb[i]
    if c <= 0.04045:
        rgb_linear[i] = c / 12.92
    else:
        rgb_linear[i] = ((c + 0.055) / 1.055) ** 2.4

print(f"Linear RGB: {rgb_linear}")

# Manual linear to XYZ
matrix = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041]
])

xyz_manual = matrix @ rgb_linear
print(f"XYZ manual: {xyz_manual}")
print(f"XYZ colour: {xyz}")
print(f"Ratio: {xyz[0]/xyz_manual[0]:.10f}")

# This ratio should be our scaling factor
scaling = xyz[0] / xyz_manual[0]
print(f"\nScaling factor: {scaling:.10f}")

# Apply scaling to manual XYZ
xyz_scaled = xyz_manual * scaling
print(f"XYZ manual scaled: {xyz_scaled}")
print(f"Matches colour? {np.allclose(xyz_scaled, xyz)}")

# Now convert scaled XYZ to xyY
total_scaled = xyz_scaled[0] + xyz_scaled[1] + xyz_scaled[2]
x_scaled = xyz_scaled[0] / total_scaled
y_scaled = xyz_scaled[1] / total_scaled
Y_scaled = xyz_scaled[1]

print(f"\nxyY from scaled XYZ: [{x_scaled:.6f}, {y_scaled:.6f}, {Y_scaled:.6f}]")

# The key insight
print("\n=== KEY INSIGHT ===")
print("The x,y chromaticity values should NOT change with XYZ scaling!")
print("Because x = X/(X+Y+Z) and scaling all three by the same factor cancels out")
print(f"Unscaled: x={xyz_manual[0]/sum(xyz_manual):.6f}")
print(f"Scaled:   x={xyz_scaled[0]/sum(xyz_scaled):.6f}")
print("These should be identical!")