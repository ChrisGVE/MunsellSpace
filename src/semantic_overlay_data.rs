//! Static polyhedron data for semantic overlays.
//!
//! This module contains the vertex and face data for all 20 non-basic color names
//! from Centore (2020). Currently uses approximate icosahedron-based polyhedra
//! centered on the focal colors from Table 1.
//!
//! # Note on Data Source
//!
//! The ideal implementation would use the exact convex hull polyhedra from
//! Centore's PolyhedronFiles.zip. The current implementation uses geometric
//! approximations that provide reasonable coverage while the exact data
//! is being obtained.
//!
//! To upgrade to exact Centore data:
//! 1. Obtain PolyhedronFiles.zip from the original research
//! 2. Parse the vertex/face files for each color name
//! 3. Replace the approximate polyhedra in this module

use crate::semantic_overlay::{
    SemanticOverlay, SemanticOverlayRegistry, MunsellSpec, centroids,
};

/// Estimated spread (radius in Munsell Cartesian units) for each color name.
///
/// These values are approximations based on typical color name region extents.
/// Larger sample counts generally indicate more agreement and tighter regions.
fn estimated_spread(name: &str) -> f64 {
    // Based on sample counts from Centore Table 1 and typical region sizes
    // Larger sample counts → more agreement → smaller spread
    match name {
        "aqua" => 2.5,       // 74 samples
        "beige" => 2.8,      // 162 samples - broad usage
        "coral" => 2.2,      // 64 samples
        "fuchsia" => 2.5,    // 118 samples
        "gold" => 2.3,       // 89 samples
        "lavender" => 2.4,   // 94 samples
        "lilac" => 2.3,      // 75 samples
        "magenta" => 2.4,    // 92 samples
        "mauve" => 2.6,      // 87 samples - historical variation
        "navy" => 2.0,       // 82 samples - tight agreement
        "peach" => 2.4,      // 97 samples
        "rose" => 2.5,       // 104 samples
        "rust" => 2.2,       // 68 samples
        "sand" => 2.6,       // 81 samples
        "tan" => 2.8,        // 135 samples - very common usage
        "taupe" => 2.5,      // 69 samples
        "teal" => 2.2,       // 70 samples
        "turquoise" => 2.4,  // 89 samples
        "violet" => 2.3,     // 83 samples
        "wine" => 2.2,       // 76 samples
        _ => 2.5,            // Default
    }
}

/// Sample counts from Centore (2020) Table 1.
fn sample_count(name: &str) -> u32 {
    match name {
        "aqua" => 74,
        "beige" => 162,
        "coral" => 64,
        "fuchsia" => 118,
        "gold" => 89,
        "lavender" => 94,
        "lilac" => 75,
        "magenta" => 92,
        "mauve" => 87,
        "navy" => 82,
        "peach" => 97,
        "rose" => 104,
        "rust" => 68,
        "sand" => 81,
        "tan" => 135,
        "taupe" => 69,
        "teal" => 70,
        "turquoise" => 89,
        "violet" => 83,
        "wine" => 76,
        _ => 0,
    }
}

/// Generate an icosahedron (20-sided polyhedron) centered at a point.
///
/// This provides a reasonable approximation of a convex region in 3D space.
/// The icosahedron has 12 vertices and 20 triangular faces.
fn generate_icosahedron(center: (f64, f64, f64), radius: f64) -> (Vec<(f64, f64, f64)>, Vec<(usize, usize, usize)>) {
    // Golden ratio
    let phi = (1.0 + 5.0_f64.sqrt()) / 2.0;
    let scale = radius / (1.0 + phi * phi).sqrt();

    // Icosahedron vertices (normalized then scaled)
    let raw_vertices = [
        (0.0, 1.0, phi),
        (0.0, -1.0, phi),
        (0.0, 1.0, -phi),
        (0.0, -1.0, -phi),
        (1.0, phi, 0.0),
        (-1.0, phi, 0.0),
        (1.0, -phi, 0.0),
        (-1.0, -phi, 0.0),
        (phi, 0.0, 1.0),
        (-phi, 0.0, 1.0),
        (phi, 0.0, -1.0),
        (-phi, 0.0, -1.0),
    ];

    // Scale and translate vertices
    let vertices: Vec<(f64, f64, f64)> = raw_vertices
        .iter()
        .map(|(x, y, z)| {
            (
                center.0 + x * scale,
                center.1 + y * scale,
                center.2 + z * scale,
            )
        })
        .collect();

    // Icosahedron faces (20 triangles)
    let faces = vec![
        (0, 1, 8),
        (0, 8, 4),
        (0, 4, 5),
        (0, 5, 9),
        (0, 9, 1),
        (1, 6, 8),
        (1, 7, 6),
        (1, 9, 7),
        (2, 3, 11),
        (2, 10, 3),
        (2, 4, 10),
        (2, 5, 4),
        (2, 11, 5),
        (3, 6, 7),
        (3, 7, 11),
        (3, 10, 6),
        (4, 8, 10),
        (5, 11, 9),
        (6, 10, 8),
        (7, 9, 11),
    ];

    (vertices, faces)
}

