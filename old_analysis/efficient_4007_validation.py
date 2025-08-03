#!/usr/bin/env python3
"""
Efficient validation of all 4007 reference colors.
Processes colors in batches for better performance.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import time

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

def test_batch_rust(colors):
    """Test a batch of colors with Rust implementation."""
    # Create input for batch converter
    input_data = '\n'.join([f"{r},{g},{b}" for r, g, b in colors])
    
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    # Parse output - extract Munsell notations
    lines = result.stdout.strip().split('\n')
    results = []
    for line in lines:
        # Skip debug output and empty lines
        if line and (line[0].isdigit() or line.startswith('N ')):
            results.append(line)
    
    return results

def test_batch_python(colors):
    """Test a batch of colors with Python implementation."""
    results = []
    for r, g, b in colors:
        try:
            rgb_norm = [r/255.0, g/255.0, b/255.0]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            python_result = xyY_to_munsell_colour(xyY)
            results.append(python_result)
        except Exception as e:
            results.append(f"ERROR: {e}")
    return results

def main():
    print("=" * 80)
    print("EFFICIENT 4007 COLOR VALIDATION: Rust vs Python")
    print("=" * 80)
    
    # Load reference colors
    colors = []
    references = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            colors.append([
                int(row['R']),
                int(row['G']),
                int(row['B'])
            ])
            references.append(row['Munsell Colour'])
    
    print(f"\nTesting {len(colors)} colors...")
    print("Processing in batches for efficiency...")
    print("-" * 80)
    
    # Process in batches
    batch_size = 100
    all_rust_results = []
    all_python_results = []
    
    start_time = time.time()
    
    for i in range(0, len(colors), batch_size):
        batch = colors[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(colors)-1)//batch_size + 1}...")
        
        # Test with Rust
        rust_batch = test_batch_rust(batch)
        all_rust_results.extend(rust_batch)
        
        # Test with Python
        python_batch = test_batch_python(batch)
        all_python_results.extend(python_batch)
    
    elapsed = time.time() - start_time
    print(f"\nProcessing completed in {elapsed:.1f} seconds")
    
    # Ensure we have the right number of results
    print(f"Rust results: {len(all_rust_results)}")
    print(f"Python results: {len(all_python_results)}")
    
    # Align results if needed
    min_len = min(len(all_rust_results), len(all_python_results), len(colors))
    
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
    
    # Process results
    for i in range(min_len):
        r, g, b = colors[i]
        rust_result = all_rust_results[i] if i < len(all_rust_results) else "N/A"
        python_result = all_python_results[i] if i < len(all_python_results) else "N/A"
        reference = references[i]
        
        # Skip error cases
        if "ERROR" in rust_result or "ERROR" in python_result:
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
                'python': python_result,
                'reference': reference
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
    
    # Calculate statistics
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    total_tested = min_len
    print(f"\nTotal colors tested: {total_tested}")
    print(f"Exact matches: {exact_matches} ({100*exact_matches/total_tested:.2f}%)")
    print(f"Family mismatches: {len(family_mismatches)} ({100*len(family_mismatches)/total_tested:.2f}%)")
    
    # Percentile analysis
    print("\n" + "-" * 80)
    print("HUE DIFFERENCES (percentiles)")
    print("-" * 80)
    if hue_differences:
        hue_arr = np.array(hue_differences)
        percentiles = [50, 75, 90, 95, 99, 100]
        for p in percentiles:
            val = np.percentile(hue_arr, p)
            print(f"  {p:3d}th percentile: {val:.4f}")
        print(f"  Mean: {np.mean(hue_arr):.4f}")
        print(f"  Std Dev: {np.std(hue_arr):.4f}")
    
    print("\n" + "-" * 80)
    print("VALUE DIFFERENCES (percentiles)")
    print("-" * 80)
    if value_differences:
        value_arr = np.array(value_differences)
        for p in percentiles:
            val = np.percentile(value_arr, p)
            print(f"  {p:3d}th percentile: {val:.4f}")
        print(f"  Mean: {np.mean(value_arr):.4f}")
        print(f"  Std Dev: {np.std(value_arr):.4f}")
    
    print("\n" + "-" * 80)
    print("CHROMA DIFFERENCES (percentiles)")
    print("-" * 80)
    if chroma_differences:
        chroma_arr = np.array(chroma_differences)
        for p in percentiles:
            val = np.percentile(chroma_arr, p)
            print(f"  {p:3d}th percentile: {val:.4f}")
        print(f"  Mean: {np.mean(chroma_arr):.4f}")
        print(f"  Std Dev: {np.std(chroma_arr):.4f}")
    
    # Sort and display worst cases
    print("\n" + "=" * 80)
    print("WORST CASES")
    print("=" * 80)
    
    print("\nWorst 10 HUE differences:")
    worst_hue_cases.sort(key=lambda x: x['diff'], reverse=True)
    for case in worst_hue_cases[:10]:
        print(f"  RGB{case['rgb']}: Δ{case['diff']:.4f}")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    print("\nWorst 10 VALUE differences:")
    worst_value_cases.sort(key=lambda x: x['diff'], reverse=True)
    for case in worst_value_cases[:10]:
        print(f"  RGB{case['rgb']}: Δ{case['diff']:.4f}")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    print("\nWorst 10 CHROMA differences:")
    worst_chroma_cases.sort(key=lambda x: x['diff'], reverse=True)
    for case in worst_chroma_cases[:10]:
        print(f"  RGB{case['rgb']}: Δ{case['diff']:.4f}")
        print(f"    Rust:   {case['rust']}")
        print(f"    Python: {case['python']}")
    
    print("\nFamily MISMATCHES (first 10):")
    for case in family_mismatches[:10]:
        print(f"  RGB{case['rgb']}:")
        print(f"    Rust:      {case['rust']}")
        print(f"    Python:    {case['python']}")
        print(f"    Reference: {case['reference']}")
    
    # Save worst cases to CSV
    print("\n" + "-" * 80)
    print("Saving worst cases to worst_cases_full.csv...")
    
    with open('worst_cases_full.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Category', 'Difference', 'Rust', 'Python'])
        
        # Add worst hue cases
        for case in worst_hue_cases[:20]:
            writer.writerow([
                case['rgb'][0], case['rgb'][1], case['rgb'][2],
                'worst_hue', f"{case['diff']:.4f}", case['rust'], case['python']
            ])
        
        # Add worst value cases
        for case in worst_value_cases[:20]:
            writer.writerow([
                case['rgb'][0], case['rgb'][1], case['rgb'][2],
                'worst_value', f"{case['diff']:.4f}", case['rust'], case['python']
            ])
        
        # Add worst chroma cases
        for case in worst_chroma_cases[:20]:
            writer.writerow([
                case['rgb'][0], case['rgb'][1], case['rgb'][2],
                'worst_chroma', f"{case['diff']:.4f}", case['rust'], case['python']
            ])
        
        # Add family mismatches
        for case in family_mismatches[:20]:
            writer.writerow([
                case['rgb'][0], case['rgb'][1], case['rgb'][2],
                'family_mismatch', 'N/A', case['rust'], case['python']
            ])
    
    print("Worst cases saved to worst_cases_full.csv")
    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()