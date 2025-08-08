#!/usr/bin/env python3
"""Check how colour library does RGB to XYZ conversion"""

import numpy as np
from colour import RGB_to_XYZ
from colour.models import RGB_COLOURSPACE_sRGB

# Get the colorspace details
cs = RGB_COLOURSPACE_sRGB
print("sRGB Colorspace details:")
print(f"  Whitepoint: {cs.whitepoint}")
print(f"  Matrix RGB to XYZ:\n{cs.matrix_RGB_to_XYZ}")
print(f"  Use derived matrix: {cs.use_derived_matrix_RGB_to_XYZ}")

# Test RGB(221, 238, 238)
rgb_norm = np.array([221/255.0, 238/255.0, 238/255.0])
print(f"\nTesting RGB: {rgb_norm}")

# Get XYZ with different settings
xyz_default = RGB_to_XYZ(rgb_norm, RGB_COLOURSPACE_sRGB)
print(f"\nDefault XYZ: {xyz_default}")

# Try with explicit illuminant 
xyz_with_illuminant = RGB_to_XYZ(rgb_norm, RGB_COLOURSPACE_sRGB, illuminant=cs.whitepoint)
print(f"XYZ with explicit illuminant: {xyz_with_illuminant}")

# Check if it's applying normalization
print(f"\nWhitepoint name: {cs.whitepoint_name}")

# Calculate XYZ manually using colour's matrix
def manual_rgb_to_xyz(rgb):
    """Manual conversion using colour's matrix"""
    # First apply gamma correction
    linear = np.zeros(3)
    for i in range(3):
        c = rgb[i]
        if c <= 0.04045:
            linear[i] = c / 12.92
        else:
            linear[i] = ((c + 0.055) / 1.055) ** 2.4
    
    # Then apply matrix
    xyz = np.dot(cs.matrix_RGB_to_XYZ, linear)
    return xyz

xyz_manual = manual_rgb_to_xyz(rgb_norm)
print(f"\nManual calculation with colour's matrix: {xyz_manual}")

# Check if there's scaling
ratio = xyz_default / xyz_manual
print(f"Ratio (colour/manual): {ratio}")

# Check the whitepoint values
print(f"\nD65 whitepoint XYZ: {cs.whitepoint}")
print(f"Sum of whitepoint: {np.sum(cs.whitepoint)}")

# It might be normalizing by the whitepoint
xyz_normalized = xyz_manual / cs.whitepoint
print(f"\nXYZ divided by whitepoint: {xyz_normalized}")

# Or maybe scaling to Y=1 for white
white_rgb = np.array([1.0, 1.0, 1.0])
white_xyz = RGB_to_XYZ(white_rgb, RGB_COLOURSPACE_sRGB)
print(f"\nWhite RGB [1,1,1] -> XYZ: {white_xyz}")

# The scaling factor might be from this
scale_factor = white_xyz[1]  # Y component of white
xyz_scaled = xyz_manual * scale_factor
print(f"\nXYZ scaled by white Y ({scale_factor:.6f}): {xyz_scaled}")

# That's close! Let's check the exact calculation
print(f"\nDifference (scaled - colour): {xyz_scaled - xyz_default}")
print(f"Relative error: {(xyz_scaled - xyz_default) / xyz_default * 100}%")