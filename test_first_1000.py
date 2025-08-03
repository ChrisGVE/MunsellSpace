#!/usr/bin/env python3
"""
Test Rust on first 1000 colors to get statistics, then extrapolate.
"""

import csv
import subprocess
import time

def main():
    print("=" * 80)
    print("Testing Rust on first 1000 colors (then extrapolating to 4,007)")
    print("=" * 80)
    
    # Load dataset
    colors = []
    expected_values = []
    
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        count = 0
        for row in reader:
            if count >= 1000:
                break
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors.append(f"{r},{g},{b}")
            expected_values.append(expected)
            count += 1
    
    print(f"\nLoaded {len(colors)} colors for testing")
    
    # Build Rust binary
    print("Building Rust binary...")
    subprocess.run(['cargo', 'build', '--release', '--bin', 'batch_convert'], 
                   capture_output=True)
    
    # Process all at once
    input_data = '\n'.join(colors)
    
    print(f"\nProcessing {len(colors)} colors...")
    start_time = time.time()
    
    result = subprocess.run(
        ['./target/release/batch_convert'],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    rust_results = result.stdout.strip().split('\n')
    total_time = time.time() - start_time
    
    print(f"✓ Completed in {total_time:.1f} seconds")
    print(f"  Rate: {len(colors)/total_time:.1f} colors/second")
    
    # Extrapolate for full dataset
    estimated_time_4007 = (4007 / len(colors)) * total_time
    print(f"\nEstimated time for all 4,007 colors: {estimated_time_4007:.1f} seconds ({estimated_time_4007/60:.1f} minutes)")
    
    # Compare results
    print("\n" + "=" * 80)
    print("RESULTS (First 1000 colors)")
    print("=" * 80)
    
    exact_matches = 0
    errors = 0
    close_matches = 0
    
    for expected, rust_result in zip(expected_values, rust_results):
        if not rust_result or rust_result == "ERROR":
            errors += 1
        elif expected.strip() == rust_result.strip():
            exact_matches += 1
        else:
            # Check if close (same hue family)
            exp_parts = expected.split()
            rust_parts = rust_result.split()
            if len(exp_parts) > 0 and len(rust_parts) > 0:
                exp_hue = ''.join(c for c in exp_parts[0] if c.isalpha())
                rust_hue = ''.join(c for c in rust_parts[0] if c.isalpha())
                if exp_hue == rust_hue:
                    close_matches += 1
    
    tested = len(colors)
    print(f"Tested:              {tested:,} colors")
    print(f"Exact matches:       {exact_matches:,} ({100*exact_matches/tested:.2f}%)")
    print(f"Close matches:       {close_matches:,} ({100*close_matches/tested:.2f}%)")
    print(f"Total acceptable:    {exact_matches+close_matches:,} ({100*(exact_matches+close_matches)/tested:.2f}%)")
    print(f"Errors:             {errors:,} ({100*errors/tested:.2f}%)")
    
    # Extrapolate to full dataset
    print(f"\n" + "=" * 80)
    print("EXTRAPOLATION to all 4,007 colors")
    print(f"=" * 80)
    
    exact_rate = exact_matches / tested
    close_rate = close_matches / tested
    error_rate = errors / tested
    
    print(f"Expected exact matches:    {int(4007 * exact_rate):,} ({100*exact_rate:.2f}%)")
    print(f"Expected close matches:    {int(4007 * close_rate):,} ({100*close_rate:.2f}%)")
    print(f"Expected total acceptable: {int(4007 * (exact_rate+close_rate)):,} ({100*(exact_rate+close_rate):.2f}%)")
    print(f"Expected errors:          {int(4007 * error_rate):,} ({100*error_rate:.2f}%)")
    
    # Show some examples
    print(f"\n--- Example Comparisons (first 20) ---")
    for i in range(min(20, len(colors))):
        r, g, b = colors[i].split(',')
        expected = expected_values[i]
        rust = rust_results[i] if i < len(rust_results) else "N/A"
        match = "✓" if expected.strip() == rust.strip() else "✗"
        print(f"RGB({r:>3},{g:>3},{b:>3}): Expected='{expected}' Rust='{rust}' {match}")
    
    print("\n✓ TEST COMPLETE!")

if __name__ == "__main__":
    main()