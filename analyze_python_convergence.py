#!/usr/bin/env python3
"""Analyze how Python handles the stuck case when phi_input == phi_current."""

import numpy as np
from colour.notation.munsell import _xyY_to_munsell_specification, _munsell_specification_to_xyY
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.algebra import euclidean_distance

# Let's directly test with our problematic specification
# hue=7.860852, value=5.219872, chroma=20.86, code=7
test_spec = [7.860852, 5.219872126711, 20.86, 7]

print("Testing with specification that causes oscillation in Rust:")
print(f"  spec = {test_spec}")

# Convert to xyY
xyy_from_spec = _munsell_specification_to_xyY(test_spec)
print(f"  spec→xyY: x={xyy_from_spec[0]:.12f}, y={xyy_from_spec[1]:.12f}, Y={xyy_from_spec[2]:.12f}")

# Now convert back to specification
spec_back = _xyY_to_munsell_specification(xyy_from_spec)
print(f"  xyY→spec: hue={spec_back[0]:.12f}, value={spec_back[1]:.12f}, chroma={spec_back[2]:.12f}, code={spec_back[3]}")

# Calculate distance
target_xyy = np.array([0.640074499457, 0.329970510632, 0.212600000000])  # Our target
distance = euclidean_distance([xyy_from_spec[0], xyy_from_spec[1]], [target_xyy[0], target_xyy[1]])
print(f"  Distance from target: {distance:.12e}")

# Check if Python can converge from this point
print("\nChecking Python's convergence from this point:")
final_spec = _xyY_to_munsell_specification(target_xyy)
print(f"  Target spec: hue={final_spec[0]:.12f}, value={final_spec[1]:.12f}, chroma={final_spec[2]:.12f}")

# Let's trace what happens with slight variations
print("\nTesting convergence with variations around stuck point:")
for hue_offset in [-0.01, -0.001, 0, 0.001, 0.01]:
    test_hue = 7.860852 + hue_offset
    test_spec_var = [test_hue, 5.219872126711, 20.86, 7]
    xyy_var = _munsell_specification_to_xyY(test_spec_var)
    dist = euclidean_distance([xyy_var[0], xyy_var[1]], [target_xyy[0], target_xyy[1]])
    print(f"  hue={test_hue:.6f} → distance={dist:.12e}")