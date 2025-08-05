#!/usr/bin/env python3
"""Test to understand Python's inner loop behavior"""

import numpy as np
import colour
import colour.notation.munsell as munsell

# Monkey patch to trace inner loop
original_xyY_to_munsell = munsell._xyY_to_munsell_specification

def traced_xyY_to_munsell(xyY):
    """Traced version to see inner loop behavior"""
    # Convert RGB [238,0,85] which seems problematic
    print(f"\n=== Tracing xyY {xyY} ===")
    
    # Run original but we'll look at the source to understand
    result = original_xyY_to_munsell(xyY)
    
    return result

# Test
rgb = [238/255, 0, 85/255]
XYZ = colour.sRGB_to_XYZ(rgb)
xyY = colour.XYZ_to_xyY(XYZ)

print("Testing RGB [238,0,85]")
print(f"xyY: {xyY}")

# Instead, let's manually trace key parts
print("\nChecking inner loop logic from Python source:")
print("Line 120-124: while (np.sign(np.min(phi_differences_data)) == np.sign(np.max(phi_differences_data)) and extrapolate is False):")
print("Line 157-158: if len(phi_differences_data) >= 2: extrapolate = True")
print("Line 160: if extrapolate is False: [add point to phi_differences_data]")
print("\nThis means:")
print("1. Start with 1 point (phi_current_difference)")
print("2. Add 1 more point (iteration 1)")
print("3. Set extrapolate=True when we have 2 points")
print("4. Don't add any more points after that")
print("5. Exit loop and interpolate/extrapolate with just 2 points")

# Let's also check what the condition means
test_data = [[1.5, 2.0], [-1.5, -2.0], [-1.5, 2.0], [0.0, 1.0]]
for data in test_data:
    same_sign = np.sign(np.min(data)) == np.sign(np.max(data))
    print(f"\nData {data}: same sign? {same_sign}")