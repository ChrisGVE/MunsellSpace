#!/usr/bin/env python3
"""Debug what happens at angle 288.8°"""

import numpy as np
from colour.notation.munsell import hue_angle_to_hue

# Test angle 288.8°
angle = 288.764

hue, code = hue_angle_to_hue(angle)
print(f"hue_angle_to_hue({angle:.3f}°):")
print(f"  hue = {hue:.3f}")
print(f"  code = {code}")

families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
            6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
print(f"  family = {families.get(int(code), '?')}")

# What about angle 288.8 exactly?
angle2 = 288.8
hue2, code2 = hue_angle_to_hue(angle2)
print(f"\nhue_angle_to_hue({angle2:.1f}°):")
print(f"  hue = {hue2:.3f}")
print(f"  code = {code2}")
print(f"  family = {families.get(int(code2), '?')}")

# Rust says angle 288.8° gives hue=0.628, code=8 (RP)
# Let's verify
print("\n" + "=" * 60)
print("Rust says angle 288.8° -> hue=0.628, code=8 (RP)")
print("Python says angle 288.8° -> hue={:.3f}, code={} ({})".format(
    hue2, int(code2), families.get(int(code2), '?')))