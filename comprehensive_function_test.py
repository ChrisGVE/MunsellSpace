#!/usr/bin/env python3
"""Comprehensive test comparing EVERY ported function with Python colour-science"""

import subprocess
import json
import numpy as np
from colour.notation import munsell
from colour.algebra import LinearInterpolator, Extrapolator
import colour.utilities

# Test data for various functions
TEST_SPEC = [5.0, 4.0, 10.0, 7.0]  # 5R 4/10
TEST_XYY = [0.31006, 0.31616, 0.2]
TEST_XYZ = [0.31006, 0.2, 0.48976]
TEST_LAB = [50.0, 20.0, 30.0]
TEST_LCHAB = [50.0, 36.0555, 56.3099]
TEST_MUNSELL_STR = "5R 4/10"
TEST_MUNSELL_GREY = "N5.5"
TEST_HUE_ANGLE = 25.0
TEST_RGB = [0.5, 0.5, 0.5]  # For sRGB conversion

def test_string_parsing():
    """Test string parsing functions"""
    print("\n" + "="*80)
    print("STRING PARSING FUNCTIONS:")
    print("="*80)
    
    # parse_munsell_colour
    result = munsell.parse_munsell_colour(TEST_MUNSELL_STR)
    print(f"parse_munsell_colour('{TEST_MUNSELL_STR}'): {result}")
    
    # parse grey
    result = munsell.parse_munsell_colour(TEST_MUNSELL_GREY)
    print(f"parse_munsell_colour('{TEST_MUNSELL_GREY}'): {result}")
    
    # munsell_colour_to_munsell_specification
    result = munsell.munsell_colour_to_munsell_specification(TEST_MUNSELL_STR)
    print(f"munsell_colour_to_munsell_specification('{TEST_MUNSELL_STR}'): {result}")
    
    # munsell_specification_to_munsell_colour
    result = munsell.munsell_specification_to_munsell_colour(TEST_SPEC)
    print(f"munsell_specification_to_munsell_colour({TEST_SPEC}): '{result}'")

def test_lab_functions():
    """Test Lab color space functions"""
    print("\n" + "="*80)
    print("LAB COLOR SPACE FUNCTIONS:")
    print("="*80)
    
    # XYZ_to_Lab
    result = munsell.XYZ_to_Lab(TEST_XYZ)
    print(f"XYZ_to_Lab({TEST_XYZ}): {result}")
    
    # Lab_to_LCHab
    result = munsell.Lab_to_LCHab(TEST_LAB)
    print(f"Lab_to_LCHab({TEST_LAB}): {result}")
    
    # LCHab_to_munsell_specification (if exists)
    if hasattr(munsell, 'LCHab_to_munsell_specification'):
        result = munsell.LCHab_to_munsell_specification(TEST_LCHAB)
        print(f"LCHab_to_munsell_specification({TEST_LCHAB}): {result}")

def test_core_conversions():
    """Test core conversion functions"""
    print("\n" + "="*80)
    print("CORE CONVERSION FUNCTIONS:")
    print("="*80)
    
    # xyY_to_munsell_specification
    result = munsell.xyY_to_munsell_specification(TEST_XYY)
    print(f"xyY_to_munsell_specification({TEST_XYY}): {result}")
    
    # munsell_specification_to_xyY
    result = munsell.munsell_specification_to_xyY(TEST_SPEC)
    print(f"munsell_specification_to_xyY({TEST_SPEC}): {result}")
    
    # xyY_to_munsell_colour
    result = munsell.xyY_to_munsell_colour(TEST_XYY)
    print(f"xyY_to_munsell_colour({TEST_XYY}): '{result}'")
    
    # munsell_colour_to_xyY
    result = munsell.munsell_colour_to_xyY(TEST_MUNSELL_STR)
    print(f"munsell_colour_to_xyY('{TEST_MUNSELL_STR}'): {result}")

