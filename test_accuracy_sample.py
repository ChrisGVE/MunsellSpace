#!/usr/bin/env python3
"""Test accuracy on a small sample"""

import subprocess
import json

# Test colors from the reference dataset
test_colors = [
    (0, 0, 0, "N 0.0"),           # Black
    (255, 255, 255, "N 10.0"),    # White
    (255, 0, 0, "7.1R 5.0/20.4"), # Red
    (0, 255, 0, "7.6GY 8.7/17.6"), # Green
    (0, 0, 255, "7.5PB 2.7/20.0"), # Blue
    (128, 128, 128, "N 5.2"),      # Grey
    (221, 238, 238, "7.1G 9.3/2.1"),  # Our test case
    (0, 68, 119, "2.9PB 2.8/7.0"),
    (51, 0, 0, "5.0R 0.9/2.5"),
    (100, 150, 200, "5.0PB 6.1/7.7"),
]

def test_color(r, g, b, expected):
    """Test a single color"""
    result = subprocess.run(
        ["./target/release/convert_rgb", str(r), str(g), str(b)],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return None, "ERROR"
    
    actual = result.stdout.strip()
    return actual, expected

print("Testing sample colors...")
print("=" * 60)

correct = 0
total = 0

for r, g, b, expected in test_colors:
    actual, exp = test_color(r, g, b, expected)
    
    if actual is None:
        print(f"RGB({r:3},{g:3},{b:3}): ERROR")
        continue
    
    match = actual == expected
    if match:
        correct += 1
    
    symbol = "✓" if match else "✗"
    print(f"RGB({r:3},{g:3},{b:3}): {actual:20} (expected: {expected:20}) {symbol}")
    total += 1

print("=" * 60)
print(f"Accuracy: {correct}/{total} = {correct/total*100:.1f}%")