import subprocess
import json
import colour

# Test specific RGB that we know is problematic
rgb = [238, 0, 85]
print(f"Testing RGB {rgb}")

# Run through Rust
rust_result = subprocess.run(
    ['./target/release/mathematical_convert_rgb'] + [str(c) for c in rgb],
    capture_output=True,
    text=True
)

if rust_result.returncode == 0:
    rust_output = rust_result.stdout.strip()
    print(f"Rust output: {rust_output}")
else:
    print(f"Rust error: {rust_result.stderr}")

# Compare with Python
rgb_normalized = [c/255.0 for c in rgb]
munsell_py = colour.notation.RGB_to_munsell(rgb_normalized)
print(f"Python output: {munsell_py}")

# Also test the color that was working
print("\nTesting RGB [68,0,68] which was working correctly:")
rgb2 = [68, 0, 68]
rust_result2 = subprocess.run(
    ['./target/release/mathematical_convert_rgb'] + [str(c) for c in rgb2],
    capture_output=True,
    text=True
)
if rust_result2.returncode == 0:
    print(f"Rust output: {rust_result2.stdout.strip()}")
rgb2_normalized = [c/255.0 for c in rgb2]
munsell_py2 = colour.notation.RGB_to_munsell(rgb2_normalized)
print(f"Python output: {munsell_py2}")