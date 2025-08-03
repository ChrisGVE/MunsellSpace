#!/usr/bin/env python3
"""
Extract actual worst cases from the 500-color validation and analyze them.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A":
        return None
        
    if notation.startswith('N '):
        return {
            'family': 'N',
            'hue': 0.0,
            'value': float(notation.split()[1]),
            'chroma': 0.0
        }
    
    parts = notation.split(' ')
    if len(parts) != 2:
        return None
    
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    
    # Extract hue number and family
    hue_num = ""
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            family = hue_part[len(hue_num):]
            break
    
    return {
        'family': family,
        'hue': float(hue_num) if hue_num else 0.0,
        'value': float(value_chroma[0]),
        'chroma': float(value_chroma[1]) if len(value_chroma) > 1 else 0.0
    }

# Load reference dataset
reference_map = {}
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        rgb_key = (int(row['R']), int(row['G']), int(row['B']))
        reference_map[rgb_key] = row['Munsell Colour']

print("Finding worst cases from first 500 colors...")

# Process first 500 colors to find actual worst cases
colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for i, row in enumerate(reader):
        if i >= 500:
            break
        colors.append([
            int(row['R']),
            int(row['G']),
            int(row['B'])
        ])

# Get Rust results in batch
input_data = '\n'.join([f"{r},{g},{b}" for r, g, b in colors])
result = subprocess.run(
    ['./target/release/batch_convert'],
    input=input_data,
    capture_output=True,
    text=True
)

# Parse Rust output
rust_results = []
for line in result.stdout.split('\n'):
    if line and not line.startswith('TRACE') and not line.startswith('Looking') and not line.startswith('EXACT'):
        if line and (line[0].isdigit() or line.startswith('N ')):
            rust_results.append(line)

# Get Python results and find worst cases
worst_hue = []
worst_value = []
worst_chroma = []

for i, (r, g, b) in enumerate(colors[:len(rust_results)]):
    try:
        rgb_norm = [r/255.0, g/255.0, b/255.0]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        python_result = xyY_to_munsell_colour(xyY)
        
        rust_result = rust_results[i]
        
        # Parse both results
        rust_p = parse_munsell(rust_result)
        python_p = parse_munsell(python_result)
        
        if rust_p and python_p:
            # Calculate differences
            if rust_p['family'] == python_p['family']:
                hue_diff = abs(rust_p['hue'] - python_p['hue'])
                if hue_diff > 5:
                    hue_diff = 10 - hue_diff
                
                if hue_diff > 0.05:  # Threshold for "worst"
                    worst_hue.append({
                        'rgb': [r, g, b],
                        'diff': hue_diff,
                        'rust': rust_result,
                        'python': python_result
                    })
            
            value_diff = abs(rust_p['value'] - python_p['value'])
            if value_diff > 0.01:
                worst_value.append({
                    'rgb': [r, g, b],
                    'diff': value_diff,
                    'rust': rust_result,
                    'python': python_result
                })
            
            chroma_diff = abs(rust_p['chroma'] - python_p['chroma'])
            if chroma_diff > 0.3:
                worst_chroma.append({
                    'rgb': [r, g, b],
                    'diff': chroma_diff,
                    'rust': rust_result,
                    'python': python_result
                })
                
    except Exception:
        pass

# Sort by difference
worst_hue.sort(key=lambda x: x['diff'], reverse=True)
worst_value.sort(key=lambda x: x['diff'], reverse=True)
worst_chroma.sort(key=lambda x: x['diff'], reverse=True)

print(f"Found {len(worst_hue)} colors with hue diff > 0.05")
print(f"Found {len(worst_value)} colors with value diff > 0.01")
print(f"Found {len(worst_chroma)} colors with chroma diff > 0.3")

print("\n" + "=" * 80)
print("DETAILED ANALYSIS OF ACTUAL WORST CASES")
print("=" * 80)

# Analyze top worst cases
def analyze_color(rgb, rust_result, python_result, diff_type, diff_value):
    """Detailed analysis of a single color."""
    rgb_key = tuple(rgb)
    reference = reference_map.get(rgb_key, "Not in reference")
    
    print(f"\n{diff_type} Difference: {diff_value:.4f}")
    print(f"RGB{rgb}")
    print(f"  Reference: {reference}")
    print(f"  Python:    {python_result}")
    print(f"  Rust:      {rust_result}")
    
    # Check which matches reference better
    if reference != "Not in reference":
        if python_result == reference:
            print("  → Python MATCHES reference exactly")
        elif rust_result == reference:
            print("  → Rust MATCHES reference exactly")
        else:
            print("  → Neither matches reference exactly")

print("\n" + "-" * 80)
print("TOP 5 WORST HUE DIFFERENCES")
print("-" * 80)
for case in worst_hue[:5]:
    analyze_color(case['rgb'], case['rust'], case['python'], "Hue", case['diff'])

print("\n" + "-" * 80)
print("TOP 5 WORST VALUE DIFFERENCES")
print("-" * 80)
for case in worst_value[:5]:
    analyze_color(case['rgb'], case['rust'], case['python'], "Value", case['diff'])

print("\n" + "-" * 80)
print("TOP 5 WORST CHROMA DIFFERENCES")
print("-" * 80)
for case in worst_chroma[:5]:
    analyze_color(case['rgb'], case['rust'], case['python'], "Chroma", case['diff'])

# Statistical summary
print("\n" + "=" * 80)
print("STATISTICAL SUMMARY OF DIFFERENCES")
print("=" * 80)

if worst_hue:
    hue_diffs = [c['diff'] for c in worst_hue]
    print(f"\nHue differences (n={len(hue_diffs)}):")
    print(f"  Mean: {np.mean(hue_diffs):.4f}")
    print(f"  Max:  {np.max(hue_diffs):.4f}")
    print(f"  Min:  {np.min(hue_diffs):.4f}")

if worst_value:
    value_diffs = [c['diff'] for c in worst_value]
    print(f"\nValue differences (n={len(value_diffs)}):")
    print(f"  Mean: {np.mean(value_diffs):.4f}")
    print(f"  Max:  {np.max(value_diffs):.4f}")
    print(f"  Min:  {np.min(value_diffs):.4f}")

if worst_chroma:
    chroma_diffs = [c['diff'] for c in worst_chroma]
    print(f"\nChroma differences (n={len(chroma_diffs)}):")
    print(f"  Mean: {np.mean(chroma_diffs):.4f}")
    print(f"  Max:  {np.max(chroma_diffs):.4f}")
    print(f"  Min:  {np.min(chroma_diffs):.4f}")

print("\n" + "=" * 80)