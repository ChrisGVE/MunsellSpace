//! Semantic overlay registry using Centore polyhedron data.
//!
//! This module creates the semantic overlay registry from the polyhedron data
//! constants defined in `crate::constants::centore_polyhedra`.
//!
//! The polyhedra are the exact convex hulls from Paul Centore's 2020 paper
//! "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names"
//! (Journal of the International Colour Association, 25, 24-54).

use crate::constants::centore_polyhedra::{get_polyhedron_data, get_sample_count};
use crate::semantic_overlay::{
    SemanticOverlay, SemanticOverlayRegistry, MunsellSpec, centroids,
};

/// Create a semantic overlay from Centore polyhedron data.
fn create_centore_overlay(name: &'static str, centroid: MunsellSpec) -> SemanticOverlay {
    let (vertices, faces) = get_polyhedron_data(name)
        .unwrap_or_else(|| panic!("Unknown overlay: {}", name));

    // Convert slices to vecs of tuples
    let vertices_vec: Vec<(f64, f64, f64)> = vertices.to_vec();
    let faces_vec: Vec<(usize, usize, usize)> = faces.to_vec();

    let count = get_sample_count(name);
    SemanticOverlay::new(name, &vertices_vec, &faces_vec, centroid, count)
}

/// Create the complete registry of all 30 semantic overlays.
///
/// This uses the exact convex hull polyhedra from Centore (2020),
/// derived from ~16,000 CAUS fabric samples.
/// Includes both 20 non-basic and 10 basic color names.
pub fn create_overlay_registry() -> SemanticOverlayRegistry {
    let overlays = vec![
        // 20 non-basic colors
        create_centore_overlay("aqua", centroids::aqua()),
        create_centore_overlay("beige", centroids::beige()),
        create_centore_overlay("coral", centroids::coral()),
        create_centore_overlay("fuchsia", centroids::fuchsia()),
        create_centore_overlay("gold", centroids::gold()),
        create_centore_overlay("lavender", centroids::lavender()),
        create_centore_overlay("lilac", centroids::lilac()),
        create_centore_overlay("magenta", centroids::magenta()),
        create_centore_overlay("mauve", centroids::mauve()),
        create_centore_overlay("navy", centroids::navy()),
        create_centore_overlay("peach", centroids::peach()),
        create_centore_overlay("rose", centroids::rose()),
        create_centore_overlay("rust", centroids::rust()),
        create_centore_overlay("sand", centroids::sand()),
        create_centore_overlay("tan", centroids::tan()),
        create_centore_overlay("taupe", centroids::taupe()),
        create_centore_overlay("teal", centroids::teal()),
        create_centore_overlay("turquoise", centroids::turquoise()),
        create_centore_overlay("violet", centroids::violet()),
        create_centore_overlay("wine", centroids::wine()),
        // 10 basic colors
        create_centore_overlay("blue", centroids::blue()),
        create_centore_overlay("brown", centroids::brown()),
        create_centore_overlay("gray", centroids::gray()),
        create_centore_overlay("green", centroids::green()),
        create_centore_overlay("orange", centroids::orange()),
        create_centore_overlay("pink", centroids::pink()),
        create_centore_overlay("purple", centroids::purple()),
        create_centore_overlay("red", centroids::red()),
        create_centore_overlay("white", centroids::white()),
        create_centore_overlay("yellow", centroids::yellow()),
    ];

    SemanticOverlayRegistry::new(overlays)
}

/// Get a lazily-initialized global registry.
///
/// This is the recommended way to access the overlay registry for most uses.
pub fn get_registry() -> &'static SemanticOverlayRegistry {
    use std::sync::OnceLock;
    static REGISTRY: OnceLock<SemanticOverlayRegistry> = OnceLock::new();
    REGISTRY.get_or_init(create_overlay_registry)
}

#[cfg(test)]
#[allow(deprecated)] // Tests verify deprecated functions still work
mod tests {
    use super::*;
    use crate::semantic_overlay::MunsellSpec;

    #[test]
    fn test_create_registry() {
        let registry = create_overlay_registry();
        assert_eq!(registry.len(), 30);
    }

