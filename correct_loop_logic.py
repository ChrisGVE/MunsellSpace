#!/usr/bin/env python3
"""The CORRECT loop logic with bracketing check"""

# Initial state
phi_differences = []
hue_angle_diffs = []

# Add initial point
phi_differences.append(-7.458)
hue_angle_diffs.append(0.0)

print("Inner hue loop with bracketing check:")
print("=" * 60)

# Known phi differences from trace
known_phi = [-4.130, -0.077, 4.746, 9.0]  # More values in case

for i in range(1, 10):
    print(f"\nIteration {i}:")
    print(f"  Current points: {len(phi_differences)}")
    print(f"  phi_differences: {phi_differences}")
    
    # Check if we have bracketed zero
    if len(phi_differences) >= 2:
        min_phi = min(phi_differences)
        max_phi = max(phi_differences)
        if min_phi < 0 < max_phi:
            print(f"  -> BRACKETED ZERO! min={min_phi:.3f}, max={max_phi:.3f}")
            print(f"  -> Breaking loop")
            break
        elif abs(min_phi) < 1e-6 or abs(max_phi) < 1e-6:
            print(f"  -> Found zero! Breaking loop")
            break
    
    # Check extrapolation
    extrapolate = len(phi_differences) >= 2
    print(f"  extrapolate={extrapolate}")
    
    # Check loop condition
    all_same_sign = (all(d >= 0 for d in phi_differences) or 
                     all(d <= 0 for d in phi_differences))
    print(f"  all_same_sign={all_same_sign}")
    
    if not all_same_sign or extrapolate:
        print(f"  -> Normal exit condition (not all_same_sign or extrapolate)")
        # But don't break yet - still need to check bracketing
    
    # Add next point (if available)
    if i <= len(known_phi):
        phi_diff = known_phi[i-1]
        phi_differences.append(phi_diff)
        hue_angle_diffs.append(i * 7.458)
        print(f"  -> Added point: phi_diff={phi_diff:.3f}")

print(f"\nFinal: {len(phi_differences)} points")
print(f"phi_differences: {phi_differences}")
print(f"hue_angle_diffs: {hue_angle_diffs}")