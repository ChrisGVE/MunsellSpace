//! Deprecated public API functions for semantic overlay matching.
//!
//! These functions are preserved for backward compatibility and will be
//! removed in v2.0.0. Use `ColorClassifier` instead.

use super::types::MunsellSpec;
use super::parsing::parse_munsell_notation;

/// Get the best matching semantic overlay name for a Munsell color.
///
/// # Deprecated
/// Use [`ColorClassifier`](crate::ColorClassifier) for unified color naming.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::{semantic_overlay, parse_munsell_notation};
///
/// // The aqua centroid should match "aqua"
/// let aqua = parse_munsell_notation("7.4BG 6.2/3.4").unwrap();
/// assert_eq!(semantic_overlay(&aqua), Some("aqua"));
/// ```
#[deprecated(
    since = "1.2.0",
    note = "Use ColorClassifier for unified color naming. Access semantic names via ColorDescriptor::semantic_name. This function will be removed in v2.0.0."
)]
pub fn semantic_overlay(color: &MunsellSpec) -> Option<&'static str> {
    let registry = crate::semantic_overlay_data::get_registry();
    registry.best_match(color).map(|o| o.name)
}

/// Get all semantic overlay names that match a Munsell color.
///
/// # Deprecated
/// Use [`ColorClassifier`](crate::ColorClassifier) for unified color naming.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::{matching_overlays, parse_munsell_notation};
///
/// let color = parse_munsell_notation("7.4BG 6.2/3.4").unwrap();
/// let matches = matching_overlays(&color);
/// assert!(matches.contains(&"aqua"));
/// ```
#[deprecated(
    since = "1.2.0",
    note = "Use ColorClassifier for unified color naming. Access semantic matches via ColorDescriptor::semantic_name and semantic_alternates. This function will be removed in v2.0.0."
)]
pub fn matching_overlays(color: &MunsellSpec) -> Vec<&'static str> {
    let registry = crate::semantic_overlay_data::get_registry();
    registry.matching_overlays(color)
        .into_iter()
        .map(|o| o.name)
        .collect()
}

/// Get all matching overlay names ranked by distance to centroid.
///
/// # Deprecated
/// Use [`ColorClassifier`](crate::ColorClassifier) for unified color naming.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::{matching_overlays_ranked, parse_munsell_notation};
///
/// let color = parse_munsell_notation("6.7YR 6.1/3.4").unwrap();
/// let ranked = matching_overlays_ranked(&color);
/// if !ranked.is_empty() {
///     let (best_name, distance) = ranked[0];
///     println!("Best match: {} (distance: {:.2})", best_name, distance);
/// }
/// ```
#[deprecated(
    since = "1.2.0",
    note = "Use ColorClassifier for unified color naming. Access ranked matches via ColorDescriptor::nearest_semantic_descriptor(). This function will be removed in v2.0.0."
)]
pub fn matching_overlays_ranked(color: &MunsellSpec) -> Vec<(&'static str, f64)> {
    let registry = crate::semantic_overlay_data::get_registry();
    registry.matching_overlays_ranked(color)
        .into_iter()
        .map(|(o, d)| (o.name, d))
        .collect()
}

/// Check if a Munsell color matches a specific overlay by name.
///
/// # Deprecated
/// Use [`ColorClassifier`](crate::ColorClassifier) for unified color naming.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::{matches_overlay, parse_munsell_notation};
///
/// let color = parse_munsell_notation("7.4BG 6.2/3.4").unwrap();
/// assert!(matches_overlay(&color, "aqua"));
/// assert!(matches_overlay(&color, "AQUA")); // Case-insensitive
/// ```
#[deprecated(
    since = "1.2.0",
    note = "Use ColorClassifier for unified color naming. Check semantic matches via ColorDescriptor. This function will be removed in v2.0.0."
)]
pub fn matches_overlay(color: &MunsellSpec, overlay_name: &str) -> bool {
    let registry = crate::semantic_overlay_data::get_registry();
    registry.matches(color, overlay_name)
}

/// Find the closest overlay by centroid distance.
///
/// # Deprecated
/// Use [`ColorClassifier`](crate::ColorClassifier) for unified color naming.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::{closest_overlay, MunsellSpec};
///
/// let gray = MunsellSpec::neutral(5.0);
/// if let Some((name, distance)) = closest_overlay(&gray) {
///     println!("Closest color name: {} (distance: {:.2})", name, distance);
/// }
/// ```
#[deprecated(
    since = "1.2.0",
    note = "Use ColorClassifier for unified color naming. Access nearest overlay via ColorDescriptor::nearest_semantic. This function will be removed in v2.0.0."
)]
pub fn closest_overlay(color: &MunsellSpec) -> Option<(&'static str, f64)> {
    let registry = crate::semantic_overlay_data::get_registry();
    registry.closest_overlay(color).map(|(o, d)| (o.name, d))
}

/// Get a semantic overlay name from a Munsell notation string.
///
/// # Deprecated
/// Use [`ColorClassifier::classify_munsell()`](crate::ColorClassifier) instead.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::semantic_overlay_from_notation;
///
/// assert_eq!(semantic_overlay_from_notation("7.4BG 6.2/3.4"), Some("aqua"));
/// assert_eq!(semantic_overlay_from_notation("invalid"), None);
/// ```
#[deprecated(
    since = "1.2.0",
    note = "Use ColorClassifier::classify_munsell() for unified color naming. This function will be removed in v2.0.0."
)]
#[allow(deprecated)]
pub fn semantic_overlay_from_notation(notation: &str) -> Option<&'static str> {
    let spec = parse_munsell_notation(notation)?;
    semantic_overlay(&spec)
}
