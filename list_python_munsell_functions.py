#!/usr/bin/env python3
"""List all available functions in colour.notation.munsell"""

import colour.notation.munsell as munsell

print("Available functions in colour.notation.munsell:")
print("=" * 80)

# Get all attributes
attrs = dir(munsell)

# Filter to just functions and non-private attributes
functions = []
for attr in attrs:
    if not attr.startswith('_'):
        obj = getattr(munsell, attr)
        if callable(obj):
            functions.append(attr)

# Sort and print
functions.sort()
for func in functions:
    print(f"  {func}")