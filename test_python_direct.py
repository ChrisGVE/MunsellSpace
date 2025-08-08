#!/usr/bin/env python3
"""Test Python colour library directly"""

import numpy as np
from colour import sRGB_to_XYZ
from colour.notation import munsell

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
print(f"RGB normalized: {rgb}")

# Get XYZ
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ: {xyz}")

# Convert to xyY
total = xyz[0] + xyz[1] + xyz[2]
x = xyz[0] / total
y = xyz[1] / total
Y = xyz[1]

xyy = np.array([x, y, Y])
print(f"xyY: {xyy}")
print(f"  x = {x:.10f}")
print(f"  y = {y:.10f}")
print(f"  Y = {Y:.10f}")

# Convert to Munsell
spec = munsell.xyY_to_munsell_specification(xyy)
print(f"\nMunsell specification: {spec}")

# Convert to notation
notation = munsell.munsell_specification_to_munsell(spec)
print(f"Munsell notation: {notation}")

# Also test the reference result: 7.1G 9.3/2.1
print("\n--- Testing reference notation ---")
ref_spec = munsell.munsell_to_munsell_specification("7.1G 9.3/2.1")
print(f"Reference spec: {ref_spec}")

ref_xyy = munsell.munsell_specification_to_xyY(ref_spec)
print(f"Reference xyY: {ref_xyy}")

# Convert back to XYZ
ref_xyz = [
    ref_xyy[0] * ref_xyy[2] / ref_xyy[1],
    ref_xyy[2],
    (1 - ref_xyy[0] - ref_xyy[1]) * ref_xyy[2] / ref_xyy[1]
]
print(f"Reference XYZ: {ref_xyz}")

# Compare
print("\n--- Comparison ---")
print(f"Input xyY:     {xyy}")
print(f"Reference xyY: {ref_xyy}")
print(f"Difference:    {xyy - ref_xyy}")