#!/usr/bin/env python3

import numpy as np

def test_xyy_conversion():
    """Compare xyY conversion between different methods"""
    
    # RGB (34, 17, 119) = #221177
    rgb = np.array([34, 17, 119])
    rgb_normalized = rgb / 255.0
    
    print(f"RGB: {rgb}")
    print(f"RGB normalized: {rgb_normalized}")
    print()
    
    # Method 1: Manual calculation (matching Rust implementation)
    print("=== METHOD 1: Manual (matching Rust) ===")
    
    # Gamma correction (sRGB -> linear RGB)
    linear_rgb = np.where(rgb_normalized <= 0.04045, 
                         rgb_normalized / 12.92, 
                         ((rgb_normalized + 0.055) / 1.055) ** 2.4)
    
    print(f"Linear RGB: {linear_rgb}")
    
    # sRGB matrix (ITU-R BT.709) - exactly as in Rust
    srgb_matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750], 
        [0.0193339, 0.1191920, 0.9503041]
    ])
    
    xyz = np.dot(srgb_matrix, linear_rgb)
    print(f"XYZ: {xyz}")
    
    # Convert to xyY
    xyz_sum = np.sum(xyz)
    if xyz_sum > 1e-10:
        xyY_manual = np.array([xyz[0] / xyz_sum, xyz[1] / xyz_sum, xyz[1]])
    else:
        xyY_manual = np.array([0.31006, 0.31616, xyz[1]])  # Illuminant C
    
    print(f"xyY (manual): ({xyY_manual[0]:.6f}, {xyY_manual[1]:.6f}, {xyY_manual[2]:.6f})")
    
    # Method 2: Using colour library
    print("\n=== METHOD 2: colour library ===")
    
    try:
        from colour import sRGB_to_XYZ, XYZ_to_xyY
        
        xyz_colour = sRGB_to_XYZ(rgb_normalized)
        xyY_colour = XYZ_to_xyY(xyz_colour)
        
        print(f"XYZ (colour): {xyz_colour}")
        print(f"xyY (colour): ({xyY_colour[0]:.6f}, {xyY_colour[1]:.6f}, {xyY_colour[2]:.6f})")
        
        # Compare the differences
        print(f"\n=== COMPARISON ===")
        xyz_diff = xyz_colour - xyz
        xyy_diff = xyY_colour - xyY_manual
        
        print(f"XYZ difference: {xyz_diff}")
        print(f"xyY difference: {xyy_diff}")
        print(f"xyY difference magnitude: {np.linalg.norm(xyy_diff):.8f}")
        
    except ImportError:
        print("colour library not available")

if __name__ == "__main__":
    test_xyy_conversion()