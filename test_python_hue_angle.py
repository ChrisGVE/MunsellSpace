#!/usr/bin/env python3
"""Test Python's hue_angle_to_hue behavior"""

import numpy as np
from colour.notation.munsell import hue_angle_to_hue

# Test various angles, especially around GY/Y boundary
test_angles = [
    133.0,  # Around GY/Y boundary
    134.0,
    135.0,  # Exact boundary
    136.0,
    160.0,  # Y range
]

print("Python hue_angle_to_hue:")
print("="*60)

families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
           6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}

for angle in test_angles:
    hue, code = hue_angle_to_hue(angle)
    family = families.get(code, '?')
    print(f"  {angle:5.1f}° -> hue={hue:6.3f}, code={code:2} ({hue:.1f}{family})")