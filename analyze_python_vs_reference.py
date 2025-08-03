#!/usr/bin/env python3
"""
Analyze Python results vs Reference dataset to check:
1. Does Python make family mismatches against reference?
2. What are the percentile differences for Python vs Reference?
"""

import csv
import numpy as np
from collections import defaultdict

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A" or notation.startswith("ERROR"):
        return None
        
    # Clean up notation
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

print("=" * 80)
print("PYTHON vs REFERENCE ANALYSIS")
print("Checking Python library accuracy against ground truth")
print("=" * 80)

# Load all data
print("\nLoading data...")

# Reference colors and notations
colors = []
reference_notations = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        colors.append([int(row['R']), int(row['G']), int(row['B'])])
        reference_notations.append(row['Munsell Colour'])

# Python results
python_results = []
with open('python_complete_4007.txt', 'r') as f:
    for line in f:
        python_results.append(line.strip())

print(f"Loaded {len(colors)} reference colors")
print(f"Loaded {len(python_results)} Python results")

# Categorize results
exact_matches = 0
family_mismatches = []
hue_differences = []  # Only when families match
value_differences = []  # All valid comparisons
chroma_differences = []  # All valid comparisons
python_errors = []
valid_comparisons = 0

# Store all results for detailed analysis
all_results = []

for i in range(len(colors)):
    r, g, b = colors[i]
    python_result = python_results[i] if i < len(python_results) else None
    reference = reference_notations[i]
    
    # Check for Python errors
    if python_result and python_result.startswith("ERROR"):
        python_errors.append({
            'index': i,
            'rgb': [r, g, b],
            'error': python_result,
            'reference': reference
        })
        continue
    
    # Skip if missing results
    if not python_result:
        continue
    
    # Parse results
    python_p = parse_munsell(python_result)
    ref_p = parse_munsell(reference)
    
    if not python_p or not ref_p:
        continue
    
    valid_comparisons += 1
    
    # Check exact match
    if python_result == reference:
        exact_matches += 1
    
    # Store complete result
    result = {
        'index': i,
        'rgb': [r, g, b],
        'reference': reference,
        'python': python_result,
        'python_parsed': python_p,
        'ref_parsed': ref_p
    }
    
    # HIERARCHY: Family is most important
    if python_p['family'] != ref_p['family']:
        family_mismatches.append(result)
        # Don't calculate hue difference when families don't match
        result['hue_diff'] = None
    else:
        # Calculate hue difference only when families match
        hue_diff = abs(python_p['hue'] - ref_p['hue'])
        if hue_diff > 5:  # Handle wraparound
            hue_diff = 10 - hue_diff
        hue_differences.append(hue_diff)
        result['hue_diff'] = hue_diff
    
    # Always calculate value and chroma differences
    value_diff = abs(python_p['value'] - ref_p['value'])
    chroma_diff = abs(python_p['chroma'] - ref_p['chroma'])
    
    value_differences.append(value_diff)
    chroma_differences.append(chroma_diff)
    
    result['value_diff'] = value_diff
    result['chroma_diff'] = chroma_diff
    
    all_results.append(result)

print(f"\n{valid_comparisons} valid comparisons out of {len(colors)} colors")
print(f"Python errors: {len(python_errors)}")

# Basic statistics
print("\n" + "=" * 80)
print("BASIC STATISTICS - PYTHON vs REFERENCE")
print("=" * 80)

print(f"\nExact matches: {exact_matches} ({100*exact_matches/valid_comparisons:.2f}%)")
print(f"Family mismatches: {len(family_mismatches)} ({100*len(family_mismatches)/valid_comparisons:.2f}%)")
print(f"Family matches: {valid_comparisons - len(family_mismatches)} ({100*(valid_comparisons - len(family_mismatches))/valid_comparisons:.2f}%)")

# Detailed percentile analysis
print("\n" + "=" * 80)
print("PERCENTILE ANALYSIS - PYTHON vs REFERENCE")
print("=" * 80)

