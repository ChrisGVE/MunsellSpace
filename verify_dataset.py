#!/usr/bin/env python3
"""Verify that our Rust dataset matches Python colour-science."""

import sys
import os

# Add colour-science to path
sys.path.insert(0, '/Users/chris/Dropbox/dev/projects/libraries/MunsellSpace/venv_comparison/lib/python3.13/site-packages')

from colour.notation.datasets.munsell.all import MUNSELL_COLOURS_ALL

# Print first 10 entries from Python dataset
print("Python dataset (first 10 entries):")
for i, ((hue, value, chroma), (x, y, Y)) in enumerate(MUNSELL_COLOURS_ALL[:10]):
    print(f'    (("{hue}", {value}, {chroma}), ({x}, {y}, {Y})),')
    
print("\nTotal entries in Python:", len(MUNSELL_COLOURS_ALL))

# Check specific entries that appear in our Rust code
test_entries = [
    ("2.5GY", 0.2, 2.0),
    ("5GY", 0.2, 2.0),
    ("7.5GY", 0.2, 2.0),
]

print("\nVerifying specific entries:")
for hue, value, chroma in test_entries:
    for entry in MUNSELL_COLOURS_ALL:
        if entry[0] == (hue, value, chroma):
            print(f"Python: {entry}")
            break
    else:
        print(f"NOT FOUND: ({hue}, {value}, {chroma})")

# Count how many entries we have
rust_count = 0
with open('src/munsell_renotation_data_entries.rs', 'r') as f:
    for line in f:
        if line.strip().startswith('(("'):
            rust_count += 1
            
print(f"\nRust dataset entries: {rust_count}")
print(f"Python dataset entries: {len(MUNSELL_COLOURS_ALL)}")
print(f"Match: {rust_count == len(MUNSELL_COLOURS_ALL)}")