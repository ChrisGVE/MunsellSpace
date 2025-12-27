#!/usr/bin/env python3
"""
Multi-stage XKCD Survey Aggregation Script.

Aggregates 3.3M individual XKCD survey responses into unique color names
with mean RGB values and counts.

Stages:
1. Canonical normalization (remove hyphens, normalize spaces)
2. Spelling variant mapping (grey→gray, colour→color, etc.)
3. Character n-gram similarity clustering (catches "lightblue" ≈ "light blue")
4. Optional SBERT clustering for ambiguous cases

Output: Aggregated color names with RGB, count, and variant info.
"""

import csv
import re
import sys
import time
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
import numpy as np

# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent / "datasets"
NORMALIZED_DIR = DATASETS_DIR / "normalized"
OUTPUT_DIR = DATASETS_DIR / "aggregated"

# Input file
XKCD_SURVEY_FILE = NORMALIZED_DIR / "xkcd_survey_normalized.csv"


# =============================================================================
# Stage 2: Spelling Variant Mappings
# =============================================================================

# Common spelling variants (American English preferred as canonical)
SPELLING_VARIANTS = {
    # British → American
    'grey': 'gray',
    'colour': 'color',
    'coloured': 'colored',
    'colours': 'colors',

    # Common misspellings
    'fuschia': 'fuchsia',
    'fushia': 'fuchsia',
    'fucshia': 'fuchsia',
    'turquise': 'turquoise',
    'turqoise': 'turquoise',
    'turquois': 'turquoise',
    'lavendar': 'lavender',
    'lavander': 'lavender',
    'magenta': 'magenta',  # already correct, but catch 'majenta'
    'majenta': 'magenta',
    'burgandy': 'burgundy',
    'burgungy': 'burgundy',
    'aquamarine': 'aquamarine',
    'aquamrine': 'aquamarine',
    'chartruese': 'chartreuse',
    'chartreause': 'chartreuse',
    'perriwinkle': 'periwinkle',
    'periwinkle': 'periwinkle',
    'marroon': 'maroon',
    'marron': 'maroon',
    'vermillion': 'vermilion',
    'cerulean': 'cerulean',
    'cerulian': 'cerulean',
    'tangerine': 'tangerine',
    'tangirine': 'tangerine',

    # Suffix variants (ish/y/ey/ie)
    # These are handled in normalization, not here
}

# Build reverse mapping for word-level replacement
def build_variant_pattern():
    """Build regex pattern for spelling variants."""
    # Sort by length (longest first) to match longer variants first
    sorted_variants = sorted(SPELLING_VARIANTS.keys(), key=len, reverse=True)
    pattern = r'\b(' + '|'.join(re.escape(v) for v in sorted_variants) + r')\b'
    return re.compile(pattern, re.IGNORECASE)

VARIANT_PATTERN = build_variant_pattern()


# =============================================================================
# Stage 1 & 2: Canonical Normalization
# =============================================================================

def normalize_to_canonical(name: str) -> str:
    """
    Apply stages 1 and 2: canonical normalization + spelling variants.

    Stage 1:
    - Lowercase
    - Remove hyphens between words (light-blue → light blue)
    - Normalize whitespace
    - Remove apostrophes in possessives but keep in contractions

    Stage 2:
    - Apply spelling variant mappings
    """
    if not name:
        return ""

    # Lowercase
    result = name.lower().strip()

    # Replace hyphens with spaces (light-blue → light blue)
    result = result.replace('-', ' ')

    # Remove apostrophe-s possessives (hunter's → hunter)
    result = re.sub(r"'s\b", '', result)

    # Normalize whitespace
    result = re.sub(r'\s+', ' ', result).strip()

    # Stage 2: Apply spelling variants
    def replace_variant(match):
        word = match.group(1).lower()
        return SPELLING_VARIANTS.get(word, word)

    result = VARIANT_PATTERN.sub(replace_variant, result)

    return result


def normalize_to_compact(name: str) -> str:
    """
    Create compact form for n-gram comparison.
    Removes all spaces to catch "light blue" = "lightblue".
    """
    canonical = normalize_to_canonical(name)
    return canonical.replace(' ', '')


