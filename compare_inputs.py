#!/usr/bin/env python3
"""Compare exact inputs between Python and Rust at each step"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import xyY_to_XYZ, XYZ_to_Lab
from colour.colorimetry import CCS_ILLUMINANTS
from colour.notation.munsell import (
    munsell_specification_to_xyY,
)

# Green test case - EXACT same input
xyY = np.array([0.3, 0.6, 0.715152])
print(f"Initial xyY input: [{xyY[0]:.6f}, {xyY[1]:.6f}, {xyY[2]:.6f}]")

# Get Illuminant C
ILLUMINANT_C = CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
print(f"Illuminant C: [{ILLUMINANT_C[0]:.6f}, {ILLUMINANT_C[1]:.6f}]")

# Step 1: Convert to XYZ
XYZ = xyY_to_XYZ(xyY)
print(f"\nStep 1 - xyY to XYZ:")
print(f"  XYZ: [{XYZ[0]:.10f}, {XYZ[1]:.10f}, {XYZ[2]:.10f}]")

# Step 2: Convert to Lab
Lab = XYZ_to_Lab(XYZ, ILLUMINANT_C)
print(f"\nStep 2 - XYZ to Lab:")
print(f"  Lab: [{Lab[0]:.10f}, {Lab[1]:.10f}, {Lab[2]:.10f}]")

# Step 3: Convert to LCHab
L = Lab[0]
a = Lab[1]
b = Lab[2]
C = np.sqrt(a**2 + b**2)
H = np.degrees(np.arctan2(b, a)) % 360
LCHab = np.array([L, C, H])
print(f"\nStep 3 - Lab to LCHab:")
print(f"  LCHab: [{L:.10f}, {C:.10f}, {H:.10f}]")

# Step 4: We need to compute initial spec manually since we can't import the function
# From Python colour-science, the formula is approximately:
# hue_angle = H + 18 (adjusted)
# Then convert to Munsell hue
print(f"\nStep 4 - LCHab to initial Munsell spec:")
print(f"  (Cannot directly compute in this script, but Python gets:)")
print(f"  From actual run: [7.877, 8.773, 24.855, 4] according to Rust debug")

# Run the actual conversion to see what Python gets
print(f"\n=== Running full conversion ===")
final_spec = xyY_to_munsell_specification(xyY)
print(f"Final Python result: [{final_spec[0]:.10f}, {final_spec[1]:.10f}, {final_spec[2]:.10f}, {final_spec[3]:.0f}]")

print("\n=== What Rust is getting ===")
print("From Rust debug output:")
print("  Initial spec from LCHab: [7.877, 8.773, 24.855, 4]")
print("  Spec after init: [7.877, 8.747, 22.595, 4]")
print("\nDifferences from Python:")
print(f"  Hue: Rust=7.877, Python={initial_spec[0]:.3f}, diff={7.877-initial_spec[0]:.3f}")
print(f"  Value: Rust=8.773, Python={initial_spec[1]:.3f}, diff={8.773-initial_spec[1]:.3f}")
print(f"  Chroma: Rust=24.855, Python={initial_spec[2]:.3f}, diff={24.855-initial_spec[2]:.3f}")