#!/usr/bin/env python3
"""Check xy coordinates for RP specification"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Rust's specification: hue=0.628, value=1.313, chroma=8.117, code=8 (RP)
hue = 0.628
value = 1.313
chroma = 8.117
code = 8

munsell_spec = np.array([hue, value, chroma, code])
xyy = munsell_specification_to_xyY(munsell_spec)

print(f"Munsell specification: {hue:.3f}RP {value:.3f}/{chroma:.3f}")
print(f"Python xy: ({xyy[0]:.6f}, {xyy[1]:.6f})")
print(f"Rust xy: (0.339663, 0.165219)")
print(f"\nDifference:")
print(f"  x: {xyy[0] - 0.339663:.6f}")
print(f"  y: {xyy[1] - 0.165219:.6f}")

# Let's also check what happens with value=1.312891 (the exact value)
value_exact = 1.312891
munsell_spec2 = np.array([hue, value_exact, chroma, code])
xyy2 = munsell_specification_to_xyY(munsell_spec2)
print(f"\nWith exact value {value_exact}:")
print(f"Python xy: ({xyy2[0]:.6f}, {xyy2[1]:.6f})")