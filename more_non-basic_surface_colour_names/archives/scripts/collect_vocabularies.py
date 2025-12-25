#!/usr/bin/env python3
"""
Collect color vocabularies from multiple authoritative sources.

This script fetches color name data from:
1. Centore (20 non-basic colors with Munsell centroids) - local data
2. XKCD color survey (865 colors) - https://xkcd.com/color/rgb.txt
3. meodai/color-names (30K+ colors) - GitHub
4. Wikipedia List of Colors (A-Z)
5. colorhexa.com

Each source is saved as a separate CSV with columns: name, coordinates
where coordinates is hex or munsell notation depending on source.
"""

import csv
import re
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

OUTPUT_DIR = Path(__file__).parent

# Centore data extracted from Rust source
CENTORE_COLORS = {
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
}


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch URL content with proper headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ColorVocabularyCollector/1.0'
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except (HTTPError, URLError) as e:
        print(f"  Error fetching {url}: {e}")
        return ""


def save_csv(filename: str, data: list, source_name: str):
    """Save color data to CSV."""
    output_path = OUTPUT_DIR / filename
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'coordinates'])
        writer.writerows(data)
    print(f"  Saved {len(data)} colors to {filename}")


def collect_centore():
    """Save Centore color data (already in memory)."""
    print("\n1. Collecting Centore colors...")
    data = [(name, munsell) for name, munsell in sorted(CENTORE_COLORS.items())]
    save_csv("centore_colors.csv", data, "Centore (2020)")


def collect_xkcd():
    """Fetch XKCD color survey data."""
    print("\n2. Collecting XKCD colors...")
    url = "https://xkcd.com/color/rgb.txt"
    content = fetch_url(url)

    if not content:
        print("  Failed to fetch XKCD data")
        return

    data = []
    for line in content.strip().split('\n'):
        # Skip header/comments
        if line.startswith('#') or not line.strip():
            continue

        # Format: "color name\t#hexcode\t" (with trailing whitespace)
        # Split by tab and clean
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0].strip()
            hex_code = parts[1].strip()
            if name and hex_code.startswith('#'):
                data.append((name, hex_code))

    save_csv("xkcd_colors.csv", data, "XKCD Color Survey")


def collect_meodai():
    """Fetch meodai/color-names from GitHub CSV."""
    print("\n3. Collecting meodai/color-names...")

    # The source CSV file
    url = "https://raw.githubusercontent.com/meodai/color-names/master/src/colornames.csv"
    content = fetch_url(url)

    if not content:
        print("  Failed to fetch meodai data")
        return

    data = []
    lines = content.strip().split('\n')

    # Skip header line
    for line in lines[1:]:
        # Format: name,hex,good name
        parts = line.split(',')
        if len(parts) >= 2:
            name = parts[0].strip()
            hex_code = parts[1].strip()
            if name and hex_code:
                # Ensure hex code has # prefix
                if not hex_code.startswith('#'):
                    hex_code = '#' + hex_code
                data.append((name, hex_code.upper()))

    save_csv("meodai_colors.csv", data, "meodai/color-names")


def collect_wikipedia():
    """Fetch Wikipedia List of Colors (A-F, G-M, N-Z)."""
    print("\n4. Collecting Wikipedia colors...")

    urls = [
        ("A-F", "https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F"),
        ("G-M", "https://en.wikipedia.org/wiki/List_of_colors:_G%E2%80%93M"),
        ("N-Z", "https://en.wikipedia.org/wiki/List_of_colors:_N%E2%80%93Z"),
    ]

    all_data = []

    for label, url in urls:
        print(f"  Fetching {label}...")
        content = fetch_url(url)
        if not content:
            continue

        # Extract table rows with color data
        # Pattern: <td...><a...>Color Name</a></td> followed by <td...>#HEXCODE</td>
        # Using simpler regex approach

        # Find all rows that have both a name link and a hex code
        # The name is in an <a> tag, hex is in the following <td>

        # Pattern to find name and hex in sequence
        pattern = re.compile(
            r'<td[^>]*>(?:<[^>]*>)*<a[^>]*>([^<]+)</a>.*?</td>\s*<td[^>]*[^>]*>#([0-9A-Fa-f]{6})',
            re.DOTALL
        )

        matches = pattern.findall(content)
        for name, hex_code in matches:
            name = name.strip()
            if name and len(name) > 1:
                all_data.append((name, f'#{hex_code.upper()}'))

        print(f"    Found {len(matches)} colors")
        time.sleep(0.5)  # Be polite

    # De-duplicate by lowercase name
    seen = set()
    unique_data = []
    for name, hex_code in all_data:
        key = name.lower()
        if key not in seen:
            seen.add(key)
            unique_data.append((name, hex_code))

    save_csv("wikipedia_colors.csv", unique_data, "Wikipedia List of Colors")


def collect_colorhexa():
    """Fetch colorhexa.com color names."""
    print("\n5. Collecting colorhexa colors...")

    url = "https://www.colorhexa.com/color-names"
    content = fetch_url(url)

    if not content:
        print("  Failed to fetch colorhexa data")
        return

    data = []

    # Pattern: href="/HEXCODE">Color Name</a>
    pattern = re.compile(
        r'<a[^>]*href="/([0-9a-f]{6})"[^>]*>([^<]+)</a>',
        re.IGNORECASE
    )

    matches = pattern.findall(content)
    for hex_code, name in matches:
        name = name.strip()
        # Filter out non-color entries (hex codes used as names, single chars, etc.)
        if name and len(name) > 2 and not re.match(r'^[0-9a-f]{6}$', name, re.I):
            data.append((name, f'#{hex_code.upper()}'))

    # De-duplicate
    seen = set()
    unique_data = []
    for name, hex_code in data:
        key = name.lower()
        if key not in seen:
            seen.add(key)
            unique_data.append((name, hex_code))

    save_csv("colorhexa_colors.csv", unique_data, "colorhexa.com")


def main():
    print("=" * 70)
    print("COLOR VOCABULARY COLLECTION")
    print("=" * 70)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Collect from all sources
    collect_centore()
    collect_xkcd()
    collect_meodai()
    collect_wikipedia()
    collect_colorhexa()

    # Summary
    print("\n" + "=" * 70)
    print("COLLECTION COMPLETE")
    print("=" * 70)

    # Count and show summary
    total = 0
    for csv_file in sorted(OUTPUT_DIR.glob("*.csv")):
        with open(csv_file) as f:
            count = sum(1 for _ in f) - 1  # Subtract header
        print(f"  {csv_file.name}: {count:,} colors")
        total += count

    print(f"\n  Total colors (with duplicates across sources): {total:,}")

    # Build master vocabulary (unique names only)
    print("\nBuilding master vocabulary (unique names only)...")
    all_names = set()
    for csv_file in OUTPUT_DIR.glob("*.csv"):
        if csv_file.name == "master_vocabulary.csv":
            continue
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row:
                    all_names.add(row[0].lower().strip())

    # Save master vocabulary
    master_path = OUTPUT_DIR / "master_vocabulary.csv"
    with open(master_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name'])
        for name in sorted(all_names):
            writer.writerow([name])

    print(f"  Master vocabulary: {len(all_names):,} unique names")
    print(f"  Saved to {master_path}")


if __name__ == "__main__":
    main()
