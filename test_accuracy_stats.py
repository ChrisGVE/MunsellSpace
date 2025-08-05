#!/usr/bin/env python3
"""Test accuracy statistics for mathematical converter"""

import subprocess
import random
import colour
import numpy as np
# from tqdm import tqdm

def rgb_to_munsell_python(r, g, b):
    """Convert RGB to Munsell using Python colour-science"""
    try:
        # Convert RGB [0-255] to [0-1]
        RGB = np.array([r/255.0, g/255.0, b/255.0])
        
        # Convert to Munsell
        munsell = colour.notation.RGB_to_Munsell(RGB, illuminant=np.array([0.31006, 0.31616]))
        return munsell, True
    except Exception as e:
        return str(e), False

def rgb_to_munsell_rust(r, g, b):
    """Convert RGB to Munsell using Rust mathematical converter"""
    try:
        result = subprocess.run(
            ['cargo', 'run', '--bin', 'mathematical_convert_rgb', str(r), str(g), str(b)],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip(), True
        else:
            return result.stderr.strip(), False
    except Exception as e:
        return str(e), False

def parse_munsell(munsell_str):
    """Parse Munsell string to extract value, hue, and chroma"""
    if munsell_str.startswith('N '):
        # Neutral color
        value = float(munsell_str.split()[1])
        return {'value': value, 'hue': 0.0, 'chroma': 0.0, 'is_neutral': True}
    
    # Parse regular Munsell notation
    parts = munsell_str.split(' ')
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    
    # Extract numeric hue
    hue_num = ''
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            break
    
    hue = float(hue_num) if hue_num else 0.0
    value = float(value_chroma[0])
    chroma = float(value_chroma[1])
    
    return {'value': value, 'hue': hue, 'chroma': chroma, 'is_neutral': False}

def compare_accuracy(num_samples=100):
    """Compare accuracy between Python and Rust implementations"""
    
    print(f"🔬 ACCURACY TEST: {num_samples} random colors")
    
    value_diffs = []
    hue_diffs = []
    chroma_diffs = []
    failures = 0
    
    for i in range(num_samples):
        if i % 10 == 0:
            print(f"  Progress: {i}/{num_samples}", end='\r')
        # Generate random RGB
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        
        # Convert with both systems
        python_result, python_success = rgb_to_munsell_python(r, g, b)
        rust_result, rust_success = rgb_to_munsell_rust(r, g, b)
        
        if not (python_success and rust_success):
            failures += 1
            continue
        
        # Parse results
        py_data = parse_munsell(python_result)
        rust_data = parse_munsell(rust_result)
        
        # Calculate differences
        value_diff = abs(py_data['value'] - rust_data['value'])
        value_diffs.append(value_diff)
        
        if not (py_data['is_neutral'] or rust_data['is_neutral']):
            hue_diff = abs(py_data['hue'] - rust_data['hue'])
            # Handle hue wraparound
            if hue_diff > 5.0:
                hue_diff = 10.0 - hue_diff
            hue_diffs.append(hue_diff)
            
            chroma_diff = abs(py_data['chroma'] - rust_data['chroma'])
            chroma_diffs.append(chroma_diff)
    
    # Calculate statistics
    print(f"\n📊 RESULTS ({num_samples - failures} successful conversions):")
    
    if value_diffs:
        value_within_0_1 = sum(1 for d in value_diffs if d <= 0.1) / len(value_diffs) * 100
        print(f"\nValue differences:")
        print(f"  Within 0.1: {value_within_0_1:.1f}%")
        print(f"  Max diff: {max(value_diffs):.3f}")
        print(f"  Mean diff: {np.mean(value_diffs):.3f}")
    
    if hue_diffs:
        hue_within_0_1 = sum(1 for d in hue_diffs if d <= 0.1) / len(hue_diffs) * 100
        print(f"\nHue differences:")
        print(f"  Within 0.1: {hue_within_0_1:.1f}%")
        print(f"  Max diff: {max(hue_diffs):.3f}")
        print(f"  Mean diff: {np.mean(hue_diffs):.3f}")
    
    if chroma_diffs:
        chroma_within_0_1 = sum(1 for d in chroma_diffs if d <= 0.1) / len(chroma_diffs) * 100
        print(f"\nChroma differences:")
        print(f"  Within 0.1: {chroma_within_0_1:.1f}%")
        print(f"  Max diff: {max(chroma_diffs):.3f}")
        print(f"  Mean diff: {np.mean(chroma_diffs):.3f}")
    
    print(f"\nExact matches: {sum(1 for v, h, c in zip(value_diffs, hue_diffs or [0]*len(value_diffs), chroma_diffs or [0]*len(value_diffs)) if v == 0 and h == 0 and c == 0)}")
    print(f"Failed conversions: {failures}")

if __name__ == '__main__':
    compare_accuracy(100)