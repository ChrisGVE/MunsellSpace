#!/usr/bin/env python3
"""
Consolidate Color Name Datasets.

Merges all normalized color name sources into a unified dataset ready
for the color family clustering pipeline.

Sources consolidated:
- XKCD Survey (aggregated) - 157K unique names with counts
- XKCD Curated - 954 colors (highest quality)
- Meodai - ~30K color names
- ColorHexa - ~1.2K color names
- Wikipedia - ~1.5K color names
- ColorName.com - ~2K color names

Centore is kept separate as anchor/reference families (Munsell coordinates).

Output format:
- name: normalized color name
- hex: hex RGB color value
- r, g, b: RGB decimal values
- source_count: number of sources containing this name
- sources: pipe-separated list of sources
- total_votes: combined count from survey sources
- confidence: quality score based on source count and votes
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Optional, Tuple
import math

# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent / "datasets"
NORMALIZED_DIR = DATASETS_DIR / "normalized"
AGGREGATED_DIR = DATASETS_DIR / "aggregated"
OUTPUT_DIR = DATASETS_DIR / "consolidated"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """Convert RGB values to hex color."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def normalize_name(name: str) -> str:
    """
    Normalize a color name for deduplication.

    - Lowercase
    - Remove hyphens
    - Normalize whitespace
    """
    result = name.lower().strip()
    result = result.replace('-', ' ')
    result = re.sub(r'\s+', ' ', result).strip()
    return result


class ColorEntry:
    """Represents a consolidated color entry."""

    def __init__(self, name: str):
        self.name = name
        self.hex_values: List[str] = []
        self.rgb_values: List[Tuple[float, float, float]] = []
        self.sources: Set[str] = set()
        self.votes: int = 0  # From survey data
        self.variants: Set[str] = set()  # Original name variants

    def add_color(self, hex_color: str, source: str, votes: int = 1,
                  raw_name: Optional[str] = None):
        """Add a color value from a source."""
        self.hex_values.append(hex_color)
        r, g, b = hex_to_rgb(hex_color)
        self.rgb_values.append((r, g, b))
        self.sources.add(source)
        self.votes += votes
        if raw_name:
            self.variants.add(raw_name)

    @property
    def mean_rgb(self) -> Tuple[float, float, float]:
        """Compute mean RGB across all sources."""
        if not self.rgb_values:
            return (0, 0, 0)
        r = sum(v[0] for v in self.rgb_values) / len(self.rgb_values)
        g = sum(v[1] for v in self.rgb_values) / len(self.rgb_values)
        b = sum(v[2] for v in self.rgb_values) / len(self.rgb_values)
        return (r, g, b)

    @property
    def mean_hex(self) -> str:
        """Compute mean hex color across all sources."""
        r, g, b = self.mean_rgb
        return rgb_to_hex(r, g, b)

    @property
    def source_count(self) -> int:
        """Number of sources containing this color."""
        return len(self.sources)

    @property
    def confidence(self) -> float:
        """
        Compute confidence score based on:
        - Source count (0-1 scale, log)
        - Vote count (0-1 scale, log)
        - Cross-source agreement (color similarity)
        """
        # Source score: log scale, max at 5 sources
        source_score = min(math.log(self.source_count + 1) / math.log(6), 1.0)

        # Vote score: log scale, max at 100K votes
        vote_score = min(math.log(self.votes + 1) / math.log(100001), 1.0)

        # Combine scores (weighted)
        # Source diversity is valuable, votes show popularity
        score = (source_score * 0.4 + vote_score * 0.6)

        return round(score, 3)


def load_normalized_csv(filepath: Path, source_name: str) -> List[Dict]:
    """Load a normalized CSV file."""
    print(f"Loading {source_name} from {filepath.name}...")

    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'name': row['name'],
                'name_raw': row.get('name_raw', row['name']),
                'coordinates': row['coordinates'],
                'source': source_name
            })

    print(f"  -> {len(rows):,} rows")
    return rows


