#!/usr/bin/env python3
"""Test what happens when hue angle wraps around 360 degrees."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour.notation.munsell import hue_to_hue_angle, hue_angle_to_hue

# Start with hue=9.8947, code=4 (GY)
hue1 = 9.8947
code1 = 4

print(f"Starting: hue={hue1:.4f}, code={code1} (GY)")

# Convert to angle
# Python's hue_to_hue_angle takes [hue, code]
angle1 = hue_to_hue_angle([hue1, code1])
print(f"Hue angle: {angle1:.4f}°")

# Simulate a small adjustment that might wrap
adjustments = [-5, -2, -1, -0.5, 0, 0.5, 1, 2, 5]

print("\nTesting small angle adjustments:")
print("=" * 60)

for adj in adjustments:
    new_angle = angle1 + adj
    
    # Handle wrapping manually like Rust might
    if new_angle < 0:
        new_angle += 360
    elif new_angle >= 360:
        new_angle -= 360
    
    hue_new, code_new = hue_angle_to_hue(new_angle)
    
    families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}
    
    print(f"Angle {angle1:.2f}° + {adj:+.1f}° = {new_angle:.2f}° → hue={hue_new:.4f}, code={code_new} ({families[code_new]})")

print("\n" + "=" * 60)
print("HYPOTHESIS:")
print("When hue is near 10.0 in GY family (code=4),")
print("the angle is near 135° (the GY/G boundary).")
print("A small negative adjustment crosses into G family (code=3).")
print("But the hue value wraps incorrectly from ~10 to ~0.")