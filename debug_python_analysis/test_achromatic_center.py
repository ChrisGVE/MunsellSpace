#!/usr/bin/env python3
"""Test what achromatic center is being used"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Check achromatic center for value 9.5
achromatic_spec = np.array([0.0, 9.5, 0.0, 0])  # N 9.5
achromatic_xyY = munsell_specification_to_xyY(achromatic_spec)

print(f"Achromatic center for N 9.5:")
print(f"  x={achromatic_xyY[0]:.6f}, y={achromatic_xyY[1]:.6f}")

# Compare with Illuminant C
print(f"\nIlluminant C:")
print(f"  x=0.310060, y=0.316160")

# Check if they're the same
print(f"\nDifference:")
print(f"  dx={abs(achromatic_xyY[0] - 0.310060):.6f}")
print(f"  dy={abs(achromatic_xyY[1] - 0.316160):.6f}")

# Now let's check what happens with our target
target_x, target_y = 0.328945, 0.422625

print(f"\nTarget xy: ({target_x:.6f}, {target_y:.6f})")
print(f"Distance from Illuminant C: {np.sqrt((target_x - 0.310060)**2 + (target_y - 0.316160)**2):.6f}")
print(f"Distance from N 9.5 center: {np.sqrt((target_x - achromatic_xyY[0])**2 + (target_y - achromatic_xyY[1])**2):.6f}")