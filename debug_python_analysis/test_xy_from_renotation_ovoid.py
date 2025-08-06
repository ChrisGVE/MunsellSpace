#!/usr/bin/env python3
"""Test Python's _xy_from_renotation_ovoid function to understand its exact behavior"""

import numpy as np
from colour.notation.munsell import _xy_from_renotation_ovoid

# Test cases covering various scenarios
test_cases = [
    # Standard hues with even chromas (should be direct lookup)
    (2.5, 9.0, 6.0, 4),   # 2.5GY 9/6
    (5.0, 9.0, 8.0, 4),   # 5.0GY 9/8
    (7.5, 9.0, 6.0, 4),   # 7.5GY 9/6
    (10.0, 9.0, 8.0, 4),  # 10.0GY 9/8
    
    # Non-standard hues with even chromas (hue interpolation)
    (8.548, 9.0, 6.0, 4), # 8.548GY 9/6
    (8.548, 9.0, 8.0, 4), # 8.548GY 9/8
    
    # Standard hues with odd chromas (chroma interpolation)
    (7.5, 9.0, 7.125, 4), # 7.5GY 9/7.125
    (10.0, 9.0, 7.125, 4), # 10.0GY 9/7.125
    
    # Non-standard hues with odd chromas (both interpolations)
    (8.548, 9.0, 7.125, 4), # 8.548GY 9/7.125
    
    # Edge cases
    (0.0, 9.0, 0.0, 4),    # Achromatic
    (2.5, 9.0, 2.0, 4),    # Low chroma
    (7.5, 9.0, 20.0, 4),   # High chroma (may not exist)
    
    # Different families
    (5.0, 5.0, 10.0, 7),   # 5.0R 5/10
    (7.5, 7.0, 8.0, 1),    # 7.5B 7/8
]

print("Testing _xy_from_renotation_ovoid:")
print("=" * 80)
print(f"{'Specification':25} {'Result xy':30} {'Notes':25}")
print("-" * 80)

for hue, value, chroma, code in test_cases:
    spec = np.array([hue, value, chroma, code])
    try:
        result = _xy_from_renotation_ovoid(spec)
        family = ['', 'B', 'BG', 'G', 'GY', 'Y', 'YR', 'R', 'RP', 'P', 'PB'][code] if code <= 10 else '?'
        spec_str = f"{hue}{family} {value}/{chroma}"
        print(f"{spec_str:25} ({result[0]:.6f}, {result[1]:.6f})")
    except Exception as e:
        family = ['', 'B', 'BG', 'G', 'GY', 'Y', 'YR', 'R', 'RP', 'P', 'PB'][code] if code <= 10 else '?'
        spec_str = f"{hue}{family} {value}/{chroma}"
        print(f"{spec_str:25} ERROR: {str(e)[:40]}...")

# Now let's trace through the exact steps for our problematic case
print("\n\nDetailed trace for 8.548GY 9.0/7.125:")
print("=" * 80)

# This is the case where Rust and Python differ
spec = np.array([8.548, 9.0, 7.125, 4])
result = _xy_from_renotation_ovoid(spec)
print(f"Result: ({result[0]:.6f}, {result[1]:.6f})")

# Let's also check the boundary hues
print("\nBoundary hues for 8.548GY:")
from colour.notation.munsell import _bounding_hues_from_renotation
bounds = _bounding_hues_from_renotation(spec)
print(f"Clockwise: {bounds[0]}")
print(f"Counter-clockwise: {bounds[1]}")

# Check interpolation method
from colour.notation.munsell import _interpolation_method_from_renotation_ovoid
method = _interpolation_method_from_renotation_ovoid(spec)
print(f"\nInterpolation method: {method}")