def load_xkcd_aggregated(filepath: Path) -> List[Dict]:
    """Load XKCD aggregated survey data."""
    print(f"Loading XKCD Survey (aggregated) from {filepath.name}...")

    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'name': row['name'],
                'name_raw': row['name'],
                'hex': row['hex'],
                'r': float(row['r']),
                'g': float(row['g']),
                'b': float(row['b']),
                'count': int(row['count']),
                'variants': int(row['variants']),
                'source': 'xkcd_survey'
            })

    print(f"  -> {len(rows):,} rows")
    return rows


def consolidate_sources(
    xkcd_survey: List[Dict],
    xkcd_curated: List[Dict],
    meodai: List[Dict],
    colorhexa: List[Dict],
    wikipedia: List[Dict],
    colorname_com: List[Dict]
) -> Dict[str, ColorEntry]:
    """Consolidate all sources into unified entries."""
    print("\nConsolidating sources...")

    entries: Dict[str, ColorEntry] = defaultdict(lambda: None)

    def get_or_create(name: str) -> ColorEntry:
        if entries[name] is None:
            entries[name] = ColorEntry(name)
        return entries[name]

    # 1. XKCD Survey (largest, with vote counts)
    print("  Processing XKCD Survey...")
    for row in xkcd_survey:
        name = normalize_name(row['name'])
        entry = get_or_create(name)
        entry.add_color(row['hex'], 'xkcd_survey', votes=row['count'])

    # 2. XKCD Curated (high quality)
    print("  Processing XKCD Curated...")
    for row in xkcd_curated:
        name = normalize_name(row['name'])
        entry = get_or_create(name)
        # Curated list is high quality, give it weight
        entry.add_color(row['coordinates'], 'xkcd_curated', votes=1000,
                       raw_name=row['name_raw'])

    # 3. Meodai
    print("  Processing Meodai...")
    for row in meodai:
        name = normalize_name(row['name'])
        entry = get_or_create(name)
        entry.add_color(row['coordinates'], 'meodai', votes=100,
                       raw_name=row['name_raw'])

    # 4. ColorHexa
    print("  Processing ColorHexa...")
    for row in colorhexa:
        name = normalize_name(row['name'])
        entry = get_or_create(name)
        entry.add_color(row['coordinates'], 'colorhexa', votes=50,
                       raw_name=row['name_raw'])

    # 5. Wikipedia
    print("  Processing Wikipedia...")
    for row in wikipedia:
        name = normalize_name(row['name'])
        entry = get_or_create(name)
        entry.add_color(row['coordinates'], 'wikipedia', votes=50,
                       raw_name=row['name_raw'])

    # 6. ColorName.com
    print("  Processing ColorName.com...")
    for row in colorname_com:
        name = normalize_name(row['name'])
        entry = get_or_create(name)
        entry.add_color(row['coordinates'], 'colorname_com', votes=10,
                       raw_name=row['name_raw'])

    # Remove None entries (shouldn't happen, but be safe)
    entries = {k: v for k, v in entries.items() if v is not None}

    return entries


def analyze_consolidation(entries: Dict[str, ColorEntry]):
    """Print consolidation analysis."""
    print("\n" + "=" * 60)
    print("CONSOLIDATION ANALYSIS")
    print("=" * 60)

    total = len(entries)
    print(f"Total unique color names: {total:,}")

    # Source distribution
    source_counts = defaultdict(int)
    for entry in entries.values():
        for source in entry.sources:
            source_counts[source] += 1

    print("\nColors per source:")
    for source in sorted(source_counts.keys()):
        count = source_counts[source]
        pct = count / total * 100
        print(f"  {source}: {count:,} ({pct:.1f}%)")

    # Multi-source colors
    multi_source = [e for e in entries.values() if e.source_count > 1]
    print(f"\nColors in multiple sources: {len(multi_source):,} ({len(multi_source)/total*100:.1f}%)")

    # Source count distribution
    source_dist = defaultdict(int)
    for entry in entries.values():
        source_dist[entry.source_count] += 1

    print("\nSource count distribution:")
    for count in sorted(source_dist.keys()):
        num = source_dist[count]
        pct = num / total * 100
        print(f"  {count} source(s): {num:,} ({pct:.1f}%)")

    # Top colors by confidence
    top_colors = sorted(entries.values(), key=lambda e: e.confidence, reverse=True)

    print("\nTop 20 colors by confidence:")
    for entry in top_colors[:20]:
        sources_str = ', '.join(sorted(entry.sources))
        print(f"  {entry.name}: {entry.confidence:.3f} [{entry.source_count} src, {entry.votes:,} votes] -> {entry.mean_hex}")


