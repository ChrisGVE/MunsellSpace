#!/usr/bin/env python3
"""
Phase 5.2: Jacobian Analysis for RGB↔Munsell Volume Distortion

Compute the Jacobian determinant across color space to understand how
volume transforms between RGB and Munsell spaces.

Key insight: |det(J)| represents local volume scaling factor.
- |det(J)| > 1: RGB volumes expand in Munsell
- |det(J)| < 1: RGB volumes contract in Munsell
- |det(J)| varies spatially: non-uniform volume mapping
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import sys

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent))
from color_transforms import rgb_to_munsell_cartesian

BASE_DIR = Path(__file__).parent.parent


@dataclass
class JacobianPoint:
    """A point with Jacobian information."""
    rgb: Tuple[float, float, float]
    munsell: Optional[Tuple[float, float, float]]
    jacobian_det: Optional[float]
    jacobian_matrix: Optional[List[List[float]]]
    valid: bool


def compute_jacobian_numerical(rgb: np.ndarray, epsilon: float = 1e-5) -> Tuple[Optional[np.ndarray], Optional[float]]:
    """
    Compute Jacobian matrix and determinant numerically via finite differences.

    J_ij = ∂f_i/∂x_j ≈ [f_i(x + ε·e_j) - f_i(x)] / ε

    Args:
        rgb: RGB coordinates [0, 1]^3
        epsilon: Finite difference step size

    Returns:
        (jacobian_matrix, determinant) or (None, None) if invalid
    """
    # Get base Munsell coordinates
    base_munsell = rgb_to_munsell_cartesian(rgb)
    if base_munsell is None:
        return None, None

    jacobian = np.zeros((3, 3))

    for j in range(3):  # For each input dimension (R, G, B)
        # Perturbed point
        rgb_plus = rgb.copy()
        rgb_plus[j] = min(1.0, rgb[j] + epsilon)

        rgb_minus = rgb.copy()
        rgb_minus[j] = max(0.0, rgb[j] - epsilon)

        # Get Munsell at perturbed points
        munsell_plus = rgb_to_munsell_cartesian(rgb_plus)
        munsell_minus = rgb_to_munsell_cartesian(rgb_minus)

        if munsell_plus is None or munsell_minus is None:
            # Use one-sided difference if boundary
            if munsell_plus is not None:
                for i in range(3):
                    jacobian[i, j] = (munsell_plus[i] - base_munsell[i]) / epsilon
            elif munsell_minus is not None:
                for i in range(3):
                    jacobian[i, j] = (base_munsell[i] - munsell_minus[i]) / epsilon
            else:
                return None, None
        else:
            # Central difference
            h = rgb_plus[j] - rgb_minus[j]
            for i in range(3):
                jacobian[i, j] = (munsell_plus[i] - munsell_minus[i]) / h

    det = np.linalg.det(jacobian)
    return jacobian, det


def sample_color_space(resolution: int = 20) -> List[JacobianPoint]:
    """
    Sample color space on a regular 3D grid and compute Jacobian at each point.

    Args:
        resolution: Grid points per dimension

    Returns:
        List of JacobianPoint results
    """
    results = []
    total = resolution ** 3

    for i, r in enumerate(np.linspace(0.05, 0.95, resolution)):
        for j, g in enumerate(np.linspace(0.05, 0.95, resolution)):
            for k, b in enumerate(np.linspace(0.05, 0.95, resolution)):
                rgb = np.array([r, g, b])

                # Get Munsell coordinates
                munsell = rgb_to_munsell_cartesian(rgb)

                if munsell is not None:
                    # Compute Jacobian
                    jacobian, det = compute_jacobian_numerical(rgb)

                    if jacobian is not None:
                        results.append(JacobianPoint(
                            rgb=(float(r), float(g), float(b)),
                            munsell=tuple(float(x) for x in munsell),
                            jacobian_det=float(det),
                            jacobian_matrix=jacobian.tolist(),
                            valid=True
                        ))
                    else:
                        results.append(JacobianPoint(
                            rgb=(float(r), float(g), float(b)),
                            munsell=tuple(float(x) for x in munsell),
                            jacobian_det=None,
                            jacobian_matrix=None,
                            valid=False
                        ))
                else:
                    results.append(JacobianPoint(
                        rgb=(float(r), float(g), float(b)),
                        munsell=None,
                        jacobian_det=None,
                        jacobian_matrix=None,
                        valid=False
                    ))

    return results


def analyze_jacobian_results(results: List[JacobianPoint]) -> Dict:
    """Analyze Jacobian computation results."""
    valid_points = [r for r in results if r.valid and r.jacobian_det is not None]

    if not valid_points:
        return {"error": "No valid Jacobian computations"}

    dets = np.array([abs(r.jacobian_det) for r in valid_points])

    # Basic statistics
    stats = {
        "total_points": len(results),
        "valid_points": len(valid_points),
        "valid_fraction": len(valid_points) / len(results),
        "jacobian_det_abs": {
            "mean": float(np.mean(dets)),
            "std": float(np.std(dets)),
            "min": float(np.min(dets)),
            "max": float(np.max(dets)),
            "median": float(np.median(dets)),
            "percentile_5": float(np.percentile(dets, 5)),
            "percentile_95": float(np.percentile(dets, 95)),
        },
        "volume_scaling": {
            "expansion_fraction": float(np.mean(dets > 1)),  # |det(J)| > 1
            "contraction_fraction": float(np.mean(dets < 1)),  # |det(J)| < 1
            "coefficient_of_variation": float(np.std(dets) / np.mean(dets)),
        }
    }

    # Analyze by Munsell value (luminance)
    values = np.array([r.munsell[2] for r in valid_points])  # z is value
    value_bins = [(0, 3), (3, 5), (5, 7), (7, 10)]

    stats["by_munsell_value"] = {}
    for v_low, v_high in value_bins:
        mask = (values >= v_low) & (values < v_high)
        if np.sum(mask) > 0:
            bin_dets = dets[mask]
            stats["by_munsell_value"][f"{v_low}-{v_high}"] = {
                "count": int(np.sum(mask)),
                "mean": float(np.mean(bin_dets)),
                "std": float(np.std(bin_dets)),
            }

    # Analyze by chroma (saturation)
    # Chroma is sqrt(x^2 + y^2) in Munsell Cartesian
    chromas = np.array([np.sqrt(r.munsell[0]**2 + r.munsell[1]**2) for r in valid_points])
    chroma_bins = [(0, 4), (4, 8), (8, 12), (12, 20)]

    stats["by_munsell_chroma"] = {}
    for c_low, c_high in chroma_bins:
        mask = (chromas >= c_low) & (chromas < c_high)
        if np.sum(mask) > 0:
            bin_dets = dets[mask]
            stats["by_munsell_chroma"][f"{c_low}-{c_high}"] = {
                "count": int(np.sum(mask)),
                "mean": float(np.mean(bin_dets)),
                "std": float(np.std(bin_dets)),
            }

    # Identify high-distortion regions
    high_distortion_threshold = np.percentile(dets, 95)
    low_distortion_threshold = np.percentile(dets, 5)

    high_distortion_points = [r for r in valid_points if abs(r.jacobian_det) > high_distortion_threshold]
    low_distortion_points = [r for r in valid_points if abs(r.jacobian_det) < low_distortion_threshold]

    stats["high_distortion_regions"] = {
        "threshold": float(high_distortion_threshold),
        "count": len(high_distortion_points),
        "example_points": [
            {"rgb": p.rgb, "munsell": p.munsell, "det": p.jacobian_det}
            for p in high_distortion_points[:5]
        ]
    }

    stats["low_distortion_regions"] = {
        "threshold": float(low_distortion_threshold),
        "count": len(low_distortion_points),
        "example_points": [
            {"rgb": p.rgb, "munsell": p.munsell, "det": p.jacobian_det}
            for p in low_distortion_points[:5]
        ]
    }

    return stats


def generate_report(stats: Dict, results: List[JacobianPoint]) -> str:
    """Generate Jacobian analysis report."""
    report = []
    report.append("# Jacobian Analysis: RGB↔Munsell Volume Distortion")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")

    report.append("## Overview")
    report.append("")
    report.append("The Jacobian determinant |det(J)| represents the local volume scaling factor")
    report.append("when transforming from RGB to Munsell Cartesian space.")
    report.append("")
    report.append("- |det(J)| > 1: RGB volumes **expand** in Munsell space")
    report.append("- |det(J)| < 1: RGB volumes **contract** in Munsell space")
    report.append("- |det(J)| ≈ 1: Volume-preserving transformation (locally)")
    report.append("")

    report.append("## Sampling Statistics")
    report.append("")
    report.append(f"- Total points sampled: {stats['total_points']}")
    report.append(f"- Valid Jacobian computations: {stats['valid_points']} ({stats['valid_fraction']*100:.1f}%)")
    report.append("")

    report.append("## Jacobian Determinant Statistics")
    report.append("")
    det_stats = stats["jacobian_det_abs"]
    report.append("| Statistic | Value |")
    report.append("|-----------|-------|")
    report.append(f"| Mean | {det_stats['mean']:.4f} |")
    report.append(f"| Std Dev | {det_stats['std']:.4f} |")
    report.append(f"| Median | {det_stats['median']:.4f} |")
    report.append(f"| Min | {det_stats['min']:.6f} |")
    report.append(f"| Max | {det_stats['max']:.4f} |")
    report.append(f"| 5th percentile | {det_stats['percentile_5']:.4f} |")
    report.append(f"| 95th percentile | {det_stats['percentile_95']:.4f} |")
    report.append("")

    vol_stats = stats["volume_scaling"]
    report.append("## Volume Scaling Distribution")
    report.append("")
    report.append(f"- **Expansion (|det(J)| > 1)**: {vol_stats['expansion_fraction']*100:.1f}% of color space")
    report.append(f"- **Contraction (|det(J)| < 1)**: {vol_stats['contraction_fraction']*100:.1f}% of color space")
    report.append(f"- **Coefficient of Variation**: {vol_stats['coefficient_of_variation']:.2f}")
    report.append("")

    if vol_stats['coefficient_of_variation'] > 0.5:
        report.append("**High CV indicates significant non-uniformity** in volume mapping.")
        report.append("Volume-based losses may need position-dependent weighting.")
    else:
        report.append("**Moderate CV suggests reasonably uniform** volume mapping.")
    report.append("")

    report.append("## Analysis by Munsell Value (Luminance)")
    report.append("")
    report.append("| Value Range | Count | Mean |det(J)| | Std Dev |")
    report.append("|-------------|-------|---------------|---------|")
    for range_name, data in stats.get("by_munsell_value", {}).items():
        report.append(f"| {range_name} | {data['count']} | {data['mean']:.4f} | {data['std']:.4f} |")
    report.append("")

    report.append("## Analysis by Munsell Chroma (Saturation)")
    report.append("")
    report.append("| Chroma Range | Count | Mean |det(J)| | Std Dev |")
    report.append("|--------------|-------|---------------|---------|")
    for range_name, data in stats.get("by_munsell_chroma", {}).items():
        report.append(f"| {range_name} | {data['count']} | {data['mean']:.4f} | {data['std']:.4f} |")
    report.append("")

    report.append("## High Distortion Regions")
    report.append("")
    high = stats.get("high_distortion_regions", {})
    report.append(f"Threshold (95th percentile): |det(J)| > {high.get('threshold', 0):.4f}")
    report.append(f"Number of points: {high.get('count', 0)}")
    report.append("")

    report.append("## Key Findings")
    report.append("")

    mean_det = det_stats['mean']
    cv = vol_stats['coefficient_of_variation']

    if mean_det > 1.5:
        report.append(f"1. **Overall expansion**: Mean |det(J)| = {mean_det:.2f} indicates RGB volumes expand ~{mean_det:.1f}x in Munsell")
    elif mean_det < 0.67:
        report.append(f"1. **Overall contraction**: Mean |det(J)| = {mean_det:.2f} indicates RGB volumes contract to ~{mean_det:.1f}x in Munsell")
    else:
        report.append(f"1. **Near-preserving**: Mean |det(J)| = {mean_det:.2f} indicates roughly volume-preserving transformation")

    report.append(f"2. **Non-uniformity**: CV = {cv:.2f} - {'High' if cv > 0.5 else 'Moderate'} spatial variation in volume mapping")
    report.append("")

    report.append("## Implications for Transformation Search")
    report.append("")
    report.append("- Volume matching in loss function may benefit from Jacobian weighting")
    report.append("- Per-family correction factors can account for local distortion")
    report.append("- High-distortion regions may require special handling")
    report.append("")

    return "\n".join(report)


def main():
    """Run Jacobian analysis."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Phase 5.2: Jacobian Analysis for Volume Distortion")
    print("=" * 70)

    # Sample color space
    resolution = 15  # 15^3 = 3375 points (balance of coverage and speed)
    print(f"\nSampling color space with resolution {resolution}^3 = {resolution**3} points...")

    results = sample_color_space(resolution)
    valid_count = sum(1 for r in results if r.valid)
    print(f"Valid Jacobian computations: {valid_count}/{len(results)}")

    # Analyze results
    print("\nAnalyzing Jacobian distribution...")
    stats = analyze_jacobian_results(results)

    # Print summary
    det_stats = stats.get("jacobian_det_abs", {})
    print(f"\n|det(J)| statistics:")
    print(f"  Mean: {det_stats.get('mean', 0):.4f}")
    print(f"  Std:  {det_stats.get('std', 0):.4f}")
    print(f"  Range: [{det_stats.get('min', 0):.6f}, {det_stats.get('max', 0):.4f}]")

    vol_stats = stats.get("volume_scaling", {})
    print(f"\nVolume scaling:")
    print(f"  Expansion (>1): {vol_stats.get('expansion_fraction', 0)*100:.1f}%")
    print(f"  Contraction (<1): {vol_stats.get('contraction_fraction', 0)*100:.1f}%")
    print(f"  CV: {vol_stats.get('coefficient_of_variation', 0):.2f}")

    # Save results
    results_file = output_dir / "jacobian_analysis.json"
    results_data = {
        "metadata": {
            "resolution": resolution,
            "total_points": len(results),
            "valid_points": valid_count,
            "generated": datetime.now().isoformat()
        },
        "statistics": stats,
        "sample_points": [asdict(r) for r in results[:100]]  # Save first 100 for inspection
    }

    with open(results_file, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(stats, results)
    report_file = output_dir / "jacobian_analysis.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")

    # Save full Jacobian map for visualization
    jacobian_map_file = output_dir / "jacobian_map.json"
    jacobian_map = [
        {
            "rgb": r.rgb,
            "munsell": r.munsell,
            "jacobian_det": r.jacobian_det
        }
        for r in results if r.valid and r.jacobian_det is not None
    ]

    with open(jacobian_map_file, "w") as f:
        json.dump(jacobian_map, f)
    print(f"Saved: {jacobian_map_file} ({len(jacobian_map)} points)")

    print("\n" + "=" * 70)
    print("JACOBIAN ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
