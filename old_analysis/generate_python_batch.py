#!/usr/bin/env python3
"""
Generate Python results for a batch of colors and save to file.
Usage: python3 generate_python_batch.py start_idx end_idx
"""

import csv
import sys
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings

# Suppress warnings to keep output clean
warnings.filterwarnings('ignore')

if len(sys.argv) != 3:
    print("Usage: python3 generate_python_batch.py start_idx end_idx")
    sys.exit(1)

start_idx = int(sys.argv[1])
end_idx = int(sys.argv[2])

# Load colors in the specified range
colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for i, row in enumerate(reader):
        if i >= start_idx and i < end_idx:
            colors.append([int(row['R']), int(row['G']), int(row['B'])])
        elif i >= end_idx:
            break

# Generate results
results = []
for r, g, b in colors:
    try:
        rgb_norm = [r/255.0, g/255.0, b/255.0]
        XYZ = sRGB_to_XYZ(rgb_norm)
        xyY = XYZ_to_xyY(XYZ)
        result = xyY_to_munsell_colour(xyY)
        results.append(result)
    except Exception as e:
        # Record the specific error message for analysis
        error_msg = str(e).replace('\n', ' ')
        results.append(f"ERROR: {error_msg}")

# Save to file
filename = f'python_batch_{start_idx}_{end_idx}.txt'
with open(filename, 'w') as f:
    for result in results:
        f.write(f"{result}\n")

print(f"Processed {len(results)} colors, saved to {filename}")