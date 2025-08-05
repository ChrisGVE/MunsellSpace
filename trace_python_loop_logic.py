#!/usr/bin/env python3
"""Trace Python's exact inner hue loop logic"""

import numpy as np

# Simulate Python's inner hue loop logic
phi_input = -86.158  # degrees
phi_current = 266.380  # degrees
hue_angle_current = 273.84  # degrees

phi_differences_data = []
hue_angles_differences_data = []

# Initial phi difference
phi_current_difference = (360 - phi_input + phi_current) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360

print(f"Initial: phi_current_difference = {phi_current_difference:.3f}°")

# Include initial point if not essentially zero
if abs(phi_current_difference) >= 1e-6:
    phi_differences_data.append(phi_current_difference)
    hue_angles_differences_data.append(0.0)
    print(f"  Added initial point: phi_diff={phi_current_difference:.3f}, hue_diff=0.0")

extrapolate = False
iterations_inner = 0

# Python's loop condition (lines 1151-1204)
# Continue while all have same sign AND not extrapolating
while ((all(d >= 0 for d in phi_differences_data) or 
        all(d <= 0 for d in phi_differences_data)) and 
       not extrapolate):
    
    iterations_inner += 1
    if iterations_inner > 20:  # Safety limit
        print("  Max iterations reached")
        break
    
    # Step calculation (Python line 1167)
    step = iterations_inner * (phi_input - phi_current)
    hue_angle_inner = (hue_angle_current + step) % 360
    
    # Normalize step to [-180, 180]
    step_mod = step % 360
    if step_mod > 180:
        hue_angle_difference_inner = step_mod - 360
    else:
        hue_angle_difference_inner = step_mod
    
    print(f"\nIteration {iterations_inner}:")
    print(f"  step = {iterations_inner} * ({phi_input:.3f} - {phi_current:.3f}) = {step:.3f}")
    print(f"  hue_angle_inner = ({hue_angle_current:.3f} + {step:.3f}) % 360 = {hue_angle_inner:.3f}")
    print(f"  hue_angle_difference_inner = {hue_angle_difference_inner:.3f}")
    
    # Check if we should enable extrapolation (Python lines 1187-1188)
    if len(phi_differences_data) >= 2:
        extrapolate = True
        print("  -> Extrapolation enabled (have 2+ points)")
    
    # If not extrapolating, we would calculate phi_inner here
    # For this simulation, using known values from trace
    if not extrapolate:
        # These phi_differences come from our trace
        phi_diffs_from_trace = [-7.458, -4.130, -0.077, 4.746]
        if iterations_inner <= len(phi_diffs_from_trace):
            phi_inner_difference = phi_diffs_from_trace[iterations_inner - 1]
            phi_differences_data.append(phi_inner_difference)
            hue_angles_differences_data.append(hue_angle_difference_inner)
            print(f"  -> Added point: phi_diff={phi_inner_difference:.3f}, hue_diff={hue_angle_difference_inner:.3f}")

print(f"\nLoop ended after {iterations_inner} iterations")
print(f"Collected {len(phi_differences_data)} points:")
print(f"  phi_differences: {phi_differences_data}")
print(f"  hue_angle_diffs: {hue_angles_differences_data}")

# Now check if Python would continue or stop
if all(d >= 0 for d in phi_differences_data):
    print("\nAll phi_differences >= 0 - would continue if not extrapolating")
elif all(d <= 0 for d in phi_differences_data):
    print("\nAll phi_differences <= 0 - would continue if not extrapolating")
else:
    print("\nPhi_differences have mixed signs - would stop loop")