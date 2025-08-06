#!/usr/bin/env python3
"""Test specific specification that's failing"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xy
from colour.utilities import domain_range_scale

# Test the failing specification
spec = np.array([0.0, 8.0, 22.0, 5.0])
print(f"Testing specification: hue={spec[0]}, value={spec[1]}, chroma={spec[2]}, code={spec[3]}")

# This is inside xy_from_renotation_ovoid
# It's being called with hue=0.0 (should this be 10.0?)

# Test with standard hues
for hue in [0.0, 2.5, 5.0, 7.5, 10.0]:
    spec_test = np.array([hue, 8.0, 22.0, 5.0])
    try:
        with domain_range_scale("ignore"):
            xy = munsell_specification_to_xy(spec_test)
        print(f"  hue={hue}: Success - xy={xy}")
    except Exception as e:
        print(f"  hue={hue}: Error - {e}")

# Test what hue should be used for code 5 (Y) at hue=0
print("\nFor code 5 (Y), hue=0.0 might need to be treated as 10.0Y")