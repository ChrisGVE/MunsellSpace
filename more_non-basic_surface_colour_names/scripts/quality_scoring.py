#!/usr/bin/env python3
"""
Phase 3: High-Confidence Assignment Quality Criteria

Implements quality scoring combining:
1. NLP confidence (SBERT similarity)
2. Colorimetric consistency (hue range checks)
3. Source reliability weighting
"""

import json
import csv
import math
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent

# Expected hue ranges per family (in Munsell hue degrees, 0-100 scale)
# Based on Centore's research and color science consensus
# Format: (center_hue, tolerance_degrees)
FAMILY_HUE_RANGES = {
    # Basic colors
    "red": (5.0, 10),       # 5R center, ±10 hue steps
    "orange": (15.0, 8),    # 5YR center
    "yellow": (25.0, 8),    # 5Y center
    "green": (45.0, 20),    # 5G center, wider range
    "blue": (70.0, 15),     # 5PB center
    "purple": (85.0, 10),   # 5P center
    "brown": (12.0, 12),    # YR region
    "gray": (None, None),   # Neutral, no hue check
    "white": (None, None),  # Neutral, no hue check
    "pink": (95.0, 12),     # RP region

    # Non-basic Centore families
    "aqua": (55.0, 10),     # BG region
    "beige": (20.0, 10),    # Y-YR region
    "coral": (8.0, 8),      # R-YR region
    "fuchsia": (92.0, 8),   # RP region
    "gold": (22.0, 6),      # Y region
    "lavender": (78.0, 10), # PB-P region
    "lilac": (82.0, 8),     # P region
    "magenta": (90.0, 10),  # RP region
    "mauve": (85.0, 12),    # P-RP region
    "navy": (70.0, 8),      # PB region (dark)
    "peach": (15.0, 8),     # YR region
    "rose": (97.0, 8),      # RP region
    "rust": (10.0, 8),      # R-YR region
    "sand": (20.0, 10),     # Y-YR region
    "tan": (18.0, 10),      # YR region
    "taupe": (15.0, 15),    # YR-neutral region
    "teal": (55.0, 8),      # BG region
    "turquoise": (52.0, 8), # BG region
    "violet": (78.0, 8),    # PB-P region
    "wine": (98.0, 8),      # RP-R region (dark)

    # New candidate families
    "indigo": (72.0, 8),    # PB region
    "maroon": (2.0, 8),     # R region (dark)
    "lime": (38.0, 8),      # GY region
    "plum": (88.0, 8),      # P-RP region
    "aquamarine": (52.0, 10), # BG region
}

# Source reliability weights
SOURCE_RELIABILITY = {
    # Native spectrophotometer surface colors (highest reliability)
    "Golden Artist Colors": 1.0,
    "Williamsburg": 1.0,

    # Surface standards with RGB proxy (high reliability)
    "NCS": 0.9,
    "Pantone TCX Textile": 0.9,
    "Pantone PMS Solid Coated": 0.85,
    "Pantone Mixed": 0.85,
    "RAL Classic": 0.85,
    "RHS Colour Chart": 0.8,

    # Markers (medium-high, designed for surface use)
    "Copic": 0.75,
    "Ohuhu": 0.75,

    # Research estimates (medium reliability)
    "Gemological estimates": 0.6,

    # Screen/web sources (lower reliability for surface color)
    "xkcd_survey": 0.5,
    "xkcd_curated": 0.55,
    "colorhexa": 0.5,
    "meodai": 0.5,
    "wikipedia": 0.55,
    "colorname_com": 0.5,

    # Default for unknown sources
    "default": 0.5,
}


