#!/usr/bin/env python3

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification

# Test with exact xyY values to eliminate RGB conversion differences
test_cases = [
    # Rust's xyY for RGB(34, 17, 119)
    ([0.1753396561, 0.0867531270, 0.0207251690], "RGB(34,17,119) Rust xyY"),
    # Python's xyY for same color
    ([0.1753479176, 0.0867504734, 0.0207288827], "RGB(34,17,119) Python xyY"),
    # Pure blue xyY
    ([0.15, 0.06, 0.0722], "Pure blue approx"),
]

print("=== DIRECT XYY TO MUNSELL COMPARISON ===")
print()

for xyy, label in test_cases:
    spec = xyY_to_munsell_specification(np.array(xyy))
    print(f"{label}:")
    print(f"  xyY: ({xyy[0]:.10f}, {xyy[1]:.10f}, {xyy[2]:.10f})")
    print(f"  Specification: [{spec[0]:.10f}, {spec[1]:.10f}, {spec[2]:.10f}, {spec[3]:.1f}]")
    print()

# Compare with Rust's output
print("Rust output for RGB(34,17,119):")
print("  Specification: [7.4603511372, 1.5544834819, 13.4780327058, 10.0]")
print()
print("Difference (Rust - Python with Rust xyY):")
spec_py = xyY_to_munsell_specification(np.array([0.1753396561, 0.0867531270, 0.0207251690]))
print(f"  Hue:    {7.4603511372 - spec_py[0]:+.10f}")
print(f"  Value:  {1.5544834819 - spec_py[1]:+.10f}")
print(f"  Chroma: {13.4780327058 - spec_py[2]:+.10f}")