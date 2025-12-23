#!/usr/bin/env python3
"""
A Priori Color Word Extraction

Pattern-based extraction of color words from XKCD color survey data.
Matches color names against a predefined list of overlay patterns.

Method: Pre-define expected color terms, search for matches in data.
Pros: High precision for known colors, fast
Cons: Introduces selection bias, misses unknown color terms

Results:
- 210 candidates found
- Only 16% of responses captured
- Missed many valid color terms not in pattern list

Usage:
    python overlay-preprocessing/a_priori_extraction.py

Input:
    assets/xkcd/mainsurvey_sqldump.txt

Output:
    overlay-preprocessing/results/xkcd_color_aggregates.json
    overlay-preprocessing/results/xkcd_overlay_candidates_apriori.csv
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
SQL_DUMP_PATH = PROJECT_ROOT / "assets/xkcd/mainsurvey_sqldump.txt"
OUTPUT_DIR = PROJECT_ROOT / "overlay-preprocessing/results"
OUTPUT_JSON = OUTPUT_DIR / "xkcd_color_aggregates.json"
OUTPUT_CSV = OUTPUT_DIR / "xkcd_overlay_candidates_apriori.csv"
MIN_RESPONSES = 100  # Minimum responses to consider a color name

# Predefined overlay patterns (introduces a priori bias)
OVERLAY_PATTERNS = [
    "salmon", "seafoam", "burgundy", "maroon", "cream", "ivory",
    "mustard", "charcoal", "slate", "plum", "greige", "mint",
    "coral", "teal", "turquoise", "lavender", "mauve", "peach",
    "rust", "sand", "tan", "taupe", "wine", "rose", "gold",
    "navy", "fuchsia", "magenta", "violet", "lilac", "beige", "aqua"
]


def normalize_colorname(name: str) -> str:
    """Normalize a color name for grouping."""
    name = name.strip().lower()
    name = name.replace("grey", "gray")
    name = name.replace("colour", "color")
    return name


def parse_sql_dump(filepath: Path) -> dict:
    """Parse the SQL dump and extract color data."""
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

        if count < 3:
            continue

        r_vals = [rgb[0] for rgb in rgb_list]
        g_vals = [rgb[1] for rgb in rgb_list]
        b_vals = [rgb[2] for rgb in rgb_list]

        mean_r = mean(r_vals)
        mean_g = mean(g_vals)
        mean_b = mean(b_vals)

        try:
            std_r = stdev(r_vals) if count > 1 else 0
            std_g = stdev(g_vals) if count > 1 else 0
            std_b = stdev(b_vals) if count > 1 else 0
            avg_std = (std_r + std_g + std_b) / 3
        except Exception:
            avg_std = 0

        hex_color = f"#{int(mean_r):02x}{int(mean_g):02x}{int(mean_b):02x}"

        results.append({
            "colorname": colorname,
            "count": count,
            "mean_rgb": [round(mean_r, 1), round(mean_g, 1), round(mean_b, 1)],
            "hex": hex_color,
            "avg_std": round(avg_std, 2),
            "rgb_samples": rgb_list[:10]
        })

    results.sort(key=lambda x: x["count"], reverse=True)
    return results


def identify_overlay_candidates(stats: list, min_count: int = MIN_RESPONSES) -> list:
    """Identify potential overlay candidates using a priori patterns."""
    candidates = []
    for entry in stats:
        if entry["count"] < min_count:
            continue

        name = entry["colorname"]

        is_candidate = False
        matched_pattern = None

        for pattern in OVERLAY_PATTERNS:
            if pattern in name:
                is_candidate = True
                matched_pattern = pattern
                break

        if is_candidate:
            candidates.append({
                **entry,
                "base_pattern": matched_pattern,
                "is_modified": name != matched_pattern
            })

    return candidates


def main():
    if not SQL_DUMP_PATH.exists():
        print(f"Error: SQL dump not found at {SQL_DUMP_PATH}")
        print("Please ensure the XKCD color survey data has been downloaded.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    color_data = parse_sql_dump(SQL_DUMP_PATH)

    print("\nComputing statistics...")
    stats = compute_statistics(color_data)

    print("\nTop 50 most frequent color names:")
    print("-" * 60)
    for i, entry in enumerate(stats[:50], 1):
        print(f"{i:3}. {entry['colorname']:25} {entry['count']:>8,} responses  {entry['hex']}")

    print(f"\nIdentifying overlay candidates (a priori patterns, min {MIN_RESPONSES} responses)...")
    candidates = identify_overlay_candidates(stats)

    print(f"\nFound {len(candidates)} overlay candidate colors:")
    print("-" * 70)
    for c in candidates[:30]:
        mod = " (variant)" if c["is_modified"] else ""
        print(f"  {c['colorname']:25} {c['count']:>6,} responses  base: {c['base_pattern']}{mod}")

    # Calculate coverage
    total_responses = sum(s["count"] for s in stats)
    candidate_responses = sum(c["count"] for c in candidates)
    coverage = candidate_responses / total_responses * 100

    print(f"\n*** Coverage Analysis ***")
    print(f"Total responses in dataset: {total_responses:,}")
    print(f"Responses matching patterns: {candidate_responses:,}")
    print(f"Coverage: {coverage:.1f}%")
    print(f"Responses ignored: {total_responses - candidate_responses:,} ({100-coverage:.1f}%)")

    print(f"\nSaving full statistics to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w') as f:
        json.dump({
            "method": "a_priori",
            "patterns_used": OVERLAY_PATTERNS,
            "total_unique_names": len(stats),
            "colors_with_100_plus": len([s for s in stats if s["count"] >= 100]),
            "colors_with_1000_plus": len([s for s in stats if s["count"] >= 1000]),
            "coverage_percent": round(coverage, 2),
            "statistics": stats
        }, f, indent=2)

    print(f"Saving overlay candidates to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, 'w') as f:
        f.write("colorname,count,base_pattern,is_variant,mean_r,mean_g,mean_b,hex,avg_std\n")
        for c in candidates:
            f.write(f"{c['colorname']},{c['count']},{c['base_pattern']},{c['is_modified']},"
                   f"{c['mean_rgb'][0]},{c['mean_rgb'][1]},{c['mean_rgb'][2]},"
                   f"{c['hex']},{c['avg_std']}\n")

    print("\n" + "=" * 60)
    print("SUMMARY (A Priori Method)")
    print("=" * 60)
    print(f"Total unique color names:    {len(stats):>10,}")
    print(f"Names with >= 100 responses: {len([s for s in stats if s['count'] >= 100]):>10,}")
    print(f"Overlay candidates found:    {len(candidates):>10,}")
    print(f"Coverage of total responses: {coverage:>9.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
