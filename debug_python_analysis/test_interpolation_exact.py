#!/usr/bin/env python3
"""Test exact interpolation values"""

import numpy as np
from colour.algebra.interpolation import LinearInterpolator

# Test the exact case that's failing
# Hue angles for 8.548GY
hue_angle_lower = 86.25
hue_angle_upper = 102.50
hue_angle = 93.062

# For radial interpolation at chroma=6
# CW (7.5GY): rho=0.09818658, phi=75.22495368
# CCW (10GY): rho=0.08480205, phi=86.45738191

rho_minus = 0.09818658
rho_plus = 0.08480205
phi_minus_deg = 75.22495368
phi_plus_deg = 86.45738191

# Test linear interpolation
hue_angles = np.array([hue_angle_lower, hue_angle_upper])
rhos = np.array([rho_minus, rho_plus])
phis = np.array([phi_minus_deg, phi_plus_deg])

rho_interp = LinearInterpolator(hue_angles, rhos)(hue_angle)
phi_interp = LinearInterpolator(hue_angles, phis)(hue_angle)

print(f"Interpolation test for 8.548GY 9/6:")
print(f"Hue angles: {hue_angle_lower} -> {hue_angle} -> {hue_angle_upper}")
print(f"Rho: {rho_minus} -> {rho_interp} -> {rho_plus}")
print(f"Phi: {phi_minus_deg} -> {phi_interp} -> {phi_plus_deg}")

# Manual calculation
t = (hue_angle - hue_angle_lower) / (hue_angle_upper - hue_angle_lower)
print(f"\nt = ({hue_angle} - {hue_angle_lower}) / ({hue_angle_upper} - {hue_angle_lower}) = {t}")

rho_manual = rho_minus + t * (rho_plus - rho_minus)
phi_manual = phi_minus_deg + t * (phi_plus_deg - phi_minus_deg)

print(f"\nManual calculation:")
print(f"rho = {rho_minus} + {t} * ({rho_plus} - {rho_minus}) = {rho_manual}")
print(f"phi = {phi_minus_deg} + {t} * ({phi_plus_deg} - {phi_minus_deg}) = {phi_manual}")

print(f"\nDifferences:")
print(f"Δrho = {abs(rho_interp - rho_manual):.2e}")
print(f"Δphi = {abs(phi_interp - phi_manual):.2e}")

# Convert to cartesian
import math
x_grey, y_grey = 0.31006, 0.31616

x_offset = rho_interp * math.cos(math.radians(phi_interp))
y_offset = rho_interp * math.sin(math.radians(phi_interp))
x = x_offset + x_grey
y = y_offset + y_grey

print(f"\nFinal xy: ({x:.8f}, {y:.8f})")