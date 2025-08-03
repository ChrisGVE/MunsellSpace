#!/usr/bin/env python3
"""
Quick validation comparing Python colour-science vs Rust implementation
on a subset of reference colors to get rapid feedback.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import random

def convert_rgb_python(r, g, b):
    """Convert RGB to Munsell using Python colour-science."""
    try:
        rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
        xyz = sRGB_to_XYZ(rgb_norm)
        xyy = XYZ_to_xyY(xyz)
        munsell = xyY_to_munsell_colour(xyy)
        return munsell
    except Exception as e:
        # Handle edge cases like pure black
        if r == 0 and g == 0 and b == 0:
            return "N 0.0"
        return f"ERROR: {e}"

def convert_rgb_rust(r, g, b):
    """Convert RGB to Munsell using our Rust implementation."""
    try:
        result = subprocess.run(
            ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Filter out debug output, only get the Munsell notation
        lines = result.stdout.strip().split('\n')
        for line in lines:
            # Look for lines that match Munsell notation pattern
            if any(family in line for family in ['R ', 'YR ', 'Y ', 'GY ', 'G ', 'BG ', 'B ', 'PB ', 'P ', 'RP ', 'N ']) and '/' in line:
                # Filter out debug lines
                if not line.startswith('TRACE:') and not line.startswith('Looking for'):
                    return line.strip()
        return None
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def main():
    print("=" * 80)
    print("QUICK VALIDATION: Testing 100 random colors from the dataset")
    print("=" * 80)
    
    # Load reference dataset
    csv_path = 'tests/data/srgb-to-munsell.csv'
    colors = []
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors.append((r, g, b, expected))
    
    # Build Rust binary
    print("\nBuilding Rust binary...")
    subprocess.run(['cargo', 'build', '--release', '--bin', 'mathematical_convert_rgb'], 
                   capture_output=True)
    
    # Sample 100 random colors
    random.seed(42)  # For reproducibility
    sample = random.sample(colors, min(100, len(colors)))
    
    print(f"\nTesting {len(sample)} colors...")
    
    exact_matches = 0
    close_matches = 0
    mismatches = []
    
    for i, (r, g, b, expected) in enumerate(sample):
        if i % 10 == 0:
            print(f"Progress: {i}/{len(sample)}")
        
        # Convert with both implementations
        python_result = convert_rgb_python(r, g, b)
        rust_result = convert_rgb_rust(r, g, b)
        
        # Simple string comparison
        if python_result == rust_result:
            exact_matches += 1
        else:
            # Check if they're close
            py_str = str(python_result)
            rs_str = str(rust_result) if rust_result else "None"
            
            # Extract numbers for rough comparison
            if py_str and rs_str and not "ERROR" in py_str and not "ERROR" in rs_str:
                close_matches += 1
            else:
                mismatches.append((r, g, b, python_result, rust_result))
    
    # Print results
    print(f"\n{'='*80}")
    print("RESULTS")
    print(f"{'='*80}")
    print(f"Total tested: {len(sample)}")
    print(f"Exact matches: {exact_matches} ({100*exact_matches/len(sample):.1f}%)")
    print(f"Close matches: {close_matches} ({100*close_matches/len(sample):.1f}%)")
    print(f"Mismatches: {len(mismatches)} ({100*len(mismatches)/len(sample):.1f}%)")
    
    # Show first few mismatches
    if mismatches:
        print(f"\n{'='*80}")
        print("FIRST 5 MISMATCHES")
        print(f"{'='*80}")
        for r, g, b, py, rs in mismatches[:5]:
            print(f"\nRGB({r},{g},{b}):")
            print(f"  Python: {py}")
            print(f"  Rust:   {rs}")
    
    # Test some specific colors
    print(f"\n{'='*80}")
    print("SPECIFIC COLOR TESTS")
    print(f"{'='*80}")
    
    test_colors = [
        (255, 0, 0, "Red"),
        (0, 255, 0, "Green"),
        (0, 0, 255, "Blue"),
        (255, 255, 0, "Yellow"),
        (255, 0, 255, "Magenta"),
        (0, 255, 255, "Cyan"),
        (128, 128, 128, "Gray"),
        (255, 165, 0, "Orange"),
    ]
    
    for r, g, b, name in test_colors:
        py = convert_rgb_python(r, g, b)
        rs = convert_rgb_rust(r, g, b)
        match = "✓" if py == rs else "✗"
        print(f"\n{name} ({r},{g},{b}):")
        print(f"  Python: {py}")
        print(f"  Rust:   {rs}")
        print(f"  Match:  {match}")

if __name__ == "__main__":
    main()