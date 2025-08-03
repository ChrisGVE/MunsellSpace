#!/usr/bin/env python3
"""
Complete analysis of ALL 4007 colors with detailed percentiles and family mismatches.
No shortcuts - everything computed on the full dataset.
"""

import csv
import numpy as np
from collections import defaultdict

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A" or notation.startswith("ERROR"):
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

print("=" * 80)
print("COMPLETE 4007 COLOR ANALYSIS - NO SHORTCUTS")
print("=" * 80)

# Load all data
print("\nLoading data...")

# Reference colors
colors = []
reference_notations = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        colors.append([int(row['R']), int(row['G']), int(row['B'])])
        reference_notations.append(row['Munsell Colour'])

# Rust results
rust_results = []
with open('rust_4007_munsell_only.txt', 'r') as f:
    for line in f:
        rust_results.append(line.strip())

# Python results
python_results = []
with open('python_4007_correct.txt', 'r') as f:
    for line in f:
        python_results.append(line.strip())

print(f"Loaded {len(colors)} colors")
print(f"Loaded {len(rust_results)} Rust results")
print(f"Loaded {len(python_results)} Python results")

# Analyze differences
print("\nAnalyzing differences for all 4007 colors...")

exact_matches = 0
family_mismatches = []
hue_differences = []
value_differences = []
chroma_differences = []

# For 99th percentile tracking
all_differences = []

for i in range(len(colors)):
    r, g, b = colors[i]
    rust_result = rust_results[i] if i < len(rust_results) else None
    python_result = python_results[i] if i < len(python_results) else None
    reference = reference_notations[i]
    
    # Skip if any result is missing or error
    if not rust_result or not python_result or python_result.startswith("ERROR"):
        continue
    
    # Parse all three
    rust_p = parse_munsell(rust_result)
    python_p = parse_munsell(python_result)
    ref_p = parse_munsell(reference)
    
    if not rust_p or not python_p:
        continue
    
    # Check exact match between Rust and Python
    if rust_result == python_result:
        exact_matches += 1
    
    # Calculate differences between Rust and Python
    if rust_p['family'] != python_p['family']:
        family_mismatches.append({
            'rgb': [r, g, b],
            'rust_family': rust_p['family'],
            'python_family': python_p['family'],
            'reference_family': ref_p['family'] if ref_p else None,
            'rust_full': rust_result,
            'python_full': python_result,
            'reference_full': reference
        })
    else:
        # Hue difference (with wraparound)
        hue_diff = abs(rust_p['hue'] - python_p['hue'])
        if hue_diff > 5:
            hue_diff = 10 - hue_diff
        hue_differences.append(hue_diff)
    
    # Value difference
    value_diff = abs(rust_p['value'] - python_p['value'])
    value_differences.append(value_diff)
    
    # Chroma difference
    chroma_diff = abs(rust_p['chroma'] - python_p['chroma'])
    chroma_differences.append(chroma_diff)
    
    # Store complete record for percentile analysis
    all_differences.append({
        'rgb': [r, g, b],
        'hue_diff': hue_diff if rust_p['family'] == python_p['family'] else None,
        'value_diff': value_diff,
        'chroma_diff': chroma_diff,
        'rust': rust_result,
        'python': python_result,
        'reference': reference
    })

print(f"\nProcessed {len(all_differences)} valid comparisons")

# Calculate detailed percentiles
print("\n" + "=" * 80)
print("DETAILED PERCENTILE ANALYSIS (ALL 4007 COLORS)")
print("=" * 80)

def print_detailed_percentiles(data, name):
    """Print 50th, then every percentile from 90-100"""
    if not data:
        print(f"No data for {name}")
        return
    
    arr = np.array(data)
    print(f"\n{name} DIFFERENCES (n={len(data)}):")
    print("-" * 50)
    
    # 50th percentile
    print(f"  50th percentile: {np.percentile(arr, 50):.6f}")
    
    # Every percentile from 90 to 100
    for p in range(90, 101):
        val = np.percentile(arr, p)
        print(f"  {p}th percentile: {val:.6f}")
    
    print(f"\n  Mean: {np.mean(arr):.6f}")
    print(f"  Std Dev: {np.std(arr):.6f}")
    print(f"  Min: {np.min(arr):.6f}")
    print(f"  Max: {np.max(arr):.6f}")
    
    return arr

hue_arr = print_detailed_percentiles(hue_differences, "HUE")
value_arr = print_detailed_percentiles(value_differences, "VALUE")
chroma_arr = print_detailed_percentiles(chroma_differences, "CHROMA")

