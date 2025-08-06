#!/usr/bin/env python3
"""Check the format of Python's renotation data"""

from colour.notation.munsell import MUNSELL_COLOURS_ALL

print("Checking MUNSELL_COLOURS_ALL type:", type(MUNSELL_COLOURS_ALL))
print(f"Number of entries: {len(MUNSELL_COLOURS_ALL)}")

# Sample first few entries
print("\nFirst 20 entries with 'GY' and value 9:")
print("=" * 80)
count = 0

# MUNSELL_COLOURS_ALL might be a different structure
if hasattr(MUNSELL_COLOURS_ALL, 'items'):
    # It's a dictionary
    for key, value in MUNSELL_COLOURS_ALL.items():
        if 'GY' in str(key) and ' 9/' in str(key):
            print(f"{key}: {value}")
            count += 1
            if count >= 20:
                break
else:
    # It might be a list or tuple
    print("Not a dictionary, checking structure...")
    print("First few items:", MUNSELL_COLOURS_ALL[:5] if len(MUNSELL_COLOURS_ALL) > 5 else MUNSELL_COLOURS_ALL)

# Let's also check what exact data is available for standard hues
print("\n\nSearching for standard GY hues at value 9:")
print("=" * 80)

# Try different key formats
test_formats = [
    "2.5GY 9/6",
    "2.5 GY 9/6",
    "2.5GY 9/6.0",
    "2.5GY 9.0/6.0",
    "5GY 9/6",
    "5.0GY 9/6",
    "7.5GY 9/6",
    "10GY 9/6",
    "10.0GY 9/6",
]

if hasattr(MUNSELL_COLOURS_ALL, 'get'):
    for fmt in test_formats:
        value = MUNSELL_COLOURS_ALL.get(fmt)
        if value is not None:
            print(f"Found: {fmt} -> {value}")

# Let's check the actual Munsell renotation dataset structure
print("\n\nChecking colour.datasets for Munsell data:")
try:
    from colour.datasets import MUNSELL_COLOURS
    print("Found MUNSELL_COLOURS dataset")
    print("Type:", type(MUNSELL_COLOURS))
    if hasattr(MUNSELL_COLOURS, 'items'):
        # Sample a few GY entries
        count = 0
        for key, value in MUNSELL_COLOURS.items():
            if 'GY' in str(key) and '9' in str(key):
                print(f"  {key}: {value}")
                count += 1
                if count >= 5:
                    break
except ImportError:
    print("Could not import MUNSELL_COLOURS from colour.datasets")