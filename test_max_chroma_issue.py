#!/usr/bin/env python3
"""Test maximum chroma issue for green initial guess"""

import numpy as np
from colour.notation.munsell import maximum_chroma_from_renotation

# The initial spec causing issues
initial_spec = np.array([7.78198484, 9.37037846, 109.37445748, 5])

# Rounded values as used in Rust
hue = 7.877
value = 8.747
chroma = 22.595
code = 4  # GY

print(f"Initial spec: hue={hue:.3f}, value={value:.3f}, chroma={chroma:.3f}, code={code}")

# Check maximum chroma - Python needs (hue, value, code)
max_chroma = maximum_chroma_from_renotation(np.array([hue, value, code]))
print(f"Maximum chroma from renotation: {max_chroma}")

# The issue: chroma=22.595 but max for GY at this value might be lower

# Test different hues/codes at value=8.747
test_specs = [
    (7.5, 8.747, 4),   # 7.5GY
    (10.0, 8.747, 4),  # 10GY (becomes 0Y)
    (0.0, 8.747, 5),   # 0Y 
    (7.877, 8.747, 4), # Our problematic hue
]

for test_hue, test_value, test_code in test_specs:
    max_c = maximum_chroma_from_renotation(np.array([test_hue, test_value, test_code]))
    print(f"Max chroma for {test_hue:.3f} at V={test_value:.3f} (code {test_code}): {max_c}")