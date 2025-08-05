#!/usr/bin/env python3
"""Test single_hue calculation for 0.628RP"""

# For 0.628RP, code=8
hue = 0.628
code = 8

# Rust's calculation (wrong, uses 18):
single_hue_rust = ((18.0 - code) % 10.0 + (hue / 10.0) - 0.5) % 10.0
print(f"Rust (wrong, uses 18): single_hue = {single_hue_rust:.3f}")

# Should use 17 like Python:
single_hue_python = ((17.0 - code) % 10.0 + (hue / 10.0) - 0.5) % 10.0
print(f"Python (uses 17): single_hue = {single_hue_python:.3f}")

# What angle would each give?
# Using Python's breakpoints: [0, 2, 3, 4, 5, 6, 8, 9, 10]
# Using Python's angles:      [0, 45, 70, 135, 160, 225, 255, 315, 360]

def interpolate_angle(single_hue):
    breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0]
    angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0]
    
    for i in range(len(breakpoints) - 1):
        if breakpoints[i] <= single_hue <= breakpoints[i+1]:
            t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i])
            return angles[i] + t * (angles[i+1] - angles[i])
    return 360.0

angle_rust = interpolate_angle(single_hue_rust)
angle_python = interpolate_angle(single_hue_python)

print(f"\nAngle from Rust single_hue: {angle_rust:.3f}°")
print(f"Angle from Python single_hue: {angle_python:.3f}°")
print(f"Python expects: 288.768°")