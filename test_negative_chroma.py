#!/usr/bin/env python3
"""
Test colors that are producing negative chroma values in Rust.
These seem to be colors very close to neutral (near-achromatic).
"""

import subprocess

# Colors that showed negative chroma in the worst cases
test_colors = [
    (85, 85, 102),   # 6.2PB 3.6/1.5 -> 1.0P 3.6/-30053.8
    (204, 187, 204), # 0.7RP 7.7/1.8 -> 2.1RP 7.7/-229.6
    (221, 204, 221), # 1.1RP 8.3/1.8 -> 2.2RP 8.3/-226.3
    (238, 221, 238), # 1.8RP 9.0/1.6 -> 2.4RP 9.0/-113.7
    (187, 187, 204), # 2.8PB 7.6/1.3 -> 1.1PB 7.6/109.9
    (85, 68, 68),    # 2.3YR 3.0/1.2 -> 2.4YR 3.0/-106.3
    (204, 187, 170), # 3.5Y 7.6/2.0 -> 1.5Y 7.6/-67.4
    (85, 102, 102),  # 1.0BG 4.1/1.8 -> 2.1BG 4.1/-56.6
]

print("Testing colors with negative chroma values...")
print("=" * 80)

# Build Rust binary
subprocess.run(['cargo', 'build', '--release', '--bin', 'batch_convert'], 
               capture_output=True)

# Test each color
for r, g, b in test_colors:
    # Test with Rust
    input_data = f"{r},{g},{b}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    rust_result = result.stdout.strip()
    
    print(f"RGB({r:3},{g:3},{b:3}): {rust_result}")
    
    # Check if chroma is negative
    if '/-' in rust_result:
        print(f"  ⚠️  NEGATIVE CHROMA DETECTED!")
        
        # Let's also check the intermediate values
        print(f"  Debugging this color...")
        
        # Create a debug script
        debug_code = f"""
import colour
import numpy as np

rgb = [{r/255.0}, {g/255.0}, {b/255.0}]
XYZ = colour.sRGB_to_XYZ(rgb)
xyY = colour.XYZ_to_xyY(XYZ)

print(f"  RGB: {rgb}")
print(f"  XYZ: {XYZ}")
print(f"  xyY: {xyY}")

# Check if it's near achromatic
x, y, Y = xyY
illuminant_C = [0.31006, 0.31616]
dist = np.sqrt((x - illuminant_C[0])**2 + (y - illuminant_C[1])**2)
print(f"  Distance from illuminant C: {dist:.6f}")
print(f"  Is near-achromatic (< 0.02): {dist < 0.02}")
"""
        
        with open('/tmp/debug_color.py', 'w') as f:
            f.write(debug_code)
        
        subprocess.run(['python3', '/tmp/debug_color.py'])
        print()

print("\n" + "=" * 80)
print("ANALYSIS:")
print("The negative chroma values appear to be a bug in the Rust implementation")
print("when handling near-achromatic colors (colors very close to neutral).")
print("These should be detected and handled as achromatic (N) colors instead.")