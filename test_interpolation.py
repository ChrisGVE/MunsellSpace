"""Test Python's interpolation behavior"""

import numpy as np
from colour.algebra import LinearInterpolator, Extrapolator

# Test case from our debug output
phi_differences = [7.301094632171612, 0.4943931600425344]
hue_angles_differences = [0.0, -7.301094632171612]

# Sort by phi differences
indices = np.argsort(phi_differences)
sorted_phi = np.array(phi_differences)[indices]
sorted_hue = np.array(hue_angles_differences)[indices]

print(f"Sorted phi: {sorted_phi}")
print(f"Sorted hue: {sorted_hue}")

# Create interpolator and extrapolator
interpolator = LinearInterpolator(sorted_phi, sorted_hue)
extrapolator = Extrapolator(interpolator)

# Evaluate at 0
result = extrapolator(0.0)
print(f"\nExtrapolator(0.0) = {result}")
print(f"Modulo 360: {result % 360}")

# Also test direct np.interp
np_result = np.interp(0.0, sorted_phi, sorted_hue)
print(f"\nnp.interp(0.0) = {np_result}")

# Test extrapolation formula manually
# Linear extrapolation: y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
x1, x2 = sorted_phi[0], sorted_phi[1]
y1, y2 = sorted_hue[0], sorted_hue[1]
manual = y1 + (0.0 - x1) * (y2 - y1) / (x2 - x1)
print(f"\nManual extrapolation: {manual}")