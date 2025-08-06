#!/usr/bin/env python3
"""Test what's special about hue 0"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xy
from colour.utilities import domain_range_scale

# Test hue=0 which is succeeding
print("Testing hue=0.0 at various chromas:")
for chroma in [14, 16, 18, 20, 22, 24, 26]:
    spec = np.array([0.0, 8.0, float(chroma), 5.0])  # 0Y 8/chroma
    try:
        with domain_range_scale("ignore"):
            xy = munsell_specification_to_xy(spec)
        print(f"  0Y 8/{chroma}: Success - xy={xy}")
    except Exception as e:
        print(f"  0Y 8/{chroma}: Failed")

print("\nTesting hue=10.0 (which should be equivalent):")
for chroma in [14, 16, 18, 20, 22, 24]:
    spec = np.array([10.0, 8.0, float(chroma), 5.0])  # 10Y 8/chroma
    try:
        with domain_range_scale("ignore"):
            xy = munsell_specification_to_xy(spec)
        print(f"  10Y 8/{chroma}: Success - xy={xy}")
    except Exception as e:
        print(f"  10Y 8/{chroma}: Failed")

# What about other standard hues?
print("\nTesting other standard hues at chroma 22:")
for hue in [0.0, 2.5, 5.0, 7.5, 10.0]:
    spec = np.array([hue, 8.0, 22.0, 5.0])
    try:
        with domain_range_scale("ignore"):
            xy = munsell_specification_to_xy(spec)
        print(f"  {hue}Y 8/22: Success - xy={xy}")
    except Exception as e:
        print(f"  {hue}Y 8/22: Failed")