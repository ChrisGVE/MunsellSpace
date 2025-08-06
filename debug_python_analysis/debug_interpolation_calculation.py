#!/usr/bin/env python3
"""Debug the exact interpolation calculation for 8.548GY 9/6"""

import numpy as np
from colour.notation.munsell import (
    xy_from_renotation_ovoid,
    bounding_hues_from_renotation,
    hue_to_hue_angle,
    xyY_from_renotation,
    interpolation_method_from_renotation_ovoid
)
from colour.algebra import cartesian_to_cylindrical, polar_to_cartesian
from colour.algebra.interpolation import LinearInterpolator
from colour.models import xyY_to_XYZ
import math

# Test case: 8.548GY 9/6
hue = 8.548
value = 9
chroma = 6
code = 4  # GY

spec = np.array([hue, value, chroma, code])
print(f"Testing {hue}GY {value}/{chroma}")
print("=" * 80)

# Get the result from the function
xy_result = xy_from_renotation_ovoid(spec)
print(f"Python result: xy=({xy_result[0]:.8f}, {xy_result[1]:.8f})")

# Now let's trace through the calculation manually
# Illuminant C
CCS_ILLUMINANT_MUNSELL = np.array([0.31006, 0.31616])
x_grey, y_grey = CCS_ILLUMINANT_MUNSELL

# Get bounding hues
hue_code = np.array([hue, code])
bounds = bounding_hues_from_renotation(hue_code)
hue_cw, code_cw = bounds[0]
hue_ccw, code_ccw = bounds[1]

print(f"\nBounding hues:")
print(f"  CW:  {hue_cw}GY (code={code_cw})")
print(f"  CCW: {hue_ccw}GY (code={code_ccw})")

# Get xy for boundaries
spec_cw = np.array([hue_cw, value, chroma, code_cw])
x_minus, y_minus, Y_minus = xyY_from_renotation(spec_cw)
print(f"\nCW boundary: xy=({x_minus:.8f}, {y_minus:.8f}), Y={Y_minus:.8f}")

spec_ccw = np.array([hue_ccw, value, chroma, code_ccw])
x_plus, y_plus, Y_plus = xyY_from_renotation(spec_ccw)
print(f"CCW boundary: xy=({x_plus:.8f}, {y_plus:.8f}), Y={Y_plus:.8f}")

# Convert to cylindrical coordinates
rho_minus, phi_minus, z_minus = cartesian_to_cylindrical([x_minus - x_grey, y_minus - y_grey, Y_minus])
phi_minus_deg = np.degrees(phi_minus)

rho_plus, phi_plus, z_plus = cartesian_to_cylindrical([x_plus - x_grey, y_plus - y_grey, Y_plus])
phi_plus_deg = np.degrees(phi_plus)

print(f"\nCylindrical coordinates (relative to grey):")
print(f"  CW:  rho={rho_minus:.8f}, phi={phi_minus_deg:.8f}°")
print(f"  CCW: rho={rho_plus:.8f}, phi={phi_plus_deg:.8f}°")

# Get hue angles
hue_angle_lower = hue_to_hue_angle([hue_cw, code_cw])
hue_angle = hue_to_hue_angle([hue, code])
hue_angle_upper = hue_to_hue_angle([hue_ccw, code_ccw])

print(f"\nHue angles:")
print(f"  Lower: {hue_angle_lower:.8f}°")
print(f"  Current: {hue_angle:.8f}°")
print(f"  Upper: {hue_angle_upper:.8f}°")

# Handle phi angle wrapping
if phi_minus_deg - phi_plus_deg > 180:
    phi_plus_deg += 360

# Handle hue angle corrections
hue_angle_lower_corrected = hue_angle_lower
hue_angle_corrected = hue_angle

if hue_angle_lower == 0:
    hue_angle_lower_corrected = 360

if hue_angle_lower_corrected > hue_angle_upper:
    if hue_angle_lower_corrected > hue_angle:
        hue_angle_lower_corrected -= 360
    else:
        hue_angle_lower_corrected -= 360
        hue_angle_corrected -= 360

print(f"\nCorrected angles:")
print(f"  Lower: {hue_angle_lower_corrected:.8f}°")
print(f"  Current: {hue_angle_corrected:.8f}°")

# Get interpolation method
method = interpolation_method_from_renotation_ovoid(spec)
print(f"\nInterpolation method: {method}")

# Do the interpolation
hue_angle_lower_upper = np.array([hue_angle_lower_corrected, hue_angle_upper])

if method == "Linear":
    x_minus_plus = np.array([x_minus, x_plus])
    y_minus_plus = np.array([y_minus, y_plus])
    
    x = LinearInterpolator(hue_angle_lower_upper, x_minus_plus)(hue_angle_corrected)
    y = LinearInterpolator(hue_angle_lower_upper, y_minus_plus)(hue_angle_corrected)
elif method == "Radial":
    rho_minus_plus = np.array([rho_minus, rho_plus])
    phi_minus_plus = np.array([phi_minus_deg, phi_plus_deg])
    
    rho = LinearInterpolator(hue_angle_lower_upper, rho_minus_plus)(hue_angle_corrected)
    phi = LinearInterpolator(hue_angle_lower_upper, phi_minus_plus)(hue_angle_corrected)
    
    print(f"\nInterpolated polar:")
    print(f"  rho={rho:.8f}, phi={phi:.8f}°")
    
    # Convert back to cartesian
    rho_phi = np.array([rho, np.radians(phi)])
    xy_offset = polar_to_cartesian(rho_phi)
    x = xy_offset[0] + x_grey
    y = xy_offset[1] + y_grey

print(f"\nFinal result:")
print(f"  x={x:.8f}")
print(f"  y={y:.8f}")
print(f"\nDifference from function result:")
print(f"  Δx={abs(x - xy_result[0]):.2e}")
print(f"  Δy={abs(y - xy_result[1]):.2e}")