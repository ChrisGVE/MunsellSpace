#!/usr/bin/env python3
"""Check XYZ normalization in colour library"""

import numpy as np
from colour import RGB_to_XYZ
from colour.models import RGB_COLOURSPACE_sRGB

# Test with white to understand normalization
white_rgb = np.array([1.0, 1.0, 1.0])
white_xyz = RGB_to_XYZ(white_rgb, RGB_COLOURSPACE_sRGB)
print(f"White RGB [1,1,1] -> XYZ: {white_xyz}")
print(f"White Y component: {white_xyz[1]:.10f}")

# Now test our color
rgb_norm = np.array([221/255.0, 238/255.0, 238/255.0])

# Manual calculation
def manual_srgb_to_xyz(rgb):
    """Manual sRGB to XYZ"""
    # Linearize
    linear = np.zeros(3)
    for i in range(3):
        c = rgb[i]
        if c <= 0.04045:
            linear[i] = c / 12.92
        else:
            linear[i] = ((c + 0.055) / 1.055) ** 2.4
    
    # Matrix from sRGB standard
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    
    xyz = np.dot(matrix, linear)
    return xyz

xyz_manual = manual_srgb_to_xyz(rgb_norm)
xyz_colour = RGB_to_XYZ(rgb_norm, RGB_COLOURSPACE_sRGB)

print(f"\nRGB {rgb_norm}:")
print(f"  Manual XYZ: {xyz_manual}")
print(f"  Colour XYZ: {xyz_colour}")
print(f"  Ratio: {xyz_colour / xyz_manual}")

# The scaling factor appears to be white_xyz[1]
scale = white_xyz[1]
xyz_scaled = xyz_manual * scale
print(f"\nManual XYZ scaled by {scale:.10f}: {xyz_scaled}")
print(f"Difference from colour: {xyz_scaled - xyz_colour}")
print(f"Max absolute error: {np.max(np.abs(xyz_scaled - xyz_colour)):.10f}")

# Check if this is exactly 1/0.9505 (the Y component of white in the matrix)
matrix_white_y = 0.2126729 + 0.7151522 + 0.0721750
print(f"\nSum of Y row in matrix: {matrix_white_y:.10f}")
print(f"1 / matrix_white_y: {1.0 / matrix_white_y:.10f}")
print(f"White XYZ Y: {white_xyz[1]:.10f}")
print(f"Are they equal? {np.isclose(1.0 / matrix_white_y, white_xyz[1])}")

# So the colour library normalizes XYZ so that white has Y=1
print(f"\n=== CONCLUSION ===")
print(f"The colour library scales XYZ values by {scale:.10f}")
print(f"This makes white RGB(255,255,255) map to Y=1.0")
print(f"Rust is using unscaled values where white maps to Y≈0.9505")