#!/usr/bin/env python3
"""Quick test of key colors to show accuracy"""

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess

test_colors = [
    ([255, 0, 0], "Red"),
    ([0, 255, 0], "Green"),
    ([0, 238, 17], "Worst hue case"),
    ([187, 0, 255], "Worst chroma case"),
]

for rgb, name in test_colors:
    # Python
    rgb_norm = [c/255.0 for c in rgb]
    XYZ = sRGB_to_XYZ(rgb_norm)
    xyY = XYZ_to_xyY(XYZ)
    python = xyY_to_munsell_colour(xyY)
    
    # Rust
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    # Extract just the Munsell line (skip TRACE and Looking for lines)
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking') and not line.startswith('EXACT'):
            rust = line
            break
    
    print(f"{name:20} RGB{str(rgb):15}")
    print(f"  Python: {python}")
    print(f"  Rust:   {rust}")
    print(f"  {'✅ MATCH' if python == rust else f'❌ Diff'}")
    print()