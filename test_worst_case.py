#!/usr/bin/env python3

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification
import subprocess

def test_color(r, g, b):
    """Test a single color"""
    rgb = np.array([r, g, b]) / 255.0
    
    # Python conversion
    xyz = sRGB_to_XYZ(rgb)
    xyY = XYZ_to_xyY(xyz)
    spec_py = xyY_to_munsell_specification(xyY)
    
    print(f"RGB({r}, {g}, {b}) = #{r:02x}{g:02x}{b:02x}")
    print(f"xyY: ({xyY[0]:.10f}, {xyY[1]:.10f}, {xyY[2]:.10f})")
    print(f"Python spec: [{spec_py[0]:.10f}, {spec_py[1]:.10f}, {spec_py[2]:.10f}, {spec_py[3]:.1f}]")
    
    # Test with Rust
    result = subprocess.run(
        ['./target/debug/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True, text=True, stderr=subprocess.STDOUT
    )
    
    # Find the specification line
    for line in result.stdout.split('\n'):
        if 'Specification:' in line and '[' in line:
            print(f"Rust output: {line.strip()}")
            break
    
    return spec_py

# Test the worst case
print("=== WORST CASE ANALYSIS ===")
print()
spec1 = test_color(221, 238, 238)  # 0.6 chroma difference

print("\n=== ANOTHER HIGH ERROR CASE ===")
print()
spec2 = test_color(68, 0, 187)  # 0.4 chroma difference

print("\n=== PATTERN ANALYSIS ===")
print("All high-error cases show Rust chroma > Python chroma")
print("This suggests our convergence is overshooting the target")