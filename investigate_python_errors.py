#!/usr/bin/env python3
"""
Investigate Python errors and test potential solutions.
"""

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings

print("=" * 80)
print("PYTHON ERROR INVESTIGATION")
print("=" * 80)

# Test cases that cause errors
error_cases = [
    ([0, 0, 0], "Pure black - value normalisation error"),
    ([255, 255, 255], "Pure white - value normalisation error"),
    ([0, 255, 187], "Convergence failure"),
    ([0, 51, 0], "Specification not found"),
    ([0, 170, 136], "Chroma normalisation error"),
]

for rgb, description in error_cases:
    print(f"\n{description}: RGB{rgb}")
    print("-" * 60)
    
    # Test without any parameters
    print("\n1. Default parameters:")
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        result = xyY_to_munsell_colour(xyY)
        print(f"   Success: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test with different parameters if available
    print("\n2. With increased iterations:")
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        # Check if we can pass parameters
        import inspect
        sig = inspect.signature(xyY_to_munsell_colour)
        params = list(sig.parameters.keys())
        print(f"   Available parameters: {params}")
        
        # Try with different parameters if they exist
        if 'iterations' in params:
            result = xyY_to_munsell_colour(xyY, iterations=1000)
            print(f"   Success with iterations=1000: {result}")
        else:
            print("   No 'iterations' parameter available")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Check the actual xyY values
    print("\n3. xyY values:")
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        print(f"   xyY: {xyY}")
        print(f"   Y (luminance): {xyY[2]}")
        
        # Check if Y is in valid range
        if xyY[2] < 0.01:
            print(f"   ⚠️  Y value {xyY[2]} is very low (< 0.01)")
        if xyY[2] > 1.0:
            print(f"   ⚠️  Y value {xyY[2]} is above 1.0")
    except Exception as e:
        print(f"   Error calculating xyY: {e}")

# Check available parameters and documentation
print("\n" + "=" * 80)
print("FUNCTION DOCUMENTATION")
print("=" * 80)

import inspect
print("\nxyY_to_munsell_colour signature:")
sig = inspect.signature(xyY_to_munsell_colour)
print(f"  {sig}")

print("\nxyY_to_munsell_colour docstring:")
if xyY_to_munsell_colour.__doc__:
    lines = xyY_to_munsell_colour.__doc__.split('\n')[:20]  # First 20 lines
    for line in lines:
        print(f"  {line}")

# Test handling edge cases
print("\n" + "=" * 80)
print("EDGE CASE HANDLING STRATEGIES")
print("=" * 80)

print("\n1. Black handling (Y ≈ 0):")
rgb = [0, 0, 0]
rgb_norm = [c/255.0 for c in rgb]
XYZ = sRGB_to_XYZ(rgb_norm)
xyY = XYZ_to_xyY(XYZ)
print(f"   Original xyY: {xyY}")

# Try adjusting Y slightly
if xyY[2] < 0.01:
    xyY_adjusted = xyY.copy()
    xyY_adjusted[2] = 0.01  # Minimum Y value
    print(f"   Adjusted xyY: {xyY_adjusted}")
    try:
        result = xyY_to_munsell_colour(xyY_adjusted)
        print(f"   Success with adjusted Y: {result}")
    except Exception as e:
        print(f"   Still fails: {e}")

print("\n2. White handling (Y ≈ 1):")
rgb = [255, 255, 255]
rgb_norm = [c/255.0 for c in rgb]
XYZ = sRGB_to_XYZ(rgb_norm)
xyY = XYZ_to_xyY(XYZ)
print(f"   Original xyY: {xyY}")

# Check if Y > 1 is the issue
if xyY[2] > 0.95:
    xyY_adjusted = xyY.copy()
    xyY_adjusted[2] = 0.95  # Cap at 0.95
    print(f"   Adjusted xyY: {xyY_adjusted}")
    try:
        result = xyY_to_munsell_colour(xyY_adjusted)
        print(f"   Success with adjusted Y: {result}")
    except Exception as e:
        print(f"   Still fails: {e}")

print("\n" + "=" * 80)