#!/usr/bin/env python3
"""Test converting YR Munsell notation back to RGB"""

import colour
from colour.notation.munsell import munsell_specification_to_xyY
import numpy as np

# Test the YR specification that Python is producing
munsell_spec = [9.5, 6.3, 7.9, 2]  # 9.5YR 6.3/7.9 (YR = code 2)
print(f"Munsell spec: {munsell_spec} (9.5YR 6.3/7.9)")

try:
    # Convert to xyY
    xyy = munsell_specification_to_xyY(munsell_spec)
    print(f"xyY: {xyy}")
    
    # Convert to XYZ
    xyz = colour.xyY_to_XYZ(xyy)
    print(f"XYZ: {xyz}")
    
    # Convert to sRGB
    srgb = colour.XYZ_to_sRGB(xyz)
    print(f"sRGB normalized: {srgb}")
    
    # Convert to 8-bit RGB
    rgb = [int(round(c * 255)) for c in srgb]
    print(f"RGB: {rgb}")
    
    print(f"Expected RGB: [0, 170, 187]")
    
    # Check if close
    expected = [0, 170, 187]
    diff = [abs(a - b) for a, b in zip(rgb, expected)]
    print(f"Difference: {diff}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()