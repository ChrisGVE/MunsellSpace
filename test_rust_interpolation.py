"""Test what Rust should be getting from interpolation"""
import subprocess
import json

# Test interpolation for 4.130R at value 4 and value 5
test_cases = [
    # Value 4
    {"r": 125, "g": 60, "b": 60, "expected": "4.1R 4.0/18.2"},  # Should give us coordinates at value 4
    # Value 5  
    {"r": 178, "g": 85, "b": 85, "expected": "4.1R 5.0/18.2"},  # Should give us coordinates at value 5
]

for test in test_cases:
    # Run Rust binary
    result = subprocess.run(
        ["cargo", "run", "--bin", "mathematical_convert_rgb", str(test['r']), str(test['g']), str(test['b'])],
        capture_output=True,
        text=True,
        cwd="/Users/chris/Dropbox/dev/projects/libraries/MunsellSpace"
    )
    
    munsell = result.stdout.strip()
    print(f"RGB [{test['r']},{test['g']},{test['b']}] -> {munsell}")

# Now test in Python
print("\nPython verification:")
import colour

# First, let's get the actual xy coordinates for these specifications
specs = [
    [4.13, 4.0, 18.2, 7],  # 4.13R 4.0/18.2
    [4.13, 5.0, 18.2, 7],  # 4.13R 5.0/18.2
]

for spec in specs:
    xyY = colour.notation.munsell.munsell_specification_to_xyY(spec)
    print(f"{spec[0]}R {spec[1]}/{spec[2]} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f})")
    
# Now let's interpolate between them for value 4.95
print("\nInterpolating for value 4.95:")
# Get luminances
Y_4 = colour.notation.munsell.luminance_ASTMD1535(4.0) / 100
Y_5 = colour.notation.munsell.luminance_ASTMD1535(5.0) / 100  
Y_495 = colour.notation.munsell.luminance_ASTMD1535(4.95) / 100

t = (Y_495 - Y_4) / (Y_5 - Y_4)
print(f"Y_4={Y_4:.6f}, Y_5={Y_5:.6f}, Y_4.95={Y_495:.6f}")
print(f"t = {t:.6f}")

# Get xy for both
spec_4 = [4.13, 4.0, 18.2, 7]
spec_5 = [4.13, 5.0, 18.2, 7]
xyY_4 = colour.notation.munsell.munsell_specification_to_xyY(spec_4)
xyY_5 = colour.notation.munsell.munsell_specification_to_xyY(spec_5)

# Interpolate
x_interp = xyY_4[0] + t * (xyY_5[0] - xyY_4[0])
y_interp = xyY_4[1] + t * (xyY_5[1] - xyY_4[1])

print(f"\nInterpolated xy for 4.13R 4.95/18.2: ({x_interp:.6f}, {y_interp:.6f})")

# Compare to what Python gets directly
spec_495 = [4.13, 4.95, 18.2, 7]
xyY_495 = colour.notation.munsell.munsell_specification_to_xyY(spec_495)
print(f"Direct Python for 4.13R 4.95/18.2: ({xyY_495[0]:.6f}, {xyY_495[1]:.6f})")