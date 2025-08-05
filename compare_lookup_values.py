"""Compare lookup values between Python and what Rust would get"""
import colour
from colour.notation.munsell import munsell_specification_to_xyY

# Test case: 4.1R 5.0/18.2 (what Rust gets)
spec1 = [4.1, 5.0, 18.2, 7]  # R = code 7
xyY1 = munsell_specification_to_xyY(spec1)
print(f"Rust result 4.1R 5.0/18.2:")
print(f"  xyY: {xyY1}")
print(f"  xy: ({xyY1[0]:.6f}, {xyY1[1]:.6f})")

# Test case: 3.0R 4.9/17.6 (what Python gets)
spec2 = [3.0, 4.9, 17.6, 7]
xyY2 = munsell_specification_to_xyY(spec2)
print(f"\nPython result 3.0R 4.9/17.6:")
print(f"  xyY: {xyY2}")
print(f"  xy: ({xyY2[0]:.6f}, {xyY2[1]:.6f})")

# Target
target_xy = [0.558939, 0.285274]
print(f"\nTarget xy: ({target_xy[0]:.6f}, {target_xy[1]:.6f})")

# Distances
import numpy as np
dist1 = np.linalg.norm(np.array(target_xy) - xyY1[:2])
dist2 = np.linalg.norm(np.array(target_xy) - xyY2[:2])
print(f"\nDistance from Rust result: {dist1:.6f}")
print(f"Distance from Python result: {dist2:.6f}")

# Let's check some intermediate values
print("\n--- Checking intermediate hue/chroma combinations ---")
for hue in [3.0, 3.5, 4.0, 4.1]:
    for chroma in [17.6, 18.0, 18.2]:
        spec = [hue, 5.0, chroma, 7]
        xyY = munsell_specification_to_xyY(spec)
        dist = np.linalg.norm(np.array(target_xy) - xyY[:2])
        print(f"{hue}R 5.0/{chroma} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f}), dist={dist:.6f}")