#!/usr/bin/env python3
"""
Process, analyze, and deduplicate XKCD survey data.

This script:
1. Parses the raw XKCD survey SQL dump directly
2. Normalizes color names (separate phase - transforms only)
3. Filters invalid entries (separate phase - removes only)
4. Deduplicates based on (name + hex)
5. Generates analysis report
6. Outputs single cleaned CSV

NORMALIZATION (transforms, does not remove):
- HTML entity decoding
- Fancy quotes to straight quotes
- SQL escape handling
- Lowercase
- Whitespace normalization
- Strip leading punctuation (except apostrophe+alphanumeric like '60s)
- Convert 'word' to "word" (apostrophe pairs around words become quotes)
- Remove surrounding quotes

FILTERING (removes entries, order-independent):
- Empty after normalization
- Trivial content (<=1 alphanumeric after removing special chars)
- Numbers in any base (decimal, hex, octal, binary with prefixes)
- Only special characters
- Very long (>50 chars)
- Keyboard mash patterns
- Code snippets / URLs

NOT filtered (per pipeline - filtered at end):
- Profanity / bodily functions
- Non-English names
"""

import csv
import html
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional, Tuple

# Paths
DATASETS_DIR = Path(__file__).parent.parent.parent / "datasets"
XKCD_DIR = DATASETS_DIR / "xkcd"
NORMALIZED_DIR = DATASETS_DIR / "normalized"
SOURCE_FILE = XKCD_DIR / "mainsurvey_sqldump.txt"
OUTPUT_FILE = NORMALIZED_DIR / "xkcd_survey_normalized.csv"
REPORT_FILE = NORMALIZED_DIR / "xkcd_survey_analysis_report.txt"


# =============================================================================
# NORMALIZATION FUNCTIONS (transforms only, no filtering)
# =============================================================================

def normalize_name(name: str) -> str:
    """
    Normalize a color name. Only transforms, never filters.

    Transformations applied:
    1. Decode HTML entities
    2. Normalize fancy quotes to straight quotes
    3. Handle SQL-escaped quotes
    4. Lowercase
    5. Collapse whitespace
    6. Strip leading punctuation (except apostrophe+alphanumeric)
    7. Convert 'word' to "word"
    8. Remove surrounding quotes
    9. Final trim
    """
    if not name:
        return ""

    result = name

    # 1. Decode HTML entities (&#039; -> ', &#8217; -> ', &amp; -> &)
    result = html.unescape(result)

    # 2. Normalize fancy quotes to straight quotes
    result = result.replace('\u2019', "'")  # Right single quotation mark
    result = result.replace('\u2018', "'")  # Left single quotation mark
    result = result.replace('\u201c', '"')  # Left double quotation mark
    result = result.replace('\u201d', '"')  # Right double quotation mark

    # 3. Handle SQL-escaped single quotes ('' -> ')
    result = result.replace("''", "'")

    # 4. Lowercase
    result = result.lower()

    # 5. Collapse multiple whitespace to single space and trim
    result = re.sub(r'\s+', ' ', result).strip()

    # 6. Strip leading punctuation, EXCEPT apostrophe followed by alphanumeric
    # e.g., "'60s colors" should keep the apostrophe, but "---blue" should become "blue"
    while result and not result[0].isalnum():
        # Check if it's an apostrophe followed by alphanumeric
        if result[0] == "'" and len(result) > 1 and result[1].isalnum():
            break
        result = result[1:].lstrip()

    # 7. Convert 'word' (apostrophe pairs around words) to "word"
    # Match 'word' where word contains no apostrophes
    result = re.sub(r"'([^']+)'", r'"\1"', result)

    # 8. Remove surrounding quotes (single or double)
    if len(result) >= 2:
        if (result[0] == '"' and result[-1] == '"') or \
           (result[0] == "'" and result[-1] == "'"):
            result = result[1:-1].strip()

    # 9. Final trim
    result = result.strip()

    return result


