#!/usr/bin/env python3
"""
Precise validation: Test all 4,007 colors and measure exact differences
in hue, value, and chroma between reference and Rust implementation.
"""

import csv
import subprocess
import time
import numpy as np
from collections import defaultdict

def parse_munsell(notation):
    """Parse Munsell notation into numeric components."""
    if not notation or notation == "ERROR":
        return None
    
    notation = notation.strip()
    
    # Handle neutral colors
    if notation.startswith('N '):
        parts = notation.split()
        if len(parts) >= 2:
            return {
                'family': 'N',
                'hue': 0.0,
                'value': float(parts[1]),
                'chroma': 0.0
            }
    
    # Handle chromatic colors (e.g., "7.9R 5.2/20.4")
    try:
        parts = notation.split(' ')
        if len(parts) != 2:
            return None
        
        hue_part = parts[0]
        value_chroma = parts[1]
        
        # Extract hue number and family
        hue_num = ""
        hue_family = ""
        for i, char in enumerate(hue_part):
            if char.isalpha() or char == '.':
                if char == '.':
                    hue_num += char
                else:
                    hue_family = hue_part[i:]
                    break
            else:
                hue_num += char
        
        if not hue_num or not hue_family:
            return None
            
        # Extract value and chroma
        if '/' in value_chroma:
            value_str, chroma_str = value_chroma.split('/')
            return {
                'family': hue_family,
                'hue': float(hue_num),
                'value': float(value_str),
                'chroma': float(chroma_str)
            }
    except:
        pass
    
    return None

def calculate_differences(expected, rust):
    """Calculate precise differences between expected and Rust results."""
    exp_parsed = parse_munsell(expected)
    rust_parsed = parse_munsell(rust)
    
    if not exp_parsed or not rust_parsed:
        return None
    
    result = {
        'expected': expected,
        'rust': rust,
        'family_match': exp_parsed['family'] == rust_parsed['family'],
        'exp_family': exp_parsed['family'],
        'rust_family': rust_parsed['family']
    }
    
    # Calculate hue difference (accounting for wraparound)
    if exp_parsed['family'] == rust_parsed['family'] and exp_parsed['family'] != 'N':
        hue_diff = abs(exp_parsed['hue'] - rust_parsed['hue'])
        if hue_diff > 5.0:  # Handle wraparound (e.g., 9.9 vs 0.1)
            hue_diff = 10.0 - hue_diff
        result['hue_diff'] = hue_diff
    else:
        result['hue_diff'] = None  # Different families or neutral
    
    # Calculate value and chroma differences
    result['value_diff'] = abs(exp_parsed['value'] - rust_parsed['value'])
    result['chroma_diff'] = abs(exp_parsed['chroma'] - rust_parsed['chroma'])
    
    return result

