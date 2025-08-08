#!/usr/bin/env python3
"""Compare Lab calculations between Python and Rust implementations"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ
from colour.models import xyY_to_XYZ, XYZ_to_Lab

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
print("Testing RGB(221, 238, 238)")
print("="*60)

# Get XYZ
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ: {xyz}")

# Convert to xyY
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
print(f"xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")

# Illuminant C
x_c, y_c = 0.31006, 0.31616

print("\n" + "="*60)
print("PYTHON's APPROACH (from munsell.py):")
print("="*60)

# How Python ACTUALLY does it (incorrectly)
print("\nPython's INCORRECT usage (Y matches sample):")
xyz_ref_wrong = xyY_to_XYZ([x_c, y_c, xyy[2]])  # Y=0.827
Lab_wrong = XYZ_to_Lab(xyz, xyz_ref_wrong)
print(f"Reference XYZ: {xyz_ref_wrong}")
print(f"Lab: [{Lab_wrong[0]:.2f}, {Lab_wrong[1]:.2f}, {Lab_wrong[2]:.2f}]")
print(f"⚠️ b* = {Lab_wrong[2]:.2f} is unrealistic!")

# How it SHOULD be done
print("\nCORRECT usage (Y=1 for white point):")
xyz_ref_correct = xyY_to_XYZ([x_c, y_c, 1.0])  # Y=1
Lab_correct = XYZ_to_Lab(xyz, xyz_ref_correct)
print(f"Reference XYZ: {xyz_ref_correct}")
print(f"Lab: [{Lab_correct[0]:.2f}, {Lab_correct[1]:.2f}, {Lab_correct[2]:.2f}]")

# Calculate LCHab for both
import math
C_wrong = math.hypot(Lab_wrong[1], Lab_wrong[2])
H_wrong = math.degrees(math.atan2(Lab_wrong[2], Lab_wrong[1]))
if H_wrong < 0:
    H_wrong += 360

C_correct = math.hypot(Lab_correct[1], Lab_correct[2])
H_correct = math.degrees(math.atan2(Lab_correct[2], Lab_correct[1]))
if H_correct < 0:
    H_correct += 360

print("\n" + "="*60)
print("LCHab COMPARISON:")
print("="*60)
print(f"WRONG (Y=0.827): L={Lab_wrong[0]:.2f}, C={C_wrong:.2f}, H={H_wrong:.2f}")
print(f"CORRECT (Y=1):   L={Lab_correct[0]:.2f}, C={C_correct:.2f}, H={H_correct:.2f}")

print("\n" + "="*60)
print("RUST's TRACED VALUES:")
print("="*60)
print("From trace output:")
print("Lab: [92.880004, -10.404759, 3.206791]")
print("LCHab: L=92.880004, C=10.887723, H=162.870479")

print("\n" + "="*60)
print("ANALYSIS:")
print("="*60)
print(f"Python WRONG:   L={Lab_wrong[0]:.2f}, a={Lab_wrong[1]:.2f}, b={Lab_wrong[2]:.2f}")
print(f"Python CORRECT: L={Lab_correct[0]:.2f}, a={Lab_correct[1]:.2f}, b={Lab_correct[2]:.2f}")
print(f"Rust:           L=92.88, a=-10.40, b=3.21")
print()
print("Rust's values are close to Python's CORRECT values!")
print("This suggests Rust might be using Y=1 (correct) while Python uses Y=sample (wrong)")

print("\n" + "="*60)
print("CHECKING PYTHON'S INTERNAL CALCULATION:")
print("="*60)

# Let's trace what Python actually does
print("\nTracing Python's xyY_to_munsell_specification for this color...")

# Get the specification
spec = munsell.xyY_to_munsell_specification(xyy)
print(f"Final Munsell: {spec[0]:.1f}G {spec[1]:.1f}/{spec[2]:.1f}")

# The question is: does Python's wrong Lab calculation affect the final result?
print("\nDoes the wrong Lab calculation affect convergence?")
print("If Python and Rust get different Munsell values, then YES")
print("If they get the same Munsell values, then the Lab calculation")
print("might be used differently or not affect the final convergence")