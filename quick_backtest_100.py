#!/usr/bin/env python3
"""Quick backtesting on first 100 colors after infinite loop fix"""

import subprocess
import csv
import json
from colour import notation
import numpy as np

def rust_to_munsell(r, g, b):
    """Call Rust implementation via test binary"""
    test_code = f"""
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {{
    let converter = PythonMunsellConverter::new();
    let rgb = [{r}u8, {g}u8, {b}u8];
    match converter.srgb_to_munsell(rgb) {{
        Ok(munsell) => println!("{{}}", munsell),
        Err(e) => eprintln!("ERROR: {{}}", e),
    }}
}}
"""
    
    with open('src/bin/test_temp.rs', 'w') as f:
        f.write(test_code)
    
    result = subprocess.run(
        ['cargo', 'run', '--bin', 'test_temp', '--release'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def python_to_munsell(r, g, b):
    """Call Python implementation"""
    rgb = np.array([r/255.0, g/255.0, b/255.0])
    try:
        # First convert RGB to xyY
        from colour import RGB_to_XYZ, XYZ_to_xyY
        from colour.models import RGB_COLOURSPACE_sRGB
        
        # RGB to XYZ
        XYZ = RGB_to_XYZ(rgb, RGB_COLOURSPACE_sRGB)
        
        # XYZ to xyY
        xyY = XYZ_to_xyY(XYZ)
        
        # xyY to Munsell
        munsell_colour = notation.xyY_to_munsell_colour(xyY)
        return munsell_colour
    except Exception as e:
        return None

# Build once
print("Building Rust binary...")
subprocess.run(['cargo', 'build', '--release', '--bin', 'test_simple_color'], 
               capture_output=True, text=True)

# Read test data
test_colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 100:  # Only test first 100
            break
        test_colors.append({
            'r': int(row['R']),
            'g': int(row[' G']),
            'b': int(row[' B']),
            'expected': row[' Munsell Colour']
        })

print(f"\nTesting {len(test_colors)} colors...")

exact_matches = 0
value_matches = 0
chroma_matches = 0
hue_matches = 0
total = 0

for i, color in enumerate(test_colors):
    if i % 10 == 0:
        print(f"Processing color {i}/{len(test_colors)}...")
    
    r, g, b = color['r'], color['g'], color['b']
    expected = color['expected']
    
    rust_result = rust_to_munsell(r, g, b)
    python_result = python_to_munsell(r, g, b)
    
    if rust_result and python_result:
        total += 1
        
        # Parse results
        try:
            # Parse Rust
            rust_parts = rust_result.split()
            rust_hue = rust_parts[0]
            rust_val, rust_chroma = rust_parts[1].split('/')
            rust_val = float(rust_val)
            rust_chroma = float(rust_chroma)
            
            # Parse Python
            py_parts = python_result.split()
            py_hue = py_parts[0]
            py_val, py_chroma = py_parts[1].split('/')
            py_val = float(py_val)
            py_chroma = float(py_chroma)
            
            # Check matches
            if abs(rust_val - py_val) <= 0.1:
                value_matches += 1
            if abs(rust_chroma - py_chroma) <= 0.1:
                chroma_matches += 1
            if rust_hue == py_hue:
                hue_matches += 1
            if rust_result == python_result:
                exact_matches += 1
            
            # Show mismatches
            if abs(rust_val - py_val) > 0.1 or abs(rust_chroma - py_chroma) > 0.1:
                print(f"  RGB({r},{g},{b}): Rust={rust_result}, Python={python_result}")
                print(f"    Value diff: {abs(rust_val - py_val):.3f}, Chroma diff: {abs(rust_chroma - py_chroma):.3f}")
                
        except Exception as e:
            pass

print("\n" + "="*60)
print("SUMMARY (First 100 colors):")
print(f"Total tested: {total}")
print(f"Exact matches: {exact_matches}/{total} ({exact_matches/total*100:.1f}%)")
print(f"Value within 0.1: {value_matches}/{total} ({value_matches/total*100:.1f}%)")  
print(f"Chroma within 0.1: {chroma_matches}/{total} ({chroma_matches/total*100:.1f}%)")
print(f"Hue family matches: {hue_matches}/{total} ({hue_matches/total*100:.1f}%)")
print(f"Overall accuracy (V&C within 0.1): {min(value_matches, chroma_matches)}/{total} ({min(value_matches, chroma_matches)/total*100:.1f}%)")

# Clean up
import os
if os.path.exists('src/bin/test_temp.rs'):
    os.remove('src/bin/test_temp.rs')