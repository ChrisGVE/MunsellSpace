#!/usr/bin/env python3
"""Check if Python rounds chroma in xy_from_renotation_ovoid."""

import numpy as np

# Simulate what Python does in xy_from_renotation_ovoid
def check_chroma_rounding(chroma):
    # Python's logic from munsell.py line 2335
    # chroma = as_float_scalar(np.around(specification[2] / 2)) * 2
    chroma_rounded = np.around(chroma / 2) * 2
    return chroma_rounded

test_chromas = [20.0, 20.5, 20.860931, 21.0, 21.5, 22.0]

print("Python's chroma rounding in xy_from_renotation_ovoid:")
for c in test_chromas:
    rounded = check_chroma_rounding(c)
    print(f"  chroma={c:.6f} → rounded={rounded:.1f}")

print("\nThis rounding is ONLY used for direct dataset lookup.")
print("The iterative algorithm keeps fractional chromas and interpolates between them!")

# Let's verify this by checking what Python actually returns
from colour.notation.munsell import _munsell_specification_to_xyY

print("\nVerifying Python's actual behavior:")
spec1 = [7.5, 5.0, 20.86, 7]  # Exact hue, should use rounding
spec2 = [7.86, 5.0, 20.86, 7]  # Non-exact hue, should interpolate

print(f"Exact hue (7.5): {spec1}")
xyy1 = _munsell_specification_to_xyY(spec1)
print(f"  → xy=({xyy1[0]:.9f}, {xyy1[1]:.9f})")

print(f"Non-exact hue (7.86): {spec2}")
xyy2 = _munsell_specification_to_xyY(spec2)
print(f"  → xy=({xyy2[0]:.9f}, {xyy2[1]:.9f})")

# The difference shows interpolation is happening
print(f"\nDifference: dx={xyy2[0]-xyy1[0]:.9f}, dy={xyy2[1]-xyy1[1]:.9f}")