#!/usr/bin/env python3
"""Trace convergence for RGB(187,255,153) - the problematic color"""

import sys
import os
import numpy as np

# Add InkyFingers to path
sys.path.insert(0, 'InkyFingers')

from colour import sRGB_to_XYZ
from colour.notation.munsell import xyY_to_munsell_specification
from colour.notation.munsell import (
    munsell_renotation_dataset
)
from colour.notation.munsell_renotation_ovoid import (
    maximum_chroma_from_renotation,
    xy_from_renotation_ovoid
)
from colour.algebra import euclidean_distance
from colour.models import XYZ_to_xyY

# Test RGB(187,255,153)
rgb = np.array([187, 255, 153]) / 255.0
print(f"Testing RGB: {[187, 255, 153]}")

# Convert to XYZ then xyY
xyz = sRGB_to_XYZ(rgb)
xyy = XYZ_to_xyY(xyz)
print(f"XYZ: {xyz}")
print(f"xyY: {xyy}")
print()

# Now trace the convergence
print("=== CONVERGENCE TRACE ===")

# Set up detailed tracing by monkey-patching
original_xy_from = xy_from_renotation_ovoid
iteration_count = 0

def traced_xy_from(specification):
    global iteration_count
    iteration_count += 1
    result = original_xy_from(specification)
    print(f"  Iter {iteration_count}: spec={specification} -> xy={result}")
    return result

# Temporarily replace function
import colour.notation.munsell_renotation_ovoid as mr
mr.xy_from_renotation_ovoid = traced_xy_from

# Run conversion
try:
    munsell = xyY_to_munsell_specification(xyy)
    print(f"\nFinal result: {munsell}")
    
    # Convert to string notation
    from colour.notation.munsell import munsell_colour_to_munsell_specification
    from colour.notation.munsell import munsell_specification_to_munsell_colour
    munsell_str = munsell_specification_to_munsell_colour(munsell)
    print(f"Munsell notation: {munsell_str}")
    
    print(f"\nExpected: 8.5GY 9.3/12.8")
    print(f"Got:      {munsell_str}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original function
    mr.xy_from_renotation_ovoid = original_xy_from