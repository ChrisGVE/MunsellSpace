#!/usr/bin/env python3
"""
Batch validation comparing Python colour-science vs Rust implementation
on all 4,007 reference colors using efficient batch processing.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import time
import warnings
warnings.filterwarnings('ignore')

def convert_all_python(colors):
    """Convert all colors using Python colour-science."""
    results = []
    for r, g, b in colors:
        try:
            rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
            xyz = sRGB_to_XYZ(rgb_norm)
            xyy = XYZ_to_xyY(xyz)
            munsell = str(xyY_to_munsell_colour(xyy))
            results.append(munsell)
        except:
            if r == 0 and g == 0 and b == 0:
                results.append("N 0.0")
            else:
                results.append(None)
    return results

def convert_all_rust(colors):
    """Convert all colors using Rust batch converter."""
    # Prepare input for batch converter
    input_data = '\n'.join(f"{r},{g},{b}" for r, g, b in colors)
    
    # Run batch converter
    try:
        result = subprocess.run(
            ['./target/release/batch_convert'],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        lines = result.stdout.strip().split('\n')
        return [line if line != "ERROR" else None for line in lines]
    except subprocess.TimeoutExpired:
        print("Rust batch converter timed out!")
        return [None] * len(colors)
    except Exception as e:
        print(f"Error running Rust converter: {e}")
        return [None] * len(colors)

def normalize_notation(notation):
    """Normalize Munsell notation for comparison."""
    if notation is None:
        return None
    notation = str(notation).strip()
    # Remove extra spaces and standardize format
    parts = notation.split()
    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"
    return notation

def main():
    print("=" * 80)
    print("BATCH VALIDATION: Testing ALL 4,007 colors efficiently")
    print("=" * 80)
    
    # Load reference dataset
    csv_path = 'tests/data/srgb-to-munsell.csv'
    colors = []
    
    print(f"\nLoading dataset from {csv_path}...")
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            colors.append((r, g, b))
    
    print(f"Loaded {len(colors)} colors")
    
    # Build Rust binary
    print("\nBuilding Rust batch converter...")
    result = subprocess.run(['cargo', 'build', '--release', '--bin', 'batch_convert'], 
                          capture_output=True)
    if result.returncode != 0:
        print("Failed to build Rust binary!")
        print(result.stderr.decode())
        return
    
    # Convert all colors with Python
    print(f"\nConverting all {len(colors)} colors with Python...")
    start_py = time.time()
    python_results = convert_all_python(colors)
    py_time = time.time() - start_py
    print(f"Python conversion complete in {py_time:.1f} seconds ({len(colors)/py_time:.1f} colors/sec)")
    
    # Convert all colors with Rust
    print(f"\nConverting all {len(colors)} colors with Rust...")
    start_rs = time.time()
    rust_results = convert_all_rust(colors)
    rs_time = time.time() - start_rs
    print(f"Rust conversion complete in {rs_time:.1f} seconds ({len(colors)/rs_time:.1f} colors/sec)")
    
    # Compare results
    print("\nComparing results...")
    
    exact_matches = 0
    python_errors = 0
    rust_errors = 0
    both_valid = 0
    differences = []
    
    for i, ((r, g, b), py_result, rs_result) in enumerate(zip(colors, python_results, rust_results)):
        if py_result is None:
            python_errors += 1
        if rs_result is None:
            rust_errors += 1
        
        if py_result and rs_result:
            both_valid += 1
            py_norm = normalize_notation(py_result)
            rs_norm = normalize_notation(rs_result)
            
            if py_norm == rs_norm:
                exact_matches += 1
            else:
                differences.append((r, g, b, py_result, rs_result))
    
    # Print results
    print(f"\n{'='*80}")
    print("VALIDATION RESULTS - ALL 4,007 COLORS")
    print(f"{'='*80}")
    
    print(f"\n--- Performance ---")
    print(f"Python: {py_time:.1f}s ({len(colors)/py_time:.1f} colors/sec)")
    print(f"Rust:   {rs_time:.1f}s ({len(colors)/rs_time:.1f} colors/sec)")
    print(f"Speedup: {py_time/rs_time:.1f}x faster")
    
    print(f"\n--- Coverage ---")
    print(f"Total colors tested:        {len(colors):,}")
    print(f"Both implementations valid: {both_valid:,} ({100*both_valid/len(colors):.1f}%)")
    print(f"Python errors:             {python_errors:,} ({100*python_errors/len(colors):.1f}%)")
    print(f"Rust errors:               {rust_errors:,} ({100*rust_errors/len(colors):.1f}%)")
    
    if both_valid > 0:
        print(f"\n--- Accuracy (on {both_valid:,} valid comparisons) ---")
        print(f"Exact matches:      {exact_matches:,} ({100*exact_matches/both_valid:.1f}%)")
        print(f"Differences:        {len(differences):,} ({100*len(differences)/both_valid:.1f}%)")
        
        # Analyze differences by hue family
        if differences:
            same_family = 0
            for r, g, b, py, rs in differences:
                if py and rs:
                    # Extract hue families
                    py_parts = py.split()
                    rs_parts = rs.split()
                    if len(py_parts) >= 1 and len(rs_parts) >= 1:
                        py_hue = ''.join(c for c in py_parts[0] if c.isalpha())
                        rs_hue = ''.join(c for c in rs_parts[0] if c.isalpha())
                        if py_hue == rs_hue:
                            same_family += 1
            
            print(f"\n--- Difference Analysis ---")
            print(f"Same hue family:    {same_family:,}/{len(differences):,} ({100*same_family/len(differences):.1f}%)")
            print(f"Different family:   {len(differences)-same_family:,}/{len(differences):,} ({100*(len(differences)-same_family)/len(differences):.1f}%)")
    
    # Show sample differences
    if differences:
        print(f"\n--- Sample Differences (first 10) ---")
        for r, g, b, py, rs in differences[:10]:
            print(f"RGB({r:3},{g:3},{b:3}): Python='{py}' vs Rust='{rs}'")
    
    # Save results
    output_file = f"batch_validation_4007_{int(time.time())}.csv"
    print(f"\n--- Saving Results ---")
    print(f"Writing to {output_file}...")
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Python', 'Rust', 'Match'])
        
        for (r, g, b), py, rs in zip(colors, python_results, rust_results):
            match = "YES" if py and rs and normalize_notation(py) == normalize_notation(rs) else "NO"
            writer.writerow([r, g, b, py or "ERROR", rs or "ERROR", match])
    
    print(f"Results saved to {output_file}")
    
    print(f"\n{'='*80}")
    print("✓ BATCH VALIDATION COMPLETE - ALL 4,007 COLORS TESTED!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()