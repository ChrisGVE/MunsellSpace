#!/usr/bin/env python3
"""Check what Rust produces for boundary colors."""

import subprocess

def get_rust_spec(r, g, b):
    """Get Rust specification."""
    result = subprocess.run(
        ['./target/release/test_rgb_cli', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    lines = result.stdout.strip().split('\n')
    spec = None
    munsell = None
    
    for line in lines:
        if line.startswith('Specification:'):
            spec_str = line.split('[')[1].split(']')[0]
            spec = [float(x) for x in spec_str.split(',')]
        if line.startswith('Munsell:'):
            munsell = line.split('Munsell:')[1].strip()
    
    return spec, munsell

# Test the misclassified colors
misclassified = [
    ((68, 102, 68), "10.0GY→0.0G", "Python: hue=9.9968"),
    ((85, 0, 51), "0.2R→10.0RP", "Python: hue=0.1935"),
    ((119, 85, 221), "10.0PB→0.0P", "Python: hue=9.9954"),
    ((136, 17, 68), "0.1R→10.0RP", "Python: hue=0.0471"),
    ((153, 68, 51), "0.0YR→10.0R", "Python: hue=0.0195"),
    ((170, 34, 0), "0.1YR→10.0R", "Python: hue=0.0515"),
    ((170, 34, 85), "0.0R→10.0RP", "Python: hue=0.0116"),
    ((221, 85, 204), "10.0P→0.0RP", "Python: hue=0.0033"),
    ((255, 238, 238), "0.0Y→10.0YR", "Python: hue=9.9614"),
]

print("Rust specifications for boundary colors:")
print("=" * 70)

for (r, g, b), issue, python_info in misclassified:
    spec, munsell = get_rust_spec(r, g, b)
    
    if spec:
        families = {1:'B', 2:'BG', 3:'G', 4:'GY', 5:'Y', 6:'YR', 7:'R', 8:'RP', 9:'P', 10:'PB'}
        family = families.get(int(spec[3]), '?')
        
        print(f"RGB({r:3},{g:3},{b:3}): {issue}")
        print(f"  {python_info}")
        print(f"  Rust: hue={spec[0]:.4f}, value={spec[1]:.4f}, chroma={spec[2]:.4f}, code={spec[3]:.0f} ({family})")
        print(f"  Munsell: {munsell}")
        
        # Check if hue is near boundary
        if spec[0] < 0.1:
            print(f"  -> Rust hue {spec[0]:.4f} < 0.1 (should try code-1 with hue+10)")
        elif spec[0] > 9.9:
            print(f"  -> Rust hue {spec[0]:.4f} > 9.9 (should try code+1 with hue-10)")
        else:
            print(f"  -> Rust hue {spec[0]:.4f} not near boundary")
        print()