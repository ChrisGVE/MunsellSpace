#!/usr/bin/env python3
"""Quick test to check current accuracy after infinite loop fix"""

import subprocess
import json
from colour.notation import munsell
from colour import delta_E
import numpy as np

def rust_to_munsell(r, g, b):
    """Call Rust implementation"""
    result = subprocess.run(
        ['cargo', 'run', '--bin', 'rgb_to_munsell', '--', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def python_to_munsell(r, g, b):
    """Call Python implementation"""
    rgb = np.array([r/255.0, g/255.0, b/255.0])
    try:
        munsell_color = munsell.RGB_to_munsell_colour(rgb)
        return munsell_color
    except:
        return None

# Test a few specific colors
test_colors = [
    (221, 238, 238),  # The problematic color
    (255, 0, 0),      # Pure red
    (0, 255, 0),      # Pure green
    (0, 0, 255),      # Pure blue
    (128, 128, 128),  # Grey
    (255, 255, 255),  # White
    (0, 0, 0),        # Black
    (34, 17, 119),    # The other problematic color
]

print("Testing current accuracy after infinite loop fix:\n")
print("RGB\t\tRust\t\t\tPython\t\t\tMatch?")
print("-" * 80)

matches = 0
for r, g, b in test_colors:
    rust_result = rust_to_munsell(r, g, b)
    python_result = python_to_munsell(r, g, b)
    
    if rust_result and python_result:
        # Parse Rust result to get numerical values
        parts = rust_result.split()
        if len(parts) >= 2:
            rust_hue = parts[0]
            rust_val_chroma = parts[1].split('/')
            if len(rust_val_chroma) == 2:
                rust_value = float(rust_val_chroma[0])
                rust_chroma = float(rust_val_chroma[1])
                
                # Parse Python result
                py_parts = python_result.split()
                if len(py_parts) >= 2:
                    py_hue = py_parts[0]
                    py_val_chroma = py_parts[1].split('/')
                    if len(py_val_chroma) == 2:
                        py_value = float(py_val_chroma[0])
                        py_chroma = float(py_val_chroma[1])
                        
                        # Check if values match within tolerance
                        value_diff = abs(rust_value - py_value)
                        chroma_diff = abs(rust_chroma - py_chroma)
                        
                        match = value_diff <= 0.1 and chroma_diff <= 0.1
                        if match:
                            matches += 1
                        
                        print(f"({r:3},{g:3},{b:3})\t{rust_result:20}\t{python_result:20}\t{'✓' if match else '✗'}")
                        if not match:
                            print(f"  → Value diff: {value_diff:.3f}, Chroma diff: {chroma_diff:.3f}")

print(f"\nMatches: {matches}/{len(test_colors)} ({matches/len(test_colors)*100:.1f}%)")