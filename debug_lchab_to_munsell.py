#!/usr/bin/env python3
"""Debug the LCHab to Munsell specification conversion"""

import numpy as np
from colour.notation.munsell import (
    xyY_to_munsell_specification,
    _LCHab_to_munsell_specification
)
from colour.models import XYZ_to_Lab, Lab_to_LCHab
from colour import CCS_ILLUMINANTS

# RGB(221, 238, 238) in xyY
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing LCHab to Munsell conversion for RGB(221, 238, 238)")
print(f"xyY: {xyY}")
print()

# Calculate LCHab as initial spec
x, y, Y = xyY
X = x * Y / y
Z = (1.0 - x - y) * Y / y
XYZ = np.array([X, Y, Z])

Lab = XYZ_to_Lab(XYZ, CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"])
LCHab = Lab_to_LCHab(Lab)
print(f"LCHab: {LCHab}")
print(f"  L* = {LCHab[0]:.6f}")
print(f"  C* = {LCHab[1]:.6f}")
print(f"  H  = {LCHab[2]:.6f}")
print()

# Convert LCHab to Munsell specification
munsell_spec = _LCHab_to_munsell_specification(LCHab)
print(f"Munsell spec from LCHab: {munsell_spec}")
print(f"  Hue:    {munsell_spec[0]:.6f}")
print(f"  Value:  {munsell_spec[1]:.6f}")
print(f"  Chroma: {munsell_spec[2]:.6f}")
print(f"  Code:   {munsell_spec[3]}")
print()

# Compare with final result
final_spec = xyY_to_munsell_specification(xyY)
print(f"Final Munsell spec: {final_spec}")
print(f"  Hue:    {final_spec[0]:.6f}")
print(f"  Value:  {final_spec[1]:.6f}")
print(f"  Chroma: {final_spec[2]:.6f}")
print(f"  Code:   {final_spec[3]}")
print()

print("Key observation:")
print(f"  LCHab to Munsell gives chroma: {munsell_spec[2]:.6f}")
print(f"  Final converged chroma: {final_spec[2]:.6f}")
print(f"  Ratio: {final_spec[2] / munsell_spec[2]:.6f}")