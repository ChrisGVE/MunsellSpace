#!/usr/bin/env python3
"""Trace the EXACT Python loop from colour-science"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import (
    munsell_value, munsell_specification_to_xyY,
    hue_angle_to_hue, hue_to_hue_angle,
    maximum_chroma_from_renotation
)
from colour.algebra import cartesian_to_cylindrical
from colour.utilities import as_float_array

# Test RGB [68,0,68]
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

# First iteration - just the inner hue loop
chroma_maximum = maximum_chroma_from_renotation(
    np.array([hue_current, munsell_val, code_current])
)
if chroma_current > chroma_maximum:
    chroma_current = chroma_maximum

munsell_specification[0] = hue_current
munsell_specification[2] = chroma_current
munsell_specification[3] = code_current

x_current, y_current = munsell_specification_to_xyY(munsell_specification)[0:2]
rho_current, phi_current, _ = cartesian_to_cylindrical(
    np.array([x_current - x_center, y_current - y_center, Y])
)

phi_current_difference = (360 - np.degrees(phi_input) + np.degrees(phi_current)) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360

print(f"\nStarting inner hue loop:")
print(f"  phi_input={np.degrees(phi_input):.3f}°, phi_current={np.degrees(phi_current):.3f}°")
print(f"  phi_current_difference={phi_current_difference:.3f}°")

# The actual inner loop from Python
phi_differences_data = []
hue_angles_differences_data = []

if abs(phi_current_difference) >= 1e-6:
    phi_differences_data.append(phi_current_difference)
    hue_angles_differences_data.append(0)

hue_angle_current = hue_to_hue_angle(np.array([hue_current, code_current]))
extrapolate = False

# This is the EXACT loop condition from colour-science line 1151
iterations = 0
max_iterations = 10  # Just for this trace

# The loop continues while either:
# 1. All phi_differences have the same sign AND not extrapolating
# 2. Maximum iterations not reached
while (((all(d >= 0 for d in phi_differences_data) or
         all(d <= 0 for d in phi_differences_data)) and
        not extrapolate) and
       iterations < max_iterations):
    
    iterations += 1
    
    # Line 1167: Calculate test angle
    hue_angle_inner = (hue_angle_current + 
                      iterations * (np.degrees(phi_input) - np.degrees(phi_current))) % 360
    
    hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
    
    # Update specification for test
    munsell_specification[0] = hue_inner
    munsell_specification[3] = code_inner
    
    # Get xy for this test point
    x_inner, y_inner = munsell_specification_to_xyY(munsell_specification)[0:2]
    
    # Check if we should enable extrapolation (lines 1187-1188)
    # IMPORTANT: This happens AFTER getting xy but BEFORE storing results
    if len(phi_differences_data) >= 2:
        extrapolate = True
    
    # Only store results if not extrapolating (lines 1190-1201)
    if not extrapolate:
        rho_inner, phi_inner, _ = cartesian_to_cylindrical(
            np.array([x_inner - x_center, y_inner - y_center, Y])
        )
        
        phi_inner_difference = (360 - np.degrees(phi_input) + np.degrees(phi_inner)) % 360
        if phi_inner_difference > 180:
            phi_inner_difference -= 360
        
        phi_differences_data.append(phi_inner_difference)
        hue_angles_differences_data.append(
            iterations * (np.degrees(phi_input) - np.degrees(phi_current))
        )
        
        print(f"  Iteration {iterations}: angle={hue_angle_inner:.1f}° -> {hue_inner:.2f} (code={code_inner})")
        print(f"    phi_diff={phi_inner_difference:.3f}°")
    else:
        print(f"  Iteration {iterations}: extrapolating, not storing results")

print(f"\nCollected {len(phi_differences_data)} points")
print(f"phi_differences: {[f'{d:.3f}' for d in phi_differences_data]}")
print(f"hue_angle_diffs: {[f'{d:.3f}' for d in hue_angles_differences_data]}")