def munsell_hue_to_numeric(hue_str):
    """Convert Munsell hue string to numeric (0-100 scale).

    Munsell hues: R, YR, Y, GY, G, BG, B, PB, P, RP (10 major hues)
    Each major hue spans 10 steps (e.g., 5R, 10R, 5YR, etc.)
    Full circle = 100 units
    """
    if not hue_str or hue_str == "N":
        return None

    hue_map = {
        "R": 0, "YR": 10, "Y": 20, "GY": 30, "G": 40,
        "BG": 50, "B": 60, "PB": 70, "P": 80, "RP": 90
    }

    # Parse hue string like "5R", "10YR", "7.5PB"
    import re
    match = re.match(r"(\d+\.?\d*)([A-Z]+)", hue_str)
    if not match:
        return None

    num_part = float(match.group(1))
    hue_part = match.group(2)

    if hue_part not in hue_map:
        return None

    base = hue_map[hue_part]
    return (base + num_part) % 100


def compute_hue_distance(hue1, hue2):
    """Compute circular distance between two hues (0-100 scale)."""
    if hue1 is None or hue2 is None:
        return None

    diff = abs(hue1 - hue2)
    return min(diff, 100 - diff)


def compute_nlp_confidence(similarity_score):
    """Compute NLP confidence from SBERT similarity score.

    The similarity_score is already 0-1, so we use it directly.
    """
    if similarity_score is None:
        return 0.0
    return max(0.0, min(1.0, float(similarity_score)))


def compute_colorimetric_consistency(hue_numeric, family):
    """Compute colorimetric consistency based on hue match.

    Returns 1.0 if hue is within expected range, decreasing score for
    larger deviations.
    """
    if family not in FAMILY_HUE_RANGES:
        return 0.5  # Unknown family, neutral score

    center_hue, tolerance = FAMILY_HUE_RANGES[family]

    if center_hue is None:
        # Neutral family (gray, white) - check for low chroma instead
        return 1.0  # Will be handled separately

    if hue_numeric is None:
        return 0.5  # No hue data, neutral score

    distance = compute_hue_distance(hue_numeric, center_hue)

    if distance <= tolerance:
        return 1.0
    elif distance <= tolerance * 2:
        # Linear decay from 1.0 to 0.5
        excess = distance - tolerance
        return 1.0 - 0.5 * (excess / tolerance)
    else:
        # Rapid decay for very off-hue samples
        return max(0.1, 0.5 - 0.4 * ((distance - tolerance * 2) / tolerance))


def compute_source_reliability(sources_str):
    """Compute source reliability weight from source list.

    Takes average reliability of all sources.
    """
    if not sources_str:
        return SOURCE_RELIABILITY["default"]

    sources = sources_str.split("|")
    weights = []

    for source in sources:
        source = source.strip()
        if source in SOURCE_RELIABILITY:
            weights.append(SOURCE_RELIABILITY[source])
        else:
            # Try partial match
            matched = False
            for key, value in SOURCE_RELIABILITY.items():
                if key.lower() in source.lower() or source.lower() in key.lower():
                    weights.append(value)
                    matched = True
                    break
            if not matched:
                weights.append(SOURCE_RELIABILITY["default"])

    return sum(weights) / len(weights) if weights else SOURCE_RELIABILITY["default"]


def compute_quality_score(nlp_conf, colorimetric_cons, source_rel,
                          w_nlp=0.4, w_color=0.4, w_source=0.2):
    """Compute combined quality score.

    Default weights: NLP 40%, Colorimetric 40%, Source 20%
    """
    return (w_nlp * nlp_conf +
            w_color * colorimetric_cons +
            w_source * source_rel)


def analyze_quality_distribution(samples):
    """Analyze quality score distribution across samples."""
    thresholds = [0.5, 0.6, 0.7, 0.8]
    results = {}

    for thresh in thresholds:
        passing = [s for s in samples if s["quality_score"] >= thresh]
        results[thresh] = {
            "count": len(passing),
            "percentage": 100 * len(passing) / len(samples) if samples else 0,
            "families": len(set(s["family"] for s in passing))
        }

    return results


