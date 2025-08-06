#!/usr/bin/env python3
"""Complete validation of all 4007 reference colors"""

import subprocess
import csv
import re
import time

# Pattern to parse Munsell notation
pattern = re.compile(r'([\d.]+)?([A-Z]+)\s+([\d.]+)(?:/([\d.]+))?')

def parse_munsell(notation):
    """Parse Munsell notation into components"""
    if notation.startswith('N '):
        # Neutral
        parts = notation.split()
        return {'hue': 0, 'family': 'N', 'value': float(parts[1]), 'chroma': 0}
    
    match = pattern.match(notation)
    if match:
        hue = float(match.group(1)) if match.group(1) else 10.0
        family = match.group(2)
        value = float(match.group(3))
        chroma = float(match.group(4)) if match.group(4) else 0.0
        return {'hue': hue, 'family': family, 'value': value, 'chroma': chroma}
    
    return None

# Track metrics
total = 0
exact_matches = 0
family_matches = 0
value_within_01 = 0
chroma_within_01 = 0
hue_within_01 = 0

# Track differences for statistics
value_diffs = []
chroma_diffs = []
hue_diffs = []

print("Validating all 4007 reference colors...")
print("=" * 70)

start_time = time.time()

with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    
    for row in reader:
        r, g, b, expected = int(row[0]), int(row[1]), int(row[2]), row[3].strip()
        
        # Get Rust result
        result = subprocess.run(
            ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        
        if result.returncode == 0:
            rust_output = result.stdout.strip()
            
            # Check exact match
            if rust_output == expected:
                exact_matches += 1
            
            # Parse and compare components
            expected_parsed = parse_munsell(expected)
            rust_parsed = parse_munsell(rust_output)
            
            if expected_parsed and rust_parsed:
                # Family match
                if expected_parsed['family'] == rust_parsed['family']:
                    family_matches += 1
                    
                    # Component differences
                    v_diff = abs(expected_parsed['value'] - rust_parsed['value'])
                    c_diff = abs(expected_parsed['chroma'] - rust_parsed['chroma'])
                    
                    value_diffs.append(v_diff)
                    chroma_diffs.append(c_diff)
                    
                    if v_diff <= 0.1:
                        value_within_01 += 1
                    if c_diff <= 0.1:
                        chroma_within_01 += 1
                    
                    # Hue difference (only for chromatic colors)
                    if expected_parsed['family'] != 'N':
                        h_diff = abs(expected_parsed['hue'] - rust_parsed['hue'])
                        # Handle wraparound (e.g., 9.9 vs 0.1)
                        if h_diff > 5:
                            h_diff = 10 - h_diff
                        hue_diffs.append(h_diff)
                        if h_diff <= 0.1:
                            hue_within_01 += 1
        
        total += 1
        
        # Progress indicator
        if total % 500 == 0:
            elapsed = time.time() - start_time
            rate = total / elapsed
            remaining = (4007 - total) / rate
            print(f"Processed {total}/4007 colors... ({100*total/4007:.1f}%, ~{remaining:.1f}s remaining)")

elapsed_time = time.time() - start_time

# Statistics
import statistics

print("\n" + "=" * 70)
print("FINAL RESULTS FOR ALL 4007 REFERENCE COLORS")
print("=" * 70)

print(f"\nExact Matches: {exact_matches}/{total} ({100*exact_matches/total:.2f}%)")
print(f"Family Matches: {family_matches}/{total} ({100*family_matches/total:.2f}%)")

print(f"\nComponent Accuracy (for {family_matches} family matches):")
print(f"  Values within 0.1: {value_within_01}/{family_matches} ({100*value_within_01/family_matches:.1f}%)")
print(f"  Chromas within 0.1: {chroma_within_01}/{family_matches} ({100*chroma_within_01/family_matches:.1f}%)")

chromatic_count = len(hue_diffs)
if chromatic_count > 0:
    print(f"  Hues within 0.1: {hue_within_01}/{chromatic_count} ({100*hue_within_01/chromatic_count:.1f}%)")

print(f"\nDifference Statistics (for {family_matches} family matches):")
print(f"  Value differences:")
print(f"    Mean: {statistics.mean(value_diffs):.4f}")
print(f"    Median: {statistics.median(value_diffs):.4f}")
print(f"    Std Dev: {statistics.stdev(value_diffs):.4f}")
print(f"    Max: {max(value_diffs):.4f}")

print(f"  Chroma differences:")
print(f"    Mean: {statistics.mean(chroma_diffs):.4f}")
print(f"    Median: {statistics.median(chroma_diffs):.4f}")
print(f"    Std Dev: {statistics.stdev(chroma_diffs):.4f}")
print(f"    Max: {max(chroma_diffs):.4f}")

if hue_diffs:
    print(f"  Hue differences (chromatic only):")
    print(f"    Mean: {statistics.mean(hue_diffs):.4f}")
    print(f"    Median: {statistics.median(hue_diffs):.4f}")
    print(f"    Std Dev: {statistics.stdev(hue_diffs):.4f}")
    print(f"    Max: {max(hue_diffs):.4f}")

print(f"\nProcessing time: {elapsed_time:.2f} seconds ({total/elapsed_time:.1f} colors/sec)")

# Success criteria
print("\n" + "=" * 70)
print("SUCCESS CRITERIA ASSESSMENT:")
print("=" * 70)
if family_matches >= 0.99 * total:
    print("✅ Family accuracy ≥ 99%: PASSED")
else:
    print("❌ Family accuracy ≥ 99%: FAILED")

if value_within_01 >= 0.9 * family_matches:
    print("✅ Values within 0.1 ≥ 90%: PASSED")
else:
    print("❌ Values within 0.1 ≥ 90%: FAILED")

if chroma_within_01 >= 0.85 * family_matches:
    print("✅ Chromas within 0.1 ≥ 85%: PASSED")
else:
    print("❌ Chromas within 0.1 ≥ 85%: FAILED")

if chromatic_count > 0 and hue_within_01 >= 0.85 * chromatic_count:
    print("✅ Hues within 0.1 ≥ 85%: PASSED")
else:
    print("❌ Hues within 0.1 ≥ 85%: FAILED")

print("\n" + "=" * 70)