#!/usr/bin/env python3
"""Debug high value colors with chroma issues."""

import subprocess

def test_color(r, g, b, expected):
    """Test a single color."""
    result = subprocess.run(
        ['cargo', 'run', '--release', '--bin', 'test_single'],
        env={**subprocess.os.environ, 'TEST_RGB': f'{r},{g},{b}'},
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        output = result.stdout.strip()
        if output.startswith('Success: '):
            rust_result = output[9:]
            print(f"RGB({r},{g},{b}):")
            print(f"  Expected: {expected}")
            print(f"  Got:      {rust_result}")
            
            # Parse values
            if expected.startswith('N'):
                # Neutral color
                exp_value = float(expected[1:].strip())
                exp_chroma = 0.0
            else:
                exp_parts = expected.split()
                if len(exp_parts) == 2:
                    exp_vc = exp_parts[1].split('/')
                    exp_value = float(exp_vc[0])
                    exp_chroma = float(exp_vc[1])
                else:
                    return None, None
            
            if rust_result.startswith('N'):
                rust_value = float(rust_result[1:].strip())
                rust_chroma = 0.0
            else:
                rust_parts = rust_result.split()
                if len(rust_parts) == 2:
                    rust_vc = rust_parts[1].split('/')
                    rust_value = float(rust_vc[0])
                    rust_chroma = float(rust_vc[1])
                else:
                    rust_value = exp_value
                    rust_chroma = 0.0
            
            print(f"  Value: {rust_value:.1f} (expected {exp_value:.1f}) - diff={rust_value-exp_value:+.1f}")
            print(f"  Chroma: {rust_chroma:.1f} (expected {exp_chroma:.1f}) - diff={rust_chroma-exp_chroma:+.1f}")
            
            # Check if this is a high value issue
            if exp_value >= 9.0:
                print(f"  -> HIGH VALUE COLOR (>= 9.0)")
                if abs(rust_chroma - exp_chroma) > 1.0:
                    print(f"  -> LARGE CHROMA ERROR for high value!")
                    
            return rust_value, rust_chroma
    return None, None

print("Testing high-value colors with chroma issues...")
print("=" * 80)

# Test colors with value >= 9.0
test_cases = [
    # The problematic color
    (187, 255, 153, "8.5GY 9.3/12.8"),
    
    # Other high-value colors from the dataset
    (255, 255, 238, "5.8Y 9.9/1.6"),
    (238, 238, 238, "N 9.3"),
    (221, 238, 238, "7.1G 9.3/2.1"),
    (238, 255, 238, "8.9GY 9.8/3.3"),
    (255, 238, 238, "7.5R 9.5/1.7"),
    (238, 238, 255, "5.3PB 9.5/2.7"),
    (238, 255, 255, "0.9B 9.7/2.9"),
    (255, 238, 255, "5.7P 9.6/3.5"),
]

high_value_errors = []

for r, g, b, expected in test_cases:
    rust_value, rust_chroma = test_color(r, g, b, expected)
    
    if rust_value and rust_value >= 9.0:
        # Parse expected chroma
        if expected.startswith('N'):
            exp_chroma = 0.0
        else:
            exp_chroma = float(expected.split()[1].split('/')[1])
        error = rust_chroma - exp_chroma
        high_value_errors.append((rust_value, error))
    
    print()

print("=" * 80)
print("ANALYSIS:")

if high_value_errors:
    avg_error = sum(e for _, e in high_value_errors) / len(high_value_errors)
    print(f"Average chroma error for value >= 9.0: {avg_error:+.3f}")
    
    # Check if errors correlate with value
    errors_by_value = {}
    for value, error in high_value_errors:
        v_key = round(value, 1)
        if v_key not in errors_by_value:
            errors_by_value[v_key] = []
        errors_by_value[v_key].append(error)
    
    print("\nErrors by value level:")
    for value in sorted(errors_by_value.keys()):
        errors = errors_by_value[value]
        avg = sum(errors) / len(errors)
        print(f"  Value {value}: avg error = {avg:+.3f} (n={len(errors)})")
    
    # Check for systematic under/over estimation
    under = sum(1 for _, e in high_value_errors if e < -0.5)
    over = sum(1 for _, e in high_value_errors if e > 0.5)
    
    print(f"\nLarge errors (>0.5 chroma):")
    print(f"  Underestimates: {under}/{len(high_value_errors)}")
    print(f"  Overestimates: {over}/{len(high_value_errors)}")
    
    if under > over:
        print("\nPATTERN: High-value colors tend to have UNDERESTIMATED chroma")