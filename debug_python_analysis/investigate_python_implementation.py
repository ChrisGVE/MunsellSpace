#!/usr/bin/env python3
"""Investigate the exact Python implementation of Munsell conversion"""

import numpy as np
import colour

# Test RGB(204, 255, 170) 
rgb = np.array([204/255, 255/255, 170/255])
print(f"Testing RGB: {rgb}")
print("=" * 80)

# First let's see what Python gives us
munsell = colour.notation.RGB_to_munsell(rgb, 'ITU-R BT.709', 'C')
print(f"Python result: {munsell}")

# Now let's trace through the implementation
# Convert RGB to XYZ
XYZ = colour.sRGB_to_XYZ(rgb, illuminant=colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C'])
print(f"\nXYZ (Illuminant C): {XYZ}")

# Convert to xyY
xyY = colour.XYZ_to_xyY(XYZ)
print(f"xyY: {xyY}")

# Now the key part - convert xyY to Munsell
from colour.notation.munsell import xyY_to_munsell_specification
munsell_spec = xyY_to_munsell_specification(xyY)
print(f"\nMunsell specification: {munsell_spec}")

# Let's look at what the convergence algorithm is doing
# I'll examine the source code approach
print("\n\nExamining convergence approach:")

# The key insight is that Python may be using a different convergence strategy
# Let me check the actual XYZ values Rust is using
rust_XYZ = np.array([0.6493396, 0.8632931, 0.5620267])
rust_xyY = colour.XYZ_to_xyY(rust_XYZ)
print(f"\nRust's XYZ: {rust_XYZ}")
print(f"Rust's xyY: {rust_xyY}")

# Convert Rust's xyY to Munsell
rust_munsell_spec = xyY_to_munsell_specification(rust_xyY)
print(f"Munsell from Rust's xyY: {rust_munsell_spec}")

# Compare
print(f"\nDifference in x: {abs(xyY[0] - rust_xyY[0]):.6f}")
print(f"Difference in y: {abs(xyY[1] - rust_xyY[1]):.6f}")
print(f"Difference in Y: {abs(xyY[2] - rust_xyY[2]):.6f}")

# The issue might be the XYZ calculation or the illuminant adaptation