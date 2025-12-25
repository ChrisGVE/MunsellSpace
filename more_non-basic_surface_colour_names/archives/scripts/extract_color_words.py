#!/usr/bin/env python3
"""
A Posteriori Color Word Extraction

Instead of pre-defining patterns, this script:
1. Extracts ALL unique words from color names
2. For each word, aggregates colors containing it
3. Computes statistics to identify potential color terms
4. Outputs candidates without a priori bias

This is more rigorous than pattern matching.
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
import math

INPUT_FILE = Path("tmp/xkcd_color_aggregates.json")
OUTPUT_FILE = Path("tmp/xkcd_word_analysis.json")
OUTPUT_CSV = Path("tmp/xkcd_word_candidates.csv")

# Minimum instances to consider a word
MIN_WORD_INSTANCES = 30  # Centore uses ~30-100 samples per overlay


def tokenize_colorname(name: str) -> list[str]:
    """Split color name into words, handling various formats."""
    # Replace hyphens and underscores with spaces
    name = name.replace("-", " ").replace("_", " ")
    # Split on whitespace
    words = name.lower().split()
    # Filter out very short words and numbers
    words = [w for w in words if len(w) >= 2 and not w.isdigit()]
    return words


def rgb_to_hue_saturation(r, g, b):
    """Convert RGB to hue (0-360) and saturation (0-1)."""
    r, g, b = r/255, g/255, b/255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    # Saturation
    saturation = 0 if max_c == 0 else delta / max_c

    # Hue
    if delta == 0:
        hue = None  # Achromatic
    elif max_c == r:
        hue = 60 * (((g - b) / delta) % 6)
    elif max_c == g:
        hue = 60 * (((b - r) / delta) + 2)
    else:
        hue = 60 * (((r - g) / delta) + 4)

    # Value (brightness)
    value = max_c

    return hue, saturation, value


def circular_mean(angles):
    """Compute mean of circular data (hue angles)."""
    if not angles:
        return None
    angles = [a for a in angles if a is not None]
    if not angles:
        return None

    sin_sum = sum(math.sin(math.radians(a)) for a in angles)
    cos_sum = sum(math.cos(math.radians(a)) for a in angles)

    mean_angle = math.degrees(math.atan2(sin_sum, cos_sum))
    if mean_angle < 0:
        mean_angle += 360

    return mean_angle


def circular_std(angles):
    """Compute circular standard deviation."""
    if not angles or len(angles) < 2:
        return None
    angles = [a for a in angles if a is not None]
    if len(angles) < 2:
        return None

    sin_sum = sum(math.sin(math.radians(a)) for a in angles)
    cos_sum = sum(math.cos(math.radians(a)) for a in angles)
    n = len(angles)

    R = math.sqrt(sin_sum**2 + cos_sum**2) / n

    # Circular std approximation
    if R >= 1:
        return 0
    return math.degrees(math.sqrt(-2 * math.log(R)))


def main():
    print("Loading color data...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    stats = data['statistics']
    print(f"  Loaded {len(stats):,} unique color names")

    # Build word -> colors mapping
    print("\nExtracting words from all color names...")
    word_colors = defaultdict(list)

    for entry in stats:
        name = entry['colorname']
        rgb = entry['mean_rgb']
        count = entry['count']

        words = tokenize_colorname(name)
        for word in words:
            word_colors[word].append({
                'name': name,
                'rgb': rgb,
                'count': count,
                'hex': entry['hex']
            })

    print(f"  Found {len(word_colors):,} unique words")

    # Analyze each word
    print("\nAnalyzing word statistics...")
    word_stats = []

    for word, colors in word_colors.items():
        if len(colors) < MIN_WORD_INSTANCES:
            continue

        # Total responses across all colors containing this word
        total_responses = sum(c['count'] for c in colors)

        # Compute color statistics
        hues = []
        saturations = []
        values = []

        for c in colors:
            h, s, v = rgb_to_hue_saturation(*c['rgb'])
            if h is not None:
                hues.append(h)
            saturations.append(s)
            values.append(v)

        # Hue coherence (low std = word refers to specific hue)
        hue_mean = circular_mean(hues)
        hue_std = circular_std(hues)

        # Saturation and value stats
        sat_mean = mean(saturations) if saturations else 0
        sat_std = stdev(saturations) if len(saturations) > 1 else 0
        val_mean = mean(values) if values else 0
        val_std = stdev(values) if len(values) > 1 else 0

        # Compute mean RGB
        mean_r = mean(c['rgb'][0] for c in colors)
        mean_g = mean(c['rgb'][1] for c in colors)
        mean_b = mean(c['rgb'][2] for c in colors)

        word_stats.append({
            'word': word,
            'num_colors': len(colors),
            'total_responses': total_responses,
            'hue_mean': hue_mean,
            'hue_std': hue_std,
            'sat_mean': sat_mean,
            'sat_std': sat_std,
            'val_mean': val_mean,
            'val_std': val_std,
            'mean_rgb': [mean_r, mean_g, mean_b],
            'hex': f"#{int(mean_r):02x}{int(mean_g):02x}{int(mean_b):02x}",
            'sample_names': [c['name'] for c in sorted(colors, key=lambda x: x['count'], reverse=True)[:5]]
        })

    # Sort by total responses
    word_stats.sort(key=lambda x: x['total_responses'], reverse=True)

    print(f"  Analyzed {len(word_stats):,} words with >= {MIN_WORD_INSTANCES} instances")

    # Classify words into categories
    # A "color word" should have:
    # 1. Relatively low hue_std (refers to specific hue region) OR be a modifier
    # 2. High total_responses (commonly used)

    # Identify modifiers (words that appear with many different hues)
    modifiers = []
    color_words = []
    ambiguous = []

    for ws in word_stats:
        hue_std = ws['hue_std']

        if hue_std is None:
            # Achromatic words (gray, black, white, etc.)
            if ws['sat_mean'] < 0.15:
                color_words.append(ws)
            else:
                ambiguous.append(ws)
        elif hue_std > 60:
            # High hue variance = modifier (light, dark, bright, pale, etc.)
            modifiers.append(ws)
        elif hue_std < 40:
            # Low hue variance = specific color term
            color_words.append(ws)
        else:
            ambiguous.append(ws)

    print("\n" + "=" * 80)
    print("WORD CLASSIFICATION RESULTS")
    print("=" * 80)

    print(f"\nCOLOR WORDS (low hue variance, likely color terms): {len(color_words)}")
    print("-" * 80)
    for ws in color_words[:50]:
        hue_str = f"{ws['hue_mean']:.0f}°" if ws['hue_mean'] else "N/A"
        std_str = f"±{ws['hue_std']:.0f}°" if ws['hue_std'] else ""
        print(f"  {ws['word']:20} {ws['total_responses']:>8,} responses  "
              f"hue: {hue_str:>6} {std_str:>6}  {ws['hex']}  "
              f"({ws['num_colors']} variants)")

    print(f"\nMODIFIERS (high hue variance, apply to many colors): {len(modifiers)}")
    print("-" * 80)
    for ws in modifiers[:30]:
        hue_str = f"{ws['hue_mean']:.0f}°" if ws['hue_mean'] else "N/A"
        std_str = f"±{ws['hue_std']:.0f}°" if ws['hue_std'] else ""
        print(f"  {ws['word']:20} {ws['total_responses']:>8,} responses  "
              f"hue: {hue_str:>6} {std_str:>6}  "
              f"({ws['num_colors']} variants)")

    print(f"\nAMBIGUOUS (medium hue variance): {len(ambiguous)}")
    print("-" * 80)
    for ws in ambiguous[:20]:
        hue_str = f"{ws['hue_mean']:.0f}°" if ws['hue_mean'] else "N/A"
        std_str = f"±{ws['hue_std']:.0f}°" if ws['hue_std'] else ""
        print(f"  {ws['word']:20} {ws['total_responses']:>8,} responses  "
              f"hue: {hue_str:>6} {std_str:>6}  {ws['hex']}  "
              f"({ws['num_colors']} variants)")

    # Save results
    print(f"\nSaving results to {OUTPUT_FILE}...")
    output = {
        'total_words_analyzed': len(word_stats),
        'color_words': color_words,
        'modifiers': modifiers,
        'ambiguous': ambiguous
    }
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    # Save CSV of color words
    print(f"Saving color words to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, 'w') as f:
        f.write("word,num_colors,total_responses,hue_mean,hue_std,sat_mean,val_mean,hex\n")
        for ws in color_words:
            f.write(f"{ws['word']},{ws['num_colors']},{ws['total_responses']},"
                   f"{ws['hue_mean'] or 0:.1f},{ws['hue_std'] or 0:.1f},"
                   f"{ws['sat_mean']:.3f},{ws['val_mean']:.3f},{ws['hex']}\n")

    print("\nDone!")


if __name__ == "__main__":
    main()
