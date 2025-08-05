"""Debug hue angle calculation"""

# Python's hue_to_hue_angle formula
def hue_to_hue_angle(hue, code):
    return code * 36 + hue * 3.6

# Test our cases
print("Hue angle calculations:")
print(f"2.5R (hue=2.5, code=7): {hue_to_hue_angle(2.5, 7)}°")
print(f"5.0R (hue=5.0, code=7): {hue_to_hue_angle(5.0, 7)}°")  
print(f"4.13R (hue=4.13, code=7): {hue_to_hue_angle(4.13, 7)}°")

# Check if we're using just hue values
print("\nIf using just hue values (wrong):")
print(f"t = (4.13 - 2.5) / (5.0 - 2.5) = {(4.13 - 2.5) / (5.0 - 2.5):.6f}")

# Check if we're using full angles (correct)
angle_2_5 = hue_to_hue_angle(2.5, 7)
angle_5_0 = hue_to_hue_angle(5.0, 7)
angle_4_13 = hue_to_hue_angle(4.13, 7)

print("\nIf using full hue angles (correct):")
print(f"t = ({angle_4_13} - {angle_2_5}) / ({angle_5_0} - {angle_2_5})")
print(f"t = {(angle_4_13 - angle_2_5) / (angle_5_0 - angle_2_5):.6f}")

# BUT WAIT! Both give the same t!
# That's because the code is the same for all three
# So (code * 36) cancels out in the division