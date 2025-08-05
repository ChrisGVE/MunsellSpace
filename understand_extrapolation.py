#!/usr/bin/env python3
"""Understand the extrapolation logic better"""

# From Python colour-science munsell.py, the inner hue loop (lines 1143-1224):
#
# Key parts:
# Line 1151-1152: while loop condition
# Line 1187-1188: set extrapolate = True when len >= 2
# Line 1190: if not extrapolate:
# Line 1191-1201: calculate and store phi_difference
#
# So the flow is:
# 1. Start loop
# 2. Calculate hue_angle_inner
# 3. Get xy for test point
# 4. If len >= 2, set extrapolate = True
# 5. If NOT extrapolate, calculate and store phi
# 6. Check loop condition: (all same sign) AND not extrapolate
#
# This means:
# - Iteration 1: len=1, extrapolate=False, store point 2
# - Iteration 2: len=2, extrapolate=True, DON'T store point 3
# - Loop exits (extrapolate=True)
#
# So Python should only get 2 points too!

# Unless... let me check if there's something about the initial point

print("Analyzing the 4 data points:")
print("=" * 60)

phi_differences = [-7.458, -4.130, -0.077, 4.746]
hue_angle_diffs = [0.000, 7.458, 14.917, 22.375]

for i, (phi, hue) in enumerate(zip(phi_differences, hue_angle_diffs)):
    print(f"Point {i}: phi_diff={phi:7.3f}, hue_diff={hue:7.3f}")
    if i > 0:
        hue_step = hue_angle_diffs[i] - hue_angle_diffs[i-1]
        print(f"         Step from previous: {hue_step:.3f}")

print("\nPattern in hue_angle_diffs:")
print("  Differences: 0.000, 7.458, 14.917, 22.375")
print("  These are: 0*7.458, 1*7.458, 2*7.458, 3*7.458")
print("  So iterations 0, 1, 2, 3 of the inner loop")
print("\nBUT the loop should stop after iteration 1 (when we have 2 points)!")

print("\n" + "=" * 60)
print("WAIT - I need to reread the Python code...")
print("Maybe the 'extrapolate' flag doesn't stop data collection?")
print("Or maybe there's a different loop structure?")