#!/usr/bin/env python3
"""Check the exact bracketing logic"""

# Test the bracketing conditions with Python's data
test_sequences = [
    [-7.458],
    [-7.458, -4.130],
    [-7.458, -4.130, -0.077],
    [-7.458, -4.130, -0.077, 4.746]
]

print("Testing bracketing conditions:")
print("=" * 60)

for seq in test_sequences:
    print(f"\nSequence: {seq}")
    if len(seq) >= 2:
        min_val = min(seq)
        max_val = max(seq)
        print(f"  min={min_val:.3f}, max={max_val:.3f}")
        
        # Check different conditions
        has_bracket = min_val < 0 < max_val
        has_zero = abs(min_val) < 1e-6 or abs(max_val) < 1e-6
        
        print(f"  min < 0 < max? {has_bracket}")
        print(f"  Has zero (< 1e-6)? {has_zero}")
        print(f"  Would break? {has_bracket or has_zero}")

# Now test with Rust's data
print("\n" + "=" * 60)
print("Rust's sequence:")
rust_seq = [-7.462, -4.131, 7.254]
print(f"  {rust_seq}")
min_val = min(rust_seq)
max_val = max(rust_seq)
print(f"  min={min_val:.3f}, max={max_val:.3f}")
print(f"  min < 0 < max? {min_val < 0 < max_val}")
print(f"  -> Rust breaks here (correctly)")

print("\nThe issue: Rust gets a different 3rd point!")
print("Python: -0.077 (very close to zero, negative)")
print("Rust: 7.254 (positive, overshoots zero)")