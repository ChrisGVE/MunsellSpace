//! Diagnostics, statistics, and validation for the mechanical wedge system.

use std::collections::HashMap;
use geo::CoordsIter;
use crate::iscc::IsccNbsColor;
use super::system::MechanicalWedgeSystem;

/// Statistics about wedge container distribution.
#[derive(Debug)]
pub struct WedgeStatistics {
    pub total_wedges: usize,
    pub total_polygons: usize,
    pub wedge_counts: HashMap<String, usize>,
}

impl WedgeStatistics {
    fn new() -> Self {
        Self {
            total_wedges: 0,
            total_polygons: 0,
            wedge_counts: HashMap::new(),
        }
    }
}

/// Results of validating all wedge containers.
#[derive(Debug)]
pub struct WedgeValidationResults {
    pub wedge_results: HashMap<String, SingleWedgeValidation>,
}

impl WedgeValidationResults {
    fn new() -> Self {
        Self {
            wedge_results: HashMap::new(),
        }
    }
}

/// Validation results for a single wedge container.
#[derive(Debug)]
pub struct SingleWedgeValidation {
    pub polygon_count: usize,
    pub coverage_complete: bool,
    pub gaps_detected: Vec<String>,
    pub intersections_detected: Vec<String>,
}

impl SingleWedgeValidation {
    fn new() -> Self {
        Self {
            polygon_count: 0,
            coverage_complete: false,
            gaps_detected: Vec::new(),
            intersections_detected: Vec::new(),
        }
    }
}

impl MechanicalWedgeSystem {
    /// Get statistics about wedge container distribution.
    pub fn get_wedge_statistics(&self) -> WedgeStatistics {
        let mut stats = WedgeStatistics::new();

        for (wedge_key, container) in &self.wedge_containers {
            stats.wedge_counts.insert(wedge_key.clone(), container.len());
            stats.total_polygons += container.len();
        }

        stats.total_wedges = self.wedge_containers.len();
        stats
    }

    /// Debug method to check if a specific wedge exists and list its contents.
    pub fn debug_wedge_contents(&self, wedge_key: &str) -> Option<Vec<String>> {
        if let Some(container) = self.wedge_containers.get(wedge_key) {
            let contents = container
                .iter()
                .map(|color| {
                    format!(
                        "Color {} (polygon: {} points)",
                        color.color_number,
                        color.polygon.exterior().coords_count()
                    )
                })
                .collect();
            Some(contents)
        } else {
            None
        }
    }

    /// Debug method to find all wedge keys that contain a specific color number.
    pub fn debug_find_color(&self, color_number: u16) -> Vec<String> {
        let mut found_wedges = Vec::new();

        for (wedge_key, container) in &self.wedge_containers {
            if container.iter().any(|color| color.color_number == color_number) {
                found_wedges.push(wedge_key.clone());
            }
        }

        found_wedges
    }

    /// Debug method to test point-in-polygon for a specific color.
    pub fn debug_point_test(
        &self,
        wedge_key: &str,
        color_number: u16,
        value: f64,
        chroma: f64,
    ) -> Option<bool> {
        if let Some(container) = self.wedge_containers.get(wedge_key) {
            if let Some(color) = container.iter().find(|c| c.color_number == color_number) {
                let result = self.point_in_polygon(value, chroma, color);
                return Some(result);
            }
        }
        None
    }

    /// Detailed debug method to show polygon bounds and test point.
    pub fn debug_point_test_detailed(
        &self,
        wedge_key: &str,
        color_number: u16,
        value: f64,
        chroma: f64,
    ) -> Option<String> {
        if let Some(container) = self.wedge_containers.get(wedge_key) {
            if let Some(color) = container.iter().find(|c| c.color_number == color_number) {
                let coord_count = color.polygon.exterior().coords_count();
                let coord_points: Vec<_> = color.polygon.exterior().coords().collect();

                let _test_point = geo::Point::new(chroma, value);
                let result = self.point_in_polygon(value, chroma, color);

                let debug_info = format!(
                    "Color {} in wedge {}\n\
                     Hue range: {} to {}\n\
                     Test point: (value={}, chroma={}) -> Point::new(x={}, y={}) \
                     [chroma=x, value=y]\n\
                     Polygon {} coordinates: {:?}\n\
                     Point-in-polygon result: {}",
                    color_number, wedge_key,
                    color.hue_range.0, color.hue_range.1,
                    value, chroma, chroma, value,
                    coord_count, coord_points,
                    result
                );

                return Some(debug_info);
            }
        }
        None
    }

    /// Validate all wedge containers for coverage, gaps, and intersections.
    pub fn validate_all_wedges(&self) -> WedgeValidationResults {
        let mut results = WedgeValidationResults::new();

        for (wedge_key, container) in &self.wedge_containers {
            let wedge_result = self.validate_single_wedge(wedge_key, container);
            results.wedge_results.insert(wedge_key.clone(), wedge_result);
        }

        results
    }

    /// Validate a single wedge container.
    fn validate_single_wedge(
        &self,
        _wedge_key: &str,
        container: &[IsccNbsColor],
    ) -> SingleWedgeValidation {
        let mut validation = SingleWedgeValidation::new();

        // Check coverage: should cover chroma 0->50, value 0->10
        validation.coverage_complete = self.check_wedge_coverage(container);

        // Check for gaps between adjacent polygons
        validation.gaps_detected = self.detect_wedge_gaps(container);

        // Check for polygon intersections
        validation.intersections_detected = self.detect_wedge_intersections(container);

        validation.polygon_count = container.len();
        validation
    }

    /// Check if wedge container provides complete coverage.
    fn check_wedge_coverage(&self, _container: &[IsccNbsColor]) -> bool {
        // TODO: Implement coverage checking using geo crate operations
        // Should verify that union of all polygons covers rectangle [0,50] x [0,10]
        true // Placeholder
    }

    /// Detect gaps between polygons in wedge container.
    fn detect_wedge_gaps(&self, _container: &[IsccNbsColor]) -> Vec<String> {
        // TODO: Implement gap detection using geo crate
        // Look for areas not covered by any polygon
        Vec::new() // Placeholder
    }

    /// Detect intersections between polygons in wedge container.
    fn detect_wedge_intersections(&self, _container: &[IsccNbsColor]) -> Vec<String> {
        // TODO: Implement intersection detection using geo crate
        // Look for overlapping polygon interiors
        Vec::new() // Placeholder
    }
}
