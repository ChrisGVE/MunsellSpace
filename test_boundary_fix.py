#!/usr/bin/env python3
"""Test the boundary fix on problematic colors."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

def rust_to_spec(r, g, b):
    """Get Rust specification."""
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if line.startswith('Specification:'):
            spec_str = line.split('[')[1].split(']')[0]
            values = [float(x) for x in spec_str.split(',')]
            return values
        if line.startswith('Munsell:'):
            munsell = line.split('Munsell:')[1].strip()
            return munsell
    return None

def python_to_munsell(r, g, b):
    """Get Python Munsell notation."""
    if r == 0 and g == 0 and b == 0:
        return "N 0.0"
    
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    try:
        from colour.notation import xyY_to_munsell_colour
        return xyY_to_munsell_colour(xyY)
    except:
        spec = xyY_to_munsell_specification(xyY)
        # Manual formatting for edge cases
        if spec[2] < 2.0:  # Low chroma
            if spec[0] == spec[0]:  # Not NaN
                code = int(spec[3])
                hue_family = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}[code]
                return f"{spec[0]:.1f}{hue_family} {spec[1]:.1f}/{spec[2]:.1f}"
            else:  # Neutral
                return f"N {spec[1]:.1f}"
        return None

# Test the misclassified colors
misclassified = [
    ((68, 102, 68), "10.0GY→0.0G"),
    ((85, 0, 51), "0.2R→10.0RP"),
    ((119, 85, 221), "10.0PB→0.0P"),
    ((136, 17, 68), "0.1R→10.0RP"),
    ((153, 68, 51), "0.0YR→10.0R"),
    ((170, 34, 0), "0.1YR→10.0R"),
    ((170, 34, 85), "0.0R→10.0RP"),
    ((221, 85, 204), "10.0P→0.0RP"),
    ((255, 238, 238), "0.0Y→10.0YR"),
]

print("Testing boundary fix on misclassified colors:")
print("=" * 70)

fixed_count = 0
for (r, g, b), expected_issue in misclassified:
    python_result = python_to_munsell(r, g, b)
    rust_result = rust_to_spec(r, g, b)
    
    # Extract hue family from notation
    if isinstance(rust_result, str):
        rust_notation = rust_result
    else:
        # Get the Munsell notation from a second call
        result = subprocess.run(
            ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in result.stdout.strip().split('\n'):
            if line.startswith('Munsell:'):
                rust_notation = line.split('Munsell:')[1].strip()
                break
    
    # Compare families
    python_family = ''.join(c for c in python_result.split()[0] if c.isalpha()) if python_result else "?"
    rust_family = ''.join(c for c in rust_notation.split()[0] if c.isalpha()) if rust_notation else "?"
    
    match = "✓ FIXED!" if python_family == rust_family else "✗ Still wrong"
    if python_family == rust_family:
        fixed_count += 1
    
    print(f"RGB({r:3},{g:3},{b:3}): Expected {expected_issue:12}")
    print(f"  Python: {python_result:15} Rust: {rust_notation:15} {match}")

print("=" * 70)
print(f"Fixed: {fixed_count}/{len(misclassified)} boundary issues")