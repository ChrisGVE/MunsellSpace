#!/usr/bin/env python3
"""
Preliminary Shape Analysis: Compare polyhedra shapes between Centore (surface)
and our screen color families.

Questions to answer:
a) Do polyhedra look alike (spherical, ovoid, elongated, irregular)?
b) Is the centroid placed at equivalent positions within each polyhedron?

This is a qualitative starting point before optimization.
"""

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
from scipy.spatial import ConvexHull

# Paths
BASE_DIR = Path(__file__).parent.parent
CENTORE_DIR = BASE_DIR / "centore" / "PolyhedronFilesJustNames"
PHASE6_DIR = BASE_DIR / "phase6" / "polyhedra"

# Munsell hue names for conversion
MUNSELL_HUES = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"]


def munsell_to_cartesian(notation: str) -> Optional[Tuple[float, float, float]]:
    """Convert Munsell notation like '5.12G 5.19/2.32' to Cartesian (x, y, z)."""
    try:
        # Pattern: number + hue letters + space + value/chroma
        pattern = r"(\d+\.?\d*)([A-Z]+)\s+(\d+\.?\d*)/(\d+\.?\d*)"
        match = re.match(pattern, notation.strip())
        if not match:
            return None

        hue_num = float(match.group(1))
        hue_name = match.group(2)
        value = float(match.group(3))
        chroma = float(match.group(4))

        # Convert to angle (0-2π)
        hue_index = MUNSELL_HUES.index(hue_name)
        total_hue = hue_index * 10 + hue_num
        angle = (total_hue / 100) * 2 * math.pi

        # Cartesian
        x = chroma * math.cos(angle)
        y = chroma * math.sin(angle)
        z = value

        return (x, y, z)
    except (ValueError, IndexError):
        return None


@dataclass
class ShapeMetrics:
    """Metrics describing polyhedron shape."""
    name: str
    n_vertices: int
    volume: float
    surface_area: float

    # Bounding box
    bbox_dims: Tuple[float, float, float]  # (dx, dy, dz)

    # Shape characteristics
    sphericity: float  # 0-1, 1 = perfect sphere
    elongation: float  # ratio of longest to shortest principal axis
    flatness: float    # ratio of middle to shortest principal axis

    # Centroid position
    centroid: Tuple[float, float, float]
    centroid_offset: Tuple[float, float, float]  # relative to bbox center (normalized)

    # Principal axes
    principal_axes: np.ndarray  # 3x3 matrix of eigenvectors
    principal_lengths: Tuple[float, float, float]  # eigenvalues (sorted)


def compute_shape_metrics(vertices: np.ndarray, name: str) -> Optional[ShapeMetrics]:
    """Compute shape metrics for a set of vertices."""
    if len(vertices) < 4:
        return None

    try:
        hull = ConvexHull(vertices)
    except Exception:
        return None

    # Volume and surface area from convex hull
    volume = hull.volume
    surface_area = hull.area

    # Bounding box
    mins = vertices.min(axis=0)
    maxs = vertices.max(axis=0)
    bbox_dims = tuple(maxs - mins)
    bbox_center = (mins + maxs) / 2

    # Centroid (mean of vertices)
    centroid = vertices.mean(axis=0)

    # Normalized centroid offset (-0.5 to 0.5 range, 0 = centered)
    offset = (centroid - bbox_center) / (np.array(bbox_dims) + 1e-10)
    centroid_offset = tuple(offset)

    # Principal Component Analysis for shape
    centered = vertices - centroid
    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    # Sort by eigenvalue (largest first)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Principal lengths (sqrt of eigenvalues gives spread in each direction)
    principal_lengths = tuple(np.sqrt(np.maximum(eigenvalues, 0)))

    # Elongation: ratio of largest to smallest principal length
    if principal_lengths[2] > 1e-10:
        elongation = principal_lengths[0] / principal_lengths[2]
        flatness = principal_lengths[1] / principal_lengths[2]
    else:
        elongation = float('inf')
        flatness = float('inf')

    # Sphericity: how close to a sphere
    # Using Wadell sphericity: (π^(1/3) * (6V)^(2/3)) / A
    if surface_area > 0:
        sphericity = (math.pi ** (1/3) * (6 * volume) ** (2/3)) / surface_area
    else:
        sphericity = 0

    return ShapeMetrics(
        name=name,
        n_vertices=len(vertices),
        volume=volume,
        surface_area=surface_area,
        bbox_dims=bbox_dims,
        sphericity=sphericity,
        elongation=elongation,
        flatness=flatness,
        centroid=tuple(centroid),
        centroid_offset=centroid_offset,
        principal_axes=eigenvectors,
        principal_lengths=principal_lengths
    )


