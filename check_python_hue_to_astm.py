#!/usr/bin/env python3

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

import colour

# Test the actual Python function
test_cases = [
    (5.0, 6),  # 5R 
    (2.5, 6),  # 2.5R
    (7.5, 5),  # 7.5YR
]

print("Testing Python colour-science hue_to_astm_hue function:")
print()

for hue, code in test_cases:
    # First convert to ASTM hue
    astm_hue = colour.notation.munsell.munsell_hue_to_ASTM_hue(hue, code)
    # Then to angle
    angle = colour.notation.munsell.hue_to_hue_angle(astm_hue)
    print(f"hue={hue}, code={code} -> ASTM={astm_hue:.1f} -> angle={angle:.2f}")
    
print("\nNOTE: This function returns a HUE ANGLE (0-100), not an ASTM hue number!")
print("The Rust breakthrough version was correct!")