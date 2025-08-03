#!/usr/bin/env python3
"""
Comprehensive analysis of ALL 4007 colors with proper hierarchy:
Family errors > Hue (when family correct) > Chroma > Value
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
print("COMPREHENSIVE 4007 COLOR ANALYSIS - RUST vs PYTHON")
print("Hierarchy: Family > Hue > Chroma > Value")
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

# Rust results
rust_results = []
with open('rust_complete_4007.txt', 'r') as f:
    for line in f:
        rust_results.append(line.strip())

# Python results
python_results = []
with open('python_complete_4007.txt', 'r') as f:
    for line in f:
        python_results.append(line.strip())

print(f"Loaded {len(colors)} colors")
print(f"Loaded {len(rust_results)} Rust results")
print(f"Loaded {len(python_results)} Python results")

# Categorize results
exact_matches = 0
family_mismatches = []
hue_differences = []  # Only when families match
value_differences = []  # All valid comparisons
chroma_differences = []  # All valid comparisons
python_errors = []
valid_comparisons = 0

# Store all results for percentile analysis
all_results = []

for i in range(len(colors)):
    r, g, b = colors[i]
    rust_result = rust_results[i] if i < len(rust_results) else None
    python_result = python_results[i] if i < len(python_results) else None
    reference = reference_notations[i]
    
    # Check for Python errors
    if python_result and python_result.startswith("ERROR"):
        python_errors.append({
            'index': i,
            'rgb': [r, g, b],
            'error': python_result,
            'reference': reference,
            'rust': rust_result
        })
        continue
    
    # Skip if missing results
    if not rust_result or not python_result:
        continue
    
    # Parse results
    rust_p = parse_munsell(rust_result)
    python_p = parse_munsell(python_result)
    ref_p = parse_munsell(reference)
    
    if not rust_p or not python_p:
        continue
    
    valid_comparisons += 1
    
    # Check exact match
    if rust_result == python_result:
        exact_matches += 1
    
    # Store complete result
    result = {
        'index': i,
        'rgb': [r, g, b],
        'reference': reference,
        'rust': rust_result,
        'python': python_result,
        'rust_parsed': rust_p,
        'python_parsed': python_p,
        'ref_parsed': ref_p
    }
    
    # HIERARCHY: Family is most important
    if rust_p['family'] != python_p['family']:
        family_mismatches.append(result)
        # Don't calculate hue difference when families don't match
        result['hue_diff'] = None
    else:
        # Calculate hue difference only when families match
        hue_diff = abs(rust_p['hue'] - python_p['hue'])
        if hue_diff > 5:  # Handle wraparound
            hue_diff = 10 - hue_diff
        hue_differences.append(hue_diff)
        result['hue_diff'] = hue_diff
    
    # Always calculate value and chroma differences
    value_diff = abs(rust_p['value'] - python_p['value'])
    chroma_diff = abs(rust_p['chroma'] - python_p['chroma'])
    
    value_differences.append(value_diff)
    chroma_differences.append(chroma_diff)
    
    result['value_diff'] = value_diff
    result['chroma_diff'] = chroma_diff
    
    all_results.append(result)

print(f"\n{valid_comparisons} valid comparisons out of {len(colors)} colors")
print(f"Python errors: {len(python_errors)}")

# Basic statistics
print("\n" + "=" * 80)
print("BASIC STATISTICS")
print("=" * 80)

print(f"\nExact matches: {exact_matches} ({100*exact_matches/valid_comparisons:.2f}%)")
print(f"Family mismatches: {len(family_mismatches)} ({100*len(family_mismatches)/valid_comparisons:.2f}%)")
print(f"Family matches: {valid_comparisons - len(family_mismatches)} ({100*(valid_comparisons - len(family_mismatches))/valid_comparisons:.2f}%)")

# Detailed percentile analysis
print("\n" + "=" * 80)
print("PERCENTILE ANALYSIS")
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
print("FAMILY MISMATCH ANALYSIS")
print("=" * 80)

if family_mismatches:
    # Count mismatch types
    mismatch_types = defaultdict(int)
    for m in family_mismatches:
        key = f"{m['python_parsed']['family']} → {m['rust_parsed']['family']}"
        mismatch_types[key] += 1
    
    print(f"\nTotal family mismatches: {len(family_mismatches)}")
    print("\nTop 20 mismatch patterns:")
    sorted_types = sorted(mismatch_types.items(), key=lambda x: x[1], reverse=True)
    for pattern, count in sorted_types[:20]:
        print(f"  {pattern}: {count} occurrences")

# Collect worst 1% for each dimension
print("\n" + "=" * 80)
print("WORST 1% ANALYSIS")
print("=" * 80)

# Calculate 99th percentile thresholds (top 1%)
hue_99th = np.percentile(hue_arr, 99) if hue_arr is not None else None
value_99th = np.percentile(value_arr, 99) if value_arr is not None else None
chroma_99th = np.percentile(chroma_arr, 99) if chroma_arr is not None else None

# Collect worst cases
worst_hue = []
worst_value = []
worst_chroma = []

for result in all_results:
    # Hue worst cases (only when families match)
    if result.get('hue_diff') is not None and hue_99th and result['hue_diff'] >= hue_99th:
        worst_hue.append(result)
    
    # Value worst cases
    if value_99th and result['value_diff'] >= value_99th:
        worst_value.append(result)
    
    # Chroma worst cases
    if chroma_99th and result['chroma_diff'] >= chroma_99th:
        worst_chroma.append(result)

print(f"\nWorst 1% (≥99th percentile):")
print(f"  Family mismatches: {len(family_mismatches)} colors")
print(f"  Hue (≥{hue_99th:.6f}): {len(worst_hue)} colors")
print(f"  Value (≥{value_99th:.6f}): {len(worst_value)} colors")
print(f"  Chroma (≥{chroma_99th:.6f}): {len(worst_chroma)} colors")

# Save worst cases to CSV
with open('worst_1_percent.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Category', 'R', 'G', 'B', 'Difference', 'Reference', 'Python', 'Rust'])
    
    # Family mismatches (all of them are worst)
    for m in family_mismatches[:50]:  # Limit to 50 for practicality
        family_diff = f"{m['python_parsed']['family']}→{m['rust_parsed']['family']}"
        writer.writerow(['FamilyMismatch', m['rgb'][0], m['rgb'][1], m['rgb'][2],
                        family_diff, m['reference'], m['python'], m['rust']])
    
    # Hue worst 1%
    for h in sorted(worst_hue, key=lambda x: x['hue_diff'], reverse=True)[:20]:
        writer.writerow(['Hue', h['rgb'][0], h['rgb'][1], h['rgb'][2],
                        h['hue_diff'], h['reference'], h['python'], h['rust']])
    
    # Value worst 1%
    for v in sorted(worst_value, key=lambda x: x['value_diff'], reverse=True)[:20]:
        writer.writerow(['Value', v['rgb'][0], v['rgb'][1], v['rgb'][2],
                        v['value_diff'], v['reference'], v['python'], v['rust']])
    
    # Chroma worst 1%
    for c in sorted(worst_chroma, key=lambda x: x['chroma_diff'], reverse=True)[:20]:
        writer.writerow(['Chroma', c['rgb'][0], c['rgb'][1], c['rgb'][2],
                        c['chroma_diff'], c['reference'], c['python'], c['rust']])

print(f"\nWorst cases saved to 'worst_1_percent.csv'")

# Python error analysis
print("\n" + "=" * 80)
print("PYTHON ERROR ANALYSIS")
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
    if cases:
        example = cases[0]
        print(f"  Example: RGB{example['rgb']}")
        print(f"  Error: {example['error'][:100]}...")
        print(f"  Reference: {example['reference']}")
        print(f"  Rust: {example['rust']}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)