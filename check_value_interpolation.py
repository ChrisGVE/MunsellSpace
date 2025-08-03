#!/usr/bin/env python3
"""Check how Python handles non-integer values in the full conversion."""

import numpy as np
from colour.notation.munsell import _munsell_specification_to_xyY
from colour.algebra import euclidean_distance

# Our target
target_xyy = np.array([0.640074499457, 0.329970510632, 0.212600000000])

# Test with exact value from our algorithm
spec_exact = [7.860852, 5.219872126711, 20.860931, 7]
print("Testing with non-integer value (5.219872):")
print(f"  spec: {spec_exact}")
xyy = _munsell_specification_to_xyY(spec_exact)
print(f"  → xyY: x={xyy[0]:.12f}, y={xyy[1]:.12f}, Y={xyy[2]:.12f}")
dist = euclidean_distance([xyy[0], xyy[1]], [target_xyy[0], target_xyy[1]])
print(f"  → distance from target: {dist:.12e}")

# Test with floor value
spec_floor = [7.860852, 5.0, 20.860931, 7]
print("\nTesting with floor value (5.0):")
print(f"  spec: {spec_floor}")
xyy_floor = _munsell_specification_to_xyY(spec_floor)
print(f"  → xyY: x={xyy_floor[0]:.12f}, y={xyy_floor[1]:.12f}, Y={xyy_floor[2]:.12f}")

# Test with ceiling value
spec_ceil = [7.860852, 6.0, 20.860931, 7]
print("\nTesting with ceiling value (6.0):")
print(f"  spec: {spec_ceil}")
xyy_ceil = _munsell_specification_to_xyY(spec_ceil)
print(f"  → xyY: x={xyy_ceil[0]:.12f}, y={xyy_ceil[1]:.12f}, Y={xyy_ceil[2]:.12f}")

# Let's trace what Python's internal function does
print("\n\nChecking internal conversion path:")
from colour.notation.munsell.renotation import (
    xy_from_renotation_ovoid,
    xyY_from_renotation
)

# This is what gets called for non-integer values
spec = [7.860852, 5.219872126711, 20.860931, 7]
print(f"For spec: {spec}")

# Python internally calls xy_from_renotation_ovoid
try:
    xy_ovoid = xy_from_renotation_ovoid(spec)
    print(f"  xy_from_renotation_ovoid: ({xy_ovoid[0]:.12f}, {xy_ovoid[1]:.12f})")
except Exception as e:
    print(f"  xy_from_renotation_ovoid error: {e}")

# For exact match, it would call xyY_from_renotation
spec_exact_match = [7.5, 5.0, 20.0, 7]
print(f"\nFor exact match spec: {spec_exact_match}")
try:
    xyy_exact = xyY_from_renotation(spec_exact_match)
    print(f"  xyY_from_renotation: x={xyy_exact[0]:.12f}, y={xyy_exact[1]:.12f}, Y={xyy_exact[2]:.12f}")
except Exception as e:
    print(f"  Error: {e}")