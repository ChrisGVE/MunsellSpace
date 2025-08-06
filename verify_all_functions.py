#!/usr/bin/env python3
"""
Systematically verify EVERY function in the Rust port against Python colour-science.
This script will output the exact Python implementation for comparison.
"""

import numpy as np
import inspect
import colour
from colour.notation import munsell
from colour.algebra import cartesian_to_cylindrical, polar_to_cartesian
from colour.algebra.interpolation import LinearInterpolator, Extrapolator
from colour.models import XYZ_to_Lab, Lab_to_LCHab, xyY_to_XYZ, XYZ_to_xyY

# List ALL functions we need to verify
functions_to_verify = [
    # Main conversion functions
    ("xyY_to_munsell_specification", munsell._xyY_to_munsell_specification),
    ("munsell_specification_to_xyY", munsell._munsell_specification_to_xyY),
    
    # Value functions
    ("munsell_value_ASTMD1535", munsell.munsell_value_ASTMD1535),
    ("luminance_ASTMD1535", munsell.luminance_ASTMD1535),
    
    # Hue/angle conversions
    ("hue_to_ASTM_hue", munsell.hue_to_ASTM_hue),
    ("ASTM_hue_to_hue", munsell.ASTM_hue_to_hue),
    ("hue_angle_to_hue", munsell.hue_angle_to_hue),
    ("hue_to_hue_angle", munsell.hue_to_hue_angle),
    
    # Renotation functions
    ("xy_from_renotation_ovoid", munsell.xy_from_renotation_ovoid),
    ("maximum_chroma_from_renotation", munsell.maximum_chroma_from_renotation),
    ("bounding_hues_from_renotation", munsell.bounding_hues_from_renotation),
    ("interpolation_method_from_renotation_ovoid", munsell.interpolation_method_from_renotation_ovoid),
    
    # Initial guess
    ("LCHab_to_munsell_specification", munsell.LCHab_to_munsell_specification),
    
    # Normalization
    ("normalise_munsell_specification", munsell.normalise_munsell_specification),
    ("is_grey_munsell_colour", munsell.is_grey_munsell_colour),
    
    # Coordinate transforms
    ("cartesian_to_cylindrical", cartesian_to_cylindrical),
    ("polar_to_cartesian", polar_to_cartesian),
    
    # Color space conversions
    ("XYZ_to_Lab", XYZ_to_Lab),
    ("Lab_to_LCHab", Lab_to_LCHab),
    ("xyY_to_XYZ", xyY_to_XYZ),
    ("XYZ_to_xyY", XYZ_to_xyY),
]

def print_function_source(name, func):
    """Print the source code of a function"""
    print(f"\n{'='*80}")
    print(f"FUNCTION: {name}")
    print(f"Module: {func.__module__}")
    print(f"{'='*80}")
    
    try:
        source = inspect.getsource(func)
        print(source)
    except:
        print(f"[Cannot get source - may be implemented in C/Cython]")
        print(f"Docstring: {func.__doc__}")
    
    print(f"\n--- Constants and variables used ---")
    if hasattr(func, '__globals__'):
        # Look for relevant constants
        for key, value in func.__globals__.items():
            if any(keyword in key.lower() for keyword in ['munsell', 'astm', 'threshold', 'illuminant', 'renotation']):
                if not callable(value) and not key.startswith('_'):
                    print(f"{key} = {value}")

# Print all function sources
for name, func in functions_to_verify:
    print_function_source(name, func)

# Also print key constants
print(f"\n{'='*80}")
print("KEY CONSTANTS FROM colour.notation.munsell")
print(f"{'='*80}")

import colour.notation.munsell as m
print(f"MUNSELL_HUE_LETTER_CODES = {m.MUNSELL_HUE_LETTER_CODES}")
print(f"CCS_ILLUMINANT_MUNSELL = {m.CCS_ILLUMINANT_MUNSELL}")
print(f"MUNSELL_RENOTATION = (shape: {m.MUNSELL_RENOTATION.shape}, dtype: {m.MUNSELL_RENOTATION.dtype})")

# Print interpolation method table info
print(f"\n--- Interpolation Method Table ---")
print(f"INTERPOLATION_METHODS_MUNSELL_RENOTATION = (type: {type(m.INTERPOLATION_METHODS_MUNSELL_RENOTATION)})")
if hasattr(m.INTERPOLATION_METHODS_MUNSELL_RENOTATION, 'shape'):
    print(f"  Shape: {m.INTERPOLATION_METHODS_MUNSELL_RENOTATION.shape}")
print(f"  First few entries: {list(m.INTERPOLATION_METHODS_MUNSELL_RENOTATION.items())[:5]}")

# Test specific functions with example inputs
print(f"\n{'='*80}")
print("FUNCTION BEHAVIOR TESTS")
print(f"{'='*80}")

# Test hue_to_ASTM_hue
print("\n--- hue_to_ASTM_hue ---")
for hue in [0.0, 2.5, 5.0, 7.5, 10.0]:
    for code in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        astm = munsell.hue_to_ASTM_hue(hue, code)
        print(f"hue_to_ASTM_hue({hue}, {code}) = {astm}")

# Test hue_angle_to_hue
print("\n--- hue_angle_to_hue ---")
for angle in [0, 18, 36, 54, 90, 136.357, 180, 270, 359]:
    hue, code = munsell.hue_angle_to_hue(angle)
    print(f"hue_angle_to_hue({angle}) = ({hue:.3f}, {code})")

# Test LCHab_to_munsell_specification
print("\n--- LCHab_to_munsell_specification ---")
test_lchab = np.array([87.735, 124.273, 136.357])
spec = munsell.LCHab_to_munsell_specification(test_lchab)
print(f"LCHab_to_munsell_specification([87.735, 124.273, 136.357]) = {spec}")