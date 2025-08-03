#!/usr/bin/env python3
"""
Analyze the differences between Python and Rust Munsell conversions.
Focus on colors where both produce valid results.
"""

import csv
import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings

def convert_rgb_python(r, g, b):
    """Convert RGB to Munsell using Python colour-science."""
    try:
        rgb_norm = np.array([r/255.0, g/255.0, b/255.0])
        xyz = sRGB_to_XYZ(rgb_norm)
        xyy = XYZ_to_xyY(xyz)
        munsell = xyY_to_munsell_colour(xyy)
        return munsell
    except Exception:
        return None

def convert_rgb_rust(r, g, b):
    """Convert RGB to Munsell using our Rust implementation."""
    try:
        result = subprocess.run(
            ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if any(family in line for family in ['R ', 'YR ', 'Y ', 'GY ', 'G ', 'BG ', 'B ', 'PB ', 'P ', 'RP ', 'N ']) and '/' in line:
                if not line.startswith('TRACE:') and not line.startswith('Looking for'):
                    return line.strip()
        return None
    except:
        return None

def parse_munsell(notation):
    """Parse Munsell notation into numeric components."""
    if not notation:
        return None
    
    notation = str(notation).strip()
    
    # Handle neutral colors
    if notation.startswith('N '):
        parts = notation.split()
        return {'family': 'N', 'hue': 0.0, 'value': float(parts[1]), 'chroma': 0.0}
    
    # Handle chromatic colors
    try:
        parts = notation.split(' ')
        if len(parts) != 2:
            return None
        
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
        return {
            'family': hue_family,
            'hue': hue_num,
            'value': float(value),
            'chroma': float(chroma)
        }
    except:
        return None

def analyze_difference(py_parsed, rs_parsed):
    """Analyze the numeric difference between two Munsell notations."""
    if not py_parsed or not rs_parsed:
        return None
    
    if py_parsed['family'] != rs_parsed['family']:
        return {'status': 'family_mismatch', 'py_family': py_parsed['family'], 'rs_family': rs_parsed['family']}
    
    hue_diff = abs(py_parsed['hue'] - rs_parsed['hue'])
    # Handle hue wraparound
    if hue_diff > 5:
        hue_diff = 10 - hue_diff
    
    return {
        'status': 'ok',
        'hue_diff': hue_diff,
        'value_diff': abs(py_parsed['value'] - rs_parsed['value']),
        'chroma_diff': abs(py_parsed['chroma'] - rs_parsed['chroma']),
        'total_diff': hue_diff + abs(py_parsed['value'] - rs_parsed['value']) + abs(py_parsed['chroma'] - rs_parsed['chroma'])
    }

def main():
    print("=" * 80)
    print("DIFFERENCE ANALYSIS: Python vs Rust Munsell Conversion")
    print("=" * 80)
    
    # Build Rust binary
    subprocess.run(['cargo', 'build', '--release', '--bin', 'mathematical_convert_rgb'], 
                   capture_output=True)
    
    # Test a range of colors
    test_colors = []
    
    # Add primary and secondary colors
    primaries = [
        (255, 0, 0, "Pure Red"),
        (0, 255, 0, "Pure Green"),
        (0, 0, 255, "Pure Blue"),
        (255, 255, 0, "Yellow"),
        (255, 0, 255, "Magenta"),
        (0, 255, 255, "Cyan"),
    ]
    
    # Add some grays
    grays = [
        (64, 64, 64, "Dark Gray"),
        (128, 128, 128, "Medium Gray"),
        (192, 192, 192, "Light Gray"),
    ]
    
    # Add some real-world colors
    real_world = [
        (255, 165, 0, "Orange"),
        (128, 0, 128, "Purple"),
        (139, 69, 19, "Brown"),
        (255, 192, 203, "Pink"),
        (0, 128, 0, "Dark Green"),
        (255, 215, 0, "Gold"),
        (64, 224, 208, "Turquoise"),
        (255, 99, 71, "Tomato"),
        (147, 112, 219, "Medium Purple"),
        (255, 140, 0, "Dark Orange"),
    ]
    
    all_colors = primaries + grays + real_world
    
    valid_comparisons = []
    python_errors = []
    rust_errors = []
    
    print("\nTesting colors...")
    for r, g, b, name in all_colors:
        py_result = convert_rgb_python(r, g, b)
        rs_result = convert_rgb_rust(r, g, b)
        
        if py_result and rs_result:
            py_parsed = parse_munsell(py_result)
            rs_parsed = parse_munsell(rs_result)
            
            if py_parsed and rs_parsed:
                diff = analyze_difference(py_parsed, rs_parsed)
                if diff:
                    valid_comparisons.append({
                        'rgb': (r, g, b),
                        'name': name,
                        'python': py_result,
                        'rust': rs_result,
                        'diff': diff
                    })
        elif not py_result:
            python_errors.append((r, g, b, name))
        elif not rs_result:
            rust_errors.append((r, g, b, name))
    
    # Analyze results
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total colors tested: {len(all_colors)}")
    print(f"Valid comparisons: {len(valid_comparisons)}")
    print(f"Python errors: {len(python_errors)}")
    print(f"Rust errors: {len(rust_errors)}")
    
    if valid_comparisons:
        print(f"\n{'='*80}")
        print("VALID COMPARISONS (Both Python and Rust produced results)")
        print(f"{'='*80}")
        
        exact_matches = 0
        very_close = 0  # < 0.1 total difference
        close = 0       # < 0.5 total difference
        
        for comp in valid_comparisons:
            diff = comp['diff']
            if diff['status'] == 'ok':
                total = diff['total_diff']
                if total < 0.001:
                    exact_matches += 1
                elif total < 0.1:
                    very_close += 1
                elif total < 0.5:
                    close += 1
                
                print(f"\n{comp['name']} ({comp['rgb'][0]},{comp['rgb'][1]},{comp['rgb'][2]}):")
                print(f"  Python: {comp['python']}")
                print(f"  Rust:   {comp['rust']}")
                print(f"  Δhue={diff['hue_diff']:.3f}, Δvalue={diff['value_diff']:.3f}, Δchroma={diff['chroma_diff']:.3f}")
                print(f"  Total difference: {total:.3f}")
                
                if total < 0.001:
                    print("  Status: EXACT MATCH ✓")
                elif total < 0.1:
                    print("  Status: Very close")
                elif total < 0.5:
                    print("  Status: Close")
                else:
                    print("  Status: Different")
            else:
                print(f"\n{comp['name']}: Family mismatch - Python:{diff['py_family']} vs Rust:{diff['rs_family']}")
        
        print(f"\n{'='*80}")
        print("ACCURACY STATISTICS")
        print(f"{'='*80}")
        print(f"Exact matches: {exact_matches}/{len(valid_comparisons)} ({100*exact_matches/len(valid_comparisons):.1f}%)")
        print(f"Very close (<0.1): {very_close}/{len(valid_comparisons)} ({100*very_close/len(valid_comparisons):.1f}%)")
        print(f"Close (<0.5): {close}/{len(valid_comparisons)} ({100*close/len(valid_comparisons):.1f}%)")
        
        total_acceptable = exact_matches + very_close + close
        print(f"Total acceptable (<0.5): {total_acceptable}/{len(valid_comparisons)} ({100*total_acceptable/len(valid_comparisons):.1f}%)")
    
    if python_errors:
        print(f"\n{'='*80}")
        print("PYTHON ERRORS (Python couldn't convert these)")
        print(f"{'='*80}")
        for r, g, b, name in python_errors:
            rs_result = convert_rgb_rust(r, g, b)
            print(f"{name} ({r},{g},{b}): Rust gives {rs_result}")
    
    if rust_errors:
        print(f"\n{'='*80}")
        print("RUST ERRORS (Rust couldn't convert these)")
        print(f"{'='*80}")
        for r, g, b, name in rust_errors:
            py_result = convert_rgb_python(r, g, b)
            print(f"{name} ({r},{g},{b}): Python gives {py_result}")

if __name__ == "__main__":
    main()