# =============================================================================
# Stage 3: Character N-gram Similarity
# =============================================================================

# Pairs that should NOT be merged despite high n-gram similarity
# Format: frozenset({canonical1, canonical2})
DO_NOT_MERGE = {
    frozenset({'slime green', 'lime green'}),
    frozenset({'night blue', 'light blue'}),
    frozenset({'bright green', 'light green'}),
    frozenset({'bright blue', 'light blue'}),
    frozenset({'bright pink', 'light pink'}),
    frozenset({'bright purple', 'light purple'}),
    frozenset({'bright red', 'light red'}),
    frozenset({'bright yellow', 'light yellow'}),
    frozenset({'night sky', 'light sky'}),
    frozenset({'blood red', 'flood red'}),
    frozenset({'rust', 'dust'}),
    frozenset({'dusty', 'rusty'}),
    frozenset({'grape', 'grope'}),
    frozenset({'cream', 'dream'}),
    frozenset({'plum', 'glum'}),
    frozenset({'slate', 'state'}),
    frozenset({'olive', 'alive'}),
    frozenset({'coral', 'choral'}),
    frozenset({'rose', 'hose'}),
    frozenset({'teal', 'real'}),
    frozenset({'mint', 'hint'}),
}


def should_merge(name1: str, name2: str) -> bool:
    """
    Check if two names should be allowed to merge.

    Rules:
    1. Explicit block list
    2. If both are multi-word, first words must be similar
       (prevents "slime green" ~ "lime green" via "limegreen")
    """
    # Check explicit block list
    pair = frozenset({name1, name2})
    if pair in DO_NOT_MERGE:
        return False

    # For multi-word names, check first word similarity
    words1 = name1.split()
    words2 = name2.split()

    if len(words1) > 1 and len(words2) > 1:
        # Both multi-word: first words should be similar
        first1, first2 = words1[0], words2[0]
        if first1 != first2:
            # Different first words - check if one is substring of other
            # (allows "light" ~ "light" but blocks "slime" ~ "lime")
            if first1 not in first2 and first2 not in first1:
                # Check edit distance - allow 1 char difference for typos
                if len(first1) > 2 and len(first2) > 2:
                    # Simple check: same length and differ by 1 char
                    if abs(len(first1) - len(first2)) > 1:
                        return False
                    # Count differing characters
                    diffs = sum(1 for a, b in zip(first1, first2) if a != b)
                    diffs += abs(len(first1) - len(first2))
                    if diffs > 1:
                        return False

    # Also check: single-word vs multi-word
    # "limegreen" should merge with "lime green" but not "slime green"
    if len(words1) == 1 and len(words2) > 1:
        # name1 is compact, name2 is spaced
        compact = name1
        first_word = words2[0]
        # Compact should start with first word
        if not compact.startswith(first_word):
            return False
    elif len(words2) == 1 and len(words1) > 1:
        compact = name2
        first_word = words1[0]
        if not compact.startswith(first_word):
            return False

    return True


def get_character_ngrams(text: str, n: int = 3) -> Set[str]:
    """Extract character n-grams from text."""
    if len(text) < n:
        return {text}
    return {text[i:i+n] for i in range(len(text) - n + 1)}


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def ngram_similarity(name1: str, name2: str, n: int = 3) -> float:
    """Compute n-gram Jaccard similarity between two names."""
    # Use compact form (no spaces) for comparison
    compact1 = normalize_to_compact(name1)
    compact2 = normalize_to_compact(name2)

    ngrams1 = get_character_ngrams(compact1, n)
    ngrams2 = get_character_ngrams(compact2, n)

    return jaccard_similarity(ngrams1, ngrams2)


