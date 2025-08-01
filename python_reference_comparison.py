#!/usr/bin/env python3
"""
Python reference comparison script to identify the source of systematic hue bias.

This script compares our Rust Munsell conversion against the Python colour-science library
to identify where the +4.54 hue point systematic bias originates.

The goal is to test the same RGB inputs through both systems and compare:
1. sRGB → XYZ conversion
2. XYZ → xyY conversion  
3. xyY → Munsell conversion (hue angle calculation)
4. Final Munsell notation

Dependencies:
    pip install colour-science numpy pandas
"""

import sys
import csv
import numpy as np
import pandas as pd
from pathlib import Path

try:
    import colour
    from colour import RGB_to_XYZ, XYZ_to_xyY, xyY_to_XYZ, XYZ_to_Lab
    from colour.notation import xyY_to_munsell_colour, munsell_colour_to_xyY
    print(f"✅ colour-science library version: {colour.__version__}")
except ImportError as e:
    print(f"❌ ERROR: colour-science library import failed: {e}")
    print("Please install with: pip install colour-science")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Warning during colour-science import: {e}")
    try:
        import colour
        from colour import RGB_to_XYZ, XYZ_to_xyY, xyY_to_XYZ, XYZ_to_Lab
        from colour.notation import xyY_to_munsell_colour, munsell_colour_to_xyY
        print(f"✅ colour-science library version: {colour.__version__}")
    except Exception as e2:
        print(f"❌ ERROR: Failed to import colour-science: {e2}")
        sys.exit(1)

def rgb_to_munsell_python_pipeline(rgb_array):
    """
    Complete sRGB → Munsell conversion using Python colour-science library.
    
    This follows the same pipeline as our Rust implementation:
    1. sRGB → Linear RGB (gamma correction)
    2. Linear RGB → XYZ (D65 illuminant, ITU-R BT.709)
    3. XYZ → xyY (chromaticity + luminance)
    4. xyY → Munsell (hue angle, value, chroma)
    
    Args:
        rgb_array: [R, G, B] values in 0-255 range
        
    Returns:
        dict with intermediate steps and final Munsell notation
    """
    try:
        # Convert to 0-1 range for colour-science
        rgb_normalized = np.array(rgb_array) / 255.0
        
        # Step 1: sRGB → XYZ using D65 illuminant
        xyz = RGB_to_XYZ(
            rgb_normalized,
            colour.RGB_COLOURSPACES['sRGB'].whitepoint,
            colour.RGB_COLOURSPACES['sRGB'].whitepoint,
            colour.RGB_COLOURSPACES['sRGB'].matrix_RGB_to_XYZ
        )
        
        # Step 2: XYZ → xyY
        xyy = XYZ_to_xyY(xyz)
        
        # Step 3: xyY → Munsell conversion using colour-science's algorithm
        try:
            munsell_spec = xyY_to_munsell_colour(xyy)
            
            # Parse the specification - it should be a string like "5.2R 4.1/8.3"
            if isinstance(munsell_spec, str):
                # Parse "5.2R 4.1/8.3" format
                parts = munsell_spec.split()
                if len(parts) == 2:
                    hue_part = parts[0]
                    value_chroma = parts[1].split('/')
                    
                    # Extract hue number and family
                    hue_family_start = 0
                    for i, c in enumerate(hue_part):
                        if c.isalpha():
                            hue_family_start = i
                            break
                    
                    hue_number = float(hue_part[:hue_family_start])
                    hue_family = hue_part[hue_family_start:]
                    value = float(value_chroma[0])
                    chroma = float(value_chroma[1]) if len(value_chroma) > 1 else 0.0
                    
                else:
                    # Fallback for parsing issues
                    hue_number, hue_family, value, chroma = 0.0, "N", 0.0, 0.0
            else:
                # If it's already parsed (shouldn't happen but safety)
                hue_number, hue_family, value, chroma = 0.0, "N", 0.0, 0.0
                munsell_spec = "PARSING_ERROR"
            
        except Exception as e:
            print(f"⚠️  Munsell conversion failed for {rgb_array}: {e}")
            munsell_spec = "CONVERSION_FAILED"
            hue_number, hue_family, value, chroma = 0.0, "N", 0.0, 0.0
        
        return {
            'rgb_input': rgb_array,
            'rgb_normalized': rgb_normalized.tolist(),
            'xyz': xyz.tolist(),
            'xyy': xyy.tolist(),
            'munsell_notation': munsell_spec,
            'hue_number': hue_number,
            'hue_family': hue_family,
            'value': value,
            'chroma': chroma,
            'success': munsell_spec != "CONVERSION_FAILED"
        }
        
    except Exception as e:
        print(f"❌ Pipeline failed for {rgb_array}: {e}")
        return {
            'rgb_input': rgb_array,
            'error': str(e),
            'success': False
        }

def load_test_colors():
    """Load test colors from our reference dataset for comparison."""
    test_colors = []
    
    # Load a sample from our ISCC reference dataset
    csv_path = Path("ISCC_NBS_REFERENCE_DATASET.csv")
    if csv_path.exists():
        print(f"📂 Loading test colors from {csv_path}")
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= 50:  # Limit to first 50 colors for initial comparison
                    break
                    
                hex_color = row[0].strip()
                
                # Parse hex to RGB
                if hex_color.startswith('#'):
                    hex_color = hex_color[1:]
                    
                if len(hex_color) == 6:
                    try:
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        test_colors.append([r, g, b])
                    except ValueError:
                        continue
    else:
        print("⚠️  ISCC dataset not found, using hardcoded test colors")
        # Hardcoded test colors from our analysis
        test_colors = [
            [255, 181, 186],  # #ffb5ba - systematic bias example
            [234, 147, 153],  # #ea9399 - systematic bias example  
            [234, 216, 215],  # #ead8d7 - systematic bias example
            [255, 0, 0],      # Pure red
            [0, 255, 0],      # Pure green
            [0, 0, 255],      # Pure blue
            [255, 255, 0],    # Pure yellow
            [255, 0, 255],    # Pure magenta
            [0, 255, 255],    # Pure cyan
            [128, 128, 128],  # Neutral gray
        ]
    
    print(f"✅ Loaded {len(test_colors)} test colors")
    return test_colors

