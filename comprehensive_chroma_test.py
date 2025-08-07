#!/usr/bin/env python3

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY, xyY_to_munsell_colour
import subprocess
import json

def test_color(r, g, b):
    """Test a color through both Python and Rust"""
    rgb = np.array([r, g, b]) / 255.0
    
    # Python conversion
    xyz = sRGB_to_XYZ(rgb)
    xyY = XYZ_to_xyY(xyz)
    munsell_py = xyY_to_munsell_colour(xyY)
    
    # Parse Python result
    if '/' in munsell_py:
        parts = munsell_py.split(' ')
        hue_part_py = parts[0]
        value_chroma = parts[1].split('/')
        value_py = float(value_chroma[0])
        chroma_py = float(value_chroma[1])
    else:
        # Achromatic color
        hue_part_py = "N"
        value_py = float(munsell_py.replace('N ', ''))
        chroma_py = 0.0
    
    # Rust conversion
    result = subprocess.run(
        ['./target/debug/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True, text=True
    )
    
    # Parse Rust output
    munsell_rust = None
    for line in result.stdout.split('\n'):
        if 'Final Munsell:' in line:
            munsell_rust = line.split('Final Munsell:')[1].strip()
            break
    
    if munsell_rust and '/' in munsell_rust:
        parts = munsell_rust.split(' ')
        hue_part_rust = parts[0]
        value_chroma = parts[1].split('/')
        value_rust = float(value_chroma[0])
        chroma_rust = float(value_chroma[1])
    else:
        hue_part_rust = "?"
        value_rust = 0.0
        chroma_rust = 0.0
    
    return {
        'rgb': [r, g, b],
        'python': {'hue': hue_part_py, 'value': value_py, 'chroma': chroma_py, 'full': munsell_py},
        'rust': {'hue': hue_part_rust, 'value': value_rust, 'chroma': chroma_rust, 'full': munsell_rust},
        'chroma_diff': abs(chroma_py - chroma_rust),
        'value_diff': abs(value_py - value_rust)
    }

# Test problematic colors
test_colors = [
    (34, 17, 119),   # #221177 - Deep blue with large chroma difference
    (255, 0, 0),     # Pure red
    (0, 255, 0),     # Pure green  
    (0, 0, 255),     # Pure blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (128, 128, 128), # Grey
]

print("=== CHROMA COMPARISON TEST ===")
print()

for r, g, b in test_colors:
    result = test_color(r, g, b)
    print(f"RGB({r:3}, {g:3}, {b:3}):")
    print(f"  Python: {result['python']['full']}")
    print(f"  Rust:   {result['rust']['full']}")
    print(f"  Chroma diff: {result['chroma_diff']:.3f}")
    print(f"  Value diff:  {result['value_diff']:.3f}")
    print()