#!/usr/bin/env python3
"""Check what interpolation method Python uses for our test cases."""

import numpy as np
from colour.notation.munsell import _xyY_to_munsell_specification
from colour.notation.munsell.renotation import interpolation_method_from_renotation_ovoid
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

# Check what interpolation method would be used for various hue/chroma values
print("\nChecking interpolation methods for various specifications:")

# Test some specific values near our convergence point
test_specs = [
    [7.86, 5.22, 20.0, 7],  # Near our convergence
    [7.86, 5.22, 21.0, 7],  # Slightly higher chroma
    [7.9, 5.22, 20.0, 7],   # Slightly different hue
    [8.0, 5.22, 20.0, 7],   # Hue 8.0
    [7.5, 5.22, 20.0, 7],   # Hue 7.5 (exact standard)
]

for spec in test_specs:
    method = interpolation_method_from_renotation_ovoid(spec)
    method_str = "None" if method is None else ("Linear" if method == 1 else "Radial")
    print(f"  spec={spec} → method={method_str}")

# Check if there's an ASTM hue calculation
from colour.notation.munsell import hue_to_ASTM_hue

print("\nChecking ASTM hue calculations:")
for hue, code in [(7.86, 7), (7.9, 7), (8.0, 7), (8.2, 7)]:
    astm_hue = hue_to_ASTM_hue([hue, code])
    print(f"  hue={hue}, code={code} → ASTM_hue={astm_hue:.2f}")