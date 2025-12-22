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
}
