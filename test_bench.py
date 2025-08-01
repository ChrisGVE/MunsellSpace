#!/usr/bin/env python3
"""
Rigorous Test Bench: Python colour-science vs Rust MunsellSpace

This script performs a comprehensive comparison between Python colour-science library
and our Rust implementation on both random RGB colors and the 4007 reference colors.

The key insight: If our Rust system is truly doing mathematical conversion, it should
work on random RGB colors that are NOT in the reference table. If it's just doing
lookup table matching, it will fail or give very different results on random colors.

Usage:
    python test_bench.py <num_random_samples>
    
Example:
    python test_bench.py 100    # Test 100 random colors + all 4007 reference colors
"""

import sys
import csv
import random
import subprocess
import json
import numpy as np
from pathlib import Path

# Import colour-science library
try:
    import colour
    from colour import RGB_to_XYZ, XYZ_to_xyY
    from colour.notation import xyY_to_munsell_colour
    print(f"✅ colour-science library version: {colour.__version__}")
except ImportError as e:
    print(f"❌ ERROR: colour-science library not available: {e}")
    print("Please run in the virtual environment: source venv_comparison/bin/activate")
    sys.exit(1)

def generate_random_rgb_colors(num_samples):
    """Generate random RGB colors that are likely NOT in the reference table."""
    random.seed(42)  # For reproducible results
    colors = []
    
    for i in range(num_samples):
        # Generate truly random RGB values
        r = random.randint(0, 255)
        g = random.randint(0, 255) 
        b = random.randint(0, 255)
        colors.append((r, g, b))
    
    return colors

def load_4007_reference_colors():
    """Load the 4007 reference colors from the CSV file."""
    reference_colors = []
    
    csv_path = Path("tests/data/srgb-to-munsell.csv")
    if not csv_path.exists():
        print(f"❌ ERROR: Reference file not found: {csv_path}")
        return []
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        for row in reader:
            if len(row) >= 4:
                r = int(row[0].strip())
                g = int(row[1].strip()) 
                b = int(row[2].strip())
                reference_munsell = row[3].strip()
                reference_colors.append((r, g, b, reference_munsell))
    
    print(f"📂 Loaded {len(reference_colors)} reference colors")
    return reference_colors

def python_munsell_conversion(rgb):
    """Convert RGB to Munsell using Python colour-science library."""
    try:
        # Convert to 0-1 range
        rgb_normalized = np.array(rgb) / 255.0
        
        # sRGB → XYZ using D65 illuminant
        xyz = RGB_to_XYZ(
            rgb_normalized,
            colour.RGB_COLOURSPACES['sRGB'].whitepoint,
            colour.RGB_COLOURSPACES['sRGB'].whitepoint,
            colour.RGB_COLOURSPACES['sRGB'].matrix_RGB_to_XYZ
        )
        
        # XYZ → xyY
        xyy = XYZ_to_xyY(xyz)
        
        # xyY → Munsell
        munsell_spec = xyY_to_munsell_colour(xyy)
        
        return {
            'success': True,
            'munsell': munsell_spec,
            'xyz': xyz.tolist(),
            'xyy': xyy.tolist(),
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'munsell': None,
            'xyz': None,
            'xyy': None,
            'error': str(e)
        }

def rust_munsell_conversion(rgb):
    """Convert RGB to Munsell using our Rust implementation."""
    try:
        # Call our Rust binary
        result = subprocess.run(
            ["cargo", "run", "--bin", "convert_rgb", "--", str(rgb[0]), str(rgb[1]), str(rgb[2])],
            capture_output=True, text=True, cwd="."
        )
        
        if result.returncode == 0:
            munsell_str = result.stdout.strip()
            return {
                'success': True,
                'munsell': munsell_str,
                'error': None
            }
        else:
            error_msg = result.stderr.strip() or "Unknown error"
            return {
                'success': False,
                'munsell': None,
                'error': error_msg
            }
            
    except Exception as e:
        return {
            'success': False,
            'munsell': None,
            'error': str(e)
        }

