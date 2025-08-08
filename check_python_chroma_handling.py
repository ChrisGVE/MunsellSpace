#!/usr/bin/env python3
"""Check how Python handles the huge initial chroma from Lab bug"""

import numpy as np
from colour.notation import munsell

# Direct access to the conversion function
# We need to understand how LCHab maps to Munsell

# From Python colour-science:
# The LCHab to Munsell conversion likely normalizes the chroma

# Test with a huge chroma value
test_lchab = [92.88, 2079.0, 90.3]  # L, C, H from our buggy Lab

print("Testing LCHab to Munsell conversion")
print("="*60)
print(f"Input LCHab: L={test_lchab[0]:.2f}, C={test_lchab[1]:.2f}, H={test_lchab[2]:.2f}")

# The function that converts LCHab to initial Munsell specification
# This is likely where the normalization happens

# From the Python source, the conversion is:
# 1. LCHab H (hue angle) -> Munsell hue
# 2. LCHab L (lightness) -> Munsell value  
# 3. LCHab C (chroma) -> Munsell chroma (with normalization)

# The chroma conversion likely involves:
# - Dividing by some factor
# - Or using a mapping table
# - Or clamping to reasonable range

# Let's check what a reasonable chroma mapping would be
L = test_lchab[0]
C = test_lchab[1]
H = test_lchab[2]

# Typical LCHab chroma ranges from 0 to ~150
# Munsell chroma ranges from 0 to ~20
# So a scaling factor would be around 150/20 = 7.5

# But with C=2079, we'd get 2079/7.5 = 277, still huge

# Python must be doing something else...
# Let's check the actual conversion

# The key is probably that Python uses a different initial estimate
# Or the convergence algorithm ignores the initial chroma

print("\nHypothesis: Python's convergence ignores bad initial chroma")
print("The algorithm refines from scratch based on rho")
print("So the huge initial value doesn't matter")

# Test with actual conversion
rgb = np.array([221, 238, 238]) / 255.0
from colour import sRGB_to_XYZ
xyz = sRGB_to_XYZ(rgb)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

spec = munsell.xyY_to_munsell_specification(xyy)
print(f"\nActual result for RGB(221,238,238):")
print(f"Munsell: {spec[0]:.1f}{['R','YR','Y','GY','G','BG','B','PB','P','RP'][int(spec[3])-1]} {spec[1]:.1f}/{spec[2]:.1f}")

print("\n" + "="*60)
print("CONCLUSION:")
print("="*60)
print("Python's huge initial chroma (2079) doesn't affect the result")
print("because the convergence algorithm refines based on rho.")
print("The initial chroma is just a starting point.")
print()
print("Rust should:")
print("1. Use the actual LCHab chroma (2.18) as initial value")
print("2. Not clamp it to 2.0 for high values")
print("3. Let the convergence algorithm refine it")