def main():
    print("=" * 80)
    print("PRECISE VALIDATION: Measuring exact differences for all 4,007 colors")
    print("=" * 80)
    
    # Load reference dataset
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors.append((r, g, b, expected))
    
    print(f"\nLoaded {len(colors)} colors from reference dataset")
    
    # Build Rust binary
    print("Building Rust binary...")
    subprocess.run(['cargo', 'build', '--release', '--bin', 'batch_convert'], 
                   capture_output=True)
    
    # Prepare input for batch converter
    input_data = '\n'.join(f"{r},{g},{b}" for r, g, b, _ in colors)
    
    # Run Rust converter on all colors
    print(f"\nProcessing all {len(colors)} colors with Rust...")
    start = time.time()
    
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    rust_results = result.stdout.strip().split('\n')
    elapsed = time.time() - start
    
    print(f"✓ Completed in {elapsed:.1f} seconds ({len(colors)/elapsed:.1f} colors/second)")
    
    # Calculate differences for all colors
    print("\nCalculating precise differences...")
    
    all_differences = []
    parse_errors = 0
    exact_matches = 0
    family_mismatches = []
    
    hue_diffs = []
    value_diffs = []
    chroma_diffs = []
    
    for (r, g, b, expected), rust_result in zip(colors, rust_results):
        diff = calculate_differences(expected, rust_result)
        
        if not diff:
            parse_errors += 1
            continue
        
        all_differences.append((r, g, b, diff))
        
        # Check for exact match
        if expected == rust_result:
            exact_matches += 1
        
        # Track family mismatches
        if not diff['family_match']:
            family_mismatches.append((r, g, b, diff))
        
        # Collect numeric differences
        if diff['hue_diff'] is not None:
            hue_diffs.append(diff['hue_diff'])
        value_diffs.append(diff['value_diff'])
        chroma_diffs.append(diff['chroma_diff'])
    
    # Calculate statistics
    print("\n" + "=" * 80)
    print("OVERALL STATISTICS")
    print("=" * 80)
    
    print(f"Total colors tested:     {len(colors):,}")
    print(f"Successfully parsed:     {len(all_differences):,}")
    print(f"Parse errors:           {parse_errors:,}")
    print(f"Exact matches:          {exact_matches:,} ({100*exact_matches/len(colors):.1f}%)")
    print(f"Family mismatches:      {len(family_mismatches):,} ({100*len(family_mismatches)/len(colors):.1f}%)")
    
    # Percentile analysis
    print("\n" + "=" * 80)
    print("DIFFERENCE PERCENTILES")
    print("=" * 80)
    
    if hue_diffs:
        print(f"\nHue Differences (n={len(hue_diffs)}, same family only):")
        for p in [0, 25, 50, 75, 90, 95, 99, 100]:
            val = np.percentile(hue_diffs, p)
            print(f"  {p:3d}th percentile: {val:.3f}")
    
    print(f"\nValue Differences (n={len(value_diffs)}):")
    for p in [0, 25, 50, 75, 90, 95, 99, 100]:
        val = np.percentile(value_diffs, p)
        print(f"  {p:3d}th percentile: {val:.3f}")
    
    print(f"\nChroma Differences (n={len(chroma_diffs)}):")
    for p in [0, 25, 50, 75, 90, 95, 99, 100]:
        val = np.percentile(chroma_diffs, p)
        print(f"  {p:3d}th percentile: {val:.3f}")
    
    # Find worst cases
    print("\n" + "=" * 80)
    print("WORST CASES")
    print("=" * 80)
    
    # Sort by hue difference (same family only)
    hue_sorted = [(r, g, b, d) for r, g, b, d in all_differences 
                  if d['hue_diff'] is not None]
    hue_sorted.sort(key=lambda x: x[3]['hue_diff'], reverse=True)
    
    print("\n--- Worst 10 Hue Differences (same family) ---")
    for r, g, b, diff in hue_sorted[:10]:
        print(f"RGB({r:3},{g:3},{b:3}): {diff['expected']:20s} vs {diff['rust']:20s} | Δhue={diff['hue_diff']:.3f}")
    
    # Sort by value difference
    value_sorted = sorted(all_differences, key=lambda x: x[3]['value_diff'], reverse=True)
    
    print("\n--- Worst 10 Value Differences ---")
    for r, g, b, diff in value_sorted[:10]:
        print(f"RGB({r:3},{g:3},{b:3}): {diff['expected']:20s} vs {diff['rust']:20s} | Δvalue={diff['value_diff']:.3f}")
    
    # Sort by chroma difference
    chroma_sorted = sorted(all_differences, key=lambda x: x[3]['chroma_diff'], reverse=True)
    
    print("\n--- Worst 10 Chroma Differences ---")
    for r, g, b, diff in chroma_sorted[:10]:
        print(f"RGB({r:3},{g:3},{b:3}): {diff['expected']:20s} vs {diff['rust']:20s} | Δchroma={diff['chroma_diff']:.3f}")
    
    # Show family mismatches
    print("\n--- First 10 Family Mismatches ---")
    for r, g, b, diff in family_mismatches[:10]:
        print(f"RGB({r:3},{g:3},{b:3}): {diff['expected']:20s} vs {diff['rust']:20s} | {diff['exp_family']} → {diff['rust_family']}")
    
    # Save worst cases for Python testing
    print("\n" + "=" * 80)
    print("SAVING WORST CASES FOR PYTHON TESTING")
    print("=" * 80)
    
    worst_cases = []
    
    # Add worst hue differences
    for r, g, b, _ in hue_sorted[:5]:
        worst_cases.append((r, g, b, "worst_hue"))
    
    # Add worst value differences
    for r, g, b, _ in value_sorted[:5]:
        worst_cases.append((r, g, b, "worst_value"))
    
    # Add worst chroma differences
    for r, g, b, _ in chroma_sorted[:5]:
        worst_cases.append((r, g, b, "worst_chroma"))
    
    # Add family mismatches
    for r, g, b, _ in family_mismatches[:5]:
        worst_cases.append((r, g, b, "family_mismatch"))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_worst = []
    for item in worst_cases:
        key = (item[0], item[1], item[2])
        if key not in seen:
            seen.add(key)
            unique_worst.append(item)
    
    with open('worst_cases.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Category'])
        for r, g, b, category in unique_worst:
            writer.writerow([r, g, b, category])
    
    print(f"Saved {len(unique_worst)} worst case colors to worst_cases.csv")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    # Count colors by difference threshold
    very_close = sum(1 for _, _, _, d in all_differences 
                     if d['hue_diff'] is not None and d['hue_diff'] <= 0.5 
                     and d['value_diff'] <= 0.5 and d['chroma_diff'] <= 0.5
                     and d['family_match'])
    
    close = sum(1 for _, _, _, d in all_differences 
                if d['hue_diff'] is not None and d['hue_diff'] <= 1.0 
                and d['value_diff'] <= 1.0 and d['chroma_diff'] <= 1.0
                and d['family_match'])
    
    print(f"Colors with all differences ≤ 0.5: {very_close:,} ({100*very_close/len(colors):.1f}%)")
    print(f"Colors with all differences ≤ 1.0: {close:,} ({100*close/len(colors):.1f}%)")
    print(f"Colors with correct family:        {len(colors)-len(family_mismatches):,} ({100*(len(colors)-len(family_mismatches))/len(colors):.1f}%)")

if __name__ == "__main__":
    main()