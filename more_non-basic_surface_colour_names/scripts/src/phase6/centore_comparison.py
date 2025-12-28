#!/usr/bin/env python3
"""
Phase 6.5: Centore Comparison Analysis

Compares the polyhedra constructed from screen colors (RGB) with
Centore's original polyhedra derived from surface colors (CAUS samples).

Key analyses:
1. Centroid shift: How far did the center move?
2. Volume change: Did the family expand or contract?
3. New families: Analyze the 5 candidates not in Centore

Input: datasets/phase6/polyhedra/
       Centore data from semantic_overlay.rs centroids
Output: datasets/phase6/centore_comparison.json
        datasets/phase6/centore_comparison_report.md
"""

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
PHASE6_DIR = DATASETS_DIR / "phase6"
POLYHEDRA_DIR = PHASE6_DIR / "polyhedra"


# Centore centroids from semantic_overlay.rs (Munsell notation)
# Format: "HueLetter HueNumber Value/Chroma"
CENTORE_CENTROIDS_MUNSELL = {
    # 20 Non-basic
    "aqua": "7.4BG 6.2/3.4",
    "beige": "6.7YR 6.1/3.4",
    "coral": "6.5R 5.8/8.3",
    "fuchsia": "4.8RP 4.1/10.3",
    "gold": "9.8YR 6.4/7.4",
    "lavender": "5.6P 5.4/4.8",
    "lilac": "7.8P 5.6/4.8",
    "magenta": "3.8RP 3.4/9.4",
    "mauve": "1.2RP 5.1/3.9",
    "navy": "7.3PB 2.1/3.6",
    "peach": "2.9YR 7.0/5.9",
    "rose": "0.5R 5.0/7.7",
    "rust": "9.4R 3.9/7.4",
    "sand": "7.6YR 6.3/3.2",
    "tan": "6.3YR 5.2/4.1",
    "taupe": "3.2YR 4.7/1.4",
    "teal": "1.6B 3.3/4.5",
    "turquoise": "1.6B 5.5/5.9",
    "violet": "7.0P 3.8/6.2",
    "wine": "2.7R 3.0/4.9",
    # 10 Basic
    "blue": "1.8PB 4.8/5.0",
    "brown": "2.2YR 3.5/3.4",
    "gray": "3.2Y 5.0/1.9",
    "green": "2.3G 5.0/4.0",
    "orange": "2.5YR 6.1/10.3",
    "pink": "0.7R 6.1/7.2",
    "purple": "4.3P 3.0/6.5",
    "red": "5.1R 3.9/9.6",
    "white": "2.2Y 8.3/1.6",
    "yellow": "3.9Y 7.8/8.0",
}

# Centore sample counts from centore_polyhedra.rs
CENTORE_SAMPLE_COUNTS = {
    "aqua": 119, "beige": 277, "coral": 215, "fuchsia": 46,
    "gold": 362, "lavender": 47, "lilac": 78, "magenta": 25,
    "mauve": 181, "navy": 100, "peach": 102, "rose": 467,
    "rust": 93, "sand": 123, "tan": 129, "taupe": 76,
    "teal": 43, "turquoise": 121, "violet": 178, "wine": 83,
    "blue": 1673, "brown": 536, "gray": 485, "green": 1296,
    "orange": 378, "pink": 594, "purple": 226, "red": 662,
    "white": 152, "yellow": 394,
}

# Centore vertex/face counts from tests
CENTORE_POLYHEDRA_STATS = {
    "aqua": (28, 52), "beige": (32, 60), "coral": (34, 64), "fuchsia": (18, 32),
    "gold": (47, 90), "lavender": (15, 26), "lilac": (20, 36), "magenta": (7, 10),
    "mauve": (44, 84), "navy": (24, 44), "peach": (28, 52), "rose": (51, 98),
    "rust": (24, 44), "sand": (24, 44), "tan": (27, 50), "taupe": (23, 42),
    "teal": (15, 26), "turquoise": (26, 48), "violet": (31, 58), "wine": (21, 38),
    "blue": (66, 128), "brown": (33, 62), "gray": (39, 74), "green": (66, 128),
    "orange": (46, 88), "pink": (55, 106), "purple": (45, 86), "red": (39, 74),
    "white": (24, 44), "yellow": (35, 66),
}


