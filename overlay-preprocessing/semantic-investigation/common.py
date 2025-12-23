#!/usr/bin/env python3
"""
Common utilities for semantic color name experiments.
"""

import json
import re
import os
from pathlib import Path
from typing import Optional

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
INVESTIGATION_DIR = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "overlay-preprocessing" / "investigation"
XKCD_CACHE = DATA_DIR / "xkcd_color_counts_cache.json"


def load_xkcd_names() -> dict:
    """Load XKCD color names and their counts."""
    if XKCD_CACHE.exists():
        with open(XKCD_CACHE) as f:
            return json.load(f)
    raise FileNotFoundError(f"XKCD cache not found at {XKCD_CACHE}")


def load_centore_names() -> set:
    """Load Centore color names from polyhedron files."""
    centore_dir = PROJECT_ROOT / "overlay-preprocessing" / "data" / "Centore" / "PolyhedronFilesJustNames"
    names = set()

    if not centore_dir.exists():
        return names

    for txt_file in centore_dir.glob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Format: Name: H V/C or Name: Neutral V
                    if ':' in line:
                        name = line.split(':')[0].strip()
                        if name:
                            names.add(name.lower())

    return names


# Known color vocabulary for validation
BASIC_COLORS = {
    'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown',
    'black', 'white', 'gray', 'grey', 'cyan', 'magenta', 'violet', 'indigo',
    'teal', 'turquoise', 'maroon', 'navy', 'olive', 'lime', 'aqua', 'coral',
    'salmon', 'crimson', 'scarlet', 'burgundy', 'fuchsia', 'lavender',
    'lilac', 'mauve', 'beige', 'tan', 'cream', 'ivory', 'gold', 'silver',
    'bronze', 'copper', 'rose', 'peach', 'apricot', 'amber', 'ochre',
    'sienna', 'umber', 'khaki', 'chartreuse', 'mint', 'sage', 'forest',
    'emerald', 'jade', 'azure', 'cobalt', 'cerulean', 'sapphire', 'plum',
    'grape', 'wine', 'rust', 'terracotta', 'taupe', 'charcoal', 'slate'
}

COLOR_MODIFIERS = {
    'light', 'dark', 'bright', 'pale', 'deep', 'vivid', 'dull', 'muted',
    'pastel', 'neon', 'fluorescent', 'metallic', 'dusty', 'dirty', 'muddy',
    'warm', 'cool', 'hot', 'cold', 'soft', 'hard', 'faded', 'washed',
    'rich', 'royal', 'baby', 'powder', 'electric', 'burnt', 'raw',
    'very', 'really', 'slightly', 'somewhat', 'almost', 'nearly',
    'ish', 'esque', 'like', 'tinted', 'hued', 'colored', 'coloured'
}

COLOR_SUFFIXES = {'ish', 'y', 'er', 'est', 'esque'}


def preprocess_name(name: str) -> str:
    """Basic preprocessing: lowercase, strip, normalize whitespace."""
    name = name.lower().strip()
    name = re.sub(r'\s+', ' ', name)
    return name


def clean_special_chars(name: str) -> str:
    """Remove special characters that are clearly noise."""
    # Remove leading/trailing punctuation except hyphens
    name = re.sub(r'^[^\w\s-]+', '', name)
    name = re.sub(r'[^\w\s-]+$', '', name)
    # Normalize internal punctuation
    name = re.sub(r"[''`]", "'", name)
    return name.strip()


def is_hex_color(name: str) -> Optional[tuple]:
    """Check if name is a hex color code and return RGB if so."""
    name = name.strip()
    if re.match(r'^#?[0-9a-fA-F]{6}$', name):
        hex_str = name.lstrip('#')
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return (r, g, b)
    return None


def contains_color_word(name: str) -> bool:
    """Quick check if name contains any known color word."""
    words = set(re.split(r'[\s\-_]+', name.lower()))
    return bool(words & BASIC_COLORS)


def get_test_set() -> dict:
    """Return a curated test set for validation."""
    return {
        # Valid descriptive colors
        'valid_descriptive': [
            'light blue', 'dark green', 'pale yellow', 'bright red',
            'deep purple', 'soft pink', 'muted orange', 'vivid cyan',
            'dusty rose', 'pastel lavender', 'neon green', 'baby blue'
        ],
        # Valid metaphorical colors
        'valid_metaphor': [
            'sky blue', 'grass green', 'lemon yellow', 'cherry red',
            'forest green', 'ocean blue', 'sunset orange', 'midnight blue',
            'rose pink', 'chocolate brown', 'cream white', 'coal black'
        ],
        # Valid artistic/brand colors
        'valid_artistic': [
            'fedex purple', 'tiffany blue', 'klein blue', 'barbie pink',
            'coke red', 'starbucks green', 'ikea blue', 'ferrari red'
        ],
        # Valid compound colors
        'valid_compound': [
            'bluish green', 'greenish blue', 'reddish orange', 'yellowish green',
            'blue green', 'red orange', 'yellow green', 'blue violet',
            'purplish pink', 'orangey red', 'brownish yellow'
        ],
        # Invalid - no color meaning
        'invalid_no_color': [
            'john', 'hello', 'computer', 'table', 'running', 'happy',
            'asdfgh', 'qwerty', 'abcdef', 'testing', 'sample'
        ],
        # Invalid - spam/noise
        'invalid_noise': [
            '!!!', '???', '...', '---', 'lol', 'wtf', 'idk',
            '123', '456', 'aaa', 'bbb', 'xxx', 'yyy'
        ],
        # Edge cases - should be valid after cleaning
        'edge_clean_to_valid': [
            ('!!!green', 'green'),
            ('##red##', 'red'),
            ('  blue  ', 'blue'),
            ('YELLOW', 'yellow'),
            ("it's blue", "it's blue"),
        ],
        # Edge cases - hex codes
        'edge_hex': [
            ('#0000FF', (0, 0, 255)),  # blue
            ('#FF0000', (255, 0, 0)),  # red
            ('#00FF00', (0, 255, 0)),  # green
            ('0000FF', (0, 0, 255)),   # without hash
        ]
    }


def save_results(results: dict, filename: str):
    """Save experiment results to JSON."""
    output_path = INVESTIGATION_DIR / filename
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {output_path}")


def load_results(filename: str) -> dict:
    """Load experiment results from JSON."""
    input_path = INVESTIGATION_DIR / filename
    with open(input_path) as f:
        return json.load(f)
