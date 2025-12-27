#!/usr/bin/env python3
"""
Validate discovered clusters against Centore anchor families.

Compares the color families discovered through clustering with the 30
reference families from Centore (2020) to measure:

1. Coverage: How many Centore families have matching discovered clusters?
2. Purity: What % of each cluster's members match a single Centore family?
3. Recall: What % of names matching a Centore family were grouped together?

The 30 Centore families are:
- 20 non-basic: aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta,
                mauve, navy, peach, rose, rust, sand, tan, taupe, teal,
                turquoise, violet, wine
- 10 basic: blue, brown, gray, green, orange, pink, purple, red, white, yellow

Usage:
    python validate_centore.py [--method consensus] [--detailed]
"""

import json
import re
import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass, field

# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
CLUSTERED_DIR = DATASETS_DIR / "clustered"
COLLECTED_DIR = DATASETS_DIR / "collected"


# Centore category name patterns (from centore_comparison.py)
CENTORE_PATTERNS = {
    'aqua': [r'\baqua\b', r'\baquamarine\b'],
    'beige': [r'\bbeige\b'],
    'blue': [r'\bblue\b'],
    'brown': [r'\bbrown\b'],
    'coral': [r'\bcoral\b'],
    'fuchsia': [r'\bfuchsia\b'],
    'gold': [r'\bgold\b', r'\bgolden\b'],
    'gray': [r'\bgr[ae]y\b'],
    'green': [r'\bgreen\b'],
    'lavender': [r'\blavender\b'],
    'lilac': [r'\blilac\b'],
    'magenta': [r'\bmagenta\b'],
    'mauve': [r'\bmauve\b'],
    'navy': [r'\bnavy\b'],
    'orange': [r'\borange\b'],
    'peach': [r'\bpeach\b'],
    'pink': [r'\bpink\b'],
    'purple': [r'\bpurple\b'],
    'red': [r'\bred\b'],
    'rose': [r'\brose\b'],
    'rust': [r'\brust\b'],
    'sand': [r'\bsand\b', r'\bsandy\b'],
    'tan': [r'\btan\b'],
    'taupe': [r'\btaupe\b'],
    'teal': [r'\bteal\b'],
    'turquoise': [r'\bturquoise\b'],
    'violet': [r'\bviolet\b'],
    'white': [r'\bwhite\b'],
    'wine': [r'\bwine\b'],
    'yellow': [r'\byellow\b'],
}

# Compile patterns for efficiency
CENTORE_COMPILED = {
    cat: [re.compile(p, re.IGNORECASE) for p in patterns]
    for cat, patterns in CENTORE_PATTERNS.items()
}


@dataclass
class ClusterValidation:
    """Validation result for a discovered cluster."""
    cluster_name: str
    cluster_size: int
    centore_matches: Dict[str, int] = field(default_factory=dict)
    dominant_centore: Optional[str] = None
    purity: float = 0.0
    unmatched_count: int = 0


@dataclass
class CentoreValidation:
    """Validation result for a Centore family."""
    centore_name: str
    total_matches: int  # Total names matching this Centore family
    cluster_distribution: Dict[str, int] = field(default_factory=dict)
    primary_cluster: Optional[str] = None
    recall: float = 0.0  # % of matches in primary cluster
    fragmentation: float = 0.0  # How spread across clusters


def match_to_centore(name: str) -> List[str]:
    """Find which Centore categories a color name matches."""
    matches = []
    name_lower = name.lower()

    for category, patterns in CENTORE_COMPILED.items():
        for pattern in patterns:
            if pattern.search(name_lower):
                matches.append(category)
                break  # Only count once per category

    return matches


def load_families(method: str = "consensus") -> Dict:
    """Load discovered families from JSON."""
    filepath = CLUSTERED_DIR / f"families_{method}.json"
    if not filepath.exists():
        raise FileNotFoundError(f"No families found: {filepath}")

    with open(filepath, 'r') as f:
        return json.load(f)


def load_centore_centroids() -> Dict[str, str]:
    """Load Centore family centroids."""
    filepath = COLLECTED_DIR / "centore_colors.csv"
    centroids = {}

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            centroids[row['name']] = row['coordinates']

    return centroids


