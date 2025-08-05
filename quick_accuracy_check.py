#!/usr/bin/env python3
"""Quick accuracy check on key test colors"""

import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "Error":
        return None
        
    if notation.startswith('N '):
        return {
            'family': 'N',
            'hue': 0.0,
            'value': float(notation.split()[1]),
            'chroma': 0.0
        }
    
    parts = notation.split(' ')
    if len(parts) != 2:
        return None
    
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    
    # Extract hue number and family
    hue_num = ""
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            family = hue_part[len(hue_num):]
            break
    
    return {
        'family': family,
        'hue': float(hue_num) if hue_num else 0.0,
        'value': float(value_chroma[0]),
        'chroma': float(value_chroma[1]) if len(value_chroma) > 1 else 0.0
    }

# Test specific colors that were problematic
test_colors = [
    ([68, 0, 68], "0.7RP"),    # RP/P boundary
    ([238, 0, 85], "3.0R"),     # High chroma red
    ([255, 255, 255], "N 9.5"), # White
    ([0, 0, 0], "N 0.0"),       # Black
    ([128, 128, 128], "N 5.0"), # Gray
    ([255, 0, 0], "7.5R"),      # Pure red
    ([0, 255, 0], "7.5GY"),     # Pure green
    ([0, 0, 255], "7.5PB"),     # Pure blue
]

print("🔬 QUICK ACCURACY CHECK")
print("=" * 60)

for rgb, expected_family in test_colors:
    # Get Rust result
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb'] + [str(c) for c in rgb],
        capture_output=True,
        text=True
    )
    rust_notation = result.stdout.strip()
    rust_parsed = parse_munsell(rust_notation)
    
    # Get Python result
    rgb_normalized = np.array(rgb) / 255.0
    try:
        xyz = sRGB_to_XYZ(rgb_normalized)
        xyy = XYZ_to_xyY(xyz)
        python_notation = xyY_to_munsell_colour(xyy)
        python_parsed = parse_munsell(python_notation.replace('/', ' '))
    except:
        python_notation = "Error"
        python_parsed = None
    
    print(f"\nRGB {rgb}:")
    print(f"  Expected: ~{expected_family}")
    print(f"  Rust:     {rust_notation}")
    print(f"  Python:   {python_notation}")
    
    # Check family match
    if rust_parsed and python_parsed:
        family_match = rust_parsed['family'] == python_parsed['family']
        value_diff = abs(rust_parsed['value'] - python_parsed['value'])
        hue_diff = abs(rust_parsed['hue'] - python_parsed['hue'])
        chroma_diff = abs(rust_parsed['chroma'] - python_parsed['chroma'])
        
        print(f"  Family match: {'✅' if family_match else '❌'}")
        print(f"  Value diff:   {value_diff:.3f} {'✅' if value_diff <= 0.1 else '❌'}")
        print(f"  Hue diff:     {hue_diff:.3f} {'✅' if hue_diff <= 0.1 else '❌'}")
        print(f"  Chroma diff:  {chroma_diff:.3f} {'✅' if chroma_diff <= 0.1 else '❌'}")

print("\n" + "=" * 60)
print("✅ = Within tolerance (≤0.1)")
print("❌ = Outside tolerance (>0.1)")