#!/usr/bin/env python3
"""Explore the colour-science API to find the right functions"""

import colour
from colour.notation import munsell

print("colour-science version:", colour.__version__)
print("\nAvailable functions in colour.notation.munsell:")
print("-" * 50)

# List all functions
for name in dir(munsell):
    if not name.startswith('_'):
        print(f"  {name}")

# Let's trace through a conversion to understand the internals
print("\n\nTracing a conversion:")
print("-" * 50)

import numpy as np
from colour.notation import xyY_to_munsell_colour, munsell_colour_to_xyY
from colour import munsell_specification_from_renotation

# Test the problematic case
munsell_str = "8.548GY 9.0/7.125"
print(f"Testing: {munsell_str}")

# We can work backwards from the Munsell specification
spec = np.array([8.548, 9.0, 7.125, 4])  # hue, value, chroma, code
xyY = munsell_colour_to_xyY(spec)
print(f"munsell_colour_to_xyY result: {xyY}")

# Let's also test the full round trip
from colour import sRGB_to_XYZ, XYZ_to_xyY
rgb = np.array([204, 255, 170]) / 255.0
XYZ = sRGB_to_XYZ(rgb)
xyY = XYZ_to_xyY(XYZ)
print(f"\nTarget xyY from RGB: {xyY}")

munsell = xyY_to_munsell_colour(xyY)
print(f"Munsell result: {munsell}")