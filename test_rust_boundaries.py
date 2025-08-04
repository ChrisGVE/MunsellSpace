#!/usr/bin/env python3
"""Test what our Rust code should be doing at boundaries"""

# From Python, we know:
# 0.7RP -> 289.2° 
# 10.0P -> 285.0°

# Our Rust reverse interpolation from angle to single_hue
def reverse_interpolate_hue_angle(hue_angle):
    """Simulate Rust's reverse interpolation"""
    angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0]
    breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0]
    
    for i in range(len(angles)-1):
        if angles[i] <= hue_angle <= angles[i+1]:
            t = (hue_angle - angles[i]) / (angles[i+1] - angles[i])
            return breakpoints[i] + t * (breakpoints[i+1] - breakpoints[i])
    
    return 0.0

# Test problematic angles
test_angles = [285.0, 289.2, 290.0, 310.0, 314.0, 315.0]

print("Testing angle -> single_hue -> code mapping:")
print("=" * 60)

for angle in test_angles:
    single_hue = reverse_interpolate_hue_angle(angle)
    
    # Apply Rust's code determination logic
    if single_hue <= 0.5:
        code = 7  # R
    elif single_hue <= 1.5:
        code = 6  # YR
    elif single_hue <= 2.5:
        code = 5  # Y
    elif single_hue <= 3.5:
        code = 4  # GY
    elif single_hue <= 4.5:
        code = 3  # G
    elif single_hue <= 5.5:
        code = 2  # BG
    elif single_hue <= 6.5:
        code = 1  # B
    elif single_hue <= 7.5:
        code = 10  # PB
    elif single_hue <= 8.5:
        code = 9  # P
    elif single_hue <= 9.5:
        code = 8  # RP
    else:
        code = 7  # R (wraparound)
    
    families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
                6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
    family = families.get(code, '?')
    
    # Calculate hue from single_hue
    hue = (10.0 * (single_hue % 1.0) + 5.0) % 10.0
    if hue == 0.0:
        hue = 10.0
    
    print(f"  {angle:6.1f}° -> single_hue={single_hue:5.3f} -> code={code:2} ({family:2}) -> {hue:4.1f}{family}")

print("\n" + "=" * 60)
print("PROBLEM IDENTIFIED:")
print("=" * 60)
print("289.2° (should be 0.7RP) gives single_hue=8.276")
print("This maps to code=9 (P) instead of code=8 (RP)")
print("Because 8.276 <= 8.5 so it's classified as P")
print("\nThe boundary at single_hue=8.5 is WRONG!")
print("It should probably be around 8.0 or 8.25")

# Check Python's exact mapping
print("\n" + "=" * 60)
print("Testing Python's exact mappings:")
print("=" * 60)

import subprocess
test_script = """
import numpy as np
from colour.notation.munsell import hue_angle_to_hue

# Find the exact boundary angle between P and RP
angles = np.linspace(285, 290, 50)
for angle in angles:
    hue, code = hue_angle_to_hue(angle)
    if angle == 285.0 or angle == 290.0 or abs(angle - 287.5) < 0.1:
        families = {8: 'RP', 9: 'P'}
        print(f"  {angle:.2f}° -> code={code:.0f} ({families.get(int(code), '?')})")
"""

with open('test_exact.py', 'w') as f:
    f.write(test_script)

result = subprocess.run(
    ['./venv_comparison/bin/python', 'test_exact.py'],
    capture_output=True,
    text=True
)
print(result.stdout)

import os
os.remove('test_exact.py')