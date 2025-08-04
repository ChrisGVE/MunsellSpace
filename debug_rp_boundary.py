#!/usr/bin/env python3
"""Debug the RP/P boundary issue"""

import subprocess

# Test colors that show RP -> P mismatch
test_cases = [
    ([68, 0, 68], "0.7RP 1.3/8.6"),
    ([255, 34, 221], "0.8RP 5.8/22.4"),
    ([255, 17, 221], "0.8RP 5.8/23.0"),
    ([255, 187, 238], "0.9RP 8.3/7.2"),
]

print("Testing RP/P boundary colors:")
print("=" * 70)

for rgb, expected in test_cases:
    r, g, b = rgb
    
    # Get Rust result with debug output
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    
    rust_output = result.stdout.strip() if result.returncode == 0 else "ERROR"
    
    # Extract debug info from stderr
    debug_lines = result.stderr.split('\n') if result.stderr else []
    
    print(f"\nRGB [{r:3},{g:3},{b:3}]:")
    print(f"  Expected: {expected}")
    print(f"  Got:      {rust_output}")
    
    # Look for key debug info
    for line in debug_lines:
        if 'Initial guess:' in line:
            print(f"  {line.strip()}")
        if 'Hue refinement:' in line and 'Iteration 0' in str(debug_lines):
            print(f"  {line.strip()}")
        if 'Final state:' in line:
            print(f"  {line.strip()}")

print("\n" + "=" * 70)
print("Testing hue angle boundaries in Python:")
print("=" * 70)

# Test what Python does with angles near RP/P boundary
test_script = """
import numpy as np
from colour.notation.munsell import hue_angle_to_hue, hue_to_hue_angle

# Test angles around RP/P boundary (RP is code 8, P is code 9)
# RP should be roughly 315-360 degrees
# P should be roughly 255-315 degrees

test_angles = [310, 312, 314, 315, 316, 318, 320]
print("Angle to hue conversion near RP/P boundary:")
for angle in test_angles:
    hue, code = hue_angle_to_hue(angle)
    families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
                6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
    family = families.get(int(code), '?')
    print(f"  {angle:3}° -> {hue:4.1f}{family} (code {code})")

print("\\nHue to angle conversion for RP values:")
rp_hues = [(0.5, 8), (0.7, 8), (0.9, 8), (1.0, 8), (9.9, 8), (10.0, 8)]
for hue, code in rp_hues:
    angle = hue_to_hue_angle(np.array([hue, code]))
    print(f"  {hue:4.1f}RP -> {angle:6.2f}°")

print("\\nHue to angle conversion for P values:")
p_hues = [(0.1, 9), (0.5, 9), (1.0, 9), (9.5, 9), (9.9, 9), (10.0, 9)]
for hue, code in p_hues:
    angle = hue_to_hue_angle(np.array([hue, code]))
    print(f"  {hue:4.1f}P -> {angle:6.2f}°")
"""

with open('test_boundary.py', 'w') as f:
    f.write(test_script)

result = subprocess.run(
    ['./venv_comparison/bin/python', 'test_boundary.py'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Clean up
import os
os.remove('test_boundary.py')

print("=" * 70)
print("HYPOTHESIS:")
print("=" * 70)
print("The issue appears to be that hues near 0.7-0.9 RP are being")
print("incorrectly mapped to 10.0 P instead of staying as RP.")
print("This suggests a problem with the hue normalization or")
print("boundary handling in the convergence algorithm.")