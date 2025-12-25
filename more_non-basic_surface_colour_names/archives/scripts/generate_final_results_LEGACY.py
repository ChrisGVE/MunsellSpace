#!/usr/bin/env python3
"""
Generate Final Overlay Results

Creates the final output files for overlay preprocessing:
1. overlay_colors_dataset.csv - Complete dataset with all sources
2. overlay_centroids.json - Centroid coordinates for all overlays
3. combined_color_dictionary.json - Merged Centore + XKCD data
4. iscc_nbs_contradictions.json - Contradiction analysis report

Usage:
    python overlay-preprocessing/generate_final_results.py
"""

import json
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_DIR = PROJECT_ROOT / "overlay-preprocessing/results"
EXCLUDED_FILE = PROJECT_ROOT / "overlay-preprocessing/excluded_colors.txt"

# Centore's 20 semantic overlay centroids (from the paper)
# Format: (hue_number, value, chroma)
CENTORE_CENTROIDS = {
    "aqua": (21.2, 6.8, 4.1),
    "beige": (2.0, 7.1, 3.1),
    "coral": (3.6, 5.8, 9.9),
    "fuchsia": (37.5, 4.6, 11.1),
    "gold": (9.7, 6.5, 7.7),
    "lavender": (31.7, 6.9, 5.1),
    "lilac": (33.6, 6.7, 5.6),
    "magenta": (36.9, 4.9, 11.1),
    "mauve": (35.0, 5.6, 5.7),
    "navy": (26.0, 2.5, 5.7),
    "peach": (4.0, 7.5, 6.1),
    "rose": (38.5, 5.3, 8.0),
    "rust": (5.5, 4.0, 8.2),
    "sand": (8.5, 6.8, 4.2),
    "tan": (6.5, 6.0, 4.5),
    "taupe": (7.5, 5.2, 2.8),
    "teal": (21.5, 4.5, 6.5),
    "turquoise": (19.5, 6.5, 7.5),
    "violet": (32.5, 4.5, 9.5),
    "wine": (38.0, 3.5, 7.5),
}

# ISCC-NBS basic color hue ranges (approximate)
# Format: (min_hue, max_hue) in Munsell hue numbers (0-40)
ISCC_NBS_HUE_RANGES = {
    "red": (37.0, 40.0, 0.0, 3.0),  # Wraps around
    "orange": (3.0, 7.0),
    "yellow": (7.0, 12.0),
    "green": (14.0, 22.0),
    "blue": (22.0, 30.0),
    "purple": (30.0, 37.0),
    "pink": (37.0, 40.0, 0.0, 5.0),  # Red-purple region
    "brown": (3.0, 10.0),  # Low value orange-yellow
    "olive": (10.0, 16.0),  # Low chroma yellow-green
}


def load_exclusions() -> set:
    """Load excluded color names from file."""
    excluded = set()
    if EXCLUDED_FILE.exists():
        with open(EXCLUDED_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    color = line.split('|')[0].strip()
                    if color:
                        excluded.add(color.lower())
    return excluded


def hue_to_cartesian(hue_num, value, chroma):
    """Convert Munsell cylindrical to Cartesian coordinates."""
    theta = hue_num * 9 * math.pi / 180  # 40 steps = 360 degrees
    x = chroma * math.cos(theta)
    y = chroma * math.sin(theta)
    z = value
    return (round(x, 2), round(y, 2), round(z, 2))


def rgb_to_munsell_approx(r, g, b):
    """
    Approximate RGB to Munsell conversion for analysis.
    NOTE: Use MunsellSpace library for accurate conversions.
    """
    # Simplified HSV conversion
    r, g, b = r/255, g/255, b/255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    # Value
    value = max_c * 10  # Scale to 0-10

    # Saturation -> Chroma (approximate)
    saturation = 0 if max_c == 0 else delta / max_c
    chroma = saturation * 14  # Approximate scaling

    # Hue
    if delta == 0:
        hue = None
    elif max_c == r:
        hue = 60 * (((g - b) / delta) % 6)
    elif max_c == g:
        hue = 60 * (((b - r) / delta) + 2)
    else:
        hue = 60 * (((r - g) / delta) + 4)

    # Convert HSV hue to Munsell hue number
    if hue is not None:
        # Map 0-360 to Munsell 0-40
        # Munsell: R=0, YR=4, Y=8, GY=12, G=16, BG=20, B=24, PB=28, P=32, RP=36
        munsell_hue = ((hue + 18) % 360) / 9  # Approximate mapping
    else:
        munsell_hue = None

    return munsell_hue, value, chroma


def check_iscc_nbs_consistency(color_name, hue_num, value, chroma):
    """Check if a color's coordinates are consistent with its name."""
    issues = []

    # Extract base color term from name
    base_colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "olive"]

    for base in base_colors:
        if base in color_name.lower():
            expected_range = ISCC_NBS_HUE_RANGES.get(base)
            if expected_range and hue_num is not None:
                if len(expected_range) == 2:
                    min_h, max_h = expected_range
                    if not (min_h <= hue_num <= max_h):
                        issues.append({
                            "type": "hue_mismatch",
                            "expected_base": base,
                            "expected_hue_range": f"{min_h}-{max_h}",
                            "actual_hue": hue_num,
                            "severity": "warning"
                        })
                else:
                    # Wrapping range (e.g., red spans 37-40 and 0-3)
                    min1, max1, min2, max2 = expected_range
                    if not ((min1 <= hue_num <= max1) or (min2 <= hue_num <= max2)):
                        issues.append({
                            "type": "hue_mismatch",
                            "expected_base": base,
                            "expected_hue_range": f"{min1}-{max1} or {min2}-{max2}",
                            "actual_hue": hue_num,
                            "severity": "warning"
                        })

    return issues


