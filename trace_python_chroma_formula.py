#!/usr/bin/env python3
"""Trace Python's exact chroma refinement formula"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ
from colour.models import xyY_to_XYZ
from colour.algebra import cartesian_to_cylindrical

# Monkey-patch to trace the chroma refinement
original_xyy_to_spec = munsell.xyY_to_munsell_specification

def traced_xyy_to_spec(xyy):
    """Trace chroma refinement details"""
    # We need to look at the actual Python source
    # The key is in the chroma refinement loop
    
    # From Python colour-science source:
    # chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
    
    # Let's trace what Python actually does
    return original_xyy_to_spec(xyy)

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

print("Testing RGB(221, 238, 238)")
print("="*60)
print(f"xyY: {xyy}")

# Get the result
spec = munsell.xyY_to_munsell_specification(xyy)
print(f"Final spec: {spec}")
print(f"Final chroma: {spec[2]:.6f}")

print("\n" + "="*60)
print("PYTHON'S CHROMA FORMULA (from source):")
print("="*60)
print("chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current")
print()
print("Key difference from Rust:")
print("- Python uses ** (power operator)")
print("- Rust uses .powf() method")
print("- Both should be equivalent")
print()
print("The issue might be:")
print("1. Different initial chroma estimate")
print("2. Different convergence criteria")
print("3. Different rho calculation")

# Let's check the initial estimate
# Illuminant C
x_center, y_center = 0.31006, 0.31616

# Calculate rho for our color
x, y = xyy[0], xyy[1]
big_y = xyy[2]

# Cylindrical coordinates
rho_input, phi_input, _ = cartesian_to_cylindrical(
    np.array([x - x_center, y - y_center, big_y])
)

print(f"\nInput rho: {rho_input:.9f}")
print(f"Input phi: {np.degrees(phi_input):.6f}°")

# Check if the issue is the initial chroma from LCHab
from colour.models import XYZ_to_Lab

# Python's WRONG approach with Y=sample
xyz_r = xyY_to_XYZ([x_center, y_center, xyy[2]])
Lab = XYZ_to_Lab(xyz, xyz_r)
C = np.hypot(Lab[1], Lab[2])

print(f"\nInitial chroma from LCHab (with bug): {C:.6f}")

# The huge b* value causes huge C value
# But this gets normalized somehow...

# The key insight:
print("\n" + "="*60)
print("KEY INSIGHT:")
print("="*60)
print("Python's Lab bug (b*=2078) creates huge initial chroma")
print("But the convergence algorithm still works because:")
print("1. The chroma gets refined based on rho")
print("2. The formula (rho_input/rho_current)^n reduces it")
print("3. Final chroma depends more on rho than initial estimate")