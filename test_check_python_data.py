#!/usr/bin/env python3
"""Check what renotation data Python has"""

from colour.notation.munsell.dataset import MUNSELL_COLOURS_ALL
import numpy as np

# Look for specific entries
targets = [
    ("5YR", 5.0, 20.0),
    ("5YR", 5.0, 14.0),
    ("5R", 5.0, 20.0),
    ("5R", 5.0, 14.0),
]

print("Checking Python's renotation data:\n")

# MUNSELL_COLOURS_ALL is a list of tuples
for hue_str, value, chroma in targets:
    found = False
    for entry in MUNSELL_COLOURS_ALL:
        munsell_tuple, xyy = entry
        # munsell_tuple is (hue_str, value, chroma)
        if (munsell_tuple[0] == hue_str and 
            abs(munsell_tuple[1] - value) < 0.01 and 
            abs(munsell_tuple[2] - chroma) < 0.01):
            print(f"Found {munsell_tuple}: xyY = {xyy}")
            found = True
            break
    
    if not found:
        print(f"NOT FOUND: {hue_str} {value}/{chroma}")

# Also check what xyY_from_renotation returns
print("\nChecking xyY_from_renotation function:")
from colour.notation.munsell import xyY_from_renotation

spec = np.array([5.0, 5, 20, 1])  # 5YR 5/20
try:
    result = xyY_from_renotation(spec)
    print(f"xyY_from_renotation([5.0, 5, 20, 1]) = {result}")
    
    # Check if this is interpolated or exact
    found_exact = False
    for entry in MUNSELL_COLOURS_ALL:
        munsell_tuple, xyy = entry
        if (munsell_tuple[0] == "5YR" and 
            abs(munsell_tuple[1] - 5.0) < 0.01 and 
            abs(munsell_tuple[2] - 20.0) < 0.01):
            print(f"  Exact match in data: {xyy}")
            found_exact = True
            break
    if not found_exact:
        print(f"  Not an exact match - must be interpolated")
except Exception as e:
    print(f"Error: {e}")