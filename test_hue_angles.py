"""Test hue angle calculations"""

# Python's formula from colour-science
def hue_to_hue_angle(hue, code):
    single_hue = ((17 - code) % 10 + hue / 10 - 0.5) % 10
    
    # Breakpoints from Python
    breakpoints = [0, 2, 3, 4, 5, 6, 8, 9, 10]
    angles = [0, 45, 70, 135, 160, 225, 255, 315, 360]
    
    # Find interpolation
    for i in range(len(breakpoints) - 1):
        if breakpoints[i] <= single_hue <= breakpoints[i+1]:
            t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i])
            return angles[i] + t * (angles[i+1] - angles[i])
    
    return 360.0

# Test the specific cases
print("Testing hue angle calculations:")
print(f"2.5R (hue=2.5, code=7):")
single_hue = ((17 - 7) % 10 + 2.5 / 10 - 0.5) % 10
print(f"  single_hue = {single_hue:.3f}")
print(f"  angle = {hue_to_hue_angle(2.5, 7):.3f}°")

print(f"\n4.13R (hue=4.13, code=7):")
single_hue = ((17 - 7) % 10 + 4.13 / 10 - 0.5) % 10
print(f"  single_hue = {single_hue:.3f}")
print(f"  angle = {hue_to_hue_angle(4.13, 7):.3f}°")

print(f"\n5.0R (hue=5.0, code=7):")
single_hue = ((17 - 7) % 10 + 5.0 / 10 - 0.5) % 10
print(f"  single_hue = {single_hue:.3f}")
print(f"  angle = {hue_to_hue_angle(5.0, 7):.3f}°")

# Check the actual Python colour-science function
import colour
from colour.notation.munsell import hue_to_hue_angle as py_hue_to_hue_angle

print("\n\nPython colour-science hue_to_hue_angle:")
print(f"2.5R: {py_hue_to_hue_angle(2.5, 7):.3f}°")
print(f"4.13R: {py_hue_to_hue_angle(4.13, 7):.3f}°")
print(f"5.0R: {py_hue_to_hue_angle(5.0, 7):.3f}°")