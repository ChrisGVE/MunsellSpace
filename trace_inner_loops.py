#!/usr/bin/env python3
"""Trace the inner loops more carefully"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import (
    munsell_value, munsell_specification_to_xyY,
    hue_angle_to_hue, hue_to_hue_angle,
    maximum_chroma_from_renotation
)
from colour.algebra import cartesian_to_cylindrical
from colour.utilities import as_float_array

# Setup
rgb = [68, 0, 68]
rgb_normalized = np.array(rgb) / 255.0
xyz = sRGB_to_XYZ(rgb_normalized)
xyy = XYZ_to_xyY(xyz)

THRESHOLD_INTEGER = 1e-3
x_input, y_input, Y = as_float_array(xyy).tolist()
Y = Y * 100

munsell_val = munsell_value(Y)
munsell_specification = as_float_array([0, munsell_val, 0, 0])
x_center, y_center = munsell_specification_to_xyY(munsell_specification)[0:2]

rho_input, phi_input, _ = cartesian_to_cylindrical(
    np.array([x_input - x_center, y_input - y_center, Y])
)

# Initial guess
hue_initial_angle = np.degrees(phi_input) % 360
hue_current, code_current = hue_angle_to_hue(hue_initial_angle)
chroma_current = rho_input * 50

print(f"Initial: hue={hue_current:.3f}, code={code_current}, chroma={chroma_current:.3f}")
print("=" * 70)

# First iteration - focus on the inner hue loop
print("\nIteration 0 - Inner Hue Loop:")
print("-" * 40)

# Cap chroma
chroma_maximum = maximum_chroma_from_renotation(
    np.array([hue_current, munsell_val, code_current])
)
if chroma_current > chroma_maximum:
    chroma_current = chroma_maximum
    print(f"Chroma capped at {chroma_maximum:.3f}")

munsell_specification[0] = hue_current
munsell_specification[2] = chroma_current
munsell_specification[3] = code_current

# Current position
x_current, y_current = munsell_specification_to_xyY(munsell_specification)[0:2]
rho_current, phi_current, _ = cartesian_to_cylindrical(
    np.array([x_current - x_center, y_current - y_center, Y])
)

print(f"Current position: hue={hue_current:.3f}, code={code_current}")
print(f"  xy: ({x_current:.6f}, {y_current:.6f})")
print(f"  polar: rho={rho_current:.6f}, phi={np.degrees(phi_current):.2f}°")

# Calculate phi difference
phi_current_difference = (360 - np.degrees(phi_input) + np.degrees(phi_current)) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360
print(f"  phi_difference: {phi_current_difference:.3f}°")

# The inner hue loop (Python lines 1143-1224)
# This loop collects points by testing different hue angles
print("\nCollecting points for hue interpolation:")

phi_differences_data = []
hue_angles_differences_data = []

if abs(phi_current_difference) > 1e-6:
    phi_differences_data.append(phi_current_difference)
    hue_angles_differences_data.append(0)

hue_angle_current = hue_to_hue_angle(np.array([hue_current, code_current]))
print(f"  Starting hue_angle: {hue_angle_current:.2f}°")

# Inner loop iterations
for i in range(1, 5):  # Show first few iterations
    # Python line 1167: step by i * (phi_input - phi_current)
    hue_angle_inner = (hue_angle_current + i * (np.degrees(phi_input) - np.degrees(phi_current))) % 360
    
    hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
    
    # Test this position
    munsell_specification[0] = hue_inner
    munsell_specification[3] = code_inner
    x_inner, y_inner = munsell_specification_to_xyY(munsell_specification)[0:2]
    
    rho_inner, phi_inner, _ = cartesian_to_cylindrical(
        np.array([x_inner - x_center, y_inner - y_center, Y])
    )
    
    phi_inner_difference = (360 - np.degrees(phi_input) + np.degrees(phi_inner)) % 360
    if phi_inner_difference > 180:
        phi_inner_difference -= 360
    
    print(f"  Step {i}: angle={hue_angle_inner:.1f}° -> hue={hue_inner:.2f}, code={code_inner}")
    print(f"    phi_diff={phi_inner_difference:.3f}°")
    
    phi_differences_data.append(phi_inner_difference)
    hue_angles_differences_data.append(i * (np.degrees(phi_input) - np.degrees(phi_current)))
    
    # Check if we've bracketed zero
    if len(phi_differences_data) >= 2:
        if (min(phi_differences_data) < 0 < max(phi_differences_data) or
            abs(min(phi_differences_data)) < 1e-6 or
            abs(max(phi_differences_data)) < 1e-6):
            print("  -> Found bracket around zero, can interpolate")
            break

# Interpolation
print(f"\nInterpolation data:")
print(f"  phi_differences: {[f'{d:.3f}' for d in phi_differences_data]}")
print(f"  hue_angle_diffs: {[f'{d:.3f}' for d in hue_angles_differences_data]}")

# The actual interpolation would find where phi_difference = 0
# This determines the hue angle adjustment needed