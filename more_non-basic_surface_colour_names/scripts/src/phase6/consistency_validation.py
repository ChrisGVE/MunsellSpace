#!/usr/bin/env python3
"""
Phase 6.3: Consistency Validation

Validates that each color's Munsell coordinates are consistent with its
assigned family. Flags colors where NLP-based family assignment contradicts
the actual Munsell position.

The validation uses expected hue ranges for each family based on:
- Centore centroids for the 30 established families
- Semantic expectations for the 5 new candidate families

Note: We use generous tolerances because:
1. Screen colors (RGB) differ from surface colors (Munsell)
2. Color names are culturally subjective
3. We want to catch only clear contradictions (e.g., "red" with blue coordinates)

Input: datasets/phase6/family_assignments_munsell.csv
Output: datasets/phase6/validated_assignments.csv (consistent only)
        datasets/phase6/inconsistent_assignments.csv (flagged)
        datasets/phase6/validation_stats.json
"""

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter


# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
PHASE6_DIR = DATASETS_DIR / "phase6"


@dataclass
class HueRange:
    """Expected hue range for a color family."""
    center: float  # Center hue on 0-100 Munsell scale
    tolerance: float  # Allowed deviation from center
    wraps: bool = False  # Whether range wraps around 0/100

    def contains(self, hue: float) -> bool:
        """Check if a hue value falls within this range."""
        if self.tolerance >= 50:  # Nearly all hues allowed
            return True

        low = self.center - self.tolerance
        high = self.center + self.tolerance

        if not self.wraps:
            return low <= hue <= high
        else:
            # Handle wraparound (e.g., range from 95 to 5)
            if low < 0:
                return hue >= (100 + low) or hue <= high
            elif high > 100:
                return hue >= low or hue <= (high - 100)
            else:
                return low <= hue <= high


# Centore family centroids converted to hue on 0-100 scale
# Hue order: R(0) -> YR(10) -> Y(20) -> GY(30) -> G(40) -> BG(50) -> B(60) -> PB(70) -> P(80) -> RP(90)
# Formula: hue_100 = (hue_letter_index * 10) + hue_number

def munsell_to_hue100(hue_str: str) -> float:
    """Convert Munsell hue notation to 0-100 scale."""
    if not hue_str or hue_str == "N":
        return 0.0  # Neutral

    hue_order = {'R': 0, 'YR': 10, 'Y': 20, 'GY': 30, 'G': 40, 'BG': 50, 'B': 60, 'PB': 70, 'P': 80, 'RP': 90}

    # Parse hue like "7.4BG" -> 7.4 + 50 = 57.4
    for suffix, base in hue_order.items():
        if hue_str.endswith(suffix):
            try:
                num = float(hue_str[:-len(suffix)])
                return base + num
            except ValueError:
                return 0.0
    return 0.0


# Define expected hue ranges for all 35 families
# Centore 30 are based on the paper's centroids
# New 5 are based on semantic expectations

