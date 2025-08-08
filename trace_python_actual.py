#!/usr/bin/env python3
"""Trace the actual Python colour-science implementation for RGB(221,238,238)"""

import numpy as np
import sys
from colour.notation import munsell
from colour import RGB_to_XYZ, XYZ_to_xyY, xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab
from colour.models import RGB_COLOURSPACE_sRGB

# Monkey-patch to add tracing
original_xyY_to_munsell = munsell.xyY_to_munsell_specification

def traced_xyY_to_munsell(xyY, **kwargs):
    """Wrapper with tracing"""
    print(f"TRACE|xyY_to_munsell:ENTRY|xyY={xyY[0]:.6f},{xyY[1]:.6f},{xyY[2]:.6f}", file=sys.stderr)
    
    # Call original
    result = original_xyY_to_munsell(xyY, **kwargs)
    
    print(f"TRACE|xyY_to_munsell:EXIT|result={result}", file=sys.stderr)
    return result

# Patch it
munsell.xyY_to_munsell_specification = traced_xyY_to_munsell

# Also trace intermediate functions if accessible
if hasattr(munsell, 'munsell_specification_to_xy'):
    original_spec_to_xy = munsell.munsell_specification_to_xy
    
    def traced_spec_to_xy(specification):
        print(f"TRACE|spec_to_xy:CALL|spec={specification}", file=sys.stderr)
        result = original_spec_to_xy(specification)
        print(f"TRACE|spec_to_xy:RESULT|xy={result}", file=sys.stderr)
        return result
    
    munsell.munsell_specification_to_xy = traced_spec_to_xy

# Test RGB(221, 238, 238)
r, g, b = 221, 238, 238
print(f"\nTesting Python implementation for RGB({r},{g},{b})\n")

# Convert RGB to XYZ
rgb = np.array([r/255.0, g/255.0, b/255.0])
print(f"TRACE|main:RGB|rgb={rgb[0]:.6f},{rgb[1]:.6f},{rgb[2]:.6f}", file=sys.stderr)

XYZ = RGB_to_XYZ(rgb, RGB_COLOURSPACE_sRGB)
print(f"TRACE|main:XYZ|XYZ={XYZ[0]:.6f},{XYZ[1]:.6f},{XYZ[2]:.6f}", file=sys.stderr)

# XYZ to xyY
xyY = XYZ_to_xyY(XYZ)
print(f"TRACE|main:xyY|xyY={xyY[0]:.6f},{xyY[1]:.6f},{xyY[2]:.6f}", file=sys.stderr)

# xyY to Munsell
try:
    munsell_result = munsell.xyY_to_munsell_colour(xyY)
    print(f"\nPython Result: {munsell_result}")
    print(f"TRACE|main:RESULT|munsell={munsell_result}", file=sys.stderr)
except Exception as e:
    print(f"Error: {e}")
    print(f"TRACE|main:ERROR|error={e}", file=sys.stderr)

# Also calculate Lab/LCHab for comparison
Lab = XYZ_to_Lab(XYZ, illuminant=np.array([0.31006, 0.31616]))  # Illuminant C
print(f"TRACE|main:LAB|Lab={Lab[0]:.6f},{Lab[1]:.6f},{Lab[2]:.6f}", file=sys.stderr)

LCHab = Lab_to_LCHab(Lab)
print(f"TRACE|main:LCHAB|LCHab={LCHab[0]:.6f},{LCHab[1]:.6f},{LCHab[2]:.6f}", file=sys.stderr)