#!/usr/bin/env python3
"""Check why Python collects 4 points instead of 2"""

# The data from my trace shows 4 points:
phi_differences = [-7.458, -4.130, -0.077, 4.746]

# Check the loop exit conditions
print("Checking loop exit conditions after each point:")
print("=" * 60)

for i in range(1, len(phi_differences) + 1):
    subset = phi_differences[:i]
    print(f"\nAfter {i} points: {subset}")
    
    all_positive = all(d >= 0 for d in subset)
    all_negative = all(d <= 0 for d in subset)
    same_sign = all_positive or all_negative
    
    print(f"  All >= 0? {all_positive}")
    print(f"  All <= 0? {all_negative}")
    print(f"  Same sign? {same_sign}")
    
    extrapolate = (i >= 2)
    print(f"  Extrapolate? {extrapolate}")
    
    continue_loop = same_sign and not extrapolate
    print(f"  Continue loop? {continue_loop}")
    
    if not continue_loop:
        print(f"  -> Loop would exit after {i} points")
        if i < 4:
            print("  BUT we have 4 points, so something else is happening...")

print("\n" + "=" * 60)
print("INSIGHT: The 4 points have mixed signs!")
print("Points 1-2: negative (-7.458, -4.130)")
print("Point 3: near zero (-0.077)")  
print("Point 4: positive (4.746)")
print("\nThis means the loop continues PAST enabling extrapolation!")
print("The loop must continue until signs are mixed, not just until extrapolate=True")