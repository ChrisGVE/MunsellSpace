#!/usr/bin/env python3
"""
Process, analyze, and deduplicate XKCD survey data.

This script:
1. Parses the raw XKCD survey SQL dump directly
2. Normalizes color names (lowercase, HTML entities, quotes, etc.)
3. Analyzes for potential issues
4. Deduplicates based on (name + hex) - keeps unique color assignments
5. Applies cleaning filters
6. Generates analysis report
7. Outputs single cleaned CSV

Deduplication rule: Remove row only if BOTH normalized name AND hex are identical.
Different RGB values for the same name are kept (they represent different user perceptions).

Cleaning filters (applied after deduplication):
- Very short names (<=1 char)
- Very long names (>50 chars)
- Numbers only
- Keyboard mash patterns
- URLs/code snippets
- Only special characters / whitespace

NOT filtered at this stage (per pipeline - filtered at end):
- Profanity / bodily functions
- Non-English names (legitimate color names)
"""

import csv
import html
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

# Paths
DATASETS_DIR = Path(__file__).parent.parent.parent / "datasets"
XKCD_DIR = DATASETS_DIR / "xkcd"
NORMALIZED_DIR = DATASETS_DIR / "normalized"
SOURCE_FILE = XKCD_DIR / "mainsurvey_sqldump.txt"
OUTPUT_FILE = NORMALIZED_DIR / "xkcd_survey_normalized.csv"
REPORT_FILE = NORMALIZED_DIR / "xkcd_survey_analysis_report.txt"

# Patterns to filter during normalization
FILTER_PATTERNS = [
    r'^#?[0-9a-f]{3}$',          # 3-digit hex
    r'^#?[0-9a-f]{6}$',          # 6-digit hex
    r'^#?[0-9a-f]{8}$',          # 8-digit hex (with alpha)
]
FILTER_REGEX = re.compile('|'.join(FILTER_PATTERNS), re.IGNORECASE)

# Patterns for ANALYSIS (not all are filtered)
ANALYSIS_PATTERNS = {
    'very_short': lambda n: len(n) <= 1,
    'very_long': lambda n: len(n) > 50,
    'only_numbers': lambda n: bool(re.match(r'^[\d\s.,-]+$', n)),
    'only_special_chars': lambda n: bool(re.match(r'^[^\w]+$', n)),  # No word chars at all
    'excessive_punctuation': lambda n: len(re.findall(r'[^\w\s]', n)) > 5,
    'repeated_chars': lambda n: bool(re.search(r'(.)\1{4,}', n)),  # 5+ same char
    'keyboard_mash': lambda n: bool(re.search(r'[qwerty]{5,}|[asdfgh]{5,}|[zxcvbn]{5,}|[aeiou]{5,}', n, re.I)),
    'profanity': lambda n: any(w in n for w in ['fuck', 'shit', ' ass ', 'dick', 'cunt', 'bitch', 'nigger', 'faggot']),
    'bodily_functions': lambda n: any(w in n for w in ['puke', 'vomit', 'poop', 'pee ', 'snot', 'booger', 'fart', 'barf']),
    'urls_or_code': lambda n: bool(re.search(r'http|www\.|\.com|\.org|\.net|<[^>]+>|\{|\}|function|var |document\.|script', n)),
    'has_emoji': lambda n: bool(re.search(r'[\U0001F300-\U0001F9FF]', n)),
    'non_ascii': lambda n: bool(re.search(r'[^\x00-\x7F]', n)),
}

# Patterns for CLEANING (these get filtered out)
CLEANING_FILTERS = {
    'very_short': lambda n: len(n) <= 1,
    'very_long': lambda n: len(n) > 50,
    'only_numbers': lambda n: bool(re.match(r'^[\d\s.,-]+$', n)),
    'only_special_chars': lambda n: bool(re.match(r'^[^\w]+$', n)),
    'keyboard_mash': lambda n: bool(re.search(r'[qwerty]{6,}|[asdfgh]{6,}|[zxcvbn]{6,}', n, re.I)),
    'urls_or_code': lambda n: bool(re.search(r'https?://|www\.|<script|<[a-z]+>|document\.|function\s*\(', n, re.I)),
}


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

    # Filter out unwanted patterns (hex codes)
    if not result or FILTER_REGEX.search(result):
        return None

    return result