# =============================================================================
# FILTERING FUNCTIONS (each returns True if entry should be REMOVED)
# =============================================================================

def extract_alphanumeric(s: str) -> str:
    """Extract only ASCII alphanumeric characters from string."""
    return ''.join(c for c in s if c.isascii() and c.isalnum())


def is_trivial_content(name: str) -> bool:
    """
    Returns True if name has trivial content (should be filtered).
    After removing all ASCII special characters, if only 0-2 alphanumeric remains.
    """
    alphanum = extract_alphanumeric(name)
    return len(alphanum) <= 2


def is_number_any_base(name: str) -> bool:
    """
    Returns True if name is a number in any base (should be filtered).

    Matches:
    - Plain integers: 42, 123
    - Decimals: 3.14, .5, 5.
    - Hex: 0x1a2b, #ff00ff, 1a2b3c (6 hex digits), abc (3 hex digits)
    - Octal: 0o755, 0755
    - Binary: 0b1010
    - With common suffixes: 42px, 100%, 12pt
    - Negative numbers: -42, -0xff
    - Space-separated numbers: 255 128 64 (RGB values)
    """
    # Strip and lowercase for matching
    s = name.strip().lower()

    # Remove common suffixes
    s = re.sub(r'(px|pt|em|rem|%|deg|rad)$', '', s)

    # Space-separated numbers (like RGB: "255 128 64")
    if re.match(r'^[\d\s.,]+$', s) and re.search(r'\d', s):
        return True

    # Hex color codes: #rgb, #rrggbb, #rrggbbaa
    if re.match(r'^#?[0-9a-f]{3}$', s) or \
       re.match(r'^#?[0-9a-f]{6}$', s) or \
       re.match(r'^#?[0-9a-f]{8}$', s):
        return True

    # Prefixed numbers: 0x (hex), 0o (octal), 0b (binary)
    if re.match(r'^-?0x[0-9a-f]+$', s):  # Hex
        return True
    if re.match(r'^-?0o[0-7]+$', s):      # Octal
        return True
    if re.match(r'^-?0b[01]+$', s):       # Binary
        return True

    # Old-style octal (leading zero)
    if re.match(r'^-?0[0-7]+$', s) and len(s) > 1:
        return True

    # Plain integers and decimals
    if re.match(r'^-?[\d]+\.?[\d]*$', s) or re.match(r'^-?\.[\d]+$', s):
        return True

    # Scientific notation
    if re.match(r'^-?[\d.]+e[+-]?[\d]+$', s):
        return True

    return False


def is_only_special_chars(name: str) -> bool:
    """Returns True if name contains no alphanumeric characters at all."""
    return not any(c.isalnum() for c in name)


def is_too_long(name: str, max_length: int = 50) -> bool:
    """Returns True if name exceeds maximum length."""
    return len(name) > max_length


