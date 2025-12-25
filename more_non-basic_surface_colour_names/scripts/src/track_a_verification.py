#!/usr/bin/env python3
"""
Track A Verification: Parse and verify Centore polyhedra files.

This script validates our ability to correctly parse and reproduce Centore's
published polyhedra by:
1. Parsing the polyhedron files to extract samples and published centroids
2. Converting Munsell coordinates to Cartesian
3. Computing our own inner convex hull
4. Computing filled-solid centroid
5. Comparing to published centroid

Reference: Centore, P. (2020) "Beige, aqua, fuchsia, etc." JAIC Vol. 25, pp. 24-54
"""

import os
import re
import math
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.spatial import ConvexHull

# Path to polyhedron files
POLYHEDRON_DIR = Path(__file__).parent.parent.parent / "datasets" / "centore" / "PolyhedronFiles"


@dataclass
class MunsellCoord:
    """Munsell color coordinate."""
    hue_number: float  # 0-10 within hue family
    hue_letter: str    # R, YR, Y, GY, G, BG, B, PB, P, RP
    value: float       # 0-10
    chroma: float      # 0-~20

    @property
    def hue_continuous(self) -> float:
        """Convert to continuous 0-100 hue scale (Centore's formula)."""
        hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        try:
            idx = hue_order.index(self.hue_letter)
        except ValueError:
            raise ValueError(f"Unknown hue letter: {self.hue_letter}")
        return (idx * 10) + self.hue_number

    def to_cartesian(self) -> tuple[float, float, float]:
        """
        Convert to Centore's Cartesian coordinates.

        From paper: x = C * cos(H * pi/50), y = C * sin(H * pi/50), z = V
        Where H is on 0-100 scale (100 = 360 degrees)
        """
        h = self.hue_continuous
        angle = h * math.pi / 50  # Convert 0-100 to 0-2*pi
        x = self.chroma * math.cos(angle)
        y = self.chroma * math.sin(angle)
        z = self.value
        return (x, y, z)


def parse_munsell(s: str) -> Optional[MunsellCoord]:
    """
    Parse a Munsell notation string like "6.66YR 6.15/3.40" or "8.77R 5.22/3.94"
    """
    # Pattern: number + hue letters + space + value / chroma
    pattern = r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)'
    match = re.match(pattern, s.strip())
    if not match:
        return None

    return MunsellCoord(
        hue_number=float(match.group(1)),
        hue_letter=match.group(2),
        value=float(match.group(3)),
        chroma=float(match.group(4))
    )


@dataclass
class PolyhedronData:
    """Parsed polyhedron file data."""
    color_name: str
    num_non_unique_samples: int
    num_unique_samples: int
    published_centroid_munsell: str
    published_centroid_cartesian: tuple[float, float, float]
    vertices_munsell: list[MunsellCoord]
    vertices_cartesian: list[tuple[float, float, float]]
    faces: list[tuple[int, int, int]]
    samples: list[MunsellCoord]