def parse_munsell_to_cartesian(notation: str) -> Tuple[float, float, float]:
    """Convert Munsell notation to Cartesian coordinates."""
    import re

    # Parse: "7.4BG 6.2/3.4" -> hue=57.4, value=6.2, chroma=3.4
    # Hue order: R=0, YR=10, Y=20, GY=30, G=40, BG=50, B=60, PB=70, P=80, RP=90

    hue_bases = {'R': 0, 'YR': 10, 'Y': 20, 'GY': 30, 'G': 40, 'BG': 50, 'B': 60, 'PB': 70, 'P': 80, 'RP': 90}

    # Handle neutral colors
    if notation.startswith('N'):
        value = float(notation[1:].split('/')[0])
        return (0.0, 0.0, value)

    # Parse chromatic: "7.4BG 6.2/3.4"
    pattern = r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)'
    match = re.match(pattern, notation)
    if not match:
        return (0.0, 0.0, 5.0)  # Default

    hue_num = float(match.group(1))
    hue_letter = match.group(2)
    value = float(match.group(3))
    chroma = float(match.group(4))

    # Convert to continuous hue (0-100)
    hue_100 = hue_bases[hue_letter] + hue_num

    # Convert to Cartesian (Centore's formula)
    angle = hue_100 * math.pi / 50  # Convert 0-100 to radians
    x = chroma * math.cos(angle)
    y = chroma * math.sin(angle)
    z = value

    return (x, y, z)


def load_our_polyhedra() -> Dict[str, Dict]:
    """Load our constructed polyhedra."""
    polyhedra = {}

    for json_path in POLYHEDRA_DIR.glob("*_polyhedron.json"):
        with open(json_path) as f:
            data = json.load(f)
            polyhedra[data["family"]] = data

    return polyhedra


def euclidean_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """Compute Euclidean distance between two 3D points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def compute_comparisons(our_polyhedra: Dict[str, Dict]) -> Dict:
    """Compare our polyhedra with Centore's."""
    comparisons = {
        "centore_30": {},
        "new_5": {},
        "summary": {}
    }

    # Compare Centore 30
    for family, notation in CENTORE_CENTROIDS_MUNSELL.items():
        centore_centroid = parse_munsell_to_cartesian(notation)
        centore_verts, centore_faces = CENTORE_POLYHEDRA_STATS[family]
        centore_samples = CENTORE_SAMPLE_COUNTS[family]

        if family in our_polyhedra:
            our = our_polyhedra[family]
            our_centroid = tuple(our["centroid"])

            # Compute metrics
            centroid_shift = euclidean_distance(centore_centroid, our_centroid)

            # Direction of shift (in Munsell terms)
            dx = our_centroid[0] - centore_centroid[0]
            dy = our_centroid[1] - centore_centroid[1]
            dz = our_centroid[2] - centore_centroid[2]

            comparisons["centore_30"][family] = {
                "centore_centroid": list(centore_centroid),
                "our_centroid": list(our_centroid),
                "centroid_shift": round(centroid_shift, 4),
                "shift_x": round(dx, 4),
                "shift_y": round(dy, 4),
                "shift_z": round(dz, 4),  # Value shift (+ = lighter, - = darker)
                "centore_vertices": centore_verts,
                "our_vertices": our["vertex_count"],
                "centore_faces": centore_faces,
                "our_faces": our["face_count"],
                "centore_samples": centore_samples,
                "our_samples": our["sample_count"],
                "our_volume": round(our["volume"], 2),
                "sample_ratio": round(our["sample_count"] / centore_samples, 2) if centore_samples else 0,
            }
        else:
            comparisons["centore_30"][family] = {
                "error": "Not in our polyhedra",
                "centore_centroid": list(centore_centroid),
            }

    # New 5 candidates (no Centore reference)
    new_families = ["indigo", "maroon", "lime", "plum", "aquamarine"]
    for family in new_families:
        if family in our_polyhedra:
            our = our_polyhedra[family]
            comparisons["new_5"][family] = {
                "centroid": list(our["centroid"]),
                "vertices": our["vertex_count"],
                "faces": our["face_count"],
                "volume": round(our["volume"], 2),
                "samples": our["sample_count"],
                "point_count": our["point_count"],
            }

    # Summary statistics
    shifts = [c["centroid_shift"] for c in comparisons["centore_30"].values() if "centroid_shift" in c]
    value_shifts = [c["shift_z"] for c in comparisons["centore_30"].values() if "shift_z" in c]

    comparisons["summary"] = {
        "centore_families_compared": len([c for c in comparisons["centore_30"].values() if "centroid_shift" in c]),
        "new_families": len(comparisons["new_5"]),
        "avg_centroid_shift": round(sum(shifts) / len(shifts), 4) if shifts else 0,
        "max_centroid_shift": round(max(shifts), 4) if shifts else 0,
        "min_centroid_shift": round(min(shifts), 4) if shifts else 0,
        "avg_value_shift": round(sum(value_shifts) / len(value_shifts), 4) if value_shifts else 0,
        "families_shifted_lighter": sum(1 for v in value_shifts if v > 0.1),
        "families_shifted_darker": sum(1 for v in value_shifts if v < -0.1),
    }

    return comparisons


