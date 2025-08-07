#!/usr/bin/env python3
"""Trace how Python converges for the grey color"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

# Test the problematic grey color
rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"RGB: {rgb * 255}")
print(f"xyY: ({xyy[0]:.10f}, {xyy[1]:.10f}, {xyy[2]:.10f})")
print()

# Get the final result
spec = xyY_to_munsell_specification(xyy)
print(f"Python final spec: [{spec[0]:.10f}, {spec[1]:.10f}, {spec[2]:.10f}, {int(spec[3])}]")
print(f"Python Munsell: {spec[0]:.1f}G {spec[1]:.1f}/{spec[2]:.1f}")
print()

# What Rust gets
print("Rust gets: [7.1234266911, 9.2773635406, 1.5409509919, 3.0]")
print("Rust Munsell: 7.1G 9.3/1.5")
print()

print("Difference:")
print(f"  Hue: {7.1234266911 - spec[0]:.10f}")
print(f"  Value: {9.2773635406 - spec[1]:.10f}")  
print(f"  Chroma: {1.5409509919 - spec[2]:.10f}")
print()

print("The chroma difference of -0.54 suggests our convergence is stopping too early")
print("or using a different interpolation for low chromas.")