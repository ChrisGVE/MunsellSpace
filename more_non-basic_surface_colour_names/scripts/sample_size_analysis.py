#!/usr/bin/env python3
"""
Phase 5.2: Bootstrap Sample Size Analysis (Task 100)

Determines convex hull volume stability with respect to sample count
using bootstrap resampling.

For each color family:
1. Subsample N points from full point set (N ∈ {10, 20, 30, 50, 100, all})
2. Compute convex hull volume
3. Repeat 100 times (bootstrap)
4. Record mean and std of volume
5. Determine N_min where CV < 0.05 (5% stability threshold)

Output: sample_size_analysis.json, sample_size_analysis.md
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from scipy.spatial import ConvexHull
import warnings


def load_polyhedra_points(polyhedra_dir: Path) -> Dict[str, np.ndarray]:
    """Load point sets for all families (not just hull vertices)."""
    families = {}

    for f in polyhedra_dir.glob("*_polyhedron.json"):
        name = f.stem.replace("_polyhedron", "")
        with open(f) as fp:
            data = json.load(fp)

            # Try to get original points (not just hull vertices)
            # Different polyhedra may store this differently
            if "original_points" in data:
                points = np.array(data["original_points"])
            elif "points" in data:
                points = np.array(data["points"])
            elif "vertices" in data:
                points = np.array(data["vertices"])
            else:
                continue

            if len(points) >= 4:  # Minimum for 3D hull
                families[name] = points

    return families


def load_samples_from_csv(csv_path: Path) -> Dict[str, np.ndarray]:
    """
    Load original sample points from family_assignments_munsell.csv.

    Returns dict mapping family name to array of Munsell Cartesian coordinates.
    """
    import csv

    families = {}

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            family = row.get('assigned_family', '')
            if not family or family == 'assigned_family':
                continue

            try:
                x = float(row.get('cartesian_x', 0))
                y = float(row.get('cartesian_y', 0))
                z = float(row.get('cartesian_z', 0))

                # Skip invalid coordinates
                if x == 0 and y == 0 and z == 0:
                    continue

                if family not in families:
                    families[family] = []
                families[family].append([x, y, z])

            except (ValueError, TypeError):
                continue

    # Convert lists to numpy arrays
    return {k: np.array(v) for k, v in families.items() if len(v) >= 10}


def compute_hull_volume(points: np.ndarray) -> Optional[float]:
    """Compute convex hull volume, returns None if degenerate."""
    if len(points) < 4:
        return None

    try:
        # Check if points are coplanar (2D extent only)
        centered = points - points.mean(axis=0)
        U, S, Vt = np.linalg.svd(centered, full_matrices=False)

        # If smallest singular value is near zero, points are ~planar
        if S[-1] / S[0] < 1e-6:
            return None

        hull = ConvexHull(points)
        return hull.volume
    except Exception:
        return None


def bootstrap_volume_analysis(
    points: np.ndarray,
    sample_sizes: List[int],
    n_bootstrap: int = 100
) -> Dict[str, Dict]:
    """
    Perform bootstrap analysis of hull volume at different sample sizes.

    Args:
        points: Full point set, shape (N, 3)
        sample_sizes: List of sample sizes to test
        n_bootstrap: Number of bootstrap iterations

    Returns:
        Dictionary with statistics for each sample size
    """
    n_total = len(points)
    results = {}

    for n_samples in sample_sizes:
        if n_samples > n_total:
            continue

        volumes = []
        for _ in range(n_bootstrap):
            # Random subsample (without replacement for subsample, with for bootstrap)
            if n_samples == n_total:
                # Bootstrap: sample with replacement
                indices = np.random.choice(n_total, n_total, replace=True)
            else:
                # Subsample: sample without replacement
                indices = np.random.choice(n_total, n_samples, replace=False)

            sample_points = points[indices]
            vol = compute_hull_volume(sample_points)

            if vol is not None and vol > 0:
                volumes.append(vol)

        if len(volumes) >= 10:  # Need minimum samples for statistics
            volumes = np.array(volumes)
            mean_vol = float(np.mean(volumes))
            std_vol = float(np.std(volumes))
            cv = std_vol / mean_vol if mean_vol > 0 else float('inf')

            results[str(n_samples)] = {
                "n_samples": n_samples,
                "n_valid_bootstrap": len(volumes),
                "mean_volume": mean_vol,
                "std_volume": std_vol,
                "cv": cv,
                "ci_95_lower": float(mean_vol - 1.96 * std_vol),
                "ci_95_upper": float(mean_vol + 1.96 * std_vol),
                "stable": cv < 0.05
            }
        else:
            results[str(n_samples)] = {
                "n_samples": n_samples,
                "n_valid_bootstrap": len(volumes),
                "stable": False,
                "reason": "Insufficient valid bootstrap samples"
            }

    return results


def find_minimum_stable_n(results: Dict[str, Dict], threshold: float = 0.05) -> Optional[int]:
    """Find the minimum sample size where CV < threshold."""
    for n_str in sorted(results.keys(), key=lambda x: int(x)):
        if results[n_str].get("cv", float('inf')) < threshold:
            return int(n_str)
    return None


def main():
    print("=" * 70)
    print("Phase 5.2: Bootstrap Sample Size Analysis (Task 100)")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent
    analysis_dir = base_dir / "datasets" / "transformation_analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)

    # Prefer loading from CSV with full sample sets
    csv_path = base_dir / "datasets" / "phase6" / "family_assignments_munsell.csv"

    if csv_path.exists():
        print(f"\nLoading original samples from: {csv_path}")
        families = load_samples_from_csv(csv_path)
        print(f"Loaded {len(families)} families from CSV")
        total_samples = sum(len(v) for v in families.values())
        print(f"Total samples: {total_samples:,}")
    else:
        # Fallback to polyhedra (hull vertices only)
        polyhedra_dir = base_dir / "datasets" / "screen_polyhedra" / "threshold_0.6"
        if not polyhedra_dir.exists():
            polyhedra_dir = base_dir / "datasets" / "phase6" / "polyhedra"

        if not polyhedra_dir.exists():
            print(f"ERROR: No data source found")
            return

        print(f"\nLoading point sets from: {polyhedra_dir}")
        print("WARNING: Using hull vertices only (limited bootstrap accuracy)")
        families = load_polyhedra_points(polyhedra_dir)
        print(f"Loaded {len(families)} families")

    # Sample sizes to test
    sample_sizes = [10, 15, 20, 30, 50, 100, 200, 500]
    n_bootstrap = 100

    print(f"\nBootstrap settings:")
    print(f"  Sample sizes: {sample_sizes}")
    print(f"  Bootstrap iterations: {n_bootstrap}")
    print(f"  Stability threshold (CV): 0.05")

    # Analyze each family
    print(f"\nAnalyzing {len(families)} families...")

    results = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "n_families": len(families),
            "sample_sizes_tested": sample_sizes,
            "n_bootstrap": n_bootstrap,
            "stability_threshold_cv": 0.05
        },
        "families": {},
        "summary": {}
    }

    insufficient_families = []
    stable_families = []
    min_n_distribution = []

    for i, (family, points) in enumerate(sorted(families.items())):
        n_points = len(points)
        print(f"  [{i+1}/{len(families)}] {family} (n={n_points})...", end=" ")

        # Filter sample sizes based on available points
        valid_sizes = [s for s in sample_sizes if s <= n_points] + [n_points]
        valid_sizes = sorted(set(valid_sizes))

        analysis = bootstrap_volume_analysis(points, valid_sizes, n_bootstrap)

        # Find minimum stable N
        min_n = find_minimum_stable_n(analysis)

        family_result = {
            "n_points": n_points,
            "bootstrap_results": analysis,
            "min_stable_n": min_n,
            "is_stable_at_current_n": analysis.get(str(n_points), {}).get("stable", False)
        }

        if min_n is None:
            print(f"UNSTABLE at all sample sizes")
            family_result["status"] = "unstable"
            insufficient_families.append(family)
        elif min_n > n_points:
            print(f"INSUFFICIENT (needs N≥{min_n}, has {n_points})")
            family_result["status"] = "insufficient"
            insufficient_families.append(family)
        else:
            cv_at_n = analysis.get(str(n_points), {}).get("cv", 0)
            print(f"stable (min_N={min_n}, CV@{n_points}={cv_at_n:.4f})")
            family_result["status"] = "stable"
            stable_families.append(family)
            min_n_distribution.append(min_n)

        results["families"][family] = family_result

    # Summary statistics
    results["summary"] = {
        "stable_families": len(stable_families),
        "insufficient_families": len(insufficient_families),
        "insufficient_list": insufficient_families,
        "min_n_distribution": {
            "mean": float(np.mean(min_n_distribution)) if min_n_distribution else None,
            "median": float(np.median(min_n_distribution)) if min_n_distribution else None,
            "min": int(np.min(min_n_distribution)) if min_n_distribution else None,
            "max": int(np.max(min_n_distribution)) if min_n_distribution else None
        }
    }

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Stable families: {len(stable_families)}/{len(families)}")
    print(f"Insufficient families: {len(insufficient_families)}")

    if min_n_distribution:
        print(f"\nMinimum stable N distribution:")
        print(f"  Mean: {np.mean(min_n_distribution):.1f}")
        print(f"  Median: {np.median(min_n_distribution):.1f}")
        print(f"  Range: [{np.min(min_n_distribution)}, {np.max(min_n_distribution)}]")

    if insufficient_families:
        print(f"\nInsufficient families: {', '.join(insufficient_families)}")

    # Save results
    output_json = analysis_dir / "sample_size_analysis.json"
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_json}")

    # Generate markdown report
    md_content = generate_markdown_report(results)
    output_md = analysis_dir / "sample_size_analysis.md"
    with open(output_md, "w") as f:
        f.write(md_content)
    print(f"Saved: {output_md}")

    print(f"\n{'=' * 70}")
    print("BOOTSTRAP SAMPLE SIZE ANALYSIS COMPLETE")
    print(f"{'=' * 70}")


def generate_markdown_report(results: Dict) -> str:
    """Generate markdown report of sample size analysis."""

    lines = [
        "# Bootstrap Sample Size Analysis (Task 100)",
        "",
        f"Generated: {results['metadata']['generated'][:10]}",
        "",
        "## Overview",
        "",
        "This analysis determines the minimum sample size needed for stable",
        "convex hull volume estimation using bootstrap resampling.",
        "",
        f"- Sample sizes tested: {results['metadata']['sample_sizes_tested']}",
        f"- Bootstrap iterations: {results['metadata']['n_bootstrap']}",
        f"- Stability threshold: CV < {results['metadata']['stability_threshold_cv']}",
        "",
        "## Summary",
        "",
        f"- Stable families: {results['summary']['stable_families']}/{results['metadata']['n_families']}",
        f"- Insufficient families: {results['summary']['insufficient_families']}",
        "",
    ]

    if results['summary'].get('min_n_distribution', {}).get('mean'):
        dist = results['summary']['min_n_distribution']
        lines.extend([
            "### Minimum Stable Sample Size Distribution",
            "",
            f"- Mean: {dist['mean']:.1f}",
            f"- Median: {dist['median']:.1f}",
            f"- Range: [{dist['min']}, {dist['max']}]",
            "",
        ])

    if results['summary']['insufficient_list']:
        lines.extend([
            "### Insufficient Families",
            "",
            "These families have fewer samples than needed for stable volume estimation:",
            "",
        ])
        for fam in results['summary']['insufficient_list']:
            fam_data = results['families'][fam]
            lines.append(f"- **{fam}**: n={fam_data['n_points']}, min_stable={fam_data.get('min_stable_n', 'N/A')}")
        lines.append("")

    # Per-family table (summary)
    lines.extend([
        "## Per-Family Results",
        "",
        "| Family | N Points | Min Stable N | CV @ N | Status |",
        "|--------|----------|--------------|--------|--------|",
    ])

    for family, data in sorted(results["families"].items()):
        n_points = data['n_points']
        min_n = data.get('min_stable_n', '-')
        bootstrap = data.get('bootstrap_results', {})
        cv_at_n = bootstrap.get(str(n_points), {}).get('cv', '-')
        if isinstance(cv_at_n, float):
            cv_at_n = f"{cv_at_n:.4f}"
        status = data.get('status', 'unknown')

        lines.append(f"| {family} | {n_points} | {min_n} | {cv_at_n} | {status} |")

    lines.extend([
        "",
        "## Implications",
        "",
        "1. **Stability threshold (CV < 0.05)**: Ensures volume estimates vary < 5%",
        "2. **Minimum N recommendations**: Use median as guideline for new families",
        "3. **Insufficient families**: May need more samples or alternative methods",
        "",
        "## Recommendations",
        "",
    ])

    stable_pct = results['summary']['stable_families'] / results['metadata']['n_families'] * 100
    if stable_pct >= 90:
        lines.append("**Excellent stability**: >90% of families have sufficient samples.")
    elif stable_pct >= 70:
        lines.append("**Good stability**: 70-90% of families stable. Consider augmenting insufficient families.")
    else:
        lines.append("**Stability concerns**: <70% families stable. Sample augmentation recommended.")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
