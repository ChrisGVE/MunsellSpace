#!/usr/bin/env python3
"""Compare interpolation details between Python and Rust"""

import numpy as np
from colour.notation import munsell
import subprocess

def get_python_xy(spec):
    """Get xy from Python's xy_from_renotation_ovoid"""
    xy = munsell.xy_from_renotation_ovoid(spec)
    return xy

def trace_convergence_comparison():
    """Compare convergence details between Python and Rust"""
    
    print("="*80)
    print("CONVERGENCE COMPARISON: Python vs Rust")
    print("="*80)
    
    # Initial specification from trace
    spec_iter1 = [5.2418, 9.2774, 2.0, 3]
    
    print(f"\nIteration 1 specification: {spec_iter1}")
    
    # Python xy
    py_xy = get_python_xy(spec_iter1)
    print(f"Python xy_from_renotation: [{py_xy[0]:.6f}, {py_xy[1]:.6f}]")
    
    # From Rust trace
    print(f"Rust   xy_from_renotation: [0.301626, 0.335313]")
    
    # Check interpolation method
    method = munsell.interpolation_method_from_renotation_ovoid(spec_iter1)
    print(f"Interpolation method: {method}")
    
    # Check what happens at exact value 9.0
    print("\n--- Testing at value 9.0 ---")
    spec_v9 = [5.2418, 9.0, 2.0, 3]
    py_xy_v9 = get_python_xy(spec_v9)
    print(f"Python at value 9.0: [{py_xy_v9[0]:.6f}, {py_xy_v9[1]:.6f}]")
    
    # Check the renotation data being used
    print("\n--- Checking renotation data ---")
    
    # Test specific values that should be in the dataset
    test_specs = [
        [5.0, 9.0, 2.0, 3],  # Should exist in data
        [7.5, 9.0, 2.0, 3],  # Should exist in data
        [7.1, 9.0, 2.0, 3],  # May need interpolation
    ]
    
    for spec in test_specs:
        xy = get_python_xy(spec)
        print(f"Spec {spec} -> xy=[{xy[0]:.6f}, {xy[1]:.6f}]")
    
    # Now let's check what the final converged values give
    print("\n--- Final converged specifications ---")
    
    # Python converges to
    py_final = [7.12078279, 9.2774064, 2.08371095, 3]
    py_xy_final = get_python_xy(py_final)
    print(f"Python final: {py_final}")
    print(f"  -> xy=[{py_xy_final[0]:.6f}, {py_xy_final[1]:.6f}]")
    
    # Rust converges to
    rust_final = [7.181109, 9.277364, 1.555758, 3]
    rust_xy_final = get_python_xy(rust_final)
    print(f"Rust final: {rust_final}")
    print(f"  -> xy=[{rust_xy_final[0]:.6f}, {rust_xy_final[1]:.6f}]")
    
    # Check the target we're trying to reach
    print("\n--- Target xy ---")
    print("Target: [0.301656, 0.328990]")
    
    # Distance from target
    target = np.array([0.301656, 0.328990])
    py_dist = np.linalg.norm(py_xy_final - target)
    rust_dist = np.linalg.norm(rust_xy_final - target)
    
    print(f"Python distance from target: {py_dist:.10f}")
    print(f"Rust distance from target: {rust_dist:.10f}")

if __name__ == "__main__":
    trace_convergence_comparison()