def validate_clusters(families_data: Dict) -> Tuple[List[ClusterValidation], List[CentoreValidation]]:
    """
    Validate discovered clusters against Centore families.

    Returns:
        cluster_validations: Validation results per cluster
        centore_validations: Validation results per Centore family
    """
    families = families_data.get('families', [])

    # Track Centore matches across all clusters
    centore_in_clusters: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    centore_total: Dict[str, int] = defaultdict(int)

    cluster_validations = []

    # Analyze each cluster
    for family in families:
        cluster_name = family['name']
        members = family.get('members', [])

        # Count Centore matches in this cluster
        centore_counts: Dict[str, int] = defaultdict(int)
        unmatched = 0

        for member in members:
            matches = match_to_centore(member)
            if matches:
                for match in matches:
                    centore_counts[match] += 1
                    centore_in_clusters[match][cluster_name] += 1
                    centore_total[match] += 1
            else:
                unmatched += 1

        # Find dominant Centore category
        if centore_counts:
            dominant = max(centore_counts.items(), key=lambda x: x[1])
            dominant_centore = dominant[0]
            purity = dominant[1] / len(members) if members else 0
        else:
            dominant_centore = None
            purity = 0.0

        validation = ClusterValidation(
            cluster_name=cluster_name,
            cluster_size=len(members),
            centore_matches=dict(centore_counts),
            dominant_centore=dominant_centore,
            purity=purity,
            unmatched_count=unmatched
        )
        cluster_validations.append(validation)

    # Analyze each Centore family
    centore_validations = []

    for centore_name in CENTORE_PATTERNS.keys():
        total = centore_total.get(centore_name, 0)
        cluster_dist = dict(centore_in_clusters.get(centore_name, {}))

        if cluster_dist:
            primary = max(cluster_dist.items(), key=lambda x: x[1])
            primary_cluster = primary[0]
            recall = primary[1] / total if total > 0 else 0
            # Fragmentation: 1 - (primary / total), lower is better
            fragmentation = 1 - recall
        else:
            primary_cluster = None
            recall = 0.0
            fragmentation = 1.0

        validation = CentoreValidation(
            centore_name=centore_name,
            total_matches=total,
            cluster_distribution=cluster_dist,
            primary_cluster=primary_cluster,
            recall=recall,
            fragmentation=fragmentation
        )
        centore_validations.append(validation)

    return cluster_validations, centore_validations


def print_validation_report(
    cluster_vals: List[ClusterValidation],
    centore_vals: List[CentoreValidation],
    detailed: bool = False
):
    """Print validation report."""
    print("\n" + "=" * 70)
    print("CENTORE ANCHOR VALIDATION REPORT")
    print("=" * 70)

    # Summary statistics
    total_colors = sum(cv.cluster_size for cv in cluster_vals)
    avg_purity = sum(cv.purity for cv in cluster_vals) / len(cluster_vals) if cluster_vals else 0

    covered_centore = sum(1 for cv in centore_vals if cv.total_matches > 0)
    avg_recall = sum(cv.recall for cv in centore_vals if cv.total_matches > 0)
    avg_recall = avg_recall / covered_centore if covered_centore > 0 else 0

    print(f"\nSUMMARY")
    print("-" * 40)
    print(f"Total colors clustered: {total_colors:,}")
    print(f"Number of clusters: {len(cluster_vals)}")
    print(f"Average cluster purity: {avg_purity:.1%}")
    print(f"Centore families covered: {covered_centore}/30")
    print(f"Average recall per Centore family: {avg_recall:.1%}")

    # Cluster analysis
    print(f"\n{'=' * 70}")
    print("CLUSTER ANALYSIS (by purity)")
    print("=" * 70)
    print(f"{'Cluster':<20} {'Size':>6} {'Purity':>8} {'Dominant':>12} {'Matches':>20}")
    print("-" * 70)

    for cv in sorted(cluster_vals, key=lambda x: -x.purity):
        top_matches = sorted(cv.centore_matches.items(), key=lambda x: -x[1])[:3]
        match_str = ', '.join(f"{k}:{v}" for k, v in top_matches) if top_matches else "none"

        print(f"{cv.cluster_name:<20} {cv.cluster_size:>6} {cv.purity:>7.1%} "
              f"{cv.dominant_centore or 'N/A':>12} {match_str}")

    # Centore family analysis
    print(f"\n{'=' * 70}")
    print("CENTORE FAMILY ANALYSIS (by recall)")
    print("=" * 70)
    print(f"{'Centore':<12} {'Total':>6} {'Recall':>8} {'Primary Cluster':<20} {'Distribution'}")
    print("-" * 70)

    for cv in sorted(centore_vals, key=lambda x: -x.recall):
        if cv.total_matches == 0:
            print(f"{cv.centore_name:<12} {'0':>6} {'N/A':>8} {'(no matches)':<20}")
            continue

        top_clusters = sorted(cv.cluster_distribution.items(), key=lambda x: -x[1])[:3]
        dist_str = ', '.join(f"{k}:{v}" for k, v in top_clusters)

        print(f"{cv.centore_name:<12} {cv.total_matches:>6} {cv.recall:>7.1%} "
              f"{cv.primary_cluster or 'N/A':<20} {dist_str}")

    # Best and worst matches
    print(f"\n{'=' * 70}")
    print("BEST CENTORE-CLUSTER MATCHES (high recall)")
    print("=" * 70)

    best = [(cv.centore_name, cv.primary_cluster, cv.recall, cv.total_matches)
            for cv in centore_vals if cv.recall > 0.5 and cv.total_matches >= 10]
    best.sort(key=lambda x: -x[2])

    if best:
        for centore, cluster, recall, count in best[:10]:
            print(f"  {centore} -> {cluster}: {recall:.1%} recall ({count} colors)")
    else:
        print("  No high-recall matches found (>50% with 10+ colors)")

    print(f"\n{'=' * 70}")
    print("FRAGMENTED CENTORE FAMILIES (low recall)")
    print("=" * 70)

    fragmented = [(cv.centore_name, cv.recall, cv.fragmentation, cv.cluster_distribution)
                  for cv in centore_vals if cv.total_matches >= 10 and cv.recall < 0.3]
    fragmented.sort(key=lambda x: x[2], reverse=True)

    if fragmented:
        for centore, recall, frag, dist in fragmented[:10]:
            top = sorted(dist.items(), key=lambda x: -x[1])[:3]
            dist_str = ', '.join(f"{k}:{v}" for k, v in top)
            print(f"  {centore}: {recall:.1%} recall, spread across: {dist_str}")
    else:
        print("  No highly fragmented families found")

    if detailed:
        print(f"\n{'=' * 70}")
        print("DETAILED CLUSTER BREAKDOWN")
        print("=" * 70)

        for cv in sorted(cluster_vals, key=lambda x: -x.cluster_size):
            print(f"\n{cv.cluster_name} ({cv.cluster_size} colors)")
            print(f"  Purity: {cv.purity:.1%}")
            print(f"  Dominant: {cv.dominant_centore or 'none'}")
            print(f"  Unmatched: {cv.unmatched_count}")
            print("  Centore breakdown:")
            for cat, count in sorted(cv.centore_matches.items(), key=lambda x: -x[1]):
                pct = count / cv.cluster_size * 100
                print(f"    {cat}: {count} ({pct:.1f}%)")


