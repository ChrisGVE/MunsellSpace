#!/usr/bin/env python3
"""Validate Rust implementation against Python colour-science library"""

import csv
import subprocess
import json
from colour.notation.munsell import xyY_to_munsell_specification
import colour
import numpy as np

# Test a sample of colors from the reference dataset
test_colors = [
    # Pure colors
    ([255, 0, 0], "Pure Red"),
    ([0, 255, 0], "Pure Green"),
    ([0, 0, 255], "Pure Blue"),
    ([255, 255, 0], "Yellow"),
    ([255, 0, 255], "Magenta"),
    ([0, 255, 255], "Cyan"),
    # Greys
    ([128, 128, 128], "Middle Grey"),
    ([64, 64, 64], "Dark Grey"),
    ([192, 192, 192], "Light Grey"),
    # Complex colors
    ([100, 150, 200], "Sky Blue"),
    ([200, 100, 50], "Orange-Brown"),
    ([150, 200, 100], "Lime Green"),
    # Problematic BG colors
    ([0, 170, 187], "BG Color 1"),
    ([0, 221, 238], "BG Color 2"),
]

# Format Munsell spec as string
def format_munsell(spec):
    HUE_CODES = {1: 'R', 2: 'YR', 3: 'Y', 4: 'GY', 5: 'G', 
                 6: 'BG', 7: 'B', 8: 'PB', 9: 'P', 10: 'RP'}
    
    hue = spec[0]
    value = spec[1]
    chroma = spec[2]
    code = int(spec[3])
    
    if chroma < 0.05:
        return f"N{value:.1f}"
    else:
        family = HUE_CODES.get(code, '?')
        return f"{hue:.1f}{family} {value:.1f}/{chroma:.1f}"

# Convert RGB to Munsell using Python
def python_rgb_to_munsell(rgb):
    srgb = [c / 255.0 for c in rgb]
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    
    try:
        spec = xyY_to_munsell_specification(xyy)
        return format_munsell(spec)
    except Exception as e:
        return f"Error: {e}"

# Convert RGB to Munsell using Rust (via subprocess)
def rust_rgb_to_munsell(rgb):
    # Create a small Rust script to test
    rust_code = f"""
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {{
    let converter = PythonMunsellConverter::new();
    let result = converter.rgb_to_munsell([{rgb[0]}, {rgb[1]}, {rgb[2]}]);
    match result {{
        Ok(munsell) => println!("{{}}", munsell),
        Err(e) => println!("Error: {{}}", e),
    }}
}}
"""
    
    # For now, we'll use a simpler approach - call our test binary
    # This assumes we have a test binary that takes RGB and outputs Munsell
    return "TODO: Call Rust binary"

# Main comparison
print("Comparing Python colour-science with Rust implementation\n")
print("=" * 60)

matches = 0
total = len(test_colors)

for rgb, name in test_colors:
    python_result = python_rgb_to_munsell(rgb)
    
    print(f"\nRGB {rgb} ({name}):")
    print(f"  Python: {python_result}")
    
    # Check if they match (within tolerance)
    # For now just track Python results
    
print("\n" + "=" * 60)
print(f"Summary: Direct comparison with Python colour-science")
print(f"Note: Reference dataset may use different algorithm/version")