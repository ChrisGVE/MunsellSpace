#!/usr/bin/env python3
"""Test Munsell Value range handling"""

import numpy as np
from colour.notation import munsell

print("Testing Munsell Value range:")
print("="*60)

# Test munsell_value functions
test_Y_values = [0, 10, 50, 90, 100]  # Y in 0-100 range

for Y in test_Y_values:
    value = munsell.munsell_value_ASTMD1535(Y)
    print(f"Y={Y:3.0f}% -> Value={value:.2f}")

print("\n" + "="*60)
print("Munsell Value should range from 0 to 10")
print("Y=100% (perfect white) should give Value=10")
print("="*60)

# Test what values the renotation data accepts
print("\nTesting xy_from_renotation_ovoid with different Values:")

test_specs = [
    [5.0, 8.0, 4.0, 3],   # Value 8 - should work
    [5.0, 9.0, 4.0, 3],   # Value 9 - should work  
    [5.0, 9.5, 4.0, 3],   # Value 9.5 - ?
    [5.0, 10.0, 4.0, 3],  # Value 10 - ?
]

for spec in test_specs:
    try:
        xy = munsell.xy_from_renotation_ovoid(spec)
        print(f"  Value={spec[1]:4.1f} -> SUCCESS, xy=[{xy[0]:.6f}, {xy[1]:.6f}]")
    except Exception as e:
        print(f"  Value={spec[1]:4.1f} -> ERROR: {str(e)[:60]}...")

print("\n" + "="*60)
print("CHECKING RUST IMPLEMENTATION:")
print("="*60)

# From Rust trace, we have value 9.277364
print("Rust gets Value=9.277364 from Y=0.826943")
print("This is > 9.0 but < 10.0, which is valid for Munsell")

# Check Python's calculation
Y_percent = 0.826943 * 100
value_py = munsell.munsell_value_ASTMD1535(Y_percent)
print(f"\nPython: Y={Y_percent:.2f}% -> Value={value_py:.6f}")

print("\n" + "="*60)
print("ISSUE IDENTIFIED:")
print("="*60)
print("1. Munsell Value correctly ranges from 0 to 10")
print("2. Python's xy_from_renotation_ovoid only accepts Value in [1, 9]")
print("3. This is a limitation of the renotation dataset, not Munsell spec")
print("4. Values > 9 need extrapolation, which Rust handles but Python doesn't")
print("5. The convergence produces Value=9.277 which is valid but needs special handling")