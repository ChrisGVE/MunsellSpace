#!/usr/bin/env python3
"""Understand how Python does interpolation for non-integer values"""

import numpy as np
from colour.notation.munsell import (
    munsell_specification_to_xyY,
    xy_from_renotation_ovoid,
    munsell_colour_to_munsell_specification
)

# Test case: 8.0GY 9.5/12.7
munsell_str = "8.0GY 9.5/12.7"
print(f"Testing: {munsell_str}")

try:
    spec = munsell_colour_to_munsell_specification(munsell_str)
    print(f"Specification: {spec}")
except Exception as e:
    print(f"Can't parse directly: {e}")
    # Create manually
    spec = np.array([8.0, 9.5, 12.7, 4.0])
    print(f"Manual specification: {spec}")

# This should work even with non-integer value
xyY = munsell_specification_to_xyY(spec)
print(f"\nmunsell_specification_to_xyY result: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")

# Now let's see what happens for integer values above and below
print("\n\nTesting interpolation between value planes:")
for value in [9.0, 9.5, 10.0]:
    # For testing, use even chroma
    spec_test = np.array([8.0, value, 12.0, 4.0])
    try:
        xyY_test = munsell_specification_to_xyY(spec_test)
        print(f"Value {value}: x={xyY_test[0]:.6f}, y={xyY_test[1]:.6f}, Y={xyY_test[2]:.6f}")
    except Exception as e:
        print(f"Value {value}: ERROR - {e}")

# The key difference: munsell_specification_to_xyY handles interpolation
# while xy_from_renotation_ovoid is just for direct lookups

print("\n\nComparing different chromas at value 9:")
for chroma in [12.0, 12.7, 14.0]:
    spec_test = np.array([8.0, 9.0, chroma, 4.0])
    try:
        xyY_test = munsell_specification_to_xyY(spec_test)
        print(f"Chroma {chroma}: x={xyY_test[0]:.6f}, y={xyY_test[1]:.6f}")
    except Exception as e:
        print(f"Chroma {chroma}: ERROR - {e}")

# Now test our problematic case with Rust's values
print("\n\nTesting Rust's convergence point: 8.548GY 9.479/7.125")
spec_rust = np.array([8.548, 9.479, 7.125, 4.0])
try:
    xyY_rust = munsell_specification_to_xyY(spec_rust)
    print(f"Result: x={xyY_rust[0]:.6f}, y={xyY_rust[1]:.6f}, Y={xyY_rust[2]:.6f}")
    
    # Compare with our target
    target_x, target_y = 0.328945, 0.422625
    dist = np.sqrt((target_x - xyY_rust[0])**2 + (target_y - xyY_rust[1])**2)
    print(f"Distance from target: {dist:.6f}")
except Exception as e:
    print(f"ERROR: {e}")

# Test exact integer/even values for comparison
print("\n\nTesting nearby integer/even values:")
for v, c in [(9, 6), (9, 8), (10, 6), (10, 8)]:
    spec_test = np.array([8.548, v, c, 4.0])
    try:
        xy = xy_from_renotation_ovoid(spec_test) if v <= 9 else None
        if xy:
            print(f"8.548GY {v}/{c}: xy=({xy[0]:.6f}, {xy[1]:.6f}) [ovoid lookup]")
        xyY = munsell_specification_to_xyY(spec_test)
        print(f"8.548GY {v}/{c}: xy=({xyY[0]:.6f}, {xyY[1]:.6f}) [full conversion]")
    except Exception as e:
        print(f"8.548GY {v}/{c}: ERROR - {e}")