#!/usr/bin/env python3
"""
Phase 4: Calibration Analysis

Detects and characterizes systematic bias between Centore and XKCD data
using the 20+ shared overlay color names as calibration reference points.

Approach:
1. Extract Centore centroids for shared overlays (Munsell coordinates)
2. Compute XKCD aggregate RGB for same overlay names
3. Analyze differences in comparable metrics
4. Test for systematic vs random differences

Note: Full comparison requires RGB-to-Munsell conversion (MunsellSpace library).
This analysis documents the methodology and preliminary findings.
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

# Data sources
XKCD_COORDS_CACHE = OUTPUT_DIR / "xkcd_coordinates_cache.json"
CENTORE_NAMES_DIR = PROJECT_ROOT / "PolyhedronFilesJustNames"

# The 20 shared overlay colors mentioned in the PRD
SHARED_OVERLAYS = {
    'aqua', 'beige', 'coral', 'fuchsia', 'gold', 'lavender', 'lilac',
    'magenta', 'mauve', 'navy', 'peach', 'rose', 'rust', 'sand', 'tan',
    'taupe', 'teal', 'turquoise', 'violet', 'wine'
}

# Additional basic colors available in both datasets
BASIC_COLORS = {'blue', 'green', 'red', 'orange', 'yellow', 'purple', 'pink', 'brown', 'gray', 'white'}


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_xkcd_coordinates() -> dict:
    """Load XKCD RGB coordinates from cache."""
    if not XKCD_COORDS_CACHE.exists():
        print(f"Error: XKCD cache not found at {XKCD_COORDS_CACHE}")
        print("Run Phase 3 first to generate the cache.")
        return {}

    with open(XKCD_COORDS_CACHE, 'r') as f:
        cached = json.load(f)
    return {k: [tuple(v) for v in vals] for k, vals in cached.items()}


def load_centore_centroids() -> dict:
    """Load Centore overlay centroids from polyhedron files."""
    centroids = {}

    for txt_file in CENTORE_NAMES_DIR.glob("*.txt"):
        overlay_name = txt_file.stem.replace("PolyhedronDataFor", "").lower()

        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith("Centroid in Munsell coordinates:"):
                    munsell = line.split('\t')[-1].strip()
                    parsed = parse_munsell(munsell)
                    if parsed:
                        centroids[overlay_name] = {
                            'munsell_string': munsell,
                            **parsed
                        }
                elif line.startswith("Centroid in Cartesian coordinates:"):
                    parts = line.split('\t')[1:]
                    if len(parts) >= 3:
                        try:
                            if overlay_name in centroids:
                                centroids[overlay_name]['cartesian'] = (
                                    float(parts[0]), float(parts[1]), float(parts[2])
                                )
                        except (ValueError, IndexError):
                            pass

    return centroids


def parse_munsell(munsell_str: str) -> dict:
    """Parse Munsell notation to components."""
    if not munsell_str:
        return None

    pattern = re.compile(r'([\d.]+)([A-Z]+)\s+([\d.]+)/([\d.]+)')
    match = pattern.match(munsell_str)

    if match:
        hue_value = float(match.group(1))
        hue_letter = match.group(2)
        return {
            'hue_value': hue_value,
            'hue_letter': hue_letter,
            'hue_angle': munsell_hue_to_angle(hue_value, hue_letter),
            'value': float(match.group(3)),
            'chroma': float(match.group(4))
        }
    return None


def munsell_hue_to_angle(hue_value: float, hue_letter: str) -> float:
    """Convert Munsell hue to angle (0-360 degrees)."""
    hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
    if hue_letter not in hue_order:
        return None
    base_angle = hue_order.index(hue_letter) * 36
    return base_angle + (hue_value / 10) * 36


# ============================================================================
# RGB Analysis Functions
# ============================================================================

def compute_rgb_centroid(rgb_list: list) -> dict:
    """Compute RGB centroid and HSV conversion."""
    if not rgb_list:
        return None

    r_values = [c[0] for c in rgb_list]
    g_values = [c[1] for c in rgb_list]
    b_values = [c[2] for c in rgb_list]

    r_mean = statistics.mean(r_values)
    g_mean = statistics.mean(g_values)
    b_mean = statistics.mean(b_values)

    # Convert to HSV for hue comparison
    hsv = rgb_to_hsv(r_mean, g_mean, b_mean)

    return {
        'rgb': (r_mean, g_mean, b_mean),
        'rgb_int': (int(round(r_mean)), int(round(g_mean)), int(round(b_mean))),
        'hsv': hsv,
        'hue_angle': hsv['h'] * 360 if hsv['h'] is not None else None,
        'count': len(rgb_list),
        'r_std': statistics.stdev(r_values) if len(r_values) > 1 else 0,
        'g_std': statistics.stdev(g_values) if len(g_values) > 1 else 0,
        'b_std': statistics.stdev(b_values) if len(b_values) > 1 else 0
    }


def rgb_to_hsv(r: float, g: float, b: float) -> dict:
    """Convert RGB (0-255) to HSV (h: 0-1, s: 0-1, v: 0-1)."""
    r, g, b = r/255, g/255, b/255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c

    # Value
    v = max_c

    # Saturation
    s = diff / max_c if max_c > 0 else 0

    # Hue
    if diff == 0:
        h = None  # Undefined for achromatic
    elif max_c == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_c == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    return {
        'h': h / 360 if h is not None else None,
        's': s,
        'v': v
    }


def approximate_munsell_value_from_rgb(r: float, g: float, b: float) -> float:
    """
    Approximate Munsell Value from RGB.
    Uses simplified luminance formula.
    Munsell Value 0=black, 10=white.
    """
    # sRGB luminance
    luminance = 0.2126 * (r/255) + 0.7152 * (g/255) + 0.0722 * (b/255)
    # Approximate Munsell Value (simplified, not exact)
    return luminance * 10


def approximate_munsell_chroma_from_rgb(r: float, g: float, b: float) -> float:
    """
    Approximate Munsell Chroma from RGB.
    Uses saturation as proxy.
    """
    hsv = rgb_to_hsv(r, g, b)
    # Chroma roughly correlates with saturation * some scaling
    # Max Munsell chroma varies by hue, typically 10-16
    return hsv['s'] * 12  # Rough approximation


# ============================================================================
# Calibration Analysis Functions
# ============================================================================

def compare_color_coordinates(
    xkcd_centroid: dict,
    centore_centroid: dict,
    color_name: str
) -> dict:
    """
    Compare XKCD and Centore coordinates for a single color.
    Returns comparison metrics.
    """
    comparison = {
        'color': color_name,
        'xkcd_rgb': xkcd_centroid['rgb_int'],
        'xkcd_hue': xkcd_centroid['hue_angle'],
        'xkcd_count': xkcd_centroid['count'],
        'centore_munsell': centore_centroid.get('munsell_string'),
        'centore_hue': centore_centroid.get('hue_angle'),
        'centore_value': centore_centroid.get('value'),
        'centore_chroma': centore_centroid.get('chroma'),
    }

    # Compare hues (circular difference)
    if xkcd_centroid['hue_angle'] and centore_centroid.get('hue_angle'):
        hue_diff = xkcd_centroid['hue_angle'] - centore_centroid['hue_angle']
        # Normalize to [-180, 180]
        if hue_diff > 180:
            hue_diff -= 360
        elif hue_diff < -180:
            hue_diff += 360
        comparison['hue_difference'] = hue_diff
    else:
        comparison['hue_difference'] = None

    # Approximate value comparison
    rgb = xkcd_centroid['rgb']
    xkcd_value = approximate_munsell_value_from_rgb(*rgb)
    comparison['xkcd_value_approx'] = xkcd_value
    if centore_centroid.get('value'):
        comparison['value_difference'] = xkcd_value - centore_centroid['value']
    else:
        comparison['value_difference'] = None

    # Approximate chroma comparison
    xkcd_chroma = approximate_munsell_chroma_from_rgb(*rgb)
    comparison['xkcd_chroma_approx'] = xkcd_chroma
    if centore_centroid.get('chroma'):
        comparison['chroma_difference'] = xkcd_chroma - centore_centroid['chroma']
    else:
        comparison['chroma_difference'] = None

    return comparison


def analyze_systematic_bias(comparisons: list) -> dict:
    """
    Analyze comparisons for systematic bias patterns.
    Tests whether differences are consistent (systematic) vs random.
    """
    hue_diffs = [c['hue_difference'] for c in comparisons if c['hue_difference'] is not None]
    value_diffs = [c['value_difference'] for c in comparisons if c['value_difference'] is not None]
    chroma_diffs = [c['chroma_difference'] for c in comparisons if c['chroma_difference'] is not None]

    def analyze_bias(diffs, name):
        if not diffs:
            return {'name': name, 'n': 0, 'mean': None, 'std': None, 'systematic': None}

        mean = statistics.mean(diffs)
        std = statistics.stdev(diffs) if len(diffs) > 1 else 0

        # Test for systematic bias: is mean significantly different from 0?
        # Simple heuristic: |mean| > std/sqrt(n) suggests systematic
        n = len(diffs)
        se = std / math.sqrt(n) if n > 0 else 0
        t_stat = abs(mean) / se if se > 0 else 0

        return {
            'name': name,
            'n': n,
            'mean': mean,
            'std': std,
            'min': min(diffs),
            'max': max(diffs),
            't_statistic': t_stat,
            'systematic': t_stat > 2.0  # Rough threshold
        }

    return {
        'hue': analyze_bias(hue_diffs, 'Hue'),
        'value': analyze_bias(value_diffs, 'Value'),
        'chroma': analyze_bias(chroma_diffs, 'Chroma')
    }


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 4: Calibration Analysis")
    print("=" * 70)

    # Load data
    print("\n1. Loading data...")

    print("   Loading XKCD RGB coordinates...")
    xkcd_coords = load_xkcd_coordinates()
    print(f"   → Loaded {len(xkcd_coords):,} color names")

    print("   Loading Centore centroids...")
    centore_centroids = load_centore_centroids()
    print(f"   → Loaded {len(centore_centroids):,} overlay centroids")

    # Find shared colors
    print("\n2. Identifying shared colors...")
    shared_colors = set(xkcd_coords.keys()) & set(centore_centroids.keys())
    overlay_shared = shared_colors & SHARED_OVERLAYS
    basic_shared = shared_colors & BASIC_COLORS

    print(f"   → Shared overlay colors: {len(overlay_shared)} ({', '.join(sorted(overlay_shared))})")
    print(f"   → Shared basic colors: {len(basic_shared)} ({', '.join(sorted(basic_shared))})")

    # Compute XKCD centroids for shared colors
    print("\n3. Computing XKCD RGB centroids for shared colors...")
    xkcd_centroids = {}
    for color in shared_colors:
        if color in xkcd_coords:
            xkcd_centroids[color] = compute_rgb_centroid(xkcd_coords[color])

    print(f"   → Computed {len(xkcd_centroids)} centroids")

    # Compare coordinates
    print("\n4. Comparing coordinates...")
    comparisons = []
    for color in sorted(shared_colors):
        if color in xkcd_centroids and color in centore_centroids:
            comp = compare_color_coordinates(
                xkcd_centroids[color],
                centore_centroids[color],
                color
            )
            comparisons.append(comp)
            print(f"   {color}: hue_diff={comp['hue_difference']:.1f}°, "
                  f"value_diff={comp['value_difference']:.2f}, "
                  f"chroma_diff={comp['chroma_difference']:.2f}"
                  if comp['hue_difference'] is not None else f"   {color}: (achromatic)")

    # Analyze for systematic bias
    print("\n5. Analyzing systematic bias...")
    bias_analysis = analyze_systematic_bias(comparisons)

    for dim, analysis in bias_analysis.items():
        if analysis['n'] > 0:
            systematic = "YES" if analysis['systematic'] else "no"
            print(f"   {dim}: mean={analysis['mean']:.2f}, std={analysis['std']:.2f}, "
                  f"t={analysis['t_statistic']:.2f}, systematic={systematic}")

    # Generate report
    print("\n6. Generating outputs...")

    report = []
    report.append("# Phase 4: Calibration Analysis Report")
    report.append("")
    report.append("## 1. Executive Summary")
    report.append("")
    report.append("This analysis compares XKCD (RGB) and Centore (Munsell) color coordinates")
    report.append("using shared overlay color names as calibration reference points.")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Shared overlay colors | {len(overlay_shared)} |")
    report.append(f"| Shared basic colors | {len(basic_shared)} |")
    report.append(f"| Total comparisons | {len(comparisons)} |")
    report.append("")

    report.append("## 2. Methodology")
    report.append("")
    report.append("### 2.1 Coordinate Systems")
    report.append("- **XKCD**: RGB (0-255), from uncalibrated consumer monitors")
    report.append("- **Centore**: Munsell HVC, from spectrophotometer measurements")
    report.append("")
    report.append("### 2.2 Comparison Approach")
    report.append("1. Compute XKCD RGB centroid for each shared color name")
    report.append("2. Extract Centore Munsell centroid from polyhedron data")
    report.append("3. Convert RGB to approximate Munsell-comparable metrics:")
    report.append("   - **Hue**: RGB → HSV → Hue angle (0-360°)")
    report.append("   - **Value**: RGB luminance → approximate Munsell Value (0-10)")
    report.append("   - **Chroma**: HSV saturation → approximate Munsell Chroma")
    report.append("4. Compute differences and test for systematic bias")
    report.append("")
    report.append("### 2.3 Limitations")
    report.append("- RGB-to-Munsell conversion is approximate")
    report.append("- XKCD monitors were uncalibrated (random viewing conditions)")
    report.append("- Centore uses illuminant C; sRGB assumes D65")
    report.append("- Full analysis requires proper colorimetric conversion")
    report.append("")

    report.append("## 3. Calibration Point Comparison")
    report.append("")
    report.append("| Color | XKCD RGB | Centore Munsell | Hue Δ | Value Δ | Chroma Δ | XKCD n |")
    report.append("|-------|----------|-----------------|-------|---------|----------|--------|")

    for comp in comparisons:
        rgb = f"({comp['xkcd_rgb'][0]},{comp['xkcd_rgb'][1]},{comp['xkcd_rgb'][2]})"
        munsell = comp['centore_munsell'] or '-'
        hue_d = f"{comp['hue_difference']:.1f}" if comp['hue_difference'] is not None else '-'
        val_d = f"{comp['value_difference']:.2f}" if comp['value_difference'] is not None else '-'
        chr_d = f"{comp['chroma_difference']:.2f}" if comp['chroma_difference'] is not None else '-'
        report.append(f"| {comp['color']} | {rgb} | {munsell} | {hue_d}° | {val_d} | {chr_d} | {comp['xkcd_count']:,} |")
    report.append("")

    report.append("## 4. Systematic Bias Analysis")
    report.append("")
    report.append("### 4.1 Test for Systematic Differences")
    report.append("")
    report.append("| Dimension | n | Mean Δ | Std | t-stat | Systematic? |")
    report.append("|-----------|---|--------|-----|--------|-------------|")

    for dim, analysis in bias_analysis.items():
        if analysis['n'] > 0:
            systematic = "**YES**" if analysis['systematic'] else "no"
            report.append(f"| {analysis['name']} | {analysis['n']} | {analysis['mean']:.2f} | "
                         f"{analysis['std']:.2f} | {analysis['t_statistic']:.2f} | {systematic} |")
    report.append("")

    report.append("### 4.2 Interpretation")
    report.append("")

    # Interpret hue bias
    hue_analysis = bias_analysis['hue']
    if hue_analysis['n'] > 0:
        if hue_analysis['systematic']:
            direction = "redder" if hue_analysis['mean'] > 0 else "bluer"
            report.append(f"**Hue**: Systematic bias detected. XKCD colors appear {direction} ")
            report.append(f"than Centore by ~{abs(hue_analysis['mean']):.1f}° on average.")
        else:
            report.append("**Hue**: No significant systematic bias. Differences appear random.")
    report.append("")

    # Interpret value bias
    value_analysis = bias_analysis['value']
    if value_analysis['n'] > 0:
        if value_analysis['systematic']:
            direction = "lighter" if value_analysis['mean'] > 0 else "darker"
            report.append(f"**Value**: Systematic bias detected. XKCD colors appear {direction} ")
            report.append(f"than Centore by ~{abs(value_analysis['mean']):.2f} Munsell Value units.")
        else:
            report.append("**Value**: No significant systematic bias. Differences appear random.")
    report.append("")

    # Interpret chroma bias
    chroma_analysis = bias_analysis['chroma']
    if chroma_analysis['n'] > 0:
        if chroma_analysis['systematic']:
            direction = "more saturated" if chroma_analysis['mean'] > 0 else "less saturated"
            report.append(f"**Chroma**: Systematic bias detected. XKCD colors appear {direction} ")
            report.append(f"than Centore by ~{abs(chroma_analysis['mean']):.2f} Chroma units.")
        else:
            report.append("**Chroma**: No significant systematic bias. Differences appear random.")
    report.append("")

    report.append("## 5. Recommendations")
    report.append("")
    report.append("### 5.1 If Systematic Bias Found")
    report.append("1. Consider applying a global correction transformation")
    report.append("2. Use regression analysis to fit correction parameters")
    report.append("3. Validate correction on held-out colors")
    report.append("")
    report.append("### 5.2 If No Systematic Bias")
    report.append("1. Differences may be due to random monitor variation")
    report.append("2. Consider using robust statistics (median) for aggregation")
    report.append("3. Document uncertainty without applying corrections")
    report.append("")
    report.append("### 5.3 For Full Analysis")
    report.append("1. Install MunsellSpace Python library for accurate RGB→Munsell conversion")
    report.append("2. Use colorimetric transforms (sRGB → XYZ → Munsell)")
    report.append("3. Account for illuminant differences (D65 vs C)")
    report.append("")

    report.append("## 6. Uncertainty Budget")
    report.append("")
    report.append("| Source | Impact | Mitigation |")
    report.append("|--------|--------|------------|")
    report.append("| Uncalibrated monitors | High | Use large sample sizes |")
    report.append("| RGB-Munsell approximation | Medium | Use proper conversion |")
    report.append("| Illuminant difference | Low-Medium | Apply chromatic adaptation |")
    report.append("| Sample size variation | Low | Weight by sample count |")
    report.append("")

    report.append("---")
    report.append("")
    report.append("*Generated by Phase 4: Calibration Analysis*")

    # Write report
    report_path = OUTPUT_DIR / "calibration_analysis.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"   → Report: {report_path}")

    # Write JSON data
    json_output = {
        'summary': {
            'shared_overlays': list(overlay_shared),
            'shared_basics': list(basic_shared),
            'total_comparisons': len(comparisons)
        },
        'comparisons': comparisons,
        'bias_analysis': bias_analysis,
        'xkcd_centroids': {
            k: {
                'rgb': v['rgb'],
                'hue_angle': v['hue_angle'],
                'count': v['count']
            }
            for k, v in xkcd_centroids.items()
        },
        'centore_centroids': {
            k: {
                'munsell': v.get('munsell_string'),
                'hue_angle': v.get('hue_angle'),
                'value': v.get('value'),
                'chroma': v.get('chroma')
            }
            for k, v in centore_centroids.items()
        }
    }

    json_path = OUTPUT_DIR / "calibration_analysis.json"
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   → Data: {json_path}")

    print(f"\nPhase 4 complete!")
    print(f"Compared {len(comparisons)} shared colors for calibration analysis.")


if __name__ == "__main__":
    main()
