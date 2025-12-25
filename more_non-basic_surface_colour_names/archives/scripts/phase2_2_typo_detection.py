#!/usr/bin/env python3
"""
Phase 2.2: Typo Detection and Correction

Focuses on identifying typos using frequency-based analysis:
- Low-frequency names similar to high-frequency names are likely typos
- Evaluates correction accuracy against known typos
- Measures false positive rate (valid rare names incorrectly "corrected")

Builds on Phase 2.1 canonical mappings.
"""

import json
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(__file__).parent

# Load cached XKCD data from Phase 2.1
XKCD_CACHE = OUTPUT_DIR / "xkcd_color_counts_cache.json"
CANONICAL_MAPPINGS = OUTPUT_DIR / "canonical_names.json"

# Frequency thresholds
HIGH_FREQ_THRESHOLD = 500  # Names with >= this many responses are "established"
LOW_FREQ_THRESHOLD = 10    # Names with <= this many responses are "rare"

# Edit distance threshold for typo detection
EDIT_SIMILARITY_THRESHOLD = 0.80  # More lenient than Phase 2.1 (0.85)


# ============================================================================
# Typo Detection Functions
# ============================================================================

def edit_similarity(s1: str, s2: str) -> float:
    """Compute similarity ratio between two strings."""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()


def detect_frequency_based_typos(
    color_counts: dict,
    high_freq_threshold: int = HIGH_FREQ_THRESHOLD,
    low_freq_threshold: int = LOW_FREQ_THRESHOLD,
    similarity_threshold: float = EDIT_SIMILARITY_THRESHOLD
) -> dict:
    """
    Detect typos using frequency analysis.

    Logic: If a rare name (low frequency) is very similar to an established
    name (high frequency), the rare name is likely a typo.

    Returns dict: {typo: {'correction': correct_name, 'similarity': score, ...}}
    """
    # Separate high-frequency (established) and low-frequency (candidate typos)
    established = {k: v for k, v in color_counts.items() if v >= high_freq_threshold}
    candidates = {k: v for k, v in color_counts.items() if v <= low_freq_threshold}

    print(f"   Established names (>={high_freq_threshold} responses): {len(established):,}")
    print(f"   Candidate typos (<={low_freq_threshold} responses): {len(candidates):,}")

    typos = {}
    established_names = list(established.keys())

    for i, (candidate, count) in enumerate(candidates.items()):
        if i % 5000 == 0:
            print(f"      Processing {i:,}/{len(candidates):,}...")

        # Find best match among established names
        best_match = None
        best_score = 0

        for est_name in established_names:
            # Quick length filter
            if abs(len(candidate) - len(est_name)) > 3:
                continue

            score = edit_similarity(candidate, est_name)
            if score > best_score and score >= similarity_threshold and score < 1.0:
                best_score = score
                best_match = est_name

        if best_match:
            # Frequency ratio: how much more common is the correction?
            freq_ratio = established[best_match] / max(count, 1)

            typos[candidate] = {
                'correction': best_match,
                'similarity': best_score,
                'typo_count': count,
                'correct_count': established[best_match],
                'frequency_ratio': freq_ratio,
                'confidence': calculate_typo_confidence(best_score, freq_ratio)
            }

    return typos


def calculate_typo_confidence(similarity: float, freq_ratio: float) -> float:
    """
    Calculate confidence that this is actually a typo.

    Higher similarity and higher frequency ratio = higher confidence.
    """
    # Base confidence from similarity
    sim_confidence = similarity

    # Frequency ratio bonus (capped)
    # If correction is 100x more common, add 0.1 to confidence
    freq_bonus = min(0.2, freq_ratio / 500)

    return min(1.0, sim_confidence + freq_bonus)


def categorize_typos(typos: dict) -> dict:
    """
    Categorize detected typos by type.

    Categories:
    - transposition: adjacent letters swapped (teh -> the)
    - substitution: single letter replaced (grean -> green)
    - insertion: extra letter added (purpple -> purple)
    - deletion: letter missing (blu -> blue)
    - multiple: multiple edits combined
    """
    categories = defaultdict(list)

    for typo, info in typos.items():
        correction = info['correction']
        category = classify_edit_type(typo, correction)
        categories[category].append((typo, info))

    return dict(categories)


