#!/usr/bin/env python3

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

# RGB (34, 17, 119) = #221177
rgb = np.array([34, 17, 119]) / 255.0

# Convert to xyY
xyz = sRGB_to_XYZ(rgb)
xyY = XYZ_to_xyY(xyz)

print(f"RGB: {rgb * 255}")
print(f"xyY: ({xyY[0]:.10f}, {xyY[1]:.10f}, {xyY[2]:.10f})")
print()

# Get raw specification
spec = xyY_to_munsell_specification(xyY)
print(f"Python specification: [{spec[0]:.10f}, {spec[1]:.10f}, {spec[2]:.10f}, {spec[3]:.1f}]")

# Also test with exact Rust xyY values
xyY_rust = np.array([0.1753396561, 0.0867531270, 0.0207251690])
spec_rust = xyY_to_munsell_specification(xyY_rust)
print(f"Python spec (Rust xyY): [{spec_rust[0]:.10f}, {spec_rust[1]:.10f}, {spec_rust[2]:.10f}, {spec_rust[3]:.1f}]")

# Compare with what Rust reports
print("\nRust specification: [7.4603511372, 1.5544834819, 13.4780327058, 10.0]")
print("\nDifferences:")
print(f"  Hue: {7.4603511372 - spec_rust[0]:.10f}")
print(f"  Value: {1.5544834819 - spec_rust[1]:.10f}")
print(f"  Chroma: {13.4780327058 - spec_rust[2]:.10f}")