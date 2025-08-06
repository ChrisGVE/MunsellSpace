#!/usr/bin/env python3
"""Test Python's xy_from_renotation_ovoid function to create reference data"""

import numpy as np
from colour.notation.munsell import xy_from_renotation_ovoid
from colour.notation.munsell import bounding_hues_from_renotation
from colour.notation.munsell import interpolation_method_from_renotation_ovoid
from colour.notation.munsell import maximum_chroma_from_renotation

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
    
    # Additional test cases for comprehensive coverage
    (4.13, 4.0, 18.159, 7),  # Previous problematic case
    (0.0, 5.0, 10.0, 7),     # 0R should become 10R
    (1.234, 3.5, 5.678, 2),  # Fractional values
]

print("Testing xy_from_renotation_ovoid:")
print("=" * 80)
print(f"{'Specification':25} {'Result xy':30} {'Interpolation':15}")
print("-" * 80)

results = []
for hue, value, chroma, code in test_cases:
    spec = np.array([hue, value, chroma, code])
    try:
        # Get xy coordinates
        xy = xy_from_renotation_ovoid(spec)
        
        # Get interpolation method
        method = interpolation_method_from_renotation_ovoid(spec)
        
        # Format output
        family = ['', 'B', 'BG', 'G', 'GY', 'Y', 'YR', 'R', 'RP', 'P', 'PB'][code] if code <= 10 else '?'
        spec_str = f"{hue}{family} {value}/{chroma}"
        print(f"{spec_str:25} ({xy[0]:.6f}, {xy[1]:.6f})    {method}")
        
        results.append({
            'hue': hue,
            'value': value,
            'chroma': chroma,
            'code': code,
            'x': xy[0],
            'y': xy[1],
            'method': method
        })
    except Exception as e:
        family = ['', 'B', 'BG', 'G', 'GY', 'Y', 'YR', 'R', 'RP', 'P', 'PB'][code] if code <= 10 else '?'
        spec_str = f"{hue}{family} {value}/{chroma}"
        print(f"{spec_str:25} ERROR: {str(e)[:40]}...")

# Save results for unit testing
print("\n\nSaving results to xy_from_renotation_reference.csv...")
import csv
with open('xy_from_renotation_reference.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['hue', 'value', 'chroma', 'code', 'x', 'y', 'method'])
    writer.writeheader()
    writer.writerows(results)

# Test bounding hues function
print("\n\nTesting bounding_hues_from_renotation:")
print("=" * 80)
test_hues = [
    (0.0, 7),    # 0R -> should become 10R
    (2.5, 7),    # 2.5R
    (8.548, 4),  # 8.548GY
    (10.0, 1),   # 10B
    (1.234, 10), # 1.234PB
]

for hue, code in test_hues:
    spec = np.array([hue, 5.0, 10.0, code])  # value and chroma don't matter for this function
    bounds = bounding_hues_from_renotation(spec)
    family = ['', 'B', 'BG', 'G', 'GY', 'Y', 'YR', 'R', 'RP', 'P', 'PB'][code] if code <= 10 else '?'
    print(f"{hue}{family}: CW={bounds[0]}, CCW={bounds[1]}")

# Test maximum chroma function
print("\n\nTesting maximum_chroma_from_renotation:")
print("=" * 80)
test_specs = [
    (7.5, 9.0, 4),   # 7.5GY at value 9
    (8.548, 9.0, 4), # 8.548GY at value 9
    (5.0, 5.0, 7),   # 5R at value 5
    (2.5, 1.0, 1),   # 2.5B at value 1
]

for hue, value, code in test_specs:
    spec = np.array([hue, value, 0.0, code])  # chroma=0 for testing max
    max_chroma = maximum_chroma_from_renotation(spec)
    family = ['', 'B', 'BG', 'G', 'GY', 'Y', 'YR', 'R', 'RP', 'P', 'PB'][code] if code <= 10 else '?'
    print(f"{hue}{family} at value {value}: max chroma = {max_chroma:.1f}")