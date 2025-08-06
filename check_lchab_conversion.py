#!/usr/bin/env python3
"""Check how Python converts LCHab to Munsell"""

import numpy as np

# Our LCHab values
L = 87.7347126826
C = 124.2733082965
H = 136.3570439856

print(f"LCHab: [{L:.3f}, {C:.3f}, {H:.3f}]")

# From Python colour-science source, the conversion is:
# 1. Adjust hue angle
hue_angle_adjusted = (H + 18) % 360  # Note: it's +18, not -18!
print(f"\nAdjusted hue angle: {hue_angle_adjusted:.3f}°")

# 2. Convert to Munsell hue
import math
code = (17 - math.floor((hue_angle_adjusted - 18) % 360 / 36)) % 10 + 1
hue = 10 - ((hue_angle_adjusted - 18) % 360 % 36) * 10 / 36
print(f"Munsell hue: {hue:.3f}")
print(f"Munsell code: {code}")

families = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
print(f"Family: {families[code-1]}")

# 3. Convert value
# Simplified approximation
value = L / 10
print(f"\nMunsell value (approx): {value:.3f}")

# 4. Convert chroma  
# Very rough approximation
chroma = C / 5
print(f"Munsell chroma (approx): {chroma:.3f}")

print(f"\nExpected initial spec: [{hue:.3f}, {value:.3f}, {chroma:.3f}, {code}]")
print(f"Rust gets: [7.877, 8.773, 24.855, 4]")

# Let's check what hue angle gives code 4 (GY)
print("\n=== Checking hue angle ranges ===")
for test_h in [100, 110, 120, 130, 136.357, 140, 150, 160]:
    adjusted = (test_h + 18) % 360
    test_code = (17 - math.floor((adjusted - 18) % 360 / 36)) % 10 + 1
    test_hue = 10 - ((adjusted - 18) % 360 % 36) * 10 / 36
    print(f"H={test_h:7.3f}° -> adjusted={adjusted:7.3f}° -> code={test_code} ({families[test_code-1]:2}) hue={test_hue:.3f}")