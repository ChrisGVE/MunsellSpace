#!/usr/bin/env python3
"""Test a single color through both implementations"""

import subprocess
import json

def test_rust(rgb):
    """Test Rust implementation"""
    # Create a simple Rust test program
    rust_code = f'''
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {{
    let rgb = [{rgb[0]}u8, {rgb[1]}u8, {rgb[2]}u8];
    let converter = PythonMunsellConverter::new();
    
    match converter.srgb_to_munsell(rgb) {{
        Ok(munsell) => {{
            println!("{{}}", munsell.notation);
        }}
        Err(e) => {{
            eprintln!("Error: {{:?}}", e);
        }}
    }}
}}
'''
    
    # Write to temp file
    with open('/tmp/test_rust.rs', 'w') as f:
        f.write(rust_code)
    
    # Compile and run
    subprocess.run(['rustc', '--edition', '2021', '-L', 'target/release/deps', '/tmp/test_rust.rs', '-o', '/tmp/test_rust'], check=True, capture_output=True)
    result = subprocess.run(['/tmp/test_rust'], capture_output=True, text=True)
    return result.stdout.strip()

def test_python(rgb):
    """Test Python implementation"""
    import numpy as np
    from colour import sRGB_to_XYZ
    from colour.notation import munsell
    
    rgb_norm = np.array(rgb) / 255.0
    xyz = sRGB_to_XYZ(rgb_norm)
    total = xyz[0] + xyz[1] + xyz[2]
    xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
    
    spec = munsell.xyY_to_munsell_specification(xyy)
    
    # Format as notation
    hue = spec[0]
    value = spec[1]
    chroma = spec[2]
    code = int(spec[3])
    
    families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
               6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
    family = families.get(code, '?')
    
    if chroma < 0.05:
        return f"N {value:.1f}"
    else:
        return f"{hue:.1f}{family} {value:.1f}/{chroma:.1f}"

# Test RGB(221, 238, 238)
rgb = [221, 238, 238]
print(f"Testing RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")

python_result = test_python(rgb)
print(f"Python: {python_result}")

# For Rust, just compile and run our test binary
result = subprocess.run(['./target/release/test_xyz_flow'], capture_output=True, text=True)
# Extract the result line
for line in result.stdout.split('\n'):
    if line.startswith('Result:'):
        rust_result = line.split('Result: ')[1]
        print(f"Rust:   {rust_result}")
        break

print(f"Reference: 7.1G 9.3/2.1")