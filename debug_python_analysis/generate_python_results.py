#!/usr/bin/env python3
"""
Generate Python results for all 4007 colors and save to file.
"""

import csv
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

def main():
    print("Generating Python results for all 4007 colors...")
    
    # Load reference colors
    colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            colors.append([
                int(row['R']),
                int(row['G']),
                int(row['B'])
            ])
    
    print(f"Loaded {len(colors)} colors")
    
    # Generate Python results
    with open('python_4007_results.txt', 'w') as out:
        for i, (r, g, b) in enumerate(colors):
            if i % 500 == 0:
                print(f"Progress: {i}/{len(colors)}")
            try:
                rgb_norm = [r/255.0, g/255.0, b/255.0]
                XYZ = sRGB_to_XYZ(rgb_norm)
                xyY = XYZ_to_xyY(XYZ)
                python_result = xyY_to_munsell_colour(xyY)
                out.write(f"{python_result}\n")
            except Exception as e:
                out.write(f"ERROR: {e}\n")
    
    print("Python results saved to python_4007_results.txt")

if __name__ == "__main__":
    main()