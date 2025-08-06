#!/usr/bin/env python3
"""Test the interpolation method decision tree for our problematic case"""

import numpy as np
from colour.notation.munsell import (
    interpolation_method_from_renotation_ovoid,
    munsell_colour_to_munsell_specification,
    hue_to_ASTM_hue
)

# Test RGB(204, 255, 170) which gives 8.548GY 9/6 at some point
test_cases = [
    "8.548GY 9/6",    # The problematic case
    "8.0GY 9/6",      # For comparison
    "8.5GY 9/6",      # For comparison
    "7.5GY 9/6",      # Boundary case
    "10.0GY 9/6",     # Boundary case
]

print("Testing interpolation method decisions:")
print("=" * 80)
print(f"{'Munsell':15} {'Specification':20} {'ASTM Hue':10} {'Method':10}")
print("-" * 80)

for munsell_str in test_cases:
    spec = munsell_colour_to_munsell_specification(munsell_str)
    
    # Get ASTM hue
    hue, value, chroma, code = spec
    astm_hue = hue_to_ASTM_hue([hue, code])
    
    # Get interpolation method
    method = interpolation_method_from_renotation_ovoid(spec)
    
    print(f"{munsell_str:15} {str(spec):20} {astm_hue:10.3f} {method:10}")

# Let's also check what happens with exact boundary values
print("\n\nChecking exact interpolation logic for value=9:")
print("-" * 80)

# For value=9, chroma=6 (from line 492-493):
# elif chroma in (6, 8, 10, 12, 14):
#     interpolation_method = 2 if 5 < ASTM_hue < 42.5 else 1

# GY family has code=4, so:
# ASTM_hue = hue * 10 + 40 (for GY)
# 7.5GY -> ASTM_hue = 7.5 * 10 + 40 = 115
# 8.548GY -> ASTM_hue = 8.548 * 10 + 40 = 125.48
# 10.0GY -> ASTM_hue = 10.0 * 10 + 40 = 140

print("\nFor value=9, chroma=6:")
print("Condition: interpolation_method = 2 if 5 < ASTM_hue < 42.5 else 1")
print("Since all GY hues have ASTM_hue > 100, they will use method 1 (Linear)")

# Test with different values
print("\n\nTesting different values at 8.548GY /6:")
for v in range(1, 10):
    spec = np.array([8.548, v, 6, 4])
    method = interpolation_method_from_renotation_ovoid(spec)
    print(f"8.548GY {v}/6: {method}")