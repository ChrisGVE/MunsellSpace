#!/usr/bin/env python3
"""Compare exact numerical values between Python and Rust"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import xyY_to_XYZ, XYZ_to_Lab
from colour.colorimetry import CCS_ILLUMINANTS

# Green test case - EXACT same input
xyY = np.array([0.3, 0.6, 0.715152])
print(f"Initial xyY input: [{xyY[0]:.10f}, {xyY[1]:.10f}, {xyY[2]:.10f}]")

# Get Illuminant C
ILLUMINANT_C = CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
print(f"Illuminant C: [{ILLUMINANT_C[0]:.10f}, {ILLUMINANT_C[1]:.10f}]")

# Step 1: Convert to XYZ
XYZ = xyY_to_XYZ(xyY)
print(f"\nxyY → XYZ:")
print(f"  Python: [{XYZ[0]:.10f}, {XYZ[1]:.10f}, {XYZ[2]:.10f}]")

# Step 2: Convert to Lab
Lab = XYZ_to_Lab(XYZ, ILLUMINANT_C)
print(f"\nXYZ → Lab (Illuminant C):")
print(f"  Python: [{Lab[0]:.10f}, {Lab[1]:.10f}, {Lab[2]:.10f}]")

# Step 3: Convert to LCHab
L = Lab[0]
a = Lab[1]
b = Lab[2]
C = np.sqrt(a**2 + b**2)
H = np.degrees(np.arctan2(b, a)) % 360
print(f"\nLab → LCHab:")
print(f"  Python L: {L:.10f}")
print(f"  Python C: {C:.10f}")
print(f"  Python H: {H:.10f}")
print(f"  Rust (from debug): L=87.735, C=124.273, H=136.357")
print(f"  Differences: L={87.735-L:.6f}, C={124.273-C:.6f}, H={136.357-H:.6f}")

# Now let's check the initial Munsell spec calculation
print(f"\n=== Initial Munsell Spec from LCHab ===")
print(f"Rust gets: [7.877, 8.773, 24.855, 4]")

# To understand this, we need to know how LCHab maps to Munsell
# The hue angle formula is: adjusted_angle = (H - 18) % 360
adjusted_angle = (H - 18) % 360
print(f"Adjusted hue angle: {adjusted_angle:.10f}")

# Then this maps to Munsell hue using the formula:
# code = (17 - floor(adjusted_angle / 36)) % 10 + 1
# hue = 10 - (adjusted_angle % 36) * 10 / 36
import math
code = (17 - math.floor(adjusted_angle / 36)) % 10 + 1
hue = 10 - (adjusted_angle % 36) * 10 / 36
print(f"From angle {adjusted_angle:.3f}:")
print(f"  Expected code: {code}")
print(f"  Expected hue: {hue:.3f}")

# Value from L
munsell_value = L / 10  # Simplified, actual formula is more complex
print(f"Value from L={L:.3f}: ~{munsell_value:.3f}")

# Chroma from C
munsell_chroma = C / 5  # Very rough approximation
print(f"Chroma from C={C:.3f}: ~{munsell_chroma:.3f}")

print(f"\n=== Final Result Comparison ===")
final_spec = xyY_to_munsell_specification(xyY)
print(f"Python final: [{final_spec[0]:.10f}, {final_spec[1]:.10f}, {final_spec[2]:.10f}, {final_spec[3]:.0f}]")
print(f"Python final: {final_spec[0]:.3f} {['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP'][int(final_spec[3]-1)]} {final_spec[1]:.1f}/{final_spec[2]:.1f}")
print(f"Rust stuck at: ~2.2 Y 8.7/18.0 (from debug output)")