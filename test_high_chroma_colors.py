#!/usr/bin/env python3
"""Test high chroma colors that were being capped"""

import subprocess

# Test cases that had chroma capping issues
test_cases = [
    (170, 0, 255, "2.8P 4.6/25.9"),  # Was capped at 15.0
    (187, 0, 204, "7.3P 4.5/21.1"),  # Was capped at 15.0
    (119, 17, 187, "2.0P 3.3/19.1"), # Was capped at 15.0
    (187, 255, 204, "1.8G 9.4/10.0"), # Was reduced to 5.9
    (187, 255, 187, "0.4G 9.4/10.8"), # Was reduced to 6.8
]

print("Testing high chroma colors:")
print("-" * 60)

for r, g, b, reference in test_cases:
    result = subprocess.run(
        ['./target/release/mathematical_convert_rgb', str(r), str(g), str(b)],
        capture_output=True,
        text=True
    )
    rust_munsell = result.stdout.strip()
    
    # Parse chromas
    ref_chroma = float(reference.split('/')[-1])
    rust_chroma = float(rust_munsell.split('/')[-1]) if '/' in rust_munsell else 0.0
    
    status = "✓" if abs(ref_chroma - rust_chroma) <= 0.5 else "✗"
    
    print(f"RGB({r:3}, {g:3}, {b:3})")
    print(f"  Reference: {reference}")
    print(f"  Rust:      {rust_munsell}")
    print(f"  Chroma diff: {abs(ref_chroma - rust_chroma):.1f} {status}")
    print()