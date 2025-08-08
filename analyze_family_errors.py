#!/usr/bin/env python3
"""Analyze wrong family assignments"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ

# Test colors that might have family issues
# Including colors near family boundaries
test_colors = [
    # Near R/YR boundary (~2.5R to 2.5YR)
    ([255, 100, 100], "Near R/YR"),
    ([255, 150, 100], "Near R/YR"),
    
    # Near B/PB boundary (~2.5B to 2.5PB)
    ([100, 100, 255], "Near B/PB"),
    ([150, 100, 255], "Near B/PB"),
    
    # Near G/BG boundary
    ([100, 200, 150], "Near G/BG"),
    
    # Known problematic PB colors
    ([100, 50, 150], "PB region"),
    ([120, 80, 180], "PB region"),
]

print("Analyzing Family Assignment Issues")
print("="*60)

hue_families = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}

# Family boundaries (hue angles)
# Based on Python's implementation
family_boundaries = {
    'R':  (0, 36),    # 0-36 degrees
    'YR': (36, 72),   # 36-72 degrees
    'Y':  (72, 108),  # etc...
    'GY': (108, 144),
    'G':  (144, 180),
    'BG': (180, 216),
    'B':  (216, 252),
    'PB': (252, 288),
    'P':  (288, 324),
    'RP': (324, 360),
}

for rgb_vals, description in test_colors:
    rgb = np.array(rgb_vals) / 255.0
    xyz = sRGB_to_XYZ(rgb)
    total = xyz[0] + xyz[1] + xyz[2]
    xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
    
    # Get Python's result
    spec = munsell.xyY_to_munsell_specification(xyy)
    family_code = int(spec[3])
    family = hue_families.get(family_code, '?')
    
    print(f"\nRGB{tuple(rgb_vals)} - {description}:")
    print(f"  Munsell: {spec[0]:.1f}{family} {spec[1]:.1f}/{spec[2]:.1f}")
    print(f"  Family code: {family_code} ({family})")
    print(f"  Hue value: {spec[0]:.4f}")
    
    # Check if near boundary
    if spec[0] < 3.0 or spec[0] > 7.5:
        print(f"  ⚠️ Near family boundary!")

print("\n" + "="*60)
print("FAMILY BOUNDARIES ANALYSIS:")
print("="*60)
print("Munsell hue notation within each family:")
print("  0.0-2.5: Transitioning from previous family")
print("  2.5-7.5: Core of the family")
print("  7.5-10.0: Transitioning to next family")
print("\nExample:")
print("  2.4R  -> Very red, almost at RP boundary")
print("  5.0R  -> Pure red")
print("  7.6R  -> Reddish, moving toward YR")
print("  10.0R = 0.0YR -> Same color, different notation")

print("\n" + "="*60)
print("POTENTIAL ISSUES:")
print("="*60)
print("1. Hue angle to family code conversion")
print("2. Boundary handling (e.g., 10.0R = 0.0YR)")
print("3. Negative hue handling")
print("4. Modulo operations for wraparound")