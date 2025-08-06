#!/usr/bin/env python3
"""Debug why hue angle refinement isn't working"""

import numpy as np
from colour.notation.munsell import hue_angle_to_hue, hue_to_hue_angle

# Test our specific case
hue_current = 5.0
code_current = 7
hue_angle_current = hue_to_hue_angle([hue_current, code_current])
print(f"Current: hue={hue_current}, code={code_current}, hue_angle={hue_angle_current}")

# Test what happens when we adjust the angle
phi_input = 2.402
phi_current = -1.557
angle_diff = phi_input - phi_current
print(f"\nAngle adjustment: phi_input={phi_input:.3f}, phi_current={phi_current:.3f}, diff={angle_diff:.3f}")

for i in range(1, 5):
    hue_angle_inner = (hue_angle_current + i * angle_diff) % 360
    hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
    print(f"\nStep {i}: angle={hue_angle_inner:.3f}")
    print(f"  Result: hue={hue_inner:.3f}, code={code_inner}")

# Test with a different starting point
print("\n\n=== Test with different starting point ===")
hue_current = 1.671
code_current = 6
hue_angle_current = hue_to_hue_angle([hue_current, code_current])
print(f"Current: hue={hue_current}, code={code_current}, hue_angle={hue_angle_current}")

phi_current = 13.422
angle_diff = phi_input - phi_current
print(f"\nAngle adjustment: phi_input={phi_input:.3f}, phi_current={phi_current:.3f}, diff={angle_diff:.3f}")

for i in range(1, 5):
    hue_angle_inner = (hue_angle_current + i * angle_diff) % 360
    hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
    print(f"\nStep {i}: angle={hue_angle_inner:.3f}")
    print(f"  Result: hue={hue_inner:.3f}, code={code_inner}")