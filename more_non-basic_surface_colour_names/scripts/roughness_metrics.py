#!/usr/bin/env python3
"""
Roughness and noise metrics for polyhedra analysis.

This module implements various metrics for assessing the roughness and noise
characteristics of 3D polyhedra constructed from point clouds, particularly
for color family boundary analysis.

Functions:
    surface_to_volume_ratio: Calculate normalized S/V roughness metric
    compute_alpha_shape: Construct alpha shape with parameter alpha
    hull_comparison_ratio: Compare alpha shape to convex hull volume
    calculate_fractal_dimension: Box-counting fractal dimension
    outlier_detection: Robust outlier detection using MAD or IQR
    analyze_outlier_sensitivity: Sensitivity analysis across thresholds
"""

import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial.distance import pdist, squareform
from typing import Tuple, List, Dict, Optional, Literal
import warnings


def surface_to_volume_ratio(points: np.ndarray) -> Dict[str, float]:
    """
    Calculate surface-to-volume ratio as roughness indicator.

    Computes normalized roughness metric R = S / V^(2/3) where S is surface
    area and V is volume. Theoretical minimum for sphere is 4.84.

    Args:
        points: Nx3 array of 3D coordinates

    Returns:
        Dictionary containing:
            - surface_area: total surface area
            - volume: total volume
            - ratio: normalized S/V^(2/3) roughness metric
            - sphere_ratio: theoretical minimum (4.84)
            - excess_roughness: (ratio - 4.84) / 4.84, percentage above sphere

    Raises:
        ValueError: If points has fewer than 4 points or wrong shape

    Example:
        >>> points = np.random.randn(100, 3)
        >>> metrics = surface_to_volume_ratio(points)
        >>> print(f"Roughness: {metrics['ratio']:.2f}")
    """
    if points.shape[0] < 4:
        raise ValueError("Need at least 4 points for convex hull")
    if points.shape[1] != 3:
        raise ValueError(f"Expected 3D points, got shape {points.shape}")

    hull = ConvexHull(points)
    surface_area = hull.area
    volume = hull.volume

    # Avoid division by zero for degenerate cases
    if volume < 1e-10:
        return {
            'surface_area': surface_area,
            'volume': volume,
            'ratio': np.inf,
            'sphere_ratio': 4.84,
            'excess_roughness': np.inf
        }

    # Normalized ratio: S / V^(2/3)
    ratio = surface_area / (volume ** (2/3))

    # Theoretical minimum for sphere: 4π r² / (4/3 π r³)^(2/3) = 4.835975...
    sphere_ratio = 4.835975254989877

    # Percentage excess over theoretical minimum
    excess_roughness = (ratio - sphere_ratio) / sphere_ratio

    return {
        'surface_area': float(surface_area),
        'volume': float(volume),
        'ratio': float(ratio),
        'sphere_ratio': sphere_ratio,
        'excess_roughness': float(excess_roughness)
    }


