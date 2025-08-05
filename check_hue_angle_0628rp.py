#!/usr/bin/env python3
"""Check what hue angle 0.628RP should have"""

from colour.notation.munsell import hue_to_hue_angle
import numpy as np

# 0.628RP
hue = 0.628
code = 8  # RP

angle = hue_to_hue_angle(np.array([hue, code]))
print(f"hue_to_hue_angle({hue}, {code}) = {angle:.3f}°")

# Also check the boundaries
angle_10p = hue_to_hue_angle(np.array([10.0, 9]))  # 10P
angle_25rp = hue_to_hue_angle(np.array([2.5, 8]))  # 2.5RP

print(f"\nBoundaries:")
print(f"10P: {angle_10p:.3f}°")
print(f"2.5RP: {angle_25rp:.3f}°")

# The issue is that 0.628RP is very close to 0
# In Python, what happens with hue close to 0?
angle_0rp = hue_to_hue_angle(np.array([0.0, 8]))  # 0RP
print(f"0RP: {angle_0rp:.3f}°")

# What about 0.1RP?
angle_01rp = hue_to_hue_angle(np.array([0.1, 8]))  # 0.1RP
print(f"0.1RP: {angle_01rp:.3f}°")