def parse_munsell_components(munsell_str):
    """Parse Munsell string into components."""
    if not munsell_str or munsell_str == "CONVERSION_FAILED":
        return None, None, None, None
        
    try:
        # Handle neutral colors
        if munsell_str.startswith("N "):
            value_str = munsell_str.replace("N ", "").strip()
            return 0.0, "N", float(value_str), 0.0
        
        # Parse "5.9R 8.1/5.5" format
        parts = munsell_str.split()
        if len(parts) != 2:
            return None, None, None, None
            
        # Parse hue (e.g., "5.9R")
        hue_part = parts[0]
        hue_family_start = 0
        for i, c in enumerate(hue_part):
            if c.isalpha():
                hue_family_start = i
                break
        
        hue_number = float(hue_part[:hue_family_start])
        hue_family = hue_part[hue_family_start:]
        
        # Parse value/chroma (e.g., "8.1/5.5")
        value_chroma = parts[1].split('/')
        value = float(value_chroma[0])
        chroma = float(value_chroma[1]) if len(value_chroma) > 1 else 0.0
        
        return hue_number, hue_family, value, chroma
        
    except:
        return None, None, None, None

def calculate_munsell_difference(munsell1, munsell2):
    """Calculate difference between two Munsell colors."""
    if not munsell1 or not munsell2:
        return None, None, None
        
    h1, f1, v1, c1 = parse_munsell_components(munsell1)
    h2, f2, v2, c2 = parse_munsell_components(munsell2)
    
    if None in [h1, f1, v1, c1, h2, f2, v2, c2]:
        return None, None, None
    
    # Hue difference (circular)
    families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"]
    f1_idx = families.index(f1) if f1 in families else 0
    f2_idx = families.index(f2) if f2 in families else 0
    
    pos1 = f1_idx * 10.0 + h1
    pos2 = f2_idx * 10.0 + h2
    
    hue_diff = pos1 - pos2
    if abs(hue_diff) > 50.0:
        hue_diff = hue_diff - 100.0 if hue_diff > 0 else hue_diff + 100.0
    
    return hue_diff, v1 - v2, c1 - c2

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_bench.py <num_random_samples>")
        print("Example: python test_bench.py 100")
        sys.exit(1)
    
    try:
        num_random = int(sys.argv[1])
    except ValueError:
        print("Error: num_random_samples must be an integer")
        sys.exit(1)
    
    print("🔬 RIGOROUS TEST BENCH: Python vs Rust Munsell Conversion")
    print("=" * 60)
    print(f"Testing {num_random} random colors + 4007 reference colors")
    print("This will reveal if our Rust system uses true math or lookup tables")
    
    # Generate test data
    print("\n📊 Generating test data...")
    random_colors = generate_random_rgb_colors(num_random)
    reference_colors = load_4007_reference_colors()
    
    # Create output CSV
    output_file = f"rigorous_comparison_{num_random}_random.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'source', 'r', 'g', 'b',
            'python_munsell', 'python_hue_num', 'python_hue_family', 'python_value', 'python_chroma', 'python_success',
            'rust_munsell', 'rust_hue_num', 'rust_hue_family', 'rust_value', 'rust_chroma', 'rust_success',
            'reference_munsell', 'reference_hue_num', 'reference_hue_family', 'reference_value', 'reference_chroma',
            'hue_diff_py_rust', 'value_diff_py_rust', 'chroma_diff_py_rust',
            'match_type', 'analysis'
        ])
        
        total_tests = len(random_colors) + len(reference_colors)
        processed = 0
        
        print(f"\n🧪 Testing {len(random_colors)} random colors...")
        
        # Test random colors
        for rgb in random_colors:
            processed += 1
            if processed % 50 == 0:
                print(f"  Progress: {processed}/{total_tests}")
            
            # Convert with both systems
            python_result = python_munsell_conversion(rgb)
            rust_result = rust_munsell_conversion(rgb)
            
            # Parse results
            py_h, py_f, py_v, py_c = parse_munsell_components(python_result['munsell']) if python_result['success'] else (None, None, None, None)
            rust_h, rust_f, rust_v, rust_c = parse_munsell_components(rust_result['munsell']) if rust_result['success'] else (None, None, None, None)
            
            # Calculate differences
            if python_result['success'] and rust_result['success']:
                hue_diff, value_diff, chroma_diff = calculate_munsell_difference(
                    python_result['munsell'], rust_result['munsell'])
                
                if python_result['munsell'] == rust_result['munsell']:
                    match_type = "EXACT_MATCH"
                    analysis = "Perfect agreement between systems"
                elif hue_diff is not None and abs(hue_diff) < 2.0 and abs(value_diff) < 0.5 and abs(chroma_diff) < 1.0:
                    match_type = "CLOSE_MATCH"
                    analysis = "Minor differences within tolerance"
                elif hue_diff is not None and abs(hue_diff) > 10.0:
                    match_type = "MAJOR_HUE_DIFF"
                    analysis = f"Major hue difference: {hue_diff:.1f} points"
                else:
                    match_type = "DIFFERENT"
                    analysis = "Significant differences detected"
            else:
                hue_diff = value_diff = chroma_diff = None
                if not python_result['success'] and not rust_result['success']:
                    match_type = "BOTH_FAILED"
                    analysis = "Both systems failed conversion"
                elif not python_result['success']:
                    match_type = "PYTHON_FAILED"
                    analysis = f"Python failed: {python_result['error']}"
                else:
                    match_type = "RUST_FAILED"
                    analysis = f"Rust failed: {rust_result['error']}"
            
            # Write row
            writer.writerow([
                'random', rgb[0], rgb[1], rgb[2],
                python_result['munsell'] if python_result['success'] else 'FAILED',
                py_h, py_f, py_v, py_c, python_result['success'],
                rust_result['munsell'] if rust_result['success'] else 'FAILED',
                rust_h, rust_f, rust_v, rust_c, rust_result['success'],
                '', '', '', '', '',  # No reference for random colors
                hue_diff, value_diff, chroma_diff,
                match_type, analysis
            ])
        
        print(f"\n🔍 Testing {len(reference_colors)} reference colors...")
        
        # Test reference colors
        for rgb_ref in reference_colors:
            processed += 1
            if processed % 200 == 0:
                print(f"  Progress: {processed}/{total_tests}")
                
            rgb = (rgb_ref[0], rgb_ref[1], rgb_ref[2])
            reference_munsell = rgb_ref[3]
            
            # Convert with both systems
            python_result = python_munsell_conversion(rgb)
            rust_result = rust_munsell_conversion(rgb)
            
            # Parse results
            py_h, py_f, py_v, py_c = parse_munsell_components(python_result['munsell']) if python_result['success'] else (None, None, None, None)
            rust_h, rust_f, rust_v, rust_c = parse_munsell_components(rust_result['munsell']) if rust_result['success'] else (None, None, None, None)
            ref_h, ref_f, ref_v, ref_c = parse_munsell_components(reference_munsell)
            
            # Calculate differences
            if python_result['success'] and rust_result['success']:
                hue_diff, value_diff, chroma_diff = calculate_munsell_difference(
                    python_result['munsell'], rust_result['munsell'])
                    
                if rust_result['munsell'] == reference_munsell:
                    match_type = "RUST_MATCHES_REF"
                    analysis = "Rust matches reference exactly"
                elif python_result['munsell'] == reference_munsell:
                    match_type = "PYTHON_MATCHES_REF"
                    analysis = "Python matches reference exactly"
                elif python_result['munsell'] == rust_result['munsell']:
                    match_type = "PY_RUST_AGREE"
                    analysis = "Python and Rust agree (both differ from reference)"
                else:
                    match_type = "ALL_DIFFERENT"
                    analysis = "All three results are different"
            else:
                hue_diff = value_diff = chroma_diff = None
                match_type = "CONVERSION_ISSUES"
                analysis = "One or both conversions failed"
            
            # Write row
            writer.writerow([
                'reference', rgb[0], rgb[1], rgb[2],
                python_result['munsell'] if python_result['success'] else 'FAILED',
                py_h, py_f, py_v, py_c, python_result['success'],
                rust_result['munsell'] if rust_result['success'] else 'FAILED', 
                rust_h, rust_f, rust_v, rust_c, rust_result['success'],
                reference_munsell, ref_h, ref_f, ref_v, ref_c,
                hue_diff, value_diff, chroma_diff,
                match_type, analysis
            ])
    
    print(f"\n✅ Test completed! Results saved to: {output_file}")
    print(f"\n🔍 ANALYSIS SUMMARY:")
    print(f"This rigorous test will reveal:")
    print(f"1. Whether our Rust system works on random colors (true math vs lookup)")
    print(f"2. How Python vs Rust compare on the same inputs")
    print(f"3. Which system is more accurate against the 4007 reference")
    print(f"4. The nature of any systematic differences")
    
    print(f"\n📊 Open {output_file} to analyze the results!")

if __name__ == "__main__":
    main()