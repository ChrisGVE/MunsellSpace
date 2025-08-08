#!/usr/bin/env python3
"""Test maximum chroma for high values"""

import numpy as np
from colour.notation.munsell import _maximum_chroma_from_renotation

# Test for G family at high values
hue = 7.1
code = 3  # G family
values_to_test = [8.0, 8.5, 9.0, 9.2, 9.277, 9.5, 9.8, 9.9, 9.95, 9.99]

print("Testing maximum chroma for G family at high values:")
print()
for value in values_to_test:
    spec = np.array([hue, value, 0.0, code])
    max_chroma = _maximum_chroma_from_renotation(spec)
    print(f"  Value {value:5.3f}: max_chroma = {max_chroma:.3f}")