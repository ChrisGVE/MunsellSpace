#!/usr/bin/env python3
"""Clarify the different meanings of 'Y' in color science."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

# Example: a yellow color
r, g, b = 255, 200, 0  # Orange-yellow color

print("The Two Different Meanings of 'Y':")
print("=" * 70)

# Convert to XYZ
srgb = [r/255, g/255, b/255]
XYZ = sRGB_to_XYZ(srgb)
print(f"\n1. CIE XYZ Color Space:")
print(f"   RGB({r},{g},{b}) → XYZ = [{XYZ[0]:.4f}, {XYZ[1]:.4f}, {XYZ[2]:.4f}]")
print(f"   Here Y = {XYZ[1]:.4f} is LUMINANCE (brightness)")
print(f"   Range: [0, 1] in normalized form, or [0, 100] when scaled")

# Convert to xyY
xyY = XYZ_to_xyY(XYZ)
print(f"\n2. CIE xyY Color Space:")
print(f"   xyY = [{xyY[0]:.4f}, {xyY[1]:.4f}, {xyY[2]:.4f}]")
print(f"   x = {xyY[0]:.4f} (chromaticity coordinate)")
print(f"   y = {xyY[1]:.4f} (chromaticity coordinate)")  
print(f"   Y = {xyY[2]:.4f} (luminance, same as XYZ's Y)")

# Convert to Munsell
munsell = xyY_to_munsell_colour(xyY)
print(f"\n3. Munsell Notation:")
print(f"   {munsell}")

# Parse the notation
parts = munsell.split(' ')
hue_part = parts[0]
for i, char in enumerate(hue_part):
    if char.isalpha():
        hue_num = float(hue_part[:i])
        hue_family = hue_part[i:]
        break

print(f"   Hue: {hue_num} in family '{hue_family}'")
if 'Y' in hue_family:
    print(f"   Here 'Y' means YELLOW (a hue family)")
    if hue_family == 'Y':
        print("   Pure Yellow family")
    elif hue_family == 'GY':
        print("   Green-Yellow family")
    elif hue_family == 'YR':
        print("   Yellow-Red family")

print("\n" + "=" * 70)
print("SUMMARY:")
print("- Y in XYZ/xyY = Luminance (brightness), range [0,1] or [0,100]")
print("- Y in Munsell = Yellow hue family (one of 10 color families)")
print("- They are completely unrelated!")