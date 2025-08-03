#!/usr/bin/env python3
"""Check the actual distance values from our oscillating states."""

import numpy as np
from colour.notation.munsell import _munsell_specification_to_xyY
from colour.algebra import euclidean_distance

# Our target from red RGB(255,0,0)
target_xyy = np.array([0.640074499457, 0.329970510632, 0.212600000000])
print(f"Target xyY: x={target_xyy[0]:.12f}, y={target_xyy[1]:.12f}")

# Our oscillating states from the Rust trace
oscillating_specs = [
    # hue, value, chroma, code
    [7.860852, 5.219872, 20.860931, 7],  # State 1
    [8.203989, 5.219872, 19.989749, 7],  # State 2
    [7.860855, 5.219872, 20.771680, 7],  # Variations
]

print("\nChecking our oscillating states:")
for spec in oscillating_specs:
    xyy = _munsell_specification_to_xyY(spec)
    distance = euclidean_distance([xyy[0], xyy[1]], [target_xyy[0], target_xyy[1]])
    print(f"  spec: hue={spec[0]:.6f}, chroma={spec[2]:.6f}")
    print(f"    → xy=({xyy[0]:.12f}, {xyy[1]:.12f})")
    print(f"    → distance={distance:.12e}")

# What Rust reports:
print("\nWhat Rust reports:")
print("  State 1: xy=(0.634425, 0.329766), distance=0.00558001")
print("  State 2: xy=(0.636956, 0.334891), distance=0.00576055")

# Check those specific xy values
rust_xy_1 = [0.634425, 0.329766]
rust_xy_2 = [0.636956, 0.334891]

print("\nVerifying Rust's reported distances:")
dist_1 = euclidean_distance(rust_xy_1, [target_xyy[0], target_xyy[1]])
dist_2 = euclidean_distance(rust_xy_2, [target_xyy[0], target_xyy[1]])
print(f"  State 1 distance: {dist_1:.12e} (Rust reports 0.00558001)")
print(f"  State 2 distance: {dist_2:.12e} (Rust reports 0.00576055)")

# The actual converged Python value
print("\nPython's converged value:")
python_spec = [7.937881783583, 5.219872126711, 20.447882669046, 7]
python_xyy = _munsell_specification_to_xyY(python_spec)
python_dist = euclidean_distance([python_xyy[0], python_xyy[1]], [target_xyy[0], target_xyy[1]])
print(f"  spec: hue={python_spec[0]:.6f}, chroma={python_spec[2]:.6f}")
print(f"  → xy=({python_xyy[0]:.12f}, {python_xyy[1]:.12f})")
print(f"  → distance={python_dist:.12e}")