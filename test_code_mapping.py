#!/usr/bin/env python3
"""
Test the exact code mapping in Python's normalization.
"""

# Test Python's normalization for hue=0 with each code
test_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

code_to_family = {
    1: 'BG', 2: 'G', 3: 'GY', 4: 'Y', 5: 'YR',
    6: 'R', 7: 'RP', 8: 'P', 9: 'PB', 10: 'B'
}

print("Python normalization: if hue == 0: hue, code = 10, (code + 1) % 10")
print("=" * 60)

for code in test_codes:
    # Python formula from normalise_munsell_specification
    new_code_raw = (code + 1) % 10
    # But in Python, code 0 doesn't exist, it would be 10
    # Let me check the actual behavior
    
    print(f"Code {code:2d} ({code_to_family[code]:2s}) + 1 % 10 = {new_code_raw:2d}", end="")
    
    # Map 0 back to 10 since codes are 1-10
    if new_code_raw == 0:
        new_code = 10
        print(f" → 10 ({code_to_family[10]:2s})")
    else:
        new_code = new_code_raw
        print(f" → {new_code:2d} ({code_to_family[new_code]:2s})")

print("\nWait, this doesn't look right. Let me test with actual Python colour-science:")

import numpy as np
from colour.notation.munsell import normalise_munsell_specification

print("\nActual Python normalise_munsell_specification results:")
print("=" * 60)

for code in test_codes:
    spec = np.array([0.0, 5.0, 10.0, code])
    normalized = normalise_munsell_specification(spec)
    norm_hue, norm_value, norm_chroma, norm_code = normalized
    
    old_family = code_to_family[int(code)]
    if np.isnan(norm_code):
        new_family = "N"
        code_str = "N"
    else:
        nc = int(norm_code)
        if nc == 0:
            nc = 10
        new_family = code_to_family[nc]
        code_str = str(nc)
    
    print(f"[0.0, 5.0, 10.0, {code:2d}] ({old_family:2s}) → [{norm_hue:4.1f}, {norm_value:.1f}, {norm_chroma:.1f}, {code_str:>2s}] ({new_family:2s})")