#!/usr/bin/env python3
"""
Parallel Backtesting - Process all 4,007 colors efficiently using multiprocessing
"""

import csv
import json
import subprocess
import numpy as np
from collections import defaultdict
from colour.notation import munsell
from colour import sRGB_to_XYZ, XYZ_to_xyY
from datetime import datetime
import multiprocessing as mp
from functools import partial
import os
import sys

def process_color_batch(batch, rust_binary='./target/release/test_rgb_cli'):
    """Process a batch of colors (runs in parallel)"""
    results = []
    
    for r, g, b, expected in batch:
        try:
            # Python conversion
            srgb = [r/255.0, g/255.0, b/255.0]
            xyz = sRGB_to_XYZ(srgb)
            xyy = XYZ_to_xyY(xyz)
            raw_spec = munsell.xyY_to_munsell_specification(xyy)
            py_notation = munsell.munsell_specification_to_munsell_colour(raw_spec, 1, 1, 1)
            py_spec = munsell.munsell_colour_to_munsell_specification(py_notation)
            
            # Rust conversion
            result = subprocess.run(
                [rust_binary, str(r), str(g), str(b)],
                capture_output=True,
                text=True,
                timeout=0.5
            )
            
            if result.returncode == 0 and 'Munsell:' in result.stdout:
                rust_notation = result.stdout.split('Munsell:')[1].strip()
                rust_spec = munsell.munsell_colour_to_munsell_specification(rust_notation)
                
                # Calculate differences with circular hue
                py_hue = 0 if np.isnan(py_spec[0]) else py_spec[0]
                py_chroma = 0 if np.isnan(py_spec[2]) else py_spec[2]
                rust_hue = 0 if np.isnan(rust_spec[0]) else rust_spec[0]
                rust_chroma = 0 if np.isnan(rust_spec[2]) else rust_spec[2]
                
                # Circular hue difference
                if py_chroma == 0 and rust_chroma == 0:
                    hue_diff = 0.0
                else:
                    direct_diff = abs(py_hue - rust_hue)
                    wraparound_diff = 10.0 - direct_diff
                    hue_diff = min(direct_diff, wraparound_diff)
                
                results.append({
                    'rgb': (r, g, b),
                    'hex': f"#{r:02x}{g:02x}{b:02x}",
                    'expected': expected,
                    'py_notation': py_notation,
                    'rust_notation': rust_notation,
                    'hue_diff': hue_diff,
                    'value_diff': abs(py_spec[1] - rust_spec[1]),
                    'chroma_diff': abs(py_chroma - rust_chroma),
                    'family_match': int(py_spec[3]) == int(rust_spec[3]),
                    'py_family': int(py_spec[3]),
                    'rust_family': int(rust_spec[3])
                })
        except Exception:
            pass
    
    return results