def save_consolidated(entries: Dict[str, ColorEntry], output_path: Path):
    """Save consolidated data to CSV."""
    print(f"\nSaving consolidated data to {output_path}...")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sort by confidence (descending)
    sorted_entries = sorted(entries.values(), key=lambda e: e.confidence, reverse=True)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'hex', 'r', 'g', 'b',
            'source_count', 'sources', 'total_votes', 'confidence'
        ])
        writer.writeheader()

        for entry in sorted_entries:
            r, g, b = entry.mean_rgb
            writer.writerow({
                'name': entry.name,
                'hex': entry.mean_hex,
                'r': round(r, 1),
                'g': round(g, 1),
                'b': round(b, 1),
                'source_count': entry.source_count,
                'sources': '|'.join(sorted(entry.sources)),
                'total_votes': entry.votes,
                'confidence': entry.confidence
            })

    print(f"  -> Saved {len(sorted_entries):,} rows")

    # Also save detailed version with variants
    detailed_path = output_path.with_suffix('.detailed.csv')
    with open(detailed_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'hex', 'r', 'g', 'b',
            'source_count', 'sources', 'total_votes', 'confidence',
            'hex_values', 'variants'
        ])
        writer.writeheader()

        for entry in sorted_entries:
            r, g, b = entry.mean_rgb
            writer.writerow({
                'name': entry.name,
                'hex': entry.mean_hex,
                'r': round(r, 1),
                'g': round(g, 1),
                'b': round(b, 1),
                'source_count': entry.source_count,
                'sources': '|'.join(sorted(entry.sources)),
                'total_votes': entry.votes,
                'confidence': entry.confidence,
                'hex_values': '|'.join(entry.hex_values[:10]),  # First 10 values
                'variants': '|'.join(sorted(entry.variants)[:10])  # First 10 variants
            })

    print(f"  -> Saved detailed version to {detailed_path.name}")


def main():
    print("=" * 60)
    print("Color Name Dataset Consolidation")
    print("=" * 60)
    print()

    # Load all sources
    xkcd_survey = load_xkcd_aggregated(
        AGGREGATED_DIR / "xkcd_survey_aggregated.csv"
    )

    xkcd_curated = load_normalized_csv(
        NORMALIZED_DIR / "xkcd_curated_normalized.csv",
        "xkcd_curated"
    )

    meodai = load_normalized_csv(
        NORMALIZED_DIR / "meodai_normalized.csv",
        "meodai"
    )

    colorhexa = load_normalized_csv(
        NORMALIZED_DIR / "colorhexa_normalized.csv",
        "colorhexa"
    )

    wikipedia = load_normalized_csv(
        NORMALIZED_DIR / "wikipedia_normalized.csv",
        "wikipedia"
    )

    colorname_com = load_normalized_csv(
        NORMALIZED_DIR / "colorname_com_normalized.csv",
        "colorname_com"
    )

    # Consolidate
    entries = consolidate_sources(
        xkcd_survey, xkcd_curated, meodai,
        colorhexa, wikipedia, colorname_com
    )

    # Analyze
    analyze_consolidation(entries)

    # Save
    output_path = OUTPUT_DIR / "color_names_consolidated.csv"
    save_consolidated(entries, output_path)

    print("\n" + "=" * 60)
    print("CONSOLIDATION COMPLETE")
    print("=" * 60)
    print(f"Output: {output_path}")
    print(f"Ready for Phase B (semantic validation) and Phase C (clustering)")


if __name__ == "__main__":
    main()
