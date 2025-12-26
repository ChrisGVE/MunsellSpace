#!/usr/bin/env python3
"""
Normalize color name datasets.

Reads each source dataset and outputs a normalized CSV with:
- name: normalized color name
- name_raw: original color name (for review)
- coordinates: color coordinates (hex RGB or Munsell, depending on source)

Normalization rules:
- Decode HTML entities (&#039; -> ', &#8217; -> ', etc.)
- Lowercase all names
- Normalize whitespace (collapse multiple spaces, trim)
- Remove surrounding quotes (but keep internal apostrophes)
- Strip leading/trailing whitespace

Filtering rules:
- Drop names that are only hex codes (#rrggbb)
- Drop metadata names (e.g., "complete list of html color names")
"""

import csv
import html
import re
import sys
from pathlib import Path
from typing import Optional

# Paths
DATASETS_DIR = Path(__file__).parent.parent.parent / "datasets"
COLLECTED_DIR = DATASETS_DIR / "collected"
XKCD_DIR = DATASETS_DIR / "xkcd"
NORMALIZED_DIR = DATASETS_DIR / "normalized"

# Patterns to filter out (case-insensitive, checked after normalization)
FILTER_PATTERNS = [
    r'^#?[0-9a-f]{3}$',          # 3-digit hex
    r'^#?[0-9a-f]{6}$',          # 6-digit hex
    r'^#?[0-9a-f]{8}$',          # 8-digit hex (with alpha)
    r'^complete list of',        # Metadata
    r'^list of',                 # Metadata
    r'^color names?$',           # Generic metadata
    r'^html color',              # Metadata
    r'^web color',               # Metadata
]
FILTER_REGEX = re.compile('|'.join(FILTER_PATTERNS), re.IGNORECASE)


def normalize_name(name: str) -> Optional[str]:
    """
    Normalize a color name.

    Rules:
    - Decode HTML entities
    - Lowercase
    - Collapse multiple whitespace to single space
    - Trim leading/trailing whitespace
    - Remove surrounding quotes (but keep internal apostrophes like "hunter's")
    - Normalize fancy quotes to straight quotes

    Returns None if name should be filtered out.
    """
    if not name:
        return None

    # Decode HTML entities (&#039; -> ', &#8217; -> ', &amp; -> &, etc.)
    result = html.unescape(name)

    # Normalize fancy quotes to straight apostrophe
    result = result.replace(''', "'")  # U+2019 right single quotation mark
    result = result.replace(''', "'")  # U+2018 left single quotation mark
    result = result.replace('"', '"')  # U+201C left double quotation mark
    result = result.replace('"', '"')  # U+201D right double quotation mark

    # Handle SQL-escaped single quotes ('' -> ')
    result = result.replace("''", "'")

    # Lowercase
    result = result.lower()

    # Collapse multiple whitespace to single space
    result = re.sub(r'\s+', ' ', result)

    # Trim
    result = result.strip()

    # Remove surrounding quotes (single or double)
    if len(result) >= 2:
        if (result[0] == '"' and result[-1] == '"') or \
           (result[0] == "'" and result[-1] == "'"):
            result = result[1:-1].strip()

    # Filter out unwanted patterns
    if not result or FILTER_REGEX.search(result):
        return None

    return result


def process_simple_csv(input_path: Path, output_path: Path, source_name: str):
    """Process a simple name,coordinates CSV file."""
    print(f"Processing {source_name}...")

    rows = []
    filtered_count = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name_raw = row['name']
            name_normalized = normalize_name(name_raw)
            if name_normalized is None:
                filtered_count += 1
                continue
            coordinates = row['coordinates']
            rows.append({
                'name': name_normalized,
                'name_raw': name_raw,
                'coordinates': coordinates
            })

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'name_raw', 'coordinates'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {len(rows)} rows written to {output_path.name} ({filtered_count} filtered)")
    return len(rows)


