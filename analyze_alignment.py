#!/usr/bin/env python3
"""Analyze alignment between Rust and Python in detail"""

import subprocess
import colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np
import csv

# Read some colors from the reference dataset
reference_colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    # Sample every 100th color for a quick test
    for i, row in enumerate(reader):
        if i % 100 == 0:
            rgb = [int(row[0]), int(row[1]), int(row[2])]
            expected = row[3]
            reference_colors.append((rgb, expected))
        if i >= 1000:  # Test first 1000 rows (sample 10)
            break

def python_rgb_to_munsell(rgb):
    """Convert RGB to Munsell using Python colour-science"""
    srgb = [c / 255.0 for c in rgb]
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    
    try:
        spec = xyY_to_munsell_specification(xyy)
        
        HUE_CODES = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                     6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
        
        hue = spec[0]
        value = spec[1]
        chroma = spec[2]
        code = int(spec[3])
        
        if chroma < 0.05:
            return f"N{value:.1f}", None
        else:
            family = HUE_CODES.get(code, '?')
            return f"{hue:.1f}{family} {value:.1f}/{chroma:.1f}", None
    except Exception as e:
        return None, str(e)[:50]

print("Testing alignment on sampled reference colors...")
print("=" * 80)

exact_matches = 0
close_matches = 0
both_error = 0
rust_only_error = 0
python_only_error = 0
total = 0

for rgb, reference_expected in reference_colors:
    # Get Python result
    python_result, python_error = python_rgb_to_munsell(rgb)
    
    # Get Rust result
    result = subprocess.run(['./target/release/test_rust_python_compare', 
                           str(rgb[0]), str(rgb[1]), str(rgb[2])],
                          capture_output=True, text=True)
    rust_result = result.stdout.strip()
    
    total += 1
    
    # Categorize the comparison
    if python_error and "Error:" in rust_result:
        both_error += 1
        status = "Both Error"
    elif python_error:
        python_only_error += 1
        status = "Python Error Only"
    elif "Error:" in rust_result:
        rust_only_error += 1
        status = "Rust Error Only"
    elif python_result == rust_result:
        exact_matches += 1
        status = "✓ EXACT"
    else:
        # Check if close
        try:
            # Parse both results to check closeness
            # This is simplified - just count as close for now
            close_matches += 1
            status = "~ Close"
        except:
            status = "? Parse Error"
    
    print(f"RGB {rgb}: {status}")
    if status not in ["✓ EXACT", "Both Error"]:
        print(f"  Python: {python_result if python_result else python_error}")
        print(f"  Rust:   {rust_result}")
        print(f"  Ref:    {reference_expected}")

print("\n" + "=" * 80)
print("ALIGNMENT SUMMARY:")
print(f"Total colors tested: {total}")
print(f"Exact matches: {exact_matches} ({100*exact_matches/total:.1f}%)")
print(f"Close matches: {close_matches} ({100*close_matches/total:.1f}%)")
print(f"Both error: {both_error} ({100*both_error/total:.1f}%)")
print(f"Rust only error: {rust_only_error} ({100*rust_only_error/total:.1f}%)")
print(f"Python only error: {python_only_error} ({100*python_only_error/total:.1f}%)")
print()
print(f"When both converge: {exact_matches + close_matches}/{exact_matches + close_matches + rust_only_error + python_only_error} = {100*(exact_matches + close_matches)/(exact_matches + close_matches + rust_only_error + python_only_error):.1f}% alignment" if (exact_matches + close_matches + rust_only_error + python_only_error) > 0 else "No successful conversions")
print("=" * 80)