class NGramIndex:
    """
    Inverted index for efficient n-gram similarity search.
    Uses blocking to avoid O(n²) comparisons.
    """

    def __init__(self, n: int = 3, similarity_threshold: float = 0.7):
        self.n = n
        self.threshold = similarity_threshold
        self.ngram_to_names: Dict[str, Set[str]] = defaultdict(set)
        self.name_to_ngrams: Dict[str, Set[str]] = {}
        self.name_to_compact: Dict[str, str] = {}

    def add(self, name: str, canonical: str):
        """Add a name to the index."""
        compact = canonical.replace(' ', '')
        ngrams = get_character_ngrams(compact, self.n)

        self.name_to_ngrams[name] = ngrams
        self.name_to_compact[name] = compact

        for ngram in ngrams:
            self.ngram_to_names[ngram].add(name)

    def find_similar(self, name: str) -> List[Tuple[str, float]]:
        """Find names similar to the given name."""
        if name not in self.name_to_ngrams:
            return []

        query_ngrams = self.name_to_ngrams[name]

        # Find candidate names (those sharing at least one n-gram)
        candidates = set()
        for ngram in query_ngrams:
            candidates.update(self.ngram_to_names[ngram])

        # Remove self
        candidates.discard(name)

        # Compute exact similarity for candidates
        similar = []
        for candidate in candidates:
            sim = jaccard_similarity(query_ngrams, self.name_to_ngrams[candidate])
            if sim >= self.threshold:
                similar.append((candidate, sim))

        return sorted(similar, key=lambda x: -x[1])


# Known color modifiers and base colors for compound validation
COLOR_MODIFIERS = {
    'light', 'dark', 'pale', 'bright', 'deep', 'pastel', 'neon', 'hot', 'baby',
    'powder', 'dusty', 'dirty', 'dull', 'soft', 'muted', 'vivid', 'electric',
    'royal', 'navy', 'sky', 'sea', 'ocean', 'forest', 'olive', 'lime',
    'burnt', 'rust', 'blood', 'wine', 'brick', 'salmon', 'coral', 'peach',
    'ice', 'midnight', 'true', 'pure', 'rich', 'warm', 'cool', 'faded',
    'ash', 'charcoal', 'slate', 'steel', 'silver', 'gold', 'bronze', 'copper',
    'cream', 'ivory', 'bone', 'sand', 'tan', 'nude', 'blush', 'rose',
    'grass', 'mint', 'jade', 'teal', 'aqua', 'turquoise', 'cyan', 'cobalt',
    'indigo', 'violet', 'plum', 'grape', 'berry', 'cherry', 'ruby', 'scarlet',
    'crimson', 'maroon', 'burgundy', 'magenta', 'fuchsia', 'mauve', 'lilac',
    'lavender', 'periwinkle', 'cornflower', 'sapphire', 'cerulean', 'azure',
    'ish', 'ey', 'y',  # Suffix modifiers (greenish, bluey)
}

BASE_COLORS = {
    'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown',
    'gray', 'grey', 'white', 'black', 'tan', 'beige', 'cream', 'gold',
    'silver', 'bronze', 'copper', 'teal', 'cyan', 'magenta', 'maroon',
    'navy', 'olive', 'coral', 'salmon', 'peach', 'mint', 'lavender',
    'turquoise', 'aqua', 'indigo', 'violet', 'plum', 'burgundy', 'crimson',
    'scarlet', 'ruby', 'rose', 'fuchsia', 'mauve', 'lilac', 'periwinkle',
}


def is_valid_compound(parts: List[str]) -> bool:
    """
    Check if parts form a valid color compound (like "light blue").

    Valid compounds have:
    - All parts at least 2 characters
    - At least one known modifier or base color

    Invalid compounds (like "pur ple") won't have recognizable parts.
    """
    if not all(len(part) >= 2 for part in parts):
        return False

    # Check if any part is a known color term
    known_parts = sum(
        1 for part in parts
        if part in COLOR_MODIFIERS or part in BASE_COLORS
    )

    # Valid if at least one part is recognized
    # (e.g., "light blue" has "light" in modifiers and "blue" in base colors)
    return known_parts >= 1


