"""Trace what Python does when phi_input ≈ phi_current"""

import numpy as np
from colour.algebra import LinearInterpolator, Extrapolator

# Simulate the stuck case
phi_input = -7.066
phi_current = -7.066  # Nearly equal

# Initial phi difference
phi_current_difference = (360 - phi_input + phi_current) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360
print(f"Initial phi_current_difference: {phi_current_difference}")

# Simulate inner loop
phi_differences_data = [phi_current_difference]  # Start with initial
hue_angles_differences_data = [0.0]

# Iteration 1
iterations_inner = 1
step = iterations_inner * (phi_input - phi_current)  # This is 0!
print(f"\nIteration {iterations_inner}: step = {step}")

# Since step is 0, hue_angle_inner will be the same as hue_angle_current
# This means phi_inner will also be approximately phi_current
# So phi_inner_difference will be approximately the same as phi_current_difference

# Let's say we get the same phi difference
phi_inner_difference = phi_current_difference  # approximately
hue_angle_difference_inner = 0.0  # Since step was 0

phi_differences_data.append(phi_inner_difference)
hue_angles_differences_data.append(hue_angle_difference_inner)

print(f"After iteration 1:")
print(f"  phi_differences_data: {phi_differences_data}")
print(f"  hue_angles_differences_data: {hue_angles_differences_data}")

# Now Python extrapolates
phi_differences = np.array(phi_differences_data)
hue_angles_differences = np.array(hue_angles_differences_data)

# Sort by phi differences
indices = phi_differences.argsort()
sorted_phi = phi_differences[indices]
sorted_hue = hue_angles_differences[indices]

print(f"\nSorted data:")
print(f"  phi: {sorted_phi}")
print(f"  hue: {sorted_hue}")

# This is the key issue!
# Both phi differences are approximately 0
# Both hue angle differences are 0
# When we try to interpolate/extrapolate to find where phi=0, we get 0/0

# Python's LinearInterpolator/Extrapolator behavior:
try:
    interpolator = LinearInterpolator(sorted_phi, sorted_hue)
    extrapolator = Extrapolator(interpolator)
    result = extrapolator(0.0)
    print(f"\nExtrapolator(0.0) = {result}")
except Exception as e:
    print(f"\nError: {e}")

# Test with actual different values
print("\n--- Testing with slightly different values ---")
phi_diffs = [0.001, 0.001]  # Nearly the same
hue_diffs = [0.0, 0.0]  # Both zero

try:
    interpolator = LinearInterpolator(phi_diffs, hue_diffs)
    extrapolator = Extrapolator(interpolator)
    result = extrapolator(0.0)
    print(f"Extrapolator(0.0) = {result}")
except Exception as e:
    print(f"Error: {e}")