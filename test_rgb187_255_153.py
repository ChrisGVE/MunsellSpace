#!/usr/bin/env python3
"""Test the problematic RGB(187,255,153) color with -3.9 chroma error."""

import subprocess
import os

# Enable debug output
result = subprocess.run(
    ['cargo', 'run', '--release', '--bin', 'test_single'],
    env={**subprocess.os.environ, 'TEST_RGB': '187,255,153', 'RUST_BACKTRACE': '1'},
    capture_output=True,
    text=True,
    timeout=10
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR (first 100 lines):")
print('\n'.join(result.stderr.split('\n')[:100]))

# Also get the expected value
print("\n" + "="*80)
print("Expected: 8.5GY 9.3/12.8")
print("Got:     ", result.stdout.strip().replace("Success: ", ""))