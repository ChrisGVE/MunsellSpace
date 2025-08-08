#!/usr/bin/env python3
"""Test a sample of colors from the reference dataset."""

import csv
import subprocess
import random

def get_rust_result(r, g, b):
    """Get Rust conversion result."""
    try:
        result = subprocess.run(
            ['cargo', 'run', '--release', '--bin', 'test_single'],
            env={**subprocess.os.environ, 'TEST_RGB': f'{r},{g},{b}'},
            capture_output=True,
            text=True,
            timeout=3
        )
        
        if result.returncode != 0:
            return None
        
        output = result.stdout.strip()
        if output.startswith('Success: '):
            return output[9:]
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    return None

def parse_munsell(notation):
    """Parse Munsell notation."""
    if notation.startswith('N'):
        value = float(notation[1:].strip())
        return None, value, None
    
    parts = notation.split()
    if len(parts) != 2:
        return None, None, None
    
    hue_str = parts[0]
    vc_parts = parts[1].split('/')
    
    # Extract hue
    for i, c in enumerate(hue_str):
        if c.isalpha():
            hue_num = float(hue_str[:i]) if i > 0 else 5.0
            hue_family = hue_str[i:]
            break
    
    value = float(vc_parts[0])
    chroma = float(vc_parts[1])
    
    return (hue_num, hue_family), value, chroma

# Load all colors from reference
all_colors = []
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        r = int(row['R'])
        g = int(row['G'])
        b = int(row['B'])
        expected = row['Munsell Colour'].strip()
        all_colors.append((r, g, b, expected))

# Sample 50 random colors
random.seed(42)  # For reproducibility
sample_colors = random.sample(all_colors, min(50, len(all_colors)))

print("Testing 50 random colors from reference dataset...")
print("=" * 80)

exact_matches = 0
chroma_diffs = []
timeouts = 0

for r, g, b, expected in sample_colors:
    rust_result = get_rust_result(r, g, b)
    
    if rust_result == "TIMEOUT":
        print(f"RGB({r:3},{g:3},{b:3}): TIMEOUT")
        timeouts += 1
        continue
    
    if rust_result == expected:
        exact_matches += 1
        print(f"RGB({r:3},{g:3},{b:3}): EXACT MATCH - {expected}")
    elif rust_result:
        py_hue, py_value, py_chroma = parse_munsell(expected)
        rust_hue, rust_value, rust_chroma = parse_munsell(rust_result)
        
        if py_chroma is not None and rust_chroma is not None:
            diff = rust_chroma - py_chroma
            chroma_diffs.append(diff)
            
            if abs(diff) > 0.5:
                print(f"RGB({r:3},{g:3},{b:3}): Python={expected:15} Rust={rust_result:15} ChromaDiff={diff:+.2f}")
            else:
                print(f"RGB({r:3},{g:3},{b:3}): Close - ChromaDiff={diff:+.2f}")

print("\n" + "=" * 80)
print("RESULTS:")
print(f"  Exact matches: {exact_matches}/50 ({100*exact_matches/50:.1f}%)")
print(f"  Timeouts: {timeouts}/50")

if chroma_diffs:
    print(f"\nCHROMA STATISTICS (n={len(chroma_diffs)}):")
    print(f"  Average difference: {sum(chroma_diffs)/len(chroma_diffs):+.3f}")
    print(f"  Max overestimate: {max(chroma_diffs):+.3f}")
    print(f"  Max underestimate: {min(chroma_diffs):+.3f}")
    print(f"  Within ±0.1: {sum(1 for d in chroma_diffs if abs(d) <= 0.1)}/{len(chroma_diffs)}")
    print(f"  Within ±0.5: {sum(1 for d in chroma_diffs if abs(d) <= 0.5)}/{len(chroma_diffs)}")
    
    # Pattern analysis
    over = sum(1 for d in chroma_diffs if d > 0.1)
    under = sum(1 for d in chroma_diffs if d < -0.1)
    print(f"\n  Rust overestimates (>0.1): {over}/{len(chroma_diffs)}")
    print(f"  Rust underestimates (<-0.1): {under}/{len(chroma_diffs)}")