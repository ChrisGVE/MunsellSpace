#!/usr/bin/env python3
"""Direct comparison between Rust and Python Munsell conversions"""

import subprocess
import colour
from colour.notation.munsell import xyY_to_munsell_specification
import numpy as np

# Test colors covering various cases
test_colors = [
    # Primary colors
    ([255, 0, 0], "Red"),
    ([0, 255, 0], "Green"),
    ([0, 0, 255], "Blue"),
    
    # Secondary colors
    ([255, 255, 0], "Yellow"),
    ([255, 0, 255], "Magenta"),
    ([0, 255, 255], "Cyan"),
    
    # Greys
    ([128, 128, 128], "Grey 50%"),
    ([64, 64, 64], "Grey 25%"),
    ([192, 192, 192], "Grey 75%"),
    
    # Complex colors from our test set
    ([100, 150, 200], "Sky Blue"),
    ([200, 100, 50], "Orange-Brown"),
    ([150, 200, 100], "Lime Green"),
    
    # The problematic BG colors
    ([0, 170, 187], "Problem BG 1"),
    ([0, 221, 238], "Problem BG 2"),
    ([0, 187, 204], "Problem BG 3"),
]

def format_munsell(spec):
    """Format Munsell specification as string"""
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

def python_rgb_to_munsell(rgb):
    """Convert RGB to Munsell using Python colour-science"""
    srgb = [c / 255.0 for c in rgb]
    xyz = colour.sRGB_to_XYZ(srgb)
    xyy = colour.XYZ_to_xyY(xyz)
    
    try:
        spec = xyY_to_munsell_specification(xyy)
        return format_munsell(spec), spec
    except Exception as e:
        return f"Error: {str(e)[:50]}", None

# Create Rust test program
rust_test_code = """
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 {
        eprintln!("Usage: {} R G B", args[0]);
        std::process::exit(1);
    }
    
    let r: u8 = args[1].parse().unwrap();
    let g: u8 = args[2].parse().unwrap();
    let b: u8 = args[3].parse().unwrap();
    
    let converter = PythonMunsellConverter::new();
    match converter.srgb_to_munsell([r, g, b]) {
        Ok(munsell) => {
            println!("{}", munsell);
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}
"""

# Write Rust test program
with open('src/bin/test_rust_python_compare.rs', 'w') as f:
    f.write(rust_test_code)

print("Building Rust test binary...")
result = subprocess.run(['cargo', 'build', '--release', '--bin', 'test_rust_python_compare'], 
                       capture_output=True, text=True)
if result.returncode != 0:
    print("Failed to build Rust binary")
    print(result.stderr)
    exit(1)

print("\n" + "="*80)
print("DIRECT COMPARISON: Rust vs Python colour-science")
print("="*80)

matches = 0
close_matches = 0
total = 0

for rgb, name in test_colors:
    print(f"\nRGB {rgb} ({name}):")
    
    # Get Python result
    python_result, python_spec = python_rgb_to_munsell(rgb)
    print(f"  Python:  {python_result}")
    
    # Get Rust result
    result = subprocess.run(['./target/release/test_rust_python_compare', 
                           str(rgb[0]), str(rgb[1]), str(rgb[2])],
                          capture_output=True, text=True)
    rust_result = result.stdout.strip()
    print(f"  Rust:    {rust_result}")
    
    # Compare
    if python_spec is not None and not rust_result.startswith("Error"):
        total += 1
        if python_result == rust_result:
            print("  ✓ EXACT MATCH")
            matches += 1
        else:
            # Check if they're close (within 0.1 for each component)
            try:
                # Parse Rust result
                if rust_result.startswith('N'):
                    # Grey color
                    rust_value = float(rust_result[1:])
                    if abs(python_spec[1] - rust_value) < 0.1:
                        print("  ~ Close match (grey)")
                        close_matches += 1
                    else:
                        print("  ✗ Mismatch")
                else:
                    # Parse colored result (e.g., "7.5GY 8.0/22.0")
                    parts = rust_result.split()
                    hue_family = parts[0]
                    value_chroma = parts[1].split('/')
                    
                    # Extract hue number
                    import re
                    hue_match = re.match(r'([\d.]+)([A-Z]+)', hue_family)
                    if hue_match:
                        rust_hue = float(hue_match.group(1))
                        rust_value = float(value_chroma[0])
                        rust_chroma = float(value_chroma[1])
                        
                        # Check closeness
                        hue_close = abs(python_spec[0] - rust_hue) < 0.2
                        value_close = abs(python_spec[1] - rust_value) < 0.1
                        chroma_close = abs(python_spec[2] - rust_chroma) < 0.2
                        
                        if hue_close and value_close and chroma_close:
                            print(f"  ~ Close match (Δhue={abs(python_spec[0]-rust_hue):.2f}, Δvalue={abs(python_spec[1]-rust_value):.2f}, Δchroma={abs(python_spec[2]-rust_chroma):.2f})")
                            close_matches += 1
                        else:
                            print("  ✗ Mismatch")
            except:
                print("  ? Could not parse for comparison")
    elif rust_result.startswith("Error") and python_result.startswith("Error"):
        print("  ~ Both errored (consistent)")
        total += 1
        matches += 1

print("\n" + "="*80)
print("SUMMARY:")
print(f"  Total valid comparisons: {total}")
print(f"  Exact matches: {matches} ({100*matches/total:.1f}%)" if total > 0 else "  No valid comparisons")
print(f"  Close matches: {close_matches} ({100*close_matches/total:.1f}%)" if total > 0 else "")
print(f"  Total aligned: {matches + close_matches} ({100*(matches + close_matches)/total:.1f}%)" if total > 0 else "")
print("="*80)