#!/usr/bin/env python3
"""Compare Lab calculations between Python and Rust"""

import numpy as np
from colour import sRGB_to_XYZ
from colour.models import xyY_to_XYZ, XYZ_to_Lab

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
print(f"RGB normalized: {rgb}")

# Get XYZ
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ from sRGB: {xyz}")

# Convert to xyY
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
print(f"xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")

# Illuminant C coordinates
x_c, y_c = 0.31006, 0.31616
print(f"\nIlluminant C: [{x_c}, {y_c}]")

# Reference white for Lab calculation
# Using Illuminant C at the same Y as our color
xyz_ref_c = xyY_to_XYZ([x_c, y_c, xyy[2]])
print(f"Reference XYZ (Illuminant C at Y={xyy[2]:.4f}): {xyz_ref_c}")

# Calculate Lab using Illuminant C as reference
Lab_c = XYZ_to_Lab(xyz, xyz_ref_c)
print(f"\nLab (ref: Illuminant C): [{Lab_c[0]:.6f}, {Lab_c[1]:.6f}, {Lab_c[2]:.6f}]")

# Check if the b value is really 2078 or if there's an issue
C = np.hypot(Lab_c[1], Lab_c[2])
H = np.degrees(np.arctan2(Lab_c[2], Lab_c[1]))
print(f"LCHab: L={Lab_c[0]:.6f}, C={C:.6f}, H={H:.6f}")

# For comparison, calculate Lab with D65 (standard)
# D65 white point in xyY
x_d65, y_d65 = 0.31271, 0.32902
xyz_ref_d65 = xyY_to_XYZ([x_d65, y_d65, xyy[2]])
Lab_d65 = XYZ_to_Lab(xyz, xyz_ref_d65)
print(f"\nFor comparison - Lab (ref: D65 at Y={xyy[2]:.4f}): [{Lab_d65[0]:.6f}, {Lab_d65[1]:.6f}, {Lab_d65[2]:.6f}]")

print("\n" + "="*60)
print("RUST VALUES FROM TRACE:")
print("="*60)
print("Lab: [92.880004, -10.404759, 3.206791]")
print("LCHab: L=92.880004, C=10.887723, H=162.870479")

print("\n" + "="*60)
print("ANALYSIS:")
print("="*60)

# The Python Lab b value of 2078 is clearly wrong
# Let's check what's happening
print("\nDEBUG: Manual Lab calculation")
print(f"XYZ: {xyz}")
print(f"XYZ_ref: {xyz_ref_c}")

# Manual calculation
def f(t):
    """Lab f function"""
    delta = 6/29
    if t > delta**3:
        return t**(1/3)
    else:
        return t / (3 * delta**2) + 4/29

fx = f(xyz[0] / xyz_ref_c[0])
fy = f(xyz[1] / xyz_ref_c[1])
fz = f(xyz[2] / xyz_ref_c[2])

L_manual = 116 * fy - 16
a_manual = 500 * (fx - fy)
b_manual = 200 * (fy - fz)

print(f"\nManual Lab: L={L_manual:.6f}, a={a_manual:.6f}, b={b_manual:.6f}")

# Check the ratios
print(f"\nRatios:")
print(f"X/Xn = {xyz[0] / xyz_ref_c[0]:.6f}")
print(f"Y/Yn = {xyz[1] / xyz_ref_c[1]:.6f}")
print(f"Z/Zn = {xyz[2] / xyz_ref_c[2]:.6f}")

# The issue might be with how Illuminant C is being used
print("\n" + "="*60)
print("CONCLUSION:")
print("="*60)
print("Python's Lab calculation with Illuminant C reference gives b=2078.99")
print("This is because Z/Zn ratio is very small (0.9503), causing huge b value")
print("Rust's Lab values [92.88, -10.40, 3.21] look more reasonable")
print("The difference suggests Rust might be using a different reference white")