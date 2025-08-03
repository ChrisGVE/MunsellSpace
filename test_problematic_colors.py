#!/usr/bin/env python3
"""
Test specific problematic colors to understand the issue.
"""

import subprocess
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings

warnings.filterwarnings('ignore')

# Test the most problematic cases
test_cases = [
    [204, 221, 238],  # B→PB with chroma -55.3
    [221, 238, 255],  # B→PB with chroma -0.7
    [255, 238, 238],  # YR→Y with chroma -2.5
    [255, 85, 136],   # Exactly 0.0R vs 9.7RP
]

print("=" * 80)
print("DEBUGGING PROBLEMATIC COLORS")
print("=" * 80)

for rgb in test_cases:
    print(f"\nRGB{rgb}")
    print("-" * 60)
    
    # Get Python result
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        print(f"  xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
        
        # Calculate distance from Illuminant C
        x_c, y_c = 0.31006, 0.31616
        dx = xyY[0] - x_c
        dy = xyY[1] - y_c
        distance = (dx**2 + dy**2) ** 0.5
        print(f"  Distance from C: {distance:.6f} (dx={dx:.6f}, dy={dy:.6f})")
        
        python_result = xyY_to_munsell_colour(xyY)
        print(f"  Python: {python_result}")
    except Exception as e:
        print(f"  Python ERROR: {e}")
    
    # Get detailed Rust output with debug enabled
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    
    # Run with RUST_LOG=trace to see debug output
    import os
    env = os.environ.copy()
    # env['RUST_LOG'] = 'trace'
    
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True,
        env=env
    )
    
    rust_result = None
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking'):
            if line and (line[0].isdigit() or line.startswith('N ')):
                rust_result = line
                print(f"  Rust:   {line}")
                break
    
    # Check for debug/error output
    if result.stderr:
        print(f"  Rust stderr: {result.stderr[:200]}")

print("\n" + "=" * 80)
print("OBSERVATIONS")
print("=" * 80)
print("""
1. Negative chroma values (-55.3, -0.7, -2.5) are impossible and indicate
   a serious bug in the interpolation or lookup code.
   
2. These colors are near the achromatic axis (low saturation) which may
   be causing numerical issues.
   
3. The family mismatches are happening at boundaries where Python and Rust
   choose different representations of the same hue angle.
""")