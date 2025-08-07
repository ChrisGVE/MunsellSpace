#!/usr/bin/env python3
"""Analyze the pattern of low-chroma interpolation in Python"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour import sRGB_to_XYZ, XYZ_to_xyY

# Test colors with low chroma
test_cases = [
    ([221, 238, 238], "Near grey - high value"),
    ([128, 130, 128], "Near grey - mid value"),  
    ([50, 51, 50], "Near grey - low value"),
]

print("=== LOW CHROMA INTERPOLATION ANALYSIS ===")
print()

for rgb, description in test_cases:
    rgb_norm = np.array(rgb) / 255.0
    xyz = sRGB_to_XYZ(rgb_norm)
    xyy = XYZ_to_xyY(xyz)
    
    spec = xyY_to_munsell_specification(xyy)
    
    print(f"{description}:")
    print(f"  RGB: {rgb}")
    print(f"  xyY: ({xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f})")
    print(f"  Spec: [{spec[0]:.3f}, {spec[1]:.3f}, {spec[2]:.3f}, {int(spec[3])}]")
    print(f"  Value: {spec[1]:.3f} (floor={np.floor(spec[1]):.0f}, ceil={np.ceil(spec[1]):.0f})")
    print(f"  Chroma: {spec[2]:.3f}")
    
    # Key insight: For low chromas, does Python handle value interpolation differently?
    if spec[2] < 2.0:
        print(f"  -> Low chroma case: Would interpolate between grey and chroma 2")
        print(f"     At value {spec[1]:.3f}, need to handle non-integer carefully")
    print()

print("Key Questions:")
print("1. How does Python get xy at chroma 2 for non-integer values?")
print("2. Does Python use a different grey point for different values?")
print("3. Is the interpolation linear in xy space or some other space?")