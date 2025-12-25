#!/usr/bin/env python3
"""
Experiment 1: SBERT Semantic Similarity

Hypothesis: Color names with similar meanings will cluster together in
SBERT embedding space. Names without color meaning will be distant from
known color terms.

Method:
1. Embed all XKCD color names using SBERT
2. Embed known color vocabulary (basic colors + modifiers)
3. For each name, compute max similarity to known color terms
4. Names below threshold likely lack color semantics
"""

import json
import time
import argparse
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from common import (
    load_xkcd_names, load_centore_names, get_test_set,
    BASIC_COLORS, COLOR_MODIFIERS, preprocess_name, save_results,
    INVESTIGATION_DIR
)


def build_color_vocabulary() -> list:
    """Build comprehensive color vocabulary for comparison."""
    vocab = set()

    # Basic colors
    vocab.update(BASIC_COLORS)

    # Basic + modifiers
    for modifier in ['light', 'dark', 'bright', 'pale', 'deep', 'vivid']:
        for color in list(BASIC_COLORS)[:20]:  # Top colors
            vocab.add(f"{modifier} {color}")

    # Compound colors
    for c1 in ['blue', 'green', 'red', 'yellow', 'purple', 'orange']:
        for c2 in ['blue', 'green', 'red', 'yellow', 'purple', 'orange']:
            if c1 != c2:
                vocab.add(f"{c1}ish {c2}")
                vocab.add(f"{c1} {c2}")

    # Metaphorical colors
    metaphors = [
        'sky blue', 'grass green', 'lemon yellow', 'cherry red',
        'forest green', 'ocean blue', 'sunset orange', 'midnight blue',
        'rose pink', 'chocolate brown', 'cream white', 'coal black',
        'blood red', 'sea green', 'sand beige', 'moss green'
    ]
    vocab.update(metaphors)

    return sorted(vocab)


def run_small_scale(model_name: str = "all-MiniLM-L6-v2"):
    """Run experiment on test set first."""
    print("=" * 70)
    print("Experiment 1: SBERT Semantic Similarity (Small Scale)")
    print("=" * 70)
    print()

    # Load model
    print(f"1. Loading SBERT model: {model_name}")
    start = time.time()
    model = SentenceTransformer(model_name)
    print(f"   Loaded in {time.time() - start:.1f}s")
    print()

    # Build vocabulary
    print("2. Building color vocabulary...")
    vocab = build_color_vocabulary()
    print(f"   Vocabulary size: {len(vocab)}")

    # Embed vocabulary
    print("3. Embedding vocabulary...")
    vocab_embeddings = model.encode(vocab, show_progress_bar=True)
    print(f"   Embedding shape: {vocab_embeddings.shape}")
    print()

    # Test on curated test set
    print("4. Testing on curated test set...")
    test_set = get_test_set()

    results = {'test_results': {}, 'threshold_analysis': {}}

    for category, names in test_set.items():
        if category.startswith('edge_'):
            continue  # Skip edge cases for now

        print(f"\n   Category: {category}")
        # Handle tuple format for some test cases
        if isinstance(names[0], tuple):
            test_names = [n[0] for n in names]
        else:
            test_names = names

        # Embed test names
        test_embeddings = model.encode(test_names)

        # Compute similarity to vocabulary
        sims = cosine_similarity(test_embeddings, vocab_embeddings)
        max_sims = np.max(sims, axis=1)

        results['test_results'][category] = {
            'names': test_names,
            'max_similarities': max_sims.tolist(),
            'mean_similarity': float(np.mean(max_sims)),
            'min_similarity': float(np.min(max_sims)),
            'max_similarity': float(np.max(max_sims))
        }

        print(f"   Mean max similarity: {np.mean(max_sims):.3f}")
        print(f"   Range: [{np.min(max_sims):.3f}, {np.max(max_sims):.3f}]")

    # Analyze threshold
    print("\n5. Threshold analysis...")
    valid_sims = []
    invalid_sims = []

    for cat, data in results['test_results'].items():
        if 'valid' in cat:
            valid_sims.extend(data['max_similarities'])
        elif 'invalid' in cat:
            invalid_sims.extend(data['max_similarities'])

    valid_sims = np.array(valid_sims)
    invalid_sims = np.array(invalid_sims)

    print(f"   Valid colors: mean={np.mean(valid_sims):.3f}, std={np.std(valid_sims):.3f}")
    print(f"   Invalid: mean={np.mean(invalid_sims):.3f}, std={np.std(invalid_sims):.3f}")

    # Find optimal threshold
    best_f1 = 0
    best_threshold = 0

    for threshold in np.arange(0.3, 0.8, 0.01):
        tp = np.sum(valid_sims >= threshold)
        fp = np.sum(invalid_sims >= threshold)
        fn = np.sum(valid_sims < threshold)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    results['threshold_analysis'] = {
        'best_threshold': float(best_threshold),
        'best_f1': float(best_f1),
        'valid_mean': float(np.mean(valid_sims)),
        'invalid_mean': float(np.mean(invalid_sims))
    }

    print(f"\n   Best threshold: {best_threshold:.3f} (F1={best_f1:.3f})")

    # Save results
    save_results(results, 'exp1_sbert_small_results.json')

    return results, model, vocab, vocab_embeddings


