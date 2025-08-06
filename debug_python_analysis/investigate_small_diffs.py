#!/usr/bin/env python3
"""Investigate small differences in conversions"""

import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import munsell_colour_to_munsell_specification

# Test cases with small differences
test_cases = [
    (0, 102, 85),   # 8.3G 3.7/6.1 vs 8.3G 3.8/6.1
    (0, 68, 153),   # 5.9PB 3.0/11.3 vs 5.8PB 3.0/11.3
]

for r, g, b in test_cases:
    print(f"\nTesting RGB({r}, {g}, {b}):")
    print("=" * 50)
    
    # Python conversion
    rgb_norm = [r/255.0, g/255.0, b/255.0]
    XYZ = sRGB_to_XYZ(rgb_norm)
    xyY = XYZ_to_xyY(XYZ)
    print(f"xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
    
    munsell = xyY_to_munsell_colour(xyY)
    spec = munsell_colour_to_munsell_specification(munsell)
    print(f"Python: {munsell}")
    print(f"  Specification: hue={spec[0]:.6f}, value={spec[1]:.6f}, chroma={spec[2]:.6f}, code={spec[3]}")
    
    # Rust conversion
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    rust_munsell = result.stdout.strip()
    print(f"Rust: {rust_munsell}")
    
    # Check intermediate values with debug
    print("\nDebug output:")
    env = {'DEBUG_MUNSELL': '1'}
    result = subprocess.run(
        ['cargo', 'run', '--bin', 'mathematical_convert_rgb', '--', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        env={**subprocess.os.environ, **env}
    )
    
    # Extract key debug lines
    for line in result.stderr.split('\n'):
        if 'Munsell Value calculated:' in line:
            print(f"  {line.strip()}")
        elif 'Initial guess:' in line:
            print(f"  {line.strip()}")
        elif 'Converged after' in line:
            print(f"  {line.strip()}")