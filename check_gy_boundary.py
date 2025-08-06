#!/usr/bin/env python3
"""Check hue angle boundaries for GY"""

# Check what hue angles correspond to GY family
angles = [85, 90, 95, 100, 105, 110, 115, 120, 125]

for angle in angles:
    # Based on Python's mapping:
    # MUNSELL_HUE_LETTER_CODES = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
    # Each family spans 36 degrees
    # R: 0-36, YR: 36-72, Y: 72-108, GY: 108-144, G: 144-180, etc.
    
    # Actually, let me use the exact formula from Python
    # Python uses: code = (17 - np.floor((angle - 18) % 360 / 36).astype(dtype=np.int64)) % 10 + 1
    # Which in our case is:
    import math
    code = (17 - math.floor((angle - 18) % 360 / 36)) % 10 + 1
    
    # And hue within family:
    # hue = 10 - ((angle - 18) % 360 % 36) * 10 / 36
    hue = 10 - ((angle - 18) % 360 % 36) * 10 / 36
    
    families = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
    family = families[code - 1]
    
    print(f"Angle {angle:3}° => code={code} ({family:2}) hue={hue:.2f}")

print("\nGY family (code 4) spans angles approximately 90° to 126°")
print("At 116.9°, we should still be in GY, not YR!")