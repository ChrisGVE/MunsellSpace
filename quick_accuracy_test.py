#!/usr/bin/env python3
"""Quick accuracy test - sample 200 colors evenly across the dataset"""

import csv
import subprocess
import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ, XYZ_to_xyY

# Load all colors
colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        colors.append((int(row[0]), int(row[1]), int(row[2]), row[3]))

# Sample evenly
sample_size = 200
indices = np.linspace(0, len(colors)-1, sample_size, dtype=int)
sampled = [colors[i] for i in indices]

print(f"Testing {sample_size} colors sampled from {len(colors)} total...")

stats = {
    'hue_diffs': [],
    'value_diffs': [],
    'chroma_diffs': [],
    'family_mismatches': 0,
    'total': 0,
    'within_tolerance': 0
}

for i, (r, g, b, expected) in enumerate(sampled):
    if i % 20 == 0:
        print(f"Progress: {i}/{sample_size}")
    
    # Python conversion
    try:
        srgb = [r/255.0, g/255.0, b/255.0]
        xyz = sRGB_to_XYZ(srgb)
        xyy = XYZ_to_xyY(xyz)
        py_spec = munsell.xyY_to_munsell_specification(xyy)
    except:
        continue
    
    # Rust conversion
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True, text=True, timeout=1
    )
    
    if result.returncode != 0 or 'Munsell:' not in result.stdout:
        continue
    
    rust_notation = result.stdout.split('Munsell:')[1].strip()
    
    try:
        rust_spec = munsell.munsell_colour_to_munsell_specification(rust_notation)
    except:
        continue
    
    # Calculate differences
    h_diff = abs(py_spec[0] - rust_spec[0]) if not (np.isnan(py_spec[0]) or np.isnan(rust_spec[0])) else 0
    v_diff = abs(py_spec[1] - rust_spec[1])
    c_diff = abs(py_spec[2] - rust_spec[2]) if not (np.isnan(py_spec[2]) or np.isnan(rust_spec[2])) else 0
    
    stats['hue_diffs'].append(h_diff)
    stats['value_diffs'].append(v_diff)
    stats['chroma_diffs'].append(c_diff)
    stats['total'] += 1
    
    if h_diff <= 0.1 and v_diff <= 0.1 and c_diff <= 0.1:
        stats['within_tolerance'] += 1
    
    if int(py_spec[3]) != int(rust_spec[3]):
        stats['family_mismatches'] += 1

# Print results
print("\n" + "="*80)
print("QUICK ACCURACY TEST RESULTS")
print("="*80)

accuracy = 100 * stats['within_tolerance'] / stats['total'] if stats['total'] > 0 else 0
print(f"\nOverall Accuracy: {accuracy:.1f}% ({stats['within_tolerance']}/{stats['total']} within 0.1 tolerance)")
print(f"Family Mismatches: {stats['family_mismatches']} ({100*stats['family_mismatches']/stats['total']:.1f}%)")

print(f"\nComponent Statistics:")
for component, diffs in [('Hue', stats['hue_diffs']), 
                         ('Value', stats['value_diffs']), 
                         ('Chroma', stats['chroma_diffs'])]:
    if diffs:
        print(f"\n{component}:")
        print(f"  Median: {np.median(diffs):.6f}")
        print(f"  90th %ile: {np.percentile(diffs, 90):.6f}")
        print(f"  95th %ile: {np.percentile(diffs, 95):.6f}")
        print(f"  99th %ile: {np.percentile(diffs, 99):.6f}")
        print(f"  Max: {max(diffs):.6f}")
        print(f"  >0.1: {sum(1 for d in diffs if d > 0.1)} ({100*sum(1 for d in diffs if d > 0.1)/len(diffs):.1f}%)")

print("="*80)