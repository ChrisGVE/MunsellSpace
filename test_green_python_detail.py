#!/usr/bin/env python3
"""Test green color conversion in detail"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import xyY_to_XYZ, XYZ_to_Lab
from colour.colorimetry import CCS_ILLUMINANTS

# Green test case
xyY = np.array([0.3, 0.6, 0.715152])

# Get Illuminant C
ILLUMINANT_C = CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']

# Convert to XYZ
XYZ = xyY_to_XYZ(xyY)
print(f"xyY {xyY} -> XYZ {XYZ}")

# Convert to Lab
Lab = XYZ_to_Lab(XYZ, ILLUMINANT_C)
print(f"XYZ -> Lab {Lab}")

# Convert to LCHab
L = Lab[0]
a = Lab[1]
b = Lab[2]
C = np.sqrt(a**2 + b**2)
H = np.degrees(np.arctan2(b, a)) % 360
print(f"Lab -> LCHab [{L:.3f}, {C:.3f}, {H:.3f}]")

# Now call the actual function
spec = xyY_to_munsell_specification(xyY)
print(f"\nFinal result: {spec}")
print(f"That's {spec[0]:.3f}{['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP'][int(spec[3]-1)]} {spec[1]:.1f}/{spec[2]:.1f}")