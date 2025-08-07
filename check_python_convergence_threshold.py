#!/usr/bin/env python3
"""Check Python's actual convergence behavior"""

from colour.notation.munsell import _munsell_specification_to_xyY
import numpy as np

# Test specification from Python's result for RGB(221, 238, 238)
spec = [7.105611, 9.277364, 2.084644, 3.0]
xyY_target = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Python's final specification:", spec)
print()

# Test different chroma values around Python's result
chromas = [2.08, 2.084, 2.0844, 2.08464, 2.084644, 2.08465, 2.085, 2.09]
print("Testing chromas around Python's result:")
for chroma in chromas:
    test_spec = [spec[0], spec[1], chroma, spec[3]]
    xy_result = _munsell_specification_to_xyY(test_spec)
    distance = np.sqrt((xy_result[0] - xyY_target[0])**2 + (xy_result[1] - xyY_target[1])**2)
    print(f"Chroma {chroma:.6f}: distance={distance:.12f}, < 1e-7? {distance < 1e-7}")

# Check what the actual threshold might be
print("\nTesting different thresholds:")
thresholds = [1e-6, 1e-7, 1e-8, 1e-9]
test_spec = [spec[0], spec[1], 2.084644, spec[3]]
xy_result = _munsell_specification_to_xyY(test_spec)
distance = np.sqrt((xy_result[0] - xyY_target[0])**2 + (xy_result[1] - xyY_target[1])**2)

for threshold in thresholds:
    print(f"Distance {distance:.12f} < {threshold:.0e}? {distance < threshold}")

# Check what distance we get at chroma 1.556 (our Rust result)
print("\nOur Rust result (chroma 1.556):")
test_spec = [spec[0], spec[1], 1.556, spec[3]]
xy_result = _munsell_specification_to_xyY(test_spec)
distance = np.sqrt((xy_result[0] - xyY_target[0])**2 + (xy_result[1] - xyY_target[1])**2)
print(f"Distance: {distance:.12f}")
print(f"Distance < 1e-7? {distance < 1e-7}")
print(f"Distance < 1e-6? {distance < 1e-6}")