def name_quality_score(name: str) -> Tuple[int, int, int]:
    """
    Score name quality for representative selection.

    Returns tuple for sorting (higher = better):
    - (well_formed, is_proper_compound, -length)

    A name is "well-formed" if:
    - It has no spaces (simple word like "green")
    - OR it's a valid compound (like "light blue") with known color terms

    For valid compounds, we prefer "light blue" over "lightblue" for readability.

    Malformed examples: "gree n", "b lue", "pur ple", "g r e e n"
    """
    if ' ' not in name:
        # No spaces = well-formed simple word
        # Score: (well_formed=1, is_compound=0, -length)
        return (1, 0, -len(name))

    parts = name.split()

    if is_valid_compound(parts):
        # Well-formed compound like "light blue"
        # is_compound=1 makes this preferred over non-spaced "lightblue"
        # Then prefer fewer parts (2 > 3 > 4), then shorter
        return (1, 1, -len(parts))
    else:
        # Malformed or unrecognized compound (like "pur ple")
        return (0, 0, -len(name))


def cluster_by_compact_form(names: List[str]) -> Dict[str, str]:
    """
    Fast clustering by compact form (no spaces).

    Groups "light blue" with "lightblue" without expensive n-gram comparison.
    Returns: mapping from each name to its cluster representative.
    """
    print(f"  Clustering {len(names):,} names by compact form...")

    # Group by compact form
    compact_to_names: Dict[str, List[str]] = defaultdict(list)
    for name in names:
        compact = name.replace(' ', '')
        compact_to_names[compact].append(name)

    # Build cluster mapping
    cluster_map = {}
    merged_count = 0

    for compact, group in compact_to_names.items():
        if len(group) == 1:
            cluster_map[group[0]] = group[0]
        else:
            # Check if all names in group should merge
            # Apply should_merge check pairwise
            valid_group = [group[0]]
            for name in group[1:]:
                if all(should_merge(name, other) for other in valid_group):
                    valid_group.append(name)
                else:
                    # This name doesn't merge, keep separate
                    cluster_map[name] = name

            if len(valid_group) > 1:
                # Pick representative: best quality score
                # Prefers: well-formed > simple words > proper compounds > shortest
                representative = max(valid_group, key=name_quality_score)

                for name in valid_group:
                    cluster_map[name] = representative
                merged_count += len(valid_group) - 1
            else:
                cluster_map[valid_group[0]] = valid_group[0]

    print(f"  Merged {merged_count:,} names into clusters")
    return cluster_map


def cluster_by_ngram_similarity(
    names: List[str],
    threshold: float = 0.7,
    n: int = 3,
    progress_interval: int = 10000
) -> Dict[str, str]:
    """
    Cluster names by n-gram similarity using Union-Find.

    Returns: mapping from each name to its cluster representative.
    """
    print(f"  Building n-gram index for {len(names):,} names...")

    # Build index
    index = NGramIndex(n=n, similarity_threshold=threshold)
    canonical_map = {}

    for name in names:
        canonical = normalize_to_canonical(name)
        canonical_map[name] = canonical
        index.add(name, canonical)

    print(f"  Index built with {len(index.ngram_to_names):,} unique n-grams")

    # Union-Find for clustering
    parent = {name: name for name in names}
    rank = {name: 0 for name in names}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Find similar pairs and union them
    print(f"  Finding similar pairs (threshold={threshold})...")
    pairs_found = 0
    pairs_blocked = 0

    for i, name in enumerate(names):
        if i > 0 and i % progress_interval == 0:
            print(f"    Processed {i:,}/{len(names):,} ({i/len(names)*100:.1f}%), "
                  f"pairs found: {pairs_found:,}, blocked: {pairs_blocked:,}")

        similar = index.find_similar(name)
        for other, sim in similar:
            # Check if this pair should be merged
            if should_merge(name, other):
                union(name, other)
                pairs_found += 1
            else:
                pairs_blocked += 1

    print(f"  Total pairs found: {pairs_found:,}, blocked: {pairs_blocked:,}")

    # Build cluster mapping
    cluster_map = {}
    for name in names:
        cluster_map[name] = find(name)

    # Count clusters
    unique_clusters = len(set(cluster_map.values()))
    print(f"  Formed {unique_clusters:,} clusters from {len(names):,} names")

    return cluster_map


# =============================================================================
# Main Aggregation Pipeline
# =============================================================================