def process_screen_assignments():
    """Process screen color family assignments with quality scoring."""
    input_file = BASE_DIR / "datasets/phase6/family_assignments_munsell.csv"
    output_dir = BASE_DIR / "datasets/quality_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    samples = []

    with open(input_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse existing data
            similarity = float(row.get("similarity_score", 0) or 0)
            family = row.get("assigned_family", "")
            hue_str = row.get("hue_str", "")
            sources = row.get("sources", "")

            # Compute hue numeric
            hue_numeric = munsell_hue_to_numeric(hue_str)

            # Compute quality components
            nlp_conf = compute_nlp_confidence(similarity)
            color_cons = compute_colorimetric_consistency(hue_numeric, family)
            source_rel = compute_source_reliability(sources)

            # Compute combined score
            quality = compute_quality_score(nlp_conf, color_cons, source_rel)

            samples.append({
                "name": row.get("name", ""),
                "hex": row.get("hex", ""),
                "family": family,
                "hue_str": hue_str,
                "hue_numeric": hue_numeric,
                "nlp_confidence": nlp_conf,
                "colorimetric_consistency": color_cons,
                "source_reliability": source_rel,
                "quality_score": quality,
                "sources": sources
            })

    return samples


def process_surface_colors():
    """Process surface colors with quality scoring."""
    input_file = BASE_DIR / "datasets/surface_colors/consolidated_surface_colors.csv"
    output_dir = BASE_DIR / "datasets/quality_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    samples = []

    with open(input_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            family = row.get("color_family", "Unknown")
            if family == "Unknown":
                continue

            source = row.get("source", "")
            hue_str = row.get("munsell_h", "")

            # Compute hue numeric
            hue_numeric = munsell_hue_to_numeric(hue_str)

            # For surface colors, NLP confidence is based on family assignment quality
            # We'll use a heuristic: well-named colors get higher confidence
            name = row.get("color_name", "").lower()
            if family.lower() in name:
                nlp_conf = 0.95
            else:
                nlp_conf = 0.7  # Default for surface colors without explicit family name

            color_cons = compute_colorimetric_consistency(hue_numeric, family.lower())
            source_rel = compute_source_reliability(source)

            quality = compute_quality_score(nlp_conf, color_cons, source_rel)

            samples.append({
                "name": row.get("color_name", ""),
                "hex": row.get("hex", ""),
                "family": family.lower(),
                "hue_str": hue_str,
                "hue_numeric": hue_numeric,
                "nlp_confidence": nlp_conf,
                "colorimetric_consistency": color_cons,
                "source_reliability": source_rel,
                "quality_score": quality,
                "source": source
            })

    return samples


def generate_sensitivity_report(screen_samples, surface_samples):
    """Generate threshold sensitivity analysis report."""
    report = []
    report.append("# Quality Scoring Threshold Sensitivity Analysis")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    report.append("## Methodology")
    report.append("")
    report.append("Quality score combines three components:")
    report.append("- **NLP Confidence (40%)**: SBERT similarity score for family assignment")
    report.append("- **Colorimetric Consistency (40%)**: Hue within expected family range")
    report.append("- **Source Reliability (20%)**: Data source quality weighting")
    report.append("")

    # Screen data analysis
    report.append("## Screen Color Data")
    report.append("")
    report.append(f"Total samples: {len(screen_samples)}")
    report.append("")

    screen_dist = analyze_quality_distribution(screen_samples)
    report.append("| Threshold | Samples | Percentage | Families |")
    report.append("|-----------|---------|------------|----------|")
    for thresh, data in sorted(screen_dist.items()):
        report.append(f"| {thresh} | {data['count']} | {data['percentage']:.1f}% | {data['families']} |")
    report.append("")

    # Per-family breakdown
    report.append("### Per-Family Quality Summary (Threshold 0.6)")
    report.append("")
    family_stats = defaultdict(lambda: {"count": 0, "passing": 0, "avg_score": 0})
    for s in screen_samples:
        fam = s["family"]
        family_stats[fam]["count"] += 1
        family_stats[fam]["avg_score"] += s["quality_score"]
        if s["quality_score"] >= 0.6:
            family_stats[fam]["passing"] += 1

    for fam in family_stats:
        family_stats[fam]["avg_score"] /= family_stats[fam]["count"]

    report.append("| Family | Total | Pass (≥0.6) | Pass Rate | Avg Score |")
    report.append("|--------|-------|-------------|-----------|-----------|")
    for fam in sorted(family_stats.keys()):
        stats = family_stats[fam]
        rate = 100 * stats["passing"] / stats["count"]
        report.append(f"| {fam} | {stats['count']} | {stats['passing']} | {rate:.1f}% | {stats['avg_score']:.3f} |")
    report.append("")

    # Surface data analysis
    report.append("## Surface Color Data")
    report.append("")
    report.append(f"Total samples: {len(surface_samples)}")
    report.append("")

    surface_dist = analyze_quality_distribution(surface_samples)
    report.append("| Threshold | Samples | Percentage | Families |")
    report.append("|-----------|---------|------------|----------|")
    for thresh, data in sorted(surface_dist.items()):
        report.append(f"| {thresh} | {data['count']} | {data['percentage']:.1f}% | {data['families']} |")
    report.append("")

    # Source reliability breakdown
    report.append("## Source Reliability Weights")
    report.append("")
    report.append("| Source | Weight | Category |")
    report.append("|--------|--------|----------|")
    for source, weight in sorted(SOURCE_RELIABILITY.items(), key=lambda x: -x[1]):
        if source == "default":
            continue
        if weight >= 0.9:
            cat = "Spectrophotometer"
        elif weight >= 0.75:
            cat = "Surface Standard"
        elif weight >= 0.6:
            cat = "Research"
        else:
            cat = "Screen/Web"
        report.append(f"| {source} | {weight} | {cat} |")
    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("Based on the sensitivity analysis:")
    report.append("")

    # Determine best threshold
    best_thresh = 0.6
    for thresh in [0.5, 0.6, 0.7]:
        if screen_dist[thresh]["families"] >= 30:
            best_thresh = thresh

    report.append(f"**Recommended threshold: {best_thresh}**")
    report.append("")
    report.append(f"- Retains {screen_dist[best_thresh]['count']} screen samples ({screen_dist[best_thresh]['percentage']:.1f}%)")
    report.append(f"- Covers {screen_dist[best_thresh]['families']} color families")
    report.append("")

    return "\n".join(report)


def main():
    """Run quality scoring analysis."""
    print("Phase 3: Quality Scoring Analysis")
    print("=" * 50)

    output_dir = BASE_DIR / "datasets/quality_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process screen assignments
    print("Processing screen color assignments...")
    screen_samples = process_screen_assignments()
    print(f"  Processed {len(screen_samples)} screen samples")

    # Save screen quality scores
    screen_output = output_dir / "screen_quality_scores.json"
    with open(screen_output, "w") as f:
        json.dump(screen_samples, f, indent=2)
    print(f"  Saved: {screen_output}")

    # Process surface colors
    print("Processing surface colors...")
    surface_samples = process_surface_colors()
    print(f"  Processed {len(surface_samples)} surface samples")

    # Save surface quality scores
    surface_output = output_dir / "surface_quality_scores.json"
    with open(surface_output, "w") as f:
        json.dump(surface_samples, f, indent=2)
    print(f"  Saved: {surface_output}")

    # Generate sensitivity report
    print("Generating sensitivity report...")
    report = generate_sensitivity_report(screen_samples, surface_samples)
    report_path = output_dir / "threshold_sensitivity.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Saved: {report_path}")

    # Print summary
    print()
    print("Summary:")
    screen_dist = analyze_quality_distribution(screen_samples)
    for thresh, data in sorted(screen_dist.items()):
        print(f"  Screen @ {thresh}: {data['count']} samples ({data['percentage']:.1f}%), {data['families']} families")


if __name__ == "__main__":
    main()
