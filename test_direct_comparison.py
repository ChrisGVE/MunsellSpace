#!/usr/bin/env python3
"""Direct comparison test after infinite loop fix"""

import subprocess
import sys
import os
from colour.notation import munsell
import numpy as np

# Build the Rust test binary first
print("Building Rust test binary...")
result = subprocess.run(['cargo', 'build', '--bin', 'test_simple_color'], capture_output=True, text=True)
if result.returncode != 0:
    print(f"Failed to build: {result.stderr}")
    sys.exit(1)

# Test colors
test_colors = [
    (221, 238, 238, "7.5BG 9.277364/2.084771"),  # The problematic color
    (255, 0, 0, "7.5R 5.398/20.076"),  # Pure red
    (128, 128, 128, "N 5.5"),  # Grey
    (34, 17, 119, "8.3PB 2.090/11.533"),  # Another problematic color
]

print("\nComparing Rust vs Python after infinite loop fix:")
print("=" * 80)

for r, g, b, expected in test_colors:
    print(f"\nRGB({r}, {g}, {b}):")
    print(f"  Expected: {expected}")
    
    # Get Python result
    rgb = np.array([r/255.0, g/255.0, b/255.0])
    try:
        python_result = munsell.RGB_to_munsell_colour(rgb)
        print(f"  Python:   {python_result}")
    except Exception as e:
        print(f"  Python:   ERROR - {e}")
        python_result = None
    
    # Get Rust result by writing and running a simple test
    test_code = f"""
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {{
    let converter = PythonMunsellConverter::new();
    let rgb = [{r}u8, {g}u8, {b}u8];
    match converter.srgb_to_munsell(rgb) {{
        Ok(munsell) => println!("{{}}", munsell),
        Err(e) => println!("ERROR: {{}}", e),
    }}
}}
"""
    
    with open('src/bin/test_color_temp.rs', 'w') as f:
        f.write(test_code)
    
    # Build and run
    result = subprocess.run(['cargo', 'run', '--bin', 'test_color_temp'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        rust_result = result.stdout.strip()
        print(f"  Rust:     {rust_result}")
        
        # Compare if both succeeded
        if python_result and rust_result and rust_result != "ERROR":
            # Parse both results
            try:
                # Parse Rust
                parts = rust_result.split()
                rust_hue = parts[0]
                rust_val, rust_chroma = parts[1].split('/')
                rust_val = float(rust_val)
                rust_chroma = float(rust_chroma)
                
                # Parse Python
                py_parts = python_result.split()
                py_hue = py_parts[0]
                py_val, py_chroma = py_parts[1].split('/')
                py_val = float(py_val)
                py_chroma = float(py_chroma)
                
                # Calculate differences
                val_diff = abs(rust_val - py_val)
                chroma_diff = abs(rust_chroma - py_chroma)
                
                print(f"  Differences:")
                print(f"    Value:  {val_diff:.6f} {'✓' if val_diff <= 0.1 else '✗'}")
                print(f"    Chroma: {chroma_diff:.6f} {'✓' if chroma_diff <= 0.1 else '✗'}")
                print(f"    Hue:    {rust_hue} vs {py_hue} {'✓' if rust_hue == py_hue else '✗'}")
            except:
                pass
    else:
        print(f"  Rust:     ERROR - {result.stderr}")

# Clean up
if os.path.exists('src/bin/test_color_temp.rs'):
    os.remove('src/bin/test_color_temp.rs')