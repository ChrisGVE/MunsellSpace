#!/usr/bin/env python3
"""Inspect the parse_munsell_colour function to port it exactly"""

import inspect
from colour.notation.munsell import parse_munsell_colour

# Get the source code
source = inspect.getsource(parse_munsell_colour)
print("Python's parse_munsell_colour implementation:")
print("="*80)
print(source)
print("="*80)

# Test some examples
test_cases = [
    "N5.5",
    "5R 4/10",
    "2.5YR 6.5/8.2",
    "10GY 9/2",
]

print("\nTest cases:")
for case in test_cases:
    result = parse_munsell_colour(case)
    print(f"{case:15} -> {result}")