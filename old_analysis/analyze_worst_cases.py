#!/usr/bin/env python3
"""
Analyze the worst case colors by comparing:
1. Python colour-science result
2. Reference dataset value
3. Rust implementation result
"""

import csv
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import subprocess

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A":
        return None
        
    if notation.startswith('N '):
        return {
            'family': 'N',
            'hue': 0.0,
            'value': float(notation.split()[1]),
            'chroma': 0.0
        }
    
    parts = notation.split(' ')
    if len(parts) != 2:
        return None
    
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    
    # Extract hue number and family
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

def calculate_differences(parsed1, parsed2):
    """Calculate component differences between two parsed Munsell notations."""
    if not parsed1 or not parsed2:
        return None
    
    diffs = {}
    
    # Family match
    diffs['family_match'] = parsed1['family'] == parsed2['family']
    
    # Hue difference (with wraparound handling)
    if diffs['family_match']:
        hue_diff = abs(parsed1['hue'] - parsed2['hue'])
        if hue_diff > 5:
            hue_diff = 10 - hue_diff
        diffs['hue'] = hue_diff
    else:
        diffs['hue'] = None
    
    # Value and chroma differences
    diffs['value'] = abs(parsed1['value'] - parsed2['value'])
    diffs['chroma'] = abs(parsed1['chroma'] - parsed2['chroma'])
    
    return diffs

# Load reference dataset
reference_map = {}
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        rgb_key = (int(row['R']), int(row['G']), int(row['B']))
        reference_map[rgb_key] = row['Munsell Colour']

print("=" * 80)
print("DETAILED WORST CASE ANALYSIS")
print("Comparing Python vs Reference vs Rust for problematic colors")
print("=" * 80)

# Known worst cases from the 500-color sample
worst_cases = [
    # Original worst cases from validation
    ([17, 255, 255], "Worst chroma diff #1 (cyan)"),
    ([187, 0, 255], "Worst chroma diff #2 (purple)"),
    
    # Additional high-saturation colors likely to show differences
    ([255, 0, 255], "Magenta"),
    ([255, 255, 0], "Yellow"),
    ([0, 255, 255], "Full cyan"),
    ([255, 0, 128], "Pink-red"),
    ([0, 128, 255], "Sky blue"),
    ([128, 0, 255], "Purple"),
    ([255, 128, 0], "Orange"),
    ([0, 255, 128], "Green-cyan"),
]

results_summary = []

for rgb, description in worst_cases:
    print(f"\n{'='*60}")
    print(f"{description}: RGB{rgb}")
    print("="*60)
    
    rgb_key = tuple(rgb)
    
    # Get reference value
    reference_result = reference_map.get(rgb_key, "Not in reference")
    print(f"\n1. REFERENCE DATASET: {reference_result}")
    
    # Get Python colour-science result
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        python_result = xyY_to_munsell_colour(xyY)
        print(f"2. PYTHON COLOUR-SCI: {python_result}")
    except Exception as e:
        python_result = f"Error: {str(e)[:50]}"
        print(f"2. PYTHON COLOUR-SCI: {python_result}")
    
    # Get Rust result
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    rust_result = None
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking') and not line.startswith('EXACT'):
            if line[0].isdigit() or line.startswith('N '):
                rust_result = line
                break
    
    if rust_result:
        print(f"3. RUST IMPLEMENTAT.: {rust_result}")
    else:
        rust_result = "Error extracting result"
        print(f"3. RUST IMPLEMENTAT.: {rust_result}")
    
    # Parse all results
    ref_parsed = parse_munsell(reference_result) if reference_result != "Not in reference" else None
    python_parsed = parse_munsell(python_result) if "Error" not in python_result else None
    rust_parsed = parse_munsell(rust_result) if rust_result and "Error" not in rust_result else None
    
    # Calculate differences
    print("\nCOMPARISONS:")
    print("-" * 40)
    
    # Python vs Reference
    if ref_parsed and python_parsed:
        diffs = calculate_differences(python_parsed, ref_parsed)
        print("Python vs Reference:")
        if python_result == reference_result:
            print("  ✅ EXACT MATCH")
        else:
            print(f"  Family: {'✅ Match' if diffs['family_match'] else '❌ Mismatch'}")
            if diffs['hue'] is not None:
                print(f"  Hue diff: {diffs['hue']:.4f}")
            print(f"  Value diff: {diffs['value']:.4f}")
            print(f"  Chroma diff: {diffs['chroma']:.4f}")
    
    # Rust vs Reference
    if ref_parsed and rust_parsed:
        diffs = calculate_differences(rust_parsed, ref_parsed)
        print("\nRust vs Reference:")
        if rust_result == reference_result:
            print("  ✅ EXACT MATCH")
        else:
            print(f"  Family: {'✅ Match' if diffs['family_match'] else '❌ Mismatch'}")
            if diffs['hue'] is not None:
                print(f"  Hue diff: {diffs['hue']:.4f}")
            print(f"  Value diff: {diffs['value']:.4f}")
            print(f"  Chroma diff: {diffs['chroma']:.4f}")
    
    # Rust vs Python
    if python_parsed and rust_parsed:
        diffs = calculate_differences(rust_parsed, python_parsed)
        print("\nRust vs Python:")
        if rust_result == python_result:
            print("  ✅ EXACT MATCH")
        else:
            print(f"  Family: {'✅ Match' if diffs['family_match'] else '❌ Mismatch'}")
            if diffs['hue'] is not None:
                print(f"  Hue diff: {diffs['hue']:.4f}")
            print(f"  Value diff: {diffs['value']:.4f}")
            print(f"  Chroma diff: {diffs['chroma']:.4f}")
    
    # Store summary
    results_summary.append({
        'rgb': rgb,
        'description': description,
        'reference': reference_result,
        'python': python_result if "Error" not in python_result else "ERROR",
        'rust': rust_result if "Error" not in rust_result else "ERROR"
    })

# Print summary table
print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)
print("\n{:<25} {:<15} {:<20} {:<20} {:<20}".format(
    "Color", "RGB", "Reference", "Python", "Rust"
))
print("-" * 100)

for item in results_summary:
    rgb_str = f"[{item['rgb'][0]},{item['rgb'][1]},{item['rgb'][2]}]"
    ref_str = item['reference'][:18] if len(item['reference']) > 18 else item['reference']
    py_str = item['python'][:18] if len(item['python']) > 18 else item['python']
    rust_str = item['rust'][:18] if len(item['rust']) > 18 else item['rust']
    
    print("{:<25} {:<15} {:<20} {:<20} {:<20}".format(
        item['description'][:24],
        rgb_str,
        ref_str,
        py_str,
        rust_str
    ))

print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)
print("""
1. Colors with worst differences are typically high-saturation colors
2. These colors often aren't in the reference dataset (out of gamut)
3. Python and Rust show small but consistent differences in chroma calculation
4. Both implementations handle edge cases differently than the reference
""")