def test_hue_functions():
    """Test hue conversion functions"""
    print("\n" + "="*80)
    print("HUE CONVERSION FUNCTIONS:")
    print("="*80)
    
    # hue_angle_to_hue
    result = munsell.hue_angle_to_hue(TEST_HUE_ANGLE)
    print(f"hue_angle_to_hue({TEST_HUE_ANGLE}): {result}")
    
    # hue_to_hue_angle
    hue_and_code = [5.0, 7.0]  # 5R
    result = munsell.hue_to_hue_angle(hue_and_code)
    print(f"hue_to_hue_angle({hue_and_code}): {result}")
    
    # hue_to_ASTM_hue
    result = munsell.hue_to_ASTM_hue(hue_and_code)
    print(f"hue_to_ASTM_hue({hue_and_code}): {result}")

def test_validation_functions():
    """Test validation functions"""
    print("\n" + "="*80)
    print("VALIDATION FUNCTIONS:")
    print("="*80)
    
    # is_grey_munsell_colour
    result = munsell.is_grey_munsell_colour(TEST_SPEC)
    print(f"is_grey_munsell_colour({TEST_SPEC}): {result}")
    
    grey_spec = [np.nan, 5.0, np.nan, np.nan]
    result = munsell.is_grey_munsell_colour(grey_spec)
    print(f"is_grey_munsell_colour({grey_spec}): {result}")
    
    # normalise_munsell_specification
    result = munsell.normalise_munsell_specification(TEST_SPEC)
    print(f"normalise_munsell_specification({TEST_SPEC}): {result}")
    
    # Test with 10YR (hue >= 10)
    spec_10yr = [10.0, 4.0, 10.0, 6.0]
    result = munsell.normalise_munsell_specification(spec_10yr)
    print(f"normalise_munsell_specification({spec_10yr}): {result}")

def test_value_methods():
    """Test Munsell value computation methods"""
    print("\n" + "="*80)
    print("MUNSELL VALUE METHODS:")
    print("="*80)
    
    Y = 0.5
    methods = [
        'ASTM D1535',
        'Priest 1920',
        'Munsell 1933',
        'Moon 1943',
        'Saunderson 1944',
        'Ladd 1955',
        'McCamy 1987'
    ]
    
    for method in methods:
        result = munsell.munsell_value(Y, method=method)
        print(f"munsell_value({Y}, method='{method}'): {result}")

def test_renotation_functions():
    """Test renotation-related functions"""
    print("\n" + "="*80)
    print("RENOTATION FUNCTIONS:")
    print("="*80)
    
    # xy_from_renotation_ovoid
    result = munsell.xy_from_renotation_ovoid(TEST_SPEC)
    print(f"xy_from_renotation_ovoid({TEST_SPEC}): {result}")
    
    # interpolation_method_from_renotation_ovoid
    result = munsell.interpolation_method_from_renotation_ovoid(TEST_SPEC)
    print(f"interpolation_method_from_renotation_ovoid({TEST_SPEC}): {result}")
    
    # xyY_from_renotation
    try:
        result = munsell.xyY_from_renotation(TEST_SPEC)
        print(f"xyY_from_renotation({TEST_SPEC}): {result}")
    except:
        print(f"xyY_from_renotation({TEST_SPEC}): Not in renotation data")
    
    # bounding_hues_from_renotation (takes hue and code as separate params)
    hue_and_code = [TEST_SPEC[0], TEST_SPEC[3]]
    result = munsell.bounding_hues_from_renotation(hue_and_code, TEST_SPEC[1], TEST_SPEC[2])
    print(f"bounding_hues_from_renotation({hue_and_code}, {TEST_SPEC[1]}, {TEST_SPEC[2]}): {result}")
    
    # maximum_chroma_from_renotation (also takes hue and code as separate params)
    result = munsell.maximum_chroma_from_renotation(hue_and_code, TEST_SPEC[1])
    print(f"maximum_chroma_from_renotation({hue_and_code}, {TEST_SPEC[1]}): {result}")

