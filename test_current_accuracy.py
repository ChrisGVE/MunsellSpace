#!/usr/bin/env python3
"""
Test current accuracy after all fixes
"""

import csv

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A" or notation.startswith("ERROR"):
        return None
        
    notation = notation.strip()
    
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

print("Loading results...")

# Load Python results
python_results = []
with open('python_4007_final.txt', 'r') as f:
    for line in f:
        python_results.append(line.strip())

# Load Rust results
rust_results = []
with open('rust_4007_current.txt', 'r') as f:
    for line in f:
        rust_results.append(line.strip())

# Load reference data
reference_data = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        reference_data.append(row[3])  # Munsell notation is in column 4

print(f"Loaded {len(rust_results)} Rust results")
print(f"Loaded {len(python_results)} Python results")
print(f"Loaded {len(reference_data)} reference entries")

# Compare
exact_matches = 0
family_mismatches = 0
max_hue_diff = 0
max_value_diff = 0
max_chroma_diff = 0

for i in range(min(len(rust_results), len(python_results))):
    rust = parse_munsell(rust_results[i])
    python = parse_munsell(python_results[i])
    
    if not rust or not python:
        continue
    
    if rust == python:
        exact_matches += 1
    else:
        # Check family mismatch
        if rust['family'] != python['family']:
            family_mismatches += 1
        
        # Track max differences
        hue_diff = abs(rust['hue'] - python['hue'])
        value_diff = abs(rust['value'] - python['value'])
        chroma_diff = abs(rust['chroma'] - python['chroma'])
        
        max_hue_diff = max(max_hue_diff, hue_diff)
        max_value_diff = max(max_value_diff, value_diff)
        max_chroma_diff = max(max_chroma_diff, chroma_diff)

print("\n" + "="*60)
print("CURRENT ACCURACY AFTER FIXES")
print("="*60)
print(f"Exact matches: {exact_matches}/{len(rust_results)} ({100*exact_matches/len(rust_results):.2f}%)")
print(f"Family mismatches: {family_mismatches}")
print(f"Max hue difference: {max_hue_diff:.1f}")
print(f"Max value difference: {max_value_diff:.1f}")
print(f"Max chroma difference: {max_chroma_diff:.1f}")

# Check success criteria
print("\n" + "="*60)
print("SUCCESS CRITERIA CHECK")
print("="*60)
print(f"✓ Family mismatches ≤ 2: {'YES' if family_mismatches <= 2 else 'NO'} ({family_mismatches} mismatches)")
print(f"✓ All differences ≤ 0.1: {'YES' if max_hue_diff <= 0.1 and max_value_diff <= 0.1 and max_chroma_diff <= 0.1 else 'NO'}")
if max_hue_diff > 0.1:
    print(f"  - Hue: {max_hue_diff:.1f} > 0.1")
if max_value_diff > 0.1:
    print(f"  - Value: {max_value_diff:.1f} > 0.1")
if max_chroma_diff > 0.1:
    print(f"  - Chroma: {max_chroma_diff:.1f} > 0.1")