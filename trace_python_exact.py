#!/usr/bin/env python3
"""Trace EXACTLY what Python does for RGB [68,0,68] - line by line"""

import numpy as np
from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import munsell_value
from colour.algebra import cartesian_to_cylindrical
from colour.utilities import as_float_array

# Test RGB [68,0,68] - expects 0.7RP
rgb = [68, 0, 68]
rgb_normalized = np.array(rgb) / 255.0
xyz = sRGB_to_XYZ(rgb_normalized)
xyy = XYZ_to_xyY(xyz)

print(f"RGB {rgb} -> xyY: {xyy}")
print("=" * 70)

# Now trace through Python's xyY_to_munsell_specification
# From colour-science munsell.py lines 1060-1340

THRESHOLD_INTEGER = 1e-3
CONVERGENCE_THRESHOLD = THRESHOLD_INTEGER / 1e4

x_input, y_input, Y = as_float_array(xyy).tolist()
Y = Y * 100  # Convert to percentage

print(f"Input: x={x_input:.6f}, y={y_input:.6f}, Y={Y:.6f}")

# Step 1: Calculate Munsell value (line 1069-1073)
munsell_val = munsell_value(Y)
print(f"Munsell value: {munsell_val:.6f}")

# Step 2: Create achromatic specification and get center (line 1074-1077)
from colour.notation.munsell import munsell_specification_to_xyY
munsell_specification = as_float_array([0, munsell_val, 0, 0])
x_center, y_center = munsell_specification_to_xyY(munsell_specification)[0:2]
print(f"Achromatic center: x={x_center:.6f}, y={y_center:.6f}")

# Step 3: Calculate polar coordinates (line 1079-1081)
rho_input, phi_input, _ = cartesian_to_cylindrical(
    np.array([x_input - x_center, y_input - y_center, Y])
)
print(f"Polar coords: rho={rho_input:.6f}, phi={np.degrees(phi_input):.2f}°")

# Step 4: Check for achromatic (line 1084-1088)
if rho_input < THRESHOLD_INTEGER:
    print("Would return achromatic")
else:
    print("Chromatic - continuing...")

# Step 5: Initial guess (line 1098-1105)
from colour.notation.munsell import hue_angle_to_hue
hue_initial_angle = np.degrees(phi_input) % 360
hue_initial, code_initial = hue_angle_to_hue(hue_initial_angle)
chroma_initial = rho_input * 50

print(f"\nInitial guess:")
print(f"  angle={hue_initial_angle:.2f}° -> hue={hue_initial:.3f}, code={code_initial}, chroma={chroma_initial:.3f}")

# Now the main loop (lines 1110-1338)
print("\n" + "=" * 70)
print("MAIN CONVERGENCE LOOP:")
print("=" * 70)

hue_current = hue_initial
code_current = code_initial
chroma_current = chroma_initial

for iteration in range(3):  # Just first 3 iterations for clarity
    print(f"\n--- Iteration {iteration} ---")
    print(f"Starting: hue={hue_current:.3f}, code={code_current}, chroma={chroma_current:.3f}")
    
    # Check maximum chroma (line 1116-1120)
    from colour.notation.munsell import maximum_chroma_from_renotation
    chroma_maximum = maximum_chroma_from_renotation(
        np.array([hue_current, munsell_val, code_current])
    )
    if chroma_current > chroma_maximum:
        chroma_current = chroma_maximum
        print(f"  Chroma capped at {chroma_maximum:.3f}")
    
    # Update specification and calculate current xy (line 1122-1129)
    munsell_specification[0] = hue_current
    munsell_specification[2] = chroma_current
    munsell_specification[3] = code_current
    x_current, y_current = munsell_specification_to_xyY(munsell_specification)[0:2]
    
    print(f"  Current xy: ({x_current:.6f}, {y_current:.6f})")
    
    # Calculate current polar coords (line 1131-1133)
    rho_current, phi_current, _ = cartesian_to_cylindrical(
        np.array([x_current - x_center, y_current - y_center, Y])
    )
    print(f"  Current polar: rho={rho_current:.6f}, phi={np.degrees(phi_current):.2f}°")
    
    # Inner loop: Hue angle refinement (lines 1136-1224)
    print("\n  Hue angle refinement:")
    
    # Calculate phi difference (line 1138-1140)
    phi_current_difference = (360 - np.degrees(phi_input) + np.degrees(phi_current)) % 360
    if phi_current_difference > 180:
        phi_current_difference -= 360
    print(f"    phi_current_difference = {phi_current_difference:.3f}°")
    
    # Collect points for interpolation (simplified for clarity)
    from colour.notation.munsell import hue_to_hue_angle
    hue_angle_current = hue_to_hue_angle(np.array([hue_current, code_current]))
    print(f"    hue_angle_current = {hue_angle_current:.2f}°")
    
    # This is where the inner loop would collect multiple points
    # For brevity, showing the key calculation
    
    # After collecting points, interpolate (around line 1210)
    # The actual interpolation finds where phi_difference = 0
    # For now, let's see what the next hue would be
    
    # Inner loop: Chroma refinement (lines 1237-1318)
    print("\n  Chroma refinement:")
    print(f"    rho_input={rho_input:.6f}, rho_current={rho_current:.6f}")
    
    # The chroma loop adjusts chroma to match rho_input
    # Using exponential scaling (line 1278)
    
    # Check convergence (line 1324-1327)
    from math import sqrt
    convergence_error = sqrt((x_input - x_current)**2 + (y_input - y_current)**2)
    print(f"\n  Convergence error: {convergence_error:.8f} vs threshold {CONVERGENCE_THRESHOLD:.8f}")
    
    if convergence_error < CONVERGENCE_THRESHOLD:
        print("  CONVERGED!")
        break

# Get final result
from colour.notation.munsell import xyY_to_munsell_specification
result = xyY_to_munsell_specification(xyy)
print(f"\nFinal Python result: hue={result[0]:.3f}, value={result[1]:.3f}, chroma={result[2]:.3f}, code={result[3]}")