#!/usr/bin/env python3
"""Test how Python's _xy_from_renotation handles high chromas"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xy
from colour.utilities import domain_range_scale

# Decompose what happens for a high chroma
# Green: [0.0, 8.0, 22.0, 5.0]

# Try to understand the interpolation layers
print("Testing munsell_specification_to_xy with high chroma:")
spec = np.array([0.0, 8.0, 22.0, 5.0])
with domain_range_scale("ignore"):
    xy = munsell_specification_to_xy(spec)
print(f"Result: {xy}")

# Test what maximum chromas are available
print("\nTesting maximum available chromas at value 8:")
for chroma in [14, 16, 18, 20, 22, 24]:
    spec_test = np.array([5.0, 8.0, float(chroma), 5.0])  # Use 5Y which should exist
    try:
        with domain_range_scale("ignore"):
            xy = munsell_specification_to_xy(spec_test)
        print(f"  5Y 8/{chroma}: Success - xy={xy}")
    except Exception as e:
        print(f"  5Y 8/{chroma}: Failed - {e}")

# Now test if Python extrapolates when calling _munsell_specification_to_xy
print("\nDirect test of high chroma handling:")
# Force a specification that requires extrapolation
spec_high = np.array([2.5, 8.0, 24.0, 5.0])  # 2.5Y 8/24
try:
    with domain_range_scale("ignore"):
        xy_high = munsell_specification_to_xy(spec_high)
    print(f"High chroma (24): {xy_high}")
    
    # Compare with lower chromas
    spec_20 = np.array([2.5, 8.0, 20.0, 5.0])
    xy_20 = munsell_specification_to_xy(spec_20)
    print(f"Chroma 20: {xy_20}")
    
    spec_18 = np.array([2.5, 8.0, 18.0, 5.0])
    xy_18 = munsell_specification_to_xy(spec_18)
    print(f"Chroma 18: {xy_18}")
    
    # Check if it's linear extrapolation
    delta_x = xy_20[0] - xy_18[0]
    delta_y = xy_20[1] - xy_18[1]
    predicted_x = xy_20[0] + 2 * delta_x  # 2 steps from 20 to 24
    predicted_y = xy_20[1] + 2 * delta_y
    print(f"\nPredicted xy for chroma 24 by extrapolation: [{predicted_x:.6f}, {predicted_y:.6f}]")
    print(f"Actual xy: [{xy_high[0]:.6f}, {xy_high[1]:.6f}]")
    
except Exception as e:
    print(f"Failed: {e}")