#!/usr/bin/env python3
"""Examine how Python handles the extrapolation when angles are very close."""

import numpy as np
from colour.algebra import LinearInterpolator, Extrapolator

# Simulate the case where phi_input and phi_current are very close
phi_input = 2.402  # degrees
phi_current = 2.402  # degrees

print("Case 1: phi_input == phi_current")
print(f"  phi_input = {phi_input:.6f}°")
print(f"  phi_current = {phi_current:.6f}°")
print(f"  difference = {phi_input - phi_current:.12e}°")

# Let's see what Python does with extrapolation
# Simulating the inner loop data collection
phi_differences = [-8.443e-7, 6.186e-6]  # From our trace
hue_angles_differences = [-6.186e-6, 0.0]

print("\nExtrapolation data:")
print(f"  phi_differences = {phi_differences}")
print(f"  hue_angles_differences = {hue_angles_differences}")

# Create extrapolator
interpolator = LinearInterpolator(phi_differences, hue_angles_differences)
extrapolator = Extrapolator(interpolator)

# Extrapolate to phi_diff = 0
result = extrapolator(0)
print(f"\nExtrapolation result at phi_diff=0: {result:.12e}")

# Let's check a more typical case
print("\n\nCase 2: Normal convergence")
phi_differences_normal = [-0.844, 0.079]
hue_angles_normal = [0.0, 0.844]

interpolator_normal = LinearInterpolator(phi_differences_normal, hue_angles_normal)
extrapolator_normal = Extrapolator(interpolator_normal)
result_normal = extrapolator_normal(0)
print(f"  phi_differences = {phi_differences_normal}")
print(f"  hue_angles_differences = {hue_angles_normal}")
print(f"  Extrapolation at 0: {result_normal:.6f}")

# Check if there's special handling for very small differences
print("\n\nCase 3: Very small differences")
tiny_diff = 1e-10
phi_differences_tiny = [-tiny_diff, tiny_diff]
hue_angles_tiny = [-tiny_diff, 0.0]

interpolator_tiny = LinearInterpolator(phi_differences_tiny, hue_angles_tiny)
extrapolator_tiny = Extrapolator(interpolator_tiny)
result_tiny = extrapolator_tiny(0)
print(f"  phi_differences = {phi_differences_tiny}")
print(f"  hue_angles_differences = {hue_angles_tiny}")
print(f"  Extrapolation at 0: {result_tiny:.12e}")

# What happens with just one point?
print("\n\nCase 4: Single point extrapolation")
try:
    interpolator_single = LinearInterpolator([0.5], [1.0])
    extrapolator_single = Extrapolator(interpolator_single)
    result_single = extrapolator_single(0)
    print(f"  Works! Result: {result_single}")
except Exception as e:
    print(f"  Error: {e}")

# Test what happens when we have multiple very similar points
print("\n\nCase 5: Multiple similar points")
phi_diffs_similar = [-0.000001, 0.0, 0.000001, 0.000002]
hue_diffs_similar = [-0.000001, 0.0, 0.000001, 0.000002]

interpolator_similar = LinearInterpolator(phi_diffs_similar, hue_diffs_similar)
extrapolator_similar = Extrapolator(interpolator_similar)
result_similar = extrapolator_similar(0)
print(f"  Result at 0: {result_similar:.12e}")