def parse_polyhedron_file(filepath: Path) -> PolyhedronData:
    """Parse a Centore polyhedron data file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()

    data = {}
    current_section = None
    section_data = []

    for line in lines:
        line = line.rstrip()

        # Header fields
        if line.startswith('Colour name:'):
            data['color_name'] = line.split('\t')[1].strip()
        elif line.startswith('Number of non-unique CAUS samples:'):
            data['num_non_unique'] = int(line.split('\t')[1])
        elif line.startswith('Number of unique CAUS samples:'):
            data['num_unique'] = int(line.split('\t')[1])
        elif line.startswith('Centroid in Munsell coordinates:'):
            data['centroid_munsell'] = line.split('\t')[1].strip()
        elif line.startswith('Centroid in Cartesian coordinates:'):
            parts = line.split('\t')[1:]
            data['centroid_cartesian'] = tuple(float(p.strip()) for p in parts)

        # Section headers
        elif line.startswith('Polyhedron vertices in Munsell'):
            current_section = 'vertices_munsell'
            section_data = []
        elif line.startswith('Polyhedron vertices in Cartesian'):
            if current_section == 'vertices_munsell':
                data['vertices_munsell'] = section_data
            current_section = 'vertices_cartesian'
            section_data = []
        elif line.startswith('Polyhedron faces'):
            if current_section == 'vertices_cartesian':
                data['vertices_cartesian'] = section_data
            current_section = 'faces'
            section_data = []
        elif line.startswith('Unique samples'):
            if current_section == 'faces':
                data['faces'] = section_data
            current_section = 'samples'
            section_data = []

        # Section content
        elif current_section and line.strip():
            section_data.append(line)

    # Final section
    if current_section == 'samples':
        data['samples'] = section_data

    # Parse vertices
    vertices_munsell = []
    for v in data.get('vertices_munsell', []):
        parsed = parse_munsell(v)
        if parsed:
            vertices_munsell.append(parsed)

    vertices_cartesian = []
    for v in data.get('vertices_cartesian', []):
        parts = v.split('\t')
        vertices_cartesian.append(tuple(float(p.strip()) for p in parts))

    # Parse faces
    faces = []
    for f in data.get('faces', []):
        parts = f.split('\t')
        faces.append(tuple(int(p.strip()) for p in parts))

    # Parse samples (format: year season market name munsell_coords numeric_hue)
    samples = []
    for s in data.get('samples', []):
        # Find the Munsell coordinates pattern in the line
        match = re.search(r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)', s)
        if match:
            parsed = parse_munsell(match.group(0))
            if parsed:
                samples.append(parsed)

    return PolyhedronData(
        color_name=data['color_name'],
        num_non_unique_samples=data['num_non_unique'],
        num_unique_samples=data['num_unique'],
        published_centroid_munsell=data['centroid_munsell'],
        published_centroid_cartesian=data['centroid_cartesian'],
        vertices_munsell=vertices_munsell,
        vertices_cartesian=vertices_cartesian,
        faces=faces,
        samples=samples
    )


def compute_inner_hull(points: np.ndarray) -> np.ndarray:
    """
    Compute inner convex hull by Centore's single-layer peeling.

    1. Compute outer convex hull
    2. Remove vertices of outer hull
    3. Compute hull of remaining points
    """
    if len(points) < 4:
        return points

    # Compute outer hull
    try:
        outer_hull = ConvexHull(points)
    except Exception:
        return points

    # Get vertices of outer hull
    outer_vertices = set(outer_hull.vertices)

    # Remove outer vertices
    inner_points_idx = [i for i in range(len(points)) if i not in outer_vertices]

    if len(inner_points_idx) < 4:
        # Not enough points for inner hull
        return points[inner_points_idx] if inner_points_idx else points

    return points[inner_points_idx]


def compute_filled_solid_centroid(points: np.ndarray) -> np.ndarray:
    """
    Compute filled-solid centroid of a convex polyhedron.

    This uses the decomposition into tetrahedra method:
    For each face, form a tetrahedron with a reference point (centroid of vertices).
    Weight each tetrahedron's centroid by its volume.

    Simplified approach: use centroid of hull vertices as approximation.
    For more accuracy, would implement Centore's equations 6-8.
    """
    if len(points) < 4:
        return np.mean(points, axis=0)

    try:
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]

        # Simple approach: centroid of hull vertices
        # This is a reasonable approximation for relatively uniform polyhedra
        return np.mean(hull_points, axis=0)
    except Exception:
        return np.mean(points, axis=0)


def compute_proper_filled_solid_centroid(points: np.ndarray) -> np.ndarray:
    """
    Compute proper filled-solid centroid using tetrahedron decomposition.

    For each face of the convex hull, form a tetrahedron with the geometric center.
    The centroid is the volume-weighted average of tetrahedron centroids.
    """
    if len(points) < 4:
        return np.mean(points, axis=0)

    try:
        hull = ConvexHull(points)
    except Exception:
        return np.mean(points, axis=0)

    # Reference point (geometric center of all hull vertices)
    hull_vertices = points[hull.vertices]
    ref_point = np.mean(hull_vertices, axis=0)

    total_volume = 0.0
    weighted_centroid = np.zeros(3)

    for simplex in hull.simplices:
        # Get the three vertices of this face
        v0, v1, v2 = points[simplex[0]], points[simplex[1]], points[simplex[2]]

        # Form tetrahedron with reference point
        # Volume = |det([v1-v0, v2-v0, ref-v0])| / 6
        mat = np.array([v1 - v0, v2 - v0, ref_point - v0])
        volume = abs(np.linalg.det(mat)) / 6.0

        # Centroid of tetrahedron
        tet_centroid = (v0 + v1 + v2 + ref_point) / 4.0

        total_volume += volume
        weighted_centroid += volume * tet_centroid

    if total_volume > 0:
        return weighted_centroid / total_volume
    return np.mean(hull_vertices, axis=0)


def verify_centroid(data: PolyhedronData) -> dict:
    """
    Verify our centroid computation against Centore's published centroid.
    """
    # Convert samples to Cartesian
    sample_points = np.array([s.to_cartesian() for s in data.samples])

    if len(sample_points) < 4:
        return {
            'color': data.color_name,
            'error': 'Not enough samples for hull computation',
            'num_samples': len(sample_points)
        }

    # Compute inner hull points
    inner_points = compute_inner_hull(sample_points)

    if len(inner_points) < 4:
        return {
            'color': data.color_name,
            'error': 'Not enough inner points for hull computation',
            'num_inner': len(inner_points)
        }

    # Compute centroids
    simple_centroid = compute_filled_solid_centroid(inner_points)
    proper_centroid = compute_proper_filled_solid_centroid(inner_points)

    # Compare to published
    published = np.array(data.published_centroid_cartesian)

    simple_error = np.linalg.norm(simple_centroid - published)
    proper_error = np.linalg.norm(proper_centroid - published)

    # Also try computing centroid from published vertices
    if data.vertices_cartesian:
        pub_vertices = np.array(data.vertices_cartesian)
        pub_vertex_centroid = compute_proper_filled_solid_centroid(pub_vertices)
        pub_vertex_error = np.linalg.norm(pub_vertex_centroid - published)
    else:
        pub_vertex_error = None

    return {
        'color': data.color_name,
        'num_samples': len(data.samples),
        'num_published_vertices': len(data.vertices_cartesian),
        'published_centroid': published.tolist(),
        'computed_simple_centroid': simple_centroid.tolist(),
        'computed_proper_centroid': proper_centroid.tolist(),
        'simple_error': float(simple_error),
        'proper_error': float(proper_error),
        'from_published_vertices_error': float(pub_vertex_error) if pub_vertex_error else None
    }


def main():
    """Run Track A verification on all polyhedron files."""
    if not POLYHEDRON_DIR.exists():
        print(f"ERROR: Polyhedron directory not found: {POLYHEDRON_DIR}")
        return

    files = sorted(POLYHEDRON_DIR.glob("PolyhedronDataFor*.txt"))
    if not files:
        print(f"ERROR: No polyhedron files found in {POLYHEDRON_DIR}")
        return

    print(f"Track A Verification: Parsing {len(files)} polyhedron files")
    print("=" * 70)

    results = []

    for filepath in files:
        try:
            data = parse_polyhedron_file(filepath)
            result = verify_centroid(data)
            results.append(result)

            # Print summary
            if 'error' in result:
                print(f"  {result['color']:12s}: ERROR - {result['error']}")
            else:
                proper_err = result['proper_error']
                pub_vert_err = result['from_published_vertices_error']
                print(f"  {result['color']:12s}: "
                      f"samples={result['num_samples']:3d}, "
                      f"vertices={result['num_published_vertices']:2d}, "
                      f"centroid_error={proper_err:.4f}, "
                      f"from_pub_verts={pub_vert_err:.4f}" if pub_vert_err else "")

        except Exception as e:
            print(f"  ERROR parsing {filepath.name}: {e}")
            results.append({'color': filepath.stem, 'error': str(e)})

    print("=" * 70)

    # Summary statistics
    valid_results = [r for r in results if 'error' not in r]
    if valid_results:
        proper_errors = [r['proper_error'] for r in valid_results]
        pub_vert_errors = [r['from_published_vertices_error'] for r in valid_results
                          if r['from_published_vertices_error'] is not None]

        print(f"\nSummary ({len(valid_results)} categories verified):")
        print(f"  Centroid error from samples:")
        print(f"    Mean: {np.mean(proper_errors):.4f}")
        print(f"    Max:  {np.max(proper_errors):.4f}")
        print(f"    Min:  {np.min(proper_errors):.4f}")

        if pub_vert_errors:
            print(f"\n  Centroid error from published vertices:")
            print(f"    Mean: {np.mean(pub_vert_errors):.4f}")
            print(f"    Max:  {np.max(pub_vert_errors):.4f}")
            print(f"    Min:  {np.min(pub_vert_errors):.4f}")

    # Save detailed results
    output_path = Path(__file__).parent.parent.parent / "writeups" / "results" / "track_a_verification.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump({
            'description': 'Track A Verification: Centroid computation comparison',
            'method': 'Inner convex hull via single-layer peeling, filled-solid centroid via tetrahedron decomposition',
            'results': results
        }, f, indent=2)

    print(f"\nDetailed results saved to: {output_path}")


if __name__ == '__main__':
    main()
