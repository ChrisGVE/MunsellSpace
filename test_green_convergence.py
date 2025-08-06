#!/usr/bin/env python3
"""Test green color convergence in Python"""

from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np

# Green test case
xyY = np.array([0.3, 0.6, 0.715152])

print(f"Testing green xyY {xyY}")

try:
    spec = xyY_to_munsell_specification(xyY)
    print(f"Success: {spec}")
    
    # Try converting back
    from colour.notation.munsell import munsell_specification_to_xyY
    xyY_back = munsell_specification_to_xyY(spec)
    print(f"Converted back to xyY: {xyY_back}")
    print(f"Difference: {np.linalg.norm(xyY - xyY_back):.6f}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()