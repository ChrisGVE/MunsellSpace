#!/usr/bin/env python3
"""Inspect Munsell patterns and constants"""

from colour.notation.munsell import (
    MUNSELL_GRAY_PATTERN,
    MUNSELL_COLOUR_PATTERN,
    MUNSELL_HUE_LETTER_CODES,
    munsell_colour_to_munsell_specification,
    munsell_specification_to_munsell_colour,
)
import inspect

print("MUNSELL_GRAY_PATTERN:")
print(MUNSELL_GRAY_PATTERN)
print()

print("MUNSELL_COLOUR_PATTERN:")
print(MUNSELL_COLOUR_PATTERN)
print()

print("MUNSELL_HUE_LETTER_CODES:")
print(MUNSELL_HUE_LETTER_CODES)
print()

# Get source of the conversion functions
print("="*80)
print("munsell_colour_to_munsell_specification:")
print("="*80)
source = inspect.getsource(munsell_colour_to_munsell_specification)
print(source)

print("="*80)
print("munsell_specification_to_munsell_colour:")
print("="*80)
source = inspect.getsource(munsell_specification_to_munsell_colour)
print(source)