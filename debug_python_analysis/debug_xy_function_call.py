#!/usr/bin/env python3
"""Debug why xy_from_renotation_ovoid gave wrong values earlier"""

import numpy as np
from colour.notation.munsell import xy_from_renotation_ovoid

# Test different ways of calling the function
print("Testing different ways to call xy_from_renotation_ovoid:")
print("=" * 80)

# Method 1: As I did before (might be wrong)
spec1 = np.array([7.5, 9, 6, 4])
try:
    xy1 = xy_from_renotation_ovoid(spec1)
    print(f"Method 1 - np.array([7.5, 9, 6, 4]): xy=({xy1[0]:.6f}, {xy1[1]:.6f})")
except Exception as e:
    print(f"Method 1 failed: {e}")

# Method 2: With float values
spec2 = np.array([7.5, 9.0, 6.0, 4.0])
try:
    xy2 = xy_from_renotation_ovoid(spec2)
    print(f"Method 2 - np.array([7.5, 9.0, 6.0, 4.0]): xy=({xy2[0]:.6f}, {xy2[1]:.6f})")
except Exception as e:
    print(f"Method 2 failed: {e}")

# Method 3: As a list
spec3 = [7.5, 9, 6, 4]
try:
    xy3 = xy_from_renotation_ovoid(spec3)
    print(f"Method 3 - list [7.5, 9, 6, 4]: xy=({xy3[0]:.6f}, {xy3[1]:.6f})")
except Exception as e:
    print(f"Method 3 failed: {e}")

# Let me check the exact values from the earlier script
print("\n\nRecreating the exact call from compare_boundary_values.py:")
spec = np.array([7.5, 9, 6, 4])  # Must use integer value for xy_from_renotation_ovoid
print(f"Input spec: {spec}")
print(f"Type: {type(spec)}, dtype: {spec.dtype}")

xy = xy_from_renotation_ovoid(spec)
print(f"Result: xy=({xy[0]:.6f}, {xy[1]:.6f})")

# Let's also check what happens if we look at the raw data
print("\n\nChecking raw MUNSELL_COLOURS_ALL data:")
from colour.notation.munsell import MUNSELL_COLOURS_ALL

# Find the exact entry
for entry in MUNSELL_COLOURS_ALL:
    (hue_str, value, chroma), xyY = entry
    if hue_str == '7.5GY' and value == 9.0 and chroma == 6.0:
        print(f"Found in raw data: {hue_str} {value}/{chroma} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f})")
        break

# Maybe the function is doing some transformation?
print("\n\nLet's trace what's happening...")
print("The values I got earlier (0.312000, 0.278800) are completely different.")
print("This suggests there might be an issue with how I ran the script earlier.")

# Let me re-run the exact code from the problematic output
from colour.notation.munsell import bounding_hues_from_renotation

spec = np.array([8.548, 9, 6, 4])
hue_code = spec[:2]
bounds = bounding_hues_from_renotation(hue_code)

print(f"\nBounds for 8.548GY: {bounds}")

# Get xy for CW boundary
spec_cw = np.array([bounds[0][0], 9, 6, int(bounds[0][1])])
print(f"CW spec: {spec_cw}")
xy_cw = xy_from_renotation_ovoid(spec_cw)
print(f"CW xy: ({xy_cw[0]:.6f}, {xy_cw[1]:.6f})")