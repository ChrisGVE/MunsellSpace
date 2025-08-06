#!/usr/bin/env python3
"""Test if there are multiple local minima for the green color"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Target from RGB(204, 255, 170)
target_x, target_y = 0.328945, 0.422625

# Test different hue/chroma combinations around the solution space
print("Testing different Munsell specifications for distance to target:")
print("=" * 70)

best_dist = float('inf')
best_spec = None

for hue in np.arange(7.5, 9.0, 0.1):
    for chroma in np.arange(6.0, 14.0, 0.5):
        spec = np.array([hue, 9.5, chroma, 4])  # GY family
        xyY = munsell_specification_to_xyY(spec)
        dist = np.sqrt((target_x - xyY[0])**2 + (target_y - xyY[1])**2)
        
        if dist < 0.001:  # Very close matches
            print(f"{hue:3.1f}GY 9.5/{chroma:4.1f} -> dist={dist:.8f}")
            
        if dist < best_dist:
            best_dist = dist
            best_spec = (hue, chroma)

print(f"\nBest match: {best_spec[0]:.1f}GY 9.5/{best_spec[1]:.1f} with dist={best_dist:.8f}")

# Check the two specific solutions
print("\nComparing the two solutions:")
specs = [
    (8.5, 7.1),   # Rust result
    (8.0, 12.7),  # Python result
]

for hue, chroma in specs:
    spec = np.array([hue, 9.5, chroma, 4])
    xyY = munsell_specification_to_xyY(spec)
    dist = np.sqrt((target_x - xyY[0])**2 + (target_y - xyY[1])**2)
    print(f"{hue:3.1f}GY 9.5/{chroma:4.1f} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f}), dist={dist:.8f}")