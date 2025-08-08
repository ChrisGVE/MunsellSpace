#!/usr/bin/env python3
"""Debug the initial spec calculation in Python"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import XYZ_to_Lab, Lab_to_LCHab
from colour import CCS_ILLUMINANTS

# RGB(221, 238, 238) in xyY
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing initial specification for RGB(221, 238, 238)")
print(f"xyY: {xyY}")
print()

# Manually calculate the initial spec like Python does
x, y, Y = xyY

# Convert to XYZ
X = x * Y / y
Z = (1.0 - x - y) * Y / y
XYZ = np.array([X, Y, Z])
print(f"XYZ: {XYZ}")

# Convert to Lab using Illuminant C
Lab = XYZ_to_Lab(XYZ, CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"])
print(f"Lab: {Lab}")

# Convert to LCHab
LCHab = Lab_to_LCHab(Lab)
print(f"LCHab: {LCHab}")
print()

# This is what would be used as initial spec
print("Initial specification components:")
print(f"  L* (lightness): {LCHab[0]:.6f}")
print(f"  C* (chroma):    {LCHab[1]:.6f}")
print(f"  H (hue angle):  {LCHab[2]:.6f}")
print()

# Now check what Python actually does
spec = xyY_to_munsell_specification(xyY)
print("Python's final Munsell specification:")
print(f"  Hue:    {spec[0]:.6f}")
print(f"  Value:  {spec[1]:.6f}")
print(f"  Chroma: {spec[2]:.6f}")
print(f"  Code:   {spec[3]}")
print()

print("Key insight:")
print(f"  LCHab chroma is {LCHab[1]:.6f}")
print(f"  Final chroma is {spec[2]:.6f}")
print(f"  Ratio: {spec[2] / LCHab[1]:.6f}")