def compare_with_rust_system(test_colors):
    """
    Compare Python colour-science results with our Rust system.
    
    This function will run the Rust tests and compare the results.
    For now, we'll generate the Python reference data that can be compared
    against the Rust output.
    """
    print("\n=== PYTHON COLOUR-SCIENCE REFERENCE RESULTS ===")
    
    results = []
    
    for i, rgb in enumerate(test_colors):
        print(f"Testing color {i+1}/{len(test_colors)}: RGB{rgb}")
        
        result = rgb_to_munsell_python_pipeline(rgb)
        results.append(result)
        
        if result['success']:
            print(f"  ✅ Python result: {result['munsell_notation']}")
            print(f"     XYZ: [{result['xyz'][0]:.4f}, {result['xyz'][1]:.4f}, {result['xyz'][2]:.4f}]")
            print(f"     xyY: [{result['xyy'][0]:.4f}, {result['xyy'][1]:.4f}, {result['xyy'][2]:.4f}]")
            print(f"     Hue: {result['hue_number']:.1f}{result['hue_family']} Value: {result['value']:.1f} Chroma: {result['chroma']:.1f}")
        else:
            print(f"  ❌ Python conversion failed: {result.get('error', 'Unknown error')}")
        print()
    
    return results

def save_python_reference_csv(results):
    """Save Python reference results to CSV for comparison with Rust."""
    output_path = "python_reference_results.csv"
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'r', 'g', 'b', 
            'xyz_x', 'xyz_y', 'xyz_z',
            'xyy_x', 'xyy_y', 'xyy_Y',
            'munsell_notation', 'hue_number', 'hue_family', 'value', 'chroma',
            'conversion_success'
        ])
        
        # Write data
        for result in results:
            if result['success']:
                writer.writerow([
                    result['rgb_input'][0], result['rgb_input'][1], result['rgb_input'][2],
                    result['xyz'][0], result['xyz'][1], result['xyz'][2],
                    result['xyy'][0], result['xyy'][1], result['xyy'][2],
                    result['munsell_notation'], result['hue_number'], 
                    result['hue_family'], result['value'], result['chroma'],
                    'SUCCESS'
                ])
            else:
                writer.writerow([
                    result['rgb_input'][0], result['rgb_input'][1], result['rgb_input'][2],
                    '', '', '', '', '', '',
                    'FAILED', '', '', '', '',
                    'FAILED'
                ])
    
    print(f"📊 Python reference results saved to: {output_path}")
    return output_path

def analyze_specific_examples():
    """Analyze the specific examples from our bias analysis."""
    print("\n=== ANALYZING SPECIFIC BIAS EXAMPLES ===")
    
    examples = [
        ([255, 181, 186], "#ffb5ba", "Should be close to 6.8R 8.2/5.2"),
        ([234, 147, 153], "#ea9399", "Should be close to 6.0R 7.1/7.1"),
        ([234, 216, 215], "#ead8d7", "Should be close to 8.4GY 8.8/0.8"),
    ]
    
    for rgb, hex_color, expected_note in examples:
        print(f"\n🔍 Analyzing {hex_color} RGB{rgb}")
        print(f"   Expected: {expected_note}")
        
        result = rgb_to_munsell_python_pipeline(rgb)
        
        if result['success']:
            print(f"   ✅ Python colour-science: {result['munsell_notation']}")
            print(f"      Hue: {result['hue_number']:.1f}{result['hue_family']}")
            print(f"      Value: {result['value']:.1f}")
            print(f"      Chroma: {result['chroma']:.1f}")
            print(f"      XYZ: [{result['xyz'][0]:.4f}, {result['xyz'][1]:.4f}, {result['xyz'][2]:.4f}]")
        else:
            print(f"   ❌ Python conversion failed: {result.get('error', 'Unknown error')}")

def main():
    """Main function to run the Python reference comparison."""
    print("🔬 PYTHON REFERENCE COMPARISON SCRIPT")
    print("=====================================")
    print("Comparing our Rust Munsell conversion against Python colour-science library")
    print("to identify the source of systematic +4.54 hue point bias.\n")
    
    # Load test colors
    test_colors = load_test_colors()
    
    # Analyze specific bias examples first
    analyze_specific_examples()
    
    # Run comparison with full test set
    print(f"\n🧪 Running full comparison with {len(test_colors)} colors...")
    results = compare_with_rust_system(test_colors)
    
    # Save results for comparison
    csv_path = save_python_reference_csv(results)
    
    # Summary statistics
    successful_conversions = sum(1 for r in results if r['success'])
    success_rate = (successful_conversions / len(results)) * 100
    
    print(f"\n=== PYTHON REFERENCE SUMMARY ===")
    print(f"Total colors tested: {len(results)}")
    print(f"Successful conversions: {successful_conversions} ({success_rate:.1f}%)")
    print(f"Failed conversions: {len(results) - successful_conversions}")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Create a Rust test that loads {csv_path}")
    print(f"2. Compare XYZ, xyY, and Munsell results step-by-step")
    print(f"3. Identify where the +4.54 hue point bias originates")
    print(f"4. Focus on hue angle calculation and empirical correction factors")
    
    return csv_path

if __name__ == "__main__":
    main()