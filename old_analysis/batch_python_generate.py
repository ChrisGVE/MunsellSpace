#!/usr/bin/env python3
"""
Generate Python results in batches of 1000 colors at a time.
"""

import csv
import sys
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 batch_python_generate.py <start_idx> <end_idx>")
        sys.exit(1)
    
    start_idx = int(sys.argv[1])
    end_idx = int(sys.argv[2])
    
    print(f"Processing colors {start_idx} to {end_idx}...")
    
    # Load reference colors
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for i, row in enumerate(reader):
            if i >= start_idx and i < end_idx:
                colors.append([
                    int(row['R']),
                    int(row['G']),
                    int(row['B'])
                ])
            elif i >= end_idx:
                break
    
    # Generate Python results for this batch
    results = []
    for r, g, b in colors:
        try:
            rgb_norm = [r/255.0, g/255.0, b/255.0]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            python_result = xyY_to_munsell_colour(xyY)
            results.append(python_result)
        except Exception as e:
            results.append(f"ERROR: {e}")
    
    # Save batch results
    with open(f'python_batch_{start_idx}_{end_idx}.txt', 'w') as out:
        for result in results:
            out.write(f"{result}\n")
    
    print(f"Saved {len(results)} results to python_batch_{start_idx}_{end_idx}.txt")

if __name__ == "__main__":
    main()