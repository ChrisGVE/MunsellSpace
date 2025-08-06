#!/usr/bin/env python3
"""Test LCHab initial guess for green color"""

import numpy as np
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab
from colour.notation.munsell import LCHab_to_munsell_specification

# Green test case
xyy = np.array([0.3, 0.6, 0.715152])

# Convert to XYZ
xyz = xyY_to_XYZ(xyy)
print(f"xyY {xyy} -> XYZ {xyz}")

# Reference white (scaled by Y)
# Python uses custom reference white scaled by input Y
xyz_r = np.array([0.31006, 0.31616, 0.715152])  # Using Y value for reference
xyz_r = xyY_to_XYZ(xyz_r)
print(f"Reference white XYZ: {xyz_r}")

# Convert to Lab
lab = XYZ_to_Lab(xyz, xyz_r)
print(f"Lab: {lab}")

# Convert to LCHab
lchab = Lab_to_LCHab(lab)
print(f"LCHab: {lchab}")

# Initial guess from LCHab
initial_spec = LCHab_to_munsell_specification(lchab)
print(f"Initial spec from LCHab: {initial_spec}")

# What our Rust code would produce with the old complex formula
hab = lchab[2]
adjusted_angle = (hab + 18.0) % 360.0
code_complex = ((17 - ((adjusted_angle - 18.0) % 360.0 / 36.0)) % 10 + 1)
hue_complex = 10.0 - ((adjusted_angle - 18.0) % 360.0 % 36.0) * 10.0 / 36.0
print(f"\nRust OLD complex formula would produce:")
print(f"  Adjusted angle: {adjusted_angle:.1f}")
print(f"  Code: {code_complex}")
print(f"  Hue: {hue_complex:.3f}")

# What our Rust code produces with the fixed simple mapping
code_simple = (7 if hab <= 36.0 else
               6 if hab <= 72.0 else
               5 if hab <= 108.0 else
               4 if hab <= 144.0 else
               3 if hab <= 180.0 else
               2 if hab <= 216.0 else
               1 if hab <= 252.0 else
               10 if hab <= 288.0 else
               9 if hab <= 324.0 else
               8)
hue_raw = (hab % 36.0) * 10.0 / 36.0
hue_simple = 10.0 if hue_raw == 0.0 else hue_raw
print(f"\nRust NEW simple mapping produces:")
print(f"  Code: {code_simple}")
print(f"  Hue: {hue_simple:.3f}")