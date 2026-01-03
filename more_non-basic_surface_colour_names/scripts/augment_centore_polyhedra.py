#!/usr/bin/env python3
"""
Augment Centore Polyhedra with Surface Color Data

Loads Centore's original 30 polyhedra and augments them with collected surface
color data, then reconstructs convex hulls to create improved polyhedra.

Data quality tiers:
- HIGH confidence: Golden Acrylics, Williamsburg Oils (native spectrophotometer)
- MEDIUM confidence: NCS, RAL Classic, RHS (RGB-derived from surface standards)

Based on Centore (2020) methodology.
"""

import csv
import json
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass

import numpy as np
from scipy.spatial import ConvexHull

SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent / "datasets"
SURFACE_DIR = DATASETS_DIR / "surface_colors"
CENTORE_DIR = DATASETS_DIR / "centore" / "PolyhedronFiles"
OUTPUT_DIR = DATASETS_DIR / "augmented_polyhedra"

# Centore 30 families with expected Munsell hue ranges
# (copied from construct_surface_polyhedra.py for consistency)
OVERLAY_HUE_RANGES = {
    # Reds (R)
    "red": {"hue_start": 0, "hue_end": 10, "hue_letters": ["R"]},
    "rust": {"hue_start": 5, "hue_end": 15, "hue_letters": ["R", "YR"], "value_max": 5},
    "coral": {"hue_start": 5, "hue_end": 20, "hue_letters": ["R", "YR"], "value_min": 5, "chroma_min": 6},
    "wine": {"hue_start": 0, "hue_end": 10, "hue_letters": ["R", "RP"], "value_max": 4},
    "maroon": {"hue_start": 0, "hue_end": 10, "hue_letters": ["R", "RP"], "value_max": 4, "chroma_min": 4},

    # Yellow-Reds (YR) - Orange/Brown region
    "orange": {"hue_start": 10, "hue_end": 25, "hue_letters": ["YR"], "chroma_min": 8},
    "brown": {"hue_start": 10, "hue_end": 30, "hue_letters": ["YR", "Y"], "value_max": 5, "chroma_max": 6},
    "tan": {"hue_start": 10, "hue_end": 30, "hue_letters": ["YR", "Y"], "value_min": 5, "chroma_max": 5},
    "peach": {"hue_start": 10, "hue_end": 25, "hue_letters": ["YR"], "value_min": 6, "chroma_min": 3, "chroma_max": 8},
    "sand": {"hue_start": 15, "hue_end": 35, "hue_letters": ["YR", "Y"], "value_min": 6, "chroma_max": 4},
    "beige": {"hue_start": 15, "hue_end": 35, "hue_letters": ["YR", "Y"], "value_min": 6, "chroma_max": 4},
    "taupe": {"hue_start": 10, "hue_end": 35, "hue_letters": ["YR", "Y"], "value_min": 4, "value_max": 7, "chroma_max": 4},

    # Yellows (Y)
    "yellow": {"hue_start": 25, "hue_end": 40, "hue_letters": ["Y"], "chroma_min": 6},
    "gold": {"hue_start": 25, "hue_end": 40, "hue_letters": ["Y", "YR"], "value_min": 5, "value_max": 8},

    # Yellow-Greens (GY) to Greens (G)
    "lime": {"hue_start": 35, "hue_end": 50, "hue_letters": ["GY"], "chroma_min": 8},
    "green": {"hue_start": 45, "hue_end": 65, "hue_letters": ["G", "GY"]},

    # Blue-Greens (BG)
    "teal": {"hue_start": 60, "hue_end": 75, "hue_letters": ["BG", "G"], "value_max": 6},
    "aqua": {"hue_start": 60, "hue_end": 80, "hue_letters": ["BG"], "value_min": 5},
    "aquamarine": {"hue_start": 60, "hue_end": 80, "hue_letters": ["BG", "B"], "value_min": 6, "chroma_min": 4},
    "turquoise": {"hue_start": 60, "hue_end": 80, "hue_letters": ["BG"], "value_min": 5, "chroma_min": 5},

    # Blues (B)
    "blue": {"hue_start": 75, "hue_end": 90, "hue_letters": ["B", "PB"]},
    "navy": {"hue_start": 75, "hue_end": 90, "hue_letters": ["B", "PB"], "value_max": 4},

    # Purple-Blues (PB) to Purples (P)
    "indigo": {"hue_start": 82, "hue_end": 95, "hue_letters": ["PB", "P"], "value_max": 5},
    "violet": {"hue_start": 85, "hue_end": 100, "hue_letters": ["P", "PB"]},
    "purple": {"hue_start": 85, "hue_end": 100, "hue_letters": ["P"]},
    "lavender": {"hue_start": 85, "hue_end": 100, "hue_letters": ["P", "PB"], "value_min": 6, "chroma_max": 6},
    "lilac": {"hue_start": 85, "hue_end": 100, "hue_letters": ["P"], "value_min": 6, "chroma_max": 5},
    "plum": {"hue_start": 88, "hue_end": 100, "hue_letters": ["P", "RP"], "value_max": 5, "chroma_min": 4},

    # Red-Purples (RP)
    "magenta": {"hue_start": 92, "hue_end": 100, "hue_letters": ["RP", "P"], "chroma_min": 8},
    "fuchsia": {"hue_start": 92, "hue_end": 100, "hue_letters": ["RP"], "chroma_min": 6},
    "mauve": {"hue_start": 90, "hue_end": 100, "hue_letters": ["RP", "P"], "chroma_max": 6},
    "rose": {"hue_start": 95, "hue_end": 100, "hue_letters": ["RP"], "value_min": 5},
    "pink": {"hue_start": 95, "hue_end": 100, "hue_letters": ["RP", "R"], "value_min": 6},

    # Neutrals
    "gray": {"hue_letters": ["N"], "chroma_max": 2},
    "white": {"hue_letters": ["N"], "value_min": 8},
}

