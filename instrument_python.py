#!/usr/bin/env python3

import numpy as np
import sys

# Monkey-patch the colour library to add instrumentation
import colour.notation.munsell as munsell_module

# Save original function
original_chroma_from_renotation = munsell_module._chroma_from_renotation_ovoid

def instrumented_chroma_from_renotation(*args, **kwargs):
    """Wrapper to trace the chroma convergence"""
    global trace_enabled
    
    if trace_enabled:
        x, y, Y, specification_current = args[:4]
        print(f"  _chroma_from_renotation_ovoid called:")
        print(f"    Target xy: ({x:.6f}, {y:.6f})")
        print(f"    Current spec: [{specification_current[0]:.3f}, {specification_current[1]:.3f}, {specification_current[2]:.3f}, {specification_current[3]}]")
    
    result = original_chroma_from_renotation(*args, **kwargs)
    
    if trace_enabled:
        print(f"    Result chroma: {result[2]:.6f}")
    
    return result

# Apply monkey patch
munsell_module._chroma_from_renotation_ovoid = instrumented_chroma_from_renotation

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

# Test specific colors
test_cases = [
    ([34, 17, 119], "Deep blue - overshoots"),
    ([221, 238, 238], "Near grey - undershoots"),
]

trace_enabled = False

for rgb, description in test_cases:
    print(f"\n{'='*60}")
    print(f"Test: RGB{tuple(rgb)} - {description}")
    print('='*60)
    
    rgb_norm = np.array(rgb) / 255.0
    xyz = sRGB_to_XYZ(rgb_norm)
    xyy = XYZ_to_xyY(xyz)
    
    print(f"xyY: ({xyy[0]:.10f}, {xyy[1]:.10f}, {xyy[2]:.10f})")
    
    # Enable tracing for this conversion
    trace_enabled = True
    spec = xyY_to_munsell_specification(xyy)
    trace_enabled = False
    
    print(f"\nFinal specification: [{spec[0]:.10f}, {spec[1]:.10f}, {spec[2]:.10f}, {spec[3]:.1f}]")
    print(f"Final chroma: {spec[2]:.10f}")