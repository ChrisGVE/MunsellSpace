#!/usr/bin/env python3
"""Test how Python handles the 10GY -> 0Y normalization"""

import numpy as np
from colour.notation.munsell import normalise_munsell_specification, xyY_from_renotation

# Test what happens with 10GY spec
spec_10gy = np.array([10.0, 8.0, 22.0, 4])  # 10GY 8/22
print(f"Original spec: {spec_10gy}")

# Normalize it
normalized = normalise_munsell_specification(spec_10gy)
print(f"Normalized spec: {normalized}")

# Now check if we can get xyY from both
print("\nLooking up xyY values:")
try:
    xyy_original = xyY_from_renotation(spec_10gy)
    print(f"xyY from 10GY: {xyy_original}")
except Exception as e:
    print(f"Error getting xyY from 10GY: {e}")

try:
    xyy_normalized = xyY_from_renotation(normalized)
    print(f"xyY from normalized: {xyy_normalized}")
except Exception as e:
    print(f"Error getting xyY from normalized: {e}")

# Test with exact 10GY 8/20 which exists
spec_exists = np.array([10.0, 8.0, 20.0, 4])  # 10GY 8/20
print(f"\nTesting spec that exists: {spec_exists}")
normalized_exists = normalise_munsell_specification(spec_exists)
print(f"Normalized: {normalized_exists}")

try:
    xyy_exists = xyY_from_renotation(spec_exists)
    print(f"xyY from 10GY 8/20: {xyy_exists}")
except Exception as e:
    print(f"Error: {e}")

try:
    xyy_norm_exists = xyY_from_renotation(normalized_exists)
    print(f"xyY from normalized: {xyy_norm_exists}")
except Exception as e:
    print(f"Error: {e}")

# Check what normalise does to various specs
test_specs = [
    np.array([10.0, 8.0, 22.0, 4]),  # 10GY
    np.array([0.0, 8.0, 22.0, 5]),    # 0Y (which becomes 10Y)
    np.array([9.9, 8.0, 22.0, 4]),    # 9.9GY
]

print("\nNormalization tests:")
for spec in test_specs:
    norm = normalise_munsell_specification(spec)
    print(f"  {spec} -> {norm}")