#!/usr/bin/env python3
"""Debug the initial conversion in Python step by step"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import XYZ_to_Lab, Lab_to_LCHab
from colour import CCS_ILLUMINANTS

# RGB(221, 238, 238) in xyY
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing initial conversion for RGB(221, 238, 238)")
print(f"xyY: {xyY}")
print()

# Calculate XYZ
x, y, Y = xyY
X = x * Y / y
Z = (1.0 - x - y) * Y / y
XYZ = np.array([X, Y, Z])
print(f"XYZ: {XYZ}")

# Calculate Lab
Lab = XYZ_to_Lab(XYZ, CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"])
print(f"Lab: {Lab}")

# Calculate LCHab
LCHab = Lab_to_LCHab(Lab)
print(f"LCHab: {LCHab}")
print()

# What Python's algorithm does with this
print("Initial specification from LCHab:")
print(f"  L* (lightness): {LCHab[0]:.6f} -> becomes initial value proxy")
print(f"  C* (chroma):    {LCHab[1]:.6f} -> becomes initial chroma")
print(f"  H (hue angle):  {LCHab[2]:.6f} -> becomes initial hue angle")
print()

# The hue angle 162.86° should map to a G (Green) family
# since it's in the greenish range
hue_angle = LCHab[2]
# Hue angle ranges (approximate):
# R: 355-35°, YR: 35-65°, Y: 65-95°, GY: 95-125°, 
# G: 125-155°, BG: 155-185°, B: 185-215°, PB: 215-245°,
# P: 245-275°, RP: 275-355°
if 155 <= hue_angle < 185:
    print(f"Hue angle {hue_angle:.1f}° suggests BG (Blue-Green) family")
elif 125 <= hue_angle < 155:
    print(f"Hue angle {hue_angle:.1f}° suggests G (Green) family")
print()

# Value calculation
# Munsell value is related to lightness
# Approximate: Value ≈ L* / 10
munsell_value_approx = LCHab[0] / 10
print(f"Approximate Munsell value from L*: {munsell_value_approx:.3f}")
print()

# Now get actual Python result
spec = xyY_to_munsell_specification(xyY)
print("Python's final Munsell specification:")
print(f"  Hue:    {spec[0]:.6f}")
print(f"  Value:  {spec[1]:.6f}")
print(f"  Chroma: {spec[2]:.6f}")
print(f"  Code:   {spec[3]}")
print()

# What family is code 3?
families = {0: 'R', 1: 'YR', 2: 'Y', 3: 'GY', 4: 'G', 
           5: 'BG', 6: 'B', 7: 'PB', 8: 'P', 9: 'RP'}
print(f"Code {int(spec[3])} corresponds to family: {families.get(int(spec[3]), 'Unknown')}")
print()

print("Summary:")
print(f"  Initial LCHab chroma: {LCHab[1]:.3f}")
print(f"  Final Munsell chroma: {spec[2]:.3f}")
print(f"  Chroma reduction factor: {spec[2] / LCHab[1]:.3f}")