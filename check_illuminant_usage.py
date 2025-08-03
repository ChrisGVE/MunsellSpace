#!/usr/bin/env python3
"""Check how Python colour-science handles illuminants in Munsell conversion."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour import CCS_ILLUMINANTS

# List available illuminants
print("Available illuminants in colour-science:")
for observer in CCS_ILLUMINANTS:
    print(f"\n{observer}:")
    for illuminant in CCS_ILLUMINANTS[observer]:
        print(f"  {illuminant}: {CCS_ILLUMINANTS[observer][illuminant]}")
        
# Test with different illuminants
print("\n\nTesting RGB(255,0,0) conversion:")

# Standard D65
rgb = np.array([1.0, 0.0, 0.0])
xyz_d65 = sRGB_to_XYZ(rgb)
xyy_d65 = XYZ_to_xyY(xyz_d65)
munsell_d65 = xyY_to_munsell_colour(xyy_d65)
print(f"D65 (default): XYZ={xyz_d65}, xyY={xyy_d65}")
print(f"  Munsell: {munsell_d65}")

# Check what illuminant the Munsell data uses
print("\n\nMunsell renotation data illuminant:")
print("The Munsell renotation data uses Illuminant C as reference")
print(f"Illuminant C: {CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']}")