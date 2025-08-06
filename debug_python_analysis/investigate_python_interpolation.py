#!/usr/bin/env python3
"""Investigate how Python does the interpolation"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY
from colour.notation.munsell import MUNSELL_COLOURS_ALL
from colour.notation.munsell._munsell import _munsell_value_to_Y
from colour.notation.munsell._munsell import _xy_from_renotation_ovoid

# Let's trace through what Python does for 8.548GY 9.0/6.0
hue = 8.548
value = 9.0 
chroma = 6.0
code = 4  # GY

# Check what's in the renotation data
print("Checking renotation data around 8.548GY 9.0/6.0:")
for key, xyY in MUNSELL_COLOURS_ALL.items():
    # Parse the key like "7.5GY 9/6"
    parts = key.split()
    if len(parts) == 2:
        hue_str = parts[0]
        val_chroma = parts[1].split('/')
        if 'GY' in hue_str and len(val_chroma) == 2:
            try:
                data_value = int(val_chroma[0])
                data_chroma = int(val_chroma[1])
                if data_value == 9 and data_chroma in [6, 8]:
                    print(f"  {key}: xyY={xyY}")
            except:
                pass

# Now let's call the internal function directly
print("\nCalling Python's _xy_from_renotation_ovoid:")
try:
    result = _xy_from_renotation_ovoid(np.array([hue, value, chroma, code]))
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")

# Let's also check what interpolation method Python uses
print("\nChecking Python's interpolation approach...")
print("Python uses scipy.interpolate.LinearNDInterpolator for non-standard hues")