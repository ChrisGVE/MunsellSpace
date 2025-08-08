#!/usr/bin/env python3
"""Test munsell_specification_to_xyY for specific specs"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Test the converged spec from Rust
specs_to_test = [
    ([7.240, 9.000, 1.545, 3], "Rust's converged spec"),
    ([7.106, 9.277, 2.085, 3], "Python's final spec"),
    ([7.0, 9.0, 2.0, 3], "Round values for comparison"),
    ([7.240, 9.277, 1.545, 3], "Rust hue with Python value"),
    ([7.106, 9.000, 2.085, 3], "Python hue with Rust value"),
]

print("Testing munsell_specification_to_xyY:")
print()

target_x = 0.3016555411
target_y = 0.3289901051
target_Y = 0.8269331673

print(f"Target: x={target_x:.6f}, y={target_y:.6f}, Y={target_Y:.6f}")
print()

for spec, desc in specs_to_test:
    try:
        xyY = munsell_specification_to_xyY(np.array(spec))
        print(f"{desc}:")
        print(f"  Spec: {spec}")
        print(f"  xyY: ({xyY[0]:.6f}, {xyY[1]:.6f}, {xyY[2]:.6f})")
        
        # Calculate distance from target
        distance = np.sqrt((xyY[0] - target_x)**2 + (xyY[1] - target_y)**2)
        print(f"  Distance from target xy: {distance:.9f}")
        print(f"  Y difference: {xyY[2] - target_Y:.6f}")
    except Exception as e:
        print(f"{desc}: ERROR - {e}")
    print()