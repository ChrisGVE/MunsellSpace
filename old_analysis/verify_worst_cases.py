#!/usr/bin/env python3
"""
Verify the worst case colors individually with Python colour-science.
"""

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess

# Worst cases identified from 500-color sample
worst_cases = [
    ([0, 238, 17], "Worst hue difference"),
    ([17, 255, 255], "Worst chroma difference #1"),
    ([187, 0, 255], "Worst chroma difference #2"),
    # Add some additional edge cases
    ([255, 0, 0], "Pure red"),
    ([0, 255, 0], "Pure green"),
    ([0, 0, 255], "Pure blue"),
    ([255, 255, 255], "Pure white"),
    ([0, 0, 0], "Pure black"),
    ([128, 128, 128], "Medium gray"),
]

print("=" * 80)
print("VERIFYING WORST CASE COLORS WITH PYTHON COLOUR-SCIENCE")
print("=" * 80)

for rgb, description in worst_cases:
    print(f"\n{description}: RGB{rgb}")
    print("-" * 60)
    
    # Python colour-science calculation
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        python_result = xyY_to_munsell_colour(xyY)
        print(f"Python colour-science: {python_result}")
    except Exception as e:
        print(f"Python error: {e}")
        python_result = None
    
    # Rust implementation
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    # Extract Munsell notation from output
    rust_result = None
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking') and not line.startswith('EXACT'):
            if line[0].isdigit() or line.startswith('N '):
                rust_result = line
                break
    
    if rust_result:
        print(f"Rust implementation:   {rust_result}")
    else:
        print(f"Rust error: Could not extract result")
    
    # Compare
    if python_result and rust_result:
        if python_result == rust_result:
            print("✅ EXACT MATCH")
        else:
            print(f"❌ DIFFERENCE")
            
            # Parse and show component differences
            def parse_munsell(notation):
                if notation.startswith('N '):
                    return {'family': 'N', 'hue': 0.0, 
                           'value': float(notation.split()[1]), 'chroma': 0.0}
                parts = notation.split(' ')
                if len(parts) != 2:
                    return None
                hue_part = parts[0]
                value_chroma = parts[1].split('/')
                hue_num = ""
                for char in hue_part:
                    if char.isdigit() or char == '.':
                        hue_num += char
                    else:
                        family = hue_part[len(hue_num):]
                        break
                return {
                    'family': family,
                    'hue': float(hue_num) if hue_num else 0.0,
                    'value': float(value_chroma[0]),
                    'chroma': float(value_chroma[1]) if len(value_chroma) > 1 else 0.0
                }
            
            rust_p = parse_munsell(rust_result)
            python_p = parse_munsell(python_result)
            
            if rust_p and python_p:
                if rust_p['family'] != python_p['family']:
                    print(f"   Family mismatch: {rust_p['family']} vs {python_p['family']}")
                else:
                    hue_diff = abs(rust_p['hue'] - python_p['hue'])
                    if hue_diff > 5:
                        hue_diff = 10 - hue_diff
                    print(f"   Hue difference: {hue_diff:.4f}")
                
                print(f"   Value difference: {abs(rust_p['value'] - python_p['value']):.4f}")
                print(f"   Chroma difference: {abs(rust_p['chroma'] - python_p['chroma']):.4f}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)