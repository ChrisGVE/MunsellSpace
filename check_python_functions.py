#!/usr/bin/env python3

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import colour
import inspect

# Check what hue_to_ASTM_hue actually does
print("=== hue_to_ASTM_hue source ===")
print(inspect.getsource(colour.notation.munsell.hue_to_ASTM_hue))
print()

# Test it
print("=== Testing hue_to_ASTM_hue ===")
test_cases = [(5.0, 6), (2.5, 6), (7.5, 5)]
for hue, code in test_cases:
    result = colour.notation.munsell.hue_to_ASTM_hue(hue, code)
    print(f"hue={hue}, code={code} -> {result}")

print("\n=== hue_to_hue_angle source ===")
print(inspect.getsource(colour.notation.munsell.hue_to_hue_angle))