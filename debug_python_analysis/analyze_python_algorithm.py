#!/usr/bin/env python3
"""Analyze how Python's algorithm avoids premature convergence"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import munsell_colour_to_munsell_specification

# Let's trace through Python's algorithm manually
# RGB(204, 255, 170) 
rgb_norm = [204/255.0, 255/255.0, 170/255.0]
XYZ = sRGB_to_XYZ(rgb_norm)
xyY = XYZ_to_xyY(XYZ)

print(f"Target xyY: {xyY}")

# Python result is 8.0GY 9.5/12.7
# Let's see if we can understand why it doesn't stop at lower chromas

# Check the source code behavior
import colour.notation.munsell
print(f"\nPython colour-science version: {colour.__version__}")

# The key insight: Python's algorithm might not check convergence after 
# hue refinement alone, or it might have a different convergence criterion

# Let's check what happens if we manually test convergence at different points
from colour.notation.munsell import munsell_specification_to_xyY

test_specs = [
    (8.548, 9.479, 7.125),  # Where Rust converges
    (8.0, 9.5, 12.7),       # Python result
]

print("\nTesting convergence distances:")
for h, v, c in test_specs:
    spec = np.array([h, v, c, 4])  # 4 = GY
    test_xyY = munsell_specification_to_xyY(spec)
    dist = np.sqrt((xyY[0] - test_xyY[0])**2 + (xyY[1] - test_xyY[1])**2)
    print(f"{h:.3f}GY {v:.1f}/{c:.1f}: dist={dist:.8f}")

print("\nKey insight: The Rust algorithm finds a valid solution with very low")
print("distance but wrong chroma. Python must continue iterating to explore") 
print("higher chromas even when the distance is already very small.")