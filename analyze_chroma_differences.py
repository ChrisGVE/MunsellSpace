#!/usr/bin/env python3
"""Analyze chroma differences between Python and Rust implementations."""

import subprocess
import csv

def get_rust_result(r, g, b):
    """Get Rust conversion result."""
    result = subprocess.run(
        ['cargo', 'run', '--release', '--bin', 'test_single'],
        env={**subprocess.os.environ, 'TEST_RGB': f'{r},{g},{b}'},
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode != 0:
        return None
    
    output = result.stdout.strip()
    if output.startswith('Success: '):
        return output[9:]
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

# Test colors with various chroma levels
test_colors = [
    # Low chroma colors
    (200, 200, 200),  # Gray - should be near achromatic
    (210, 200, 200),  # Slightly red gray
    (200, 210, 200),  # Slightly green gray
    (200, 200, 210),  # Slightly blue gray
    
    # Medium chroma colors  
    (200, 150, 150),  # Red-ish
    (150, 200, 150),  # Green-ish
    (150, 150, 200),  # Blue-ish
    
    # High chroma colors
    (255, 0, 0),      # Pure red
    (0, 255, 0),      # Pure green
    (0, 0, 255),      # Pure blue
    (255, 255, 0),    # Yellow
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    
    # Problem colors from testing
    (221, 238, 238),  # The 7.1G vs 7.2G issue
    (34, 17, 119),    # #221177
]

print("Analyzing chroma differences...")
print("=" * 80)

# Load reference data for Python results
reference_data = {}
with open('tests/data/srgb-to-munsell.csv', 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        rgb = (int(row['R']), int(row['G']), int(row['B']))
        reference_data[rgb] = row['Munsell Colour'].strip()

chroma_diffs = []
for r, g, b in test_colors:
    # Get Python result from reference data or skip
    python_result = reference_data.get((r, g, b))
    if not python_result:
        print(f"RGB({r:3},{g:3},{b:3}): Not in reference dataset, skipping")
        continue
    
    # Get Rust result
    rust_result = get_rust_result(r, g, b)
    
    if rust_result:
        py_hue, py_value, py_chroma = parse_munsell(python_result)
        rust_hue, rust_value, rust_chroma = parse_munsell(rust_result)
        
        if py_chroma is not None and rust_chroma is not None:
            diff = rust_chroma - py_chroma
            chroma_diffs.append(diff)
            
            print(f"RGB({r:3},{g:3},{b:3}): Python={python_result:15} Rust={rust_result:15} ChomaDiff={diff:+.2f}")
            
            # If significant difference, show more detail
            if abs(diff) > 0.5:
                print(f"  -> Python chroma: {py_chroma:.2f}, Rust chroma: {rust_chroma:.2f}")
                print(f"  -> ERROR: Large chroma difference of {abs(diff):.2f}")
        else:
            # Achromatic color
            print(f"RGB({r:3},{g:3},{b:3}): Python={python_result:15} Rust={rust_result:15} (achromatic)")
    else:
        print(f"RGB({r:3},{g:3},{b:3}): Rust conversion failed or timed out")

print("\n" + "=" * 80)
print("CHROMA DIFFERENCE STATISTICS:")
if chroma_diffs:
    avg_diff = sum(chroma_diffs) / len(chroma_diffs)
    max_diff = max(chroma_diffs, key=abs)
    min_diff = min(chroma_diffs, key=abs)
    
    print(f"  Average difference: {avg_diff:+.3f}")
    print(f"  Maximum difference: {max_diff:+.3f}")
    print(f"  Minimum difference: {min_diff:+.3f}")
    print(f"  Within 0.1: {sum(1 for d in chroma_diffs if abs(d) <= 0.1)}/{len(chroma_diffs)}")
    print(f"  Within 0.5: {sum(1 for d in chroma_diffs if abs(d) <= 0.5)}/{len(chroma_diffs)}")
    
    # Check if Rust consistently over or under estimates
    over = sum(1 for d in chroma_diffs if d > 0)
    under = sum(1 for d in chroma_diffs if d < 0)
    print(f"\n  Rust higher: {over}/{len(chroma_diffs)}")
    print(f"  Rust lower: {under}/{len(chroma_diffs)}")
    
    if over > under * 2:
        print("\n  PATTERN: Rust tends to OVERESTIMATE chroma")
    elif under > over * 2:
        print("\n  PATTERN: Rust tends to UNDERESTIMATE chroma")