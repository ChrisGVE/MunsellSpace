#!/usr/bin/env python3
"""Trace the convergence for RGB(221, 238, 238) in Python"""

from colour.notation.munsell import xyY_to_munsell_colour, xyY_to_munsell_specification, _munsell_specification_to_xyY
import numpy as np

# From our Rust code, we know the xyY for RGB(221, 238, 238) is:
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print(f"Testing xyY: {xyY}")
print(f"Expected Munsell notation: {xyY_to_munsell_colour(xyY)}")
print()

# Get the specification
spec = xyY_to_munsell_specification(xyY)
print(f"Final specification: hue={spec[0]:.6f}, value={spec[1]:.6f}, chroma={spec[2]:.6f}, code={spec[3]}")
print()

# Let's test what happens if we try different chroma values
print("=== Testing different chroma values ===")
print("Finding which chroma gives us the closest xy to our target...")

test_chromas = [1.5, 1.541, 1.556, 1.6, 1.8, 2.0, 2.084, 2.1, 2.2]
best_chroma = None
best_distance = float('inf')

for chroma in test_chromas:
    test_spec = [spec[0], spec[1], chroma, spec[3]]
    try:
        xy_result = _munsell_specification_to_xyY(test_spec)
        distance = np.sqrt((xy_result[0] - xyY[0])**2 + (xy_result[1] - xyY[1])**2)
        print(f"Chroma {chroma:.3f}: xy=({xy_result[0]:.6f}, {xy_result[1]:.6f}), distance={distance:.9f}")
        
        if distance < best_distance:
            best_distance = distance
            best_chroma = chroma
    except Exception as e:
        print(f"Chroma {chroma:.3f}: FAILED - {e}")

print(f"\nBest chroma: {best_chroma:.3f} with distance: {best_distance:.9f}")
print(f"Python gets chroma: {spec[2]:.6f}")
print(f"Our Rust gets chroma: 1.556")
print()

# Test convergence threshold
threshold = 1e-7
print(f"Convergence threshold: {threshold}")
print(f"Best distance ({best_distance:.9f}) < threshold ({threshold})? {best_distance < threshold}")