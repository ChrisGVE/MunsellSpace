#!/usr/bin/env python3
"""Test Python's behavior at different values to understand extrapolation."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import _munsell_specification_to_xyY

# Test with chroma=12.6521 at different values
specs = [
    [8.6058, 8.0, 12.6521, 4.0],
    [8.6058, 9.0, 12.6521, 4.0],
    [8.6058, 9.3528, 12.6521, 4.0],
]

print("Testing at different values with same chroma=12.6521:")
print("="*60)

x_center = 0.31006
y_center = 0.31616

for spec in specs:
    try:
        xyY = _munsell_specification_to_xyY(spec)
        x_diff = xyY[0] - x_center
        y_diff = xyY[1] - y_center
        rho = np.sqrt(x_diff**2 + y_diff**2)
        
        print(f"\nValue {spec[1]:.4f}:")
        print(f"  x: {xyY[0]:.6f}, y: {xyY[1]:.6f}")
        print(f"  rho: {rho:.6f}")
    except Exception as e:
        print(f"\nValue {spec[1]:.4f}: Error: {e}")

# Now let's check what Rust would compute with linear extrapolation
print("\n" + "="*60)
print("Rust's linear extrapolation from 8->9 to 9.3528:")

# These are the Python values we just found
x_8 = 0.342595  # Need to run to get actual value
y_8 = 0.568078  # Need to run to get actual value

# Run to get actual values first
spec_8 = [8.6058, 8.0, 12.6521, 4.0]
xyY_8 = _munsell_specification_to_xyY(spec_8)
x_8 = xyY_8[0]
y_8 = xyY_8[1]

spec_9 = [8.6058, 9.0, 12.6521, 4.0]
xyY_9 = _munsell_specification_to_xyY(spec_9)
x_9 = xyY_9[0]
y_9 = xyY_9[1]

# Rust's extrapolation: t = value - 8.0 = 9.3528 - 8.0 = 1.3528
t = 9.3528 - 8.0
x_rust = x_8 + t * (x_9 - x_8)
y_rust = y_8 + t * (y_9 - y_8)

print(f"  From value=8: x={x_8:.6f}, y={y_8:.6f}")
print(f"  From value=9: x={x_9:.6f}, y={y_9:.6f}")
print(f"  t = {t:.4f}")
print(f"  Extrapolated: x={x_rust:.6f}, y={y_rust:.6f}")

x_diff = x_rust - x_center
y_diff = y_rust - y_center
rho_rust = np.sqrt(x_diff**2 + y_diff**2)
print(f"  Extrapolated rho: {rho_rust:.6f}")

print(f"\nPython actually gives: x=0.326212, y=0.443071, rho=0.127935")
print(f"Difference suggests Python is NOT using simple linear extrapolation")