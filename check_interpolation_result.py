#!/usr/bin/env python3
"""Check what the interpolation should give"""

import numpy as np

# From our Rust output:
phi_differences = [-7.462, -4.131, 7.254]
hue_angle_diffs = [0.0, 7.462, 14.924]

print("Rust collected points:")
print(f"phi_differences: {phi_differences}")
print(f"hue_angle_diffs: {hue_angle_diffs}")

# Interpolate to find where phi_diff = 0
result = np.interp(0.0, sorted(phi_differences), 
                  [y for x,y in sorted(zip(phi_differences, hue_angle_diffs))])
print(f"\nnp.interp(0.0, ...) = {result:.3f}")

# What angle does this give?
hue_angle_current = 273.84
hue_angle_new = (hue_angle_current + result) % 360
print(f"New angle: {hue_angle_current:.2f} + {result:.3f} = {hue_angle_new:.2f}°")

# But wait, Python gets 4 points, not 3!
print("\n" + "=" * 60)
print("Python collected 4 points:")
phi_differences_py = [-7.458, -4.130, -0.077, 4.746]
hue_angle_diffs_py = [0.000, 7.458, 14.917, 22.375]

print(f"phi_differences: {phi_differences_py}")
print(f"hue_angle_diffs: {hue_angle_diffs_py}")

result_py = np.interp(0.0, sorted(phi_differences_py), 
                     [y for x,y in sorted(zip(phi_differences_py, hue_angle_diffs_py))])
print(f"\nnp.interp(0.0, ...) = {result_py:.3f}")

hue_angle_new_py = (hue_angle_current + result_py) % 360
print(f"New angle: {hue_angle_current:.2f} + {result_py:.3f} = {hue_angle_new_py:.2f}°")

print("\nDifference: Rust gets {:.2f}° vs Python {:.2f}°".format(hue_angle_new, hue_angle_new_py))