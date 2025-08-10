#!/usr/bin/env python3
"""
Detailed analysis of RGB→Munsell conversion precision issues.
Focus on 4 specific colors with known ISCC-NBS classification problems.
"""

import subprocess
import sys
import numpy as np

# Ensure we use the venv colour library
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import colour
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

# Problem colors from ISCC-NBS analysis
PROBLEM_COLORS = [
    {
        'hex': '#EFDDE5',
        'rgb': [239, 221, 229],
        'issue': 'Expected chroma 1.5, got 1.6 - affects "pinkish white" vs "pale yellowish pink"'
    },
    {
        'hex': '#5C0625', 
        'rgb': [92, 6, 37],
        'issue': 'Expected R family, got 6.6RP - affects "very deep red" vs "very dark purplish red"'
    },
    {
        'hex': '#C7B6BD',
        'rgb': [199, 182, 189], 
        'issue': 'Expected chroma 1.5, got 1.6'
    },
    {
        'hex': '#481127',
        'rgb': [72, 17, 39],
        'issue': 'Expected R family, got 3.7RP'
    }
]

def trace_python_conversion(rgb):
    """Trace through Python's conversion step-by-step"""
    print(f"  Python conversion trace for RGB{rgb}:")
    
    # Step 1: sRGB to Linear RGB (gamma correction)
    srgb_norm = np.array(rgb) / 255.0
    print(f"    sRGB normalized: [{srgb_norm[0]:.6f}, {srgb_norm[1]:.6f}, {srgb_norm[2]:.6f}]")
    
    # Gamma correction (done inside sRGB_to_XYZ)
    def gamma_correct(c):
        if c <= 0.04045:
            return c / 12.92
        else:
            return np.power((c + 0.055) / 1.055, 2.4)
    
    linear_rgb = np.array([gamma_correct(c) for c in srgb_norm])
    print(f"    Linear RGB: [{linear_rgb[0]:.6f}, {linear_rgb[1]:.6f}, {linear_rgb[2]:.6f}]")
    
    # Step 2: Linear RGB to XYZ
    xyz = sRGB_to_XYZ(srgb_norm)
    print(f"    XYZ: [{xyz[0]:.6f}, {xyz[1]:.6f}, {xyz[2]:.6f}]")
    
    # Step 3: XYZ to xyY
    xyy = XYZ_to_xyY(xyz)
    print(f"    xyY: x={xyy[0]:.8f}, y={xyy[1]:.8f}, Y={xyy[2]:.8f}")
    
    # Step 4: xyY to Munsell
    try:
        munsell_spec = xyY_to_munsell_specification(xyy)
        print(f"    Munsell spec: hue={munsell_spec[0]:.6f}, value={munsell_spec[1]:.6f}, chroma={munsell_spec[2]:.6f}, code={munsell_spec[3]:.0f}")
        return {
            'srgb_norm': srgb_norm,
            'linear_rgb': linear_rgb, 
            'xyz': xyz,
            'xyy': xyy,
            'munsell_spec': munsell_spec,
            'success': True
        }
    except Exception as e:
        print(f"    Python conversion failed: {e}")
        return {
            'srgb_norm': srgb_norm,
            'linear_rgb': linear_rgb,
            'xyz': xyz,
            'xyy': xyy,
            'munsell_spec': None,
            'success': False
        }

def get_rust_conversion(rgb):
    """Get Rust conversion result with detailed trace"""
    print(f"  Rust conversion for RGB{rgb}:")
    
    # First, let's build a Rust CLI tool if it doesn't exist
    rust_cli_code = '''
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
    
    // Get detailed conversion info
    let rgb_array = [r, g, b];
    println!("RGB input: [{}, {}, {}]", r, g, b);
    
    match converter.srgb_to_munsell(rgb_array) {
        Ok(munsell_str) => {
            println!("Munsell result: {}", munsell_str);
            
            // Try to get the specification
            match converter.srgb_to_specification(rgb_array) {
                Ok(spec) => {
                    println!("Specification: hue={:.6}, value={:.6}, chroma={:.6}, code={}", 
                             spec[0], spec[1], spec[2], spec[3] as u8);
                }
                Err(e) => {
                    println!("Could not get specification: {}", e);
                }
            }
        }
        Err(e) => {
            println!("Rust conversion failed: {}", e);
        }
    }
}
'''
    
    # Write the CLI tool
    with open('src/bin/precision_debug.rs', 'w') as f:
        f.write(rust_cli_code)
    
    # Build it
    build_result = subprocess.run(['cargo', 'build', '--release', '--bin', 'precision_debug'], 
                                capture_output=True, text=True)
    
    if build_result.returncode != 0:
        print("    Failed to build Rust CLI")
        print(f"    Error: {build_result.stderr}")
        return None
    
    # Run the conversion
    result = subprocess.run(['./target/release/precision_debug', str(rgb[0]), str(rgb[1]), str(rgb[2])],
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        print(f"    Rust output:")
        for line in lines:
            print(f"      {line}")
            
        # Parse the specification
        for line in lines:
            if line.startswith('Specification:'):
                parts = line.replace('Specification: hue=', '').replace(' value=', '').replace(' chroma=', '').replace(' code=', '').split(',')
                try:
                    return {
                        'munsell_spec': [float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])],
                        'success': True
                    }
                except:
                    pass
        
        return {'success': False}
    else:
        print(f"    Rust execution failed: {result.stderr}")
        return None

