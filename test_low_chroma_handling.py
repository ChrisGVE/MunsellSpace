#!/usr/bin/env python3
"""Test how Python handles low chromas < 2.0 in xy_from_renotation."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import (
    xy_from_renotation_ovoid,
    munsell_specification_to_xy,
    normalise_munsell_specification
)

# Test specifications with chromas < 2.0 at high value
# Note: munsell_specification_to_xy requires integer values
test_specs = [
    [9.68, 9.0, 0.99, 6.0],  # Rust's result for RGB(255,238,238) with value rounded
    [9.96, 9.0, 1.96, 6.0],  # Python's result for RGB(255,238,238) with value rounded
    [9.96, 9.0, 1.50, 6.0],  # In between
    [9.96, 9.0, 1.00, 6.0],  # Exactly 1.0
    [9.96, 9.0, 0.50, 6.0],  # Very low chroma
]

print("Testing low chroma handling:")
print("=" * 60)

for spec in test_specs:
    print(f"\nSpec: hue={spec[0]:.2f}, value={spec[1]:.2f}, chroma={spec[2]:.2f}, code={spec[3]}")
    
    # Normalize
    spec_norm = normalise_munsell_specification(spec)
    
    # Try munsell_specification_to_xy (handles chromas < 2.0)
    try:
        xy = munsell_specification_to_xy(spec_norm)
        print(f"  munsell_specification_to_xy: x={xy[0]:.6f}, y={xy[1]:.6f}")
        
        # Calculate rho from neutral
        x_center = 0.31006
        y_center = 0.31616
        rho = np.sqrt((xy[0] - x_center)**2 + (xy[1] - y_center)**2)
        print(f"  rho = {rho:.6f}")
    except Exception as e:
        print(f"  Error: {e}")

# Now test what happens when we call xy_from_renotation_ovoid directly
print("\n" + "=" * 60)
print("Testing xy_from_renotation_ovoid directly (requires chroma >= 2.0):")

for spec in test_specs:
    spec_norm = normalise_munsell_specification(spec)
    print(f"\nSpec: chroma={spec_norm[2]:.2f}")
    try:
        xy = xy_from_renotation_ovoid(spec_norm)
        print(f"  Success: x={xy[0]:.6f}, y={xy[1]:.6f}")
    except Exception as e:
        print(f"  Error: {e}")

# Test how Python interpolates between grey and chroma=2
print("\n" + "=" * 60)
print("Testing interpolation between grey (chroma=0) and chroma=2:")

spec_grey = [9.96, 9.0, 0.0, 6.0]  # Grey (value must be integer)
spec_2 = [9.96, 9.0, 2.0, 6.0]     # Chroma=2 (value must be integer)

xy_grey = munsell_specification_to_xy(spec_grey)
xy_2 = munsell_specification_to_xy(spec_2)

print(f"Grey (chroma=0): x={xy_grey[0]:.6f}, y={xy_grey[1]:.6f}")
print(f"Chroma=2: x={xy_2[0]:.6f}, y={xy_2[1]:.6f}")

# Manually interpolate for chroma=1.0
t = 1.0 / 2.0  # chroma=1.0 is halfway between 0 and 2
x_interp = xy_grey[0] * (1 - t) + xy_2[0] * t
y_interp = xy_grey[1] * (1 - t) + xy_2[1] * t
print(f"\nManual interpolation for chroma=1.0:")
print(f"  t = {t}")
print(f"  x = {x_interp:.6f}, y = {y_interp:.6f}")

# Compare with what Python gives
spec_1 = [9.96, 9.0, 1.0, 6.0]  # value must be integer
xy_1 = munsell_specification_to_xy(spec_1)
print(f"\nPython's result for chroma=1.0:")
print(f"  x = {xy_1[0]:.6f}, y = {xy_1[1]:.6f}")

print(f"\nDifference:")
print(f"  dx = {xy_1[0] - x_interp:.6f}")
print(f"  dy = {xy_1[1] - y_interp:.6f}")