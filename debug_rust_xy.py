#!/usr/bin/env python3
"""Compare exact xy coordinates between Python and Rust."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour, munsell_colour_to_xyY

# Test pure red
rgb = np.array([1.0, 0.0, 0.0])  # Normalized RGB
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"Input xyY: x={xyy[0]:.6f}, y={xyy[1]:.6f}, Y={xyy[2]:.6f}")

# Convert to Munsell
munsell = xyY_to_munsell_colour(xyy)
print(f"Final Munsell: {munsell}")

# Convert back to xyY to see what coordinates Python converged to
xyy_back = munsell_colour_to_xyY(munsell)
print(f"Converged xyY: x={xyy_back[0]:.6f}, y={xyy_back[1]:.6f}, Y={xyy_back[2]:.6f}")

# Calculate difference
diff_x = abs(xyy[0] - xyy_back[0])
diff_y = abs(xyy[1] - xyy_back[1])
euclidean = np.sqrt(diff_x**2 + diff_y**2)
print(f"Difference: Δx={diff_x:.6f}, Δy={diff_y:.6f}, euclidean={euclidean:.6f}")

print("\n=== Rust values for comparison ===")
print("Rust Input: x=0.640000, y=0.330000, Y=0.212673")
print("Rust Result: 8.1R 5.2/19.6")
rust_converged_x = 0.642843  # From the iteration output
rust_converged_y = 0.330119
print(f"Rust Converged: x={rust_converged_x:.6f}, y={rust_converged_y:.6f}")

# Calculate Rust difference  
rust_diff_x = abs(0.640000 - rust_converged_x)
rust_diff_y = abs(0.330000 - rust_converged_y)
rust_euclidean = np.sqrt(rust_diff_x**2 + rust_diff_y**2)
print(f"Rust Difference: Δx={rust_diff_x:.6f}, Δy={rust_diff_y:.6f}, euclidean={rust_euclidean:.6f}")