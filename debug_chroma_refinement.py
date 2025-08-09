#!/usr/bin/env python3
"""Debug why chroma gets refined from 12.65 to 8.86 for RGB(187,255,153)."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import _xyY_to_munsell_specification
import numpy as np

# Test RGB(187,255,153) - Expected: 8.5GY 9.3/12.8
rgb = np.array([187/255.0, 255/255.0, 153/255.0])
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"RGB: [187, 255, 153]")
print(f"Expected: 8.5GY 9.3/12.8")
print(f"XYZ: {xyz}")
print(f"xyY: {xyy}")
print()

# Monkey-patch to add debug output
original_func = _xyY_to_munsell_specification

def traced_xyY_to_munsell_specification(xyY):
    """Traced version with debugging output."""
    import numpy as np
    from colour.utilities import tsplit, from_range_100, as_float_array
    from colour.notation.munsell import (
        munsell_value_ASTMD1535,
        _munsell_specification_to_xyY,
        normalise_munsell_specification,
        cartesian_to_cylindrical,
        is_grey_munsell_colour,
        hue_to_hue_angle,
        maximum_chroma_from_renotation,
        euclidean_distance
    )
    from colour.models import (
        xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab
    )
    from colour import ILLUMINANTS
    from colour.adaptation import chromatic_adaptation_VonKries
    from colour.notation.munsell import LCHab_to_munsell_specification
    from colour.utilities import sdiv, spow
    from scipy.interpolate import LinearNDInterpolator
    
    x, y, Y = tsplit(xyY)
    value = as_float_array(munsell_value_ASTMD1535(from_range_100(Y * 100)))
    
    print(f"Initial value calculation: {value}")
    
    # Get neutral specification
    x_center, y_center, Y_center = tsplit(
        _munsell_specification_to_xyY([np.nan, value, 0, np.nan])
    )
    
    # Convert to cylindrical
    rho_input, phi_input, _z_input = cartesian_to_cylindrical(
        [x - x_center, y - y_center, Y_center]
    )
    phi_input = np.degrees(phi_input)
    
    print(f"Input rho: {rho_input}")
    print(f"Input phi: {phi_input}")
    
    # Check if grey
    if rho_input < 1e-3:
        return normalise_munsell_specification([np.nan, value, 0, np.nan])
    
    # Initial estimate from LCHab
    XYZ = xyY_to_XYZ(xyY)
    XYZ_c = chromatic_adaptation_VonKries(
        XYZ,
        ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"],
        ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"],
    )
    Lab = XYZ_to_Lab(XYZ_c, ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"])
    LCHab = Lab_to_LCHab(Lab)
    
    specification_current = LCHab_to_munsell_specification(LCHab)
    specification_current[1] = value
    
    print(f"\nInitial specification from LCHab:")
    print(f"  Hue: {specification_current[0]}")
    print(f"  Value: {specification_current[1]}")
    print(f"  Chroma: {specification_current[2]}")
    print(f"  Code: {specification_current[3]}")
    
    convergence_threshold = 1e-7
    iterations_maximum = 64
    
    for iteration in range(iterations_maximum):
        hue_current = specification_current[0]
        _value_current = specification_current[1]
        chroma_current = specification_current[2]
        code_current = specification_current[3]
        
        hue_angle_current = hue_to_hue_angle([hue_current, code_current])
        
        # Check chroma maximum
        chroma_maximum = maximum_chroma_from_renotation(
            [hue_current, value, 0, code_current]
        )
        
        if iteration < 3:  # Only print first few iterations
            print(f"\nIteration {iteration + 1}:")
            print(f"  Current chroma: {chroma_current}")
            print(f"  Maximum chroma: {chroma_maximum}")
        
        if chroma_current > chroma_maximum:
            chroma_current = chroma_maximum
            specification_current[2] = chroma_maximum
            if iteration < 3:
                print(f"  Clamped chroma to maximum: {chroma_maximum}")
        
        # Get current xy
        x_current, y_current, _Y_current = tsplit(
            _munsell_specification_to_xyY(specification_current)
        )
        
        # Check convergence
        difference = euclidean_distance([x, y], [x_current, y_current])
        
        if iteration < 3:
            print(f"  Target xy: [{x}, {y}]")
            print(f"  Current xy: [{x_current}, {y_current}]")
            print(f"  Distance: {difference}")
        
        if difference < convergence_threshold:
            print(f"\nConverged at iteration {iteration + 1}")
            break
        
        # Chroma refinement inner loop
        rho_current, phi_current, _z_current = cartesian_to_cylindrical(
            [x_current - x_center, y_current - y_center, Y_center]
        )
        phi_current = np.degrees(phi_current)
        
        phi_current_difference = (360 - phi_input + phi_current) % 360
        if phi_current_difference > 180:
            phi_current_difference -= 360
        
        # Inner loop for chroma refinement
        rho_bounds_data = [rho_current]
        chroma_bounds_data = [chroma_current]
        
        iterations_maximum_inner = 16
        for iteration_inner in range(iterations_maximum_inner):
            if not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)):
                chroma_inner = (
                    sdiv(rho_input, rho_current) ** (iteration_inner + 1)
                ) * chroma_current
                
                if iteration < 3 and iteration_inner < 3:
                    print(f"    Inner {iteration_inner + 1}: chroma_inner = {chroma_inner}")
                
                if chroma_inner > chroma_maximum:
                    chroma_inner = chroma_maximum
                
                specification_inner = [
                    hue_current,
                    value,
                    chroma_inner,
                    code_current,
                ]
                
                x_inner, y_inner, _Y_inner = tsplit(
                    _munsell_specification_to_xyY(specification_inner)
                )
                
                rho_inner, _phi_inner, _z_inner = cartesian_to_cylindrical(
                    [x_inner - x_center, y_inner - y_center, Y_center]
                )
                
                rho_bounds_data.append(rho_inner)
                chroma_bounds_data.append(chroma_inner)
            else:
                break
        
        # Interpolate final chroma
        rho_bounds = np.array(rho_bounds_data)
        chroma_bounds = np.array(chroma_bounds_data)
        
        rhos_bounds_indexes = np.argsort(rho_bounds)
        rho_bounds = rho_bounds[rhos_bounds_indexes]
        chroma_bounds = chroma_bounds[rhos_bounds_indexes]
        
        chroma_new = LinearNDInterpolator(
            rho_bounds[:, np.newaxis], chroma_bounds
        )(rho_input)[0]
        
        if iteration < 3:
            print(f"  Interpolated new chroma: {chroma_new}")
        
        specification_current = [
            hue_current,
            value,
            chroma_new,
            code_current,
        ]
    
    result = normalise_munsell_specification(specification_current)
    print(f"\nFinal specification: {result}")
    return result

# Patch and run
import colour.notation.munsell
colour.notation.munsell._xyY_to_munsell_specification = traced_xyY_to_munsell_specification

from colour.notation import xyY_to_munsell_colour
result = xyY_to_munsell_colour(xyy)
print(f"\nFinal Munsell: {result}")