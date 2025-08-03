#!/usr/bin/env python3
"""Trace through the Python algorithm to understand the exact logic."""

import numpy as np

# Simulate the inner hue angle loop
def simulate_hue_loop(phi_input, phi_current_initial, debug=True):
    """Simulate Python's inner hue angle loop."""
    
    phi_differences = []
    hue_angle_differences = []
    
    # Initial difference
    phi_current_difference = (360 - phi_input + phi_current_initial) % 360
    if phi_current_difference > 180:
        phi_current_difference -= 360
    
    if debug:
        print(f"Initial: phi_input={phi_input:.3f}, phi_current={phi_current_initial:.3f}, diff={phi_current_difference:.3f}")
    
    # Python includes initial point
    phi_differences.append(phi_current_difference)
    hue_angle_differences.append(0)
    
    # Simulate iterations
    for i in range(1, 5):
        # Python: step by (phi_input - phi_current) * iteration_number
        hue_angle_diff = i * (phi_input - phi_current_initial)
        
        # Simulate getting new phi (this would come from munsell_specification_to_xy)
        # For our stuck case, let's assume small changes
        if abs(phi_current_difference) < 0.01:
            # When we're close, phi changes slowly
            phi_inner = phi_current_initial + hue_angle_diff * 0.5  # Simulated response
        else:
            phi_inner = phi_current_initial + hue_angle_diff * 0.9  # Larger response
        
        phi_inner_diff = (360 - phi_input + phi_inner) % 360
        if phi_inner_diff > 180:
            phi_inner_diff -= 360
            
        if debug:
            print(f"  Iteration {i}: hue_diff={hue_angle_diff:.3f}, phi_inner={phi_inner:.3f}, phi_diff={phi_inner_diff:.3f}")
        
        phi_differences.append(phi_inner_diff)
        hue_angle_differences.append(hue_angle_diff)
        
        # Check for sign change
        if not (all(d >= 0 for d in phi_differences) or all(d <= 0 for d in phi_differences)):
            if debug:
                print(f"  Sign change detected after {i} iterations")
            break
    
    # Linear interpolation to find where phi_diff = 0
    if len(phi_differences) >= 2:
        # Sort by phi_differences
        paired = sorted(zip(phi_differences, hue_angle_differences))
        phi_sorted = [p[0] for p in paired]
        hue_sorted = [p[1] for p in paired]
        
        # Find where phi_diff = 0
        for i in range(len(phi_sorted) - 1):
            if (phi_sorted[i] <= 0 <= phi_sorted[i+1]) or (phi_sorted[i] >= 0 >= phi_sorted[i+1]):
                # Interpolate
                t = -phi_sorted[i] / (phi_sorted[i+1] - phi_sorted[i])
                hue_correction = hue_sorted[i] + t * (hue_sorted[i+1] - hue_sorted[i])
                if debug:
                    print(f"  Interpolation: between ({phi_sorted[i]:.3f}, {hue_sorted[i]:.3f}) and ({phi_sorted[i+1]:.3f}, {hue_sorted[i+1]:.3f})")
                    print(f"  Result: hue_correction={hue_correction:.3f}")
                return hue_correction
    
    return 0

# Test cases
print("Case 1: Far from target (like iteration 0)")
simulate_hue_loop(2.402, 14.062)

print("\nCase 2: Close to target (like iteration 3)")
simulate_hue_loop(2.402, 2.402)

print("\nCase 3: Slightly off (like what we need)")
simulate_hue_loop(2.402, 2.5)