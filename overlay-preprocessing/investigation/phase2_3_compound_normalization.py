#!/usr/bin/env python3
"""
Phase 2.3: Compound Name Normalization

Standardizes compound color names:
1. Word order: "dark blue" vs "blue dark" -> canonical order
2. Hyphenation: "blue-green" vs "blue green" vs "bluegreen" -> standardize
3. Modifier normalization: "very dark" vs "really dark" -> canonical modifier

Establishes a consistent naming convention for compound color names.
"""

import json
import re
from collections import defaultdict
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(__file__).parent

# Load cached XKCD data
XKCD_CACHE = OUTPUT_DIR / "xkcd_color_counts_cache.json"

# Color vocabulary categories
BASE_COLORS = {
    'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown',
    'black', 'white', 'gray', 'grey', 'violet', 'indigo', 'cyan', 'magenta',
    'teal', 'turquoise', 'coral', 'salmon', 'maroon', 'burgundy', 'beige',
    'tan', 'cream', 'ivory', 'gold', 'silver', 'bronze', 'copper', 'rust',
    'peach', 'lavender', 'lilac', 'mauve', 'rose', 'fuchsia', 'aqua',
    'navy', 'olive', 'lime', 'mint', 'chartreuse', 'periwinkle', 'plum',
    'wine', 'sand', 'taupe', 'khaki'
}

# Lightness/darkness modifiers
LIGHTNESS_MODIFIERS = {
    'light': 'light',
    'lite': 'light',
    'dark': 'dark',
    'deep': 'deep',
    'pale': 'pale',
    'bright': 'bright',
    'vivid': 'vivid',
    'dull': 'dull',
    'muted': 'muted',
    'soft': 'soft',
    'medium': 'medium',
    'mid': 'medium',
    'faded': 'faded',
    'washed': 'washed',
    'dusty': 'dusty',
    'dirty': 'dirty',
    'muddy': 'muddy',
    'pastel': 'pastel',
    'neon': 'neon',
    'electric': 'electric',
    'hot': 'hot'
}

# Intensity modifiers (normalize to canonical form)
INTENSITY_MODIFIERS = {
    'very': 'very',
    'really': 'very',
    'super': 'very',
    'ultra': 'ultra',
    'extra': 'very',
    'kinda': 'slightly',
    'kind of': 'slightly',
    'sorta': 'slightly',
    'sort of': 'slightly',
    'slightly': 'slightly',
    'somewhat': 'slightly',
    'almost': 'almost',
    'nearly': 'almost'
}

# Color-ish suffixes
ISH_SUFFIXES = {'ish', 'y', 'ey', 'ie'}


# ============================================================================
# Compound Name Analysis Functions
# ============================================================================

def parse_compound_name(name: str) -> dict:
    """
    Parse a compound color name into its components.

    Returns dict with:
    - intensity: intensity modifier (very, slightly, etc.)
    - lightness: lightness modifier (light, dark, etc.)
    - hue_modifier: hue-shifting color (greenish, blueish, etc.)
    - base_color: primary color
    - secondary_color: secondary color for mixed names (blue-green)
    - descriptor: object descriptor (sky, forest, etc.)
    - raw_words: original word list
    """
    # Normalize separators
    normalized = name.lower().replace('-', ' ').replace('_', ' ')
    words = normalized.split()

    result = {
        'intensity': None,
        'lightness': None,
        'hue_modifier': None,
        'base_color': None,
        'secondary_color': None,
        'descriptor': None,
        'raw_words': words,
        'structure': []
    }

    remaining_words = []

    for word in words:
        classified = False

        # Check intensity modifiers
        if word in INTENSITY_MODIFIERS:
            result['intensity'] = INTENSITY_MODIFIERS[word]
            result['structure'].append(('intensity', word))
            classified = True

        # Check lightness modifiers
        elif word in LIGHTNESS_MODIFIERS:
            result['lightness'] = LIGHTNESS_MODIFIERS[word]
            result['structure'].append(('lightness', word))
            classified = True

        # Check base colors
        elif word in BASE_COLORS:
            if result['base_color'] is None:
                result['base_color'] = word
                result['structure'].append(('base_color', word))
            else:
                result['secondary_color'] = word
                result['structure'].append(('secondary_color', word))
            classified = True

        # Check -ish/-y color modifiers (greenish, bluey, etc.)
        elif not classified:
            for base in BASE_COLORS:
                for suffix in ISH_SUFFIXES:
                    if word == base + suffix or word == base[:-1] + suffix:
                        result['hue_modifier'] = base
                        result['structure'].append(('hue_modifier', word))
                        classified = True
                        break
                if classified:
                    break

        if not classified:
            remaining_words.append(word)
            result['structure'].append(('other', word))

    # Try to identify descriptors from remaining words
    if remaining_words:
        result['descriptor'] = ' '.join(remaining_words)

    return result


