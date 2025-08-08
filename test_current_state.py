#!/usr/bin/env python3
"""Test current accuracy on a few colors without trace output"""

import subprocess
import tempfile
import os
import numpy as np
from colour.notation import munsell

def rust_to_munsell(r, g, b):
    """Convert RGB to Munsell using Rust implementation"""
    # Write a temp test program
    test_code = f"""
use munsellspace::{{MunsellColor, RgbColor}};

fn main() {{
    let rgb = RgbColor::new({r}, {g}, {b}).unwrap();
    match rgb.to_munsell_mathematical() {{
        Ok(munsell) => {{
            println!("{{}}", munsell);
        }}
        Err(e) => {{
            eprintln!("Error: {{}}", e);
            std::process::exit(1);
        }}
    }}
}}
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.rs', dir='src/bin', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Compile and run without trace output
        result = subprocess.run(
            ['cargo', 'run', '--bin', os.path.splitext(os.path.basename(temp_path))[0], '--release', '--quiet'],
            capture_output=True,
            text=True,
            timeout=10,
            env={**os.environ, 'RUST_LOG': ''}  # Disable logging
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    finally:
        os.unlink(temp_path)

def python_to_munsell(r, g, b):
    """Convert RGB to Munsell using Python colour-science"""
    from colour import sRGB_to_XYZ
    rgb = np.array([r, g, b]) / 255.0
    xyz = sRGB_to_XYZ(rgb)
    total = xyz[0] + xyz[1] + xyz[2]
    xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
    spec = munsell.xyY_to_munsell_specification(xyy)
    
    families = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
    if spec[3] > 0:
        family = families[int(spec[3]) - 1]
        return f"{spec[0]:.1f}{family} {spec[1]:.1f}/{spec[2]:.1f}"
    else:
        return f"N {spec[1]:.1f}"

# Test colors that had issues
test_colors = [
    (221, 238, 238),  # 7.2G vs 7.1G issue
    (34, 17, 119),    # #221177 - PB color  
    (255, 0, 0),      # Pure red
    (0, 255, 0),      # Pure green
    (0, 0, 255),      # Pure blue
    (128, 128, 128),  # Gray
]

print("Testing current accuracy:")
print("=" * 60)

matches = 0
for r, g, b in test_colors:
    python_result = python_to_munsell(r, g, b)
    rust_result = rust_to_munsell(r, g, b)
    
    match = "✓" if python_result == rust_result else "✗"
    print(f"RGB({r:3},{g:3},{b:3}): Python={python_result:12} Rust={rust_result:12} {match}")
    
    if python_result == rust_result:
        matches += 1

print("=" * 60)
print(f"Accuracy: {matches}/{len(test_colors)} = {100*matches/len(test_colors):.1f}%")