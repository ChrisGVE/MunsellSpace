#!/usr/bin/env python3
"""Verify if the Lab calculation is a bug or expected behavior"""

import numpy as np
from colour.models import XYZ_to_Lab, xyY_to_XYZ

# Test case: RGB(221, 238, 238) -> xyY
xyy = [0.301646, 0.328969, 0.826943]
xyz = xyY_to_XYZ(xyy)

print("Testing Lab calculation with different illuminants:")
print("="*60)
print(f"Input XYZ: {xyz}")

# Test with different illuminants
illuminants = {
    "D65": [0.31271, 0.32902],  # Standard
    "C": [0.31006, 0.31616],    # Illuminant C
    "E": [1/3, 1/3],            # Equal energy
}

for name, xy in illuminants.items():
    xyz_ref = xyY_to_XYZ([xy[0], xy[1], xyy[2]])
    Lab = XYZ_to_Lab(xyz, xyz_ref)
    print(f"\n{name}: xy={xy}")
    print(f"  Reference XYZ: {xyz_ref}")
    print(f"  Lab: [{Lab[0]:.2f}, {Lab[1]:.2f}, {Lab[2]:.2f}]")
    
    # Check if b value is reasonable
    if abs(Lab[2]) > 200:
        print(f"  ⚠️ WARNING: b* value {Lab[2]:.2f} is unreasonably large!")

# Test with standard D65 at Y=1 (proper white point)
print("\n" + "="*60)
print("Testing with proper white points (Y=1):")
print("="*60)

for name, xy in illuminants.items():
    xyz_ref_proper = xyY_to_XYZ([xy[0], xy[1], 1.0])  # Y=1 for white
    Lab_proper = XYZ_to_Lab(xyz, xyz_ref_proper)
    print(f"\n{name} (Y=1): {xyz_ref_proper}")
    print(f"  Lab: [{Lab_proper[0]:.2f}, {Lab_proper[1]:.2f}, {Lab_proper[2]:.2f}]")

print("\n" + "="*60)
print("ANALYSIS:")
print("="*60)
print("The huge b* values (2078, 2333) appear when reference Y ≠ 1")
print("This might not be a bug but rather improper use of the function")
print("Lab should use a fixed white point (Y=1), not scaled to match sample")