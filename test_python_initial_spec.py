#!/usr/bin/env python3
"""Test what initial spec Python generates for red"""

import numpy as np
from colour.notation.munsell import (
    munsell_value_ASTMD1535,
    _munsell_specification_to_xyY,
    LCHab_to_munsell_specification
)
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab, XYZ_to_xy
from colour.utilities import to_domain_1, domain_range_scale

# Test red color
xyy = np.array([0.640000, 0.330000, 0.212673])
x, y, Y = xyy[0], xyy[1], to_domain_1(xyy[2])

# Convert to Lab
XYZ = xyY_to_XYZ(xyy)
x_i, y_i = 0.31006, 0.31616  # Illuminant C
X_r, Y_r, Z_r = xyY_to_XYZ([x_i, y_i, Y])
XYZ_r = np.array([(1 / Y_r) * X_r, 1, (1 / Y_r) * Z_r])
Lab = XYZ_to_Lab(XYZ, XYZ_to_xy(XYZ_r))
LCHab = Lab_to_LCHab(Lab)

print(f"Lab: L={Lab[0]:.3f}, a={Lab[1]:.3f}, b={Lab[2]:.3f}")
print(f"LCHab: L={LCHab[0]:.3f}, C={LCHab[1]:.3f}, h={LCHab[2]:.3f}")

# Get initial spec
hue_initial, _value_initial, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)
print(f"\nFrom LCHab_to_munsell_specification:")
print(f"  hue={hue_initial:.3f}, value={_value_initial:.3f}, chroma={chroma_initial:.3f}, code={code_initial}")

# Get value
with domain_range_scale("ignore"):
    value = munsell_value_ASTMD1535(Y * 100)

# Build initial spec
specification_current = [
    hue_initial,
    value,
    (5 / 5.5) * chroma_initial,
    code_initial,
]

print(f"\nInitial specification:")
print(f"  hue={specification_current[0]:.3f}")
print(f"  value={specification_current[1]:.3f}")
print(f"  chroma={specification_current[2]:.3f} (scaled from {chroma_initial:.3f})")
print(f"  code={specification_current[3]}")

# Check the position this gives
with domain_range_scale("ignore"):
    x_spec, y_spec, _ = _munsell_specification_to_xyY(specification_current)

print(f"\nPosition from initial spec: x={x_spec:.6f}, y={y_spec:.6f}")
print(f"Target position: x={x:.6f}, y={y:.6f}")