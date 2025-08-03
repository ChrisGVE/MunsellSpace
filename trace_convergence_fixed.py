#!/usr/bin/env python3
"""Trace exact convergence steps by examining intermediate values."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import _xyY_to_munsell_specification, _munsell_specification_to_xyY
from colour.algebra import euclidean_distance

# Test colors
test_colors = [
    ([255, 0, 0], "Red"),
]

for rgb, name in test_colors:
    print(f"\n{name} ({rgb[0]}, {rgb[1]}, {rgb[2]}):")
    
    # Convert to xyY
    rgb_norm = np.array([c/255.0 for c in rgb])
    xyz = sRGB_to_XYZ(rgb_norm)
    xyy = XYZ_to_xyY(xyz)
    
    print(f"  Input xyY: x={xyy[0]:.12f}, y={xyy[1]:.12f}, Y={xyy[2]:.12f}")
    
    # Get Munsell specification
    spec = _xyY_to_munsell_specification(xyy)
    print(f"  Output spec: hue={spec[0]:.12f}, value={spec[1]:.12f}, chroma={spec[2]:.12f}, code={spec[3]}")
    
    # Let's check a few iterations manually
    print("\n  Checking convergence by converting back...")
    
    for i in range(5):
        # Convert spec back to xyY
        xyy_back = _munsell_specification_to_xyY(spec)
        
        # Calculate distance
        diff_x = xyy[0] - xyy_back[0]
        diff_y = xyy[1] - xyy_back[1]
        distance = euclidean_distance([xyy[0], xyy[1]], [xyy_back[0], xyy_back[1]])
        
        print(f"    Iteration {i}: distance={distance:.12e}")
        print(f"      xyY_back: x={xyy_back[0]:.12f}, y={xyy_back[1]:.12f}")
        print(f"      diff: dx={diff_x:.12e}, dy={diff_y:.12e}")
        
        if distance < 1e-7:
            print(f"    Would converge at iteration {i}")
            break
        
        # For next iteration, convert the back value to a new spec
        # This simulates what the algorithm might be doing
        spec = _xyY_to_munsell_specification(xyy_back)
        print(f"      New spec: hue={spec[0]:.8f}, value={spec[1]:.8f}, chroma={spec[2]:.8f}")

print("\n\nLet's check if our Rust implementation matches Python's initial calculations...")
print("Key things to verify:")
print("1. Initial guess calculation (Lab/LCHab conversion)")
print("2. Chroma scaling factor (5/5.5)")
print("3. Maximum chroma boundary check")
print("4. Exact convergence distance calculation")