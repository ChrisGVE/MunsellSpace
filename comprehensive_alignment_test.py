#!/usr/bin/env python3
"""Comprehensive alignment test between Rust and Python"""

import subprocess
import colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np
import random

# Generate a comprehensive test set
test_colors = []

# Add systematic grid of colors
for r in [0, 64, 128, 192, 255]:
    for g in [0, 64, 128, 192, 255]:
        for b in [0, 64, 128, 192, 255]:
            if len(test_colors) < 50:  # Limit to 50 for quick test
                test_colors.append([r, g, b])

def parse_munsell(munsell_str):
    """Parse Munsell string to components"""
    if munsell_str.startswith('N'):
        # Grey
        return None, float(munsell_str[1:]), 0.0, None
    
    # Parse colored notation
    import re
    match = re.match(r'([\d.]+)([A-Z]+)\s+([\d.]+)/([\d.]+)', munsell_str)
    if match:
        hue = float(match.group(1))
        family = match.group(2)
        value = float(match.group(3))
        chroma = float(match.group(4))
        return hue, value, chroma, family
    return None

def compare_munsell(python_str, rust_str):
    """Compare two Munsell strings"""
    p = parse_munsell(python_str)
    r = parse_munsell(rust_str)
    
    if not p or not r:
        return None
    
    # Both parsed successfully
    if p[3] != r[3]:  # Different families
        return "family_mismatch"
    
    # Same family, check component differences
    hue_diff = abs(p[0] - r[0]) if p[0] and r[0] else 0
    value_diff = abs(p[1] - r[1])
    chroma_diff = abs(p[2] - r[2])
    
    if hue_diff < 0.1 and value_diff < 0.1 and chroma_diff < 0.1:
        return "exact"
    elif hue_diff < 0.2 and value_diff < 0.2 and chroma_diff < 0.2:
        return "close"
    else:
        return "different"

def python_rgb_to_munsell(rgb):
    """Convert RGB to Munsell using Python colour-science"""
    srgb = [c / 255.0 for c in rgb]
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    
    try:
        spec = xyY_to_munsell_specification(xyy)
        
        HUE_CODES = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                     6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
        
        hue = spec[0]
        value = spec[1]
        chroma = spec[2]
        code = int(spec[3])
        
        if chroma < 0.05:
            return f"N{value:.1f}", None
        else:
            family = HUE_CODES.get(code, '?')
            return f"{hue:.1f}{family} {value:.1f}/{chroma:.1f}", None
    except Exception as e:
        return None, str(e)[:30]

print("Running comprehensive alignment test...")
print("=" * 80)

categories = {
    'exact': 0,
    'close': 0,
    'family_mismatch': 0,
    'different': 0,
    'both_error': 0,
    'rust_error': 0,
    'python_error': 0,
    'parse_error': 0
}

family_mismatches = []

for rgb in test_colors:
    # Get Python result
    python_result, python_error = python_rgb_to_munsell(rgb)
    
    # Get Rust result
    result = subprocess.run(['./target/release/test_rust_python_compare', 
                           str(rgb[0]), str(rgb[1]), str(rgb[2])],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    rust_result = result.stdout.strip()
    
    # Categorize
    if python_error and "Error:" in rust_result:
        categories['both_error'] += 1
    elif python_error:
        categories['python_error'] += 1
    elif "Error:" in rust_result:
        categories['rust_error'] += 1
    else:
        # Both succeeded, compare
        comparison = compare_munsell(python_result, rust_result)
        if comparison:
            categories[comparison] += 1
            if comparison == 'family_mismatch':
                family_mismatches.append({
                    'rgb': rgb,
                    'python': python_result,
                    'rust': rust_result
                })
        else:
            categories['parse_error'] += 1

print("\nRESULTS:")
print(f"Tested {len(test_colors)} colors")
print()
print("When both converge:")
print(f"  Exact matches:    {categories['exact']:3d}")
print(f"  Close matches:    {categories['close']:3d}")
print(f"  Family mismatch:  {categories['family_mismatch']:3d}")
print(f"  Different:        {categories['different']:3d}")
print()
print("Errors:")
print(f"  Both error:       {categories['both_error']:3d}")
print(f"  Rust only error:  {categories['rust_error']:3d}")
print(f"  Python only error:{categories['python_error']:3d}")
print()

successful = categories['exact'] + categories['close'] + categories['family_mismatch'] + categories['different']
if successful > 0:
    print(f"Alignment when both converge: {categories['exact'] + categories['close']}/{successful} = {100*(categories['exact'] + categories['close'])/successful:.1f}%")

if family_mismatches:
    print("\nFamily mismatches (first 5):")
    for m in family_mismatches[:5]:
        print(f"  RGB {m['rgb']}: Python={m['python']}, Rust={m['rust']}")

print("=" * 80)