#!/usr/bin/env python3
"""Test if the value difference affects the result"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Test with both values
specs = [
    (8.548, 9.479, 7.125, 4),  # What Rust is using
    (8.548, 9.5, 7.125, 4),    # Rounded value
]

print("Testing effect of value on xy coordinates:")
for h, v, c, code in specs:
    spec = np.array([h, v, c, code])
    xyY = munsell_specification_to_xyY(spec)
    print(f"{h:.3f}GY {v:.3f}/{c:.3f} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f})")