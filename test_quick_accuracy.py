#!/usr/bin/env python3
"""Quick accuracy test"""

import subprocess
import colour
import numpy as np

# Test specific RGB values
test_cases = [
    (238, 0, 85),    # Known problematic case
    (100, 150, 200), # Test case we just ran
    (255, 0, 0),     # Pure red
    (0, 255, 0),     # Pure green
    (0, 0, 255),     # Pure blue
    (128, 128, 128), # Gray
    (255, 255, 255), # White
    (0, 0, 0),       # Black
]

print("Testing specific RGB values:")
print("-" * 60)

for r, g, b in test_cases:
    # Python conversion
    try:
        rgb_norm = [r/255.0, g/255.0, b/255.0]
        XYZ = colour.sRGB_to_XYZ(rgb_norm)
        xyY = colour.XYZ_to_xyY(XYZ)
        py_munsell = colour.notation.xyY_to_munsell_colour(xyY)
    except Exception as e:
        py_munsell = f"FAILED: {e}"
    
    # Rust conversion
    try:
        result = subprocess.run(
            ['cargo', 'run', '--bin', 'mathematical_convert_rgb', '--', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=10
        )
        rust_munsell = result.stdout.strip() if result.returncode == 0 else "FAILED"
    except:
        rust_munsell = "FAILED"
    
    print(f"RGB({r:3}, {g:3}, {b:3})")
    print(f"  Python: {py_munsell}")
    print(f"  Rust:   {rust_munsell}")
    print()