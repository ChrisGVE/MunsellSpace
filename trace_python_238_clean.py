import colour
import numpy as np

# Test RGB [238,0,85]
rgb = [238/255, 0, 85/255]
print(f"Testing RGB {[int(r*255) for r in rgb]}")

# Step by step
XYZ = colour.sRGB_to_XYZ(rgb)
print(f"XYZ: {XYZ}")

xyY = colour.XYZ_to_xyY(XYZ)
print(f"xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")

# Now the critical part - let's manually check Lab/LCH
# Python uses special xy reference
x_i, y_i = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
Y = xyY[2]
X_r = x_i * Y / y_i
Y_r = Y
Z_r = (1.0 - x_i - y_i) * Y / y_i

# Normalize
XYZ_r = np.array([X_r/Y_r, 1.0, Z_r/Y_r])
xy_ref = colour.XYZ_to_xy(XYZ_r)
print(f"xy reference: {xy_ref}")

# Convert to Lab
Lab = colour.XYZ_to_Lab(XYZ, xy_ref)
print(f"Lab: L={Lab[0]:.2f}, a={Lab[1]:.2f}, b={Lab[2]:.2f}")

# Convert to LCH
LCHab = colour.Lab_to_LCHab(Lab)
print(f"LCHab: L={LCHab[0]:.2f}, C={LCHab[1]:.2f}, h={LCHab[2]:.1f}°")

# Check LCH to Munsell conversion
from colour.notation.munsell import LCHab_to_munsell_specification
munsell_spec = LCHab_to_munsell_specification(LCHab)
print(f"LCH to Munsell spec: hue={munsell_spec[0]:.3f}, value={munsell_spec[1]:.3f}, chroma={munsell_spec[2]:.3f}, code={munsell_spec[3]}")

# Get Munsell
munsell = colour.notation.munsell.xyY_to_munsell_colour(xyY)
print(f"Final Munsell: {munsell}")