def save_validation_json(
    cluster_vals: List[ClusterValidation],
    centore_vals: List[CentoreValidation],
    method: str
):
    """Save validation results to JSON."""
    output = {
        "method": method,
        "summary": {
            "total_colors": sum(cv.cluster_size for cv in cluster_vals),
            "n_clusters": len(cluster_vals),
            "avg_purity": sum(cv.purity for cv in cluster_vals) / len(cluster_vals) if cluster_vals else 0,
            "centore_covered": sum(1 for cv in centore_vals if cv.total_matches > 0),
            "avg_recall": sum(cv.recall for cv in centore_vals if cv.total_matches > 0) /
                         sum(1 for cv in centore_vals if cv.total_matches > 0) if any(cv.total_matches > 0 for cv in centore_vals) else 0,
        },
        "cluster_validations": [
            {
                "cluster_name": cv.cluster_name,
                "cluster_size": cv.cluster_size,
                "centore_matches": cv.centore_matches,
                "dominant_centore": cv.dominant_centore,
                "purity": round(cv.purity, 4),
                "unmatched_count": cv.unmatched_count,
            }
            for cv in cluster_vals
        ],
        "centore_validations": [
            {
                "centore_name": cv.centore_name,
                "total_matches": cv.total_matches,
                "cluster_distribution": cv.cluster_distribution,
                "primary_cluster": cv.primary_cluster,
                "recall": round(cv.recall, 4),
                "fragmentation": round(cv.fragmentation, 4),
            }
            for cv in centore_vals
        ]
    }

    output_path = CLUSTERED_DIR / f"validation_{method}.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nValidation saved to: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate clusters against Centore families")
    parser.add_argument('--method', type=str, default='consensus',
                       help='Clustering method to validate')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed breakdown per cluster')
    parser.add_argument('--all-methods', action='store_true',
                       help='Validate all available clustering methods')
    args = parser.parse_args()

    if args.all_methods:
        methods = ['kmeans_rgb', 'kmeans_munsell', 'gmm_rgb', 'hierarchical_rgb', 'sbert', 'consensus']
    else:
        methods = [args.method]

    for method in methods:
        try:
            print(f"\n{'#' * 70}")
            print(f"# Validating: {method}")
            print(f"{'#' * 70}")

            families_data = load_families(method)
            cluster_vals, centore_vals = validate_clusters(families_data)
            print_validation_report(cluster_vals, centore_vals, detailed=args.detailed)
            save_validation_json(cluster_vals, centore_vals, method)

        except FileNotFoundError as e:
            print(f"Skipping {method}: {e}")


if __name__ == "__main__":
    main()