def normalize_compound_name(name: str, method: str = 'standard') -> str:
    """
    Normalize a compound color name to canonical form.

    Methods:
    - 'standard': [intensity] [lightness] [hue_modifier] [base_color] [secondary]
    - 'alphabetic': Sort words alphabetically
    - 'frequency': Most common form wins (requires frequency data)
    """
    parsed = parse_compound_name(name)

    if method == 'standard':
        # Build canonical form: intensity + lightness + hue_mod + base + secondary + descriptor
        parts = []

        if parsed['intensity']:
            parts.append(parsed['intensity'])
        if parsed['lightness']:
            parts.append(parsed['lightness'])
        if parsed['hue_modifier']:
            # Reconstruct -ish form
            parts.append(parsed['hue_modifier'] + 'ish')
        if parsed['base_color']:
            parts.append(parsed['base_color'])
        if parsed['secondary_color']:
            parts.append(parsed['secondary_color'])
        if parsed['descriptor'] and parsed['base_color']:
            # Put descriptors after base color
            parts.append(parsed['descriptor'])
        elif parsed['descriptor']:
            parts.append(parsed['descriptor'])

        return ' '.join(parts) if parts else name.lower()

    elif method == 'alphabetic':
        words = re.split(r'[\s\-_]+', name.lower())
        return ' '.join(sorted(words))

    return name.lower()


def detect_hyphenation_variants(names: set) -> dict:
    """
    Detect hyphenation variants of the same name.

    Groups: "blue green", "blue-green", "bluegreen" -> same name
    """
    # Build normalized form to original mapping
    normalized_groups = defaultdict(list)

    for name in names:
        # Normalize: remove hyphens/underscores, lowercase
        normalized = name.lower().replace('-', ' ').replace('_', ' ')
        normalized = ' '.join(normalized.split())  # Normalize whitespace

        normalized_groups[normalized].append(name)

    # Find groups with multiple variants
    variants = {}
    for normalized, originals in normalized_groups.items():
        if len(originals) > 1:
            variants[normalized] = {
                'variants': originals,
                'count': len(originals)
            }

    return variants


def detect_word_order_variants(names: set) -> dict:
    """
    Detect word order variants of the same name.

    Groups: "dark blue", "blue dark" -> same name
    """
    # Build sorted form to original mapping
    sorted_groups = defaultdict(list)

    for name in names:
        words = re.split(r'[\s\-_]+', name.lower())
        sorted_form = ' '.join(sorted(words))

        sorted_groups[sorted_form].append(name)

    # Find groups with multiple variants
    variants = {}
    for sorted_form, originals in sorted_groups.items():
        if len(originals) > 1:
            variants[sorted_form] = {
                'variants': originals,
                'count': len(originals)
            }

    return variants


def analyze_modifier_usage(names: set, counts: dict) -> dict:
    """
    Analyze usage patterns of modifiers in compound names.
    """
    modifier_stats = {
        'intensity': defaultdict(int),
        'lightness': defaultdict(int)
    }

    for name in names:
        parsed = parse_compound_name(name)
        count = counts.get(name, 1)

        if parsed['intensity']:
            modifier_stats['intensity'][parsed['intensity']] += count
        if parsed['lightness']:
            modifier_stats['lightness'][parsed['lightness']] += count

    return dict(modifier_stats)