def is_keyboard_mash(name: str) -> bool:
    """
    Returns True if name appears to be keyboard mashing.

    Detects:
    - Consecutive same-row keyboard characters (qwerty, asdfgh, zxcvbn)
    - Repeated characters (5+ same char in a row)
    - Random character sequences without vowels
    - Short keyboard mash patterns (3-4 chars from home row)
    """
    s = name.lower()

    # Keyboard rows (5+ chars)
    if re.search(r'[qwerty]{5,}|[asdfgh]{5,}|[zxcvbn]{5,}', s):
        return True

    # Repeated characters (5+ same char)
    if re.search(r'(.)\1{4,}', s):
        return True

    # Long sequences without vowels (likely random typing)
    consonant_seqs = re.findall(r'[bcdfghjklmnpqrstvwxz]{6,}', s)
    if consonant_seqs:
        return True

    # Check for "mash" patterns: alternating hands, etc.
    if re.search(r'(asdf|jkl;|qwer|uiop){2,}', s):
        return True

    # Short keyboard mash patterns (3-4 char combinations from keyboard rows)
    short_mash_patterns = {
        # Home row
        'sdf', 'asd', 'dsf', 'dsa', 'fds', 'fsd', 'jkl', 'klj', 'ljk',
        'dfg', 'fgh', 'ghj', 'hjk', 'gfd', 'hgf', 'jhg', 'kjh',
        'asdf', 'sdfg', 'dfgh', 'fghj', 'ghjk', 'hjkl',
        'fdsa', 'gfds', 'hgfd', 'jhgf', 'kjhg', 'lkjh',
        # Top row
        'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
        'ewq', 'rew', 'tre', 'ytr', 'uyt', 'iuy', 'oiu', 'poi',
        'qwer', 'wert', 'erty', 'rtyu', 'tyui', 'yuio', 'uiop',
        'rewq', 'trew', 'ytre', 'uytr', 'iuyt', 'oiuy', 'poiu',
        # Bottom row
        'zxc', 'xcv', 'cvb', 'vbn', 'bnm',
        'cxz', 'vcx', 'bvc', 'nbv', 'mnb',
        'zxcv', 'xcvb', 'cvbn', 'vbnm',
        'vcxz', 'bvcx', 'nbvc', 'mnbv',
        # Mixed/other common mash
        'dfs', 'asf', 'ads', 'sad', 'das', 'gdf', 'sdg', 'sfd', 'sfg',
        'erf', 'rth', 'erg', 'teh', 'hte', 'tna',
    }
    if s in short_mash_patterns:
        return True

    # Repeated single character (any length >= 3)
    if len(s) >= 3 and len(set(s)) == 1:
        return True

    return False


def is_non_color_word(name: str) -> bool:
    """
    Returns True if name is a known non-color word.

    Filters short words that are clearly not color names:
    - Internet expressions (idk, wtf, lol, etc.)
    - Common words (the, and, you, etc.)
    - Names (bob, ian, etc.)
    - Profanity/bodily that aren't color-related
    """
    # Only check short names (efficiency)
    if len(name) > 4:
        return False

    s = name.lower()

    # Non-color words blocklist
    non_color_words = {
        # Internet expressions
        'idk', 'wtf', 'ugh', 'meh', 'lol', 'eww', 'yuk', 'omg', 'brb', 'btw',
        'rofl', 'lmao', 'yolo', 'tbh', 'smh', 'fml', 'imo', 'aka', 'hmm',
        'wow', 'wat', 'wut', 'huh', 'moo', 'boo', 'yay', 'nah', 'duh',
        'idc', 'eew', 'uck', 'bleh', 'derp', 'herp', 'meh',
        # Common words
        'the', 'and', 'you', 'yes', 'bye', 'end', 'but', 'for', 'not', 'are',
        'was', 'has', 'had', 'have', 'been', 'will', 'can', 'did', 'does',
        'this', 'that', 'with', 'from', 'they', 'were', 'said', 'each',
        'she', 'her', 'him', 'his', 'who', 'what', 'when', 'how', 'why',
        'ten', 'odd',
        # Names
        'bob', 'ian', 'joe', 'tom', 'dan', 'sam', 'ben', 'max', 'tim', 'jim',
        'ann', 'amy', 'sue', 'pat', 'kim', 'lee', 'jay', 'ray', 'roy', 'ted',
        # Profanity/bodily/offensive (not color-related)
        'gay', 'poo', 'ass', 'fag', 'sex', 'pee', 'ick', 'die', 'pig', 'pus',
        'cum', 'tit', 'rot',
        # Other non-colors
        'mad', 'bad', 'god', 'dog', 'cat', 'car', 'man', 'run',
        'sit', 'eat', 'see', 'say', 'get', 'got', 'put', 'let', 'set',
        'now', 'new', 'old', 'big', 'hot', 'cut', 'try', 'ask', 'use',
        'way', 'day', 'too', 'two', 'one', 'all', 'any', 'few', 'our',
        'own', 'its', 'out', 'off', 'may', 'just', 'also', 'well', 'back',
        'only', 'come', 'over', 'such', 'take', 'into', 'year', 'some',
        'them', 'then', 'than', 'been', 'call', 'first', 'could', 'other',
        # Abbreviations (not colors)
        'res', 'ref', 'tel', 'etc', 'inc', 'ltd', 'org', 'gov',
        'reg', 'ren', 'rep', 'req', 'ret', 'rev',
    }

    return s in non_color_words


