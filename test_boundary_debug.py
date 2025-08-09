#!/usr/bin/env python3
"""Debug why boundary fix isn't working for all colors."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification, hue_to_hue_angle, hue_angle_to_hue

def test_color(r, g, b):
    """Test a single color."""
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    # Get Python's specification
    spec = xyY_to_munsell_specification(xyY)
    
    # Get the hue angle
    angle = hue_to_hue_angle([spec[0], spec[3]])
    
    # Map code to family
    families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}
    family = families.get(int(spec[3]), '?')
    
    print(f"RGB({r:3},{g:3},{b:3}):")
    print(f"  xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
    print(f"  Spec: hue={spec[0]:.4f}, value={spec[1]:.4f}, chroma={spec[2]:.4f}, code={spec[3]}")
    print(f"  Family: {family}")
    print(f"  Hue angle: {angle:.4f}°")
    print()

# Test the misclassified colors
misclassified = [
    (68, 102, 68),   # 10.0GY→0.0G
    (85, 0, 51),     # 0.2R→10.0RP
    (119, 85, 221),  # 10.0PB→0.0P
    (136, 17, 68),   # 0.1R→10.0RP
    (153, 68, 51),   # 0.0YR→10.0R
    (170, 34, 0),    # 0.1YR→10.0R
    (170, 34, 85),   # 0.0R→10.0RP
    (221, 85, 204),  # 10.0P→0.0RP  (FIXED)
    (255, 238, 238), # 0.0Y→10.0YR  (FIXED)
]

print("=" * 70)
print("Python specifications for problematic colors:")
print("=" * 70)

for rgb in misclassified:
    test_color(*rgb)

print("=" * 70)
print("KEY OBSERVATIONS:")
print("- Colors with hue exactly 0.0 or 10.0 are problematic")
print("- Hue < 0.1 or hue > 9.9 triggers the boundary issue")
print("- The boundary fix should detect these and try both interpretations")