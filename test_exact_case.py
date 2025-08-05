"""Test the exact case that's getting stuck"""
import numpy as np
from colour.algebra import LinearInterpolator, Extrapolator

# From iteration 2 in our debug output
# We have hue_angle_current = 356.1 degrees
# phi_input = -7.066 degrees, phi_current = probably close to 0

# When phi_input == phi_current (or very close), the inner loop collects:
# - phi_differences_data[0] = phi_current_difference 
# - phi_differences_data[1] = result of iteration 1

# The key issue: when phi_input ≈ phi_current, the step is ≈ 0
# This means all iterations test roughly the same angle!

# Let's simulate this
hue_angle_current = 356.1
phi_input = -7.066
phi_current = -7.066  # If they're equal after convergence

# Step calculation from Python
step_1 = 1 * (phi_input - phi_current)
step_2 = 2 * (phi_input - phi_current)

print(f"hue_angle_current: {hue_angle_current}")
print(f"phi_input: {phi_input}, phi_current: {phi_current}")
print(f"Step 1: {step_1}")
print(f"Step 2: {step_2}")
print(f"This means all inner loop iterations test the SAME angle!")

# This is why we get stuck - the algorithm can't make progress
# when phi_input == phi_current