# Hue letter to numeric degree mapping
HUE_LETTER_DEGREES = {
    "R": 0, "YR": 10, "Y": 20, "GY": 35,
    "G": 50, "BG": 65, "B": 80, "PB": 87,
    "P": 92, "RP": 97, "N": None  # Neutral
}


def parse_munsell_hue(hue_str: str) -> Tuple[Optional[float], Optional[str]]:
    """Parse Munsell hue notation into numeric value and letter."""
    if not hue_str or hue_str == "N":
        return None, "N"

    # Match patterns like "5R", "10YR", "2.5GY", "7.5PB", "N0"
    match = re.match(r'^(\d+\.?\d*)\s*([A-Z]+)$', hue_str.strip().upper())
    if match:
        return float(match.group(1)), match.group(2)

    # Handle "N" followed by number (neutrals)
    if hue_str.strip().upper().startswith('N'):
        return None, "N"

    return None, None


def hue_to_degrees(hue_value: float, hue_letter: str) -> float:
    """Convert Munsell hue notation to degrees (0-100 scale)."""
    if hue_letter == "N":
        return None

    base = HUE_LETTER_DEGREES.get(hue_letter, 0)
    next_hue = _next_hue(hue_letter)
    next_base = HUE_LETTER_DEGREES.get(next_hue, base + 10)

    # Each hue letter spans a range; hue_value goes from 0 to 10 within each letter
    return base + (hue_value / 10) * (next_base - base)


def _next_hue(hue_letter: str) -> str:
    """Get next hue letter in sequence."""
    order = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"]
    try:
        idx = order.index(hue_letter)
        return order[(idx + 1) % len(order)]
    except ValueError:
        return hue_letter


def munsell_to_cartesian(hue_deg: Optional[float], value: float, chroma: float) -> Tuple[float, float, float]:
    """Convert Munsell HVC to Cartesian coordinates."""
    if hue_deg is None:  # Neutral
        return (0, 0, value)

    # Convert from 0-100 scale to radians
    hue_rad = (hue_deg / 100) * 2 * math.pi
    x = chroma * math.cos(hue_rad)
    y = chroma * math.sin(hue_rad)
    return (x, y, value)


