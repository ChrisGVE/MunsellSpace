#!/usr/bin/env python3
"""Trace exactly how Python converts specs to xy"""

from colour.notation.munsell import _munsell_specification_to_xyY
import numpy as np

# Test specs that are problematic
test_specs = [
    ([7.123, 9.0, 2.0, 3], "Integer value at chroma 2"),
    ([7.123, 9.277, 2.0, 3], "Non-integer value at chroma 2"),
    ([7.123, 9.277, 1.541, 3], "What Rust gets"),
    ([7.121, 9.277, 2.084, 3], "What Python gets"),
]

print("Testing how Python handles different specs:\n")

for spec, description in test_specs:
    print(f"{description}:")
    print(f"  Spec: {spec}")
    
    try:
        result = _munsell_specification_to_xyY(spec)
        print(f"  SUCCESS: xy = ({result[0]:.6f}, {result[1]:.6f}, {result[2]:.6f})")
    except Exception as e:
        print(f"  FAILED: {e}")
    print()

print("Key observations:")
print("1. Python CAN handle non-integer values at chroma 2")
print("2. This means _munsell_specification_to_xyY has logic to interpolate values")
print("3. Our xy_from_renotation_ovoid may be too restrictive")