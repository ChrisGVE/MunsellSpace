use std::collections::HashMap;
use crate::{MunsellError, Result};
use crate::iscc::ISCC_NBS_Color;
use geo::CoordsIter;

// Method 2 is the only method used: Excludes starting boundary, includes ending boundary
// Example: "8R-2YR" -> [9R, 10R, 1YR, 2YR]

/// Mechanical hue wedge distribution system for ISCC-NBS classification
/// Implements the deterministic approach outlined in ALGO.md
pub struct MechanicalWedgeSystem {
    /// All 100 wedge containers (e.g., "1R→2R", "2R→3R", etc.)
    wedge_containers: HashMap<String, Vec<ISCC_NBS_Color>>,
    /// Ordered sequence of all Munsell hue references  
    hue_sequence: Vec<String>,
    /// Quick lookup from hue to sequence position
    hue_to_position: HashMap<String, usize>,
}

impl MechanicalWedgeSystem {
    /// Create new mechanical wedge system with all 100 wedge containers
    /// Uses the optimal method: excludes starting boundary, includes ending boundary
    pub fn new() -> Self {
        let hue_sequence = Self::create_reference_hue_sequence();
        let hue_to_position = Self::create_position_lookup(&hue_sequence);
        let wedge_containers = Self::create_all_wedge_containers(&hue_sequence);
        
        Self {
            wedge_containers,
            hue_sequence,
            hue_to_position,
        }
    }
    
    /// Create the complete ordered sequence of Munsell hue references
    fn create_reference_hue_sequence() -> Vec<String> {
        let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        let mut sequence = Vec::with_capacity(100); // 10 families × 10 hues = 100 total
        
        for family in &families {
            for hue_num in 1..=10 {
                sequence.push(format!("{}{}", hue_num, family));
            }
        }
        
        sequence
    }
    
    /// Create quick lookup from hue string to sequence position
    fn create_position_lookup(sequence: &[String]) -> HashMap<String, usize> {
        sequence.iter()
            .enumerate()
            .map(|(pos, hue)| (hue.clone(), pos))
            .collect()
    }
    
    /// Create all 100 wedge containers (empty initially)
    fn create_all_wedge_containers(sequence: &[String]) -> HashMap<String, Vec<ISCC_NBS_Color>> {
        let mut containers = HashMap::new();
        
        for i in 0..sequence.len() {
            let start_hue = &sequence[i];
            let end_hue = &sequence[(i + 1) % sequence.len()]; // Wraparound for 10RP→1R
            let wedge_key = format!("{}→{}", start_hue, end_hue);
            containers.insert(wedge_key, Vec::new());
        }
        
        containers
    }
    
    /// Distribute a polygon into appropriate wedge containers
    /// For polygon spanning hue1 to hue2, copies go into all wedges in that range
    pub fn distribute_polygon(&mut self, polygon: ISCC_NBS_Color) -> Result<()> {
        let (start_hue, end_hue) = Self::parse_polygon_hue_range(&polygon)?;
        let wedge_keys = self.find_wedges_in_range(&start_hue, &end_hue)?;
        
        // Copy polygon into each wedge container in the range
        for wedge_key in wedge_keys {
            if let Some(container) = self.wedge_containers.get_mut(&wedge_key) {
                container.push(polygon.clone());
            }
        }
        
        Ok(())
    }
    
    /// Parse polygon hue range from ISCC-NBS data
    fn parse_polygon_hue_range(polygon: &ISCC_NBS_Color) -> Result<(String, String)> {
        // Extract hue range from polygon data (e.g., "5R" to "7YR")
        // This depends on how hue ranges are stored in IsccNbsColor
        // For now, assume they're in a hue_range field
        Ok((polygon.hue_range.0.clone(), polygon.hue_range.1.clone()))
    }
    
