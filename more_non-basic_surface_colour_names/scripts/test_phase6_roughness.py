#!/usr/bin/env python3
"""
Test roughness metrics on Phase 6 polyhedra to establish baseline values.

Loads all polyhedra from datasets/phase6/polyhedra/ and computes:
- Surface-to-volume ratio
- Fractal dimension
- Outlier statistics
- Alpha shape comparisons

Results are saved to datasets/phase6/roughness_baseline.json
"""

import json
import numpy as np
from pathlib import Path
from roughness_metrics import (
    surface_to_volume_ratio,
    calculate_fractal_dimension,
    outlier_detection,
    hull_comparison_ratio
)


def load_polyhedron(filepath: Path) -> np.ndarray:
    """Load vertices from polyhedron JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return np.array(data['vertices'])


def analyze_polyhedron(family_name: str, vertices: np.ndarray) -> dict:
    """Run complete roughness analysis on a polyhedron."""
    try:
        # Surface-to-volume ratio
        sv_metrics = surface_to_volume_ratio(vertices)

        # Fractal dimension
        fractal = calculate_fractal_dimension(
            vertices,
            min_boxes=5,
            max_boxes=30,
            num_scales=8
        )

        # Outlier detection with MAD
        outliers_mad = outlier_detection(
            vertices,
            method='mad',
            threshold=3.5,
            coordinate_wise=False
        )

        # Outlier detection with IQR
        outliers_iqr = outlier_detection(
            vertices,
            method='iqr',
            threshold=1.5,
            coordinate_wise=False
        )

        # Alpha shape comparisons at multiple scales
        alpha_comparisons = []
        for alpha in [0.5, 1.0, 2.0, 5.0]:
            try:
                comparison = hull_comparison_ratio(vertices, alpha)
                alpha_comparisons.append({
                    'alpha': alpha,
                    **comparison
                })
            except Exception as e:
                alpha_comparisons.append({
                    'alpha': alpha,
                    'error': str(e)
                })

        return {
            'family': family_name,
            'num_vertices': len(vertices),
            'surface_to_volume': sv_metrics,
            'fractal_dimension': {
                'dimension': fractal['dimension'],
                'r_squared': fractal['r_squared']
            },
            'outliers': {
                'mad': {
                    'num_outliers': outliers_mad['num_outliers'],
                    'percentage': outliers_mad['outlier_percentage']
                },
                'iqr': {
                    'num_outliers': outliers_iqr['num_outliers'],
                    'percentage': outliers_iqr['outlier_percentage']
                }
            },
            'alpha_shapes': alpha_comparisons,
            'quality_assessment': assess_quality(sv_metrics, fractal, outliers_mad)
        }
    except Exception as e:
        return {
            'family': family_name,
            'error': str(e)
        }


def assess_quality(sv_metrics: dict, fractal: dict, outliers: dict) -> dict:
    """Assess polyhedron quality based on roughness metrics."""
    # Quality thresholds from NOISE_ROUGHNESS_METRICS.md
    ratio = sv_metrics['ratio']
    dimension = fractal['dimension']
    outlier_pct = outliers['outlier_percentage']

    # S/V ratio assessment
    if ratio < 6.0:
        sv_quality = 'good'
    elif ratio < 7.0:
        sv_quality = 'acceptable'
    else:
        sv_quality = 'poor'

    # Fractal dimension assessment
    if dimension < 2.3:
        fd_quality = 'good'
    elif dimension < 2.6:
        fd_quality = 'acceptable'
    else:
        fd_quality = 'poor'

    # Outlier percentage assessment
    if outlier_pct < 5.0:
        outlier_quality = 'good'
    elif outlier_pct < 10.0:
        outlier_quality = 'acceptable'
    else:
        outlier_quality = 'poor'

    # Overall quality
    qualities = [sv_quality, fd_quality, outlier_quality]
    if all(q == 'good' for q in qualities):
        overall = 'good'
    elif any(q == 'poor' for q in qualities):
        overall = 'poor'
    else:
        overall = 'acceptable'

    return {
        'sv_ratio': sv_quality,
        'fractal_dimension': fd_quality,
        'outliers': outlier_quality,
        'overall': overall,
        'flags': {
            'high_roughness': ratio > 7.0,
            'high_fractal_dimension': dimension > 2.5,
            'high_outlier_rate': outlier_pct > 10.0
        }
    }


def main():
    # Paths
    base_dir = Path(__file__).parent.parent
    polyhedra_dir = base_dir / 'datasets' / 'phase6' / 'polyhedra'
    output_file = base_dir / 'datasets' / 'phase6' / 'roughness_baseline.json'

    print("Analyzing Phase 6 polyhedra roughness metrics...")
    print(f"Loading from: {polyhedra_dir}")

    # Load all polyhedra
    results = []
    polyhedron_files = sorted(polyhedra_dir.glob('*_polyhedron.json'))

    for i, filepath in enumerate(polyhedron_files, 1):
        family_name = filepath.stem.replace('_polyhedron', '')
        print(f"[{i}/{len(polyhedron_files)}] Analyzing {family_name}...")

        vertices = load_polyhedron(filepath)
        analysis = analyze_polyhedron(family_name, vertices)
        results.append(analysis)

        # Print summary
        if 'error' in analysis:
            print(f"  ERROR: {analysis['error']}")
        else:
            print(f"  S/V ratio: {analysis['surface_to_volume']['ratio']:.3f} "
                  f"({analysis['quality_assessment']['sv_ratio']})")
            print(f"  Fractal D: {analysis['fractal_dimension']['dimension']:.3f} "
                  f"({analysis['quality_assessment']['fractal_dimension']})")
            print(f"  Outliers:  {analysis['outliers']['mad']['percentage']:.1f}% "
                  f"({analysis['quality_assessment']['outliers']})")
            print(f"  Overall:   {analysis['quality_assessment']['overall'].upper()}")

    # Compute summary statistics
    valid_results = [r for r in results if 'error' not in r]

    if valid_results:
        sv_ratios = [r['surface_to_volume']['ratio'] for r in valid_results]
        fractal_dims = [r['fractal_dimension']['dimension'] for r in valid_results]
        outlier_pcts = [r['outliers']['mad']['percentage'] for r in valid_results]

        summary = {
            'total_families': len(polyhedron_files),
            'analyzed_successfully': len(valid_results),
            'statistics': {
                'sv_ratio': {
                    'mean': float(np.mean(sv_ratios)),
                    'std': float(np.std(sv_ratios)),
                    'min': float(np.min(sv_ratios)),
                    'max': float(np.max(sv_ratios)),
                    'median': float(np.median(sv_ratios))
                },
                'fractal_dimension': {
                    'mean': float(np.mean(fractal_dims)),
                    'std': float(np.std(fractal_dims)),
                    'min': float(np.min(fractal_dims)),
                    'max': float(np.max(fractal_dims)),
                    'median': float(np.median(fractal_dims))
                },
                'outlier_percentage': {
                    'mean': float(np.mean(outlier_pcts)),
                    'std': float(np.std(outlier_pcts)),
                    'min': float(np.min(outlier_pcts)),
                    'max': float(np.max(outlier_pcts)),
                    'median': float(np.median(outlier_pcts))
                }
            },
            'quality_distribution': {
                'good': sum(1 for r in valid_results if r['quality_assessment']['overall'] == 'good'),
                'acceptable': sum(1 for r in valid_results if r['quality_assessment']['overall'] == 'acceptable'),
                'poor': sum(1 for r in valid_results if r['quality_assessment']['overall'] == 'poor')
            }
        }

        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        print(f"Families analyzed: {summary['analyzed_successfully']}/{summary['total_families']}")
        print(f"\nS/V Ratio:")
        print(f"  Mean: {summary['statistics']['sv_ratio']['mean']:.3f} "
              f"± {summary['statistics']['sv_ratio']['std']:.3f}")
        print(f"  Range: [{summary['statistics']['sv_ratio']['min']:.3f}, "
              f"{summary['statistics']['sv_ratio']['max']:.3f}]")
        print(f"\nFractal Dimension:")
        print(f"  Mean: {summary['statistics']['fractal_dimension']['mean']:.3f} "
              f"± {summary['statistics']['fractal_dimension']['std']:.3f}")
        print(f"  Range: [{summary['statistics']['fractal_dimension']['min']:.3f}, "
              f"{summary['statistics']['fractal_dimension']['max']:.3f}]")
        print(f"\nOutlier Percentage:")
        print(f"  Mean: {summary['statistics']['outlier_percentage']['mean']:.1f}% "
              f"± {summary['statistics']['outlier_percentage']['std']:.1f}%")
        print(f"\nQuality Distribution:")
        print(f"  Good:       {summary['quality_distribution']['good']}")
        print(f"  Acceptable: {summary['quality_distribution']['acceptable']}")
        print(f"  Poor:       {summary['quality_distribution']['poor']}")

        # Save results
        output_data = {
            'summary': summary,
            'polyhedra': results
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nResults saved to: {output_file}")
    else:
        print("\nERROR: No polyhedra analyzed successfully!")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
