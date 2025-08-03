#!/usr/bin/env python3
"""
Verify individual colors to understand the discrepancy.
"""

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess

# Test specific colors
test_colors = [
    ([0, 68, 153], "Index 7"),
    ([0, 102, 68], "Index 2"),
    ([0, 68, 119], "Index 1"),
]

for rgb, description in test_colors:
    print(f"\n{description}: RGB{rgb}")
    print("-" * 40)
    
    # Python calculation
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        python_result = xyY_to_munsell_colour(xyY)
        print(f"Python fresh: {python_result}")
    except Exception as e:
        print(f"Python error: {e}")
    
    # Get Rust result
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking') and not line.startswith('EXACT'):
            if line[0].isdigit() or line.startswith('N '):
                print(f"Rust fresh:   {line}")
                break

# Check what we have in the files
print("\n" + "=" * 50)
print("FROM FILES:")
print("=" * 50)

with open('rust_4007_munsell_only.txt', 'r') as f:
    lines = f.readlines()
    print(f"\nRust file line 8 (index 7): {lines[7].strip()}")
    print(f"Rust file line 3 (index 2): {lines[2].strip()}")
    print(f"Rust file line 2 (index 1): {lines[1].strip()}")

with open('python_4007_final.txt', 'r') as f:
    lines = f.readlines()
    print(f"\nPython file line 8 (index 7): {lines[7].strip()}")
    print(f"Python file line 3 (index 2): {lines[2].strip()}")
    print(f"Python file line 2 (index 1): {lines[1].strip()}")