def compute_alpha_shape(points: np.ndarray, alpha: float) -> Dict[str, any]:
    """
    Compute alpha shape for given parameter alpha.

    Alpha shapes generalize convex hulls by allowing concavities at scale 1/alpha.
    Uses Delaunay triangulation and edge/face filtering based on circumradius.

    Args:
        points: Nx3 array of 3D coordinates
        alpha: Shape parameter (0 = convex hull, larger = more concave)

    Returns:
        Dictionary containing:
            - vertices: Mx3 array of shape vertices
            - simplices: Kx4 array of tetrahedron indices
            - volume: total volume
            - surface_area: total surface area (approximate)
            - num_vertices: number of vertices
            - num_simplices: number of tetrahedra

    Raises:
        ValueError: If alpha < 0 or points invalid

    Note:
        This is a simplified implementation. For production use, consider
        libraries like alphashape or CGAL for more robust alpha shape
        computation with proper boundary extraction.

    Example:
        >>> points = np.random.randn(100, 3)
        >>> shape = compute_alpha_shape(points, alpha=1.0)
        >>> print(f"Volume: {shape['volume']:.2f}")
    """
    if alpha < 0:
        raise ValueError("Alpha must be non-negative")
    if points.shape[0] < 4:
        raise ValueError("Need at least 4 points")
    if points.shape[1] != 3:
        raise ValueError(f"Expected 3D points, got shape {points.shape}")

    # Alpha = 0 is just the convex hull
    if alpha == 0:
        hull = ConvexHull(points)
        return {
            'vertices': points[np.unique(hull.simplices)],
            'simplices': hull.simplices,
            'volume': float(hull.volume),
            'surface_area': float(hull.area),
            'num_vertices': len(np.unique(hull.simplices)),
            'num_simplices': len(hull.simplices)
        }

    # Compute Delaunay triangulation
    tri = Delaunay(points)

    # Filter tetrahedra based on circumradius
    # Circumradius test: keep tetrahedron if circumradius < 1/alpha
    threshold = 1.0 / alpha if alpha > 0 else np.inf

    valid_simplices = []
    for simplex in tri.simplices:
        # Get the 4 vertices of this tetrahedron
        verts = points[simplex]

        # Calculate circumradius using formula for tetrahedron
        # This is approximate - proper calculation requires matrix operations
        # For simplicity, use maximum edge length as upper bound
        edges = pdist(verts)
        max_edge = np.max(edges)

        # Approximation: circumradius ≈ max_edge * factor
        # For regular tetrahedron, circumradius = edge_length * sqrt(6)/4 ≈ 0.612 * edge
        # Use conservative estimate
        approx_circumradius = max_edge * 0.7

        if approx_circumradius <= threshold:
            valid_simplices.append(simplex)

    if len(valid_simplices) == 0:
        # No simplices pass the test - return degenerate shape
        return {
            'vertices': points,
            'simplices': np.array([]),
            'volume': 0.0,
            'surface_area': 0.0,
            'num_vertices': len(points),
            'num_simplices': 0
        }

    valid_simplices = np.array(valid_simplices)

    # Calculate volume as sum of tetrahedron volumes
    total_volume = 0.0
    for simplex in valid_simplices:
        verts = points[simplex]
        # Volume of tetrahedron: |det(v1-v0, v2-v0, v3-v0)| / 6
        v0, v1, v2, v3 = verts
        mat = np.array([v1 - v0, v2 - v0, v3 - v0])
        vol = abs(np.linalg.det(mat)) / 6.0
        total_volume += vol

    # Approximate surface area (this is rough - proper extraction needs boundary faces)
    # Use convex hull of included vertices as approximation
    included_vertices = np.unique(valid_simplices.flatten())
    if len(included_vertices) >= 4:
        surface_hull = ConvexHull(points[included_vertices])
        surface_area = surface_hull.area
    else:
        surface_area = 0.0

    return {
        'vertices': points[included_vertices],
        'simplices': valid_simplices,
        'volume': float(total_volume),
        'surface_area': float(surface_area),
        'num_vertices': len(included_vertices),
        'num_simplices': len(valid_simplices)
    }


def hull_comparison_ratio(
    points: np.ndarray,
    alpha: float
) -> Dict[str, float]:
    """
    Compare alpha shape volume to convex hull volume.

    Computes ratio V_alpha / V_hull to assess how much volume is lost
    when allowing concavities at scale 1/alpha.

    Args:
        points: Nx3 array of 3D coordinates
        alpha: Alpha shape parameter

    Returns:
        Dictionary containing:
            - hull_volume: convex hull volume
            - alpha_volume: alpha shape volume
            - ratio: V_alpha / V_hull
            - volume_lost: absolute volume difference
            - percent_lost: percentage volume reduction

    Example:
        >>> points = np.random.randn(100, 3)
        >>> ratio = hull_comparison_ratio(points, alpha=2.0)
        >>> print(f"Volume retained: {ratio['ratio']*100:.1f}%")
    """
    hull = ConvexHull(points)
    hull_volume = hull.volume

    alpha_shape = compute_alpha_shape(points, alpha)
    alpha_volume = alpha_shape['volume']

    # Handle degenerate cases
    if hull_volume < 1e-10:
        ratio = 0.0 if alpha_volume < 1e-10 else np.inf
        percent_lost = 0.0
    else:
        ratio = alpha_volume / hull_volume
        percent_lost = (1.0 - ratio) * 100.0

    volume_lost = hull_volume - alpha_volume

    return {
        'hull_volume': float(hull_volume),
        'alpha_volume': float(alpha_volume),
        'ratio': float(ratio),
        'volume_lost': float(volume_lost),
        'percent_lost': float(percent_lost)
    }


