#!/usr/bin/env python3
"""Investigate the hue angle to family mapping difference"""

import colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np

# Test specific colors where we see the mismatch
test_cases = [
    ([0, 64, 64], "3.6YR vs 3.7BG"),
    ([0, 128, 128], "4.7YR vs 4.7BG"),
]

for rgb, note in test_cases:
    print(f"\nRGB {rgb} ({note}):")
    
    srgb = [c / 255.0 for c in rgb]
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    
    print(f"  xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
    
    # Get the Munsell spec from Python
    spec = xyY_to_munsell_specification(xyy)
    print(f"  Python spec: [{spec[0]:.2f}, {spec[1]:.2f}, {spec[2]:.2f}, {int(spec[3])}]")
    
    # The spec[3] is the hue code
    HUE_CODES = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                 6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
    print(f"  Python family: {HUE_CODES[int(spec[3])]} (code {int(spec[3])})")
    
    # Calculate the hue angle from xy
    x, y = xyy[0], xyy[1]
    x_c, y_c = 0.31006, 0.31616  # Illuminant C
    
    # Convert to polar
    dx = x - x_c
    dy = y - y_c
    angle = np.arctan2(dy, dx) * 180 / np.pi
    if angle < 0:
        angle += 360
    
    print(f"  Hue angle from xy: {angle:.1f}°")
    
    # Check what Python thinks the hue angle should be
    from colour.notation.munsell import hue_to_hue_angle
    python_angle = hue_to_hue_angle(spec[0], int(spec[3]))
    print(f"  Python's hue angle: {python_angle:.1f}°")