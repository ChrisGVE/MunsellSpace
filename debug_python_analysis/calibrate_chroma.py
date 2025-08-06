#!/usr/bin/env python3
"""
Calibrate the chroma calculation by comparing with successful Python colour-science results.
"""

import colour
import numpy as np

def analyze_specific_color(rgb):
    """Analyze a specific color to understand the chroma calculation."""
    print(f"Analyzing RGB{rgb}")
    
    # Convert using Python colour-science (our reference)
    srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    munsell_result = colour.notation.munsell.xyY_to_munsell_colour(xyy)
    
    print(f"  sRGB normalized: {srgb}")
    print(f"  XYZ: {xyz}")
    print(f"  xyY: {xyy}")
    print(f"  Munsell result: {munsell_result}")
    
    # Extract chroma from result
    if "ERROR" not in munsell_result:
        try:
            spec = colour.notation.munsell.munsell_colour_to_munsell_specification(munsell_result)
            print(f"  Specification: {spec}")
            if not np.isnan(spec[2]):  # Has chroma
                chroma = spec[2]
                print(f"  Extracted chroma: {chroma}")
                
                # Calculate what our Rust algorithm would compute
                x, y, big_y = xyy
                white_x, white_y = 0.31271, 0.32902
                chromaticity_distance = np.sqrt((x - white_x)**2 + (y - white_y)**2)
                
                print(f"  Chromaticity distance: {chromaticity_distance}")
                print(f"  Y (luminance): {big_y}")
                
                # What scaling factor would give us the correct chroma?
                if chromaticity_distance > 0:
                    required_scaling = chroma / chromaticity_distance
                    print(f"  Required scaling factor: {required_scaling}")
                    
                    # Account for luminance
                    luminance_factor = np.sqrt(big_y * 100.0) / 10.0
                    base_scaling = required_scaling / luminance_factor if luminance_factor > 0 else 0
                    print(f"  Luminance factor: {luminance_factor}")
                    print(f"  Base scaling needed: {base_scaling}")
                
        except Exception as e:
            print(f"  Error parsing specification: {e}")
    
    print()

def main():
    """Analyze several working examples to calibrate chroma."""
    print("CHROMA CALIBRATION ANALYSIS")
    print("="*40)
    
    # Test colors that work well in Python
    test_colors = [
        (0, 68, 119),   # Expected: 2.9PB 2.8/7.0
        (0, 102, 68),   # Expected: 3.4G 3.7/7.0
        (0, 68, 136),   # Expected: 5.1PB 2.9/9.1
        (0, 102, 85),   # Expected: 8.3G 3.8/6.1
        (0, 68, 153),   # Expected: 5.8PB 3.0/11.3
    ]
    
    scaling_factors = []
    
    for rgb in test_colors:
        analyze_specific_color(rgb)

if __name__ == "__main__":
    main()