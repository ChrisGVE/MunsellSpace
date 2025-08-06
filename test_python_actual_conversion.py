#!/usr/bin/env python3
"""Test Python's actual xyY_to_munsell_specification behavior"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification

# Test red color that was failing
xyy = np.array([0.640000, 0.330000, 0.212673])
print(f"Testing red xyY: {xyy}")

try:
    spec = xyY_to_munsell_specification(xyy)
    print(f"Success! Result: {spec}")
    print(f"  Hue: {spec[0]:.3f}")
    print(f"  Value: {spec[1]:.3f}")
    print(f"  Chroma: {spec[2]:.3f}")
    print(f"  Code: {spec[3]}")
except Exception as e:
    print(f"Error: {e}")

# Let's trace through to see what's happening differently
# I'll add some debugging to understand the flow

# Import the private function to trace it
from colour.notation.munsell import _xyY_to_munsell_specification
from colour.utilities import as_float_array

print("\nTracing through _xyY_to_munsell_specification:")
try:
    spec = _xyY_to_munsell_specification(as_float_array(xyy))
    print(f"Success! Result: {spec}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Let me check what rho_input vs rho_current actually is for red
from colour.notation.munsell import (
    munsell_value_ASTMD1535,
    _munsell_specification_to_xyY,
    LCHab_to_munsell_specification,
    hue_to_hue_angle,
    maximum_chroma_from_renotation
)
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab, XYZ_to_xy
from colour.algebra import cartesian_to_cylindrical
from colour.notation.munsell import ILLUMINANT_NAME_MUNSELL
from colour.colorimetry import CCS_ILLUMINANTS
from colour.utilities import domain_range_scale, to_domain_1

x, y, Y = xyy[0], xyy[1], xyy[2]
Y = to_domain_1(Y)

print(f"\nInput: x={x}, y={y}, Y={Y}")

# Get value
with domain_range_scale("ignore"):
    value = munsell_value_ASTMD1535(Y * 100)
print(f"Value: {value}")

# Get center point
with domain_range_scale("ignore"):
    x_center, y_center, Y_center = _munsell_specification_to_xyY(value)
print(f"Center: x={x_center}, y={y_center}, Y={Y_center}")

# Get input rho
rho_input, phi_input, _z_input = cartesian_to_cylindrical([x - x_center, y - y_center, Y_center])
phi_input = np.degrees(phi_input)
print(f"Input rho: {rho_input}, phi: {phi_input}")

# Get initial spec from Lab
XYZ = xyY_to_XYZ(xyy)
x_i, y_i = 0.31006, 0.31616  # Illuminant C
X_r, Y_r, Z_r = xyY_to_XYZ([x_i, y_i, Y])
XYZ_r = np.array([(1 / Y_r) * X_r, 1, (1 / Y_r) * Z_r])
Lab = XYZ_to_Lab(XYZ, XYZ_to_xy(XYZ_r))
LCHab = Lab_to_LCHab(Lab)
hue_initial, _value_initial, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)

print(f"\nInitial from Lab:")
print(f"  Hue: {hue_initial}, Code: {code_initial}")
print(f"  Chroma (raw): {chroma_initial}")
print(f"  Chroma (scaled): {(5 / 5.5) * chroma_initial}")

specification_current = [
    hue_initial,
    value,
    (5 / 5.5) * chroma_initial,
    code_initial,
]

print(f"\nInitial specification: {specification_current}")

# Get current position
with domain_range_scale("ignore"):
    x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)

rho_current, phi_current, _z_current = cartesian_to_cylindrical(
    [x_current - x_center, y_current - y_center, Y_center]
)

print(f"\nCurrent position:")
print(f"  x,y: ({x_current}, {y_current})")
print(f"  rho_current: {rho_current}")
print(f"  phi_current: {np.degrees(phi_current)}")

print(f"\nKey comparison:")
print(f"  rho_input: {rho_input}")
print(f"  rho_current: {rho_current}")
print(f"  Are they equal? {np.isclose(rho_input, rho_current)}")
print(f"  Difference: {abs(rho_input - rho_current)}")