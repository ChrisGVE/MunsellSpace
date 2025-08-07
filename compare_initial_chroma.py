#!/usr/bin/env python3

import numpy as np
from colour.models import XYZ_to_Lab, xyY_to_XYZ
from colour.algebra import cartesian_to_cylindrical

def analyze_initial_chroma(xyy):
    """Analyze how Python calculates initial chroma"""
    
    # Illuminant C
    x_center, y_center = 0.31006, 0.31616
    
    x, y, Y = xyy
    
    # Convert to Lab for initial guess
    xyz = xyY_to_XYZ(xyy)
    xyz_r = xyY_to_XYZ([x_center, y_center, Y])
    
    # Normalize reference
    xyz_r = xyz_r / xyz_r[1]
    
    Lab = XYZ_to_Lab(xyz, xyz_r)
    
    # Calculate LCHab
    L = Lab[0]
    a = Lab[1]
    b = Lab[2]
    C = np.hypot(a, b)
    H = np.degrees(np.arctan2(b, a))
    
    print(f"xyY: ({xyy[0]:.6f}, {xyy[1]:.6f}, {xyy[2]:.6f})")
    print(f"XYZ: ({xyz[0]:.6f}, {xyz[1]:.6f}, {xyz[2]:.6f})")
    print(f"XYZ_r: ({xyz_r[0]:.6f}, {xyz_r[1]:.6f}, {xyz_r[2]:.6f})")
    print(f"Lab: L={L:.3f}, a={a:.3f}, b={b:.3f}")
    print(f"LCHab: L={L:.3f}, C={C:.3f}, H={H:.3f}")
    
    # Python's initial chroma guess
    # From the code, it seems to use a simple conversion
    initial_chroma = C * 0.05  # This is a rough approximation
    print(f"Initial chroma estimate: {initial_chroma:.3f}")
    
    # Also calculate the polar coordinates
    rho_input, phi_input, _ = cartesian_to_cylindrical([x - x_center, y - y_center, Y])
    print(f"Polar coords: rho={rho_input:.6f}, phi={np.degrees(phi_input):.3f}")
    
    return initial_chroma

# Test our problem colors
print("=== RGB(34, 17, 119) - Deep blue ===")
analyze_initial_chroma(np.array([0.175340, 0.086753, 0.020725]))

print("\n=== RGB(221, 238, 238) - Near grey ===")
analyze_initial_chroma(np.array([0.3016456112, 0.3289687108, 0.8269427000]))