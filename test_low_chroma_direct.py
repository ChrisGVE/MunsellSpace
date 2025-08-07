#!/usr/bin/env python3
"""Test low chroma handling directly"""

from colour.notation.munsell import _munsell_specification_to_xyY
import numpy as np

# Test specification that Rust converges to
rust_spec = [7.181, 9.277, 1.556, 3.0]  # What Rust gets
python_spec = [7.105611, 9.277364, 2.084644, 3.0]  # What Python gets

# Target xyY for RGB(221, 238, 238)
xyY_target = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Testing low chroma handling:")
print(f"Rust spec: {rust_spec}")
print(f"Python spec: {python_spec}")
print(f"Target xyY: {xyY_target}")
print()

# Test both specs
for name, spec in [("Rust", rust_spec), ("Python", python_spec)]:
    xy_result = _munsell_specification_to_xyY(spec)
    distance = np.sqrt((xy_result[0] - xyY_target[0])**2 + (xy_result[1] - xyY_target[1])**2)
    print(f"{name} spec -> xy=({xy_result[0]:.6f}, {xy_result[1]:.6f})")
    print(f"  Distance from target: {distance:.9f}")
    print(f"  Converged (< 1e-7)? {distance < 1e-7}")
    print()

# Test intermediate chromas
print("Testing chroma progression from 1.556 to 2.084:")
chromas = np.linspace(1.556, 2.084, 10)
for chroma in chromas:
    spec = [7.105611, 9.277364, chroma, 3.0]  # Use Python's hue/value
    xy_result = _munsell_specification_to_xyY(spec)
    distance = np.sqrt((xy_result[0] - xyY_target[0])**2 + (xy_result[1] - xyY_target[1])**2)
    print(f"  Chroma {chroma:.4f}: distance={distance:.9f}, converged? {distance < 1e-7}")