def generate_report(comparisons: Dict) -> str:
    """Generate a markdown report."""
    lines = [
        "# Phase 6.5: Centore Comparison Analysis",
        "",
        "Comparison of polyhedra constructed from screen colors (RGB) with",
        "Centore's polyhedra from spectrophotometer-measured surface colors (CAUS).",
        "",
        "## Summary",
        "",
        f"- Centore families compared: {comparisons['summary']['centore_families_compared']}",
        f"- New candidate families: {comparisons['summary']['new_families']}",
        f"- Average centroid shift: {comparisons['summary']['avg_centroid_shift']:.2f} Munsell units",
        f"- Maximum centroid shift: {comparisons['summary']['max_centroid_shift']:.2f} Munsell units",
        f"- Families shifted lighter: {comparisons['summary']['families_shifted_lighter']}",
        f"- Families shifted darker: {comparisons['summary']['families_shifted_darker']}",
        "",
        "## Centore 30 Comparison",
        "",
        "| Family | Shift | Value Δ | Our Vertices | Centore Vertices | Our Samples | Centore Samples |",
        "|--------|-------|---------|--------------|------------------|-------------|-----------------|",
    ]

    # Sort by shift magnitude
    sorted_families = sorted(
        [(f, c) for f, c in comparisons["centore_30"].items() if "centroid_shift" in c],
        key=lambda x: -x[1]["centroid_shift"]
    )

    for family, data in sorted_families:
        value_sign = "+" if data["shift_z"] > 0 else ""
        lines.append(
            f"| {family} | {data['centroid_shift']:.2f} | {value_sign}{data['shift_z']:.2f} | "
            f"{data['our_vertices']} | {data['centore_vertices']} | "
            f"{data['our_samples']:,} | {data['centore_samples']:,} |"
        )

    lines.extend([
        "",
        "## New Candidate Families",
        "",
        "These 5 families are not in Centore's original 30:",
        "",
        "| Family | Centroid (x,y,z) | Volume | Vertices | Samples |",
        "|--------|------------------|--------|----------|---------|",
    ])

    for family, data in comparisons["new_5"].items():
        centroid = f"({data['centroid'][0]:.1f}, {data['centroid'][1]:.1f}, {data['centroid'][2]:.1f})"
        lines.append(
            f"| {family} | {centroid} | {data['volume']:.0f} | {data['vertices']} | {data['samples']:,} |"
        )

    lines.extend([
        "",
        "## Key Findings",
        "",
        "### Centroid Shifts",
        "",
    ])

    # Find largest shifts
    largest_shifts = sorted_families[:5]
    lines.append("Families with largest centroid shifts (screen → surface difference):")
    for family, data in largest_shifts:
        lines.append(f"- **{family}**: {data['centroid_shift']:.2f} units")

    lines.extend([
        "",
        "### Value (Lightness) Trends",
        "",
    ])

    lighter = [(f, c) for f, c in comparisons["centore_30"].items() if c.get("shift_z", 0) > 0.5]
    darker = [(f, c) for f, c in comparisons["centore_30"].items() if c.get("shift_z", 0) < -0.5]

    if lighter:
        lines.append("Families perceived lighter on screen than surface:")
        for family, data in sorted(lighter, key=lambda x: -x[1]["shift_z"])[:5]:
            lines.append(f"- {family}: +{data['shift_z']:.2f} value")

    if darker:
        lines.append("")
        lines.append("Families perceived darker on screen than surface:")
        for family, data in sorted(darker, key=lambda x: x[1]["shift_z"])[:5]:
            lines.append(f"- {family}: {data['shift_z']:.2f} value")

    lines.extend([
        "",
        "## Interpretation",
        "",
        "The systematic differences between screen colors and surface colors reflect:",
        "",
        "1. **Emissive vs Reflective**: Screen colors are additive (light emission),",
        "   surface colors are subtractive (light reflection)",
        "",
        "2. **Crowdsourced Perception**: XKCD data represents how people *describe* colors",
        "   on screens, which may differ from standardized color naming",
        "",
        "3. **Cultural Factors**: Color names have semantic associations beyond colorimetric",
        "   properties (e.g., 'navy' evokes the military uniform)",
        "",
        "This 'dry run' pipeline establishes infrastructure for future analysis with",
        "properly measured surface color data.",
    ])

    return "\n".join(lines)


