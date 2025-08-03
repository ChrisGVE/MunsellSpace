#!/usr/bin/env python3
"""
Test if the Rust normalization fix resolves family mismatches.
"""

import csv
import subprocess
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings

warnings.filterwarnings('ignore')

# The 17 family mismatches we found before
family_mismatches = [
    [68, 255, 221],   # G→BG
    [102, 51, 68],    # RP→R
    [136, 0, 68],     # RP→R
    [153, 51, 85],    # RP→R
    [170, 17, 85],    # RP→R
    [170, 255, 238],  # G→BG
    [204, 85, 119],   # RP→R
    [204, 34, 102],   # RP→R
    [204, 136, 153],  # RP→R
    [204, 221, 238],  # B→PB
    [221, 0, 102],    # R→RP (note: this is reverse!)
    [221, 68, 119],   # RP→R
    [221, 153, 170],  # RP→R
    [221, 238, 255],  # B→PB
    [255, 85, 136],   # RP→R
    [255, 204, 221],  # RP→R
    [255, 238, 238],  # YR→Y (note: Python says YR, Rust says Y)
]

print("=" * 80)
print("TESTING FAMILY MISMATCH FIX")
print("=" * 80)

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A" or notation.startswith("ERROR"):
        return None
    notation = notation.strip()
    
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

matches = 0
mismatches = []

for i, rgb in enumerate(family_mismatches, 1):
    # Get Python result
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        python_result = xyY_to_munsell_colour(xyY)
    except Exception as e:
        python_result = f"ERROR: {e}"
    
    # Get Rust result
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    rust_result = None
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking'):
            if line and (line[0].isdigit() or line.startswith('N ')):
                rust_result = line
                break
    
    # Parse and compare
    python_p = parse_munsell(python_result) if python_result else None
    rust_p = parse_munsell(rust_result) if rust_result else None
    
    if python_p and rust_p:
        if python_p['family'] == rust_p['family']:
            matches += 1
            print(f"{i:2d}. RGB{rgb} - MATCH: {python_p['family']} == {rust_p['family']}")
        else:
            mismatches.append({
                'rgb': rgb,
                'python': python_result,
                'rust': rust_result,
                'python_family': python_p['family'],
                'rust_family': rust_p['family']
            })
            print(f"{i:2d}. RGB{rgb} - MISMATCH: Python={python_p['family']}, Rust={rust_p['family']}")
            print(f"    Python: {python_result}")
            print(f"    Rust:   {rust_result}")
    else:
        print(f"{i:2d}. RGB{rgb} - ERROR parsing results")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Matches: {matches}/{len(family_mismatches)}")
print(f"Mismatches: {len(mismatches)}/{len(family_mismatches)}")

if mismatches:
    print("\nRemaining mismatches:")
    for m in mismatches:
        print(f"  RGB{m['rgb']}: {m['python_family']} → {m['rust_family']}")
else:
    print("\n✅ ALL FAMILY MISMATCHES RESOLVED!")