#!/usr/bin/env python3
"""Trace Python's full convergence for RGB(221, 238, 238)"""

import numpy as np
from colour.notation.munsell import xyY_to_munsell_specification
from colour.models import XYZ_to_Lab, Lab_to_LCHab
from colour import CCS_ILLUMINANTS

# Monkey-patch to add debugging
import colour.notation.munsell

original_xyy_to_munsell = colour.notation.munsell.xyY_to_munsell_specification

iteration_count = 0

def debug_xyy_to_munsell(xyY):
    global iteration_count
    iteration_count = 0
    
    # Get the original function
    import inspect
    import types
    
    # Find the _xyY_to_munsell_specification function
    for name, obj in inspect.getmembers(colour.notation.munsell):
        if name == '_xyY_to_munsell_specification':
            original_inner = obj
            break
    
    def debug_inner(xyY):
        global iteration_count
        iteration_count += 1
        
        # Call original to get specification_current
        # We'll intercept at key points
        
        # Get initial spec through normal path
        x, y, Y = xyY
        X = x * Y / y
        Z = (1.0 - x - y) * Y / y
        XYZ = np.array([X, Y, Z])
        
        Lab = XYZ_to_Lab(XYZ, CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["C"])
        LCHab = Lab_to_LCHab(Lab)
        
        if iteration_count == 1:
            print(f"=== ITERATION {iteration_count} ===")
            print(f"Input xyY: {xyY}")
            print(f"XYZ: {XYZ}")
            print(f"Lab: {Lab}")
            print(f"LCHab: {LCHab}")
            
            # Try to determine initial spec
            # Python uses _LCHab_to_munsell_specification
            # which is likely a simple mapping
            
        return original_inner(xyY)
    
    # Replace temporarily
    colour.notation.munsell._xyY_to_munsell_specification = debug_inner
    result = original_xyy_to_munsell(xyY)
    # Restore
    colour.notation.munsell._xyY_to_munsell_specification = original_inner
    
    return result

# Test
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])
print("Testing RGB(221, 238, 238)")
print(f"Input xyY: {xyY}")
print()

result = debug_xyy_to_munsell(xyY)
print()
print(f"Final result: {result}")
print(f"Total iterations: {iteration_count}")