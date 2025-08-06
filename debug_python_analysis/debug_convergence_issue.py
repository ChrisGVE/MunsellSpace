#!/usr/bin/env python3
"""Debug the convergence issue more deeply"""

import subprocess
import json

# Run with very detailed debug output
env = {'DEBUG_MUNSELL': '1', 'RUST_BACKTRACE': '1'}
result = subprocess.run(
    ['cargo', 'run', '--bin', 'mathematical_convert_rgb', '--', '204', '255', '170'],
    capture_output=True,
    text=True,
    env={**subprocess.os.environ, **env}
)

print("=== STDOUT ===")
print(result.stdout)
print("\n=== STDERR (focusing on convergence) ===")

# Extract key lines
lines = result.stderr.split('\n')
in_iteration = False
iteration_num = -1

for i, line in enumerate(lines):
    if "--- Iteration" in line:
        in_iteration = True
        iteration_num = int(line.split()[2])
        if iteration_num >= 3:  # Focus on iterations 3 and 4
            print(line)
    elif in_iteration and iteration_num >= 3:
        if any(key in line for key in [
            "Current:", "Hue refinement:", "Converged", "target=", 
            "After hue", "Before chroma loop", "Getting xy"
        ]):
            print(line)
        if "Converged" in line:
            # Print next few lines to see what happens
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip():
                    print(f"  AFTER CONVERGENCE: {lines[j]}")