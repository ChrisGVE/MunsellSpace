#!/usr/bin/env python3
"""
Screen Color Polyhedra Construction with Confidence Thresholds

Builds screen color polyhedra from 184K crowdsourced data with multiple NLP
confidence thresholds to analyze quality vs. quantity trade-offs.

Input: datasets/phase6/family_assignments_munsell.csv
Output: datasets/screen_polyhedra/threshold_X.X/{family}_polyhedron.json
        datasets/screen_polyhedra/threshold_comparison.md

Uses SBERT family assignments from Phase 6 pipeline with confidence filtering.
"""

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import numpy as np
from scipy.spatial import ConvexHull


# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent / "datasets"
PHASE6_DIR = DATASETS_DIR / "phase6"
OUTPUT_DIR = DATASETS_DIR / "screen_polyhedra"
OUTPUT_DIR.mkdir(exist_ok=True)

# Confidence thresholds to test
THRESHOLDS = [0.6, 0.7, 0.8, 0.9]


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
    point_count: int
    avg_confidence: float
    avg_similarity: float
    min_confidence: float
    max_confidence: float

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
            "avg_confidence": round(self.avg_confidence, 4),
            "avg_similarity": round(self.avg_similarity, 4),
            "min_confidence": round(self.min_confidence, 4),
            "max_confidence": round(self.max_confidence, 4),
        }


def load_family_assignments(threshold: float) -> Tuple[List[Dict], Dict[str, List[float]]]:
    """
    Load family assignments filtered by confidence threshold.
    Returns (colors, confidence_stats) where confidence_stats tracks all confidence/similarity scores.
    """
    csv_path = PHASE6_DIR / "family_assignments_munsell.csv"
    colors = []
    confidence_stats = defaultdict(lambda: {"confidences": [], "similarities": []})

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                confidence = float(row.get("confidence", 0))
                similarity = float(row.get("similarity_score", 0))

                # Track stats for all colors in this family
                family = row["assigned_family"]
                confidence_stats[family]["confidences"].append(confidence)
                confidence_stats[family]["similarities"].append(similarity)

                # Only include if meets threshold
                if confidence < threshold:
                    continue

                # Only include colors with valid Cartesian coordinates
                if row.get("cartesian_x") and row.get("cartesian_y") and row.get("cartesian_z"):
                    x = float(row["cartesian_x"])
                    y = float(row["cartesian_y"])
                    z = float(row["cartesian_z"])

                    if not (math.isnan(x) or math.isnan(y) or math.isnan(z)):
                        colors.append({
                            **row,
                            "point": (x, y, z),
                            "confidence": confidence,
                            "similarity": similarity,
                        })
            except (ValueError, TypeError, KeyError):
                pass

    print(f"  Loaded {len(colors)} colors with confidence >= {threshold}")
    return colors, confidence_stats


def group_by_family(colors: List[Dict]) -> Tuple[Dict[str, List[Tuple]], Dict[str, Dict]]:
    """
    Group colors by family and extract unique Cartesian points.
    Returns (family_points, family_stats).
    """
    families = defaultdict(set)
    family_stats = defaultdict(lambda: {
        "confidences": [],
        "similarities": [],
        "sample_count": 0
    })

    for color in colors:
        family = color["assigned_family"]
        point = color["point"]

        # Track statistics
        family_stats[family]["confidences"].append(color["confidence"])
        family_stats[family]["similarities"].append(color["similarity"])
        family_stats[family]["sample_count"] += 1

        # Round to avoid floating point duplicates
        rounded = (round(point[0], 4), round(point[1], 4), round(point[2], 4))
        families[family].add(rounded)

    # Convert sets to lists
    result = {f: list(points) for f, points in families.items()}

    print(f"  Grouped into {len(result)} families")
    return result, family_stats


