#!/usr/bin/env python3
"""Check Python's initial specification calculation"""

import numpy as np

# RGB(221, 238, 238) in xyY
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing initial specification for RGB(221, 238, 238)")
print(f"xyY: {xyY}")
print()

# What we know from debugging:
# - Initial spec from Rust: chroma=1.980
# - Python final result: chroma=2.084644
# - Rust is scaling by (5.0/5.5) = 0.909

print("Key observations:")
print("1. Rust starts with chroma=1.980")
print("2. Python ends with chroma=2.084644")
print("3. Rust scales initial chroma by (5.0/5.5) = 0.909")
print()

# If Rust didn't scale
unscaled_chroma = 1.980 / (5.0/5.5)
print(f"Unscaled initial chroma would be: {unscaled_chroma:.3f}")
print()

# The issue
print("THE PROBLEM:")
print("Rust scales the initial chroma down by (5.0/5.5), making it start at 1.98")
print("This causes the convergence to find a lower chroma (1.556) instead of the correct 2.084")
print("The scaling factor (5.0/5.5) appears to be incorrect or misapplied")