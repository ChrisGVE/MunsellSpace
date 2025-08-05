"""Test renotation data lookup for specific values"""
import colour
import numpy as np

# Test case: Looking up data for hue=3.0, value=4.9, chroma=17.6, code=7 (R)
# This is what Python converged to for RGB [238,0,85]

# Let's check what xy coordinates Python would get for this specification
from colour.notation.munsell import munsell_specification_to_xyY

spec = [3.0, 4.9, 17.6, 7]  # hue, value, chroma, code
print(f"Testing Munsell spec: {spec}")

# This should give us the xy coordinates
xyY = munsell_specification_to_xyY(spec)
print(f"xyY from spec: {xyY}")

# Also test our Rust result
spec2 = [4.1, 5.0, 18.2, 7]
xyY2 = munsell_specification_to_xyY(spec2)
print(f"\nRust spec: {spec2}")
print(f"xyY from Rust spec: {xyY2}")

# Compare with target
target_xyY = colour.XYZ_to_xyY(colour.sRGB_to_XYZ([238/255, 0, 85/255]))
print(f"\nTarget xyY: {target_xyY}")
print(f"Distance from Python result: {np.linalg.norm(xyY[:2] - target_xyY[:2]):.6f}")
print(f"Distance from Rust result: {np.linalg.norm(xyY2[:2] - target_xyY[:2]):.6f}")