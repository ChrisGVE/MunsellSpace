#!/usr/bin/env python3
"""Test accuracy on a larger sample"""

import csv
import subprocess
import random

def parse_munsell_value(notation):
    """Extract just the numeric value from Munsell notation"""
    if notation.startswith('N '):
        return float(notation.split()[1])
    parts = notation.split(' ')
    if len(parts) >= 2:
        value_chroma = parts[1].split('/')
        return float(value_chroma[0])
    return 0.0

def parse_munsell_chroma(notation):
    """Extract just the numeric chroma from Munsell notation"""
    if notation.startswith('N '):
        return 0.0
    parts = notation.split(' ')
    if len(parts) >= 2:
        value_chroma = parts[1].split('/')
        if len(value_chroma) >= 2:
            return float(value_chroma[1])
    return 0.0

def parse_munsell_hue(notation):
    """Extract numeric hue from Munsell notation"""
    if notation.startswith('N '):
        return 0.0
    parts = notation.split(' ')
    hue_part = parts[0]
    hue_num = ''
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            break
    return float(hue_num) if hue_num else 0.0

def parse_munsell_family(notation):
    """Extract hue family from Munsell notation"""
    if notation.startswith('N '):
        return 'N'
    parts = notation.split(' ')
    hue_part = parts[0]
    family = ''
    for char in hue_part:
        if not (char.isdigit() or char == '.'):
            family += char
    return family

# Read reference dataset
print("Loading reference dataset...")
reference_data = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        r, g, b = int(row[0]), int(row[1]), int(row[2])
        ref_munsell = row[3].strip()
        reference_data.append((r, g, b, ref_munsell))

# Test on a sample
sample_size = 200
test_samples = random.sample(reference_data, min(sample_size, len(reference_data)))

print(f"\nTesting {sample_size} colors...")
exact_matches = 0
value_close = 0
hue_close = 0
chroma_close = 0
family_matches = 0

for i, (r, g, b, ref_munsell) in enumerate(test_samples):
    if i % 20 == 0:
        print(f"  Progress: {i}/{sample_size}", end='\r')
    
    # Convert with Rust
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        continue
        
    rust_munsell = result.stdout.strip()
    
    # Compare
    if rust_munsell == ref_munsell:
        exact_matches += 1
    
    # Parse components
    ref_value = parse_munsell_value(ref_munsell)
    rust_value = parse_munsell_value(rust_munsell)
    if abs(ref_value - rust_value) <= 0.1:
        value_close += 1
    
    ref_family = parse_munsell_family(ref_munsell)
    rust_family = parse_munsell_family(rust_munsell)
    if ref_family == rust_family:
        family_matches += 1
        
        ref_hue = parse_munsell_hue(ref_munsell)
        rust_hue = parse_munsell_hue(rust_munsell)
        if abs(ref_hue - rust_hue) <= 0.1:
            hue_close += 1
    
    ref_chroma = parse_munsell_chroma(ref_munsell)
    rust_chroma = parse_munsell_chroma(rust_munsell)
    if abs(ref_chroma - rust_chroma) <= 0.1:
        chroma_close += 1

print(f"\n\nResults on {sample_size} reference colors:")
print(f"  Exact matches: {exact_matches} ({exact_matches/sample_size*100:.1f}%)")
print(f"  Family matches: {family_matches} ({family_matches/sample_size*100:.1f}%)")
print(f"  Values within 0.1: {value_close} ({value_close/sample_size*100:.1f}%)")
print(f"  Hues within 0.1 (same family): {hue_close}/{family_matches} ({hue_close/family_matches*100:.1f}%)" if family_matches > 0 else "")
print(f"  Chromas within 0.1: {chroma_close} ({chroma_close/sample_size*100:.1f}%)")