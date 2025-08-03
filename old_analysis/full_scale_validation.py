#!/usr/bin/env python3
"""
Full-scale validation comparing Python colour-science vs Rust implementation
on all 4,007 reference colors from srgb-to-munsell.csv
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import time
from collections import defaultdict

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
        return None  # Return None for errors to simplify comparison

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

def parse_munsell(notation):
    """Parse Munsell notation into components for comparison."""
    if notation is None:
        return None, None, None, None
    
    notation = notation.strip()
    
    # Handle neutral colors
    if notation.startswith('N '):
        parts = notation.split()
        return 'N', 0.0, float(parts[1]), 0.0
    
    # Handle chromatic colors (e.g., "7.9R 5.2/20.4")
    try:
        # Split by space to get hue and value/chroma
        parts = notation.split(' ')
        if len(parts) != 2:
            return None, None, None, None
        
        hue_part = parts[0]
        value_chroma = parts[1]
        
        # Extract hue number and family
        for i, char in enumerate(hue_part):
            if char.isalpha():
                hue_num = float(hue_part[:i])
                hue_family = hue_part[i:]
                break
        
        # Extract value and chroma
        value, chroma = value_chroma.split('/')
        return hue_family, hue_num, float(value), float(chroma)
    except:
        return None, None, None, None

def calculate_difference(python_notation, rust_notation):
    """Calculate the difference between Python and Rust results."""
    py_family, py_hue, py_value, py_chroma = parse_munsell(python_notation)
    rs_family, rs_hue, rs_value, rs_chroma = parse_munsell(rust_notation)
    
    if py_family is None or rs_family is None:
        return None, "Parse error"
    
    # Check if families match
    if py_family != rs_family:
        return None, f"Family mismatch: {py_family} vs {rs_family}"
    
    # Calculate numerical differences
    hue_diff = abs(py_hue - rs_hue) if py_hue is not None and rs_hue is not None else 0
    value_diff = abs(py_value - rs_value)
    chroma_diff = abs(py_chroma - rs_chroma)
    
    # Handle hue wraparound (e.g., 9.9 vs 0.1)
    if hue_diff > 5:
        hue_diff = 10 - hue_diff
    
    total_diff = hue_diff + value_diff + chroma_diff
    return total_diff, (hue_diff, value_diff, chroma_diff)

def main():
    print("=" * 80)
    print("FULL-SCALE VALIDATION: Python colour-science vs Rust MunsellSpace")
    print("=" * 80)
    
    # Load reference dataset
    csv_path = 'tests/data/srgb-to-munsell.csv'
    colors = []
    
    print(f"\nLoading reference dataset from {csv_path}...")
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors.append((r, g, b, expected))
    
    print(f"Loaded {len(colors)} colors for validation")
    
    # Build Rust binary in release mode
    print("\nBuilding Rust binary in release mode...")
    subprocess.run(['cargo', 'build', '--release', '--bin', 'mathematical_convert_rgb'], 
                   capture_output=True)
    
    # Statistics
    exact_matches = 0
    close_matches = 0  # Within 0.5 total difference
    good_matches = 0   # Within 1.0 total difference
    mismatches = 0
    errors = 0
    
    differences = []
    error_cases = []
    mismatch_cases = []
    
    print("\nStarting validation (this may take a few minutes)...")
    print("Progress: ", end="", flush=True)
    
    start_time = time.time()
    
    for i, (r, g, b, expected) in enumerate(colors):
        # Progress indicator
        if i % 100 == 0:
            print(f"{i//100}", end="", flush=True)
        
        # Convert with both implementations
        python_result = convert_rgb_python(r, g, b)
        rust_result = convert_rgb_rust(r, g, b)
        
        if rust_result is None or rust_result.startswith("ERROR") or rust_result == "TIMEOUT":
            errors += 1
            error_cases.append((r, g, b, expected, rust_result))
            continue
        
        # Compare results
        total_diff, components = calculate_difference(python_result, rust_result)
        
        if total_diff is None:
            mismatches += 1
            mismatch_cases.append((r, g, b, python_result, rust_result, components))
        else:
            differences.append(total_diff)
            hue_diff, value_diff, chroma_diff = components
            
            if total_diff < 0.001:
                exact_matches += 1
            elif total_diff <= 0.5:
                close_matches += 1
            elif total_diff <= 1.0:
                good_matches += 1
            else:
                mismatches += 1
                mismatch_cases.append((r, g, b, python_result, rust_result, 
                                     f"Δh={hue_diff:.2f}, Δv={value_diff:.2f}, Δc={chroma_diff:.2f}"))
    
    elapsed = time.time() - start_time
    
    # Print results
    print(f"\n\n{'='*80}")
    print("VALIDATION RESULTS")
    print(f"{'='*80}")
    
    print(f"\nTotal colors tested: {len(colors)}")
    print(f"Time elapsed: {elapsed:.2f} seconds ({len(colors)/elapsed:.1f} colors/sec)")
    
    print(f"\nAccuracy breakdown:")
    print(f"  Exact matches (Δ < 0.001):  {exact_matches:4d} ({100*exact_matches/len(colors):.2f}%)")
    print(f"  Close matches (Δ ≤ 0.5):    {close_matches:4d} ({100*close_matches/len(colors):.2f}%)")
    print(f"  Good matches (Δ ≤ 1.0):     {good_matches:4d} ({100*good_matches/len(colors):.2f}%)")
    print(f"  Poor matches (Δ > 1.0):     {mismatches:4d} ({100*mismatches/len(colors):.2f}%)")
    print(f"  Errors/timeouts:            {errors:4d} ({100*errors/len(colors):.2f}%)")
    
    total_accurate = exact_matches + close_matches + good_matches
    print(f"\nTotal accurate (Δ ≤ 1.0):   {total_accurate:4d} ({100*total_accurate/len(colors):.2f}%)")
    
    if differences:
        print(f"\nDifference statistics:")
        print(f"  Mean difference:   {np.mean(differences):.4f}")
        print(f"  Median difference: {np.median(differences):.4f}")
        print(f"  Std deviation:     {np.std(differences):.4f}")
        print(f"  Min difference:    {np.min(differences):.4f}")
        print(f"  Max difference:    {np.max(differences):.4f}")
    
    # Show some examples of mismatches
    if mismatch_cases:
        print(f"\n{'='*80}")
        print(f"EXAMPLES OF LARGEST MISMATCHES (showing first 10)")
        print(f"{'='*80}")
        # Sort by difference magnitude
        mismatch_cases.sort(key=lambda x: sum(parse_munsell(x[3])[1:]) if parse_munsell(x[3])[0] else 999)
        for r, g, b, py_result, rs_result, diff_info in mismatch_cases[:10]:
            print(f"\nRGB({r},{g},{b}):")
            print(f"  Python:  {py_result}")
            print(f"  Rust:    {rs_result}")
            print(f"  Diff:    {diff_info}")
    
    if error_cases:
        print(f"\n{'='*80}")
        print(f"ERROR CASES (showing first 5)")
        print(f"{'='*80}")
        for r, g, b, expected, error in error_cases[:5]:
            print(f"RGB({r},{g},{b}): {error}")
    
    # Save detailed results to CSV
    output_file = f"validation_results_{int(time.time())}.csv"
    print(f"\n{'='*80}")
    print(f"Saving detailed results to {output_file}...")
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Python Result', 'Rust Result', 
                        'Hue Diff', 'Value Diff', 'Chroma Diff', 'Total Diff'])
        
        for r, g, b, expected in colors:
            python_result = convert_rgb_python(r, g, b)
            rust_result = convert_rgb_rust(r, g, b)
            
            if rust_result and not rust_result.startswith("ERROR"):
                total_diff, components = calculate_difference(python_result, rust_result)
                if total_diff is not None:
                    hue_diff, value_diff, chroma_diff = components
                    writer.writerow([r, g, b, python_result, rust_result, 
                                   hue_diff, value_diff, chroma_diff, total_diff])
                else:
                    writer.writerow([r, g, b, python_result, rust_result, 
                                   'N/A', 'N/A', 'N/A', 'N/A'])
            else:
                writer.writerow([r, g, b, python_result, rust_result or 'ERROR', 
                               'N/A', 'N/A', 'N/A', 'N/A'])
    
    print(f"Detailed results saved to {output_file}")
    print(f"\n{'='*80}")
    print("VALIDATION COMPLETE!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()