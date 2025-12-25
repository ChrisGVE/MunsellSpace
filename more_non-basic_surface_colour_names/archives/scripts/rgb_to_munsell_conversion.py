#!/usr/bin/env python3
"""
Stage 3: RGB to Munsell Conversion

Converts all validated color names from RGB to Munsell space using the
MunsellSpace Rust library.

Pipeline:
1. Load validated color names from Stage 1
2. Load RGB coordinates from XKCD cache
3. Compute average RGB per color name (multiple responses per name)
4. Run Rust converter via subprocess
5. Parse results and save for Stage 4

Usage:
    python rgb_to_munsell_conversion.py
"""

import csv
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import statistics

from common import save_results, INVESTIGATION_DIR


class RgbToMunsellConverter:
    """Orchestrates RGB to Munsell conversion using the Rust library."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.investigation_dir = INVESTIGATION_DIR
        self.vocab_dir = Path(__file__).parent.parent / "color-vocabularies"

        self.validated_names: Dict = {}
        self.rgb_coordinates: Dict[str, List[List[int]]] = {}
        self.color_hex: Dict[str, str] = {}  # For colors with hex only

    def load_validated_names(self) -> int:
        """Load validated color names from Stage 1."""
        path = self.investigation_dir / "validated_color_names.json"
        if not path.exists():
            raise FileNotFoundError(f"Validated names not found: {path}")

        with open(path) as f:
            self.validated_names = json.load(f)

        print(f"  Loaded {len(self.validated_names):,} validated names")
        return len(self.validated_names)

    def load_rgb_coordinates(self) -> int:
        """Load RGB coordinates from all available sources."""
        # Primary source: XKCD coordinates cache (175K names with RGB lists)
        # Note: this file is in the parent investigation folder
        xkcd_cache_path = Path(__file__).parent.parent / "investigation" / "xkcd_coordinates_cache.json"
        if xkcd_cache_path.exists():
            with open(xkcd_cache_path) as f:
                self.rgb_coordinates = json.load(f)
            print(f"  Loaded {len(self.rgb_coordinates):,} from XKCD cache")

        # Secondary sources: vocabulary CSVs (for hex values)
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
                        hex_val = row[1].strip().lstrip('#')
                        if name not in self.color_hex and len(hex_val) == 6:
                            self.color_hex[name] = hex_val
                            csv_count += 1

        print(f"  Loaded {csv_count:,} hex values from CSVs")
        return len(self.rgb_coordinates) + len(self.color_hex)

    def hex_to_rgb(self, hex_str: str) -> Tuple[int, int, int]:
        """Convert hex string to RGB tuple."""
        hex_str = hex_str.lstrip('#')
        return (
            int(hex_str[0:2], 16),
            int(hex_str[2:4], 16),
            int(hex_str[4:6], 16)
        )

    def compute_average_rgb(self, rgb_list: List[List[int]]) -> Tuple[int, int, int]:
        """Compute average RGB from list of RGB values."""
        if not rgb_list:
            return (128, 128, 128)  # Default gray

        if len(rgb_list) == 1:
            return tuple(rgb_list[0])

        # Compute mean for each channel
        r_vals = [rgb[0] for rgb in rgb_list]
        g_vals = [rgb[1] for rgb in rgb_list]
        b_vals = [rgb[2] for rgb in rgb_list]

        return (
            round(statistics.mean(r_vals)),
            round(statistics.mean(g_vals)),
            round(statistics.mean(b_vals))
        )

    def get_rgb_for_name(self, name: str) -> Optional[Tuple[int, int, int]]:
        """Get RGB values for a color name."""
        name_lower = name.lower().strip()

        # Check XKCD cache first (has multiple samples)
        if name_lower in self.rgb_coordinates:
            rgb_list = self.rgb_coordinates[name_lower]
            return self.compute_average_rgb(rgb_list)

        # Fall back to hex values
        if name_lower in self.color_hex:
            return self.hex_to_rgb(self.color_hex[name_lower])

        return None

    def prepare_input_csv(self) -> Tuple[str, int, int]:
        """Prepare CSV input for Rust converter.

        Returns:
            Tuple of (csv_path, processed_count, missing_count)
        """
        # Create temporary CSV file
        tmp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False,
            encoding='utf-8'
        )

        processed = 0
        missing = 0
        missing_names = []

        tmp_file.write("name,r,g,b\n")

        for name in self.validated_names:
            rgb = self.get_rgb_for_name(name)
            if rgb is None:
                missing += 1
                if missing <= 20:
                    missing_names.append(name)
                continue

            r, g, b = rgb
            # Escape name if it contains commas
            if ',' in name:
                name_escaped = f'"{name}"'
            else:
                name_escaped = name

            tmp_file.write(f"{name_escaped},{r},{g},{b}\n")
            processed += 1

        tmp_file.close()

        if missing_names:
            print(f"  WARNING: {missing} names have no RGB coordinates")
            print(f"  Examples: {missing_names[:5]}")

        return tmp_file.name, processed, missing

    def run_rust_converter(self, input_path: str) -> str:
        """Run the Rust RGB to Munsell converter.

        Returns:
            Path to output CSV
        """
        output_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False,
            encoding='utf-8'
        )
        output_file.close()

        # Run cargo command
        cmd = [
            'cargo', 'run', '--release',
            '--example', 'simple_rgb_to_munsell'
        ]

        print(f"  Running: {' '.join(cmd)}")

        with open(input_path, 'r') as stdin_file:
            with open(output_file.name, 'w') as stdout_file:
                result = subprocess.run(
                    cmd,
                    stdin=stdin_file,
                    stdout=stdout_file,
                    stderr=subprocess.PIPE,
                    cwd=self.project_root,
                    text=True
                )

        if result.returncode != 0:
            print(f"  ERROR: Conversion failed")
            print(f"  stderr: {result.stderr}")
            raise RuntimeError("Rust converter failed")

        # Count any errors in stderr
        if result.stderr:
            error_lines = [l for l in result.stderr.split('\n') if l.strip()]
            if error_lines:
                print(f"  Converter warnings/errors: {len(error_lines)}")
                for line in error_lines[:5]:
                    print(f"    {line}")

        return output_file.name

    def parse_output(self, output_path: str) -> Dict:
        """Parse Rust converter output into structured data."""
        results = {}

        with open(output_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name']
                results[name] = {
                    'rgb': {
                        'r': int(row['r']),
                        'g': int(row['g']),
                        'b': int(row['b'])
                    },
                    'munsell': {
                        'notation': row['munsell_notation'],
                        'hue_str': row['hue_str'],
                        'hue_num': float(row['hue_num']),
                        'value': float(row['value']),
                        'chroma': float(row['chroma'])
                    },
                    'cartesian': {
                        'x': float(row['x']),
                        'y': float(row['y']),
                        'z': float(row['z'])
                    }
                }

        return results

    def run_conversion(self) -> Dict:
        """Run the complete Stage 3 conversion pipeline."""
        print("=" * 70)
        print("STAGE 3: RGB TO MUNSELL CONVERSION")
        print("=" * 70)
        print()

        # Step 1: Load data
        print("1. Loading validated color names...")
        self.load_validated_names()

        print("\n2. Loading RGB coordinates...")
        self.load_rgb_coordinates()

        # Step 2: Prepare input
        print("\n3. Preparing input for Rust converter...")
        input_path, processed, missing = self.prepare_input_csv()
        print(f"  Prepared {processed:,} colors for conversion")
        print(f"  Missing RGB: {missing:,}")

        # Step 3: Run Rust converter
        print("\n4. Running Rust RGB→Munsell converter...")
        output_path = self.run_rust_converter(input_path)
        print(f"  Conversion complete")

        # Step 4: Parse results
        print("\n5. Parsing results...")
        munsell_data = self.parse_output(output_path)
        print(f"  Parsed {len(munsell_data):,} Munsell conversions")

        # Step 5: Compute statistics
        print("\n6. Computing statistics...")
        stats = self._compute_statistics(munsell_data)

        # Step 6: Save results
        print("\n7. Saving results...")
        results = {
            'total_validated': len(self.validated_names),
            'converted': len(munsell_data),
            'missing_rgb': missing,
            'statistics': stats,
            'colors': munsell_data
        }

        save_results(results, 'munsell_conversions.json')

        # Also save a compact version without the full color data
        summary = {
            'total_validated': len(self.validated_names),
            'converted': len(munsell_data),
            'missing_rgb': missing,
            'statistics': stats
        }
        save_results(summary, 'munsell_conversion_summary.json')

        # Clean up temp files
        Path(input_path).unlink()
        Path(output_path).unlink()

        # Print summary
        print()
        print("=" * 70)
        print("CONVERSION SUMMARY")
        print("=" * 70)
        print(f"  Total validated names: {len(self.validated_names):,}")
        print(f"  Successfully converted: {len(munsell_data):,}")
        print(f"  Missing RGB coordinates: {missing:,}")
        print()
        print("  VALUE DISTRIBUTION:")
        for bucket, count in sorted(stats['value_distribution'].items()):
            print(f"    {bucket}: {count:,}")
        print()
        print("  HUE DISTRIBUTION:")
        for hue, count in sorted(stats['hue_distribution'].items(),
                                  key=lambda x: -x[1])[:10]:
            print(f"    {hue}: {count:,}")
        print()
        print(f"  Neutral colors: {stats['neutral_count']:,}")
        print(f"  Chromatic colors: {stats['chromatic_count']:,}")
        print()
        print("=" * 70)

        return results

    def _compute_statistics(self, munsell_data: Dict) -> Dict:
        """Compute statistics about the Munsell conversions."""
        values = []
        chromas = []
        hue_counts = defaultdict(int)
        neutral_count = 0
        chromatic_count = 0

        # Value buckets
        value_buckets = defaultdict(int)

        for name, data in munsell_data.items():
            m = data['munsell']
            values.append(m['value'])
            chromas.append(m['chroma'])

            # Categorize by value
            v = m['value']
            if v < 2:
                value_buckets['0-2 (very dark)'] += 1
            elif v < 4:
                value_buckets['2-4 (dark)'] += 1
            elif v < 6:
                value_buckets['4-6 (medium)'] += 1
            elif v < 8:
                value_buckets['6-8 (light)'] += 1
            else:
                value_buckets['8-10 (very light)'] += 1

            # Count hues
            if m['hue_str'] == 'N':
                neutral_count += 1
            else:
                chromatic_count += 1
                # Extract hue family (e.g., "5R" -> "R")
                hue_str = m['hue_str']
                for family in ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']:
                    if hue_str.endswith(family):
                        hue_counts[family] += 1
                        break

        return {
            'value_mean': round(statistics.mean(values), 2) if values else 0,
            'value_std': round(statistics.stdev(values), 2) if len(values) > 1 else 0,
            'chroma_mean': round(statistics.mean(chromas), 2) if chromas else 0,
            'chroma_std': round(statistics.stdev(chromas), 2) if len(chromas) > 1 else 0,
            'neutral_count': neutral_count,
            'chromatic_count': chromatic_count,
            'value_distribution': dict(value_buckets),
            'hue_distribution': dict(hue_counts)
        }


def main():
    """Run Stage 3 conversion."""
    converter = RgbToMunsellConverter()
    converter.run_conversion()


if __name__ == "__main__":
    main()
