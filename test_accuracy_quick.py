#!/usr/bin/env python3
"""Quick accuracy test on 200 colors from the reference dataset."""

import csv
import subprocess
import json
from pathlib import Path

def parse_munsell(munsell_str):
    """Parse Munsell notation into components."""
    munsell_str = munsell_str.strip()
    if munsell_str.startswith('N'):
        # Neutral color
        value = float(munsell_str[1:].strip())
        return None, value, None
    
    # Split hue from value/chroma
    parts = munsell_str.split()
    if len(parts) != 2:
        return None, None, None
    
    hue_str = parts[0]
    vc_parts = parts[1].split('/')
    if len(vc_parts) != 2:
        return None, None, None
    
    # Extract hue number and family
    for i, c in enumerate(hue_str):
        if c.isalpha():
            hue_num = float(hue_str[:i]) if i > 0 else 5.0
            hue_family = hue_str[i:]
            break
    else:
        return None, None, None
    
    value = float(vc_parts[0])
    chroma = float(vc_parts[1])
    
    return (hue_num, hue_family), value, chroma

def family_matches(rust_family, expected_family):
    """Check if families match, accounting for RP/R boundary."""
    if rust_family == expected_family:
        return True
    # Handle RP/R boundary crossing
    if (rust_family == 'RP' and expected_family == 'R') or \
       (rust_family == 'R' and expected_family == 'RP'):
        return True
    return False

def main():
    # Read test data - use every 20th color for quick test (200 colors)
    test_colors = []
    with open('tests/data/srgb-to-munsell.csv', 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for i, row in enumerate(reader):
            if i % 20 == 0:  # Take every 20th color
                r = int(row['R'])
                g = int(row['G'])
                b = int(row['B'])
                expected = row['Munsell Colour'].strip()
                test_colors.append((r, g, b, expected))
    
    print(f"Testing {len(test_colors)} colors from reference dataset...")
    
    # Test each color
    exact_matches = 0
    family_mismatches = 0
    hue_errors = []
    value_errors = []
    chroma_errors = []
    
    for r, g, b, expected in test_colors:
        # Run Rust converter
        try:
            result = subprocess.run(
                ['cargo', 'run', '--release', '--bin', 'test_single'],
                env={**subprocess.os.environ, 'TEST_RGB': f'{r},{g},{b}'},
                capture_output=True,
                text=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            print(f"  Timeout: RGB({r}, {g}, {b})")
            continue
        
        if result.returncode != 0:
            print(f"  Error: RGB({r}, {g}, {b}) failed")
            continue
        
        # Parse output
        output = result.stdout.strip()
        if output.startswith('Success: '):
            rust_notation = output[9:]
        else:
            print(f"  Unexpected output for RGB({r}, {g}, {b}): {output}")
            continue
        
        # Parse both notations
        exp_hue, exp_value, exp_chroma = parse_munsell(expected)
        rust_hue, rust_value, rust_chroma = parse_munsell(rust_notation)
        
        # Check exact match
        if rust_notation == expected:
            exact_matches += 1
        else:
            # Check component differences
            if exp_hue and rust_hue:
                # Check family
                if not family_matches(rust_hue[1], exp_hue[1]):
                    family_mismatches += 1
                    print(f"  Family mismatch: RGB({r}, {g}, {b}) -> {rust_notation} (expected {expected})")
                
                # Calculate hue difference
                hue_diff = abs(rust_hue[0] - exp_hue[0])
                if hue_diff > 5:  # Handle wraparound
                    hue_diff = 10 - hue_diff
                hue_errors.append(hue_diff)
            
            # Value difference
            if exp_value is not None and rust_value is not None:
                value_errors.append(abs(rust_value - exp_value))
            
            # Chroma difference
            if exp_chroma is not None and rust_chroma is not None:
                chroma_errors.append(abs(rust_chroma - exp_chroma))
    
    # Calculate statistics
    print(f"\n=== RESULTS ===")
    print(f"Exact matches: {exact_matches}/{len(test_colors)} ({100*exact_matches/len(test_colors):.1f}%)")
    print(f"Family mismatches: {family_mismatches}")
    
    if hue_errors:
        within_tolerance = sum(1 for e in hue_errors if e <= 0.1)
        print(f"Hue: {within_tolerance}/{len(hue_errors)} within 0.1 tolerance ({100*within_tolerance/len(hue_errors):.1f}%)")
        print(f"  Errors > 0.1: {sum(1 for e in hue_errors if e > 0.1)}")
    
    if value_errors:
        within_tolerance = sum(1 for e in value_errors if e <= 0.1)
        print(f"Value: {within_tolerance}/{len(value_errors)} within 0.1 tolerance ({100*within_tolerance/len(value_errors):.1f}%)")
        print(f"  Errors > 0.1: {sum(1 for e in value_errors if e > 0.1)}")
    
    if chroma_errors:
        within_tolerance = sum(1 for e in chroma_errors if e <= 0.1)
        print(f"Chroma: {within_tolerance}/{len(chroma_errors)} within 0.1 tolerance ({100*within_tolerance/len(chroma_errors):.1f}%)")
        print(f"  Errors > 0.1: {sum(1 for e in chroma_errors if e > 0.1)}")
    
    # Overall accuracy (within 0.1 tolerance for all components)
    total_within_tolerance = 0
    for i in range(len(test_colors)):
        if (i < len(hue_errors) and hue_errors[i] <= 0.1) or (i >= len(hue_errors)):
            if (i < len(value_errors) and value_errors[i] <= 0.1) or (i >= len(value_errors)):
                if (i < len(chroma_errors) and chroma_errors[i] <= 0.1) or (i >= len(chroma_errors)):
                    total_within_tolerance += 1
    
    print(f"\nOverall accuracy: {total_within_tolerance}/{len(test_colors)} within 0.1 tolerance ({100*total_within_tolerance/len(test_colors):.1f}%)")

if __name__ == '__main__':
    main()