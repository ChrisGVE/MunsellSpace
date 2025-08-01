#!/usr/bin/env python3
"""
Fast Test Bench: Python colour-science vs Rust MunsellSpace

Optimized version for quick testing with configurable samples.
"""

import sys
import csv
import random
import subprocess
import numpy as np
from pathlib import Path

# Import colour-science library
try:
    import colour
    from colour import RGB_to_XYZ, XYZ_to_xyY
    from colour.notation import xyY_to_munsell_colour
except ImportError as e:
    print(f"❌ ERROR: colour-science library not available: {e}")
    sys.exit(1)

def generate_random_rgb_colors(num_samples):
    """Generate random RGB colors."""
    random.seed(42)  # For reproducible results
    return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_samples)]

def load_sample_reference_colors(num_samples=100):
    """Load a sample of reference colors."""
    reference_colors = []
    csv_path = Path("tests/data/srgb-to-munsell.csv")
    
    if not csv_path.exists():
        print(f"❌ ERROR: Reference file not found: {csv_path}")
        return []
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        for i, row in enumerate(reader):
            if i >= num_samples:  # Limit samples for speed
                break
            if len(row) >= 4:
                r, g, b = int(row[0].strip()), int(row[1].strip()), int(row[2].strip())
                reference_munsell = row[3].strip()
                reference_colors.append((r, g, b, reference_munsell))
    
    return reference_colors

def python_munsell_conversion(rgb):
    """Convert RGB to Munsell using Python colour-science library."""
    try:
        rgb_normalized = np.array(rgb) / 255.0
        xyz = RGB_to_XYZ(rgb_normalized, colour.RGB_COLOURSPACES['sRGB'].whitepoint,
                        colour.RGB_COLOURSPACES['sRGB'].whitepoint,
                        colour.RGB_COLOURSPACES['sRGB'].matrix_RGB_to_XYZ)
        xyy = XYZ_to_xyY(xyz)
        munsell_spec = xyY_to_munsell_colour(xyy)
        return {'success': True, 'munsell': munsell_spec, 'error': None}
    except Exception as e:
        return {'success': False, 'munsell': None, 'error': str(e)[:100]}

def rust_munsell_conversion(rgb):
    """Convert RGB to Munsell using our Rust implementation."""
    try:
        result = subprocess.run(
            ["cargo", "run", "--release", "--bin", "convert_rgb", "--", str(rgb[0]), str(rgb[1]), str(rgb[2])],
            capture_output=True, text=True, cwd=".", timeout=30
        )
        
        if result.returncode == 0:
            return {'success': True, 'munsell': result.stdout.strip(), 'error': None}
        else:
            return {'success': False, 'munsell': None, 'error': result.stderr.strip()[:100]}
    except Exception as e:
        return {'success': False, 'munsell': None, 'error': str(e)[:100]}

def main():
    if len(sys.argv) != 2:
        print("Usage: python fast_test_bench.py <num_random_samples>")
        print("Example: python fast_test_bench.py 50")
        sys.exit(1)

    num_random = int(sys.argv[1])
    print(f"🔬 FAST TEST BENCH: {num_random} random + {min(100, num_random)} reference colors")
    
    # Generate test data
    random_colors = generate_random_rgb_colors(num_random)
    reference_colors = load_sample_reference_colors(min(100, num_random))
    
    output_file = f"fast_comparison_{num_random}.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'r', 'g', 'b', 'python_munsell', 'python_success', 
                        'rust_munsell', 'rust_success', 'reference_munsell', 'match_analysis'])
        
        print(f"Testing {num_random} random colors...")
        random_exact_matches = 0
        random_both_success = 0
        
        # Test random colors
        for i, rgb in enumerate(random_colors):
            if (i + 1) % 10 == 0:
                print(f"  Random: {i + 1}/{num_random}")
                
            python_result = python_munsell_conversion(rgb)
            rust_result = rust_munsell_conversion(rgb)
            
            if python_result['success'] and rust_result['success']:
                random_both_success += 1
                if python_result['munsell'] == rust_result['munsell']:
                    random_exact_matches += 1
                    analysis = "EXACT_MATCH"
                else:
                    analysis = "DIFFERENT_ALGORITHMS"
            else:
                analysis = "CONVERSION_FAILED"
            
            writer.writerow(['random', rgb[0], rgb[1], rgb[2],
                           python_result['munsell'] if python_result['success'] else 'FAILED',
                           python_result['success'],
                           rust_result['munsell'] if rust_result['success'] else 'FAILED', 
                           rust_result['success'], '', analysis])
        
        print(f"Testing {len(reference_colors)} reference colors...")
        ref_rust_matches = 0
        ref_python_matches = 0
        ref_both_success = 0
        
        # Test reference colors
        for i, (r, g, b, ref_munsell) in enumerate(reference_colors):
            if (i + 1) % 20 == 0:
                print(f"  Reference: {i + 1}/{len(reference_colors)}")
                
            rgb = (r, g, b)
            python_result = python_munsell_conversion(rgb)
            rust_result = rust_munsell_conversion(rgb)
            
            if python_result['success'] and rust_result['success']:
                ref_both_success += 1
                
            if rust_result['success'] and rust_result['munsell'] == ref_munsell:
                ref_rust_matches += 1
                analysis = "RUST_MATCHES_REF"
            elif python_result['success'] and python_result['munsell'] == ref_munsell:
                ref_python_matches += 1
                analysis = "PYTHON_MATCHES_REF"
            elif (python_result['success'] and rust_result['success'] and 
                  python_result['munsell'] == rust_result['munsell']):
                analysis = "PY_RUST_AGREE"
            else:
                analysis = "ALL_DIFFERENT"
            
            writer.writerow(['reference', r, g, b,
                           python_result['munsell'] if python_result['success'] else 'FAILED',
                           python_result['success'],
                           rust_result['munsell'] if rust_result['success'] else 'FAILED',
                           rust_result['success'], ref_munsell, analysis])
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"Random Colors ({num_random} tested):")
    print(f"  Both systems succeeded: {random_both_success}/{num_random} ({100*random_both_success/num_random:.1f}%)")
    print(f"  Exact matches: {random_exact_matches}/{random_both_success} ({100*random_exact_matches/max(1,random_both_success):.1f}%)")
    
    print(f"\nReference Colors ({len(reference_colors)} tested):")
    print(f"  Rust matches reference: {ref_rust_matches}/{len(reference_colors)} ({100*ref_rust_matches/len(reference_colors):.1f}%)")
    print(f"  Python matches reference: {ref_python_matches}/{len(reference_colors)} ({100*ref_python_matches/len(reference_colors):.1f}%)")
    
    print(f"\n🎯 KEY INSIGHTS:")
    if ref_rust_matches > ref_python_matches:
        print(f"  ✅ Rust system appears to use reference table lookup")
        print(f"  📊 Python system uses different mathematical conversion")
    
    if random_exact_matches == 0:
        print(f"  🔍 Systems give different results on non-reference colors")
        print(f"  💡 This confirms they use different algorithms/implementations")
    
    print(f"\n📁 Results saved to: {output_file}")

if __name__ == "__main__":
    main()