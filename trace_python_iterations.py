#!/usr/bin/env python3

import numpy as np

def simulate_python_chroma_loop():
    """Simulate Python's chroma convergence loop for our test color"""
    
    # Values from our test case RGB(34, 17, 119)
    rho_input = 0.142919  # From debug output
    rho_current = 0.222495  # Initial rho from chroma 20.5
    chroma_current = 20.5
    chroma_maximum = 20.5
    
    rho_bounds_data = [rho_current]
    chroma_bounds_data = [chroma_current]
    
    iterations_inner = 0
    iterations_maximum_inner = 16
    
    print(f"Starting: rho_input={rho_input:.6f}, rho_current={rho_current:.6f}")
    print(f"Initial chroma={chroma_current:.3f}")
    print()
    
    while not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)):
        iterations_inner += 1
        
        if iterations_inner > iterations_maximum_inner:
            print("Maximum iterations reached!")
            break
        
        # Python's calculation
        chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
        
        print(f"Iteration {iterations_inner}:")
        print(f"  rho_ratio = {rho_input/rho_current:.6f}")
        print(f"  exponent = {iterations_inner}")
        print(f"  ({rho_input/rho_current:.6f})^{iterations_inner} = {(rho_input/rho_current)**iterations_inner:.6f}")
        print(f"  chroma_inner = {chroma_inner:.6f}")
        
        if chroma_inner > chroma_maximum:
            chroma_inner = chroma_maximum
            print(f"  Clamped to maximum: {chroma_maximum:.3f}")
        
        # For this simulation, let's assume we get a new rho
        # In reality this would come from xy_from_renotation_ovoid_interpolated
        # Let's use approximate values from the debug output
        if iterations_inner == 1:
            rho_new = 0.164  # Approximate from debug
        elif iterations_inner == 2:
            rho_new = 0.148
        else:
            rho_new = 0.145
        
        rho_bounds_data.append(rho_new)
        chroma_bounds_data.append(chroma_inner)
        
        print(f"  New rho = {rho_new:.6f}")
        print(f"  Bounds: [{np.min(rho_bounds_data):.6f}, {np.max(rho_bounds_data):.6f}]")
        print(f"  Check: {np.min(rho_bounds_data):.6f} < {rho_input:.6f} < {np.max(rho_bounds_data):.6f}?", 
              np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data))
        print()
        
        rho_current = rho_new
        chroma_current = chroma_inner
        
        if iterations_inner >= 3:
            break  # Stop after a few iterations for debugging

if __name__ == "__main__":
    simulate_python_chroma_loop()