    #[test]
    fn test_polyhedra_have_correct_structure() {
        let registry = create_overlay_registry();

        // Expected vertex and face counts from Centore data
        let expected = [
            // 20 non-basic colors
            ("aqua", 28, 52),
            ("beige", 32, 60),
            ("coral", 34, 64),
            ("fuchsia", 18, 32),
            ("gold", 47, 90),
            ("lavender", 15, 26),
            ("lilac", 20, 36),
            ("magenta", 7, 10),
            ("mauve", 44, 84),
            ("navy", 24, 44),
            ("peach", 28, 52),
            ("rose", 51, 98),
            ("rust", 24, 44),
            ("sand", 24, 44),
            ("tan", 27, 50),
            ("taupe", 23, 42),
            ("teal", 15, 26),
            ("turquoise", 26, 48),
            ("violet", 31, 58),
            ("wine", 21, 38),
            // 10 basic colors
            ("blue", 66, 128),
            ("brown", 33, 62),
            ("gray", 39, 74),
            ("green", 66, 128),
            ("orange", 46, 88),
            ("pink", 55, 106),
            ("purple", 45, 86),
            ("red", 39, 74),
            ("white", 24, 44),
            ("yellow", 35, 66),
        ];

        for (name, expected_vertices, expected_faces) in &expected {
            let overlay = registry.get(name).expect(&format!("Should have {}", name));
            assert_eq!(
                overlay.polyhedron.vertices.len(),
                *expected_vertices,
                "{} should have {} vertices",
                name,
                expected_vertices
            );
            assert_eq!(
                overlay.polyhedron.faces.len(),
                *expected_faces,
                "{} should have {} faces",
                name,
                expected_faces
            );
        }
    }

    #[test]
    fn test_sample_counts() {
        let registry = get_registry();

        // Verify sample counts match Centore (2020) data
        let expected = [
            // 20 non-basic colors
            ("aqua", 119),
            ("beige", 277),
            ("coral", 215),
            ("fuchsia", 46),
            ("gold", 362),
            ("lavender", 47),
            ("lilac", 78),
            ("magenta", 25),
            ("mauve", 181),
            ("navy", 100),
            ("peach", 102),
            ("rose", 467),
            ("rust", 93),
            ("sand", 123),
            ("tan", 129),
            ("taupe", 76),
            ("teal", 43),
            ("turquoise", 121),
            ("violet", 178),
            ("wine", 83),
            // 10 basic colors
            ("blue", 1673),
            ("brown", 536),
            ("gray", 485),
            ("green", 1296),
            ("orange", 378),
            ("pink", 594),
            ("purple", 226),
            ("red", 662),
            ("white", 152),
            ("yellow", 394),
        ];

        for (name, expected_count) in &expected {
            let overlay = registry.get(name).unwrap();
            assert_eq!(
                overlay.sample_count, *expected_count,
                "{} should have {} samples",
                name, expected_count
            );
        }
    }

    #[test]
    fn test_centroid_is_inside_polyhedron() {
        let registry = create_overlay_registry();
        for overlay in registry.all() {
            assert!(
                overlay.contains(&overlay.centroid),
                "Centroid of '{}' should be inside its polyhedron",
                overlay.name
            );
        }
    }

    #[test]
    fn test_get_registry() {
        let registry = get_registry();
        assert_eq!(registry.len(), 30);

        // Should return the same instance
        let registry2 = get_registry();
        assert!(std::ptr::eq(registry, registry2));
    }