def get_unicode_category(char):
    """Get human-readable Unicode category for a character."""
    try:
        name = unicodedata.name(char, 'UNKNOWN')
        category = unicodedata.category(char)
        return f"{char} (U+{ord(char):04X}) - {category} - {name}"
    except:
        return f"{char} (U+{ord(char):04X}) - UNKNOWN"


def analyze_utf8_characters(rows):
    """Analyze non-ASCII characters in the dataset."""
    char_counter = Counter()
    char_examples = defaultdict(list)

    for row in rows:
        name = row['name']
        for char in name:
            if ord(char) > 127:  # Non-ASCII
                char_counter[char] += 1
                if len(char_examples[char]) < 3:
                    char_examples[char].append(name[:50])

    # Categorize characters
    categories = defaultdict(list)
    for char, count in char_counter.most_common():
        cat = unicodedata.category(char)
        cat_name = {
            'Ll': 'Lowercase Letter',
            'Lu': 'Uppercase Letter',
            'Lo': 'Other Letter',
            'Mn': 'Nonspacing Mark',
            'Mc': 'Spacing Mark',
            'So': 'Other Symbol (emoji, etc.)',
            'Sm': 'Math Symbol',
            'Sc': 'Currency Symbol',
            'Sk': 'Modifier Symbol',
            'Po': 'Other Punctuation',
            'Ps': 'Open Punctuation',
            'Pe': 'Close Punctuation',
            'Pd': 'Dash Punctuation',
            'Nd': 'Decimal Number',
            'Nl': 'Letter Number',
            'No': 'Other Number',
            'Zs': 'Space Separator',
            'Cc': 'Control Character',
            'Cf': 'Format Character',
        }.get(cat, cat)

        categories[cat_name].append((char, count, char_examples[char]))

    return char_counter, categories


def analyze_code_snippets(rows):
    """Analyze what the code/URL snippets contain."""
    snippets = []
    url_pattern = re.compile(r'https?://|www\.|\.com|\.org|\.net')
    code_pattern = re.compile(r'<[^>]+>|\{|\}|function|var |document\.|script')

    for row in rows:
        name = row['name']
        if url_pattern.search(name):
            snippets.append(('URL', name[:80], row['hex']))
        elif code_pattern.search(name):
            snippets.append(('CODE', name[:80], row['hex']))

    return snippets[:50]  # Return first 50


def load_from_sql_dump():
    """
    Parse the raw XKCD survey SQL dump and normalize names.

    Extracts from answers table: R, G, B, colorname
    Returns list of dicts with: name, name_raw, r, g, b, hex
    """
    print("Parsing XKCD survey SQL dump (this may take a while)...")

    # Pattern to match INSERT INTO answers
    # Format: INSERT INTO "answers" VALUES(id,user_id,timestamp,R,G,B,'colorname');
    pattern = re.compile(
        r'INSERT INTO "answers" VALUES\((\d+),(\d+),([\d.]+),(\d+),(\d+),(\d+),\'(.*?)\'\);'
    )

    rows = []
    line_count = 0
    match_count = 0
    filtered_count = 0

    with open(SOURCE_FILE, 'r', encoding='utf-8', errors='replace') as f:
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

    print(f"  Parsed {match_count:,} answers, {filtered_count:,} filtered during normalization")
    return rows


