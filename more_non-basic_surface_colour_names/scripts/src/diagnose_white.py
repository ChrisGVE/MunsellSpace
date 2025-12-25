#!/usr/bin/env python3
"""Diagnose the white polyhedron discrepancy."""

import re
from pathlib import Path

POLYHEDRON_DIR = Path(__file__).parent.parent.parent / "datasets" / "centore" / "PolyhedronFiles"

def parse_munsell_standard(s: str):
    """Standard parser (misses neutral colors)."""
    pattern = r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)'
    match = re.match(pattern, s.strip())
    return match is not None

def parse_munsell_with_neutral(s: str):
    """Parser that also handles neutral (N) colors."""
    # Standard chromatic pattern
    pattern = r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)'
    if re.match(pattern, s.strip()):
        return True, "chromatic"

    # Neutral pattern: N followed by value
    neutral_pattern = r'N(\d+\.?\d*)'
    if re.match(neutral_pattern, s.strip()):
        return True, "neutral"

    return False, None

# Read white polyhedron file
filepath = POLYHEDRON_DIR / "PolyhedronDataForwhite.txt"
with open(filepath, 'r') as f:
    lines = f.readlines()

# Find vertices section
in_vertices_munsell = False
vertices = []
for line in lines:
    line = line.rstrip()
    if line.startswith('Polyhedron vertices in Munsell'):
        in_vertices_munsell = True
        continue
    if line.startswith('Polyhedron vertices in Cartesian'):
        break
    if in_vertices_munsell and line.strip():
        vertices.append(line.strip())

print(f"White polyhedron: {len(vertices)} published vertices")
print("\nChecking each vertex:")
print("-" * 60)

parsed_standard = 0
parsed_with_neutral = 0

for i, v in enumerate(vertices, 1):
    std = parse_munsell_standard(v)
    ext, type_ = parse_munsell_with_neutral(v)

    if std:
        parsed_standard += 1
    if ext:
        parsed_with_neutral += 1

    status = "OK" if std else ("NEUTRAL" if ext else "FAILED")
    print(f"  {i:2d}. {v:20s} -> {status}")

print("-" * 60)
print(f"\nStandard parser:      {parsed_standard}/{len(vertices)} vertices parsed")
print(f"With neutral support: {parsed_with_neutral}/{len(vertices)} vertices parsed")

# Also check samples
print("\n\nChecking samples for neutral colors...")
in_samples = False
samples = []
for line in lines:
    if line.startswith('Unique samples'):
        in_samples = True
        continue
    if in_samples and line.strip():
        samples.append(line.strip())

neutral_samples = 0
for s in samples:
    if re.search(r'\bN\d+\.?\d*\b', s):
        neutral_samples += 1
        print(f"  Neutral sample: {s[:60]}...")

print(f"\nTotal neutral samples: {neutral_samples}")
