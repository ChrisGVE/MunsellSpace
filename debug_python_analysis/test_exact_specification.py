#!/usr/bin/env python3
"""Test the exact specification that Rust converges to"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Test the exact specification that Rust thinks matches
spec = np.array([8.548, 9.479, 7.125, 4])  # What Rust converges to
xyY = munsell_specification_to_xyY(spec)

print(f"Testing 8.548GY 9.479/7.125:")
print(f"Python xy: ({xyY[0]:.6f}, {xyY[1]:.6f})")
print(f"Rust claims: (0.328953, 0.422638)")
print(f"Difference: dx={abs(xyY[0] - 0.328953):.6f}, dy={abs(xyY[1] - 0.422638):.6f}")

# Also test with value 9.0 (what's actually used in interpolation)
spec_v9 = np.array([8.548, 9.0, 7.125, 4])
xyY_v9 = munsell_specification_to_xyY(spec_v9)
print(f"\nTesting 8.548GY 9.0/7.125 (rounded value):")
print(f"Python xy: ({xyY_v9[0]:.6f}, {xyY_v9[1]:.6f})")
print(f"Rust claims: (0.328953, 0.422638)")

# Let's also check the boundary values
print("\nBoundary values for interpolation:")
for chroma in [6.0, 8.0]:
    spec = np.array([8.548, 9.0, chroma, 4])
    xyY = munsell_specification_to_xyY(spec)
    print(f"  8.548GY 9.0/{chroma}: xy=({xyY[0]:.6f}, {xyY[1]:.6f})")