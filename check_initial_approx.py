#!/usr/bin/env python3
"""Check how Python and Rust differ in their initial approximations."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY, XYZ_to_Lab
from colour.notation.munsell import Lab_to_LCHab, hue_angle_to_hue
import numpy as np

def check_color(r, g, b):
    """Check initial approximation for a color."""
    # Python's approach
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    # Convert to Lab and LCHab for initial hue angle
    Lab = XYZ_to_Lab(XYZ)
    LCHab = Lab_to_LCHab(Lab)
    
    # Get initial hue angle from LCHab
    initial_angle = LCHab[2]
    
    # Convert to Munsell hue and code
    hue_initial, code_initial = hue_angle_to_hue(initial_angle)
    
    families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}
    
    print(f"RGB({r:3},{g:3},{b:3}):")
    print(f"  xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
    print(f"  Lab: L={Lab[0]:.4f}, a={Lab[1]:.4f}, b={Lab[2]:.4f}")
    print(f"  LCHab: L={LCHab[0]:.4f}, C={LCHab[1]:.4f}, H={LCHab[2]:.4f}°")
    print(f"  Initial hue angle: {initial_angle:.4f}°")
    print(f"  Initial Munsell: hue={hue_initial:.4f}, code={code_initial} ({families[code_initial]})")
    print()

# Test the problematic boundary colors
colors = [
    (68, 102, 68),   # Python: 10.0GY, Rust: 0.0G
    (85, 0, 51),     # Python: 0.2R, Rust: 10.0RP
    (119, 85, 221),  # Python: 10.0PB, Rust: 0.0P
]

print("Initial approximations from LCHab:")
print("=" * 70)

for r, g, b in colors:
    check_color(r, g, b)

print("=" * 70)
print("KEY OBSERVATION:")
print("The initial hue angle from LCHab determines which family we start in.")
print("Small differences in this calculation can lead to different convergence paths.")