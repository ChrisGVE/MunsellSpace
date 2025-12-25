#!/usr/bin/env python3
"""
Stage 2: Color Wheel Consistency Check

Verifies that color names semantically match their RGB coordinates.
For example, "blue" should have a hue around 240°, not near 0° (red).

Method:
1. Extract expected hue from color name semantics
2. Compute actual hue from RGB coordinates
3. Check consistency within tolerance
4. Flag mismatches for review
"""

import csv
import json
import colorsys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from collections import defaultdict
import numpy as np

from common import save_results, INVESTIGATION_DIR


# Color wheel reference: hue angles in degrees (HSV/HSL)
# Standard color wheel has Red at 0°, Green at 120°, Blue at 240°
HUE_REFERENCE = {
    # Primary colors
    'red': 0,
    'green': 120,
    'blue': 240,

    # Secondary colors
    'yellow': 60,
    'cyan': 180,
    'magenta': 300,

    # Tertiary colors
    'orange': 30,
    'chartreuse': 90,
    'spring': 150,  # spring green
    'azure': 210,
    'violet': 270,
    'rose': 330,

    # Common color names mapped to hue ranges
    'teal': 180,
    'aqua': 180,
    'turquoise': 175,
    'lime': 90,
    'olive': 60,  # yellowish-green
    'gold': 50,
    'amber': 40,
    'coral': 15,
    'salmon': 10,
    'pink': 340,
    'fuchsia': 300,
    'purple': 280,
    'indigo': 260,
    'navy': 240,
    'cerulean': 200,
    'mint': 150,
    'emerald': 145,
    'jade': 155,
    'forest': 120,
    'sage': 100,
    'khaki': 55,
    'tan': 35,
    'beige': 40,
    'peach': 25,
    'maroon': 0,
    'crimson': 348,
    'scarlet': 5,
    'vermilion': 10,
    'rust': 20,
    'copper': 25,
    'bronze': 30,
    'sienna': 15,
    'umber': 25,
    'lavender': 270,
    'lilac': 285,
    'plum': 290,
    'mauve': 310,
    'periwinkle': 250,
    'cobalt': 220,
    'sapphire': 225,
    'denim': 215,
    'cornflower': 220,
    'sky': 200,
    'ocean': 200,
    'sea': 170,
    'seafoam': 160,
    'moss': 110,
    'grass': 100,
    'leaf': 100,
    'pear': 85,
    'pistachio': 100,
    'avocado': 80,
    'mustard': 50,
    'lemon': 55,
    'canary': 55,
    'sunflower': 45,
    'tangerine': 25,
    'apricot': 30,
    'melon': 20,
    'papaya': 25,
    'mango': 40,
    'pumpkin': 25,
    'carrot': 25,
    'persimmon': 20,
    'brick': 10,
    'terracotta': 15,
    'wine': 340,
    'burgundy': 345,
    'berry': 320,
    'raspberry': 335,
    'strawberry': 350,
    'cherry': 355,
    'cranberry': 345,
    'orchid': 300,
    'heather': 290,
    'wisteria': 270,
    'amethyst': 275,
    'grape': 280,
    'eggplant': 285,
    'aubergine': 285,
    'mulberry': 310,
}

# Pure neutral colors (no specific hue - check saturation instead)
NEUTRAL_COLORS = {
    'white', 'black', 'gray', 'grey', 'silver',
    'ash', 'smoke', 'snow',
    'pearl', 'cloud', 'fog', 'mist',
    'pewter', 'graphite', 'coal', 'ebony',
}

# Warm off-whites (have yellow undertone)
WARM_OFF_WHITES = {
    'cream': (50, 70),
    'ivory': (45, 65),
    'bone': (40, 60),
    'eggshell': (45, 65),
}

# Colors that often combine with blue/gray - treat specially
BLUE_GRAY_COLORS = {
    'slate': 210,  # Slate typically has blue undertone
    'charcoal': 210,  # Often has blue-gray tone
    'steel': 210,  # Steel blue
}

