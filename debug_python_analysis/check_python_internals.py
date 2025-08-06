#!/usr/bin/env python3
"""Check Python's internal interpolation"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Let's check multiple points to see the pattern
print("Checking interpolation pattern for GY family at value 9.0:")
print("Hue     Chroma=6.0            Chroma=8.0")
print("-" * 50)

for hue in [7.5, 8.0, 8.5, 8.548, 9.0, 9.5, 10.0]:
    xy6 = munsell_specification_to_xyY(np.array([hue, 9.0, 6.0, 4]))
    xy8 = munsell_specification_to_xyY(np.array([hue, 9.0, 8.0, 4]))
    print(f"{hue:4.1f}    ({xy6[0]:.6f},{xy6[1]:.6f})  ({xy8[0]:.6f},{xy8[1]:.6f})")

# The key insight: Python might be using a different data set or applying
# some correction that we're not aware of