def is_code_or_url(name: str) -> bool:
    """
    Returns True if name appears to be code or URL.

    Detects:
    - URLs (http://, https://, www., .com, .org, .net, .io)
    - HTML tags (<tag>, </tag>)
    - JavaScript code (function, var, document., alert, script)
    - CSS/code braces ({, })
    - Programming patterns
    """
    s = name.lower()

    # URLs
    if re.search(r'https?://|www\.|\.com\b|\.org\b|\.net\b|\.io\b', s):
        return True

    # HTML tags
    if re.search(r'</?[a-z][a-z0-9]*[^>]*>', s):
        return True

    # JavaScript patterns
    if re.search(r'\bfunction\s*\(|\bvar\s+|document\.|alert\s*\(|<script', s):
        return True

    # Code braces (but not emoji-like uses)
    if re.search(r'\{[^}]*\}', s) and not re.search(r'^\{[^}]{1,3}\}$', s):
        return True

    # SQL injection attempts
    if re.search(r";\s*(drop|select|insert|delete|update)\s", s):
        return True

    return False


# =============================================================================
# COMBINED FILTER (applies all filters, returns reason if filtered)
# =============================================================================

def should_filter(name: str) -> Tuple[bool, Optional[str]]:
    """
    Apply all filters to a name.
    Returns (should_filter, reason) where reason is None if not filtered.

    Filters are applied in order of simplicity/cost.
    """
    # Empty check
    if not name:
        return True, "empty"

    # Trivial content (<=1 alphanumeric after removing special chars)
    if is_trivial_content(name):
        return True, "trivial_content"

    # Only special characters
    if is_only_special_chars(name):
        return True, "only_special_chars"

    # Numbers in any base
    if is_number_any_base(name):
        return True, "number"

    # Too long
    if is_too_long(name):
        return True, "too_long"

    # Keyboard mash
    if is_keyboard_mash(name):
        return True, "keyboard_mash"

    # Code or URL
    if is_code_or_url(name):
        return True, "code_or_url"

    # Non-color words (expressions, names, common words)
    if is_non_color_word(name):
        return True, "non_color_word"

    return False, None


# =============================================================================
# ANALYSIS PATTERNS (for reporting, not filtering)
# =============================================================================

ANALYSIS_PATTERNS = {
    'profanity': lambda n: any(w in n for w in ['fuck', 'shit', ' ass ', 'dick', 'cunt', 'bitch', 'nigger', 'faggot']),
    'bodily_functions': lambda n: any(w in n for w in ['puke', 'vomit', 'poop', 'pee ', 'snot', 'booger', 'fart', 'barf']),
    'has_emoji': lambda n: bool(re.search(r'[\U0001F300-\U0001F9FF]', n)),
    'non_ascii': lambda n: bool(re.search(r'[^\x00-\x7F]', n)),
}


# =============================================================================
# DATA LOADING
# =============================================================================

