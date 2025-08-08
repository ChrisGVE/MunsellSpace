#!/usr/bin/env python3
"""Detailed convergence tracing for Python munsell module"""

import sys
import os
import numpy as np

# Add parent directory to path to import munsell
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import munsell
from colour import sRGB_to_XYZ
from colour.algebra import cartesian_to_cylindrical, euclidean_distance
from colour.models import xyY_to_XYZ

def trace_python_convergence(xyy, max_iterations=10):
    """Trace Python's convergence algorithm step by step"""
    
    print(f"=== PYTHON CONVERGENCE TRACE ===")
    print(f"Input xyY: ({xyy[0]:.10f}, {xyy[1]:.10f}, {xyy[2]:.10f})")
    print()
    
    # Import internals
    from colour.notation.munsell import (
        MUNSELL_VALUE_METHODS,
        THRESHOLD_INTEGER,
        hue_angle_to_hue,
        hue_to_hue_angle,
        munsell_specification_to_munsell,
        normalise_munsell_specification
    )
    
    # Convert Y to value
    value = MUNSELL_VALUE_METHODS['ASTMD1535'](xyy[2] * 100)
    print(f"Value: {value:.10f}")
    
    # Illuminant C
    x_center, y_center = 0.31006, 0.31616
    
    # Convert to polar coordinates
    x, y, Y = xyy
    rho_input, phi_input, _ = cartesian_to_cylindrical([x - x_center, y - y_center, Y])
    phi_input = np.degrees(phi_input)
    
    print(f"Target rho: {rho_input:.10f}")
    print(f"Target phi: {phi_input:.10f}")
    
    # Check if grey
    if rho_input < THRESHOLD_INTEGER:
        print("Color is grey (rho < threshold)")
        return normalise_munsell_specification([np.nan, value, 0, np.nan])
    
    # Get initial specification using Lab
    xyz = xyY_to_XYZ(xyy)
    xyz_r = xyY_to_XYZ([x_center, y_center, Y])
    
    # I'll trace the first few iterations manually
    from colour.models import XYZ_to_Lab
    from colour.models.cie_lab import LCHab_to_Lab
    
    Lab = XYZ_to_Lab(xyz, xyz_r)
    LCHab = np.array([Lab[0], np.hypot(Lab[1], Lab[2]), np.degrees(np.arctan2(Lab[2], Lab[1]))])
    
    # Initial guess
    hue_initial, code_initial = hue_angle_to_hue(LCHab[2])
    chroma_initial = min(LCHab[1] * 0.05, 30)  # Rough conversion
    
    print(f"\nInitial guess:")
    print(f"  Hue: {hue_initial:.3f}, Code: {code_initial}")
    print(f"  Chroma: {chroma_initial:.3f}")
    
    # Start convergence
    specification_current = [hue_initial, value, chroma_initial, code_initial]
    
    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")
        
        hue_current = specification_current[0]
        chroma_current = specification_current[2]
        code_current = specification_current[3]
        
        # Check max chroma
        chroma_max = maximum_chroma_from_renotation(hue_current, value, code_current)
        if chroma_current > chroma_max:
            chroma_current = chroma_max
            specification_current[2] = chroma_current
            print(f"  Clamped chroma to max: {chroma_max:.3f}")
        
        # Get current xy
        try:
            xy_current = xy_from_renotation_ovoid(specification_current)
            x_current, y_current = xy_current
            print(f"  Current xy: ({x_current:.6f}, {y_current:.6f})")
        except:
            print(f"  Failed to get xy for {specification_current}")
            break
        
        # Check convergence
        distance = euclidean_distance([x, y], [x_current, y_current])
        print(f"  Distance to target: {distance:.10f}")
        
        if distance < THRESHOLD_INTEGER / 1e4:
            print(f"  CONVERGED!")
            break
        
        # Get current polar coords
        rho_current, phi_current, _ = cartesian_to_cylindrical(
            [x_current - x_center, y_current - y_center, Y]
        )
        phi_current = np.degrees(phi_current)
        
        print(f"  Current rho: {rho_current:.6f}, phi: {phi_current:.3f}")
        
        # This is where the complex chroma refinement would happen
        # For now, just show the key values
        print(f"  Rho ratio: {rho_input/rho_current:.6f}")
        
        # Simplified update for demonstration
        if iteration >= 3:
            print("  (Stopping trace for brevity)")
            break
    
    # Get final result
    final_spec = xyY_to_munsell_specification(xyy)
    print(f"\nFinal specification: {final_spec}")
    print(f"Final chroma: {final_spec[2]:.10f}")
    
    return final_spec

# Test cases
test_cases = [
    ([0.175340, 0.086753, 0.020725], "RGB(34,17,119) - Deep blue"),
    ([0.3016456112, 0.3289687108, 0.8269427000], "RGB(221,238,238) - Near grey"),
]

for xyy, description in test_cases:
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print('='*60)
    trace_python_convergence(np.array(xyy), max_iterations=3)