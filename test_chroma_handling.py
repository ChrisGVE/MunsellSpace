#!/usr/bin/env python3
"""Test how Python handles chroma values in lookup."""

import numpy as np
from colour.notation.munsell import _munsell_specification_to_xyY

# Test various chroma values
test_specs = [
    [7.860852, 5.219872, 20.0, 7],      # Even chroma
    [7.860852, 5.219872, 20.5, 7],      # Half chroma
    [7.860852, 5.219872, 20.860931, 7], # Our exact value
    [7.860852, 5.219872, 21.0, 7],      # Next even
    [7.860852, 5.219872, 22.0, 7],      # Two up
]

print("Testing chroma handling:")
for spec in test_specs:
    xyy = _munsell_specification_to_xyY(spec)
    print(f"  chroma={spec[2]:.6f} → xy=({xyy[0]:.9f}, {xyy[1]:.9f})")

# What about exact dataset entries?
print("\nChecking exact dataset values:")
exact_specs = [
    [7.5, 5.0, 20.0, 7],  # Should be exact
    [7.5, 5.0, 22.0, 7],  # Should be exact
    [10.0, 5.0, 20.0, 7], # Should be exact
]

for spec in exact_specs:
    xyy = _munsell_specification_to_xyY(spec)
    print(f"  {spec} → xy=({xyy[0]:.9f}, {xyy[1]:.9f})")

# Test with our converged Python value
print("\nPython's converged specification:")
converged = [7.937881783583, 5.219872126711, 20.447882669046, 7]
xyy_conv = _munsell_specification_to_xyY(converged)
print(f"  {converged}")
print(f"  → xy=({xyy_conv[0]:.12f}, {xyy_conv[1]:.12f})")

# Check the range of chromas in the dataset for 7.5R 5/X
print("\nAvailable chromas for 7.5R 5.0:")
from colour.notation.datasets.munsell.all import MUNSELL_COLOURS_ALL

available_chromas = []
for (hue, value, chroma), _ in MUNSELL_COLOURS_ALL:
    if hue == "7.5R" and value == 5.0:
        available_chromas.append(chroma)

available_chromas.sort()
print(f"  Available: {available_chromas}")