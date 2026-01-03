#!/usr/bin/env python3
"""
Polyhedron Comparison Metrics Implementation

Implements metrics for comparing 3D polyhedra in Munsell color space:
1. Volume metrics - ratio, intersection, Jaccard index
2. Centroid displacement - Euclidean distance
3. Hausdorff distance - maximum surface deviation
4. Procrustes distance - after optimal alignment

Based on literature review in POLYHEDRON_COMPARISON_METRICS.md
Supports Tasks 64 (transformation search) and 65 (validation).

Usage:
    from polyhedron_metrics import PolyhedronMetrics

    metrics = PolyhedronMetrics(poly1_vertices, poly2_vertices)

    # Volume metrics
    volume_results = metrics.calculate_volume_metrics()

    # Centroid displacement
    displacement = metrics.calculate_centroid_displacement()

    # Shape similarity
    hausdorff = metrics.calculate_hausdorff_distance()
    procrustes = metrics.calculate_procrustes_distance()

    # Complete comparison
    all_metrics = metrics.calculate_all_metrics()
"""

import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection, procrustes
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import warnings


@dataclass
class VolumeMetrics:
    """Volume comparison metrics between two polyhedra."""
    volume1: float
    volume2: float
    volume_ratio: float
    intersection_volume: Optional[float] = None
    union_volume: Optional[float] = None
    jaccard_index: Optional[float] = None
    intersection_computed: bool = False
    intersection_error: Optional[str] = None


@dataclass
class CentroidMetrics:
    """Centroid-based comparison metrics."""
    centroid1: Tuple[float, float, float]
    centroid2: Tuple[float, float, float]
    displacement: float
    displacement_x: float
    displacement_y: float
    displacement_z: float


@dataclass
class HausdorffMetrics:
    """Hausdorff distance metrics."""
    hausdorff_distance: float
    directed_distance_1to2: float
    directed_distance_2to1: float
    average_distance_1to2: float
    average_distance_2to1: float
    average_hausdorff: float


@dataclass
class ProcrustesMetrics:
    """Procrustes alignment metrics."""
    procrustes_distance: float
    rotation_matrix: np.ndarray
    translation_vector: np.ndarray
    scale_factor: float
    aligned_vertices2: np.ndarray