def calculate_fractal_dimension(
    points: np.ndarray,
    min_boxes: int = 5,
    max_boxes: int = 50,
    num_scales: int = 10
) -> Dict[str, any]:
    """
    Calculate box-counting fractal dimension.

    Uses box-counting method to estimate fractal dimension D from the
    scaling relationship N(s) ~ s^(-D) where N is number of occupied
    boxes at scale s.

    Args:
        points: Nx3 array of 3D coordinates
        min_boxes: Minimum number of boxes along each axis
        max_boxes: Maximum number of boxes along each axis
        num_scales: Number of different box sizes to test

    Returns:
        Dictionary containing:
            - dimension: estimated fractal dimension
            - r_squared: goodness of fit for linear regression
            - box_sizes: array of box sizes tested
            - box_counts: array of number of occupied boxes
            - slope: slope of log-log plot (negative of dimension)
            - intercept: y-intercept of fit

    Raises:
        ValueError: If points invalid or parameters out of range

    Example:
        >>> points = np.random.randn(100, 3)
        >>> result = calculate_fractal_dimension(points)
        >>> print(f"Fractal dimension: {result['dimension']:.3f}")
        >>> print(f"R²: {result['r_squared']:.3f}")
    """
    if points.shape[0] < 10:
        raise ValueError("Need at least 10 points for reliable fractal dimension")
    if points.shape[1] != 3:
        raise ValueError(f"Expected 3D points, got shape {points.shape}")
    if min_boxes < 2:
        raise ValueError("min_boxes must be at least 2")
    if max_boxes <= min_boxes:
        raise ValueError("max_boxes must be greater than min_boxes")

    # Get data bounds with small padding to avoid edge effects
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    ranges = maxs - mins

    # Add 1% padding
    mins -= ranges * 0.01
    maxs += ranges * 0.01
    ranges = maxs - mins

    # Test logarithmically spaced box sizes
    # Number of boxes along each axis
    box_counts_per_axis = np.logspace(
        np.log10(min_boxes),
        np.log10(max_boxes),
        num_scales
    )

    box_sizes = []
    box_counts = []

    for n_boxes in box_counts_per_axis:
        n_boxes = int(n_boxes)

        # Box size along each dimension
        box_size = ranges / n_boxes

        # Assign each point to a box
        box_indices = np.floor((points - mins) / box_size).astype(int)

        # Clamp to valid range (handle edge cases)
        box_indices = np.clip(box_indices, 0, n_boxes - 1)

        # Convert to unique box IDs
        # Use tuple conversion for set uniqueness
        unique_boxes = set(map(tuple, box_indices))

        # Store results
        box_sizes.append(np.mean(box_size))  # Average box size
        box_counts.append(len(unique_boxes))

    box_sizes = np.array(box_sizes)
    box_counts = np.array(box_counts)

    # Fit line to log-log plot: log(N) = -D * log(s) + c
    # So slope = -D
    log_sizes = np.log10(box_sizes)
    log_counts = np.log10(box_counts)

    # Linear regression
    coeffs = np.polyfit(log_sizes, log_counts, 1)
    slope = coeffs[0]
    intercept = coeffs[1]

    # Dimension is negative of slope
    dimension = -slope

    # Calculate R² to assess fit quality
    log_counts_fit = slope * log_sizes + intercept
    ss_res = np.sum((log_counts - log_counts_fit) ** 2)
    ss_tot = np.sum((log_counts - np.mean(log_counts)) ** 2)
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    return {
        'dimension': float(dimension),
        'r_squared': float(r_squared),
        'box_sizes': box_sizes.tolist(),
        'box_counts': box_counts.tolist(),
        'slope': float(slope),
        'intercept': float(intercept)
    }


