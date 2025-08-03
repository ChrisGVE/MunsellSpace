#!/usr/bin/env python3
"""Debug Python colour-science Munsell conversion iterations."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

# Test pure red
rgb = np.array([1.0, 0.0, 0.0])  # Normalized RGB
print(f"Input RGB: {rgb}")

# Get XYZ and xyY
xyz = sRGB_to_XYZ(rgb)
print(f"XYZ (D65): {xyz}")

xyy = XYZ_to_xyY(xyz)
print(f"xyY (D65): x={xyy[0]:.6f}, y={xyy[1]:.6f}, Y={xyy[2]:.6f}")

# Convert to Munsell
# Convert xyY to Munsell directly
munsell = xyY_to_munsell_colour(xyy)
print(f"Final Munsell (from D65 xyY): {munsell}")

# Let's manually call the internal function to see more detail
from colour.notation.munsell import xyY_to_munsell_specification
from colour.adaptation import chromatic_adaptation_VonKries
from colour.models import XYZ_to_Lab, Lab_to_LCHab

# Apply chromatic adaptation from D65 to C
from colour.models import CCS_ILLUMINANTS
from colour import ILLUMINANTS

# Get the full XYZ coordinates for D65 and C
XYZ_D65 = ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
XYZ_C = ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']

XYZ_c = chromatic_adaptation_VonKries(
    xyz, 
    XYZ_D65,  # D65
    XYZ_C,    # C
    transform='Bradford'
)
print(f"XYZ (Illuminant C): {XYZ_c}")

# Convert to Lab and LCHab
Lab = XYZ_to_Lab(XYZ_c, illuminant=XYZ_C)
print(f"Lab (Illuminant C): L={Lab[0]:.6f}, a={Lab[1]:.6f}, b={Lab[2]:.6f}")

LCH = Lab_to_LCHab(Lab)
print(f"LCHab: L={LCH[0]:.6f}, C={LCH[1]:.6f}, H={LCH[2]:.6f}")

# Convert to Munsell specification
# We need the xyY in Illuminant C space
xyY_c = XYZ_to_xyY(XYZ_c)
print(f"xyY (Illuminant C): x={xyY_c[0]:.6f}, y={xyY_c[1]:.6f}, Y={xyY_c[2]:.6f}")

# Get Munsell specification
spec = xyY_to_munsell_specification(xyY_c)
print(f"Munsell specification: {spec}")