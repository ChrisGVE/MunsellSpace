#!/usr/bin/env python3
"""
Phase 6.4: Polyhedra Construction

Constructs convex hull polyhedra in Munsell Cartesian space for each
color family based on the validated assignments.

Uses only consistent colors (those where NLP assignment matches Munsell position).

Input: datasets/phase6/validated_assignments.csv
Output: datasets/phase6/polyhedra/
          - {family}_polyhedron.json (vertices, faces, centroid, stats)
        datasets/phase6/polyhedra_summary.json
"""

import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import numpy as np
from scipy.spatial import ConvexHull


# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
PHASE6_DIR = DATASETS_DIR / "phase6"
OUTPUT_DIR = PHASE6_DIR / "polyhedra"
OUTPUT_DIR.mkdir(exist_ok=True)


@dataclass
class Polyhedron:
    """Convex hull polyhedron for a color family."""
    family: str
    vertices: List[Tuple[float, float, float]]
    faces: List[Tuple[int, int, int]]
    centroid: Tuple[float, float, float]
    volume: float
    surface_area: float
    sample_count: int
    point_count: int  # Number of unique Cartesian points

    def to_dict(self) -> Dict:
        return {
            "family": self.family,
            "vertices": self.vertices,
            "faces": self.faces,
            "centroid": list(self.centroid),
            "volume": self.volume,
            "surface_area": self.surface_area,
            "sample_count": self.sample_count,
            "point_count": self.point_count,
            "vertex_count": len(self.vertices),
            "face_count": len(self.faces),
        }


def load_validated_data() -> List[Dict]:
    """Load validated color assignments."""
    csv_path = PHASE6_DIR / "validated_assignments.csv"
    colors = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include colors with valid Cartesian coordinates
            if row.get("cartesian_x") and row.get("cartesian_y") and row.get("cartesian_z"):
                try:
                    x = float(row["cartesian_x"])
                    y = float(row["cartesian_y"])
                    z = float(row["cartesian_z"])
                    if not (math.isnan(x) or math.isnan(y) or math.isnan(z)):
                        colors.append({
                            **row,
                            "point": (x, y, z)
                        })
                except (ValueError, TypeError):
                    pass

    print(f"Loaded {len(colors)} validated colors with coordinates")
    return colors


