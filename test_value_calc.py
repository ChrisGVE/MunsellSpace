#!/usr/bin/env python3

import numpy as np

def luminance_astmd1535(V):
    """Forward function: Munsell value to Y"""
    if V <= 1:
        return V * (2.73 + V * (2.70 - 2.17 * V)) / 100
    else:
        V2 = V * V
        V3 = V2 * V
        V4 = V3 * V
        V5 = V4 * V
        return (1.1914 * V - 0.22533 * V2 + 0.23352 * V3 - 0.020484 * V4 + 0.00081939 * V5) / 100

def munsell_value_astmd1535(Y):
    """Newton-Raphson to solve the inverse"""
    Y = Y * 100  # Convert to percentage
    value = 10.0 * Y ** 0.5  # Initial guess
    
    for _ in range(100):
        y_current = luminance_astmd1535(value) * 100
        error = y_current - Y
        
        if abs(error) < 1e-10:
            break
        
        # Derivative
        v = value
        v2 = v * v
        v3 = v2 * v
        v4 = v3 * v
        derivative = 1.1914 - 2 * 0.22533 * v + 3 * 0.23352 * v2 - 4 * 0.020484 * v3 + 5 * 0.00081939 * v4
        
        value -= error / derivative
        value = max(0, min(10, value))
    
    return value

# Test with our Y values
Y_rust = 0.0207251690
Y_python = 0.0207288827

print(f"Y (Rust): {Y_rust:.10f} -> Value: {munsell_value_astmd1535(Y_rust):.6f}")
print(f"Y (Python): {Y_python:.10f} -> Value: {munsell_value_astmd1535(Y_python):.6f}")

# Test what Python actually does
from colour.notation.munsell import munsell_value_ASTMD1535
print(f"\nPython library:")
print(f"Y (Rust): {Y_rust:.10f} -> Value: {munsell_value_ASTMD1535(Y_rust * 100):.6f}")
print(f"Y (Python): {Y_python:.10f} -> Value: {munsell_value_ASTMD1535(Y_python * 100):.6f}")