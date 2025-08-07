#!/usr/bin/env python3

import numpy as np
from colour.notation import munsell
import inspect

# Get the source code of the function
try:
    source = inspect.getsource(munsell._chroma_from_renotation_ovoid)
    print("=== Python _chroma_from_renotation_ovoid source ===")
    # Print lines around the chroma calculation
    lines = source.split('\n')
    for i, line in enumerate(lines):
        if 'rho_input / rho_current' in line:
            # Print context around this line
            start = max(0, i - 5)
            end = min(len(lines), i + 10)
            for j in range(start, end):
                if j == i:
                    print(f">>> {j}: {lines[j]}")
                else:
                    print(f"    {j}: {lines[j]}")
except Exception as e:
    print(f"Could not get source: {e}")

# Also test the actual calculation
print("\n=== Testing chroma calculation ===")
# Simulate the values we see in the debug output
rho_input = 0.143  # approximate value from debug
rho_current = 0.222  # approximate value from debug
chroma_current = 20.5  # from debug
iterations_inner = 1

# What Rust is doing (WRONG - using iterations_inner as exponent)
chroma_rust_wrong = ((rho_input / rho_current) ** iterations_inner) * chroma_current
print(f"Rust (wrong): ((rho_input/rho_current)^{iterations_inner}) * chroma = {chroma_rust_wrong:.3f}")

# What Python likely does (using a fixed exponent)
chroma_python_likely = ((rho_input / rho_current) ** 1.5) * chroma_current
print(f"Python (likely with ^1.5): {chroma_python_likely:.3f}")

chroma_python_2 = ((rho_input / rho_current) ** 2) * chroma_current
print(f"Python (if using ^2): {chroma_python_2:.3f}")