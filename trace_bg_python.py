#!/usr/bin/env python3
"""Trace what's happening with BG color conversion"""

import colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np

# Test the problematic color
rgb = [0, 170, 187]
srgb = [c / 255.0 for c in rgb]

print(f"RGB: {rgb}")
print(f"sRGB normalized: {srgb}")

# Convert to XYZ then xyY
xyz = colour.sRGB_to_XYZ(srgb)
print(f"XYZ: {xyz}")

xyy = colour.XYZ_to_xyY(xyz)
print(f"xyY: {xyy}")

# Convert to Lab/LCH to see initial spec
Lab = colour.XYZ_to_Lab(xyz)
print(f"Lab: {Lab}")

LCHab = colour.Lab_to_LCHab(Lab)
print(f"LCHab: {LCHab}")

# Get initial specification from LCHab
# Skip this since we don't have the function
# initial_spec = lchab_to_munsell_specification(LCHab, 100)
# print(f"\nInitial spec from LCHab: {initial_spec}")

# Now trace the full conversion
print("\n=== Full xyY to Munsell conversion ===")
result = xyY_to_munsell_specification(xyy)
print(f"Final result: {result}")

# Map the result
HUE_CODES = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
             6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
family = HUE_CODES[int(result[3])]
print(f"Formatted: {result[0]:.1f}{family} {result[1]:.1f}/{result[2]:.1f}")
print(f"Expected: 9.6BG 6.3/7.9")