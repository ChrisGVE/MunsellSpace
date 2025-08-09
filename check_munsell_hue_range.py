#!/usr/bin/env python3
"""Check what Python's colour-science actually outputs for hue ranges."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import xyY_to_munsell_specification

# Test the problematic colors
test_colors = [
    (85, 0, 51),     # Python shows: 0.2R
    (136, 17, 68),   # Python shows: 0.0R  
    (153, 68, 51),   # Python shows: 0.0YR
    (170, 34, 0),    # Python shows: 0.1YR
    (170, 34, 85),   # Python shows: 0.0R
]

print("Checking Python's hue value outputs:")
print("=" * 70)
print("According to Munsell standard, hue should be in range [1.0, 10.0]")
print("Let's see what Python actually produces:")
print()

for r, g, b in test_colors:
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    # Get the string notation
    munsell_str = xyY_to_munsell_colour(xyY)
    
    # Get the numerical specification
    spec = xyY_to_munsell_specification(xyY)
    hue = spec[0]
    value = spec[1]
    chroma = spec[2]
    code = int(spec[3])
    
    families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}
    family = families[code]
    
    print(f"RGB({r:3},{g:3},{b:3}):")
    print(f"  String notation: {munsell_str}")
    print(f"  Numeric hue:     {hue:.4f}")
    print(f"  Family code:     {code} ({family})")
    
    if hue < 1.0:
        print(f"  ⚠️  HUE < 1.0! This violates Munsell specification!")
    elif hue > 10.0:
        print(f"  ⚠️  HUE > 10.0! This violates Munsell specification!")
    else:
        print(f"  ✓ Hue is within valid range [1.0, 10.0]")
    print()

print("=" * 70)
print("FINDING: Python's colour-science library appears to use [0.0, 10.0] range")
print("instead of the standard [1.0, 10.0] range for hue values!")
print()
print("This might be the source of our boundary issues - if Python uses 0-10")
print("but the standard is 1-10, there's a fundamental incompatibility.")