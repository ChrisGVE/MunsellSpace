#!/usr/bin/env python3
"""
Analyze the gap between our simple Rust implementation and Python colour-science.
Test specific colors to understand what's missing.
"""

import subprocess
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def test_color(rgb):
    """Test a single color with both Rust and Python."""
    r, g, b = rgb
    
    # Test with Rust
    input_data = f"{r},{g},{b}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    rust_result = result.stdout.strip()
    
    # Test with Python
    try:
        # Normalize RGB to [0, 1] range
        rgb_norm = [r/255.0, g/255.0, b/255.0]
        
        # Convert sRGB to XYZ then to xyY
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        
        # Convert to Munsell
        munsell = xyY_to_munsell_colour(xyY)
        
        # Format Python result
        if munsell.startswith('N '):
            python_result = munsell
        else:
            # Parse and format to match Rust output
            parts = munsell.split(' ')
            if len(parts) == 2:
                hue_part = parts[0]
                value_chroma = parts[1]
                python_result = munsell
            else:
                python_result = munsell
                
    except Exception as e:
        python_result = f"ERROR: {e}"
    
    return rust_result, python_result

def main():
    print("=" * 80)
    print("ANALYZING IMPLEMENTATION GAP: Rust Simple vs Python Full")
    print("=" * 80)
    
    # Test specific problematic colors
    test_cases = [
        # High chroma greens (worst hue differences)
        ([0, 238, 17], "Vivid green - high chroma"),
        ([17, 187, 34], "Medium green - high chroma"),
        
        # High chroma purples (worst chroma differences)
        ([187, 0, 255], "Vivid purple - extreme chroma"),
        ([255, 0, 255], "Magenta - extreme chroma"),
        
        # Family mismatches
        ([0, 34, 17], "Dark green - family mismatch"),
        ([0, 102, 119], "Cyan - family mismatch"),
        
        # Reference colors for baseline
        ([255, 0, 0], "Pure red"),
        ([0, 255, 0], "Pure green"),
        ([0, 0, 255], "Pure blue"),
        ([128, 128, 128], "Gray 50%"),
    ]
    
    print("\nDetailed Color Analysis:")
    print("-" * 80)
    
    for rgb, description in test_cases:
        rust, python = test_color(rgb)
        
        print(f"\n{description} - RGB{rgb}")
        print(f"  Rust:   {rust:20s}")
        print(f"  Python: {python:20s}")
        
        # Analyze the difference
        if "ERROR" not in python:
            # Parse both results
            def parse_munsell(notation):
                if notation.startswith('N '):
                    return {'family': 'N', 'hue': 0, 'value': float(notation.split()[1]), 'chroma': 0}
                    
                parts = notation.split(' ')
                if len(parts) != 2:
                    return None
                    
                hue_part = parts[0]
                value_chroma = parts[1].split('/')
                
                # Extract hue number
                hue_num = ""
                family = ""
                for char in hue_part:
                    if char.isdigit() or char == '.':
                        hue_num += char
                    else:
                        family = hue_part[len(hue_num):]
                        break
                
                return {
                    'family': family,
                    'hue': float(hue_num) if hue_num else 0,
                    'value': float(value_chroma[0]),
                    'chroma': float(value_chroma[1]) if len(value_chroma) > 1 else 0
                }
            
            rust_parsed = parse_munsell(rust)
            python_parsed = parse_munsell(python)
            
            if rust_parsed and python_parsed:
                print(f"  Differences:")
                
                if rust_parsed['family'] != python_parsed['family']:
                    print(f"    Family: {rust_parsed['family']} vs {python_parsed['family']} ❌")
                else:
                    hue_diff = abs(rust_parsed['hue'] - python_parsed['hue'])
                    if hue_diff > 5:
                        hue_diff = 10 - hue_diff  # Handle wraparound
                    if hue_diff > 0.1:
                        print(f"    Hue: Δ{hue_diff:.1f}")
                
                value_diff = abs(rust_parsed['value'] - python_parsed['value'])
                if value_diff > 0.1:
                    print(f"    Value: Δ{value_diff:.1f}")
                
                chroma_diff = abs(rust_parsed['chroma'] - python_parsed['chroma'])
                if chroma_diff > 0.5:
                    print(f"    Chroma: Δ{chroma_diff:.1f} ⚠️")
    
    print("\n" + "=" * 80)
    print("KEY OBSERVATIONS:")
    print("=" * 80)
    
    print("""
1. CHROMA LIMITATION: Rust simple implementation has very limited chroma values
   - Usually just 2.0 or 4.0
   - Python achieves full range (0-25+)
   
2. INTERPOLATION: Rust uses nearest-neighbor, Python uses sophisticated interpolation
   - This causes massive chroma differences
   - Also causes family mismatches
   
3. SOLUTION: Need the full iterative algorithm with proper interpolation
   - Dual-loop convergence (64 outer, 16 inner iterations)
   - Radial basis function or advanced interpolation
   - Proper chromatic adaptation (which we now have!)
""")

if __name__ == "__main__":
    main()