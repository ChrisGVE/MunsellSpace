#!/usr/bin/env python3
"""
Phase 1: Data Inventory and Exploration

Objective: Understand the raw color naming data before any transformations.

This script inventories all unique color names in both Centore and XKCD datasets,
analyzes their characteristics, and documents data quality observations.

Methodologies Compared:
1. Simple tokenization (split on whitespace/punctuation)
2. Character n-gram analysis (for later typo detection)

Deliverables:
- data_inventory.json: Raw statistics
- data_exploration.md: Observations and findings
"""

import json
import re
import string
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
XKCD_AGGREGATES = PROJECT_ROOT / "overlay-preprocessing/results/xkcd_color_aggregates.json"
OUTPUT_DIR = PROJECT_ROOT / "overlay-preprocessing/investigation"

# Centore's color names (from the paper's ~16,000 CAUS samples)
# Note: We only have the 20 overlay names directly; individual sample names
# would need to be extracted from the original PolyhedronFiles
CENTORE_OVERLAYS = [
    "aqua", "beige", "coral", "fuchsia", "gold", "lavender", "lilac",
    "magenta", "mauve", "navy", "peach", "rose", "rust", "sand",
    "tan", "taupe", "teal", "turquoise", "violet", "wine"
]

CENTORE_BASIC = [
    "black", "blue", "brown", "gray", "green", "orange",
    "pink", "purple", "red", "yellow", "white"
]


def load_xkcd_data():
    """Load XKCD color aggregates."""
    with open(XKCD_AGGREGATES, 'r') as f:
        data = json.load(f)
    return data['statistics']


def analyze_name(name):
    """Analyze a single color name."""
    # Basic metrics
    char_count = len(name)
    word_count = len(name.split())

    # Character classes
    has_hyphen = '-' in name
    has_underscore = '_' in name
    has_digits = any(c.isdigit() for c in name)
    has_special = any(c in string.punctuation and c not in '-_' for c in name)

    # Word analysis
    words = re.split(r'[\s\-_]+', name.lower())
    words = [w for w in words if w]

    return {
        'char_count': char_count,
        'word_count': word_count,
        'has_hyphen': has_hyphen,
        'has_underscore': has_underscore,
        'has_digits': has_digits,
        'has_special': has_special,
        'words': words
    }


def generate_ngrams(text, n=2):
    """Generate character n-grams for a string."""
    text = text.lower()
    return [text[i:i+n] for i in range(len(text) - n + 1)]


def categorize_name(name, word_count):
    """Categorize name by structure."""
    if word_count == 1:
        return 'single_word'
    elif word_count == 2:
        return 'two_word'
    elif word_count == 3:
        return 'three_word'
    else:
        return 'phrase'


