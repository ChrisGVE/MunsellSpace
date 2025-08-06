#!/usr/bin/env python3
"""Quick accuracy test"""

import subprocess
import random

# Build once
print("Building Rust binary...")
subprocess.run(['cargo', 'build', '--release', '--bin', 'mathematical_convert_rgb'], check=True)

def test_specific_colors():
    """Test specific problematic colors"""
    test_cases = [
        (238, 0, 85),    # Previously problematic
        (68, 0, 68),     # Purple  
        (100, 150, 200), # Light blue
        (255, 0, 0),     # Red
        (0, 255, 0),     # Green
        (0, 0, 255),     # Blue
        (255, 255, 0),   # Yellow
        (255, 0, 255),   # Magenta
        (0, 255, 255),   # Cyan
        (128, 128, 128), # Gray
    ]
    
    print("\nTesting specific colors:")
    print("-" * 50)
    
    for r, g, b in test_cases:
        result = subprocess.run(
            ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
            capture_output=True,
            text=True
        )
        rust_munsell = result.stdout.strip()
        print(f"RGB({r:3}, {g:3}, {b:3}) → {rust_munsell}")

def test_reference_sample():
    """Test a small sample from reference dataset"""
    import csv
    
    print("\n\nTesting reference colors:")
    print("-" * 50)
    
    # Read some reference data
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        # Test first 10 colors
        count = 0
        matches = 0
        for row in reader:
            if count >= 10:
                break
            
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            ref_munsell = row[3].strip()
            
            result = subprocess.run(
                ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
                capture_output=True,
                text=True
            )
            rust_munsell = result.stdout.strip()
            
            match = "✓" if rust_munsell == ref_munsell else "✗"
            if rust_munsell == ref_munsell:
                matches += 1
            
            print(f"RGB({r:3}, {g:3}, {b:3}) → {rust_munsell:20} (ref: {ref_munsell:20}) {match}")
            count += 1
        
        print(f"\nExact matches: {matches}/10")

if __name__ == '__main__':
    test_specific_colors()
    test_reference_sample()