FAMILY_HUE_RANGES = {
    # Basic colors (10)
    "red": HueRange(center=5, tolerance=15, wraps=True),      # 5.1R -> hue ~5
    "orange": HueRange(center=12, tolerance=10),               # 2.5YR -> hue ~12
    "yellow": HueRange(center=24, tolerance=10),               # 3.9Y -> hue ~24
    "green": HueRange(center=42, tolerance=20),                # 2.3G -> hue ~42
    "blue": HueRange(center=72, tolerance=15),                 # 1.8PB -> hue ~72
    "purple": HueRange(center=84, tolerance=10),               # 4.3P -> hue ~84
    "pink": HueRange(center=1, tolerance=20, wraps=True),      # 0.7R -> hue ~1
    "brown": HueRange(center=12, tolerance=15),                # 2.2YR -> hue ~12
    "gray": HueRange(center=50, tolerance=50),                 # Neutral - all hues ok
    "white": HueRange(center=50, tolerance=50),                # Near-neutral - all hues ok

    # Non-basic Centore 20
    "aqua": HueRange(center=57, tolerance=15),                 # 7.4BG -> hue ~57
    "beige": HueRange(center=17, tolerance=10),                # 6.7YR -> hue ~17
    "coral": HueRange(center=7, tolerance=12, wraps=True),     # 6.5R -> hue ~7
    "fuchsia": HueRange(center=95, tolerance=15, wraps=True),  # 4.8RP -> hue ~95
    "gold": HueRange(center=20, tolerance=10),                 # 9.8YR -> hue ~20
    "lavender": HueRange(center=86, tolerance=12),             # 5.6P -> hue ~86
    "lilac": HueRange(center=88, tolerance=12),                # 7.8P -> hue ~88
    "magenta": HueRange(center=94, tolerance=10, wraps=True),  # 3.8RP -> hue ~94
    "mauve": HueRange(center=91, tolerance=15, wraps=True),    # 1.2RP -> hue ~91
    "navy": HueRange(center=77, tolerance=10),                 # 7.3PB -> hue ~77
    "peach": HueRange(center=13, tolerance=10),                # 2.9YR -> hue ~13
    "rose": HueRange(center=1, tolerance=15, wraps=True),      # 0.5R -> hue ~0.5
    "rust": HueRange(center=9, tolerance=10, wraps=True),      # 9.4R -> hue ~9
    "sand": HueRange(center=18, tolerance=12),                 # 7.6YR -> hue ~18
    "tan": HueRange(center=16, tolerance=12),                  # 6.3YR -> hue ~16
    "taupe": HueRange(center=13, tolerance=15),                # 3.2YR -> hue ~13
    "teal": HueRange(center=62, tolerance=12),                 # 1.6B -> hue ~62
    "turquoise": HueRange(center=62, tolerance=12),            # 1.6B -> hue ~62
    "violet": HueRange(center=87, tolerance=10),               # 7.0P -> hue ~87
    "wine": HueRange(center=3, tolerance=12, wraps=True),      # 2.7R -> hue ~3

    # New 5 candidate families (semantic expectations)
    "indigo": HueRange(center=78, tolerance=12),               # Between blue and purple
    "maroon": HueRange(center=5, tolerance=15, wraps=True),    # Dark red, similar to red/wine
    "lime": HueRange(center=32, tolerance=12),                 # Yellow-green
    "plum": HueRange(center=87, tolerance=15),                 # Purple family, like violet
    "aquamarine": HueRange(center=55, tolerance=15),           # Between green and blue-green
}


def is_neutral(row: Dict) -> bool:
    """Check if a color is neutral (gray scale)."""
    hue_str = row.get("hue_str", "")
    chroma = float(row.get("munsell_chroma", 0)) if row.get("munsell_chroma") else 0
    return hue_str == "N" or chroma < 1.0


def validate_consistency(row: Dict) -> Tuple[bool, str]:
    """
    Validate if a color's Munsell coordinates are consistent with its family.

    Returns: (is_consistent, reason)
    """
    family = row.get("assigned_family", "")
    hue_str = row.get("hue_str", "")
    munsell_notation = row.get("munsell_notation", "")

    # Skip if no Munsell data
    if not munsell_notation:
        return False, "no_munsell"

    # Skip neutral colors - they can belong to any family semantically
    if is_neutral(row):
        return True, "neutral"

    # Get expected hue range for this family
    if family not in FAMILY_HUE_RANGES:
        return True, "unknown_family"  # Can't validate unknown families

    expected = FAMILY_HUE_RANGES[family]

    # Convert actual hue to 0-100 scale
    actual_hue = munsell_to_hue100(hue_str)

    # Check if within expected range
    if expected.contains(actual_hue):
        return True, "consistent"
    else:
        return False, f"hue_mismatch:{actual_hue:.1f}"


def load_data() -> List[Dict]:
    """Load the Munsell-converted family assignments."""
    csv_path = PHASE6_DIR / "family_assignments_munsell.csv"
    colors = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            colors.append(row)

    print(f"Loaded {len(colors)} colors")
    return colors


