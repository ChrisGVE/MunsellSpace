#!/usr/bin/env python3
"""Check Python's chroma refinement formula"""

import numpy as np

# Simulate the chroma refinement loop
rho_input = 0.0155  # Example from our trace
rho_current = 0.0139  # Example starting rho
chroma_current = 2.0  # Starting chroma

print("Python's chroma refinement formula:")
print("chroma_inner = (rho_input / rho_current) ** iterations_inner * chroma_current")
print()
print(f"rho_input = {rho_input}")
print(f"rho_current = {rho_current}")
print(f"chroma_current = {chroma_current}")
print(f"ratio = rho_input / rho_current = {rho_input / rho_current:.6f}")
print()

print("Iterations:")
for iterations_inner in range(1, 6):
    # Python formula
    chroma_inner = (rho_input / rho_current) ** iterations_inner * chroma_current
    print(f"  iter {iterations_inner}: chroma = {rho_input/rho_current:.6f}^{iterations_inner} * {chroma_current} = {chroma_inner:.6f}")

print()
print("This shows the chroma increases exponentially with iterations_inner as the exponent")
print("The goal is to find a chroma that gives an rho between min and max bounds")