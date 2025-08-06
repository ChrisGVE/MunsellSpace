#!/usr/bin/env python3
"""Investigate issues with green color conversions"""

import csv
import subprocess
import random

def parse_munsell_components(notation):
    """Parse all components from Munsell notation"""
    if notation.startswith('N '):
        return {'family': 'N', 'hue': 0.0, 'value': float(notation.split()[1]), 'chroma': 0.0}
    
    parts = notation.split(' ')
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    
    # Extract hue and family
    hue_num = ''
    family = ''
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            family += char
    
    return {
        'family': family,
        'hue': float(hue_num) if hue_num else 0.0,
        'value': float(value_chroma[0]),
        'chroma': float(value_chroma[1])
    }

# Read reference dataset
reference_data = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        r, g, b = int(row[0]), int(row[1]), int(row[2])
        ref_munsell = row[3].strip()
        reference_data.append((r, g, b, ref_munsell))

# Find green colors with significant differences
print("Analyzing green color conversions...")
green_issues = []

for r, g, b, ref_munsell in reference_data:
    ref_comp = parse_munsell_components(ref_munsell)
    
    # Skip if not a green family
    if ref_comp['family'] not in ['G', 'GY', 'BG']:
        continue
    
    # Convert with Rust
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        continue
        
    rust_munsell = result.stdout.strip()
    rust_comp = parse_munsell_components(rust_munsell)
    
    # Check for significant differences
    value_diff = abs(ref_comp['value'] - rust_comp['value'])
    hue_diff = abs(ref_comp['hue'] - rust_comp['hue'])
    chroma_diff = abs(ref_comp['chroma'] - rust_comp['chroma'])
    
    if chroma_diff > 1.0 or value_diff > 0.5 or hue_diff > 1.0:
        green_issues.append({
            'rgb': (r, g, b),
            'ref': ref_munsell,
            'rust': rust_munsell,
            'value_diff': value_diff,
            'hue_diff': hue_diff,
            'chroma_diff': chroma_diff
        })

# Sort by chroma difference
green_issues.sort(key=lambda x: x['chroma_diff'], reverse=True)

print(f"\nFound {len(green_issues)} green colors with significant differences")
print("\nTop 10 problematic green colors:")
print("-" * 80)

for i, issue in enumerate(green_issues[:10]):
    print(f"\n{i+1}. RGB{issue['rgb']}:")
    print(f"   Reference: {issue['ref']}")
    print(f"   Rust:      {issue['rust']}")
    print(f"   Differences: value={issue['value_diff']:.2f}, hue={issue['hue_diff']:.2f}, chroma={issue['chroma_diff']:.2f}")

# Analyze patterns
print("\n\nPattern Analysis:")
high_value_issues = [i for i in green_issues if parse_munsell_components(i['ref'])['value'] > 7]
low_chroma_issues = [i for i in green_issues if parse_munsell_components(i['ref'])['chroma'] < 5]
gy_family_issues = [i for i in green_issues if 'GY' in i['ref']]

print(f"  High value (>7) issues: {len(high_value_issues)}/{len(green_issues)}")
print(f"  Low chroma (<5) issues: {len(low_chroma_issues)}/{len(green_issues)}")
print(f"  GY family issues: {len(gy_family_issues)}/{len(green_issues)}")

# Check if it's a systematic under-prediction
total_chroma_ref = sum(parse_munsell_components(i['ref'])['chroma'] for i in green_issues)
total_chroma_rust = sum(parse_munsell_components(i['rust'])['chroma'] for i in green_issues)
avg_chroma_ratio = total_chroma_rust / total_chroma_ref if total_chroma_ref > 0 else 0

print(f"\nAverage chroma ratio (Rust/Reference): {avg_chroma_ratio:.3f}")
if avg_chroma_ratio < 0.9:
    print("  -> Systematic under-prediction of chroma for greens")