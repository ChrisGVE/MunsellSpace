#!/usr/bin/env python3
"""Find the exact P/RP boundary in Python"""

import numpy as np
from colour.notation.munsell import hue_angle_to_hue

# Binary search for the boundary
left, right = 285.0, 290.0
epsilon = 0.001

while right - left > epsilon:
    mid = (left + right) / 2
    hue, code = hue_angle_to_hue(mid)
    
    if int(code) == 9:  # P
        left = mid
    else:  # RP (code 8)
        right = mid

boundary = (left + right) / 2
print(f"P/RP boundary is at approximately {boundary:.3f}°")

# Test around the boundary
test_angles = [boundary - 0.1, boundary - 0.01, boundary, boundary + 0.01, boundary + 0.1]
print(f"\nTesting around boundary:")
for angle in test_angles:
    hue, code = hue_angle_to_hue(angle)
    families = {8: 'RP', 9: 'P'}
    print(f"  {angle:.3f}° -> code={int(code)} ({families.get(int(code), '?')})")

# Now find what single_hue this corresponds to
print(f"\nFinding single_hue at boundary angle {boundary:.3f}°:")

# Simulate reverse interpolation
angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0]
breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0]

for i in range(len(angles)-1):
    if angles[i] <= boundary <= angles[i+1]:
        t = (boundary - angles[i]) / (angles[i+1] - angles[i])
        single_hue = breakpoints[i] + t * (breakpoints[i+1] - breakpoints[i])
        print(f"  Boundary angle {boundary:.3f}° -> single_hue = {single_hue:.4f}")
        print(f"  (interpolated between angles[{i}]={angles[i]} and angles[{i+1}]={angles[i+1]})")
        print(f"   with breakpoints[{i}]={breakpoints[i]} and breakpoints[{i+1}]={breakpoints[i+1]})")
        break

print(f"\nRECOMMENDATION:")
print(f"Change the P/RP boundary from 'single_hue <= 8.5' to 'single_hue < {single_hue:.3f}'")