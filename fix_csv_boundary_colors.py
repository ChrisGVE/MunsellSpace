#!/usr/bin/env python3
"""Fix incorrect boundary colors in the CSV file."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour

# Colors that need fixing based on actual Python output
fixes = [
    ((221, 85, 204), "0.0RP 5.7/16.7"),   # Was: 10.0P 5.7/16.7
    ((255, 238, 238), "10.0YR 9.5/2.0"),   # Was: 0.0Y 9.5/2.0
]

print("Verifying fixes needed:")
print("=" * 60)

for (r, g, b), expected in fixes:
    srgb = [r/255, g/255, b/255]
    XYZ = sRGB_to_XYZ(srgb)
    xyY = XYZ_to_xyY(XYZ)
    actual = xyY_to_munsell_colour(xyY)
    
    print(f"RGB({r},{g},{b}):")
    print(f"  Expected in fix: {expected}")
    print(f"  Actual Python:   {actual}")
    print(f"  Match: {'✓' if expected == actual else '✗'}")
    print()

print("=" * 60)
print("Reading CSV file...")

# Read the CSV
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    lines = f.readlines()

# Apply fixes
fixed_lines = []
fix_count = 0

for line in lines:
    original_line = line
    for (r, g, b), correct_value in fixes:
        # Check if this line needs fixing
        if line.startswith(f"{r},{g},{b},"):
            old_value = line.split(',', 3)[3].strip()
            if old_value != correct_value:
                line = f"{r},{g},{b},{correct_value}\n"
                print(f"Fixed: RGB({r},{g},{b}) from '{old_value}' to '{correct_value}'")
                fix_count += 1
    fixed_lines.append(line)

if fix_count > 0:
    print(f"\nWriting {fix_count} fixes to CSV...")
    with open('tests/data/srgb-to-munsell.csv', 'w') as f:
        f.writelines(fixed_lines)
    print("Done!")
else:
    print("\nNo fixes needed - CSV already correct.")