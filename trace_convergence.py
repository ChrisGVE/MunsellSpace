#!/usr/bin/env python3
"""Trace exact convergence steps in Python to understand the algorithm."""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import THRESHOLD_INTEGER
from colour.algebra import euclidean_distance, cartesian_to_cylindrical
from colour.models import XYZ_to_Lab, Lab_to_LCHab
from colour.colorimetry import CCS_ILLUMINANTS

# Monkey-patch to trace iterations
original_xyY_to_munsell = None

def traced_xyY_to_munsell_specification(xyY):
    """Traced version of the algorithm to see iteration details."""
    from colour.notation.munsell import (
        _munsell_value_ASTMD1535,
        _LCHab_to_munsell_specification,
        _munsell_specification_to_xyY,
        maximum_chroma_from_renotation,
        hue_to_hue_angle
    )
    from colour.algebra.interpolation import LinearInterpolator, Extrapolator
    
    x, y, Y = xyY[0], xyY[1], xyY[2]
    
    # Calculate Value
    value = _munsell_value_ASTMD1535(Y * 100)
    print(f"Calculated value: {value:.12f}")
    
    # Get illuminant C
    x_grey, y_grey = CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
    print(f"Illuminant C: x={x_grey:.12f}, y={y_grey:.12f}")
    
    # Check if achromatic
    grey_threshold = THRESHOLD_INTEGER
    if euclidean_distance([x, y], [x_grey, y_grey]) < grey_threshold:
        print("Color is achromatic")
        return [0, value, 0, 0]
    
    # Initial guess using Lab/LCHab
    XYZ = np.array([x * Y / y, Y, (1 - x - y) * Y / y])
    Lab = XYZ_to_Lab(XYZ, illuminant=CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C'])
    LCHab = Lab_to_LCHab(Lab)
    
    hue_initial, _value_initial, chroma_initial, code_initial = _LCHab_to_munsell_specification(LCHab)
    
    specification_current = [
        hue_initial,
        value,
        (5 / 5.5) * chroma_initial,
        code_initial,
    ]
    
    print(f"\nInitial guess: hue={specification_current[0]:.8f}, value={specification_current[1]:.8f}, chroma={specification_current[2]:.8f}, code={specification_current[3]}")
    
    # Iterative refinement
    convergence_threshold = THRESHOLD_INTEGER / 1e4
    iterations_maximum = 64
    
    iterations = 0
    while iterations <= iterations_maximum:
        hue_current, value_current, chroma_current, code_current = specification_current
        
        # Check chroma bounds
        chroma_maximum = maximum_chroma_from_renotation([hue_current, value_current, code_current])
        if chroma_current > chroma_maximum:
            chroma_current = chroma_maximum
            specification_current[2] = chroma_current
        
        # Convert specification to xyY
        x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)
        
        # Calculate difference
        difference = euclidean_distance([x, y], [x_current, y_current])
        
        if iterations % 10 == 0 or difference < convergence_threshold:
            print(f"Iteration {iterations}: distance={difference:.12e}, spec=[{hue_current:.8f}, {value_current:.8f}, {chroma_current:.8f}, {code_current}]")
        
        if difference < convergence_threshold:
            print(f"CONVERGED at iteration {iterations}")
            return specification_current
        
        # ... rest of algorithm would be here
        iterations += 1
        
        # For now, just return after showing initial iterations
        if iterations > 5:
            print("(stopping trace early for brevity)")
            break
    
    # Fall back to actual implementation
    from colour.notation.munsell import _xyY_to_munsell_specification as original
    return original(xyY)

# Test with red
print("Testing RGB(255, 0, 0):")
rgb = np.array([1.0, 0.0, 0.0])
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)
print(f"Input xyY: x={xyy[0]:.12f}, y={xyy[1]:.12f}, Y={xyy[2]:.12f}")

# Use traced version
spec = traced_xyY_to_munsell_specification(xyy)