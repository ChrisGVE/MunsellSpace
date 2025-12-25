#!/usr/bin/env python3
"""
Experiment 2: BERT Token Analysis

Hypothesis: BERT tokenization reveals whether a name contains color-related
tokens, even with spelling variations (gray/grey should tokenize similarly).

Method:
1. Tokenize all names with BERT tokenizer
2. Build color token vocabulary from training set
3. Score names by presence/overlap of color tokens
4. Compare robustness to spelling variations
"""

import json
import time
import argparse
from pathlib import Path
from collections import Counter
import numpy as np
from transformers import AutoTokenizer

from common import (
    load_xkcd_names, get_test_set, BASIC_COLORS, COLOR_MODIFIERS,
    preprocess_name, save_results, INVESTIGATION_DIR
)


def analyze_tokenization(tokenizer, words: list) -> dict:
    """Analyze how words are tokenized."""
    results = {}
    for word in words:
        tokens = tokenizer.tokenize(word)
        token_ids = tokenizer.encode(word, add_special_tokens=False)
        results[word] = {
            'tokens': tokens,
            'token_ids': token_ids,
            'num_tokens': len(tokens)
        }
    return results


def build_color_token_vocabulary(tokenizer) -> set:
    """Build set of tokens that appear in known color terms."""
    color_tokens = set()

    # Tokenize basic colors
    for color in BASIC_COLORS:
        tokens = tokenizer.tokenize(color)
        color_tokens.update(tokens)

    # Tokenize modifiers
    for modifier in COLOR_MODIFIERS:
        tokens = tokenizer.tokenize(modifier)
        color_tokens.update(tokens)

    # Common compound colors
    compounds = [
        'light blue', 'dark green', 'bright red', 'pale yellow',
        'sky blue', 'forest green', 'rose pink', 'midnight blue',
        'bluish green', 'reddish orange', 'yellowish brown'
    ]
    for compound in compounds:
        tokens = tokenizer.tokenize(compound)
        color_tokens.update(tokens)

    return color_tokens


def compute_token_overlap(tokenizer, name: str, color_tokens: set) -> dict:
    """Compute overlap between name tokens and color vocabulary."""
    tokens = tokenizer.tokenize(name.lower())

    if not tokens:
        return {'overlap': 0, 'ratio': 0, 'tokens': [], 'matching': []}

    matching = [t for t in tokens if t in color_tokens]
    overlap = len(matching)
    ratio = overlap / len(tokens)

    return {
        'overlap': overlap,
        'ratio': ratio,
        'tokens': tokens,
        'matching': matching
    }


