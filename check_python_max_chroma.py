#!/usr/bin/env python3
"""Check how Python handles maximum chroma"""

from colour.notation.munsell import maximum_chroma_from_renotation
import numpy as np

# Test cases where we saw chroma capping
test_cases = [
    (2.8, 4.6, 9),  # P family, value 4.6 - was capped at 15.0 instead of 25.9
    (7.3, 4.5, 9),  # P family, value 4.5 - was capped at 15.0 instead of 21.1
    (2.0, 3.3, 9),  # P family, value 3.3 - was capped at 15.0 instead of 19.1
]

print("Python maximum_chroma_from_renotation:")
for hue, value, code in test_cases:
    # Create specification array [hue, value, code] (no chroma needed)
    specification = np.array([hue, value, code])
    max_chroma = maximum_chroma_from_renotation(specification)
    print(f"  Hue={hue}, Value={value}, Code={code} -> Max chroma: {max_chroma}")

# Also check what the actual renotation data shows
print("\nChecking actual high-chroma colors in renotation data:")
from colour.notation.munsell import MUNSELL_RENOTATION_DATA

# Find high chroma entries
high_chromas = []
for spec, xyY in MUNSELL_RENOTATION_DATA.items():
    hue_str, value, chroma = spec
    if chroma > 20:
        high_chromas.append((hue_str, value, chroma))

# Sort by chroma
high_chromas.sort(key=lambda x: x[2], reverse=True)

print("\nTop 10 highest chromas in renotation data:")
for hue_str, value, chroma in high_chromas[:10]:
    print(f"  {hue_str} {value}/{chroma}")