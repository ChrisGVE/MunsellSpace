#!/usr/bin/env python3
"""Quickly find family mismatches in sampled data"""

import subprocess
import csv
import re

pattern = re.compile(r'([\d.]+)?([A-Z]+)\s+([\d.]+)(?:/([\d.]+))?')

def get_family(notation):
    """Extract just the family from notation"""
    if notation.startswith('N '):
        return 'N'
    match = pattern.match(notation)
    if match:
        return match.group(2)
    return None

def test_color(r, g, b):
    """Test a single color and return Rust output"""
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None

print("Finding family mismatches (testing every 20th color)...")
print("=" * 70)

mismatches = []
total = 0

with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    
    for i, row in enumerate(reader):
        # Sample every 20th color for speed
        if i % 20 != 0:
            continue
            
        r, g, b, expected = int(row[0]), int(row[1]), int(row[2]), row[3].strip()
        
        rust_output = test_color(r, g, b)
        if rust_output:
            expected_family = get_family(expected)
            rust_family = get_family(rust_output)
            
            if expected_family and rust_family and expected_family != rust_family:
                mismatches.append({
                    'rgb': (r, g, b),
                    'expected': expected,
                    'rust': rust_output,
                    'exp_fam': expected_family,
                    'rust_fam': rust_family
                })
        
        total += 1

print(f"\nFound {len(mismatches)} family mismatches in {total} samples")

if mismatches:
    print("\nFamily mismatch examples:")
    print("-" * 80)
    
    for m in mismatches[:10]:
        print(f"RGB [{m['rgb'][0]:3},{m['rgb'][1]:3},{m['rgb'][2]:3}]: {m['expected']:15} -> {m['rust']:15} ({m['exp_fam']:2} -> {m['rust_fam']:2})")
    
    # Pattern analysis
    transitions = {}
    for m in mismatches:
        key = f"{m['exp_fam']} -> {m['rust_fam']}"
        transitions[key] = transitions.get(key, 0) + 1
    
    print("\nTransition patterns:")
    for trans, count in sorted(transitions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {trans}: {count} cases")
    
    # Test specific problematic colors
    print("\n" + "=" * 70)
    print("Testing specific problematic colors in detail:")
    print("=" * 70)
    
    if mismatches:
        # Take first mismatch for detailed analysis
        m = mismatches[0]
        r, g, b = m['rgb']
        
        print(f"\nRGB [{r},{g},{b}]:")
        print(f"  Expected: {m['expected']}")
        print(f"  Got:      {m['rust']}")
        
        # Get Python's conversion
        print("\n  Testing with Python colour-science...")
        test_script = f"""
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

rgb = [{r}, {g}, {b}]
rgb_normalized = np.array(rgb) / 255.0
xyz = sRGB_to_XYZ(rgb_normalized)
xyy = XYZ_to_xyY(xyz)

try:
    result = xyY_to_munsell_specification(xyy)
    hue, value, chroma, code = result
    
    # Format like our Rust output
    families = {{1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
                6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}}
    family = families.get(int(code), 'N')
    
    if chroma < 0.05:
        print(f"  Python:   N {{value:.1f}}")
    else:
        print(f"  Python:   {{hue:.1f}}{{family}} {{value:.1f}}/{{chroma:.1f}}")
except Exception as e:
    print(f"  Python:   ERROR - {{e}}")
"""
        
        with open('test_specific.py', 'w') as f:
            f.write(test_script)
        
        result = subprocess.run(
            ['./venv_comparison/bin/python', 'test_specific.py'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        
        # Check if it's a boundary case
        import re
        match = pattern.match(m['expected'])
        if match:
            hue = float(match.group(1)) if match.group(1) else 10.0
            print(f"\n  Expected hue: {hue:.1f}")
            if hue >= 9.0 or hue <= 2.5:
                print("  -> This is near a family boundary!")
        
        # Clean up
        import os
        os.remove('test_specific.py')