def compute_centroid(points: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Compute centroid of a set of points."""
    arr = np.array(points)
    return tuple(np.mean(arr, axis=0).tolist())


def build_polyhedron(
    family: str,
    points: List[Tuple[float, float, float]],
    stats: Dict
) -> Optional[Polyhedron]:
    """Build a convex hull polyhedron from points."""
    if len(points) < 4:
        print(f"    {family}: Only {len(points)} points, need at least 4 for 3D hull")
        return None

    arr = np.array(points)

    # Check if points are coplanar or nearly coplanar
    try:
        hull = ConvexHull(arr)
    except Exception as e:
        print(f"    {family}: ConvexHull failed: {e}")
        # Try adding small jitter
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

    # Calculate confidence statistics
    confidences = stats["confidences"]
    similarities = stats["similarities"]

    return Polyhedron(
        family=family,
        vertices=actual_vertices,
        faces=faces,
        centroid=centroid,
        volume=hull.volume,
        surface_area=hull.area,
        sample_count=stats["sample_count"],
        point_count=len(points),
        avg_confidence=np.mean(confidences),
        avg_similarity=np.mean(similarities),
        min_confidence=min(confidences),
        max_confidence=max(confidences),
    )


def build_all_polyhedra(
    family_points: Dict[str, List[Tuple]],
    family_stats: Dict[str, Dict]
) -> List[Polyhedron]:
    """Build polyhedra for all families."""
    polyhedra = []

    print("  Building polyhedra...")
    for family, points in sorted(family_points.items()):
        poly = build_polyhedron(family, points, family_stats[family])
        if poly:
            polyhedra.append(poly)
            print(f"    {family}: {len(poly.vertices)} vertices, "
                  f"{len(poly.faces)} faces, volume={poly.volume:.2f}, "
                  f"avg_conf={poly.avg_confidence:.3f}")

    return polyhedra


def save_polyhedra(polyhedra: List[Polyhedron], threshold: float):
    """Save each polyhedron to a separate JSON file."""
    threshold_dir = OUTPUT_DIR / f"threshold_{threshold}"
    threshold_dir.mkdir(exist_ok=True)

    for poly in polyhedra:
        json_path = threshold_dir / f"{poly.family}_polyhedron.json"
        with open(json_path, "w") as f:
            json.dump(poly.to_dict(), f, indent=2)

    print(f"  Saved {len(polyhedra)} polyhedra to {threshold_dir}")


def create_summary(polyhedra: List[Polyhedron], threshold: float) -> Dict:
    """Create a summary of all polyhedra for this threshold."""
    summary = {
        "threshold": threshold,
        "total_families": len(polyhedra),
        "total_samples": sum(p.sample_count for p in polyhedra),
        "total_unique_points": sum(p.point_count for p in polyhedra),
        "total_vertices": sum(len(p.vertices) for p in polyhedra),
        "total_faces": sum(len(p.faces) for p in polyhedra),
        "total_volume": sum(p.volume for p in polyhedra),
        "avg_confidence": np.mean([p.avg_confidence for p in polyhedra]),
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
            "avg_confidence": round(poly.avg_confidence, 4),
            "avg_similarity": round(poly.avg_similarity, 4),
        }

    return summary


def print_threshold_summary(polyhedra: List[Polyhedron], threshold: float):
    """Print summary for this threshold."""
    print(f"\n{'='*70}")
    print(f"THRESHOLD {threshold} SUMMARY")
    print(f"{'='*70}")

    total_samples = sum(p.sample_count for p in polyhedra)
    total_points = sum(p.point_count for p in polyhedra)

    print(f"\nTotal families: {len(polyhedra)}")
    print(f"Total samples: {total_samples:,}")
    print(f"Total unique points: {total_points:,}")
    print(f"Average confidence: {np.mean([p.avg_confidence for p in polyhedra]):.4f}")
    print(f"Total volume: {sum(p.volume for p in polyhedra):.2f}")

    print(f"\n{'Family':<15} {'Samples':>10} {'Points':>10} {'Volume':>12} {'Avg Conf':>10}")
    print("-" * 70)

    for poly in sorted(polyhedra, key=lambda x: -x.sample_count)[:15]:
        print(f"{poly.family:<15} {poly.sample_count:>10,} {poly.point_count:>10} "
              f"{poly.volume:>12.2f} {poly.avg_confidence:>10.3f}")


def compare_thresholds(all_summaries: Dict[float, Dict]):
    """Generate threshold comparison report."""
    report_lines = []

    report_lines.append("# Screen Color Polyhedra - Confidence Threshold Comparison")
    report_lines.append("")
    report_lines.append("Analysis of how NLP confidence thresholds affect polyhedra construction.")
    report_lines.append("")

    # Overall comparison table
    report_lines.append("## Overall Statistics by Threshold")
    report_lines.append("")
    report_lines.append("| Threshold | Families | Samples | Unique Points | Volume | Avg Confidence |")
    report_lines.append("|-----------|----------|---------|---------------|--------|----------------|")

    for threshold in THRESHOLDS:
        summary = all_summaries[threshold]
        report_lines.append(
            f"| {threshold:.1f} | {summary['total_families']} | "
            f"{summary['total_samples']:,} | {summary['total_unique_points']:,} | "
            f"{summary['total_volume']:.2f} | {summary['avg_confidence']:.4f} |"
        )

    report_lines.append("")

    # Family survival analysis
    report_lines.append("## Family Coverage Across Thresholds")
    report_lines.append("")

    # Get all families that appear in any threshold
    all_families: Set[str] = set()
    for summary in all_summaries.values():
        all_families.update(summary["families"].keys())

    report_lines.append("| Family | 0.6 | 0.7 | 0.8 | 0.9 |")
    report_lines.append("|--------|-----|-----|-----|-----|")

    for family in sorted(all_families):
        row = [family]
        for threshold in THRESHOLDS:
            if family in all_summaries[threshold]["families"]:
                count = all_summaries[threshold]["families"][family]["sample_count"]
                row.append(f"{count:,}")
            else:
                row.append("—")
        report_lines.append("| " + " | ".join(row) + " |")

    report_lines.append("")

    # Detailed analysis per threshold
    for threshold in THRESHOLDS:
        summary = all_summaries[threshold]
        report_lines.append(f"## Threshold {threshold:.1f} Details")
        report_lines.append("")
        report_lines.append(f"- **Families:** {summary['total_families']}")
        report_lines.append(f"- **Total Samples:** {summary['total_samples']:,}")
        report_lines.append(f"- **Unique Points:** {summary['total_unique_points']:,}")
        report_lines.append(f"- **Total Volume:** {summary['total_volume']:.2f} cubic Munsell units")
        report_lines.append(f"- **Average Confidence:** {summary['avg_confidence']:.4f}")
        report_lines.append("")

        # Top 10 families by volume
        top_families = sorted(
            summary["families"].items(),
            key=lambda x: x[1]["volume"],
            reverse=True
        )[:10]

        report_lines.append("### Top 10 Families by Volume")
        report_lines.append("")
        report_lines.append("| Family | Samples | Points | Volume | Confidence |")
        report_lines.append("|--------|---------|--------|--------|------------|")

        for family, data in top_families:
            report_lines.append(
                f"| {family} | {data['sample_count']:,} | {data['point_count']} | "
                f"{data['volume']:.2f} | {data['avg_confidence']:.3f} |"
            )

        report_lines.append("")

    # Recommendations
    report_lines.append("## Recommendations")
    report_lines.append("")
    report_lines.append("### Optimal Threshold Selection")
    report_lines.append("")

    # Find threshold with best balance
    best_threshold = None
    best_score = -1

    for threshold in THRESHOLDS:
        summary = all_summaries[threshold]
        # Score: balance between data quantity and quality
        # Normalize families (0-1), samples (0-1), confidence (already 0-1)
        max_families = max(s["total_families"] for s in all_summaries.values())
        max_samples = max(s["total_samples"] for s in all_summaries.values())

        norm_families = summary["total_families"] / max_families
        norm_samples = summary["total_samples"] / max_samples
        norm_conf = summary["avg_confidence"]

        # Weight: 30% families, 30% samples, 40% confidence
        score = 0.3 * norm_families + 0.3 * norm_samples + 0.4 * norm_conf

        if score > best_score:
            best_score = score
            best_threshold = threshold

    report_lines.append(f"**Recommended threshold: {best_threshold:.1f}**")
    report_lines.append("")
    report_lines.append("This threshold provides the best balance between:")
    report_lines.append("- **Data Quantity:** Sufficient samples for stable polyhedra")
    report_lines.append("- **Data Quality:** High confidence NLP assignments")
    report_lines.append("- **Family Coverage:** Maximum number of families represented")
    report_lines.append("")

    # Trade-off analysis
    report_lines.append("### Trade-off Analysis")
    report_lines.append("")
    report_lines.append("- **Lower thresholds (0.6-0.7):**")
    report_lines.append("  - More samples per family → more stable polyhedra")
    report_lines.append("  - Better family coverage")
    report_lines.append("  - Risk of noisy boundaries from ambiguous assignments")
    report_lines.append("")
    report_lines.append("- **Higher thresholds (0.8-0.9):**")
    report_lines.append("  - Cleaner, more precise boundaries")
    report_lines.append("  - Higher confidence in family membership")
    report_lines.append("  - Risk of losing some families with fewer high-confidence samples")
    report_lines.append("  - May miss legitimate boundary regions")
    report_lines.append("")

    # Save report
    report_path = OUTPUT_DIR / "threshold_comparison.md"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"\nSaved threshold comparison report to {report_path}")


def main():
    """Main entry point."""
    print("Screen Color Polyhedra Construction with Confidence Thresholds")
    print("=" * 70)

    all_summaries = {}

    for threshold in THRESHOLDS:
        print(f"\n{'='*70}")
        print(f"Processing Threshold: {threshold}")
        print(f"{'='*70}")

        # Load data for this threshold
        colors, confidence_stats = load_family_assignments(threshold)

        # Group by family
        family_points, family_stats = group_by_family(colors)

        # Build polyhedra
        polyhedra = build_all_polyhedra(family_points, family_stats)

        # Save polyhedra
        save_polyhedra(polyhedra, threshold)

        # Create and save summary
        summary = create_summary(polyhedra, threshold)
        summary_path = OUTPUT_DIR / f"threshold_{threshold}_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        all_summaries[threshold] = summary

        # Print summary
        print_threshold_summary(polyhedra, threshold)

    # Compare all thresholds
    print(f"\n{'='*70}")
    print("Generating Threshold Comparison Report")
    print(f"{'='*70}")
    compare_thresholds(all_summaries)

    print("\n" + "="*70)
    print("Screen color polyhedra construction complete!")
    print("="*70)
    print(f"\nResults saved to: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("1. Review threshold_comparison.md for recommendations")
    print("2. Compare with Centore surface color polyhedra")
    print("3. Analyze systematic biases in screen vs surface colors")


if __name__ == "__main__":
    main()
