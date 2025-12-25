#!/usr/bin/env python3
"""
Full-scale validation of the color name pipeline.

Tests the pipeline on all 175K XKCD names and analyzes:
1. How many pass/fail at each stage
2. Distribution of similarity scores
3. Quality of filtering by sample count
4. Edge case analysis
"""

import json
import time
from pathlib import Path
from collections import Counter
import numpy as np

from color_name_pipeline import ColorNamePipeline
from common import load_xkcd_names, save_results, INVESTIGATION_DIR


def run_full_validation():
    """Run full-scale validation."""
    print("=" * 70)
    print("FULL-SCALE PIPELINE VALIDATION")
    print("=" * 70)
    print()

    # Load data
    print("1. Loading data...")
    xkcd_data = load_xkcd_names()
    names = list(xkcd_data.keys())
    counts = {n: xkcd_data[n] for n in names}
    total_responses = sum(counts.values())
    print(f"   Unique names: {len(names):,}")
    print(f"   Total responses: {total_responses:,}")
    print()

    # Initialize pipeline (cached mode for speed)
    print("2. Initializing pipeline...")
    pipeline = ColorNamePipeline(load_model=False)
    print()

    # Process all names
    print("3. Processing all names...")
    start_time = time.time()

    results = {
        'valid': [],
        'invalid': [],
        'preprocessing_changes': [],
        'filter_reasons': Counter()
    }

    for i, name in enumerate(names):
        count = counts[name]
        result = pipeline.process(name, sample_count=count)

        if result['valid']:
            results['valid'].append({
                'name': name,
                'cleaned': result['cleaned'],
                'similarity': result['similarity'],
                'best_match': result['best_match'],
                'count': count
            })
        else:
            results['invalid'].append({
                'name': name,
                'cleaned': result['cleaned'],
                'similarity': result['similarity'],
                'reason': result['reason'],
                'count': count
            })
            results['filter_reasons'][result['reason']] += 1

        # Track preprocessing changes
        if result['cleaned'] != name.lower().strip():
            results['preprocessing_changes'].append({
                'original': name,
                'cleaned': result['cleaned'],
                'steps': result['preprocessing']['steps']
            })

        if (i + 1) % 50000 == 0:
            print(f"   Processed {i+1:,}/{len(names):,} "
                  f"({(i+1)/len(names)*100:.1f}%)")

    elapsed = time.time() - start_time
    print(f"   Complete in {elapsed:.1f}s ({len(names)/elapsed:.0f} names/sec)")
    print()

    # Analyze results
    print("4. Analyzing results...")
    valid_count = len(results['valid'])
    invalid_count = len(results['invalid'])
    valid_responses = sum(r['count'] for r in results['valid'])
    invalid_responses = sum(r['count'] for r in results['invalid'])

    print(f"\n   OVERALL SUMMARY:")
    print(f"   ├─ Valid names: {valid_count:,} ({valid_count/len(names)*100:.1f}%)")
    print(f"   │  └─ Responses: {valid_responses:,} ({valid_responses/total_responses*100:.1f}%)")
    print(f"   └─ Invalid names: {invalid_count:,} ({invalid_count/len(names)*100:.1f}%)")
    print(f"      └─ Responses: {invalid_responses:,} ({invalid_responses/total_responses*100:.1f}%)")

    print(f"\n   FILTER REASONS:")
    for reason, count in results['filter_reasons'].most_common():
        pct = count / invalid_count * 100
        print(f"   ├─ {reason}: {count:,} ({pct:.1f}%)")

    print(f"\n   PREPROCESSING CHANGES: {len(results['preprocessing_changes']):,} names modified")

    # Analyze by sample count
    print("\n   QUALITY BY SAMPLE COUNT:")
    count_brackets = [
        (1, 1, "n=1 (noise)"),
        (2, 10, "n=2-10"),
        (11, 100, "n=11-100"),
        (101, 1000, "n=101-1000"),
        (1001, float('inf'), "n>1000 (reliable)")
    ]

    for low, high, label in count_brackets:
        valid_in_bracket = [r for r in results['valid']
                           if low <= r['count'] <= high]
        invalid_in_bracket = [r for r in results['invalid']
                              if low <= r['count'] <= high]
        total_bracket = len(valid_in_bracket) + len(invalid_in_bracket)

        if total_bracket > 0:
            valid_pct = len(valid_in_bracket) / total_bracket * 100
            print(f"   ├─ {label}: {len(valid_in_bracket):,}/{total_bracket:,} valid ({valid_pct:.1f}%)")

    # Similarity distribution for valid names
    print("\n   SIMILARITY DISTRIBUTION (valid names):")
    valid_sims = [r['similarity'] for r in results['valid']]
    if valid_sims:
        percentiles = [10, 25, 50, 75, 90]
        pct_values = np.percentile(valid_sims, percentiles)
        for p, v in zip(percentiles, pct_values):
            print(f"   ├─ {p}th percentile: {v:.3f}")
        print(f"   └─ Mean: {np.mean(valid_sims):.3f}")

    # Sample edge cases
    print("\n5. Edge case samples...")

    # Low similarity but valid
    print("\n   VALID with lowest similarity (edge cases to review):")
    sorted_valid = sorted(results['valid'], key=lambda x: x['similarity'])
    for r in sorted_valid[:10]:
        print(f"   ├─ sim={r['similarity']:.3f}: '{r['name']}' → '{r['best_match']}' (n={r['count']})")

    # High count but invalid
    print("\n   INVALID with highest count (potential false negatives):")
    sorted_invalid = sorted(results['invalid'], key=lambda x: -x['count'])
    for r in sorted_invalid[:10]:
        print(f"   ├─ n={r['count']}: '{r['name']}' (reason: {r['reason']})")

    # Preprocessing examples
    print("\n   PREPROCESSING EXAMPLES:")
    for change in results['preprocessing_changes'][:10]:
        print(f"   ├─ '{change['original']}' → '{change['cleaned']}'")

    # Save detailed results
    print("\n6. Saving results...")
    summary = {
        'total_names': len(names),
        'total_responses': total_responses,
        'valid_names': valid_count,
        'valid_responses': valid_responses,
        'invalid_names': invalid_count,
        'invalid_responses': invalid_responses,
        'filter_reasons': dict(results['filter_reasons']),
        'preprocessing_changes_count': len(results['preprocessing_changes']),
        'valid_similarity_stats': {
            'mean': float(np.mean(valid_sims)) if valid_sims else 0,
            'min': float(np.min(valid_sims)) if valid_sims else 0,
            'max': float(np.max(valid_sims)) if valid_sims else 0,
        }
    }

    save_results(summary, 'full_scale_validation_summary.json')

    # Save valid names for further use
    valid_output = {r['cleaned']: {
        'original': r['name'],
        'similarity': r['similarity'],
        'best_match': r['best_match'],
        'count': r['count']
    } for r in results['valid']}
    save_results(valid_output, 'validated_color_names.json')

    print(f"   Saved validation summary and {len(valid_output):,} validated names")
    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

    return results, summary


if __name__ == "__main__":
    run_full_validation()
