#!/usr/bin/env python3
"""
Compare specific functions between Python and Rust implementations.
"""

import numpy as np
import colour
from colour.models import XYZ_to_Lab, Lab_to_LCHab
from colour.notation.munsell import LCHab_to_munsell_specification
import inspect

# Test values
xyz_test = np.array([0.20654008, 0.12197225, 0.05136952])
xy_white = np.array([0.31270, 0.32900])  # D65
lchab_test = np.array([87.735, 124.273, 136.357])

print("=== PYTHON REFERENCE IMPLEMENTATIONS ===\n")

# 1. Test XYZ_to_Lab
print("1. XYZ_to_Lab function:")
try:
    source = inspect.getsource(XYZ_to_Lab)
    print(source)
except:
    print("Cannot get source - checking constants...")
    lab_result = XYZ_to_Lab(xyz_test)
    print(f"XYZ_to_Lab({xyz_test}) = {lab_result}")

# 2. Test Lab_to_LCHab  
print("\n2. Lab_to_LCHab function:")
try:
    source = inspect.getsource(Lab_to_LCHab)
    print(source)
except:
    print("Cannot get source - checking result...")
    lab_input = np.array([87.735, 22.103, -45.517])
    lch_result = Lab_to_LCHab(lab_input)
    print(f"Lab_to_LCHab({lab_input}) = {lch_result}")

# 3. Test LCHab_to_munsell_specification
print("\n3. LCHab_to_munsell_specification function:")
try:
    source = inspect.getsource(LCHab_to_munsell_specification)
    print(source)
except:
    print("Cannot get source - checking result...")

spec_result = LCHab_to_munsell_specification(lchab_test)
print(f"LCHab_to_munsell_specification({lchab_test}) = {spec_result}")

# Check constants
print("\n=== KEY CONSTANTS ===")
print(f"epsilon (6/29)^3 = {(6.0/29.0)**3}")
print(f"kappa 24389/27 = {24389.0/27.0}")

# Test the critical hue angle adjustment
print("\n=== HUE ANGLE ADJUSTMENT TEST ===")
for h in [0, 18, 36, 136.357, 180, 270, 324, 360]:
    adjusted = (h + 18) % 360
    print(f"Angle {h} -> adjusted: {adjusted}")
    spec = LCHab_to_munsell_specification([50, 50, h])
    print(f"  -> Munsell spec: {spec}\n")