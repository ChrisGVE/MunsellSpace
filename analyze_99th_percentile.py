#!/usr/bin/env python3
"""
Detailed analysis of 99th percentile worst cases.
Compare Python vs Reference vs Rust for each color.
"""

import csv
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess

# Load the 99th percentile colors from the CSV
worst_cases = []
with open('99th_percentile_detailed.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        worst_cases.append({
            'type': row['Type'],
            'rgb': [int(row['R']), int(row['G']), int(row['B'])],
            'difference': float(row['Difference']) if row['Difference'] and not '→' in row['Difference'] else row['Difference'],
            'reference': row['Reference'],
            'python_saved': row['Python'],
            'rust_saved': row['Rust']
        })

print("=" * 80)
print("DETAILED 99TH PERCENTILE WORST CASE ANALYSIS")
print("=" * 80)

# Group by type
by_type = {}
for case in worst_cases:
    if case['type'] not in by_type:
        by_type[case['type']] = []
    by_type[case['type']].append(case)

# Analyze each type
for case_type in ['Hue', 'Value', 'Chroma', 'Family']:
    if case_type not in by_type:
        continue
    
    cases = by_type[case_type]
    print(f"\n{'='*80}")
    print(f"{case_type.upper()} WORST CASES: {len(cases)} colors")
    print("="*80)
    
    # Analyze first 10 cases of each type
    for i, case in enumerate(cases[:10]):
        rgb = case['rgb']
        print(f"\n{i+1}. RGB{rgb} - Difference: {case['difference']}")
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
            python_error = str(e)
        
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
            if line and not line.startswith('TRACE') and not line.startswith('Looking') and not line.startswith('EXACT'):
                if line and (line[0].isdigit() or line.startswith('N ')):
                    rust_fresh = line
                    break
        
        # Display all results
        print(f"Reference (CSV):     {case['reference']}")
        print(f"Python (saved):      {case['python_saved']}")
        if python_fresh:
            print(f"Python (fresh calc): {python_fresh}")
            if python_fresh != case['python_saved']:
                print("  ⚠️  Python fresh differs from saved!")
        else:
            print(f"Python (fresh calc): ERROR - {python_error[:80]}")
        
        print(f"Rust (saved):        {case['rust_saved']}")
        if rust_fresh:
            print(f"Rust (fresh calc):   {rust_fresh}")
            if rust_fresh != case['rust_saved']:
                print("  ⚠️  Rust fresh differs from saved!")
        
        # Comparisons
        print("\nComparisons:")
        
        # Compare with reference
        if python_fresh == case['reference']:
            print("  Python = Reference ✅")
        elif python_fresh:
            print("  Python ≠ Reference")
        
        if rust_fresh == case['reference']:
            print("  Rust = Reference ✅")
        else:
            print("  Rust ≠ Reference")
        
        if python_fresh and rust_fresh:
            if python_fresh == rust_fresh:
                print("  Python = Rust ✅")
            else:
                print("  Python ≠ Rust")

# Summary statistics
print("\n" + "=" * 80)
print("SUMMARY OF 99TH PERCENTILE COLORS")
print("=" * 80)

total_analyzed = min(10, len(by_type.get('Hue', []))) + \
                 min(10, len(by_type.get('Value', []))) + \
                 min(10, len(by_type.get('Chroma', []))) + \
                 min(10, len(by_type.get('Family', [])))

print(f"\nTotal colors analyzed: {total_analyzed}")
print(f"  Hue worst cases: {min(10, len(by_type.get('Hue', [])))}")
print(f"  Value worst cases: {min(10, len(by_type.get('Value', [])))}")
print(f"  Chroma worst cases: {min(10, len(by_type.get('Chroma', [])))}")
print(f"  Family mismatches: {min(10, len(by_type.get('Family', [])))}")

print("\n" + "=" * 80)