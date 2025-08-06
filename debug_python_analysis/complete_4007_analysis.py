#!/usr/bin/env python3
"""
Complete analysis of all 4007 colors comparing pre-generated Rust results with Python.
"""

import csv
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
    print("=" * 80)
    print("COMPLETE 4007 COLOR ANALYSIS: Rust vs Python")
    print("=" * 80)
    
    # Load reference colors
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            colors.append([
                int(row['R']),
                int(row['G']),
                int(row['B'])
            ])
    
    print(f"\nLoaded {len(colors)} reference colors")
    
    # Load pre-generated Rust results
    rust_results = []
    with open('rust_4007_clean.txt', 'r') as f:
        for line in f:
            rust_results.append(line.strip())
    
    print(f"Loaded {len(rust_results)} Rust results")
    
    # Generate Python results
    print("\nGenerating Python results...")
    python_results = []
    for i, (r, g, b) in enumerate(colors):
        if i % 500 == 0:
            print(f"  Progress: {i}/{len(colors)}")
        try:
            rgb_norm = [r/255.0, g/255.0, b/255.0]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            python_result = xyY_to_munsell_colour(xyY)
            python_results.append(python_result)
        except Exception as e:
            python_results.append(f"ERROR: {e}")
    
    print(f"Generated {len(python_results)} Python results")
    
    # Statistics tracking
    exact_matches = 0
    family_mismatches = []
    hue_differences = []
    value_differences = []
    chroma_differences = []
    
    # Worst cases tracking
    worst_hue_cases = []
    worst_value_cases = []
    worst_chroma_cases = []
    
    # Compare all results
    print("\nAnalyzing differences...")
    for i in range(len(colors)):
        r, g, b = colors[i]
        rust_result = rust_results[i] if i < len(rust_results) else "N/A"
        python_result = python_results[i] if i < len(python_results) else "N/A"
        
        # Skip error cases
        if "ERROR" in str(rust_result) or "ERROR" in str(python_result):
            continue
        
        # Parse results
        rust_parsed = parse_munsell(rust_result)
        python_parsed = parse_munsell(python_result)
        
        if not rust_parsed or not python_parsed:
            continue
        
        # Check for exact match
        if rust_result == python_result:
            exact_matches += 1
        
        # Calculate differences
        if rust_parsed['family'] != python_parsed['family']:
            family_mismatches.append({
                'rgb': [r, g, b],
                'rust': rust_result,
                'python': python_result
            })
        else:
            # Calculate hue difference (handling wraparound)
            hue_diff = abs(rust_parsed['hue'] - python_parsed['hue'])
            if hue_diff > 5:
                hue_diff = 10 - hue_diff
            hue_differences.append(hue_diff)
            
            # Track worst hue cases
            if hue_diff > 0.1:
                worst_hue_cases.append({
                    'rgb': [r, g, b],
                    'diff': hue_diff,
                    'rust': rust_result,
                    'python': python_result
                })
        
        # Value difference
        value_diff = abs(rust_parsed['value'] - python_parsed['value'])
        value_differences.append(value_diff)
        
        # Track worst value cases
        if value_diff > 0.1:
            worst_value_cases.append({
                'rgb': [r, g, b],
                'diff': value_diff,
                'rust': rust_result,
                'python': python_result
            })
        
        # Chroma difference
        chroma_diff = abs(rust_parsed['chroma'] - python_parsed['chroma'])
        chroma_differences.append(chroma_diff)
        
        # Track worst chroma cases
        if chroma_diff > 0.5:
            worst_chroma_cases.append({
                'rgb': [r, g, b],
                'diff': chroma_diff,
                'rust': rust_result,
                'python': python_result
            })
    
    # Calculate and display statistics
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    total_tested = len(colors)
    print(f"\nTotal colors tested: {total_tested}")
    print(f"Exact matches: {exact_matches} ({100*exact_matches/total_tested:.2f}%)")
    print(f"Family mismatches: {len(family_mismatches)} ({100*len(family_mismatches)/total_tested:.2f}%)")
    
    # Percentile analysis
    percentiles = [50, 75, 90, 95, 99, 99.9, 100]
    
    print("\n" + "-" * 80)
    print("HUE DIFFERENCES (percentiles)")
    print("-" * 80)
    if hue_differences:
        hue_arr = np.array(hue_differences)
        for p in percentiles:
            val = np.percentile(hue_arr, p)
            print(f"  {p:5.1f}th percentile: {val:.6f}")
        print(f"  Mean: {np.mean(hue_arr):.6f}")
        print(f"  Std Dev: {np.std(hue_arr):.6f}")
    
    print("\n" + "-" * 80)
    print("VALUE DIFFERENCES (percentiles)")
    print("-" * 80)
    if value_differences:
        value_arr = np.array(value_differences)
        for p in percentiles:
            val = np.percentile(value_arr, p)
            print(f"  {p:5.1f}th percentile: {val:.6f}")
        print(f"  Mean: {np.mean(value_arr):.6f}")
        print(f"  Std Dev: {np.std(value_arr):.6f}")
    
    print("\n" + "-" * 80)
    print("CHROMA DIFFERENCES (percentiles)")
    print("-" * 80)
    if chroma_differences:
        chroma_arr = np.array(chroma_differences)
        for p in percentiles:
            val = np.percentile(chroma_arr, p)
            print(f"  {p:5.1f}th percentile: {val:.6f}")
        print(f"  Mean: {np.mean(chroma_arr):.6f}")
        print(f"  Std Dev: {np.std(chroma_arr):.6f}")
    
    # Sort and display worst cases
    print("\n" + "=" * 80)
    print("WORST CASES")
    print("=" * 80)
    
    print("\nWorst 20 HUE differences:")
    worst_hue_cases.sort(key=lambda x: x['diff'], reverse=True)
    for i, case in enumerate(worst_hue_cases[:20]):
        print(f"{i+1:2}. RGB{case['rgb']}: Δ{case['diff']:.6f}")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    print("\nWorst 20 VALUE differences:")
    worst_value_cases.sort(key=lambda x: x['diff'], reverse=True)
    for i, case in enumerate(worst_value_cases[:20]):
        print(f"{i+1:2}. RGB{case['rgb']}: Δ{case['diff']:.6f}")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    print("\nWorst 20 CHROMA differences:")
    worst_chroma_cases.sort(key=lambda x: x['diff'], reverse=True)
    for i, case in enumerate(worst_chroma_cases[:20]):
        print(f"{i+1:2}. RGB{case['rgb']}: Δ{case['diff']:.6f}")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    print("\nAll FAMILY MISMATCHES:")
    for i, case in enumerate(family_mismatches):
        print(f"{i+1:2}. RGB{case['rgb']}:")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    # Verify worst cases with Python
    print("\n" + "=" * 80)
    print("VERIFYING WORST CASES WITH PYTHON")
    print("=" * 80)
    
    # Collect unique worst cases
    worst_colors = set()
    
    # Add worst from each category
    for case in worst_hue_cases[:10]:
        worst_colors.add(tuple(case['rgb']))
    
    for case in worst_value_cases[:10]:
        worst_colors.add(tuple(case['rgb']))
    
    for case in worst_chroma_cases[:10]:
        worst_colors.add(tuple(case['rgb']))
    
    for case in family_mismatches[:10]:
        worst_colors.add(tuple(case['rgb']))
    
    print(f"\nVerifying {len(worst_colors)} worst case colors individually:")
    print("-" * 80)
    
    for rgb_tuple in sorted(worst_colors):
        r, g, b = rgb_tuple
        
        # Python test
        rgb_norm = [r/255.0, g/255.0, b/255.0]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        python_individual = xyY_to_munsell_colour(xyY)
        
        # Find original results
        idx = colors.index([r, g, b])
        rust_original = rust_results[idx] if idx < len(rust_results) else "N/A"
        python_original = python_results[idx] if idx < len(python_results) else "N/A"
        
        print(f"\nRGB[{r}, {g}, {b}]:")
        print(f"  Rust result:              {rust_original}")
        print(f"  Python batch result:      {python_original}")
        print(f"  Python individual verify: {python_individual}")
        if python_original == python_individual:
            print(f"  ✅ Python results consistent")
        else:
            print(f"  ⚠️ Python results differ!")
    
    print("\n" + "=" * 80)
    print("COMPLETE ANALYSIS FINISHED")
    print("=" * 80)

if __name__ == "__main__":
    main()