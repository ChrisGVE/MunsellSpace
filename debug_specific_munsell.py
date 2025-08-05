"""Debug specific Munsell coordinates"""
import colour
from colour.notation.munsell import munsell_specification_to_xyY
import numpy as np

# Test what our algorithm converged to
spec = [4.130, 4.950, 18.159, 7]  # 4.130R 4.950/18.159
xyY = munsell_specification_to_xyY(spec)
print(f"4.130R 4.950/18.159 -> xy=({xyY[0]:.6f}, {xyY[1]:.6f})")

# Test what Python gets
rgb = [238/255, 0, 85/255]
XYZ = colour.sRGB_to_XYZ(rgb)
xyY_target = colour.XYZ_to_xyY(XYZ)
print(f"\nTarget from RGB [238,0,85]: xy=({xyY_target[0]:.6f}, {xyY_target[1]:.6f})")

# Get what Python converts to
munsell = colour.notation.munsell.xyY_to_munsell_colour(xyY_target)
print(f"Python result: {munsell}")

# Test variations around our result
print("\n--- Testing variations ---")
for hue in [3.0, 3.5, 4.0, 4.1, 4.13]:
    for chroma in [17.6, 18.0, 18.16, 18.5]:
        spec = [hue, 4.950, chroma, 7]
        xyY = munsell_specification_to_xyY(spec)
        dist = np.linalg.norm(np.array([xyY[0], xyY[1]]) - np.array([xyY_target[0], xyY_target[1]]))
        print(f"{hue}R 4.950/{chroma} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f}), dist={dist:.6f}")