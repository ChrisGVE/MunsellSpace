#!/usr/bin/env python3
"""
Generate Python results sequentially, saving after each color.
This ensures we get results even if interrupted.
"""

import csv
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
import warnings
import os

# Suppress warnings
warnings.filterwarnings('ignore')

# Check if we're resuming
start_index = 0
if os.path.exists('python_complete_4007.txt'):
    with open('python_complete_4007.txt', 'r') as f:
        start_index = len(f.readlines())
    print(f"Resuming from color {start_index}")
    mode = 'a'
else:
    print("Starting fresh")
    mode = 'w'

# Load colors
colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        colors.append([int(row['R']), int(row['G']), int(row['B'])])

print(f"Processing {len(colors) - start_index} remaining colors...")

# Open output file
with open('python_complete_4007.txt', mode) as out:
    for i in range(start_index, len(colors)):
        r, g, b = colors[i]
        
        if i % 100 == 0:
            print(f"Progress: {i}/{len(colors)}")
        
        try:
            rgb_norm = [r/255.0, g/255.0, b/255.0]
            XYZ = sRGB_to_XYZ(rgb_norm)
            xyY = XYZ_to_xyY(XYZ)
            result = xyY_to_munsell_colour(xyY)
        except Exception as e:
            result = f"ERROR: {str(e).replace(chr(10), ' ')}"
        
        out.write(f"{result}\n")
        out.flush()  # Ensure it's written immediately

print(f"Completed! Total {len(colors)} colors processed")