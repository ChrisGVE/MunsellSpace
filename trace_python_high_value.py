#!/usr/bin/env python3
"""Trace Python's handling of high-value colors."""

import sys
import os
sys.path.append('InkyFingers')

# Enable detailed debug output
os.environ['DEBUG_MUNSELL'] = '1'

from colour.notation.munsell import xyY_to_munsell_specification
from colour.notation.munsell_renotation import xy_from_renotation_ovoid
import numpy as np

# Test the problematic high-value color RGB(187,255,153)
# This has xyY from earlier testing
xyy = np.array([0.3445, 0.5041, 0.8831])  # Approximate values for RGB(187,255,153)

print("Testing high-value color with Python colour-science")
print(f"Input xyY: {xyy}")
print()

# Get the Munsell specification
spec = xyY_to_munsell_specification(xyy)
print(f"Result specification: hue={spec[0]:.2f}, value={spec[1]:.2f}, chroma={spec[2]:.2f}, code={spec[3]}")
print()

# Now test what happens with value > 9.0 in xy_from_renotation_ovoid
print("Testing xy_from_renotation_ovoid with high values:")
for value in [8.9, 9.0, 9.1, 9.3, 9.5, 9.8]:
    test_spec = np.array([5.0, value, 10.0, 5])  # 5Y at different values, chroma=10
    try:
        xy = xy_from_renotation_ovoid(test_spec)
        print(f"  Value {value:.1f}: xy = [{xy[0]:.4f}, {xy[1]:.4f}]")
    except Exception as e:
        print(f"  Value {value:.1f}: ERROR - {e}")

print()
print("Testing maximum chroma at high values:")
# Test how maximum chroma changes with value
from colour.notation.munsell_renotation import maximum_chroma_from_renotation

for value in [8.9, 9.0, 9.1, 9.3, 9.5]:
    try:
        max_chroma = maximum_chroma_from_renotation(5.0, value, 5)
        print(f"  Value {value:.1f}: max_chroma = {max_chroma:.2f}")
    except Exception as e:
        print(f"  Value {value:.1f}: ERROR - {e}")