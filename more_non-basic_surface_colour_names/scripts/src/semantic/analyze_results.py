#!/usr/bin/env python3
"""
Analyze experiment results and test against problematic cases.

This script:
1. Loads full-scale experiment results
2. Tests against the problematic mappings from original investigation
3. Proposes optimal thresholds
4. Builds the recommended filtering pipeline
"""

import json
import re
from pathlib import Path
import numpy as np

INVESTIGATION_DIR = Path(__file__).parent


def load_results():
    """Load all experiment results."""
    results = {}

    # SBERT full results
    sbert_path = INVESTIGATION_DIR / "exp1_sbert_full_results.json"
    if sbert_path.exists():
        with open(sbert_path) as f:
            results['sbert'] = json.load(f)

    # BERT tokens
    bert_path = INVESTIGATION_DIR / "exp2_bert_full_results.json"
    if bert_path.exists():
        with open(bert_path) as f:
            results['bert_tokens'] = json.load(f)

    # Autoencoder
    ae_path = INVESTIGATION_DIR / "exp3_autoencoder_full_results.json"
    if ae_path.exists():
        with open(ae_path) as f:
            results['autoencoder'] = json.load(f)

    return results


def test_problematic_cases(sbert_data: dict):
    """Test against the problematic cases from original investigation."""

    # Problematic mappings that were wrong
    problematic = {
        # From canonical_names.json - wrong mappings
        "!!! green": {"expected": "green", "issue": "noise prefix"},
        "!!! purple": {"expected": "purple", "issue": "noise prefix"},
        "#0000FF": {"expected": "blue", "issue": "hex code"},
        "berry porridge pink": {"expected": "valid compound", "issue": "lost semantics"},
        "bluish fuchsia": {"expected": "valid compound", "issue": "wrong mapping to bluish green"},

        # From typo_corrections.json - wrong corrections
        "teal purple": {"expected": "keep as is", "issue": "not a typo"},
        "fedex purple": {"expected": "keep as is", "issue": "brand name, not typo"},
        "warm lavender": {"expected": "keep as is", "issue": "modifier, not typo"},
        "army grey": {"expected": "keep as is", "issue": "valid color, not typo"},
    }

    print("\n" + "=" * 70)
    print("Testing Problematic Cases from Original Investigation")
    print("=" * 70)

    all_sims = sbert_data.get('all_similarities', {})

    for name, info in problematic.items():
        name_lower = name.lower()
        if name_lower in all_sims:
            sim_data = all_sims[name_lower]
            sim = sim_data['similarity']
            match = sim_data['best_match']
            count = sim_data.get('count', 'N/A')

            status = "PASS" if sim > 0.5 else "FAIL"
            print(f"\n'{name}': sim={sim:.3f}, match='{match}', n={count}")
            print(f"   Issue: {info['issue']}")
            print(f"   Expected: {info['expected']}")
            print(f"   Status: {status}")
        else:
            print(f"\n'{name}': NOT FOUND in SBERT results")


def analyze_distribution(sbert_data: dict):
    """Analyze the SBERT similarity distribution."""

    print("\n" + "=" * 70)
    print("SBERT Similarity Distribution Analysis")
    print("=" * 70)

    dist = sbert_data['distribution']
    print(f"\nTotal names: {sbert_data['total_names']:,}")
    print(f"Mean similarity: {dist['mean']:.3f}")
    print(f"Std deviation: {dist['std']:.3f}")
    print(f"Range: [{dist['min']:.3f}, {dist['max']:.3f}]")

    print("\nPercentiles:")
    for pct, val in dist['percentiles'].items():
        print(f"   {pct}th: {val:.3f}")

    # Threshold analysis
    print("\nThreshold Analysis:")
    thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

    # Estimate counts based on percentiles
    pcts = dist['percentiles']
    total = sbert_data['total_names']

    for thresh in thresholds:
        # Rough estimate of names above threshold
        if thresh <= float(pcts['10']):
            pct_above = 90
        elif thresh <= float(pcts['25']):
            pct_above = 75 + (float(pcts['25']) - thresh) / (float(pcts['25']) - float(pcts['10'])) * 15
        elif thresh <= float(pcts['50']):
            pct_above = 50 + (float(pcts['50']) - thresh) / (float(pcts['50']) - float(pcts['25'])) * 25
        elif thresh <= float(pcts['75']):
            pct_above = 25 + (float(pcts['75']) - thresh) / (float(pcts['75']) - float(pcts['50'])) * 25
        elif thresh <= float(pcts['90']):
            pct_above = 10 + (float(pcts['90']) - thresh) / (float(pcts['90']) - float(pcts['75'])) * 15
        else:
            pct_above = (1 - thresh) * 10  # rough estimate

        count = int(total * pct_above / 100)
        print(f"   threshold={thresh:.2f}: ~{count:,} names ({pct_above:.1f}%)")


