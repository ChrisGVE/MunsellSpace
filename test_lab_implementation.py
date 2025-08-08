#!/usr/bin/env python3
"""Test Lab implementation differences between Python and Rust"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ
from colour.models import xyY_to_XYZ, XYZ_to_Lab

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

print("Testing Lab calculation approaches")
print("="*60)
print(f"Input: RGB(221, 238, 238)")
print(f"XYZ: {xyz}")
print(f"xyY: {xyy}")

# Illuminant C coordinates
x_c, y_c = 0.31006, 0.31616

print("\n" + "="*60)
print("APPROACH 1: Python's WRONG way (Y matches sample)")
print("="*60)
# This is what Python colour-science actually does in munsell.py
xyz_r_wrong = xyY_to_XYZ([x_c, y_c, xyy[2]])  # Y=0.827 (sample's Y)
Lab_wrong = XYZ_to_Lab(xyz, xyz_r_wrong)
print(f"Reference XYZ (Y={xyy[2]:.3f}): {xyz_r_wrong}")
print(f"Lab: [{Lab_wrong[0]:.2f}, {Lab_wrong[1]:.2f}, {Lab_wrong[2]:.2f}]")

print("\n" + "="*60)  
print("APPROACH 2: CORRECT way (Y=1 for white)")
print("="*60)
xyz_r_correct = xyY_to_XYZ([x_c, y_c, 1.0])  # Y=1 (proper white point)
Lab_correct = XYZ_to_Lab(xyz, xyz_r_correct)
print(f"Reference XYZ (Y=1): {xyz_r_correct}")
print(f"Lab: [{Lab_correct[0]:.2f}, {Lab_correct[1]:.2f}, {Lab_correct[2]:.2f}]")

print("\n" + "="*60)
print("APPROACH 3: What Rust MIGHT be doing")
print("="*60)
# Looking at the Rust code, it normalizes the reference:
# xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]]
xyz_r = xyY_to_XYZ([x_c, y_c, xyy[2]])
xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]]
print(f"Normalized ref XYZ: {xyz_r_norm}")

# The Rust code then converts this back to xy coordinates
x_norm = xyz_r_norm[0] / (xyz_r_norm[0] + xyz_r_norm[1] + xyz_r_norm[2])
y_norm = xyz_r_norm[1] / (xyz_r_norm[0] + xyz_r_norm[1] + xyz_r_norm[2])
print(f"Normalized ref xy: [{x_norm:.6f}, {y_norm:.6f}]")

# If Rust's xyz_to_lab takes xy coordinates and assumes Y=1...
# Then it would effectively use the CORRECT approach!

print("\n" + "="*60)
print("CONCLUSION:")
print("="*60)
print("Python uses Y=sample (WRONG): Lab b* = 2078")
print("Correct uses Y=1 (RIGHT):     Lab b* = 1397")
print("Rust normalizes to Y=1:       Should get b* ≈ 1397")
print()
print("But Rust trace shows: Lab b* = 3.21")
print("This suggests Rust is doing something different!")
print()
print("The normalization in Rust (xyz_r_norm) ensures Y=1,")
print("which should prevent the huge b* value issue.")