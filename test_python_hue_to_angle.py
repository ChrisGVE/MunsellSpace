#!/usr/bin/env python3
"""Test how Python's hue_to_hue_angle function works with the exact values from our trace"""

import numpy as np
from colour.notation.munsell import hue_to_hue_angle

# Test the exact values from the trace divergence
# Python trace shows: hue=[5.2417998370553125, 3.0]
# Rust trace shows: hue=5.2417998371, code=3

# Try calling with array format as Python does
hue_array = np.array([5.2417998370553125, 3.0])
result_array = hue_to_hue_angle(hue_array)
print(f"Python hue_to_hue_angle([5.2417998370553125, 3.0]) = {result_array}")

# Also try with scalar and code
hue_value = 5.2417998370553125
code = 3
# Check if we can pass them separately
try:
    result_separate = hue_to_hue_angle(hue_value, code)
    print(f"Python hue_to_hue_angle(5.2417998370553125, 3) = {result_separate}")
except:
    print("Cannot pass hue and code as separate parameters")

# Let's also inspect the function signature
import inspect
sig = inspect.signature(hue_to_hue_angle)
print(f"\nFunction signature: {sig}")

# Let's test what the function actually does internally
print("\n=== Detailed calculation ===")
hue = 5.2417998370553125
code = 3

# Follow the Python formula exactly
raw = (17 - code) % 10 + (hue / 10) - 0.5
print(f"raw = (17 - {code}) % 10 + ({hue} / 10) - 0.5 = {raw}")

# Python's modulo
if raw < 0:
    single_hue = (raw % 10) + 10
else:
    single_hue = raw % 10
print(f"single_hue = {single_hue}")

# Interpolation breakpoints
breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0]
angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0]

# Find which segment single_hue falls into
for i in range(len(breakpoints)-1):
    if single_hue >= breakpoints[i] and single_hue <= breakpoints[i+1]:
        t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i])
        angle = angles[i] + t * (angles[i+1] - angles[i])
        print(f"Interpolation: segment [{breakpoints[i]}, {breakpoints[i+1]}], t={t:.6f}")
        print(f"angle = {angles[i]} + {t:.6f} * ({angles[i+1]} - {angles[i]}) = {angle}")
        break

# Compare with Python's result
print(f"\nPython's result: {result_array}")
print(f"Manual calculation: {angle}")
print(f"Difference: {abs(result_array - angle)}")