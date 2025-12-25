#!/usr/bin/env python3
"""
Build Convex Hull Polyhedra for Color Names

This script implements Centore's methodology for constructing polyhedra:
1. Collect color samples in Munsell space
2. Convert to Cartesian coordinates
3. Compute convex hull (minimal generating set)
4. Output vertices, faces, and centroid

Usage:
    python build_convex_hulls.py [--source centore|xkcd|both] [--validate]

Options:
    --source: Which data source to process (default: both)
    --validate: Validate against Centore's original polyhedra
"""

import json
import math
import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
import numpy as np
from scipy.spatial import ConvexHull

from common import save_results, INVESTIGATION_DIR


@dataclass
class MunsellPoint:
    """A point in Munsell color space."""
    hue_str: str        # e.g., "5R", "7.5BG"
    hue_degrees: float  # 0-360
    value: float        # 0-10
    chroma: float       # 0-20+
    name: str = ""      # Sample name (optional)

    def to_cartesian(self) -> Tuple[float, float, float]:
        """Convert to Cartesian coordinates (x, y, z)."""
        if self.chroma < 0.01:  # Neutral
            return (0.0, 0.0, self.value)

        hue_rad = self.hue_degrees * math.pi / 180.0
        x = self.chroma * math.cos(hue_rad)
        y = self.chroma * math.sin(hue_rad)
        z = self.value
        return (x, y, z)


@dataclass
class Polyhedron:
    """A convex polyhedron in Munsell Cartesian space."""
    color_name: str
    vertices: np.ndarray        # Nx3 array of vertex coordinates
    faces: np.ndarray           # Mx3 array of face indices (triangles)
    centroid: Tuple[float, float, float]
    sample_count: int
    vertex_count: int
    volume: float = 0.0
    source: str = ""            # "centore" or "xkcd"


# Hue family angles (center of each family in degrees)
HUE_FAMILIES = {
    'R': 0, 'YR': 36, 'Y': 72, 'GY': 108,
    'G': 144, 'BG': 180, 'B': 216, 'PB': 252,
    'P': 288, 'RP': 324
}


def parse_munsell_notation(notation: str) -> Optional[MunsellPoint]:
    """
    Parse Munsell notation string to MunsellPoint.

    Formats:
    - Chromatic: "5.5R 4.5/12" or "5R 4/12" or "5.5R4.5/12"
    - Neutral: "N 5.0" or "N5.0"
    """
    notation = notation.strip()

    # Handle neutral colors
    if notation.startswith('N'):
        match = re.match(r'N\s*([0-9.]+)', notation)
        if match:
            value = float(match.group(1))
            return MunsellPoint('N', 0.0, value, 0.0)
        return None

    # Parse chromatic colors: "5.61P 5.37/4.79" or "6.80PB 6.06/6.09"
    match = re.match(
        r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s*(\d+\.?\d*)/(\d+\.?\d*)',
        notation
    )
    if match:
        hue_value = float(match.group(1))
        hue_family = match.group(2)
        value = float(match.group(3))
        chroma = float(match.group(4))

        # Convert to degrees (0-360)
        family_base = HUE_FAMILIES.get(hue_family, 0)
        # Each family spans 36 degrees, hue_value 0-10 maps within that
        hue_degrees = family_base + (hue_value / 10.0) * 36.0
        if hue_degrees >= 360:
            hue_degrees -= 360

        return MunsellPoint(
            f"{hue_value}{hue_family}",
            hue_degrees,
            value,
            chroma
        )

    return None


def load_centore_samples(color_name: str) -> List[MunsellPoint]:
    """Load CAUS samples for a color from Centore polyhedron files."""
    project_root = Path(__file__).parent.parent.parent
    polydir = project_root / "PolyhedronFilesJustNames"

    filename = f"PolyhedronDataFor{color_name}.txt"
    filepath = polydir / filename

    if not filepath.exists():
        return []

    samples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        in_samples = False
        for line in f:
            line = line.strip()

            if "Samples, with Munsell coordinates" in line:
                in_samples = True
                continue

            if in_samples and line:
                # Format: "Sample Name\tMunsell Notation"
                parts = line.split('\t')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    notation = parts[1].strip()
                    point = parse_munsell_notation(notation)
                    if point:
                        point.name = name
                        samples.append(point)

    return samples


