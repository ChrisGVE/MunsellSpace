#!/usr/bin/env python3
"""Test Python's exact algorithm implementation"""

import numpy as np
import colour

# Test RGB(204, 255, 170)
rgb = np.array([204/255, 255/255, 170/255])
print(f"Testing RGB: {rgb * 255}")
print("=" * 80)

# The correct function is xyY_to_munsell_colour
# First convert RGB to xyY with illuminant C
# Using the sRGB to XYZ matrix with D65, then adapt to C
XYZ_D65 = colour.sRGB_to_XYZ(rgb)
print(f"XYZ (D65): {XYZ_D65}")

# Chromatic adaptation from D65 to C
XYZ_C = colour.adaptation.chromatic_adaptation(
    XYZ_D65,
    colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'],
    colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C'],
    method='Von Kries'
)
print(f"XYZ (C): {XYZ_C}")

# Convert to xyY
xyY = colour.XYZ_to_xyY(XYZ_C)
print(f"xyY: {xyY}")

# Convert to Munsell
munsell = colour.notation.xyY_to_munsell_colour(xyY)
print(f"\nPython's Munsell result: {munsell}")

# Now let's understand the algorithm by checking intermediate steps
print("\n\nChecking intermediate steps:")
print("-" * 80)

# Import the internal functions
from colour.notation.munsell import (
    xyY_to_munsell_specification,
    munsell_specification_to_munsell_colour,
    munsell_colour_to_munsell_specification,
    munsell_specification_to_xyY
)

# Get the specification
spec = xyY_to_munsell_specification(xyY)
print(f"Munsell specification: {spec}")

# Convert back to check
xyY_check = munsell_specification_to_xyY(spec)
print(f"xyY check: {xyY_check}")
print(f"Distance: {np.linalg.norm(xyY[:2] - xyY_check[:2]):.6f}")

# Let's also check what Rust's values give
print("\n\nChecking Rust's values:")
rust_spec = munsell_colour_to_munsell_specification("8.5GY 9.5/7.1")
print(f"Rust specification: {rust_spec}")
rust_xyY = munsell_specification_to_xyY(rust_spec)
print(f"Rust xyY: {rust_xyY}")
print(f"Distance from target: {np.linalg.norm(xyY[:2] - rust_xyY[:2]):.6f}")