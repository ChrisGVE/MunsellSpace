#!/usr/bin/env python3
"""
Detailed analysis of the 17 family mismatches between Rust and Python
to understand the root cause.
"""

import csv
import subprocess
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings
import math

warnings.filterwarnings('ignore')

def parse_munsell(notation):
    """Parse Munsell notation into components."""
    if not notation or notation == "N/A" or notation.startswith("ERROR"):
        return None
    notation = notation.strip()
    
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

# Family mismatches from our analysis
family_mismatches = [
    [68, 255, 221],   # G→BG
    [102, 51, 68],    # RP→R
    [136, 0, 68],     # RP→R
    [153, 51, 85],    # RP→R
    [170, 17, 85],    # RP→R
    [170, 255, 238],  # G→BG
    [204, 85, 119],   # RP→R
    [204, 34, 102],   # RP→R
    [204, 136, 153],  # RP→R
    [204, 221, 238],  # B→PB
    [221, 0, 102],    # R→RP (note: this is reverse!)
    [221, 68, 119],   # RP→R
    [221, 153, 170],  # RP→R
    [221, 238, 255],  # B→PB
    [255, 85, 136],   # RP→R
    [255, 204, 221],  # RP→R
    [255, 238, 238],  # YR→Y (note: Python says YR, Rust says Y)
]

print("=" * 80)
print("DETAILED FAMILY MISMATCH ANALYSIS")
print("=" * 80)

# Define hue angle ranges for families (from Python colour-science)
HUE_FAMILIES = [
    ('R', 0, 10),      # 0-10 and 350-360
    ('YR', 10, 50),    # 10-50
    ('Y', 50, 90),     # 50-90
    ('GY', 90, 110),   # 90-110
    ('G', 110, 170),   # 110-170
    ('BG', 170, 190),  # 170-190
    ('B', 190, 250),   # 190-250
    ('PB', 250, 290),  # 250-290
    ('P', 290, 330),   # 290-330
    ('RP', 330, 350),  # 330-350
]

def hue_angle_to_family(angle):
    """Convert hue angle to Munsell family."""
    # Normalize angle to 0-360
    angle = angle % 360
    
    for family, start, end in HUE_FAMILIES:
        if start <= angle < end:
            return family
    
    # Handle wraparound for R (350-360 and 0-10)
    if angle >= 350 or angle < 10:
        return 'R'
    
    return None

for i, rgb in enumerate(family_mismatches, 1):
    print(f"\n{i}. RGB{rgb}")
    print("-" * 60)
    
    # Get Python calculation with intermediate values
    try:
        rgb_norm = [c/255.0 for c in rgb]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        
        # Calculate hue angle manually
        x, y, Y = xyY
        
        # Illuminant C chromaticity (from Python colour-science)
        x_c, y_c = 0.31006, 0.31616
        
        # Calculate angle
        dx = x - x_c
        dy = y - y_c
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        if angle_deg < 0:
            angle_deg += 360
        
        python_munsell = xyY_to_munsell_colour(xyY)
        
        print(f"  XYZ: [{XYZ[0]:.6f}, {XYZ[1]:.6f}, {XYZ[2]:.6f}]")
        print(f"  xyY: [{x:.6f}, {y:.6f}, {Y:.6f}]")
        print(f"  Delta from C: dx={dx:.6f}, dy={dy:.6f}")
        print(f"  Hue angle: {angle_deg:.2f}°")
        print(f"  Expected family from angle: {hue_angle_to_family(angle_deg)}")
        print(f"  Python result: {python_munsell}")
        
    except Exception as e:
        print(f"  Python error: {e}")
    
    # Get Rust calculation
    input_data = f"{rgb[0]},{rgb[1]},{rgb[2]}"
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    rust_result = None
    for line in result.stdout.split('\n'):
        if line and not line.startswith('TRACE') and not line.startswith('Looking'):
            if line and (line[0].isdigit() or line.startswith('N ')):
                rust_result = line
                break
    
    print(f"  Rust result: {rust_result}")
    
    # Parse and compare
    if rust_result and python_munsell:
        rust_p = parse_munsell(rust_result)
        python_p = parse_munsell(python_munsell)
        
        if rust_p and python_p:
            print(f"\n  Comparison:")
            print(f"    Python: {python_p['family']} {python_p['hue']:.1f}")
            print(f"    Rust:   {rust_p['family']} {rust_p['hue']:.1f}")
            
            # Check if this is a boundary case
            if python_p['hue'] >= 9.5 or python_p['hue'] <= 0.5:
                print(f"    ⚠️  BOUNDARY CASE: Hue {python_p['hue']} near family edge")
            if rust_p['hue'] >= 9.5 or rust_p['hue'] <= 0.5:
                print(f"    ⚠️  BOUNDARY CASE: Rust hue {rust_p['hue']} near family edge")

# Summary patterns
print("\n" + "=" * 80)
print("PATTERN ANALYSIS")
print("=" * 80)

print("\nObservations:")
print("1. Most mismatches involve RP→R transitions (11 out of 17)")
print("2. Several are at family boundaries (9.5-10.0 or 0.0-0.5)")
print("3. Some involve B→PB and G→BG transitions")
print("4. One case has reversed mismatch: R→RP")

print("\nHypothesis:")
print("The issue appears to be in how Rust handles hue angles near family boundaries,")
print("particularly around the RP/R transition (330-350° and 350-10°)")