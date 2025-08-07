#!/usr/bin/env python3
"""Quick test of backtesting on a few colors to verify it works"""

import subprocess

# Test just a few colors
test_colors = [
    (221, 238, 238, "7.1G 9.3/2.1"),   # Low chroma edge case
    (34, 17, 119, "7.4PB 1.6/13.1"),   # Mid-chroma blue
    (68, 0, 187, "8.3PB 2.6/20.7"),    # High chroma
]

print("Testing Rust conversion on sample colors:")
for r, g, b, expected in test_colors:
    result = subprocess.run(
        ['cargo', 'run', '--release', '--bin', 'test_rgb_cli', '--', str(r), str(g), str(b)],
        capture_output=True,
        text=True,
        timeout=5,
        cwd='/Users/chris/Dropbox/dev/projects/libraries/MunsellSpace'
    )
    
    munsell = None
    for line in result.stdout.split('\n'):
        if line.startswith('Munsell: '):
            munsell = line.replace('Munsell: ', '').strip()
            break
    
    for line in result.stderr.split('\n'):
        if line.startswith('Munsell: '):
            munsell = line.replace('Munsell: ', '').strip()
            break
    
    print(f"RGB({r:3},{g:3},{b:3}): Expected={expected:15} Got={munsell if munsell else 'None':15}")

print("\nIf results show, the backtesting agent should work.")