#!/usr/bin/env python3
"""Test what interpolation method Python uses for our problematic cases"""

import numpy as np
from colour.notation.munsell import (
    interpolation_method_from_renotation_ovoid,
    munsell_colour_to_munsell_specification
)

# Test cases
test_specs = [
    # Our problematic green case
    ("8.548GY 9/6", "Rust boundary value for green"),
    ("8.548GY 9/8", "Rust boundary value for green"),
    ("8.0GY 9/12", "Python result (even chroma)"),
    ("8.0GY 9/14", "Higher chroma"),
    
    # Standard hues for comparison
    ("7.5GY 9/6", "Standard hue"),
    ("10.0GY 9/8", "Standard hue"),
    
    # Other families
    ("5.0R 5/10", "Red family"),
    ("2.5B 7/8", "Blue family"),
    ("3.75P 4/12", "Purple family"),
]

print("Testing interpolation methods:")
print("=" * 80)
print(f"{'Specification':20} {'Method':10} {'Description':40}")
print("-" * 80)

for munsell_str, desc in test_specs:
    try:
        # Parse specification
        spec = munsell_colour_to_munsell_specification(munsell_str)
        
        # Get interpolation method
        method = interpolation_method_from_renotation_ovoid(spec)
        
        print(f"{munsell_str:20} {method:10} {desc:40}")
        
    except Exception as e:
        print(f"{munsell_str:20} ERROR      {str(e)[:40]}")

# Now let's understand the exact criteria
print("\n\nUnderstanding interpolation method selection:")
print("=" * 80)

# Create a grid of test values to understand the pattern
print("\nTesting GY family at different values and chromas:")
print(f"{'Value':8} {'Chroma':8} {'Method':10}")
print("-" * 30)

for value in [1, 3, 5, 7, 9]:
    for chroma in [2, 6, 10, 14, 18]:
        try:
            spec = np.array([8.548, value, chroma, 4])  # 8.548GY
            method = interpolation_method_from_renotation_ovoid(spec)
            print(f"{value:8} {chroma:8} {method:10}")
        except:
            print(f"{value:8} {chroma:8} {'N/A':10}")