def outlier_detection(
    points: np.ndarray,
    method: Literal['mad', 'iqr', 'mahalanobis', 'hull_peeling'] = 'mad',
    threshold: float = 3.5,
    coordinate_wise: bool = True
) -> Dict[str, any]:
    """
    Robust outlier detection using MAD, IQR, or other methods.

    Args:
        points: Nx3 array of 3D coordinates
        method: Detection method ('mad', 'iqr', 'mahalanobis', 'hull_peeling')
        threshold: Outlier threshold (interpretation depends on method)
            - mad: Modified z-score threshold (default 3.5)
            - iqr: IQR multiplier (default 1.5 for mild, 3.0 for extreme)
            - mahalanobis: Mahalanobis distance threshold
            - hull_peeling: Number of convex hull layers to remove
        coordinate_wise: If True, apply method to each coordinate separately
            and flag points that are outliers in ANY dimension (for mad/iqr only)

    Returns:
        Dictionary containing:
            - outlier_mask: Boolean array indicating outliers
            - outlier_indices: Array of outlier indices
            - outlier_scores: Outlier scores for each point
            - num_outliers: Number of outliers detected
            - outlier_percentage: Percentage of points flagged
            - method: Method used
            - threshold: Threshold used

    Example:
        >>> points = np.random.randn(100, 3)
        >>> # Add some outliers
        >>> points[0] = [10, 10, 10]
        >>> result = outlier_detection(points, method='mad')
        >>> print(f"Found {result['num_outliers']} outliers")
    """
    if points.shape[0] < 4:
        raise ValueError("Need at least 4 points for outlier detection")
    if points.shape[1] != 3:
        raise ValueError(f"Expected 3D points, got shape {points.shape}")

    n_points = points.shape[0]

    if method == 'mad':
        # Median Absolute Deviation method
        if coordinate_wise:
            outlier_mask = np.zeros(n_points, dtype=bool)
            scores = np.zeros(n_points)

            for dim in range(3):
                values = points[:, dim]
                median = np.median(values)
                mad = np.median(np.abs(values - median))

                # Avoid division by zero
                if mad < 1e-10:
                    continue

                # Modified z-score: 0.6745 is the constant to make MAD
                # consistent with standard deviation for normal distribution
                modified_z = 0.6745 * (values - median) / mad

                dim_outliers = np.abs(modified_z) > threshold
                outlier_mask |= dim_outliers
                scores = np.maximum(scores, np.abs(modified_z))
        else:
            # Multivariate MAD - use distance from median point
            median_point = np.median(points, axis=0)
            distances = np.linalg.norm(points - median_point, axis=1)
            mad = np.median(np.abs(distances - np.median(distances)))

            if mad < 1e-10:
                outlier_mask = np.zeros(n_points, dtype=bool)
                scores = distances
            else:
                modified_z = 0.6745 * (distances - np.median(distances)) / mad
                outlier_mask = np.abs(modified_z) > threshold
                scores = np.abs(modified_z)

    elif method == 'iqr':
        # Interquartile Range method
        if coordinate_wise:
            outlier_mask = np.zeros(n_points, dtype=bool)
            scores = np.zeros(n_points)

            for dim in range(3):
                values = points[:, dim]
                q1 = np.percentile(values, 25)
                q3 = np.percentile(values, 75)
                iqr = q3 - q1

                lower_fence = q1 - threshold * iqr
                upper_fence = q3 + threshold * iqr

                dim_outliers = (values < lower_fence) | (values > upper_fence)
                outlier_mask |= dim_outliers

                # Score is distance from nearest fence
                score = np.maximum(lower_fence - values, values - upper_fence)
                score = np.maximum(score, 0) / (iqr if iqr > 0 else 1.0)
                scores = np.maximum(scores, score)
        else:
            # Multivariate - use distance from median
            median_point = np.median(points, axis=0)
            distances = np.linalg.norm(points - median_point, axis=1)
            q1 = np.percentile(distances, 25)
            q3 = np.percentile(distances, 75)
            iqr = q3 - q1

            upper_fence = q3 + threshold * iqr
            outlier_mask = distances > upper_fence
            scores = distances / (iqr if iqr > 0 else 1.0)

    elif method == 'mahalanobis':
        # Mahalanobis distance
        mean = np.mean(points, axis=0)
        cov = np.cov(points.T)

        # Check for singular covariance matrix
        try:
            inv_cov = np.linalg.inv(cov)
        except np.linalg.LinAlgError:
            # Use pseudo-inverse for singular matrices
            inv_cov = np.linalg.pinv(cov)

        # Calculate Mahalanobis distance for each point
        diff = points - mean
        scores = np.sqrt(np.sum(diff @ inv_cov * diff, axis=1))
        outlier_mask = scores > threshold

    elif method == 'hull_peeling':
        # Convex hull peeling (onion peeling)
        # threshold interpreted as number of layers to remove
        n_layers = int(threshold)
        remaining_indices = np.arange(n_points)
        outlier_indices_set = set()
        scores = np.zeros(n_points)

        for layer in range(n_layers):
            if len(remaining_indices) < 4:
                break

            # Compute hull of remaining points
            try:
                hull = ConvexHull(points[remaining_indices])
                hull_vertices = hull.vertices

                # Flag vertices in this hull layer
                actual_indices = remaining_indices[hull_vertices]
                outlier_indices_set.update(actual_indices)
                scores[actual_indices] = n_layers - layer  # Outer layers get higher scores

                # Remove hull vertices for next iteration
                mask = np.ones(len(remaining_indices), dtype=bool)
                mask[hull_vertices] = False
                remaining_indices = remaining_indices[mask]
            except Exception:
                break

        outlier_mask = np.zeros(n_points, dtype=bool)
        if len(outlier_indices_set) > 0:
            outlier_mask[list(outlier_indices_set)] = True
    else:
        raise ValueError(f"Unknown method: {method}")

    outlier_indices = np.where(outlier_mask)[0]

    return {
        'outlier_mask': outlier_mask,
        'outlier_indices': outlier_indices.tolist(),
        'outlier_scores': scores.tolist(),
        'num_outliers': int(np.sum(outlier_mask)),
        'outlier_percentage': float(100.0 * np.sum(outlier_mask) / n_points),
        'method': method,
        'threshold': threshold
    }


