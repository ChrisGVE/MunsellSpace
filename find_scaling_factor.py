#!/usr/bin/env python3
"""Find the exact scaling factor colour library uses"""

import numpy as np
from colour import RGB_to_XYZ
from colour.models import RGB_COLOURSPACE_sRGB

rgb_norm = np.array([221/255.0, 238/255.0, 238/255.0])

# Manual calculation with standard matrix
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
    
    # Standard sRGB to XYZ matrix
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    
    xyz = np.dot(matrix, linear)
    return xyz

xyz_manual = manual_srgb_to_xyz(rgb_norm)
xyz_colour = RGB_to_XYZ(rgb_norm, RGB_COLOURSPACE_sRGB)

print("Comparison:")
print(f"  Manual XYZ: [{xyz_manual[0]:.10f}, {xyz_manual[1]:.10f}, {xyz_manual[2]:.10f}]")
print(f"  Colour XYZ: [{xyz_colour[0]:.10f}, {xyz_colour[1]:.10f}, {xyz_colour[2]:.10f}]")

# Calculate the scaling factor for each component
scale_x = xyz_colour[0] / xyz_manual[0]
scale_y = xyz_colour[1] / xyz_manual[1]
scale_z = xyz_colour[2] / xyz_manual[2]

print(f"\nScaling factors:")
print(f"  X: {scale_x:.10f}")
print(f"  Y: {scale_y:.10f}")
print(f"  Z: {scale_z:.10f}")

# Check if they're all close to the same value
if np.allclose([scale_x, scale_y, scale_z], scale_y):
    print(f"\nUniform scaling factor: {scale_y:.10f}")
    
    # What is this scaling factor?
    # Check against white normalization
    white_linear = np.array([1.0, 1.0, 1.0])
    matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    white_xyz_unscaled = np.dot(matrix, white_linear)
    print(f"\nWhite XYZ (unscaled): {white_xyz_unscaled}")
    print(f"White Y (unscaled): {white_xyz_unscaled[1]:.10f}")
    
    expected_scale = 1.0 / white_xyz_unscaled[1]
    print(f"Expected scale (1/white_Y): {expected_scale:.10f}")
    print(f"Actual scale: {scale_y:.10f}")
    print(f"Match? {np.isclose(expected_scale, scale_y)}")
else:
    print("\nNon-uniform scaling!")
    
# Let's check the exact matrix colour uses
print(f"\nColour library matrix:\n{RGB_COLOURSPACE_sRGB.matrix_RGB_to_XYZ}")

# Compare matrices
our_matrix = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
])

colour_matrix = RGB_COLOURSPACE_sRGB.matrix_RGB_to_XYZ

print(f"\nMatrix difference:")
print(colour_matrix - our_matrix)

# The colour library might be using a slightly different matrix
# Let's apply colour's exact matrix
linear = np.zeros(3) 
for i in range(3):
    c = rgb_norm[i]
    if c <= 0.04045:
        linear[i] = c / 12.92
    else:
        linear[i] = ((c + 0.055) / 1.055) ** 2.4

xyz_with_colour_matrix = np.dot(colour_matrix, linear)
print(f"\nUsing colour's matrix: {xyz_with_colour_matrix}")
print(f"Colour library result: {xyz_colour}")
print(f"Difference: {xyz_colour - xyz_with_colour_matrix}")

# Calculate new scale
new_scale = xyz_colour[1] / xyz_with_colour_matrix[1]
print(f"\nScale factor with colour's matrix: {new_scale:.10f}")