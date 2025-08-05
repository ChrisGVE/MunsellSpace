#!/usr/bin/env python3
"""Debug Rust's interpolation logic by simulating it in Python"""

import numpy as np

def python_style_interp(x_points, y_points, x_target):
    """Simulate np.interp behavior exactly"""
    # Sort by x
    sorted_indices = np.argsort(x_points)
    x_sorted = np.array(x_points)[sorted_indices]
    y_sorted = np.array(y_points)[sorted_indices]
    
    # Clamp to boundaries (no extrapolation)
    if x_target <= x_sorted[0]:
        return y_sorted[0]
    elif x_target >= x_sorted[-1]:
        return y_sorted[-1]
    
    # Find interpolation segment
    for i in range(len(x_sorted) - 1):
        if x_sorted[i] <= x_target <= x_sorted[i+1]:
            # Linear interpolation
            t = (x_target - x_sorted[i]) / (x_sorted[i+1] - x_sorted[i])
            return y_sorted[i] + t * (y_sorted[i+1] - y_sorted[i])
    
    # Should not reach here
    return y_sorted[-1]

# Test case from Python's trace for RGB [68,0,68]
print("Testing interpolation for RGB [68,0,68]:")
print("=" * 60)

# From Python's inner hue loop
phi_differences = [-7.458, -4.130, -0.077, 4.746]
hue_angle_diffs = [0.000, 7.458, 14.917, 22.375]

print(f"phi_differences: {phi_differences}")
print(f"hue_angle_diffs: {hue_angle_diffs}")

# Python's np.interp
result_np = np.interp(0.0, sorted(phi_differences), 
                      [y for x,y in sorted(zip(phi_differences, hue_angle_diffs))])
print(f"\nnp.interp(0.0, ...) = {result_np:.3f}")

# Our simulation
result_sim = python_style_interp(phi_differences, hue_angle_diffs, 0.0)
print(f"Simulated interp = {result_sim:.3f}")

# What does this mean for hue angle?
hue_angle_current = 273.84  # From initial guess
hue_angle_new = (hue_angle_current + result_np) % 360
print(f"\nNew hue angle: {hue_angle_current:.2f} + {result_np:.3f} = {hue_angle_new:.2f}°")

# Check boundary cases
print("\n" + "=" * 60)
print("Testing boundary behavior:")

# Test extrapolation (should clamp)
test_x = [-10, -8, -5, 0, 3, 5, 10]
for x in test_x:
    y = np.interp(x, sorted(phi_differences), 
                  [y for x,y in sorted(zip(phi_differences, hue_angle_diffs))])
    print(f"  np.interp({x:3}) = {y:.3f}")