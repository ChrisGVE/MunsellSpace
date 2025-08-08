#!/usr/bin/env python3
"""Test enhanced tracing for chroma and family issues"""

import subprocess
import sys

# Test case: RGB(221, 238, 238) - known chroma issue
print("Testing enhanced tracing for RGB(221, 238, 238)")
print("="*60)

# Run Rust with enhanced tracing
print("\nRust output (with enhanced tracing):")
print("-"*60)
result = subprocess.run(
    ["cargo", "run", "--bin", "trace_convergence_detail"],
    capture_output=True,
    text=True
)

# Filter for important trace lines
important_prefixes = [
    "TRACE|ITER_",
    "TRACE|HUE_",
    "TRACE|CHROMA_",
    "Final Munsell:",
]

for line in result.stderr.split('\n'):
    for prefix in important_prefixes:
        if prefix in line:
            print(line)
            break

# Also check stdout for final result
for line in result.stdout.split('\n'):
    if "Final" in line or "Munsell" in line:
        print(line)