#!/usr/bin/env python3

import colour
import numpy as np

def debug_python_coordinates():
    """Debug Python colour-science xyY coordinates for comparison"""
    
    # Test color: RGB [57, 12, 140]
    rgb_normalized = np.array([57, 12, 140]) / 255.0
    
    print("🐍 PYTHON colour-science DEBUG")
    print(f"RGB: [57, 12, 140] -> normalized: {rgb_normalized}")
    print()
    
    # Step 1: RGB to XYZ (D65)
    try:
        xyz_d65 = colour.RGB_to_XYZ(rgb_normalized, 
                                   colour.models.RGB_COLOURSPACE_sRGB)
        print(f"XYZ (D65): {xyz_d65}")
        
        # Step 2: XYZ to xyY
        xyy_d65 = colour.XYZ_to_xyY(xyz_d65)
        print(f"xyY (D65): {xyy_d65}")
        
        # Step 3: Chromatic adaptation D65 -> Illuminant C
        d65_white = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
        c_white = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
        xyz_c = colour.chromatic_adaptation(xyz_d65, d65_white, c_white, 'Von Kries')
        print(f"XYZ (Illuminant C): {xyz_c}")
        
        # Step 4: XYZ (C) to xyY (C)
        xyy_c = colour.XYZ_to_xyY(xyz_c)
        print(f"xyY (Illuminant C): {xyy_c}")
        print()
        
        # Step 5: xyY to Munsell (this is where the magic happens)
        munsell = colour.xyY_to_munsell_specification(xyy_c)
        print(f"Munsell result: {munsell}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("🔍 COMPARISON WITH RUST:")
    print("Rust xyY (Illuminant C): x=0.186109, y=0.084076, Y=0.031428")
    print("Python xyY (Illuminant C): x={:.6f}, y={:.6f}, Y={:.6f}".format(xyy_c[0], xyy_c[1], xyy_c[2]))

if __name__ == "__main__":
    debug_python_coordinates()