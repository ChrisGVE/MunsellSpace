#!/usr/bin/env python3
"""
Phase 2.1: Spelling Variant Detection

Implements ensemble approach for detecting spelling variants:
1. Rule-based: Known variant mappings (US English canonical)
2. Phonetic: Soundex algorithm for sound-alike detection
3. Edit distance: Levenshtein via difflib for typo detection
4. Dictionary: Compare against high-frequency color word reference

Multi-hit agreement strengthens confidence in detected variants.
"""

import json
import os
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
XKCD_DUMP = PROJECT_ROOT / "assets" / "xkcd" / "mainsurvey_sqldump.txt"
CENTORE_NAMES_DIR = PROJECT_ROOT / "PolyhedronFilesJustNames"
OUTPUT_DIR = Path(__file__).parent
PHASE1_INVENTORY = OUTPUT_DIR / "data_inventory.json"

# Edit distance threshold (0-1, higher = stricter)
EDIT_SIMILARITY_THRESHOLD = 0.85
# Minimum response count for reference dictionary
REFERENCE_MIN_COUNT = 500


# ============================================================================
# Rule-Based Variant Mappings (US English Canonical)
# ============================================================================

# Known spelling variants with US English as canonical
US_ENGLISH_VARIANTS = {
    # gray/grey - prefer gray (US)
    "grey": "gray",
    # colour/color - prefer color (US)
    "colour": "color",
}

# Known misspelling mappings (common -> canonical)
KNOWN_MISSPELLINGS = {
    # fuchsia variants
    "fuschia": "fuchsia",
    "fushia": "fuchsia",
    "fuchia": "fuchsia",
    "fusia": "fuchsia",
    "fucsia": "fuchsia",
    # turquoise variants
    "turqoise": "turquoise",
    "turqouise": "turquoise",
    "tourquoise": "turquoise",
    "turquise": "turquoise",
    "turqouoise": "turquoise",
    # lavender variants
    "lavendar": "lavender",
    "lavander": "lavender",
    "lavenader": "lavender",
    # burgundy variants
    "burgandy": "burgundy",
    "burgudny": "burgundy",
    "bergundy": "burgundy",
    # chartreuse variants
    "chartruse": "chartreuse",
    "chartruese": "chartreuse",
    "chartrusse": "chartreuse",
    "chartrusse": "chartreuse",
    # magenta variants
    "megenta": "magenta",
    "magents": "magenta",
    "mageta": "magenta",
    # beige variants
    "biege": "beige",
    "bege": "beige",
    # cyan variants
    "cyaan": "cyan",
    "syan": "cyan",
    "cayan": "cyan",
    # purple variants
    "purpel": "purple",
    "perple": "purple",
    "purle": "purple",
    # orange variants
    "oragne": "orange",
    "ornage": "orange",
    # yellow variants
    "yelow": "yellow",
    "yello": "yellow",
    "yelllow": "yellow",
    # green variants
    "grean": "green",
    "gren": "green",
    # blue variants
    "bleu": "blue",  # French, but common variant
    "bule": "blue",
    "blu": "blue",
    # violet variants
    "voilet": "violet",
    "viloet": "violet",
    # maroon variants
    "marroon": "maroon",
    "maron": "maroon",
    # salmon variants
    "samon": "salmon",
    "samlon": "salmon",
    # coral variants
    "corral": "coral",
    "corol": "coral",
    # mauve variants
    "moave": "mauve",
    "muave": "mauve",
    # taupe variants
    "tope": "taupe",
    "tawpe": "taupe",
    # aqua variants
    "aqau": "aqua",
    "aque": "aqua",
    # peach variants
    "peacch": "peach",
    "peech": "peach",
}


# ============================================================================
# Soundex Implementation (American Soundex)
# ============================================================================

