#!/usr/bin/env python3
"""Compare xy_from_renotation_ovoid for specific specs"""

import numpy as np
from colour.notation.munsell import _xy_from_renotation_ovoid

# Test the converged spec from Rust
specs_to_test = [
    ([7.240, 9.000, 1.545, 3], "Rust's converged spec"),
    ([7.106, 9.277, 2.085, 3], "Python's final spec"),
    ([7.0, 9.0, 2.0, 3], "Round values for comparison"),
]

print("Comparing xy_from_renotation_ovoid results:")
print()

for spec, desc in specs_to_test:
    try:
        xy = _xy_from_renotation_ovoid(np.array(spec))
        print(f"{desc}:")
        print(f"  Spec: {spec}")
        print(f"  xy: ({xy[0]:.6f}, {xy[1]:.6f})")
        
        # Calculate distance from target
        target_x = 0.3016555411
        target_y = 0.3289901051
        distance = np.sqrt((xy[0] - target_x)**2 + (xy[1] - target_y)**2)
        print(f"  Distance from target: {distance:.9f}")
    except Exception as e:
        print(f"{desc}: ERROR - {e}")
    print()