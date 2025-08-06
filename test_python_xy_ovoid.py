#!/usr/bin/env python3
"""Test Python's xy_from_renotation_ovoid with non-standard values"""

import numpy as np
from colour.notation.munsell import xy_from_renotation_ovoid

# Test cases with non-standard values
test_cases = [
    # Standard values (should work)
    ([5.0, 5, 10, 0], "Standard: 5R 5/10"),
    
    # Non-even chroma
    ([5.0, 5, 11, 0], "Non-even chroma: 5R 5/11"),
    ([5.0, 5, 10.5, 0], "Decimal chroma: 5R 5/10.5"),
    
    # Non-integer value
    ([5.0, 5.5, 10, 0], "Non-integer value: 5R 5.5/10"),
    ([5.0, 5.22, 10, 0], "Decimal value: 5R 5.22/10"),
    
    # Non-standard hue
    ([8.548, 9, 6, 4], "Non-standard hue: 8.548G 9/6"),
    
    # Extreme chroma from algorithm
    ([0.0, 5.22, 16.94, 0], "Algorithm output: 0R 5.22/16.94"),
    
    # Low chroma
    ([5.0, 5, 1.5, 0], "Low chroma: 5R 5/1.5"),
    ([5.0, 5, 0.5, 0], "Very low chroma: 5R 5/0.5"),
]

print("Testing Python's xy_from_renotation_ovoid with various inputs:\n")

for spec, description in test_cases:
    try:
        result = xy_from_renotation_ovoid(np.array(spec))
        print(f"✓ {description}")
        print(f"  Input: {spec}")
        print(f"  Output: [{result[0]:.6f}, {result[1]:.6f}]")
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Input: {spec}")
        print(f"  Error: {e}")
    print()