def analyze_dataset():
    """Load and analyze the XKCD survey dataset."""
    rows = load_from_sql_dump()
    print(f"Loaded {len(rows):,} normalized rows")

    # Statistics
    stats = {
        'total_rows': len(rows),
        'unique_names': len(set(r['name'] for r in rows)),
        'unique_hex': len(set(r['hex'] for r in rows)),
        'unique_name_hex_pairs': len(set((r['name'], r['hex']) for r in rows)),
    }

    # Name length distribution
    name_lengths = [len(r['name']) for r in rows]
    stats['name_length_min'] = min(name_lengths)
    stats['name_length_max'] = max(name_lengths)
    stats['name_length_avg'] = sum(name_lengths) / len(name_lengths)

    # Find issues (for analysis/reporting)
    issues = defaultdict(list)
    issue_counts = Counter()
    for row in rows:
        name = row['name']
        for issue_name, check_fn in ANALYSIS_PATTERNS.items():
            if check_fn(name):
                issue_counts[issue_name] += 1
                if len(issues[issue_name]) < 20:  # Keep up to 20 examples
                    issues[issue_name].append((name, row['hex']))

    stats['issue_counts'] = issue_counts

    # Most common names
    name_counts = Counter(r['name'] for r in rows)
    stats['most_common_names'] = name_counts.most_common(30)

    # Names with most color variations
    name_to_colors = defaultdict(set)
    for row in rows:
        name_to_colors[row['name']].add(row['hex'])

    names_by_variation = [(name, len(colors)) for name, colors in name_to_colors.items()]
    names_by_variation.sort(key=lambda x: -x[1])
    stats['most_varied_names'] = names_by_variation[:30]

    # UTF-8 character analysis
    print("Analyzing UTF-8 characters...")
    char_counter, char_categories = analyze_utf8_characters(rows)
    stats['utf8_char_count'] = len(char_counter)
    stats['utf8_categories'] = char_categories

    # Code snippet analysis
    print("Analyzing code/URL snippets...")
    stats['code_snippets'] = analyze_code_snippets(rows)

    # Deduplicate: keep unique (name, hex) pairs
    print("Deduplicating...")
    seen = set()
    deduplicated = []
    duplicates_removed = 0

    for row in rows:
        key = (row['name'], row['hex'])
        if key not in seen:
            seen.add(key)
            deduplicated.append(row)
        else:
            duplicates_removed += 1

    stats['duplicates_removed'] = duplicates_removed
    stats['rows_after_dedup'] = len(deduplicated)

    # Clean: apply filters
    print("Applying cleaning filters...")
    cleaned = []
    filtered_out = defaultdict(list)

    for row in deduplicated:
        name = row['name']
        filtered = False
        for filter_name, check_fn in CLEANING_FILTERS.items():
            if check_fn(name):
                filtered = True
                if len(filtered_out[filter_name]) < 20:
                    filtered_out[filter_name].append((name[:50], row['hex']))
                break
        if not filtered:
            cleaned.append(row)

    stats['rows_after_clean'] = len(cleaned)
    stats['filtered_out'] = filtered_out
    stats['total_filtered'] = len(deduplicated) - len(cleaned)

    return stats, issues, deduplicated, cleaned


