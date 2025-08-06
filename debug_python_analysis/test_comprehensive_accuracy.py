#!/usr/bin/env python3
"""Comprehensive accuracy test on reference dataset"""

import csv
import subprocess
import random
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def parse_munsell(notation):
    """Parse Munsell notation into components"""
    if notation.startswith('N '):
        # Neutral color
        parts = notation.split()
        return {'hue': 0.0, 'value': float(parts[1]), 'chroma': 0.0, 'family': 'N'}
    
    # Regular color
    parts = notation.split(' ')
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    
    # Extract numeric hue
    hue_num = ''
    family = ''
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            family += char
    
    return {
        'hue': float(hue_num) if hue_num else 0.0,
        'value': float(value_chroma[0]),
        'chroma': float(value_chroma[1]),
        'family': family
    }

def test_reference_colors(sample_size=100):
    """Test a sample of reference colors"""
    
    print(f"Testing {sample_size} reference colors...")
    
    # Read reference dataset
    reference_data = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            ref_munsell = row[3].strip()
            reference_data.append((r, g, b, ref_munsell))
    
    # Sample randomly
    test_samples = random.sample(reference_data, min(sample_size, len(reference_data)))
    
    exact_matches = 0
    value_within_0_1 = 0
    hue_within_0_1 = 0
    chroma_within_0_1 = 0
    family_matches = 0
    
    for r, g, b, ref_munsell in test_samples:
        # Convert with Rust
        try:
            result = subprocess.run(
                ['cargo', 'run', '--bin', 'mathematical_convert_rgb', '--quiet', '--', str(r), str(g), str(b)],
                capture_output=True,
                text=True,
                timeout=5
            )
            rust_munsell = result.stdout.strip() if result.returncode == 0 else None
        except:
            rust_munsell = None
        
        if not rust_munsell:
            continue
        
        # Parse results
        ref_data = parse_munsell(ref_munsell)
        rust_data = parse_munsell(rust_munsell)
        
        # Compare
        if rust_munsell == ref_munsell:
            exact_matches += 1
        
        if abs(ref_data['value'] - rust_data['value']) <= 0.1:
            value_within_0_1 += 1
        
        if ref_data['family'] == rust_data['family']:
            family_matches += 1
            if abs(ref_data['hue'] - rust_data['hue']) <= 0.1:
                hue_within_0_1 += 1
        
        if abs(ref_data['chroma'] - rust_data['chroma']) <= 0.1:
            chroma_within_0_1 += 1
    
    # Report results
    print(f"\nResults on {sample_size} reference colors:")
    print(f"  Exact matches: {exact_matches}/{sample_size} ({exact_matches/sample_size*100:.1f}%)")
    print(f"  Family matches: {family_matches}/{sample_size} ({family_matches/sample_size*100:.1f}%)")
    print(f"  Values within 0.1: {value_within_0_1}/{sample_size} ({value_within_0_1/sample_size*100:.1f}%)")
    print(f"  Hues within 0.1 (same family): {hue_within_0_1}/{family_matches} ({hue_within_0_1/family_matches*100:.1f}%)" if family_matches > 0 else "")
    print(f"  Chromas within 0.1: {chroma_within_0_1}/{sample_size} ({chroma_within_0_1/sample_size*100:.1f}%)")

def test_random_colors(sample_size=100):
    """Test random RGB colors"""
    
    print(f"\nTesting {sample_size} random colors...")
    
    exact_matches = 0
    value_within_0_1 = 0
    hue_within_0_1 = 0
    chroma_within_0_1 = 0
    family_matches = 0
    both_succeeded = 0
    
    for _ in range(sample_size):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        
        # Python conversion
        try:
            rgb_norm = [r/255.0, g/255.0, b/255.0]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            py_munsell = xyY_to_munsell_colour(xyY)
            py_success = True
        except:
            py_success = False
        
        # Rust conversion
        try:
            result = subprocess.run(
                ['cargo', 'run', '--bin', 'mathematical_convert_rgb', '--quiet', '--', str(r), str(g), str(b)],
                capture_output=True,
                text=True,
                timeout=5
            )
            rust_munsell = result.stdout.strip() if result.returncode == 0 else None
            rust_success = rust_munsell is not None
        except:
            rust_success = False
        
        if not (py_success and rust_success):
            continue
        
        both_succeeded += 1
        
        # Parse results
        py_data = parse_munsell(py_munsell)
        rust_data = parse_munsell(rust_munsell)
        
        # Compare
        if rust_munsell == py_munsell:
            exact_matches += 1
        
        if abs(py_data['value'] - rust_data['value']) <= 0.1:
            value_within_0_1 += 1
        
        if py_data['family'] == rust_data['family']:
            family_matches += 1
            # Handle hue wraparound
            hue_diff = abs(py_data['hue'] - rust_data['hue'])
            if hue_diff > 5.0:
                hue_diff = 10.0 - hue_diff
            if hue_diff <= 0.1:
                hue_within_0_1 += 1
        
        if abs(py_data['chroma'] - rust_data['chroma']) <= 0.1:
            chroma_within_0_1 += 1
    
    # Report results
    print(f"\nResults on {both_succeeded} random colors (both systems succeeded):")
    print(f"  Exact matches: {exact_matches}/{both_succeeded} ({exact_matches/both_succeeded*100:.1f}%)" if both_succeeded > 0 else "")
    print(f"  Family matches: {family_matches}/{both_succeeded} ({family_matches/both_succeeded*100:.1f}%)" if both_succeeded > 0 else "")
    print(f"  Values within 0.1: {value_within_0_1}/{both_succeeded} ({value_within_0_1/both_succeeded*100:.1f}%)" if both_succeeded > 0 else "")
    print(f"  Hues within 0.1 (same family): {hue_within_0_1}/{family_matches} ({hue_within_0_1/family_matches*100:.1f}%)" if family_matches > 0 else "")
    print(f"  Chromas within 0.1: {chroma_within_0_1}/{both_succeeded} ({chroma_within_0_1/both_succeeded*100:.1f}%)" if both_succeeded > 0 else "")

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')
    
    test_reference_colors(100)
    test_random_colors(100)