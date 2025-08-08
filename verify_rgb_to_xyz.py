#!/usr/bin/env python3
"""Verify RGB to XYZ conversion step by step"""

import numpy as np

def srgb_to_linear(rgb):
    """Convert sRGB to linear RGB"""
    linear = np.zeros(3)
    for i in range(3):
        c = rgb[i]
        if c <= 0.04045:
            linear[i] = c / 12.92
        else:
            linear[i] = ((c + 0.055) / 1.055) ** 2.4
    return linear

def linear_rgb_to_xyz_d65(rgb_linear):
    """Convert linear RGB to XYZ using D65 illuminant"""
    # sRGB to XYZ matrix (D65 illuminant)
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    
    xyz = np.dot(matrix, rgb_linear)
    return xyz

def xyz_to_xyy(xyz):
    """Convert XYZ to xyY"""
    total = xyz[0] + xyz[1] + xyz[2]
    if total < 1e-10:
        return np.array([0.31271, 0.32902, 0.0])  # D65 white point for black
    else:
        return np.array([xyz[0] / total, xyz[1] / total, xyz[1]])

# Test RGB(221, 238, 238)
r, g, b = 221, 238, 238
print(f"Testing RGB({r}, {g}, {b})")
print("="*50)

# Step 1: Normalize to 0-1
rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
print(f"1. Normalized RGB: [{rgb_norm[0]:.6f}, {rgb_norm[1]:.6f}, {rgb_norm[2]:.6f}]")

# Step 2: sRGB to linear RGB
rgb_linear = srgb_to_linear(rgb_norm)
print(f"2. Linear RGB: [{rgb_linear[0]:.6f}, {rgb_linear[1]:.6f}, {rgb_linear[2]:.6f}]")

# Step 3: Linear RGB to XYZ
xyz = linear_rgb_to_xyz_d65(rgb_linear)
print(f"3. XYZ (D65): [{xyz[0]:.6f}, {xyz[1]:.6f}, {xyz[2]:.6f}]")

# Step 4: XYZ to xyY
xyy = xyz_to_xyy(xyz)
print(f"4. xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")

print("\nComparison:")
print(f"  Python gets XYZ: [0.859640, 0.919160, 1.015113]")
print(f"  We calculated:   [{xyz[0]:.6f}, {xyz[1]:.6f}, {xyz[2]:.6f}]")
print(f"  Python gets xyY: [0.307683, 0.328987, 0.919160]")
print(f"  We calculated:   [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")

# Also check what the colour library gets
from colour import RGB_to_XYZ, XYZ_to_xyY
from colour.models import RGB_COLOURSPACE_sRGB

xyz_colour = RGB_to_XYZ(rgb_norm, RGB_COLOURSPACE_sRGB)
xyy_colour = XYZ_to_xyY(xyz_colour)

print(f"\nColour library:")
print(f"  XYZ: [{xyz_colour[0]:.6f}, {xyz_colour[1]:.6f}, {xyz_colour[2]:.6f}]")
print(f"  xyY: [{xyy_colour[0]:.6f}, {xyy_colour[1]:.6f}, {xyy_colour[2]:.6f}]")

# The difference might be if Python scales Y differently
print(f"\nNote: Rust seems to get xyY with Y={0.826933:.6f}")
print(f"      Python gets xyY with Y={0.919160:.6f}")
print(f"      Ratio: {0.919160/0.826933:.6f}")