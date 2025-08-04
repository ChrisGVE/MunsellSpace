#!/usr/bin/env python3
"""Fast validation of all 4007 reference colors using batch processing"""

import subprocess
import csv
import re
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

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

def process_color(rgb_expected):
    """Process a single color and return comparison results"""
    r, g, b, expected = rgb_expected
    
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
        exact_match = (rust_output == expected)
        
        # Parse and compare components
        expected_parsed = parse_munsell(expected)
        rust_parsed = parse_munsell(rust_output)
        
        if expected_parsed and rust_parsed:
            family_match = expected_parsed['family'] == rust_parsed['family']
            
            if family_match:
                v_diff = abs(expected_parsed['value'] - rust_parsed['value'])
                c_diff = abs(expected_parsed['chroma'] - rust_parsed['chroma'])
                
                # Hue difference (only for chromatic colors)
                h_diff = None
                if expected_parsed['family'] != 'N':
                    h_diff = abs(expected_parsed['hue'] - rust_parsed['hue'])
                    # Handle wraparound
                    if h_diff > 5:
                        h_diff = 10 - h_diff
                
                return {
                    'exact': exact_match,
                    'family': family_match,
                    'v_diff': v_diff,
                    'c_diff': c_diff,
                    'h_diff': h_diff,
                    'v_within_01': v_diff <= 0.1,
                    'c_within_01': c_diff <= 0.1,
                    'h_within_01': h_diff <= 0.1 if h_diff is not None else None
                }
            else:
                return {
                    'exact': exact_match,
                    'family': False
                }
    
    return None

# Read all colors
colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        colors.append((int(row[0]), int(row[1]), int(row[2]), row[3].strip()))

print(f"Validating all {len(colors)} reference colors...")
print("=" * 70)

start_time = time.time()

# Process in parallel for speed
results = []
with ProcessPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_color, color): i for i, color in enumerate(colors)}
    
    completed = 0
    for future in as_completed(futures):
        result = future.result()
        if result:
            results.append(result)
        
        completed += 1
        if completed % 500 == 0:
            elapsed = time.time() - start_time
            rate = completed / elapsed
            remaining = (len(colors) - completed) / rate
            print(f"Processed {completed}/{len(colors)} colors... ({100*completed/len(colors):.1f}%, ~{remaining:.1f}s remaining)")

elapsed_time = time.time() - start_time

# Calculate metrics
total = len(colors)
exact_matches = sum(1 for r in results if r and r.get('exact', False))
family_matches = sum(1 for r in results if r and r.get('family', False))

# Component metrics (only for family matches)
family_results = [r for r in results if r and r.get('family', False)]
value_within_01 = sum(1 for r in family_results if r.get('v_within_01', False))
chroma_within_01 = sum(1 for r in family_results if r.get('c_within_01', False))

# Hue metrics (only for chromatic colors with family match)
chromatic_results = [r for r in family_results if r.get('h_diff') is not None]
hue_within_01 = sum(1 for r in chromatic_results if r.get('h_within_01', False))

# Collect differences for statistics
value_diffs = [r['v_diff'] for r in family_results if 'v_diff' in r]
chroma_diffs = [r['c_diff'] for r in family_results if 'c_diff' in r]
hue_diffs = [r['h_diff'] for r in chromatic_results]

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

chromatic_count = len(chromatic_results)
if chromatic_count > 0:
    print(f"  Hues within 0.1: {hue_within_01}/{chromatic_count} ({100*hue_within_01/chromatic_count:.1f}%)")

print(f"\nDifference Statistics (for {family_matches} family matches):")
if value_diffs:
    print(f"  Value differences:")
    print(f"    Mean: {statistics.mean(value_diffs):.4f}")
    print(f"    Median: {statistics.median(value_diffs):.4f}")
    print(f"    Std Dev: {statistics.stdev(value_diffs):.4f}")
    print(f"    Max: {max(value_diffs):.4f}")

if chroma_diffs:
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
    print(f"❌ Family accuracy ≥ 99%: FAILED ({100*family_matches/total:.2f}%)")

if value_within_01 >= 0.9 * family_matches:
    print("✅ Values within 0.1 ≥ 90%: PASSED")
else:
    print(f"❌ Values within 0.1 ≥ 90%: FAILED ({100*value_within_01/family_matches:.1f}%)")

if chroma_within_01 >= 0.85 * family_matches:
    print("✅ Chromas within 0.1 ≥ 85%: PASSED")
else:
    print(f"❌ Chromas within 0.1 ≥ 85%: FAILED ({100*chroma_within_01/family_matches:.1f}%)")

if chromatic_count > 0 and hue_within_01 >= 0.85 * chromatic_count:
    print("✅ Hues within 0.1 ≥ 85%: PASSED")
else:
    print(f"❌ Hues within 0.1 ≥ 85%: FAILED ({100*hue_within_01/chromatic_count:.1f}% if chromatic_count > 0 else 'N/A')")

print("\n" + "=" * 70)