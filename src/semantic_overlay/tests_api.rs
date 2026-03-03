//! Tests for semantic overlay API and registry operations.

use super::*;

#[allow(deprecated)]
use super::deprecated_api::*;

// ========================================================================
// SemanticOverlay Data Structure Tests
// ========================================================================

#[test]
fn test_centroid_functions() {
    for name in &super::OVERLAY_NAMES {
        let centroid = super::centroids::get(name);
        assert!(centroid.is_some(), "Centroid for '{}' should exist", name);
    }

    let aqua = super::centroids::aqua();
    assert!((aqua.value - 6.2).abs() < 0.01);

    let navy = super::centroids::navy();
    assert!((navy.value - 2.1).abs() < 0.01);
}

#[test]
fn test_centroid_get_case_insensitive() {
    assert!(super::centroids::get("AQUA").is_some());
    assert!(super::centroids::get("Aqua").is_some());
    assert!(super::centroids::get("aqua").is_some());
    assert!(super::centroids::get("invalid").is_none());
}

#[test]
fn test_overlay_names_count() {
    assert_eq!(super::OVERLAY_NAMES.len(), 30);
}

#[test]
fn test_semantic_overlay_creation() {
    let vertices = vec![
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.5, 0.866, 0.0),
        (0.5, 0.289, 0.816),
    ];

    let faces = vec![
        (0, 2, 1),
        (0, 1, 3),
        (1, 2, 3),
        (2, 0, 3),
    ];

    let centroid = MunsellSpec::new(2.0, 5.0, 8.0);
    let overlay = SemanticOverlay::new("test", &vertices, &faces, centroid, 100);

    assert_eq!(overlay.name, "test");
    assert_eq!(overlay.sample_count, 100);
}

// ========================================================================
// Public API Tests
// ========================================================================

#[test]
fn test_semantic_overlay_at_centroid() {
    assert_eq!(semantic_overlay(&super::centroids::aqua()), Some("aqua"));
    assert_eq!(semantic_overlay(&super::centroids::navy()), Some("navy"));
    assert_eq!(semantic_overlay(&super::centroids::beige()), Some("beige"));
}

#[test]
fn test_matching_overlays_at_centroid() {
    let aqua = super::centroids::aqua();
    let matches = matching_overlays(&aqua);
    assert!(matches.contains(&"aqua"));
}

#[test]
fn test_matches_overlay_function() {
    let navy = super::centroids::navy();
    assert!(matches_overlay(&navy, "navy"));
    assert!(matches_overlay(&navy, "NAVY"));
    assert!(matches_overlay(&navy, "Navy"));
}

#[test]
fn test_closest_overlay_function() {
    let gray = MunsellSpec::neutral(5.0);
    let result = closest_overlay(&gray);
    assert!(result.is_some());
    let (name, distance) = result.unwrap();
    assert!(!name.is_empty());
    assert!(distance > 0.0);
}

#[test]
fn test_semantic_overlay_from_notation_function() {
    assert_eq!(semantic_overlay_from_notation("7.4BG 6.2/3.4"), Some("aqua"));
    assert_eq!(semantic_overlay_from_notation("invalid"), None);
}

#[test]
fn test_registry_basic_operations() {
    let vertices = vec![
        (-1.0, -1.0, -1.0),
        (1.0, -1.0, -1.0),
        (1.0, 1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, -1.0, 1.0),
        (1.0, -1.0, 1.0),
        (1.0, 1.0, 1.0),
        (-1.0, 1.0, 1.0),
    ];

    let faces = vec![
        (0, 2, 1), (0, 3, 2),
        (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4),
        (2, 3, 7), (2, 7, 6),
        (0, 4, 7), (0, 7, 3),
        (1, 2, 6), (1, 6, 5),
    ];

    let overlay1 = SemanticOverlay::new(
        "test1",
        &vertices,
        &faces,
        MunsellSpec::new(0.0, 0.0, 0.0),
        50,
    );

    let registry = SemanticOverlayRegistry::new(vec![overlay1]);

    assert_eq!(registry.len(), 1);
    assert!(!registry.is_empty());
    assert!(registry.get("test1").is_some());
    assert!(registry.get("TEST1").is_some());
    assert!(registry.get("nonexistent").is_none());
}

// ========================================================================
// Ranked Overlay Matching Tests
// ========================================================================

#[test]
fn test_matching_overlays_ranked_single_match() {
    let navy = super::centroids::navy();
    let ranked = matching_overlays_ranked(&navy);

    assert!(!ranked.is_empty(), "Navy centroid should match at least navy");
    assert_eq!(ranked[0].0, "navy", "Best match should be navy");
    assert!(ranked[0].1 < 0.001, "Distance to own centroid should be ~0");
}

#[test]
fn test_matching_overlays_ranked_is_sorted() {
    let beige = super::centroids::beige();
    let ranked = matching_overlays_ranked(&beige);

    if ranked.len() > 1 {
        for i in 1..ranked.len() {
            assert!(
                ranked[i].1 >= ranked[i-1].1,
                "Ranked overlays should be sorted by distance: {} (dist {}) should not come after {} (dist {})",
                ranked[i].0, ranked[i].1,
                ranked[i-1].0, ranked[i-1].1
            );
        }
    }
}

#[test]
fn test_matching_overlays_ranked_empty_for_black() {
    let pure_black = MunsellSpec::neutral(0.0);
    let ranked = matching_overlays_ranked(&pure_black);
    assert!(ranked.is_empty(), "Pure black should not match any overlays");
}

#[test]
fn test_matching_overlays_ranked_public_api() {
    let aqua = super::centroids::aqua();
    let ranked = matching_overlays_ranked(&aqua);

    assert!(!ranked.is_empty());
    let (name, distance) = ranked[0];
    assert_eq!(name, "aqua");
    assert!(distance < 0.001);
}

#[test]
fn test_matching_overlays_ranked_consistency_with_best_match() {
    for name in &super::OVERLAY_NAMES {
        let centroid = super::centroids::get(name).unwrap();
        let ranked = matching_overlays_ranked(&centroid);
        let best = semantic_overlay(&centroid);

        if !ranked.is_empty() && best.is_some() {
            assert_eq!(
                ranked[0].0, best.unwrap(),
                "First ranked should equal best_match for {}",
                name
            );
        }
    }
}
