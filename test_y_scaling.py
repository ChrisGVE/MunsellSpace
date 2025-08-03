#!/usr/bin/env python3
"""Test Y scaling in Python colour-science."""

import numpy as np
from colour.notation.munsell import munsell_value_ASTM_D1535
from colour.notation.munsell import luminance_ASTM_D1535

# Test ASTM D1535 functions
print("Testing ASTM D1535 Y scaling:")
print("\nMunsell Value -> Y Luminance:")
for value in [0, 1, 5, 9, 10]:
    Y = luminance_ASTM_D1535(value)
    print(f"  Value {value:2}: Y = {Y:.6f}")
    
print("\nY Luminance -> Munsell Value:")
for Y in [0.0, 0.01, 0.2, 0.9, 1.0]:
    value = munsell_value_ASTM_D1535(Y)
    print(f"  Y {Y:.2f}: Value = {value:.6f}")
    
print("\n\nIMPORTANT NOTE:")
print("The ASTM D1535 polynomial coefficients already include the 0.975 factor")
print("The dataset Y values are scaled by 1/0.975 (i.e., larger than they should be)")
print("So when looking up in the dataset, we DON'T apply any additional scaling")