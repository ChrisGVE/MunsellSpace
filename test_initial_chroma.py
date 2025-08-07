#!/usr/bin/env python3

import numpy as np

def calculate_rust_initial(C):
    """Calculate what Rust would compute for initial chroma"""
    # From lchab_to_munsell_specification
    chroma_from_lchab = C / 5.0
    
    # From xyy_to_munsell_specification line 1227
    initial_chroma = (5.0 / 5.5) * chroma_from_lchab
    
    # Line 1228-1231: clamp if needed
    if np.isnan(initial_chroma) or initial_chroma < 0.1:
        initial_chroma = 1.0
    
    return initial_chroma

# Test cases
print("=== INITIAL CHROMA CALCULATION ===")
print()

test_cases = [
    (263.549, "Deep blue - RGB(34,17,119)"),
    (1397.239, "Near grey - RGB(221,238,238)"),
]

for C, description in test_cases:
    rust_initial = calculate_rust_initial(C)
    print(f"{description}:")
    print(f"  Lab C: {C:.3f}")
    print(f"  Rust initial chroma: {rust_initial:.3f}")
    print(f"  Formula: (5.0/5.5) * (C/5.0) = (5.0/5.5) * ({C:.1f}/5.0) = {rust_initial:.3f}")
    print()

print("But debug output shows:")
print("  Deep blue: initial chroma = 11.520")
print("  Near grey: initial chroma = 1.978")
print()
print("This suggests the Lab calculation itself is different or clamped")