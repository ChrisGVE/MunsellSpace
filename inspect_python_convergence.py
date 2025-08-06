#!/usr/bin/env python3
"""Inspect Python's xyY_to_munsell_specification convergence algorithm"""

import inspect
from colour.notation.munsell import xyY_to_munsell_specification

# Get the source code
source = inspect.getsource(xyY_to_munsell_specification)

# Save to file for easier reading
with open('python_xyy_to_munsell_source.txt', 'w') as f:
    f.write(source)

print("Source code saved to python_xyy_to_munsell_source.txt")

# Also let's trace through a simple example
import numpy as np

# Enable verbose output if possible
import colour
colour.set_options(print_warnings=True)

# Test with red
xyy = np.array([0.640000, 0.330000, 0.212673])
print(f"\nTesting red xyY: {xyy}")

try:
    spec = xyY_to_munsell_specification(xyy)
    print(f"Result: {spec}")
except Exception as e:
    print(f"Error: {e}")