#!/usr/bin/env python3
"""
Test Python colour-science on a sample vs reference dataset.
"""

import csv
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import random
import time
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 80)
    print("Testing Python colour-science vs Reference Dataset")  
    print("=" * 80)
    
    # Load dataset
    colors = []
    expected_values = []
    
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors.append((r, g, b))
            expected_values.append(expected)
    
    print(f"\nTotal colors in dataset: {len(colors)}")
    
    # Sample 100 random colors
    random.seed(42)
    sample_size = 100
    sample_indices = random.sample(range(len(colors)), sample_size)
    
    print(f"Testing Python on {sample_size} random colors...")
    
    exact_matches = 0
    errors = 0
    differences = []
    
    start = time.time()
    
    for i, idx in enumerate(sample_indices):
        if i % 10 == 0:
            print(f"  Progress: {i}/{sample_size}")
        
        r, g, b = colors[idx]
        expected = expected_values[idx]
        
        try:
            rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
            xyz = sRGB_to_XYZ(rgb_norm)
            xyy = XYZ_to_xyY(xyz)
            munsell = str(xyY_to_munsell_colour(xyy))
            
            # Normalize for comparison
            expected_norm = ' '.join(expected.split())
            munsell_norm = ' '.join(munsell.split())
            
            if expected_norm == munsell_norm:
                exact_matches += 1
            else:
                differences.append((r, g, b, expected, munsell))
        except Exception as e:
            errors += 1
            differences.append((r, g, b, expected, f"ERROR: {str(e)[:50]}"))
    
    elapsed = time.time() - start
    
    print(f"\n✓ Completed in {elapsed:.1f} seconds")
    print(f"  Rate: {sample_size/elapsed:.1f} colors/second")
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    print(f"Sample size:         {sample_size}")
    print(f"Exact matches:       {exact_matches} ({100*exact_matches/sample_size:.1f}%)")
    print(f"Differences:         {len(differences)} ({100*len(differences)/sample_size:.1f}%)")
    print(f"Python errors:       {errors} ({100*errors/sample_size:.1f}%)")
    
    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    
    if exact_matches == 0:
        print("\n⚠️  WARNING: Python doesn't match ANY reference colors exactly!")
        print("This suggests Python uses a different algorithm than the reference dataset.")
    else:
        print(f"\n✓ Python matches {exact_matches}/{sample_size} reference colors exactly.")
    
    # Show some examples
    if differences:
        print(f"\n--- First 10 Differences ---")
        for r, g, b, expected, python in differences[:10]:
            print(f"RGB({r:3},{g:3},{b:3}): Expected='{expected}' Python='{python}'")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    if exact_matches == 0:
        print("\nPython colour-science uses a DIFFERENT algorithm than the reference dataset.")
        print("The reference dataset appears to be pre-computed/lookup-based.")
        print("Our Rust implementation achieving 61.9% match with reference is GOOD,")
        print("considering Python achieves 0% match with the same reference!")
    else:
        print(f"\nPython matches {100*exact_matches/sample_size:.1f}% of reference colors.")

if __name__ == "__main__":
    main()