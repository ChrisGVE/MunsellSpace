#!/usr/bin/env python3
"""
Phase 6.2: RGB to Munsell Conversion

Converts all family-assigned colors from RGB to Munsell coordinates using
the MunsellSpace Rust library via subprocess.

Input: datasets/phase6/family_assignments.csv
Output: datasets/phase6/family_assignments_munsell.csv
        (adds Munsell coordinates: hue_str, hue_num, value, chroma, munsell_notation, x, y, z)
"""

import csv
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List
import json


# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # MunsellSpace root
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
PHASE6_DIR = DATASETS_DIR / "phase6"


def load_family_assignments() -> List[Dict]:
    """Load the family assignments from Phase 6.1."""
    csv_path = PHASE6_DIR / "family_assignments.csv"
    colors = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            colors.append(row)

    print(f"Loaded {len(colors)} colors from family assignments")
    return colors


def prepare_rust_input(colors: List[Dict]) -> str:
    """Prepare input CSV for the Rust converter."""
    lines = ["name,r,g,b"]  # Header
    for color in colors:
        # Quote name if it contains comma
        name = color["name"]
        if "," in name:
            name = f'"{name}"'
        lines.append(f"{name},{int(float(color['r']))},{int(float(color['g']))},{int(float(color['b']))}")
    return "\n".join(lines)


def run_rust_converter(input_csv: str) -> Dict[str, Dict]:
    """Run the Rust RGB to Munsell converter and parse results."""
    print("Running Rust converter...")

    # Build the example first if needed
    build_cmd = [
        "cargo", "build", "--release", "--example", "simple_rgb_to_munsell"
    ]
    build_result = subprocess.run(
        build_cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    if build_result.returncode != 0:
        print(f"Build warning: {build_result.stderr}")

    # Run the converter
    run_cmd = [
        "cargo", "run", "--release", "--example", "simple_rgb_to_munsell"
    ]

    result = subprocess.run(
        run_cmd,
        cwd=PROJECT_ROOT,
        input=input_csv,
        capture_output=True,
        text=True,
        timeout=600  # 10 minute timeout for large dataset
    )

    if result.returncode != 0:
        print(f"Converter stderr: {result.stderr[:1000]}")

    # Parse output CSV
    munsell_data = {}
    lines = result.stdout.strip().split("\n")

    # Skip header
    header = None
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("name,"):
            header = line.strip().split(",")
            continue
        if header is None:
            continue

        # Parse CSV line (handling quoted names)
        parts = []
        current = ""
        in_quotes = False
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(current)
                current = ""
            else:
                current += char
        parts.append(current)

        if len(parts) >= 12:
            name = parts[0].strip('"')
            munsell_data[name] = {
                "hue_str": parts[4],
                "hue_num": float(parts[5]) if parts[5] else 0.0,
                "munsell_value": float(parts[6]) if parts[6] else 0.0,
                "munsell_chroma": float(parts[7]) if parts[7] else 0.0,
                "munsell_notation": parts[8],
                "cartesian_x": float(parts[9]) if parts[9] else 0.0,
                "cartesian_y": float(parts[10]) if parts[10] else 0.0,
                "cartesian_z": float(parts[11]) if parts[11] else 0.0,
            }

    print(f"  Parsed {len(munsell_data)} Munsell conversions")
    return munsell_data


def merge_results(colors: List[Dict], munsell_data: Dict[str, Dict]) -> List[Dict]:
    """Merge Munsell data with family assignments."""
    results = []
    converted = 0
    failed = 0

    for color in colors:
        name = color["name"]
        result = dict(color)

        if name in munsell_data:
            result.update(munsell_data[name])
            converted += 1
        else:
            # Failed conversion - add empty fields
            result.update({
                "hue_str": "",
                "hue_num": "",
                "munsell_value": "",
                "munsell_chroma": "",
                "munsell_notation": "",
                "cartesian_x": "",
                "cartesian_y": "",
                "cartesian_z": "",
            })
            failed += 1

        results.append(result)

    print(f"  Converted: {converted:,}")
    print(f"  Failed: {failed:,}")
    return results


def save_results(results: List[Dict]):
    """Save merged results to CSV."""
    csv_path = PHASE6_DIR / "family_assignments_munsell.csv"

    fieldnames = [
        "name", "hex", "r", "g", "b", "source_count", "sources",
        "total_votes", "confidence", "assigned_family", "similarity_score",
        "hue_str", "hue_num", "munsell_value", "munsell_chroma",
        "munsell_notation", "cartesian_x", "cartesian_y", "cartesian_z"
    ]

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved {len(results)} results to {csv_path}")


def compute_statistics(results: List[Dict]) -> Dict:
    """Compute statistics about the conversions."""
    from collections import Counter

    stats = {
        "total": len(results),
        "converted": sum(1 for r in results if r.get("munsell_notation")),
        "failed": sum(1 for r in results if not r.get("munsell_notation")),
        "families": {}
    }

    # Per-family stats
    for result in results:
        if not result.get("munsell_notation"):
            continue

        family = result["assigned_family"]
        if family not in stats["families"]:
            stats["families"][family] = {
                "count": 0,
                "values": [],
                "chromas": [],
                "hue_nums": [],
            }

        fam = stats["families"][family]
        fam["count"] += 1
        fam["values"].append(float(result["munsell_value"]))
        fam["chromas"].append(float(result["munsell_chroma"]))
        if result["hue_num"]:
            fam["hue_nums"].append(float(result["hue_num"]))

    # Compute averages per family
    import numpy as np
    for family, fam in stats["families"].items():
        fam["avg_value"] = round(np.mean(fam["values"]), 2) if fam["values"] else 0
        fam["avg_chroma"] = round(np.mean(fam["chromas"]), 2) if fam["chromas"] else 0
        fam["avg_hue"] = round(np.mean(fam["hue_nums"]), 1) if fam["hue_nums"] else 0
        # Remove raw data for JSON
        del fam["values"]
        del fam["chromas"]
        del fam["hue_nums"]

    return stats


def print_summary(stats: Dict):
    """Print summary of Munsell conversions."""
    print("\n" + "=" * 70)
    print("MUNSELL CONVERSION SUMMARY")
    print("=" * 70)

    print(f"\nTotal: {stats['total']:,}")
    print(f"Converted: {stats['converted']:,} ({100*stats['converted']/stats['total']:.1f}%)")
    print(f"Failed: {stats['failed']:,}")

    print(f"\n{'Family':<15} {'Count':>8} {'Avg Value':>10} {'Avg Chroma':>12} {'Avg Hue':>10}")
    print("-" * 60)

    sorted_families = sorted(
        stats["families"].items(),
        key=lambda x: -x[1]["count"]
    )

    for family, data in sorted_families[:20]:
        print(f"{family:<15} {data['count']:>8} {data['avg_value']:>10.2f} {data['avg_chroma']:>12.2f} {data['avg_hue']:>10.1f}")


def main():
    """Main entry point."""
    print("Phase 6.2: RGB to Munsell Conversion")
    print("=" * 50)

    # Load Phase 6.1 results
    colors = load_family_assignments()

    # Prepare input for Rust converter
    input_csv = prepare_rust_input(colors)

    # Run converter
    munsell_data = run_rust_converter(input_csv)

    # Merge results
    results = merge_results(colors, munsell_data)

    # Save results
    save_results(results)

    # Compute and save statistics
    stats = compute_statistics(results)
    stats_path = PHASE6_DIR / "munsell_conversion_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved statistics to {stats_path}")

    # Print summary
    print_summary(stats)

    print("\nPhase 6.2 complete!")


if __name__ == "__main__":
    main()
