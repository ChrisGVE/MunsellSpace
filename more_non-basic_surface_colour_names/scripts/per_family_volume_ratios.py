#!/usr/bin/env python3
"""
Phase 5.2: Per-Family Position-Dependent Volume Ratio Analysis (Task 99)

Analyzes how the RGB→Munsell volume mapping varies for each color family's
polyhedron using Monte Carlo sampling within convex hulls.

Uses Jacobian determinant results from Task 98 to:
1. Sample points within each family's screen polyhedron
2. Compute average Jacobian within each hull
3. Calculate effective volume correction factors
4. Compare corrected vs uncorrected volume matching

Output: per_family_volume_ratios.json, per_family_volume_ratios.md
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from scipy.spatial import ConvexHull, Delaunay
import sys

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from color_transforms import rgb_to_munsell_cartesian


def load_jacobian_map(analysis_dir: Path) -> Dict:
    """Load the spatial Jacobian map from Task 98."""
    map_path = analysis_dir / "jacobian_map.json"
    if not map_path.exists():
        raise FileNotFoundError(f"Jacobian map not found: {map_path}")

    with open(map_path) as f:
        return json.load(f)


def load_polyhedra(polyhedra_dir: Path) -> Dict[str, Dict]:
    """Load screen polyhedra for all families."""
    families = {}

    for f in polyhedra_dir.glob("*_polyhedron.json"):
        name = f.stem.replace("_polyhedron", "")
        with open(f) as fp:
            data = json.load(fp)
            # Handle both 'vertices' and 'points' keys
            vertices_key = "vertices" if "vertices" in data else "points"
            vertices = np.array(data.get(vertices_key, []))

            if len(vertices) >= 4:  # Need at least 4 points for 3D hull
                families[name] = {
                    "vertices": vertices,
                    "sample_count": data.get("sample_count", len(vertices))
                }

    return families


def sample_in_convex_hull(vertices: np.ndarray, n_samples: int = 1000) -> np.ndarray:
    """
    Generate random points uniformly inside a convex hull using rejection sampling.

    Args:
        vertices: Vertices of the convex hull, shape (N, 3)
        n_samples: Number of samples to generate

    Returns:
        Points inside the hull, shape (n_samples, 3)
    """
    try:
        hull = ConvexHull(vertices)
        delaunay = Delaunay(vertices)
    except Exception as e:
        return np.array([])

    # Get bounding box
    min_coords = vertices.min(axis=0)
    max_coords = vertices.max(axis=0)

    samples = []
    attempts = 0
    max_attempts = n_samples * 100  # Prevent infinite loop

    while len(samples) < n_samples and attempts < max_attempts:
        # Generate batch of random points in bounding box
        batch_size = min(1000, (n_samples - len(samples)) * 10)
        random_points = np.random.uniform(min_coords, max_coords, (batch_size, 3))

        # Check which points are inside the hull
        inside = delaunay.find_simplex(random_points) >= 0
        samples.extend(random_points[inside])
        attempts += batch_size

    return np.array(samples[:n_samples])


def compute_jacobian_at_point(rgb: np.ndarray, epsilon: float = 1e-5) -> Optional[float]:
    """Compute Jacobian determinant at a single RGB point."""
    base_munsell = rgb_to_munsell_cartesian(rgb)
    if base_munsell is None:
        return None

    jacobian = np.zeros((3, 3))

    for j in range(3):
        rgb_plus = rgb.copy()
        rgb_minus = rgb.copy()

        rgb_plus[j] = min(rgb_plus[j] + epsilon, 1.0)
        rgb_minus[j] = max(rgb_minus[j] - epsilon, 0.0)

        munsell_plus = rgb_to_munsell_cartesian(rgb_plus)
        munsell_minus = rgb_to_munsell_cartesian(rgb_minus)

        if munsell_plus is None or munsell_minus is None:
            return None

        jacobian[:, j] = (munsell_plus - munsell_minus) / (rgb_plus[j] - rgb_minus[j])

    return abs(np.linalg.det(jacobian))


def analyze_family_jacobian(
    vertices: np.ndarray,
    n_samples: int = 1000,
    sample_vertices: bool = True
) -> Dict:
    """
    Analyze Jacobian distribution within a family's polyhedron.

    Args:
        vertices: Munsell Cartesian coordinates of polyhedron vertices
        n_samples: Number of Monte Carlo samples
        sample_vertices: If True, convert vertices back to RGB and sample

    Returns:
        Dictionary with statistics
    """
    # Note: vertices are in Munsell space, but we need to sample in RGB space
    # For this analysis, we approximate by sampling in the bounding box of the
    # original RGB colors that generated these vertices

    # Sample within the hull
    samples = sample_in_convex_hull(vertices, n_samples)

    if len(samples) < 10:
        return {
            "valid": False,
            "reason": "Insufficient samples in hull"
        }

    # For each sample point (assuming Munsell coords), estimate what the
    # RGB coordinate would be, then compute Jacobian there
    # This is a simplification - ideally we'd have the original RGB coords

    # Since vertices are in Munsell space and the Jacobian is RGB→Munsell,
    # we need to work with RGB input. For now, we approximate by using the
    # global Jacobian statistics since CV=0.02 shows uniformity.

    # Alternative approach: sample RGB space in the approximate region
    # For this, we use the rough inverse: Munsell→RGB (approximate)

    jacobians = []
    for point in samples:
        # Convert Munsell back to approximate RGB (rough estimate)
        # Using the approximate inverse from color_transforms
        from color_transforms import munsell_cartesian_to_rgb
        rgb = munsell_cartesian_to_rgb(point)

        if rgb is None:
            continue

        det_j = compute_jacobian_at_point(rgb)
        if det_j is not None and det_j > 0:
            jacobians.append(det_j)

    if len(jacobians) < 10:
        return {
            "valid": False,
            "reason": f"Only {len(jacobians)} valid Jacobian computations"
        }

    jacobians = np.array(jacobians)

    return {
        "valid": True,
        "n_samples": len(jacobians),
        "mean_det_j": float(np.mean(jacobians)),
        "std_det_j": float(np.std(jacobians)),
        "cv": float(np.std(jacobians) / np.mean(jacobians)) if np.mean(jacobians) > 0 else 0,
        "min_det_j": float(np.min(jacobians)),
        "max_det_j": float(np.max(jacobians)),
        "median_det_j": float(np.median(jacobians)),
    }


def main():
    print("=" * 70)
    print("Phase 5.2: Per-Family Volume Ratio Analysis (Task 99)")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent
    analysis_dir = base_dir / "datasets" / "transformation_analysis"
    screen_polyhedra_dir = base_dir / "datasets" / "screen_polyhedra" / "threshold_0.6"

    # Check if we have polyhedra from the correct source
    if not screen_polyhedra_dir.exists():
        # Try phase6 polyhedra
        screen_polyhedra_dir = base_dir / "datasets" / "phase6" / "polyhedra"

    if not screen_polyhedra_dir.exists():
        print(f"ERROR: No polyhedra directory found")
        return

    print(f"\nLoading polyhedra from: {screen_polyhedra_dir}")
    families = load_polyhedra(screen_polyhedra_dir)
    print(f"Loaded {len(families)} families with valid polyhedra")

    # Load global Jacobian stats for reference
    global_stats_path = analysis_dir / "jacobian_analysis.json"
    if global_stats_path.exists():
        with open(global_stats_path) as f:
            global_stats = json.load(f)
        global_mean = global_stats.get("mean_det_j", 2054.70)
        global_cv = global_stats.get("cv", 0.02)
        print(f"\nGlobal Jacobian: mean={global_mean:.2f}, CV={global_cv:.4f}")
    else:
        global_mean = 2054.70
        global_cv = 0.02
        print(f"\nUsing default global Jacobian: mean={global_mean:.2f}")

    # Analyze each family
    print(f"\nAnalyzing {len(families)} families (500 samples each)...")

    results = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "n_families": len(families),
            "samples_per_family": 500,
            "global_mean_det_j": global_mean,
            "global_cv": global_cv
        },
        "families": {}
    }

    for i, (family, data) in enumerate(sorted(families.items())):
        print(f"  [{i+1}/{len(families)}] {family}...", end=" ")

        stats = analyze_family_jacobian(data["vertices"], n_samples=500)

        if stats["valid"]:
            correction_factor = stats["mean_det_j"] / global_mean
            stats["correction_factor"] = correction_factor
            stats["deviation_from_global_pct"] = (correction_factor - 1) * 100
            print(f"mean={stats['mean_det_j']:.2f}, CV={stats['cv']:.4f}, correction={correction_factor:.4f}")
        else:
            print(f"SKIPPED: {stats.get('reason', 'unknown')}")

        results["families"][family] = stats

    # Summary statistics
    valid_families = {k: v for k, v in results["families"].items() if v["valid"]}

    if valid_families:
        corrections = [v["correction_factor"] for v in valid_families.values()]
        cvs = [v["cv"] for v in valid_families.values()]

        results["summary"] = {
            "valid_families": len(valid_families),
            "correction_factor_mean": float(np.mean(corrections)),
            "correction_factor_std": float(np.std(corrections)),
            "correction_factor_range": [float(np.min(corrections)), float(np.max(corrections))],
            "per_family_cv_mean": float(np.mean(cvs)),
            "per_family_cv_max": float(np.max(cvs)),
            "max_deviation_pct": float(max(abs(c - 1) * 100 for c in corrections)),
        }

        print(f"\n{'=' * 70}")
        print("SUMMARY")
        print(f"{'=' * 70}")
        print(f"Valid families analyzed: {len(valid_families)}")
        print(f"Correction factor: {results['summary']['correction_factor_mean']:.4f} ± {results['summary']['correction_factor_std']:.4f}")
        print(f"Range: [{results['summary']['correction_factor_range'][0]:.4f}, {results['summary']['correction_factor_range'][1]:.4f}]")
        print(f"Max deviation from global: {results['summary']['max_deviation_pct']:.2f}%")
        print(f"Per-family CV (mean): {results['summary']['per_family_cv_mean']:.4f}")

    # Save JSON
    output_json = analysis_dir / "per_family_volume_ratios.json"
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_json}")

    # Generate markdown report
    md_content = generate_markdown_report(results, global_mean, global_cv)
    output_md = analysis_dir / "per_family_volume_ratios.md"
    with open(output_md, "w") as f:
        f.write(md_content)
    print(f"Saved: {output_md}")

    print(f"\n{'=' * 70}")
    print("PER-FAMILY VOLUME RATIO ANALYSIS COMPLETE")
    print(f"{'=' * 70}")


def generate_markdown_report(results: Dict, global_mean: float, global_cv: float) -> str:
    """Generate markdown report of per-family volume ratios."""

    lines = [
        "# Per-Family Volume Ratio Analysis (Task 99)",
        "",
        f"Generated: {results['metadata']['generated'][:10]}",
        "",
        "## Overview",
        "",
        "This analysis examines how the RGB→Munsell volume mapping varies within each",
        "color family's polyhedron. Using Monte Carlo sampling within convex hulls,",
        "we compute per-family Jacobian statistics and correction factors.",
        "",
        "## Reference: Global Jacobian Statistics",
        "",
        f"From Task 98 analysis (3375 sample points across RGB space):",
        f"- Mean |det(J)|: {global_mean:.2f}",
        f"- CV (coefficient of variation): {global_cv:.4f}",
        "",
    ]

    if "summary" in results:
        s = results["summary"]
        lines.extend([
            "## Summary",
            "",
            f"- Valid families analyzed: {s['valid_families']}",
            f"- Mean correction factor: {s['correction_factor_mean']:.4f}",
            f"- Correction factor std: {s['correction_factor_std']:.4f}",
            f"- Range: [{s['correction_factor_range'][0]:.4f}, {s['correction_factor_range'][1]:.4f}]",
            f"- Max deviation from global: {s['max_deviation_pct']:.2f}%",
            "",
        ])

    # Per-family table
    lines.extend([
        "## Per-Family Results",
        "",
        "| Family | Mean |det(J)| | CV | Correction Factor | Deviation (%) |",
        "|--------|----------------|------|-------------------|---------------|",
    ])

    for family, stats in sorted(results["families"].items()):
        if stats["valid"]:
            lines.append(
                f"| {family} | {stats['mean_det_j']:.2f} | {stats['cv']:.4f} | "
                f"{stats['correction_factor']:.4f} | {stats['deviation_from_global_pct']:+.2f} |"
            )
        else:
            lines.append(f"| {family} | - | - | - | ({stats.get('reason', 'invalid')}) |")

    lines.extend([
        "",
        "## Implications",
        "",
        "1. **Correction factors near 1.0**: Volume mapping is uniform across families",
        "2. **Low per-family CV**: Jacobian is consistent within each polyhedron",
        "3. **Max deviation indicates**: Whether per-family corrections are needed",
        "",
        "## Recommendation",
        "",
    ])

    if "summary" in results:
        max_dev = results["summary"]["max_deviation_pct"]
        if max_dev < 5:
            lines.append("**No per-family correction needed**: Max deviation < 5%, use global scaling.")
        elif max_dev < 10:
            lines.append("**Optional per-family correction**: Moderate deviation (5-10%), may improve accuracy.")
        else:
            lines.append("**Per-family correction recommended**: Significant deviation > 10% detected.")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
