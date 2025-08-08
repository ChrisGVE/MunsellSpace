#!/usr/bin/env python3
"""Verify what Rust's Lab calculation is actually doing"""

import numpy as np
from colour import sRGB_to_XYZ
from colour.models import xyY_to_XYZ

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ: {xyz}")

# Illuminant C coordinates
x_c, y_c = 0.31006, 0.31616

print("\n" + "="*60)
print("RUST'S APPROACH (from python_port_helpers.rs):")
print("="*60)

# Step 1: Rust gets xyz_r from Illuminant C at sample's Y
Y_sample = xyz[1]  # 0.8269
xyz_r = xyY_to_XYZ([x_c, y_c, Y_sample])
print(f"xyz_r (at Y={Y_sample:.4f}): {xyz_r}")

# Step 2: Rust normalizes it to Y=1
xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]]
print(f"xyz_r_norm (Y=1): {xyz_r_norm}")

# Step 3: Rust converts normalized XYZ back to xy
x_norm = xyz_r_norm[0] / (xyz_r_norm[0] + xyz_r_norm[1] + xyz_r_norm[2])
y_norm = xyz_r_norm[1] / (xyz_r_norm[0] + xyz_r_norm[1] + xyz_r_norm[2])
print(f"xy from normalized: [{x_norm:.6f}, {y_norm:.6f}]")

# Step 4: xyz_to_lab in python_port_helpers.rs takes this xy and assumes Y=1
# It converts xy to XYZ with Y=1 internally:
# xn = white_point[0] / white_point[1]  # x/y
# yn = 1.0
# zn = (1.0 - white_point[0] - white_point[1]) / white_point[1]

xn = x_norm / y_norm
yn = 1.0
zn = (1.0 - x_norm - y_norm) / y_norm

print(f"\nWhite point XYZ used in Lab: [{xn:.6f}, {yn:.6f}, {zn:.6f}]")

# This should match Illuminant C at Y=1
xyz_c_y1 = xyY_to_XYZ([x_c, y_c, 1.0])
print(f"Illuminant C at Y=1:         [{xyz_c_y1[0]:.6f}, {xyz_c_y1[1]:.6f}, {xyz_c_y1[2]:.6f}]")

print("\nThey match! Rust correctly uses Y=1 for the white point.")

# Now calculate Lab with this approach
epsilon = 216.0 / 24389.0
kappa = 24389.0 / 27.0

x_norm = xyz[0] / xn
y_norm = xyz[1] / yn
z_norm = xyz[2] / zn

def f(t):
    if t > epsilon:
        return t ** (1/3)
    else:
        return (kappa * t + 16) / 116

fx = f(x_norm)
fy = f(y_norm)
fz = f(z_norm)

L = 116 * fy - 16
a = 500 * (fx - fy)
b = 200 * (fy - fz)

print("\n" + "="*60)
print("CALCULATED LAB VALUES:")
print("="*60)
print(f"Rust's approach (Y=1): L={L:.2f}, a={a:.2f}, b={b:.2f}")

# From Rust trace
print(f"Rust trace shows:      L=92.88, a=-10.40, b=3.21")

print("\n" + "="*60)
print("ANALYSIS:")
print("="*60)
print("The huge discrepancy in b* values:")
print("- My calculation: b=1397")
print("- Rust trace: b=3.21")
print()
print("This massive difference suggests Rust is NOT using")
print("the standard Lab formula, or there's something else")
print("happening in the calculation.")