def test_utility_functions():
    """Test utility functions"""
    print("\n" + "="*80)
    print("UTILITY FUNCTIONS:")
    print("="*80)
    
    # Domain scaling
    val = 0.5
    print(f"to_domain_1({val}): {colour.utilities.to_domain_1(val)}")
    print(f"to_domain_10({val}): {colour.utilities.to_domain_10(val)}")
    print(f"to_domain_100({val}): {colour.utilities.to_domain_100(val)}")
    print(f"from_range_1({val}): {colour.utilities.from_range_1(val)}")
    print(f"from_range_10(5.0): {colour.utilities.from_range_10(5.0)}")
    print(f"from_range_100(50.0): {colour.utilities.from_range_100(50.0)}")
    
    # Math utilities
    print(f"sdiv(10.0, 2.0): {colour.algebra.sdiv(10.0, 2.0)}")
    print(f"sdiv(10.0, 0.0): {colour.algebra.sdiv(10.0, 0.0)}")
    print(f"spow(2.0, 3.0): {colour.algebra.spow(2.0, 3.0)}")
    print(f"spow(-2.0, 2.0): {colour.algebra.spow(-2.0, 2.0)}")
    print(f"spow(-2.0, 2.5): {colour.algebra.spow(-2.0, 2.5)}")
    
    # Type checking
    print(f"is_numeric(5.0): {colour.utilities.is_numeric(5.0)}")
    print(f"is_numeric(np.nan): {colour.utilities.is_numeric(np.nan)}")
    print(f"is_integer(5.0): {colour.utilities.is_integer(5.0)}")
    print(f"is_integer(5.5): {colour.utilities.is_integer(5.5)}")

def test_coordinate_conversions():
    """Test coordinate conversion functions"""
    print("\n" + "="*80)
    print("COORDINATE CONVERSIONS:")
    print("="*80)
    
    # cartesian_to_cylindrical
    x, y, z = 1.0, 1.0, 1.0
    result = munsell.cartesian_to_cylindrical([x, y, z])
    print(f"cartesian_to_cylindrical([{x}, {y}, {z}]): {result}")
    
    # polar_to_cartesian
    r, theta = 1.414, 45.0
    result = munsell.polar_to_cartesian((r, theta))
    print(f"polar_to_cartesian(({r}, {theta})): {result}")

def test_interpolation():
    """Test interpolation classes"""
    print("\n" + "="*80)
    print("INTERPOLATION CLASSES:")
    print("="*80)
    
    # LinearInterpolator
    x = [0.0, 1.0, 2.0, 3.0]
    y = [0.0, 2.0, 4.0, 6.0]
    interp = LinearInterpolator(x, y)
    
    print(f"LinearInterpolator interpolate(0.5): {interp(0.5)}")
    print(f"LinearInterpolator interpolate(1.5): {interp(1.5)}")
    print(f"LinearInterpolator interpolate(-1.0): {interp(-1.0)}")  # Clamps
    print(f"LinearInterpolator interpolate(4.0): {interp(4.0)}")    # Clamps
    
    # Extrapolator
    extrap = Extrapolator(interp, method='Linear')
    print(f"Extrapolator (Linear) extrapolate(4.0): {extrap(4.0)}")
    print(f"Extrapolator (Linear) extrapolate(-1.0): {extrap(-1.0)}")
    
    extrap_const = Extrapolator(interp, method='Constant')
    print(f"Extrapolator (Constant) extrapolate(4.0): {extrap_const(4.0)}")
    print(f"Extrapolator (Constant) extrapolate(-1.0): {extrap_const(-1.0)}")

def main():
    """Run all tests"""
    print("="*80)
    print("COMPREHENSIVE PYTHON COLOUR-SCIENCE FUNCTION TEST")
    print("="*80)
    
    test_string_parsing()
    test_lab_functions()
    test_core_conversions()
    test_hue_functions()
    test_validation_functions()
    test_value_methods()
    test_renotation_functions()
    test_utility_functions()
    test_coordinate_conversions()
    test_interpolation()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED - Use these outputs to verify Rust implementation")
    print("="*80)

if __name__ == "__main__":
    main()