    /// Find all wedge keys that span from start_hue to end_hue
    /// Uses the optimal method: excludes starting boundary, includes ending boundary
    /// Example: "8R" to "2YR" -> [9R→10R, 10R→1YR, 1YR→2YR, 2YR→3YR]
    fn find_wedges_in_range(&self, start_hue: &str, end_hue: &str) -> Result<Vec<String>> {
        let start_pos = self.hue_to_position.get(start_hue)
            .ok_or_else(|| MunsellError::ConversionError { 
                message: format!("Unknown start hue: {}", start_hue) 
            })?;
        
        let end_pos = self.hue_to_position.get(end_hue)
            .ok_or_else(|| MunsellError::ConversionError { 
                message: format!("Unknown end hue: {}", end_hue) 
            })?;
        
        let mut wedge_keys = Vec::new();
        
        // Excludes starting boundary, includes ending boundary
        let mut current_pos = (*start_pos + 1) % self.hue_sequence.len();
        
        loop {
            let next_pos = (current_pos + 1) % self.hue_sequence.len();
            let start_hue_at_pos = &self.hue_sequence[current_pos];
            let end_hue_at_pos = &self.hue_sequence[next_pos];
            
            wedge_keys.push(format!("{}→{}", start_hue_at_pos, end_hue_at_pos));
            
            // Stop when we've included the end position
            if current_pos == *end_pos {
                break;
            }
            
            current_pos = next_pos;
        }
        
        Ok(wedge_keys)
    }
    
    /// Find all ISCC-NBS colors that contain the given point.
    /// Returns all overlapping colors, useful for detecting polygon overlaps.
    pub fn find_all_colors_at_point(&self, hue: &str, value: f64, chroma: f64) -> Vec<u16> {
        // 1. Find the containing wedge for this hue
        let wedge_key = match self.find_containing_wedge(hue) {
            Some(key) => key,
            None => return vec![],
        };
        
        // 2. Get all polygons in this wedge
        let container = match self.wedge_containers.get(&wedge_key) {
            Some(c) => c,
            None => return vec![],
        };
        
        // 3. Find ALL polygons that contain this point
        let mut matching_colors = Vec::new();
        
        for polygon in container {
            if self.point_in_polygon(value, chroma, polygon) {
                matching_colors.push(polygon.color_number);
            }
        }
        
        // Remove duplicates (same color might appear multiple times in a wedge)
        matching_colors.sort_unstable();
        matching_colors.dedup();
        
        matching_colors
    }
    
    /// Classify a color by finding its containing wedge and searching within it
    pub fn classify_color(&self, hue: &str, value: f64, chroma: f64) -> Option<&ISCC_NBS_Color> {
        // 1. Find the containing wedge for this hue
        let wedge_key = self.find_containing_wedge(hue)?;
        
        // 2. Search within that wedge container
        let container = self.wedge_containers.get(&wedge_key)?;
        
        // 3. Find first polygon in the wedge that contains this point
        container.iter()
            .find(|polygon| self.point_in_polygon(value, chroma, polygon))
    }
    
    /// Find which wedge contains the given hue using correct range interpretation
    /// 1R represents [0-1], 2R represents (1-2], ..., 10R represents (9-10]
    fn find_containing_wedge(&self, hue: &str) -> Option<String> {
        let (hue_number, hue_family) = self.parse_hue(hue).ok()?;
        
        // Handle the range interpretation directly without modulo first
        // to properly handle the 10.0 case
        let wedge_number = if hue_number == 0.0 || (hue_number > 0.0 && hue_number <= 1.0) {
            // [0, 1] belongs to 1R
            1
        } else if hue_number > 1.0 && hue_number <= 2.0 {
            // (1, 2] belongs to 2R
            2
        } else if hue_number > 2.0 && hue_number <= 3.0 {
            // (2, 3] belongs to 3R
            3
        } else if hue_number > 3.0 && hue_number <= 4.0 {
            // (3, 4] belongs to 4R
            4
        } else if hue_number > 4.0 && hue_number <= 5.0 {
            // (4, 5] belongs to 5R
            5
        } else if hue_number > 5.0 && hue_number <= 6.0 {
            // (5, 6] belongs to 6R
            6
        } else if hue_number > 6.0 && hue_number <= 7.0 {
            // (6, 7] belongs to 7R
            7
        } else if hue_number > 7.0 && hue_number <= 8.0 {
            // (7, 8] belongs to 8R
            8
        } else if hue_number > 8.0 && hue_number <= 9.0 {
            // (8, 9] belongs to 9R
            9
        } else if hue_number > 9.0 && hue_number <= 10.0 {
            // (9, 10] belongs to 10R
            10
        } else {
            // Handle wraparound for values > 10.0
            let normalized = hue_number % 10.0;
            if normalized == 0.0 || normalized <= 1.0 {
                1
            } else {
                (normalized.ceil() as u8).min(10)
            }
        };
        
        // Find the corresponding wedge key
        let wedge_hue = format!("{}{}", wedge_number, hue_family);
        let wedge_pos = self.hue_to_position.get(&wedge_hue)?;
        let wedge_end_pos = (*wedge_pos + 1) % self.hue_sequence.len();
        
        let start_hue = &self.hue_sequence[*wedge_pos];
        let end_hue = &self.hue_sequence[wedge_end_pos];
        
        Some(format!("{}→{}", start_hue, end_hue))
    }
    
