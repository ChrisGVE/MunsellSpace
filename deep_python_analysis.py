#!/usr/bin/env python3
"""Deep analysis of Python's exact Munsell conversion algorithm."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import _xyY_to_munsell_specification
from colour.constants import EPSILON

# Test colors
test_colors = [
    ([255, 0, 0], "Red"),
    ([0, 255, 0], "Green"),
    ([255, 165, 0], "Orange"),
    ([128, 0, 128], "Purple"),
    ([0, 255, 255], "Cyan"),
    ([255, 0, 255], "Magenta"),
]

for rgb, name in test_colors:
    print(f"\n{name} ({rgb[0]}, {rgb[1]}, {rgb[2]}):")
    
    # Convert to xyY
    rgb_norm = np.array([c/255.0 for c in rgb])
    xyz = sRGB_to_XYZ(rgb_norm)
    xyy = XYZ_to_xyY(xyz)
    
    print(f"  xyY: x={xyy[0]:.8f}, y={xyy[1]:.8f}, Y={xyy[2]:.8f}")
    
    # Get Munsell specification (internal format)
    spec = _xyY_to_munsell_specification(xyy)
    print(f"  Specification: hue={spec[0]:.8f}, value={spec[1]:.8f}, chroma={spec[2]:.8f}, code={spec[3]}")
    
    # Get Munsell notation (string format)
    munsell = xyY_to_munsell_colour(xyy)
    print(f"  Munsell: {munsell}")

# Check convergence threshold
print(f"\nPython's convergence threshold: {EPSILON / 1e4}")
print("This is 1e-3 / 1e4 = 1e-7")

# Check iteration limits
print("\nChecking iteration limits from source...")
from colour.notation.munsell import _xyY_to_munsell_specification
import inspect
source = inspect.getsource(_xyY_to_munsell_specification)
for line in source.split('\n'):
    if 'iterations' in line.lower() and '=' in line:
        print(f"  {line.strip()}")