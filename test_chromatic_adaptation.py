#!/usr/bin/env python3
"""Test if colour library applies chromatic adaptation for Munsell"""

import numpy as np
from colour import RGB_to_XYZ, XYZ_to_xyY
from colour.models import RGB_COLOURSPACE_sRGB
from colour.adaptation import chromatic_adaptation_VonKries

# D65 and Illuminant C in XYZ (normalized to Y=1)
# D65: x=0.31271, y=0.32902
D65_xy = np.array([0.31271, 0.32902])
D65_XYZ = np.array([D65_xy[0]/D65_xy[1], 1.0, (1-D65_xy[0]-D65_xy[1])/D65_xy[1]])

# Illuminant C: x=0.31006, y=0.31616  
C_xy = np.array([0.31006, 0.31616])
C_XYZ = np.array([C_xy[0]/C_xy[1], 1.0, (1-C_xy[0]-C_xy[1])/C_xy[1]])

print(f"D65 XYZ: {D65_XYZ}")
print(f"C XYZ: {C_XYZ}")

# Test color
rgb_norm = np.array([221/255.0, 238/255.0, 238/255.0])

# Get XYZ under D65
xyz_d65 = RGB_to_XYZ(rgb_norm, RGB_COLOURSPACE_sRGB)
print(f"\nXYZ (D65): {xyz_d65}")

# Apply chromatic adaptation from D65 to C
xyz_c = chromatic_adaptation_VonKries(xyz_d65, D65_XYZ, C_XYZ)
print(f"XYZ (C) after adaptation: {xyz_c}")

# Convert to xyY
xyy_d65 = XYZ_to_xyY(xyz_d65)
xyy_c = XYZ_to_xyY(xyz_c)

print(f"\nxyY (D65): {xyy_d65}")
print(f"xyY (C): {xyy_c}")

# What Python trace shows
print(f"\nPython trace shows:")
print(f"  XYZ: [0.859640, 0.919160, 1.015113]")
print(f"  xyY: [0.307683, 0.328987, 0.919160]")

# Compare
print(f"\nOur D65 XYZ: {xyz_d65}")
print(f"Python XYZ:  [0.859640, 0.919160, 1.015113]")
print(f"Match? {np.allclose(xyz_d65, [0.859640, 0.919160, 1.015113])}")

# The Python munsell function might be expecting XYZ scaled differently
# Let's check what happens if we DON'T scale
def manual_srgb_to_xyz_unscaled(rgb):
    """Manual sRGB to XYZ without any scaling"""
    # Linearize
    linear = np.zeros(3)
    for i in range(3):
        c = rgb[i]
        if c <= 0.04045:
            linear[i] = c / 12.92
        else:
            linear[i] = ((c + 0.055) / 1.055) ** 2.4
    
    # Standard matrix
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    
    return np.dot(matrix, linear)

xyz_unscaled = manual_srgb_to_xyz_unscaled(rgb_norm)
xyy_unscaled = XYZ_to_xyY(xyz_unscaled)

print(f"\nUnscaled XYZ: {xyz_unscaled}")
print(f"Unscaled xyY: {xyy_unscaled}")
print(f"Rust gets xyY: [0.301656, 0.328990, 0.826933]")
print(f"Match? {np.allclose(xyy_unscaled, [0.301656, 0.328990, 0.826933], atol=1e-5)}")