# Brown family: warm hues with low-medium saturation (hue range in degrees)
BROWN_HUES = {
    'brown': (5, 45),  # broad range for brown
    'chocolate': (10, 35),
    'coffee': (15, 40),
    'mocha': (15, 40),
    'chestnut': (5, 30),
    'walnut': (20, 45),
    'mahogany': (0, 25),
    'cinnamon': (10, 35),
    'caramel': (25, 50),
    'tan': (25, 55),
    'beige': (30, 60),
    'khaki': (40, 70),
    'taupe': (25, 55),
    'sand': (35, 60),
    'wheat': (35, 55),
    'oatmeal': (30, 50),
    'stone': (30, 60),
    'mushroom': (20, 45),
    'dirt': (15, 40),
    'mud': (20, 50),
    'clay': (10, 35),
    'earth': (15, 40),
    'umber': (20, 45),
    'sienna': (10, 30),
    'rust': (10, 30),
    'copper': (15, 35),
    'bronze': (20, 45),
}


class ColorWheelConsistencyChecker:
    """Check consistency between color name semantics and actual RGB values."""

    # Hue tolerance in degrees
    HUE_TOLERANCE = 45  # Allow ±45° variation

    # Saturation threshold for "colorless" (neutral)
    NEUTRAL_SATURATION_THRESHOLD = 0.15

    # Lightness thresholds
    DARK_THRESHOLD = 0.25
    LIGHT_THRESHOLD = 0.75

    def __init__(self):
        self.vocab_dir = Path(__file__).parent.parent / "color-vocabularies"
        self.investigation_dir = Path(__file__).parent.parent / "investigation"
        self.color_coordinates: Dict[str, str] = {}  # name -> hex
        self._load_color_coordinates()

    def _rgb_to_hex(self, rgb: List[int]) -> str:
        """Convert RGB list to hex string."""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def _load_color_coordinates(self):
        """Load color coordinates from all available sources."""
        # First, load the complete XKCD coordinates cache (175K names with RGB)
        xkcd_cache_path = self.investigation_dir / "xkcd_coordinates_cache.json"
        if xkcd_cache_path.exists():
            with open(xkcd_cache_path) as f:
                xkcd_data = json.load(f)
            for name, rgb_list in xkcd_data.items():
                name_lower = name.lower().strip()
                if name_lower not in self.color_coordinates and rgb_list:
                    # Take the first (or most common) RGB value
                    if isinstance(rgb_list[0], list):
                        rgb = rgb_list[0]
                    else:
                        rgb = rgb_list
                    self.color_coordinates[name_lower] = self._rgb_to_hex(rgb)
            print(f"  Loaded {len(self.color_coordinates):,} from XKCD coordinates cache")

        # Then add from vocabulary CSVs (for non-XKCD names)
        sources = [
            'xkcd_colors.csv',
            'colorhexa_colors.csv',
            'wikipedia_colors.csv',
            'meodai_colors.csv',
            'color_name_com_colors.csv',
        ]

        csv_count = 0
        for source in sources:
            path = self.vocab_dir / source
            if not path.exists():
                continue

            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        name = row[0].lower().strip()
                        coords = row[1].strip()
                        # Only store if not already present (XKCD cache has priority)
                        if name not in self.color_coordinates:
                            self.color_coordinates[name] = coords
                            csv_count += 1

        print(f"  Added {csv_count:,} from vocabulary CSVs")
        print(f"  Total: {len(self.color_coordinates):,} color coordinates")

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )

    def rgb_to_hsl(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSL (hue in degrees, saturation and lightness 0-1)."""
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
        return h * 360, s, l  # Return hue in degrees

    def extract_base_color(self, name: str) -> Optional[str]:
        """Extract the base color word from a color name."""
        name = name.lower().strip()
        words = re.split(r'[\s\-_]+', name)

        # Check each word against known color references
        for word in reversed(words):  # Check last word first (e.g., "light blue" -> "blue")
            # Remove common suffixes
            for suffix in ['ish', 'y', 'ey', 'ie', 'er', 'est', 'esque']:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    base = word[:-len(suffix)]
                    if base in HUE_REFERENCE:
                        return base
                    if base in NEUTRAL_COLORS:
                        return base

            if word in HUE_REFERENCE:
                return word
            if word in NEUTRAL_COLORS:
                return word
            if word in BLUE_GRAY_COLORS:
                return word
            if word in WARM_OFF_WHITES:
                return word
            if word in BROWN_HUES:
                return word

        # Check for partial matches (e.g., "greenish" contains "green")
        for color in HUE_REFERENCE:
            if color in name:
                return color

        for color in NEUTRAL_COLORS:
            if color in name:
                return color

        for color in BLUE_GRAY_COLORS:
            if color in name:
                return color

        for color in WARM_OFF_WHITES:
            if color in name:
                return color

        for color in BROWN_HUES:
            if color in name:
                return color

        return None

    def get_expected_hue(self, name: str) -> Optional[Tuple[float, bool, Optional[Tuple[int, int]]]]:
        """
        Get expected hue for a color name.

        Returns:
            Tuple of (expected_hue, is_neutral, hue_range) or None if unknown
            - hue_range is (min, max) for brown family colors, None otherwise
        """
        base_color = self.extract_base_color(name)

        if base_color is None:
            return None

        if base_color in NEUTRAL_COLORS:
            # Check if name also contains a chromatic color (e.g., "blue gray")
            for word in re.split(r'[\s\-_]+', name.lower()):
                if word in HUE_REFERENCE and word != base_color:
                    # It's a compound like "blue gray" - use the chromatic hue
                    return (HUE_REFERENCE[word], False, None)
            return (0, True, None)  # Pure neutral - hue doesn't matter

        if base_color in BLUE_GRAY_COLORS:
            hue = BLUE_GRAY_COLORS[base_color]
            return (hue, False, None)  # Treat as chromatic with expected hue

        if base_color in WARM_OFF_WHITES:
            hue_range = WARM_OFF_WHITES[base_color]
            mid_hue = (hue_range[0] + hue_range[1]) / 2
            return (mid_hue, False, hue_range)  # Warm off-white with range

        if base_color in BROWN_HUES:
            hue_range = BROWN_HUES[base_color]
            mid_hue = (hue_range[0] + hue_range[1]) / 2
            return (mid_hue, False, hue_range)  # Brown family with range

        if base_color in HUE_REFERENCE:
            return (HUE_REFERENCE[base_color], False, None)

        return None

    def check_consistency(self, name: str, hex_color: str) -> Dict:
        """
        Check if a color name is consistent with its RGB value.

        Returns dict with:
            - consistent: bool
            - reason: str
            - expected_hue: float or None
            - actual_hue: float
            - hue_diff: float
            - is_neutral: bool
        """
        result = {
            'name': name,
            'hex': hex_color,
            'consistent': True,
            'reason': 'unknown',
            'base_color': None,
            'expected_hue': None,
            'actual_hue': None,
            'hue_diff': None,
            'saturation': None,
            'lightness': None,
            'is_neutral': False,
        }

        # Convert to HSL
        try:
            r, g, b = self.hex_to_rgb(hex_color)
            hue, sat, light = self.rgb_to_hsl(r, g, b)
        except (ValueError, IndexError):
            result['consistent'] = False
            result['reason'] = 'invalid_hex'
            return result

        result['actual_hue'] = round(hue, 1)
        result['saturation'] = round(sat, 3)
        result['lightness'] = round(light, 3)

        # Get expected hue
        expected = self.get_expected_hue(name)

        if expected is None:
            result['reason'] = 'no_base_color'
            return result

        expected_hue, is_neutral, hue_range = expected
        result['expected_hue'] = expected_hue
        result['is_neutral'] = is_neutral
        result['base_color'] = self.extract_base_color(name)

        # Check neutral colors (should have low saturation)
        if is_neutral:
            if sat < self.NEUTRAL_SATURATION_THRESHOLD:
                result['reason'] = 'neutral_match'
                return result
            else:
                result['consistent'] = False
                result['reason'] = 'neutral_has_saturation'
                return result

        # Check brown family colors (have specific hue ranges)
        if hue_range is not None:
            low, high = hue_range
            if low <= hue <= high:
                result['reason'] = 'brown_family_match'
                result['hue_diff'] = 0  # Within range
                return result
            else:
                # Calculate distance to range
                if hue < low:
                    hue_diff = low - hue
                else:
                    hue_diff = hue - high
                result['hue_diff'] = round(hue_diff, 1)

                # Allow some tolerance beyond range
                if hue_diff <= 15:  # 15° tolerance beyond range
                    result['reason'] = 'brown_family_match'
                    return result

                result['consistent'] = False
                result['reason'] = 'brown_hue_mismatch'
                return result

        # Check chromatic colors (should have matching hue)
        # Calculate hue difference (accounting for circular nature)
        hue_diff = abs(hue - expected_hue)
        if hue_diff > 180:
            hue_diff = 360 - hue_diff

        result['hue_diff'] = round(hue_diff, 1)

        # Very low saturation colors - can't reliably determine hue
        if sat < 0.1:
            result['reason'] = 'low_saturation_hue_unreliable'
            return result

        # Check if within tolerance
        if hue_diff <= self.HUE_TOLERANCE:
            result['reason'] = 'hue_match'
            return result

        # Check for compound colors (e.g., "blue green" should be between blue and green)
        if self._is_compound_color(name):
            if self._check_compound_hue(name, hue):
                result['reason'] = 'compound_match'
                return result

        # Mismatch
        result['consistent'] = False
        result['reason'] = 'hue_mismatch'
        return result

    def _is_compound_color(self, name: str) -> bool:
        """Check if name is a compound color (e.g., 'blue green', 'yellowish green')."""
        words = re.split(r'[\s\-_]+', name.lower())

        # Count direct color words
        color_count = sum(1 for w in words if w in HUE_REFERENCE)
        if color_count >= 2:
            return True

        # Check for "-ish" modified colors (e.g., "yellowish green" = yellow + green)
        for word in words:
            for suffix in ['ish', 'y', 'ey']:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    base = word[:-len(suffix)]
                    if base in HUE_REFERENCE and color_count >= 1:
                        return True

        return False

    def _get_compound_hues(self, name: str) -> List[float]:
        """Extract all hue values implied by a compound color name."""
        words = re.split(r'[\s\-_]+', name.lower())
        hues = []

        for word in words:
            # Direct color words
            if word in HUE_REFERENCE:
                hues.append(HUE_REFERENCE[word])
                continue

            # Handle "-ish" suffixes
            for suffix in ['ish', 'y', 'ey']:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    base = word[:-len(suffix)]
                    if base in HUE_REFERENCE:
                        hues.append(HUE_REFERENCE[base])
                        break

        return hues

    def _check_compound_hue(self, name: str, actual_hue: float) -> bool:
        """Check if actual hue falls between compound color components."""
        hues = self._get_compound_hues(name)

        if len(hues) < 2:
            return False

        # Get min and max hue (handle wraparound)
        min_hue = min(hues)
        max_hue = max(hues)

        # Check if actual hue is between the components
        # Handle wraparound case (e.g., red-violet spans 0°)
        if max_hue - min_hue <= 180:
            # Normal case
            margin = 30
            return min_hue - margin <= actual_hue <= max_hue + margin
        else:
            # Wraparound case
            margin = 30
            return actual_hue >= max_hue - margin or actual_hue <= min_hue + margin

    def validate_colors(self, validated_names: Dict) -> Dict:
        """
        Validate all color names for color wheel consistency.

        Args:
            validated_names: Dict of validated color names from Stage 1

        Returns:
            Validation results with statistics and flagged items
        """
        results = {
            'total': 0,
            'consistent': 0,
            'inconsistent': 0,
            'unknown': 0,
            'by_reason': defaultdict(int),
            'inconsistent_samples': [],
            'unknown_samples': [],
            'statistics': {},
        }

        all_checks = []

        for name in validated_names:
            # Find coordinates for this name
            name_lower = name.lower().strip()
            hex_color = self.color_coordinates.get(name_lower)

            if hex_color is None:
                results['unknown'] += 1
                if len(results['unknown_samples']) < 20:
                    results['unknown_samples'].append(name)
                continue

            results['total'] += 1
            check = self.check_consistency(name_lower, hex_color)
            all_checks.append(check)

            results['by_reason'][check['reason']] += 1

            if check['consistent']:
                results['consistent'] += 1
            else:
                results['inconsistent'] += 1
                if len(results['inconsistent_samples']) < 100:
                    results['inconsistent_samples'].append({
                        'name': name,
                        'hex': hex_color,
                        'base_color': check['base_color'],
                        'expected_hue': check['expected_hue'],
                        'actual_hue': check['actual_hue'],
                        'hue_diff': check['hue_diff'],
                        'saturation': check['saturation'],
                        'reason': check['reason'],
                    })

        # Calculate statistics
        hue_diffs = [c['hue_diff'] for c in all_checks
                     if c['hue_diff'] is not None and not c['is_neutral']]

        if hue_diffs:
            results['statistics'] = {
                'mean_hue_diff': round(np.mean(hue_diffs), 1),
                'median_hue_diff': round(np.median(hue_diffs), 1),
                'std_hue_diff': round(np.std(hue_diffs), 1),
                'max_hue_diff': round(max(hue_diffs), 1),
                'percentiles': {
                    '50': round(np.percentile(hue_diffs, 50), 1),
                    '75': round(np.percentile(hue_diffs, 75), 1),
                    '90': round(np.percentile(hue_diffs, 90), 1),
                    '95': round(np.percentile(hue_diffs, 95), 1),
                }
            }

        return results


def run_consistency_check():
    """Run the color wheel consistency check."""
    print("=" * 70)
    print("STAGE 2: COLOR WHEEL CONSISTENCY CHECK")
    print("=" * 70)
    print()

    # Load validated names from Stage 1
    print("1. Loading validated color names...")
    validated_path = INVESTIGATION_DIR / "validated_color_names.json"

    if not validated_path.exists():
        print(f"   ERROR: {validated_path} not found")
        print("   Run full_scale_validation.py first")
        return None

    with open(validated_path) as f:
        validated_names = json.load(f)

    print(f"   Loaded {len(validated_names):,} validated names")
    print()

    # Initialize checker
    print("2. Initializing color wheel checker...")
    checker = ColorWheelConsistencyChecker()
    print()

    # Run validation
    print("3. Checking color wheel consistency...")
    results = checker.validate_colors(validated_names)
    print()

    # Report results
    print("4. Results:")
    print()
    print(f"   SUMMARY:")
    print(f"   ├─ Total checked: {results['total']:,}")
    print(f"   ├─ Consistent: {results['consistent']:,} "
          f"({results['consistent']/results['total']*100:.1f}%)")
    print(f"   ├─ Inconsistent: {results['inconsistent']:,} "
          f"({results['inconsistent']/results['total']*100:.1f}%)")
    print(f"   └─ Unknown (no coordinates): {results['unknown']:,}")

    print()
    print(f"   BY REASON:")
    for reason, count in sorted(results['by_reason'].items(),
                                 key=lambda x: -x[1]):
        pct = count / results['total'] * 100
        print(f"   ├─ {reason}: {count:,} ({pct:.1f}%)")

    if results['statistics']:
        print()
        print(f"   HUE DIFFERENCE STATISTICS (chromatic colors):")
        stats = results['statistics']
        print(f"   ├─ Mean: {stats['mean_hue_diff']}°")
        print(f"   ├─ Median: {stats['median_hue_diff']}°")
        print(f"   ├─ Std: {stats['std_hue_diff']}°")
        print(f"   ├─ 90th percentile: {stats['percentiles']['90']}°")
        print(f"   └─ Max: {stats['max_hue_diff']}°")

    print()
    print("   INCONSISTENT SAMPLES (to review):")
    for sample in results['inconsistent_samples'][:15]:
        print(f"   ├─ '{sample['name']}' ({sample['hex']})")
        print(f"   │  base='{sample['base_color']}', "
              f"expected={sample['expected_hue']}°, actual={sample['actual_hue']}°, "
              f"diff={sample['hue_diff']}°")

    if results['unknown_samples']:
        print()
        print(f"   UNKNOWN SAMPLES (no coordinates found):")
        for name in results['unknown_samples'][:10]:
            print(f"   ├─ '{name}'")

    # Save results
    print()
    print("5. Saving results...")
    save_results(results, 'color_wheel_consistency_results.json')

    print()
    print("=" * 70)
    print("CONSISTENCY CHECK COMPLETE")
    print("=" * 70)

    return results


if __name__ == "__main__":
    run_consistency_check()