def run_small_scale(model_name: str = "bert-base-uncased"):
    """Run experiment on test set first."""
    print("=" * 70)
    print("Experiment 2: BERT Token Analysis (Small Scale)")
    print("=" * 70)
    print()

    # Load tokenizer
    print(f"1. Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print(f"   Vocabulary size: {tokenizer.vocab_size:,}")
    print()

    # Analyze spelling variants
    print("2. Analyzing spelling variant tokenization...")
    variants = [
        ('gray', 'grey'),
        ('color', 'colour'),
        ('fuchsia', 'fuschia'),  # common misspelling
        ('turquoise', 'turqoise'),
        ('lavender', 'lavendar'),
    ]

    variant_analysis = {}
    for v1, v2 in variants:
        t1 = tokenizer.tokenize(v1)
        t2 = tokenizer.tokenize(v2)
        variant_analysis[f"{v1}/{v2}"] = {
            v1: t1,
            v2: t2,
            'same_tokens': t1 == t2,
            'token_overlap': len(set(t1) & set(t2)) / max(len(set(t1) | set(t2)), 1)
        }
        print(f"   {v1}: {t1}")
        print(f"   {v2}: {t2}")
        print(f"   Same: {t1 == t2}, Overlap: {variant_analysis[f'{v1}/{v2}']['token_overlap']:.2f}")
        print()

    # Build color token vocabulary
    print("3. Building color token vocabulary...")
    color_tokens = build_color_token_vocabulary(tokenizer)
    print(f"   Color tokens: {len(color_tokens)}")
    print(f"   Sample: {list(color_tokens)[:20]}")
    print()

    # Test on curated test set
    print("4. Testing on curated test set...")
    test_set = get_test_set()
    results = {'test_results': {}, 'variant_analysis': variant_analysis}

    for category, names in test_set.items():
        if category.startswith('edge_'):
            continue

        print(f"\n   Category: {category}")
        if isinstance(names[0], tuple):
            test_names = [n[0] for n in names]
        else:
            test_names = names

        category_results = []
        for name in test_names:
            overlap_info = compute_token_overlap(tokenizer, name, color_tokens)
            category_results.append({
                'name': name,
                **overlap_info
            })

        ratios = [r['ratio'] for r in category_results]
        results['test_results'][category] = {
            'items': category_results,
            'mean_ratio': float(np.mean(ratios)),
            'min_ratio': float(np.min(ratios)),
            'max_ratio': float(np.max(ratios))
        }

        print(f"   Mean token overlap ratio: {np.mean(ratios):.3f}")
        print(f"   Range: [{np.min(ratios):.3f}, {np.max(ratios):.3f}]")

    # Threshold analysis
    print("\n5. Threshold analysis...")
    valid_ratios = []
    invalid_ratios = []

    for cat, data in results['test_results'].items():
        ratios = [item['ratio'] for item in data['items']]
        if 'valid' in cat:
            valid_ratios.extend(ratios)
        elif 'invalid' in cat:
            invalid_ratios.extend(ratios)

    valid_ratios = np.array(valid_ratios)
    invalid_ratios = np.array(invalid_ratios)

    print(f"   Valid colors: mean={np.mean(valid_ratios):.3f}")
    print(f"   Invalid: mean={np.mean(invalid_ratios):.3f}")

    # Find best threshold
    best_f1 = 0
    best_threshold = 0

    for threshold in np.arange(0.0, 1.0, 0.05):
        tp = np.sum(valid_ratios >= threshold)
        fp = np.sum(invalid_ratios >= threshold)
        fn = np.sum(valid_ratios < threshold)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    results['threshold_analysis'] = {
        'best_threshold': float(best_threshold),
        'best_f1': float(best_f1)
    }

    print(f"   Best threshold: {best_threshold:.3f} (F1={best_f1:.3f})")

    # Save results
    save_results(results, 'exp2_bert_small_results.json')

    return results, tokenizer, color_tokens


def run_full_scale(tokenizer, color_tokens, batch_size: int = 10000):
    """Run on full XKCD dataset."""
    print()
    print("=" * 70)
    print("Experiment 2: BERT Token Analysis (Full Scale)")
    print("=" * 70)
    print()

    # Load XKCD names
    print("1. Loading XKCD names...")
    xkcd_data = load_xkcd_names()
    names = list(xkcd_data.keys())
    counts = [xkcd_data[n] for n in names]
    print(f"   Loaded {len(names):,} names")
    print()

    # Process all names
    print(f"2. Computing token overlap...")
    all_ratios = []
    all_overlaps = []

    start_time = time.time()
    for i, name in enumerate(names):
        overlap_info = compute_token_overlap(tokenizer, name, color_tokens)
        all_ratios.append(overlap_info['ratio'])
        all_overlaps.append(overlap_info['overlap'])

        if i % 50000 == 0 and i > 0:
            elapsed = time.time() - start_time
            progress = i / len(names)
            print(f"   Processed {i:,}/{len(names):,} ({progress * 100:.1f}%)")

    print(f"   Total time: {(time.time() - start_time):.1f} seconds")
    print()

    # Analyze results
    print("3. Analyzing results...")
    all_ratios = np.array(all_ratios)
    all_overlaps = np.array(all_overlaps)

    # Distribution
    print("   Token overlap ratio distribution:")
    for threshold in [0.0, 0.25, 0.5, 0.75, 1.0]:
        count = np.sum(all_ratios >= threshold)
        pct = count / len(all_ratios) * 100
        print(f"      ratio >= {threshold:.2f}: {count:,} ({pct:.1f}%)")

    # Sample by ratio
    sorted_indices = np.argsort(all_ratios)

    zero_overlap = [(names[i], all_ratios[i], counts[i])
                    for i in sorted_indices if all_overlaps[i] == 0][:50]
    full_overlap = [(names[i], all_ratios[i], counts[i])
                    for i in sorted_indices if all_ratios[i] == 1.0][-50:]

    print(f"\n   Names with zero color token overlap: {len(zero_overlap)}")
    for name, ratio, count in zero_overlap[:10]:
        print(f"      '{name}' (n={count})")

    print(f"\n   Names with full color token overlap: {len(full_overlap)}")
    for name, ratio, count in full_overlap[-10:]:
        print(f"      '{name}' (n={count})")

    # Build results
    results = {
        'total_names': len(names),
        'distribution': {
            'mean_ratio': float(np.mean(all_ratios)),
            'mean_overlap': float(np.mean(all_overlaps)),
            'zero_overlap_count': int(np.sum(all_overlaps == 0)),
            'full_overlap_count': int(np.sum(all_ratios == 1.0))
        },
        'zero_overlap_samples': [
            {'name': n, 'ratio': float(r), 'count': c}
            for n, r, c in zero_overlap
        ],
        'full_overlap_samples': [
            {'name': n, 'ratio': float(r), 'count': c}
            for n, r, c in full_overlap
        ]
    }

    # Save results
    save_results(results, 'exp2_bert_full_results.json')

    print(f"\n4. Results saved to exp2_bert_full_results.json")

    return results


def main():
    parser = argparse.ArgumentParser(description="BERT Token Analysis Experiment")
    parser.add_argument('--small-only', action='store_true',
                        help='Run only small-scale test')
    parser.add_argument('--full-only', action='store_true',
                        help='Run only full-scale')
    args = parser.parse_args()

    if args.full_only:
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        color_tokens = build_color_token_vocabulary(tokenizer)
        run_full_scale(tokenizer, color_tokens)
    else:
        results, tokenizer, color_tokens = run_small_scale()

        if not args.small_only:
            run_full_scale(tokenizer, color_tokens)


if __name__ == "__main__":
    main()
