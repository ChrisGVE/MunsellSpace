#!/usr/bin/env python3
"""
Debug the hue calculation to understand how Python gets 2.9PB from RGB(0, 68, 119).
"""

import colour
import numpy as np
import math

def debug_hue_calculation(rgb):
    """Debug step-by-step hue calculation."""
    print(f"Debugging hue calculation for RGB{rgb}")
    
    # Convert using Python colour-science
    srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    munsell_result = colour.notation.munsell.xyY_to_munsell_colour(xyy)
    spec = colour.notation.munsell.munsell_colour_to_munsell_specification(munsell_result)
    
    print(f"  sRGB normalized: {srgb}")
    print(f"  XYZ: {xyz}")
    print(f"  xyY: {xyy}")
    print(f"  Munsell result: {munsell_result}")
    print(f"  Specification: {spec}")
    
    x, y, Y = xyy
    
    # Calculate hue angle relative to white point (what our Rust code does)
    white_x_d65 = 0.31271  # D65 white point
    white_y_d65 = 0.32902
    
    hue_angle_d65 = math.atan2(y - white_y_d65, x - white_x_d65)
    hue_degrees_d65 = math.degrees(hue_angle_d65)
    
    print(f"  D65 white point: ({white_x_d65}, {white_y_d65})")
    print(f"  Hue angle (D65): {hue_degrees_d65:.2f}°")
    
    # Try with Illuminant C white point
    white_x_c = 0.31006  # Illuminant C white point
    white_y_c = 0.31616
    
    hue_angle_c = math.atan2(y - white_y_c, x - white_x_c)
    hue_degrees_c = math.degrees(hue_angle_c)
    
    print(f"  C white point: ({white_x_c}, {white_y_c})")
    print(f"  Hue angle (C): {hue_degrees_c:.2f}°")
    
    # What should 2.9PB correspond to in degrees?
    # PB family typically ranges from around 220° to 260° (purple-blue)
    # 2.9 within PB family should be close to the beginning of PB range
    
    print(f"  Expected result: {spec[0]} (hue step {spec[0]} in PB family)")
    
    # Try to reverse-engineer the correct angle mapping
    # If 2.9PB is correct, what angle range should PB cover?
    
    print()

def analyze_munsell_hue_mapping():
    """Analyze how angles map to Munsell hue families."""
    print("MUNSELL HUE FAMILY ANALYSIS")
    print("=" * 40)
    
    # Test several known colors to understand the angle mapping
    test_colors = [
        ((0, 68, 119), "2.9PB"),    # Our problem case
        ((255, 0, 0), "R"),         # Pure red
        ((255, 255, 0), "Y"),       # Pure yellow  
        ((0, 255, 0), "G"),         # Pure green
        ((0, 0, 255), "B"),         # Pure blue
    ]
    
    for rgb, expected_family in test_colors:
        print(f"\nAnalyzing {expected_family} color RGB{rgb}:")
        
        srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
        xyz = colour.sRGB_to_XYZ(srgb)
        xyy = colour.XYZ_to_xyY(xyz)
        
        try:
            munsell_result = colour.notation.munsell.xyY_to_munsell_colour(xyy)
            spec = colour.notation.munsell.munsell_colour_to_munsell_specification(munsell_result)
            
            x, y, Y = xyy
            
            # Calculate angle relative to D65
            white_x = 0.31271
            white_y = 0.32902
            hue_angle = math.atan2(y - white_y, x - white_x)
            hue_degrees = math.degrees(hue_angle)
            
            print(f"  xyY: [{x:.6f}, {y:.6f}, {Y:.6f}]")
            print(f"  Hue angle: {hue_degrees:.2f}°")
            print(f"  Python result: {munsell_result}")
            print(f"  Parsed hue: {spec[0] if not np.isnan(spec[0]) else 'neutral'}")
            
        except Exception as e:
            print(f"  ERROR: {e}")

def main():
    """Main analysis function."""
    debug_hue_calculation((0, 68, 119))
    analyze_munsell_hue_mapping()

if __name__ == "__main__":
    main()