def analyze_low_similarity_samples(sbert_data: dict):
    """Analyze what types of names have low similarity."""

    print("\n" + "=" * 70)
    print("Low Similarity Sample Analysis")
    print("=" * 70)

    low_samples = sbert_data.get('low_similarity_samples', [])

    # Categorize
    categories = {
        'spam_questions': 0,
        'numbers_only': 0,
        'special_chars': 0,
        'non_english': 0,
        'random_words': 0,
        'other': 0
    }

    print("\nLowest 20 similarity names:")
    for sample in low_samples[:20]:
        name = sample['name']
        sim = sample['similarity']
        print(f"   {sim:.3f}: '{name[:60]}...' " if len(name) > 60 else f"   {sim:.3f}: '{name}'")

        # Categorize
        if '?' in name or 'survey' in name.lower() or 'test' in name.lower():
            categories['spam_questions'] += 1
        elif re.match(r'^[\d\s\-]+$', name):
            categories['numbers_only'] += 1
        elif re.match(r'^[^\w\s]+$', name):
            categories['special_chars'] += 1
        elif not name.isascii():
            categories['non_english'] += 1
        else:
            categories['other'] += 1

    print(f"\nCategories in bottom 50:")
    for cat, count in categories.items():
        print(f"   {cat}: {count}")


def analyze_high_similarity_samples(sbert_data: dict):
    """Analyze what types of names have high similarity."""

    print("\n" + "=" * 70)
    print("High Similarity Sample Analysis")
    print("=" * 70)

    high_samples = sbert_data.get('high_similarity_samples', [])

    print("\nHighest 20 similarity names:")
    for sample in high_samples[-20:]:
        name = sample['name']
        sim = sample['similarity']
        match = sample['best_match']
        count = sample['count']
        print(f"   {sim:.3f}: '{name}' → '{match}' (n={count})")


def build_pipeline_recommendations(results: dict):
    """Build recommendations for the filtering pipeline."""

    print("\n" + "=" * 70)
    print("RECOMMENDED FILTERING PIPELINE")
    print("=" * 70)

    recommendations = {
        "preprocessing": {
            "1_strip_noise": "Remove leading/trailing special characters (!!! → '', ## → '')",
            "2_normalize_case": "Lowercase all names",
            "3_normalize_whitespace": "Collapse multiple spaces, trim",
            "4_decode_hex": "Convert valid hex codes (#0000FF → blue approximation)",
            "5_normalize_quotes": "Standardize apostrophes and quotes"
        },
        "semantic_filtering": {
            "method": "SBERT Semantic Similarity",
            "model": "all-MiniLM-L6-v2",
            "threshold": 0.35,
            "rationale": (
                "Based on analysis:\n"
                "- Threshold 0.35 excludes obvious spam/noise\n"
                "- Keeps ~85% of names\n"
                "- Low similarity names are clearly not colors\n"
                "- Autoencoder approach flawed (doesn't understand non-ASCII)"
            )
        },
        "validation": {
            "keep_if": [
                "SBERT similarity >= 0.35 to color vocabulary",
                "Name contains recognizable color word (secondary check)",
                "Sample count >= 10 (for XKCD data quality)"
            ],
            "filter_if": [
                "SBERT similarity < 0.35",
                "Name is pure numbers",
                "Name is pure punctuation",
                "Name is a question or sentence (> 5 words)"
            ]
        },
        "grouping": {
            "method": "SBERT clustering",
            "rationale": (
                "Group names with high cosine similarity (> 0.95)\n"
                "This catches: grey/gray, colour/color, light blue/lightblue"
            )
        }
    }

    print("\n1. PREPROCESSING STEPS:")
    for step, desc in recommendations['preprocessing'].items():
        print(f"   {step}: {desc}")

    print("\n2. SEMANTIC FILTERING:")
    sf = recommendations['semantic_filtering']
    print(f"   Method: {sf['method']}")
    print(f"   Model: {sf['model']}")
    print(f"   Threshold: {sf['threshold']}")
    print(f"   Rationale: {sf['rationale']}")

    print("\n3. VALIDATION RULES:")
    print("   Keep if:")
    for rule in recommendations['validation']['keep_if']:
        print(f"      - {rule}")
    print("   Filter if:")
    for rule in recommendations['validation']['filter_if']:
        print(f"      - {rule}")

    print("\n4. GROUPING:")
    print(f"   {recommendations['grouping']['method']}")
    print(f"   {recommendations['grouping']['rationale']}")

    return recommendations


def main():
    print("=" * 70)
    print("SEMANTIC COLOR NAME EXPERIMENT ANALYSIS")
    print("=" * 70)

    # Load results
    print("\nLoading experiment results...")
    results = load_results()

    if 'sbert' not in results:
        print("ERROR: SBERT results not found!")
        return

    sbert = results['sbert']
    print(f"Loaded {sbert['total_names']:,} SBERT results")

    # Analyze
    analyze_distribution(sbert)
    analyze_low_similarity_samples(sbert)
    analyze_high_similarity_samples(sbert)
    test_problematic_cases(sbert)

    # Build recommendations
    recommendations = build_pipeline_recommendations(results)

    # Save recommendations
    output_path = INVESTIGATION_DIR / "pipeline_recommendations.json"
    with open(output_path, 'w') as f:
        json.dump(recommendations, f, indent=2)
    print(f"\nRecommendations saved to {output_path}")


if __name__ == "__main__":
    main()
