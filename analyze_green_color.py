#!/usr/bin/env python3
"""
Analyze the green color RGB(0, 102, 68) to understand calibration needed.
"""

import colour
import numpy as np
import math

def analyze_green_color():
    """Analyze RGB(0, 102, 68) -> Expected: 3.4G 3.7/7.0"""
    print("ANALYZING GREEN COLOR RGB(0, 102, 68)")
    print("=" * 50)
    
    rgb = (0, 102, 68)
    print(f"Target: RGB{rgb} -> Expected: 3.4G 3.7/7.0")
    
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
    
    # Check which hue family this should be in
    print(f"\nHUE ANALYSIS:")
    print(f"Expected: 3.4G (Green family, step 3.4)")
    
    # My current hue family ranges
    hue_families = [
        (0.0, "R"), (20.0, "YR"), (60.0, "Y"), (90.0, "GY"), (120.0, "G"),
        (150.0, "BG"), (190.0, "B"), (220.0, "PB"), (260.0, "P"), (320.0, "RP")
    ]
    
    # Find where this angle falls
    for i in range(len(hue_families)):
        start_angle, family = hue_families[i]
        next_angle = 360.0 if i == len(hue_families) - 1 else hue_families[i + 1][0]
        
        if normalized >= start_angle and normalized < next_angle:
            family_position = (normalized - start_angle) / (next_angle - start_angle)
            hue_step = family_position * 10.0 + 1.0
            floored_hue = math.floor(hue_step * 10.0) / 10.0
            
            print(f"Current mapping: {normalized:.2f}° -> {floored_hue:.1f}{family}")
            print(f"Expected: 3.4G")
            
            if family != "G":
                print(f"❌ WRONG FAMILY: Getting {family}, expected G")
                
                # The angle should map to G family (120° to 150°)
                g_start, g_end = 120.0, 150.0
                print(f"G family range: [{g_start}° - {g_end}°)")
                
                if normalized < g_start:
                    print(f"Angle {normalized:.2f}° is {g_start - normalized:.2f}° too low for G family")
                elif normalized >= g_end:
                    print(f"Angle {normalized:.2f}° is {normalized - g_end:.2f}° too high for G family")
                    
                # What should the hue step be if it's in G family?
                if g_start <= normalized < g_end:
                    g_family_position = (normalized - g_start) / (g_end - g_start)
                    g_hue_step = g_family_position * 10.0 + 1.0
                    g_floored_hue = math.floor(g_hue_step * 10.0) / 10.0
                    print(f"If in G family: {g_floored_hue:.1f}G")
            else:
                print(f"✅ CORRECT FAMILY: {family}")
                print(f"Hue step: {floored_hue:.1f} (expected: 3.4)")
            
            break
    
    # Analyze chroma calculation
    print(f"\nCHROMA ANALYSIS:")
    expected_chroma = 7.0
    print(f"Expected chroma: {expected_chroma}")
    
    chromaticity_distance = math.sqrt((x - white_x)**2 + (y - white_y)**2)
    luminance_factor = math.sqrt(Y * 100.0) / 10.0
    
    print(f"Chromaticity distance: {chromaticity_distance:.6f}")
    print(f"Luminance factor: {luminance_factor:.6f}")
    
    # What scaling factor would give us the correct chroma?
    if chromaticity_distance > 0 and luminance_factor > 0:
        required_scaling = expected_chroma / (chromaticity_distance * luminance_factor)
        print(f"Required scaling factor: {required_scaling:.1f}")
        
        # Compare with blue color scaling (157.6)
        print(f"Blue color scaling: 157.6")
        print(f"Green color scaling: {required_scaling:.1f}")
        print(f"Ratio: {required_scaling/157.6:.3f}")
    
    # Analyze value calculation  
    print(f"\nVALUE ANALYSIS:")
    expected_value = 3.7
    print(f"Expected value: {expected_value}")
    print(f"Y (luminance): {Y:.6f}")
    
    # Try different value calculation approaches
    simple_sqrt = 10.0 * math.sqrt(Y) * 0.975  # My current approach adjusted
    y_percent = Y * 100.0
    
    print(f"Simple sqrt * 0.975: {simple_sqrt:.1f}")
    print(f"Y as percentage: {y_percent:.2f}%")
    
    # What multiplier would give us 3.7?
    if Y > 0:
        needed_multiplier = expected_value / (10.0 * math.sqrt(Y))
        print(f"Needed multiplier for 3.7: {needed_multiplier:.3f}")

def main():
    """Main analysis function."""
    analyze_green_color()

if __name__ == "__main__":
    main()