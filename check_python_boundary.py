#!/usr/bin/env python3
"""Check how Python handles hue boundaries."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import numpy as np
from colour.notation.munsell import normalise_munsell_specification

# Test specifications near boundaries
test_specs = [
    [0.0039, 3.91, 4.66, 3.0],   # Very close to 0
    [9.997, 3.91, 4.65, 4.0],     # Very close to 10
    [0.0, 3.91, 4.65, 4.0],       # Exactly 0
    [10.0, 3.91, 4.65, 4.0],      # Exactly 10
    [0.02, 3.91, 7.98, 6.0],      # Close to 0
    [9.99, 1.61, 8.16, 8.0],      # Close to 10
]

print("Testing Python's normalise_munsell_specification:")
print("=" * 60)

for spec in test_specs:
    normalized = normalise_munsell_specification(spec)
    print(f"Input:  [{spec[0]:6.3f}, {spec[1]:.2f}, {spec[2]:.2f}, {spec[3]:.0f}]")
    print(f"Output: [{normalized[0]:6.3f}, {normalized[1]:.2f}, {normalized[2]:.2f}, {normalized[3]:.0f}]")
    if spec[0] != normalized[0] or spec[3] != normalized[3]:
        print(f"  → CHANGED: hue {spec[0]:.3f}→{normalized[0]:.3f}, code {spec[3]:.0f}→{normalized[3]:.0f}")
    print()

print("=" * 60)
print("OBSERVATIONS:")
print("Python only adjusts when hue is EXACTLY 0.0")
print("Values like 0.0039 or 9.997 are left as-is")
print("This means the boundary issue is NOT in normalization")