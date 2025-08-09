#!/usr/bin/env python3
"""Test how hue values should be normalized according to Munsell standard."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour.notation.munsell import parse_munsell_colour

# Test parsing various notations
test_notations = [
    "0.2R 1.6/7.9",   # What Python outputs
    "10.2R 1.6/7.9",  # What if we try > 10?
    "0.0R 1.6/7.9",   # Exactly 0
    "10.0R 1.6/7.9",  # Exactly 10
    "1.0R 1.6/7.9",   # Minimum valid
    "9.9R 1.6/7.9",   # Near max
]

print("Testing Munsell notation parsing:")
print("=" * 70)

for notation in test_notations:
    try:
        result = parse_munsell_colour(notation)
        hue = result[0] if result[0] is not None else "N/A"
        value = result[1]
        chroma = result[2] if result[2] is not None else "N/A"
        code = result[3] if result[3] is not None else "N/A"
        print(f"{notation:15} -> hue={hue:5}, value={value:4}, chroma={chroma:4}, code={code}")
    except Exception as e:
        print(f"{notation:15} -> ERROR: {e}")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("Python's colour-science accepts hue values < 1.0 in string notation")
print("This is technically invalid according to Munsell standard (1-10 range)")
print("But the library treats it as valid and uses 0-10 range internally")