#!/usr/bin/env python3
"""
Deep analysis of the Python colour-science library algorithm.
Extract key constants, methods, and structure.
"""

import colour
import numpy as np

def analyze_python_algorithm():
    """Analyze key components of the Python colour-science algorithm."""
    print("PYTHON COLOUR-SCIENCE ALGORITHM ANALYSIS")
    print("=" * 60)
    
    # 1. Check ASTM D1535 lookup table
    print("\n1. ASTM D1535 VALUE CALCULATION:")
    print("-" * 40)
    
    # Test several Y values to understand the relationship
    test_y_values = [0, 1, 5, 10, 20, 30, 50, 70, 90, 100]
    print("Y (luminance) -> Munsell Value:")
    for y in test_y_values:
        try:
            value = colour.notation.munsell.munsell_value_ASTMD1535(y)
            print(f"  {y:3.0f} -> {value:.3f}")
        except Exception as e:
            print(f"  {y:3.0f} -> ERROR: {e}")
    
    # 2. Check MacAdam limits
    print("\n2. MACADAM LIMITS:")
    print("-" * 40)
    
    illuminant_name = colour.notation.munsell.ILLUMINANT_NAME_MUNSELL
    print(f"Illuminant used: {illuminant_name}")
    
    # Test some colors for MacAdam limits
    test_colors = [
        ([0.3127, 0.3290, 0.1], "D65 white point"),
        ([0.1855, 0.1879, 0.0547], "RGB(0,68,119) dark blue"),
        ([0.2542, 0.4352, 0.0992], "RGB(0,102,68) dark green"),
    ]
    
    for xyy, desc in test_colors:
        within_limits = colour.notation.munsell.is_within_macadam_limits(xyy, illuminant_name)
        print(f"  {desc}: {within_limits}")
        print(f"    xyY: [{xyy[0]:.4f}, {xyy[1]:.4f}, {xyy[2]:.4f}]")
    
    # 3. Check key constants
    print("\n3. KEY ALGORITHM CONSTANTS:")
    print("-" * 40)
    
    try:
        threshold = colour.notation.munsell.THRESHOLD_INTEGER
        print(f"THRESHOLD_INTEGER: {threshold}")
    except:
        print("THRESHOLD_INTEGER: Not accessible")
    
    try:
        illuminant = colour.notation.munsell.CCS_ILLUMINANT_MUNSELL
        print(f"CCS_ILLUMINANT_MUNSELL: {illuminant}")
    except:
        print("CCS_ILLUMINANT_MUNSELL: Not accessible")
    
    # 4. Analyze the iterative algorithm structure
    print("\n4. ALGORITHM STRUCTURE ANALYSIS:")
    print("-" * 40)
    
    print("The algorithm uses:")
    print("  - ASTM D1535 for Munsell value calculation")
    print("  - MacAdam limits checking for color gamut validation")
    print("  - Iterative convergence with threshold-based stopping")
    print("  - Cylindrical coordinate transformations")
    print("  - Linear interpolation and extrapolation")
    print("  - Maximum 64 outer iterations, 16 inner iterations")
    print("  - Convergence threshold: THRESHOLD_INTEGER / 1e4")
    
    # 5. Test the complete conversion on our reference colors
    print("\n5. REFERENCE COLOR ANALYSIS:")
    print("-" * 40)
    
    reference_colors = [
        ([0, 0, 0], "N 0.0"),
        ([0, 68, 119], "2.9PB 2.8/7.0"),
        ([0, 102, 68], "3.4G 3.7/7.0"),
    ]
    
    for rgb, expected in reference_colors:
        print(f"\nRGB{rgb} -> Expected: {expected}")
        
        # Convert step by step
        srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
        xyz = colour.sRGB_to_XYZ(srgb)
        xyy = colour.XYZ_to_xyY(xyz)
        
        print(f"  sRGB: [{srgb[0]:.6f}, {srgb[1]:.6f}, {srgb[2]:.6f}]")
        print(f"  XYZ:  [{xyz[0]:.6f}, {xyz[1]:.6f}, {xyz[2]:.6f}]")
        print(f"  xyY:  [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
        
        try:
            # Get the specification
            spec = colour.notation.munsell.xyY_to_munsell_specification(xyy)
            print(f"  Spec: [{spec[0]:.3f}, {spec[1]:.3f}, {spec[2]:.3f}, {spec[3]:.0f}]")
            
            # Get the final Munsell color
            munsell = colour.notation.munsell.xyY_to_munsell_colour(xyy)
            print(f"  Result: {munsell}")
            print(f"  Match: {'✓' if munsell == expected else '✗'}")
            
        except Exception as e:
            print(f"  ERROR: {e}")

def analyze_munsell_renotation_data():
    """Analyze the Munsell renotation data used by the algorithm."""
    print("\n" + "=" * 60)
    print("MUNSELL RENOTATION DATA ANALYSIS")
    print("=" * 60)
    
    try:
        # Check if we can access the renotation data
        print("Attempting to access Munsell renotation data...")
        
        # The algorithm uses maximum_chroma_from_renotation function
        test_specs = [
            [2.9, 2.8, 10],  # PB family
            [3.4, 3.7, 3],   # G family
        ]
        
        for spec in test_specs:
            try:
                max_chroma = colour.notation.munsell.maximum_chroma_from_renotation(spec)
                print(f"  Spec {spec} -> Max chroma: {max_chroma:.1f}")
            except Exception as e:
                print(f"  Spec {spec} -> ERROR: {e}")
                
    except Exception as e:
        print(f"Could not access renotation data: {e}")

def main():
    """Main analysis function."""
    analyze_python_algorithm()
    analyze_munsell_renotation_data()
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("Key findings:")
    print("1. Uses ASTM D1535 lookup table for value calculation")
    print("2. Sophisticated iterative algorithm with convergence checking")
    print("3. MacAdam limits validation for color gamut")
    print("4. Maximum 64 outer iterations for precision")
    print("5. Cylindrical coordinate transformations")
    print("6. Linear interpolation and extrapolation")
    print("7. Extensive use of Munsell renotation reference data")

if __name__ == "__main__":
    main()