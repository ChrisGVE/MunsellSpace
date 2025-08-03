#!/usr/bin/env python3
"""
Test Rust implementation on ALL 4,007 colors against reference dataset.
Simple script with progress tracking.
"""

import csv
import subprocess
import time

def main():
    print("=" * 80)
    print("Testing Rust on ALL 4,007 colors vs Reference Dataset")
    print("=" * 80)
    
    # Load dataset
    colors = []
    expected_values = []
    
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            r, g, b = int(row[0]), int(row[1]), int(row[2])
            expected = row[3].strip()
            colors.append(f"{r},{g},{b}")
            expected_values.append(expected)
    
    print(f"\nLoaded {len(colors)} colors")
    
    # Build Rust binary
    print("Building Rust binary...")
    subprocess.run(['cargo', 'build', '--release', '--bin', 'batch_convert'], 
                   capture_output=True)
    
    # Process in chunks to show progress
    chunk_size = 100
    all_results = []
    
    print(f"\nProcessing in chunks of {chunk_size}...")
    start_time = time.time()
    
    for i in range(0, len(colors), chunk_size):
        chunk = colors[i:i+chunk_size]
        input_data = '\n'.join(chunk)
        
        # Process chunk
        result = subprocess.run(
            ['./target/release/batch_convert'],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        chunk_results = result.stdout.strip().split('\n')
        all_results.extend(chunk_results)
        
        # Progress
        processed = min(i + chunk_size, len(colors))
        elapsed = time.time() - start_time
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (len(colors) - processed) / rate if rate > 0 else 0
        
        print(f"Progress: {processed}/{len(colors)} ({100*processed/len(colors):.1f}%) - "
              f"Rate: {rate:.1f} colors/s - ETA: {eta:.0f}s")
    
    total_time = time.time() - start_time
    print(f"\n✓ Completed in {total_time:.1f} seconds")
    print(f"  Average rate: {len(colors)/total_time:.1f} colors/second")
    
    # Compare results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    exact_matches = 0
    errors = 0
    differences = []
    
    for i, (expected, rust_result) in enumerate(zip(expected_values, all_results)):
        if not rust_result or rust_result == "ERROR":
            errors += 1
        elif expected.strip() == rust_result.strip():
            exact_matches += 1
        else:
            # Check if they're close (same notation format)
            exp_parts = expected.replace('/', ' ').split()
            rust_parts = rust_result.replace('/', ' ').split()
            
            if len(exp_parts) == len(rust_parts) and len(exp_parts) >= 2:
                # Extract hue family
                exp_hue = ''.join(c for c in exp_parts[0] if c.isalpha())
                rust_hue = ''.join(c for c in rust_parts[0] if c.isalpha())
                
                if exp_hue == rust_hue:
                    # Same family, might be close
                    pass
                else:
                    differences.append((i, expected, rust_result))
            else:
                differences.append((i, expected, rust_result))
    
    print(f"Total colors tested:  {len(colors):,}")
    print(f"Exact matches:        {exact_matches:,} ({100*exact_matches/len(colors):.2f}%)")
    print(f"Not exact matches:    {len(colors)-exact_matches-errors:,} ({100*(len(colors)-exact_matches-errors)/len(colors):.2f}%)")
    print(f"Errors:              {errors:,} ({100*errors/len(colors):.2f}%)")
    
    # Show some differences
    if differences:
        print(f"\n--- Sample Differences (first 20) ---")
        for idx, expected, rust in differences[:20]:
            r, g, b = colors[idx].split(',')
            print(f"  RGB({r:>3},{g:>3},{b:>3}): '{expected}' vs '{rust}'")
    
    # Save results
    output_file = f"rust_all_4007_results_{int(time.time())}.csv"
    print(f"\nSaving results to {output_file}...")
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'R', 'G', 'B', 'Expected', 'Rust', 'Match'])
        
        for i, (color_str, expected, rust) in enumerate(zip(colors, expected_values, all_results)):
            r, g, b = color_str.split(',')
            match = "YES" if expected.strip() == rust.strip() else "NO"
            writer.writerow([i, r, g, b, expected, rust, match])
    
    print(f"Results saved to {output_file}")
    print("\n✓ VALIDATION COMPLETE!")

if __name__ == "__main__":
    main()