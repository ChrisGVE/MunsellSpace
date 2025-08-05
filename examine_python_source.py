#!/usr/bin/env python3
"""Examine Python colour-science source to understand exact implementation"""

import inspect
from colour.notation import munsell

# Get the main conversion functions
print("=== Main Conversion Functions ===")
print("\n1. xyY_to_munsell_specification:")
print(inspect.getsource(munsell.xyY_to_munsell_specification))

print("\n" + "="*80 + "\n")
print("2. munsell_specification_to_xyY:")
print(inspect.getsource(munsell.munsell_specification_to_xyY))