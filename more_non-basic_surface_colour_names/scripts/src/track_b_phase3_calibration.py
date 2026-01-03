#!/usr/bin/env python3
"""
Track B Phase 3: Calibration Subset Analysis

Uses non-XKCD, non-Centore sources (Meodai, ColorHexa, Wikipedia) to:
1. Select colors whose names match Centore's 30 families
2. Convert RGB to Munsell using MunsellSpace library
3. Build polyhedra from calibration samples
4. Compare to Centore's polyhedra to quantify screen-physical bias

This is the proper calibration methodology per PIPELINE_DRAFT_v2.md
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from collections import defaultdict

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from data_service import DataService, ColorEntry, ColorSource
from core.munsell import parse_munsell, MunsellCoord
from core.geometry import compute_inner_hull, compute_filled_solid_centroid

# Try to import munsellspace for RGB->Munsell conversion
try:
    import munsellspace
    HAS_MUNSELLSPACE = True
except ImportError:
    HAS_MUNSELLSPACE = False
    print("WARNING: munsellspace not installed. Using approximation for RGB->Munsell.")


@dataclass
class CalibrationResult:
    """Result of comparing calibration polyhedra to Centore."""
    family: str
    calibration_count: int
    centore_count: int
    has_calibration_hull: bool
    has_centore_hull: bool
    centroid_diff: Optional[Tuple[float, float, float]]  # (dx, dy, dz)
    hue_bias: Optional[float]
    value_bias: Optional[float]
    chroma_bias: Optional[float]


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def rgb_to_munsell(r: int, g: int, b: int) -> Optional[MunsellCoord]:
    """Convert RGB to Munsell using MunsellSpace or approximation."""
    if HAS_MUNSELLSPACE:
        try:
            result = munsellspace.rgb_to_munsell(r, g, b)
            if result:
                return parse_munsell(result)
        except Exception:
            pass

    # Fallback: simple approximation via HSV
    # This is NOT accurate but provides a baseline
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r_norm, g_norm, b_norm)
    min_c = min(r_norm, g_norm, b_norm)
    delta = max_c - min_c

    # Value (approximate)
    value = max_c * 10.0  # Scale 0-10

    # Chroma (approximate)
    if max_c == 0:
        chroma = 0.0
    else:
        chroma = (delta / max_c) * 14.0  # Scale roughly

    # Hue (approximate)
    if delta == 0:
        hue_number = 0.0
        hue_letter = 'N'
        chroma = 0.0
    else:
        if max_c == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif max_c == g_norm:
            h = 60 * ((b_norm - r_norm) / delta + 2)
        else:
            h = 60 * ((r_norm - g_norm) / delta + 4)

        # Convert to Munsell hue (0-100 scale)
        # Munsell: R=0-10, YR=10-20, Y=20-30, GY=30-40, G=40-50, BG=50-60, B=60-70, PB=70-80, P=80-90, RP=90-100
        hue_continuous = (h / 360.0) * 100.0

        # Determine hue letter and number
        hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        hue_idx = int(hue_continuous // 10)
        if hue_idx >= 10:
            hue_idx = 0
        hue_letter = hue_order[hue_idx]
        hue_number = hue_continuous % 10.0
        if hue_number == 0:
            hue_number = 10.0
            hue_idx = (hue_idx - 1) % 10
            hue_letter = hue_order[hue_idx]

    return MunsellCoord(
        hue_number=hue_number,
        hue_letter=hue_letter,
        value=value,
        chroma=chroma
    )


def load_centore_polyhedra(datasets_root: Path) -> Dict[str, dict]:
    """Load Centore's 30 polyhedra."""
    polyhedra = {}
    poly_dir = datasets_root / 'centore' / 'PolyhedronFiles'

    for txt_file in sorted(poly_dir.glob('PolyhedronDataFor*.txt')):
        family = txt_file.stem.replace('PolyhedronDataFor', '').lower()

        with open(txt_file, 'r') as f:
            content = f.read()

        # Parse centroid
        centroid = None
        for line in content.split('\n'):
            if 'Centroid in Cartesian coordinates:' in line:
                parts = line.split(':')[1].strip().split()
                if len(parts) >= 3:
                    centroid = (float(parts[0]), float(parts[1]), float(parts[2]))
                break

        # Parse vertices
        vertices = []
        in_vertices = False
        for line in content.split('\n'):
            line = line.strip()
            if 'Polyhedron vertices in Cartesian coordinates:' in line:
                in_vertices = True
                continue
            if in_vertices:
                if 'Polyhedron faces' in line:
                    break
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        v = (float(parts[0]), float(parts[1]), float(parts[2]))
                        vertices.append(v)
                    except ValueError:
                        pass

        polyhedra[family] = {
            'centroid': centroid,
            'vertices': vertices,
            'num_vertices': len(vertices)
        }

    return polyhedra