def group_by_family(colors: List[Dict]) -> Dict[str, List[Tuple[float, float, float]]]:
    """Group colors by family and extract unique Cartesian points."""
    families = defaultdict(set)

    for color in colors:
        family = color["assigned_family"]
        point = color["point"]
        # Round to avoid floating point duplicates
        rounded = (round(point[0], 4), round(point[1], 4), round(point[2], 4))
        families[family].add(rounded)

    # Convert sets to lists
    result = {f: list(points) for f, points in families.items()}

    print(f"Grouped into {len(result)} families")
    for family, points in sorted(result.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {family}: {len(points)} unique points")

    return result


def compute_centroid(points: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Compute centroid of a set of points."""
    arr = np.array(points)
    return tuple(np.mean(arr, axis=0).tolist())


def build_polyhedron(family: str, points: List[Tuple[float, float, float]], sample_count: int) -> Optional[Polyhedron]:
    """Build a convex hull polyhedron from points."""
    if len(points) < 4:
        print(f"  {family}: Only {len(points)} points, need at least 4 for 3D hull")
        return None

    arr = np.array(points)

    # Check if points are coplanar or nearly coplanar
    try:
        hull = ConvexHull(arr)
    except Exception as e:
        print(f"  {family}: ConvexHull failed: {e}")
        # Try adding jitter
        jitter = np.random.normal(0, 0.001, arr.shape)
        try:
            hull = ConvexHull(arr + jitter)
        except Exception:
            return None

    # Extract vertices and faces
    vertices = [tuple(hull.points[i].tolist()) for i in range(len(hull.points)) if i in set(hull.vertices)]
    vertex_map = {old: new for new, old in enumerate(sorted(set(hull.vertices)))}

    # ConvexHull uses simplices (triangular faces)
    faces = []
    for simplex in hull.simplices:
        # Map to new vertex indices
        face = tuple(vertex_map.get(i, i) for i in simplex if i in vertex_map)
        if len(face) == 3:
            faces.append(face)

    # Get actual vertices in order
    actual_vertices = [tuple(hull.points[i].tolist()) for i in sorted(set(hull.vertices))]

    centroid = compute_centroid(points)

    return Polyhedron(
        family=family,
        vertices=actual_vertices,
        faces=faces,
        centroid=centroid,
        volume=hull.volume,
        surface_area=hull.area,
        sample_count=sample_count,
        point_count=len(points)
    )


def build_all_polyhedra(family_points: Dict[str, List[Tuple]], sample_counts: Dict[str, int]) -> List[Polyhedron]:
    """Build polyhedra for all families."""
    polyhedra = []

    print("\nBuilding polyhedra...")
    for family, points in sorted(family_points.items()):
        poly = build_polyhedron(family, points, sample_counts.get(family, 0))
        if poly:
            polyhedra.append(poly)
            print(f"  {family}: {len(poly.vertices)} vertices, {len(poly.faces)} faces, volume={poly.volume:.2f}")

    return polyhedra


def save_polyhedra(polyhedra: List[Polyhedron]):
    """Save each polyhedron to a separate JSON file."""
    for poly in polyhedra:
        json_path = OUTPUT_DIR / f"{poly.family}_polyhedron.json"
        with open(json_path, "w") as f:
            json.dump(poly.to_dict(), f, indent=2)

    print(f"\nSaved {len(polyhedra)} polyhedra to {OUTPUT_DIR}")


def create_summary(polyhedra: List[Polyhedron]) -> Dict:
    """Create a summary of all polyhedra."""
    summary = {
        "total_families": len(polyhedra),
        "total_vertices": sum(len(p.vertices) for p in polyhedra),
        "total_faces": sum(len(p.faces) for p in polyhedra),
        "total_volume": sum(p.volume for p in polyhedra),
        "families": {}
    }

    for poly in sorted(polyhedra, key=lambda x: -x.volume):
        summary["families"][poly.family] = {
            "vertex_count": len(poly.vertices),
            "face_count": len(poly.faces),
            "volume": round(poly.volume, 4),
            "surface_area": round(poly.surface_area, 4),
            "sample_count": poly.sample_count,
            "point_count": poly.point_count,
            "centroid": [round(c, 4) for c in poly.centroid],
        }

    return summary


def print_summary(polyhedra: List[Polyhedron]):
    """Print summary of constructed polyhedra."""
    print("\n" + "=" * 70)
    print("POLYHEDRA CONSTRUCTION SUMMARY")
    print("=" * 70)

    print(f"\nTotal families with polyhedra: {len(polyhedra)}")
    print(f"Total vertices: {sum(len(p.vertices) for p in polyhedra)}")
    print(f"Total faces: {sum(len(p.faces) for p in polyhedra)}")

    print(f"\n{'Family':<15} {'Vertices':>10} {'Faces':>8} {'Volume':>12} {'Points':>10}")
    print("-" * 60)

    for poly in sorted(polyhedra, key=lambda x: -x.volume):
        print(f"{poly.family:<15} {len(poly.vertices):>10} {len(poly.faces):>8} {poly.volume:>12.2f} {poly.point_count:>10}")


def main():
    """Main entry point."""
    print("Phase 6.4: Polyhedra Construction")
    print("=" * 50)

    # Load validated data
    colors = load_validated_data()

    # Count samples per family (before deduplication)
    sample_counts = defaultdict(int)
    for color in colors:
        sample_counts[color["assigned_family"]] += 1

    # Group by family
    family_points = group_by_family(colors)

    # Build polyhedra
    polyhedra = build_all_polyhedra(family_points, sample_counts)

    # Save individual polyhedra
    save_polyhedra(polyhedra)

    # Create and save summary
    summary = create_summary(polyhedra)
    summary_path = PHASE6_DIR / "polyhedra_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary to {summary_path}")

    # Print summary
    print_summary(polyhedra)

    print("\nPhase 6.4 complete!")


if __name__ == "__main__":
    main()