def load_centore_polyhedron(filepath: Path) -> Tuple[str, np.ndarray, Tuple[float, float, float]]:
    """Load Centore polyhedron vertices and centroid."""
    with open(filepath) as f:
        lines = f.readlines()

    name = None
    centroid_cartesian = None
    vertices = []
    in_vertices = False
    in_cartesian = False

    for line in lines:
        line = line.strip()
        if line.startswith("Colour name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("Centroid in Cartesian"):
            parts = line.split(":", 1)[1].strip().split()
            if len(parts) >= 3:
                centroid_cartesian = (float(parts[0]), float(parts[1]), float(parts[2]))
        elif line.startswith("Polyhedron vertices in Munsell"):
            in_vertices = True
            in_cartesian = False
        elif line.startswith("Polyhedron vertices in Cartesian"):
            in_vertices = False
            in_cartesian = True
        elif line.startswith("Polyhedron faces") or line.startswith("Samples,"):
            # Stop parsing - we've reached non-vertex data
            in_vertices = False
            in_cartesian = False
        elif in_vertices and line:
            # Parse Munsell vertex
            cart = munsell_to_cartesian(line)
            if cart:
                vertices.append(cart)
        elif in_cartesian and line:
            # Parse Cartesian vertex directly
            parts = line.split()
            if len(parts) >= 3:
                try:
                    vertices.append((float(parts[0]), float(parts[1]), float(parts[2])))
                except ValueError:
                    pass

    return name, np.array(vertices), centroid_cartesian


def load_screen_polyhedron(filepath: Path) -> Tuple[str, np.ndarray, Tuple[float, float, float]]:
    """Load our screen color polyhedron."""
    with open(filepath) as f:
        data = json.load(f)

    # Name from "family" field or filename
    name = data.get("family", filepath.stem.replace("_polyhedron", ""))

    # Get vertices - format is list of [x, y, z] arrays
    vertices = []
    if "vertices" in data:
        for v in data["vertices"]:
            if isinstance(v, list) and len(v) >= 3:
                vertices.append((v[0], v[1], v[2]))

    # Get centroid if available
    centroid = None
    if "centroid" in data:
        c = data["centroid"]
        if isinstance(c, list) and len(c) >= 3:
            centroid = (c[0], c[1], c[2])
        elif isinstance(c, dict):
            centroid = (c.get("x", 0), c.get("y", 0), c.get("z", 0))

    return name, np.array(vertices) if vertices else np.array([]), centroid


def classify_shape(metrics: ShapeMetrics) -> str:
    """Classify polyhedron shape qualitatively."""
    if metrics.sphericity > 0.8:
        shape = "spherical"
    elif metrics.elongation > 3:
        if metrics.flatness > 2:
            shape = "elongated rod"
        else:
            shape = "cigar-shaped"
    elif metrics.flatness < 1.5 and metrics.elongation < 2:
        shape = "roughly spherical"
    elif metrics.elongation > 2:
        shape = "ovoid/ellipsoid"
    else:
        shape = "irregular"

    return shape


def main():
    print("=" * 70)
    print("POLYHEDRA SHAPE ANALYSIS: Centore (Surface) vs Screen Colors")
    print("=" * 70)

    # Load Centore polyhedra
    print("\nLoading Centore polyhedra...")
    centore_data = {}
    for filepath in sorted(CENTORE_DIR.glob("PolyhedronDataFor*.txt")):
        name, vertices, centroid = load_centore_polyhedron(filepath)
        if len(vertices) >= 4:
            metrics = compute_shape_metrics(vertices, name)
            if metrics:
                centore_data[name] = {
                    "vertices": vertices,
                    "centroid": centroid,
                    "metrics": metrics
                }
    print(f"  Loaded {len(centore_data)} Centore polyhedra")

    # Load screen color polyhedra
    print("\nLoading screen color polyhedra...")
    screen_data = {}
    if PHASE6_DIR.exists():
        for filepath in sorted(PHASE6_DIR.glob("*_polyhedron.json")):
            name, vertices, centroid = load_screen_polyhedron(filepath)
            if len(vertices) >= 4:
                metrics = compute_shape_metrics(vertices, name)
                if metrics:
                    screen_data[name] = {
                        "vertices": vertices,
                        "centroid": centroid,
                        "metrics": metrics
                    }
    print(f"  Loaded {len(screen_data)} screen polyhedra")

    # Find common families
    common_names = set(centore_data.keys()) & set(screen_data.keys())
    print(f"\nCommon families: {len(common_names)}")
    print(f"  {sorted(common_names)}")

    # Compare shapes
    print("\n" + "=" * 70)
    print("SHAPE COMPARISON FOR COMMON FAMILIES")
    print("=" * 70)

    print(f"\n{'Family':<12} {'Centore Shape':<18} {'Screen Shape':<18} {'Match?':<8}")
    print("-" * 60)

    shape_matches = 0
    shape_comparisons = []

    for name in sorted(common_names):
        cm = centore_data[name]["metrics"]
        sm = screen_data[name]["metrics"]

        c_shape = classify_shape(cm)
        s_shape = classify_shape(sm)

        match = c_shape == s_shape or (
            ("spherical" in c_shape and "spherical" in s_shape) or
            ("ovoid" in c_shape and "ovoid" in s_shape) or
            ("elongated" in c_shape and "elongated" in s_shape)
        )

        if match:
            shape_matches += 1
            match_str = "✓"
        else:
            match_str = "✗"

        print(f"{name:<12} {c_shape:<18} {s_shape:<18} {match_str}")

        shape_comparisons.append({
            "name": name,
            "centore_shape": c_shape,
            "screen_shape": s_shape,
            "match": match,
            "centore_metrics": cm,
            "screen_metrics": sm
        })

    print(f"\nShape similarity: {shape_matches}/{len(common_names)} ({100*shape_matches/len(common_names):.1f}%)")

    # Centroid position analysis
    print("\n" + "=" * 70)
    print("CENTROID POSITION ANALYSIS")
    print("=" * 70)
    print("\nCentroid offset from bbox center (normalized -0.5 to 0.5, 0=centered):")

    print(f"\n{'Family':<12} {'Centore offset':<30} {'Screen offset':<30} {'Similar?'}")
    print("-" * 80)

    position_matches = 0

    for name in sorted(common_names):
        cm = centore_data[name]["metrics"]
        sm = screen_data[name]["metrics"]

        c_off = cm.centroid_offset
        s_off = sm.centroid_offset

        c_str = f"({c_off[0]:+.2f}, {c_off[1]:+.2f}, {c_off[2]:+.2f})"
        s_str = f"({s_off[0]:+.2f}, {s_off[1]:+.2f}, {s_off[2]:+.2f})"

        # Check if offsets are similar (within 0.2 on each axis)
        offset_diff = np.array(c_off) - np.array(s_off)
        similar = np.all(np.abs(offset_diff) < 0.25)

        if similar:
            position_matches += 1
            match_str = "✓"
        else:
            match_str = "✗"

        print(f"{name:<12} {c_str:<30} {s_str:<30} {match_str}")

    print(f"\nCentroid position similarity: {position_matches}/{len(common_names)} ({100*position_matches/len(common_names):.1f}%)")

    # Detailed metrics comparison
    print("\n" + "=" * 70)
    print("DETAILED METRICS COMPARISON")
    print("=" * 70)

    print(f"\n{'Family':<10} {'C.Sph':>6} {'S.Sph':>6} {'C.Elong':>8} {'S.Elong':>8} {'C.Vol':>10} {'S.Vol':>10}")
    print("-" * 65)

    for name in sorted(common_names):
        cm = centore_data[name]["metrics"]
        sm = screen_data[name]["metrics"]

        print(f"{name:<10} {cm.sphericity:6.3f} {sm.sphericity:6.3f} "
              f"{cm.elongation:8.2f} {sm.elongation:8.2f} "
              f"{cm.volume:10.1f} {sm.volume:10.1f}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
Common families analyzed: {len(common_names)}

a) Shape similarity: {shape_matches}/{len(common_names)} ({100*shape_matches/len(common_names):.1f}%)
   - Measures whether polyhedra are similarly spherical/elongated/irregular

b) Centroid position: {position_matches}/{len(common_names)} ({100*position_matches/len(common_names):.1f}%)
   - Measures whether centroids sit at equivalent positions within bbox

Pattern detected: {"YES - shapes/positions correlate" if shape_matches > len(common_names)/2 and position_matches > len(common_names)/2 else "WEAK/NO - significant differences"}
""")

    return shape_comparisons


if __name__ == "__main__":
    comparisons = main()
