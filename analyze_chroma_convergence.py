#!/usr/bin/env python3
"""Analyze chroma convergence differences between Python and Rust"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ

# Test cases with known chroma differences
test_cases = [
    # RGB, Expected Python chroma, Current Rust chroma
    ([221, 238, 238], 2.084, 1.6),  # Low chroma issue
    ([100, 150, 200], None, None),   # To be tested
    ([255, 200, 150], None, None),   # To be tested
]

print("Analyzing Chroma Convergence Differences")
print("="*60)

for rgb_vals, expected_py, current_rust in test_cases:
    rgb = np.array(rgb_vals) / 255.0
    xyz = sRGB_to_XYZ(rgb)
    total = xyz[0] + xyz[1] + xyz[2]
    xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
    
    # Get Python's result
    spec = munsell.xyY_to_munsell_specification(xyy)
    # Convert to notation manually
    hue_letters = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                   6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
    hue_letter = hue_letters.get(int(spec[3]), '?')
    notation = f"{spec[0]:.1f}{hue_letter} {spec[1]:.1f}/{spec[2]:.1f}"
    
    print(f"\nRGB{tuple(rgb_vals)}:")
    print(f"  Python: {notation}")
    print(f"  Spec: H={spec[0]:.4f}, V={spec[1]:.4f}, C={spec[2]:.4f}")
    
    if expected_py:
        print(f"  Expected Python Chroma: {expected_py:.3f}")
    if current_rust:
        print(f"  Current Rust Chroma: {current_rust:.3f}")
        if expected_py:
            diff = abs(expected_py - current_rust)
            print(f"  Difference: {diff:.3f} ({diff/expected_py*100:.1f}%)")

print("\n" + "="*60)
print("CHROMA CONVERGENCE ANALYSIS:")
print("="*60)

# Let's trace what happens during chroma convergence for low values
print("\nTracing low chroma convergence for RGB(221, 238, 238):")

# Monkey-patch to see chroma updates
original_convergence = munsell.xyY_to_munsell_specification
calls = []

def traced_convergence(xyy, *args, **kwargs):
    """Trace chroma values during convergence"""
    # We can't easily trace inside, but we can check multiple chromas
    return original_convergence(xyy, *args, **kwargs)

# Test different starting chroma values
print("\nTesting convergence with different initial chromas:")
test_chromas = [1.0, 1.5, 2.0, 2.5, 3.0]

for init_c in test_chromas:
    # We can't easily inject initial chroma, but we can observe
    # Let's at least document what we know
    print(f"  Initial chroma {init_c:.1f}: Would need internal access")

print("\n" + "="*60)
print("KEY OBSERVATIONS:")
print("="*60)
print("1. Low chroma colors (C < 2) show largest differences")
print("2. Python converges to 2.084, Rust to ~1.6")
print("3. This suggests different:")
print("   - Initial chroma estimates")
print("   - Convergence step sizes")
print("   - Stopping criteria")
print("   - Interpolation at low chromas")