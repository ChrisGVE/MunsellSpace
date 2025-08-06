#!/usr/bin/env python3
"""Check ASTM hue calculation"""

from colour.notation.munsell import hue_to_ASTM_hue
import inspect

# Get the source of hue_to_ASTM_hue
print("hue_to_ASTM_hue implementation:")
print("=" * 80)
print(inspect.getsource(hue_to_ASTM_hue))

# Test various hues
print("\n\nTesting ASTM hue calculations:")
print("=" * 80)
print(f"{'Hue':10} {'Code':6} {'Family':6} {'ASTM Hue':10}")
print("-" * 80)

hue_families = {
    0: "R", 1: "YR", 2: "Y", 3: "GY", 4: "G",
    5: "BG", 6: "B", 7: "PB", 8: "P", 9: "RP"
}

# Test GY family (code=3)
for hue in [2.5, 5.0, 7.5, 8.0, 8.548, 10.0]:
    astm_hue = hue_to_ASTM_hue([hue, 3])
    print(f"{hue:10.3f} {3:6} {'GY':6} {astm_hue:10.3f}")

print("\n\nChecking the full ASTM hue range:")
# ASTM hue goes from 0 to 100, wrapping around
# Each family gets 10 units
for code, family in hue_families.items():
    base_astm = code * 10
    print(f"{family:3}: ASTM hue range {base_astm:3} - {base_astm + 10:3}")