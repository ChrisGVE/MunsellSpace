#!/usr/bin/env python3
"""Debug what Rust should be getting for RP lookup"""

# For hue=0.628, code=8 (RP), value=1.313, chroma=8.117
# Rust needs to find bounding hues

# Standard hues in RP family: 2.5RP, 5.0RP, 7.5RP, 10RP
# hue=0.628 is between 10RP (previous family) and 2.5RP

# Since value=1.313 is not an integer, it will be rounded to 1.0
# And chroma=8.117 is not even, so it needs to interpolate

print("Debug Rust's RP lookup:")
print("=" * 60)
print("Input: hue=0.628RP, value=1.313, chroma=8.117")
print("\nStep 1: Round value to integer")
print("  value_normalized = 1.0")

print("\nStep 2: Check if standard hue")
print("  0.628 is NOT a standard hue (2.5, 5.0, 7.5, 10.0)")
print("  -> Need hue interpolation")

print("\nStep 3: Check if chroma is even")
print("  8.117 is NOT even (2, 4, 6, 8, 10...)")
print("  -> Need chroma interpolation")

print("\nStep 4: Get bounding hues")
print("  For 0.628RP:")
print("    Previous standard: 10P (code=9, wraps to previous family)")
print("    Next standard: 2.5RP (code=8)")
print("  BUT: If using bounding_hues_from_renotation, it would be:")
print("    CW: 10P (code=9)")
print("    CCW: 2.5RP (code=8)")

print("\nStep 5: Chroma interpolation")
print("  chroma_lower = 8.0")
print("  chroma_upper = 10.0")

print("\nStep 6: Lookup renotation data")
print("  Need to find:")
print("    - 10P value=1 chroma=8")
print("    - 2.5RP value=1 chroma=8")
print("    - 10P value=1 chroma=10")
print("    - 2.5RP value=1 chroma=10")

# The issue might be in how Rust handles the P/RP boundary
print("\n" + "=" * 60)
print("POTENTIAL ISSUE:")
print("When looking up 10P with value=1, Rust might be getting wrong data")
print("Or the boundary logic for P/RP transition might be incorrect")