#!/usr/bin/env python3
"""Test how Python handles max chroma for high values"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification, munsell_specification_to_xyY

# Test xyY for RGB(221, 238, 238)
xyy = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing Python's convergence for RGB(221, 238, 238):")
print(f"xyY: {xyy}")
print()

# Convert to Munsell
spec = xyY_to_munsell_specification(xyy)
print(f"Final Munsell spec: {spec}")
print(f"  Hue:    {spec[0]:.6f}")
print(f"  Value:  {spec[1]:.6f}")
print(f"  Chroma: {spec[2]:.6f}")
print(f"  Code:   {spec[3]}")

# Now test what xy Python gets for the converged spec
xy_final = munsell_specification_to_xyY(spec)
print(f"\nxyY from final spec: {xy_final}")
print(f"  Distance from target: {np.linalg.norm(xy_final[:2] - xyy[:2]):.9f}")

# Test what xy we get for intermediate specs with value=9.277
test_specs = [
    np.array([7.1, 9.0, 2.0, 3]),    # Value 9, chroma 2
    np.array([7.1, 9.277, 2.0, 3]),  # Value 9.277, chroma 2
    np.array([7.1, 9.0, 1.5, 3]),    # Value 9, chroma 1.5
    np.array([7.1, 9.277, 1.5, 3]),  # Value 9.277, chroma 1.5
]

print("\nTesting intermediate specs:")
for spec in test_specs:
    try:
        xy = munsell_specification_to_xyY(spec)
        print(f"  Spec [{spec[0]:.1f}, {spec[1]:.3f}, {spec[2]:.1f}, {int(spec[3])}]: xy=({xy[0]:.6f}, {xy[1]:.6f})")
    except Exception as e:
        print(f"  Spec [{spec[0]:.1f}, {spec[1]:.3f}, {spec[2]:.1f}, {int(spec[3])}]: ERROR - {e}")