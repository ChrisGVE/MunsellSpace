#!/usr/bin/env python3
"""Test Python's Munsell functions with correct API usage"""

import numpy as np
from colour.notation.munsell import (
    xy_from_renotation_ovoid,
    bounding_hues_from_renotation,
    interpolation_method_from_renotation_ovoid,
    maximum_chroma_from_renotation,
    munsell_specification_to_xyY,
    munsell_colour_to_munsell_specification
)

# Create test cases with proper Munsell notation
test_cases = [
    # Standard hues with even chromas
    "2.5GY 9/6",
    "5.0GY 9/8", 
    "7.5GY 9/6",
    "10.0GY 9/8",
    
    # Non-standard hues
    "8.548GY 9/6",
    "8.548GY 9/8",
    "8.548GY 9/7.125",
    
    # Edge cases
    "N 9",          # Achromatic
    "2.5GY 9/2",    # Low chroma
    "7.5GY 9/20",   # High chroma
    
    # Different families
    "5.0R 5/10",
    "7.5B 7/8",
    "2.5P 4/12",
    
    # Problematic cases from before
    "8.0GY 9.5/12.7",  # Python's result for RGB(204,255,170)
    "8.5GY 9.5/7.1",   # Rust's result for RGB(204,255,170)
]

print("Testing Munsell functions with proper notation:")
print("=" * 80)

# First, let's understand the specification format
for munsell_str in ["2.5GY 9/6", "8.548GY 9/7.125", "N 9"]:
    try:
        spec = munsell_colour_to_munsell_specification(munsell_str)
        print(f"\n{munsell_str} -> specification array: {spec}")
        
        # Now test xy_from_renotation_ovoid
        xy = xy_from_renotation_ovoid(spec)
        print(f"  xy_from_renotation_ovoid: ({xy[0]:.6f}, {xy[1]:.6f})")
        
        # Test interpolation method
        method = interpolation_method_from_renotation_ovoid(spec)
        print(f"  Interpolation method: {method}")
        
        # Test full xyY conversion
        xyY = munsell_specification_to_xyY(spec)
        print(f"  Full xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")
        
    except Exception as e:
        print(f"\n{munsell_str} -> ERROR: {e}")

# Now let's specifically test the problematic green case
print("\n\nDetailed analysis of the green color issue:")
print("=" * 80)

specs_to_compare = [
    ("8.0GY 9.5/12.7", "Python's result"),
    ("8.5GY 9.5/7.1", "Rust's result"),
    ("8.548GY 9.479/7.125", "Rust's exact convergence point"),
]

for munsell_str, desc in specs_to_compare:
    print(f"\n{desc}: {munsell_str}")
    try:
        spec = munsell_colour_to_munsell_specification(munsell_str)
        print(f"  Specification: {spec}")
        
        # Get xy from ovoid function
        xy = xy_from_renotation_ovoid(spec)
        print(f"  xy_from_renotation_ovoid: ({xy[0]:.6f}, {xy[1]:.6f})")
        
        # Get full xyY
        xyY = munsell_specification_to_xyY(spec)
        print(f"  munsell_specification_to_xyY: ({xyY[0]:.6f}, {xyY[1]:.6f})")
        
        # Check if they're the same
        if np.allclose(xy, xyY[:2]):
            print("  ✓ Both methods give same xy")
        else:
            print(f"  ✗ Methods differ by: dx={abs(xy[0]-xyY[0]):.6f}, dy={abs(xy[1]-xyY[1]):.6f}")
            
    except Exception as e:
        print(f"  ERROR: {e}")

# Test bounding hues with correct format
print("\n\nTesting bounding_hues_from_renotation:")
print("=" * 80)

for munsell_str in ["2.5R 5/10", "8.548GY 9/6", "0.0YR 5/10"]:
    try:
        spec = munsell_colour_to_munsell_specification(munsell_str)
        hue_code = spec[:2]  # Just hue and code
        bounds = bounding_hues_from_renotation(hue_code)
        print(f"{munsell_str}: spec={spec}, bounds={bounds}")
    except Exception as e:
        print(f"{munsell_str}: ERROR - {e}")

# Save reference data for unit tests
print("\n\nGenerating reference data for Rust unit tests...")
import csv

reference_data = []
for munsell_str in test_cases:
    try:
        spec = munsell_colour_to_munsell_specification(munsell_str)
        xy = xy_from_renotation_ovoid(spec)
        xyY = munsell_specification_to_xyY(spec)
        method = interpolation_method_from_renotation_ovoid(spec)
        
        reference_data.append({
            'munsell': munsell_str,
            'hue': spec[0],
            'value': spec[1],
            'chroma': spec[2],
            'code': spec[3],
            'xy_ovoid_x': xy[0],
            'xy_ovoid_y': xy[1],
            'xyY_full_x': xyY[0],
            'xyY_full_y': xyY[1],
            'xyY_Y': xyY[2],
            'interpolation': method
        })
    except Exception as e:
        print(f"Skipping {munsell_str}: {e}")

with open('python_munsell_reference.csv', 'w', newline='') as f:
    if reference_data:
        writer = csv.DictWriter(f, fieldnames=reference_data[0].keys())
        writer.writeheader()
        writer.writerows(reference_data)
        print(f"Saved {len(reference_data)} test cases to python_munsell_reference.csv")