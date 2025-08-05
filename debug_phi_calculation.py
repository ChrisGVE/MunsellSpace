#!/usr/bin/env python3
"""Debug phi calculation for angle 288.8°"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import (
    munsell_value, munsell_specification_to_xyY,
    hue_angle_to_hue
)
from colour.algebra import cartesian_to_cylindrical

# Setup for RGB [68,0,68]
rgb = [68, 0, 68]
rgb_normalized = np.array(rgb) / 255.0
xyz = sRGB_to_XYZ(rgb_normalized)
xyy = XYZ_to_xyY(xyz)

x_input, y_input, Y = xyy[0], xyy[1], xyy[2] * 100
munsell_val = munsell_value(Y)

# Get achromatic center
munsell_spec_achromatic = np.array([0, munsell_val, 0, 0])
xy_center = munsell_specification_to_xyY(munsell_spec_achromatic)
x_center, y_center = xy_center[0], xy_center[1]

# Input point's phi
rho_input, phi_input, _ = cartesian_to_cylindrical(
    np.array([x_input - x_center, y_input - y_center, Y])
)

print(f"Input point: x={x_input:.6f}, y={y_input:.6f}")
print(f"Achromatic center: x={x_center:.6f}, y={y_center:.6f}")
print(f"Input phi: {np.degrees(phi_input):.3f}°")
print("=" * 60)

# Test angle 288.8° with RP family
angle = 288.8
hue, code = hue_angle_to_hue(angle)
print(f"\nTest angle {angle}° -> hue={hue:.3f}, code={code} (RP)")

# Current chroma from iteration 0
chroma = 8.117

# Create specification and get xy
munsell_spec = np.array([hue, munsell_val, chroma, code])
xy_test = munsell_specification_to_xyY(munsell_spec)
x_test, y_test = xy_test[0], xy_test[1]

print(f"Test point: x={x_test:.6f}, y={y_test:.6f}")

# Calculate phi for test point
rho_test, phi_test, _ = cartesian_to_cylindrical(
    np.array([x_test - x_center, y_test - y_center, Y])
)

print(f"Test phi: {np.degrees(phi_test):.3f}°")

# Calculate phi difference (Python's formula)
phi_diff = (360 - np.degrees(phi_input) + np.degrees(phi_test)) % 360
if phi_diff > 180:
    phi_diff -= 360

print(f"\nPhi difference calculation:")
print(f"  (360 - {np.degrees(phi_input):.3f} + {np.degrees(phi_test):.3f}) % 360")
print(f"  = {(360 - np.degrees(phi_input) + np.degrees(phi_test)):.3f} % 360")
print(f"  = {(360 - np.degrees(phi_input) + np.degrees(phi_test)) % 360:.3f}")
print(f"  After normalization: {phi_diff:.3f}°")

print("\nExpected: -0.077° (from Python trace)")
print(f"Calculated: {phi_diff:.3f}°")