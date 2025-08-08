#!/usr/bin/env python3
"""Simple trace for RGB(187,255,153)"""

import sys
sys.path.insert(0, 'InkyFingers')

from colour import sRGB_to_XYZ
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import XYZ_to_xyY
import numpy as np

# Test RGB(187,255,153)
rgb = np.array([187, 255, 153]) / 255.0
print(f"Testing RGB: {[187, 255, 153]}")
print(f"Expected: 8.5GY 9.3/12.8")

# Convert to XYZ then xyY
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)
print(f"XYZ: {xyz}")
print(f"xyY: {xyy}")

# Run conversion
munsell = xyY_to_munsell_specification(xyy)
print(f"\nMunsell specification: {munsell}")

# Convert to string notation
from colour.notation.munsell import munsell_specification_to_munsell_colour
munsell_str = munsell_specification_to_munsell_colour(munsell)
print(f"Munsell notation: {munsell_str}")

print(f"\nExpected: 8.5GY 9.3/12.8")
print(f"Got:      {munsell_str}")

# Check chroma difference
expected_chroma = 12.8
got_chroma = munsell[2]
print(f"\nChroma difference: {got_chroma - expected_chroma:.2f}")