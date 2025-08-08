#!/usr/bin/env python3
"""Test Python's maximum_chroma_from_renotation for high values"""

import sys
sys.path.insert(0, 'InkyFingers')

from colour.notation.munsell_renotation import maximum_chroma_from_renotation
import numpy as np

# Test for GY family (code 4) at high values
print("Testing maximum chroma for GY (code 4) at various values:")
print()

for value in [9.0, 9.1, 9.2, 9.3, 9.35, 9.4, 9.5, 9.6, 9.8, 9.9]:
    # Test at hue 8.5 (middle of GY)
    try:
        max_chroma = maximum_chroma_from_renotation(8.5, value, 4)
        print(f"Value {value:.2f}: max_chroma = {max_chroma:.2f}")
    except Exception as e:
        print(f"Value {value:.2f}: ERROR - {e}")

print()
print("For RGB(187,255,153):")
print("  Expected chroma: 12.8")
print("  Value: 9.35")
max_chroma_935 = maximum_chroma_from_renotation(8.5, 9.35, 4)
print(f"  Max chroma at 9.35: {max_chroma_935:.2f}")
print(f"  Chroma 12.8 is {'VALID' if 12.8 <= max_chroma_935 else 'INVALID'}")