#!/usr/bin/env python3
"""
Polyhedra-Based Bias Analysis

Compares XKCD polyhedra centroids with Centore polyhedra centroids to detect
systematic biases between screen colors and physical colors.

This uses the inner convex hull centroids (Centore's methodology) rather than
simple mean centroids, providing a more robust comparison that excludes outliers.

Usage:
    python polyhedra_bias_analysis.py
"""

import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import statistics

from common import save_results, INVESTIGATION_DIR


@dataclass
class PolyhedronCentroid:
    """Polyhedron centroid in Cartesian coordinates."""
    x: float
    y: float
    z: float  # Value
    sample_count: int
    vertex_count: int
    volume: float

    def to_munsell(self) -> Tuple[float, float, float]:
        """Convert centroid to Munsell (hue_degrees, value, chroma)."""
        chroma = math.sqrt(self.x**2 + self.y**2)
        hue_rad = math.atan2(self.y, self.x)
        hue_degrees = hue_rad * 180.0 / math.pi
        if hue_degrees < 0:
            hue_degrees += 360
        return (hue_degrees, self.z, chroma)


class PolyhedraBiasAnalyzer:
    """Analyzes bias between XKCD and Centore polyhedra."""

    def __init__(self):
        self.investigation_dir = INVESTIGATION_DIR
        self.project_root = Path(__file__).parent.parent.parent
        self.centore_dir = self.project_root / "PolyhedronFilesJustNames"
        self.centore_polyhedra: Dict[str, PolyhedronCentroid] = {}
        self.xkcd_polyhedra: Dict[str, PolyhedronCentroid] = {}

    def _load_centore_published_centroid(self, color: str) -> Optional[Tuple[float, float, float]]:
        """Load Centore's PUBLISHED centroid from his original files."""
        filepath = self.centore_dir / f'PolyhedronDataFor{color}.txt'
        if not filepath.exists():
            return None
        with open(filepath) as f:
            for line in f:
                if 'Centroid in Cartesian coordinates:' in line:
                    parts = line.split(':')[1].strip().split()
                    if len(parts) >= 3:
                        return (float(parts[0]), float(parts[1]), float(parts[2]))
        return None

    def load_polyhedra(self) -> Tuple[int, int]:
        """Load polyhedra data - Centore from HIS files, XKCD from our results."""
        results_path = self.investigation_dir / "convex_hull_results.json"

        if not results_path.exists():
            raise FileNotFoundError(f"Convex hull results not found: {results_path}")

        with open(results_path) as f:
            data = json.load(f)

        # Load Centore polyhedra using HIS PUBLISHED centroids
        for name, poly_data in data.get('centore', {}).items():
            published_centroid = self._load_centore_published_centroid(name)
            if published_centroid:
                centroid = published_centroid
            else:
                # Fallback to our computed centroid if file not found
                centroid = tuple(poly_data.get('centroid', [0, 0, 0]))

            self.centore_polyhedra[name] = PolyhedronCentroid(
                x=centroid[0],
                y=centroid[1],
                z=centroid[2],
                sample_count=poly_data.get('sample_count', 0),
                vertex_count=poly_data.get('vertex_count', 0),
                volume=poly_data.get('volume', 0),
            )

        # Load XKCD polyhedra
        for name, poly_data in data.get('xkcd', {}).items():
            centroid = poly_data.get('centroid', [0, 0, 0])
            self.xkcd_polyhedra[name] = PolyhedronCentroid(
                x=centroid[0],
                y=centroid[1],
                z=centroid[2],
                sample_count=poly_data.get('sample_count', 0),
                vertex_count=poly_data.get('vertex_count', 0),
                volume=poly_data.get('volume', 0),
            )

        return len(self.centore_polyhedra), len(self.xkcd_polyhedra)

    def compute_bias(self, centore: PolyhedronCentroid, xkcd: PolyhedronCentroid) -> Dict:
        """Compute bias between Centore and XKCD polyhedra centroids."""
        # Cartesian differences
        delta_x = xkcd.x - centore.x
        delta_y = xkcd.y - centore.y
        delta_z = xkcd.z - centore.z

        # Euclidean distance
        distance = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        # Convert to Munsell for interpretable comparisons
        centore_munsell = centore.to_munsell()  # (hue, value, chroma)
        xkcd_munsell = xkcd.to_munsell()

        # Hue difference (circular)
        hue_diff = xkcd_munsell[0] - centore_munsell[0]
        if hue_diff > 180:
            hue_diff -= 360
        elif hue_diff < -180:
            hue_diff += 360

        value_diff = xkcd_munsell[1] - centore_munsell[1]
        chroma_diff = xkcd_munsell[2] - centore_munsell[2]

        # Volume ratio (how much larger is XKCD polyhedron)
        volume_ratio = xkcd.volume / centore.volume if centore.volume > 0 else float('inf')

        return {
            'delta_x': round(delta_x, 3),
            'delta_y': round(delta_y, 3),
            'delta_z': round(delta_z, 3),
            'euclidean_distance': round(distance, 3),
            'hue_diff': round(hue_diff, 2),
            'value_diff': round(value_diff, 2),
            'chroma_diff': round(chroma_diff, 2),
            'volume_ratio': round(volume_ratio, 2),
            'centore_munsell': {
                'hue': round(centore_munsell[0], 1),
                'value': round(centore_munsell[1], 2),
                'chroma': round(centore_munsell[2], 2),
            },
            'xkcd_munsell': {
                'hue': round(xkcd_munsell[0], 1),
                'value': round(xkcd_munsell[1], 2),
                'chroma': round(xkcd_munsell[2], 2),
            },
        }

    def run_analysis(self) -> Dict:
        """Run the complete polyhedra bias analysis."""
        print("=" * 70)
        print("POLYHEDRA-BASED BIAS ANALYSIS")
        print("Using Inner Convex Hull Centroids (Centore Methodology)")
        print("=" * 70)
        print()

        # Load data
        print("1. Loading polyhedra data...")
        n_centore, n_xkcd = self.load_polyhedra()
        print(f"   Centore polyhedra: {n_centore}")
        print(f"   XKCD polyhedra: {n_xkcd}")

        # Find matching categories
        matching_colors = set(self.centore_polyhedra.keys()) & set(self.xkcd_polyhedra.keys())
        print(f"   Matching categories: {len(matching_colors)}")

        # Compute biases
        print("\n2. Computing biases for each category...")

        comparisons = {}
        all_biases = []

        for color in sorted(matching_colors):
            centore_poly = self.centore_polyhedra[color]
            xkcd_poly = self.xkcd_polyhedra[color]

            bias = self.compute_bias(centore_poly, xkcd_poly)
            all_biases.append(bias)

            comparisons[color] = {
                'centore': {
                    'sample_count': centore_poly.sample_count,
                    'vertex_count': centore_poly.vertex_count,
                    'volume': round(centore_poly.volume, 2),
                    'centroid': [round(centore_poly.x, 3), round(centore_poly.y, 3), round(centore_poly.z, 3)],
                },
                'xkcd': {
                    'sample_count': xkcd_poly.sample_count,
                    'vertex_count': xkcd_poly.vertex_count,
                    'volume': round(xkcd_poly.volume, 2),
                    'centroid': [round(xkcd_poly.x, 3), round(xkcd_poly.y, 3), round(xkcd_poly.z, 3)],
                },
                'bias': bias,
            }

            direction = "→" if bias['hue_diff'] > 0 else "←"
            print(f"   {color:<12}: dist={bias['euclidean_distance']:.2f}, "
                  f"Δhue={bias['hue_diff']:+.1f}° {direction}, "
                  f"Δval={bias['value_diff']:+.2f}, "
                  f"Δchroma={bias['chroma_diff']:+.2f}, "
                  f"vol×{bias['volume_ratio']:.1f}")

        # Compute aggregate statistics
        print("\n3. Computing aggregate statistics...")

        aggregate = self._compute_aggregate_stats(all_biases)

        # Save results
        print("\n4. Saving results...")

        results = {
            'summary': {
                'centore_polyhedra': n_centore,
                'xkcd_polyhedra': n_xkcd,
                'matching_categories': len(matching_colors),
                'methodology': 'Inner Convex Hull (Centore JAIC 2020)',
            },
            'aggregate_bias': aggregate,
            'comparisons': comparisons,
        }

        save_results(results, 'polyhedra_bias_results.json')

        # Print summary
        self._print_summary(aggregate, matching_colors)

        return results

    def _compute_aggregate_stats(self, biases: List[Dict]) -> Dict:
        """Compute aggregate statistics from all biases."""
        if not biases:
            return {}

        def stats_for(key: str) -> Dict:
            values = [b[key] for b in biases]
            return {
                'mean': round(statistics.mean(values), 3),
                'std': round(statistics.stdev(values), 3) if len(values) > 1 else 0,
                'min': round(min(values), 3),
                'max': round(max(values), 3),
                'median': round(statistics.median(values), 3),
            }

        return {
            'hue_diff': stats_for('hue_diff'),
            'value_diff': stats_for('value_diff'),
            'chroma_diff': stats_for('chroma_diff'),
            'euclidean_distance': stats_for('euclidean_distance'),
            'volume_ratio': stats_for('volume_ratio'),
        }

    def _print_summary(self, aggregate: Dict, matching_colors: set):
        """Print analysis summary."""
        print()
        print("=" * 70)
        print("POLYHEDRA BIAS SUMMARY")
        print("=" * 70)
        print(f"  Matching categories analyzed: {len(matching_colors)}")
        print()

        if aggregate:
            print("  AGGREGATE BIAS (XKCD polyhedra - Centore polyhedra):")
            print(f"  ├─ Hue shift:      {aggregate['hue_diff']['mean']:+.2f}° "
                  f"(±{aggregate['hue_diff']['std']:.2f}°) "
                  f"[{aggregate['hue_diff']['min']:.1f}° to {aggregate['hue_diff']['max']:.1f}°]")
            print(f"  ├─ Value shift:    {aggregate['value_diff']['mean']:+.2f} "
                  f"(±{aggregate['value_diff']['std']:.2f}) "
                  f"[{aggregate['value_diff']['min']:.2f} to {aggregate['value_diff']['max']:.2f}]")
            print(f"  ├─ Chroma shift:   {aggregate['chroma_diff']['mean']:+.2f} "
                  f"(±{aggregate['chroma_diff']['std']:.2f}) "
                  f"[{aggregate['chroma_diff']['min']:.2f} to {aggregate['chroma_diff']['max']:.2f}]")
            print(f"  ├─ Mean distance:  {aggregate['euclidean_distance']['mean']:.2f} "
                  f"(±{aggregate['euclidean_distance']['std']:.2f}) "
                  f"[{aggregate['euclidean_distance']['min']:.2f} to {aggregate['euclidean_distance']['max']:.2f}]")
            print(f"  └─ Volume ratio:   {aggregate['volume_ratio']['mean']:.1f}× "
                  f"(±{aggregate['volume_ratio']['std']:.1f}) "
                  f"[{aggregate['volume_ratio']['min']:.1f}× to {aggregate['volume_ratio']['max']:.1f}×]")
            print()

            # Interpretation
            print("  INTERPRETATION:")

            # Hue interpretation
            if abs(aggregate['hue_diff']['mean']) > 10:
                if aggregate['hue_diff']['mean'] > 0:
                    print("  ├─ XKCD hues shifted toward yellow-red (warmer)")
                else:
                    print("  ├─ XKCD hues shifted toward blue-green (cooler)")
            else:
                print("  ├─ Hue: No significant systematic shift")

            # Value interpretation
            if aggregate['value_diff']['mean'] > 0.5:
                print("  ├─ XKCD colors appear LIGHTER than physical references")
            elif aggregate['value_diff']['mean'] < -0.5:
                print("  ├─ XKCD colors appear DARKER than physical references")
            else:
                print("  ├─ Value: No significant systematic shift")

            # Chroma interpretation
            if aggregate['chroma_diff']['mean'] > 1.0:
                print("  ├─ XKCD colors appear MORE SATURATED than physical")
            elif aggregate['chroma_diff']['mean'] < -1.0:
                print("  ├─ XKCD colors appear LESS SATURATED than physical")
            else:
                print("  ├─ Chroma: No significant systematic shift")

            # Volume interpretation
            if aggregate['volume_ratio']['mean'] > 5:
                print("  └─ XKCD polyhedra much LARGER (higher variance/noise)")
            elif aggregate['volume_ratio']['mean'] > 2:
                print("  └─ XKCD polyhedra moderately larger (more variance)")
            else:
                print("  └─ Volume: Similar spread between datasets")

        print()
        print("=" * 70)


def main():
    """Run polyhedra bias analysis."""
    analyzer = PolyhedraBiasAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
