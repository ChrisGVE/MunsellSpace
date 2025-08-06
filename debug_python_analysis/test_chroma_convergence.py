#!/usr/bin/env python3
"""Test to understand chroma convergence behavior"""

import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import munsell_colour_to_munsell_specification

# Test case: RGB(204, 255, 170) -> 8.0GY 9.5/12.7
r, g, b = 204, 255, 170

# Python conversion
rgb_norm = [r/255.0, g/255.0, b/255.0]
XYZ = sRGB_to_XYZ(rgb_norm)
xyY = XYZ_to_xyY(XYZ)

# Get Python result
munsell = xyY_to_munsell_colour(xyY)
spec = munsell_colour_to_munsell_specification(munsell)

print(f"Testing RGB({r}, {g}, {b}):")
print(f"Target xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
print(f"Python result: {munsell}")
print(f"  Specification: hue={spec[0]:.3f}, value={spec[1]:.3f}, chroma={spec[2]:.3f}")

# Let's understand what's happening at the convergence point
# The Rust algorithm is returning 8.5GY 9.5/7.1

print("\nChecking what xy coordinates 8.5GY 9.5/7.1 produces:")
from colour.notation.munsell import munsell_specification_to_xyY

# Convert Rust result back to xy
rust_spec = np.array([8.5, 9.5, 7.1, 4])  # 4 is code for GY
rust_xyY = munsell_specification_to_xyY(rust_spec)
print(f"Rust result xy: x={rust_xyY[0]:.6f}, y={rust_xyY[1]:.6f}")

# Calculate distance
dist = np.sqrt((xyY[0] - rust_xyY[0])**2 + (xyY[1] - rust_xyY[1])**2)
print(f"Distance from target: {dist:.8f}")

# Now check what the correct result produces
correct_spec = np.array([8.0, 9.5, 12.7, 4])
correct_xyY = munsell_specification_to_xyY(correct_spec)
print(f"\nCorrect result xy: x={correct_xyY[0]:.6f}, y={correct_xyY[1]:.6f}")
dist_correct = np.sqrt((xyY[0] - correct_xyY[0])**2 + (xyY[1] - correct_xyY[1])**2)
print(f"Distance from target: {dist_correct:.8f}")

print("\nConclusion:")
print(f"The Rust algorithm is converging to a lower chroma that happens to match")
print(f"the target xy coordinates within the threshold, but it's not the correct")
print(f"Munsell specification. The algorithm needs to continue iterating to find")
print(f"the higher chroma solution.")