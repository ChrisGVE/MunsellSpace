#!/usr/bin/env python3
"""Test hue angle to hue conversion at boundaries."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import hue_angle_to_hue

# Test angles near 0°/360° boundary
test_angles = [
    359.9,
    359.99,
    359.999,
    0.0,
    0.001,
    0.01,
    0.1,
    # Specific angles from our problem colors
    359.654,  # Might be from GY→G transition
    0.346,    # Might be from GY→G transition
]

print("Testing hue_angle_to_hue near 0°/360° boundary:")
print("=" * 60)

for angle in test_angles:
    result = hue_angle_to_hue(angle)
    hue = result[0]
    code = result[1]
    
    # Map code to family name
    families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}
    family = families.get(code, '?')
    
    print(f"Angle {angle:7.3f}° → hue={hue:6.3f}, code={code:2} ({family})")
    
    # Calculate what single_hue would be
    # LinearInterpolator([0, 45, 70, 135, 160, 225, 255, 315, 360], [0, 2, 3, 4, 5, 6, 8, 9, 10])
    angles_interp = [0, 45, 70, 135, 160, 225, 255, 315, 360]
    values_interp = [0, 2, 3, 4, 5, 6, 8, 9, 10]
    
    for i in range(len(angles_interp)-1):
        if angles_interp[i] <= angle <= angles_interp[i+1]:
            t = (angle - angles_interp[i]) / (angles_interp[i+1] - angles_interp[i])
            single_hue = values_interp[i] + t * (values_interp[i+1] - values_interp[i])
            print(f"  → single_hue = {single_hue:.6f}")
            break

print("\n" + "=" * 60)
print("CRITICAL OBSERVATION:")
print("At angle ≈ 0°, single_hue ≈ 0.0, which maps to code 7 (R)")
print("At angle ≈ 360°, single_hue ≈ 10.0, which maps to code 7 (R)")
print("The boundary between 359.9° and 0.1° should stay in R family!")
print("But floating-point errors might cause jumps.")