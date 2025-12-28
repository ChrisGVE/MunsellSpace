#!/usr/bin/env python3
"""
Analyze Spatial Coherence of New Overlay Candidates

This script validates that new overlay candidates have coherent color space distributions,
indicating they represent genuine color categories rather than arbitrary groupings.

Metrics:
- RGB centroid and standard deviation
- Color space volume (spread in RGB cube)
- Munsell coherence (hue/value/chroma variance)
"""

import json
import csv
import math
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import numpy as np


@dataclass
class ColorPoint:
    """A color point with RGB and optional Munsell coordinates."""
    name: str
    rgb: Tuple[int, int, int]
    munsell: Optional[str] = None
    hue_number: Optional[float] = None
    value: Optional[float] = None
    chroma: Optional[float] = None


@dataclass
class SpatialAnalysis:
    """Spatial coherence analysis for a candidate overlay."""
    name: str
    sample_count: int
    rgb_centroid: Tuple[float, float, float]
    rgb_std: Tuple[float, float, float]
    rgb_volume: float  # Product of std devs (smaller = more coherent)
    hex_centroid: str
    coherence_score: float  # 0-1, higher = more coherent


def load_colornames_data(csv_path: Path) -> Dict[str, ColorPoint]:
    """Load the combined colornames dataset."""
    colors = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].lower().strip()
            colors[name] = ColorPoint(
                name=name,
                rgb=(int(row['R']), int(row['G']), int(row['B']))
            )
    return colors


def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    """Convert RGB tuple to hex string."""
    r, g, b = [int(min(255, max(0, x))) for x in rgb]
    return f"#{r:02x}{g:02x}{b:02x}"


def compute_spatial_coherence(
    candidate_name: str,
    variant_names: List[str],
    color_data: Dict[str, ColorPoint]
) -> Optional[SpatialAnalysis]:
    """Compute spatial coherence metrics for a candidate overlay."""

    # Find RGB values for all variants
    rgb_values = []
    matched_names = []

    for variant in variant_names:
        variant_lower = variant.lower().strip()
        if variant_lower in color_data:
            rgb_values.append(color_data[variant_lower].rgb)
            matched_names.append(variant_lower)

    if len(rgb_values) < 3:
        return None

    # Convert to numpy array
    rgb_array = np.array(rgb_values, dtype=float)

    # Compute centroid
    centroid = tuple(rgb_array.mean(axis=0))

    # Compute standard deviation
    std = tuple(rgb_array.std(axis=0))

    # Compute volume (product of std devs, normalized)
    # Lower volume = more coherent
    volume = (std[0] + 1) * (std[1] + 1) * (std[2] + 1)

    # Compute coherence score (inverse of normalized volume)
    # Max possible std for RGB is ~127.5, so max volume is ~128^3
    max_volume = 128 ** 3
    coherence_score = max(0, 1 - (volume / max_volume))

    return SpatialAnalysis(
        name=candidate_name,
        sample_count=len(rgb_values),
        rgb_centroid=centroid,
        rgb_std=std,
        rgb_volume=volume,
        hex_centroid=rgb_to_hex(centroid),
        coherence_score=coherence_score
    )


def load_candidates(json_path: Path) -> Dict[str, List[str]]:
    """Load candidates and their variants from the extraction results."""
    with open(json_path) as f:
        data = json.load(f)

    candidates = {}
    for tier in ['tier1_strong', 'tier2_good', 'tier3_marginal']:
        for c in data['tiers'][tier]:
            candidates[c['name']] = c['examples']

    return candidates


