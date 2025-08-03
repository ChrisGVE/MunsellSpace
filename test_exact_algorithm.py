#!/usr/bin/env python3
"""Test exact algorithm behavior to understand what Python does."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import _xyY_to_munsell_specification
from colour.notation.munsell import xyY_to_munsell_colour
from colour.notation.munsell import munsell_value_ASTMD1535

# Test RGB(255,0,0)
rgb = np.array([1.0, 0.0, 0.0])
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print("Input:")
print(f"  RGB: {rgb}")
print(f"  XYZ (D65): {xyz}")
print(f"  xyY (D65): {xyy}")

# Direct conversion
munsell = xyY_to_munsell_colour(xyy)
print(f"\nDirect conversion result: {munsell}")

# Get specification details
spec = _xyY_to_munsell_specification(xyy)
print(f"\nSpecification: {spec}")
print(f"  Hue: {spec[0]:.6f}")
print(f"  Value: {spec[1]:.6f}") 
print(f"  Chroma: {spec[2]:.6f}")
print(f"  Code: {spec[3]:.6f}")

# Check value calculation
Y = xyy[2]
value = munsell_value_ASTMD1535(Y)
print(f"\nValue calculation:")
print(f"  Y = {Y:.6f}")
print(f"  Munsell Value (raw) = {value:.6f}")
print(f"  Munsell Value (scaled to 0-10) = {value * 10:.6f}")

# Check if there's a Y scaling issue
print(f"\nY scaling check:")
print(f"  Y * 0.975 = {Y * 0.975:.6f}")
print(f"  Y / 0.975 = {Y / 0.975:.6f}")