# Family mismatch analysis
print("\n" + "=" * 80)
print("FAMILY MISMATCH ANALYSIS")
print("=" * 80)

print(f"\nTotal family mismatches: {len(family_mismatches)}")

if family_mismatches:
    # Count mismatch types
    mismatch_types = defaultdict(int)
    for m in family_mismatches:
        key = f"{m['python_family']} → {m['rust_family']}"
        mismatch_types[key] += 1
    
    print("\nMismatch breakdown by type:")
    for mismatch_type, count in sorted(mismatch_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {mismatch_type}: {count} occurrences")
    
    print("\nFirst 10 family mismatches:")
    for i, m in enumerate(family_mismatches[:10]):
        print(f"\n{i+1}. RGB{m['rgb']}:")
        print(f"   Reference: {m['reference_full']} (family: {m['reference_family']})")
        print(f"   Python:    {m['python_full']} (family: {m['python_family']})")
        print(f"   Rust:      {m['rust_full']} (family: {m['rust_family']})")

# Save results for further analysis
print("\n" + "=" * 80)
print("SAVING DETAILED RESULTS")
print("=" * 80)

# Identify 99th percentile colors for each dimension
if hue_arr is not None:
    hue_99th_threshold = np.percentile(hue_arr, 99)
    hue_99th_colors = [d for d in all_differences if d['hue_diff'] is not None and d['hue_diff'] >= hue_99th_threshold]
    print(f"\nHue 99th percentile: {len(hue_99th_colors)} colors with diff >= {hue_99th_threshold:.6f}")

if value_arr is not None:
    value_99th_threshold = np.percentile(value_arr, 99)
    value_99th_colors = [d for d in all_differences if d['value_diff'] >= value_99th_threshold]
    print(f"Value 99th percentile: {len(value_99th_colors)} colors with diff >= {value_99th_threshold:.6f}")

if chroma_arr is not None:
    chroma_99th_threshold = np.percentile(chroma_arr, 99)
    chroma_99th_colors = [d for d in all_differences if d['chroma_diff'] >= chroma_99th_threshold]
    print(f"Chroma 99th percentile: {len(chroma_99th_colors)} colors with diff >= {chroma_99th_threshold:.6f}")

# Save 99th percentile colors to file for further analysis
with open('99th_percentile_colors.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Type', 'R', 'G', 'B', 'Difference', 'Reference', 'Python', 'Rust'])
    
    if hue_arr is not None:
        for d in hue_99th_colors[:20]:  # Top 20
            writer.writerow(['Hue', d['rgb'][0], d['rgb'][1], d['rgb'][2], 
                           d['hue_diff'], d['reference'], d['python'], d['rust']])
    
    if value_arr is not None:
        for d in value_99th_colors[:20]:  # Top 20
            writer.writerow(['Value', d['rgb'][0], d['rgb'][1], d['rgb'][2], 
                           d['value_diff'], d['reference'], d['python'], d['rust']])
    
    if chroma_arr is not None:
        for d in chroma_99th_colors[:20]:  # Top 20
            writer.writerow(['Chroma', d['rgb'][0], d['rgb'][1], d['rgb'][2], 
                           d['chroma_diff'], d['reference'], d['python'], d['rust']])
    
    for m in family_mismatches:
        writer.writerow(['Family', m['rgb'][0], m['rgb'][1], m['rgb'][2], 
                        f"{m['python_family']}→{m['rust_family']}", 
                        m['reference_full'], m['python_full'], m['rust_full']])

print("\nSaved 99th percentile colors and family mismatches to '99th_percentile_colors.csv'")

# Count Python errors
python_errors = [p for p in python_results if p.startswith("ERROR")]
print(f"\nPython errors: {len(python_errors)} out of 4007 colors")

if python_errors:
    # Categorize errors
    error_types = defaultdict(list)
    for i, error in enumerate(python_errors):
        # Extract error type
        if "does not exist" in error:
            error_types["specification does not exist"].append(i)
        elif "must be normalised" in error:
            error_types["value must be normalised"].append(i)
        elif "Maximum" in error and "iterations" in error:
            error_types["Maximum iterations reached"].append(i)
        elif "divide by zero" in error:
            error_types["divide by zero"].append(i)
        else:
            error_types["other"].append(i)
    
    print("\nPython error types:")
    for error_type, indices in error_types.items():
        print(f"  {error_type}: {len(indices)} occurrences")
        # Show first example
        if indices:
            first_idx = indices[0]
            print(f"    Example: RGB{colors[first_idx]} - {python_results[first_idx][:100]}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)