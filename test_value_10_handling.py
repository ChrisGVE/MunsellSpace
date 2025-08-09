#!/usr/bin/env python3
"""Test how Python handles value=10 in interpolation."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import (
    munsell_specification_to_xy,
    luminance_ASTMD1535,
    LinearInterpolator
)
from colour.utilities import from_range_100

# Test specification with value=9.3528
spec = [8.6058, 9.3528, 12.6521, 4.0]

print("Testing Python's approach for value=9.3528:")
print("="*60)

# Python's logic:
value = 9.3528
value_minus = np.floor(value)  # 9
value_plus = value_minus + 1    # 10

print(f"value_minus = {value_minus}")
print(f"value_plus = {value_plus}")

# For value_minus=9
spec_minus = [8.6058, value_minus, 12.6521, 4.0]
xy_minus = munsell_specification_to_xy(spec_minus)
print(f"\nspec_minus = {spec_minus}")
print(f"xy_minus = {xy_minus}")

# For value_plus=10, Python does something special!
# From line 903: if value_plus == 10, it doesn't pass chroma
spec_plus = value_plus  # Just the value, not the full spec!
print(f"\nspec_plus = {spec_plus} (just value, not full spec!)")

# What does munsell_specification_to_xy return for just a value?
xy_plus = munsell_specification_to_xy(spec_plus)
print(f"xy_plus = {xy_plus}")

# Now interpolate based on Y luminance
Y = luminance_ASTMD1535(value)
Y_minus = luminance_ASTMD1535(value_minus)
Y_plus = luminance_ASTMD1535(value_plus)

print(f"\nLuminance values:")
print(f"Y (at {value}) = {Y}")
print(f"Y_minus (at {value_minus}) = {Y_minus}")
print(f"Y_plus (at {value_plus}) = {Y_plus}")

# Python uses LinearInterpolator with Y values
Y_minus_plus = np.array([Y_minus, Y_plus])
x_minus_plus = np.array([xy_minus[0], xy_plus[0]])
y_minus_plus = np.array([xy_minus[1], xy_plus[1]])

x_interpolated = LinearInterpolator(Y_minus_plus, x_minus_plus)(Y)
y_interpolated = LinearInterpolator(Y_minus_plus, y_minus_plus)(Y)

print(f"\nInterpolation:")
print(f"Y values for interpolation: {Y_minus_plus}")
print(f"x values for interpolation: {x_minus_plus}")
print(f"y values for interpolation: {y_minus_plus}")
print(f"\nInterpolated x = {x_interpolated}")
print(f"Interpolated y = {y_interpolated}")

# Calculate rho
x_center = 0.31006
y_center = 0.31616
x_diff = x_interpolated - x_center
y_diff = y_interpolated - y_center
rho = np.sqrt(x_diff**2 + y_diff**2)

print(f"\nFinal result:")
print(f"x = {x_interpolated:.6f}, y = {y_interpolated:.6f}")
print(f"rho = {rho:.6f}")

print(f"\nExpected from _munsell_specification_to_xyY: x=0.326212, y=0.443071, rho=0.127935")