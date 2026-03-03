//! Boundary detection and point-in-polygon tests for the mechanical wedge system.

use crate::iscc::IsccNbsColor;
use super::system::MechanicalWedgeSystem;

impl MechanicalWedgeSystem {
    /// Check if a point (value, chroma) is inside a polygon with proper boundary rules.
    ///
    /// For a point on a polygon boundary, we determine inclusion by finding the
    /// horizontal and vertical segments that contain the point. Each segment has
    /// a lower and upper bound. The inclusion rule is:
    /// - If lower bound is 0: use [0, upper] (closed interval)
    /// - Otherwise: use (lower, upper] (half-open interval)
    ///
    /// This ensures each boundary point belongs to exactly one polygon.
    #[inline]
    pub(super) fn point_in_polygon(&self, value: f64, chroma: f64, polygon: &IsccNbsColor) -> bool {
        use geo::Contains;

        let point = geo::Point::new(chroma, value); // Note: chroma=x, value=y

        // Check if point is inside (geo's contains() returns false for boundary points)
        let is_inside = polygon.polygon.contains(&point);

        // If strictly inside, we're done
        if is_inside {
            return true;
        }

        // If not inside, check if we're on a boundary and apply boundary rules
        // For ISCC-NBS polygons with only horizontal/vertical edges, we check:
        // 1. Find the bounding segments that would contain this point
        // 2. Apply the inclusion rules based on segment bounds

        // Get the polygon's range for this point
        let (chroma_range, value_range) = self.get_polygon_ranges_at_point(value, chroma, polygon);

        // Check if point is within the polygon's ranges
        if let Some((c_min, c_max)) = chroma_range {
            if let Some((v_min, v_max)) = value_range {
                // Apply boundary rules for chroma
                let in_chroma = if c_min == 0.0 {
                    chroma >= c_min && chroma <= c_max // [0, max]
                } else {
                    chroma > c_min && chroma <= c_max // (min, max]
                };

                // Apply boundary rules for value
                let in_value = if v_min == 0.0 {
                    value >= v_min && value <= v_max // [0, max]
                } else {
                    value > v_min && value <= v_max // (min, max]
                };

                return in_chroma && in_value;
            }
        }

        false
    }

    /// Get the chroma and value ranges of the polygon at the given point.
    /// Returns (chroma_range, value_range) where each range is (min, max).
    #[inline]
    fn get_polygon_ranges_at_point(
        &self,
        value: f64,
        chroma: f64,
        polygon: &IsccNbsColor,
    ) -> (Option<(f64, f64)>, Option<(f64, f64)>) {
        use geo::Coord;

        let coords: Vec<Coord<f64>> = polygon.polygon.exterior().coords().cloned().collect();

        // Find min/max chroma at this value by checking all horizontal segments and corners
        let mut chroma_min = None::<f64>;
        let mut chroma_max = None::<f64>;

        // Find min/max value at this chroma by checking all vertical segments and corners
        let mut value_min = None::<f64>;
        let mut value_max = None::<f64>;

        // Check each edge and corner
        for i in 0..coords.len() - 1 {
            let p1 = coords[i];
            let p2 = coords[i + 1];

            // Check if this edge crosses our value line
            if (p1.y <= value && p2.y >= value) || (p2.y <= value && p1.y >= value) {
                // Interpolate chroma at this value
                if (p2.y - p1.y).abs() < 1e-10 {
                    // Horizontal edge at our value
                    let min_x = p1.x.min(p2.x);
                    let max_x = p1.x.max(p2.x);
                    chroma_min = Some(chroma_min.map_or(min_x, |m| m.min(min_x)));
                    chroma_max = Some(chroma_max.map_or(max_x, |m| m.max(max_x)));
                } else {
                    // Vertical edge crossing our value
                    let x = p1.x; // Both points have same x for vertical edge
                    chroma_min = Some(chroma_min.map_or(x, |m| m.min(x)));
                    chroma_max = Some(chroma_max.map_or(x, |m| m.max(x)));
                }
            }

            // Check if this edge crosses our chroma line
            if (p1.x <= chroma && p2.x >= chroma) || (p2.x <= chroma && p1.x >= chroma) {
                // Interpolate value at this chroma
                if (p2.x - p1.x).abs() < 1e-10 {
                    // Vertical edge at our chroma
                    let min_y = p1.y.min(p2.y);
                    let max_y = p1.y.max(p2.y);
                    value_min = Some(value_min.map_or(min_y, |m| m.min(min_y)));
                    value_max = Some(value_max.map_or(max_y, |m| m.max(max_y)));
                } else {
                    // Horizontal edge crossing our chroma
                    let y = p1.y; // Both points have same y for horizontal edge
                    value_min = Some(value_min.map_or(y, |m| m.min(y)));
                    value_max = Some(value_max.map_or(y, |m| m.max(y)));
                }
            }
        }

        let chroma_range = match (chroma_min, chroma_max) {
            (Some(min), Some(max)) => Some((min, max)),
            _ => None,
        };

        let value_range = match (value_min, value_max) {
            (Some(min), Some(max)) => Some((min, max)),
            _ => None,
        };

        (chroma_range, value_range)
    }

    /// Find the horizontal segment at the given value that contains the chroma point.
    /// Returns (min_chroma, max_chroma) of the segment.
    fn _find_horizontal_segment_at_point(
        &self,
        value: f64,
        chroma: f64,
        polygon: &IsccNbsColor,
    ) -> Option<(f64, f64)> {
        use geo::Coord;

        let coords: Vec<Coord<f64>> = polygon.polygon.exterior().coords().cloned().collect();

        // Find all horizontal segments at this value
        for i in 0..coords.len() - 1 {
            let p1 = coords[i];
            let p2 = coords[i + 1];

            // Check if this is a horizontal segment at our value
            if (p1.y - value).abs() < 1e-10 && (p2.y - value).abs() < 1e-10 {
                let min_x = p1.x.min(p2.x);
                let max_x = p1.x.max(p2.x);

                // Check if our chroma point is within this segment's range
                if chroma >= min_x - 1e-10 && chroma <= max_x + 1e-10 {
                    return Some((min_x, max_x));
                }
            }
        }

        None
    }

    /// Find the vertical segment at the given chroma that contains the value point.
    /// Returns (min_value, max_value) of the segment.
    fn _find_vertical_segment_at_point(
        &self,
        value: f64,
        chroma: f64,
        polygon: &IsccNbsColor,
    ) -> Option<(f64, f64)> {
        use geo::Coord;

        let coords: Vec<Coord<f64>> = polygon.polygon.exterior().coords().cloned().collect();

        // Find all vertical segments at this chroma
        for i in 0..coords.len() - 1 {
            let p1 = coords[i];
            let p2 = coords[i + 1];

            // Check if this is a vertical segment at our chroma
            if (p1.x - chroma).abs() < 1e-10 && (p2.x - chroma).abs() < 1e-10 {
                let min_y = p1.y.min(p2.y);
                let max_y = p1.y.max(p2.y);

                // Check if our value point is within this segment's range
                if value >= min_y - 1e-10 && value <= max_y + 1e-10 {
                    return Some((min_y, max_y));
                }
            }
        }

        None
    }
}
