#!/usr/bin/env python3
"""Detailed diagnosis of white polyhedron discrepancy."""

import re
import math
from pathlib import Path
import numpy as np
from scipy.spatial import ConvexHull

POLYHEDRON_DIR = Path(__file__).parent.parent.parent / "datasets" / "centore" / "PolyhedronFiles"

def parse_munsell(s: str):
    """Parse Munsell notation including neutral colors."""
    s = s.strip()

    # Neutral pattern
    neutral_match = re.match(r'^N(\d+\.?\d*)$', s)
    if neutral_match:
        return {'hue': 0.0, 'hue_letter': 'N', 'value': float(neutral_match.group(1)), 'chroma': 0.0}

    # Chromatic pattern
    match = re.match(r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)', s)
    if match:
        hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        idx = hue_order.index(match.group(2))
        return {
            'hue': (idx * 10) + float(match.group(1)),
            'hue_letter': match.group(2),
            'value': float(match.group(3)),
            'chroma': float(match.group(4))
        }
    return None

def to_cartesian(m):
    """Convert Munsell to Cartesian."""
    if m['hue_letter'] == 'N':
        return (0.0, 0.0, m['value'])
    angle = m['hue'] * math.pi / 50
    x = m['chroma'] * math.cos(angle)
    y = m['chroma'] * math.sin(angle)
    return (x, y, m['value'])

# Parse white file
filepath = POLYHEDRON_DIR / "PolyhedronDataForwhite.txt"
with open(filepath, 'r') as f:
    content = f.read()

# Extract sections
lines = content.split('\n')

# Get published vertices
vertices_munsell = []
in_vertices = False
for line in lines:
    if 'Polyhedron vertices in Munsell' in line:
        in_vertices = True
        continue
    if 'Polyhedron vertices in Cartesian' in line:
        break
    if in_vertices and line.strip():
        vertices_munsell.append(line.strip())

# Get samples
samples_raw = []
in_samples = False
for line in lines:
    if 'Unique samples' in line:
        in_samples = True
        continue
    if in_samples and line.strip():
        samples_raw.append(line.strip())

print("=" * 70)
print("WHITE POLYHEDRON DETAILED ANALYSIS")
print("=" * 70)

# Parse published vertices
print(f"\n1. PUBLISHED VERTICES: {len(vertices_munsell)}")
pub_vertices_parsed = []
for i, v in enumerate(vertices_munsell):
    m = parse_munsell(v)
    if m:
        cart = to_cartesian(m)
        pub_vertices_parsed.append(cart)
        if m['hue_letter'] == 'N':
            print(f"   Vertex {i+1}: {v} -> NEUTRAL -> Cartesian: {cart}")
    else:
        print(f"   Vertex {i+1}: {v} -> FAILED TO PARSE")

print(f"   Successfully parsed: {len(pub_vertices_parsed)}/{len(vertices_munsell)}")

# Parse samples
print(f"\n2. SAMPLES")
samples_parsed = []
neutral_count = 0
for s in samples_raw:
    # Find Munsell notation in sample line
    # Could be standard or neutral
    neutral_match = re.search(r'\bN(\d+\.?\d*)\b', s)
    if neutral_match:
        m = {'hue': 0.0, 'hue_letter': 'N', 'value': float(neutral_match.group(1)), 'chroma': 0.0}
        samples_parsed.append(to_cartesian(m))
        neutral_count += 1
        print(f"   Neutral sample found: {s[:50]}...")
    else:
        match = re.search(r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)', s)
        if match:
            m = parse_munsell(match.group(0))
            if m:
                samples_parsed.append(to_cartesian(m))

print(f"   Total samples parsed: {len(samples_parsed)}")
print(f"   Neutral samples: {neutral_count}")

# Convert to numpy
sample_points = np.array(samples_parsed)
pub_vertices = np.array(pub_vertices_parsed)

print(f"\n3. CONVEX HULL COMPUTATION")
print(f"   Input points: {len(sample_points)}")

# Outer hull
outer_hull = ConvexHull(sample_points)
print(f"   Outer hull vertices: {len(outer_hull.vertices)}")

# Check if neutral point is on outer hull
neutral_point = np.array([0.0, 0.0, 9.02])
distances = np.linalg.norm(sample_points - neutral_point, axis=1)
neutral_idx = np.argmin(distances)
print(f"   Neutral point index in samples: {neutral_idx}")
print(f"   Neutral point on outer hull: {neutral_idx in outer_hull.vertices}")

# Inner hull (single-layer peeling)
inner_points_idx = [i for i in range(len(sample_points)) if i not in outer_hull.vertices]
print(f"   Points after peeling: {len(inner_points_idx)}")

inner_points = sample_points[inner_points_idx]
inner_hull = ConvexHull(inner_points)
print(f"   Inner hull vertices: {len(inner_hull.vertices)}")

# Compare to published
print(f"\n4. COMPARISON")
print(f"   Published vertices: {len(pub_vertices)}")
print(f"   Computed inner hull vertices: {len(inner_hull.vertices)}")
print(f"   Difference: {len(inner_hull.vertices) - len(pub_vertices)}")

# The key question: is the neutral point being removed?
print(f"\n5. NEUTRAL POINT ANALYSIS")
if neutral_idx in outer_hull.vertices:
    print(f"   The neutral point (N9.02) is ON the outer hull")
    print(f"   -> It gets REMOVED during single-layer peeling")
    print(f"   -> This is why we have 1 fewer vertex")
else:
    print(f"   The neutral point is NOT on the outer hull")

# Check where the neutral point is in relation to the hull
print(f"\n6. ALTERNATIVE EXPLANATION")
# The published inner hull has 24 vertices, one of which is the neutral point
# Check if the neutral is among published vertices
neutral_in_published = any(np.allclose([0.0, 0.0, v[2]], v, atol=0.1) for v in pub_vertices)
print(f"   Neutral point in published vertices: {neutral_in_published}")

# Find closest published vertex to neutral
if len(pub_vertices) > 0:
    neutral_cart = np.array([0.0, 0.0, 9.02])
    dists_to_pub = np.linalg.norm(pub_vertices - neutral_cart, axis=1)
    closest_idx = np.argmin(dists_to_pub)
    print(f"   Closest published vertex to (0,0,9.02): index {closest_idx+1}")
    print(f"   That vertex: {pub_vertices[closest_idx]}")
    print(f"   Distance: {dists_to_pub[closest_idx]:.4f}")
