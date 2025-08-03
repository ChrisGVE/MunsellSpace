#!/usr/bin/env python3
"""
CORRECTED analysis of ALL 4007 colors - properly handling the comparisons.
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
print("CORRECTED COMPLETE 4007 COLOR ANALYSIS")
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

# Analyze differences between Rust and Python
print("\nAnalyzing Rust vs Python differences for all 4007 colors...")

exact_matches = 0
family_mismatches = []
hue_differences = []
value_differences = []
chroma_differences = []
valid_comparisons = 0
python_errors = 0

# For percentile tracking
all_differences = []

for i in range(len(colors)):
    r, g, b = colors[i]
    rust_result = rust_results[i] if i < len(rust_results) else None
    python_result = python_results[i] if i < len(python_results) else None
    reference = reference_notations[i]
    
    # Count Python errors
    if python_result and python_result.startswith("ERROR"):
        python_errors += 1
        continue
    
    # Skip if any result is missing
    if not rust_result or not python_result:
        continue
    
    # Parse both
    rust_p = parse_munsell(rust_result)
    python_p = parse_munsell(python_result)
    
    if not rust_p or not python_p:
        continue
    
    valid_comparisons += 1
    
    # Check exact match
    if rust_result == python_result:
        exact_matches += 1
    
    # Calculate differences
    if rust_p['family'] != python_p['family']:
        family_mismatches.append({
            'rgb': [r, g, b],
            'rust_family': rust_p['family'],
            'python_family': python_p['family'],
            'rust_full': rust_result,
            'python_full': python_result,
            'reference': reference
        })
    else:
        # Only calculate hue difference if families match
        hue_diff = abs(rust_p['hue'] - python_p['hue'])
        if hue_diff > 5:
            hue_diff = 10 - hue_diff
        hue_differences.append(hue_diff)
    
    # Always calculate value and chroma differences
    value_diff = abs(rust_p['value'] - python_p['value'])
    value_differences.append(value_diff)
    
    chroma_diff = abs(rust_p['chroma'] - python_p['chroma'])
    chroma_differences.append(chroma_diff)
    
    # Store for detailed analysis
    all_differences.append({
        'rgb': [r, g, b],
        'family_match': rust_p['family'] == python_p['family'],
        'hue_diff': hue_diff if rust_p['family'] == python_p['family'] else None,
        'value_diff': value_diff,
        'chroma_diff': chroma_diff,
        'rust': rust_result,
        'python': python_result,
        'reference': reference
    })

print(f"\nValid comparisons: {valid_comparisons}")
print(f"Python errors: {python_errors}")
print(f"Exact matches: {exact_matches} ({100*exact_matches/valid_comparisons:.2f}%)")
print(f"Family mismatches: {len(family_mismatches)} ({100*len(family_mismatches)/valid_comparisons:.2f}%)")

# Detailed percentile analysis
print("\n" + "=" * 80)
print("DETAILED PERCENTILE ANALYSIS (ALL 4007 COLORS)")
print("=" * 80)

def print_detailed_percentiles(data, name):
    """Print 50th, then every percentile from 90-100"""
    if not data:
        print(f"\nNo data for {name}")
        return None
    
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

hue_arr = print_detailed_percentiles(hue_differences, "HUE (excluding family mismatches)")
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
    
    print("\nMismatch breakdown by type (showing top 20):")
    sorted_mismatches = sorted(mismatch_types.items(), key=lambda x: x[1], reverse=True)
    for mismatch_type, count in sorted_mismatches[:20]:
        print(f"  {mismatch_type}: {count} occurrences")
    
    print("\nFirst 5 family mismatches with details:")
    for i, m in enumerate(family_mismatches[:5]):
        print(f"\n{i+1}. RGB{m['rgb']}:")
        print(f"   Reference: {m['reference']}")
        print(f"   Python:    {m['python_full']}")
        print(f"   Rust:      {m['rust_full']}")

# Identify 99th percentile colors
print("\n" + "=" * 80)
print("99TH PERCENTILE WORST CASES")
print("=" * 80)

# Get thresholds
hue_99th_threshold = np.percentile(hue_arr, 99) if hue_arr is not None else None
value_99th_threshold = np.percentile(value_arr, 99) if value_arr is not None else None
chroma_99th_threshold = np.percentile(chroma_arr, 99) if chroma_arr is not None else None

# Collect 99th percentile colors
hue_99th_colors = []
value_99th_colors = []
chroma_99th_colors = []

for d in all_differences:
    if hue_99th_threshold and d['hue_diff'] is not None and d['hue_diff'] >= hue_99th_threshold:
        hue_99th_colors.append(d)
    if value_99th_threshold and d['value_diff'] >= value_99th_threshold:
        value_99th_colors.append(d)
    if chroma_99th_threshold and d['chroma_diff'] >= chroma_99th_threshold:
        chroma_99th_colors.append(d)

print(f"\nHue 99th percentile (>={hue_99th_threshold:.6f}): {len(hue_99th_colors)} colors")
print(f"Value 99th percentile (>={value_99th_threshold:.6f}): {len(value_99th_colors)} colors")
print(f"Chroma 99th percentile (>={chroma_99th_threshold:.6f}): {len(chroma_99th_colors)} colors")

# Save detailed results
with open('99th_percentile_detailed.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Type', 'R', 'G', 'B', 'Difference', 'Reference', 'Python', 'Rust'])
    
    # Hue worst cases
    for d in sorted(hue_99th_colors, key=lambda x: x['hue_diff'], reverse=True)[:20]:
        writer.writerow(['Hue', d['rgb'][0], d['rgb'][1], d['rgb'][2], 
                       d['hue_diff'], d['reference'], d['python'], d['rust']])
    
    # Value worst cases
    for d in sorted(value_99th_colors, key=lambda x: x['value_diff'], reverse=True)[:20]:
        writer.writerow(['Value', d['rgb'][0], d['rgb'][1], d['rgb'][2], 
                       d['value_diff'], d['reference'], d['python'], d['rust']])
    
    # Chroma worst cases
    for d in sorted(chroma_99th_colors, key=lambda x: x['chroma_diff'], reverse=True)[:20]:
        writer.writerow(['Chroma', d['rgb'][0], d['rgb'][1], d['rgb'][2], 
                       d['chroma_diff'], d['reference'], d['python'], d['rust']])
    
    # Family mismatches
    for m in family_mismatches[:20]:
        writer.writerow(['Family', m['rgb'][0], m['rgb'][1], m['rgb'][2], 
                        f"{m['python_family']}→{m['rust_family']}", 
                        m['reference'], m['python_full'], m['rust_full']])

print("\nSaved detailed results to '99th_percentile_detailed.csv'")

# Python error analysis
print("\n" + "=" * 80)
print("PYTHON ERROR ANALYSIS")
print("=" * 80)

error_types = defaultdict(list)
for i, result in enumerate(python_results):
    if result.startswith("ERROR"):
        error_msg = result[7:]  # Skip "ERROR: "
        
        if "value must be normalised" in error_msg:
            error_types["value_normalisation"].append((i, colors[i], error_msg))
        elif "does not exist" in error_msg:
            error_types["specification_not_found"].append((i, colors[i], error_msg))
        elif "iterations" in error_msg:
            error_types["convergence_failure"].append((i, colors[i], error_msg))
        elif "chroma must be normalised" in error_msg:
            error_types["chroma_normalisation"].append((i, colors[i], error_msg))
        else:
            error_types["other"].append((i, colors[i], error_msg))

print(f"\nTotal Python errors: {python_errors}")
for error_type, cases in error_types.items():
    print(f"\n{error_type}: {len(cases)} occurrences")
    if cases:
        idx, rgb, msg = cases[0]
        print(f"  Example: RGB{rgb}")
        print(f"  Message: {msg[:100]}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)