#!/usr/bin/env python3
"""Simple trace of chroma convergence for RGB(187,255,153)."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

# Add minimal debug tracing to the critical part
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

# Test color
rgb = np.array([187/255.0, 255/255.0, 153/255.0])
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)

print(f"RGB: [187, 255, 153]")
print(f"Expected: 8.5GY 9.3/12.8")
print(f"xyY: {xyy}")

# Monkey patch to trace chroma values
import colour.notation.munsell as munsell_module
original_xyy_func = munsell_module._xyY_to_munsell_specification

iteration_count = 0
def traced_func(xyY):
    global iteration_count
    iteration_count = 0
    
    # Call original but with tracing
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
    
    x, y, Y = tsplit(xyY)
    value = as_float_array(munsell_value_ASTMD1535(from_range_100(Y * 100)))
    
    # Continue with normal function but insert traces
    return original_xyy_func(xyY)

# Simpler approach - just run and examine intermediate values
# Let's directly examine what's happening at key points

# First, let's see what the LCHab initial estimate gives us
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab
from colour.colorimetry import CCS_ILLUMINANTS
from colour.adaptation import chromatic_adaptation_VonKries
from colour.notation.munsell import LCHab_to_munsell_specification

XYZ = xyY_to_XYZ(xyy)
D65 = CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
C = CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"]

XYZ_c = chromatic_adaptation_VonKries(XYZ, D65, C)
Lab = XYZ_to_Lab(XYZ_c, C)
LCHab = Lab_to_LCHab(Lab)

print(f"\nLCHab: {LCHab}")

initial_spec = LCHab_to_munsell_specification(LCHab)
print(f"Initial specification from LCHab: {initial_spec}")

# Now call the actual function
result = xyY_to_munsell_colour(xyy)
print(f"\nFinal Munsell: {result}")

# Let's check what chroma maximum is for this hue/value
from colour.notation.munsell import maximum_chroma_from_renotation
from colour.utilities import from_range_100, as_float_array
from colour.notation.munsell import munsell_value_ASTMD1535

value = as_float_array(munsell_value_ASTMD1535(from_range_100(xyy[2] * 100)))
print(f"\nCalculated value: {value}")

# Check maximum chroma for initial spec
max_chroma = maximum_chroma_from_renotation([initial_spec[0], value, 0, initial_spec[3]])
print(f"Maximum chroma for hue={initial_spec[0]:.2f}, value={value:.2f}: {max_chroma}")

print(f"\nInitial chroma: {initial_spec[2]:.2f}")
print(f"Maximum allowed: {max_chroma:.2f}")
print(f"Initial is within bounds: {initial_spec[2] <= max_chroma}")