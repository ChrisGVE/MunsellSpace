#!/usr/bin/env python3
"""
Debug Lab conversion for RGB(85, 85, 102).
"""

import colour
import numpy as np

# Test color
rgb = [85/255, 85/255, 102/255]
print(f"RGB: {rgb}")

# Convert to XYZ (D65)
XYZ_D65 = colour.sRGB_to_XYZ(rgb)
print(f"XYZ (D65): {XYZ_D65}")

# Convert to xyY
xyY = colour.XYZ_to_xyY(XYZ_D65)
print(f"xyY: {xyY}")

# Illuminant C coordinates
illuminant_C = np.array([0.31006, 0.31616])
print(f"Illuminant C: {illuminant_C}")

# Reconstruct XYZ from xyY for chromatic adaptation
x, y, Y = xyY
X = x * Y / y
Z = (1 - x - y) * Y / y
XYZ_from_xyY = np.array([X, Y, Z])
print(f"XYZ from xyY: {XYZ_from_xyY}")

# Get the actual illuminant XYZ values (not just xy)
D65_XYZ = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
C_XYZ = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']

# Note: CCS_ILLUMINANTS only has xy values, we need full XYZ
# For chromatic adaptation, we need to use the xy_to_XYZ conversion
D65_xy = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
C_xy = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']

# Create full XYZ with Y=1 for white points
D65_XYZ_full = colour.xy_to_XYZ(np.append(D65_xy, 1))
C_XYZ_full = colour.xy_to_XYZ(np.append(C_xy, 1))

print(f"D65 XYZ: {D65_XYZ_full}")
print(f"C XYZ: {C_XYZ_full}")

# Chromatic adaptation from D65 to C
XYZ_C = colour.chromatic_adaptation(
    XYZ_D65,
    D65_XYZ_full,
    C_XYZ_full,
    method='Von Kries'
)
print(f"XYZ (adapted to C): {XYZ_C}")

# Convert to Lab (Illuminant C)
Lab_C = colour.XYZ_to_Lab(XYZ_C, illuminant=colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C'])
print(f"Lab (Illuminant C): {Lab_C}")

# Convert to LCHab
LCHab = colour.Lab_to_LCHab(Lab_C)
print(f"LCHab: {LCHab}")

print("\n" + "=" * 60)
print("What Rust is calculating:")
print("Lab: L=36.719906, a=1.518916, b=-7.044976")
print("This is WRONG!")

print("\nPython expects (from debug output):")
print("Lab: L=53.232882, a=76.178533, b=68.631447")
print("This looks suspicious too - those a,b values are huge for a near-gray color!")

print("\nThe issue: Rust is not doing chromatic adaptation correctly!")
print("It's using the wrong reference white or wrong adaptation method.")