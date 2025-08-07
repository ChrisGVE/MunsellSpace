#!/usr/bin/env python3

import numpy as np

def test_loop_condition():
    """Test the loop condition edge cases"""
    
    # Test cases where rho_input might equal a bound
    test_cases = [
        ([0.25, 0.26], 0.255, "Between bounds"),
        ([0.25, 0.26], 0.25, "Equals min"),
        ([0.25, 0.26], 0.26, "Equals max"),
        ([0.25, 0.26], 0.24, "Below min"),
        ([0.25, 0.26], 0.27, "Above max"),
    ]
    
    print("Python condition: while not (min < rho_input < max)")
    print("This means: continue while rho_input <= min OR rho_input >= max")
    print()
    
    for bounds, rho_input, description in test_cases:
        min_val = np.min(bounds)
        max_val = np.max(bounds)
        
        # Python condition
        python_continue = not (min_val < rho_input < max_val)
        
        # Rust equivalent
        rust_continue = not (min_val < rho_input and rho_input < max_val)
        
        print(f"{description}:")
        print(f"  Bounds: [{min_val}, {max_val}], rho_input: {rho_input}")
        print(f"  Python continues: {python_continue}")
        print(f"  Rust continues: {rust_continue}")
        print(f"  Match: {python_continue == rust_continue}")
        print()

test_loop_condition()