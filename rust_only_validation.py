#!/usr/bin/env python3
"""
Test Rust implementation on all 4,007 colors and compare with Python on a sample.
"""

import csv
import subprocess
import time
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings
warnings.filterwarnings('ignore')

def convert_python_sample(colors):
    """Convert a sample of colors with Python for comparison."""
    results = []
    for r, g, b in colors:
        try:
            rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
            xyz = sRGB_to_XYZ(rgb_norm)
            xyy = XYZ_to_xyY(xyz)
            munsell = str(xyY_to_munsell_colour(xyy))
            results.append((r, g, b, munsell))
        except:
            results.append((r, g, b, None))
    return results

def test_rust_all_colors():
    """Test Rust on all 4,007 colors."""
    print("=" * 80)
    print("FULL VALIDATION: Testing Rust on ALL 4,007 colors")
    print("=" * 80)
    
    # Load dataset
    csv_path = 'tests/data/srgb-to-munsell.csv'
    colors = []
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            colors.append((r, g, b))
    
    print(f"\nLoaded {len(colors)} colors")
    
    # Prepare input for batch converter
    input_data = '\n'.join(f"{r},{g},{b}" for r, g, b in colors)
    
    # Run Rust batch converter on all colors
    print(f"\nTesting Rust implementation on all {len(colors)} colors...")
    start = time.time()
    
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=60
    )
    
    rust_time = time.time() - start
    rust_results = result.stdout.strip().split('\n')
    
    print(f"Rust processed {len(colors)} colors in {rust_time:.2f} seconds")
    print(f"Rate: {len(colors)/rust_time:.1f} colors/second")
    
    # Count errors
    rust_errors = sum(1 for r in rust_results if r == "ERROR" or not r)
    print(f"Rust errors: {rust_errors}/{len(colors)} ({100*rust_errors/len(colors):.1f}%)")
    print(f"Rust success: {len(colors)-rust_errors}/{len(colors)} ({100*(len(colors)-rust_errors)/len(colors):.1f}%)")
    
    # Test Python on a sample for comparison
    print(f"\n{'='*80}")
    print("SAMPLING: Testing Python on 100 random colors for comparison")
    print(f"{'='*80}")
    
    import random
    random.seed(42)
    sample_indices = random.sample(range(len(colors)), min(100, len(colors)))
    sample_colors = [colors[i] for i in sample_indices]
    
    print(f"\nTesting Python on {len(sample_colors)} sample colors...")
    start = time.time()
    python_sample = convert_python_sample(sample_colors)
    py_time = time.time() - start
    
    print(f"Python processed {len(sample_colors)} colors in {py_time:.2f} seconds")
    
    # Compare the sample
    matches = 0
    py_errors = 0
    
    for idx, (r, g, b, py_result) in zip(sample_indices, python_sample):
        rust_result = rust_results[idx] if idx < len(rust_results) else None
        
        if py_result is None:
            py_errors += 1
        elif rust_result and py_result:
            # Normalize for comparison
            py_norm = ' '.join(str(py_result).split())
            rs_norm = ' '.join(rust_result.split())
            if py_norm == rs_norm:
                matches += 1
    
    print(f"\nSample comparison results:")
    print(f"Python errors on sample: {py_errors}/{len(sample_colors)} ({100*py_errors/len(sample_colors):.1f}%)")
    print(f"Exact matches on valid: {matches}/{len(sample_colors)-py_errors} ({100*matches/(len(sample_colors)-py_errors):.1f}%)")
    
    # Show some examples
    print(f"\n{'='*80}")
    print("SAMPLE COMPARISONS (first 10)")
    print(f"{'='*80}")
    
    for i, (idx, (r, g, b, py_result)) in enumerate(zip(sample_indices[:10], python_sample[:10])):
        rust_result = rust_results[idx] if idx < len(rust_results) else None
        print(f"\nRGB({r},{g},{b}):")
        print(f"  Python: {py_result if py_result else 'ERROR'}")
        print(f"  Rust:   {rust_result if rust_result else 'ERROR'}")
        match = "✓" if py_result and rust_result and ' '.join(str(py_result).split()) == ' '.join(rust_result.split()) else "✗"
        print(f"  Match:  {match}")
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"✓ Rust successfully processed {len(colors)-rust_errors}/{len(colors)} colors ({100*(len(colors)-rust_errors)/len(colors):.1f}%)")
    print(f"✓ Processing speed: {len(colors)/rust_time:.1f} colors/second")
    print(f"✓ Sample accuracy vs Python: {100*matches/(len(sample_colors)-py_errors):.1f}% exact matches")

if __name__ == "__main__":
    test_rust_all_colors()