def run_calibration_analysis():
    """Run the full Track B Phase 3 calibration analysis."""
    print("=" * 70)
    print("Track B Phase 3: Calibration Subset Analysis")
    print("=" * 70)
    print()

    # Initialize data service
    service = DataService()

    # Get calibration subset (non-XKCD, non-Centore)
    calib = service.get_calibration_subset()
    calib_stats = calib.get_statistics()

    print("Calibration Subset Sources:")
    for source, count in calib_stats['by_source'].items():
        print(f"  {source}: {count:,} entries")
    print(f"  Total: {calib_stats['total_entries']:,} entries")
    print()

    # Get Centore's 30 families
    families = service.centore_families()
    print(f"Centore families: {len(families)}")
    print()

    # Collect calibration samples for each family
    family_samples: Dict[str, List[Tuple[int, int, int]]] = defaultdict(list)
    family_munsell: Dict[str, List[MunsellCoord]] = defaultdict(list)

    print("Collecting calibration samples...")
    for entry in calib.iter_all():
        if not entry.rgb_hex:
            continue

        # Check if name contains a Centore family name
        name_lower = entry.name.lower()
        matched_family = None
        for family in families:
            if family in name_lower.split():  # Match whole word
                matched_family = family
                break

        if matched_family:
            try:
                rgb = hex_to_rgb(entry.rgb_hex)
                family_samples[matched_family].append(rgb)

                # Convert to Munsell
                munsell = rgb_to_munsell(*rgb)
                if munsell:
                    family_munsell[matched_family].append(munsell)
            except Exception:
                pass

    print(f"Found samples for {len(family_samples)} families")
    for family in sorted(family_samples.keys()):
        print(f"  {family}: {len(family_samples[family])} samples")
    print()

    # Load Centore polyhedra
    centore_polyhedra = load_centore_polyhedra(service.datasets_path)
    print(f"Loaded {len(centore_polyhedra)} Centore polyhedra")
    print()

    # Build calibration polyhedra and compare
    results = []

    print("Building calibration polyhedra and comparing to Centore...")
    print("-" * 70)

    for family in sorted(families):
        samples = family_munsell.get(family, [])
        centore = centore_polyhedra.get(family, {})

        result = CalibrationResult(
            family=family,
            calibration_count=len(samples),
            centore_count=centore.get('num_vertices', 0),
            has_calibration_hull=False,
            has_centore_hull=centore.get('centroid') is not None,
            centroid_diff=None,
            hue_bias=None,
            value_bias=None,
            chroma_bias=None
        )

        if len(samples) >= 4:  # Minimum for 3D hull
            # Convert to Cartesian
            points = np.array([s.to_cartesian() for s in samples])

            try:
                # Compute inner hull
                hull_vertices, hull_faces = compute_inner_hull(points)

                if len(hull_vertices) >= 4:
                    result.has_calibration_hull = True

                    # Compute centroid
                    calib_centroid = compute_filled_solid_centroid(hull_vertices, hull_faces)

                    if centore.get('centroid'):
                        centore_c = centore['centroid']
                        dx = calib_centroid[0] - centore_c[0]
                        dy = calib_centroid[1] - centore_c[1]
                        dz = calib_centroid[2] - centore_c[2]
                        result.centroid_diff = (dx, dy, dz)

                        # Compute bias in Munsell terms
                        # x = C*cos(H*pi/50), y = C*sin(H*pi/50), z = V
                        # Value bias is just dz
                        result.value_bias = dz

                        # Chroma from xy magnitude
                        calib_chroma = np.sqrt(calib_centroid[0]**2 + calib_centroid[1]**2)
                        centore_chroma = np.sqrt(centore_c[0]**2 + centore_c[1]**2)
                        result.chroma_bias = calib_chroma - centore_chroma

                        # Hue from angle (in degrees)
                        calib_hue_rad = np.arctan2(calib_centroid[1], calib_centroid[0])
                        centore_hue_rad = np.arctan2(centore_c[1], centore_c[0])
                        calib_hue = np.degrees(calib_hue_rad)
                        centore_hue = np.degrees(centore_hue_rad)
                        hue_diff = calib_hue - centore_hue
                        # Normalize to -180 to 180
                        if hue_diff > 180:
                            hue_diff -= 360
                        elif hue_diff < -180:
                            hue_diff += 360
                        result.hue_bias = hue_diff
            except Exception as e:
                print(f"  {family}: Error computing hull - {e}")

        results.append(result)

        # Print summary
        status = "✓" if result.has_calibration_hull else "✗"
        print(f"  {status} {family:12} | samples: {result.calibration_count:4d} | ", end="")
        if result.centroid_diff:
            print(f"V={result.value_bias:+.2f} C={result.chroma_bias:+.2f} H={result.hue_bias:+.1f}°")
        else:
            print("(insufficient data)")

    print()

    # Aggregate bias statistics
    valid_results = [r for r in results if r.centroid_diff is not None]

    if valid_results:
        value_biases = [r.value_bias for r in valid_results]
        chroma_biases = [r.chroma_bias for r in valid_results]
        hue_biases = [r.hue_bias for r in valid_results]

        print("=" * 70)
        print("Aggregate Bias Analysis")
        print("=" * 70)
        print(f"Families with valid calibration hulls: {len(valid_results)}/{len(results)}")
        print()
        print(f"Value Bias (screen - surface):")
        print(f"  Mean: {np.mean(value_biases):+.3f}")
        print(f"  Std:  {np.std(value_biases):.3f}")
        print(f"  Range: [{min(value_biases):.3f}, {max(value_biases):.3f}]")
        print()
        print(f"Chroma Bias (screen - surface):")
        print(f"  Mean: {np.mean(chroma_biases):+.3f}")
        print(f"  Std:  {np.std(chroma_biases):.3f}")
        print(f"  Range: [{min(chroma_biases):.3f}, {max(chroma_biases):.3f}]")
        print()
        print(f"Hue Bias (screen - surface, degrees):")
        print(f"  Mean: {np.mean(hue_biases):+.1f}°")
        print(f"  Std:  {np.std(hue_biases):.1f}°")
        print(f"  Range: [{min(hue_biases):.1f}°, {max(hue_biases):.1f}°]")
        print()

        # Interpretation
        print("=" * 70)
        print("Interpretation")
        print("=" * 70)

        mean_v = np.mean(value_biases)
        mean_c = np.mean(chroma_biases)

        if mean_v > 0.5:
            print("• Screen colors appear LIGHTER than surface colors")
        elif mean_v < -0.5:
            print("• Screen colors appear DARKER than surface colors")
        else:
            print("• Value bias is minimal")

        if mean_c > 1.0:
            print("• Screen colors appear more SATURATED than surface colors")
        elif mean_c < -1.0:
            print("• Screen colors appear less saturated than surface colors")
        else:
            print("• Chroma bias is moderate")

        hue_std = np.std(hue_biases)
        if hue_std > 15:
            print("• Hue bias is NON-UNIFORM (category-dependent)")
        else:
            print("• Hue bias appears uniform across categories")

        print()

        # Save results
        output = {
            'methodology': 'Track B Phase 3 - Calibration Subset Analysis',
            'sources': list(calib_stats['by_source'].keys()),
            'total_calibration_samples': sum(len(v) for v in family_samples.values()),
            'families_analyzed': len(results),
            'families_with_valid_hull': len(valid_results),
            'aggregate_bias': {
                'value': {
                    'mean': float(np.mean(value_biases)),
                    'std': float(np.std(value_biases)),
                    'min': float(min(value_biases)),
                    'max': float(max(value_biases)),
                    'interpretation': 'positive = screen appears lighter'
                },
                'chroma': {
                    'mean': float(np.mean(chroma_biases)),
                    'std': float(np.std(chroma_biases)),
                    'min': float(min(chroma_biases)),
                    'max': float(max(chroma_biases)),
                    'interpretation': 'positive = screen appears more saturated'
                },
                'hue': {
                    'mean': float(np.mean(hue_biases)),
                    'std': float(np.std(hue_biases)),
                    'min': float(min(hue_biases)),
                    'max': float(max(hue_biases)),
                    'interpretation': 'degrees, category-dependent if std > 15'
                }
            },
            'per_family': [
                {
                    'family': r.family,
                    'calibration_count': r.calibration_count,
                    'centore_count': r.centore_count,
                    'has_valid_hull': r.has_calibration_hull,
                    'value_bias': r.value_bias,
                    'chroma_bias': r.chroma_bias,
                    'hue_bias': r.hue_bias
                }
                for r in results
            ]
        }

        output_path = service.datasets_path.parent / 'writeups' / 'results' / 'data' / 'track_b_phase3_calibration.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"Results saved to: {output_path}")

    else:
        print("No valid calibration hulls could be computed.")
        print("This may indicate insufficient matching samples in calibration sources.")

    print()
    print("=" * 70)
    print("Track B Phase 3 Complete")
    print("=" * 70)


if __name__ == '__main__':
    run_calibration_analysis()
