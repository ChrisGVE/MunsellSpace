#!/usr/bin/env python3
"""Debug a specific high-value green color"""

import subprocess
import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation import xyY_to_munsell_colour
from colour.notation.munsell import munsell_colour_to_munsell_specification

# Test case: RGB(204, 255, 170) -> 8.0GY 9.5/12.7 (Rust gives 8.5GY 9.5/7.1)
r, g, b = 204, 255, 170

print(f"Debugging RGB({r}, {g}, {b}):")
print("=" * 60)

# Python conversion
rgb_norm = [r/255.0, g/255.0, b/255.0]
XYZ = sRGB_to_XYZ(rgb_norm)
xyY = XYZ_to_xyY(XYZ)
print(f"\nxyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")

munsell = xyY_to_munsell_colour(xyY)
spec = munsell_colour_to_munsell_specification(munsell)
print(f"Python: {munsell}")
print(f"  Specification: hue={spec[0]:.6f}, value={spec[1]:.6f}, chroma={spec[2]:.6f}, code={spec[3]}")

# Rust conversion with debug
print("\nRust debug output:")
env = {'DEBUG_MUNSELL': '1'}
result = subprocess.run(
    ['cargo', 'run', '--bin', 'mathematical_convert_rgb', '--', str(r), str(g), str(b)],
    capture_output=True,
    text=True,
    env={**subprocess.os.environ, **env}
)

# Extract key information
for line in result.stderr.split('\n'):
    if any(key in line for key in ['Y luminance', 'Munsell Value', 'Initial guess', 'Converged', 'chroma_max']):
        print(f"  {line.strip()}")

rust_munsell = result.stdout.strip()
print(f"\nRust result: {rust_munsell}")

# Check maximum chroma for this case
print("\n\nChecking maximum chroma:")
from colour.notation.munsell import maximum_chroma_from_renotation

# For GY family at value 9.5
spec_for_max = np.array([8.0, 9.5, 4])  # GY has code 4
max_chroma = maximum_chroma_from_renotation(spec_for_max)
print(f"Python max chroma for 8.0GY 9.5: {max_chroma}")

# Check what chromas exist in the renotation data
print("\nChecking renotation data for high-value GY colors:")
print("(This would show what chromas are actually available)")

# Calculate the achromatic center and distance
x_center, y_center = 0.31006, 0.31616
distance = np.sqrt((xyY[0] - x_center)**2 + (xyY[1] - y_center)**2)
print(f"\nChromaticity distance from achromatic: {distance:.6f}")
print(f"Expected chroma (very rough): {distance * 150:.1f}")

# Check if it's a convergence issue
print("\nPossible causes:")
print("1. Maximum chroma incorrectly limited for high values")
print("2. Convergence stopping too early")
print("3. Initial guess too conservative for high-value colors")
print("4. Chroma scaling in inner loop not aggressive enough")