def validate_all(colors: List[Dict]) -> Tuple[List[Dict], List[Dict], Dict]:
    """Validate all colors and split into consistent/inconsistent."""
    consistent = []
    inconsistent = []
    stats = {
        "total": len(colors),
        "consistent": 0,
        "inconsistent": 0,
        "by_reason": Counter(),
        "by_family": {}
    }

    for row in colors:
        is_valid, reason = validate_consistency(row)
        row_with_validation = dict(row)
        row_with_validation["validation_status"] = "valid" if is_valid else "invalid"
        row_with_validation["validation_reason"] = reason

        family = row.get("assigned_family", "")
        if family not in stats["by_family"]:
            stats["by_family"][family] = {"consistent": 0, "inconsistent": 0}

        if is_valid:
            consistent.append(row_with_validation)
            stats["consistent"] += 1
            stats["by_family"][family]["consistent"] += 1
        else:
            inconsistent.append(row_with_validation)
            stats["inconsistent"] += 1
            stats["by_family"][family]["inconsistent"] += 1

        stats["by_reason"][reason] += 1

    # Convert Counter to dict for JSON
    stats["by_reason"] = dict(stats["by_reason"])

    print(f"Consistent: {stats['consistent']:,} ({100*stats['consistent']/stats['total']:.1f}%)")
    print(f"Inconsistent: {stats['inconsistent']:,} ({100*stats['inconsistent']/stats['total']:.1f}%)")

    return consistent, inconsistent, stats


def save_results(consistent: List[Dict], inconsistent: List[Dict], stats: Dict):
    """Save validated results."""

    fieldnames = [
        "name", "hex", "r", "g", "b", "source_count", "sources",
        "total_votes", "confidence", "assigned_family", "similarity_score",
        "hue_str", "hue_num", "munsell_value", "munsell_chroma",
        "munsell_notation", "cartesian_x", "cartesian_y", "cartesian_z",
        "validation_status", "validation_reason"
    ]

    # Save consistent
    csv_path = PHASE6_DIR / "validated_assignments.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(consistent)
    print(f"Saved {len(consistent)} consistent to {csv_path}")

    # Save inconsistent
    csv_path = PHASE6_DIR / "inconsistent_assignments.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inconsistent)
    print(f"Saved {len(inconsistent)} inconsistent to {csv_path}")

    # Save stats
    json_path = PHASE6_DIR / "validation_stats.json"
    with open(json_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved stats to {json_path}")


def print_summary(stats: Dict):
    """Print validation summary."""
    print("\n" + "=" * 70)
    print("CONSISTENCY VALIDATION SUMMARY")
    print("=" * 70)

    print(f"\nTotal: {stats['total']:,}")
    print(f"Consistent: {stats['consistent']:,} ({100*stats['consistent']/stats['total']:.1f}%)")
    print(f"Inconsistent: {stats['inconsistent']:,}")

    print("\nReasons:")
    for reason, count in sorted(stats["by_reason"].items(), key=lambda x: -x[1]):
        print(f"  {reason}: {count:,}")

    print(f"\n{'Family':<15} {'Consistent':>12} {'Inconsistent':>14} {'%Valid':>10}")
    print("-" * 55)

    sorted_families = sorted(
        stats["by_family"].items(),
        key=lambda x: -(x[1]["consistent"] + x[1]["inconsistent"])
    )

    for family, data in sorted_families[:20]:
        total = data["consistent"] + data["inconsistent"]
        pct = 100 * data["consistent"] / total if total > 0 else 0
        print(f"{family:<15} {data['consistent']:>12} {data['inconsistent']:>14} {pct:>9.1f}%")


def main():
    """Main entry point."""
    print("Phase 6.3: Consistency Validation")
    print("=" * 50)

    # Load data
    colors = load_data()

    # Validate
    consistent, inconsistent, stats = validate_all(colors)

    # Save results
    save_results(consistent, inconsistent, stats)

    # Print summary
    print_summary(stats)

    print("\nPhase 6.3 complete!")


if __name__ == "__main__":
    main()