def main():
    # Paths
    base_path = Path(__file__).parent.parent.parent.parent
    candidates_path = base_path / "datasets" / "clustered" / "new_overlay_candidates.json"
    colornames_path = base_path / "datasets" / "colornames_combined.csv"
    output_path = base_path / "datasets" / "clustered" / "spatial_coherence_analysis.json"

    print("Loading colornames data...")
    color_data = load_colornames_data(colornames_path)
    print(f"Loaded {len(color_data)} color names")

    print("\nLoading candidates...")
    candidates = load_candidates(candidates_path)
    print(f"Found {len(candidates)} candidates")

    print("\n" + "="*70)
    print("SPATIAL COHERENCE ANALYSIS")
    print("="*70)

    results = []

    for name, variants in sorted(candidates.items()):
        analysis = compute_spatial_coherence(name, variants, color_data)
        if analysis:
            results.append(analysis)
            print(f"\n{name.upper()}")
            print(f"  Samples matched: {analysis.sample_count}")
            print(f"  RGB centroid: ({analysis.rgb_centroid[0]:.1f}, {analysis.rgb_centroid[1]:.1f}, {analysis.rgb_centroid[2]:.1f})")
            print(f"  RGB std dev: ({analysis.rgb_std[0]:.1f}, {analysis.rgb_std[1]:.1f}, {analysis.rgb_std[2]:.1f})")
            print(f"  Hex centroid: {analysis.hex_centroid}")
            print(f"  Coherence score: {analysis.coherence_score:.3f}")
        else:
            print(f"\n{name.upper()} - Insufficient data (<3 matches)")

    # Sort by coherence score
    results.sort(key=lambda x: x.coherence_score, reverse=True)

    print("\n" + "="*70)
    print("RANKED BY COHERENCE (higher = more spatially coherent)")
    print("="*70)

    for i, r in enumerate(results, 1):
        quality = "EXCELLENT" if r.coherence_score > 0.95 else \
                  "GOOD" if r.coherence_score > 0.90 else \
                  "MODERATE" if r.coherence_score > 0.80 else "POOR"
        print(f"{i:2}. {r.name:15} | Score: {r.coherence_score:.3f} ({quality}) | {r.hex_centroid}")

    # Combine with frequency data for final recommendations
    with open(candidates_path) as f:
        freq_data = json.load(f)

    # Build lookup
    freq_lookup = {}
    for tier in ['tier1_strong', 'tier2_good', 'tier3_marginal']:
        for c in freq_data['tiers'][tier]:
            freq_lookup[c['name']] = c['variants']

    print("\n" + "="*70)
    print("FINAL RECOMMENDATIONS")
    print("="*70)
    print("\nCombined ranking (frequency × coherence):")

    combined_scores = []
    for r in results:
        freq = freq_lookup.get(r.name, 0)
        # Normalize frequency (assume max ~30)
        freq_norm = min(1.0, freq / 30.0)
        # Combined score: geometric mean of coherence and frequency
        combined = math.sqrt(r.coherence_score * freq_norm)
        combined_scores.append((r.name, combined, freq, r.coherence_score, r.hex_centroid))

    combined_scores.sort(key=lambda x: x[1], reverse=True)

    # Categorize recommendations
    strong_recs = []
    moderate_recs = []
    weak_recs = []

    for name, combined, freq, coherence, hex_code in combined_scores:
        rec = {
            "name": name,
            "combined_score": round(combined, 3),
            "frequency": freq,
            "coherence": round(coherence, 3),
            "hex_centroid": hex_code
        }
        if combined >= 0.5:
            strong_recs.append(rec)
            status = "RECOMMEND"
        elif combined >= 0.3:
            moderate_recs.append(rec)
            status = "CONSIDER"
        else:
            weak_recs.append(rec)
            status = "DEFER"

        print(f"  {status:10} {name:15} | Combined: {combined:.3f} | Freq: {freq:2} | Coherence: {coherence:.3f} | {hex_code}")

    # Special case analysis
    print("\n" + "="*70)
    print("SPECIAL CASES")
    print("="*70)

    # Check for grey vs gray
    if 'grey' in candidates:
        print("\n⚠️  GREY: This is the British spelling of GRAY, which is in Centore's 30.")
        print("    Recommendation: EXCLUDE (spelling variant, not new category)")

    # Check for black (not in Centore's basic 10, but white is)
    if 'black' in candidates:
        print("\n⚠️  BLACK: Note that Centore has 'white' but not 'black' in basic colors.")
        print("    This may be intentional (Munsell neutral axis) or an oversight.")
        print("    Recommendation: INVESTIGATE before including")

    # Save results
    output = {
        "analysis_date": "2025-12-28",
        "methodology": "RGB spatial coherence analysis",
        "recommendations": {
            "strong": strong_recs,
            "moderate": moderate_recs,
            "weak": weak_recs
        },
        "exclusions": {
            "grey": "British spelling of 'gray' - already in Centore's 30"
        },
        "notes": {
            "black": "Centore has 'white' but not 'black' - needs investigation"
        },
        "full_analysis": [
            {
                "name": r.name,
                "sample_count": r.sample_count,
                "rgb_centroid": list(r.rgb_centroid),
                "rgb_std": list(r.rgb_std),
                "coherence_score": round(r.coherence_score, 4),
                "hex_centroid": r.hex_centroid
            }
            for r in results
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
