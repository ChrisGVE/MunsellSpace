#!/usr/bin/env python3
"""
Extract XKCD Color Survey Data

Parses the XKCD color survey SQL dump and extracts color name to RGB mappings.
Outputs aggregated statistics and candidate overlay colors.

Usage:
    python scripts/extract_xkcd_colors.py

Output:
    - tmp/xkcd_color_aggregates.json: Full aggregated data
    - tmp/xkcd_overlay_candidates.csv: Filtered candidates for overlay creation
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

# Configuration
SQL_DUMP_PATH = Path("assets/xkcd_color_survey/mainsurvey_sqldump.txt")
OUTPUT_JSON = Path("tmp/xkcd_color_aggregates.json")
OUTPUT_CSV = Path("tmp/xkcd_overlay_candidates.csv")
MIN_RESPONSES = 100  # Minimum responses to consider a color name


def normalize_colorname(name: str) -> str:
    """Normalize a color name for grouping."""
    # Strip whitespace and convert to lowercase
    name = name.strip().lower()
    # Normalize common variations
    name = name.replace("grey", "gray")
    name = name.replace("colour", "color")
    return name


def parse_sql_dump(filepath: Path) -> dict:
    """Parse the SQL dump and extract color data."""
    # Pattern for INSERT INTO answers statements
    pattern = re.compile(
        r'INSERT INTO "answers" VALUES\(\d+,\d+,[\d.]+,(\d+),(\d+),(\d+),\'([^\']*)\'\);'
    )

    color_data = defaultdict(list)
    line_count = 0
    match_count = 0

    print(f"Parsing {filepath}...")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line_count += 1
            if line_count % 500000 == 0:
                print(f"  Processed {line_count:,} lines, found {match_count:,} answers...")

            match = pattern.match(line.strip())
            if match:
                r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
                colorname = normalize_colorname(match.group(4))

                # Skip empty or obviously invalid names
                if not colorname or len(colorname) > 50:
                    continue

                color_data[colorname].append((r, g, b))
                match_count += 1

    print(f"  Total: {line_count:,} lines, {match_count:,} valid answers")
    print(f"  Unique color names: {len(color_data):,}")

    return color_data


def compute_statistics(color_data: dict) -> list:
    """Compute statistics for each color name."""
    results = []

    for colorname, rgb_list in color_data.items():
        count = len(rgb_list)

        if count < 3:  # Need at least 3 points for meaningful stats
            continue

        # Compute mean RGB
        r_vals = [rgb[0] for rgb in rgb_list]
        g_vals = [rgb[1] for rgb in rgb_list]
        b_vals = [rgb[2] for rgb in rgb_list]

        mean_r = mean(r_vals)
        mean_g = mean(g_vals)
        mean_b = mean(b_vals)

        # Compute standard deviation (spread indicator)
        try:
            std_r = stdev(r_vals) if count > 1 else 0
            std_g = stdev(g_vals) if count > 1 else 0
            std_b = stdev(b_vals) if count > 1 else 0
            avg_std = (std_r + std_g + std_b) / 3
        except Exception:
            avg_std = 0

        # Convert mean RGB to hex
        hex_color = f"#{int(mean_r):02x}{int(mean_g):02x}{int(mean_b):02x}"

        results.append({
            "colorname": colorname,
            "count": count,
            "mean_rgb": [round(mean_r, 1), round(mean_g, 1), round(mean_b, 1)],
            "hex": hex_color,
            "avg_std": round(avg_std, 2),
            "rgb_samples": rgb_list[:10]  # Store first 10 samples for reference
        })

    # Sort by count (most frequent first)
    results.sort(key=lambda x: x["count"], reverse=True)
    return results


def identify_overlay_candidates(stats: list, min_count: int = MIN_RESPONSES) -> list:
    """Identify potential overlay candidates from the data."""
    # Overlay candidate patterns - non-basic color names
    overlay_patterns = [
        "salmon", "seafoam", "burgundy", "maroon", "cream", "ivory",
        "mustard", "charcoal", "slate", "plum", "greige", "mint",
        "coral", "teal", "turquoise", "lavender", "mauve", "peach",
        "rust", "sand", "tan", "taupe", "wine", "rose", "gold",
        "navy", "fuchsia", "magenta", "violet", "lilac", "beige", "aqua"
    ]

    candidates = []
    for entry in stats:
        if entry["count"] < min_count:
            continue

        name = entry["colorname"]

        # Check if it matches any overlay pattern (exact or contains)
        is_candidate = False
        matched_pattern = None

        for pattern in overlay_patterns:
            if pattern in name:
                is_candidate = True
                matched_pattern = pattern
                break

        if is_candidate:
            candidates.append({
                **entry,
                "base_pattern": matched_pattern,
                "is_modified": name != matched_pattern  # e.g., "dark salmon" vs "salmon"
            })

    return candidates


def main():
    if not SQL_DUMP_PATH.exists():
        print(f"Error: SQL dump not found at {SQL_DUMP_PATH}")
        print("Please ensure the XKCD color survey data has been downloaded.")
        sys.exit(1)

    # Ensure output directory exists
    OUTPUT_JSON.parent.mkdir(exist_ok=True)

    # Parse the SQL dump
    color_data = parse_sql_dump(SQL_DUMP_PATH)

    # Compute statistics
    print("\nComputing statistics...")
    stats = compute_statistics(color_data)

    # Show top 50 most frequent colors
    print("\nTop 50 most frequent color names:")
    print("-" * 60)
    for i, entry in enumerate(stats[:50], 1):
        print(f"{i:3}. {entry['colorname']:25} {entry['count']:>8,} responses  {entry['hex']}")

    # Identify overlay candidates
    print(f"\nIdentifying overlay candidates (min {MIN_RESPONSES} responses)...")
    candidates = identify_overlay_candidates(stats)

    print(f"\nFound {len(candidates)} overlay candidate colors:")
    print("-" * 70)
    for c in candidates[:30]:
        mod = " (variant)" if c["is_modified"] else ""
        print(f"  {c['colorname']:25} {c['count']:>6,} responses  base: {c['base_pattern']}{mod}")

    # Save full statistics
    print(f"\nSaving full statistics to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w') as f:
        json.dump({
            "total_unique_names": len(stats),
            "colors_with_100_plus": len([s for s in stats if s["count"] >= 100]),
            "colors_with_1000_plus": len([s for s in stats if s["count"] >= 1000]),
            "statistics": stats
        }, f, indent=2)

    # Save overlay candidates as CSV
    print(f"Saving overlay candidates to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, 'w') as f:
        f.write("colorname,count,base_pattern,is_variant,mean_r,mean_g,mean_b,hex,avg_std\n")
        for c in candidates:
            f.write(f"{c['colorname']},{c['count']},{c['base_pattern']},{c['is_modified']},"
                   f"{c['mean_rgb'][0]},{c['mean_rgb'][1]},{c['mean_rgb'][2]},"
                   f"{c['hex']},{c['avg_std']}\n")

    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total unique color names:    {len(stats):>10,}")
    print(f"Names with >= 100 responses: {len([s for s in stats if s['count'] >= 100]):>10,}")
    print(f"Names with >= 1000 responses:{len([s for s in stats if s['count'] >= 1000]):>10,}")
    print(f"Overlay candidates found:    {len(candidates):>10,}")
    print("=" * 60)


if __name__ == "__main__":
    main()
