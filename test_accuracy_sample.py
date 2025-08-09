#!/usr/bin/env python3
"""Quick accuracy test on sample colors."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def rust_to_munsell(r, g, b):
    """Call Rust implementation."""
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if line.startswith('Munsell:'):
            return line.split('Munsell:')[1].strip()
    return None

def python_to_munsell(r, g, b):
    """Call Python implementation."""
    # Special case for black
    if r == 0 and g == 0 and b == 0:
        return "N 0.0"
    
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    try:
        return xyY_to_munsell_colour(xyY)
    except:
        # Handle low chroma or other edge cases
        from colour.notation.munsell import xyY_to_munsell_specification
        try:
            spec = xyY_to_munsell_specification(xyY)
            # Format manually
            if spec[2] < 2.0:  # Low chroma
                if spec[0] == spec[0]:  # Not NaN
                    code = int(spec[3])
                    hue_family = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}[code]
                    return f"{spec[0]:.1f}{hue_family} {spec[1]:.1f}/{spec[2]:.1f}"
                else:  # Neutral
                    return f"N {spec[1]:.1f}"
        except:
            pass
        return None

# Test colors that were problematic
test_colors = [
    (255, 238, 238),  # High value, low chroma - was misclassified
    (255, 238, 255),  # High value, low chroma
    (238, 238, 255),  # High value, low chroma
    (238, 238, 238),  # High value, low chroma
    (0, 0, 0),        # Black - formatting issue
    (187, 255, 153),  # High value interpolation test
    (100, 150, 200),  # Normal test
    (255, 0, 0),      # Pure red
]

print("Testing accuracy improvements:")
print("=" * 60)

exact_matches = 0
total = len(test_colors)

for r, g, b in test_colors:
    python_result = python_to_munsell(r, g, b)
    rust_result = rust_to_munsell(r, g, b)
    
    match = "✓" if python_result == rust_result else "✗"
    print(f"RGB({r:3},{g:3},{b:3}): Python={python_result:12} Rust={rust_result:12} {match}")
    
    if python_result == rust_result:
        exact_matches += 1

print("=" * 60)
print(f"Exact matches: {exact_matches}/{total} ({100*exact_matches/total:.1f}%)")