def main():
    print("=" * 70)
    print("PHASE 1: DATA INVENTORY AND EXPLORATION")
    print("=" * 70)

    # Load XKCD data
    print("\n[1] Loading XKCD data...")
    xkcd_stats = load_xkcd_data()
    print(f"    Loaded {len(xkcd_stats):,} unique color names from XKCD")

    # Basic inventory
    print("\n[2] Building inventory...")

    inventory = {
        'xkcd': {
            'total_unique_names': len(xkcd_stats),
            'total_responses': sum(s['count'] for s in xkcd_stats),
            'names_by_response_count': {
                '1': len([s for s in xkcd_stats if s['count'] == 1]),
                '2-10': len([s for s in xkcd_stats if 2 <= s['count'] <= 10]),
                '11-100': len([s for s in xkcd_stats if 11 <= s['count'] <= 100]),
                '101-1000': len([s for s in xkcd_stats if 101 <= s['count'] <= 1000]),
                '1001-10000': len([s for s in xkcd_stats if 1001 <= s['count'] <= 10000]),
                '10001+': len([s for s in xkcd_stats if s['count'] > 10000]),
            }
        },
        'centore': {
            'overlays': len(CENTORE_OVERLAYS),
            'basic_colors': len(CENTORE_BASIC),
            'note': 'Individual CAUS sample names not available in this dataset'
        }
    }

    # Analyze name characteristics
    print("\n[3] Analyzing name characteristics...")

    char_counts = []
    word_counts = []
    categories = Counter()
    all_words = Counter()
    bigrams = Counter()

    names_with_hyphens = 0
    names_with_digits = 0
    names_with_special = 0

    for stat in xkcd_stats:
        name = stat['colorname']
        analysis = analyze_name(name)

        char_counts.append(analysis['char_count'])
        word_counts.append(analysis['word_count'])

        category = categorize_name(name, analysis['word_count'])
        categories[category] += 1

        for word in analysis['words']:
            all_words[word] += stat['count']  # Weight by response count

        # Generate bigrams for typo analysis
        for bg in generate_ngrams(name, 2):
            bigrams[bg] += 1

        if analysis['has_hyphen']:
            names_with_hyphens += 1
        if analysis['has_digits']:
            names_with_digits += 1
        if analysis['has_special']:
            names_with_special += 1

    # Compute statistics
    inventory['xkcd']['name_characteristics'] = {
        'char_count': {
            'min': min(char_counts),
            'max': max(char_counts),
            'mean': sum(char_counts) / len(char_counts),
            'median': sorted(char_counts)[len(char_counts) // 2]
        },
        'word_count': {
            'min': min(word_counts),
            'max': max(word_counts),
            'mean': sum(word_counts) / len(word_counts),
            'median': sorted(word_counts)[len(word_counts) // 2]
        },
        'categories': dict(categories),
        'special_characters': {
            'with_hyphens': names_with_hyphens,
            'with_digits': names_with_digits,
            'with_special_chars': names_with_special
        }
    }

    # Top words (weighted by response count)
    inventory['xkcd']['top_words'] = dict(all_words.most_common(100))

    # Top bigrams (for typo pattern detection)
    inventory['xkcd']['top_bigrams'] = dict(bigrams.most_common(50))

    # Identify potential issues
    print("\n[4] Identifying potential data quality issues...")

    issues = {
        'very_long_names': [],
        'single_char_names': [],
        'names_with_numbers': [],
        'potential_sentences': []
    }

    for stat in xkcd_stats:
        name = stat['colorname']
        if len(name) > 30:
            issues['very_long_names'].append({
                'name': name,
                'length': len(name),
                'count': stat['count']
            })
        if len(name) == 1:
            issues['single_char_names'].append({
                'name': name,
                'count': stat['count']
            })
        if any(c.isdigit() for c in name):
            issues['names_with_numbers'].append({
                'name': name,
                'count': stat['count']
            })
        if len(name.split()) > 5:
            issues['potential_sentences'].append({
                'name': name,
                'word_count': len(name.split()),
                'count': stat['count']
            })

    # Sort issues by count
    for key in issues:
        issues[key] = sorted(issues[key], key=lambda x: x['count'], reverse=True)[:20]

    inventory['data_quality_issues'] = issues

    # Known spelling variants (initial detection)
    print("\n[5] Detecting potential spelling variants...")

    # Look for gray/grey pattern
    gray_variants = [s for s in xkcd_stats if 'gray' in s['colorname'] or 'grey' in s['colorname']]

    # Look for common color misspellings
    potential_misspellings = {
        'fuchsia': ['fuschia', 'fushia', 'fuchia', 'fusia'],
        'turquoise': ['turqoise', 'tourquoise', 'turqouise', 'turquois'],
        'lavender': ['lavendar', 'lavander', 'laveneder'],
        'burgundy': ['burgandy', 'burgany', 'burgunday'],
        'chartreuse': ['chartruese', 'chartruse', 'chartruese'],
        'magenta': ['megenta', 'magents', 'mageta'],
        'beige': ['biege', 'bege', 'beig'],
        'cyan': ['cayan', 'cyaan', 'syan']
    }

    found_variants = {}
    for correct, variants in potential_misspellings.items():
        found = []
        for stat in xkcd_stats:
            name = stat['colorname']
            for variant in variants:
                if variant in name.lower():
                    found.append({
                        'name': name,
                        'variant': variant,
                        'count': stat['count']
                    })
        if found:
            found_variants[correct] = sorted(found, key=lambda x: x['count'], reverse=True)

    inventory['potential_spelling_variants'] = {
        'gray_grey_count': len(gray_variants),
        'known_misspellings': found_variants
    }

    # Save inventory
    print("\n[6] Saving results...")

    output_file = OUTPUT_DIR / "data_inventory.json"
    with open(output_file, 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f"    Saved: {output_file}")

    # Generate exploration report
    report = generate_exploration_report(inventory, xkcd_stats)
    report_file = OUTPUT_DIR / "data_exploration.md"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"    Saved: {report_file}")

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total XKCD unique names:     {inventory['xkcd']['total_unique_names']:>10,}")
    print(f"Total XKCD responses:        {inventory['xkcd']['total_responses']:>10,}")
    print(f"Single word names:           {categories['single_word']:>10,}")
    print(f"Multi-word names:            {sum(v for k,v in categories.items() if k != 'single_word'):>10,}")
    print(f"Names with hyphens:          {names_with_hyphens:>10,}")
    print(f"Names with digits:           {names_with_digits:>10,}")
    print(f"Potential misspellings found:{sum(len(v) for v in found_variants.values()):>10,}")
    print("=" * 70)


def generate_exploration_report(inventory, xkcd_stats):
    """Generate markdown exploration report."""

    report = """# Phase 1: Data Exploration Report

## 1. Executive Summary

This report documents the initial exploration of color naming data from the XKCD color survey.

### Key Findings

| Metric | Value |
|--------|-------|
| Total unique color names | {:,} |
| Total survey responses | {:,} |
| Single-word names | {:,} ({:.1f}%) |
| Multi-word names | {:,} ({:.1f}%) |
| Names with hyphens | {:,} |
| Names with digits | {:,} |

""".format(
        inventory['xkcd']['total_unique_names'],
        inventory['xkcd']['total_responses'],
        inventory['xkcd']['name_characteristics']['categories'].get('single_word', 0),
        100 * inventory['xkcd']['name_characteristics']['categories'].get('single_word', 0) / inventory['xkcd']['total_unique_names'],
        sum(v for k, v in inventory['xkcd']['name_characteristics']['categories'].items() if k != 'single_word'),
        100 * sum(v for k, v in inventory['xkcd']['name_characteristics']['categories'].items() if k != 'single_word') / inventory['xkcd']['total_unique_names'],
        inventory['xkcd']['name_characteristics']['special_characters']['with_hyphens'],
        inventory['xkcd']['name_characteristics']['special_characters']['with_digits']
    )

    report += """## 2. Dataset Overview

### 2.1 XKCD Color Survey

The XKCD color survey collected ~3.4 million color naming responses from internet users in 2010.
Each response consists of an RGB color value and a user-provided color name.

**Data Source**: `assets/xkcd/mainsurvey_sqldump.txt`

**Response Distribution**:

| Response Count | Number of Names | Interpretation |
|----------------|-----------------|----------------|
"""

    for bucket, count in inventory['xkcd']['names_by_response_count'].items():
        interpretation = {
            '1': 'Unique/rare names',
            '2-10': 'Uncommon names',
            '11-100': 'Moderately common',
            '101-1000': 'Common names',
            '1001-10000': 'Very common names',
            '10001+': 'Highly popular names'
        }.get(bucket, '')
        report += f"| {bucket} | {count:,} | {interpretation} |\n"

    report += """
### 2.2 Centore Dataset

The Centore dataset consists of ~16,000 CAUS (Color Association of the United States) fabric samples
measured with spectrophotometers. We have access to:

- 20 semantic overlay color names (aqua, beige, coral, etc.)
- 11 basic ISCC-NBS color names

**Note**: Individual CAUS sample names are not directly available in our dataset.
The polyhedron data represents aggregate boundaries, not individual samples.

## 3. Name Characteristics Analysis

### 3.1 Name Length Distribution

| Metric | Characters | Words |
|--------|------------|-------|
| Minimum | {} | {} |
| Maximum | {} | {} |
| Mean | {:.1f} | {:.1f} |
| Median | {} | {} |

""".format(
        inventory['xkcd']['name_characteristics']['char_count']['min'],
        inventory['xkcd']['name_characteristics']['word_count']['min'],
        inventory['xkcd']['name_characteristics']['char_count']['max'],
        inventory['xkcd']['name_characteristics']['word_count']['max'],
        inventory['xkcd']['name_characteristics']['char_count']['mean'],
        inventory['xkcd']['name_characteristics']['word_count']['mean'],
        inventory['xkcd']['name_characteristics']['char_count']['median'],
        inventory['xkcd']['name_characteristics']['word_count']['median']
    )

    report += """### 3.2 Name Structure Categories

| Category | Count | Percentage |
|----------|-------|------------|
"""

    total = inventory['xkcd']['total_unique_names']
    for cat, count in sorted(inventory['xkcd']['name_characteristics']['categories'].items(),
                             key=lambda x: x[1], reverse=True):
        report += f"| {cat} | {count:,} | {100*count/total:.1f}% |\n"

    report += """
### 3.3 Top 20 Words (Weighted by Response Count)

| Rank | Word | Weighted Frequency |
|------|------|-------------------|
"""

    for i, (word, count) in enumerate(list(inventory['xkcd']['top_words'].items())[:20], 1):
        report += f"| {i} | {word} | {count:,} |\n"

    report += """
## 4. Data Quality Observations

### 4.1 Potential Issues Identified

"""

    issues = inventory['data_quality_issues']

    if issues['very_long_names']:
        report += """#### Very Long Names (>30 characters)

These may be sentences, descriptions, or data entry errors:

| Name | Length | Count |
|------|--------|-------|
"""
        for item in issues['very_long_names'][:10]:
            name_truncated = item['name'][:40] + '...' if len(item['name']) > 40 else item['name']
            report += f"| {name_truncated} | {item['length']} | {item['count']} |\n"

    if issues['names_with_numbers']:
        report += """
#### Names Containing Numbers

May indicate specific color codes or measurement artifacts:

| Name | Count |
|------|-------|
"""
        for item in issues['names_with_numbers'][:10]:
            report += f"| {item['name']} | {item['count']} |\n"

    report += """
### 4.2 Spelling Variants Detected

#### Gray vs Grey

Found {:,} names containing either "gray" or "grey".

#### Known Misspelling Patterns

""".format(inventory['potential_spelling_variants']['gray_grey_count'])

    for correct, variants in inventory['potential_spelling_variants']['known_misspellings'].items():
        report += f"\n**{correct}** - Found {len(variants)} variant(s):\n"
        for v in variants[:5]:
            report += f"- `{v['name']}` ({v['count']} responses)\n"

    report += """
## 5. Methodology Notes

### 5.1 Tokenization Approach

For this initial exploration, we used simple whitespace/punctuation tokenization:
- Split on spaces, hyphens, underscores
- Preserve case for analysis (normalize to lowercase for counting)

**Limitation**: Does not handle compound words like "bluegreen" vs "blue green"

### 5.2 N-gram Analysis

Generated character bigrams for future typo detection. The most common bigrams
provide a baseline for identifying unusual character sequences that may indicate typos.

## 6. Uncertainty Considerations

### 6.1 Known Uncertainties

1. **Single-response names**: {:,} names have only 1 response. These could be:
   - Legitimate rare color names
   - Typos or misspellings
   - Nonsense entries

2. **Monitor calibration**: All RGB values are from uncalibrated consumer monitors.
   Systematic bias cannot be assessed without reference data.

3. **Centore sample names**: We lack the individual CAUS sample names, limiting
   direct comparison at the individual color name level.

### 6.2 Suggestions for Uncertainty Reduction

1. **Cross-reference with dictionaries**: Compare against color name dictionaries
   (e.g., X11 colors, CSS colors) to identify likely valid names.

2. **Frequency thresholds**: Consider filtering names with very low response counts
   before entity matching to reduce noise.

3. **Manual review**: High-frequency unusual names should be manually reviewed
   before automated correction.

**Note**: These are suggestions only. No corrections have been applied.

## 7. Files Generated

| File | Description |
|------|-------------|
| `data_inventory.json` | Raw statistics and analysis data |
| `data_exploration.md` | This report |

---

*Generated by Phase 1: Data Inventory and Exploration*
""".format(inventory['xkcd']['names_by_response_count']['1'])

    return report


if __name__ == "__main__":
    main()