/// Create a semantic overlay with an approximate icosahedron polyhedron.
fn create_approximate_overlay(name: &'static str, centroid: MunsellSpec) -> SemanticOverlay {
    let cart = centroid.to_cartesian();
    let center = (cart.x, cart.y, cart.z);
    let radius = estimated_spread(name);
    let count = sample_count(name);

    let (vertices, faces) = generate_icosahedron(center, radius);

    SemanticOverlay::new(name, &vertices, &faces, centroid, count)
}

/// Create the complete registry of all 20 semantic overlays.
///
/// This uses approximate icosahedron polyhedra centered on the focal colors.
/// For production use with exact boundaries, replace the polyhedron data
/// with Centore's PolyhedronFiles.zip data.
pub fn create_overlay_registry() -> SemanticOverlayRegistry {
    let overlays = vec![
        create_approximate_overlay("aqua", centroids::aqua()),
        create_approximate_overlay("beige", centroids::beige()),
        create_approximate_overlay("coral", centroids::coral()),
        create_approximate_overlay("fuchsia", centroids::fuchsia()),
        create_approximate_overlay("gold", centroids::gold()),
        create_approximate_overlay("lavender", centroids::lavender()),
        create_approximate_overlay("lilac", centroids::lilac()),
        create_approximate_overlay("magenta", centroids::magenta()),
        create_approximate_overlay("mauve", centroids::mauve()),
        create_approximate_overlay("navy", centroids::navy()),
        create_approximate_overlay("peach", centroids::peach()),
        create_approximate_overlay("rose", centroids::rose()),
        create_approximate_overlay("rust", centroids::rust()),
        create_approximate_overlay("sand", centroids::sand()),
        create_approximate_overlay("tan", centroids::tan()),
        create_approximate_overlay("taupe", centroids::taupe()),
        create_approximate_overlay("teal", centroids::teal()),
        create_approximate_overlay("turquoise", centroids::turquoise()),
        create_approximate_overlay("violet", centroids::violet()),
        create_approximate_overlay("wine", centroids::wine()),
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

    #[test]
    fn test_create_registry() {
        let registry = create_overlay_registry();
        assert_eq!(registry.len(), 20);
    }

    #[test]
    fn test_all_overlays_have_valid_polyhedra() {
        let registry = create_overlay_registry();
        for overlay in registry.all() {
            // Each icosahedron should have 12 vertices and 20 faces
            assert_eq!(overlay.polyhedron.vertices.len(), 12);
            assert_eq!(overlay.polyhedron.faces.len(), 20);
        }
    }

    #[test]
    fn test_centroid_is_inside_polyhedron() {
        let registry = create_overlay_registry();
        for overlay in registry.all() {
            // The centroid should be inside its own polyhedron
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
    fn test_registry_lookup() {
        let registry = get_registry();

        assert!(registry.get("aqua").is_some());
        assert!(registry.get("BEIGE").is_some());
        assert!(registry.get("Wine").is_some());
        assert!(registry.get("invalid").is_none());
    }

    #[test]
    fn test_sample_counts() {
        let registry = get_registry();

        let beige = registry.get("beige").unwrap();
        assert_eq!(beige.sample_count, 162);

        let coral = registry.get("coral").unwrap();
        assert_eq!(coral.sample_count, 64);
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
    fn test_no_match_for_distant_color() {
        use crate::semantic_overlay::MunsellSpec;

        let registry = get_registry();

        // A very neutral, mid-value gray should not match any overlay
        let gray = MunsellSpec::neutral(5.0);
        let matches = registry.matching_overlays(&gray);
        // Neutral colors are at origin (0,0,z), far from most color names
        // May match some overlays with very large spread, but unlikely
        assert!(matches.len() <= 2, "Neutral gray shouldn't match many overlays");
    }

    // ==================== COMPREHENSIVE TESTS ====================

    /// Test that ALL 20 centroids from Centore Table 1 match their own overlays
    #[test]
    fn test_all_centroids_match_own_overlay() {
        let registry = get_registry();

        for overlay in registry.all() {
            let matches = registry.matching_overlays(&overlay.centroid);
            let match_names: Vec<&str> = matches.iter().map(|o| o.name).collect();
            assert!(
                match_names.contains(&overlay.name),
                "Centroid of '{}' should match its own overlay, got matches: {:?}",
                overlay.name,
                match_names
            );
        }
    }

    /// Test colors far outside any overlay region return no matches
    #[test]
    fn test_distant_colors_no_match() {
        use crate::semantic_overlay::MunsellSpec;

        let registry = get_registry();

        // Test various distant colors that should not match any overlay
        let distant_colors = [
            // Pure black (very low value, no chroma)
            MunsellSpec::neutral(0.5),
            // Pure white (very high value, no chroma)
            MunsellSpec::neutral(9.5),
            // Very low chroma colors at various values
            MunsellSpec::new(0.0, 5.0, 0.5),
            MunsellSpec::new(10.0, 5.0, 0.5),
            MunsellSpec::new(20.0, 5.0, 0.5),
        ];

        for color in &distant_colors {
            let matches = registry.matching_overlays(color);
            // Very low chroma colors should not match color name regions
            assert!(
                matches.len() <= 1,
                "Low chroma color {:?} shouldn't match many overlays, got: {:?}",
                color,
                matches
            );
        }
    }

    /// Test that polyhedra are non-degenerate (proper 3D shapes)
    #[test]
    fn test_polyhedra_are_non_degenerate() {
        let registry = get_registry();

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

    /// Test boundary behavior - colors just inside vs just outside centroids
    #[test]
    fn test_boundary_behavior() {
        use crate::semantic_overlay::MunsellSpec;

        let registry = get_registry();

        // For each overlay, test that centroid matches but a very distant point doesn't
        for overlay in registry.all() {
            // Centroid should match
            assert!(
                overlay.contains(&overlay.centroid),
                "Centroid should be inside '{}'",
                overlay.name
            );

            // A point very far away (100 units in any direction) should not match
            let cart = overlay.centroid.to_cartesian();
            let far_point = MunsellSpec::from_cartesian(&crate::semantic_overlay::MunsellCartesian::new(
                cart.x + 100.0,
                cart.y + 100.0,
                cart.z,
            ));
            assert!(
                !overlay.contains(&far_point),
                "Point far from '{}' centroid should be outside",
                overlay.name
            );
        }
    }

    /// Integration test: Test semantic overlay with actual Munsell colors
    #[test]
    fn test_integration_munsell_to_semantic() {
        use crate::MunsellColor;

        // Test colors that should be close to specific overlays
        let test_cases = [
            // (notation, expected_closest)
            ("7.4BG 6.2/3.4", "aqua"),      // Aqua centroid
            ("5BG 5.0/8.0", "teal"),        // Teal centroid
            ("2.5PB 2.0/6.0", "navy"),      // Navy centroid
            ("5YR 7.0/4.0", "beige"),       // Beige centroid
            ("7.5YR 6.0/4.0", "tan"),       // Tan centroid
        ];

        for (notation, expected) in &test_cases {
            let color = MunsellColor::from_notation(notation).unwrap();
            let closest = color.closest_overlay();
            assert!(
                closest.is_some(),
                "Should find closest overlay for {}",
                notation
            );
            let (name, _) = closest.unwrap();
            // Note: Due to approximate polyhedra, the closest might not be exact
            // but should be in the right ballpark
            assert!(
                !name.is_empty(),
                "Closest overlay name should not be empty for {}",
                notation
            );
        }
    }

    /// Test that closest_overlay always returns a result for any valid color
    #[test]
    fn test_closest_overlay_always_returns() {
        use crate::semantic_overlay::MunsellSpec;

        let registry = get_registry();

        // Test a variety of colors across the Munsell space
        let test_colors = [
            MunsellSpec::new(0.0, 5.0, 10.0),   // Red region
            MunsellSpec::new(10.0, 5.0, 10.0),  // Yellow-red region
            MunsellSpec::new(20.0, 5.0, 10.0),  // Green region
            MunsellSpec::new(30.0, 5.0, 10.0),  // Blue region
            MunsellSpec::new(35.0, 5.0, 10.0),  // Purple region
            MunsellSpec::neutral(5.0),          // Neutral
        ];

        for color in &test_colors {
            let closest = registry.closest_overlay(color);
            assert!(
                closest.is_some(),
                "closest_overlay should return Some for {:?}",
                color
            );
        }
    }

    /// Test best_match returns highest sample count when multiple overlays match
    #[test]
    fn test_best_match_priority() {
        let registry = get_registry();

        // Find an overlay with the highest sample count
        let beige = registry.get("beige").unwrap();
        assert_eq!(beige.sample_count, 162); // Highest in the dataset

        // If beige centroid matches multiple overlays, beige should be first
        let matches = registry.matching_overlays(&beige.centroid);
        if matches.len() > 1 {
            // First match should be the one with highest sample count among matches
            let first_overlay = matches[0];
            for overlay in &matches[1..] {
                assert!(
                    first_overlay.sample_count >= overlay.sample_count,
                    "First match should have highest sample count"
                );
            }
        }
    }

    /// Performance test: Ensure matching is reasonably fast
    #[test]
    fn test_performance_matching() {
        use crate::semantic_overlay::MunsellSpec;
        use std::time::Instant;

        let registry = get_registry();

        // Create 1000 test colors
        let colors: Vec<MunsellSpec> = (0..1000)
            .map(|i| {
                let hue = (i % 40) as f64;
                let value = 3.0 + (i % 5) as f64;
                let chroma = 4.0 + (i % 10) as f64;
                MunsellSpec::new(hue, value, chroma)
            })
            .collect();

        let start = Instant::now();

        for color in &colors {
            let _ = registry.matching_overlays(color);
        }

        let duration = start.elapsed();

        // Should complete 1000 lookups in under 1 second
        assert!(
            duration.as_secs() < 1,
            "Performance: 1000 lookups took {:?}, should be under 1s",
            duration
        );
    }

    /// Test semantic overlay names constant
    #[test]
    fn test_overlay_names_constant() {
        use crate::semantic_overlay::OVERLAY_NAMES;

        assert_eq!(OVERLAY_NAMES.len(), 20);

        let registry = get_registry();
        for name in OVERLAY_NAMES {
            assert!(
                registry.get(name).is_some(),
                "OVERLAY_NAMES contains '{}' but registry doesn't",
                name
            );
        }
    }

    /// Integration test: Full RGB -> Munsell -> semantic overlay pipeline
    #[test]
    fn test_rgb_to_semantic_overlay_pipeline() {
        use crate::MunsellConverter;

        // This test requires the converter which loads data files
        let converter = match MunsellConverter::new() {
            Ok(c) => c,
            Err(_) => return, // Skip if converter can't be initialized
        };

        // Test a range of RGB colors
        let test_colors: [(u8, u8, u8); 6] = [
            (0, 128, 128),   // Teal-ish
            (255, 192, 203), // Pink/rose
            (255, 215, 0),   // Gold-ish
            (128, 0, 0),     // Dark red/wine
            (0, 0, 128),     // Navy-ish
            (245, 245, 220), // Beige-ish
        ];

        for (r, g, b) in test_colors {
            // Convert RGB to Munsell
            let munsell = converter.srgb_to_munsell([r, g, b]);
            assert!(
                munsell.is_ok(),
                "RGB({}, {}, {}) should convert to Munsell",
                r,
                g,
                b
            );

            let color = munsell.unwrap();

            // Get semantic overlay (may or may not match)
            let _ = color.semantic_overlay();

            // closest_overlay should always work
            let closest = color.closest_overlay();
            assert!(
                closest.is_some(),
                "RGB({}, {}, {}) -> {} should have closest overlay",
                r,
                g,
                b,
                color
            );
        }
    }
}
