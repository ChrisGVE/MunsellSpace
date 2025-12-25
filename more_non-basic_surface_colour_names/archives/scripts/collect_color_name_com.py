#!/usr/bin/env python3
"""
Collect colors from color-name.com across all 24 color family categories.
"""

import csv
import re
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

OUTPUT_DIR = Path(__file__).parent

# All 24 color family categories from color-name.com
COLOR_FAMILIES = [
    "blue", "teal", "green", "yellow", "orange", "red",
    "pink", "purple", "gray", "silver", "white", "black",
    "gold", "olive", "khaki", "beige", "brown", "chocolate",
    "maroon", "indigo", "navy", "cyan", "aqua", "fuchsia"
]


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch URL content with proper headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except (HTTPError, URLError) as e:
        print(f"    Error fetching {url}: {e}")
        return ""


def parse_color_page(html: str) -> list:
    """Extract color names and hex codes from a color-name.com category page."""
    colors = []

    # Structure on color-name.com:
    # <title>Color Preview HEXCODE</title>
    # ...
    # <h3><a href="...">Color Name</a></h3>

    # Pattern: Find hex in title, then color name in following h3
    pattern = re.compile(
        r'<title>Color Preview ([0-9A-Fa-f]{6})</title>\s*</svg>\s*</a>\s*<h3><a[^>]*>([^<]+)</a></h3>',
        re.IGNORECASE | re.DOTALL
    )

    matches = pattern.findall(html)
    for hex_code, name in matches:
        name = name.strip()
        if name and len(name) > 1:
            colors.append((name, f'#{hex_code.upper()}'))

    return colors


def collect_color_name_com():
    """Fetch all colors from color-name.com across all categories."""
    print("=" * 70)
    print("COLLECTING FROM COLOR-NAME.COM")
    print("=" * 70)

    all_colors = []

    for family in COLOR_FAMILIES:
        url = f"https://www.color-name.com/colors/{family}"
        print(f"  Fetching {family}...")

        content = fetch_url(url)
        if not content:
            continue

        colors = parse_color_page(content)
        print(f"    Found {len(colors)} colors")
        all_colors.extend(colors)

        time.sleep(0.5)  # Be polite

    # De-duplicate by lowercase name
    seen = set()
    unique_colors = []
    for name, hex_code in all_colors:
        key = name.lower()
        if key not in seen:
            seen.add(key)
            unique_colors.append((name, hex_code))

    # Save to CSV
    output_path = OUTPUT_DIR / "color_name_com_colors.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'coordinates'])
        writer.writerows(unique_colors)

    print(f"\nSaved {len(unique_colors)} unique colors to {output_path.name}")
    return unique_colors


def update_master_vocabulary():
    """Update the master vocabulary with new colors."""
    print("\nUpdating master vocabulary...")

    hex_pattern = re.compile(r'^#?[0-9a-f]{6}$', re.I)
    all_names = set()

    for csv_file in OUTPUT_DIR.glob('*.csv'):
        if csv_file.name in ['master_vocabulary.csv']:
            continue
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row:
                        name = row[0].lower().strip()
                        # Skip hex codes and very short names
                        if name and len(name) > 1 and not hex_pattern.match(name):
                            all_names.add(name)
        except Exception as e:
            print(f'  Error reading {csv_file}: {e}')

    # Save updated master vocabulary
    master_path = OUTPUT_DIR / 'master_vocabulary.csv'
    with open(master_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name'])
        for name in sorted(all_names):
            writer.writerow([name])

    print(f"  Master vocabulary updated: {len(all_names):,} unique color names")


if __name__ == "__main__":
    collect_color_name_com()
    update_master_vocabulary()
