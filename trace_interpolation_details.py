#!/usr/bin/env python3
"""Trace the interpolation and initial estimate details in Python"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Monkey-patch the munsell module to add detailed tracing
import colour.notation.munsell as munsell

# Save original functions
original_xy_from_renotation = munsell.xy_from_renotation_ovoid
original_interpolation_method = munsell.interpolation_method_from_renotation_ovoid
original_max_chroma = munsell.maximum_chroma_from_renotation

# Create traced versions
def traced_xy_from_renotation(specification):
    """Traced version of xy_from_renotation_ovoid"""
    hue, value, chroma, code = specification
    print(f"  xy_from_renotation: spec=[{hue:.4f}, {value:.4f}, {chroma:.4f}, {int(code)}]")
    
    # Call original
    result = original_xy_from_renotation(specification)
    print(f"    -> xy=[{result[0]:.6f}, {result[1]:.6f}]")
    
    # Also trace which interpolation method was selected
    method = original_interpolation_method([hue, value, chroma, code])
    print(f"    -> interpolation method: {method}")
    
    return result

def traced_interpolation_method(specification):
    """Traced version of interpolation_method_from_renotation_ovoid"""
    if isinstance(specification, (list, tuple, np.ndarray)):
        hue, value, chroma, code = specification
    else:
        # Called with separate arguments
        return original_interpolation_method(specification)
    result = original_interpolation_method([hue, value, chroma, code])
    print(f"  interpolation_method: hue={hue:.2f}, value={value:.2f}, chroma={chroma:.2f}, code={code}")
    print(f"    -> method: {result}")
    return result

def traced_max_chroma(specification):
    """Traced version of maximum_chroma_from_renotation"""
    if len(specification) == 3:
        hue, value, code = specification
    else:
        hue, value, chroma, code = specification
    result = original_max_chroma([hue, value, code])
    print(f"  max_chroma: hue={hue:.2f}, value={value:.2f}, code={code}")
    print(f"    -> max chroma: {result:.4f}")
    return result

# Apply patches
munsell.xy_from_renotation_ovoid = traced_xy_from_renotation
munsell.interpolation_method_from_renotation_ovoid = traced_interpolation_method
munsell.maximum_chroma_from_renotation = traced_max_chroma

# Now trace initial estimate calculation
from colour import sRGB_to_XYZ
from colour.models import xyY_to_XYZ, XYZ_to_Lab
from colour.algebra import cartesian_to_cylindrical

def trace_initial_estimate(rgb):
    """Trace how the initial estimate is calculated"""
    
    print(f"\n{'='*60}")
    print(f"TRACING INITIAL ESTIMATE for RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
    print('='*60)
    
    # Convert to xyY
    rgb_norm = np.array(rgb) / 255.0
    xyz = sRGB_to_XYZ(rgb_norm)
    total = xyz[0] + xyz[1] + xyz[2]
    xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
    
    print(f"Input xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
    
    # Illuminant C
    x_center, y_center = 0.31006, 0.31616
    print(f"Illuminant C: [{x_center}, {y_center}]")
    
    # Convert to Lab
    xyz_r = xyY_to_XYZ([x_center, y_center, xyy[2]])
    print(f"Reference XYZ (Illuminant C at Y={xyy[2]:.4f}): {xyz_r}")
    
    Lab = XYZ_to_Lab(xyz, xyz_r)
    print(f"Lab: [{Lab[0]:.6f}, {Lab[1]:.6f}, {Lab[2]:.6f}]")
    
    # Convert to LCHab
    L = Lab[0]
    C = np.hypot(Lab[1], Lab[2])
    H = np.degrees(np.arctan2(Lab[2], Lab[1]))
    if H < 0:
        H += 360
    print(f"LCHab: L={L:.6f}, C={C:.6f}, H={H:.6f}")
    
    # Get hue from angle
    print(f"\n--- Hue Angle to Hue Conversion ---")
    hue, code = munsell.hue_angle_to_hue(H)
    print(f"hue_angle_to_hue({H:.3f}) -> hue={hue:.3f}, code={code}")
    
    # Check how Python scales chroma
    print(f"\n--- Initial Chroma Estimate ---")
    print(f"Lab chroma (C): {C:.6f}")
    
    # The actual initial chroma calculation in colour-science
    # This is buried in the convergence algorithm
    # Let's see what happens in the first iteration
    
    # Get value
    value = munsell.munsell_value_ASTMD1535(xyy[2] * 100)
    print(f"Value from Y={xyy[2]:.6f}: {value:.6f}")
    
    # Try different chroma scaling factors
    for factor in [0.05, 0.1, 0.15, 0.2, 0.25]:
        chroma_est = C * factor
        print(f"  C * {factor:.2f} = {chroma_est:.4f}")
    
    print(f"\n--- Starting Convergence with Detailed Tracing ---")
    
    # Now run the actual convergence with tracing
    spec = munsell.xyY_to_munsell_specification(xyy)
    
    print(f"\nFinal specification: {spec}")
    
    return spec

# Test RGB(221, 238, 238)
rgb = [221, 238, 238]
spec = trace_initial_estimate(rgb)

# Format result
hue = spec[0]
value = spec[1]
chroma = spec[2]
code = int(spec[3])

families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
           6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
family = families.get(code, '?')

print(f"\nFinal: {hue:.1f}{family} {value:.1f}/{chroma:.1f}")
print(f"Reference: 7.1G 9.3/2.1")