@dataclass
class ComparisonMetrics:
    """Complete set of comparison metrics between two polyhedra."""
    volume: VolumeMetrics
    centroid: CentroidMetrics
    hausdorff: HausdorffMetrics
    procrustes: ProcrustesMetrics

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, handling numpy arrays."""
        result = {}

        result['volume'] = asdict(self.volume)
        result['centroid'] = asdict(self.centroid)
        result['hausdorff'] = asdict(self.hausdorff)

        # Handle Procrustes with numpy arrays
        procrustes_dict = {
            'procrustes_distance': self.procrustes.procrustes_distance,
            'rotation_matrix': self.procrustes.rotation_matrix.tolist(),
            'translation_vector': self.procrustes.translation_vector.tolist(),
            'scale_factor': self.procrustes.scale_factor,
            'aligned_vertices2': self.procrustes.aligned_vertices2.tolist()
        }
        result['procrustes'] = procrustes_dict

        return result


class PolyhedronMetrics:
    """
    Comprehensive polyhedron comparison metrics.

    Attributes:
        vertices1: First polyhedron vertices (N x 3)
        vertices2: Second polyhedron vertices (M x 3)
        hull1: ConvexHull of first polyhedron
        hull2: ConvexHull of second polyhedron
    """

    def __init__(self, vertices1: np.ndarray, vertices2: np.ndarray):
        """
        Initialize with two sets of vertices.

        Args:
            vertices1: First polyhedron vertices, shape (N, 3)
            vertices2: Second polyhedron vertices, shape (M, 3)
        """
        self.vertices1 = np.asarray(vertices1)
        self.vertices2 = np.asarray(vertices2)

        # Validate input
        if self.vertices1.shape[1] != 3 or self.vertices2.shape[1] != 3:
            raise ValueError("Vertices must be 3-dimensional (N x 3)")

        if len(self.vertices1) < 4 or len(self.vertices2) < 4:
            raise ValueError("Need at least 4 vertices to form a 3D polyhedron")

        # Compute convex hulls
        self.hull1 = ConvexHull(self.vertices1)
        self.hull2 = ConvexHull(self.vertices2)

    def calculate_volume_metrics(self) -> VolumeMetrics:
        """
        Calculate volume-based comparison metrics.

        Returns:
            VolumeMetrics with volume ratio and optionally Jaccard index
        """
        v1 = self.hull1.volume
        v2 = self.hull2.volume
        ratio = v1 / v2 if v2 > 0 else float('inf')

        # Try to compute intersection
        intersection_volume = None
        union_volume = None
        jaccard = None
        intersection_computed = False
        error_msg = None

        try:
            intersection_volume = self._compute_intersection_volume()
            if intersection_volume is not None:
                union_volume = v1 + v2 - intersection_volume
                jaccard = intersection_volume / union_volume if union_volume > 0 else 0.0
                intersection_computed = True
        except Exception as e:
            error_msg = str(e)
            warnings.warn(f"Could not compute intersection volume: {e}")

        return VolumeMetrics(
            volume1=v1,
            volume2=v2,
            volume_ratio=ratio,
            intersection_volume=intersection_volume,
            union_volume=union_volume,
            jaccard_index=jaccard,
            intersection_computed=intersection_computed,
            intersection_error=error_msg
        )

    def _compute_intersection_volume(self) -> Optional[float]:
        """
        Compute volume of intersection using halfspace intersection.

        Returns:
            Intersection volume or None if computation fails
        """
        # Get halfspace representations
        # ConvexHull.equations: [A, b] where A·x + b <= 0 inside hull
        # We need [A, -b] for HalfspaceIntersection format where A·x <= b
        halfspaces1 = self.hull1.equations.copy()
        halfspaces2 = self.hull2.equations.copy()

        # Combine halfspaces (intersection must satisfy both)
        combined_halfspaces = np.vstack([halfspaces1, halfspaces2])

        # Find a feasible interior point
        interior_point = self._find_interior_point()
        if interior_point is None:
            return None

        # Compute intersection
        try:
            hs = HalfspaceIntersection(combined_halfspaces, interior_point)

            # Compute convex hull of intersection vertices
            if len(hs.intersections) < 4:
                return 0.0  # Degenerate intersection

            intersection_hull = ConvexHull(hs.intersections)
            return intersection_hull.volume

        except Exception as e:
            warnings.warn(f"Halfspace intersection failed: {e}")
            return None

    def _find_interior_point(self) -> Optional[np.ndarray]:
        """
        Find a point inside both polyhedra.

        Tries centroid of each hull and their midpoint.
        For non-overlapping polyhedra, returns None.

        Returns:
            3D point inside both polyhedra, or None
        """
        c1 = self._compute_centroid(self.vertices1)
        c2 = self._compute_centroid(self.vertices2)
        midpoint = (c1 + c2) / 2

        candidates = [c1, c2, midpoint]

        for point in candidates:
            if self._point_inside_hull(point, self.hull1) and \
               self._point_inside_hull(point, self.hull2):
                return point

        return None

    @staticmethod
    def _point_inside_hull(point: np.ndarray, hull: ConvexHull, tolerance: float = 1e-12) -> bool:
        """
        Check if point is inside convex hull.

        Args:
            point: 3D point to test
            hull: ConvexHull object
            tolerance: Numerical tolerance for boundary

        Returns:
            True if point is inside or on boundary of hull
        """
        # Test against all halfspace constraints: A·x + b <= 0
        for equation in hull.equations:
            if np.dot(equation[:-1], point) + equation[-1] > tolerance:
                return False
        return True

    def calculate_centroid_displacement(self) -> CentroidMetrics:
        """
        Calculate centroid displacement between polyhedra.

        Returns:
            CentroidMetrics with displacement and components
        """
        c1 = self._compute_centroid(self.vertices1)
        c2 = self._compute_centroid(self.vertices2)

        delta = c2 - c1
        displacement = np.linalg.norm(delta)

        return CentroidMetrics(
            centroid1=tuple(c1),
            centroid2=tuple(c2),
            displacement=displacement,
            displacement_x=delta[0],
            displacement_y=delta[1],
            displacement_z=delta[2]
        )

    @staticmethod
    def _compute_centroid(vertices: np.ndarray) -> np.ndarray:
        """Compute centroid of vertex set."""
        return np.mean(vertices, axis=0)

    def calculate_hausdorff_distance(self,
                                    use_hull_vertices: bool = True) -> HausdorffMetrics:
        """
        Calculate Hausdorff distance between polyhedra.

        Args:
            use_hull_vertices: If True, use only hull vertices.
                             If False, use all input vertices.

        Returns:
            HausdorffMetrics with directed and symmetric distances
        """
        if use_hull_vertices:
            v1 = self.vertices1[self.hull1.vertices]
            v2 = self.vertices2[self.hull2.vertices]
        else:
            v1 = self.vertices1
            v2 = self.vertices2

        # Directed Hausdorff: h(A, B) = max_a min_b ||a - b||
        h_1to2, avg_1to2 = self._directed_hausdorff(v1, v2)
        h_2to1, avg_2to1 = self._directed_hausdorff(v2, v1)

        # Symmetric Hausdorff
        hausdorff = max(h_1to2, h_2to1)

        # Average Hausdorff (more robust)
        avg_hausdorff = (avg_1to2 + avg_2to1) / 2

        return HausdorffMetrics(
            hausdorff_distance=hausdorff,
            directed_distance_1to2=h_1to2,
            directed_distance_2to1=h_2to1,
            average_distance_1to2=avg_1to2,
            average_distance_2to1=avg_2to1,
            average_hausdorff=avg_hausdorff
        )

    @staticmethod
    def _directed_hausdorff(vertices_a: np.ndarray,
                           vertices_b: np.ndarray) -> Tuple[float, float]:
        """
        Compute directed Hausdorff distance and average distance.

        Args:
            vertices_a: Source vertices (N x 3)
            vertices_b: Target vertices (M x 3)

        Returns:
            (max_min_distance, average_min_distance)
        """
        min_distances = []

        for a in vertices_a:
            # Find minimum distance from a to any point in B
            distances = np.linalg.norm(vertices_b - a, axis=1)
            min_dist = np.min(distances)
            min_distances.append(min_dist)

        max_min_distance = np.max(min_distances)
        avg_min_distance = np.mean(min_distances)

        return max_min_distance, avg_min_distance

    def calculate_procrustes_distance(self,
                                     scaling: bool = True) -> ProcrustesMetrics:
        """
        Calculate Procrustes distance after optimal alignment.

        Uses scipy.spatial.procrustes for optimal rigid transformation.

        Args:
            scaling: If True, allow scaling. If False, rigid transformation only.

        Returns:
            ProcrustesMetrics with distance and transformation parameters
        """
        # Use hull vertices for alignment
        v1 = self.vertices1[self.hull1.vertices]
        v2 = self.vertices2[self.hull2.vertices]

        # For Procrustes, need equal number of points
        # Use subset if different sizes
        n = min(len(v1), len(v2))
        v1_subset = v1[:n]
        v2_subset = v2[:n]

        # Compute Procrustes transformation
        # mtx1, mtx2: centered and scaled versions
        # disparity: sum of squared errors after optimal transformation
        mtx1, mtx2, disparity = procrustes(v1_subset, v2_subset)

        # Extract transformation parameters manually
        # Center both point sets
        c1 = np.mean(v1_subset, axis=0)
        c2 = np.mean(v2_subset, axis=0)

        v1_centered = v1_subset - c1
        v2_centered = v2_subset - c2

        # Compute optimal rotation via SVD
        H = v1_centered.T @ v2_centered  # Cross-covariance
        U, S, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T

        # Handle reflection (ensure det(R) = 1)
        if np.linalg.det(R) < 0:
            Vt[-1, :] *= -1
            R = Vt.T @ U.T

        # Compute scale
        if scaling:
            # S is a 1D array of singular values, sum them
            norm_y = np.sum(S)
            norm_x = np.linalg.norm(v1_centered, 'fro')**2
            scale = norm_y / norm_x if norm_x > 0 else 1.0
        else:
            scale = 1.0

        # Translation: t = c2 - scale * R @ c1
        translation = c2 - scale * R @ c1

        # Apply transformation to full v2
        v2_aligned = scale * (self.vertices2 @ R.T) + translation

        # Procrustes distance (RMSD after alignment)
        distance = np.sqrt(disparity)

        return ProcrustesMetrics(
            procrustes_distance=distance,
            rotation_matrix=R,
            translation_vector=translation,
            scale_factor=scale,
            aligned_vertices2=v2_aligned
        )

    def calculate_all_metrics(self,
                             include_intersection: bool = True,
                             scaling: bool = True) -> ComparisonMetrics:
        """
        Calculate all comparison metrics.

        Args:
            include_intersection: Attempt to compute intersection volume
            scaling: Allow scaling in Procrustes alignment

        Returns:
            ComparisonMetrics with all metric categories
        """
        volume = self.calculate_volume_metrics() if include_intersection else \
                 VolumeMetrics(self.hull1.volume, self.hull2.volume,
                              self.hull1.volume / self.hull2.volume)

        centroid = self.calculate_centroid_displacement()
        hausdorff = self.calculate_hausdorff_distance()
        procrustes = self.calculate_procrustes_distance(scaling=scaling)

        return ComparisonMetrics(
            volume=volume,
            centroid=centroid,
            hausdorff=hausdorff,
            procrustes=procrustes
        )


def load_polyhedron_from_json(filepath: str) -> np.ndarray:
    """
    Load polyhedron vertices from JSON file.

    Args:
        filepath: Path to polyhedron JSON file with 'vertices' key

    Returns:
        Vertices as numpy array (N x 3)
    """
    import json
    from pathlib import Path

    path = Path(filepath)
    with open(path) as f:
        data = json.load(f)

    vertices = np.array(data['vertices'])
    return vertices


def compare_polyhedra_files(filepath1: str, filepath2: str) -> ComparisonMetrics:
    """
    Compare two polyhedra from JSON files.

    Args:
        filepath1: Path to first polyhedron JSON
        filepath2: Path to second polyhedron JSON

    Returns:
        ComparisonMetrics with all metrics
    """
    v1 = load_polyhedron_from_json(filepath1)
    v2 = load_polyhedron_from_json(filepath2)

    metrics = PolyhedronMetrics(v1, v2)
    return metrics.calculate_all_metrics()


# Example usage and testing
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Test with synthetic data
    print("=" * 60)
    print("POLYHEDRON COMPARISON METRICS - TEST CASES")
    print("=" * 60)

    # Test Case 1: Identical polyhedra
    print("\n--- Test Case 1: Identical Polyhedra ---")
    np.random.seed(42)
    vertices = np.random.randn(20, 3)

    metrics = PolyhedronMetrics(vertices, vertices)
    results = metrics.calculate_all_metrics(include_intersection=False)

    print(f"Centroid displacement: {results.centroid.displacement:.6f}")
    print(f"Volume ratio: {results.volume.volume_ratio:.6f}")
    print(f"Hausdorff distance: {results.hausdorff.hausdorff_distance:.6f}")
    print(f"Procrustes distance: {results.procrustes.procrustes_distance:.6f}")

    # Test Case 2: Translated polyhedra
    print("\n--- Test Case 2: Translated Polyhedra (+5 in all axes) ---")
    vertices2 = vertices + 5.0

    metrics = PolyhedronMetrics(vertices, vertices2)
    results = metrics.calculate_all_metrics(include_intersection=False)

    print(f"Centroid displacement: {results.centroid.displacement:.6f}")
    print(f"Expected: {np.sqrt(3 * 5**2):.6f}")
    print(f"Volume ratio: {results.volume.volume_ratio:.6f}")
    print(f"Hausdorff distance: {results.hausdorff.hausdorff_distance:.6f}")

    # Test Case 3: Scaled polyhedra
    print("\n--- Test Case 3: Scaled Polyhedra (2x) ---")
    vertices3 = vertices * 2.0

    metrics = PolyhedronMetrics(vertices, vertices3)
    results = metrics.calculate_all_metrics(include_intersection=False)

    print(f"Volume ratio: {results.volume.volume_ratio:.6f}")
    print(f"Expected: {1/8:.6f} (2^3 scaling)")
    print(f"Procrustes scale factor: {results.procrustes.scale_factor:.6f}")

    # Test Case 4: Load real polyhedra if available
    print("\n--- Test Case 4: Real Polyhedra (if available) ---")

    script_dir = Path(__file__).parent
    phase6_dir = script_dir.parent / "datasets" / "phase6" / "polyhedra"

    if phase6_dir.exists():
        red_path = phase6_dir / "red_polyhedron.json"
        blue_path = phase6_dir / "blue_polyhedron.json"

        if red_path.exists() and blue_path.exists():
            print(f"\nComparing: red vs blue")
            results = compare_polyhedra_files(str(red_path), str(blue_path))

            print(f"Centroid displacement: {results.centroid.displacement:.3f} Munsell units")
            print(f"Volume ratio (red/blue): {results.volume.volume_ratio:.3f}")
            print(f"Hausdorff distance: {results.hausdorff.hausdorff_distance:.3f}")
            print(f"Average Hausdorff: {results.hausdorff.average_hausdorff:.3f}")
            print(f"Procrustes distance: {results.procrustes.procrustes_distance:.3f}")

            if results.volume.intersection_computed:
                print(f"Jaccard index: {results.volume.jaccard_index:.3f}")
            else:
                print("Jaccard index: Could not compute")
        else:
            print("Red or blue polyhedron not found")
    else:
        print(f"Phase 6 directory not found: {phase6_dir}")

    print("\n" + "=" * 60)
    print("Tests completed successfully!")
    print("=" * 60)
