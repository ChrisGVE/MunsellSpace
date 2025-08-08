#!/usr/bin/env python3
"""Trace RGB(187,255,153) with detailed output."""

import subprocess
import os

# Enable full tracing
os.environ['MUNSELL_TRACE'] = '1'

# Add trace output to Rust
with open('src/python_port.rs', 'r') as f:
    content = f.read()

# Check if we need to uncomment trace lines
if '// eprintln!("TRACE|' in content:
    print("Uncommenting trace statements...")
    content = content.replace('// eprintln!("TRACE|', 'eprintln!("TRACE|')
    with open('src/python_port.rs', 'w') as f:
        f.write(content)
    
    # Rebuild
    subprocess.run(['cargo', 'build', '--release'], capture_output=True)

# Run the test
result = subprocess.run(
    ['cargo', 'run', '--release', '--bin', 'test_single'],
    env={**subprocess.os.environ, 'TEST_RGB': '187,255,153'},
    capture_output=True,
    text=True,
    timeout=10
)

print("=== STDERR (TRACE OUTPUT) ===")
lines = result.stderr.split('\n')
for line in lines:
    if 'TRACE|' in line or 'DEBUG:' in line or 'Iteration' in line:
        print(line)

print("\n=== STDOUT (RESULT) ===")
print(result.stdout)

print("\n=== ANALYSIS ===")
print("Expected: 8.5GY 9.3/12.8")
print("Got:     ", result.stdout.strip().replace("Success: ", ""))

# Look for key chroma values in trace
for line in lines:
    if 'chroma' in line.lower() and 'TRACE' in line:
        print(f"  {line}")

# Re-comment trace lines to avoid noise
if 'eprintln!("TRACE|' in content:
    print("\nRe-commenting trace statements...")
    with open('src/python_port.rs', 'r') as f:
        content = f.read()
    content = content.replace('eprintln!("TRACE|', '// eprintln!("TRACE|')
    with open('src/python_port.rs', 'w') as f:
        f.write(content)