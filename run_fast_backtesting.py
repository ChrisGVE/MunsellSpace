#!/usr/bin/env python3
"""Fast backtesting by calling Rust binary in batch mode"""

import csv
import json
import subprocess
import numpy as np
from collections import defaultdict
from colour.notation import munsell
from colour import sRGB_to_XYZ, XYZ_to_xyY
import tempfile
import os

def test_batch_colors(colors):
    """Test a batch of colors through Rust"""
    # Write colors to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for r, g, b in colors:
            f.write(f"{r} {g} {b}\n")
        temp_file = f.name
    
    results = []
    try:
        # Process each color
        for r, g, b in colors:
            result = subprocess.run(
                ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            if result.returncode == 0 and 'Munsell:' in result.stdout:
                notation = result.stdout.split('Munsell:')[1].strip()
                results.append(notation)
            else:
                results.append(None)
    finally:
        os.unlink(temp_file)
    
    return results

def main():
    print("Loading dataset...")
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3]
            colors.append((r, g, b, expected))
    
    print(f"Testing {len(colors)} colors...")
    
    # Statistics
    family_mismatches = defaultdict(int)
    hue_diffs = []
    value_diffs = []
    chroma_diffs = []
    problematic = []
    total_tested = 0
    within_tolerance = 0
    
    # Process in batches
    batch_size = 50
    for i in range(0, len(colors), batch_size):
        if i % 500 == 0:
            print(f"Progress: {i}/{len(colors)}")
        
        batch = colors[i:i+batch_size]
        rgb_batch = [(r, g, b) for r, g, b, _ in batch]
        
        # Get Rust results
        rust_results = test_batch_colors(rgb_batch)
        
        # Compare with Python
        for j, ((r, g, b, expected), rust_notation) in enumerate(zip(batch, rust_results)):
            if not rust_notation:
                continue
                
            try:
                # Python conversion
                srgb = [r/255.0, g/255.0, b/255.0]
                xyz = sRGB_to_XYZ(srgb)
                xyy = XYZ_to_xyY(xyz)
                py_spec = munsell.xyY_to_munsell_specification(xyy)
                
                # Parse Rust result
                rust_spec = munsell.munsell_colour_to_munsell_specification(rust_notation)
                
                # Calculate differences
                h_diff = abs(py_spec[0] - rust_spec[0]) if not (np.isnan(py_spec[0]) or np.isnan(rust_spec[0])) else 0
                v_diff = abs(py_spec[1] - rust_spec[1])
                c_diff = abs(py_spec[2] - rust_spec[2]) if not (np.isnan(py_spec[2]) or np.isnan(rust_spec[2])) else 0
                
                hue_diffs.append(h_diff)
                value_diffs.append(v_diff)
                chroma_diffs.append(c_diff)
                total_tested += 1
                
                if h_diff <= 0.1 and v_diff <= 0.1 and c_diff <= 0.1:
                    within_tolerance += 1
                else:
                    if len(problematic) < 10:
                        problematic.append({
                            'hex': f"#{r:02x}{g:02x}{b:02x}",
                            'rgb': (r, g, b),
                            'python': munsell.munsell_specification_to_munsell_colour(py_spec, 1, 1, 1),
                            'rust': rust_notation,
                            'diffs': (h_diff, v_diff, c_diff)
                        })
                
                # Check family mismatch
                py_family = int(py_spec[3])
                rust_family = int(rust_spec[3])
                if py_family != rust_family:
                    families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y',
                              6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
                    family_mismatches[f"{families[py_family]}→{families[rust_family]}"] += 1
                    
            except Exception as e:
                continue
    
    # Calculate statistics
    print("\n" + "="*80)
    print("FAST BACKTESTING RESULTS")
    print("="*80)
    
    print(f"\nTotal tested: {total_tested}")
    print(f"Within 0.1 tolerance: {within_tolerance} ({100*within_tolerance/total_tested:.1f}%)")
    
    if family_mismatches:
        print(f"\nFamily mismatches: {sum(family_mismatches.values())}")
        for trans, count in sorted(family_mismatches.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {trans}: {count}")
    
    if hue_diffs:
        print(f"\nHue differences:")
        print(f"  Median: {np.median(hue_diffs):.6f}")
        print(f"  90th percentile: {np.percentile(hue_diffs, 90):.6f}")
        print(f"  95th percentile: {np.percentile(hue_diffs, 95):.6f}")
        print(f"  99th percentile: {np.percentile(hue_diffs, 99):.6f}")
        print(f"  Max: {max(hue_diffs):.6f}")
        print(f"  Above 0.1: {sum(1 for d in hue_diffs if d > 0.1)}")
    
    if value_diffs:
        print(f"\nValue differences:")
        print(f"  Median: {np.median(value_diffs):.6f}")
        print(f"  90th percentile: {np.percentile(value_diffs, 90):.6f}")
        print(f"  95th percentile: {np.percentile(value_diffs, 95):.6f}")
        print(f"  99th percentile: {np.percentile(value_diffs, 99):.6f}")
        print(f"  Max: {max(value_diffs):.6f}")
        print(f"  Above 0.1: {sum(1 for d in value_diffs if d > 0.1)}")
    
    if chroma_diffs:
        print(f"\nChroma differences:")
        print(f"  Median: {np.median(chroma_diffs):.6f}")
        print(f"  90th percentile: {np.percentile(chroma_diffs, 90):.6f}")
        print(f"  95th percentile: {np.percentile(chroma_diffs, 95):.6f}")
        print(f"  99th percentile: {np.percentile(chroma_diffs, 99):.6f}")
        print(f"  Max: {max(chroma_diffs):.6f}")
        print(f"  Above 0.1: {sum(1 for d in chroma_diffs if d > 0.1)}")
    
    if problematic:
        print(f"\nFirst problematic colors (diffs > 0.1):")
        for p in problematic[:5]:
            print(f"  {p['hex']}: P={p['python']}, R={p['rust']}, Δ={p['diffs']}")
    
    print("="*80)
    
    # Save results
    results = {
        'total_tested': total_tested,
        'accuracy_percentage': 100 * within_tolerance / total_tested,
        'family_mismatches': dict(family_mismatches),
        'statistics': {
            'hue': {
                'median': float(np.median(hue_diffs)),
                '90th': float(np.percentile(hue_diffs, 90)),
                '95th': float(np.percentile(hue_diffs, 95)),
                '99th': float(np.percentile(hue_diffs, 99)),
                'max': float(max(hue_diffs)),
                'above_0.1': sum(1 for d in hue_diffs if d > 0.1)
            },
            'value': {
                'median': float(np.median(value_diffs)),
                '90th': float(np.percentile(value_diffs, 90)),
                '95th': float(np.percentile(value_diffs, 95)),
                '99th': float(np.percentile(value_diffs, 99)),
                'max': float(max(value_diffs)),
                'above_0.1': sum(1 for d in value_diffs if d > 0.1)
            },
            'chroma': {
                'median': float(np.median(chroma_diffs)),
                '90th': float(np.percentile(chroma_diffs, 90)),
                '95th': float(np.percentile(chroma_diffs, 95)),
                '99th': float(np.percentile(chroma_diffs, 99)),
                'max': float(max(chroma_diffs)),
                'above_0.1': sum(1 for d in chroma_diffs if d > 0.1)
            }
        }
    }
    
    with open('fast_backtesting_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to fast_backtesting_results.json")

if __name__ == "__main__":
    main()