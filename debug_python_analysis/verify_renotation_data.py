#!/usr/bin/env python3
"""Verify renotation data matches between Python and Rust"""

from colour.notation.munsell import MUNSELL_COLOURS_ALL
import csv

# Look up specific values that we know are problematic
test_keys = [
    "7.5GY 9/6",
    "10GY 9/6", 
    "10.0GY 9/6",
    "7.5GY 9/8",
    "10GY 9/8",
    "10.0GY 9/8",
]

print("Python's renotation data for key test cases:")
print("=" * 80)
print(f"{'Key':15} {'x':10} {'y':10} {'Y':10}")
print("-" * 80)

found_keys = []
for key in test_keys:
    if key in MUNSELL_COLOURS_ALL:
        xyY = MUNSELL_COLOURS_ALL[key]
        print(f"{key:15} {xyY[0]:10.6f} {xyY[1]:10.6f} {xyY[2]:10.6f}")
        found_keys.append((key, xyY))
    else:
        # Try alternate format
        alt_key = key.replace("10.0", "10")
        if alt_key in MUNSELL_COLOURS_ALL:
            xyY = MUNSELL_COLOURS_ALL[alt_key]
            print(f"{alt_key:15} {xyY[0]:10.6f} {xyY[1]:10.6f} {xyY[2]:10.6f}")
            found_keys.append((alt_key, xyY))
        else:
            print(f"{key:15} NOT FOUND")

# Now let's check what Rust has in its CSV file
print("\n\nChecking Rust's srgb-to-munsell.csv for comparison:")
print("=" * 80)

# Read Rust's reference data
rust_data = {}
try:
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            munsell = row[3].strip()
            rust_data[munsell] = (r, g, b)
            
    # Check if our test cases exist
    for key, _ in found_keys:
        if key in rust_data:
            rgb = rust_data[key]
            print(f"{key:15} -> RGB{rgb}")
        else:
            # Try with space before value
            alt_key = key.replace("GY", "GY ")
            if alt_key in rust_data:
                rgb = rust_data[alt_key]
                print(f"{alt_key:15} -> RGB{rgb}")
            else:
                print(f"{key:15} -> NOT IN RUST DATA")
                
except FileNotFoundError:
    print("Could not find Rust's CSV file")

# Let's also sample some of the actual data Python has
print("\n\nSample of Python's GY family at value 9:")
print("=" * 80)
count = 0
for key, xyY in sorted(MUNSELL_COLOURS_ALL.items()):
    if "GY" in key and " 9/" in key:
        print(f"{key:15} {xyY[0]:10.6f} {xyY[1]:10.6f} {xyY[2]:10.6f}")
        count += 1
        if count >= 20:
            print("...")
            break