#!/usr/bin/env python3
"""Test Python's normalization in detail"""

import numpy as np
from colour.notation.munsell import normalise_munsell_specification

# Test various edge cases
test_specs = [
    # GY family
    np.array([9.9, 8.0, 22.0, 4]),   # 9.9GY
    np.array([10.0, 8.0, 22.0, 4]),  # 10GY -> should become 0Y
    np.array([10.1, 8.0, 22.0, 4]),  # 10.1GY -> should become 0.1Y
    
    # Y family 
    np.array([0.0, 8.0, 22.0, 5]),   # 0Y -> should become 10Y?
    np.array([9.9, 8.0, 22.0, 5]),   # 9.9Y
    np.array([10.0, 8.0, 22.0, 5]),  # 10Y -> should become 0YR
    
    # Test negative hues
    np.array([-0.1, 8.0, 22.0, 5]),  # -0.1Y
]

print("Python normalise_munsell_specification:")
print("="*60)

families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
           6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}

for spec in test_specs:
    norm = normalise_munsell_specification(spec)
    orig_family = families.get(int(spec[3]), '?')
    norm_family = families.get(int(norm[3]), '?')
    print(f"  [{spec[0]:5.1f}, {spec[1]:.1f}, {spec[2]:.1f}, {int(spec[3]):2}] ({spec[0]:.1f}{orig_family}) -> "
          f"[{norm[0]:5.1f}, {norm[1]:.1f}, {norm[2]:.1f}, {int(norm[3]):2}] ({norm[0]:.1f}{norm_family})")