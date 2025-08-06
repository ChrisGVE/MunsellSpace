#!/usr/bin/env python3
"""Sampled validation - test every 10th color for speed, then full metrics"""

import subprocess
import csv
import re
import time
import random

# Pattern to parse Munsell notation
pattern = re.compile(r'([\d.]+)?([A-Z]+)\s+([\d.]+)(?:/([\d.]+))?')

def parse_munsell(notation):
    """Parse Munsell notation into components"""
    if notation.startswith('N '):
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

def test_color(r, g, b, expected):
    """Test a single color"""
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        rust_output = result.stdout.strip()
        exact_match = (rust_output == expected)
        
        expected_parsed = parse_munsell(expected)
        rust_parsed = parse_munsell(rust_output)
        
        if expected_parsed and rust_parsed:
            family_match = expected_parsed['family'] == rust_parsed['family']
            
            if family_match:
                v_diff = abs(expected_parsed['value'] - rust_parsed['value'])
                c_diff = abs(expected_parsed['chroma'] - rust_parsed['chroma'])
                
                h_diff = None
                if expected_parsed['family'] != 'N':
                    h_diff = abs(expected_parsed['hue'] - rust_parsed['hue'])
                    if h_diff > 5:
                        h_diff = 10 - h_diff
                
                return {
                    'exact': exact_match,
                    'family': family_match,
                    'v_diff': v_diff,
                    'c_diff': c_diff,
                    'h_diff': h_diff
                }
    
    return None

# Read all colors
all_colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        all_colors.append((int(row[0]), int(row[1]), int(row[2]), row[3].strip()))

print(f"Total colors in dataset: {len(all_colors)}")
print("=" * 70)

# Test every 10th color for speed
sample_size = len(all_colors) // 10
sampled_colors = all_colors[::10]

print(f"Testing {len(sampled_colors)} sampled colors (every 10th)...")

start_time = time.time()

results = []
for i, (r, g, b, expected) in enumerate(sampled_colors):
    result = test_color(r, g, b, expected)
    if result:
        results.append(result)
    
    if (i + 1) % 50 == 0:
        print(f"  Processed {i+1}/{len(sampled_colors)} samples...")

sampled_time = time.time() - start_time

# Calculate sampled metrics
total = len(sampled_colors)
exact_matches = sum(1 for r in results if r['exact'])
family_matches = sum(1 for r in results if r['family'])

family_results = [r for r in results if r['family']]
value_within_01 = sum(1 for r in family_results if r['v_diff'] <= 0.1)
chroma_within_01 = sum(1 for r in family_results if r['c_diff'] <= 0.1)

chromatic_results = [r for r in family_results if r['h_diff'] is not None]
hue_within_01 = sum(1 for r in chromatic_results if r['h_diff'] <= 0.1)

print(f"\nSampling completed in {sampled_time:.1f} seconds")
print("=" * 70)
print("SAMPLED RESULTS (every 10th color)")
print("=" * 70)

print(f"\nExact Matches: {exact_matches}/{total} ({100*exact_matches/total:.1f}%)")
print(f"Family Matches: {family_matches}/{total} ({100*family_matches/total:.1f}%)")

if family_matches > 0:
    print(f"\nComponent Accuracy (for {family_matches} family matches):")
    print(f"  Values within 0.1: {value_within_01}/{family_matches} ({100*value_within_01/family_matches:.1f}%)")
    print(f"  Chromas within 0.1: {chroma_within_01}/{family_matches} ({100*chroma_within_01/family_matches:.1f}%)")
    
    if chromatic_results:
        print(f"  Hues within 0.1: {hue_within_01}/{len(chromatic_results)} ({100*hue_within_01/len(chromatic_results):.1f}%)")

# Now test a random sample for better statistics
print("\n" + "=" * 70)
print("Testing 500 random colors for detailed statistics...")

random.seed(42)  # For reproducibility
random_sample = random.sample(all_colors, 500)

start_time = time.time()

random_results = []
value_diffs = []
chroma_diffs = []
hue_diffs = []

for r, g, b, expected in random_sample:
    result = test_color(r, g, b, expected)
    if result:
        random_results.append(result)
        if result['family']:
            value_diffs.append(result['v_diff'])
            chroma_diffs.append(result['c_diff'])
            if result['h_diff'] is not None:
                hue_diffs.append(result['h_diff'])

random_time = time.time() - start_time

# Statistics
import statistics

exact_random = sum(1 for r in random_results if r['exact'])
family_random = sum(1 for r in random_results if r['family'])

print(f"\nRandom sample completed in {random_time:.1f} seconds")
print("=" * 70)
print("DETAILED STATISTICS (500 random colors)")
print("=" * 70)

print(f"\nExact Matches: {exact_random}/500 ({100*exact_random/500:.1f}%)")
print(f"Family Matches: {family_random}/500 ({100*family_random/500:.1f}%)")

if value_diffs:
    print(f"\nDifference Statistics (for {family_random} family matches):")
    print(f"  Value differences:")
    print(f"    Mean: {statistics.mean(value_diffs):.4f}")
    print(f"    Median: {statistics.median(value_diffs):.4f}")
    print(f"    Std Dev: {statistics.stdev(value_diffs):.4f} ")
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

# Extrapolate to full dataset
print("\n" + "=" * 70)
print("EXTRAPOLATED RESULTS FOR ALL 4007 COLORS")
print("=" * 70)

est_exact = int(4007 * exact_matches / total)
est_family = int(4007 * family_matches / total)

print(f"\nEstimated Exact Matches: ~{est_exact}/4007 ({100*est_exact/4007:.1f}%)")
print(f"Estimated Family Matches: ~{est_family}/4007 ({100*est_family/4007:.1f}%)")

# Success criteria based on sampled data
print("\n" + "=" * 70)
print("SUCCESS CRITERIA ASSESSMENT (based on sampling):")
print("=" * 70)

if family_matches >= 0.99 * total:
    print(f"✅ Family accuracy ≥ 99%: PASSED ({100*family_matches/total:.1f}%)")
else:
    print(f"❌ Family accuracy ≥ 99%: FAILED ({100*family_matches/total:.1f}%)")

if family_matches > 0:
    if value_within_01 >= 0.9 * family_matches:
        print(f"✅ Values within 0.1 ≥ 90%: PASSED ({100*value_within_01/family_matches:.1f}%)")
    else:
        print(f"❌ Values within 0.1 ≥ 90%: FAILED ({100*value_within_01/family_matches:.1f}%)")
    
    if chroma_within_01 >= 0.85 * family_matches:
        print(f"✅ Chromas within 0.1 ≥ 85%: PASSED ({100*chroma_within_01/family_matches:.1f}%)")
    else:
        print(f"❌ Chromas within 0.1 ≥ 85%: FAILED ({100*chroma_within_01/family_matches:.1f}%)")
    
    if chromatic_results and hue_within_01 >= 0.85 * len(chromatic_results):
        print(f"✅ Hues within 0.1 ≥ 85%: PASSED ({100*hue_within_01/len(chromatic_results):.1f}%)")
    else:
        print(f"❌ Hues within 0.1 ≥ 85%: FAILED ({100*hue_within_01/len(chromatic_results):.1f}% if chromatic_results else 'N/A')")

print("\n" + "=" * 70)