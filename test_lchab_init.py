#!/usr/bin/env python3
"""Test LCHab initialization for RGB(221, 238, 238)"""

import numpy as np
from colour import XYZ_to_Lab, Lab_to_LCHab, xyY_to_XYZ
from colour.notation.munsell import LCHab_to_munsell_specification

# Test color
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])
print(f"Testing RGB(221, 238, 238) LCHab initialization")
print(f"xyY: {xyY}")

# Convert to XYZ
XYZ = xyY_to_XYZ(xyY)
print(f"\nXYZ: {XYZ}")

# Convert to Lab using Illuminant C
Lab = XYZ_to_Lab(XYZ, illuminant=np.array([0.31006, 0.31616]))
print(f"Lab: {Lab}")

# Convert to LCHab
LCHab = Lab_to_LCHab(Lab)
print(f"LCHab: {LCHab}")

# Convert to Munsell specification (if available)
try:
    spec = LCHab_to_munsell_specification(LCHab)
    print(f"\nInitial Munsell spec from LCHab:")
    print(f"  Hue:    {spec[0]:.6f}")
    print(f"  Value:  {spec[1]:.6f}")
    print(f"  Chroma: {spec[2]:.6f}")
    print(f"  Code:   {spec[3]}")
except:
    print("\nLCHab_to_munsell_specification not available")
    # Manual approximation
    L, C, H = LCHab
    value = L / 10.0
    chroma = C / 5.0
    print(f"\nManual approximation:")
    print(f"  Value (L/10):  {value:.6f}")
    print(f"  Chroma (C/5):  {chroma:.6f}")
    print(f"  Hue angle:     {H:.2f}°")