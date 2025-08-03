#!/usr/bin/env python3
"""
Sample validation of first 100 colors to get quick statistics.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation:
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

def main():
    print("SAMPLE VALIDATION: Testing first 100 colors")
    print("=" * 60)
    
    # Load reference colors
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 100:  # Only first 100
                break
            colors.append([
                int(row['R']),
                int(row['G']),
                int(row['B'])
            ])
    
    # Create batch input
    input_data = '\n'.join([f"{r},{g},{b}" for r, g, b in colors])
    
    # Get Rust results
    print("Running Rust implementation...")
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    # Parse Rust output - filter out TRACE and debug lines
    rust_results = []
    for line in result.stdout.split('\n'):
        # Skip TRACE output and debug lines
        if line.startswith('TRACE:') or line.startswith('Looking for'):
            continue
        if line and (line[0].isdigit() or line.startswith('N ')):
            rust_results.append(line)
    
    print(f"Got {len(rust_results)} Rust results")
    
    # Get Python results
    print("Running Python implementation...")
    python_results = []
    for r, g, b in colors:
        try:
            rgb_norm = [r/255.0, g/255.0, b/255.0]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            python_result = xyY_to_munsell_colour(xyY)
            python_results.append(python_result)
        except Exception as e:
            python_results.append(f"ERROR: {e}")
    
    print(f"Got {len(python_results)} Python results")
    
    # Compare results
    exact_matches = 0
    hue_diffs = []
    value_diffs = []
    chroma_diffs = []
    
    min_len = min(len(rust_results), len(python_results))
    
    for i in range(min_len):
        rust = rust_results[i]
        python = python_results[i]
        
        if rust == python:
            exact_matches += 1
        
        rust_p = parse_munsell(rust)
        python_p = parse_munsell(python)
        
        if rust_p and python_p:
            if rust_p['family'] == python_p['family']:
                hue_diff = abs(rust_p['hue'] - python_p['hue'])
                if hue_diff > 5:
                    hue_diff = 10 - hue_diff
                hue_diffs.append(hue_diff)
            
            value_diffs.append(abs(rust_p['value'] - python_p['value']))
            chroma_diffs.append(abs(rust_p['chroma'] - python_p['chroma']))
    
    # Print statistics
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Exact matches: {exact_matches}/{min_len} ({100*exact_matches/min_len:.1f}%)")
    
    if hue_diffs:
        print(f"\nHue differences:")
        print(f"  Mean: {np.mean(hue_diffs):.4f}")
        print(f"  Max:  {np.max(hue_diffs):.4f}")
        print(f"  99%:  {np.percentile(hue_diffs, 99):.4f}")
    
    if value_diffs:
        print(f"\nValue differences:")
        print(f"  Mean: {np.mean(value_diffs):.4f}")
        print(f"  Max:  {np.max(value_diffs):.4f}")
        print(f"  99%:  {np.percentile(value_diffs, 99):.4f}")
    
    if chroma_diffs:
        print(f"\nChroma differences:")
        print(f"  Mean: {np.mean(chroma_diffs):.4f}")
        print(f"  Max:  {np.max(chroma_diffs):.4f}")
        print(f"  99%:  {np.percentile(chroma_diffs, 99):.4f}")
    
    # Show a few examples
    print("\n" + "=" * 60)
    print("SAMPLE COMPARISONS")
    print("=" * 60)
    for i in range(min(5, min_len)):
        print(f"\nRGB{colors[i]}:")
        print(f"  Rust:   {rust_results[i]}")
        print(f"  Python: {python_results[i]}")
        if rust_results[i] == python_results[i]:
            print(f"  ✅ EXACT MATCH")

if __name__ == "__main__":
    main()