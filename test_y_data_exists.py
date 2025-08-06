#!/usr/bin/env python3
"""Check if the Y family data exists at the values we're looking for"""

import numpy as np
from colour.notation.munsell import MUNSELL_COLOURS_ALL

# Extract data and check what Y family values exist
y_data = []
for (hue_str, value, chroma), xyY in MUNSELL_COLOURS_ALL:
    if 'Y' in hue_str and 'YR' not in hue_str and 'GY' not in hue_str:
        y_data.append((hue_str, value, chroma))

# Sort and show Y data at value 8
print("Y family data at value 8:")
for hue_str, value, chroma in sorted(y_data):
    if abs(value - 8.0) < 0.1:
        print(f"  {hue_str} V={value} C={chroma}")

print("\nY family data at value 9:")
for hue_str, value, chroma in sorted(y_data):
    if abs(value - 9.0) < 0.1:
        print(f"  {hue_str} V={value} C={chroma}")

# Check for specific problem cases
print("\nLooking for specific specs that are failing:")
problem_specs = [
    ("0Y", 8.0, 22.0),
    ("10Y", 8.0, 22.0),
    ("0Y", 8.0, 20.0),
    ("10Y", 8.0, 20.0),
]

for hue_str_target, target_value, target_chroma in problem_specs:
    found = False
    for (hue_str, value, chroma), xyY in MUNSELL_COLOURS_ALL:
        if (hue_str == hue_str_target and 
            abs(value - target_value) < 0.1 and
            abs(chroma - target_chroma) < 0.1):
            found = True
            break
    print(f"  {hue_str_target} V={target_value} C={target_chroma}: {'FOUND' if found else 'NOT FOUND'}")

# Also check what GY data exists near 10GY at value 8
print("\nGY family data near 10GY at value 8:")
gy_high_data = []
for (hue_str, value, chroma), xyY in MUNSELL_COLOURS_ALL:
    if 'GY' in hue_str and abs(value - 8.0) < 0.1:
        # Extract hue number
        hue_num = float(hue_str.replace('GY', ''))
        if hue_num >= 7.5:
            gy_high_data.append((hue_str, value, chroma))

for hue_str, value, chroma in sorted(gy_high_data):
    print(f"  {hue_str} V={value} C={chroma}")