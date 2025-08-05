#!/usr/bin/env python3
"""Try to understand exactly why Python gets 4 points"""

# Let me trace through what I think is happening:

# Initial state:
phi_input_deg = -86.158
phi_current_deg = 266.38
hue_angle_current = 273.84

# Initial phi difference
phi_current_difference = (360 - phi_input_deg + phi_current_deg) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360
print(f"Initial phi_current_difference: {phi_current_difference:.3f}")

# Arrays
phi_differences_data = []
hue_angles_differences_data = []

# Add initial point if not zero
if abs(phi_current_difference) >= 1e-6:
    phi_differences_data.append(phi_current_difference)
    hue_angles_differences_data.append(0.0)
    print(f"Added initial: phi={phi_current_difference:.3f}, hue=0.0")

extrapolate = False
iterations_inner = 0

print("\nStarting inner loop:")
print("-" * 40)

# The key question: when does the loop actually exit?
# Loop condition: (all same sign) AND not extrapolate

while True:  # Simplified for analysis
    iterations_inner += 1
    if iterations_inner > 10:
        break
    
    print(f"\nIteration {iterations_inner}:")
    
    # Check current state
    all_positive = all(d >= 0 for d in phi_differences_data)
    all_negative = all(d <= 0 for d in phi_differences_data)
    same_sign = all_positive or all_negative
    
    print(f"  Current state: {len(phi_differences_data)} points, same_sign={same_sign}, extrapolate={extrapolate}")
    
    # Check loop condition BEFORE doing work
    if not (same_sign and not extrapolate):
        print(f"  -> Loop exit condition met, breaking")
        break
    
    # Calculate test angle
    step = iterations_inner * (phi_input_deg - phi_current_deg)
    hue_angle_inner = (hue_angle_current + step) % 360
    print(f"  hue_angle_inner = {hue_angle_inner:.1f}")
    
    # Here we would calculate xy and phi_inner
    # Using the known values from trace:
    known_phi_diffs = [-7.458, -4.130, -0.077, 4.746]
    
    # Check extrapolation AFTER calculating but BEFORE storing
    if len(phi_differences_data) >= 2:
        if not extrapolate:
            print(f"  -> Setting extrapolate=True (have {len(phi_differences_data)} points)")
        extrapolate = True
    
    # Store if not extrapolating
    if not extrapolate:
        if iterations_inner <= len(known_phi_diffs):
            phi_diff = known_phi_diffs[iterations_inner - 1]
            phi_differences_data.append(phi_diff)
            hue_angles_differences_data.append(iterations_inner * 7.458)
            print(f"  -> Stored: phi_diff={phi_diff:.3f}")
    else:
        print(f"  -> Extrapolating, not storing")

print(f"\nFinal: {len(phi_differences_data)} points collected")
print(f"phi_differences: {phi_differences_data}")

# Hmm, this still only gives 2 points...
# Unless the loop condition is different?