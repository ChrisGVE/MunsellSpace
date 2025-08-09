#!/usr/bin/env python3
"""Analyze family boundaries and understand the correct remapping."""

# The hue families and their codes
families = {
    1: 'B',   # Blue
    2: 'BG',  # Blue-Green
    3: 'G',   # Green
    4: 'GY',  # Green-Yellow
    5: 'Y',   # Yellow
    6: 'YR',  # Yellow-Red
    7: 'R',   # Red
    8: 'RP',  # Red-Purple
    9: 'P',   # Purple
    10: 'PB'  # Purple-Blue
}

print("Family boundaries and wrapping:")
print("=" * 60)

for code in range(1, 11):
    next_code = 1 if code == 10 else code + 1
    prev_code = 10 if code == 1 else code - 1
    
    print(f"Code {code:2} ({families[code]:2}): ", end="")
    print(f"hue 0.0-10.0, wraps to ", end="")
    print(f"prev={prev_code:2} ({families[prev_code]:2}) at hue≈10, ", end="")
    print(f"next={next_code:2} ({families[next_code]:2}) at hue≈0")

print("\n" + "=" * 60)
print("Boundary issue analysis:")
print("=" * 60)

# Our problematic colors and what's happening
issues = [
    ("RGB(68,102,68)", "Python: 10.0GY (code=4)", "Rust: 0.0G (code=3)", 
     "GY wraps to G at the boundary"),
    ("RGB(85,0,51)", "Python: 0.2R (code=7)", "Rust: 10.0RP (code=8)",
     "R wraps to RP at the boundary"),
    ("RGB(119,85,221)", "Python: 10.0PB (code=10)", "Rust: 0.0P (code=9)",
     "PB wraps to P at the boundary"),
]

for desc, python, rust, explanation in issues:
    print(f"{desc}:")
    print(f"  {python}")
    print(f"  {rust}")
    print(f"  → {explanation}")
    print()

print("=" * 60)
print("KEY INSIGHT:")
print("When hue ≈ 10.0 in family N, it's equivalent to hue ≈ 0.0 in family N-1")
print("When hue ≈ 0.0 in family N, it's equivalent to hue ≈ 10.0 in family N+1")
print()
print("BUT WAIT! That's backwards from what we're seeing!")
print("Actually: hue increases WITHIN a family from 0 to 10")
print("At hue=10 in family N, we transition to hue=0 in family N+1")
print()
print("So the correct mapping is:")
print("  10.0GY (code=4) → 0.0Y (code=5) NOT 0.0G (code=3)")
print("  But we're getting 0.0G (code=3)!")
print()
print("This suggests the issue is in how Rust handles the family transition.")