def load_xkcd_survey(filepath: Path, limit: Optional[int] = None) -> List[Dict]:
    """Load XKCD survey data."""
    print(f"Loading {filepath}...")

    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            rows.append({
                'name': row['name'],
                'name_raw': row['name_raw'],
                'r': int(row['r']),
                'g': int(row['g']),
                'b': int(row['b']),
                'hex': row['hex']
            })

            if (i + 1) % 500000 == 0:
                print(f"  Loaded {i + 1:,} rows...")

    print(f"  Total: {len(rows):,} rows")
    return rows


def aggregate_by_canonical(rows: List[Dict]) -> Dict[str, Dict]:
    """
    First-pass aggregation by canonical form.

    Returns: {canonical_name: {
        'names': set of original names,
        'r_sum': ..., 'g_sum': ..., 'b_sum': ...,
        'count': total count
    }}
    """
    print("Stage 1-2: Aggregating by canonical form...")

    groups = defaultdict(lambda: {
        'names': set(),
        'r_sum': 0, 'g_sum': 0, 'b_sum': 0,
        'count': 0
    })

    for row in rows:
        canonical = normalize_to_canonical(row['name'])
        if not canonical:
            continue

        groups[canonical]['names'].add(row['name'])
        groups[canonical]['r_sum'] += row['r']
        groups[canonical]['g_sum'] += row['g']
        groups[canonical]['b_sum'] += row['b']
        groups[canonical]['count'] += 1

    print(f"  Reduced to {len(groups):,} canonical groups")
    return dict(groups)


def merge_clusters(
    canonical_groups: Dict[str, Dict],
    cluster_map: Dict[str, str]
) -> Dict[str, Dict]:
    """
    Merge canonical groups based on n-gram clusters.
    """
    print("Merging clusters...")

    # Group canonical names by cluster representative
    cluster_to_canonicals = defaultdict(list)
    for canonical in canonical_groups:
        representative = cluster_map.get(canonical, canonical)
        cluster_to_canonicals[representative].append(canonical)

    # Merge groups within each cluster
    merged = {}
    for representative, canonicals in cluster_to_canonicals.items():
        if len(canonicals) == 1:
            # No merging needed
            merged[representative] = canonical_groups[canonicals[0]]
        else:
            # Merge multiple canonical forms
            combined = {
                'names': set(),
                'r_sum': 0, 'g_sum': 0, 'b_sum': 0,
                'count': 0,
                'merged_from': canonicals
            }
            for canonical in canonicals:
                group = canonical_groups[canonical]
                combined['names'].update(group['names'])
                combined['r_sum'] += group['r_sum']
                combined['g_sum'] += group['g_sum']
                combined['b_sum'] += group['b_sum']
                combined['count'] += group['count']

            merged[representative] = combined

    # Count how many were actually merged
    merged_count = sum(1 for v in merged.values() if 'merged_from' in v)
    print(f"  {merged_count:,} clusters merged from multiple canonical forms")
    print(f"  Final: {len(merged):,} unique color names")

    return merged


def compute_final_aggregates(groups: Dict[str, Dict]) -> List[Dict]:
    """
    Compute final aggregated values.
    """
    print("Computing final aggregates...")

    results = []
    for name, data in groups.items():
        count = data['count']
        r_mean = data['r_sum'] / count
        g_mean = data['g_sum'] / count
        b_mean = data['b_sum'] / count

        # Convert to hex
        hex_color = f"#{int(r_mean):02x}{int(g_mean):02x}{int(b_mean):02x}"

        result = {
            'name': name,
            'r': round(r_mean, 1),
            'g': round(g_mean, 1),
            'b': round(b_mean, 1),
            'hex': hex_color,
            'count': count,
            'variants': len(data['names']),
            'variant_names': sorted(data['names'])[:10],  # Keep first 10 variants
        }

        if 'merged_from' in data:
            result['merged_from'] = data['merged_from']

        results.append(result)

    # Sort by count (descending)
    results.sort(key=lambda x: -x['count'])

    return results


