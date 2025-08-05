#!/usr/bin/env python3
"""Test the exact extrapolation logic from Python"""

# Looking at Python's colour-science code lines 1143-1224
# The key insight is HOW the loop works with extrapolation

# The loop condition is:
# while (all same sign) and not extrapolate:

# But wait, the logic is:
# 1. Check if len >= 2, set extrapolate = True
# 2. If not extrapolate, calculate and store phi_difference
# 3. Loop continues if (all same sign) and not extrapolate

# So once extrapolate=True, the loop SHOULD stop...
# Unless there's something else going on

# Let me check the actual Python behaviour by injecting print statements

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import munsell

# Monkey-patch to add debug output
original_xyy_to_munsell = munsell.xyY_to_munsell_specification

def debug_xyy_to_munsell(xyy, **kwargs):
    """Wrapper to trace the function"""
    # For RGB [68,0,68], xyy should be approximately [0.320938, 0.154190, 0.016466]
    if abs(xyy[0] - 0.320938) < 0.001 and abs(xyy[1] - 0.154190) < 0.001:
        print("INTERCEPTED xyY_to_munsell_specification for RGB [68,0,68]")
        # We can't easily inject into the middle of the function
        # But we know from the traces that it collects 4 points
    return original_xyy_to_munsell(xyy, **kwargs)

munsell.xyY_to_munsell_specification = debug_xyy_to_munsell

# Test
rgb = [68, 0, 68]
rgb_normalized = np.array(rgb) / 255.0
xyz = sRGB_to_XYZ(rgb_normalized)
xyy = XYZ_to_xyY(xyz)

result = munsell.xyY_to_munsell_specification(xyy)
print(f"Result: {result}")

# The mystery is: how does Python collect 4 points when the loop should stop after 2?
# 
# Looking more carefully at the trace data:
# phi_differences: [-7.458, -4.130, -0.077, 4.746]
# 
# After 2 points: extrapolate=True, all negative -> loop exits
# So these must be from MULTIPLE iterations of the OUTER loop!

print("\nINSIGHT: The 4 points might be accumulated across multiple outer iterations!")
print("Each outer iteration might add points to the same arrays.")