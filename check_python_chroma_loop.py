#!/usr/bin/env python3
"""Check the Python chroma refinement loop logic"""

import numpy as np

# Simulate the chroma refinement loop condition
def test_loop_condition():
    """Test when the loop should exit"""
    
    # Case 1: Normal bracketing
    rho_bounds_data = [0.2, 0.3]
    rho_input = 0.25
    rho_min = np.min(rho_bounds_data)
    rho_max = np.max(rho_bounds_data)
    
    # Python condition: while not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data))
    should_continue = not (rho_min < rho_input < rho_max)
    print(f"Case 1: rho_min={rho_min}, rho_input={rho_input}, rho_max={rho_max}")
    print(f"  Should continue? {should_continue} (expected: False)")
    
    # Case 2: rho_input too high (like our green case)
    rho_bounds_data = [0.21, 0.21, 0.21]  # All same value (hit max chroma)
    rho_input = 0.284
    rho_min = np.min(rho_bounds_data)
    rho_max = np.max(rho_bounds_data)
    
    should_continue = not (rho_min < rho_input < rho_max)
    print(f"\nCase 2: rho_min={rho_min}, rho_input={rho_input}, rho_max={rho_max}")
    print(f"  Should continue? {should_continue} (expected: True, will keep looping!)")
    
    # Case 3: After adding more bounds
    rho_bounds_data = [0.21, 0.21, 0.21, 0.21]  # Still all same
    rho_min = np.min(rho_bounds_data)
    rho_max = np.max(rho_bounds_data)
    
    should_continue = not (rho_min < rho_input < rho_max)
    print(f"\nCase 3: rho_min={rho_min}, rho_input={rho_input}, rho_max={rho_max}")
    print(f"  Should continue? {should_continue} (min==max, so can't bracket)")

test_loop_condition()

# Check what Python actually does
print("\n--- Checking Python's actual behavior ---")
from colour.notation.munsell.renotation import xyY_to_munsell_specification
import warnings

# Try a color that might hit max chroma
test_xyY = np.array([0.3, 0.6, 0.715152])  # Our green test case

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        result = xyY_to_munsell_specification(test_xyY)
        print(f"Python result: {result}")
    except Exception as e:
        print(f"Python error: {e}")