def assign_to_overlay(hue_str: str, value: float, chroma: float) -> Optional[str]:
    """Assign a color to an overlay family based on Munsell coordinates."""
    hue_value, hue_letter = parse_munsell_hue(hue_str)

    if hue_letter == "N":
        # Neutral colors
        if value >= 8:
            return "white"
        else:
            return "gray"

    if hue_letter is None:
        return None

    for family, criteria in OVERLAY_HUE_RANGES.items():
        # Check hue letter
        if "hue_letters" in criteria:
            if hue_letter not in criteria["hue_letters"]:
                continue

        # Check value range
        if "value_min" in criteria and value < criteria["value_min"]:
            continue
        if "value_max" in criteria and value > criteria["value_max"]:
            continue

        # Check chroma range
        if "chroma_min" in criteria and chroma < criteria["chroma_min"]:
            continue
        if "chroma_max" in criteria and chroma > criteria["chroma_max"]:
            continue

        return family

    return None


def load_centore_polyhedron(family: str) -> Optional[Dict]:
    """Load Centore reference polyhedron for a family."""
    path = CENTORE_DIR / f"PolyhedronDataFor{family}.txt"
    if not path.exists():
        return None

    result = {
        'centroid': None,
        'vertices': [],
        'samples': 0
    }
    in_cartesian = False

    with open(path) as f:
        for line in f:
            line = line.strip()
            if "unique CAUS samples" in line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    try:
                        result['samples'] = int(parts[-1])
                    except ValueError:
                        pass
            elif "Centroid in Cartesian" in line:
                parts = line.split("\t")
                if len(parts) >= 4:
                    try:
                        result['centroid'] = [float(parts[1]), float(parts[2]), float(parts[3])]
                    except ValueError:
                        pass
            elif "Polyhedron vertices in Cartesian" in line:
                in_cartesian = True
            elif "Polyhedron faces" in line or "Samples" in line:
                in_cartesian = False
            elif in_cartesian:
                parts = line.split("\t")
                if len(parts) >= 3:
                    try:
                        result['vertices'].append([float(parts[0]), float(parts[1]), float(parts[2])])
                    except ValueError:
                        pass

    return result if result['vertices'] else None