    #[test]
    fn test_polyhedra_are_non_degenerate() {
        let registry = create_overlay_registry();

        for overlay in registry.all() {
            let poly = &overlay.polyhedron;

            // Check we have enough vertices for a 3D shape
            assert!(
                poly.vertices.len() >= 4,
                "Overlay '{}' needs at least 4 vertices, has {}",
                overlay.name,
                poly.vertices.len()
            );

            // Check we have faces
            assert!(
                !poly.faces.is_empty(),
                "Overlay '{}' has no faces",
                overlay.name
            );

            // Compute bounding box extent to verify 3D extent
            let xs: Vec<f64> = poly.vertices.iter().map(|v| v.x).collect();
            let ys: Vec<f64> = poly.vertices.iter().map(|v| v.y).collect();
            let zs: Vec<f64> = poly.vertices.iter().map(|v| v.z).collect();

            let x_range = xs.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
                - xs.iter().cloned().fold(f64::INFINITY, f64::min);
            let y_range = ys.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
                - ys.iter().cloned().fold(f64::INFINITY, f64::min);
            let z_range = zs.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
                - zs.iter().cloned().fold(f64::INFINITY, f64::min);

            // All dimensions should have some extent (not flat)
            assert!(
                x_range > 0.1 && y_range > 0.1 && z_range > 0.1,
                "Overlay '{}' appears flat: x={:.2}, y={:.2}, z={:.2}",
                overlay.name,
                x_range,
                y_range,
                z_range
            );

            // Check all face indices are valid
            for face in &poly.faces {
                assert!(
                    face.v0 < poly.vertices.len(),
                    "Face vertex index {} out of bounds for '{}'",
                    face.v0,
                    overlay.name
                );
                assert!(
                    face.v1 < poly.vertices.len(),
                    "Face vertex index {} out of bounds for '{}'",
                    face.v1,
                    overlay.name
                );
                assert!(
                    face.v2 < poly.vertices.len(),
                    "Face vertex index {} out of bounds for '{}'",
                    face.v2,
                    overlay.name
                );
            }
        }
    }

    #[test]
    fn test_no_match_for_distant_color() {
        let registry = get_registry();

        // Pure black (N 0/) is outside all color overlays
        let pure_black = MunsellSpec::neutral(0.0);
        let matches = registry.matching_overlays(&pure_black);
        assert!(matches.is_empty(), "Pure black shouldn't match any overlay");
    }

    #[test]
    fn test_matching_at_centroid() {
        let registry = get_registry();

        // Test that centroids match their own overlays
        let aqua = registry.get("aqua").unwrap();
        assert!(registry.matches(&aqua.centroid, "aqua"));

        let navy = registry.get("navy").unwrap();
        assert!(registry.matches(&navy.centroid, "navy"));
    }

    #[test]
    fn test_known_centroid_overlaps() {
        // Per Centore (2020): "Since many polyhedra overlap, multiple colour names
        // can sometimes be assigned to the same sample. This feature mirrors human usage."
        //
        // This test documents the known overlapping centroids (centroids that fall
        // inside another overlay's polyhedron). These overlaps are EXPECTED and
        // intentional per the research methodology.

        let registry = get_registry();
        let mut centroid_overlap_count = 0;

        for overlay in registry.all() {
            let matches = registry.matching_overlays(&overlay.centroid);
            let other_matches: Vec<_> = matches.iter()
                .filter(|m| m.name != overlay.name)
                .collect();

            if !other_matches.is_empty() {
                centroid_overlap_count += 1;
            }
        }

        // Document: there are overlapping centroids (this is expected per Centore)
        // As of initial implementation, 15 centroids overlap with other polyhedra
        assert!(
            centroid_overlap_count >= 10,
            "Expected significant centroid overlaps per Centore methodology, found {}",
            centroid_overlap_count
        );
    }

    #[test]
    fn test_overlapping_regions_handled_by_distance() {
        // When a color falls in multiple overlays, matching_overlays_ranked() should
        // return them sorted by distance to centroid (most confident match first).
        //
        // Known heavily overlapping region: beige/sand/tan/rose area in YR hues

        let registry = get_registry();

        // Beige centroid is known to be inside multiple overlays
        let beige = registry.get("beige").unwrap();
        let ranked = registry.matching_overlays_ranked(&beige.centroid);

        // Verify beige matches itself first (distance 0)
        assert!(!ranked.is_empty(), "Beige centroid should match at least beige");
        assert_eq!(ranked[0].0.name, "beige", "Beige should be best match for its own centroid");
        assert!(ranked[0].1 < 0.001, "Distance to own centroid should be ~0");

        // If there are multiple matches, verify they're sorted
        if ranked.len() > 1 {
            for i in 1..ranked.len() {
                assert!(
                    ranked[i].1 >= ranked[i-1].1,
                    "Overlaps should be sorted by centroid distance"
                );
            }
        }
    }

