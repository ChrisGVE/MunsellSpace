#!/usr/bin/env python3

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY, xyY_to_munsell_colour

# RGB (34, 17, 119) = #221177
rgb = np.array([34, 17, 119]) / 255.0

# Convert to xyY through colour library
xyz = sRGB_to_XYZ(rgb)
xyY = XYZ_to_xyY(xyz)

print(f"RGB: {rgb * 255}")
print(f"XYZ: {xyz}")
print(f"xyY: ({xyY[0]:.10f}, {xyY[1]:.10f}, {xyY[2]:.10f})")
print()

# Now convert to Munsell
munsell = xyY_to_munsell_colour(xyY)
print(f"Python Munsell: {munsell}")

# Let's also manually parse the result
if '/' in munsell:
    parts = munsell.split(' ')
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    value = float(value_chroma[0])
    chroma = float(value_chroma[1])
    print(f"Parsed: Hue={hue_part}, Value={value:.3f}, Chroma={chroma:.3f}")
    
# Try manual conversion with our exact xyY values from Rust
print("\n=== Testing with Rust's xyY values ===")
xyY_rust = np.array([0.175340, 0.086753, 0.020725])
munsell_rust = xyY_to_munsell_colour(xyY_rust)
print(f"Rust xyY input: ({xyY_rust[0]:.6f}, {xyY_rust[1]:.6f}, {xyY_rust[2]:.6f})")
print(f"Python result: {munsell_rust}")

# Parse this result too
if '/' in munsell_rust:
    parts = munsell_rust.split(' ')
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    value = float(value_chroma[0])
    chroma = float(value_chroma[1])
    print(f"Parsed: Hue={hue_part}, Value={value:.3f}, Chroma={chroma:.3f}")