#!/usr/bin/env python3
"""Trace chroma calculation for a problematic color"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import munsell
import subprocess

# Problematic color: #221177 (RGB 34, 17, 119)
# Python: 7.4PB 1.6/13.1
# Rust: 7.5PB 1.6/13.5
# Chroma difference: 0.367

r, g, b = 34, 17, 119
print(f"Testing RGB({r}, {g}, {b}) = #{r:02x}{g:02x}{b:02x}")
print("="*50)

# Python conversion with detailed tracing
srgb = [r/255.0, g/255.0, b/255.0]
print(f"sRGB: {srgb}")

xyz = sRGB_to_XYZ(srgb)
print(f"XYZ: {xyz}")

xyy = XYZ_to_xyY(xyz)
print(f"xyY: {xyy}")

# Manually trace through the conversion
print("\n--- Python munsell.xyY_to_munsell_specification ---")

# Import internal functions for tracing
from colour.notation.munsell import (
    _munsell_value_from_y,
    _hue_angle_from_xy,
    _chroma_from_renotation_ovoid,
    _xy_from_renotation_ovoid,
    _hue_angle_to_hue,
    _hue_to_ASTM_hue,
    _munsell_specification_from_xyY,
    normalise_munsell_specification
)

# Step by step
print(f"\n1. Input xyY: {xyy}")

# Calculate value
value = _munsell_value_from_y(xyy[2])
print(f"2. Munsell value from Y: {value}")

# Calculate hue angle
hue_angle = _hue_angle_from_xy(xyy[:2])
print(f"3. Hue angle from xy: {hue_angle}")

# Initial chroma estimate
xy_inner = _xy_from_renotation_ovoid(hue_angle, value, 2, 'inner')
xy_outer = _xy_from_renotation_ovoid(hue_angle, value, 2, 'outer')
print(f"4. xy_inner at chroma=2: {xy_inner}")
print(f"   xy_outer at chroma=2: {xy_outer}")

# Get specification through full conversion
spec = munsell.xyY_to_munsell_specification(xyy)
print(f"\n5. Final specification: {spec}")
print(f"   Hue: {spec[0]}, Value: {spec[1]}, Chroma: {spec[2]}, Code: {spec[3]}")

notation = munsell.munsell_specification_to_munsell_colour(spec, 1, 1, 1)
print(f"6. Notation: {notation}")

# Now test Rust
print("\n--- Rust Conversion ---")
result = subprocess.run(
    ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
    capture_output=True, text=True
)

if result.returncode == 0:
    print(result.stdout)
    
    # Parse Rust output
    if 'Munsell:' in result.stdout:
        rust_notation = result.stdout.split('Munsell:')[1].strip()
        rust_spec = munsell.munsell_colour_to_munsell_specification(rust_notation)
        print(f"Rust specification: {rust_spec}")
        
        print("\n--- Differences ---")
        print(f"Hue: {spec[0]} (Python) vs {rust_spec[0]} (Rust) = {abs(spec[0] - rust_spec[0]):.6f}")
        print(f"Value: {spec[1]} (Python) vs {rust_spec[1]} (Rust) = {abs(spec[1] - rust_spec[1]):.6f}")
        print(f"Chroma: {spec[2]} (Python) vs {rust_spec[2]} (Rust) = {abs(spec[2] - rust_spec[2]):.6f}")
        
        # The key issue is chroma
        print(f"\nChroma error: {abs(spec[2] - rust_spec[2]):.6f}")
        print(f"Python chroma: {spec[2]:.10f}")
        print(f"Rust chroma: {rust_spec[2]:.10f}")

# Test the intermediate calculations in detail
print("\n--- Detailed Chroma Calculation Trace ---")

# We need to trace through _chroma_from_renotation_ovoid
# This is where the extrapolation happens for high chroma values
import inspect

# Get the actual chroma calculation
print("\nCalculating chroma from xyY...")
print(f"Input xy: {xyy[:2]}")
print(f"Hue angle: {hue_angle}")
print(f"Value: {value}")

# The issue is likely in the extrapolation when chroma > max in renotation data
# For PB colors with high chroma, this extrapolation is critical

# Check what the maximum chroma is for this hue/value combination
from colour.notation.munsell import MUNSELL_COLOURS_ALL

max_chroma_found = 0
for entry in MUNSELL_COLOURS_ALL:
    hue_str, val, chr = entry[0]
    if 'PB' in hue_str and abs(val - value) < 0.5:
        if chr > max_chroma_found:
            max_chroma_found = chr
            
print(f"\nMaximum chroma in data for PB near value {value}: {max_chroma_found}")
print(f"Our chroma ({spec[2]}) {'exceeds' if spec[2] > max_chroma_found else 'is within'} the data range")

if spec[2] > max_chroma_found:
    print("\n*** EXTRAPOLATION REQUIRED ***")
    print("This is likely where Python and Rust diverge!")