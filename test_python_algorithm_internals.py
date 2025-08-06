#!/usr/bin/env python3
"""Test Python's algorithm internals to understand how it handles intermediate values"""

import numpy as np
from colour.notation.munsell import (
    xyY_to_munsell_specification,
    xy_from_renotation_ovoid,
    munsell_specification_to_xyY,
    maximum_chroma_from_renotation
)

print("Testing how Python's algorithm handles intermediate computations:\n")

# Test getting maximum chroma
print("1. Testing maximum_chroma_from_renotation:")
test_cases = [
    (5.0, 5, 0, "5R"),
    (5.0, 5.22, 0, "5R with non-integer value"),
    (7.939, 5, 7, "7.939PB"),
    (7.939, 5.221, 7, "7.939PB with non-integer value"),
]

for hue, value, code, desc in test_cases:
    try:
        max_chroma = maximum_chroma_from_renotation([hue, value, 0, code])
        print(f"  {desc}: max_chroma = {max_chroma}")
    except Exception as e:
        print(f"  {desc}: Error - {e}")

print("\n2. Testing munsell_specification_to_xyY with non-standard values:")
specs = [
    ([5.0, 5, 10, 0], "Standard spec"),
    ([5.0, 5.22, 10, 0], "Non-integer value"),
    ([5.0, 5, 11, 0], "Non-even chroma"),
    ([7.939, 5.221, 20.443, 7], "Algorithm output for red"),
]

for spec, desc in specs:
    try:
        xyy = munsell_specification_to_xyY(np.array(spec))
        print(f"  {desc}: xyY = [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
    except Exception as e:
        print(f"  {desc}: Error - {e}")

print("\n3. Understanding the iterative algorithm flow:")
print("  The algorithm iterates with progressively refined values")
print("  It needs to convert intermediate specs to xyY, but those specs may have:")
print("  - Non-integer values")
print("  - Non-even chromas")
print("  - Values outside standard ranges")

# Try to trace through a simple case
print("\n4. Manual trace of algorithm for red [0.64, 0.33, 0.212673]:")
xyy = np.array([0.640000, 0.330000, 0.212673])
try:
    spec = xyY_to_munsell_specification(xyy)
    print(f"  Final spec: {spec}")
except Exception as e:
    print(f"  Error: {e}")