def save_results(results: List[Dict], output_path: Path):
    """Save aggregated results to CSV."""
    print(f"Saving results to {output_path}...")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'r', 'g', 'b', 'hex', 'count', 'variants'
        ])
        writer.writeheader()

        for row in results:
            writer.writerow({
                'name': row['name'],
                'r': row['r'],
                'g': row['g'],
                'b': row['b'],
                'hex': row['hex'],
                'count': row['count'],
                'variants': row['variants']
            })

    print(f"  Saved {len(results):,} rows")

    # Also save detailed version with variant info
    detailed_path = output_path.with_suffix('.detailed.csv')
    with open(detailed_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'r', 'g', 'b', 'hex', 'count', 'variants',
            'variant_names', 'merged_from'
        ])
        writer.writeheader()

        for row in results:
            writer.writerow({
                'name': row['name'],
                'r': row['r'],
                'g': row['g'],
                'b': row['b'],
                'hex': row['hex'],
                'count': row['count'],
                'variants': row['variants'],
                'variant_names': '|'.join(row['variant_names']),
                'merged_from': '|'.join(row.get('merged_from', []))
            })

    print(f"  Saved detailed version to {detailed_path.name}")


def print_statistics(results: List[Dict]):
    """Print aggregation statistics."""
    print("\n" + "=" * 60)
    print("AGGREGATION STATISTICS")
    print("=" * 60)

    total_count = sum(r['count'] for r in results)
    total_variants = sum(r['variants'] for r in results)
    merged_count = sum(1 for r in results if r.get('merged_from'))

    print(f"Total survey responses: {total_count:,}")
    print(f"Unique color names: {len(results):,}")
    print(f"Total variant spellings: {total_variants:,}")
    print(f"Names merged via n-gram: {merged_count:,}")
    print(f"Compression ratio: {total_count / len(results):.1f}x")

    # Top 20 by count
    print("\nTop 20 colors by count:")
    for i, row in enumerate(results[:20], 1):
        variants_str = f" ({row['variants']} variants)" if row['variants'] > 1 else ""
        print(f"  {i:2}. {row['name']}: {row['count']:,}{variants_str}")

    # Examples of merged names
    merged = [r for r in results if r.get('merged_from')]
    if merged:
        print(f"\nExamples of n-gram merged names:")
        for row in merged[:10]:
            print(f"  '{row['name']}' <- {row['merged_from']}")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-stage XKCD survey aggregation"
    )
    parser.add_argument('--limit', type=int, default=None,
                        help='Limit number of rows to process (for testing)')
    parser.add_argument('--threshold', type=float, default=0.75,
                        help='N-gram similarity threshold (default: 0.75)')
    parser.add_argument('--skip-ngram', action='store_true',
                        help='Skip all clustering (stages 1-2 only)')
    parser.add_argument('--full-ngram', action='store_true',
                        help='Use full n-gram similarity (slow, O(n²))')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file path')
    args = parser.parse_args()

    start_time = time.time()

    print("=" * 60)
    print("XKCD Survey Multi-Stage Aggregation")
    print("=" * 60)
    print()

    # Load data
    rows = load_xkcd_survey(XKCD_SURVEY_FILE, limit=args.limit)
    print()

    # Stage 1-2: Canonical aggregation
    canonical_groups = aggregate_by_canonical(rows)
    print()

    # Stage 3: Clustering
    if args.skip_ngram:
        print("Stage 3: Skipped (--skip-ngram)")
        merged_groups = canonical_groups
    elif args.full_ngram:
        # Full n-gram similarity (slow, O(n²))
        print("Stage 3: N-gram similarity clustering (slow)...")
        canonical_names = list(canonical_groups.keys())
        cluster_map = cluster_by_ngram_similarity(
            canonical_names,
            threshold=args.threshold
        )
        merged_groups = merge_clusters(canonical_groups, cluster_map)
    else:
        # Default: fast compact form clustering
        print("Stage 3: Compact form clustering (fast)...")
        canonical_names = list(canonical_groups.keys())
        cluster_map = cluster_by_compact_form(canonical_names)
        merged_groups = merge_clusters(canonical_groups, cluster_map)
    print()

    # Compute final aggregates
    results = compute_final_aggregates(merged_groups)

    # Save results
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = OUTPUT_DIR / "xkcd_survey_aggregated.csv"

    save_results(results, output_path)

    # Print statistics
    print_statistics(results)

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.1f} seconds")


if __name__ == "__main__":
    main()
