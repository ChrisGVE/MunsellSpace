#!/usr/bin/env python3
"""
Stage 4: Centore Reference Comparison

Compares XKCD-derived Munsell positions with Centore reference overlays
to detect systematic biases between screen colors and physical colors.

Pipeline:
1. Load Centore reference data (spectrophotometer-measured colors)
2. Load XKCD Munsell conversions from Stage 3
3. Match XKCD colors to Centore categories by name
4. Compute XKCD-derived centroids for each category
5. Compare with Centore reference centroids
6. Detect systematic biases (hue shift, value shift, chroma shift)

Usage:
    python centore_comparison.py
"""

import json
import re
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass
import statistics

from common import save_results, INVESTIGATION_DIR


@dataclass
class MunsellCoord:
    """Munsell color coordinate."""
    hue_str: str
    hue_num: float
    value: float
    chroma: float

    @property
    def is_neutral(self) -> bool:
        return self.hue_str == 'N' or self.chroma < 0.5

    def to_cartesian(self) -> Tuple[float, float, float]:
        """Convert to cartesian coordinates (x, y, z) where z is value."""
        if self.is_neutral:
            return (0.0, 0.0, self.value)

        # Hue angle in radians (0-360 mapped to 0-2π)
        hue_angle = self.hue_num * math.pi / 180.0
        x = self.chroma * math.cos(hue_angle)
        y = self.chroma * math.sin(hue_angle)
        return (x, y, self.value)


@dataclass
class CentoreCategory:
    """Centore reference color category."""
    name: str
    sample_count: int
    centroid_munsell: str
    centroid_cartesian: Tuple[float, float, float]
    centroid_parsed: Optional[MunsellCoord]
    samples: List[Tuple[str, str]]  # (sample_name, munsell_notation)


