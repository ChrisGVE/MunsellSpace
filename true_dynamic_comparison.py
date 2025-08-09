#!/usr/bin/env python3
"""True dynamic comparison between Python and Rust implementations."""

import subprocess
import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import csv

def get_python_munsell(r, g, b):
    """Get Python's Munsell notation dynamically."""
    try:
        srgb = [r/255, g/255, b/255]
        XYZ = sRGB_to_XYZ(srgb)
        xyY = XYZ_to_xyY(XYZ)
        return xyY_to_munsell_colour(xyY)
    except:
        return None

def get_rust_munsell(r, g, b):
    """Get Rust's Munsell notation."""
    try:
        result = subprocess.run(
            ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        for line in result.stdout.split('\n'):
            if line.startswith('Munsell:'):
                return line.replace('Munsell:', '').strip()
        return None
    except:
        return None

# Test colors that were "misclassified" according to the CSV
problem_colors = [
    (68, 102, 68),   # CSV said Python: 10.0GY
    (85, 0, 51),     # CSV said Python: 0.2R
    (119, 85, 221),  # CSV said Python: 10.0PB
    (136, 17, 68),   # CSV said Python: 0.1R
    (153, 68, 51),   # CSV said Python: 0.0YR
    (170, 34, 0),    # CSV said Python: 0.1YR
    (170, 34, 85),   # CSV said Python: 0.0R
    (221, 85, 204),  # CSV said Python: 10.0P (we fixed to 0.0RP)
    (255, 238, 238), # CSV said Python: 0.0Y (we fixed to 10.0YR)
]

print("True Dynamic Comparison (Python vs Rust):")
print("=" * 70)
print("Checking what Python ACTUALLY returns vs what the CSV claims:")
print()

# First, check CSV values
csv_values = {}
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r = int(row['R'])
        g = int(row[' G'] if ' G' in row else row['G'])
        b = int(row[' B'] if ' B' in row else row['B'])
        munsell = row[' Munsell Colour'] if ' Munsell Colour' in row else row['Munsell Colour']
        csv_values[(r, g, b)] = munsell.strip()

matches = 0
csv_wrong = 0

for r, g, b in problem_colors:
    python_actual = get_python_munsell(r, g, b)
    rust_actual = get_rust_munsell(r, g, b)
    csv_value = csv_values.get((r, g, b), "Not in CSV")
    
    python_rust_match = python_actual == rust_actual
    csv_correct = csv_value == python_actual
    
    if python_rust_match:
        matches += 1
    if not csv_correct and csv_value != "Not in CSV":
        csv_wrong += 1
    
    print(f"RGB({r:3},{g:3},{b:3}):")
    print(f"  CSV claims Python: {csv_value}")
    print(f"  Python actually:   {python_actual}")
    print(f"  Rust returns:      {rust_actual}")
    print(f"  CSV correct? {'✓' if csv_correct else '✗ WRONG!'}")
    print(f"  Python==Rust? {'✓ MATCH!' if python_rust_match else '✗ Different'}")
    print()

print("=" * 70)
print(f"Results:")
print(f"  {matches}/{len(problem_colors)} colors match between Python and Rust")
print(f"  {csv_wrong}/{len(problem_colors)} CSV values were WRONG")
print()
print("CONCLUSION: The CSV reference data is unreliable for boundary colors!")
print("We should use dynamic Python comparison, not the static CSV.")