def generate_report(stats, issues):
    """Generate analysis report."""
    report = []
    report.append("=" * 70)
    report.append("XKCD SURVEY ANALYSIS REPORT")
    report.append("=" * 70)
    report.append("")

    report.append("BASIC STATISTICS")
    report.append("-" * 40)
    report.append(f"Total rows:              {stats['total_rows']:>12,}")
    report.append(f"Unique names:            {stats['unique_names']:>12,}")
    report.append(f"Unique hex colors:       {stats['unique_hex']:>12,}")
    report.append(f"Unique (name,hex) pairs: {stats['unique_name_hex_pairs']:>12,}")
    report.append(f"Duplicates removed:      {stats['duplicates_removed']:>12,}")
    report.append(f"Rows after dedup:        {stats['rows_after_dedup']:>12,}")
    report.append(f"Rows filtered (cleaned): {stats['total_filtered']:>12,}")
    report.append(f"Rows after clean:        {stats['rows_after_clean']:>12,}")
    report.append("")

    report.append("NAME LENGTH STATISTICS")
    report.append("-" * 40)
    report.append(f"Min length: {stats['name_length_min']}")
    report.append(f"Max length: {stats['name_length_max']}")
    report.append(f"Avg length: {stats['name_length_avg']:.1f}")
    report.append("")

    report.append("ISSUE COUNTS (total occurrences in raw data)")
    report.append("-" * 40)
    for issue_name, count in sorted(stats['issue_counts'].items(), key=lambda x: -x[1]):
        report.append(f"  {issue_name:25} {count:>10,}")
    report.append("")

    report.append("TOP 30 MOST COMMON NAMES (response count)")
    report.append("-" * 40)
    for name, count in stats['most_common_names']:
        report.append(f"  {count:>6,}x  {name[:50]}")
    report.append("")

    report.append("TOP 30 NAMES WITH MOST COLOR VARIATIONS")
    report.append("-" * 40)
    for name, variation_count in stats['most_varied_names']:
        report.append(f"  {variation_count:>6} colors  {name[:50]}")
    report.append("")

    # UTF-8 character analysis
    report.append("UTF-8 CHARACTER ANALYSIS")
    report.append("-" * 40)
    report.append(f"Total unique non-ASCII characters: {stats['utf8_char_count']}")
    report.append("")

    for cat_name, chars in sorted(stats['utf8_categories'].items()):
        report.append(f"\n  {cat_name} ({len(chars)} unique chars):")
        for char, count, examples in chars[:10]:
            try:
                char_info = f"U+{ord(char):04X} {unicodedata.name(char, '?')[:30]}"
            except:
                char_info = f"U+{ord(char):04X}"
            report.append(f"    '{char}' ({count:,}x) - {char_info}")
            if examples:
                report.append(f"        Example: {examples[0][:40]}")
    report.append("")

    # Code snippets analysis
    report.append("CODE/URL SNIPPETS ANALYSIS")
    report.append("-" * 40)
    for snippet_type, content, hex_color in stats['code_snippets'][:30]:
        report.append(f"  [{snippet_type}] [{hex_color}] {content}")
    report.append("")

    # Filtered entries
    report.append("ENTRIES FILTERED OUT (cleaned)")
    report.append("-" * 40)
    for filter_name, examples in sorted(stats['filtered_out'].items()):
        total = sum(1 for row in stats.get('_deduplicated', [])
                   if CLEANING_FILTERS.get(filter_name, lambda x: False)(row['name']))
        report.append(f"\n  {filter_name.upper()} ({len(examples)} examples):")
        for name, hex_color in examples[:10]:
            report.append(f"    [{hex_color}] {name}")
    report.append("")

    # Issues for review (not filtered)
    report.append("POTENTIAL ISSUES (NOT filtered - for review)")
    report.append("-" * 40)
    for issue_name in ['profanity', 'bodily_functions', 'non_ascii', 'has_emoji']:
        if issue_name in issues:
            examples = issues[issue_name]
            report.append(f"\n  {issue_name.upper()} ({len(examples)} examples shown):")
            for name, hex_color in examples[:10]:
                display_name = name[:45] + "..." if len(name) > 45 else name
                report.append(f"    [{hex_color}] {display_name}")
    report.append("")

    report.append("=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)

    return "\n".join(report)


def save_csv(rows, output_file, description):
    """Save data to CSV."""
    print(f"Saving {len(rows):,} {description} rows...")

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'name_raw', 'r', 'g', 'b', 'hex'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> Saved to {output_file.name}")


def main():
    print("=" * 60)
    print("XKCD Survey Analysis and Deduplication")
    print("=" * 60)
    print()

    stats, issues, deduplicated, cleaned = analyze_dataset()

    # Generate and save report
    report = generate_report(stats, issues)
    print(report)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to {REPORT_FILE.name}")

    # Save cleaned data (single output file)
    save_csv(cleaned, OUTPUT_FILE, "cleaned")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Original rows:      {stats['total_rows']:>12,}")
    print(f"After dedup:        {stats['rows_after_dedup']:>12,} (-{stats['duplicates_removed']:,})")
    print(f"After clean:        {stats['rows_after_clean']:>12,} (-{stats['total_filtered']:,})")
    print()
    print("Output files:")
    print(f"  - {OUTPUT_FILE.name} (deduplicated + filtered)")
    print(f"  - {REPORT_FILE.name} (analysis report)")


if __name__ == "__main__":
    main()