def classify_edit_type(s1: str, s2: str) -> str:
    """Classify the type of edit between two strings."""
    len1, len2 = len(s1), len(s2)

    if len1 == len2:
        # Same length - could be transposition or substitution
        diffs = sum(c1 != c2 for c1, c2 in zip(s1, s2))
        if diffs == 2:
            # Check for transposition
            for i in range(len1 - 1):
                if s1[i] == s2[i+1] and s1[i+1] == s2[i]:
                    # Check rest matches
                    s1_modified = s1[:i] + s1[i+1] + s1[i] + s1[i+2:]
                    if s1_modified == s2:
                        return 'transposition'
        if diffs == 1:
            return 'substitution'
        return 'multiple'

    elif len1 == len2 + 1:
        # s1 is longer - could be insertion
        for i in range(len1):
            if s1[:i] + s1[i+1:] == s2:
                return 'insertion'
        return 'multiple'

    elif len1 + 1 == len2:
        # s2 is longer - could be deletion in s1
        for i in range(len2):
            if s2[:i] + s2[i+1:] == s1:
                return 'deletion'
        return 'multiple'

    else:
        return 'multiple'


def evaluate_false_positives(
    typos: dict,
    canonical_mappings: dict,
    color_words: set
) -> dict:
    """
    Evaluate potential false positives.

    False positives are rare but valid color names incorrectly flagged as typos.
    """
    false_positive_indicators = []

    for typo, info in typos.items():
        # Check if the typo contains known color words
        words = set(re.split(r'[\s\-_]+', typo.lower()))
        color_word_overlap = words & color_words

        # Check if already in canonical mappings (might conflict)
        in_canonical = typo in canonical_mappings

        # Low similarity might indicate valid variant, not typo
        low_similarity = info['similarity'] < 0.85

        # Check for object/descriptor that might be valid
        object_words = {'chocolate', 'coffee', 'wine', 'sky', 'sea', 'forest',
                       'mint', 'salmon', 'coral', 'peach', 'rust', 'moss',
                       'sand', 'stone', 'clay', 'ivory', 'cream', 'ash'}
        contains_object = bool(words & object_words)

        indicators = {
            'has_color_words': bool(color_word_overlap),
            'in_canonical': in_canonical,
            'low_similarity': low_similarity,
            'contains_object': contains_object
        }

        if any(indicators.values()):
            false_positive_indicators.append({
                'typo': typo,
                'correction': info['correction'],
                'indicators': indicators,
                'risk_score': sum(indicators.values()) / len(indicators)
            })

    return {
        'total_flagged': len(false_positive_indicators),
        'high_risk': [x for x in false_positive_indicators if x['risk_score'] >= 0.5],
        'medium_risk': [x for x in false_positive_indicators if 0.25 <= x['risk_score'] < 0.5],
        'low_risk': [x for x in false_positive_indicators if x['risk_score'] < 0.25]
    }


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 2.2: Typo Detection and Correction")
    print("=" * 70)

    # Load data
    print("\n1. Loading data...")

    print("   Loading XKCD color counts...")
    with open(XKCD_CACHE, 'r') as f:
        xkcd_counts = json.load(f)
    print(f"   → Loaded {len(xkcd_counts):,} color names")

    print("   Loading canonical mappings from Phase 2.1...")
    with open(CANONICAL_MAPPINGS, 'r') as f:
        canonical_mappings = json.load(f)
    print(f"   → Loaded {len(canonical_mappings):,} mappings")

    # Build color word set
    color_words = set()
    for name in xkcd_counts:
        if xkcd_counts[name] >= 100:
            for word in re.split(r'[\s\-_]+', name):
                if len(word) >= 3:
                    color_words.add(word.lower())
    print(f"   → Built color word set: {len(color_words):,} words")

    # Detect typos
    print("\n2. Detecting frequency-based typos...")
    typos = detect_frequency_based_typos(xkcd_counts)
    print(f"   → Detected {len(typos):,} potential typos")

    # Categorize typos
    print("\n3. Categorizing typo types...")
    categories = categorize_typos(typos)
    for cat, items in sorted(categories.items(), key=lambda x: -len(x[1])):
        print(f"   → {cat}: {len(items):,}")

    # Evaluate false positives
    print("\n4. Evaluating false positive risks...")
    fp_analysis = evaluate_false_positives(typos, canonical_mappings, color_words)
    print(f"   → Total flagged for review: {fp_analysis['total_flagged']:,}")
    print(f"   → High risk: {len(fp_analysis['high_risk']):,}")
    print(f"   → Medium risk: {len(fp_analysis['medium_risk']):,}")
    print(f"   → Low risk: {len(fp_analysis['low_risk']):,}")

    # Analyze confidence distribution
    print("\n5. Confidence distribution...")
    high_conf = sum(1 for t in typos.values() if t['confidence'] >= 0.9)
    med_conf = sum(1 for t in typos.values() if 0.8 <= t['confidence'] < 0.9)
    low_conf = sum(1 for t in typos.values() if t['confidence'] < 0.8)
    print(f"   → High confidence (>=0.9): {high_conf:,}")
    print(f"   → Medium confidence (0.8-0.9): {med_conf:,}")
    print(f"   → Low confidence (<0.8): {low_conf:,}")

    # Generate report
    print("\n6. Generating outputs...")

    report = []
    report.append("# Phase 2.2: Typo Detection and Correction Report")
    report.append("")
    report.append("## 1. Executive Summary")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Total color names analyzed | {len(xkcd_counts):,} |")
    report.append(f"| Established names (>={HIGH_FREQ_THRESHOLD} responses) | {sum(1 for v in xkcd_counts.values() if v >= HIGH_FREQ_THRESHOLD):,} |")
    report.append(f"| Rare names (<={LOW_FREQ_THRESHOLD} responses) | {sum(1 for v in xkcd_counts.values() if v <= LOW_FREQ_THRESHOLD):,} |")
    report.append(f"| Potential typos detected | {len(typos):,} |")
    report.append(f"| High confidence typos | {high_conf:,} |")
    report.append(f"| False positive flags | {fp_analysis['total_flagged']:,} |")
    report.append("")

    report.append("## 2. Methodology")
    report.append("")
    report.append("### Frequency-Based Typo Detection")
    report.append("")
    report.append("**Assumption**: If a rare name is very similar to an established name,")
    report.append("the rare name is likely a typo of the established name.")
    report.append("")
    report.append("**Parameters**:")
    report.append(f"- Established threshold: >= {HIGH_FREQ_THRESHOLD} responses")
    report.append(f"- Rare threshold: <= {LOW_FREQ_THRESHOLD} responses")
    report.append(f"- Similarity threshold: {EDIT_SIMILARITY_THRESHOLD}")
    report.append("")
    report.append("**Confidence Calculation**:")
    report.append("- Base confidence = edit similarity score")
    report.append("- Frequency ratio bonus = min(0.2, freq_ratio / 500)")
    report.append("- Higher frequency ratio = higher confidence in correction")
    report.append("")

    report.append("## 3. Typo Categories")
    report.append("")
    report.append("| Category | Count | Description |")
    report.append("|----------|-------|-------------|")
    report.append(f"| Transposition | {len(categories.get('transposition', [])):,} | Adjacent letters swapped |")
    report.append(f"| Substitution | {len(categories.get('substitution', [])):,} | Single letter replaced |")
    report.append(f"| Insertion | {len(categories.get('insertion', [])):,} | Extra letter added |")
    report.append(f"| Deletion | {len(categories.get('deletion', [])):,} | Letter missing |")
    report.append(f"| Multiple | {len(categories.get('multiple', [])):,} | Multiple edits |")
    report.append("")

    report.append("## 4. High-Confidence Typos (Top 50)")
    report.append("")
    report.append("| Typo | Correction | Similarity | Typo Count | Correct Count | Confidence |")
    report.append("|------|------------|------------|------------|---------------|------------|")

    sorted_typos = sorted(typos.items(), key=lambda x: (-x[1]['confidence'], -x[1]['correct_count']))
    for typo, info in sorted_typos[:50]:
        report.append(f"| {typo} | {info['correction']} | {info['similarity']:.2f} | {info['typo_count']} | {info['correct_count']:,} | {info['confidence']:.2f} |")
    report.append("")

    report.append("## 5. Category Examples")
    report.append("")

    for cat in ['transposition', 'substitution', 'insertion', 'deletion']:
        cat_items = categories.get(cat, [])
        if cat_items:
            report.append(f"### {cat.title()} Examples")
            report.append("")
            report.append("| Typo | Correction | Count |")
            report.append("|------|------------|-------|")
            for typo, info in sorted(cat_items, key=lambda x: -x[1]['correct_count'])[:10]:
                report.append(f"| {typo} | {info['correction']} | {info['typo_count']} |")
            report.append("")

    report.append("## 6. False Positive Analysis")
    report.append("")
    report.append("Potential false positives are rare but valid color names flagged as typos.")
    report.append("")
    report.append("### Risk Indicators")
    report.append("- Has color words: Contains known color vocabulary")
    report.append("- In canonical: Already mapped in Phase 2.1")
    report.append("- Low similarity: Edit distance < 0.85 suggests different name, not typo")
    report.append("- Contains object: Has object descriptor (chocolate, wine, etc.)")
    report.append("")

    if fp_analysis['high_risk']:
        report.append("### High-Risk False Positives (Sample)")
        report.append("")
        report.append("| Flagged | Suggested | Risk Score |")
        report.append("|---------|-----------|------------|")
        for item in fp_analysis['high_risk'][:20]:
            report.append(f"| {item['typo']} | {item['correction']} | {item['risk_score']:.2f} |")
        report.append("")

    report.append("## 7. Recommendations")
    report.append("")
    report.append("1. **High-confidence typos** (>=0.9) can be auto-corrected")
    report.append("2. **Medium-confidence typos** (0.8-0.9) should be reviewed")
    report.append("3. **False positive flags** require manual verification")
    report.append("4. **Single-edit typos** (transposition, substitution) are most reliable")
    report.append("5. **Multiple-edit corrections** have higher false positive risk")
    report.append("")

    report.append("## 8. Integration with Phase 2.1")
    report.append("")
    report.append("This analysis complements Phase 2.1 spelling variant detection:")
    report.append("- Phase 2.1: Rule-based and phonetic matching for known variants")
    report.append("- Phase 2.2: Frequency-based detection for unknown typos")
    report.append("- Combined: More comprehensive coverage of spelling errors")
    report.append("")

    report.append("---")
    report.append("")
    report.append("*Generated by Phase 2.2: Typo Detection and Correction*")

    # Write report
    report_path = OUTPUT_DIR / "typo_detection.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    print(f"   → Report: {report_path}")

    # Write JSON data
    json_output = {
        'summary': {
            'total_names': len(xkcd_counts),
            'established_threshold': HIGH_FREQ_THRESHOLD,
            'rare_threshold': LOW_FREQ_THRESHOLD,
            'similarity_threshold': EDIT_SIMILARITY_THRESHOLD,
            'total_typos': len(typos),
            'high_confidence': high_conf,
            'medium_confidence': med_conf,
            'low_confidence': low_conf
        },
        'categories': {cat: len(items) for cat, items in categories.items()},
        'typos': {
            k: v for k, v in sorted_typos[:1000]  # Top 1000 for manageable file size
        },
        'false_positive_analysis': {
            'total_flagged': fp_analysis['total_flagged'],
            'high_risk_count': len(fp_analysis['high_risk']),
            'high_risk_samples': fp_analysis['high_risk'][:50]
        }
    }

    json_path = OUTPUT_DIR / "typo_detection.json"
    with open(json_path, 'w') as f:
        json.dump(json_output, f, indent=2)
    print(f"   → Data: {json_path}")

    # Write typo corrections for downstream use
    corrections_path = OUTPUT_DIR / "typo_corrections.json"
    high_conf_corrections = {
        k: v['correction']
        for k, v in typos.items()
        if v['confidence'] >= 0.85
    }
    with open(corrections_path, 'w') as f:
        json.dump(high_conf_corrections, f, indent=2)
    print(f"   → High-confidence corrections: {corrections_path}")

    print(f"\nPhase 2.2 complete!")
    print(f"Detected {len(typos):,} potential typos, {high_conf:,} high-confidence.")


if __name__ == "__main__":
    main()
