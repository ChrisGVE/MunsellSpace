#!/usr/bin/env python3
"""Generate aligned traces from Python and Rust starting from the same xyY input"""

import numpy as np
import subprocess
import sys

# Test color: RGB(221, 238, 238) -> xyY
xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])

print("Generating aligned traces for xyY:", xyY)
print()

# Generate Python trace starting directly from xyY
print("Generating Python trace...")
python_code = f"""
import numpy as np
from traced_python_munsell import (
    traced_xyY_to_munsell_specification,
    save_trace_to_file,
    clear_trace,
    enable_tracing,
    apply_monkey_patches
)

# Enable tracing
enable_tracing()
apply_monkey_patches()
clear_trace()

# Convert directly from xyY
xyY = np.array({list(xyY)})
print("Input xyY:", xyY)

# Run conversion
result = traced_xyY_to_munsell_specification(xyY)
print("Result:", result)

# Save trace
save_trace_to_file("python_trace_aligned.txt")
print("Python trace saved to python_trace_aligned.txt")
"""

with open("run_python_trace.py", "w") as f:
    f.write(python_code)

subprocess.run([sys.executable, "run_python_trace.py"])

print()
print("Generating Rust trace...")
# Rust trace should already start from xyY
subprocess.run(["cargo", "run", "--release", "--bin", "trace_color"], 
               capture_output=False)

print()
print("Traces generated:")
print("  - python_trace_aligned.txt")
print("  - rust_trace_ddeeee.txt")
print()
print("Now run: python3 analyze_traces.py python_trace_aligned.txt rust_trace_ddeeee.txt")