#!/usr/bin/env python3
"""
Phase 6.1: Family Assignment via NLP

Assigns each color name from the consolidated dataset to one of 35 families
(30 Centore + 5 new candidates) using SBERT embeddings and cosine similarity.

The 35 families are:
- 30 Centore: aqua, beige, blue, brown, coral, fuchsia, gold, gray, green,
              lavender, lilac, magenta, mauve, navy, orange, peach, pink,
              purple, red, rose, rust, sand, tan, taupe, teal, turquoise,
              violet, white, wine, yellow
- 5 New: indigo, maroon, lime, plum, aquamarine

Output: CSV with (name, hex, r, g, b, assigned_family, similarity_score)
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
CONSOLIDATED_DIR = DATASETS_DIR / "consolidated"
OUTPUT_DIR = DATASETS_DIR / "phase6"
OUTPUT_DIR.mkdir(exist_ok=True)

# The 35 families
CENTORE_30 = [
    "aqua", "beige", "blue", "brown", "coral", "fuchsia", "gold", "gray",
    "green", "lavender", "lilac", "magenta", "mauve", "navy", "orange",
    "peach", "pink", "purple", "red", "rose", "rust", "sand", "tan",
    "taupe", "teal", "turquoise", "violet", "white", "wine", "yellow"
]

NEW_CANDIDATES_5 = ["indigo", "maroon", "lime", "plum", "aquamarine"]

ALL_FAMILIES = CENTORE_30 + NEW_CANDIDATES_5


def load_consolidated_data() -> List[Dict]:
    """Load the consolidated color names dataset."""
    csv_path = CONSOLIDATED_DIR / "color_names_consolidated.csv"
    colors = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            colors.append({
                "name": row["name"],
                "hex": row["hex"],
                "r": float(row["r"]),
                "g": float(row["g"]),
                "b": float(row["b"]),
                "source_count": int(row["source_count"]),
                "sources": row["sources"],
                "total_votes": int(row["total_votes"]) if row["total_votes"] else 0,
                "confidence": float(row["confidence"]),
            })

    print(f"Loaded {len(colors)} color names from consolidated dataset")
    return colors


def compute_family_embeddings(model: SentenceTransformer) -> Dict[str, np.ndarray]:
    """Compute SBERT embeddings for all 35 family anchor names."""
    print(f"Computing embeddings for {len(ALL_FAMILIES)} family anchors...")

    embeddings = {}
    for family in ALL_FAMILIES:
        # Use the family name as the anchor
        embedding = model.encode(family, convert_to_numpy=True)
        embeddings[family] = embedding

    return embeddings


def assign_to_families(
    colors: List[Dict],
    model: SentenceTransformer,
    family_embeddings: Dict[str, np.ndarray],
    batch_size: int = 1000
) -> List[Dict]:
    """Assign each color name to the most similar family."""

    print(f"Assigning {len(colors)} colors to families...")

    # Stack family embeddings into a matrix
    family_names = list(family_embeddings.keys())
    family_matrix = np.stack([family_embeddings[f] for f in family_names])

    results = []

    # Process in batches to manage memory
    for i in range(0, len(colors), batch_size):
        batch = colors[i:i + batch_size]
        color_names = [c["name"] for c in batch]

        # Encode batch of color names
        color_embeddings = model.encode(color_names, convert_to_numpy=True, show_progress_bar=False)

        # Compute cosine similarity to all families
        similarities = cosine_similarity(color_embeddings, family_matrix)

        # Find best match for each color
        for j, color in enumerate(batch):
            best_idx = np.argmax(similarities[j])
            best_family = family_names[best_idx]
            best_score = similarities[j][best_idx]

            results.append({
                **color,
                "assigned_family": best_family,
                "similarity_score": float(best_score),
            })

        if (i + batch_size) % 10000 == 0 or i + batch_size >= len(colors):
            print(f"  Processed {min(i + batch_size, len(colors))}/{len(colors)} colors")

    return results


def compute_family_statistics(results: List[Dict]) -> Dict:
    """Compute statistics per family."""
    from collections import Counter

    family_counts = Counter(r["assigned_family"] for r in results)

    stats = {
        "total_colors": len(results),
        "families": {}
    }

    for family in ALL_FAMILIES:
        count = family_counts.get(family, 0)
        family_results = [r for r in results if r["assigned_family"] == family]

        if family_results:
            avg_similarity = np.mean([r["similarity_score"] for r in family_results])
            min_similarity = np.min([r["similarity_score"] for r in family_results])
            max_similarity = np.max([r["similarity_score"] for r in family_results])

            # Sample top 10 by similarity
            top_10 = sorted(family_results, key=lambda x: -x["similarity_score"])[:10]
            examples = [r["name"] for r in top_10]
        else:
            avg_similarity = 0.0
            min_similarity = 0.0
            max_similarity = 0.0
            examples = []

        stats["families"][family] = {
            "count": count,
            "percentage": round(100 * count / len(results), 2) if results else 0,
            "avg_similarity": round(avg_similarity, 4),
            "min_similarity": round(min_similarity, 4),
            "max_similarity": round(max_similarity, 4),
            "is_centore": family in CENTORE_30,
            "examples": examples
        }

    return stats


def save_results(results: List[Dict], stats: Dict):
    """Save results to CSV and statistics to JSON."""

    # Save assignments CSV
    csv_path = OUTPUT_DIR / "family_assignments.csv"
    fieldnames = [
        "name", "hex", "r", "g", "b", "source_count", "sources",
        "total_votes", "confidence", "assigned_family", "similarity_score"
    ]

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved {len(results)} assignments to {csv_path}")

    # Save statistics JSON
    json_path = OUTPUT_DIR / "family_assignment_stats.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"Saved statistics to {json_path}")


def print_summary(stats: Dict):
    """Print a summary of the family assignments."""
    print("\n" + "=" * 70)
    print("FAMILY ASSIGNMENT SUMMARY")
    print("=" * 70)

    # Sort by count descending
    sorted_families = sorted(
        stats["families"].items(),
        key=lambda x: -x[1]["count"]
    )

    print(f"\n{'Family':<15} {'Count':>8} {'%':>7} {'Avg Sim':>8} {'Type':<10}")
    print("-" * 50)

    for family, data in sorted_families:
        type_str = "Centore" if data["is_centore"] else "NEW"
        print(f"{family:<15} {data['count']:>8} {data['percentage']:>6.1f}% {data['avg_similarity']:>8.3f} {type_str:<10}")

    print("-" * 50)
    print(f"{'TOTAL':<15} {stats['total_colors']:>8}")

    # Print new candidates summary
    print("\n" + "=" * 70)
    print("NEW CANDIDATE FAMILIES")
    print("=" * 70)
    for family in NEW_CANDIDATES_5:
        data = stats["families"][family]
        print(f"\n{family.upper()} ({data['count']} colors, {data['avg_similarity']:.3f} avg similarity)")
        print(f"  Examples: {', '.join(data['examples'][:5])}")


def main():
    """Main entry point."""
    print("Phase 6.1: Family Assignment via NLP")
    print("=" * 50)

    # Load data
    colors = load_consolidated_data()

    # Load SBERT model
    print("\nLoading SBERT model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Compute family anchor embeddings
    family_embeddings = compute_family_embeddings(model)

    # Assign colors to families
    results = assign_to_families(colors, model, family_embeddings)

    # Compute statistics
    stats = compute_family_statistics(results)

    # Save results
    save_results(results, stats)

    # Print summary
    print_summary(stats)

    print("\nPhase 6.1 complete!")


if __name__ == "__main__":
    main()