def load_surface_colors_by_quality() -> Dict[str, List[Dict]]:
    """Load surface colors categorized by quality tier."""
    high_confidence = []  # Native spectrophotometer
    medium_confidence = []  # RGB-derived from surface standards

    # HIGH confidence sources
    high_sources = {
        'golden_acrylics.csv': 'art_supplies',
        'williamsburg_oils.csv': 'art_supplies'
    }

    for filename, subdir in high_sources.items():
        path = SURFACE_DIR / subdir / filename
        if path.exists():
            with open(path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('munsell_h') and row['munsell_h'].strip():
                        try:
                            high_confidence.append({
                                'name': row.get('name', ''),
                                'source': filename.replace('.csv', ''),
                                'hue': row['munsell_h'],
                                'value': float(row['munsell_v']) if row.get('munsell_v') else 0,
                                'chroma': float(row['munsell_c']) if row.get('munsell_c') else 0,
                            })
                        except (ValueError, KeyError):
                            continue

    # MEDIUM confidence sources
    medium_sources = {
        'ncs_colors.csv': 'industrial',
        'ral_classic.csv': 'industrial',
        'rhs_colors.csv': 'botanical'
    }

    for filename, subdir in medium_sources.items():
        path = SURFACE_DIR / subdir / filename
        if path.exists():
            with open(path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('munsell_h') and row['munsell_h'].strip():
                        try:
                            medium_confidence.append({
                                'name': row.get('name', row.get('color_name', '')),
                                'source': filename.replace('.csv', ''),
                                'hue': row['munsell_h'],
                                'value': float(row['munsell_v']) if row.get('munsell_v') else 0,
                                'chroma': float(row['munsell_c']) if row.get('munsell_c') else 0,
                            })
                        except (ValueError, KeyError):
                            continue

    return {
        'high': high_confidence,
        'medium': medium_confidence
    }


def calculate_centroid(points: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Calculate centroid of points."""
    if not points:
        return (0, 0, 0)
    x = sum(p[0] for p in points) / len(points)
    y = sum(p[1] for p in points) / len(points)
    z = sum(p[2] for p in points) / len(points)
    return (x, y, z)


def euclidean_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)


def compute_convex_hull(points: List[Tuple[float, float, float]]) -> Optional[Dict]:
    """Compute convex hull for a set of 3D points."""
    if len(points) < 4:
        return None

    try:
        # Convert to numpy array
        points_array = np.array(points)

        # Compute convex hull
        hull = ConvexHull(points_array)

        return {
            'vertices': hull.points[hull.vertices].tolist(),
            'faces': hull.simplices.tolist(),
            'volume': float(hull.volume),
            'n_vertices': len(hull.vertices),
            'n_faces': len(hull.simplices)
        }
    except Exception as e:
        print(f"    Warning: ConvexHull failed: {e}")
        return None


def main():
    """Augment Centore polyhedra with surface color data."""
    print("Augmenting Centore Polyhedra with Surface Color Data")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load surface colors by quality tier
    print("\nLoading surface color data...")
    colors_by_quality = load_surface_colors_by_quality()
    print(f"  HIGH confidence (spectrophotometer): {len(colors_by_quality['high'])} colors")
    print(f"  MEDIUM confidence (RGB-derived): {len(colors_by_quality['medium'])} colors")

    # Combine all surface colors
    all_surface_colors = colors_by_quality['high'] + colors_by_quality['medium']
    print(f"  Total surface colors: {len(all_surface_colors)}")

    # Assign to overlay families
    print("\nAssigning surface colors to families...")
    surface_by_family = defaultdict(list)
    unassigned = 0

    for color in all_surface_colors:
        family = assign_to_overlay(color['hue'], color['value'], color['chroma'])
        if family:
            hue_deg = hue_to_degrees(*parse_munsell_hue(color['hue']))
            point = munsell_to_cartesian(hue_deg, color['value'], color['chroma'])
            surface_by_family[family].append({
                'name': color['name'],
                'source': color['source'],
                'cartesian': point,
                'munsell': f"{color['hue']} {color['value']}/{color['chroma']}"
            })
        else:
            unassigned += 1

    print(f"  Assigned: {sum(len(v) for v in surface_by_family.values())} to families")
    print(f"  Unassigned: {unassigned}")

    # Process each Centore family
    print("\nAugmenting polyhedra...")
    results = []
    report_lines = []

    for family in sorted(OVERLAY_HUE_RANGES.keys()):
        # Load Centore original
        centore = load_centore_polyhedron(family)
        if not centore:
            print(f"  ⚠ {family}: No Centore polyhedron found, skipping")
            continue

        # Get surface samples for this family
        surface_samples = surface_by_family.get(family, [])

        # Combine Centore vertices with surface sample points
        original_vertices = [tuple(v) for v in centore['vertices']]
        surface_points = [s['cartesian'] for s in surface_samples]
        all_points = original_vertices + surface_points

        # Calculate centroids
        original_centroid = tuple(centore['centroid'])
        augmented_centroid = calculate_centroid(all_points)
        centroid_shift = euclidean_distance(original_centroid, augmented_centroid)

        # Reconstruct convex hull
        hull_data = compute_convex_hull(all_points)

        # Determine status
        significant_deviation = centroid_shift > 2.0
        status_symbol = "⚠" if significant_deviation else "✓"

        result = {
            'family': family,
            'original_samples': centore['samples'],
            'surface_samples': len(surface_samples),
            'total_points': len(all_points),
            'original_centroid': list(original_centroid),
            'augmented_centroid': list(augmented_centroid),
            'centroid_shift': centroid_shift,
            'significant_deviation': significant_deviation,
            'hull': hull_data,
            'surface_sources': list(set(s['source'] for s in surface_samples)) if surface_samples else []
        }
        results.append(result)

        # Print progress
        print(f"  {status_symbol} {family:12s}: +{len(surface_samples):3d} surface samples, "
              f"shift={centroid_shift:.2f} Munsell units")

        # Save individual augmented polyhedron
        output_path = OUTPUT_DIR / f"{family}_augmented.json"
        with open(output_path, 'w') as f:
            json.dump({
                'family': family,
                'original_samples': centore['samples'],
                'surface_samples_added': len(surface_samples),
                'total_points': len(all_points),
                'original_centroid': list(original_centroid),
                'augmented_centroid': list(augmented_centroid),
                'centroid_shift': centroid_shift,
                'vertices': hull_data['vertices'] if hull_data else [],
                'faces': hull_data['faces'] if hull_data else [],
                'volume': hull_data['volume'] if hull_data else 0,
                'surface_sources': result['surface_sources'],
                'surface_colors': [{'name': s['name'], 'munsell': s['munsell'], 'source': s['source']}
                                   for s in surface_samples]
            }, f, indent=2)

    # Generate augmentation report
    print("\nGenerating augmentation report...")
    report_path = OUTPUT_DIR / "augmentation_report.md"

    with open(report_path, 'w') as f:
        f.write("# Centore Polyhedra Augmentation Report\n\n")
        f.write("## Summary\n\n")

        total_surface_added = sum(r['surface_samples'] for r in results)
        avg_shift = sum(r['centroid_shift'] for r in results) / len(results) if results else 0
        significant_deviations = [r for r in results if r['significant_deviation']]

        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Families augmented | {len(results)} |\n")
        f.write(f"| Total surface samples added | {total_surface_added} |\n")
        f.write(f"| Average centroid shift | {avg_shift:.2f} Munsell units |\n")
        f.write(f"| Families with significant deviation (>2 units) | {len(significant_deviations)} |\n\n")

        f.write("## Augmentation by Family\n\n")
        f.write("| Family | Original Samples | Surface Added | Total | Centroid Shift | Status |\n")
        f.write("|--------|------------------|---------------|-------|----------------|--------|\n")

        for r in sorted(results, key=lambda x: -x['surface_samples']):
            status = "⚠ DEVIATION" if r['significant_deviation'] else "✓ Good"
            f.write(f"| {r['family']} | {r['original_samples']} | {r['surface_samples']} | "
                   f"{r['total_points']} | {r['centroid_shift']:.2f} | {status} |\n")

        f.write("\n## Families with Significant Deviation (>2 Munsell units)\n\n")
        if significant_deviations:
            for r in sorted(significant_deviations, key=lambda x: -x['centroid_shift']):
                f.write(f"### {r['family']}\n")
                f.write(f"- **Centroid shift**: {r['centroid_shift']:.2f} Munsell units\n")
                f.write(f"- **Surface samples added**: {r['surface_samples']}\n")
                f.write(f"- **Sources**: {', '.join(r['surface_sources'])}\n")
                f.write(f"- **Interpretation**: Large shift suggests surface samples may represent "
                       f"different color characteristics than Centore's CAUS dataset\n\n")
        else:
            f.write("No families show significant deviation. All augmented polyhedra are consistent "
                   "with Centore's originals.\n\n")

        f.write("## Data Quality Notes\n\n")
        f.write("**Centroid Shift Interpretation**:\n")
        f.write("- <1 unit: Excellent consistency\n")
        f.write("- 1-2 units: Good consistency\n")
        f.write("- >2 units: Review recommended\n\n")
        f.write("**Quality Tiers**:\n")
        f.write("- HIGH: Golden Acrylics, Williamsburg Oils (spectrophotometer measurements)\n")
        f.write("- MEDIUM: NCS, RAL Classic, RHS (RGB-derived from surface standards)\n\n")
        f.write("---\n\n")
        f.write("*Generated by augment_centore_polyhedra.py*\n")

    print(f"  Report saved to: {report_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Families augmented: {len(results)}")
    print(f"Total surface samples added: {total_surface_added}")
    print(f"Average centroid shift: {avg_shift:.2f} Munsell units")
    print(f"Significant deviations (>2 units): {len(significant_deviations)}")

    if significant_deviations:
        print("\nFamilies requiring review:")
        for r in sorted(significant_deviations, key=lambda x: -x['centroid_shift'])[:5]:
            print(f"  - {r['family']}: {r['centroid_shift']:.2f} units shift")
    else:
        print("\n✓ All augmented polyhedra show good consistency with Centore originals")

    print(f"\nOutput saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
