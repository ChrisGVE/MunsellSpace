#!/usr/bin/env python3
"""Test hue_angle_to_hue directly"""

from colour.notation.munsell import hue_angle_to_hue

# Test the angles that are causing issues
test_angles = [
    0, 30, 45, 60, 70, 90, 120, 135, 150, 
    160, 180, 210, 225, 240, 255, 270, 300, 315, 330, 360
]

print("Python's hue_angle_to_hue results:")
print("=" * 60)
for angle in test_angles:
    hue, code = hue_angle_to_hue(angle)
    HUE_CODES = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
                 6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
    print(f"Angle {angle:3d}° -> Hue {hue:.1f}, Code {int(code)} ({HUE_CODES[int(code)]})")