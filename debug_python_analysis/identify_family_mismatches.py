#!/usr/bin/env python3
"""Identify colors with family mismatches"""

import subprocess
import csv
import re

# Pattern to parse Munsell notation
pattern = re.compile(r'([\d.]+)?([A-Z]+)\s+([\d.]+)(?:/([\d.]+))?')

def parse_munsell(notation):
    """Parse Munsell notation into components"""
    if notation.startswith('N '):
        parts = notation.split()
        return {'hue': 0, 'family': 'N', 'value': float(parts[1]), 'chroma': 0}
    
    match = pattern.match(notation)
    if match:
        hue = float(match.group(1)) if match.group(1) else 10.0
        family = match.group(2)
        value = float(match.group(3))
        chroma = float(match.group(4)) if match.group(4) else 0.0
        return {'hue': hue, 'family': family, 'value': value, 'chroma': chroma}
    
    return None

print("Identifying family mismatches...")
print("=" * 70)

mismatches = []
total = 0

with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    
    for row in reader:
        r, g, b, expected = int(row[0]), int(row[1]), int(row[2]), row[3].strip()
        
        # Get Rust result
        result = subprocess.run(
            ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            rust_output = result.stdout.strip()
            
            expected_parsed = parse_munsell(expected)
            rust_parsed = parse_munsell(rust_output)
            
            if expected_parsed and rust_parsed:
                if expected_parsed['family'] != rust_parsed['family']:
                    mismatches.append({
                        'rgb': (r, g, b),
                        'expected': expected,
                        'expected_family': expected_parsed['family'],
                        'rust': rust_output,
                        'rust_family': rust_parsed['family']
                    })
        
        total += 1
        if total % 500 == 0:
            print(f"  Processed {total}/4007 colors...")

print(f"\nFound {len(mismatches)} family mismatches out of {total} colors ({100*len(mismatches)/total:.2f}%)")

if mismatches:
    print("\nFirst 20 family mismatches:")
    print("-" * 100)
    print(f"{'RGB':<15} {'Expected':<20} {'Rust Output':<20} {'Family':<15}")
    print("-" * 100)
    
    for m in mismatches[:20]:
        rgb_str = f"[{m['rgb'][0]:3},{m['rgb'][1]:3},{m['rgb'][2]:3}]"
        family_str = f"{m['expected_family']} -> {m['rust_family']}"
        print(f"{rgb_str:<15} {m['expected']:<20} {m['rust']:<20} {family_str:<15}")
    
    # Analyze patterns
    print("\n" + "=" * 70)
    print("MISMATCH PATTERNS:")
    print("=" * 70)
    
    # Count transitions
    transitions = {}
    for m in mismatches:
        key = f"{m['expected_family']} -> {m['rust_family']}"
        transitions[key] = transitions.get(key, 0) + 1
    
    # Sort by frequency
    sorted_transitions = sorted(transitions.items(), key=lambda x: x[1], reverse=True)
    
    print("\nFamily transition frequencies:")
    for transition, count in sorted_transitions[:10]:
        print(f"  {transition:<15}: {count:3} cases ({100*count/len(mismatches):.1f}% of mismatches)")
    
    # Check if they're near boundaries
    print("\n" + "=" * 70)
    print("BOUNDARY ANALYSIS:")
    print("=" * 70)
    
    boundary_cases = 0
    for m in mismatches:
        expected = parse_munsell(m['expected'])
        # Check if hue is near 10.0 or 2.5 (family boundaries)
        if expected and expected['hue'] >= 9.5 or expected['hue'] <= 2.5:
            boundary_cases += 1
    
    print(f"\nColors near hue boundaries (9.5-10.0 or 0.0-2.5): {boundary_cases}/{len(mismatches)} ({100*boundary_cases/len(mismatches):.1f}%)")
    
    # Show some boundary cases
    print("\nExample boundary cases:")
    shown = 0
    for m in mismatches:
        expected = parse_munsell(m['expected'])
        if expected and (expected['hue'] >= 9.5 or expected['hue'] <= 2.5):
            rgb_str = f"[{m['rgb'][0]:3},{m['rgb'][1]:3},{m['rgb'][2]:3}]"
            print(f"  RGB {rgb_str}: {m['expected']} -> {m['rust']}")
            shown += 1
            if shown >= 5:
                break