def main():
    """Main entry point."""
    print("Phase 6.5: Centore Comparison Analysis")
    print("=" * 50)

    # Load our polyhedra
    our_polyhedra = load_our_polyhedra()
    print(f"Loaded {len(our_polyhedra)} of our polyhedra")

    # Compute comparisons
    comparisons = compute_comparisons(our_polyhedra)

    # Save JSON
    json_path = PHASE6_DIR / "centore_comparison.json"
    with open(json_path, "w") as f:
        json.dump(comparisons, f, indent=2)
    print(f"Saved comparison data to {json_path}")

    # Generate and save report
    report = generate_report(comparisons)
    report_path = PHASE6_DIR / "centore_comparison_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved report to {report_path}")

    # Print summary
    print("\n" + "=" * 70)
    print("CENTORE COMPARISON SUMMARY")
    print("=" * 70)
    print(f"\nCentore families compared: {comparisons['summary']['centore_families_compared']}")
    print(f"New candidate families: {comparisons['summary']['new_families']}")
    print(f"\nAverage centroid shift: {comparisons['summary']['avg_centroid_shift']:.2f} Munsell units")
    print(f"Max centroid shift: {comparisons['summary']['max_centroid_shift']:.2f}")
    print(f"Families shifted lighter: {comparisons['summary']['families_shifted_lighter']}")
    print(f"Families shifted darker: {comparisons['summary']['families_shifted_darker']}")

    print(f"\n{'Family':<12} {'Shift':>8} {'Value Δ':>10} {'Our V':>8} {'Centore V':>10}")
    print("-" * 55)

    sorted_data = sorted(
        [(f, c) for f, c in comparisons["centore_30"].items() if "centroid_shift" in c],
        key=lambda x: -x[1]["centroid_shift"]
    )

    for family, data in sorted_data[:15]:
        print(f"{family:<12} {data['centroid_shift']:>8.2f} {data['shift_z']:>+10.2f} {data['our_vertices']:>8} {data['centore_vertices']:>10}")

    print("\nPhase 6.5 complete!")


if __name__ == "__main__":
    main()