def load_from_sql_dump():
    """
    Parse the raw XKCD survey SQL dump, normalize, and filter.

    Returns list of dicts with: name, name_raw, r, g, b, hex
    Also returns filter statistics.
    """
    print("Parsing XKCD survey SQL dump (this may take a while)...")

    # Pattern to match INSERT INTO answers
    pattern = re.compile(
        r'INSERT INTO "answers" VALUES\((\d+),(\d+),([\d.]+),(\d+),(\d+),(\d+),\'(.*?)\'\);'
    )

    rows = []
    filter_stats = defaultdict(int)
    line_count = 0
    match_count = 0

    with open(SOURCE_FILE, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line_count += 1
            if line_count % 500000 == 0:
                total_filtered = sum(filter_stats.values())
                print(f"  ... processed {line_count:,} lines, found {match_count:,} answers, filtered {total_filtered:,}")

            if 'INSERT INTO "answers"' not in line:
                continue

            match = pattern.match(line.strip())
            if match:
                match_count += 1
                answer_id, user_id, timestamp, r, g, b, name_raw = match.groups()

                # Normalize
                name_normalized = normalize_name(name_raw)

                # Filter
                filtered, reason = should_filter(name_normalized)
                if filtered:
                    filter_stats[reason] += 1
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

    total_filtered = sum(filter_stats.values())
    print(f"  Parsed {match_count:,} answers, {total_filtered:,} filtered")
    print(f"  Filter breakdown:")
    for reason, count in sorted(filter_stats.items(), key=lambda x: -x[1]):
        print(f"    {reason}: {count:,}")

    return rows, filter_stats


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_utf8_characters(rows):
    """Analyze non-ASCII characters in the dataset."""
    char_counter = Counter()
    char_examples = defaultdict(list)

    for row in rows:
        name = row['name']
        for char in name:
            if ord(char) > 127:
                char_counter[char] += 1
                if len(char_examples[char]) < 3:
                    char_examples[char].append(name[:50])

    categories = defaultdict(list)
    for char, count in char_counter.most_common():
        cat = unicodedata.category(char)
        cat_name = {
            'Ll': 'Lowercase Letter',
            'Lu': 'Uppercase Letter',
            'Lo': 'Other Letter',
            'Mn': 'Nonspacing Mark',
            'Mc': 'Spacing Mark',
            'So': 'Other Symbol',
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


def analyze_dataset():
    """Load and analyze the XKCD survey dataset."""
    rows, filter_stats = load_from_sql_dump()
    print(f"Loaded {len(rows):,} rows after normalization and filtering")

    stats = {
        'total_rows': len(rows),
        'unique_names': len(set(r['name'] for r in rows)),
        'unique_hex': len(set(r['hex'] for r in rows)),
        'unique_name_hex_pairs': len(set((r['name'], r['hex']) for r in rows)),
        'filter_stats': dict(filter_stats),
    }

    # Name length distribution
    name_lengths = [len(r['name']) for r in rows]
    if name_lengths:
        stats['name_length_min'] = min(name_lengths)
        stats['name_length_max'] = max(name_lengths)
        stats['name_length_avg'] = sum(name_lengths) / len(name_lengths)

    # Analysis patterns (for reporting)
    issues = defaultdict(list)
    issue_counts = Counter()
    for row in rows:
        name = row['name']
        for issue_name, check_fn in ANALYSIS_PATTERNS.items():
            if check_fn(name):
                issue_counts[issue_name] += 1
                if len(issues[issue_name]) < 20:
                    issues[issue_name].append((name, row['hex']))
    stats['issue_counts'] = issue_counts

    # Most common names
    name_counts = Counter(r['name'] for r in rows)
    stats['most_common_names'] = name_counts.most_common(30)

    # Names with most color variations
    name_to_colors = defaultdict(set)
    for row in rows:
        name_to_colors[row['name']].add(row['hex'])
    names_by_variation = sorted(
        [(name, len(colors)) for name, colors in name_to_colors.items()],
        key=lambda x: -x[1]
    )
    stats['most_varied_names'] = names_by_variation[:30]

    # UTF-8 character analysis
    print("Analyzing UTF-8 characters...")
    char_counter, char_categories = analyze_utf8_characters(rows)
    stats['utf8_char_count'] = len(char_counter)
    stats['utf8_categories'] = char_categories

    # Deduplicate
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

    return stats, issues, deduplicated


def generate_report(stats, issues):
    """Generate analysis report."""
    report = []
    report.append("=" * 70)
    report.append("XKCD SURVEY ANALYSIS REPORT")
    report.append("=" * 70)
    report.append("")

    report.append("BASIC STATISTICS")
    report.append("-" * 40)
    report.append(f"Rows after filtering:    {stats['total_rows']:>12,}")
    report.append(f"Unique names:            {stats['unique_names']:>12,}")
    report.append(f"Unique hex colors:       {stats['unique_hex']:>12,}")
    report.append(f"Unique (name,hex) pairs: {stats['unique_name_hex_pairs']:>12,}")
    report.append(f"Duplicates removed:      {stats['duplicates_removed']:>12,}")
    report.append(f"Final row count:         {stats['rows_after_dedup']:>12,}")
    report.append("")

    report.append("FILTER STATISTICS (entries removed)")
    report.append("-" * 40)
    total_filtered = sum(stats['filter_stats'].values())
    report.append(f"Total filtered:          {total_filtered:>12,}")
    for reason, count in sorted(stats['filter_stats'].items(), key=lambda x: -x[1]):
        report.append(f"  {reason:22} {count:>10,}")
    report.append("")

    if 'name_length_min' in stats:
        report.append("NAME LENGTH STATISTICS")
        report.append("-" * 40)
        report.append(f"Min length: {stats['name_length_min']}")
        report.append(f"Max length: {stats['name_length_max']}")
        report.append(f"Avg length: {stats['name_length_avg']:.1f}")
        report.append("")

    report.append("TOP 30 MOST COMMON NAMES")
    report.append("-" * 40)
    for name, count in stats['most_common_names']:
        report.append(f"  {count:>6,}x  {name[:50]}")
    report.append("")

    report.append("TOP 30 NAMES WITH MOST COLOR VARIATIONS")
    report.append("-" * 40)
    for name, variation_count in stats['most_varied_names']:
        report.append(f"  {variation_count:>6} colors  {name[:50]}")
    report.append("")

    report.append("UTF-8 CHARACTER ANALYSIS")
    report.append("-" * 40)
    report.append(f"Total unique non-ASCII characters: {stats['utf8_char_count']}")
    for cat_name, chars in sorted(stats['utf8_categories'].items()):
        report.append(f"\n  {cat_name} ({len(chars)} unique):")
        for char, count, examples in chars[:10]:
            try:
                char_info = f"U+{ord(char):04X} {unicodedata.name(char, '?')[:25]}"
            except:
                char_info = f"U+{ord(char):04X}"
            report.append(f"    '{char}' ({count:,}x) - {char_info}")
            if examples:
                report.append(f"        Ex: {examples[0][:35]}")
    report.append("")

    report.append("POTENTIAL ISSUES (NOT filtered - for review)")
    report.append("-" * 40)
    for issue_name in ['profanity', 'bodily_functions', 'non_ascii', 'has_emoji']:
        if issue_name in issues:
            examples = issues[issue_name]
            count = stats['issue_counts'].get(issue_name, 0)
            report.append(f"\n  {issue_name.upper()} ({count:,} total, {len(examples)} shown):")
            for name, hex_color in examples[:10]:
                display_name = name[:45] + "..." if len(name) > 45 else name
                report.append(f"    [{hex_color}] {display_name}")
    report.append("")

    report.append("=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)

    return "\n".join(report)


def save_csv(rows, output_file):
    """Save data to CSV."""
    print(f"Saving {len(rows):,} rows...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'name_raw', 'r', 'g', 'b', 'hex'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"  -> Saved to {output_file.name}")


def main():
    print("=" * 60)
    print("XKCD Survey Processing")
    print("=" * 60)
    print()

    stats, issues, final_rows = analyze_dataset()

    report = generate_report(stats, issues)
    print(report)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to {REPORT_FILE.name}")

    save_csv(final_rows, OUTPUT_FILE)

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_filtered = sum(stats['filter_stats'].values())
    print(f"Raw answers parsed:     {stats['total_rows'] + total_filtered:>12,}")
    print(f"Filtered out:           {total_filtered:>12,}")
    print(f"After dedup:            {stats['rows_after_dedup']:>12,}")
    print()
    print("Output files:")
    print(f"  - {OUTPUT_FILE.name}")
    print(f"  - {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
