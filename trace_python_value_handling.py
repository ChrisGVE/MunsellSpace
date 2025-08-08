#!/usr/bin/env python3
"""Trace how Python handles Value > 9 in convergence"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ

# Monkey-patch to trace internal calls
original_xy_from_ovoid = munsell.xy_from_renotation_ovoid
call_count = [0]

def traced_xy_from_ovoid(spec):
    """Traced version that shows what values are actually passed"""
    call_count[0] += 1
    hue, value, chroma, code = spec
    
    # Show what's being requested
    if call_count[0] <= 10:  # Only show first 10 calls
        print(f"  Call {call_count[0]:2d}: xy_from_ovoid([{hue:.4f}, {value:.4f}, {chroma:.4f}, {int(code)}])")
    
    # Check if value > 9
    if value > 9.0:
        print(f"    WARNING: Value {value:.4f} > 9.0!")
        # Python must handle this somehow
    
    return original_xy_from_ovoid(spec)

# Apply patch
munsell.xy_from_renotation_ovoid = traced_xy_from_ovoid

print("Tracing Python's internal Value handling during convergence:")
print("="*60)

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0
xyz = sRGB_to_XYZ(rgb)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

print(f"Input: RGB(221, 238, 238)")
print(f"xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
print(f"Expected Value: {munsell.munsell_value_ASTMD1535(xyy[2] * 100):.6f}")

print("\nCalls to xy_from_renotation_ovoid during convergence:")

try:
    spec = munsell.xyY_to_munsell_specification(xyy)
    print(f"\nFinal specification: {spec}")
    print(f"Final Value: {spec[1]:.6f}")
except Exception as e:
    print(f"\nError during convergence: {e}")

# Restore original
munsell.xy_from_renotation_ovoid = original_xy_from_ovoid

print("\n" + "="*60)
print("OBSERVATION:")
print("="*60)
print(f"Total calls to xy_from_renotation_ovoid: {call_count[0]}")
print("Python's convergence must be clamping Value to 9.0 internally")
print("or using a different function that handles Value > 9")