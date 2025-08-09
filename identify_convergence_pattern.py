#!/usr/bin/env python3
"""Identify if there's a pattern in Python vs Rust convergence preferences."""

remaining_issues = [
    # (RGB, Python family code, Rust family code, Python hue, Rust hue)
    ((68, 102, 68), 4, 3, 9.9968, 0.0039),   # GY → G
    ((85, 0, 51), 7, 8, 0.1935, 9.9944),     # R → RP
    ((119, 85, 221), 10, 9, 9.9954, 0.0048), # PB → P
    ((136, 17, 68), 7, 8, 0.0471, 9.9839),   # R → RP
    ((153, 68, 51), 6, 7, 0.0195, 9.9991),   # YR → R
    ((170, 34, 0), 6, 7, 0.0515, 9.9966),    # YR → R
    ((170, 34, 85), 7, 8, 0.0116, 9.9886),   # R → RP
]

families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}

print("Pattern Analysis:")
print("=" * 70)

# Analyze patterns
python_higher_code = 0
rust_higher_code = 0
python_near_zero = 0
python_near_ten = 0

for (r, g, b), py_code, rust_code, py_hue, rust_hue in remaining_issues:
    if py_code > rust_code or (py_code == 1 and rust_code == 10):
        python_higher_code += 1
        code_comparison = "Python > Rust"
    else:
        rust_higher_code += 1
        code_comparison = "Rust > Python"
    
    if py_hue < 0.5:
        python_near_zero += 1
        py_position = "near 0"
    else:
        python_near_ten += 1
        py_position = "near 10"
    
    print(f"RGB({r:3},{g:3},{b:3}) {families[py_code]:2}→{families[rust_code]:2}  "
          f"Py={py_hue:6.2f} ({py_position:7}) Rust={rust_hue:6.2f}  {code_comparison}")

print("\n" + "=" * 70)
print("FINDINGS:")
print(f"  Python chooses higher family code: {python_higher_code}/7")
print(f"  Rust chooses higher family code: {rust_higher_code}/7")
print(f"  Python near 0: {python_near_zero}/7")
print(f"  Python near 10: {python_near_ten}/7")

print("\n" + "=" * 70)
print("PATTERN IDENTIFIED:")
if python_near_zero > python_near_ten:
    print("  When at a boundary, Python tends to choose hue ≈ 0 in the LATER family")
    print("  while Rust tends to choose hue ≈ 10 in the EARLIER family")
else:
    print("  When at a boundary, Python tends to choose hue ≈ 10 in the EARLIER family")
    print("  while Rust tends to choose hue ≈ 0 in the LATER family")

print("\nThis suggests a systematic difference in how the algorithms handle")
print("convergence near family boundaries, possibly related to:")
print("1. Initial approximation calculation")
print("2. Convergence direction preferences")
print("3. Floating-point rounding differences")
print("4. How they handle the circular nature of hue")