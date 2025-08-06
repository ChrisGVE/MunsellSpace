#!/usr/bin/env python3
"""Create exact test cases for xy_from_renotation_ovoid"""

import numpy as np
from colour.notation.munsell import xy_from_renotation_ovoid
import json

# Test cases covering different scenarios
test_cases = [
    # Standard hues with even chroma (direct lookup)
    (7.5, 9, 6, 4),   # 7.5GY 9/6
    (10.0, 9, 6, 4),  # 10GY 9/6
    (2.5, 9, 6, 4),   # 2.5GY 9/6
    (5.0, 9, 6, 4),   # 5GY 9/6
    
    # Non-standard hues with even chroma (hue interpolation)
    (8.548, 9, 6, 4), # 8.548GY 9/6 - our problematic case
    (8.0, 9, 6, 4),   # 8.0GY 9/6
    (8.5, 9, 6, 4),   # 8.5GY 9/6
    (3.75, 9, 6, 4),  # 3.75GY 9/6
    
    # Standard hues with different even chromas
    (7.5, 9, 8, 4),   # 7.5GY 9/8
    (10.0, 9, 4, 4),  # 10GY 9/4
    
    # Non-standard hues with different even chromas
    (8.548, 9, 8, 4), # 8.548GY 9/8
    (8.0, 9, 10, 4),  # 8.0GY 9/10
    
    # Edge cases
    (0.0, 9, 6, 4),   # 0GY 9/6
    (1.0, 9, 6, 4),   # 1GY 9/6
    (9.5, 9, 6, 4),   # 9.5GY 9/6
    
    # Different values
    (8.548, 8, 6, 4),  # 8.548GY 8/6
    (8.548, 7, 6, 4),  # 8.548GY 7/6
    
    # Different chromas
    (8.548, 9, 8, 4),  # 8.548GY 9/8
    (8.548, 9, 10, 4), # 8.548GY 9/10
    (8.548, 9, 12, 4), # 8.548GY 9/12
]

results = []

print("Generating test cases for xy_from_renotation_ovoid:")
print("=" * 80)
print(f"{'Hue':8} {'Value':6} {'Chroma':6} {'Code':5} -> {'x':12} {'y':12}")
print("-" * 80)

for hue, value, chroma, code in test_cases:
    spec = np.array([hue, value, chroma, code])
    xy = xy_from_renotation_ovoid(spec)
    
    print(f"{hue:8.3f} {value:6.1f} {chroma:6.3f} {code:5} -> {xy[0]:12.8f} {xy[1]:12.8f}")
    
    results.append({
        "spec": [hue, value, chroma, code],
        "xy": [float(xy[0]), float(xy[1])]
    })

# Save to JSON for Rust test
with open('xy_from_renotation_test_cases.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nGenerated {len(results)} test cases")

# Also test the key interpolation functions
print("\n\nTesting interpolation method decisions:")
print("-" * 80)

from colour.notation.munsell import interpolation_method_from_renotation_ovoid

for hue, value, chroma, code in test_cases[:10]:
    spec = np.array([hue, value, chroma, code])
    method = interpolation_method_from_renotation_ovoid(spec)
    print(f"{hue:.3f}GY {value}/{chroma}: {method}")