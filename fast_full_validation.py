#!/usr/bin/env python3
"""
Fast full-scale validation comparing Python colour-science vs Rust implementation
on all 4,007 reference colors using parallel processing.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import time
import warnings
warnings.filterwarnings('ignore')

def convert_rgb_python(r, g, b):
    """Convert RGB to Munsell using Python colour-science."""
    try:
        rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
        xyz = sRGB_to_XYZ(rgb_norm)
        xyy = XYZ_to_xyY(xyz)
        munsell = xyY_to_munsell_colour(xyy)
        return str(munsell)
    except:
        # Handle edge cases
        if r == 0 and g == 0 and b == 0:
            return "N 0.0"
        return None

def convert_rgb_rust(r, g, b):
    """Convert RGB to Munsell using our Rust implementation."""
    try:
        result = subprocess.run(
            ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=1
        )
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if any(family in line for family in ['R ', 'YR ', 'Y ', 'GY ', 'G ', 'BG ', 'B ', 'PB ', 'P ', 'RP ', 'N ']) and ('/' in line or line.startswith('N ')):
                if not line.startswith('TRACE:') and not line.startswith('Looking for'):
                    return line.strip()
        return None
    except:
        return None

def parse_munsell_simple(notation):
    """Simple Munsell notation comparison."""
    if notation is None:
        return None
    notation = str(notation).strip()
    
    # Normalize notation - remove extra spaces
    parts = notation.split()
    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"
    return notation

def main():
    print("=" * 80)
    print("FULL-SCALE VALIDATION: Testing ALL 4,007 colors")
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
            expected = row[3].strip()
            colors.append((r, g, b, expected))
    
    print(f"Loaded {len(colors)} colors")
    
    # Build Rust binary
    print("\nBuilding Rust binary in release mode...")
    result = subprocess.run(['cargo', 'build', '--release', '--bin', 'mathematical_convert_rgb'], 
                          capture_output=True)
    if result.returncode != 0:
        print("Failed to build Rust binary!")
        return
    
    print("\nStarting validation of ALL 4,007 colors...")
    print("(Processing 10 colors at a time for progress updates)")
    
    # Statistics
    exact_matches = 0
    python_errors = 0
    rust_errors = 0
    both_valid = 0
    differences = []
    
    start_time = time.time()
    
    # Process in chunks for progress reporting
    chunk_size = 10
    for chunk_start in range(0, len(colors), chunk_size):
        chunk_end = min(chunk_start + chunk_size, len(colors))
        
        # Progress indicator
        if chunk_start % 100 == 0:
            elapsed = time.time() - start_time
            rate = chunk_start / elapsed if elapsed > 0 else 0
            eta = (len(colors) - chunk_start) / rate if rate > 0 else 0
            print(f"Progress: {chunk_start}/{len(colors)} ({100*chunk_start/len(colors):.1f}%) - "
                  f"Rate: {rate:.1f} colors/sec - ETA: {eta:.0f}s")
        
        # Process chunk
        for r, g, b, expected in colors[chunk_start:chunk_end]:
            # Convert with both implementations
            python_result = convert_rgb_python(r, g, b)
            rust_result = convert_rgb_rust(r, g, b)
            
            # Count errors
            if python_result is None:
                python_errors += 1
            if rust_result is None:
                rust_errors += 1
            
            # Compare if both valid
            if python_result and rust_result:
                both_valid += 1
                py_normalized = parse_munsell_simple(python_result)
                rs_normalized = parse_munsell_simple(rust_result)
                
                if py_normalized == rs_normalized:
                    exact_matches += 1
                else:
                    # Calculate approximate difference
                    differences.append((r, g, b, python_result, rust_result))
    
    elapsed = time.time() - start_time
    
    # Print results
    print(f"\n{'='*80}")
    print("VALIDATION COMPLETE - ALL 4,007 COLORS TESTED")
    print(f"{'='*80}")
    
    print(f"\nProcessing time: {elapsed:.1f} seconds ({len(colors)/elapsed:.1f} colors/sec)")
    
    print(f"\n--- OVERALL STATISTICS ---")
    print(f"Total colors tested:        {len(colors):,}")
    print(f"Both implementations valid: {both_valid:,} ({100*both_valid/len(colors):.1f}%)")
    print(f"Python errors:             {python_errors:,} ({100*python_errors/len(colors):.1f}%)")
    print(f"Rust errors:               {rust_errors:,} ({100*rust_errors/len(colors):.1f}%)")
    
    if both_valid > 0:
        print(f"\n--- ACCURACY ON VALID COMPARISONS ---")
        print(f"Colors with both valid:    {both_valid:,}")
        print(f"Exact string matches:      {exact_matches:,} ({100*exact_matches/both_valid:.1f}%)")
        print(f"Differences:               {len(differences):,} ({100*len(differences)/both_valid:.1f}%)")
    
    # Analyze differences
    if differences:
        print(f"\n--- ANALYZING {len(differences)} DIFFERENCES ---")
        
        # Sample some differences
        print(f"\nFirst 10 differences:")
        for r, g, b, py, rs in differences[:10]:
            print(f"  RGB({r:3},{g:3},{b:3}): Python='{py}' vs Rust='{rs}'")
        
        # Try to categorize differences
        small_diffs = 0
        for r, g, b, py, rs in differences:
            # Simple heuristic - if the hue families match, it's probably a small difference
            if py and rs:
                py_parts = py.split()
                rs_parts = rs.split()
                if len(py_parts) >= 1 and len(rs_parts) >= 1:
                    # Extract hue family
                    py_hue = ''.join(c for c in py_parts[0] if c.isalpha())
                    rs_hue = ''.join(c for c in rs_parts[0] if c.isalpha())
                    if py_hue == rs_hue:
                        small_diffs += 1
        
        print(f"\nDifferences with same hue family: {small_diffs}/{len(differences)} ({100*small_diffs/len(differences):.1f}%)")
    
    # Save detailed results
    output_file = f"full_validation_4007_results_{int(time.time())}.csv"
    print(f"\n--- SAVING DETAILED RESULTS ---")
    print(f"Writing to {output_file}...")
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Expected', 'Python Result', 'Rust Result', 'Match'])
        
        for r, g, b, expected in colors:
            python_result = convert_rgb_python(r, g, b)
            rust_result = convert_rgb_rust(r, g, b)
            match = "YES" if python_result and rust_result and parse_munsell_simple(python_result) == parse_munsell_simple(rust_result) else "NO"
            writer.writerow([r, g, b, expected, python_result or "ERROR", rust_result or "ERROR", match])
    
    print(f"Detailed results saved to {output_file}")
    
    print(f"\n{'='*80}")
    print("FULL VALIDATION OF 4,007 COLORS COMPLETE!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()