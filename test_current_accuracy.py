#!/usr/bin/env python3
"""Test current accuracy of Rust implementation vs Python"""

import subprocess
import json
from colour.notation import munsell

# Test colors from reference dataset
test_colors = [
    ([255, 0, 0], "7.5R 5.1/15.8"),    # Pure red
    ([0, 255, 0], "9.9GY 8.7/19.4"),    # Pure green  
    ([0, 0, 255], "7.5PB 3.3/39.5"),    # Pure blue
    ([255, 255, 0], "5Y 8.9/13.7"),     # Yellow
    ([255, 0, 255], "2.7RP 5.6/23.5"),  # Magenta
    ([0, 255, 255], "5BG 7.7/10.8"),    # Cyan
    ([128, 128, 128], "N5.5"),          # Grey
    ([255, 128, 0], "5.9YR 6.7/13.2"),  # Orange
    ([100, 150, 200], "5.1PB 6.2/9.8"), # Light blue
    ([200, 100, 150], "10RP 5.5/10.1"), # Pink
]

def rgb_to_srgb_normalized(rgb):
    """Convert 0-255 RGB to 0-1 sRGB"""
    return [c / 255.0 for c in rgb]

def test_python_conversion(rgb):
    """Test Python conversion"""
    srgb = rgb_to_srgb_normalized(rgb)
    
    # Convert to XYZ (D65)
    from colour import sRGB_to_XYZ
    xyz = sRGB_to_XYZ(srgb)
    
    # Convert to xyY
    from colour import XYZ_to_xyY
    xyy = XYZ_to_xyY(xyz)
    
    # Convert to Munsell
    try:
        result = munsell.xyY_to_munsell_colour(xyy)
        return result
    except Exception as e:
        return f"Error: {e}"

def test_rust_conversion(rgb):
    """Test Rust conversion using our binary"""
    try:
        # Run Rust binary
        result = subprocess.run(
            ["cargo", "run", "--bin", "test_simple_colors", "--", 
             str(rgb[0]), str(rgb[1]), str(rgb[2])],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Parse output - look for Munsell notation
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if "Munsell:" in line or "→" in line:
                    # Extract Munsell notation from line
                    parts = line.split("→")[-1].strip() if "→" in line else line.split(":")[-1].strip()
                    return parts
            return "No Munsell output found"
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"

def main():
    print("="*80)
    print("TESTING RUST vs PYTHON CONVERSION ACCURACY")
    print("="*80)
    
    exact_matches = 0
    close_matches = 0
    total = len(test_colors)
    
    for rgb, expected in test_colors:
        print(f"\nRGB {rgb}:")
        print(f"  Expected:  {expected}")
        
        # Test Python
        python_result = test_python_conversion(rgb)
        print(f"  Python:    {python_result}")
        
        # Test Rust
        rust_result = test_rust_conversion(rgb)
        print(f"  Rust:      {rust_result}")
        
        # Compare results
        if python_result == rust_result:
            print(f"  ✓ EXACT MATCH")
            exact_matches += 1
        elif isinstance(python_result, str) and isinstance(rust_result, str):
            # Try to compare numerically if both are valid Munsell notations
            try:
                python_spec = munsell.munsell_colour_to_munsell_specification(python_result)
                rust_spec = munsell.munsell_colour_to_munsell_specification(rust_result)
                
                # Check if within tolerance
                hue_diff = abs(python_spec[0] - rust_spec[0]) if not np.isnan(python_spec[0]) else 0
                value_diff = abs(python_spec[1] - rust_spec[1])
                chroma_diff = abs(python_spec[2] - rust_spec[2]) if not np.isnan(python_spec[2]) else 0
                
                if hue_diff <= 0.1 and value_diff <= 0.1 and chroma_diff <= 0.1:
                    print(f"  ≈ CLOSE MATCH (Δhue={hue_diff:.3f}, Δvalue={value_diff:.3f}, Δchroma={chroma_diff:.3f})")
                    close_matches += 1
                else:
                    print(f"  ✗ MISMATCH (Δhue={hue_diff:.3f}, Δvalue={value_diff:.3f}, Δchroma={chroma_diff:.3f})")
            except:
                print(f"  ✗ MISMATCH")
        else:
            print(f"  ✗ MISMATCH")
    
    print("\n" + "="*80)
    print(f"RESULTS: {exact_matches}/{total} exact matches, {close_matches}/{total} close matches")
    print(f"Accuracy: {100*exact_matches/total:.1f}% exact, {100*(exact_matches+close_matches)/total:.1f}% within tolerance")
    print("="*80)

if __name__ == "__main__":
    import numpy as np
    main()