def run_full_scale(model, vocab, vocab_embeddings, batch_size: int = 1000):
    """Run on full XKCD dataset."""
    print()
    print("=" * 70)
    print("Experiment 1: SBERT Semantic Similarity (Full Scale)")
    print("=" * 70)
    print()

    # Load XKCD names
    print("1. Loading XKCD names...")
    xkcd_data = load_xkcd_names()
    names = list(xkcd_data.keys())
    counts = [xkcd_data[n] for n in names]
    print(f"   Loaded {len(names):,} names")
    print()

    # Process in batches
    print(f"2. Computing embeddings in batches of {batch_size}...")
    all_max_sims = []
    all_best_matches = []

    start_time = time.time()
    for i in range(0, len(names), batch_size):
        batch_names = names[i:i + batch_size]
        batch_embeddings = model.encode(batch_names, show_progress_bar=False)

        # Compute similarity
        sims = cosine_similarity(batch_embeddings, vocab_embeddings)
        max_sims = np.max(sims, axis=1)
        best_idx = np.argmax(sims, axis=1)

        all_max_sims.extend(max_sims.tolist())
        all_best_matches.extend([vocab[idx] for idx in best_idx])

        if (i // batch_size) % 10 == 0:
            elapsed = time.time() - start_time
            progress = (i + len(batch_names)) / len(names)
            eta = elapsed / progress - elapsed if progress > 0 else 0
            print(f"   Processed {i + len(batch_names):,}/{len(names):,} "
                  f"({progress * 100:.1f}%) ETA: {eta / 60:.1f}min")

    print(f"   Total time: {(time.time() - start_time) / 60:.1f} minutes")
    print()

    # Analyze results
    print("3. Analyzing results...")
    all_max_sims = np.array(all_max_sims)

    # Distribution
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    pct_values = np.percentile(all_max_sims, percentiles)

    print("   Similarity distribution:")
    for p, v in zip(percentiles, pct_values):
        print(f"      {p}th percentile: {v:.3f}")

    # Sample low/high similarity names
    sorted_indices = np.argsort(all_max_sims)

    low_sim_samples = [(names[i], all_max_sims[i], all_best_matches[i], counts[i])
                       for i in sorted_indices[:50]]
    high_sim_samples = [(names[i], all_max_sims[i], all_best_matches[i], counts[i])
                        for i in sorted_indices[-50:]]

    print("\n   Lowest similarity samples:")
    for name, sim, match, count in low_sim_samples[:10]:
        print(f"      '{name}' → '{match}' (sim={sim:.3f}, n={count})")

    print("\n   Highest similarity samples:")
    for name, sim, match, count in high_sim_samples[-10:]:
        print(f"      '{name}' → '{match}' (sim={sim:.3f}, n={count})")

    # Build results
    results = {
        'total_names': len(names),
        'distribution': {
            'mean': float(np.mean(all_max_sims)),
            'std': float(np.std(all_max_sims)),
            'min': float(np.min(all_max_sims)),
            'max': float(np.max(all_max_sims)),
            'percentiles': {str(p): float(v) for p, v in zip(percentiles, pct_values)}
        },
        'low_similarity_samples': [
            {'name': n, 'similarity': float(s), 'best_match': m, 'count': c}
            for n, s, m, c in low_sim_samples
        ],
        'high_similarity_samples': [
            {'name': n, 'similarity': float(s), 'best_match': m, 'count': c}
            for n, s, m, c in high_sim_samples
        ],
        'all_similarities': {
            names[i]: {
                'similarity': float(all_max_sims[i]),
                'best_match': all_best_matches[i],
                'count': counts[i]
            }
            for i in range(len(names))
        }
    }

    # Save results
    save_results(results, 'exp1_sbert_full_results.json')

    print(f"\n4. Results saved to exp1_sbert_full_results.json")

    return results


def main():
    parser = argparse.ArgumentParser(description="SBERT Semantic Similarity Experiment")
    parser.add_argument('--small-only', action='store_true',
                        help='Run only small-scale test')
    parser.add_argument('--full-only', action='store_true',
                        help='Run only full-scale (requires previous small run)')
    parser.add_argument('--batch-size', type=int, default=1000,
                        help='Batch size for full-scale processing')
    args = parser.parse_args()

    if args.full_only:
        # Load model and vocab from scratch
        model = SentenceTransformer("all-MiniLM-L6-v2")
        vocab = build_color_vocabulary()
        vocab_embeddings = model.encode(vocab, show_progress_bar=True)
        run_full_scale(model, vocab, vocab_embeddings, args.batch_size)
    else:
        results, model, vocab, vocab_embeddings = run_small_scale()

        if not args.small_only:
            run_full_scale(model, vocab, vocab_embeddings, args.batch_size)


if __name__ == "__main__":
    main()