def compare_conversions(python_result, rust_result):
    """Compare Python vs Rust conversion results"""
    if not python_result['success'] or not rust_result or not rust_result['success']:
        print("    Cannot compare - one conversion failed")
        return
    
    py_spec = python_result['munsell_spec']
    rust_spec = rust_result['munsell_spec']
    
    print(f"  Precision Comparison:")
    print(f"    Python: hue={py_spec[0]:.6f}, value={py_spec[1]:.6f}, chroma={py_spec[2]:.6f}, code={py_spec[3]:.0f}")
    print(f"    Rust:   hue={rust_spec[0]:.6f}, value={rust_spec[1]:.6f}, chroma={rust_spec[2]:.6f}, code={rust_spec[3]:.0f}")
    
    # Calculate differences
    hue_diff = abs(py_spec[0] - rust_spec[0])
    value_diff = abs(py_spec[1] - rust_spec[1])
    chroma_diff = abs(py_spec[2] - rust_spec[2])
    code_diff = abs(py_spec[3] - rust_spec[3])
    
    print(f"    Differences:")
    print(f"      Δhue:   {hue_diff:.6f}")
    print(f"      Δvalue: {value_diff:.6f}")  
    print(f"      Δchroma:{chroma_diff:.6f}")
    print(f"      Δcode:  {code_diff:.0f}")
    
    # Identify critical differences
    critical_issues = []
    if hue_diff > 0.1:
        critical_issues.append(f"HUE DIFFERENCE: {hue_diff:.3f}")
    if value_diff > 0.1:
        critical_issues.append(f"VALUE DIFFERENCE: {value_diff:.3f}")
    if chroma_diff > 0.1:
        critical_issues.append(f"CHROMA DIFFERENCE: {chroma_diff:.3f}")
    if code_diff > 0:
        critical_issues.append(f"FAMILY CODE CHANGE: {py_spec[3]:.0f} → {rust_spec[3]:.0f}")
    
    if critical_issues:
        print(f"    CRITICAL ISSUES:")
        for issue in critical_issues:
            print(f"      • {issue}")
    else:
        print(f"    ✓ No critical differences")

def analyze_intermediate_steps(python_result):
    """Analyze intermediate conversion steps for potential precision loss"""
    print(f"  Intermediate Step Analysis:")
    
    # Check gamma correction precision
    srgb = python_result['srgb_norm']
    linear = python_result['linear_rgb']
    
    print(f"    Gamma correction precision:")
    for i, (s, l) in enumerate(zip(srgb, linear)):
        if s <= 0.04045:
            expected = s / 12.92
        else:
            expected = np.power((s + 0.055) / 1.055, 2.4)
        diff = abs(l - expected)
        print(f"      Channel {i}: {s:.6f} → {l:.8f} (expected {expected:.8f}, diff {diff:.10f})")
    
    # Check XYZ values against ITU-R BT.709 matrix
    xyz = python_result['xyz']
    print(f"    XYZ color space:")
    print(f"      X: {xyz[0]:.8f}")
    print(f"      Y: {xyz[1]:.8f} (luminance)")
    print(f"      Z: {xyz[2]:.8f}")
    
    # Check chromaticity calculation
    xyy = python_result['xyy']
    total_xyz = xyz[0] + xyz[1] + xyz[2]
    expected_x = xyz[0] / total_xyz if total_xyz > 0 else 0
    expected_y = xyz[1] / total_xyz if total_xyz > 0 else 0
    
    print(f"    Chromaticity calculation:")
    print(f"      Sum XYZ: {total_xyz:.8f}")
    print(f"      x: {xyy[0]:.8f} (expected {expected_x:.8f}, diff {abs(xyy[0]-expected_x):.10f})")
    print(f"      y: {xyy[1]:.8f} (expected {expected_y:.8f}, diff {abs(xyy[1]-expected_y):.10f})")
    print(f"      Y: {xyy[2]:.8f} (matches XYZ Y: {abs(xyy[2]-xyz[1]):.10f})")

def main():
    print("="*80)
    print("RGB→MUNSELL CONVERSION PRECISION ANALYSIS")
    print("Focus on 4 specific ISCC-NBS classification problem colors")
    print("="*80)
    
    for color_info in PROBLEM_COLORS:
        print(f"\n{'-'*60}")
        print(f"Color: {color_info['hex']} RGB{color_info['rgb']}")
        print(f"Issue: {color_info['issue']}")
        print(f"{'-'*60}")
        
        # Trace Python conversion
        python_result = trace_python_conversion(color_info['rgb'])
        
        print()
        
        # Get Rust conversion
        rust_result = get_rust_conversion(color_info['rgb'])
        
        print()
        
        # Compare results
        compare_conversions(python_result, rust_result)
        
        print()
        
        # Analyze intermediate steps for precision issues
        if python_result['success']:
            analyze_intermediate_steps(python_result)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()