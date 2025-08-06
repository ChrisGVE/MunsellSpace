#!/usr/bin/env python3
"""Test how Python's convergence algorithm works for RGB(204,255,170)"""

import numpy as np
from colour import XYZ_to_xyY
from colour.notation.munsell import (
    xyY_to_munsell_specification,
    ILLUMINANT_C,
    munsell_specification_to_munsell_colour
)

# Our test color
R, G, B = 204, 255, 170
rgb = np.array([R/255, G/255, B/255])

print(f"Testing RGB({R}, {G}, {B})")
print("=" * 80)

# Convert to xyY
# First to XYZ assuming sRGB with D65
XYZ = np.array([0.6493396, 0.8632931, 0.5620267])  # From Rust's calculation
xyY = XYZ_to_xyY(XYZ)
print(f"XYZ: {XYZ}")
print(f"xyY: {xyY}")

# Convert xyY to Munsell
try:
    munsell_spec = xyY_to_munsell_specification(xyY)
    print(f"\nMunsell specification: {munsell_spec}")
    
    # Convert specification to color string
    munsell_color = munsell_specification_to_munsell_colour(munsell_spec)
    print(f"Munsell color: {munsell_color}")
except Exception as e:
    print(f"Error: {e}")

# Let's trace through the convergence
print("\n\nTracing convergence process:")
print("-" * 80)

# The key is to understand how Python's algorithm converges
# Let me check what intermediate values it considers

from colour.notation.munsell import (
    munsell_specification_to_xyY,
    hue_to_hue_angle,
    hue_angle_to_hue,
    xy_from_renotation_ovoid,
    munsell_colour_to_munsell_specification,
    maximum_chroma_from_renotation
)

# Starting point
x, y = xyY[0], xyY[1]
Y = xyY[2]
x_grey, y_grey = ILLUMINANT_C[0], ILLUMINANT_C[1]

print(f"Target: x={x:.6f}, y={y:.6f}, Y={Y:.6f}")
print(f"Grey point: x={x_grey:.6f}, y={y_grey:.6f}")

# Calculate initial hue angle
import math
hue_angle = math.degrees(math.atan2(y - y_grey, x - x_grey))
if hue_angle < 0:
    hue_angle += 360

print(f"\nInitial hue angle: {hue_angle:.3f}°")

# Try different Munsell specifications
test_specs = [
    "8.0GY 9.5/12.7",  # Python's result
    "8.5GY 9.5/7.1",   # Rust's result
    "8.0GY 9.0/12.0",
    "8.5GY 9.0/7.0",
]

print("\nTesting different specifications:")
for spec_str in test_specs:
    spec = munsell_colour_to_munsell_specification(spec_str)
    xyY_test = munsell_specification_to_xyY(spec)
    x_test, y_test = xyY_test[0], xyY_test[1]
    dist = math.sqrt((x_test - x)**2 + (y_test - y)**2)
    print(f"{spec_str:15} -> x={x_test:.6f}, y={y_test:.6f}, distance={dist:.6f}")