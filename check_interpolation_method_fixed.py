#!/usr/bin/env python3
"""Check what interpolation method Python uses for our test cases."""

import numpy as np
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import _xyY_to_munsell_specification, hue_to_ASTM_hue
from colour import sRGB_to_XYZ, XYZ_to_xyY

# Test red color
rgb = np.array([1.0, 0.0, 0.0])
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"Testing RGB(255, 0, 0):")
print(f"  xyY: x={xyy[0]:.8f}, y={xyy[1]:.8f}, Y={xyy[2]:.8f}")

# Get the Munsell specification
spec = _xyY_to_munsell_specification(xyy)
print(f"  Final spec: hue={spec[0]:.8f}, value={spec[1]:.8f}, chroma={spec[2]:.8f}, code={spec[3]}")

# Check ASTM hue calculations for various hue/code pairs
print("\nChecking ASTM hue calculations:")
for hue, code in [(7.86, 7), (7.9, 7), (8.0, 7), (8.2, 7), (1.67, 6), (1.67, 7)]:
    astm_hue = hue_to_ASTM_hue([hue, code])
    print(f"  hue={hue:.2f}, code={code} → ASTM_hue={astm_hue:.2f}")

# Let's also test with some known Munsell colors
print("\nTesting exact Munsell renotation entries:")
from colour.notation.munsell import munsell_specification_to_xy

# Test some exact specifications that should be in the dataset
test_specs = [
    [7.5, 5.0, 20.0, 7],  # 7.5R 5.0/20.0 - exact entry
    [10.0, 5.0, 20.0, 7],  # 10R 5.0/20.0 - exact entry
    [5.0, 5.0, 20.0, 7],   # 5R 5.0/20.0 - exact entry
]

for spec in test_specs:
    try:
        xy = munsell_specification_to_xy(spec)
        print(f"  spec={spec} → xy=({xy[0]:.6f}, {xy[1]:.6f})")
    except Exception as e:
        print(f"  spec={spec} → Error: {e}")

# Check if there's convergence difference with slightly different values
print("\nChecking convergence with slight variations:")
for offset in [0, 0.001, -0.001, 0.01, -0.01]:
    test_xyy = np.array([xyy[0] + offset, xyy[1], xyy[2]])
    test_spec = _xyY_to_munsell_specification(test_xyy)
    print(f"  x_offset={offset:+.3f} → hue={test_spec[0]:.4f}, chroma={test_spec[2]:.4f}")