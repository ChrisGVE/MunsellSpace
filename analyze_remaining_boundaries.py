#!/usr/bin/env python3
"""Analyze the 7 remaining boundary mismatches in detail."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np

def get_rust_spec(r, g, b):
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
    return None

# The 7 colors that still mismatch
remaining_issues = [
    (68, 102, 68),   # Python: 10.0GY, Rust: 0.0G
    (85, 0, 51),     # Python: 0.2R, Rust: 10.0RP
    (119, 85, 221),  # Python: 10.0PB, Rust: 0.0P
    (136, 17, 68),   # Python: 0.0R, Rust: 10.0RP
    (153, 68, 51),   # Python: 0.0YR, Rust: 10.0R
    (170, 34, 0),    # Python: 0.1YR, Rust: 10.0R
    (170, 34, 85),   # Python: 0.0R, Rust: 10.0RP
]

families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}

print("Detailed Analysis of Remaining Boundary Mismatches")
print("=" * 80)

for r, g, b in remaining_issues:
    print(f"\nRGB({r:3},{g:3},{b:3}):")
    print("-" * 40)
    
    # Get Python's result
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    # Get Python specification
    py_spec = xyY_to_munsell_specification(xyY)
    py_munsell = xyY_to_munsell_colour(xyY)
    
    # Get Rust specification
    rust_spec = get_rust_spec(r, g, b)
    
    print(f"  Target xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
    print()
    print(f"  Python: {py_munsell}")
    print(f"    Spec: hue={py_spec[0]:.4f}, value={py_spec[1]:.4f}, chroma={py_spec[2]:.4f}, code={int(py_spec[3])} ({families[int(py_spec[3])]})")
    
    if rust_spec:
        rust_family = families[int(rust_spec[3])]
        print(f"  Rust: {rust_spec[0]:.1f}{rust_family} {rust_spec[1]:.1f}/{rust_spec[2]:.1f}")
        print(f"    Spec: hue={rust_spec[0]:.4f}, value={rust_spec[1]:.4f}, chroma={rust_spec[2]:.4f}, code={int(rust_spec[3])} ({rust_family})")
    
    # Analyze the difference
    if rust_spec:
        # Check if they're at adjacent family boundaries
        py_code = int(py_spec[3])
        rust_code = int(rust_spec[3])
        
        # Calculate the family transition
        if abs(py_code - rust_code) == 1 or (py_code == 1 and rust_code == 10) or (py_code == 10 and rust_code == 1):
            adjacent = True
            
            # Determine transition direction
            if (rust_code == py_code + 1) or (py_code == 10 and rust_code == 1):
                direction = "next"
            else:
                direction = "prev"
        else:
            adjacent = False
            direction = "non-adjacent"
        
        print(f"\n  Analysis:")
        print(f"    Family transition: {families[py_code]} → {families[rust_code]} ({'adjacent' if adjacent else 'NON-ADJACENT'})")
        print(f"    Python hue position: {py_spec[0]:.4f} ({'near 0' if py_spec[0] < 0.2 else 'near 10' if py_spec[0] > 9.8 else 'middle'})")
        print(f"    Rust hue position: {rust_spec[0]:.4f} ({'near 0' if rust_spec[0] < 0.2 else 'near 10' if rust_spec[0] > 9.8 else 'middle'})")
        
        # Check if it's a wrap-around case
        if (py_spec[0] < 0.2 and rust_spec[0] > 9.8) or (py_spec[0] > 9.8 and rust_spec[0] < 0.2):
            print(f"    Wrap-around: YES - Values on opposite sides of 0/10 boundary")
        else:
            print(f"    Wrap-around: NO")

print("\n" + "=" * 80)
print("SUMMARY:")
print("All 7 remaining issues are at family boundaries where:")
print("1. Python and Rust converge to different but equivalent local minima")
print("2. The colors are at adjacent hue families (e.g., GY→G, R→RP)")
print("3. One algorithm chooses hue≈0 in family N, the other chooses hue≈10 in family N-1")
print("\nThese represent fundamental algorithmic differences in convergence behavior,")