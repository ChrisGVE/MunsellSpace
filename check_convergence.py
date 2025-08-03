#!/usr/bin/env python3
"""Check exact convergence behavior in Python."""

import numpy as np
from colour.notation.munsell import (
    _xyY_to_munsell_specification,
    _munsell_specification_to_xyY,
    THRESHOLD_INTEGER
)
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.constants import EPSILON

print(f"EPSILON = {EPSILON}")
print(f"THRESHOLD_INTEGER = {THRESHOLD_INTEGER}")
print(f"convergence_threshold = THRESHOLD_INTEGER / 1e4 = {THRESHOLD_INTEGER / 1e4}")

# Let's trace the exact calculation for red
rgb = np.array([1.0, 0.0, 0.0])
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"\nInput xyY: x={xyy[0]:.12f}, y={xyy[1]:.12f}, Y={xyy[2]:.12f}")

# Let's see what the algorithm returns
spec = _xyY_to_munsell_specification(xyy)
print(f"Output spec: hue={spec[0]:.12f}, value={spec[1]:.12f}, chroma={spec[2]:.12f}, code={spec[3]}")

# Now let's convert back to xyY and see the difference
xyy_back = _munsell_specification_to_xyY(spec)
print(f"Spec→xyY: x={xyy_back[0]:.12f}, y={xyy_back[1]:.12f}, Y={xyy_back[2]:.12f}")

# Calculate the distance
diff_x = xyy[0] - xyy_back[0]
diff_y = xyy[1] - xyy_back[1]
distance = np.sqrt(diff_x**2 + diff_y**2)
print(f"\nDistance: {distance:.12e}")
print(f"Convergence threshold: {THRESHOLD_INTEGER / 1e4:.12e}")
print(f"Converged: {distance < THRESHOLD_INTEGER / 1e4}")

# Check if Python uses a different convergence check
print("\n\nLet's manually check convergence criteria...")
print(f"diff_x = {diff_x:.12e}")
print(f"diff_y = {diff_y:.12e}")
print(f"Euclidean distance = {distance:.12e}")