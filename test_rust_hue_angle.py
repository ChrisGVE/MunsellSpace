"""Test Rust hue angle calculation to debug"""

# Rust's code:
def rust_hue_to_hue_angle(hue, code):
    # let single_hue = ((17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5) % 10.0;
    raw = ((17.0 - code) % 10.0 + (hue / 10.0) - 0.5)
    single_hue = raw % 10.0
    
    print(f"  raw = {raw:.3f}")
    print(f"  single_hue = {single_hue:.3f}")
    
    # linear_interpolate_hue_angle
    breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0]
    angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0]
    
    # Find the two bounding points
    for i in range(len(breakpoints) - 1):
        if single_hue >= breakpoints[i] and single_hue <= breakpoints[i+1]:
            t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i])
            result = angles[i] + t * (angles[i+1] - angles[i])
            print(f"  Found between breakpoints[{i}]={breakpoints[i]} and breakpoints[{i+1}]={breakpoints[i+1]}")
            print(f"  t = {t:.3f}")
            print(f"  angle = {angles[i]} + {t:.3f} * ({angles[i+1]} - {angles[i]}) = {result:.3f}")
            return result
    
    # Handle edge case (should not happen with valid input)
    print("  Edge case - returning 360.0")
    return 360.0

print("Testing Rust hue angle calculation:")
print("\n2.5R (hue=2.5, code=7):")
angle = rust_hue_to_hue_angle(2.5, 7)
print(f"  Result: {angle:.3f}°")

print("\n4.13R (hue=4.13, code=7):")
angle = rust_hue_to_hue_angle(4.13, 7)
print(f"  Result: {angle:.3f}°")

print("\n5.0R (hue=5.0, code=7):")
angle = rust_hue_to_hue_angle(5.0, 7)
print(f"  Result: {angle:.3f}°")