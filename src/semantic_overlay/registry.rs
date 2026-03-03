//! Semantic overlay and registry data structures.

use super::types::MunsellSpec;
use super::polyhedron::ConvexPolyhedron;

/// A semantic overlay representing a non-basic color name region.
///
/// Based on Centore (2020): Each overlay is defined by a convex polyhedron
/// in 3D Munsell Cartesian space. The polyhedron encloses all colors that
/// can be called by this name.
#[derive(Debug, Clone)]
pub struct SemanticOverlay {
    /// The color name (e.g., "aqua", "beige", "coral")
    pub name: &'static str,
    /// The polyhedron defining the color region
    pub polyhedron: ConvexPolyhedron,
    /// Centroid (focal color) from Centore's Table 1
    pub centroid: MunsellSpec,
    /// Number of samples used to define this region in Centore's study
    pub sample_count: u32,
}

impl SemanticOverlay {
    /// Create a new semantic overlay.
    pub fn new(
        name: &'static str,
        vertices: &[(f64, f64, f64)],
        faces: &[(usize, usize, usize)],
        centroid: MunsellSpec,
        sample_count: u32,
    ) -> Self {
        Self {
            name,
            polyhedron: ConvexPolyhedron::from_arrays(vertices, faces),
            centroid,
            sample_count,
        }
    }

    /// Test if a Munsell color matches this overlay.
    pub fn contains(&self, color: &MunsellSpec) -> bool {
        let point = color.to_cartesian();
        self.polyhedron.contains_point(&point)
    }

    /// Test if a Munsell color matches with tolerance.
    pub fn contains_with_tolerance(&self, color: &MunsellSpec, tolerance: f64) -> bool {
        let point = color.to_cartesian();
        self.polyhedron.contains_point_with_tolerance(&point, tolerance)
    }

    /// Calculate distance from color to centroid.
    pub fn distance_to_centroid(&self, color: &MunsellSpec) -> f64 {
        color.distance_from(&self.centroid)
    }

    /// Get the centroid as a notation string.
    pub fn centroid_notation(&self) -> String {
        self.centroid.to_notation()
    }
}

/// Registry of all semantic overlays.
///
/// This struct holds all 30 color name overlays from Centore (2020):
/// 20 non-basic + 10 basic.
#[derive(Debug, Clone)]
pub struct SemanticOverlayRegistry {
    overlays: Vec<SemanticOverlay>,
}

impl SemanticOverlayRegistry {
    /// Create a new registry with the given overlays.
    pub fn new(overlays: Vec<SemanticOverlay>) -> Self {
        Self { overlays }
    }

    /// Get all overlays.
    pub fn all(&self) -> &[SemanticOverlay] {
        &self.overlays
    }

    /// Find an overlay by name (case-insensitive).
    pub fn get(&self, name: &str) -> Option<&SemanticOverlay> {
        let name_lower = name.to_lowercase();
        self.overlays.iter().find(|o| o.name.to_lowercase() == name_lower)
    }

    /// Test if a color matches a specific overlay by name.
    pub fn matches(&self, color: &MunsellSpec, overlay_name: &str) -> bool {
        self.get(overlay_name)
            .map(|o| o.contains(color))
            .unwrap_or(false)
    }

    /// Find all overlays that contain the given color.
    pub fn matching_overlays(&self, color: &MunsellSpec) -> Vec<&SemanticOverlay> {
        self.overlays
            .iter()
            .filter(|o| o.contains(color))
            .collect()
    }

    /// Find the best matching overlay for a color.
    ///
    /// If the color is inside multiple overlays, returns the one with
    /// the closest centroid. If the color is not inside any overlay,
    /// returns None.
    pub fn best_match(&self, color: &MunsellSpec) -> Option<&SemanticOverlay> {
        let matches = self.matching_overlays(color);
        if matches.is_empty() {
            return None;
        }

        matches
            .into_iter()
            .min_by(|a, b| {
                let dist_a = a.distance_to_centroid(color);
                let dist_b = b.distance_to_centroid(color);
                dist_a.partial_cmp(&dist_b).unwrap_or(std::cmp::Ordering::Equal)
            })
    }

    /// Find all overlays that contain the given color, ranked by centroid distance.
    ///
    /// Returns overlays sorted by distance from the color to each overlay's centroid,
    /// with the closest (most confident match) first.
    pub fn matching_overlays_ranked(&self, color: &MunsellSpec) -> Vec<(&SemanticOverlay, f64)> {
        let mut matches: Vec<(&SemanticOverlay, f64)> = self
            .overlays
            .iter()
            .filter(|o| o.contains(color))
            .map(|o| (o, o.distance_to_centroid(color)))
            .collect();

        matches.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
        matches
    }

    /// Find the closest overlay by centroid distance (even if color is outside).
    pub fn closest_overlay(&self, color: &MunsellSpec) -> Option<(&SemanticOverlay, f64)> {
        self.overlays
            .iter()
            .map(|o| (o, o.distance_to_centroid(color)))
            .min_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal))
    }

    /// Get overlay names.
    pub fn names(&self) -> Vec<&'static str> {
        self.overlays.iter().map(|o| o.name).collect()
    }

    /// Number of overlays in the registry.
    pub fn len(&self) -> usize {
        self.overlays.len()
    }

    /// Check if registry is empty.
    pub fn is_empty(&self) -> bool {
        self.overlays.is_empty()
    }
}