    #[test]
    fn test_non_overlapping_regions_exist() {
        // Some overlays have unique regions with no overlap (e.g., navy, teal)
        // This ensures we haven't accidentally made everything overlap

        let registry = get_registry();
        let mut non_overlapping_count = 0;

        for overlay in registry.all() {
            let matches = registry.matching_overlays(&overlay.centroid);
            if matches.len() == 1 {
                non_overlapping_count += 1;
            }
        }

        // At least some centroids should be uniquely inside their own overlay
        assert!(
            non_overlapping_count >= 3,
            "Expected some non-overlapping centroids, found {}",
            non_overlapping_count
        );
    }

    #[test]
    fn test_all_30_colors_in_registry() {
        let registry = get_registry();

        // All 30 colors should be in the registry
        let all_colors = [
            // Non-basic
            "aqua", "beige", "coral", "fuchsia", "gold", "lavender", "lilac",
            "magenta", "mauve", "navy", "peach", "rose", "rust", "sand", "tan",
            "taupe", "teal", "turquoise", "violet", "wine",
            // Basic
            "blue", "brown", "gray", "green", "orange", "pink", "purple", "red",
            "white", "yellow",
        ];

        for name in &all_colors {
            assert!(
                registry.get(name).is_some(),
                "Registry should contain '{}'", name
            );
        }
    }

    #[test]
    fn test_basic_colors_have_larger_sample_counts() {
        // Basic colors generally have more samples than non-basic colors
        // (because they are more commonly used color names)
        let registry = get_registry();

        let basic_total: u32 = ["blue", "brown", "gray", "green", "orange",
                               "pink", "purple", "red", "white", "yellow"]
            .iter()
            .map(|name| registry.get(name).unwrap().sample_count)
            .sum();

        let non_basic_total: u32 = ["aqua", "beige", "coral", "fuchsia", "gold",
                                    "lavender", "lilac", "magenta", "mauve", "navy",
                                    "peach", "rose", "rust", "sand", "tan",
                                    "taupe", "teal", "turquoise", "violet", "wine"]
            .iter()
            .map(|name| registry.get(name).unwrap().sample_count)
            .sum();

        // Basic colors have 6396 samples total, non-basic have 2865
        assert!(
            basic_total > non_basic_total,
            "Basic colors ({}) should have more samples than non-basic ({})",
            basic_total, non_basic_total
        );
    }

    #[test]
    fn test_public_api_functions() {
        use crate::semantic_overlay::{
            semantic_overlay, matching_overlays, matching_overlays_ranked,
            matches_overlay, closest_overlay,
        };

        // Test with aqua centroid (known to be inside aqua)
        let aqua = centroids::aqua();

        // semantic_overlay should return Some("aqua")
        assert_eq!(semantic_overlay(&aqua), Some("aqua"));

        // matching_overlays should include "aqua"
        let matches = matching_overlays(&aqua);
        assert!(matches.iter().any(|name| *name == "aqua"));

        // matching_overlays_ranked first result should be aqua
        let ranked = matching_overlays_ranked(&aqua);
        assert_eq!(ranked[0].0, "aqua");

        // matches_overlay should return true for "aqua"
        assert!(matches_overlay(&aqua, "aqua"));

        // closest_overlay should return (name, distance)
        let (closest_name, _distance) = closest_overlay(&aqua).unwrap();
        assert_eq!(closest_name, "aqua");
    }

    #[test]
    fn test_grey_alias_works() {
        // "grey" should be accepted as an alias for "gray"
        let gray_centroid = centroids::get("gray").unwrap();
        let grey_centroid = centroids::get("grey").unwrap();

        // Should be the same centroid
        assert_eq!(gray_centroid.hue_number, grey_centroid.hue_number);
        assert!((gray_centroid.value - grey_centroid.value).abs() < 0.001);
        assert!((gray_centroid.chroma - grey_centroid.chroma).abs() < 0.001);
    }

    #[test]
    fn test_total_sample_count() {
        // Total samples across all 30 colors should match expected
        let registry = get_registry();

        let total: u32 = registry.all().iter()
            .map(|o| o.sample_count)
            .sum();

        // Non-basic: 2865, Basic: 6396, Total: 9261
        assert_eq!(total, 9261, "Total sample count should be 9261");
    }
}