def load_centore_original_vertices(color_name: str) -> Optional[np.ndarray]:
    """Load original Centore vertices for validation."""
    project_root = Path(__file__).parent.parent.parent
    polydir = project_root / "PolyhedronFilesJustNames"

    filename = f"PolyhedronDataFor{color_name}.txt"
    filepath = polydir / filename

    if not filepath.exists():
        return None

    vertices = []
    with open(filepath, 'r', encoding='utf-8') as f:
        in_cartesian = False
        for line in f:
            line = line.strip()

            if "Polyhedron vertices in Cartesian" in line:
                in_cartesian = True
                continue

            if "Polyhedron faces" in line:
                break

            if in_cartesian and line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    try:
                        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                        vertices.append([x, y, z])
                    except ValueError:
                        pass

    return np.array(vertices) if vertices else None


def load_xkcd_samples(color_name: str) -> List[MunsellPoint]:
    """Load XKCD samples for a color from Munsell conversions."""
    munsell_path = INVESTIGATION_DIR / "munsell_conversions.json"

    if not munsell_path.exists():
        return []

    with open(munsell_path) as f:
        data = json.load(f)

    colors = data.get('colors', {})
    pattern = re.compile(rf'\b{re.escape(color_name)}\b', re.IGNORECASE)

    samples = []
    for name, color_data in colors.items():
        if pattern.search(name):
            m = color_data.get('munsell', {})
            cart = color_data.get('cartesian', {})

            if 'hue_str' in m and 'value' in m and 'chroma' in m:
                # Compute hue degrees from hue_num (0-40 Munsell scale)
                hue_num = m.get('hue_num', 0)
                hue_degrees = hue_num * 9.0  # 40 → 360

                point = MunsellPoint(
                    hue_str=m.get('hue_letter', 'R'),
                    hue_degrees=hue_degrees,
                    value=m['value'],
                    chroma=m['chroma'],
                    name=name
                )
                samples.append(point)

    return samples