    /// Parse Munsell hue notation (e.g., "4.5R", "7YR")
    fn parse_hue(&self, hue: &str) -> Result<(f64, String)> {
        let hue = hue.trim();
        
        // Find where the number ends and family begins
        let mut split_pos = 0;
        for (i, c) in hue.char_indices() {
            if c.is_alphabetic() {
                split_pos = i;
                break;
            }
        }
        
        if split_pos == 0 {
            return Err(MunsellError::ConversionError {
                message: format!("Invalid hue format: {}", hue)
            });
        }
        
        let number_str = &hue[..split_pos];
        let family_str = &hue[split_pos..];
        
        let number: f64 = number_str.parse()
            .map_err(|_| MunsellError::ConversionError {
                message: format!("Invalid hue number: {}", number_str)
            })?;
            
        Ok((number, family_str.to_string()))
    }
    
    /// Find which wedge a given hue belongs to
    pub fn find_wedge_for_hue(&self, hue: &str) -> Option<String> {
        // Parse hue like "5.2R" or "10YR"
        let (hue_num, family) = self.parse_hue(hue).ok()?;
        
        // Determine which reference hues bracket this value
        let (start_ref, end_ref) = self.find_bracketing_hues(hue_num, &family)?;
        
        // Return the wedge key
        Some(format!("{}→{}", start_ref, end_ref))
    }
    
    /// Get polygons in a specific wedge
    pub fn get_wedge_polygons(&self, wedge_key: &str) -> Option<&Vec<ISCC_NBS_Color>> {
        self.wedge_containers.get(wedge_key)
    }
    
    /// Find the reference hues that bracket a given hue value
    fn find_bracketing_hues(&self, hue_num: f64, family: &str) -> Option<(String, String)> {
        // Round down to get the starting reference
        let start_num = hue_num.floor() as u32;
        let end_num = if start_num == 10 { 1 } else { start_num + 1 };
        
        // Handle family transition at 10
        if start_num == 10 {
            // Transition to next family
            let next_family = self.get_next_family(family)?;
            Some((
                format!("{}{}", start_num, family),
                format!("{}{}", end_num, next_family)
            ))
        } else {
            Some((
                format!("{}{}", start_num, family),
                format!("{}{}", end_num, family)
            ))
        }
    }
    
    /// Get the next family in the sequence
    fn get_next_family(&self, family: &str) -> Option<String> {
        let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        let pos = families.iter().position(|&f| f == family)?;
        let next_pos = (pos + 1) % families.len();
        Some(families[next_pos].to_string())
    }
    
    /// Check if a point (value, chroma) is inside a polygon with proper boundary rules
    /// 
    /// For a point on a polygon boundary, we determine inclusion by finding the 
    /// horizontal and vertical segments that contain the point. Each segment has
    /// a lower and upper bound. The inclusion rule is:
    /// - If lower bound is 0: use [0, upper] (closed interval)
    /// - Otherwise: use (lower, upper] (half-open interval)
    /// 
    /// This ensures each boundary point belongs to exactly one polygon.
    fn point_in_polygon(&self, value: f64, chroma: f64, polygon: &ISCC_NBS_Color) -> bool {
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
                    chroma >= c_min && chroma <= c_max  // [0, max]
                } else {
                    chroma > c_min && chroma <= c_max   // (min, max]
                };
                
                // Apply boundary rules for value
                let in_value = if v_min == 0.0 {
                    value >= v_min && value <= v_max    // [0, max]
                } else {
                    value > v_min && value <= v_max     // (min, max]
                };
                
