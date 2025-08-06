#!/usr/bin/env python3
"""Diagnose why our xy conversion doesn't match Python."""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xy, _munsell_specification_to_xyY

# Test case: hue=7.860852, value=5.219872, chroma=20.860931, code=7
spec = [7.860852, 5.219872, 20.860931, 7]

print("Testing munsell_specification_to_xy:")
print(f"  Input spec: hue={spec[0]:.6f}, value={spec[1]:.6f}, chroma={spec[2]:.6f}, code={spec[3]}")

# This is what Python uses internally
xy = munsell_specification_to_xy(spec)
print(f"  Python xy result: ({xy[0]:.12f}, {xy[1]:.12f})")

# Full xyY conversion
xyy = _munsell_specification_to_xyY(spec)
print(f"  Python xyY result: x={xyy[0]:.12f}, y={xyy[1]:.12f}, Y={xyy[2]:.12f}")

# What Rust reports for this spec
print(f"\n  Rust reports: xy=(0.634425, 0.329766)")
print(f"  Difference: dx={xy[0] - 0.634425:.12f}, dy={xy[1] - 0.329766:.12f}")

# Check if it's a chroma/value rounding issue
print("\nTesting with rounded values:")
spec_rounded = [7.86, 5.22, 20.86, 7]
xy_rounded = munsell_specification_to_xy(spec_rounded)
print(f"  Rounded spec: {spec_rounded}")
print(f"  → xy=({xy_rounded[0]:.12f}, {xy_rounded[1]:.12f})")

# Test with integer value
spec_int_value = [7.860852, 5.0, 20.860931, 7]
xy_int = munsell_specification_to_xy(spec_int_value)
print(f"\nWith integer value (5.0):")
print(f"  → xy=({xy_int[0]:.12f}, {xy_int[1]:.12f})")

# Test with even chroma
spec_even_chroma = [7.860852, 5.219872, 20.0, 7]
xy_even = munsell_specification_to_xy(spec_even_chroma)
print(f"\nWith even chroma (20.0):")
print(f"  → xy=({xy_even[0]:.12f}, {xy_even[1]:.12f})")

# Test exact renotation entry
print("\nTesting exact renotation entries:")
exact_specs = [
    [7.5, 5.0, 20.0, 7],  # Should be in dataset
    [10.0, 5.0, 20.0, 7],
]
for spec in exact_specs:
    xy = munsell_specification_to_xy(spec)
    print(f"  {spec} → xy=({xy[0]:.12f}, {xy[1]:.12f})")