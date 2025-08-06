#!/usr/bin/env python3
"""Debug why initial specs have hue=0.0 with high chromas"""

import numpy as np
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab, XYZ_to_xy
from colour.notation.munsell import LCHab_to_munsell_specification, munsell_value_ASTMD1535
from colour.utilities import to_domain_1, domain_range_scale

# Test green which generates [0.0, 8.0, 22.0, 5.0]
xyy = np.array([0.3, 0.6, 0.715152])
x, y, Y = xyy[0], xyy[1], to_domain_1(xyy[2])

# Convert to Lab
XYZ = xyY_to_XYZ(xyy)
x_i, y_i = 0.31006, 0.31616  # Illuminant C
X_r, Y_r, Z_r = xyY_to_XYZ([x_i, y_i, Y])
XYZ_r = np.array([(1 / Y_r) * X_r, 1, (1 / Y_r) * Z_r])
Lab = XYZ_to_Lab(XYZ, XYZ_to_xy(XYZ_r))
LCHab = Lab_to_LCHab(Lab)

print(f"Green xyY: {xyy}")
print(f"Lab: {Lab}")
print(f"LCHab: L={LCHab[0]:.3f}, C={LCHab[1]:.3f}, h={LCHab[2]:.3f}")

# Get Munsell spec from LCHab
hue_initial, value_initial, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)
print(f"\nFrom LCHab_to_munsell_specification:")
print(f"  hue={hue_initial:.3f}, value={value_initial:.3f}, chroma={chroma_initial:.3f}, code={code_initial}")

# Check the hue angle mapping
h_angle = LCHab[2]
print(f"\nHue angle {h_angle:.3f} degrees:")
if 108 < h_angle <= 144:
    print(f"  Maps to code 4 (GY)")
    hue_segment = h_angle % 36
    hue = (hue_segment / 36) * 10
    if hue == 0:
        hue = 10
    print(f"  Segment {hue_segment:.3f} -> hue {hue:.3f}")
    
# My implementation
# code = 4 for angle 136.357
# hue_segment = 136.357 % 36 = 28.357
# hue = (28.357 / 36) * 10 = 7.877
print(f"\nMy calculation:")
hue_segment = h_angle % 36
hue = (hue_segment / 36) * 10
print(f"  Segment {hue_segment:.3f} -> hue {hue:.3f}")
if hue == 0:
    print(f"  Would change to 10.0")
    
# So hue should be 7.877, not 0.0
# The 0.0 must be coming from somewhere else in the algorithm