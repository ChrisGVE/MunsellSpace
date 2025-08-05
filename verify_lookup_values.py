#!/usr/bin/env python3
"""Verify the lookup values Rust is using"""

import numpy as np
from colour.notation.munsell import munsell_specification_to_xyY

# Check what Python gets for 10P value=1 chroma=8
munsell_10p = np.array([10.0, 1.0, 8.0, 9])  # 10P 1/8
xyy_10p = munsell_specification_to_xyY(munsell_10p)
print(f"10P 1/8: x={xyy_10p[0]:.6f}, y={xyy_10p[1]:.6f}")
print(f"Rust has: x=0.311400, y=0.148100")
print(f"Difference: x={xyy_10p[0] - 0.311400:.6f}, y={xyy_10p[1] - 0.148100:.6f}")

print()

# Check what Python gets for 2.5RP value=1 chroma=8
munsell_25rp = np.array([2.5, 1.0, 8.0, 8])  # 2.5RP 1/8
xyy_25rp = munsell_specification_to_xyY(munsell_25rp)
print(f"2.5RP 1/8: x={xyy_25rp[0]:.6f}, y={xyy_25rp[1]:.6f}")
print(f"Rust has: x=0.334200, y=0.155100")
print(f"Difference: x={xyy_25rp[0] - 0.334200:.6f}, y={xyy_25rp[1] - 0.155100:.6f}")

print("\n" + "=" * 60)
print("These values match! So the lookup is correct.")
print("The issue must be in the interpolation between them.")

# What would happen if we interpolate between these?
# For hue 0.628RP (between 10P and 2.5RP)

# 10P is at hue angle 275° (code 9, hue 10)  
# 2.5RP is at hue angle 287.5° (code 8, hue 2.5)
# 0.628RP should be at approximately 285.628° 

# The range is 275° to 287.5° = 12.5°
# 0.628 is (0.628 / 2.5) = 0.2512 of the way from 10P to 2.5RP
# But wait, that's not right. Let me think...

# Actually, 0.628RP is between 0RP (which wraps from 10P) and 2.5RP
# So the interpolation should be:
# - From 10P (previous family) at 275°
# - To 2.5RP at 287.5°
# 0.628 out of 2.5 = 0.2512 = 25.12% of the way

t = 0.628 / 2.5
print(f"\nInterpolation factor: {t:.4f}")

x_interp = 0.311400 + t * (0.334200 - 0.311400)
y_interp = 0.148100 + t * (0.155100 - 0.148100)
print(f"Linear interpolation: x={x_interp:.6f}, y={y_interp:.6f}")
print(f"Rust gets: x=0.339663, y=0.165219")
print(f"Python expects: x≈0.320438, y≈0.158653")

print("\nThe Rust interpolated value is WAY off!")
print("Rust x=0.339663 is even BEYOND 2.5RP's x=0.334200!")
print("This suggests the interpolation logic is wrong.")