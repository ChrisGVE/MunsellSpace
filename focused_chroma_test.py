#!/usr/bin/env python3

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification
import subprocess
import json

def test_color_detailed(r, g, b):
    """Test a single color in detail"""
    rgb = np.array([r, g, b]) / 255.0
    
    # Python conversion
    xyz = sRGB_to_XYZ(rgb)
    xyY = XYZ_to_xyY(xyz)
    spec_py = xyY_to_munsell_specification(xyY)
    
    # Rust conversion - get specification
    result = subprocess.run(
        ['./target/debug/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True, text=True, stderr=subprocess.STDOUT
    )
    
    # Parse Rust specification from output
    spec_rust = None
    for line in result.stdout.split('\n'):
        if 'Specification:' in line and '[' in line:
            # Extract the array
            array_str = line.split('[')[1].split(']')[0]
            spec_rust = [float(x) for x in array_str.split(',')]
            break
    
    if spec_rust:
        return {
            'rgb': [r, g, b],
            'hex': f"#{r:02x}{g:02x}{b:02x}",
            'python': {
                'hue': spec_py[0],
                'value': spec_py[1],
                'chroma': spec_py[2],
                'code': int(spec_py[3])
            },
            'rust': {
                'hue': spec_rust[0],
                'value': spec_rust[1],
                'chroma': spec_rust[2],
                'code': int(spec_rust[3])
            },
            'diff': {
                'hue': abs(spec_py[0] - spec_rust[0]),
                'value': abs(spec_py[1] - spec_rust[1]),
                'chroma': abs(spec_py[2] - spec_rust[2])
            }
        }
    return None

# Test colors with known large chroma differences
problem_colors = [
    (34, 17, 119),    # Deep blue PB - 0.346 chroma diff
    (0, 0, 255),      # Pure blue
    (0, 0, 128),      # Dark blue
    (17, 34, 119),    # Another blue variant
    (119, 17, 34),    # Red variant
    (17, 119, 34),    # Green variant
    (255, 0, 255),    # Magenta
    (128, 0, 128),    # Purple
    (75, 0, 130),     # Indigo
    (238, 130, 238),  # Violet
]

print("=== FOCUSED CHROMA DISCREPANCY TEST ===")
print()
print("Testing colors with potential chroma convergence issues:")
print()

# Sort by chroma difference
results = []
for r, g, b in problem_colors:
    result = test_color_detailed(r, g, b)
    if result:
        results.append(result)

# Sort by chroma difference
results.sort(key=lambda x: x['diff']['chroma'], reverse=True)

print(f"{'Color':<15} {'Python Chroma':<12} {'Rust Chroma':<12} {'Diff':<8} {'Py Hue':<8} {'Rust Hue':<8}")
print("-" * 75)

for result in results:
    hex_color = result['hex']
    py_chroma = result['python']['chroma']
    rust_chroma = result['rust']['chroma']
    chroma_diff = result['diff']['chroma']
    py_hue = result['python']['hue']
    rust_hue = result['rust']['hue']
    
    print(f"{hex_color:<15} {py_chroma:<12.3f} {rust_chroma:<12.3f} {chroma_diff:<8.3f} {py_hue:<8.3f} {rust_hue:<8.3f}")

print()
print("Pattern Analysis:")
print(f"  Average chroma difference: {np.mean([r['diff']['chroma'] for r in results]):.3f}")
print(f"  Max chroma difference: {max([r['diff']['chroma'] for r in results]):.3f}")
print(f"  Colors with >0.1 chroma diff: {sum(1 for r in results if r['diff']['chroma'] > 0.1)}/{len(results)}")

# Check if there's a pattern in the chroma ratio
print()
print("Chroma Ratio Analysis (Rust/Python):")
for result in results[:5]:  # Top 5 worst
    hex_color = result['hex']
    ratio = result['rust']['chroma'] / result['python']['chroma'] if result['python']['chroma'] > 0 else 0
    print(f"  {hex_color}: {ratio:.4f}")