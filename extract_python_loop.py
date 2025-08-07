#!/usr/bin/env python3

import ast
import inspect

# Get the source of the Python function
from colour.notation import munsell

# Get the source code
source = inspect.getsource(munsell._chroma_from_renotation_ovoid)

# Find the critical loop
lines = source.split('\n')

print("=== PYTHON'S CHROMA CONVERGENCE LOOP ===")
print()

in_loop = False
loop_indent = 0
for i, line in enumerate(lines):
    if 'while not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data))' in line:
        in_loop = True
        loop_indent = len(line) - len(line.lstrip())
        print(f"Line {i}: {line}")
        continue
    
    if in_loop:
        current_indent = len(line) - len(line.lstrip())
        if line.strip() and current_indent <= loop_indent:
            # End of loop
            break
        if line.strip():
            print(f"Line {i}: {line}")

print("\n=== KEY OBSERVATIONS ===")
print("1. Loop condition: while NOT (min < rho_input < max)")
print("2. Increments iterations_inner BEFORE using it")
print("3. Uses (rho_input/rho_current)**iterations_inner for chroma")
print("4. Appends rho_inner and chroma_inner to bounds arrays")
print("5. After loop, sorts by rho and interpolates")