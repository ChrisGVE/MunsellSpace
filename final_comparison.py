#!/usr/bin/env python3
"""Final comparison of Python vs Rust for RGB(221,238,238)"""

import numpy as np
from colour.notation import munsell

# Test color
rgb = np.array([221/255.0, 238/255.0, 238/255.0])
print(f"Testing RGB: {rgb}")

# Python conversion
from colour import RGB_to_XYZ, XYZ_to_xyY
from colour.models import RGB_COLOURSPACE_sRGB

XYZ = RGB_to_XYZ(rgb, RGB_COLOURSPACE_sRGB)
xyY = XYZ_to_xyY(XYZ)

print(f"\nPython:")
print(f"  XYZ: {XYZ}")
print(f"  xyY: {xyY}")

munsell_result = munsell.xyY_to_munsell_colour(xyY)
print(f"  Munsell: {munsell_result}")

# Parse result to get components
import re
match = re.match(r'([0-9.]+)([A-Z]+)\s+([0-9.]+)/([0-9.]+)', munsell_result)
if match:
    hue_num = float(match.group(1))
    hue_family = match.group(2)
    value = float(match.group(3))
    chroma = float(match.group(4))
    print(f"  Components: {hue_num}{hue_family} {value}/{chroma}")
    
print("\nExpected for Rust: 7.5BG 9.277364/2.084771")
print("Rust gets:         7.3G 9.7/1.6")

print("\nDifferences:")
print(f"  Hue family: Python={hue_family}, Expected=BG, Rust=G")
print(f"  Value: Python={value:.3f}, Expected=9.277, Rust=9.700")
print(f"  Chroma: Python={chroma:.3f}, Expected=2.085, Rust=1.600")