def soundex(name: str, length: int = 4) -> str:
    """
    Compute American Soundex code for a name.

    Soundex encodes consonants by sound, ignoring vowels after the first letter.
    Returns a code of form L### where L is the first letter.
    """
    if not name:
        return ""

    name = name.upper()
    # Keep only letters
    name = ''.join(c for c in name if c.isalpha())
    if not name:
        return ""

    # Soundex coding
    soundex_map = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6',
        # A, E, I, O, U, H, W, Y are not coded (treated as vowels/separators)
    }

    # First letter is kept as-is
    result = [name[0]]

    # Encode remaining letters
    prev_code = soundex_map.get(name[0], '0')
    for char in name[1:]:
        code = soundex_map.get(char, '0')
        if code != '0' and code != prev_code:
            result.append(code)
        prev_code = code

    # Pad with zeros or truncate to length
    code = ''.join(result)
    return (code + '0000')[:length]


def metaphone(name: str) -> str:
    """
    Simplified Metaphone algorithm for phonetic encoding.

    More accurate than Soundex for English words.
    Returns variable-length phonetic code.
    """
    if not name:
        return ""

    name = name.upper()
    name = ''.join(c for c in name if c.isalpha())
    if not name:
        return ""

    # Metaphone transformations (simplified)
    result = []
    i = 0
    while i < len(name):
        c = name[i]
        prev = name[i-1] if i > 0 else ''
        next1 = name[i+1] if i < len(name) - 1 else ''
        next2 = name[i+2] if i < len(name) - 2 else ''

        # Skip duplicate adjacent letters
        if c == prev:
            i += 1
            continue

        if c in 'AEIOU':
            # Only include vowels at start
            if i == 0:
                result.append(c)
        elif c == 'B':
            if not (i == len(name) - 1 and prev == 'M'):
                result.append('B')
        elif c == 'C':
            if next1 in 'IEY':
                result.append('S')
            elif next1 == 'H':
                result.append('X')
                i += 1
            else:
                result.append('K')
        elif c == 'D':
            if next1 == 'G' and next2 in 'IEY':
                result.append('J')
                i += 1
            else:
                result.append('T')
        elif c == 'F':
            result.append('F')
        elif c == 'G':
            if next1 == 'H':
                i += 1
            elif next1 in 'IEY':
                result.append('J')
            else:
                result.append('K')
        elif c == 'H':
            if i == 0 or prev not in 'AEIOU' or next1 in 'AEIOU':
                result.append('H')
        elif c == 'J':
            result.append('J')
        elif c == 'K':
            if prev != 'C':
                result.append('K')
        elif c == 'L':
            result.append('L')
        elif c == 'M':
            result.append('M')
        elif c == 'N':
            result.append('N')
        elif c == 'P':
            if next1 == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
        elif c == 'Q':
            result.append('K')
        elif c == 'R':
            result.append('R')
        elif c == 'S':
            if next1 == 'H':
                result.append('X')
                i += 1
            else:
                result.append('S')
        elif c == 'T':
            if next1 == 'H':
                result.append('0')  # TH sound
                i += 1
            elif next1 == 'I' and next2 in 'AO':
                result.append('X')
            else:
                result.append('T')
        elif c == 'V':
            result.append('F')
        elif c == 'W':
            if next1 in 'AEIOU':
                result.append('W')
        elif c == 'X':
            result.append('KS')
        elif c == 'Y':
            if next1 in 'AEIOU':
                result.append('Y')
        elif c == 'Z':
            result.append('S')

        i += 1

    return ''.join(result)


# ============================================================================
# Edit Distance Functions
# ============================================================================