class CentoreComparisonAnalyzer:
    """Analyzes differences between XKCD and Centore color data."""

    # Mapping from Centore category names to search patterns
    CATEGORY_PATTERNS = {
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

    # Hue family to angle mapping (center of each family)
    HUE_FAMILIES = {
        'R': 0, 'YR': 36, 'Y': 72, 'GY': 108,
        'G': 144, 'BG': 180, 'B': 216, 'PB': 252,
        'P': 288, 'RP': 324
    }

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.centore_dir = self.project_root / "PolyhedronFilesJustNames"
        self.investigation_dir = INVESTIGATION_DIR

        self.centore_categories: Dict[str, CentoreCategory] = {}
        self.xkcd_munsell: Dict = {}

    def parse_munsell_notation(self, notation: str) -> Optional[MunsellCoord]:
        """Parse Munsell notation string to MunsellCoord."""
        notation = notation.strip()

        # Handle neutral colors
        if notation.startswith('N ') or notation.startswith('N/'):
            try:
                value = float(notation.split()[1].split('/')[0])
                return MunsellCoord('N', 0.0, value, 0.0)
            except (IndexError, ValueError):
                return None

        # Parse chromatic colors: "5.61P 5.37/4.79" or "6.80PB 6.06/6.09"
        match = re.match(
            r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)',
            notation
        )
        if match:
            hue_value = float(match.group(1))
            hue_family = match.group(2)
            value = float(match.group(3))
            chroma = float(match.group(4))

            # Convert to hue number (0-360)
            family_base = self.HUE_FAMILIES.get(hue_family, 0)
            # Each family spans 36 degrees, hue_value 0-10 maps within that
            hue_num = family_base + (hue_value / 10.0) * 36.0
            if hue_num >= 360:
                hue_num -= 360

            return MunsellCoord(
                f"{hue_value}{hue_family}",
                hue_num,
                value,
                chroma
            )

        return None

    def load_centore_categories(self) -> int:
        """Load all Centore reference categories."""
        count = 0

        for file_path in self.centore_dir.glob("PolyhedronDataFor*.txt"):
            category = self._parse_centore_file(file_path)
            if category:
                self.centore_categories[category.name] = category
                count += 1

        print(f"  Loaded {count} Centore categories")
        return count

    def _parse_centore_file(self, file_path: Path) -> Optional[CentoreCategory]:
        """Parse a single Centore polyhedron file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"  Warning: Could not read {file_path}: {e}")
            return None

        name = None
        sample_count = 0
        centroid_munsell = None
        centroid_cartesian = None
        samples = []

        in_samples = False

        for line in lines:
            line = line.strip()

            if line.startswith('Colour name:'):
                name = line.split(':', 1)[1].strip()

            elif line.startswith('Number of CAUS samples:'):
                try:
                    sample_count = int(line.split(':', 1)[1].strip())
                except ValueError:
                    pass

            elif line.startswith('Centroid in Munsell coordinates:'):
                centroid_munsell = line.split(':', 1)[1].strip()

            elif line.startswith('Centroid in Cartesian coordinates:'):
                parts = line.split(':', 1)[1].strip().split()
                if len(parts) >= 3:
                    try:
                        centroid_cartesian = (
                            float(parts[0]),
                            float(parts[1]),
                            float(parts[2])
                        )
                    except ValueError:
                        pass

            elif line.startswith('Samples, with Munsell coordinates'):
                in_samples = True

            elif in_samples and line:
                # Parse sample line: "Sweet Lavender	0.85R 6.05/2.85"
                parts = line.split('\t')
                if len(parts) >= 2:
                    samples.append((parts[0].strip(), parts[1].strip()))
                elif len(parts) == 1:
                    # Try space separation
                    match = re.match(r'(.+?)\s+(\d+\.?\d*\w+\s+\d+\.?\d*/\d+\.?\d*)', line)
                    if match:
                        samples.append((match.group(1).strip(), match.group(2).strip()))

        if not name or not centroid_munsell:
            return None

        centroid_parsed = self.parse_munsell_notation(centroid_munsell)

        return CentoreCategory(
            name=name,
            sample_count=sample_count,
            centroid_munsell=centroid_munsell,
            centroid_cartesian=centroid_cartesian or (0, 0, 0),
            centroid_parsed=centroid_parsed,
            samples=samples
        )

    def load_xkcd_munsell(self) -> int:
        """Load XKCD Munsell conversions from Stage 3."""
        munsell_path = self.investigation_dir / "munsell_conversions.json"

        if not munsell_path.exists():
            raise FileNotFoundError(f"Munsell conversions not found: {munsell_path}")

        with open(munsell_path) as f:
            data = json.load(f)

        self.xkcd_munsell = data.get('colors', {})
        print(f"  Loaded {len(self.xkcd_munsell):,} XKCD Munsell conversions")
        return len(self.xkcd_munsell)

    def match_xkcd_to_category(self, category_name: str) -> List[Tuple[str, Dict]]:
        """Find XKCD colors matching a Centore category."""
        patterns = self.CATEGORY_PATTERNS.get(category_name, [])
        if not patterns:
            # Fall back to simple word match
            patterns = [rf'\b{re.escape(category_name)}\b']

        matches = []
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

        for name, data in self.xkcd_munsell.items():
            for pattern in compiled_patterns:
                if pattern.search(name):
                    matches.append((name, data))
                    break

        return matches

    def compute_xkcd_centroid(self, matches: List[Tuple[str, Dict]]) -> Optional[MunsellCoord]:
        """Compute centroid of XKCD colors in a category."""
        if not matches:
            return None

        # Collect cartesian coordinates
        xs, ys, values, chromas = [], [], [], []
        hue_sins, hue_coss = [], []

        for name, data in matches:
            m = data['munsell']
            cart = data['cartesian']

            xs.append(cart['x'])
            ys.append(cart['y'])
            values.append(m['value'])
            chromas.append(m['chroma'])

            # For circular mean of hue
            # Note: hue_num from Rust is in 0-40 Munsell scale, convert to radians
            # 0-40 maps to 0-360 degrees, so multiply by 9 to get degrees, then convert
            hue_degrees = m['hue_num'] * 9.0  # 40 -> 360
            hue_rad = hue_degrees * math.pi / 180.0
            hue_sins.append(math.sin(hue_rad))
            hue_coss.append(math.cos(hue_rad))

        # Compute means
        mean_x = statistics.mean(xs)
        mean_y = statistics.mean(ys)
        mean_value = statistics.mean(values)
        mean_chroma = statistics.mean(chromas)

        # Circular mean for hue
        mean_sin = statistics.mean(hue_sins)
        mean_cos = statistics.mean(hue_coss)
        mean_hue = math.atan2(mean_sin, mean_cos) * 180.0 / math.pi
        if mean_hue < 0:
            mean_hue += 360

        # Convert hue to Munsell notation
        hue_str = self._hue_num_to_str(mean_hue)

        return MunsellCoord(hue_str, mean_hue, mean_value, mean_chroma)

    def _hue_num_to_str(self, hue_degrees: float) -> str:
        """Convert hue degrees (0-360) to Munsell hue string."""
        # Each family spans 36 degrees, 10 families total
        families = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

        # Normalize to 0-360
        hue_degrees = hue_degrees % 360

        # Each family spans 36 degrees
        family_idx = int(hue_degrees / 36) % 10
        within_family = (hue_degrees % 36) / 36.0 * 10.0

        return f"{within_family:.1f}{families[family_idx]}"

    def compute_bias(self, centore: MunsellCoord, xkcd: MunsellCoord) -> Dict:
        """Compute bias between Centore reference and XKCD-derived centroid."""
        # Hue difference (handle circular)
        hue_diff = xkcd.hue_num - centore.hue_num
        if hue_diff > 180:
            hue_diff -= 360
        elif hue_diff < -180:
            hue_diff += 360

        # Value and chroma differences
        value_diff = xkcd.value - centore.value
        chroma_diff = xkcd.chroma - centore.chroma

        # Cartesian difference
        centore_cart = centore.to_cartesian()
        xkcd_cart = xkcd.to_cartesian()

        delta_x = xkcd_cart[0] - centore_cart[0]
        delta_y = xkcd_cart[1] - centore_cart[1]
        delta_z = xkcd_cart[2] - centore_cart[2]

        # Euclidean distance
        distance = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        # Distance in chroma-value plane only
        cv_distance = math.sqrt(chroma_diff**2 + value_diff**2)

        return {
            'hue_diff': round(hue_diff, 2),
            'value_diff': round(value_diff, 2),
            'chroma_diff': round(chroma_diff, 2),
            'delta_x': round(delta_x, 3),
            'delta_y': round(delta_y, 3),
            'delta_z': round(delta_z, 3),
            'euclidean_distance': round(distance, 3),
            'cv_distance': round(cv_distance, 3),
        }

    def run_comparison(self) -> Dict:
        """Run the complete Stage 4 comparison."""
        print("=" * 70)
        print("STAGE 4: CENTORE COMPARISON & BIAS DETECTION")
        print("=" * 70)
        print()

        # Step 1: Load data
        print("1. Loading Centore reference data...")
        self.load_centore_categories()

        print("\n2. Loading XKCD Munsell conversions...")
        self.load_xkcd_munsell()

        # Step 2: Compare each category
        print("\n3. Comparing categories...")

        comparisons = {}
        all_biases = []

        for cat_name, centore_cat in sorted(self.centore_categories.items()):
            # Find matching XKCD colors
            matches = self.match_xkcd_to_category(cat_name)

            if not matches:
                print(f"   {cat_name}: No XKCD matches found")
                comparisons[cat_name] = {
                    'centore_samples': centore_cat.sample_count,
                    'xkcd_matches': 0,
                    'comparison': None
                }
                continue

            # Compute XKCD centroid
            xkcd_centroid = self.compute_xkcd_centroid(matches)

            if not xkcd_centroid or not centore_cat.centroid_parsed:
                print(f"   {cat_name}: Could not compute centroids")
                comparisons[cat_name] = {
                    'centore_samples': centore_cat.sample_count,
                    'xkcd_matches': len(matches),
                    'comparison': None
                }
                continue

            # Compute bias
            bias = self.compute_bias(centore_cat.centroid_parsed, xkcd_centroid)
            all_biases.append(bias)

            comparisons[cat_name] = {
                'centore_samples': centore_cat.sample_count,
                'centore_centroid': {
                    'munsell': centore_cat.centroid_munsell,
                    'hue_num': centore_cat.centroid_parsed.hue_num,
                    'value': centore_cat.centroid_parsed.value,
                    'chroma': centore_cat.centroid_parsed.chroma,
                },
                'xkcd_matches': len(matches),
                'xkcd_centroid': {
                    'hue_str': xkcd_centroid.hue_str,
                    'hue_num': round(xkcd_centroid.hue_num, 2),
                    'value': round(xkcd_centroid.value, 2),
                    'chroma': round(xkcd_centroid.chroma, 2),
                },
                'bias': bias,
                'sample_names': [name for name, _ in matches[:10]],  # First 10 samples
            }

            direction = "→" if bias['hue_diff'] > 0 else "←"
            print(f"   {cat_name}: {len(matches):,} matches, "
                  f"Δhue={bias['hue_diff']:+.1f}° {direction}, "
                  f"Δvalue={bias['value_diff']:+.2f}, "
                  f"Δchroma={bias['chroma_diff']:+.2f}")

        # Step 3: Compute aggregate statistics
        print("\n4. Computing aggregate bias statistics...")

        if all_biases:
            aggregate = {
                'hue_diff': {
                    'mean': round(statistics.mean([b['hue_diff'] for b in all_biases]), 2),
                    'std': round(statistics.stdev([b['hue_diff'] for b in all_biases]) if len(all_biases) > 1 else 0, 2),
                    'min': round(min(b['hue_diff'] for b in all_biases), 2),
                    'max': round(max(b['hue_diff'] for b in all_biases), 2),
                },
                'value_diff': {
                    'mean': round(statistics.mean([b['value_diff'] for b in all_biases]), 2),
                    'std': round(statistics.stdev([b['value_diff'] for b in all_biases]) if len(all_biases) > 1 else 0, 2),
                    'min': round(min(b['value_diff'] for b in all_biases), 2),
                    'max': round(max(b['value_diff'] for b in all_biases), 2),
                },
                'chroma_diff': {
                    'mean': round(statistics.mean([b['chroma_diff'] for b in all_biases]), 2),
                    'std': round(statistics.stdev([b['chroma_diff'] for b in all_biases]) if len(all_biases) > 1 else 0, 2),
                    'min': round(min(b['chroma_diff'] for b in all_biases), 2),
                    'max': round(max(b['chroma_diff'] for b in all_biases), 2),
                },
                'euclidean_distance': {
                    'mean': round(statistics.mean([b['euclidean_distance'] for b in all_biases]), 3),
                    'std': round(statistics.stdev([b['euclidean_distance'] for b in all_biases]) if len(all_biases) > 1 else 0, 3),
                    'min': round(min(b['euclidean_distance'] for b in all_biases), 3),
                    'max': round(max(b['euclidean_distance'] for b in all_biases), 3),
                },
            }
        else:
            aggregate = {}

        # Step 4: Save results
        print("\n5. Saving results...")

        results = {
            'summary': {
                'centore_categories': len(self.centore_categories),
                'categories_with_matches': len([c for c in comparisons.values() if c['xkcd_matches'] > 0]),
                'total_xkcd_matches': sum(c['xkcd_matches'] for c in comparisons.values()),
            },
            'aggregate_bias': aggregate,
            'comparisons': comparisons,
        }

        save_results(results, 'centore_comparison_results.json')

        # Print summary
        print()
        print("=" * 70)
        print("COMPARISON SUMMARY")
        print("=" * 70)
        print(f"  Centore categories: {len(self.centore_categories)}")
        print(f"  Categories with XKCD matches: {results['summary']['categories_with_matches']}")
        print(f"  Total XKCD matches: {results['summary']['total_xkcd_matches']:,}")
        print()

        if aggregate:
            print("  AGGREGATE BIAS (XKCD - Centore):")
            print(f"  ├─ Hue shift:    {aggregate['hue_diff']['mean']:+.2f}° "
                  f"(±{aggregate['hue_diff']['std']:.2f}°)")
            print(f"  ├─ Value shift:  {aggregate['value_diff']['mean']:+.2f} "
                  f"(±{aggregate['value_diff']['std']:.2f})")
            print(f"  ├─ Chroma shift: {aggregate['chroma_diff']['mean']:+.2f} "
                  f"(±{aggregate['chroma_diff']['std']:.2f})")
            print(f"  └─ Mean distance: {aggregate['euclidean_distance']['mean']:.3f} "
                  f"(±{aggregate['euclidean_distance']['std']:.3f})")
            print()

            # Interpret biases
            print("  INTERPRETATION:")
            if abs(aggregate['hue_diff']['mean']) > 5:
                direction = "warmer (toward red/yellow)" if aggregate['hue_diff']['mean'] > 0 else "cooler (toward blue)"
                print(f"  ├─ Systematic hue shift: XKCD colors appear {direction}")
            else:
                print(f"  ├─ Hue: No significant systematic bias")

            if abs(aggregate['value_diff']['mean']) > 0.3:
                direction = "lighter" if aggregate['value_diff']['mean'] > 0 else "darker"
                print(f"  ├─ Value shift: XKCD colors appear {direction} than physical")
            else:
                print(f"  ├─ Value: No significant systematic bias")

            if abs(aggregate['chroma_diff']['mean']) > 1:
                direction = "more saturated" if aggregate['chroma_diff']['mean'] > 0 else "less saturated"
                print(f"  └─ Chroma shift: XKCD colors appear {direction} than physical")
            else:
                print(f"  └─ Chroma: No significant systematic bias")

        print()
        print("=" * 70)

        return results


def main():
    """Run Stage 4 comparison."""
    analyzer = CentoreComparisonAnalyzer()
    analyzer.run_comparison()


if __name__ == "__main__":
    main()
