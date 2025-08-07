#!/usr/bin/env python3
"""
Enhanced backtesting agent for Munsell conversion accuracy with detailed diagnostics.
Outputs both a summary report and detailed lists of problematic colors.
"""

import csv
import subprocess
import numpy as np
from datetime import datetime
import os
import sys

def parse_munsell_string(munsell_str):
    """Parse a Munsell string into components."""
    if not munsell_str or munsell_str == 'N 0':
        return 0.0, 0.0, 0.0, 'N'
    
    # Handle achromatic colors (e.g., "N 5")
    if munsell_str.startswith('N '):
        value = float(munsell_str[2:])
        return 0.0, value, 0.0, 'N'
    
    # Parse chromatic colors (e.g., "7.5PB 3.5/12.2")
    try:
        parts = munsell_str.split(' ')
        if len(parts) != 2:
            return 0.0, 0.0, 0.0, 'Unknown'
        
        hue_part = parts[0]
        value_chroma = parts[1].split('/')
        
        if len(value_chroma) != 2:
            return 0.0, 0.0, 0.0, 'Unknown'
        
        # Extract hue number and family
        for i, char in enumerate(hue_part):
            if char.isalpha():
                hue = float(hue_part[:i])
                family = hue_part[i:]
                break
        else:
            hue = 0.0
            family = 'Unknown'
        
        value = float(value_chroma[0])
        chroma = float(value_chroma[1])
        
        return hue, value, chroma, family
    except:
        return 0.0, 0.0, 0.0, 'Unknown'

def circular_hue_diff(h1, h2, c1, c2):
    """Calculate circular hue difference, accounting for achromatic colors."""
    # If either color is achromatic (chroma = 0), hue difference is 0
    if c1 == 0 or c2 == 0:
        return 0.0
    
    # Calculate minimum distance on circular scale (0-10)
    direct_diff = abs(h1 - h2)
    wraparound_diff = 10.0 - direct_diff
    return min(direct_diff, wraparound_diff)

def run_rust_conversion(r, g, b):
    """Run Rust conversion for a single RGB color."""
    try:
        result = subprocess.run(
            ['cargo', 'run', '--release', '--bin', 'test_rgb_cli', '--', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=2,
            cwd='/Users/chris/Dropbox/dev/projects/libraries/MunsellSpace'
        )
        
        # Parse output - look for "Munsell: " line
        for line in result.stdout.split('\n'):
            if line.startswith('Munsell: '):
                return line.replace('Munsell: ', '').strip()
        
        # Also check stderr
        for line in result.stderr.split('\n'):
            if line.startswith('Munsell: '):
                return line.replace('Munsell: ', '').strip()
        
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"Error running Rust conversion: {e}", file=sys.stderr)
        return None