def main():
    print("=" * 80)
    print("PARALLEL MUNSELL CONVERSION BACKTESTING")
    print("=" * 80)
    
    # Check Rust binary
    rust_binary = './target/release/test_rgb_cli'
    if not os.path.exists(rust_binary):
        print(f"Building Rust binary...")
        subprocess.run(['cargo', 'build', '--release', '--bin', 'test_rgb_cli'])
    
    # Load dataset
    print("Loading dataset...")
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            colors.append((int(row[0]), int(row[1]), int(row[2]), row[3]))
    
    print(f"Testing {len(colors)} colors using {mp.cpu_count()} CPUs...")
    
    # Split into batches for parallel processing
    batch_size = 50
    batches = [colors[i:i+batch_size] for i in range(0, len(colors), batch_size)]
    
    # Process in parallel
    start_time = datetime.now()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        all_results = pool.map(process_color_batch, batches)
    
    # Flatten results
    results = []
    for batch_results in all_results:
        results.extend(batch_results)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Completed in {elapsed:.1f} seconds ({len(results)/elapsed:.1f} colors/sec)")
    
    # Calculate statistics
    families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y',
                6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
    
    family_mismatches = defaultdict(int)
    hue_diffs = []
    value_diffs = []
    chroma_diffs = []
    within_tolerance = 0
    
    for r in results:
        hue_diffs.append(r['hue_diff'])
        value_diffs.append(r['value_diff'])
        chroma_diffs.append(r['chroma_diff'])
        
        if r['hue_diff'] <= 0.1 and r['value_diff'] <= 0.1 and r['chroma_diff'] <= 0.1:
            within_tolerance += 1
        
        if not r['family_match']:
            py_fam = families[r['py_family']]
            rust_fam = families[r['rust_family']]
            family_mismatches[f"{py_fam}→{rust_fam}"] += 1
    
    # Generate report
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    accuracy = 100 * within_tolerance / len(results) if results else 0
    print(f"\nOverall Accuracy: {accuracy:.2f}% ({within_tolerance}/{len(results)} within 0.1 tolerance)")
    
    total_mismatches = sum(family_mismatches.values())
    print(f"Family Mismatches: {total_mismatches} ({100*total_mismatches/len(results):.2f}%)")
    
    # Component statistics
    percentiles = [50, 90, 95, 96, 97, 98, 99, 99.5, 100]
    
    print("\nComponent Statistics:")
    for component, diffs in [('Hue', hue_diffs), ('Value', value_diffs), ('Chroma', chroma_diffs)]:
        print(f"\n{component}:")
        print(f"  Median: {np.median(diffs):.6f}")
        print(f"  Mean: {np.mean(diffs):.6f}")
        print(f"  96th %ile: {np.percentile(diffs, 96):.6f}")
        print(f"  97th %ile: {np.percentile(diffs, 97):.6f}")
        print(f"  98th %ile: {np.percentile(diffs, 98):.6f}")
        print(f"  99th %ile: {np.percentile(diffs, 99):.6f}")
        print(f"  Max: {max(diffs):.6f}")
        above_tol = sum(1 for d in diffs if d > 0.1)
        print(f"  Above 0.1: {above_tol} ({100*above_tol/len(diffs):.2f}%)")
    
    # Save detailed results
    stats = {
        'test_date': datetime.now().isoformat(),
        'total_tested': len(results),
        'overall_accuracy': accuracy,
        'family_mismatches': {
            'total': total_mismatches,
            'percentage': 100 * total_mismatches / len(results) if results else 0,
            'by_transition': dict(sorted(family_mismatches.items(), key=lambda x: x[1], reverse=True))
        },
        'hue': {
            'median': float(np.median(hue_diffs)),
            'mean': float(np.mean(hue_diffs)),
            'percentiles': {p: float(np.percentile(hue_diffs, p)) for p in percentiles},
            'above_0.1': sum(1 for d in hue_diffs if d > 0.1),
            'above_0.1_pct': 100 * sum(1 for d in hue_diffs if d > 0.1) / len(hue_diffs)
        },
        'value': {
            'median': float(np.median(value_diffs)),
            'mean': float(np.mean(value_diffs)),
            'percentiles': {p: float(np.percentile(value_diffs, p)) for p in percentiles},
            'above_0.1': sum(1 for d in value_diffs if d > 0.1),
            'above_0.1_pct': 100 * sum(1 for d in value_diffs if d > 0.1) / len(value_diffs)
        },
        'chroma': {
            'median': float(np.median(chroma_diffs)),
            'mean': float(np.mean(chroma_diffs)),
            'percentiles': {p: float(np.percentile(chroma_diffs, p)) for p in percentiles},
            'above_0.1': sum(1 for d in chroma_diffs if d > 0.1),
            'above_0.1_pct': 100 * sum(1 for d in chroma_diffs if d > 0.1) / len(chroma_diffs)
        }
    }
    
    # Find most problematic colors
    problematic = []
    for r in results:
        max_diff = max(r['hue_diff'], r['value_diff'], r['chroma_diff'])
        if max_diff > 0.1:
            problematic.append({
                'hex': r['hex'],
                'rgb': r['rgb'],
                'python': r['py_notation'],
                'rust': r['rust_notation'],
                'hue_diff': r['hue_diff'],
                'value_diff': r['value_diff'],
                'chroma_diff': r['chroma_diff'],
                'max_diff': max_diff
            })
    
    problematic.sort(key=lambda x: x['max_diff'], reverse=True)
    
    # Write markdown report
    with open('parallel_backtesting_report.md', 'w') as f:
        f.write("# Munsell Conversion Backtesting Report - Full Dataset\n\n")
        f.write(f"**Generated**: {stats['test_date']}\n")
        f.write(f"**Total Colors Tested**: {stats['total_tested']:,}\n")
        f.write(f"**Processing Time**: {elapsed:.1f} seconds\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write(f"- **Overall Accuracy**: {accuracy:.2f}% ({within_tolerance:,}/{len(results):,} within 0.1 tolerance)\n")
        f.write(f"- **Family Mismatches**: {stats['family_mismatches']['percentage']:.2f}% ({total_mismatches:,} colors)\n")
        f.write(f"- **Hue Accuracy**: {100 - stats['hue']['above_0.1_pct']:.2f}% within tolerance\n")
        f.write(f"- **Value Accuracy**: {100 - stats['value']['above_0.1_pct']:.2f}% within tolerance\n")
        f.write(f"- **Chroma Accuracy**: {100 - stats['chroma']['above_0.1_pct']:.2f}% within tolerance\n\n")
        
        # Detailed percentiles
        f.write("## Detailed Percentile Analysis\n\n")
        f.write("| Component | 96th %ile | 97th %ile | 98th %ile | 99th %ile | Max |\n")
        f.write("|-----------|-----------|-----------|-----------|-----------|-----|\n")
        f.write(f"| Hue | {stats['hue']['percentiles'][96]:.6f} | {stats['hue']['percentiles'][97]:.6f} | ")
        f.write(f"{stats['hue']['percentiles'][98]:.6f} | {stats['hue']['percentiles'][99]:.6f} | ")
        f.write(f"{stats['hue']['percentiles'][100]:.6f} |\n")
        f.write(f"| Value | {stats['value']['percentiles'][96]:.6f} | {stats['value']['percentiles'][97]:.6f} | ")
        f.write(f"{stats['value']['percentiles'][98]:.6f} | {stats['value']['percentiles'][99]:.6f} | ")
        f.write(f"{stats['value']['percentiles'][100]:.6f} |\n")
        f.write(f"| Chroma | {stats['chroma']['percentiles'][96]:.6f} | {stats['chroma']['percentiles'][97]:.6f} | ")
        f.write(f"{stats['chroma']['percentiles'][98]:.6f} | {stats['chroma']['percentiles'][99]:.6f} | ")
        f.write(f"{stats['chroma']['percentiles'][100]:.6f} |\n\n")
        
        # Top problematic colors
        if problematic:
            f.write("## Most Problematic Colors (Top 50)\n\n")
            f.write("| Hex | Python | Rust | ΔH | ΔV | ΔC |\n")
            f.write("|-----|--------|------|----|----|----|")
            for p in problematic[:50]:
                f.write(f"| {p['hex']} | {p['python']} | {p['rust']} | ")
                f.write(f"{p['hue_diff']:.3f} | {p['value_diff']:.3f} | {p['chroma_diff']:.3f} |\n")
        
        # Family mismatches
        if family_mismatches:
            f.write("\n## Family Mismatches\n\n")
            f.write("| Transition | Count | Percentage |\n")
            f.write("|------------|-------|------------|\n")
            for trans, count in list(stats['family_mismatches']['by_transition'].items())[:20]:
                pct = 100 * count / total_mismatches
                f.write(f"| {trans} | {count} | {pct:.1f}% |\n")
    
    print(f"\nReports saved:")
    print(f"  - parallel_backtesting_report.md")
    
    with open('parallel_backtesting_results.json', 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"  - parallel_backtesting_results.json")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    # Suppress warnings
    import warnings
    warnings.filterwarnings('ignore')
    main()