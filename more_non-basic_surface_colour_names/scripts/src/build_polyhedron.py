#!/usr/bin/env python3
"""
Build Polyhedron: Construct a colour name polyhedron from samples.

This script implements Centore's methodology for constructing inner convex hull
polyhedra from Munsell color samples. It is the standalone builder component,
separate from verification.

Usage:
    # From Munsell coordinates in a file (one per line):
    python build_polyhedron.py --input samples.txt --output polyhedron.json

    # Programmatically (import and call build_polyhedron function)

Algorithm:
1. Parse Munsell coordinates from input
2. Convert to Centore's Cartesian space
3. Compute inner convex hull (single-layer peeling)
4. Compute filled-solid centroid
5. Output polyhedron data (vertices, faces, centroid)

Reference:
    Centore, P. (2020) "Beige, aqua, fuchsia, etc.: more non-basic surface
    colour names and their Munsell settings." JAIC Vol. 25, pp. 24-54.

Validated:
    This builder uses the same core functions validated against all 30 Centore
    polyhedra with 100% concordance (Track A verification, 2025-12-25).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

import numpy as np

# Import validated core components
from core.munsell import MunsellCoord, parse_munsell, parse_munsell_from_line
from core.geometry import compute_inner_hull, compute_filled_solid_centroid, euler_edges


@dataclass
class Polyhedron:
    """
    A colour name polyhedron in Munsell Cartesian space.

    Attributes:
        colour_name: Name of the colour (e.g., "beige", "turquoise")
        num_samples: Number of input samples used
        num_vertices: Number of polyhedron vertices
        num_edges: Number of polyhedron edges (from Euler's formula)
        num_faces: Number of polyhedron faces (triangles)
        vertices: List of vertex coordinates [(x, y, z), ...]
        faces: List of face vertex indices [(i, j, k), ...]
        centroid: Filled-solid centroid (x, y, z)
    """
    colour_name: str
    num_samples: int
    num_vertices: int
    num_edges: int
    num_faces: int
    vertices: List[tuple]
    faces: List[tuple]
    centroid: tuple

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def build_polyhedron(
    samples: List[MunsellCoord],
    colour_name: str = "unnamed"
) -> Optional[Polyhedron]:
    """
    Build a polyhedron from Munsell color samples.

    This implements Centore's inner convex hull methodology:
    1. Convert samples to Cartesian coordinates
    2. Compute outer convex hull
    3. Remove outer hull vertices (single-layer peeling)
    4. Compute inner convex hull (final polyhedron)
    5. Compute filled-solid centroid

    Args:
        samples: List of MunsellCoord objects.
        colour_name: Name for the polyhedron.

    Returns:
        Polyhedron object, or None if insufficient samples.

    Raises:
        ValueError: If fewer than 4 samples provided.

    Example:
        >>> samples = [parse_munsell("5R 4/14"), parse_munsell("7.5R 5/12"), ...]
        >>> poly = build_polyhedron(samples, "red")
    """
    if len(samples) < 4:
        raise ValueError(f"Need at least 4 samples for 3D hull, got {len(samples)}")

    # Step 1: Convert to Cartesian
    points = np.array([s.to_cartesian() for s in samples])

    # Step 2-4: Compute inner hull
    inner_points, inner_hull = compute_inner_hull(points)

    if inner_hull is None:
        return None

    # Extract hull properties
    vertices = inner_points[inner_hull.vertices]
    faces = inner_hull.simplices
    num_vertices = len(vertices)
    num_faces = len(faces)
    num_edges = euler_edges(num_vertices, num_faces)

    # Step 5: Compute centroid
    centroid = compute_filled_solid_centroid(inner_points, inner_hull)

    return Polyhedron(
        colour_name=colour_name,
        num_samples=len(samples),
        num_vertices=num_vertices,
        num_edges=num_edges,
        num_faces=num_faces,
        vertices=[tuple(float(x) for x in v) for v in vertices],
        faces=[tuple(int(x) for x in f) for f in faces],
        centroid=tuple(float(x) for x in centroid)
    )


def load_samples_from_file(filepath: Path) -> List[MunsellCoord]:
    """
    Load Munsell samples from a text file.

    File format: One Munsell notation per line, or lines containing
    Munsell notation among other text (e.g., Centore's sample format).

    Args:
        filepath: Path to input file.

    Returns:
        List of parsed MunsellCoord objects.
    """
    samples = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Try direct parse first
            coord = parse_munsell(line)
            if coord is None:
                # Try extracting from line
                coord = parse_munsell_from_line(line)

            if coord is not None:
                samples.append(coord)

    return samples


def main():
    """Command-line interface for polyhedron builder."""
    parser = argparse.ArgumentParser(
        description="Build a colour name polyhedron from Munsell samples.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python build_polyhedron.py --input samples.txt --name "beige"
    python build_polyhedron.py --input samples.txt --output polyhedron.json
        """
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        required=True,
        help='Input file with Munsell samples (one per line)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output JSON file (default: stdout)'
    )
    parser.add_argument(
        '--name', '-n',
        type=str,
        default='unnamed',
        help='Colour name for the polyhedron'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print detailed progress'
    )

    args = parser.parse_args()

    # Load samples
    if args.verbose:
        print(f"Loading samples from: {args.input}")

    samples = load_samples_from_file(args.input)

    if args.verbose:
        print(f"Loaded {len(samples)} samples")

    if len(samples) < 4:
        print(f"ERROR: Need at least 4 samples, got {len(samples)}", file=sys.stderr)
        sys.exit(1)

    # Build polyhedron
    if args.verbose:
        print("Building polyhedron...")

    try:
        poly = build_polyhedron(samples, args.name)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if poly is None:
        print("ERROR: Could not compute inner hull", file=sys.stderr)
        sys.exit(1)

    # Output
    result = poly.to_dict()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        if args.verbose:
            print(f"Saved to: {args.output}")
    else:
        print(json.dumps(result, indent=2))

    # Summary
    if args.verbose:
        print(f"\nPolyhedron Summary:")
        print(f"  Colour name: {poly.colour_name}")
        print(f"  Samples: {poly.num_samples}")
        print(f"  Vertices: {poly.num_vertices}")
        print(f"  Edges: {poly.num_edges}")
        print(f"  Faces: {poly.num_faces}")
        print(f"  Centroid: ({poly.centroid[0]:.4f}, {poly.centroid[1]:.4f}, {poly.centroid[2]:.4f})")


if __name__ == '__main__':
    main()
