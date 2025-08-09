#!/usr/bin/env python3
"""Test xy_from_renotation for the problematic specification."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import (
    xy_from_renotation_ovoid,
    normalise_munsell_specification
)

# The problematic specification from iteration 1
# hue=8.6058, value=9.3528, chroma=12.6521, code=4 (GY)
spec = [8.6058, 9.3528, 12.6521, 4.0]

print(f"Testing specification: {spec}")
print(f"  Hue: {spec[0]:.4f}")
print(f"  Value: {spec[1]:.4f}") 
print(f"  Chroma: {spec[2]:.4f}")
print(f"  Code: {spec[3]} (GY)")

# Normalize it first as Python does
spec_normalized = normalise_munsell_specification(spec)
print(f"\nNormalized: {spec_normalized}")

# Get xy coordinates
try:
    xy = xy_from_renotation_ovoid(spec_normalized)
    print(f"\nPython xy_from_renotation_ovoid result: {xy}")
    print(f"  x: {xy[0]:.6f}")
    print(f"  y: {xy[1]:.6f}")
    
    # Calculate rho from neutral point
    # Illuminant C: x=0.31006, y=0.31616
    x_center = 0.31006
    y_center = 0.31616
    
    x_diff = xy[0] - x_center
    y_diff = xy[1] - y_center
    rho = np.sqrt(x_diff**2 + y_diff**2)
    
    print(f"\nCalculated rho from neutral:")
    print(f"  x_diff: {x_diff:.6f}")
    print(f"  y_diff: {y_diff:.6f}")
    print(f"  rho: {rho:.6f}")
    
    print(f"\nRust reported rho=0.187058")
    print(f"Difference: {abs(rho - 0.187058):.6f}")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

# Let's also test with a lower chroma to see the pattern
print("\n" + "="*50)
print("Testing with lower chroma (8.68):")
spec2 = [8.6058, 9.3528, 8.6815, 4.0]
spec2_normalized = normalise_munsell_specification(spec2)
print(f"Specification: {spec2}")

try:
    xy2 = xy_from_renotation_ovoid(spec2_normalized)
    print(f"Python xy result: {xy2}")
    
    x_diff2 = xy2[0] - x_center
    y_diff2 = xy2[1] - y_center
    rho2 = np.sqrt(x_diff2**2 + y_diff2**2)
    
    print(f"Calculated rho: {rho2:.6f}")
    print(f"Rust reported rho after refinement: 0.127320")
    print(f"Target rho_input: 0.130170")
    
except Exception as e:
    print(f"Error: {e}")