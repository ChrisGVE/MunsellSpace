#!/usr/bin/env python3
"""Extract the exact implementation of xy_from_renotation_ovoid from Python"""

import inspect
from colour.notation.munsell import xy_from_renotation_ovoid

# Get the source code
source = inspect.getsource(xy_from_renotation_ovoid)
print("Python's xy_from_renotation_ovoid implementation:")
print("=" * 80)
print(source)

# Also get related functions
from colour.notation.munsell import (
    xyY_from_renotation,
    interpolation_method_from_renotation_ovoid
)

print("\n\nxyY_from_renotation implementation:")
print("=" * 80)
print(inspect.getsource(xyY_from_renotation))

print("\n\ninterpolation_method_from_renotation_ovoid implementation:")
print("=" * 80)
print(inspect.getsource(interpolation_method_from_renotation_ovoid))