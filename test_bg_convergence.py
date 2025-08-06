#!/usr/bin/env python3
"""Test convergence for problematic BG colors"""

import colour

# Test colors that are failing to converge
test_colors = [
    ([0, 170, 187], "9.6BG 6.3/7.9"),
    ([0, 221, 238], "9.6BG 8.0/9.4"),
    ([0, 187, 204], "9.5BG 6.8/8.5"),
    ([0, 238, 255], "9.7BG 8.6/9.5"),
    ([0, 153, 170], "9.6BG 5.7/7.2"),
]

for rgb, expected in test_colors:
    # Convert RGB to sRGB normalized
    srgb = [c / 255.0 for c in rgb]
    
    try:
        # Convert to Munsell
        # First convert to XYZ then xyY
        xyz = colour.sRGB_to_XYZ(srgb)
        xyy = colour.XYZ_to_xyY(xyz)
        print(f"  xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
        
        # Convert xyY to Munsell
        from colour.notation.munsell import xyY_to_munsell_specification
        munsell_spec = xyY_to_munsell_specification(xyy)
        
        # Format the result
        hue = munsell_spec[0]
        value = munsell_spec[1]
        chroma = munsell_spec[2]
        hue_code = int(munsell_spec[3])
        
        # Map code to hue family
        HUE_CODES = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                     6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
        family = HUE_CODES[hue_code]
        
        if chroma < 0.05:
            result = f"N{value:.1f}"
        else:
            result = f"{hue:.1f}{family} {value:.1f}/{chroma:.1f}"
        
        print(f"RGB {rgb} -> {result} (expected {expected})")
        
        # Check if it matches
        if result == expected:
            print("  ✓ Exact match")
        else:
            print(f"  ✗ Mismatch")
        
    except Exception as e:
        print(f"RGB {rgb} -> ERROR: {e}")
    
    print()