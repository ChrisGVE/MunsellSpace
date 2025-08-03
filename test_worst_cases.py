#!/usr/bin/env python3
"""Test worst case colors from previous analysis"""

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess

worst_cases = [
    [0, 238, 17],    # worst_hue
    [187, 0, 255],    # worst_chroma 
    [0, 34, 17],      # family_mismatch
    [255, 0, 0],      # Red baseline
    [0, 255, 0],      # Green baseline
]

print("Testing worst case colors:")
print("=" * 60)

for rgb in worst_cases:
    # Python result
    rgb_norm = [c/255.0 for c in rgb]
    XYZ = sRGB_to_XYZ(rgb_norm)
    xyY = XYZ_to_xyY(XYZ)
    python_result = xyY_to_munsell_colour(xyY)
    
    # Rust result
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    # Extract just the Munsell notation from output
    lines = result.stdout.strip().split('\n')
    rust_result = None
    for line in lines:
        # Look for line that starts with a number or 'N' (for neutral)
        if line and (line[0].isdigit() or line.startswith('N ')):
            rust_result = line
            break
    
    print(f"\nRGB {rgb}:")
    print(f"  Python: {python_result}")
    print(f"  Rust:   {rust_result}")
    
    # Check if they match
    if rust_result and python_result == rust_result:
        print(f"  ✅ EXACT MATCH!")
    else:
        print(f"  ❌ Mismatch")