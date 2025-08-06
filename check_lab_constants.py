#!/usr/bin/env python3
"""
Check the exact constants and formulas used in Python colour-science Lab conversion.
"""

import numpy as np
import colour
from colour.models.cie_lab import intermediate_lightness_function_CIE1976
import inspect

print("=== LAB CONVERSION CONSTANTS ===\n")

# Check the intermediate lightness function
try:
    source = inspect.getsource(intermediate_lightness_function_CIE1976)
    print("intermediate_lightness_function_CIE1976 source:")
    print(source)
except:
    print("Cannot get source - testing behavior...")
    
    # Test the function behavior
    test_values = [0.001, 0.008856, 0.008857, 0.1, 0.5, 1.0]
    for val in test_values:
        result = intermediate_lightness_function_CIE1976(val, 1.0)
        print(f"f({val}) = {result}")

# Check constants directly
print(f"\nConstants from colour.constants:")
try:
    from colour.constants import CIE_E, CIE_K
    print(f"CIE_E (epsilon) = {CIE_E}")
    print(f"CIE_K (kappa) = {CIE_K}")
except:
    print("Cannot import constants")

# Manual calculation of thresholds
epsilon = (6.0/29.0)**3
kappa = (29.0/3.0)**3
print(f"\nCalculated thresholds:")
print(f"epsilon = (6/29)^3 = {epsilon}")
print(f"kappa = (29/3)^3 = {kappa}")
print(f"Also kappa = 24389/27 = {24389.0/27.0}")

# Test Lab conversion step by step
xyz = np.array([0.20654008, 0.12197225, 0.05136952])
illuminant = np.array([0.31270, 0.32900])  # D65

print(f"\n=== STEP BY STEP LAB CONVERSION ===")
print(f"Input XYZ: {xyz}")
print(f"Illuminant xy: {illuminant}")

# Convert white point
from colour.models import xyY_to_XYZ, xy_to_xyY
white_xyY = xy_to_xyY(illuminant)
white_XYZ = xyY_to_XYZ(white_xyY)
print(f"White point xyY: {white_xyY}")
print(f"White point XYZ: {white_XYZ}")

# Normalize
X_norm = xyz[0] / white_XYZ[0]
Y_norm = xyz[1] / white_XYZ[1]
Z_norm = xyz[2] / white_XYZ[2]
print(f"Normalized XYZ: [{X_norm}, {Y_norm}, {Z_norm}]")

# Apply f function
fx = intermediate_lightness_function_CIE1976(X_norm, 1.0)
fy = intermediate_lightness_function_CIE1976(Y_norm, 1.0)
fz = intermediate_lightness_function_CIE1976(Z_norm, 1.0)
print(f"f(X/Xn), f(Y/Yn), f(Z/Zn): [{fx}, {fy}, {fz}]")

# Calculate Lab
L = 116 * fy - 16
a = 500 * (fx - fy)
b = 200 * (fy - fz)
print(f"Lab: [{L}, {a}, {b}]")

# Compare with colour.XYZ_to_Lab
lab_ref = colour.XYZ_to_Lab(xyz, illuminant)
print(f"colour.XYZ_to_Lab result: {lab_ref}")