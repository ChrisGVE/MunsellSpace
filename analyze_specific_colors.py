#!/usr/bin/env python3
"""Analyze specific problematic colors from BACKTESTING_DETAILS.md."""

import subprocess
import sys
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

# Misclassified colors (wrong hue family)
misclassified = [
    ((68, 102, 68), "10.0GY→0.0G"),   # GY→G boundary
    ((85, 0, 51), "0.2R→10.0RP"),      # R→RP boundary
    ((119, 85, 221), "10.0PB→0.0P"),   # PB→P boundary
    ((136, 17, 68), "0.1R→10.0RP"),    # R→RP boundary
    ((153, 68, 51), "0.0YR→10.0R"),    # YR→R boundary
    ((170, 34, 0), "0.1YR→10.0R"),     # YR→R boundary
    ((170, 34, 85), "0.0R→10.0RP"),    # R→RP boundary
    ((221, 85, 204), "10.0P→0.0RP"),   # P→RP boundary
    ((255, 238, 238), "0.0Y→10.0YR"),  # Y→YR boundary (FIXED?)
]

# Top problematic colors by total difference
top_problematic = [
    ((34, 17, 102), "7.8PB", 0.5),    # ΔTotal=0.5
    ((34, 17, 119), "7.4PB", 0.5),    # ΔTotal=0.5
    ((85, 0, 34), "5.7R", 0.5),       # ΔTotal=0.5
    ((85, 0, 17), "0.3YR", 0.5),      # ΔTotal=0.5
    ((51, 0, 136), "8.3PB", 0.5),     # ΔTotal=0.5
    ((85, 0, 51), "0.2R", 0.5),       # ΔTotal=0.5 (misclassified)
    ((68, 0, 187), "8.3PB", 0.4),     # ΔTotal=0.4
    ((68, 0, 85), "5.4P", 0.4),       # ΔTotal=0.4
    ((85, 17, 238), "8.3PB", 0.4),    # ΔTotal=0.4
    ((136, 0, 204), "2.6P", 0.4),     # ΔTotal=0.4
]

print("=" * 80)
print("ANALYSIS OF MISCLASSIFIED COLORS (Family Changes)")
print("=" * 80)

for (r, g, b), transition in misclassified:
    print(f"\nRGB({r:3},{g:3},{b:3}): {transition}")
    
    rust_spec = rust_to_spec(r, g, b)
    python_spec = python_to_spec(r, g, b)
    
    if rust_spec and python_spec:
        print(f"  Python: H={python_spec[0]:5.2f}, V={python_spec[1]:.2f}, C={python_spec[2]:5.2f}, Code={python_spec[3]:.0f}")
        print(f"  Rust:   H={rust_spec[0]:5.2f}, V={rust_spec[1]:.2f}, C={rust_spec[2]:5.2f}, Code={rust_spec[3]:.0f}")
        
        # Analyze the boundary issue
        if abs(python_spec[0] - 0.0) < 0.5 or abs(python_spec[0] - 10.0) < 0.5:
            print(f"  → BOUNDARY ISSUE: Hue near 0.0 or 10.0")
        
        # Check chroma difference
        chroma_diff = abs(rust_spec[2] - python_spec[2])
        if chroma_diff > 0.2:
            print(f"  → CHROMA DIFF: {chroma_diff:.3f}")

print("\n" + "=" * 80)
print("ANALYSIS OF TOP PROBLEMATIC COLORS BY TOTAL DIFFERENCE")
print("=" * 80)

for (r, g, b), hue_family, total_diff in top_problematic:
    print(f"\nRGB({r:3},{g:3},{b:3}): {hue_family}, ΔTotal={total_diff}")
    
    rust_spec = rust_to_spec(r, g, b)
    python_spec = python_to_spec(r, g, b)
    
    if rust_spec and python_spec:
        print(f"  Python: H={python_spec[0]:5.2f}, V={python_spec[1]:.2f}, C={python_spec[2]:5.2f}")
        print(f"  Rust:   H={rust_spec[0]:5.2f}, V={rust_spec[1]:.2f}, C={rust_spec[2]:5.2f}")
        
        # Calculate individual differences
        h_diff = abs(rust_spec[0] - python_spec[0])
        v_diff = abs(rust_spec[1] - python_spec[1])
        c_diff = abs(rust_spec[2] - python_spec[2])
        
        print(f"  Diffs:  ΔH={h_diff:.3f}, ΔV={v_diff:.3f}, ΔC={c_diff:.3f}")
        
        # Identify patterns
        if python_spec[1] < 2.0:
            print(f"  → LOW VALUE: {python_spec[1]:.2f}")
        if python_spec[2] > 15.0:
            print(f"  → HIGH CHROMA: {python_spec[2]:.2f}")

print("\n" + "=" * 80)
print("PATTERN SUMMARY")
print("=" * 80)

# Count patterns in misclassified colors
boundary_issues = sum(1 for (r,g,b), _ in misclassified 
                      if "0.0" in _ or "10.0" in _)
print(f"Misclassified at hue boundaries (0.0 or 10.0): {boundary_issues}/{len(misclassified)}")

# Check value ranges in problematic colors
low_value_count = 0
high_chroma_count = 0

for (r, g, b), _, _ in top_problematic:
    python_spec = python_to_spec(r, g, b)
    if python_spec:
        if python_spec[1] < 2.0:
            low_value_count += 1
        if python_spec[2] > 15.0:
            high_chroma_count += 1

print(f"Top problematic with low value (<2.0): {low_value_count}/{len(top_problematic)}")
print(f"Top problematic with high chroma (>15.0): {high_chroma_count}/{len(top_problematic)}")