#!/usr/bin/env python3
"""Trace the exact interpolation and results"""

import numpy as np

# From our trace, Python found these points:
phi_differences = [-7.458, -4.130, -0.077, 4.746]
hue_angle_diffs = [0.000, 7.458, 14.917, 22.375]

print("Interpolation to find hue_angle_difference where phi_difference = 0:")
print("=" * 70)
print(f"phi_differences: {phi_differences}")
print(f"hue_angle_diffs: {hue_angle_diffs}")

# Sort by phi_differences (Python lines 1206-1209)
sorted_indices = np.argsort(phi_differences)
phi_sorted = np.array(phi_differences)[sorted_indices]
hue_sorted = np.array(hue_angle_diffs)[sorted_indices]

print(f"\nSorted by phi:")
print(f"phi_sorted: {phi_sorted}")
print(f"hue_sorted: {hue_sorted}")

# Interpolate to find hue_angle_diff at phi_diff = 0
result = np.interp(0.0, phi_sorted, hue_sorted)
print(f"\nnp.interp(0.0, phi_sorted, hue_sorted) = {result:.3f}")

# This means we need to adjust the hue angle by this amount
hue_angle_current = 273.84  # From initial guess
hue_angle_new = (hue_angle_current + result) % 360
print(f"\nNew hue angle: {hue_angle_current:.2f} + {result:.3f} = {hue_angle_new:.2f}°")

# Convert back to hue
from colour.notation.munsell import hue_angle_to_hue
hue_new, code_new = hue_angle_to_hue(hue_angle_new)
families = {8: 'RP', 9: 'P'}
print(f"hue_angle_to_hue({hue_angle_new:.2f}) -> {hue_new:.2f}{families.get(int(code_new), '?')}")

# Now test the chroma refinement
print("\n" + "=" * 70)
print("Chroma refinement:")
print("=" * 70)

# From our initial state
rho_input = 0.162369
rho_current = 0.164485  # After hue adjustment, this changes

print(f"rho_input = {rho_input:.6f}")
print(f"rho_current = {rho_current:.6f}")

# The chroma loop uses exponential scaling
# Python line 1278: chroma_inner = (rho_input / rho_current) ** i * chroma_current
chroma_current = 8.118

for i in range(1, 4):
    ratio = rho_input / rho_current
    chroma_inner = ratio ** i * chroma_current
    print(f"  Step {i}: ratio^{i} * {chroma_current:.3f} = {ratio**i:.3f} * {chroma_current:.3f} = {chroma_inner:.3f}")

# The actual loop collects multiple rho values and interpolates
# to find the chroma that gives rho = rho_input