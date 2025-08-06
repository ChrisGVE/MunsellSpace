#!/usr/bin/env python3
"""Debug why high chroma values are being generated"""

import numpy as np
from colour.notation.munsell import (
    munsell_value_ASTMD1535,
    xyY_to_munsell_specification,
    LCHab_to_munsell_specification
)
from colour.models import xyY_to_XYZ, XYZ_to_Lab, Lab_to_LCHab, XYZ_to_xy
from colour.utilities import to_domain_1, domain_range_scale

# Test the failing colors
test_cases = [
    ("red", np.array([0.640000, 0.330000, 0.212673])),
    ("green", np.array([0.3, 0.6, 0.715152])),
    ("blue", np.array([0.15, 0.06, 0.072175])),
]

print("Testing initial Lab conversion:")
for name, xyy in test_cases:
    x, y, Y = xyy[0], xyy[1], to_domain_1(xyy[2])
    
    # Convert to Lab
    XYZ = xyY_to_XYZ(xyy)
    x_i, y_i = 0.31006, 0.31616  # Illuminant C
    X_r, Y_r, Z_r = xyY_to_XYZ([x_i, y_i, Y])
    XYZ_r = np.array([(1 / Y_r) * X_r, 1, (1 / Y_r) * Z_r])
    Lab = XYZ_to_Lab(XYZ, XYZ_to_xy(XYZ_r))
    LCHab = Lab_to_LCHab(Lab)
    
    print(f"\n{name}: xyY = [{x:.3f}, {y:.3f}, {Y:.3f}]")
    print(f"  Lab: L={Lab[0]:.3f}, a={Lab[1]:.3f}, b={Lab[2]:.3f}")
    print(f"  LCHab: L={LCHab[0]:.3f}, C={LCHab[1]:.3f}, h={LCHab[2]:.3f}")
    
    # Get initial spec
    hue_initial, _value_initial, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)
    print(f"  Initial spec from LCHab: hue={hue_initial:.3f}, value={_value_initial:.3f}, chroma={chroma_initial:.3f}, code={code_initial}")
    
    # Get value from Y
    with domain_range_scale("ignore"):
        value = munsell_value_ASTMD1535(Y * 100)
    
    # Scaled chroma
    chroma_scaled = (5 / 5.5) * chroma_initial
    print(f"  Value from Y: {value:.3f}")
    print(f"  Scaled chroma: {chroma_scaled:.3f} (from {chroma_initial:.3f})")
    
    # Now test what Python gets with full conversion
    print(f"\nFull conversion:")
    try:
        with domain_range_scale("ignore"):
            spec = xyY_to_munsell_specification(xyy)
        print(f"  Result: {spec}")
    except Exception as e:
        print(f"  Error: {e}")