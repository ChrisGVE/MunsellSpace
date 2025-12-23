#!/usr/bin/env python3
"""
Phase 3: Pre-Consolidation Coordinate Analysis

Analyzes coordinate distributions before merging duplicates:
- XKCD: RGB coordinate statistics per color name
- Centore: Munsell coordinate statistics per overlay color
- Identifies high-variance names (inconsistent naming)
- Compares within-dataset variance

Note: XKCD uses RGB, Centore uses Munsell coordinates.
Cross-dataset comparison requires coordinate transformation (Phase 4).
"""

import json
import math
import re
from collections import defaultdict
from pathlib import Path
import statistics


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(__file__).parent

XKCD_DUMP = PROJECT_ROOT / "assets" / "xkcd" / "mainsurvey_sqldump.txt"
CENTORE_NAMES_DIR = PROJECT_ROOT / "PolyhedronFilesJustNames"


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_xkcd_coordinates(sql_dump_path: Path) -> dict:
    """
    Load color names with RGB coordinates from XKCD SQL dump.
    Returns dict: {color_name: [(r, g, b), ...]}
    """
    # Check cache
    cache_path = OUTPUT_DIR / "xkcd_coordinates_cache.json"
    if cache_path.exists():
        print("      (Loading from cache)")
        with open(cache_path, 'r') as f:
            cached = json.load(f)
            # Convert lists back to tuples
            return {k: [tuple(v) for v in vals] for k, vals in cached.items()}

    if not sql_dump_path.exists():
        print(f"Warning: XKCD dump not found at {sql_dump_path}")
        return {}

    color_coords = defaultdict(list)
    # Match: VALUES(id, user_id, timestamp, r, g, b, 'colorname')
    pattern = re.compile(r"VALUES\(\d+,\s*\d+,\s*[\d.]+,\s*(\d+),\s*(\d+),\s*(\d+),\s*'([^']*)'\)")

    print("      (Parsing SQL dump - this may take a few minutes...)")
    line_count = 0
    with open(sql_dump_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_count += 1
            if line_count % 500000 == 0:
                print(f"         Processed {line_count:,} lines...")
            if 'INSERT INTO "answers"' not in line:
                continue
            matches = pattern.findall(line)
            for r, g, b, name in matches:
                if name:
                    color_coords[name.lower().strip()].append((int(r), int(g), int(b)))

    result = dict(color_coords)

    # Save cache (convert tuples to lists for JSON)
    with open(cache_path, 'w') as f:
        json.dump({k: [list(v) for v in vals] for k, vals in result.items()}, f)
    print(f"      (Cached to {cache_path})")

    return result


def load_centore_coordinates(centore_dir: Path) -> dict:
    """
    Load Centore overlay colors with Munsell coordinates.
    Returns dict: {overlay_name: {'centroid': (h, v, c), 'samples': [...]}}
    """
    if not centore_dir.exists():
        print(f"Warning: Centore directory not found at {centore_dir}")
        return {}

    centore_data = {}

    for txt_file in centore_dir.glob("*.txt"):
        overlay_name = txt_file.stem.replace("PolyhedronDataFor", "").lower()
        samples = []
        centroid_munsell = None
        centroid_cartesian = None

        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            in_samples_section = False

            for line in f:
                line = line.strip()

                if line.startswith("Centroid in Munsell coordinates:"):
                    centroid_munsell = line.split('\t')[-1].strip()

                if line.startswith("Centroid in Cartesian coordinates:"):
                    parts = line.split('\t')[1:]
                    if len(parts) >= 3:
                        try:
                            centroid_cartesian = (float(parts[0]), float(parts[1]), float(parts[2]))
                        except (ValueError, IndexError):
                            pass

                if line.startswith("Samples, with Munsell coordinates"):
                    in_samples_section = True
                    continue

                if in_samples_section and line:
                    # Format: "Color Name\tMunsell Coords"
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        sample_name = parts[0].strip()
                        munsell = parts[1].strip()
                        if sample_name and not sample_name[0].isdigit():
                            parsed = parse_munsell(munsell)
                            if parsed:
                                samples.append({
                                    'name': sample_name,
                                    'munsell': munsell,
                                    'parsed': parsed
                                })

        if samples:
            centore_data[overlay_name] = {
                'centroid_munsell': centroid_munsell,
                'centroid_cartesian': centroid_cartesian,
                'samples': samples,
                'sample_count': len(samples)
            }

    return centore_data


def parse_munsell(munsell_str: str) -> dict:
    """
    Parse Munsell notation string to components.
    Format: "5.5YR 6.0/4.0" -> {'hue_value': 5.5, 'hue_letter': 'YR', 'value': 6.0, 'chroma': 4.0}
    """
    if not munsell_str:
        return None

    # Pattern: number + letters + space + number + / + number
    pattern = re.compile(r'([\d.]+)([A-Z]+)\s+([\d.]+)/([\d.]+)')
    match = pattern.match(munsell_str)

    if match:
        return {
            'hue_value': float(match.group(1)),
            'hue_letter': match.group(2),
            'value': float(match.group(3)),
            'chroma': float(match.group(4))
        }
    return None


# ============================================================================
# Statistical Analysis Functions
# ============================================================================

def compute_rgb_statistics(rgb_list: list) -> dict:
    """
    Compute statistics for a list of RGB tuples.
    """
    if not rgb_list:
        return None

    r_values = [c[0] for c in rgb_list]
    g_values = [c[1] for c in rgb_list]
    b_values = [c[2] for c in rgb_list]

    def channel_stats(values):
        n = len(values)
        if n == 0:
            return {'mean': 0, 'std': 0, 'min': 0, 'max': 0, 'range': 0}
        mean = statistics.mean(values)
        std = statistics.stdev(values) if n > 1 else 0
        return {
            'mean': mean,
            'std': std,
            'min': min(values),
            'max': max(values),
            'range': max(values) - min(values)
        }

    return {
        'count': len(rgb_list),
        'r': channel_stats(r_values),
        'g': channel_stats(g_values),
        'b': channel_stats(b_values),
        'total_variance': sum([
            channel_stats(r_values)['std']**2,
            channel_stats(g_values)['std']**2,
            channel_stats(b_values)['std']**2
        ]),
        'centroid': (
            statistics.mean(r_values),
            statistics.mean(g_values),
            statistics.mean(b_values)
        )
    }


def compute_munsell_statistics(samples: list) -> dict:
    """
    Compute statistics for Munsell coordinate samples.
    Note: Hue is circular, so we use circular statistics.
    """
    if not samples:
        return None

    values = [s['parsed']['value'] for s in samples if s['parsed']]
    chromas = [s['parsed']['chroma'] for s in samples if s['parsed']]

    # Hue is more complex - need to convert to angle for circular stats
    hue_angles = []
    for s in samples:
        if s['parsed']:
            angle = munsell_hue_to_angle(s['parsed']['hue_value'], s['parsed']['hue_letter'])
            if angle is not None:
                hue_angles.append(angle)

    def simple_stats(values_list):
        n = len(values_list)
        if n == 0:
            return {'mean': 0, 'std': 0, 'min': 0, 'max': 0, 'range': 0}
        mean = statistics.mean(values_list)
        std = statistics.stdev(values_list) if n > 1 else 0
        return {
            'mean': mean,
            'std': std,
            'min': min(values_list),
            'max': max(values_list),
            'range': max(values_list) - min(values_list)
        }

    # Circular statistics for hue
    hue_stats = {'mean': 0, 'std': 0}
    if hue_angles:
        hue_stats = circular_statistics(hue_angles)

    return {
        'count': len(samples),
        'value': simple_stats(values),
        'chroma': simple_stats(chromas),
        'hue': hue_stats,
        'total_variance': (
            hue_stats.get('std', 0)**2 +
            simple_stats(values).get('std', 0)**2 +
            simple_stats(chromas).get('std', 0)**2
        )
    }


def munsell_hue_to_angle(hue_value: float, hue_letter: str) -> float:
    """
    Convert Munsell hue notation to angle (0-360).
    Hue letters: R, YR, Y, GY, G, BG, B, PB, P, RP
    Each section spans 36 degrees.
    """
    hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
    if hue_letter not in hue_order:
        return None

    base_angle = hue_order.index(hue_letter) * 36
    # Hue value 0-10 within each section
    return base_angle + (hue_value / 10) * 36


def circular_statistics(angles: list) -> dict:
    """
    Compute circular mean and standard deviation for angles (degrees).
    """
    if not angles:
        return {'mean': 0, 'std': 0}

    # Convert to radians
    radians = [math.radians(a) for a in angles]

    # Circular mean
    sin_sum = sum(math.sin(r) for r in radians)
    cos_sum = sum(math.cos(r) for r in radians)
    mean_angle = math.degrees(math.atan2(sin_sum, cos_sum)) % 360

    # Circular standard deviation
    R = math.sqrt(sin_sum**2 + cos_sum**2) / len(angles)
    if R > 0:
        std = math.degrees(math.sqrt(-2 * math.log(R)))
    else:
        std = 180  # Maximum dispersion

    return {
        'mean': mean_angle,
        'std': std,
        'resultant_length': R  # 0 = uniform, 1 = all same direction
    }


def identify_high_variance_names(
    xkcd_stats: dict,
    threshold_std: float = 30.0,
    min_count: int = 10
) -> list:
    """
    Identify color names with high RGB variance (inconsistent naming).
    """
    high_variance = []

    for name, stats in xkcd_stats.items():
        if stats['count'] < min_count:
            continue

        # Total RGB variance
        total_std = math.sqrt(stats['total_variance'])
        if total_std >= threshold_std:
            high_variance.append({
                'name': name,
                'count': stats['count'],
                'total_std': total_std,
                'r_std': stats['r']['std'],
                'g_std': stats['g']['std'],
                'b_std': stats['b']['std'],
                'r_range': stats['r']['range'],
                'g_range': stats['g']['range'],
                'b_range': stats['b']['range']
            })

    return sorted(high_variance, key=lambda x: -x['total_std'])


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 3: Pre-Consolidation Coordinate Analysis")
    print("=" * 70)

    # Load XKCD coordinates
    print("\n1. Loading XKCD coordinate data...")
    xkcd_coords = load_xkcd_coordinates(XKCD_DUMP)
    print(f"   → Loaded {len(xkcd_coords):,} color names with RGB data")

    total_samples = sum(len(v) for v in xkcd_coords.values())
    print(f"   → Total RGB samples: {total_samples:,}")

    # Load Centore coordinates
    print("\n2. Loading Centore coordinate data...")
    centore_data = load_centore_coordinates(CENTORE_NAMES_DIR)
    print(f"   → Loaded {len(centore_data):,} overlay colors")

    total_centore = sum(d['sample_count'] for d in centore_data.values())
    print(f"   → Total Centore samples: {total_centore:,}")

    # Compute XKCD statistics
    print("\n3. Computing XKCD RGB statistics...")
    xkcd_stats = {}
    for name, coords in xkcd_coords.items():
        xkcd_stats[name] = compute_rgb_statistics(coords)

    # Find summary statistics
    counts = [s['count'] for s in xkcd_stats.values()]
    variances = [math.sqrt(s['total_variance']) for s in xkcd_stats.values()]

    print(f"   → Samples per name: min={min(counts)}, max={max(counts):,}, mean={statistics.mean(counts):.1f}")
    print(f"   → RGB std deviation: min={min(variances):.1f}, max={max(variances):.1f}, mean={statistics.mean(variances):.1f}")

    # Compute Centore statistics
    print("\n4. Computing Centore Munsell statistics...")
    centore_stats = {}
    for overlay, data in centore_data.items():
        centore_stats[overlay] = compute_munsell_statistics(data['samples'])

    for overlay in sorted(centore_stats.keys()):
        stats = centore_stats[overlay]
        print(f"   → {overlay}: {stats['count']} samples, value_std={stats['value']['std']:.2f}, chroma_std={stats['chroma']['std']:.2f}")

    # Identify high-variance names
    print("\n5. Identifying high-variance color names...")
    high_variance = identify_high_variance_names(xkcd_stats, threshold_std=40.0, min_count=100)
    print(f"   → Found {len(high_variance):,} high-variance names (std >= 40, count >= 100)")

    if high_variance:
        print("\n   Top 20 highest variance names:")
        for item in high_variance[:20]:
            print(f"      {item['name']}: std={item['total_std']:.1f}, count={item['count']:,}")

    # Generate report
    print("\n6. Generating outputs...")

    report = []
    report.append("# Phase 3: Pre-Consolidation Coordinate Analysis Report")
    report.append("")
    report.append("## 1. Executive Summary")
    report.append("")
    report.append("| Dataset | Names | Total Samples | Coordinate System |")
    report.append("|---------|-------|---------------|-------------------|")
    report.append(f"| XKCD | {len(xkcd_coords):,} | {total_samples:,} | RGB (0-255) |")
    report.append(f"| Centore | {len(centore_data):,} | {total_centore:,} | Munsell (HVC) |")
    report.append("")

    report.append("## 2. XKCD RGB Distribution Summary")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Min samples per name | {min(counts):,} |")
    report.append(f"| Max samples per name | {max(counts):,} |")
    report.append(f"| Mean samples per name | {statistics.mean(counts):.1f} |")
    report.append(f"| Median samples per name | {statistics.median(counts):.1f} |")
    report.append(f"| Min RGB std | {min(variances):.1f} |")
    report.append(f"| Max RGB std | {max(variances):.1f} |")
    report.append(f"| Mean RGB std | {statistics.mean(variances):.1f} |")
    report.append("")

    report.append("### 2.1 Interpretation")
    report.append("")
    report.append("- **Low variance**: Consistent color naming (same name = same color)")
    report.append("- **High variance**: Inconsistent naming or broad color category")
    report.append("- Typical RGB std < 30 indicates good naming consistency")
    report.append("")

    report.append("## 3. Centore Munsell Distribution Summary")
    report.append("")
    report.append("| Overlay | Samples | Value Std | Chroma Std | Hue Std |")
    report.append("|---------|---------|-----------|------------|---------|")

    for overlay in sorted(centore_stats.keys()):
        stats = centore_stats[overlay]
        data = centore_data[overlay]
        report.append(f"| {overlay} | {stats['count']} | {stats['value']['std']:.2f} | {stats['chroma']['std']:.2f} | {stats['hue']['std']:.1f} |")
    report.append("")

    report.append("### 3.1 Interpretation")
    report.append("")
    report.append("- **Value std**: Variation in lightness (0=dark, 10=light)")
    report.append("- **Chroma std**: Variation in saturation")
    report.append("- **Hue std**: Variation in hue angle (circular)")
    report.append("- Higher std = broader color category")
    report.append("")

    report.append("## 4. High-Variance Names (Potential Issues)")
    report.append("")
    report.append("Names with RGB std >= 40 and count >= 100:")
    report.append("These may indicate inconsistent color naming or overly broad categories.")
    report.append("")
    report.append("| Name | Count | Total Std | R Std | G Std | B Std | R Range | G Range | B Range |")
    report.append("|------|-------|-----------|-------|-------|-------|---------|---------|---------|")

    for item in high_variance[:50]:
        report.append(f"| {item['name']} | {item['count']:,} | {item['total_std']:.1f} | "
                     f"{item['r_std']:.1f} | {item['g_std']:.1f} | {item['b_std']:.1f} | "
                     f"{item['r_range']} | {item['g_range']} | {item['b_range']} |")
    report.append("")

    report.append("## 5. Coordinate System Comparison")
    report.append("")
    report.append("### 5.1 Challenge")
    report.append("XKCD and Centore use different coordinate systems:")
    report.append("- **XKCD**: RGB (device-dependent, uncalibrated monitors)")
    report.append("- **Centore**: Munsell (perceptually uniform, spectrophotometer)")
    report.append("")
    report.append("### 5.2 Implication")
    report.append("Direct coordinate comparison requires transformation.")
    report.append("Phase 4 will address this using shared overlay colors as calibration points.")
    report.append("")

    report.append("## 6. Recommendations")
    report.append("")
    report.append("### 6.1 For High-Variance Names")
    report.append("1. Review if the name represents a broad category vs specific color")
    report.append("2. Consider splitting into sub-categories if meaningful")
    report.append("3. Use median instead of mean for robust centroid estimation")
    report.append("")

    report.append("### 6.2 For Consolidation")
    report.append("1. Weight by sample count when merging duplicate names")
    report.append("2. Use robust statistics (median, IQR) for outlier handling")
    report.append("3. Document variance for uncertainty quantification")
    report.append("")

    report.append("---")
    report.append("")
    report.append("*Generated by Phase 3: Pre-Consolidation Coordinate Analysis*")

    # Write report
    report_path = OUTPUT_DIR / "coordinate_analysis.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"   → Report: {report_path}")

    # Write JSON data
    json_output = {
        'summary': {
            'xkcd_names': len(xkcd_coords),
            'xkcd_samples': total_samples,
            'centore_overlays': len(centore_data),
            'centore_samples': total_centore,
            'high_variance_count': len(high_variance)
        },
        'xkcd_distribution': {
            'samples_per_name': {
                'min': min(counts),
                'max': max(counts),
                'mean': statistics.mean(counts),
                'median': statistics.median(counts)
            },
            'rgb_std': {
                'min': min(variances),
                'max': max(variances),
                'mean': statistics.mean(variances),
                'median': statistics.median(variances)
            }
        },
        'centore_stats': {
            overlay: {
                'count': stats['count'],
                'value_std': stats['value']['std'],
                'chroma_std': stats['chroma']['std'],
                'hue_std': stats['hue']['std'],
                'centroid_cartesian': centore_data[overlay].get('centroid_cartesian')
            }
            for overlay, stats in centore_stats.items()
        },
        'high_variance_names': high_variance[:100]  # Top 100
    }

    json_path = OUTPUT_DIR / "coordinate_analysis.json"
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   → Data: {json_path}")

    print(f"\nPhase 3 complete!")
    print(f"Analyzed {len(xkcd_coords):,} XKCD names and {len(centore_data):,} Centore overlays.")


if __name__ == "__main__":
    main()
