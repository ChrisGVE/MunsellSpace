#!/usr/bin/env python3

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour.notation.munsell import bounding_hues_from_renotation
import numpy as np

# Test what Python returns for 0.0 GY
print("Testing 0.0 GY (code=4):")

# Test with just hue and code
result = bounding_hues_from_renotation([0.0, 4])
print(f"Python returns for [0.0, 4] (0GY): {result}")

# Let's also check surrounding cases
print("\nTesting related cases:")
result = bounding_hues_from_renotation([10.0, 3])
print(f"Python returns for [10.0, 3] (10G): {result}")

result = bounding_hues_from_renotation([2.5, 4])
print(f"Python returns for [2.5, 4] (2.5GY): {result}")

print("\nTesting the specific problematic case:")
# Now also test xy lookup
from colour.notation.munsell import xy_from_renotation_ovoid

# Let's see what coordinates we get for these bounding hues
spec_0_gy = np.array([0.0, 9.0, 6.0, 4.0])  # 0GY 9/6
xy_result = xy_from_renotation_ovoid(spec_0_gy)
print(f"Python xy_from_renotation_ovoid for 0GY 9/6: {xy_result}")

# What about the bounding hue coordinates?
spec_10_g = np.array([10.0, 9.0, 6.0, 3.0])  # 10G 9/6 (what should be the boundary)
xy_result_10g = xy_from_renotation_ovoid(spec_10_g)
print(f"Python xy_from_renotation_ovoid for 10G 9/6: {xy_result_10g}")

spec_25_gy = np.array([2.5, 9.0, 6.0, 4.0])  # 2.5GY 9/6 
xy_result_25gy = xy_from_renotation_ovoid(spec_25_gy)
print(f"Python xy_from_renotation_ovoid for 2.5GY 9/6: {xy_result_25gy}")