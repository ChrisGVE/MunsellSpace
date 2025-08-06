#!/usr/bin/env python3
"""Test Python's xyY_to_munsell_specification directly"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification, munsell_specification_to_munsell_colour

# Test the exact xyY values that fail in our Rust implementation
test_cases = [
    ([0.640000, 0.330000, 0.212673], "red"),
    ([0.185539, 0.187939, 0.054654], "2.9PB reference"),
    ([0.312727, 0.329023, 0.215861], "grey 128"),
    ([0.300000, 0.600000, 0.715152], "green"),
    ([0.150000, 0.060000, 0.072175], "blue"),
    ([0.31271, 0.32902, 0.0], "black"),
    ([0.31271, 0.32902, 1.0], "white"),
]

print("Testing Python's xyY_to_munsell_specification:\n")

for xyy, name in test_cases:
    print(f"Testing {name}: xyY = [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
    try:
        # Convert xyY to Munsell specification
        spec = xyY_to_munsell_specification(np.array(xyy))
        print(f"  Munsell spec: [hue={spec[0]:.3f}, value={spec[1]:.3f}, "
              f"chroma={spec[2]:.3f}, code={int(spec[3])}]")
        
        # Convert to notation
        notation = munsell_specification_to_munsell_colour(spec)
        print(f"  Munsell notation: {notation}")
        
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")
    
    print()

# Test what happens inside the algorithm
print("\nDiving deeper into the algorithm behavior:")
print("What happens when the algorithm produces non-standard values?\n")

# Simulate what the iterative algorithm might produce
algorithm_outputs = [
    ([5.0, 5.22, 16.94, 0], "Algorithm output with non-integer value and non-even chroma"),
    ([8.548, 9.0, 6.0, 4], "Non-standard hue from algorithm"),
    ([2.9, 2.8, 7.0, 7], "Exact values from reference"),
]

for spec, description in algorithm_outputs:
    print(f"{description}:")
    print(f"  Spec: {spec}")
    try:
        notation = munsell_specification_to_munsell_colour(np.array(spec))
        print(f"  → Notation: {notation}")
    except Exception as e:
        print(f"  → Error: {type(e).__name__}: {e}")