                return in_chroma && in_value;
            }
        }
        
        false
    }
    
    /// Get the chroma and value ranges of the polygon at the given point
    /// Returns (chroma_range, value_range) where each range is (min, max)
    fn get_polygon_ranges_at_point(&self, value: f64, chroma: f64, polygon: &ISCC_NBS_Color) -> (Option<(f64, f64)>, Option<(f64, f64)>) {
        use geo::Coordinate;
        
        let coords: Vec<Coordinate<f64>> = polygon.polygon.exterior().coords().cloned().collect();
        
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
    
    /// Find the horizontal segment at the given value that contains the chroma point
    /// Returns (min_chroma, max_chroma) of the segment
    fn find_horizontal_segment_at_point(&self, value: f64, chroma: f64, polygon: &ISCC_NBS_Color) -> Option<(f64, f64)> {
        use geo::Coordinate;
        
        let coords: Vec<Coordinate<f64>> = polygon.polygon.exterior().coords().cloned().collect();
        
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
    
    /// Find the vertical segment at the given chroma that contains the value point
    /// Returns (min_value, max_value) of the segment
    fn find_vertical_segment_at_point(&self, value: f64, chroma: f64, polygon: &ISCC_NBS_Color) -> Option<(f64, f64)> {
        use geo::Coordinate;
        
        let coords: Vec<Coordinate<f64>> = polygon.polygon.exterior().coords().cloned().collect();
        
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
    
    /// Get statistics about wedge container distribution
    pub fn get_wedge_statistics(&self) -> WedgeStatistics {
        let mut stats = WedgeStatistics::new();
        
        for (wedge_key, container) in &self.wedge_containers {
            stats.wedge_counts.insert(wedge_key.clone(), container.len());
            stats.total_polygons += container.len();
        }
        
        stats.total_wedges = self.wedge_containers.len();
        stats
    }
    
    /// Debug method to check if a specific wedge exists and list its contents
    pub fn debug_wedge_contents(&self, wedge_key: &str) -> Option<Vec<String>> {
        if let Some(container) = self.wedge_containers.get(wedge_key) {
            let contents = container.iter()
                .map(|color| format!("Color {} (polygon: {} points)", 
                    color.color_number,
                    color.polygon.exterior().coords_count()
                ))
                .collect();
            Some(contents)
        } else {
            None
        }
    }
    
    /// Debug method to find all wedge keys that contain a specific color number
    pub fn debug_find_color(&self, color_number: u16) -> Vec<String> {
        let mut found_wedges = Vec::new();
        
        for (wedge_key, container) in &self.wedge_containers {
            if container.iter().any(|color| color.color_number == color_number) {
                found_wedges.push(wedge_key.clone());
            }
        }
        
        found_wedges
    }
    
    /// Debug method to test point-in-polygon for a specific color
    pub fn debug_point_test(&self, wedge_key: &str, color_number: u16, value: f64, chroma: f64) -> Option<bool> {
        if let Some(container) = self.wedge_containers.get(wedge_key) {
            if let Some(color) = container.iter().find(|c| c.color_number == color_number) {
                let result = self.point_in_polygon(value, chroma, color);
                return Some(result);
            }
        }
        None
    }
    
    /// Detailed debug method to show polygon bounds and test point
    pub fn debug_point_test_detailed(&self, wedge_key: &str, color_number: u16, value: f64, chroma: f64) -> Option<String> {
        if let Some(container) = self.wedge_containers.get(wedge_key) {
            if let Some(color) = container.iter().find(|c| c.color_number == color_number) {
                // Extract polygon coordinates
                let coord_count = color.polygon.exterior().coords_count();
                let coord_points: Vec<_> = color.polygon.exterior().coords().collect();
                
                let test_point = geo::Point::new(chroma, value);
                let result = self.point_in_polygon(value, chroma, color);
                
                let debug_info = format!(
                    "Color {} in wedge {}\n\
                     Hue range: {} to {}\n\
                     Test point: (value={}, chroma={}) -> Point::new(x={}, y={}) [chroma=x, value=y]\n\
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
    
    /// Validate all wedge containers for coverage, gaps, and intersections
    pub fn validate_all_wedges(&self) -> WedgeValidationResults {
        let mut results = WedgeValidationResults::new();
        
        for (wedge_key, container) in &self.wedge_containers {
            let wedge_result = self.validate_single_wedge(wedge_key, container);
            results.wedge_results.insert(wedge_key.clone(), wedge_result);
        }
        
        results
    }
    
    /// Validate a single wedge container
    fn validate_single_wedge(&self, _wedge_key: &str, container: &[ISCC_NBS_Color]) -> SingleWedgeValidation {
        let mut validation = SingleWedgeValidation::new();
        
        // Check coverage: should cover chroma 0→50, value 0→10
        validation.coverage_complete = self.check_wedge_coverage(container);
        
        // Check for gaps between adjacent polygons
        validation.gaps_detected = self.detect_wedge_gaps(container);
        
        // Check for polygon intersections
        validation.intersections_detected = self.detect_wedge_intersections(container);
        
        validation.polygon_count = container.len();
        validation
    }
    
    /// Check if wedge container provides complete coverage
    fn check_wedge_coverage(&self, _container: &[ISCC_NBS_Color]) -> bool {
        // TODO: Implement coverage checking using geo crate operations
        // Should verify that union of all polygons covers rectangle [0,50] × [0,10]
        true // Placeholder
    }
    
    /// Detect gaps between polygons in wedge container
    fn detect_wedge_gaps(&self, _container: &[ISCC_NBS_Color]) -> Vec<String> {
        // TODO: Implement gap detection using geo crate
        // Look for areas not covered by any polygon
        Vec::new() // Placeholder
    }
    
    /// Detect intersections between polygons in wedge container
    fn detect_wedge_intersections(&self, _container: &[ISCC_NBS_Color]) -> Vec<String> {
        // TODO: Implement intersection detection using geo crate
        // Look for overlapping polygon interiors
        Vec::new() // Placeholder
    }
}

/// Statistics about wedge container distribution
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

/// Results of validating all wedge containers
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

/// Validation results for a single wedge container
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

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_hue_sequence_creation() {
        let sequence = MechanicalWedgeSystem::create_reference_hue_sequence();
        
        // Should have exactly 100 hues (10 families × 10 hues)
        assert_eq!(sequence.len(), 100);
        
        // First few should be R family
        assert_eq!(sequence[0], "1R");
        assert_eq!(sequence[1], "2R");
        assert_eq!(sequence[9], "10R");
        
        // Then YR family
        assert_eq!(sequence[10], "1YR");
        assert_eq!(sequence[19], "10YR");
        
        // Last should be 10RP
        assert_eq!(sequence[99], "10RP");
    }
    
    #[test]
    fn test_wedge_container_creation() {
        let system = MechanicalWedgeSystem::new();
        
        // Should have exactly 100 wedge containers
        assert_eq!(system.wedge_containers.len(), 100);
        
        // Should have proper wedge keys
        assert!(system.wedge_containers.contains_key("1R→2R"));
        assert!(system.wedge_containers.contains_key("10R→1YR"));
        assert!(system.wedge_containers.contains_key("10RP→1R")); // Wraparound
    }
    
    #[test]
    fn test_hue_parsing() {
        let system = MechanicalWedgeSystem::new();
        
        // Test standard hues
        let (num, family) = system.parse_hue("5R").unwrap();
        assert_eq!(num, 5.0);
        assert_eq!(family, "R");
        
        // Test fractional hues
        let (num, family) = system.parse_hue("4.5YR").unwrap();
        assert_eq!(num, 4.5);
        assert_eq!(family, "YR");
        
        // Test two-letter families
        let (num, family) = system.parse_hue("7PB").unwrap();
        assert_eq!(num, 7.0);
        assert_eq!(family, "PB");
    }
    
    #[test]
    fn test_containing_wedge_range_based_rules() {
        let system = MechanicalWedgeSystem::new();
        
        // Range-based interpretation: 1R = [0-1], 2R = (1-2], etc.
        
        // Values in [0, 1] belong to 1R wedge
        assert_eq!(system.find_containing_wedge("0.0R"), Some("1R→2R".to_string()));
        assert_eq!(system.find_containing_wedge("0.5R"), Some("1R→2R".to_string()));
        assert_eq!(system.find_containing_wedge("1.0R"), Some("1R→2R".to_string()));
        
        // Values in (1, 2] belong to 2R wedge
        assert_eq!(system.find_containing_wedge("1.1R"), Some("2R→3R".to_string()));
        assert_eq!(system.find_containing_wedge("1.5R"), Some("2R→3R".to_string()));
        assert_eq!(system.find_containing_wedge("2.0R"), Some("2R→3R".to_string()));
        
        // Values in (4, 5] belong to 5R wedge
        assert_eq!(system.find_containing_wedge("4.5R"), Some("5R→6R".to_string()));
        
        // Values in (9, 10] belong to 10R wedge
        assert_eq!(system.find_containing_wedge("9.5R"), Some("10R→1YR".to_string()));
        assert_eq!(system.find_containing_wedge("10.0R"), Some("10R→1YR".to_string()));
        
        // Test different families
        assert_eq!(system.find_containing_wedge("7.2YR"), Some("8YR→9YR".to_string()));
        
        // Test wraparound: values >= 10 should wrap to [0, 1] range
        assert_eq!(system.find_containing_wedge("10.5R"), Some("1R→2R".to_string()));
        assert_eq!(system.find_containing_wedge("11.0R"), Some("1R→2R".to_string()));
    }
}