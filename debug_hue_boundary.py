#!/usr/bin/env python3
"""Debug hue boundary wrapping issue."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

def test_boundary_color(r, g, b, expected_transition):
    """Test a color that crosses hue boundary."""
    
    print(f"\n{'='*60}")
    print(f"Testing RGB({r}, {g}, {b}) - Expected: {expected_transition}")
    print(f"{'='*60}")
    
    # Get Python specification
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    print(f"xyY: [{xyY[0]:.10f}, {xyY[1]:.10f}, {xyY[2]:.10f}]")
    
    spec = xyY_to_munsell_specification(xyY)
    print(f"Python spec: [{spec[0]:.10f}, {spec[1]:.10f}, {spec[2]:.10f}, {spec[3]:.1f}]")
    
    # Call Rust with debug output
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if line.startswith('Specification:'):
            print(f"Rust output: {line}")
    
    # Check if the issue is in the final hue adjustment
    if spec[0] < 0.5:  # Near 0.0
        print(f"\n→ Python hue {spec[0]:.3f} is near 0.0")
        print(f"  When rounded, could wrap to 10.0 in Rust?")
    elif spec[0] > 9.5:  # Near 10.0
        print(f"\n→ Python hue {spec[0]:.3f} is near 10.0")
        print(f"  When rounded, could wrap to 0.0 in Rust?")

# Test the most problematic boundary cases
test_cases = [
    (68, 102, 68, "10.0GY→0.0G"),    # GY→G at 10.0/0.0 boundary
    (85, 0, 51, "0.2R→10.0RP"),      # R→RP at 0.0/10.0 boundary
    (119, 85, 221, "10.0PB→0.0P"),   # PB→P at 10.0/0.0 boundary
    (153, 68, 51, "0.0YR→10.0R"),    # YR→R at 0.0/10.0 boundary
]

for r, g, b, transition in test_cases:
    test_boundary_color(r, g, b, transition)

print(f"\n{'='*60}")
print("HYPOTHESIS:")
print(f"{'='*60}")
print("""
The issue appears to be in the final hue normalization.
When Python produces a hue very close to 0.0 (e.g., 0.02),
Rust might be wrapping it to 10.0, causing the family change.

Similarly, when Python produces 10.0, Rust might wrap to 0.0.

This could be due to:
1. Different rounding behavior in the convergence loop
2. Epsilon differences in floating-point comparisons  
3. Incorrect modulo/wrapping in hue normalization
""")