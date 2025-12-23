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

/// Create the complete registry of all 20 semantic overlays.
///
/// This uses the exact convex hull polyhedra from Centore (2020),
/// derived from ~16,000 CAUS fabric samples.
pub fn create_overlay_registry() -> SemanticOverlayRegistry {
    let overlays = vec![
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
mod tests {
    use super::*;
    use crate::semantic_overlay::MunsellSpec;

    #[test]
    fn test_create_registry() {
        let registry = create_overlay_registry();
        assert_eq!(registry.len(), 20);
    }

    #[test]
    fn test_polyhedra_have_correct_structure() {
        let registry = create_overlay_registry();

        // Expected vertex and face counts from Centore data
        let expected = [
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

        // Verify sample counts match Centore (2020) Table 1
        let expected = [
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
        assert_eq!(registry.len(), 20);

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

        // A very neutral, mid-value gray should not match any overlay
        let gray = MunsellSpec::neutral(5.0);
        let matches = registry.matching_overlays(&gray);
        // Neutral colors are at origin (0,0,z), far from most color names
        assert!(matches.is_empty(), "Neutral gray shouldn't match any overlays with real polyhedra");
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
}
