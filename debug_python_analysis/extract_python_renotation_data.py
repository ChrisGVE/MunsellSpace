#!/usr/bin/env python3
"""Extract the correct renotation data from Python"""

from colour.notation.munsell import MUNSELL_COLOURS_ALL
import numpy as np

print("Extracting GY family data at value 9:")
print("=" * 80)
print(f"{'Hue':8} {'Value':6} {'Chroma':6} {'x':10} {'y':10} {'Y':10}")
print("-" * 80)

# Find all GY entries at value 9
gy_value_9 = []
for entry in MUNSELL_COLOURS_ALL:
    (hue_str, value, chroma), xyY = entry
    if 'GY' in hue_str and abs(value - 9.0) < 0.01:
        gy_value_9.append((hue_str, value, chroma, xyY))

# Sort by hue and chroma
gy_value_9.sort(key=lambda x: (float(x[0].replace('GY', '')), x[2]))

# Display the data
for hue_str, value, chroma, xyY in gy_value_9:
    print(f"{hue_str:8} {value:6.1f} {chroma:6.1f} {xyY[0]:10.6f} {xyY[1]:10.6f} {xyY[2]:10.6f}")

# Now specifically look for our test cases
print("\n\nSpecific test cases:")
print("=" * 80)

test_cases = [
    ('7.5GY', 9.0, 6.0),
    ('10GY', 9.0, 6.0),
    ('7.5GY', 9.0, 8.0),
    ('10GY', 9.0, 8.0),
]

for test_hue, test_value, test_chroma in test_cases:
    found = False
    for entry in MUNSELL_COLOURS_ALL:
        (hue_str, value, chroma), xyY = entry
        if hue_str == test_hue and abs(value - test_value) < 0.01 and abs(chroma - test_chroma) < 0.01:
            print(f"{hue_str} {value}/{chroma}: xy=({xyY[0]:.6f}, {xyY[1]:.6f}), Y={xyY[2]:.6f}")
            found = True
            break
    if not found:
        print(f"{test_hue} {test_value}/{test_chroma}: NOT FOUND")

# Compare with what the xy_from_renotation_ovoid function returns
print("\n\nComparing with xy_from_renotation_ovoid results:")
print("=" * 80)

from colour.notation.munsell import xy_from_renotation_ovoid

# Note: This function expects [hue_number, value, chroma, code]
# For GY, code = 4
test_specs = [
    (7.5, 9, 6, 4),   # 7.5GY 9/6
    (10.0, 9, 6, 4),  # 10GY 9/6
    (7.5, 9, 8, 4),   # 7.5GY 9/8
    (10.0, 9, 8, 4),  # 10GY 9/8
]

for hue_num, value, chroma, code in test_specs:
    spec = np.array([hue_num, value, chroma, code])
    xy = xy_from_renotation_ovoid(spec)
    print(f"{hue_num}GY {value}/{chroma}: xy=({xy[0]:.6f}, {xy[1]:.6f}) from ovoid function")

# The issue might be that xy_from_renotation_ovoid does additional processing!