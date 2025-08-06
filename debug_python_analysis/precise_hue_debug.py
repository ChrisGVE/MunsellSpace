#!/usr/bin/env python3
"""
Precise debugging of hue calculation to understand the exact mapping needed.
"""

import colour
import numpy as np
import math

def precise_hue_analysis():
    """Precise analysis of the hue calculation for RGB(0, 68, 119)."""
    print("PRECISE HUE CALCULATION ANALYSIS")
    print("=" * 50)
    
    rgb = (0, 68, 119)
    print(f"Target: RGB{rgb} -> Expected: 2.9PB")
    
    # Get Python result
    srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    munsell_result = colour.notation.munsell.xyY_to_munsell_colour(xyy)
    spec = colour.notation.munsell.munsell_colour_to_munsell_specification(munsell_result)
    
    x, y, Y = xyy
    print(f"xyY: [{x:.6f}, {y:.6f}, {Y:.6f}]")
    print(f"Python result: {munsell_result}")
    print(f"Specification: {spec}")
    
    # Calculate hue angle
    white_x = 0.31271  # D65
    white_y = 0.32902
    hue_angle = math.atan2(y - white_y, x - white_x)
    hue_degrees = math.degrees(hue_angle)
    normalized = ((hue_degrees % 360.0) + 360.0) % 360.0
    
    print(f"Raw hue angle: {hue_degrees:.6f}°")
    print(f"Normalized (0-360): {normalized:.6f}°")
    
    # Current Rust algorithm simulation
    print(f"\nCURRENT RUST ALGORITHM SIMULATION:")
    
    # My current PB range: 220° to 260°
    pb_start = 220.0
    pb_end = 260.0
    
    if normalized >= pb_start and normalized < pb_end:
        family_position = (normalized - pb_start) / (pb_end - pb_start)
        hue_step = family_position * 10.0 + 1.0
        rounded_hue = round(hue_step * 10.0) / 10.0
        
        print(f"Falls in PB range [{pb_start}° - {pb_end}°)")
        print(f"Family position: {family_position:.6f}")
        print(f"Raw hue step: {hue_step:.6f}")
        print(f"Rounded hue step: {rounded_hue:.1f}")
        print(f"Current result: {rounded_hue:.1f}PB")
        print(f"Expected: 2.9PB")
        
        # What adjustment would give us 2.9?
        target_hue = 2.9
        needed_hue_step = target_hue
        needed_family_position = (needed_hue_step - 1.0) / 10.0
        needed_angle = needed_family_position * (pb_end - pb_start) + pb_start
        
        print(f"\nREVERSE CALCULATION:")
        print(f"To get 2.9PB, we need:")
        print(f"  Hue step: {needed_hue_step}")
        print(f"  Family position: {needed_family_position:.6f}")
        print(f"  Angle: {needed_angle:.6f}°")
        
        angle_diff = normalized - needed_angle
        print(f"  Current angle is {angle_diff:.6f}° too high")
        
        # Option 1: Adjust PB range
        print(f"\nOPTION 1 - ADJUST PB RANGE:")
        # If we want 227.97° to map to 2.9PB, what should the range be?
        # 2.9 → family_position = (2.9 - 1.0) / 10.0 = 0.19
        # 227.97 = 0.19 * (end - start) + start
        # Let's keep the 40° range but shift it
        range_size = pb_end - pb_start  # 40°
        new_pb_start = normalized - needed_family_position * range_size
        new_pb_end = new_pb_start + range_size
        
        print(f"  New PB range: [{new_pb_start:.1f}° - {new_pb_end:.1f}°] (vs current [{pb_start}° - {pb_end}°])")
        
        # Option 2: Use different rounding/calculation
        print(f"\nOPTION 2 - ADJUST CALCULATION:")
        # Instead of simple rounding, what if we use a different approach?
        raw_decimal = hue_step
        floor_value = math.floor(raw_decimal * 10) / 10
        ceil_value = math.ceil(raw_decimal * 10) / 10
        
        print(f"  Raw value: {raw_decimal:.6f}")
        print(f"  Floor to 0.1: {floor_value:.1f}")
        print(f"  Ceil to 0.1: {ceil_value:.1f}")
        print(f"  Simple round: {rounded_hue:.1f}")
        
        # The issue might be that we should use floor rather than round for this case
        if abs(floor_value - 2.9) < abs(rounded_hue - 2.9):
            print(f"  Floor gives better match: {floor_value:.1f} vs {rounded_hue:.1f}")

def test_multiple_pb_colors():
    """Test multiple colors that should be in PB family to understand the pattern."""
    print(f"\n{'='*60}")
    print("TESTING MULTIPLE PB COLORS")  
    print(f"{'='*60}")
    
    # Test colors that might be PB
    test_colors = [
        (0, 68, 119),    # Our problem case
        (0, 50, 100),    # Darker blue
        (20, 60, 140),   # Slightly different blue
        (0, 80, 160),    # Brighter blue
    ]
    
    for rgb in test_colors:
        try:
            srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
            xyz = colour.sRGB_to_XYZ(srgb)
            xyy = colour.XYZ_to_xyY(xyz)
            result = colour.notation.munsell.xyY_to_munsell_colour(xyy)
            spec = colour.notation.munsell.munsell_colour_to_munsell_specification(result)
            
            if not np.isnan(spec[0]) and 'PB' in result:
                x, y, Y = xyy
                white_x, white_y = 0.31271, 0.32902
                hue_angle = math.atan2(y - white_y, x - white_x)
                hue_degrees = math.degrees(hue_angle)
                normalized = ((hue_degrees % 360.0) + 360.0) % 360.0
                
                print(f"RGB{rgb}: {normalized:.2f}° -> {result} (hue: {spec[0]:.1f})")
            
        except Exception as e:
            print(f"RGB{rgb}: ERROR - {e}")

def main():
    """Main analysis function."""
    precise_hue_analysis()
    test_multiple_pb_colors()

if __name__ == "__main__":
    main()