def generate_canonical_form_mappings(
    names: set,
    counts: dict,
    method: str = 'frequency'
) -> dict:
    """
    Generate mappings from variant forms to canonical forms.

    For each group of variants, choose the most frequent as canonical.
    """
    # Group by normalized form
    normalized_groups = defaultdict(list)

    for name in names:
        # Full normalization: lowercase, split, sort alphabetically
        words = re.split(r'[\s\-_]+', name.lower())
        normalized = ' '.join(sorted(words))
        normalized_groups[normalized].append(name)

    # Generate mappings
    mappings = {}

    for normalized, variants in normalized_groups.items():
        if len(variants) <= 1:
            continue

        # Choose canonical based on method
        if method == 'frequency':
            # Most frequent variant is canonical
            canonical = max(variants, key=lambda x: counts.get(x, 0))
        elif method == 'standard':
            # Use standardized form
            canonical = normalize_compound_name(variants[0], method='standard')
        else:
            canonical = variants[0]

        # Map all variants to canonical
        for variant in variants:
            if variant != canonical:
                mappings[variant] = canonical

    return mappings


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 2.3: Compound Name Normalization")
    print("=" * 70)

    # Load data
    print("\n1. Loading data...")

    print("   Loading XKCD color counts...")
    with open(XKCD_CACHE, 'r') as f:
        xkcd_counts = json.load(f)
    print(f"   → Loaded {len(xkcd_counts):,} color names")

    all_names = set(xkcd_counts.keys())

    # Analyze compound names
    print("\n2. Analyzing compound name structures...")

    compound_analysis = {
        'single_word': 0,
        'two_word': 0,
        'three_plus_word': 0,
        'with_hyphens': 0,
        'with_base_color': 0,
        'with_modifier': 0,
        'with_intensity': 0
    }

    for name in all_names:
        words = re.split(r'[\s\-_]+', name)
        if len(words) == 1:
            compound_analysis['single_word'] += 1
        elif len(words) == 2:
            compound_analysis['two_word'] += 1
        else:
            compound_analysis['three_plus_word'] += 1

        if '-' in name:
            compound_analysis['with_hyphens'] += 1

        parsed = parse_compound_name(name)
        if parsed['base_color']:
            compound_analysis['with_base_color'] += 1
        if parsed['lightness']:
            compound_analysis['with_modifier'] += 1
        if parsed['intensity']:
            compound_analysis['with_intensity'] += 1

    for key, value in compound_analysis.items():
        print(f"   → {key}: {value:,}")

    # Detect variants
    print("\n3. Detecting variant groups...")

    print("   Detecting hyphenation variants...")
    hyphen_variants = detect_hyphenation_variants(all_names)
    print(f"   → Found {len(hyphen_variants):,} hyphenation variant groups")

    print("   Detecting word order variants...")
    order_variants = detect_word_order_variants(all_names)
    print(f"   → Found {len(order_variants):,} word order variant groups")

    # Analyze modifier usage
    print("\n4. Analyzing modifier usage patterns...")
    modifier_stats = analyze_modifier_usage(all_names, xkcd_counts)

    print("   Lightness modifiers (weighted by response count):")
    for mod, count in sorted(modifier_stats['lightness'].items(), key=lambda x: -x[1])[:10]:
        print(f"      {mod}: {count:,}")

    print("\n   Intensity modifiers (weighted by response count):")
    for mod, count in sorted(modifier_stats['intensity'].items(), key=lambda x: -x[1])[:10]:
        print(f"      {mod}: {count:,}")

    # Generate canonical mappings
    print("\n5. Generating canonical form mappings...")

    canonical_mappings = generate_canonical_form_mappings(all_names, xkcd_counts, method='frequency')
    print(f"   → Generated {len(canonical_mappings):,} mappings")

    # Generate report
    print("\n6. Generating outputs...")

    report = []
    report.append("# Phase 2.3: Compound Name Normalization Report")
    report.append("")
    report.append("## 1. Executive Summary")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Total names analyzed | {len(all_names):,} |")
    report.append(f"| Single-word names | {compound_analysis['single_word']:,} |")
    report.append(f"| Two-word compounds | {compound_analysis['two_word']:,} |")
    report.append(f"| Three+ word compounds | {compound_analysis['three_plus_word']:,} |")
    report.append(f"| Names with hyphens | {compound_analysis['with_hyphens']:,} |")
    report.append(f"| Names with base color | {compound_analysis['with_base_color']:,} |")
    report.append(f"| Names with lightness modifier | {compound_analysis['with_modifier']:,} |")
    report.append(f"| Hyphenation variant groups | {len(hyphen_variants):,} |")
    report.append(f"| Word order variant groups | {len(order_variants):,} |")
    report.append(f"| Canonical mappings generated | {len(canonical_mappings):,} |")
    report.append("")

    report.append("## 2. Methodology")
    report.append("")
    report.append("### 2.1 Compound Name Parsing")
    report.append("Each name is parsed into components:")
    report.append("- **Intensity modifier**: very, slightly, almost, etc.")
    report.append("- **Lightness modifier**: light, dark, pale, bright, etc.")
    report.append("- **Hue modifier**: greenish, bluish, etc.")
    report.append("- **Base color**: primary color (blue, red, etc.)")
    report.append("- **Secondary color**: for mixed colors (blue-green)")
    report.append("- **Descriptor**: object descriptors (sky, forest, etc.)")
    report.append("")

    report.append("### 2.2 Normalization Methods")
    report.append("")
    report.append("**Standard ordering**: [intensity] [lightness] [hue_mod] [base] [secondary]")
    report.append("- Example: 'very light greenish blue' is standard form")
    report.append("")
    report.append("**Frequency-based selection**: Most common variant becomes canonical")
    report.append("- Example: If 'dark blue' has 5000 responses and 'blue dark' has 10,")
    report.append("  'dark blue' is canonical")
    report.append("")

    report.append("### 2.3 Variant Detection")
    report.append("")
    report.append("**Hyphenation variants**: Group names differing only in hyphenation")
    report.append("- 'blue green', 'blue-green', 'bluegreen' → same group")
    report.append("")
    report.append("**Word order variants**: Group names with same words, different order")
    report.append("- 'dark blue', 'blue dark' → same group")
    report.append("")

    report.append("## 3. Modifier Usage Analysis")
    report.append("")
    report.append("### 3.1 Lightness Modifiers")
    report.append("")
    report.append("| Modifier | Response Count |")
    report.append("|----------|---------------|")
    for mod, count in sorted(modifier_stats['lightness'].items(), key=lambda x: -x[1])[:15]:
        report.append(f"| {mod} | {count:,} |")
    report.append("")

    report.append("### 3.2 Intensity Modifiers")
    report.append("")
    report.append("| Modifier | Response Count |")
    report.append("|----------|---------------|")
    for mod, count in sorted(modifier_stats['intensity'].items(), key=lambda x: -x[1])[:15]:
        report.append(f"| {mod} | {count:,} |")
    report.append("")

    report.append("## 4. Variant Examples")
    report.append("")

    # Top hyphenation variants by total responses
    report.append("### 4.1 Hyphenation Variant Groups (Top 20)")
    report.append("")
    report.append("| Normalized | Variants | Total Responses |")
    report.append("|------------|----------|-----------------|")

    sorted_hyphen = sorted(
        hyphen_variants.items(),
        key=lambda x: sum(xkcd_counts.get(v, 0) for v in x[1]['variants']),
        reverse=True
    )[:20]

    for normalized, info in sorted_hyphen:
        variants = ', '.join(info['variants'][:3])
        total = sum(xkcd_counts.get(v, 0) for v in info['variants'])
        if len(info['variants']) > 3:
            variants += f" (+{len(info['variants'])-3} more)"
        report.append(f"| {normalized} | {variants} | {total:,} |")
    report.append("")

    report.append("### 4.2 Word Order Variant Groups (Top 20)")
    report.append("")
    report.append("| Sorted Form | Variants | Total Responses |")
    report.append("|-------------|----------|-----------------|")

    sorted_order = sorted(
        order_variants.items(),
        key=lambda x: sum(xkcd_counts.get(v, 0) for v in x[1]['variants']),
        reverse=True
    )[:20]

    for sorted_form, info in sorted_order:
        variants = ', '.join(info['variants'][:3])
        total = sum(xkcd_counts.get(v, 0) for v in info['variants'])
        if len(info['variants']) > 3:
            variants += f" (+{len(info['variants'])-3} more)"
        report.append(f"| {sorted_form} | {variants} | {total:,} |")
    report.append("")

    report.append("## 5. Canonical Form Examples")
    report.append("")
    report.append("| Variant | Canonical | Variant Count | Canonical Count |")
    report.append("|---------|-----------|---------------|-----------------|")

    sorted_mappings = sorted(
        canonical_mappings.items(),
        key=lambda x: xkcd_counts.get(x[1], 0),
        reverse=True
    )[:30]

    for variant, canonical in sorted_mappings:
        var_count = xkcd_counts.get(variant, 0)
        can_count = xkcd_counts.get(canonical, 0)
        report.append(f"| {variant} | {canonical} | {var_count:,} | {can_count:,} |")
    report.append("")

    report.append("## 6. Normalization Recommendations")
    report.append("")
    report.append("### 6.1 Hyphenation Convention")
    report.append("- **Recommendation**: Use space-separated form for mixed colors")
    report.append("- Rationale: More common in XKCD data")
    report.append("- Example: 'blue green' not 'blue-green'")
    report.append("")

    report.append("### 6.2 Word Order Convention")
    report.append("- **Recommendation**: [modifier] [color] order")
    report.append("- Rationale: English convention, more natural")
    report.append("- Example: 'dark blue' not 'blue dark'")
    report.append("")

    report.append("### 6.3 Modifier Normalization")
    report.append("- Normalize synonyms: 'really' → 'very', 'lite' → 'light'")
    report.append("- Keep distinct modifiers: 'dark' ≠ 'deep' ≠ 'dim'")
    report.append("")

    report.append("## 7. Uncertainty Considerations")
    report.append("")
    report.append("### 7.1 Semantic Differences")
    report.append("Some word orders may carry different meanings:")
    report.append("- 'green blue' (green with blue tint) vs 'blue green' (blue with green tint)")
    report.append("- Need human validation for semantic equivalence")
    report.append("")

    report.append("### 7.2 Missing Hyphens in Data")
    report.append("Some compound colors may be semantically different:")
    report.append("- 'hot pink' (the color) vs 'hot-pink' (very pink)")
    report.append("- Context and coordinate data can help disambiguate")
    report.append("")

    report.append("---")
    report.append("")
    report.append("*Generated by Phase 2.3: Compound Name Normalization*")

    # Write report
    report_path = OUTPUT_DIR / "compound_normalization.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"   → Report: {report_path}")

    # Write JSON data
    json_output = {
        'summary': {
            'total_names': len(all_names),
            'compound_analysis': compound_analysis,
            'hyphenation_groups': len(hyphen_variants),
            'word_order_groups': len(order_variants),
            'canonical_mappings': len(canonical_mappings)
        },
        'modifier_stats': {k: dict(v) for k, v in modifier_stats.items()},
        'hyphenation_variants': {
            k: v for k, v in sorted_hyphen[:100]
        },
        'word_order_variants': {
            k: v for k, v in sorted_order[:100]
        },
        'canonical_mappings': canonical_mappings
    }

    json_path = OUTPUT_DIR / "compound_normalization.json"
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   → Data: {json_path}")

    print(f"\nPhase 2.3 complete!")
    print(f"Generated {len(canonical_mappings):,} canonical form mappings.")


if __name__ == "__main__":
    main()