def analyze_outlier_sensitivity(
    points: np.ndarray,
    thresholds: List[float] = [0.90, 0.95, 0.99],
    method: Literal['mad', 'iqr', 'mahalanobis'] = 'mad'
) -> Dict[str, any]:
    """
    Analyze how polyhedron properties change when outliers are removed.

    Iteratively removes top percentage of points by outlier score and tracks
    how volume, surface area, and centroid change. High sensitivity indicates
    outliers significantly influence the boundary.

    Args:
        points: Nx3 array of 3D coordinates
        thresholds: List of quantile thresholds for outlier removal
            (e.g., 0.95 means remove top 5% by outlier score)
        method: Outlier detection method

    Returns:
        Dictionary containing:
            - baseline: Metrics with all points
            - filtered_results: List of metrics at each threshold
            - sensitivity_scores: Relative changes in metrics
            - most_sensitive_metric: Which metric changed most

    Example:
        >>> points = np.random.randn(100, 3)
        >>> analysis = analyze_outlier_sensitivity(points, thresholds=[0.9, 0.95])
        >>> print(f"Volume sensitivity: {analysis['sensitivity_scores']['volume']}")
    """
    if points.shape[0] < 10:
        raise ValueError("Need at least 10 points for sensitivity analysis")

    # Compute baseline metrics with all points
    baseline = {
        'num_points': points.shape[0],
        **surface_to_volume_ratio(points),
        'centroid': np.mean(points, axis=0).tolist()
    }

    # Detect outliers and get scores
    outlier_result = outlier_detection(points, method=method, coordinate_wise=False)
    outlier_scores = np.array(outlier_result['outlier_scores'])

    filtered_results = []

    for threshold in sorted(thresholds):
        # Determine cutoff score for this quantile
        cutoff_score = np.percentile(outlier_scores, threshold * 100)

        # Keep points below cutoff
        keep_mask = outlier_scores <= cutoff_score
        filtered_points = points[keep_mask]

        if len(filtered_points) < 4:
            # Too few points remaining
            filtered_results.append({
                'threshold': threshold,
                'num_removed': int(np.sum(~keep_mask)),
                'percent_removed': float(100.0 * np.sum(~keep_mask) / len(points)),
                'metrics': None,
                'error': 'Too few points remaining'
            })
            continue

        # Compute metrics on filtered data
        try:
            metrics = {
                'num_points': len(filtered_points),
                **surface_to_volume_ratio(filtered_points),
                'centroid': np.mean(filtered_points, axis=0).tolist()
            }

            filtered_results.append({
                'threshold': threshold,
                'num_removed': int(np.sum(~keep_mask)),
                'percent_removed': float(100.0 * np.sum(~keep_mask) / len(points)),
                'metrics': metrics,
                'error': None
            })
        except Exception as e:
            filtered_results.append({
                'threshold': threshold,
                'num_removed': int(np.sum(~keep_mask)),
                'percent_removed': float(100.0 * np.sum(~keep_mask) / len(points)),
                'metrics': None,
                'error': str(e)
            })

    # Calculate sensitivity scores
    sensitivity_scores = {
        'volume': [],
        'surface_area': [],
        'ratio': [],
        'centroid_shift': []
    }

    for result in filtered_results:
        if result['metrics'] is None:
            continue

        metrics = result['metrics']

        # Relative changes
        vol_change = abs(metrics['volume'] - baseline['volume']) / baseline['volume']
        area_change = abs(metrics['surface_area'] - baseline['surface_area']) / baseline['surface_area']
        ratio_change = abs(metrics['ratio'] - baseline['ratio']) / baseline['ratio']

        # Centroid shift (Euclidean distance)
        centroid_shift = np.linalg.norm(
            np.array(metrics['centroid']) - np.array(baseline['centroid'])
        )

        sensitivity_scores['volume'].append(vol_change)
        sensitivity_scores['surface_area'].append(area_change)
        sensitivity_scores['ratio'].append(ratio_change)
        sensitivity_scores['centroid_shift'].append(centroid_shift)

    # Find most sensitive metric
    avg_sensitivities = {
        key: np.mean(values) if len(values) > 0 else 0.0
        for key, values in sensitivity_scores.items()
    }
    most_sensitive = max(avg_sensitivities.items(), key=lambda x: x[1])[0]

    return {
        'baseline': baseline,
        'filtered_results': filtered_results,
        'sensitivity_scores': {
            key: [float(v) for v in values]
            for key, values in sensitivity_scores.items()
        },
        'average_sensitivity': avg_sensitivities,
        'most_sensitive_metric': most_sensitive,
        'method': method
    }


