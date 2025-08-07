#!/usr/bin/env python3

import numpy as np
from colour.notation.munsell import xy_from_renotation_ovoid

# Test what Python does for low chroma colors
test_specs = [
    [7.138, 9.277, 1.54, 3],  # Near grey at value 9.277
    [7.138, 9.0, 1.54, 3],    # Same but at integer value
    [7.138, 9.277, 2.0, 3],   # At chroma 2.0
    [7.138, 9.0, 2.0, 3],     # At chroma 2.0, integer value
]

print("Testing Python's xy_from_renotation_ovoid for low chroma:")
print()

for spec in test_specs:
    try:
        xy = xy_from_renotation_ovoid(np.array(spec))
        print(f"Spec [{spec[0]:.3f}, {spec[1]:.3f}, {spec[2]:.2f}, {spec[3]}]:")
        print(f"  xy: ({xy[0]:.6f}, {xy[1]:.6f})")
    except Exception as e:
        print(f"Spec [{spec[0]:.3f}, {spec[1]:.3f}, {spec[2]:.2f}, {spec[3]}]:")
        print(f"  Error: {e}")
    print()

print("Key observation: Python handles non-integer values differently")