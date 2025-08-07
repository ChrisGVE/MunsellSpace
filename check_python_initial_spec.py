#!/usr/bin/env python3
"""Check Python's initial specification calculation"""

import numpy as np
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab
from colour.notation.munsell import (
    _munsell_value_ASTMD1535,
    _LCHab_to_munsell_specification
)

# RGB(221, 238, 238) in xyY
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing initial specification for RGB(221, 238, 238)")
print(f"xyY: {xyY}")
print()

# Convert to XYZ
XYZ = xyY_to_XYZ(xyY)
print(f"XYZ: {XYZ}")

# Convert to Munsell value
value = _munsell_value_ASTMD1535(xyY[2] * 100)
print(f"Value: {value:.6f}")

# Illuminant C in xy
illuminant_C_xy = np.array([0.31006, 0.31616])
illuminant_C_xyY = np.array([illuminant_C_xy[0], illuminant_C_xy[1], xyY[2]])
XYZ_r = xyY_to_XYZ(illuminant_C_xyY)
print(f"Reference XYZ (Illuminant C): {XYZ_r}")

# Convert to Lab
Lab = XYZ_to_Lab(XYZ, XYZ_r)
print(f"Lab: {Lab}")

# Convert to LCHab
LCHab = Lab_to_LCHab(Lab)
print(f"LCHab: {LCHab}")

# Convert to initial Munsell specification
initial_spec = _LCHab_to_munsell_specification(LCHab)
print(f"Initial spec (from LCHab): {initial_spec}")

# Check the chroma scaling
print()
print(f"LCHab chroma: {LCHab[1]:.6f}")
print(f"Initial Munsell chroma: {initial_spec[2]:.6f}")
print(f"Ratio: {initial_spec[2] / LCHab[1]:.6f}")

# What Rust is doing
rust_scaled_chroma = (5.0 / 5.5) * initial_spec[2]
print(f"Rust scaled chroma (5.0/5.5): {rust_scaled_chroma:.6f}")
print(f"This is why Rust starts with chroma ~1.98 instead of ~2.17")