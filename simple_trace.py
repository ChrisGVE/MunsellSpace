#!/usr/bin/env python3
"""Simple trace of problematic color"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import munsell
import subprocess

# Problematic color: #221177 
r, g, b = 34, 17, 119
print(f"Testing RGB({r}, {g}, {b}) = #{r:02x}{g:02x}{b:02x}")
print("="*50)

# Python conversion
srgb = [r/255.0, g/255.0, b/255.0]
xyz = sRGB_to_XYZ(srgb)
xyy = XYZ_to_xyY(xyz)
spec = munsell.xyY_to_munsell_specification(xyy)

print(f"Python specification: {spec}")
print(f"  Hue: {spec[0]:.10f}")
print(f"  Value: {spec[1]:.10f}")
print(f"  Chroma: {spec[2]:.10f}")
print(f"  Code: {spec[3]}")

notation = munsell.munsell_specification_to_munsell_colour(spec, 1, 1, 1)
print(f"Python notation: {notation}")

# Rust conversion
print("\n--- Rust ---")
result = subprocess.run(
    ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
    capture_output=True, text=True
)

if result.returncode == 0 and 'Specification:' in result.stdout:
    # Parse the specification line
    for line in result.stdout.split('\n'):
        if 'Specification:' in line:
            # Parse [hue, value, chroma, code]
            spec_str = line.split('Specification:')[1].strip()
            spec_str = spec_str.strip('[]')
            rust_spec = [float(x) for x in spec_str.split(',')]
            print(f"Rust specification: {rust_spec}")
            print(f"  Hue: {rust_spec[0]:.10f}")
            print(f"  Value: {rust_spec[1]:.10f}")  
            print(f"  Chroma: {rust_spec[2]:.10f}")
            print(f"  Code: {rust_spec[3]}")
            break
    
    if 'Munsell:' in result.stdout:
        rust_notation = result.stdout.split('Munsell:')[1].strip()
        print(f"Rust notation: {rust_notation}")

print("\n--- Differences ---")
print(f"Hue diff: {abs(spec[0] - rust_spec[0]):.10f}")
print(f"Value diff: {abs(spec[1] - rust_spec[1]):.10f}")
print(f"Chroma diff: {abs(spec[2] - rust_spec[2]):.10f}")

# Check maximum chroma in renotation data
from colour.notation.munsell import MUNSELL_COLOURS_ALL

max_chromas = []
for entry in MUNSELL_COLOURS_ALL:
    hue_str, val, chr = entry[0]
    # Look for PB colors near value 1.6
    if 'PB' in hue_str and 1.0 <= val <= 2.0:
        max_chromas.append(chr)

if max_chromas:
    print(f"\n--- Data Analysis ---")
    print(f"Max chroma in data for PB at value 1.0-2.0: {max(max_chromas)}")
    print(f"Python chroma {spec[2]:.1f} {'EXCEEDS' if spec[2] > max(max_chromas) else 'within'} data")
    print(f"Rust chroma {rust_spec[2]:.1f} {'EXCEEDS' if rust_spec[2] > max(max_chromas) else 'within'} data")
    
    if spec[2] > max(max_chromas):
        print("\n*** EXTRAPOLATION CASE ***")
        print("Both values exceed the renotation data bounds.")
        print("The difference is in how extrapolation is handled!")