#!/usr/bin/env python3
"""Debug Python's full xyY_to_munsell_specification algorithm"""

import numpy as np
from colour.notation.munsell import (
    _xyY_to_munsell_specification,
    munsell_value_ASTMD1535,
    _munsell_specification_to_xyY,
    hue_to_hue_angle,
    hue_angle_to_hue,
    maximum_chroma_from_renotation,
    LCHab_to_munsell_specification
)
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab, XYZ_to_xy
from colour.algebra import cartesian_to_cylindrical, euclidean_distance
from colour.utilities import as_float_array, to_domain_1, domain_range_scale

# Test red color
xyy = np.array([0.640000, 0.330000, 0.212673])
x, y, Y = xyy[0], xyy[1], to_domain_1(xyy[2])

print(f"Testing red xyY: [{x}, {y}, {Y}]")

# Get value
with domain_range_scale("ignore"):
    value = munsell_value_ASTMD1535(Y * 100)
print(f"Value: {value}")

# Get center point
with domain_range_scale("ignore"):
    x_center, y_center, Y_center = _munsell_specification_to_xyY(value)
print(f"Center: x={x_center}, y={y_center}")

# Get input rho and phi
rho_input, phi_input, _ = cartesian_to_cylindrical([x - x_center, y - y_center, Y_center])
phi_input = np.degrees(phi_input)
print(f"Input: rho={rho_input:.6f}, phi={phi_input:.3f}")

# Initial guess from Lab
XYZ = xyY_to_XYZ(xyy)
x_i, y_i = 0.31006, 0.31616  # Illuminant C
X_r, Y_r, Z_r = xyY_to_XYZ([x_i, y_i, Y])
XYZ_r = np.array([(1 / Y_r) * X_r, 1, (1 / Y_r) * Z_r])
Lab = XYZ_to_Lab(XYZ, XYZ_to_xy(XYZ_r))
LCHab = Lab_to_LCHab(Lab)
hue_initial, _, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)

specification_current = [
    hue_initial,
    value,
    (5 / 5.5) * chroma_initial,
    code_initial,
]

print(f"\nInitial spec: hue={hue_initial:.3f}, value={value:.3f}, chroma={(5/5.5)*chroma_initial:.3f}, code={code_initial}")

# First iteration
iterations = 1
convergence_threshold = 1e-6 / 1e4

print(f"\n=== Iteration {iterations} ===")

# Get current hue angle
hue_current, _, chroma_current, code_current = specification_current
hue_angle_current = hue_to_hue_angle([hue_current, code_current])
print(f"Current hue angle: {hue_angle_current}")

# Check chroma maximum
chroma_maximum = maximum_chroma_from_renotation([hue_current, value, code_current])
print(f"Chroma maximum: {chroma_maximum}, current: {chroma_current}")

if chroma_current > chroma_maximum:
    chroma_current = specification_current[2] = chroma_maximum
    print(f"Clamped chroma to maximum: {chroma_current}")

# Get current position
with domain_range_scale("ignore"):
    x_current, y_current, _ = _munsell_specification_to_xyY(specification_current)

rho_current, phi_current, _ = cartesian_to_cylindrical(
    [x_current - x_center, y_current - y_center, Y_center]
)
phi_current = np.degrees(phi_current)

print(f"Current position: x={x_current:.6f}, y={y_current:.6f}")
print(f"Current polar: rho={rho_current:.6f}, phi={phi_current:.3f}")

# Phi difference
phi_current_difference = (360 - phi_input + phi_current) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360
print(f"Phi difference: {phi_current_difference:.3f}")

# Inner hue angle loop
phi_differences_data = [phi_current_difference]
hue_angles_differences_data = [0]
hue_angles = [hue_angle_current]

print("\nInner hue angle loop:")
for i in range(1, 4):  # Just a few iterations
    hue_angle_inner = (hue_angle_current + i * (phi_input - phi_current)) % 360
    hue_angle_difference_inner = (i * (phi_input - phi_current)) % 360
    if hue_angle_difference_inner > 180:
        hue_angle_difference_inner -= 360
    
    hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
    
    print(f"  Step {i}: hue_angle={hue_angle_inner:.3f}, hue={hue_inner:.3f}, code={code_inner}")
    
    with domain_range_scale("ignore"):
        x_inner, y_inner, _ = _munsell_specification_to_xyY([
            hue_inner, value, chroma_current, code_inner
        ])
    
    rho_inner, phi_inner, _ = cartesian_to_cylindrical(
        [x_inner - x_center, y_inner - y_center, Y_center]
    )
    phi_inner = np.degrees(phi_inner)
    
    phi_inner_difference = (360 - phi_input + phi_inner) % 360
    if phi_inner_difference > 180:
        phi_inner_difference -= 360
    
    print(f"    Position: x={x_inner:.6f}, y={y_inner:.6f}")
    print(f"    Polar: rho={rho_inner:.6f}, phi={phi_inner:.3f}, phi_diff={phi_inner_difference:.3f}")
    
    phi_differences_data.append(phi_inner_difference)
    hue_angles.append(hue_angle_inner)
    hue_angles_differences_data.append(hue_angle_difference_inner)
    
    # Check if we should stop
    if np.sign(np.min(phi_differences_data)) != np.sign(np.max(phi_differences_data)):
        print(f"    Signs differ - ready to interpolate")
        break

print(f"\nPhi differences: {phi_differences_data}")
print(f"Hue angle differences: {hue_angles_differences_data}")