#!/usr/bin/env python3
"""
Test script for the Data Service.

Run from scripts/src/:
    python -m data_service.test_service
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_service import DataService, ColorEntry, ColorSource


def test_service():
    """Test the data service."""
    print("=" * 60)
    print("Data Service Test")
    print("=" * 60)

    # Create service
    service = DataService()

    # Print status
    service.print_status()
    print()

    # Test individual sources
    print("Testing Individual Sources")
    print("-" * 40)

    for source_name in ['centore', 'xkcd', 'meodai']:
        if service.source_exists(source_name):
            try:
                source = service.get_source(source_name)
                entries = source.load()
                print(f"  {source_name}: {len(entries)} entries loaded")

                # Show first entry
                if entries:
                    e = entries[0]
                    print(f"    First: {e.name}")
                    if e.munsell:
                        print(f"      Munsell: {e.munsell}")
                    if e.rgb_hex:
                        print(f"      RGB: {e.rgb_hex}")
            except Exception as ex:
                print(f"  {source_name}: ERROR - {ex}")
        else:
            print(f"  {source_name}: Not found")

    print()

    # Test aggregation
    print("Testing Aggregation")
    print("-" * 40)

    agg = service.aggregate('all')
    stats = agg.get_statistics()
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Unique names: {stats['unique_names']}")
    print(f"  With Munsell: {stats['with_munsell']}")
    print(f"  With RGB: {stats['with_rgb']}")
    print(f"  Sources: {list(stats['by_source'].keys())}")

    print()

    # Test surface vs screen
    print("Testing Surface vs Screen Separation")
    print("-" * 40)

    surface = service.surface_colors()
    surface_stats = surface.get_statistics()
    print(f"  Surface sources: {list(surface_stats['by_source'].keys())}")
    print(f"  Surface entries: {surface_stats['total_entries']}")

    screen = service.screen_colors()
    screen_stats = screen.get_statistics()
    print(f"  Screen sources: {list(screen_stats['by_source'].keys())}")
    print(f"  Screen entries: {screen_stats['total_entries']}")

    print()

    # Test calibration subset
    print("Testing Calibration Subset")
    print("-" * 40)

    calib = service.get_calibration_subset()
    calib_stats = calib.get_statistics()
    print(f"  Calibration sources: {list(calib_stats['by_source'].keys())}")
    print(f"  Calibration entries: {calib_stats['total_entries']}")

    # Find entries matching Centore families
    families = service.centore_families()
    family_matches = 0
    for entry in calib.iter_all():
        for family in families:
            if family in entry.name.lower():
                family_matches += 1
                break

    print(f"  Entries containing Centore family names: {family_matches}")

    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == '__main__':
    test_service()
