#!/usr/bin/env python3
"""Test Rust's hue angle calculation"""

import subprocess
import json

# Create a simple Rust test program
rust_test = '''
fn main() {
    // Test hue_to_hue_angle for 8.548GY
    let hue = 8.548;
    let code = 4; // GY
    
    // Rust's calculation from hue_to_hue_angle
    let raw = (17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5;
    let single_hue = if raw < 0.0 {
        (raw % 10.0) + 10.0
    } else {
        raw % 10.0
    };
    // This is WRONG - should use interpolation not multiplication
    let angle_wrong = single_hue * 36.0;
    
    // Correct interpolation
    let breakpoints = vec![0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    let angles = vec![0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    
    let mut angle = 0.0;
    for i in 0..breakpoints.len()-1 {
        if single_hue >= breakpoints[i] && single_hue <= breakpoints[i+1] {
            let t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i]);
            angle = angles[i] + t * (angles[i+1] - angles[i]);
            break;
        }
    }
    
    println!("hue={}, code={}", hue, code);
    println!("raw={}", raw);
    println!("single_hue={}", single_hue);
    println!("angle_wrong (single_hue * 36.0) = {}", angle_wrong);
    println!("angle_correct (interpolated) = {}", angle);
}
'''

with open('test_hue_angle.rs', 'w') as f:
    f.write(rust_test)

# Compile and run
subprocess.run(['rustc', 'test_hue_angle.rs', '-o', 'test_hue_angle'])
result = subprocess.run(['./test_hue_angle'], capture_output=True, text=True)
print("Rust output:")
print(result.stdout)

# Python's calculation
from colour.notation.munsell import hue_to_hue_angle
import numpy as np

hue = 8.548
code = 4
angle = hue_to_hue_angle([hue, code])
print(f"\nPython's hue_to_hue_angle([{hue}, {code}]) = {angle}")

# Let's also check the boundaries
for h in [7.5, 8.548, 10.0]:
    angle = hue_to_hue_angle([h, 4])
    print(f"Python: {h}GY -> {angle}°")