def analyze_percentiles(data, name):
    """Analyze percentiles with focus on 90-100 range"""
    if not data:
        print(f"\n{name}: No data")
        return None
    
    arr = np.array(data)
    print(f"\n{name} (n={len(data)}):")
    print("-" * 50)
    
    # 50th percentile
    print(f"  50th percentile: {np.percentile(arr, 50):.6f}")
    
    # Every percentile from 90 to 100
    print("\n  90-100th percentiles:")
    for p in range(90, 101):
        val = np.percentile(arr, p)
        print(f"    {p:3d}th: {val:.6f}")
    
    # Statistics
    print(f"\n  Mean: {np.mean(arr):.6f}")
    print(f"  Std Dev: {np.std(arr):.6f}")
    print(f"  Min: {np.min(arr):.6f}")
    print(f"  Max: {np.max(arr):.6f}")
    
    return arr

# Analyze each dimension
hue_arr = analyze_percentiles(hue_differences, "HUE DIFFERENCES (families match)")
value_arr = analyze_percentiles(value_differences, "VALUE DIFFERENCES")
chroma_arr = analyze_percentiles(chroma_differences, "CHROMA DIFFERENCES")

# Family mismatch analysis
print("\n" + "=" * 80)
print("FAMILY MISMATCH ANALYSIS - PYTHON vs REFERENCE")
print("=" * 80)

if family_mismatches:
    # Count mismatch types
    mismatch_types = defaultdict(int)
    for m in family_mismatches:
        key = f"{m['ref_parsed']['family']} → {m['python_parsed']['family']}"
        mismatch_types[key] += 1
    
    print(f"\nTotal family mismatches: {len(family_mismatches)}")
    print("\nMismatch patterns (Reference → Python):")
    sorted_types = sorted(mismatch_types.items(), key=lambda x: x[1], reverse=True)
    for pattern, count in sorted_types:
        print(f"  {pattern}: {count} occurrences")
    
    # Show some examples
    print("\nFirst 10 family mismatch examples:")
    for i, m in enumerate(family_mismatches[:10]):
        print(f"  {i+1}. RGB{m['rgb']}")
        print(f"     Reference: {m['reference']}")
        print(f"     Python:    {m['python']}")
else:
    print("\nNO FAMILY MISMATCHES! Python perfectly matches reference families.")

# Python error analysis
print("\n" + "=" * 80)
print("PYTHON ERROR DETAILS")
print("=" * 80)

error_types = defaultdict(list)
for err in python_errors:
    error_msg = err['error']
    if "value must be normalised" in error_msg:
        error_types["value_normalisation"].append(err)
    elif "chroma must be normalised" in error_msg:
        error_types["chroma_normalisation"].append(err)
    elif "does not exist" in error_msg:
        error_types["specification_not_found"].append(err)
    elif "convergence" in error_msg:
        error_types["convergence_failure"].append(err)
    else:
        error_types["other"].append(err)

print(f"\nTotal Python errors: {len(python_errors)}")
for error_type, cases in error_types.items():
    print(f"\n{error_type}: {len(cases)} occurrences")
    if cases and len(cases) <= 3:
        # Show all if few
        for case in cases:
            print(f"  RGB{case['rgb']}: {case['reference']}")

# Compare with Rust vs Python analysis
print("\n" + "=" * 80)
print("COMPARISON: Python vs Reference AND Rust vs Python")
print("=" * 80)

print("\nPython vs Reference:")
print(f"  Exact matches: {exact_matches}/{valid_comparisons} ({100*exact_matches/valid_comparisons:.2f}%)")
print(f"  Family mismatches: {len(family_mismatches)}/{valid_comparisons} ({100*len(family_mismatches)/valid_comparisons:.2f}%)")

print("\nRust vs Python (from previous analysis):")
print(f"  Exact matches: 2389/3911 (61.08%)")
print(f"  Family mismatches: 17/3911 (0.43%)")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)