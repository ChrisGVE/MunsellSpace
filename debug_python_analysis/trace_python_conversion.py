#!/usr/bin/env python3
"""Trace through Python's actual conversion process"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import munsell_colour_to_munsell_specification

# Test RGB(204, 255, 170) 
rgb = np.array([204, 255, 170]) / 255.0
print(f"Starting with RGB: {rgb * 255}")

# Convert to XYZ
XYZ = sRGB_to_XYZ(rgb)
print(f"XYZ: {XYZ}")

# Convert to xyY
xyY = XYZ_to_xyY(XYZ)
print(f"xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")

# Convert to Munsell
munsell_str = xyY_to_munsell_colour(xyY)
print(f"\nMunsell string: {munsell_str}")

# Get specification
spec = munsell_colour_to_munsell_specification(munsell_str)
print(f"Specification: hue={spec[0]:.3f}, value={spec[1]:.3f}, chroma={spec[2]:.3f}, code={spec[3]}")

# Now let's trace the reverse - what xy does Python calculate for this Munsell spec?
print("\n\nReverse conversion:")
from colour.notation.munsell import munsell_specification_to_xyY

# Test with the exact specification
xyY_reverse = munsell_specification_to_xyY(spec)
print(f"Munsell {munsell_str} -> xyY: x={xyY_reverse[0]:.6f}, y={xyY_reverse[1]:.6f}, Y={xyY_reverse[2]:.6f}")

# Calculate distance
dist = np.sqrt((xyY[0] - xyY_reverse[0])**2 + (xyY[1] - xyY_reverse[1])**2)
print(f"Distance between original and reverse: {dist:.8f}")

# Now let's test what happens with integer value and even chroma
print("\n\nTesting with constraints for xy_from_renotation_ovoid:")
print("(Integer value, even chroma)")

# Round to nearest valid values
value_int = round(spec[1])
chroma_even = 2 * round(spec[2] / 2)
spec_constrained = np.array([spec[0], value_int, chroma_even, spec[3]])

print(f"\nConstrained spec: hue={spec_constrained[0]:.3f}, value={spec_constrained[1]}, chroma={spec_constrained[2]}, code={spec_constrained[3]}")

from colour.notation.munsell import xy_from_renotation_ovoid
try:
    xy_ovoid = xy_from_renotation_ovoid(spec_constrained)
    print(f"xy_from_renotation_ovoid result: ({xy_ovoid[0]:.6f}, {xy_ovoid[1]:.6f})")
except Exception as e:
    print(f"Error: {e}")

# Test the interpolation that must be happening
print("\n\nUnderstanding the interpolation:")
print("Python must be doing value interpolation since spec has value=9.479")
print("Let's manually check value 9 and 10:")

for v in [9, 10]:
    spec_v = np.array([spec[0], v, chroma_even, spec[3]])
    try:
        xy_v = xy_from_renotation_ovoid(spec_v)
        print(f"  Value {v}: xy=({xy_v[0]:.6f}, {xy_v[1]:.6f})")
    except Exception as e:
        print(f"  Value {v}: {e}")

# The key insight: munsell_specification_to_xyY must handle non-integer values
# and non-even chromas through interpolation!