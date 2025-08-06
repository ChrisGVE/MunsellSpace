#!/usr/bin/env python3
"""Simple test of convergence for known problematic colors"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_colour

# Test colors that were causing convergence issues
test_colors = [
    # Green (was causing family jump)
    [0.3, 0.6, 0.715152],
    # Red (was causing oscillation)
    [0.64007712, 0.3298325, 0.2126],
    # Grey (should be achromatic)
    [0.31006, 0.31616, 0.5],
]

print("Python convergence test:")
print("=" * 60)

for xyy in test_colors:
    try:
        result = xyY_to_munsell_colour(np.array(xyy))
        print(f"xyY {xyy} -> {result}")
    except Exception as e:
        print(f"xyY {xyy} -> ERROR: {e}")
print()