#!/usr/bin/env python3
"""
Phase 2.3: Family Matching Between Screen and Surface Polyhedra

Matches screen color families to surface color families by name,
documents dropped families with insufficient data on either side.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
SCREEN_DIR = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6"
SURFACE_DIR = BASE_DIR / "datasets/surface_polyhedra"
OUTPUT_DIR = BASE_DIR / "datasets/matched_families"
SURFACE_STATS = SURFACE_DIR / "polyhedra_statistics.csv"
SCREEN_SUMMARY = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6_summary.json"

# Centore's 30 families (10 basic + 20 non-basic)
CENTORE_BASIC = ["blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"]
CENTORE_NONBASIC = [
    "aqua", "beige", "coral", "fuchsia", "gold", "lavender", "lilac", "magenta", "mauve", "navy",
    "peach", "rose", "rust", "sand", "tan", "taupe", "teal", "turquoise", "violet", "wine"
]
CENTORE_30 = set(CENTORE_BASIC + CENTORE_NONBASIC)

# New candidate families from Phase 5
NEW_CANDIDATES = ["indigo", "maroon", "lime", "plum", "aquamarine"]


def get_screen_families():
    """Get families with polyhedra in screen dataset (threshold 0.6)."""
    families = {}

    # Load summary for sample counts
    with open(SCREEN_SUMMARY) as f:
        summary = json.load(f)

    # families is a dict, not a list
    families_data = summary.get("families", {})
    for name, family_data in families_data.items():
        families[name] = {
            "sample_count": family_data["sample_count"],
            "volume": family_data["volume"],
            "confidence": family_data["avg_confidence"]
        }

    return families


def get_surface_families():
    """Get families with polyhedra in surface dataset."""
    families = {}

    # Parse statistics CSV
    with open(SURFACE_STATS) as f:
        lines = f.readlines()

    header = lines[0].strip().split(",")
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.strip().split(",")
        name = parts[0]
        sample_count = int(parts[1])
        quality = parts[2]

        families[name] = {
            "sample_count": sample_count,
            "quality": quality
        }

    return families


def classify_family(name):
    """Classify family as basic, non-basic, or new candidate."""
    if name in CENTORE_BASIC:
        return "basic"
    elif name in CENTORE_NONBASIC:
        return "non-basic"
    elif name in NEW_CANDIDATES:
        return "new-candidate"
    else:
        return "unknown"


def match_families():
    """Match screen and surface families, identify drops."""
    screen = get_screen_families()
    surface = get_surface_families()

    screen_set = set(screen.keys())
    surface_set = set(surface.keys())

    # Matching
    matched = screen_set & surface_set
    screen_only = screen_set - surface_set
    surface_only = surface_set - screen_set

    # Build results
    included = []
    dropped_screen_only = []
    dropped_surface_only = []

    for name in sorted(matched):
        included.append({
            "family": name,
            "category": classify_family(name),
            "screen_samples": screen[name]["sample_count"],
            "surface_samples": surface[name]["sample_count"],
            "surface_quality": surface[name]["quality"],
            "screen_volume": screen[name]["volume"],
            "screen_confidence": screen[name]["confidence"]
        })

    for name in sorted(screen_only):
        dropped_screen_only.append({
            "family": name,
            "category": classify_family(name),
            "screen_samples": screen[name]["sample_count"],
            "reason": "No surface polyhedron available"
        })

    for name in sorted(surface_only):
        dropped_surface_only.append({
            "family": name,
            "category": classify_family(name),
            "surface_samples": surface[name]["sample_count"],
            "reason": "No screen polyhedron available"
        })

    return {
        "included": included,
        "dropped_screen_only": dropped_screen_only,
        "dropped_surface_only": dropped_surface_only,
        "summary": {
            "total_screen_families": len(screen_set),
            "total_surface_families": len(surface_set),
            "matched_families": len(matched),
            "dropped_from_screen": len(screen_only),
            "dropped_from_surface": len(surface_only)
        }
    }


def generate_report(results):
    """Generate markdown report."""
    report = []
    report.append("# Family Matching Report: Screen vs Surface Color Polyhedra")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Summary
    s = results["summary"]
    report.append("## Summary")
    report.append("")
    report.append(f"- **Screen families (threshold 0.6):** {s['total_screen_families']}")
    report.append(f"- **Surface families:** {s['total_surface_families']}")
    report.append(f"- **Matched families:** {s['matched_families']}")
    report.append(f"- **Dropped (screen only):** {s['dropped_from_screen']}")
    report.append(f"- **Dropped (surface only):** {s['dropped_from_surface']}")
    report.append("")

    # Matched families table
    report.append("## Matched Families for Comparison")
    report.append("")
    report.append("These families have polyhedra in both screen and surface datasets:")
    report.append("")
    report.append("| Family | Category | Screen Samples | Surface Samples | Surface Quality |")
    report.append("|--------|----------|----------------|-----------------|-----------------|")

    for f in results["included"]:
        report.append(f"| {f['family']} | {f['category']} | {f['screen_samples']} | {f['surface_samples']} | {f['surface_quality']} |")

    report.append("")

    # Category breakdown
    report.append("### Category Breakdown")
    report.append("")
    categories = {}
    for f in results["included"]:
        cat = f["category"]
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        report.append(f"- **{cat}:** {count} families")
    report.append("")

    # Dropped families
    report.append("## Dropped Families")
    report.append("")

    if results["dropped_screen_only"]:
        report.append("### In Screen Dataset Only (no surface polyhedron)")
        report.append("")
        report.append("| Family | Category | Screen Samples | Reason |")
        report.append("|--------|----------|----------------|--------|")
        for f in results["dropped_screen_only"]:
            report.append(f"| {f['family']} | {f['category']} | {f['screen_samples']} | {f['reason']} |")
        report.append("")

    if results["dropped_surface_only"]:
        report.append("### In Surface Dataset Only (no screen polyhedron)")
        report.append("")
        report.append("| Family | Category | Surface Samples | Reason |")
        report.append("|--------|----------|-----------------|--------|")
        for f in results["dropped_surface_only"]:
            report.append(f"| {f['family']} | {f['category']} | {f['surface_samples']} | {f['reason']} |")
        report.append("")

    # Analysis of dropped Centore families
    report.append("## Analysis: Dropped Centore Families")
    report.append("")

    dropped_centore = [f for f in results["dropped_screen_only"]
                       if f["family"] in CENTORE_30]

    if dropped_centore:
        report.append("The following Centore 30 families lack surface data:")
        report.append("")
        for f in dropped_centore:
            report.append(f"- **{f['family']}** ({f['category']}): {f['screen_samples']} screen samples, no surface polyhedron")
        report.append("")
        report.append("These families cannot be compared until surface color data is collected.")
    else:
        report.append("All Centore 30 families with screen polyhedra also have surface polyhedra.")
    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("1. **Proceed with comparison** for the {} matched families".format(s["matched_families"]))
    report.append("2. **Data collection needed** for {} families missing from surface dataset".format(s["dropped_from_screen"]))
    report.append("3. **Priority collection targets:**")

    # Prioritize by screen sample count (higher = more important)
    priority = sorted(results["dropped_screen_only"],
                     key=lambda x: x["screen_samples"], reverse=True)[:5]
    for f in priority:
        report.append(f"   - {f['family']} ({f['screen_samples']} screen samples)")

    return "\n".join(report)


def main():
    """Run family matching analysis."""
    print("Phase 2.3: Family Matching Analysis")
    print("=" * 50)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run matching
    results = match_families()

    # Save JSON outputs
    included_path = OUTPUT_DIR / "included_families.json"
    with open(included_path, "w") as f:
        json.dump(results["included"], f, indent=2)
    print(f"Saved: {included_path}")

    dropped_path = OUTPUT_DIR / "dropped_families.json"
    dropped_data = {
        "screen_only": results["dropped_screen_only"],
        "surface_only": results["dropped_surface_only"]
    }
    with open(dropped_path, "w") as f:
        json.dump(dropped_data, f, indent=2)
    print(f"Saved: {dropped_path}")

    # Generate and save report
    report = generate_report(results)
    report_path = OUTPUT_DIR / "family_matching_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved: {report_path}")

    # Print summary
    s = results["summary"]
    print()
    print("Summary:")
    print(f"  Matched families: {s['matched_families']}")
    print(f"  Dropped (screen only): {s['dropped_from_screen']}")
    print(f"  Dropped (surface only): {s['dropped_from_surface']}")
    print()
    print("Matched families:")
    for f in results["included"]:
        print(f"  - {f['family']}: {f['screen_samples']} screen / {f['surface_samples']} surface")


if __name__ == "__main__":
    main()
