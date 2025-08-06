#!/usr/bin/env python3
"""Test how Python looks up 10GY vs 0Y"""

import numpy as np
from colour.notation.munsell import xyY_from_renotation, xy_from_renotation_ovoid

# Test looking up 10GY (which exists in data)
spec_10gy = np.array([10.0, 8.0, 20.0, 4])  # 10GY 8/20 - exists
spec_0y = np.array([0.0, 8.0, 20.0, 5])      # 0Y 8/20 - doesn't exist

print("Testing xyY_from_renotation (exact lookup):")
print("="*60)

try:
    xyy_10gy = xyY_from_renotation(spec_10gy)
    print(f"10GY 8/20 (code 4): {xyy_10gy}")
except Exception as e:
    print(f"10GY 8/20 failed: {e}")

try:
    xyy_0y = xyY_from_renotation(spec_0y)
    print(f"0Y 8/20 (code 5): {xyy_0y}")
except Exception as e:
    print(f"0Y 8/20 failed: {e}")

print("\nTesting xy_from_renotation_ovoid (interpolation):")
print("="*60)

try:
    xy_10gy = xy_from_renotation_ovoid(spec_10gy)
    print(f"10GY 8/20 (code 4): {xy_10gy}")
except Exception as e:
    print(f"10GY 8/20 failed: {e}")

try:
    xy_0y = xy_from_renotation_ovoid(spec_0y)
    print(f"0Y 8/20 (code 5): {xy_0y}")
except Exception as e:
    print(f"0Y 8/20 failed: {e}")

# Check if they're the same
print("\n10GY code 4 == 0Y code 5?")
spec_10gy_22 = np.array([10.0, 8.0, 22.0, 4])
spec_0y_22 = np.array([0.0, 8.0, 22.0, 5])

xy_10gy_22 = xy_from_renotation_ovoid(spec_10gy_22)
xy_0y_22 = xy_from_renotation_ovoid(spec_0y_22)

print(f"10GY 8/22: {xy_10gy_22}")
print(f"0Y 8/22:   {xy_0y_22}")
print(f"Difference: {np.abs(xy_10gy_22 - xy_0y_22)}")