def build_polyhedron(samples: List[MunsellPoint], color_name: str, source: str,
                     use_inner_hull: bool = True) -> Optional[Polyhedron]:
    """
    Build a convex hull polyhedron from color samples.

    This implements Centore's INNER CONVEX HULL methodology (JAIC 2020, pp. 31-35):
    1. Convert samples to Cartesian coordinates (S)
    2. Compute outer convex hull H of S
    3. Find vertices V of H (minimal generating set)
    4. Discard all vertices V to get S−V (outlier removal)
    5. Compute inner convex hull Γ of S−V (final polyhedron)
    6. Compute filled-solid centroid

    Args:
        samples: List of MunsellPoint samples
        color_name: Name of the color category
        source: Data source identifier ("centore" or "xkcd")
        use_inner_hull: If True, use Centore's inner hull method.
                       If False, use pure convex hull (for comparison).
    """
    if len(samples) < 4:
        print(f"  Warning: {color_name} has only {len(samples)} samples (need >= 4 for 3D hull)")
        return None

    # Step 1: Convert to Cartesian (S)
    S = np.array([s.to_cartesian() for s in samples])

    # Step 2: Compute outer convex hull H
    try:
        H = ConvexHull(S)
    except Exception as e:
        print(f"  Warning: Could not build outer hull for {color_name}: {e}")
        return None

    if not use_inner_hull:
        # Pure convex hull (for comparison/debugging)
        vertices = S[H.vertices]
        faces = H.simplices
        centroid = (
            float(np.mean(S[:, 0])),
            float(np.mean(S[:, 1])),
            float(np.mean(S[:, 2]))
        )
        return Polyhedron(
            color_name=color_name,
            vertices=vertices,
            faces=faces,
            centroid=centroid,
            sample_count=len(samples),
            vertex_count=len(vertices),
            volume=float(H.volume),
            source=source
        )

    # Step 3: Find vertices V (minimal generating set)
    outer_vertex_indices = set(H.vertices)

    # Step 4: Discard outer vertices to get S−V
    S_minus_V_indices = [i for i in range(len(S)) if i not in outer_vertex_indices]
    S_minus_V = S[S_minus_V_indices]

    if len(S_minus_V) < 4:
        # Not enough points for inner hull - fall back to outer hull
        print(f"  Warning: {color_name} has only {len(S_minus_V)} inner points, using outer hull")
        vertices = S[H.vertices]
        faces = H.simplices
        centroid = (
            float(np.mean(S[:, 0])),
            float(np.mean(S[:, 1])),
            float(np.mean(S[:, 2]))
        )
        return Polyhedron(
            color_name=color_name,
            vertices=vertices,
            faces=faces,
            centroid=centroid,
            sample_count=len(samples),
            vertex_count=len(vertices),
            volume=float(H.volume),
            source=source
        )

    # Step 5: Compute inner convex hull Γ of S−V
    try:
        Gamma = ConvexHull(S_minus_V)
    except Exception as e:
        print(f"  Warning: Could not build inner hull for {color_name}: {e}")
        # Fall back to outer hull
        vertices = S[H.vertices]
        faces = H.simplices
        centroid = (
            float(np.mean(S[:, 0])),
            float(np.mean(S[:, 1])),
            float(np.mean(S[:, 2]))
        )
        return Polyhedron(
            color_name=color_name,
            vertices=vertices,
            faces=faces,
            centroid=centroid,
            sample_count=len(samples),
            vertex_count=len(vertices),
            volume=float(H.volume),
            source=source
        )

    # Extract inner hull vertices and faces
    vertices = S_minus_V[Gamma.vertices]
    faces = Gamma.simplices

    # Step 6: Compute centroid
    # Note: Centore uses filled-solid centroid (equations 6-8)
    # For now, use arithmetic mean of vertices as approximation
    # TODO: Implement proper filled-solid centroid
    centroid = (
        float(np.mean(vertices[:, 0])),
        float(np.mean(vertices[:, 1])),
        float(np.mean(vertices[:, 2]))
    )

    return Polyhedron(
        color_name=color_name,
        vertices=vertices,
        faces=faces,
        centroid=centroid,
        sample_count=len(samples),
        vertex_count=len(vertices),
        volume=float(Gamma.volume),
        source=source
    )


def validate_against_centore(polyhedron: Polyhedron) -> Dict:
    """Validate our computed hull against Centore's original vertices."""
    original = load_centore_original_vertices(polyhedron.color_name)

    if original is None:
        return {'valid': False, 'reason': 'Original not found'}

    computed = polyhedron.vertices

    # Compare vertex counts
    if len(original) != len(computed):
        return {
            'valid': False,
            'reason': f'Vertex count mismatch: {len(original)} vs {len(computed)}',
            'original_count': len(original),
            'computed_count': len(computed)
        }

    # Sort both arrays and compare
    # Note: vertices may be in different order
    orig_sorted = np.sort(original, axis=0)
    comp_sorted = np.sort(computed, axis=0)

    # Check if vertices match within tolerance
    max_diff = np.max(np.abs(orig_sorted - comp_sorted))

    if max_diff < 0.01:
        return {
            'valid': True,
            'max_difference': float(max_diff),
            'vertex_count': len(original)
        }
    else:
        return {
            'valid': False,
            'reason': f'Vertex values differ by {max_diff:.4f}',
            'max_difference': float(max_diff)
        }


def process_centore_colors() -> Dict[str, Polyhedron]:
    """Process all Centore overlay colors."""
    colors = [
        'aqua', 'beige', 'blue', 'brown', 'coral', 'fuchsia', 'gold',
        'gray', 'green', 'lavender', 'lilac', 'magenta', 'mauve',
        'navy', 'orange', 'peach', 'pink', 'purple', 'red', 'rose',
        'rust', 'sand', 'tan', 'taupe', 'teal', 'turquoise', 'violet',
        'white', 'wine', 'yellow'
    ]

    polyhedra = {}

    print("Processing Centore colors...")
    for color in colors:
        samples = load_centore_samples(color)
        if samples:
            poly = build_polyhedron(samples, color, "centore")
            if poly:
                polyhedra[color] = poly
                print(f"  {color}: {poly.sample_count} samples → {poly.vertex_count} vertices")

    return polyhedra


