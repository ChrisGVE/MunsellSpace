#!/usr/bin/env python3
"""Test maximum chroma lookup for the initial spec"""

from colour.notation.munsell import _maximum_chroma_from_renotation

# Test the initial spec that Rust is creating
test_specs = [
    (5.242, 9.277, 3, "Initial spec from Rust"),
    (7.181, 9.277, 3, "Converged spec from Rust"),
    (7.105611, 9.277364, 3, "Python's final spec"),
]

print("Testing maximum chroma lookups:")
for hue, value, code, desc in test_specs:
    try:
        max_chroma = _maximum_chroma_from_renotation(hue, value, code)
        print(f"{desc}: hue={hue:.3f}, value={value:.3f}, code={code}")
        print(f"  Maximum chroma: {max_chroma:.3f}")
    except Exception as e:
        print(f"{desc}: FAILED - {e}")
    print()