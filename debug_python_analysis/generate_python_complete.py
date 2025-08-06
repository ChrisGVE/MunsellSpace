#!/usr/bin/env python3
"""
Generate Python results for all 4007 colors in one go.
No batching, no timeouts - just let it run.
"""

import csv
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings

# Suppress warnings to keep output clean
warnings.filterwarnings('ignore')

print("Generating Python results for all 4007 colors...")
print("This will take time - please be patient...")

# Load all colors
colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        colors.append([int(row['R']), int(row['G']), int(row['B'])])

print(f"Loaded {len(colors)} colors")

# Generate results
results = []
for i, (r, g, b) in enumerate(colors):
    if i % 500 == 0:
        print(f"Progress: {i}/{len(colors)}")
    
    try:
        rgb_norm = [r/255.0, g/255.0, b/255.0]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        result = xyY_to_munsell_colour(xyY)
        results.append(result)
    except Exception as e:
        # Record the full error for analysis
        error_msg = str(e).replace('\n', ' ')
        results.append(f"ERROR: {error_msg}")

# Save to file
with open('python_complete_4007.txt', 'w') as f:
    for result in results:
        f.write(f"{result}\n")

print(f"\nCompleted! Generated {len(results)} results")
print("Saved to python_complete_4007.txt")