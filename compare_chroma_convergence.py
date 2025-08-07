#!/usr/bin/env python3

import numpy as np
from colour import *
import sys

def test_python_chroma_convergence():
    """Test Python's _chroma_from_renotation_ovoid with debug output"""
    
    # RGB (34, 17, 119) = #221177
    rgb = np.array([34, 17, 119]) / 255.0
    
    # Convert to xyY
    xyz = sRGB_to_XYZ(rgb)
    xyY = XYZ_to_xyY(xyz)
    
    print(f"Python xyY: ({xyY[0]:.6f}, {xyY[1]:.6f}, {xyY[2]:.6f})")
    
    # Call Python's algorithm directly
    try:
        # We need to find the hue angle and value first
        # Try different function names that might exist
        try:
            from colour.notation import munsell
            munsell_result = munsell.xyY_to_munsell(xyY)
        except:
            try:
                munsell_result = XYZ_to_munsell(xyY_to_XYZ(xyY))
            except:
                print("Cannot find munsell conversion function")
        print(f"Python result: {munsell_result}")
        
        # Extract chroma from Python result
        if munsell_result and len(munsell_result.split('/')) == 2:
            chroma_python = float(munsell_result.split('/')[1])
            print(f"Python chroma: {chroma_python:.6f}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def debug_python_algorithm():
    """Debug the Python algorithm step by step"""
    print("\n=== DEBUGGING PYTHON ALGORITHM ===")
    
    # Convert RGB to xyY manually like Rust does
    rgb = np.array([34/255.0, 17/255.0, 119/255.0])
    
    # Apply gamma correction (sRGB -> linear RGB)
    linear_rgb = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    
    # sRGB matrix (ITU-R BT.709)
    srgb_matrix = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750], 
        [0.0193339, 0.1191920, 0.9503041]
    ])
    
    xyz = np.dot(srgb_matrix, linear_rgb)
    
    # Convert to xyY
    xyz_sum = np.sum(xyz)
    if xyz_sum > 1e-10:
        xyY = np.array([xyz[0] / xyz_sum, xyz[1] / xyz_sum, xyz[1]])
    else:
        xyY = np.array([0.31006, 0.31616, xyz[1]])  # Illuminant C
    
    print(f"Manual xyY: ({xyY[0]:.6f}, {xyY[1]:.6f}, {xyY[2]:.6f})")
    
    # Now try Python's algorithm
    try:
        # Try different function names that might exist
        try:
            from colour.notation import munsell
            munsell_result = munsell.xyY_to_munsell(xyY)
        except:
            try:
                munsell_result = XYZ_to_munsell(xyY_to_XYZ(xyY))
            except:
                print("Cannot find munsell conversion function")
        print(f"Python result: {munsell_result}")
        
        if munsell_result and '/' in munsell_result:
            parts = munsell_result.split('/')
            if len(parts) == 2:
                chroma_python = float(parts[1])
                print(f"Python chroma: {chroma_python:.6f}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_python_chroma_convergence()
    debug_python_algorithm()