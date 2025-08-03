#!/usr/bin/env python3
"""
Analyze worst 1% cases by running them through Python individually
and comparing with Rust and reference.
"""

import csv
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess
import warnings

warnings.filterwarnings('ignore')

# Load worst cases from CSV
worst_cases = []
with open('worst_1_percent.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        worst_cases.append({
            'category': row['Category'],
            'rgb': [int(row['R']), int(row['G']), int(row['B'])],
            'difference': row['Difference'],
            'reference': row['Reference'],
            'python_saved': row['Python'],
            'rust_saved': row['Rust']
        })

print("=" * 80)
print("WORST 1% DETAILED ANALYSIS")
print("=" * 80)

# Group by category
categories = {}
for case in worst_cases:
    cat = case['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(case)

# Statistics tracking
comparison_stats = {
    'python_matches_reference': 0,
    'rust_matches_reference': 0,
    'python_matches_rust': 0,
    'total_tested': 0
}

# Analyze each category
for category in ['FamilyMismatch', 'Hue', 'Value', 'Chroma']:
    if category not in categories:
        continue
    
    cases = categories[category]
    print(f"\n{'='*80}")
    print(f"{category.upper()}: {len(cases)} cases")
    print("="*80)
    
    # Analyze first 10 of each category
    for i, case in enumerate(cases[:10]):
        rgb = case['rgb']
        print(f"\n{i+1}. RGB{rgb}")
        print(f"   Difference: {case['difference']}")
        print("-" * 60)
        
        # Fresh Python calculation
        python_fresh = None
        python_error = None
        try:
            rgb_norm = [c/255.0 for c in rgb]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            python_fresh = xyY_to_munsell_colour(xyY)
        except Exception as e:
            python_error = str(e)[:100]
        
        # Fresh Rust calculation
        input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
        result = subprocess.run(
            ['./target/release/batch_convert'],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        rust_fresh = None
        for line in result.stdout.split('\n'):
            if line and not line.startswith('TRACE') and not line.startswith('Looking'):
                if line and (line[0].isdigit() or line.startswith('N ')):
                    rust_fresh = line
                    break
        
        # Display results
        print(f"   Reference:     {case['reference']}")
        print(f"   Python saved:  {case['python_saved']}")
        if python_fresh:
            print(f"   Python fresh:  {python_fresh}")
        else:
            print(f"   Python fresh:  ERROR - {python_error}")
        print(f"   Rust saved:    {case['rust_saved']}")
        if rust_fresh:
            print(f"   Rust fresh:    {rust_fresh}")
        
        # Comparisons
        comparisons = []
        comparison_stats['total_tested'] += 1
        
        if python_fresh == case['reference']:
            comparisons.append("Python=Reference")
            comparison_stats['python_matches_reference'] += 1
        
        if rust_fresh == case['reference']:
            comparisons.append("Rust=Reference")
            comparison_stats['rust_matches_reference'] += 1
        
        if python_fresh and rust_fresh and python_fresh == rust_fresh:
            comparisons.append("Python=Rust")
            comparison_stats['python_matches_rust'] += 1
        
        if comparisons:
            print(f"   Matches: {', '.join(comparisons)}")
        else:
            print(f"   Matches: None (all different)")

# Summary statistics
print("\n" + "=" * 80)
print("COMPARISON STATISTICS")
print("=" * 80)

total = comparison_stats['total_tested']
if total > 0:
    print(f"\nTotal colors tested: {total}")
    print(f"Python matches reference: {comparison_stats['python_matches_reference']}/{total} ({100*comparison_stats['python_matches_reference']/total:.1f}%)")
    print(f"Rust matches reference:   {comparison_stats['rust_matches_reference']}/{total} ({100*comparison_stats['rust_matches_reference']/total:.1f}%)")
    print(f"Python matches Rust:      {comparison_stats['python_matches_rust']}/{total} ({100*comparison_stats['python_matches_rust']/total:.1f}%)")

# Detailed comparison for family mismatches
print("\n" + "=" * 80)
print("FAMILY MISMATCH DETAILS")
print("=" * 80)

if 'FamilyMismatch' in categories:
    family_cases = categories['FamilyMismatch']
    print(f"\nAnalyzing all {len(family_cases)} family mismatches:")
    
    mismatch_patterns = {}
    for case in family_cases:
        rgb = case['rgb']
        
        # Get fresh calculations
        try:
            rgb_norm = [c/255.0 for c in rgb]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            python_fresh = xyY_to_munsell_colour(xyY)
        except:
            python_fresh = "ERROR"
        
        # Pattern analysis
        pattern = case['difference']
        if pattern not in mismatch_patterns:
            mismatch_patterns[pattern] = []
        mismatch_patterns[pattern].append({
            'rgb': rgb,
            'reference': case['reference'],
            'python': python_fresh,
            'rust': case['rust_saved']
        })
    
    print("\nMismatch patterns:")
    for pattern, examples in mismatch_patterns.items():
        print(f"\n{pattern}: {len(examples)} occurrences")
        # Show first example
        ex = examples[0]
        print(f"  Example: RGB{ex['rgb']}")
        print(f"    Reference: {ex['reference']}")
        print(f"    Python:    {ex['python']}")
        print(f"    Rust:      {ex['rust']}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)