# Example usage and testing
if __name__ == '__main__':
    import json

    # Load a sample polyhedron from Phase 6 data
    print("Testing roughness metrics on Phase 6 polyhedra...")

    # Generate synthetic test data for demonstration
    # (In practice, load from actual polyhedron JSON files)
    np.random.seed(42)

    # Simulate a color family point cloud
    # Start with a roughly ellipsoidal distribution
    n_points = 200
    points = np.random.randn(n_points, 3)
    points[:, 0] *= 2.0  # Stretch along first axis
    points[:, 1] *= 1.5

    # Add a few outliers
    points[-5:] += np.random.randn(5, 3) * 5.0

    print("\n=== Surface-to-Volume Ratio ===")
    sv_metrics = surface_to_volume_ratio(points)
    print(json.dumps(sv_metrics, indent=2))

    print("\n=== Alpha Shape Analysis ===")
    for alpha in [0, 0.5, 1.0, 2.0]:
        alpha_shape = compute_alpha_shape(points, alpha)
        print(f"Alpha={alpha}: Volume={alpha_shape['volume']:.2f}, "
              f"Vertices={alpha_shape['num_vertices']}")

    print("\n=== Hull Comparison ===")
    comparison = hull_comparison_ratio(points, alpha=1.0)
    print(json.dumps(comparison, indent=2))

    print("\n=== Fractal Dimension ===")
    fractal = calculate_fractal_dimension(points)
    print(f"Dimension: {fractal['dimension']:.3f}")
    print(f"R²: {fractal['r_squared']:.3f}")

    print("\n=== Outlier Detection (MAD) ===")
    outliers = outlier_detection(points, method='mad', threshold=3.5)
    print(f"Detected {outliers['num_outliers']} outliers "
          f"({outliers['outlier_percentage']:.1f}%)")

    print("\n=== Sensitivity Analysis ===")
    sensitivity = analyze_outlier_sensitivity(
        points,
        thresholds=[0.90, 0.95, 0.99],
        method='mad'
    )
    print(f"Most sensitive metric: {sensitivity['most_sensitive_metric']}")
    print(f"Average sensitivities: {json.dumps(sensitivity['average_sensitivity'], indent=2)}")

    print("\nAll tests completed successfully!")