def main():
    print("Loading analysis results...")

    # Load classification comparison
    comparison_file = RESULTS_DIR / "classification_comparison.json"
    with open(comparison_file, 'r') as f:
        comparison = json.load(f)

    # Load word analysis
    word_analysis_file = RESULTS_DIR / "xkcd_word_analysis.json"
    with open(word_analysis_file, 'r') as f:
        word_analysis = json.load(f)

    # Load exclusions
    excluded = load_exclusions()
    print(f"  Excluded terms: {len(excluded)}")

    # Get all color words
    all_color_words = {w['word']: w for w in word_analysis['color_words']}

    # Get high-confidence candidates
    new_candidates = [c for c in comparison['new_candidates'] if c['word'] not in excluded]

    print(f"  High-confidence candidates: {len(new_candidates)}")

    # =========================================================================
    # 1. Generate overlay_colors_dataset.csv
    # =========================================================================
    print("\nGenerating overlay_colors_dataset.csv...")

    dataset_file = RESULTS_DIR / "overlay_colors_dataset.csv"
    with open(dataset_file, 'w') as f:
        f.write("color_name,source,responses,mean_r,mean_g,mean_b,hex,hue_mean,hue_std,")
        f.write("munsell_hue,munsell_value,munsell_chroma,cart_x,cart_y,cart_z,ml_confidence\n")

        # Add Centore overlays
        for name, (hue, val, chroma) in CENTORE_CENTROIDS.items():
            cart = hue_to_cartesian(hue, val, chroma)
            f.write(f"{name},centore,NA,NA,NA,NA,NA,NA,NA,")
            f.write(f"{hue:.1f},{val:.1f},{chroma:.1f},{cart[0]},{cart[1]},{cart[2]},1.0\n")

        # Add XKCD candidates
        for c in new_candidates:
            word = c['word']
            ws = all_color_words.get(word, {})
            rgb = ws.get('mean_rgb', [128, 128, 128])
            hue_approx, val_approx, chroma_approx = rgb_to_munsell_approx(*rgb)

            if hue_approx is not None:
                cart = hue_to_cartesian(hue_approx, val_approx, chroma_approx)
            else:
                cart = (0, 0, val_approx)

            hue_mean = c.get('hue_mean', '')
            hue_std = c.get('hue_std', '')

            f.write(f"{word},xkcd,{c['responses']},{rgb[0]:.0f},{rgb[1]:.0f},{rgb[2]:.0f},")
            f.write(f"{c['hex']},{hue_mean or ''},{hue_std or ''},")
            f.write(f"{hue_approx or '':.1f},{val_approx:.1f},{chroma_approx:.1f},")
            f.write(f"{cart[0]},{cart[1]},{cart[2]},{c['ml_prob']:.3f}\n")

    print(f"  Created: {dataset_file}")

    # =========================================================================
    # 2. Generate overlay_centroids.json
    # =========================================================================
    print("\nGenerating overlay_centroids.json...")

    centroids = {}

    # Centore overlays
    for name, (hue, val, chroma) in CENTORE_CENTROIDS.items():
        cart = hue_to_cartesian(hue, val, chroma)
        centroids[name] = {
            "source": "centore",
            "munsell": {
                "hue_number": hue,
                "value": val,
                "chroma": chroma
            },
            "cartesian": {
                "x": cart[0],
                "y": cart[1],
                "z": cart[2]
            },
            "sample_count": "~800 CAUS samples"
        }

    # Top XKCD candidates
    for c in new_candidates[:20]:  # Top 20
        word = c['word']
        ws = all_color_words.get(word, {})
        rgb = ws.get('mean_rgb', [128, 128, 128])
        hue_approx, val_approx, chroma_approx = rgb_to_munsell_approx(*rgb)

        if hue_approx is not None:
            cart = hue_to_cartesian(hue_approx, val_approx, chroma_approx)
        else:
            cart = (0, 0, val_approx)

        centroids[word] = {
            "source": "xkcd",
            "munsell": {
                "hue_number": round(hue_approx, 1) if hue_approx else None,
                "value": round(val_approx, 1),
                "chroma": round(chroma_approx, 1)
            },
            "cartesian": {
                "x": cart[0],
                "y": cart[1],
                "z": cart[2]
            },
            "sample_count": c['responses'],
            "hex_representative": c['hex'],
            "ml_confidence": c['ml_prob']
        }

    centroids_file = RESULTS_DIR / "overlay_centroids.json"
    with open(centroids_file, 'w') as f:
        json.dump(centroids, f, indent=2)

    print(f"  Created: {centroids_file}")
    print(f"  Total overlays: {len(centroids)} (20 Centore + {len(centroids) - 20} XKCD)")

    # =========================================================================
    # 3. Test ISCC-NBS contradictions
    # =========================================================================
    print("\nTesting ISCC-NBS contradictions...")

    contradictions = {
        "summary": {
            "total_tested": len(new_candidates),
            "with_issues": 0,
            "severity_counts": {"error": 0, "warning": 0, "info": 0}
        },
        "issues": []
    }

    for c in new_candidates:
        word = c['word']
        ws = all_color_words.get(word, {})
        rgb = ws.get('mean_rgb', [128, 128, 128])
        hue_approx, val_approx, chroma_approx = rgb_to_munsell_approx(*rgb)

        issues = check_iscc_nbs_consistency(word, hue_approx, val_approx, chroma_approx)

        if issues:
            contradictions["summary"]["with_issues"] += 1
            for issue in issues:
                contradictions["summary"]["severity_counts"][issue["severity"]] += 1

            contradictions["issues"].append({
                "color": word,
                "responses": c['responses'],
                "munsell_approx": {
                    "hue": hue_approx,
                    "value": val_approx,
                    "chroma": chroma_approx
                },
                "issues": issues
            })

    contradictions_file = RESULTS_DIR / "iscc_nbs_contradictions.json"
    with open(contradictions_file, 'w') as f:
        json.dump(contradictions, f, indent=2)

    print(f"  Created: {contradictions_file}")
    print(f"  Colors with issues: {contradictions['summary']['with_issues']}")
    print(f"  Warnings: {contradictions['summary']['severity_counts']['warning']}")

    # =========================================================================
    # 4. Generate combined_color_dictionary.json
    # =========================================================================
    print("\nGenerating combined_color_dictionary.json...")

    dictionary = {}

    # Add Centore overlays (high priority)
    for name, (hue, val, chroma) in CENTORE_CENTROIDS.items():
        cart = hue_to_cartesian(hue, val, chroma)
        dictionary[name] = {
            "munsell": f"{hue:.1f} {val:.1f}/{chroma:.1f}",
            "hue_number": hue,
            "value": val,
            "chroma": chroma,
            "cartesian": [cart[0], cart[1], cart[2]],
            "source": "centore",
            "confidence": 1.0,
            "sample_count": "~800",
            "hex_representative": None  # Would need actual computation
        }

    # Add XKCD candidates (merge if exists)
    for c in new_candidates:
        word = c['word']
        ws = all_color_words.get(word, {})
        rgb = ws.get('mean_rgb', [128, 128, 128])
        hue_approx, val_approx, chroma_approx = rgb_to_munsell_approx(*rgb)

        if hue_approx is not None:
            cart = hue_to_cartesian(hue_approx, val_approx, chroma_approx)
        else:
            cart = (0, 0, val_approx)

        if word in dictionary:
            # Merge: note both sources
            dictionary[word]["source"] = "both"
            dictionary[word]["xkcd_sample_count"] = c['responses']
            dictionary[word]["xkcd_hex"] = c['hex']
        else:
            dictionary[word] = {
                "munsell": f"{hue_approx:.1f} {val_approx:.1f}/{chroma_approx:.1f}" if hue_approx else f"N {val_approx:.1f}/0",
                "hue_number": round(hue_approx, 1) if hue_approx else None,
                "value": round(val_approx, 1),
                "chroma": round(chroma_approx, 1),
                "cartesian": [cart[0], cart[1], cart[2]],
                "source": "xkcd",
                "confidence": c['ml_prob'],
                "sample_count": c['responses'],
                "hex_representative": c['hex']
            }

    dictionary_file = RESULTS_DIR / "combined_color_dictionary.json"
    with open(dictionary_file, 'w') as f:
        json.dump(dictionary, f, indent=2)

    print(f"  Created: {dictionary_file}")
    print(f"  Total entries: {len(dictionary)}")

    # =========================================================================
    # Summary
    # =========================================================================
    print("\n" + "=" * 60)
    print("FINAL RESULTS SUMMARY")
    print("=" * 60)
    print(f"overlay_colors_dataset.csv:      {20 + len(new_candidates)} colors")
    print(f"overlay_centroids.json:          {len(centroids)} overlays")
    print(f"iscc_nbs_contradictions.json:    {contradictions['summary']['with_issues']} issues")
    print(f"combined_color_dictionary.json:  {len(dictionary)} entries")
    print("=" * 60)


if __name__ == "__main__":
    main()
