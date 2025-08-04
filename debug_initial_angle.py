#!/usr/bin/env python3
"""Debug the initial angle for RGB [68,0,68]"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.algebra import cartesian_to_cylindrical
from colour.notation.munsell import munsell_value, munsell_specification_to_xyY, hue_angle_to_hue

# Test RGB [68,0,68]
rgb = [68, 0, 68]
rgb_normalized = np.array(rgb) / 255.0

# Convert to xyY
xyz = sRGB_to_XYZ(rgb_normalized)
xyy = XYZ_to_xyY(xyz)

print(f"RGB {rgb} -> xyY: {xyy}")

# Get Munsell value
Y = xyy[2] * 100  # Convert to percentage
munsell_val = munsell_value(Y)
print(f"Y={Y:.3f} -> Munsell value={munsell_val:.3f}")

# Get achromatic center for this value
munsell_spec_achromatic = [0, munsell_val, 0, 0]  # N value
xy_center = munsell_specification_to_xyY(munsell_spec_achromatic)
x_center, y_center = xy_center[0], xy_center[1]
print(f"Achromatic center: x={x_center:.6f}, y={y_center:.6f}")

# Calculate angle from achromatic center
x_input, y_input = xyy[0], xyy[1]
print(f"Input: x={x_input:.6f}, y={y_input:.6f}")

# Polar coordinates
rho, phi, _ = cartesian_to_cylindrical(
    np.array([x_input - x_center, y_input - y_center, Y])
)

phi_degrees = np.degrees(phi)
print(f"\nPolar coords relative to center:")
print(f"  rho={rho:.6f}")
print(f"  phi={phi:.6f} radians = {phi_degrees:.2f}°")

# Normalize angle to [0, 360)
initial_angle = phi_degrees % 360
print(f"\nInitial angle (normalized): {initial_angle:.2f}°")

# Convert to hue
hue_result = hue_angle_to_hue(initial_angle)
print(f"hue_angle_to_hue({initial_angle:.2f}°) -> hue={hue_result[0]:.3f}, code={hue_result[1]}")

families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
            6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
family = families.get(int(hue_result[1]), '?')
print(f"Initial guess: {hue_result[0]:.1f}{family}")

print("\n" + "=" * 60)
print("DEBUGGING:")
print("=" * 60)

# What angle should give us 0.7RP?
from colour.notation.munsell import hue_to_hue_angle
correct_angle = hue_to_hue_angle(np.array([0.7, 8]))  # 0.7RP
print(f"0.7RP should be at angle {correct_angle:.2f}°")

# What's the difference?
print(f"Our initial angle: {initial_angle:.2f}°")
print(f"Correct angle: {correct_angle:.2f}°")
print(f"Difference: {initial_angle - correct_angle:.2f}°")