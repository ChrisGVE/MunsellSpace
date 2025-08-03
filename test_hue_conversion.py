#!/usr/bin/env python3
"""
Test Python's hue conversion at boundaries to understand the exact behavior.
"""

import numpy as np
from colour.notation.munsell import hue_angle_to_hue, normalise_munsell_specification

# Test boundary angles
test_angles = [
    0.0,    # Should be R
    350.0,  # Near RP/R boundary  
    340.0,  # RP region
    10.0,   # R region
    42.57,  # From our YR/Y mismatch case
    139.30, # From our G/BG mismatch case
    140.14, # From another G/BG mismatch
    194.28, # From our B/PB mismatch case
    196.73, # From another B/PB mismatch
]

print("Testing Python hue_angle_to_hue conversions:")
print("-" * 60)

for angle in test_angles:
    hue, code = hue_angle_to_hue(angle)
    
    # Map code to family name
    code_to_family = {
        1: 'BG', 2: 'G', 3: 'GY', 4: 'Y', 5: 'YR',
        6: 'R', 7: 'RP', 8: 'P', 9: 'PB', 10: 'B'
    }
    family = code_to_family[int(code)]
    
    print(f"Angle {angle:6.2f}° → hue={hue:5.2f}, code={int(code):2d} ({family})")
    
    # Now test normalization for boundary cases
    if hue < 0.5 or hue > 9.5:
        spec = np.array([hue, 5.0, 10.0, code])
        normalized = normalise_munsell_specification(spec)
        norm_hue, norm_value, norm_chroma, norm_code = normalized
        norm_family = code_to_family[int(norm_code)]
        print(f"    After normalization: hue={norm_hue:5.2f}, code={int(norm_code):2d} ({norm_family})")

print("\n" + "=" * 60)
print("Testing specific boundary normalizations:")
print("-" * 60)

# Test cases where hue = 0 or 10
test_specs = [
    [0.0, 5.0, 10.0, 6],   # 0R should become 10R
    [10.0, 5.0, 10.0, 6],  # 10R should stay 10R
    [0.0, 5.0, 10.0, 5],   # 0YR should become 10R (code changes!)
    [10.0, 5.0, 10.0, 7],  # 10RP should stay 10RP
    [0.0, 5.0, 10.0, 7],   # 0RP should become 10RP
]

for spec in test_specs:
    hue, value, chroma, code = spec
    code_to_family = {
        1: 'BG', 2: 'G', 3: 'GY', 4: 'Y', 5: 'YR',
        6: 'R', 7: 'RP', 8: 'P', 9: 'PB', 10: 'B'
    }
    family = code_to_family[int(code)]
    
    normalized = normalise_munsell_specification(np.array(spec))
    norm_hue, norm_value, norm_chroma, norm_code = normalized
    norm_family = code_to_family[int(norm_code)]
    
    print(f"[{hue:4.1f}, {value:.1f}, {chroma:.1f}, {int(code):2d}] ({hue:.1f}{family})")
    print(f"  → [{norm_hue:4.1f}, {norm_value:.1f}, {norm_chroma:.1f}, {int(norm_code):2d}] ({norm_hue:.1f}{norm_family})")
    if code != norm_code:
        print(f"  ⚠️  FAMILY CHANGED: {family} → {norm_family}")