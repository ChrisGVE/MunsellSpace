#!/usr/bin/env python3
"""Debug what's happening with hue_angle_to_hue"""

# Test what happens when hue_angle_to_hue is called during iteration
# In the algorithm, it may be adjusting angles that go beyond normal ranges

# Python's MUNSELL_HUE_LETTER_CODES = {
#     1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y',
#     6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'
# }

# The algorithm might generate angles > 360 or < 0
test_angles = [306.579, 360.0, 400.0, -50.0, 720.0]

for angle in test_angles:
    # Normalize to 0-360 range
    normalized = angle % 360
    
    # Determine code based on angle ranges
    if normalized == 0.0:
        code = 8  # RP
    elif 0 < normalized <= 36:
        code = 7  # R
    elif 36 < normalized <= 72:
        code = 6  # YR
    elif 72 < normalized <= 108:
        code = 5  # Y
    elif 108 < normalized <= 144:
        code = 4  # GY
    elif 144 < normalized <= 180:
        code = 3  # G
    elif 180 < normalized <= 216:
        code = 2  # BG
    elif 216 < normalized <= 252:
        code = 1  # B
    elif 252 < normalized <= 288:
        code = 10  # PB
    elif 288 < normalized <= 324:
        code = 9  # P
    else:  # 324 < normalized < 360
        code = 8  # RP
    
    print(f"Angle {angle:6.1f} -> normalized {normalized:6.1f} -> code {code}")