def process_xkcd_colors(color_names: List[str]) -> Dict[str, Polyhedron]:
    """Process XKCD colors to build polyhedra."""
    polyhedra = {}

    print("Processing XKCD colors...")
    for color in color_names:
        samples = load_xkcd_samples(color)
        if samples:
            poly = build_polyhedron(samples, color, "xkcd")
            if poly:
                polyhedra[color] = poly
                print(f"  {color}: {poly.sample_count} samples → {poly.vertex_count} vertices")

    return polyhedra


def main():
    parser = argparse.ArgumentParser(description="Build convex hull polyhedra for color names")
    parser.add_argument('--source', choices=['centore', 'xkcd', 'both'], default='both',
                        help='Data source to process')
    parser.add_argument('--validate', action='store_true',
                        help='Validate against Centore original polyhedra')
    args = parser.parse_args()

    print("=" * 70)
    print("CONVEX HULL POLYHEDRON CONSTRUCTION")
    print("=" * 70)
    print()

    results = {
        'centore': {},
        'xkcd': {},
        'validation': {}
    }

    # Process Centore data
    if args.source in ['centore', 'both']:
        print("\n1. Processing Centore CAUS samples...")
        centore_polys = process_centore_colors()
        results['centore'] = {
            name: {
                'sample_count': p.sample_count,
                'vertex_count': p.vertex_count,
                'centroid': p.centroid,
                'volume': p.volume
            }
            for name, p in centore_polys.items()
        }

        if args.validate:
            print("\n2. Validating against original Centore polyhedra...")
            for name, poly in centore_polys.items():
                validation = validate_against_centore(poly)
                results['validation'][name] = validation
                status = "✓" if validation.get('valid') else "✗"
                reason = validation.get('reason', 'OK')
                print(f"  {status} {name}: {reason}")

    # Process XKCD data
    if args.source in ['xkcd', 'both']:
        print("\n3. Processing XKCD samples...")
        # Use the same color names as Centore for comparison
        color_names = [
            'aqua', 'beige', 'coral', 'fuchsia', 'gold', 'lavender', 'lilac',
            'magenta', 'mauve', 'navy', 'peach', 'rose', 'rust', 'sand',
            'tan', 'taupe', 'teal', 'turquoise', 'violet', 'wine'
        ]
        xkcd_polys = process_xkcd_colors(color_names)
        results['xkcd'] = {
            name: {
                'sample_count': p.sample_count,
                'vertex_count': p.vertex_count,
                'centroid': p.centroid,
                'volume': p.volume
            }
            for name, p in xkcd_polys.items()
        }

    # Save results
    print("\n4. Saving results...")
    save_results(results, 'convex_hull_results.json')

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if results['centore']:
        print(f"\nCentore polyhedra: {len(results['centore'])}")
        total_samples = sum(p['sample_count'] for p in results['centore'].values())
        total_vertices = sum(p['vertex_count'] for p in results['centore'].values())
        print(f"  Total samples: {total_samples}")
        print(f"  Total vertices: {total_vertices}")
        print(f"  Vertex ratio: {total_vertices/total_samples:.1%}")

    if results['xkcd']:
        print(f"\nXKCD polyhedra: {len(results['xkcd'])}")
        total_samples = sum(p['sample_count'] for p in results['xkcd'].values())
        total_vertices = sum(p['vertex_count'] for p in results['xkcd'].values())
        print(f"  Total samples: {total_samples}")
        print(f"  Total vertices: {total_vertices}")
        print(f"  Vertex ratio: {total_vertices/total_samples:.1%}")

    if results['validation']:
        valid_count = sum(1 for v in results['validation'].values() if v.get('valid'))
        print(f"\nValidation: {valid_count}/{len(results['validation'])} polyhedra match")


if __name__ == "__main__":
    main()
