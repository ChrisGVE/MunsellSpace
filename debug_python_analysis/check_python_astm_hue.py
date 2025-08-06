#!/usr/bin/env python3
"""Check Python's actual hue_to_ASTM_hue implementation"""

import inspect
from colour.notation.munsell import hue_to_ASTM_hue

# Get the source
print("Python's hue_to_ASTM_hue implementation:")
print("=" * 80)
print(inspect.getsource(hue_to_ASTM_hue))

# Test our value
print("\n\nTest values:")
for h in [7.5, 8.0, 8.548, 10.0]:
    astm = hue_to_ASTM_hue([h, 4])
    print(f"{h}GY (code=4) -> ASTM hue = {astm}")