def edit_similarity(s1: str, s2: str) -> float:
    """
    Compute similarity ratio between two strings using SequenceMatcher.
    Returns value between 0 (completely different) and 1 (identical).
    """
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Compute Levenshtein edit distance between two strings.
    Returns minimum number of single-character edits needed.
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if len(s2) == 0:
        return len(s1)

    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row

    return prev_row[-1]


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_xkcd_color_names(sql_dump_path: Path) -> dict:
    """
    Load color names and response counts from XKCD SQL dump.
    Returns dict: {color_name: response_count}

    Format: INSERT INTO "answers" VALUES(id, user_id, timestamp, r, g, b, 'colorname');
    Uses caching for faster subsequent runs.
    """
    # Check for cached data
    cache_path = OUTPUT_DIR / "xkcd_color_counts_cache.json"
    if cache_path.exists():
        print("      (Loading from cache)")
        with open(cache_path, 'r') as f:
            return json.load(f)

    if not sql_dump_path.exists():
        print(f"Warning: XKCD dump not found at {sql_dump_path}")
        return {}

    color_counts = defaultdict(int)
    # Match: VALUES(id, user_id, timestamp, r, g, b, 'colorname')
    pattern = re.compile(r"VALUES\(\d+,\s*\d+,\s*[\d.]+,\s*\d+,\s*\d+,\s*\d+,\s*'([^']*)'\)")

    print("      (Parsing SQL dump - this may take a few minutes...)")
    line_count = 0
    with open(sql_dump_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_count += 1
            if line_count % 500000 == 0:
                print(f"         Processed {line_count:,} lines...")
            if 'INSERT INTO "answers"' not in line:
                continue
            matches = pattern.findall(line)
            for name in matches:
                if name:
                    color_counts[name.lower().strip()] += 1

    result = dict(color_counts)

    # Save cache
    with open(cache_path, 'w') as f:
        json.dump(result, f)
    print(f"      (Cached to {cache_path})")

    return result


def load_centore_color_names(centore_dir: Path) -> dict:
    """
    Load individual color sample names from Centore PolyhedronFilesJustNames.
    Returns dict: {color_name: {'overlay': overlay_name, 'munsell': munsell_coords}}
    """
    if not centore_dir.exists():
        print(f"Warning: Centore directory not found at {centore_dir}")
        return {}

    centore_names = {}

    for txt_file in centore_dir.glob("*.txt"):
        overlay_name = txt_file.stem.replace("PolyhedronDataFor", "")
        in_samples_section = False

        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()

                if line.startswith("Samples, with Munsell coordinates"):
                    in_samples_section = True
                    continue

                if in_samples_section and line:
                    # Format: "Color Name\tMunsell Coords"
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        color_name = parts[0].strip()
                        munsell = parts[1].strip()
                        if color_name and not color_name[0].isdigit():
                            centore_names[color_name.lower()] = {
                                'overlay': overlay_name,
                                'munsell': munsell,
                                'original': color_name
                            }

    return centore_names


# ============================================================================
# Variant Detection Methods
# ============================================================================

def detect_rule_based_variants(names: set) -> dict:
    """
    Detect variants using predefined rule-based mappings.
    Only matches whole words to avoid incorrect partial matches.
    Returns dict: {variant: {'canonical': canonical, 'method': 'rule', 'confidence': 1.0}}
    """
    variants = {}

    # Combine all rules
    all_rules = {**US_ENGLISH_VARIANTS, **KNOWN_MISSPELLINGS}

    for name in names:
        name_lower = name.lower()
        words = re.split(r'[\s\-_]+', name_lower)

        for variant, canonical in all_rules.items():
            # Check for whole word match
            if variant in words:
                # Replace only whole word
                canonical_name = re.sub(
                    r'\b' + re.escape(variant) + r'\b',
                    canonical,
                    name_lower
                )
                if canonical_name != name_lower:
                    variants[name] = {
                        'canonical': canonical_name,
                        'method': 'rule',
                        'rule': f"{variant} -> {canonical}",
                        'confidence': 1.0
                    }
                    break

    return variants


def detect_phonetic_variants(names: set, reference_dict: dict) -> dict:
    """
    Detect variants using phonetic algorithms (Soundex + Metaphone).
    Compares against reference dictionary of high-frequency names.
    More conservative matching - requires both algorithms to agree.
    Returns dict: {variant: {'canonical': candidate, 'method': 'phonetic', ...}}
    """
    variants = {}

    # Build phonetic index of reference names
    # Index by full name and by individual words
    name_phonetics = {}  # ref_name -> {soundex: set, metaphone: set}

    for ref_name in reference_dict:
        words = re.split(r'[\s\-_]+', ref_name)
        soundex_codes = set()
        metaphone_codes = set()
        for word in words:
            if len(word) >= 4:  # Only index words >= 4 chars
                soundex_codes.add(soundex(word))
                metaphone_codes.add(metaphone(word))
        name_phonetics[ref_name] = {
            'soundex': soundex_codes,
            'metaphone': metaphone_codes
        }

    # Check each name against reference
    for name in names:
        if name in reference_dict:
            continue  # Skip reference names

        name_words = re.split(r'[\s\-_]+', name)
        name_soundex = set()
        name_metaphone = set()

        for word in name_words:
            if len(word) >= 4:
                name_soundex.add(soundex(word))
                name_metaphone.add(metaphone(word))

        if not name_soundex:
            continue

        # Find references where BOTH soundex AND metaphone have overlap
        best_match = None
        best_overlap = 0

        for ref_name, ref_phonetics in name_phonetics.items():
            if ref_name == name:
                continue

            soundex_overlap = name_soundex & ref_phonetics['soundex']
            metaphone_overlap = name_metaphone & ref_phonetics['metaphone']

            # Require BOTH to match for higher confidence
            if soundex_overlap and metaphone_overlap:
                overlap = len(soundex_overlap) + len(metaphone_overlap)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_match = ref_name

        if best_match:
            variants[name] = {
                'canonical': best_match,
                'method': 'phonetic',
                'overlap_score': best_overlap,
                'confidence': 0.7
            }

    return variants


def detect_edit_distance_variants(names: set, reference_dict: dict, threshold: float = 0.85) -> dict:
    """
    Detect variants using edit distance against reference dictionary.
    Returns dict: {variant: {'canonical': candidate, 'method': 'edit_distance', ...}}
    """
    variants = {}

    # Only check names not in reference
    candidates = [n for n in names if n not in reference_dict]
    references = list(reference_dict.keys())

    for name in candidates:
        best_match = None
        best_score = 0

        for ref in references:
            # Quick length filter
            len_diff = abs(len(name) - len(ref))
            if len_diff > 3:
                continue

            score = edit_similarity(name, ref)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = ref

        if best_match:
            variants[name] = {
                'canonical': best_match,
                'method': 'edit_distance',
                'similarity': best_score,
                'edit_distance': levenshtein_distance(name, best_match),
                'confidence': best_score
            }

    return variants


def build_color_word_reference(xkcd_counts: dict, min_count: int = 500) -> set:
    """
    Build reference set of color words from high-frequency XKCD names.
    Extracts individual words from compound names.
    """
    reference_words = set()

    for name, count in xkcd_counts.items():
        if count >= min_count:
            words = name.replace('-', ' ').replace('_', ' ').split()
            for word in words:
                if len(word) >= 3:
                    reference_words.add(word.lower())

    return reference_words


def detect_word_level_variants(names: set, reference_words: set) -> dict:
    """
    Detect word-level variants within compound names.
    For each word in a name, check if it's a variant of a reference word.
    Requires high edit distance threshold to avoid false positives.
    """
    variants = {}
    all_rules = {**US_ENGLISH_VARIANTS, **KNOWN_MISSPELLINGS}

    for name in names:
        words = re.split(r'[\s\-_]+', name)
        corrected_words = []
        corrections = []

        for word in words:
            word_lower = word.lower()
            corrected = word_lower

            # Check rule-based first (exact match only)
            if word_lower in all_rules:
                corrected = all_rules[word_lower]
                corrections.append(f"{word_lower} -> {corrected} (rule)")
            # If no rule match, check edit distance against reference
            elif len(word_lower) >= 4:  # Only check words >= 4 chars
                best_match = None
                best_score = 0
                for ref in reference_words:
                    # Skip if lengths differ too much
                    if abs(len(word_lower) - len(ref)) > 2:
                        continue
                    score = edit_similarity(word_lower, ref)
                    # Use higher threshold (0.85) to reduce false positives
                    if score > best_score and score >= 0.85 and score < 1.0:
                        best_score = score
                        best_match = ref

                if best_match and best_match != word_lower:
                    corrected = best_match
                    corrections.append(f"{word_lower} -> {best_match} (edit:{best_score:.2f})")

            corrected_words.append(corrected)

        if corrections:
            canonical_name = ' '.join(corrected_words)
            variants[name] = {
                'canonical': canonical_name,
                'method': 'word_level',
                'corrections': corrections,
                'confidence': 0.7
            }

    return variants


# ============================================================================
# Ensemble Combination
# ============================================================================

def combine_variant_detections(detections: list) -> dict:
    """
    Combine variant detections from multiple methods.
    Multi-hit agreement increases confidence.

    detections: list of dicts from each detection method
    Returns: combined dict with multi-hit scoring
    """
    combined = {}

    # Merge all detections
    for detection_dict in detections:
        for name, info in detection_dict.items():
            if name not in combined:
                combined[name] = {
                    'canonical_votes': defaultdict(list),
                    'methods': []
                }

            canonical = info['canonical']
            method = info['method']
            confidence = info.get('confidence', 0.5)

            combined[name]['canonical_votes'][canonical].append({
                'method': method,
                'confidence': confidence,
                'details': info
            })
            combined[name]['methods'].append(method)

    # Compute final results with multi-hit scoring
    results = {}
    for name, data in combined.items():
        # Find canonical with most votes
        best_canonical = None
        best_score = 0
        best_votes = []

        for canonical, votes in data['canonical_votes'].items():
            # Multi-hit bonus: each additional method adds confidence
            base_confidence = max(v['confidence'] for v in votes)
            multi_hit_bonus = 0.1 * (len(votes) - 1)
            score = min(1.0, base_confidence + multi_hit_bonus)

            if score > best_score:
                best_score = score
                best_canonical = canonical
                best_votes = votes

        results[name] = {
            'canonical': best_canonical,
            'confidence': best_score,
            'num_methods': len(best_votes),
            'methods': [v['method'] for v in best_votes],
            'details': best_votes
        }

    return results


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 2.1: Spelling Variant Detection")
    print("=" * 70)

    # Load data
    print("\n1. Loading data sources...")

    print("   Loading XKCD color names...")
    xkcd_counts = load_xkcd_color_names(XKCD_DUMP)
    print(f"   → Found {len(xkcd_counts):,} unique XKCD color names")

    print("   Loading Centore color names...")
    centore_names = load_centore_color_names(CENTORE_NAMES_DIR)
    print(f"   → Found {len(centore_names):,} unique Centore color names")

    # Combine all names
    all_names = set(xkcd_counts.keys()) | set(centore_names.keys())
    print(f"   → Combined: {len(all_names):,} unique names across both datasets")

    # Build reference dictionary (high-frequency names)
    print("\n2. Building reference dictionary...")
    reference_dict = {k: v for k, v in xkcd_counts.items() if v >= REFERENCE_MIN_COUNT}
    reference_words = build_color_word_reference(xkcd_counts, REFERENCE_MIN_COUNT)
    print(f"   → Reference names (>={REFERENCE_MIN_COUNT} responses): {len(reference_dict):,}")
    print(f"   → Reference words: {len(reference_words):,}")

    # Run detection methods
    print("\n3. Running variant detection methods...")

    print("   3.1 Rule-based detection...")
    rule_variants = detect_rule_based_variants(all_names)
    print(f"       → Found {len(rule_variants):,} rule-based variants")

    print("   3.2 Phonetic detection (Soundex + Metaphone)...")
    phonetic_variants = detect_phonetic_variants(all_names, reference_dict)
    print(f"       → Found {len(phonetic_variants):,} phonetic variants")

    print("   3.3 Edit distance detection...")
    edit_variants = detect_edit_distance_variants(all_names, reference_dict, EDIT_SIMILARITY_THRESHOLD)
    print(f"       → Found {len(edit_variants):,} edit distance variants")

    print("   3.4 Word-level detection...")
    word_variants = detect_word_level_variants(all_names, reference_words)
    print(f"       → Found {len(word_variants):,} word-level variants")

    # Combine with ensemble
    print("\n4. Combining with ensemble multi-hit scoring...")
    combined = combine_variant_detections([
        rule_variants,
        phonetic_variants,
        edit_variants,
        word_variants
    ])
    print(f"   → Total variants detected: {len(combined):,}")

    # Analyze multi-hit agreement
    single_method = sum(1 for v in combined.values() if v['num_methods'] == 1)
    multi_method = sum(1 for v in combined.values() if v['num_methods'] >= 2)
    high_confidence = sum(1 for v in combined.values() if v['confidence'] >= 0.9)

    print(f"\n5. Confidence analysis:")
    print(f"   → Single-method detection: {single_method:,}")
    print(f"   → Multi-method agreement: {multi_method:,}")
    print(f"   → High confidence (>=0.9): {high_confidence:,}")

    # Generate output
    print("\n6. Generating outputs...")

    # Sort by confidence and response count
    sorted_variants = sorted(
        combined.items(),
        key=lambda x: (
            -x[1]['confidence'],
            -xkcd_counts.get(x[0], 0)
        )
    )

    # Top variants report
    report = []
    report.append("# Phase 2.1: Spelling Variant Detection Report")
    report.append("")
    report.append("## 1. Executive Summary")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Total names analyzed | {len(all_names):,} |")
    report.append(f"| XKCD unique names | {len(xkcd_counts):,} |")
    report.append(f"| Centore unique names | {len(centore_names):,} |")
    report.append(f"| Reference dictionary size | {len(reference_dict):,} |")
    report.append(f"| Total variants detected | {len(combined):,} |")
    report.append(f"| Multi-method agreement | {multi_method:,} |")
    report.append(f"| High confidence (>=0.9) | {high_confidence:,} |")
    report.append("")

    report.append("## 2. Detection Method Results")
    report.append("")
    report.append("| Method | Variants Found |")
    report.append("|--------|---------------|")
    report.append(f"| Rule-based | {len(rule_variants):,} |")
    report.append(f"| Phonetic | {len(phonetic_variants):,} |")
    report.append(f"| Edit distance | {len(edit_variants):,} |")
    report.append(f"| Word-level | {len(word_variants):,} |")
    report.append("")

    report.append("## 3. Methodology")
    report.append("")
    report.append("### 3.1 Rule-Based Detection")
    report.append("- Predefined mappings for known spelling variants")
    report.append("- US English as canonical form (gray > grey)")
    report.append("- Known color name misspellings (fuschia → fuchsia)")
    report.append("- Confidence: 1.0 (highest)")
    report.append("")

    report.append("### 3.2 Phonetic Detection")
    report.append("- Soundex algorithm for consonant-based sound encoding")
    report.append("- Metaphone algorithm for more accurate English phonetics")
    report.append("- Matches against reference dictionary of high-frequency names")
    report.append("- Confidence: 0.8 (both match) or 0.6 (single match)")
    report.append("")

    report.append("### 3.3 Edit Distance Detection")
    report.append("- Levenshtein distance via difflib SequenceMatcher")
    report.append(f"- Threshold: {EDIT_SIMILARITY_THRESHOLD} similarity ratio")
    report.append("- Finds similar spellings within edit threshold")
    report.append("- Confidence: proportional to similarity score")
    report.append("")

    report.append("### 3.4 Word-Level Detection")
    report.append("- Decomposes compound names into words")
    report.append("- Checks each word against reference word set")
    report.append("- Applies rules and edit distance per-word")
    report.append("- Confidence: 0.7")
    report.append("")

    report.append("### 3.5 Ensemble Combination")
    report.append("- Multiple methods vote on canonical form")
    report.append("- Multi-hit agreement adds confidence bonus (+0.1 per additional method)")
    report.append("- Final confidence capped at 1.0")
    report.append("")

    report.append("## 4. High-Impact Variants (Top 50)")
    report.append("")
    report.append("Ranked by confidence and XKCD response count:")
    report.append("")
    report.append("| Variant | Canonical | Confidence | Methods | XKCD Count |")
    report.append("|---------|-----------|------------|---------|------------|")

    for name, info in sorted_variants[:50]:
        count = xkcd_counts.get(name, 0)
        methods_str = ', '.join(info['methods'])
        report.append(f"| {name} | {info['canonical']} | {info['confidence']:.2f} | {methods_str} | {count:,} |")

    report.append("")

    # Multi-hit examples
    report.append("## 5. Multi-Method Agreement Examples")
    report.append("")
    report.append("Variants detected by 2+ methods (higher confidence):")
    report.append("")

    multi_hit_examples = [(n, v) for n, v in sorted_variants if v['num_methods'] >= 2][:30]
    if multi_hit_examples:
        report.append("| Variant | Canonical | Methods | Confidence |")
        report.append("|---------|-----------|---------|------------|")
        for name, info in multi_hit_examples:
            methods_str = ', '.join(info['methods'])
            report.append(f"| {name} | {info['canonical']} | {methods_str} | {info['confidence']:.2f} |")
    report.append("")

    # Dataset-specific analysis
    report.append("## 6. Dataset-Specific Analysis")
    report.append("")

    xkcd_variants = {k: v for k, v in combined.items() if k in xkcd_counts}
    centore_variants = {k: v for k, v in combined.items() if k in centore_names}

    report.append("### 6.1 XKCD Variants")
    report.append(f"- Total XKCD variants: {len(xkcd_variants):,}")
    xkcd_by_count = sum(xkcd_counts.get(k, 0) for k in xkcd_variants)
    report.append(f"- Total affected responses: {xkcd_by_count:,}")
    report.append("")

    report.append("### 6.2 Centore Variants")
    report.append(f"- Total Centore variants: {len(centore_variants):,}")
    report.append("")

    # Overlapping variants
    overlapping = set(xkcd_variants.keys()) & set(centore_variants.keys())
    report.append("### 6.3 Overlapping Variants")
    report.append(f"- Names appearing as variants in both datasets: {len(overlapping):,}")
    report.append("")

    report.append("## 7. Uncertainty Considerations")
    report.append("")
    report.append("### 7.1 False Positive Risks")
    report.append("- Edit distance may match unrelated color names (e.g., 'rust' vs 'rose')")
    report.append("- Phonetic matching may be too aggressive for short words")
    report.append("- Word-level detection may over-correct compound names")
    report.append("")

    report.append("### 7.2 False Negative Risks")
    report.append("- Novel misspellings not in rule database")
    report.append(f"- Edit threshold {EDIT_SIMILARITY_THRESHOLD} may miss some typos")
    report.append("- Phonetic algorithms may miss some sound-alike variants")
    report.append("")

    report.append("### 7.3 Recommendations")
    report.append("1. High-confidence variants (>=0.9) can be applied automatically")
    report.append("2. Multi-method variants are more reliable than single-method")
    report.append("3. High-response-count variants should be prioritized")
    report.append("4. Consider manual review for edge cases")
    report.append("")

    report.append("---")
    report.append("")
    report.append("*Generated by Phase 2.1: Spelling Variant Detection*")

    # Write report
    report_path = OUTPUT_DIR / "spelling_variants.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"   → Report: {report_path}")

    # Write JSON data
    json_output = {
        'summary': {
            'total_names': len(all_names),
            'xkcd_names': len(xkcd_counts),
            'centore_names': len(centore_names),
            'reference_dict_size': len(reference_dict),
            'reference_min_count': REFERENCE_MIN_COUNT,
            'edit_threshold': EDIT_SIMILARITY_THRESHOLD,
            'total_variants': len(combined),
            'single_method_variants': single_method,
            'multi_method_variants': multi_method,
            'high_confidence_variants': high_confidence
        },
        'method_results': {
            'rule_based': len(rule_variants),
            'phonetic': len(phonetic_variants),
            'edit_distance': len(edit_variants),
            'word_level': len(word_variants)
        },
        'variants': {
            name: {
                'canonical': info['canonical'],
                'confidence': info['confidence'],
                'num_methods': info['num_methods'],
                'methods': info['methods'],
                'xkcd_count': xkcd_counts.get(name, 0),
                'in_centore': name in centore_names
            }
            for name, info in sorted_variants
        },
        'us_english_rules': US_ENGLISH_VARIANTS,
        'known_misspellings': KNOWN_MISSPELLINGS
    }

    json_path = OUTPUT_DIR / "spelling_variants.json"
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   → Data: {json_path}")

    # Write canonical mappings for downstream use
    canonical_path = OUTPUT_DIR / "canonical_names.json"
    canonical_mappings = {
        name: info['canonical']
        for name, info in sorted_variants
        if info['confidence'] >= 0.7
    }
    with open(canonical_path, 'w') as f:
        json.dump(canonical_mappings, f, indent=2)
    print(f"   → Canonical mappings: {canonical_path}")

    print("\nPhase 2.1 complete!")
    print(f"Detected {len(combined):,} spelling variants with {multi_method:,} multi-method agreements.")


if __name__ == "__main__":
    main()
