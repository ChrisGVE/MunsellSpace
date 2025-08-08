#!/usr/bin/env python3
"""Detailed trace of convergence steps for both implementations"""

import numpy as np
from colour.notation import munsell
from colour import sRGB_to_XYZ
from colour.algebra import cartesian_to_cylindrical, euclidean_distance
from colour.models import xyY_to_XYZ, XYZ_to_Lab

def trace_python_convergence_detailed(rgb):
    """Trace Python's convergence in detail"""
    
    print(f"\n{'='*60}")
    print(f"PYTHON CONVERGENCE TRACE for RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
    print('='*60)
    
    # Convert to xyY
    rgb_norm = np.array(rgb) / 255.0
    xyz = sRGB_to_XYZ(rgb_norm)
    total = xyz[0] + xyz[1] + xyz[2]
    xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])
    
    print(f"Input xyY: [{xyy[0]:.10f}, {xyy[1]:.10f}, {xyy[2]:.10f}]")
    
    # Illuminant C
    x_center, y_center = 0.31006, 0.31616
    
    # Convert to Lab for initial guess
    xyz_r = xyY_to_XYZ([x_center, y_center, xyy[2]])
    Lab = XYZ_to_Lab(xyz, xyz_r)
    print(f"Lab: [{Lab[0]:.6f}, {Lab[1]:.6f}, {Lab[2]:.6f}]")
    
    # Convert to LCHab
    L = Lab[0]
    C = np.hypot(Lab[1], Lab[2])
    H = np.degrees(np.arctan2(Lab[2], Lab[1]))
    print(f"LCHab: L={L:.6f}, C={C:.6f}, H={H:.6f}")
    
    # Get initial hue from hue angle
    hue_initial, code_initial = munsell.hue_angle_to_hue(H)
    print(f"Initial hue from angle {H:.3f}: {hue_initial:.3f}, code={code_initial}")
    
    # Scale chroma
    chroma_initial = C * 0.2  # Approximate scaling
    print(f"Initial chroma estimate: {chroma_initial:.3f}")
    
    # Get value
    value = munsell.munsell_value_ASTMD1535(xyy[2] * 100)
    print(f"Value from Y={xyy[2]:.6f}: {value:.6f}")
    
    # Now trace actual convergence
    print(f"\n--- Starting Convergence ---")
    spec = munsell.xyY_to_munsell_specification(xyy)
    print(f"Final specification: {spec}")
    
    return spec

# Test RGB(221, 238, 238)
rgb = [221, 238, 238]

# Get xyY for comparison
rgb_norm = np.array(rgb) / 255.0
xyz = sRGB_to_XYZ(rgb_norm)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

spec = trace_python_convergence_detailed(rgb)

# Format as notation
hue = spec[0]
value = spec[1]
chroma = spec[2]
code = int(spec[3])

families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 
           6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
family = families.get(code, '?')

print(f"\nFinal notation: {hue:.1f}{family} {value:.1f}/{chroma:.1f}")
print(f"Reference:      7.1G 9.3/2.1")

# Now test what xy coordinates the reference specification gives
print(f"\n--- Reverse Check ---")
ref_spec = munsell.munsell_colour_to_munsell_specification("7.1G 9.3/2.1")
print(f"Reference specification: {ref_spec}")

ref_xyy = munsell.munsell_specification_to_xyY(ref_spec)
print(f"Reference xyY: {ref_xyy}")

# Compare xy values
print(f"\nInput xy:     [{xyy[0]:.10f}, {xyy[1]:.10f}]")
print(f"Reference xy: [{ref_xyy[0]:.10f}, {ref_xyy[1]:.10f}]")
print(f"Difference:   [{xyy[0]-ref_xyy[0]:.10f}, {xyy[1]-ref_xyy[1]:.10f}]")

distance = euclidean_distance([xyy[0], xyy[1]], [ref_xyy[0], ref_xyy[1]])
print(f"Euclidean distance: {distance:.10f}")