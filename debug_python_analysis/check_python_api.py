#!/usr/bin/env python3
"""Check the correct Python colour-science API"""

import colour
import colour.notation

# List all functions in colour.notation
print("Functions in colour.notation:")
print("=" * 80)
for attr in dir(colour.notation):
    if not attr.startswith('_'):
        obj = getattr(colour.notation, attr)
        if callable(obj):
            print(f"  {attr}")

print("\n\nChecking for Munsell-related functions:")
print("=" * 80)
for attr in dir(colour.notation):
    if 'munsell' in attr.lower():
        print(f"  {attr}")

# Check the munsell module
print("\n\nFunctions in colour.notation.munsell:")
print("=" * 80)
import colour.notation.munsell
for attr in dir(colour.notation.munsell):
    if not attr.startswith('_') and 'munsell' in attr.lower():
        obj = getattr(colour.notation.munsell, attr)
        if callable(obj):
            print(f"  {attr}")