def main():
    csv_path = 'tests/data/srgb-to-munsell.csv'
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return
    
    # Read the CSV file
    colors = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            colors.append({
                'r': int(row['R']),
                'g': int(row['G']),
                'b': int(row['B']),
                'python': row['Munsell Colour']
            })
    
    print(f"Testing {len(colors)} colors...")
    
    # Process colors
    results = []
    family_mismatches = []
    problematic_colors = []
    
    for i, color in enumerate(colors):
        if i % 100 == 0:
            print(f"Processing color {i}/{len(colors)}...")
        
        rust_munsell = run_rust_conversion(color['r'], color['g'], color['b'])
        
        if rust_munsell is None:
            continue
        
        # Parse both Munsell notations
        py_hue, py_value, py_chroma, py_family = parse_munsell_string(color['python'])
        rust_hue, rust_value, rust_chroma, rust_family = parse_munsell_string(rust_munsell)
        
        # Calculate differences
        hue_diff = circular_hue_diff(py_hue, rust_hue, py_chroma, rust_chroma)
        value_diff = abs(py_value - rust_value)
        chroma_diff = abs(py_chroma - rust_chroma)
        total_diff = hue_diff + value_diff + chroma_diff
        
        # Check if within tolerance
        within_tolerance = (hue_diff <= 0.1 and value_diff <= 0.1 and chroma_diff <= 0.1)
        
        # Check family mismatch
        family_match = (py_family == rust_family)
        if not family_match:
            family_mismatches.append({
                'hex': f"#{color['r']:02x}{color['g']:02x}{color['b']:02x}",
                'rgb': (color['r'], color['g'], color['b']),
                'python': color['python'],
                'rust': rust_munsell,
                'py_family': py_family,
                'rust_family': rust_family
            })
        
        # Store result
        result = {
            'hex': f"#{color['r']:02x}{color['g']:02x}{color['b']:02x}",
            'rgb': (color['r'], color['g'], color['b']),
            'python': color['python'],
            'rust': rust_munsell,
            'py_hue': py_hue,
            'py_value': py_value,
            'py_chroma': py_chroma,
            'py_family': py_family,
            'rust_hue': rust_hue,
            'rust_value': rust_value,
            'rust_chroma': rust_chroma,
            'rust_family': rust_family,
            'hue_diff': hue_diff,
            'value_diff': value_diff,
            'chroma_diff': chroma_diff,
            'total_diff': total_diff,
            'within_tolerance': within_tolerance,
            'family_match': family_match
        }
        results.append(result)
        
        # Track problematic colors
        if not within_tolerance:
            problematic_colors.append(result)
    
    # Sort problematic colors by total difference
    problematic_colors.sort(key=lambda x: x['total_diff'], reverse=True)
    
    # Calculate statistics
    total_tested = len(results)
    within_tolerance_count = sum(1 for r in results if r['within_tolerance'])
    accuracy = within_tolerance_count / total_tested * 100 if total_tested > 0 else 0
    
    hue_diffs = [r['hue_diff'] for r in results]
    value_diffs = [r['value_diff'] for r in results]
    chroma_diffs = [r['chroma_diff'] for r in results]
    
    # Write detailed diagnostics file
    with open('BACKTESTING_DETAILS.md', 'w') as f:
        f.write('# Munsell Conversion Backtesting - Detailed Diagnostics\n\n')
        f.write(f'**Generated**: {datetime.now().isoformat()}\n')
        f.write(f'**Total Colors Tested**: {total_tested}\n')
        f.write(f'**Overall Accuracy**: {accuracy:.2f}% ({within_tolerance_count}/{total_tested} within 0.1 tolerance)\n\n')
        
        # Family mismatches section
        f.write('## Family Mismatches (Wrong Hue Family Assignment)\n\n')
        f.write(f'**Total**: {len(family_mismatches)} colors\n\n')
        if family_mismatches:
            f.write('| Hex | RGB | Python | Rust | Transition |\n')
            f.write('|-----|-----|--------|------|-----------|\n')
            for fm in family_mismatches:
                f.write(f"| {fm['hex']} | {fm['rgb']} | {fm['python']} | {fm['rust']} | {fm['py_family']}→{fm['rust_family']} |\n")
        f.write('\n')
        
        # All problematic colors sorted by total difference
        f.write('## All Problematic Colors (Sorted by Total Difference)\n\n')
        f.write(f'**Total**: {len(problematic_colors)} colors exceeding 0.1 tolerance\n\n')
        f.write('| Hex | RGB | Python | Rust | ΔH | ΔV | ΔC | ΔTotal | Family |\n')
        f.write('|-----|-----|--------|------|----|----|----|---------|---------|\n')
        for i, pc in enumerate(problematic_colors):
            family_indicator = '❌' if not pc['family_match'] else '✓'
            f.write(f"| {pc['hex']} | {pc['rgb']} | {pc['python']} | {pc['rust']} | "
                   f"{pc['hue_diff']:.3f} | {pc['value_diff']:.3f} | {pc['chroma_diff']:.3f} | "
                   f"{pc['total_diff']:.3f} | {family_indicator} |\n")
        f.write('\n')
        
        # Low chroma colors (chroma < 2.0)
        f.write('## Low Chroma Colors (Python Chroma < 2.0)\n\n')
        low_chroma = [r for r in problematic_colors if r['py_chroma'] < 2.0]
        f.write(f'**Total**: {len(low_chroma)} problematic low-chroma colors\n\n')
        if low_chroma:
            f.write('| Hex | RGB | Python | Rust | ΔC | Note |\n')
            f.write('|-----|-----|--------|------|----|------|\n')
            for lc in low_chroma[:50]:  # Top 50
                note = 'Undershooting' if lc['rust_chroma'] < lc['py_chroma'] else 'Overshooting'
                f.write(f"| {lc['hex']} | {lc['rgb']} | {lc['python']} | {lc['rust']} | "
                       f"{lc['chroma_diff']:.3f} | {note} |\n")
        f.write('\n')
        
        # High chroma colors (chroma > 15.0)
        f.write('## High Chroma Colors (Python Chroma > 15.0)\n\n')
        high_chroma = [r for r in problematic_colors if r['py_chroma'] > 15.0]
        f.write(f'**Total**: {len(high_chroma)} problematic high-chroma colors\n\n')
        if high_chroma:
            f.write('| Hex | RGB | Python | Rust | ΔC | Note |\n')
            f.write('|-----|-----|--------|------|----|------|\n')
            for hc in high_chroma[:50]:  # Top 50
                note = 'Undershooting' if hc['rust_chroma'] < hc['py_chroma'] else 'Overshooting'
                f.write(f"| {hc['hex']} | {hc['rgb']} | {hc['python']} | {hc['rust']} | "
                       f"{hc['chroma_diff']:.3f} | {note} |\n")
        f.write('\n')
        
        # Edge cases (value >= 9.0)
        f.write('## Edge Cases (Value >= 9.0)\n\n')
        edge_cases = [r for r in problematic_colors if r['py_value'] >= 9.0]
        f.write(f'**Total**: {len(edge_cases)} problematic colors at high values\n\n')
        if edge_cases:
            f.write('| Hex | RGB | Python | Rust | ΔV | ΔC | Note |\n')
            f.write('|-----|-----|--------|------|----|----|------|\n')
            for ec in edge_cases[:50]:  # Top 50
                f.write(f"| {ec['hex']} | {ec['rgb']} | {ec['python']} | {ec['rust']} | "
                       f"{ec['value_diff']:.3f} | {ec['chroma_diff']:.3f} | Value={ec['py_value']:.1f} |\n")
        f.write('\n')
        
        # Family distribution of errors
        f.write('## Error Distribution by Hue Family\n\n')
        family_errors = {}
        for pc in problematic_colors:
            family = pc['py_family']
            if family not in family_errors:
                family_errors[family] = []
            family_errors[family].append(pc)
        
        f.write('| Family | Count | Avg ΔH | Avg ΔV | Avg ΔC | Avg ΔTotal |\n')
        f.write('|--------|-------|--------|--------|--------|-----------|\n')
        for family in sorted(family_errors.keys()):
            errors = family_errors[family]
            avg_h = np.mean([e['hue_diff'] for e in errors])
            avg_v = np.mean([e['value_diff'] for e in errors])
            avg_c = np.mean([e['chroma_diff'] for e in errors])
            avg_t = np.mean([e['total_diff'] for e in errors])
            f.write(f"| {family} | {len(errors)} | {avg_h:.3f} | {avg_v:.3f} | {avg_c:.3f} | {avg_t:.3f} |\n")
    
    # Write summary report
    with open('backtesting_report_v3.md', 'w') as f:
        f.write('# Munsell Conversion Backtesting Report\n\n')
        f.write(f'**Generated**: {datetime.now().isoformat()}\n')
        f.write(f'**Dataset**: {csv_path}\n')
        f.write(f'**Total Colors Tested**: {total_tested}\n\n')
        
        f.write('## Executive Summary\n\n')
        f.write(f'- **Overall Accuracy**: {accuracy:.2f}% ({within_tolerance_count}/{total_tested} within 0.1 tolerance)\n')
        f.write(f'- **Family Mismatches**: {len(family_mismatches)} colors\n')
        f.write(f'- **Hue Accuracy**: {sum(1 for r in results if r["hue_diff"] <= 0.1)/total_tested*100:.2f}% within tolerance\n')
        f.write(f'- **Value Accuracy**: {sum(1 for r in results if r["value_diff"] <= 0.1)/total_tested*100:.2f}% within tolerance\n')
        f.write(f'- **Chroma Accuracy**: {sum(1 for r in results if r["chroma_diff"] <= 0.1)/total_tested*100:.2f}% within tolerance\n\n')
        
        f.write('## Key Issues Identified\n\n')
        f.write(f'1. **Low Chroma Colors (<2.0)**: {len(low_chroma)} problematic colors\n')
        f.write(f'2. **High Chroma Colors (>15.0)**: {len(high_chroma)} problematic colors\n')
        f.write(f'3. **Edge Cases (Value ≥9.0)**: {len(edge_cases)} problematic colors\n')
        f.write(f'4. **Wrong Family Assignments**: {len(family_mismatches)} colors\n\n')
        
        f.write('See `BACKTESTING_DETAILS.md` for complete lists and detailed analysis.\n')
    
    print(f"\nBacktesting complete!")
    print(f"Overall accuracy: {accuracy:.2f}%")
    print(f"Reports written to:")
    print(f"  - backtesting_report_v3.md (summary)")
    print(f"  - BACKTESTING_DETAILS.md (detailed diagnostics)")

if __name__ == '__main__':
    main()