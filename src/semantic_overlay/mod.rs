//! Semantic overlay functionality for non-basic color names.
//!
//! This module implements semantic color naming based on Paul Centore's 2020 paper
//! "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names"
//! (Journal of the American Institute for Conservation, 25:3, 37-56).
//!
//! The methodology uses convex polyhedra in 3D Munsell space to define color name regions,
//! with point-in-polyhedron tests for membership determination.
//!
//! # Quick Start
//!
//! ```rust
//! use munsellspace::semantic_overlay::{semantic_overlay, matching_overlays, parse_munsell_notation};
//!
//! // Parse a Munsell color and find its semantic name
//! if let Some(spec) = parse_munsell_notation("7.4BG 6.2/3.4") {
//!     if let Some(name) = semantic_overlay(&spec) {
//!         println!("This color is: {}", name);  // "aqua"
//!     }
//! }
//! ```
//!
//! # Available Functions
//!
//! - [`semantic_overlay`]: Get the best matching semantic name for a color
//! - [`matching_overlays`]: Get all semantic names that match a color
//! - [`matching_overlays_ranked`]: Get all matches ranked by centroid distance (confidence)
//! - [`matches_overlay`]: Check if a color matches a specific overlay name
//! - [`closest_overlay`]: Find the nearest overlay by centroid distance
//!
//! # The 30 Color Names
//!
//! Centore defined boundaries for 30 color names (20 non-basic + 10 basic):
//! aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy,
//! peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine,
//! blue, brown, gray, green, orange, pink, purple, red, white, yellow

mod types;
mod parsing;
mod registry;
pub mod centroids;
mod polyhedron;
mod deprecated_api;

#[cfg(test)]
mod tests_polyhedron;
#[cfg(test)]
mod tests_api;

// Re-export types
pub use types::{MunsellCartesian, MunsellSpec};

// Re-export parsing
pub use parsing::{parse_hue_to_number, hue_number_to_string, parse_munsell_notation};

// Re-export overlay structures
pub use registry::{SemanticOverlay, SemanticOverlayRegistry};

// Re-export polyhedron types and functions
pub use polyhedron::{ConvexPolyhedron, TriFace, point_in_polyhedron, munsell_in_polyhedron};

// Re-export deprecated API functions
#[allow(deprecated)]
pub use deprecated_api::{
    semantic_overlay, matching_overlays, matching_overlays_ranked,
    matches_overlay, closest_overlay, semantic_overlay_from_notation,
};

/// Munsell hue families in clockwise order starting from R.
/// Each family spans 4 hue steps (0-10 within family maps to 0-4 in absolute numbering).
pub const HUE_FAMILIES: [&str; 10] = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];

/// All 30 color names from Centore (2020): 20 non-basic + 10 basic.
pub const OVERLAY_NAMES: [&str; 30] = [
    // 20 non-basic color names
    "aqua", "beige", "coral", "fuchsia", "gold",
    "lavender", "lilac", "magenta", "mauve", "navy",
    "peach", "rose", "rust", "sand", "tan",
    "taupe", "teal", "turquoise", "violet", "wine",
    // 10 basic color names
    "blue", "brown", "gray", "green", "orange",
    "pink", "purple", "red", "white", "yellow",
];
