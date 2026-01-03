#!/usr/bin/env python3
"""
Unit tests for screen_polyhedra_thresholds.py

Tests polyhedra construction with confidence thresholds.
"""

import json
import unittest
from pathlib import Path
from screen_polyhedra_thresholds import (
    load_family_assignments,
    group_by_family,
    build_polyhedron,
    compute_centroid,
    THRESHOLDS,
)

SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent / "datasets"
OUTPUT_DIR = DATASETS_DIR / "screen_polyhedra"


class TestScreenPolyhedraThresholds(unittest.TestCase):
    """Test screen color polyhedra construction."""

    def test_output_directories_exist(self):
        """Test that output directories were created for all thresholds."""
        for threshold in THRESHOLDS:
            threshold_dir = OUTPUT_DIR / f"threshold_{threshold}"
            self.assertTrue(
                threshold_dir.exists(),
                f"Directory for threshold {threshold} should exist"
            )

    def test_summary_files_exist(self):
        """Test that summary JSON files were created for all thresholds."""
        for threshold in THRESHOLDS:
            summary_path = OUTPUT_DIR / f"threshold_{threshold}_summary.json"
            self.assertTrue(
                summary_path.exists(),
                f"Summary file for threshold {threshold} should exist"
            )

            # Verify it's valid JSON
            with open(summary_path) as f:
                summary = json.load(f)

            self.assertEqual(summary["threshold"], threshold)
            self.assertIn("total_families", summary)
            self.assertIn("total_samples", summary)
            self.assertIn("families", summary)

    def test_comparison_report_exists(self):
        """Test that the threshold comparison report was created."""
        report_path = OUTPUT_DIR / "threshold_comparison.md"
        self.assertTrue(report_path.exists(), "Comparison report should exist")

        # Verify it has expected sections
        with open(report_path) as f:
            content = f.read()

        self.assertIn("Overall Statistics by Threshold", content)
        self.assertIn("Family Coverage Across Thresholds", content)
        self.assertIn("Recommendations", content)
        self.assertIn("Trade-off Analysis", content)

    def test_threshold_decreasing_samples(self):
        """Test that higher thresholds have fewer samples (expected behavior)."""
        sample_counts = []

        for threshold in THRESHOLDS:
            summary_path = OUTPUT_DIR / f"threshold_{threshold}_summary.json"
            with open(summary_path) as f:
                summary = json.load(f)
            sample_counts.append(summary["total_samples"])

        # Should generally decrease (with possible exceptions)
        self.assertGreater(
            sample_counts[0], sample_counts[-1],
            "Lowest threshold should have more samples than highest"
        )

    def test_threshold_increasing_confidence(self):
        """Test that higher thresholds have higher average confidence."""
        avg_confidences = []

        for threshold in THRESHOLDS:
            summary_path = OUTPUT_DIR / f"threshold_{threshold}_summary.json"
            with open(summary_path) as f:
                summary = json.load(f)
            avg_confidences.append(summary["avg_confidence"])

        # Should strictly increase
        for i in range(len(avg_confidences) - 1):
            self.assertGreater(
                avg_confidences[i + 1], avg_confidences[i],
                f"Confidence should increase from threshold {THRESHOLDS[i]} to {THRESHOLDS[i+1]}"
            )

    def test_polyhedra_structure(self):
        """Test that polyhedra JSON files have correct structure."""
        # Test with threshold 0.6 which should have most families
        threshold_dir = OUTPUT_DIR / "threshold_0.6"

        # Find a polyhedron file
        polyhedra_files = list(threshold_dir.glob("*_polyhedron.json"))
        self.assertGreater(len(polyhedra_files), 0, "Should have at least one polyhedron")

        # Test first polyhedron
        with open(polyhedra_files[0]) as f:
            poly = json.load(f)

        # Verify required fields
        required_fields = [
            "family", "vertices", "faces", "centroid",
            "volume", "surface_area", "sample_count", "point_count",
            "vertex_count", "face_count",
            "avg_confidence", "avg_similarity"
        ]

        for field in required_fields:
            self.assertIn(field, poly, f"Polyhedron should have '{field}' field")

        # Verify data types and ranges
        self.assertIsInstance(poly["vertices"], list)
        self.assertIsInstance(poly["faces"], list)
        self.assertIsInstance(poly["centroid"], list)
        self.assertEqual(len(poly["centroid"]), 3, "Centroid should be 3D")
        self.assertGreater(poly["volume"], 0, "Volume should be positive")
        self.assertGreater(poly["sample_count"], 0, "Should have samples")
        self.assertGreaterEqual(poly["avg_confidence"], 0.6, "Confidence should be >= threshold")

    def test_compute_centroid(self):
        """Test centroid computation."""
        points = [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        ]

        centroid = compute_centroid(points)
        self.assertEqual(len(centroid), 3)
        self.assertAlmostEqual(centroid[0], 0.25, places=5)
        self.assertAlmostEqual(centroid[1], 0.25, places=5)
        self.assertAlmostEqual(centroid[2], 0.25, places=5)

    def test_load_family_assignments(self):
        """Test loading family assignments with threshold filtering."""
        # Test with threshold 0.7
        colors, confidence_stats = load_family_assignments(0.7)

        # Should have loaded some colors
        self.assertGreater(len(colors), 0, "Should load colors")

        # All colors should meet threshold
        for color in colors:
            self.assertGreaterEqual(
                color["confidence"], 0.7,
                "All loaded colors should meet threshold"
            )

        # Should have confidence stats
        self.assertGreater(len(confidence_stats), 0, "Should have stats for families")

    def test_group_by_family(self):
        """Test grouping colors by family."""
        # Load some test data
        colors, _ = load_family_assignments(0.7)

        family_points, family_stats = group_by_family(colors)

        # Should have some families
        self.assertGreater(len(family_points), 0, "Should have families")

        # Each family should have points and stats
        for family, points in family_points.items():
            self.assertGreater(len(points), 0, f"Family {family} should have points")
            self.assertIn(family, family_stats, f"Should have stats for {family}")

            stats = family_stats[family]
            self.assertIn("confidences", stats)
            self.assertIn("similarities", stats)
            self.assertIn("sample_count", stats)

    def test_build_polyhedron_insufficient_points(self):
        """Test that polyhedron returns None with < 4 points."""
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]  # Only 3 points
        stats = {
            "sample_count": 3,
            "confidences": [0.7, 0.8, 0.9],
            "similarities": [0.9, 0.9, 0.9]
        }

        poly = build_polyhedron("test", points, stats)
        self.assertIsNone(poly, "Should return None with < 4 points")

    def test_build_polyhedron_valid(self):
        """Test building a valid polyhedron."""
        # Simple tetrahedron
        points = [
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        ]
        stats = {
            "sample_count": 4,
            "confidences": [0.7, 0.8, 0.9, 0.85],
            "similarities": [0.9, 0.9, 0.9, 0.9]
        }

        poly = build_polyhedron("test", points, stats)

        self.assertIsNotNone(poly, "Should create polyhedron")
        self.assertEqual(poly.family, "test")
        self.assertEqual(poly.sample_count, 4)
        self.assertEqual(poly.point_count, 4)
        self.assertGreater(poly.volume, 0, "Volume should be positive")
        # Expected: (0.7 + 0.8 + 0.9 + 0.85) / 4 = 3.25 / 4 = 0.8125
        self.assertAlmostEqual(poly.avg_confidence, 0.8125, places=5)

    def test_family_coverage_decreases(self):
        """Test that family coverage decreases with higher thresholds."""
        family_counts = []

        for threshold in THRESHOLDS:
            summary_path = OUTPUT_DIR / f"threshold_{threshold}_summary.json"
            with open(summary_path) as f:
                summary = json.load(f)
            family_counts.append(summary["total_families"])

        # Should generally decrease
        self.assertGreater(
            family_counts[0], family_counts[-1],
            "Lowest threshold should have more families than highest"
        )


if __name__ == "__main__":
    unittest.main()
