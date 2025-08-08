#!/usr/bin/env python3
"""Test how Python handles max chroma at high values"""

from colour import sRGB_to_XYZ
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import XYZ_to_xyY
import numpy as np

# Test several high-value greens
test_colors = [
    ([187, 255, 153], "Light green"),
    ([200, 255, 200], "Pale green"),
    ([150, 255, 150], "Bright green"),
]

print("Testing high-value green colors:")
print()

for rgb_values, name in test_colors:
    rgb = np.array(rgb_values) / 255.0
    xyz = sRGB_to_XYZ(rgb)
    xyy = XYZ_to_xyY(xyz)
    munsell = xyY_to_munsell_specification(xyy)
    
    from colour.notation.munsell import munsell_specification_to_munsell_colour
    munsell_str = munsell_specification_to_munsell_colour(munsell)
    
    print(f"RGB {rgb_values} ({name}):")
    print(f"  xyY: [{xyy[0]:.4f}, {xyy[1]:.4f}, {xyy[2]:.4f}]")
    print(f"  Munsell: {munsell_str}")
    print(f"  Value: {munsell[1]:.2f}, Chroma: {munsell[2]:.2f}")
    print()