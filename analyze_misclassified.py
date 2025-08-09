#!/usr/bin/env python3
"""Analyze misclassified colors and chroma differences."""

import subprocess
import sys
import csv
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification

def rust_to_spec(r, g, b):
    """Get Rust specification."""
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if line.startswith('Specification:'):
            # Parse: Specification: [9.9742087790, 9.5354473055, 1.9658427908, 6.0]
            spec_str = line.split('[')[1].split(']')[0]
            values = [float(x) for x in spec_str.split(',')]
            return values
    return None

def python_to_spec(r, g, b):
    """Get Python specification."""
    if r == 0 and g == 0 and b == 0:
        return [float('nan'), 0.0, float('nan'), float('nan')]
    
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    
    try:
        spec = xyY_to_munsell_specification(xyY)
        return list(spec)
    except:
        return None

# Read first 100 colors from reference
misclassified = []
large_chroma_diff = []
tested = 0

with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    
    for row in reader:
        if tested >= 100:  # Test first 100 for quick analysis
            break
            
        r, g, b = int(row[0]), int(row[1]), int(row[2])
        reference = row[3].strip()
        
        rust_spec = rust_to_spec(r, g, b)
        python_spec = python_to_spec(r, g, b)
        
        if rust_spec and python_spec:
            # Check for misclassified (different hue family)
            if not (python_spec[3] != python_spec[3]):  # Not NaN
                if abs(rust_spec[3] - python_spec[3]) > 0.5:
                    misclassified.append({
                        'rgb': (r, g, b),
                        'rust_code': rust_spec[3],
                        'python_code': python_spec[3],
                        'rust_spec': rust_spec,
                        'python_spec': python_spec
                    })
            
            # Check for large chroma differences
            if rust_spec[2] and python_spec[2]:  # Both have valid chroma
                chroma_diff = abs(rust_spec[2] - python_spec[2])
                if chroma_diff > 0.3:  # Significant difference
                    large_chroma_diff.append({
                        'rgb': (r, g, b),
                        'chroma_diff': chroma_diff,
                        'rust_chroma': rust_spec[2],
                        'python_chroma': python_spec[2],
                        'rust_value': rust_spec[1],
                        'python_value': python_spec[1]
                    })
        
        tested += 1

print("MISCLASSIFIED COLORS (different hue family):")
print("=" * 60)
for item in misclassified[:5]:  # Show first 5
    print(f"RGB{item['rgb']}: Rust code={item['rust_code']:.1f}, Python code={item['python_code']:.1f}")
    print(f"  Rust:   H={item['rust_spec'][0]:.2f}, V={item['rust_spec'][1]:.2f}, C={item['rust_spec'][2]:.2f}")
    print(f"  Python: H={item['python_spec'][0]:.2f}, V={item['python_spec'][1]:.2f}, C={item['python_spec'][2]:.2f}")

print(f"\nTotal misclassified: {len(misclassified)}/{tested}")

print("\n" + "=" * 60)
print("LARGE CHROMA DIFFERENCES (>0.3):")
print("=" * 60)

# Sort by chroma difference
large_chroma_diff.sort(key=lambda x: x['chroma_diff'], reverse=True)

for item in large_chroma_diff[:10]:  # Show top 10
    print(f"RGB{item['rgb']}: ΔC={item['chroma_diff']:.3f}")
    print(f"  Rust:   V={item['rust_value']:.2f}, C={item['rust_chroma']:.3f}")
    print(f"  Python: V={item['python_value']:.2f}, C={item['python_chroma']:.3f}")

print(f"\nTotal with large chroma diff: {len(large_chroma_diff)}/{tested}")

# Analyze patterns
print("\n" + "=" * 60)
print("PATTERN ANALYSIS:")
print("=" * 60)

# Check if high-value colors are overrepresented
high_value_chroma_issues = [x for x in large_chroma_diff if x['python_value'] > 8.5]
print(f"High-value (>8.5) colors with chroma issues: {len(high_value_chroma_issues)}/{len(large_chroma_diff)}")

# Check if low-chroma colors are overrepresented  
low_chroma_issues = [x for x in large_chroma_diff if x['python_chroma'] < 4.0]
print(f"Low-chroma (<4.0) colors with issues: {len(low_chroma_issues)}/{len(large_chroma_diff)}")

# Check value differences
avg_value_diff = sum(abs(x['rust_value'] - x['python_value']) for x in large_chroma_diff) / len(large_chroma_diff) if large_chroma_diff else 0
print(f"Average value difference in problem colors: {avg_value_diff:.4f}")