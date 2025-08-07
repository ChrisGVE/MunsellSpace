#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

from munsellspace import srgb_to_munsell

def debug_chroma_convergence():
    """Test RGB #221177 to debug chroma convergence algorithm"""
    
    # RGB (34, 17, 119) = #221177
    rgb = (34, 17, 119)
    
    print(f"=== DEBUGGING CHROMA CONVERGENCE ===")
    print(f"Testing RGB {rgb} = #{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
    print()
    
    try:
        munsell = srgb_to_munsell(rgb[0], rgb[1], rgb[2])
        print(f"Result: {munsell}")
        
        # Extract chroma from result
        if "N" not in munsell:
            parts = munsell.split('/')
            if len(parts) == 2:
                chroma = float(parts[1])
                print(f"Final chroma: {chroma:.3f}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_chroma_convergence()