#!/usr/bin/env python3
"""Test bounding_hues_from_renotation to verify code increment logic"""

import numpy as np
from colour.notation.munsell import bounding_hues_from_renotation

# Test cases focusing on code increment at hue=0
test_cases = [
    (0.0, 1),   # B family, hue=0
    (0.0, 2),   # BG family, hue=0
    (0.0, 3),   # G family, hue=0
    (0.0, 4),   # GY family, hue=0
    (0.0, 5),   # Y family, hue=0
    (0.0, 6),   # YR family, hue=0
    (0.0, 7),   # R family, hue=0
    (0.0, 8),   # RP family, hue=0
    (0.0, 9),   # P family, hue=0
    (0.0, 10),  # PB family, hue=0
    (2.5, 5),   # Y family, standard hue
    (5.0, 5),   # Y family, standard hue
    (7.5, 5),   # Y family, standard hue
    (1.3, 5),   # Y family, non-standard hue
]

print("Python bounding_hues_from_renotation results:")
print("=" * 60)

for hue, code in test_cases:
    result = bounding_hues_from_renotation(np.array([hue, code]))
    # result is [[hue_cw, code_cw], [hue_ccw, code_ccw]]
    hue_cw, code_cw = result[0]
    hue_ccw, code_ccw = result[1]
    
    print(f"Input: hue={hue:.1f}, code={code}")
    print(f"  CW:  hue={hue_cw:.1f}, code={int(code_cw)}")
    print(f"  CCW: hue={hue_ccw:.1f}, code={int(code_ccw)}")
    
    # Special case analysis for hue=0
    if hue == 0.0:
        next_code = (code + 1) % 10
        if next_code == 0:
            next_code = 10
        print(f"  -> Python: (code + 1) % 10 = {(code + 1) % 10}, adjusted to {next_code}")
    print()