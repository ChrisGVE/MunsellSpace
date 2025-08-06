#!/usr/bin/env python3
"""Test Python's full conversion pipeline"""

import numpy as np
from colour import convert
from colour.notation.munsell import xyY_to_munsell_specification

# Test colors that fail in our Rust implementation
test_colors = [
    ([0, 0, 0], "black"),
    ([255, 255, 255], "white"),
    ([128, 128, 128], "grey"),
    ([255, 0, 0], "red"),
    ([0, 255, 0], "green"),
    ([0, 0, 255], "blue"),
    ([0, 68, 119], "reference 2.9PB 2.8/7.0"),
]

print("Testing Python's full sRGB → Munsell conversion pipeline:\n")

for rgb, name in test_colors:
    print(f"Testing {name} {rgb}:")
    
    # Convert sRGB to xyY (via XYZ)
    rgb_normalized = np.array(rgb) / 255.0
    xyz = convert(rgb_normalized, 'sRGB', 'CIE XYZ', illuminant='D65')
    xyy = convert(xyz, 'CIE XYZ', 'CIE xyY', illuminant='D65')
    
    print(f"  sRGB {rgb} → xyY: [{xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f}]")
    
    try:
        # Convert xyY to Munsell
        munsell_spec = xyY_to_munsell_specification(xyy)
        print(f"  Munsell spec: [hue={munsell_spec[0]:.3f}, value={munsell_spec[1]:.3f}, "
              f"chroma={munsell_spec[2]:.3f}, code={munsell_spec[3]}]")
        
        # Convert to notation
        from colour.notation.munsell import munsell_specification_to_munsell_colour
        notation = munsell_specification_to_munsell_colour(munsell_spec)
        print(f"  Munsell notation: {notation}")
        
    except Exception as e:
        print(f"  Error: {e}")
    
    print()

# Also test the exact xyY that fails in Rust
print("\nTesting specific xyY values that fail in Rust:")
failing_xyy = [
    ([0.640000, 0.330000, 0.212673], "red xyY"),
    ([0.185539, 0.187939, 0.054654], "2.9PB xyY"),
]

for xyy, name in failing_xyy:
    print(f"\nTesting {name}: {xyy}")
    try:
        munsell_spec = xyY_to_munsell_specification(np.array(xyy))
        print(f"  Munsell spec: [hue={munsell_spec[0]:.3f}, value={munsell_spec[1]:.3f}, "
              f"chroma={munsell_spec[2]:.3f}, code={munsell_spec[3]}]")
    except Exception as e:
        print(f"  Error: {e}")