def process_xkcd_curated(input_path: Path, output_path: Path):
    """Process XKCD curated color survey (tab-separated, with header comment)."""
    print("Processing XKCD curated...")

    rows = []
    filtered_count = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Skip comments and empty lines
            if line.startswith('#') or not line.strip():
                continue

            parts = line.strip().split('\t')
            if len(parts) >= 2:
                name_raw = parts[0]
                hex_color = parts[1].strip()
                name_normalized = normalize_name(name_raw)
                if name_normalized is None:
                    filtered_count += 1
                    continue
                rows.append({
                    'name': name_normalized,
                    'name_raw': name_raw,
                    'coordinates': hex_color
                })

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'name_raw', 'coordinates'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {len(rows)} rows written to {output_path.name} ({filtered_count} filtered)")
    return len(rows)


def process_xkcd_survey(input_path: Path, output_path: Path):
    """
    Process XKCD full survey SQL dump.

    Extracts from answers table: user_id, timestamp, R, G, B, colorname
    Keeps all individual responses.
    """
    print("Processing XKCD full survey (this may take a while)...")

    # Pattern to match INSERT INTO answers
    # Format: INSERT INTO "answers" VALUES(id,user_id,timestamp,R,G,B,'colorname');
    pattern = re.compile(
        r'INSERT INTO "answers" VALUES\((\d+),(\d+),([\d.]+),(\d+),(\d+),(\d+),\'(.*?)\'\);'
    )

    rows = []
    line_count = 0
    match_count = 0
    filtered_count = 0

    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line_count += 1
            if line_count % 500000 == 0:
                print(f"  ... processed {line_count:,} lines, found {match_count:,} answers, filtered {filtered_count:,}")

            if 'INSERT INTO "answers"' not in line:
                continue

            match = pattern.match(line.strip())
            if match:
                match_count += 1
                answer_id, user_id, timestamp, r, g, b, name_raw = match.groups()
                name_normalized = normalize_name(name_raw)

                if name_normalized is None:
                    filtered_count += 1
                    continue

                # Convert RGB to hex
                hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"

                rows.append({
                    'name': name_normalized,
                    'name_raw': name_raw,
                    'r': int(r),
                    'g': int(g),
                    'b': int(b),
                    'hex': hex_color
                })

    print(f"  ... writing {len(rows):,} rows to CSV...")

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'name_raw', 'r', 'g', 'b', 'hex'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {len(rows):,} rows written to {output_path.name} ({filtered_count:,} filtered)")
    return len(rows)


def main():
    """Process all datasets."""
    NORMALIZED_DIR.mkdir(exist_ok=True)

    total_rows = 0

    # 1. Centore
    total_rows += process_simple_csv(
        COLLECTED_DIR / "centore_colors.csv",
        NORMALIZED_DIR / "centore_normalized.csv",
        "Centore"
    )

    # 2. XKCD curated
    total_rows += process_xkcd_curated(
        XKCD_DIR / "xkcd_color_survey.txt",
        NORMALIZED_DIR / "xkcd_curated_normalized.csv"
    )

    # 3. XKCD full survey - processed by analyze_xkcd_survey.py instead
    # (handles normalization + deduplication + cleaning in one step)
    print("Skipping XKCD full survey (use analyze_xkcd_survey.py)")

    # 4. Meodai
    total_rows += process_simple_csv(
        COLLECTED_DIR / "meodai_colors.csv",
        NORMALIZED_DIR / "meodai_normalized.csv",
        "Meodai"
    )

    # 5. ColorHexa
    total_rows += process_simple_csv(
        COLLECTED_DIR / "colorhexa_colors.csv",
        NORMALIZED_DIR / "colorhexa_normalized.csv",
        "ColorHexa"
    )

    # 6. Wikipedia
    total_rows += process_simple_csv(
        COLLECTED_DIR / "wikipedia_colors.csv",
        NORMALIZED_DIR / "wikipedia_normalized.csv",
        "Wikipedia"
    )

    # 7. ColorName.com
    total_rows += process_simple_csv(
        COLLECTED_DIR / "color_name_com_colors.csv",
        NORMALIZED_DIR / "colorname_com_normalized.csv",
        "ColorName.com"
    )

    print()
    print("=" * 60)
    print(f"COMPLETE: {total_rows:,} total rows across all datasets")
    print(f"Output directory: {NORMALIZED_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
