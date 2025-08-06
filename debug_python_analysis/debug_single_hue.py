#!/usr/bin/env python3
"""Debug the single_hue calculation"""

# Rust's calculation
hue = 8.548
code = 4
raw = (17.0 - code) % 10.0 + (hue / 10.0) - 0.5
single_hue = raw % 10.0 if raw >= 0 else (raw % 10.0) + 10.0

print(f"Rust calculation for {hue}GY (code={code}):")
print(f"  raw = (17.0 - {code}) % 10.0 + ({hue} / 10.0) - 0.5 = {raw}")
print(f"  single_hue = {single_hue}")

# Now interpolate using the breakpoints
breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0]
angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0]

for i in range(len(breakpoints)-1):
    if breakpoints[i] <= single_hue <= breakpoints[i+1]:
        t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i])
        angle = angles[i] + t * (angles[i+1] - angles[i])
        print(f"  Interpolation: single_hue={single_hue} is between {breakpoints[i]} and {breakpoints[i+1]}")
        print(f"  t = {t}")
        print(f"  angle = {angles[i]} + {t} * ({angles[i+1]} - {angles[i]}) = {angle}")
        break

# Check Python's hue_to_ASTM_hue
print("\nPython's hue_to_ASTM_hue calculation:")
# ASTM_hue = 10 * ((7 - code) % 10) + hue
astm_hue = 10 * ((7 - code) % 10) + hue
print(f"  ASTM_hue = 10 * ((7 - {code}) % 10) + {hue} = {astm_hue}")

# Try to understand Python's formula better
print("\nAnalyzing formulas:")
print(f"Rust:   (17 - code) % 10 + hue/10 - 0.5 = (17 - {code}) % 10 + {hue/10} - 0.5 = {raw}")
print(f"Python: ((7 - code) % 10) * 10 + hue = ((7 - {code}) % 10) * 10 + {hue} = {astm_hue}")