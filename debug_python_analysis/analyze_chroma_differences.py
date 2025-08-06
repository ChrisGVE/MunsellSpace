#!/usr/bin/env python3
"""Analyze chroma differences to find patterns"""

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

# Test and analyze chroma differences
print("Analyzing chroma differences...")
chroma_diffs = []
large_chroma_diffs = []

# Sample 100 colors
test_samples = random.sample(reference_data, min(100, len(reference_data)))

for r, g, b, ref_munsell in test_samples:
    # Convert with Rust
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        continue
        
    rust_munsell = result.stdout.strip()
    
    # Parse components
    ref_comp = parse_munsell_components(ref_munsell)
    rust_comp = parse_munsell_components(rust_munsell)
    
    chroma_diff = abs(ref_comp['chroma'] - rust_comp['chroma'])
    chroma_diffs.append(chroma_diff)
    
    # Track large differences
    if chroma_diff > 0.5:
        large_chroma_diffs.append({
            'rgb': (r, g, b),
            'ref': ref_munsell,
            'rust': rust_munsell,
            'diff': chroma_diff,
            'ref_chroma': ref_comp['chroma'],
            'rust_chroma': rust_comp['chroma']
        })

# Analyze results
chroma_diffs.sort()
print(f"\nChroma difference statistics (n={len(chroma_diffs)}):")
print(f"  Mean: {sum(chroma_diffs)/len(chroma_diffs):.3f}")
print(f"  Median: {chroma_diffs[len(chroma_diffs)//2]:.3f}")
print(f"  Max: {max(chroma_diffs):.3f}")
print(f"  Within 0.1: {sum(1 for d in chroma_diffs if d <= 0.1)} ({sum(1 for d in chroma_diffs if d <= 0.1)/len(chroma_diffs)*100:.1f}%)")
print(f"  Within 0.5: {sum(1 for d in chroma_diffs if d <= 0.5)} ({sum(1 for d in chroma_diffs if d <= 0.5)/len(chroma_diffs)*100:.1f}%)")

# Show examples of large differences
if large_chroma_diffs:
    print(f"\nExamples of large chroma differences (>{0.5}):")
    # Sort by difference
    large_chroma_diffs.sort(key=lambda x: x['diff'], reverse=True)
    for i, case in enumerate(large_chroma_diffs[:5]):
        print(f"\n  {i+1}. RGB{case['rgb']}:")
        print(f"     Reference: {case['ref']} (chroma={case['ref_chroma']})")
        print(f"     Rust:      {case['rust']} (chroma={case['rust_chroma']})")
        print(f"     Difference: {case['diff']:.2f}")

# Check if there's a pattern
print("\nChecking for patterns...")
high_chroma_refs = [case for case in large_chroma_diffs if case['ref_chroma'] > 15]
low_chroma_refs = [case for case in large_chroma_diffs if case['ref_chroma'] < 5]

if high_chroma_refs:
    print(f"  High chroma (>15) with large diffs: {len(high_chroma_refs)}")
if low_chroma_refs:
    print(f"  Low chroma (<5) with large diffs: {len(low_chroma_refs)}")