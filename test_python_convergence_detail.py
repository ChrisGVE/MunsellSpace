#!/usr/bin/env python3
"""Test Python's convergence in detail"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification

# Test the green color that's failing
xyy = np.array([0.3, 0.6, 0.715152])
print(f"Testing xyY {xyy}:")
print("="*60)

spec = xyY_to_munsell_specification(xyy)
print(f"Result: {spec}")

# Check what family code it is
families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
           6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
family = families.get(int(spec[3]), '?')
print(f"Family: {spec[0]:.1f}{family} {spec[1]:.1f}/{spec[2]:.1f}")