#!/usr/bin/env python3
"""Debug angle calculation difference"""

import colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np

# Test case that shows mismatch: RGB [0, 64, 64]
rgb = [0, 64, 64]
srgb = [c / 255.0 for c in rgb]
xyz = colour.sRGB_to_XYZ(srgb)
xyy = colour.XYZ_to_xyY(xyz)

print(f"RGB {rgb}")
print(f"xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")

# Illuminant C
x_c, y_c = 0.31006, 0.31616

# Calculate angle
x, y = xyy[0], xyy[1]
dx = x - x_c
dy = y - y_c

print(f"\nCoordinates relative to Illuminant C:")
print(f"  dx = {dx:.6f}")
print(f"  dy = {dy:.6f}")

# Python's atan2
angle = np.arctan2(dy, dx) * 180 / np.pi
if angle < 0:
    angle += 360

print(f"\nHue angle (Python): {angle:.1f}°")

# Get Munsell specification
spec = xyY_to_munsell_specification(xyy)
print(f"\nPython Munsell spec: {spec[0]:.1f}{['', 'R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP'][int(spec[3])]} {spec[1]:.1f}/{spec[2]:.1f}")

# Now check what hue_angle_to_hue thinks
from colour.notation.munsell import hue_angle_to_hue
hue, code = hue_angle_to_hue(angle)
print(f"hue_angle_to_hue({angle:.1f}°) -> {hue:.1f}, code {code}")

# Print what the spec thinks the angle should be
from colour.notation.munsell import hue_to_hue_angle
spec_angle = hue_to_hue_angle([spec[0], int(spec[3])])
print(f"\nSpec's hue angle: {spec_angle:.1f}°")