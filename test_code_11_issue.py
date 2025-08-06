#!/usr/bin/env python3
"""Debug code 11 issue"""

import numpy as np
from colour.notation.munsell import (
    xyY_to_munsell_specification,
    LCHab_to_munsell_specification
)
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab, XYZ_to_xy
from colour.utilities import to_domain_1, domain_range_scale

# Blue that's causing code 11
xyy = np.array([0.15, 0.06, 0.072175])
x, y, Y = xyy[0], xyy[1], to_domain_1(xyy[2])

# Convert to Lab
XYZ = xyY_to_XYZ(xyy)
x_i, y_i = 0.31006, 0.31616  # Illuminant C
X_r, Y_r, Z_r = xyY_to_XYZ([x_i, y_i, Y])
XYZ_r = np.array([(1 / Y_r) * X_r, 1, (1 / Y_r) * Z_r])
Lab = XYZ_to_Lab(XYZ, XYZ_to_xy(XYZ_r))
LCHab = Lab_to_LCHab(Lab)

print(f"Blue: xyY = [{x:.3f}, {y:.3f}, {Y:.3f}]")
print(f"  Lab: L={Lab[0]:.3f}, a={Lab[1]:.3f}, b={Lab[2]:.3f}")
print(f"  LCHab: L={LCHab[0]:.3f}, C={LCHab[1]:.3f}, h={LCHab[2]:.3f}")

# Get initial spec
hue_initial, _value_initial, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)
print(f"  Initial spec from LCHab: hue={hue_initial:.3f}, value={_value_initial:.3f}, chroma={chroma_initial:.3f}, code={code_initial}")

# Manual calculation from the hue angle
# h = 306.579 degrees
# This maps to:
# 288-324: code 9 (P)
# 324-360: code 8 (RP)
# So 306.579 should be code 9
print(f"\nManual hue angle analysis:")
print(f"  Hue angle 306.579 should map to code 9 (P)")
print(f"  288 < 306.579 < 324, so code should be 9")

# Test boundary case
print(f"\nBoundary test:")
print(f"  324 degrees: code={LCHab_to_munsell_specification([50, 50, 324])[3]}")
print(f"  325 degrees: code={LCHab_to_munsell_specification([50, 50, 325])[3]}")
print(f"  360 degrees: code={LCHab_to_munsell_specification([50, 50, 360])[3]}")
print(f"  0 degrees: code={LCHab_to_munsell_specification([50, 50, 0])[3]}")
print(f"  1 degrees: code={LCHab_to_munsell_specification([50, 50, 1])[3]}")