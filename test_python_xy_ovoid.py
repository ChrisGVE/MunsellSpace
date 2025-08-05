"""Test Python's xy_from_renotation_ovoid directly"""
import colour
from colour.notation.munsell import xy_from_renotation_ovoid
import numpy as np

# Test the exact calls our Rust is making
specs = [
    # At value 4, chroma 18
    [2.5, 4.0, 18.0, 7],  # 2.5R 4.0/18.0
    [5.0, 4.0, 18.0, 7],  # 5.0R 4.0/18.0
    [4.13, 4.0, 18.0, 7], # 4.13R 4.0/18.0 (what we want)
    # At value 4, chroma 20
    [2.5, 4.0, 20.0, 7],  # 2.5R 4.0/20.0
    [5.0, 4.0, 20.0, 7],  # 5.0R 4.0/20.0
    [4.13, 4.0, 20.0, 7], # 4.13R 4.0/20.0
]

print("Python xy_from_renotation_ovoid calls:")
for spec in specs:
    result = xy_from_renotation_ovoid(np.array(spec))
    print(f"{spec[0]}R {spec[1]}/{spec[2]} -> xy=({result[0]:.6f}, {result[1]:.6f})")

# Also test the interpolation method
print("\n\nChecking interpolation method:")
from colour.notation.munsell import interpolation_method_from_renotation_ovoid

test_specs = [
    [4.13, 4.0, 18.0, 7],
    [4.13, 5.0, 18.0, 7],
]

for spec in test_specs:
    method = interpolation_method_from_renotation_ovoid(np.array(spec))
    print(f"{spec[0]}R {spec[1]}/{spec[2]} -> method: {method}")

# Let's also manually interpolate between 2.5R and 5.0R
print("\n\nManual interpolation for 4.13R:")
# Hue angles: 2.5R = 270°, 5.0R = 288°, 4.13R should be ~283.668°
hue_2_5 = 2.5 * 3.6 + 7 * 36  # 261°
hue_5_0 = 5.0 * 3.6 + 7 * 36  # 270°
hue_4_13 = 4.13 * 3.6 + 7 * 36  # 266.868°
print(f"Hue angles: 2.5R={hue_2_5}°, 5.0R={hue_5_0}°, 4.13R={hue_4_13}°")

# Linear interpolation
t = (hue_4_13 - hue_2_5) / (hue_5_0 - hue_2_5)
print(f"t = {t:.6f}")

# xy values
xy_2_5 = xy_from_renotation_ovoid(np.array([2.5, 4.0, 18.0, 7]))
xy_5_0 = xy_from_renotation_ovoid(np.array([5.0, 4.0, 18.0, 7]))
x_interp = xy_2_5[0] + t * (xy_5_0[0] - xy_2_5[0])
y_interp = xy_2_5[1] + t * (xy_5_0[1] - xy_2_5[1])
print(f"\nInterpolated xy for 4.13R 4.0/18.0: ({x_interp:.6f}, {y_interp:.6f})")
print(f"Python direct result: ({xy_from_renotation_ovoid(np.array([4.13, 4.0, 18.0, 7]))[0]:.6f}, {xy_from_renotation_ovoid(np.array([4.13, 4.0, 18.0, 7]))[1]:.6f})")

# Check what our algorithm is doing - it's using incorrect hue angles
print("\n\nWhat Rust is probably doing:")
# If it's using code instead of full hue angle:
# 2.5R = hue 2.5, code 7
# 5.0R = hue 5.0, code 7  
# 4.13R = hue 4.13, code 7
# So it would interpolate t = (4.13 - 2.5) / (5.0 - 2.5) = 0.652
t_wrong = (4.13 - 2.5) / (5.0 - 2.5)
print(f"Wrong t (using hue only) = {t_wrong:.6f}")
x_wrong = xy_2_5[0] + t_wrong * (xy_5_0[0] - xy_2_5[0])
y_wrong = xy_2_5[1] + t_wrong * (xy_5_0[1] - xy_2_5[1])
print(f"Wrong interpolation: ({x_wrong:.6f}, {y_wrong:.6f})")