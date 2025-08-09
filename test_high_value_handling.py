#!/usr/bin/env python3
"""Test how Python handles high values (>9) in Munsell conversion."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import (
    munsell_specification_to_xy,
    _munsell_specification_to_xyY
)

# Test with value > 9
spec = [8.6058, 9.3528, 12.6521, 4.0]
print(f"Testing high value spec: {spec}")

# Try munsell_specification_to_xy which is used in the main algorithm
try:
    xy = munsell_specification_to_xy(spec)
    print(f"munsell_specification_to_xy result: {xy}")
except Exception as e:
    print(f"munsell_specification_to_xy error: {e}")

# Try the internal function
try:
    xyY = _munsell_specification_to_xyY(spec)
    print(f"_munsell_specification_to_xyY result: {xyY}")
    print(f"  x: {xyY[0]:.6f}")
    print(f"  y: {xyY[1]:.6f}")
    print(f"  Y: {xyY[2]:.6f}")
    
    # Calculate rho
    x_center = 0.31006
    y_center = 0.31616
    x_diff = xyY[0] - x_center
    y_diff = xyY[1] - y_center
    rho = np.sqrt(x_diff**2 + y_diff**2)
    print(f"\nCalculated rho: {rho:.6f}")
    print(f"Rust reported rho: 0.187058")
    
except Exception as e:
    print(f"_munsell_specification_to_xyY error: {e}")

# Let's trace through what Python does
print("\n" + "="*50)
print("Checking Python's approach for value > 9:")

# Look at how Python gets xy for the iterative algorithm
print("\nIn the convergence loop, Python calls _munsell_specification_to_xyY")
print("which internally handles value > 9 by extrapolation")

# Test with value=9 for comparison
spec_v9 = [8.6058, 9.0, 12.6521, 4.0]
print(f"\nTesting with value=9: {spec_v9}")
try:
    xyY_v9 = _munsell_specification_to_xyY(spec_v9)
    print(f"Result: x={xyY_v9[0]:.6f}, y={xyY_v9[1]:.6f}")
    
    x_diff = xyY_v9[0] - x_center
    y_diff = xyY_v9[1] - y_center
    rho_v9 = np.sqrt(x_diff**2 + y_diff**2)
    print(f"Rho at value=9: {rho_v9:.6f}")
except Exception as e:
    print(f"Error: {e}")