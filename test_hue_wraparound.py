#!/usr/bin/env python3
"""Test what happens with hue values near 0 and 10"""

# In Munsell, hue goes from 0 to 10 within each family
# 0.1RP, 0.5RP, 1.0RP, ..., 9.5RP, 10.0RP
# Then it transitions to the next family:
# 10.0RP = 0.0P (conceptually), but represented as 0.1P, 0.5P, etc.

# The issue: Our Rust code might be producing 10.0P when it should produce 0.7RP

print("Testing hue wraparound logic:")
print("=" * 60)

# What should happen:
# - Hues are normally 0.1 to 10.0 within a family
# - 10.0 in one family = 0.0 in the next
# - But 0.0 is represented as 10.0 of the previous family

test_cases = [
    (0.7, 'RP', "Normal RP hue"),
    (9.9, 'RP', "High RP hue"),
    (10.0, 'RP', "Maximum RP hue (= 0.0P)"),
    (0.1, 'P', "Minimum P hue"),
    (9.9, 'P', "High P hue"),
    (10.0, 'P', "Maximum P hue (= 0.0PB)"),
]

for hue, family, description in test_cases:
    print(f"  {hue:4.1f}{family:2} - {description}")

print("\n" + "=" * 60)
print("HYPOTHESIS:")
print("=" * 60)
print("The convergence algorithm is producing hue=10.0 with code=9 (P)")
print("when it should produce hue=0.7 with code=8 (RP).")
print("")
print("This could happen if:")
print("1. The initial guess is wrong (starts in P instead of RP)")
print("2. The convergence pulls it to the wrong family")
print("3. The final normalization incorrectly handles the boundary")

import subprocess

# Test with more debug output
print("\n" + "=" * 60)
print("Testing RGB [68,0,68] with debug output:")
print("=" * 60)

result = subprocess.run(
    ['./target/release/mathematical_convert_rgb', '68', '0', '68'],
    capture_output=True,
    text=True
)

print(f"Result: {result.stdout.strip()}")

# Look for key debug info in stderr
if result.stderr:
    lines = result.stderr.split('\n')
    for line in lines:
        if 'Initial guess:' in line or 'Final state:' in line:
            print(f"  {line.strip()}")
        if 'convergence check' in line.lower():
            # Extract the iteration number if present
            import re
            match = re.search(r'iteration (\d+)', line, re.IGNORECASE)
            if match:
                iter_num = int(match.group(1))
                if iter_num < 3 or iter_num > 60:
                    print(f"  {line.strip()}")