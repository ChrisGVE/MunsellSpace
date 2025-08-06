#!/usr/bin/env python3
"""Test how Python handles extrapolation for high chromas"""

import numpy as np
from colour.notation.munsell import _xy_from_renotation, _munsell_specification_to_xy
from colour.utilities import domain_range_scale

# Test a specification with high chroma that doesn't exist
# Red: hue=0.0, value=5.0, chroma=24.0, code=6
spec = np.array([0.0, 5.0, 24.0, 6.0])

print(f"Testing specification: {spec}")
print(f"  hue={spec[0]}, value={spec[1]}, chroma={spec[2]}, code={spec[3]}")

# Try the lower-level function
try:
    with domain_range_scale("ignore"):
        xy = _xy_from_renotation(spec)
    print(f"\n_xy_from_renotation result: {xy}")
except Exception as e:
    print(f"\n_xy_from_renotation error: {e}")

# Now try the higher level function that handles interpolation
try:
    with domain_range_scale("ignore"):
        xy = _munsell_specification_to_xy(spec)
    print(f"\n_munsell_specification_to_xy result: {xy}")
except Exception as e:
    print(f"\n_munsell_specification_to_xy error: {e}")

# Test what chromas are actually available at value 5
print("\n\nChecking available chromas at value 5:")
for chroma in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]:
    spec_test = np.array([0.0, 5.0, float(chroma), 6.0])
    try:
        with domain_range_scale("ignore"):
            xy = _xy_from_renotation(spec_test)
        print(f"  Chroma {chroma}: exists - xy={xy}")
    except:
        print(f"  Chroma {chroma}: NOT in data")

# Test with closest standard specification
print("\n\nTesting with hue=5.0 instead of 0.0:")
spec2 = np.array([5.0, 5.0, 24.0, 6.0])
try:
    with domain_range_scale("ignore"):
        xy = _munsell_specification_to_xy(spec2)
    print(f"_munsell_specification_to_xy result: {xy}")
except Exception as e:
    print(f"_munsell_specification_to_xy error: {e}")