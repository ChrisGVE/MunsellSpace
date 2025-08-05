"""Test Python's exact convergence for RGB [238,0,85]"""
import colour
import numpy as np

# Test RGB [238,0,85]
rgb = [238/255, 0, 85/255]
XYZ = colour.sRGB_to_XYZ(rgb)
xyY = colour.XYZ_to_xyY(XYZ)

print(f"Target xyY: {xyY}")
print(f"Target xy: ({xyY[0]:.6f}, {xyY[1]:.6f})")

# Get the final Munsell
munsell = colour.notation.munsell.xyY_to_munsell_colour(xyY)
print(f"\nFinal Munsell: {munsell}")

# Parse it
parts = munsell.split()
hue_str = parts[0]  # e.g., "3.0R"
value_chroma = parts[1]  # e.g., "4.9/17.6"

# Extract components
hue_num = float(hue_str[:-1] if hue_str[-2:] in ['YR', 'RP', 'PB', 'BG', 'GY'] else hue_str[:-1])
family = hue_str[-2:] if hue_str[-2:] in ['YR', 'RP', 'PB', 'BG', 'GY'] else hue_str[-1]
value, chroma = map(float, value_chroma.split('/'))

print(f"\nParsed: hue={hue_num}, family={family}, value={value}, chroma={chroma}")

# Get the xy coordinates for this specification
from colour.notation.munsell import munsell_specification_to_xyY
code_map = {'B': 1, 'BG': 2, 'G': 3, 'GY': 4, 'Y': 5, 'YR': 6, 'R': 7, 'RP': 8, 'P': 9, 'PB': 10}
spec = [hue_num, value, chroma, code_map[family]]
xyY_result = munsell_specification_to_xyY(spec)

print(f"\nResult xyY: {xyY_result}")
print(f"Result xy: ({xyY_result[0]:.6f}, {xyY_result[1]:.6f})")

# Calculate distance
dist = np.linalg.norm(xyY[:2] - xyY_result[:2])
print(f"\nDistance: {dist:.8f}")

# Let's also trace through some intermediate steps
print("\n--- Checking intermediate calculations ---")

# Illuminant C
x_i, y_i = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
print(f"Illuminant C: ({x_i:.6f}, {y_i:.6f})")

# Achromatic center for this value
from colour.notation.munsell import munsell_value_ASTMD1535
value_calc = munsell_value_ASTMD1535(xyY[2] * 100)
print(f"Calculated Munsell value: {value_calc:.6f}")

# Check polar coordinates
x_center, y_center = x_i, y_i  # Achromatic center
rho_input = np.sqrt((xyY[0] - x_center)**2 + (xyY[1] - y_center)**2)
phi_input = np.degrees(np.arctan2(xyY[1] - y_center, xyY[0] - x_center))
print(f"Input polar: rho={rho_input:.6f}, phi={phi_input:.3f}°")