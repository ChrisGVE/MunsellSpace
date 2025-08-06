#!/usr/bin/env python3
"""Compare boundary xy values between Python and Rust"""

import numpy as np
from colour.notation.munsell import (
    xy_from_renotation_ovoid,
    munsell_colour_to_munsell_specification,
    bounding_hues_from_renotation
)

# Test the exact case where Rust and Python differ
print("Comparing boundary values for 8.548GY 9/6:")
print("=" * 80)

# Get the boundary hues
spec = np.array([8.548, 9, 6, 4])  # Must use integer value for xy_from_renotation_ovoid
hue_code = spec[:2]
bounds = bounding_hues_from_renotation(hue_code)

print(f"\nBoundary hues for 8.548GY:")
print(f"  Clockwise (minus): {bounds[0]}")
print(f"  Counter-clockwise (plus): {bounds[1]}")

# Get xy for each boundary at the test chroma
print("\nBoundary xy values at chroma=6:")
# CW boundary
spec_cw = np.array([bounds[0][0], 9, 6, int(bounds[0][1])])
xy_cw = xy_from_renotation_ovoid(spec_cw)
print(f"  CW  ({bounds[0][0]}GY): xy=({xy_cw[0]:.6f}, {xy_cw[1]:.6f})")

# CCW boundary
spec_ccw = np.array([bounds[1][0], 9, 6, int(bounds[1][1])])
xy_ccw = xy_from_renotation_ovoid(spec_ccw)
print(f"  CCW ({bounds[1][0]}GY): xy=({xy_ccw[0]:.6f}, {xy_ccw[1]:.6f})")

# Also test chroma=8 for completeness
print("\nBoundary xy values at chroma=8:")
spec_cw_8 = np.array([bounds[0][0], 9, 8, int(bounds[0][1])])
xy_cw_8 = xy_from_renotation_ovoid(spec_cw_8)
print(f"  CW  ({bounds[0][0]}GY): xy=({xy_cw_8[0]:.6f}, {xy_cw_8[1]:.6f})")

spec_ccw_8 = np.array([bounds[1][0], 9, 8, int(bounds[1][1])])
xy_ccw_8 = xy_from_renotation_ovoid(spec_ccw_8)
print(f"  CCW ({bounds[1][0]}GY): xy=({xy_ccw_8[0]:.6f}, {xy_ccw_8[1]:.6f})")

# Compare with what Rust claims
print("\n\nRust claims for same boundaries:")
print("  CW  (7.5GY): xy=(0.335100, 0.411100) for chroma=6")
print("  CCW (10.0GY): xy=(0.315300, 0.400800) for chroma=6")
print("  CW  (7.5GY): xy=(0.341400, 0.441500) for chroma=8")  
print("  CCW (10.0GY): xy=(0.315700, 0.425900) for chroma=8")

# Calculate what the interpolation should give
print("\n\nManual interpolation calculation:")
# 8.548 is between 7.5 and 10.0
# Hue angles: 7.5GY = 82.5°, 8.548GY = ?, 10.0GY = 110°
from colour.notation.munsell import hue_to_hue_angle
angle_75 = hue_to_hue_angle(7.5, 4)
angle_8548 = hue_to_hue_angle(8.548, 4)
angle_100 = hue_to_hue_angle(10.0, 4)

print(f"\nHue angles:")
print(f"  7.5GY:   {angle_75:.3f}°")
print(f"  8.548GY: {angle_8548:.3f}°")
print(f"  10.0GY:  {angle_100:.3f}°")

# For radial interpolation, we need to work in polar coordinates
from colour.notation.munsell import ILLUMINANT_C
x_grey, y_grey = ILLUMINANT_C

print(f"\nIlluminant C (grey point): ({x_grey}, {y_grey})")

# Convert to polar for chroma=6
import math
rho_cw_6 = math.sqrt((xy_cw[0] - x_grey)**2 + (xy_cw[1] - y_grey)**2)
phi_cw_6 = math.atan2(xy_cw[1] - y_grey, xy_cw[0] - x_grey)
rho_ccw_6 = math.sqrt((xy_ccw[0] - x_grey)**2 + (xy_ccw[1] - y_grey)**2)
phi_ccw_6 = math.atan2(xy_ccw[1] - y_grey, xy_ccw[0] - x_grey)

print(f"\nPolar coordinates for chroma=6:")
print(f"  CW:  rho={rho_cw_6:.6f}, phi={math.degrees(phi_cw_6):.3f}°")
print(f"  CCW: rho={rho_ccw_6:.6f}, phi={math.degrees(phi_ccw_6):.3f}°")