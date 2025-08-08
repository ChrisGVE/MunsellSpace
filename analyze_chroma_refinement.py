#!/usr/bin/env python3
"""Analyze the chroma refinement difference"""

import numpy as np

# From our traces:
# Python: converges to 2.08
# Rust: converges to 1.56

# The formula is the same:
# chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current

# Test values from trace
rho_input = 0.015337748
rho_current_initial = 0.019664405
chroma_current_initial = 2.0

print("Analyzing chroma refinement formula")
print("="*60)
print(f"rho_input: {rho_input:.9f}")
print(f"rho_current (initial): {rho_current_initial:.9f}")
print(f"chroma_current (initial): {chroma_current_initial:.6f}")
print()

# Iteration 1
ratio = rho_input / rho_current_initial
print(f"Ratio (rho_input/rho_current): {ratio:.6f}")

# Test different iteration strategies
print("\nMethod 1: iterations_inner as sequential counter (1, 2, 3...)")
for i in range(1, 4):
    chroma = (ratio ** i) * chroma_current_initial
    print(f"  Iteration {i}: chroma = {ratio:.6f}^{i} * {chroma_current_initial:.1f} = {chroma:.6f}")

print("\nMethod 2: iterations_inner always 1 (bisection-like)")
chroma = chroma_current_initial
for i in range(1, 4):
    chroma = ratio * chroma  # Equivalent to (ratio ** 1) * chroma
    print(f"  Iteration {i}: chroma = {ratio:.6f} * {chroma:.6f} = {ratio * chroma:.6f}")
    chroma = ratio * chroma

print("\nMethod 3: Different initial chroma")
# If Python starts with huge chroma due to Lab bug
chroma_python_initial = 2079.0
for i in range(1, 4):
    chroma = (ratio ** i) * chroma_python_initial
    print(f"  Iteration {i}: chroma = {ratio:.6f}^{i} * {chroma_python_initial:.1f} = {chroma:.6f}")

print("\n" + "="*60)
print("INSIGHT:")
print("="*60)
print("The issue is NOT the formula itself, but rather:")
print("1. Python's huge initial chroma (2079) gets reduced drastically")
print("2. The convergence happens differently due to rho updates")
print("3. The inner loop may terminate at different points")
print()
print("We need to check:")
print("- How many inner iterations each implementation does")
print("- What the rho values are at each step")
print("- When the bracketing condition is satisfied")