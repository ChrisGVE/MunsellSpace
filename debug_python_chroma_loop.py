#!/usr/bin/env python3
"""Debug Python's chroma convergence loop"""

import numpy as np
from colour.notation.munsell import (
    _munsell_specification_to_xyY,
    maximum_chroma_from_renotation,
    hue_angle_to_hue
)
from colour.algebra import cartesian_to_cylindrical
from colour.models import xyY_to_XYZ, XYZ_to_xy
from colour.utilities import as_float

# Test the specific case that's failing - red
# These are the values from our Rust debug output
hue_current = 7.939  
value = 5.221
chroma_current = 20.443
code_current = 7

# Get the center point
x_center, y_center, Y_center = _munsell_specification_to_xyY(value)

# Get the maximum chroma
chroma_maximum = maximum_chroma_from_renotation([hue_current, value, code_current])
print(f"Initial chroma_current: {chroma_current}, chroma_maximum: {chroma_maximum}")

# If chroma exceeds maximum, clamp it
if chroma_current > chroma_maximum:
    chroma_current = chroma_maximum
    print(f"Clamped chroma to maximum: {chroma_current}")

# Get current x,y
specification_current = [hue_current, value, chroma_current, code_current]
x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)

# Get rho_current
rho_current, phi_current, _z_current = cartesian_to_cylindrical(
    [x_current - x_center, y_current - y_center, Y_center]
)

print(f"\nCurrent position:")
print(f"  x,y: ({x_current}, {y_current})")
print(f"  rho_current: {rho_current}")

# Now simulate what happens with rho_input = rho_current
rho_input = rho_current
print(f"\nTesting with rho_input = rho_current = {rho_input}")

rho_bounds_data = [rho_current]
chroma_bounds_data = [chroma_current]

print(f"\nInitial bounds: rho=[{rho_current}], chroma=[{chroma_current}]")
print(f"Min/max check: {np.min(rho_bounds_data)} < {rho_input} < {np.max(rho_bounds_data)} = {np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)}")

# The loop condition
iterations_inner = 0
while not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)):
    iterations_inner += 1
    if iterations_inner > 5:  # Stop early for debugging
        print("Stopping early to avoid infinite loop")
        break
    
    chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
    
    print(f"\nIteration {iterations_inner}:")
    print(f"  (rho_input/rho_current)^{iterations_inner} = ({rho_input}/{rho_current})^{iterations_inner} = {(rho_input/rho_current)**iterations_inner}")
    print(f"  chroma_inner = {chroma_inner}")
    
    if chroma_inner > chroma_maximum:
        chroma_inner = chroma_maximum
        print(f"  Clamped to maximum: {chroma_inner}")
    
    # Get new x,y for this chroma
    specification_inner = [hue_current, value, chroma_inner, code_current]
    x_inner, y_inner, _Y_inner = _munsell_specification_to_xyY(specification_inner)
    
    rho_inner, phi_inner, _z_inner = cartesian_to_cylindrical(
        [x_inner - x_center, y_inner - y_center, Y_center]
    )
    
    print(f"  x,y: ({x_inner}, {y_inner})")
    print(f"  rho_inner: {rho_inner}")
    
    rho_bounds_data.append(rho_inner)
    chroma_bounds_data.append(chroma_inner)
    
    print(f"  Bounds now: rho={rho_bounds_data}")
    print(f"  Min/max check: {np.min(rho_bounds_data)} < {rho_input} < {np.max(rho_bounds_data)} = {np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)}")

print(f"\nFinal bounds after {iterations_inner} iterations:")
print(f"  rho_bounds: {rho_bounds_data}")
print(f"  chroma_bounds: {chroma_bounds_data}")