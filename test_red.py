#!/usr/bin/env python3
"""Test red color with Python colour-science"""

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

# Test pure red
rgb = [255/255.0, 0/255.0, 0/255.0]
XYZ = sRGB_to_XYZ(rgb)
xyY = XYZ_to_xyY(XYZ)

print(f"RGB: {rgb}")
print(f"XYZ: {XYZ}")
print(f"xyY: {xyY}")

munsell = xyY_to_munsell_colour(xyY)
print(f"Munsell: {munsell}")