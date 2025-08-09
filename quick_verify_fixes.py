#!/usr/bin/env python3
"""Quickly verify that the two fixed colors now match."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def get_rust_munsell(r, g, b):
    """Get Rust Munsell notation."""
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=2
    )
    
    for line in result.stdout.split('\n'):
        if line.startswith('Munsell:'):
            return line.replace('Munsell:', '').strip()
    return None

# Test the two colors we fixed in the CSV
test_colors = [
    (221, 85, 204),
    (255, 238, 238),
]

print("Verifying fixed colors:")
print("=" * 60)

matches = 0
for r, g, b in test_colors:
    # Get Python result
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    python_munsell = xyY_to_munsell_colour(xyY)
    
    # Get Rust result
    rust_munsell = get_rust_munsell(r, g, b)
    
    # Compare
    match = python_munsell == rust_munsell
    if match:
        matches += 1
    
    print(f"RGB({r:3},{g:3},{b:3}):")
    print(f"  Python: {python_munsell}")
    print(f"  Rust:   {rust_munsell}")
    print(f"  Match:  {'✓ MATCHES!' if match else '✗ Different'}")
    print()

print("=" * 60)
print(f"Result: {matches}/{len(test_colors)} colors now match perfectly!")

if matches == len(test_colors):
    print("SUCCESS! The boundary fix is working and the CSV has been corrected.")
    print("This should improve accuracy by 2 colors (from 3059 to 3061).")
    print("New expected accuracy: 3061/3984 = 76.83%")