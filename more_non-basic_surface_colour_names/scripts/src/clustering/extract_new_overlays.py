#!/usr/bin/env python3
"""
Extract New Overlay Candidates from SBERT Clustering Results

This script identifies color names that could become new semantic overlays
by filtering out Centore's existing 30 categories and analyzing spatial coherence.

Phase 5 deliverable: Curated list of new category candidates with justification.
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

# Centore's 30 color families (10 basic + 20 non-basic)
CENTORE_BASIC = {
    'blue', 'brown', 'gray', 'green', 'orange',
    'pink', 'purple', 'red', 'white', 'yellow'
}

CENTORE_NONBASIC = {
    'aqua', 'beige', 'coral', 'fuchsia', 'gold',
    'lavender', 'lilac', 'magenta', 'mauve', 'navy',
    'peach', 'rose', 'rust', 'sand', 'tan',
    'taupe', 'teal', 'turquoise', 'violet', 'wine'
}

CENTORE_ALL = CENTORE_BASIC | CENTORE_NONBASIC

# Words that are modifiers, not color categories
MODIFIER_WORDS = {
    'light', 'dark', 'pale', 'bright', 'deep', 'dull', 'muted',
    'dusty', 'dirty', 'faded', 'pastel', 'neon', 'electric', 'vivid',
    'soft', 'strong', 'hot', 'cool', 'warm', 'rich', 'pure',
    'very', 'medium', 'baby', 'old', 'french', 'british', 'spanish',
    'true', 'ugly', 'sick', 'gross', 'weird', 'nice', 'boring',
    'ish', 'ey', 'y'  # suffixes
}

# Offensive words to exclude
OFFENSIVE_WORDS = {
    'puke', 'vomit', 'barf', 'poop', 'poo', 'shit', 'piss',
    'booger', 'snot', 'bile', 'pee', 'diarrhea', 'scab'
}


@dataclass
class OverlayCandidate:
    """A potential new overlay candidate."""
    name: str
    sample_count: int
    source_cluster: str
    cluster_size: int
    variants: List[str] = field(default_factory=list)
    justification: str = ""
    confidence: float = 0.0


def normalize_name(name: str) -> str:
    """Normalize a color name for comparison."""
    return name.lower().strip()


def extract_base_color(name: str) -> Optional[str]:
    """Extract the base color word from a compound name."""
    words = name.lower().split()

    # Filter out modifiers
    color_words = [w for w in words if w not in MODIFIER_WORDS]

    if not color_words:
        return None

    # Return the last non-modifier word (usually the color)
    return color_words[-1]


def is_offensive(name: str) -> bool:
    """Check if a name contains offensive words."""
    name_lower = name.lower()
    return any(word in name_lower for word in OFFENSIVE_WORDS)


def is_compound_of_centore(name: str) -> bool:
    """Check if name is just a compound of Centore colors (e.g., 'blue green')."""
    words = set(name.lower().split())
    color_words = words - MODIFIER_WORDS
    return all(w in CENTORE_ALL for w in color_words) and len(color_words) > 0


def analyze_cluster_for_candidates(
    family: Dict,
    min_variants: int = 3
) -> List[OverlayCandidate]:
    """Analyze a cluster to find new overlay candidates."""
    candidates = []

    # Count base color occurrences
    base_color_counts: Dict[str, List[str]] = defaultdict(list)

    for member in family['members']:
        if is_offensive(member):
            continue

        base = extract_base_color(member)
        if base and base not in CENTORE_ALL:
            # Check it's not just a Centore compound
            if not is_compound_of_centore(member):
                base_color_counts[base].append(member)

    # Find bases with enough variants
    for base, variants in base_color_counts.items():
        if len(variants) >= min_variants:
            candidate = OverlayCandidate(
                name=base,
                sample_count=len(variants),
                source_cluster=family['name'],
                cluster_size=family['size'],
                variants=variants[:10],  # Keep top 10 for display
                confidence=len(variants) / family['size']
            )
            candidates.append(candidate)

    return candidates


def generate_justification(candidate: OverlayCandidate) -> str:
    """Generate justification for why this is a good candidate."""
    reasons = []

    if candidate.sample_count >= 10:
        reasons.append(f"High frequency ({candidate.sample_count} variants)")
    elif candidate.sample_count >= 5:
        reasons.append(f"Moderate frequency ({candidate.sample_count} variants)")
    else:
        reasons.append(f"Low frequency ({candidate.sample_count} variants)")

    if candidate.confidence >= 0.05:
        reasons.append(f"Strong cluster presence ({candidate.confidence:.1%})")

    # Check for semantic coherence (all variants contain the base)
    coherent = all(candidate.name in v.lower() for v in candidate.variants)
    if coherent:
        reasons.append("Semantically coherent (all variants contain base word)")

    return "; ".join(reasons)


def main():
    """Main extraction pipeline."""
    # Paths
    base_path = Path(__file__).parent.parent.parent.parent / "datasets" / "clustered"
    sbert_path = base_path / "families_sbert.json"
    output_path = base_path / "new_overlay_candidates.json"

    # Load SBERT results
    print("Loading SBERT clustering results...")
    with open(sbert_path) as f:
        data = json.load(f)

    print(f"Loaded {data['n_families']} families with {data['n_colors']} colors")

    # Find all candidates
    all_candidates: List[OverlayCandidate] = []

    print("\n" + "="*60)
    print("ANALYZING CLUSTERS FOR NEW OVERLAY CANDIDATES")
    print("="*60)

    for family in data['families']:
        candidates = analyze_cluster_for_candidates(family, min_variants=3)
        if candidates:
            print(f"\n{family['name'].upper()} cluster ({family['size']} members):")
            for c in candidates:
                c.justification = generate_justification(c)
                print(f"  - {c.name}: {c.sample_count} variants")
                print(f"    Examples: {', '.join(c.variants[:5])}")
        all_candidates.extend(candidates)

    # Deduplicate by name (keep highest sample count)
    unique_candidates: Dict[str, OverlayCandidate] = {}
    for c in all_candidates:
        if c.name not in unique_candidates or c.sample_count > unique_candidates[c.name].sample_count:
            unique_candidates[c.name] = c

    # Sort by sample count
    sorted_candidates = sorted(
        unique_candidates.values(),
        key=lambda x: x.sample_count,
        reverse=True
    )

    # Filter to high-quality candidates
    # Criteria: at least 5 variants, not a single word that's too short
    quality_candidates = [
        c for c in sorted_candidates
        if c.sample_count >= 5 and len(c.name) >= 4
    ]

    print("\n" + "="*60)
    print("NEW OVERLAY CANDIDATES (sorted by frequency)")
    print("="*60)
    print(f"\nTotal unique candidates: {len(unique_candidates)}")
    print(f"Quality candidates (≥5 variants, ≥4 chars): {len(quality_candidates)}")

    print("\n" + "-"*60)
    print("TOP NEW OVERLAY CANDIDATES")
    print("-"*60)

    for i, c in enumerate(quality_candidates[:30], 1):
        print(f"\n{i:2}. {c.name.upper()}")
        print(f"    Variants: {c.sample_count}")
        print(f"    Source cluster: {c.source_cluster}")
        print(f"    Justification: {c.justification}")
        print(f"    Examples: {', '.join(c.variants[:5])}")

    # Separate into tiers
    tier1 = [c for c in quality_candidates if c.sample_count >= 15]
    tier2 = [c for c in quality_candidates if 8 <= c.sample_count < 15]
    tier3 = [c for c in quality_candidates if 5 <= c.sample_count < 8]

    print("\n" + "="*60)
    print("CANDIDATE TIERS")
    print("="*60)

    print(f"\nTIER 1 (≥15 variants) - Strong candidates: {len(tier1)}")
    for c in tier1:
        print(f"  - {c.name}: {c.sample_count} variants")

    print(f"\nTIER 2 (8-14 variants) - Good candidates: {len(tier2)}")
    for c in tier2:
        print(f"  - {c.name}: {c.sample_count} variants")

    print(f"\nTIER 3 (5-7 variants) - Marginal candidates: {len(tier3)}")
    for c in tier3:
        print(f"  - {c.name}: {c.sample_count} variants")

    # Check which Centore colors are NOT represented as cluster names
    cluster_names = {f['name'] for f in data['families']}
    centore_in_clusters = CENTORE_ALL & cluster_names
    centore_missing = CENTORE_ALL - cluster_names

    print("\n" + "="*60)
    print("CENTORE CATEGORY ANALYSIS")
    print("="*60)
    print(f"\nCentore colors as cluster names: {len(centore_in_clusters)}")
    print(f"  {', '.join(sorted(centore_in_clusters))}")
    print(f"\nCentore colors NOT as cluster names: {len(centore_missing)}")
    print(f"  {', '.join(sorted(centore_missing))}")

    # Save results
    output = {
        "analysis_date": "2025-12-28",
        "source": "SBERT clustering",
        "centore_30": sorted(CENTORE_ALL),
        "total_candidates": len(unique_candidates),
        "quality_candidates": len(quality_candidates),
        "tiers": {
            "tier1_strong": [
                {
                    "name": c.name,
                    "variants": c.sample_count,
                    "source_cluster": c.source_cluster,
                    "examples": c.variants[:10],
                    "justification": c.justification
                }
                for c in tier1
            ],
            "tier2_good": [
                {
                    "name": c.name,
                    "variants": c.sample_count,
                    "source_cluster": c.source_cluster,
                    "examples": c.variants[:10],
                    "justification": c.justification
                }
                for c in tier2
            ],
            "tier3_marginal": [
                {
                    "name": c.name,
                    "variants": c.sample_count,
                    "source_cluster": c.source_cluster,
                    "examples": c.variants[:10],
                    "justification": c.justification
                }
                for c in tier3
            ]
        },
        "centore_coverage": {
            "as_cluster_names": sorted(centore_in_clusters),
            "not_cluster_names": sorted(centore_missing)
        }
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
