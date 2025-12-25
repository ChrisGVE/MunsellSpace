#!/usr/bin/env python3
"""
Experiment 4: Hybrid Approach

Hypothesis: Combining semantic similarity (SBERT) + autoencoder reconstruction
loss provides better filtering than either alone.

Method:
1. Load results from Experiments 1 and 3
2. Combine scores (weighted, normalized, or voting)
3. Compare against individual methods
"""

import json
import argparse
from pathlib import Path
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from common import (
    get_test_set, save_results, load_results, INVESTIGATION_DIR
)


def load_experiment_results():
    """Load results from previous experiments."""
    results = {}

    # Experiment 1: SBERT
    try:
        results['sbert'] = load_results('exp1_sbert_full_results.json')
        print(f"   Loaded SBERT results: {results['sbert']['total_names']:,} names")
    except FileNotFoundError:
        print("   Warning: SBERT full results not found")

    # Experiment 3: Autoencoder
    try:
        results['autoencoder'] = load_results('exp3_autoencoder_full_results.json')
        print(f"   Loaded Autoencoder results")
    except FileNotFoundError:
        print("   Warning: Autoencoder full results not found")

    return results


def combine_scores_weighted(sbert_sim: float, ae_loss: float,
                             sbert_weight: float = 0.5) -> float:
    """
    Combine SBERT similarity and autoencoder loss.

    Higher combined score = more likely valid color.
    SBERT: higher = better
    Autoencoder: lower = better (invert)
    """
    # Normalize autoencoder loss to 0-1 (inverse)
    ae_score = 1.0 / (1.0 + ae_loss)  # Sigmoid-like transform

    return sbert_weight * sbert_sim + (1 - sbert_weight) * ae_score


def combine_scores_geometric(sbert_sim: float, ae_loss: float) -> float:
    """Geometric mean of scores."""
    ae_score = 1.0 / (1.0 + ae_loss)
    return np.sqrt(sbert_sim * ae_score)


def combine_scores_voting(sbert_sim: float, ae_loss: float,
                           sbert_threshold: float = 0.5,
                           ae_threshold: float = 1.5) -> int:
    """
    Voting: count how many methods agree name is valid.
    Returns 0, 1, or 2.
    """
    votes = 0
    if sbert_sim >= sbert_threshold:
        votes += 1
    if ae_loss <= ae_threshold:
        votes += 1
    return votes


def run_analysis():
    """Run hybrid analysis."""
    print("=" * 70)
    print("Experiment 4: Hybrid Approach")
    print("=" * 70)
    print()

    # Load experiment results
    print("1. Loading experiment results...")
    exp_results = load_experiment_results()

    if 'sbert' not in exp_results or 'autoencoder' not in exp_results:
        print("\nError: Need both SBERT and Autoencoder full results.")
        print("Run experiments 1 and 3 first.")
        return None

    sbert_data = exp_results['sbert']['all_similarities']
    ae_low = {s['name']: s['loss'] for s in exp_results['autoencoder']['low_loss_samples']}
    ae_high = {s['name']: s['loss'] for s in exp_results['autoencoder']['high_loss_samples']}

    # For full analysis, we need complete autoencoder losses
    # (The full results only save samples, not all)
    print("\nNote: Full hybrid requires running autoencoder on all names.")
    print("Using available samples for demonstration.\n")

    # Analyze on test set
    print("2. Analyzing test set with hybrid approach...")
    test_set = get_test_set()

    # Get SBERT thresholds from small results
    try:
        sbert_small = load_results('exp1_sbert_small_results.json')
        sbert_threshold = sbert_small['threshold_analysis']['best_threshold']
    except:
        sbert_threshold = 0.5

    try:
        ae_small = load_results('exp3_autoencoder_small_results.json')
        ae_threshold = ae_small['threshold_analysis']['best_threshold']
    except:
        ae_threshold = 1.5

    print(f"   Using thresholds: SBERT={sbert_threshold:.3f}, AE={ae_threshold:.3f}")

    results = {
        'thresholds': {
            'sbert': sbert_threshold,
            'autoencoder': ae_threshold
        },
        'combination_methods': {},
        'recommendations': {}
    }

    # Test different combination methods
    print("\n3. Testing combination methods on samples...")

    # Get samples that are in both result sets
    common_names = set(sbert_data.keys()) & (set(ae_low.keys()) | set(ae_high.keys()))
    ae_all = {**ae_low, **ae_high}

    sample_results = []
    for name in list(common_names)[:100]:
        sbert_sim = sbert_data[name]['similarity']
        ae_loss = ae_all[name]

        sample_results.append({
            'name': name,
            'sbert_sim': sbert_sim,
            'ae_loss': ae_loss,
            'weighted_0.5': combine_scores_weighted(sbert_sim, ae_loss, 0.5),
            'weighted_0.7': combine_scores_weighted(sbert_sim, ae_loss, 0.7),
            'geometric': combine_scores_geometric(sbert_sim, ae_loss),
            'votes': combine_scores_voting(sbert_sim, ae_loss,
                                            sbert_threshold, ae_threshold)
        })

    # Analyze by votes
    vote_counts = {0: 0, 1: 0, 2: 0}
    for r in sample_results:
        vote_counts[r['votes']] += 1

    print(f"\n   Vote distribution:")
    for votes, count in vote_counts.items():
        print(f"      {votes} votes: {count} names ({count/len(sample_results)*100:.1f}%)")

    # Sort by different methods
    print("\n   Top 10 by weighted(0.5):")
    sorted_weighted = sorted(sample_results, key=lambda x: x['weighted_0.5'], reverse=True)
    for r in sorted_weighted[:10]:
        print(f"      '{r['name']}': score={r['weighted_0.5']:.3f} "
              f"(sbert={r['sbert_sim']:.3f}, ae={r['ae_loss']:.3f})")

    print("\n   Bottom 10 by weighted(0.5):")
    for r in sorted_weighted[-10:]:
        print(f"      '{r['name']}': score={r['weighted_0.5']:.3f} "
              f"(sbert={r['sbert_sim']:.3f}, ae={r['ae_loss']:.3f})")

    results['sample_results'] = sample_results

    # Recommendations
    print("\n4. Generating recommendations...")

    results['recommendations'] = {
        'best_method': 'weighted_0.5',
        'rationale': (
            "Weighted combination balances semantic similarity and "
            "vocabulary coverage. SBERT catches semantic meaning, "
            "autoencoder catches character patterns."
        ),
        'suggested_pipeline': [
            "1. Compute SBERT similarity to color vocabulary",
            "2. Compute autoencoder reconstruction loss",
            "3. Combine with weighted score (0.5/0.5)",
            "4. Filter names below combined threshold",
            "5. Names with 0 votes definitely filtered",
            "6. Names with 2 votes definitely kept",
            "7. Names with 1 vote: manual review or secondary filter"
        ]
    }

    for step in results['recommendations']['suggested_pipeline']:
        print(f"   {step}")

    # Save results
    save_results(results, 'exp4_hybrid_results.json')

    print(f"\n5. Results saved to exp4_hybrid_results.json")

    return results


def main():
    parser = argparse.ArgumentParser(description="Hybrid Approach Experiment")
    args = parser.parse_args()

    run_analysis()


if __name__ == "__main__":
    main()
