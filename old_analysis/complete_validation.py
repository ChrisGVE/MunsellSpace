#!/usr/bin/env python3
"""
Complete validation:
1. Test Rust on ALL 4,007 colors against the reference dataset
2. Test Python on a sample to verify it matches the reference
No timeouts - let it run as long as needed.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import time
import random
import warnings
warnings.filterwarnings('ignore')

def normalize_munsell(notation):
    """Normalize Munsell notation for comparison."""
    if not notation:
        return None
    notation = str(notation).strip()
    # Standardize spacing
    parts = notation.split()
    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"
    return notation

def test_rust_all_colors(colors_with_expected):
    """Test Rust on all 4,007 colors against reference."""
    print("=" * 80)
    print("PART 1: Testing Rust on ALL 4,007 colors vs Reference Dataset")
    print("=" * 80)
    
    # Prepare input for batch converter
    input_data = '\n'.join(f"{r},{g},{b}" for r, g, b, _ in colors_with_expected)
    
    print(f"\nProcessing {len(colors_with_expected)} colors with Rust (no timeout)...")
    start = time.time()
    
    # Run without timeout
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    rust_time = time.time() - start
    rust_results = result.stdout.strip().split('\n')
    
    print(f"✓ Rust completed in {rust_time:.1f} seconds")
    print(f"  Rate: {len(colors_with_expected)/rust_time:.1f} colors/second")
    
    # Compare with reference
    exact_matches = 0
    rust_errors = 0
    differences = []
    
    for (r, g, b, expected), rust_result in zip(colors_with_expected, rust_results):
        if not rust_result or rust_result == "ERROR":
            rust_errors += 1
            differences.append((r, g, b, expected, "ERROR"))
        else:
            expected_norm = normalize_munsell(expected)
            rust_norm = normalize_munsell(rust_result)
            
            if expected_norm == rust_norm:
                exact_matches += 1
            else:
                differences.append((r, g, b, expected, rust_result))
    
    print(f"\n--- Rust vs Reference Results ---")
    print(f"Total colors:     {len(colors_with_expected):,}")
    print(f"Exact matches:    {exact_matches:,} ({100*exact_matches/len(colors_with_expected):.2f}%)")
    print(f"Differences:      {len(differences):,} ({100*len(differences)/len(colors_with_expected):.2f}%)")
    print(f"Rust errors:      {rust_errors:,} ({100*rust_errors/len(colors_with_expected):.2f}%)")
    
    # Show some examples of differences
    if differences:
        print(f"\n--- Sample Differences (first 10) ---")
        for r, g, b, expected, rust in differences[:10]:
            print(f"RGB({r:3},{g:3},{b:3}): Expected='{expected}' vs Rust='{rust}'")
    
    return rust_results, differences

def test_python_sample(colors_with_expected, sample_size=100):
    """Test Python on a sample to verify it matches reference."""
    print(f"\n{'='*80}")
    print(f"PART 2: Testing Python on {sample_size} random colors vs Reference")
    print(f"{'='*80}")
    
    # Random sample
    random.seed(42)
    sample_indices = random.sample(range(len(colors_with_expected)), 
                                  min(sample_size, len(colors_with_expected)))
    sample = [colors_with_expected[i] for i in sample_indices]
    
    print(f"\nProcessing {len(sample)} colors with Python (no timeout)...")
    start = time.time()
    
    python_results = []
    python_errors = 0
    
    for i, (r, g, b, expected) in enumerate(sample):
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(sample)}")
        
        try:
            rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
            xyz = sRGB_to_XYZ(rgb_norm)
            xyy = XYZ_to_xyY(xyz)
            munsell = str(xyY_to_munsell_colour(xyy))
            python_results.append((r, g, b, expected, munsell))
        except Exception as e:
            python_errors += 1
            python_results.append((r, g, b, expected, f"ERROR: {str(e)[:50]}"))
    
    py_time = time.time() - start
    print(f"✓ Python completed in {py_time:.1f} seconds")
    print(f"  Rate: {len(sample)/py_time:.1f} colors/second")
    
    # Compare with reference
    exact_matches = 0
    differences = []
    
    for r, g, b, expected, py_result in python_results:
        if "ERROR" in str(py_result):
            differences.append((r, g, b, expected, py_result))
        else:
            expected_norm = normalize_munsell(expected)
            py_norm = normalize_munsell(py_result)
            
            if expected_norm == py_norm:
                exact_matches += 1
            else:
                differences.append((r, g, b, expected, py_result))
    
    print(f"\n--- Python vs Reference Results ---")
    print(f"Sample size:      {len(sample)}")
    print(f"Exact matches:    {exact_matches} ({100*exact_matches/len(sample):.2f}%)")
    print(f"Differences:      {len(differences)} ({100*len(differences)/len(sample):.2f}%)")
    print(f"Python errors:    {python_errors} ({100*python_errors/len(sample):.2f}%)")
    
    # Show examples
    if differences:
        print(f"\n--- Python Differences (first 10) ---")
        for r, g, b, expected, py in differences[:10]:
            print(f"RGB({r:3},{g:3},{b:3}): Expected='{expected}' vs Python='{py}'")
    
    return python_results

def compare_rust_python_on_sample(colors_with_expected, rust_results, sample_size=100):
    """Compare Rust and Python on the same sample."""
    print(f"\n{'='*80}")
    print(f"PART 3: Direct Comparison - Rust vs Python on {sample_size} colors")
    print(f"{'='*80}")
    
    # Use same random sample
    random.seed(42)
    sample_indices = random.sample(range(len(colors_with_expected)), 
                                  min(sample_size, len(colors_with_expected)))
    
    print(f"\nComparing Rust and Python on the same {len(sample_indices)} colors...")
    
    exact_matches = 0
    both_match_reference = 0
    
    for idx in sample_indices[:20]:  # Show first 20
        r, g, b, expected = colors_with_expected[idx]
        rust_result = rust_results[idx] if idx < len(rust_results) else "ERROR"
        
        # Get Python result
        try:
            rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
            xyz = sRGB_to_XYZ(rgb_norm)
            xyy = XYZ_to_xyY(xyz)
            py_result = str(xyY_to_munsell_colour(xyy))
        except:
            py_result = "ERROR"
        
        # Normalize all
        expected_norm = normalize_munsell(expected)
        rust_norm = normalize_munsell(rust_result)
        py_norm = normalize_munsell(py_result)
        
        rust_matches_ref = expected_norm == rust_norm
        py_matches_ref = expected_norm == py_norm
        rust_matches_py = rust_norm == py_norm
        
        if rust_matches_py:
            exact_matches += 1
        if rust_matches_ref and py_matches_ref:
            both_match_reference += 1
        
        # Show comparison
        print(f"\nRGB({r:3},{g:3},{b:3}):")
        print(f"  Reference: {expected}")
        print(f"  Rust:      {rust_result} {'✓' if rust_matches_ref else '✗'}")
        print(f"  Python:    {py_result} {'✓' if py_matches_ref else '✗'}")
        print(f"  R vs P:    {'MATCH' if rust_matches_py else 'DIFFER'}")

def main():
    print("=" * 80)
    print("COMPLETE VALIDATION - No Timeouts")
    print("=" * 80)
    
    # Load dataset
    csv_path = 'tests/data/srgb-to-munsell.csv'
    colors_with_expected = []
    
    print(f"\nLoading reference dataset from {csv_path}...")
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors_with_expected.append((r, g, b, expected))
    
    print(f"Loaded {len(colors_with_expected)} colors with expected Munsell values")
    
    # Build Rust binary
    print("\nBuilding Rust binary...")
    subprocess.run(['cargo', 'build', '--release', '--bin', 'batch_convert'], 
                   capture_output=True)
    
    # Part 1: Test Rust on ALL colors
    rust_results, rust_diffs = test_rust_all_colors(colors_with_expected)
    
    # Part 2: Test Python on sample
    python_results = test_python_sample(colors_with_expected, sample_size=100)
    
    # Part 3: Direct comparison
    compare_rust_python_on_sample(colors_with_expected, rust_results, sample_size=100)
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"✓ Tested Rust on ALL 4,007 colors against reference dataset")
    print(f"✓ Tested Python on 100 sample colors against reference")
    print(f"✓ Compared Rust vs Python on same sample")
    
    # Save detailed results
    output_file = f"complete_validation_{int(time.time())}.csv"
    print(f"\nSaving detailed results to {output_file}...")
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Expected', 'Rust Result', 'Match'])
        
        for (r, g, b, expected), rust_result in zip(colors_with_expected, rust_results):
            match = "YES" if normalize_munsell(expected) == normalize_munsell(rust_result) else "NO"
            writer.writerow([r, g, b, expected, rust_result, match])
    
    print(f"Results saved to {output_file}")
    print("\n✓ VALIDATION COMPLETE!")

if __name__ == "__main__":
    main()