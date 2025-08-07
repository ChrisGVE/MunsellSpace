#!/usr/bin/env python3
"""Check Python's actual hue_angle_to_hue implementation"""

import inspect
from colour.notation.munsell import hue_angle_to_hue

# Get the source code
source = inspect.getsource(hue_angle_to_hue)
print("Python's hue_angle_to_hue implementation:")
print("=" * 60)
print(source)
print("=" * 60)

# Test some angles
test_angles = [0, 45, 90, 135, 180, 225, 270, 315, 360]
print("\nTest results:")
for angle in test_angles:
    hue, code = hue_angle_to_hue(angle)
    print(f"  Angle {angle:3d}° -> Hue {hue:.1f}, Code {code}")