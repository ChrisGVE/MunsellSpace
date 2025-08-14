//! Mechanical Wedge System for Deterministic ISCC-NBS Color Classification
//!
//! This module implements a deterministic hue-based partitioning system that divides
//! the Munsell hue circle into 100 wedge containers for efficient color polygon
//! distribution and lookup.
//!
//! # Algorithm Overview
//!
//! The mechanical wedge system solves the boundary ambiguity problem in ISCC-NBS
//! classification by using a deterministic rule: **exclude starting boundary, include ending boundary**.
//!
//! ## Hue Sequence
//!
//! The system uses the complete Munsell hue sequence:
//! ```text
//! [1R, 2R, 3R, ..., 10R, 1YR, 2YR, ..., 10YR, 1Y, ..., 10RP]
//! ```
//!
//! This creates 100 unique hue positions (10 families × 10 steps each).
//!
//! ## Wedge Containers
//!
//! Each wedge spans from one hue to the next:
//! - `1R→2R`: Contains colors from >1R to ≤2R
//! - `2R→3R`: Contains colors from >2R to ≤3R
//! - `10RP→1R`: Contains colors from >10RP to ≤1R (wraparound)
//!
//! ## Example Classification
//!
//! For a polygon spanning "8R-2YR":
//! 1. Find hue positions: 8R=7, 2YR=21
//! 2. Generate wedge sequence: [9R→10R, 10R→1YR, 1YR→2YR]
//! 3. Distribute polygon copies to these wedges
//!
//! # Thread Safety
//!
//! The wedge system can be safely shared across threads using `Arc<T>` as it
//! provides read-only access to its internal structure after initialization.
//!
//! # Examples
//!
//! ```rust
//! use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! let wedge_system = MechanicalWedgeSystem::new();
//!
//! // System automatically creates all 100 wedge containers
//! assert_eq!(wedge_system.wedge_count(), 100);
//!
//! // Find which wedge contains a specific hue
//! if let Some(wedge_key) = wedge_system.find_wedge_for_hue("5R") {
//!     println!("5R belongs to wedge: {}", wedge_key);
//! }
//! # Ok(())
//! # }
//! ```

use std::collections::HashMap;
use crate::{MunsellError, Result};
use crate::iscc::ISCC_NBS_Color;
use geo::CoordsIter;

// Method 2 is the only method used: Excludes starting boundary, includes ending boundary
// Example: "8R-2YR" -> [9R, 10R, 1YR, 2YR]

/// Mechanical hue wedge distribution system for deterministic ISCC-NBS classification.
///
/// This system partitions the complete Munsell hue circle into 100 wedge containers,
/// each responsible for a specific hue range. It implements deterministic boundary
/// handling to ensure consistent color classification.
///
/// # Architecture
///
/// The system maintains three key data structures:
/// - **Wedge containers**: 100 HashMap entries, each containing color polygons for a hue range
/// - **Hue sequence**: Ordered list of all 100 Munsell hues (1R through 10RP)
/// - **Position lookup**: Fast mapping from hue strings to sequence positions
///
/// # Boundary Rules
///
/// Uses "exclude start, include end" rule for deterministic classification:
/// - Hue exactly at wedge start: belongs to *previous* wedge
/// - Hue exactly at wedge end: belongs to *current* wedge
///
/// This eliminates ambiguity when colors fall exactly on wedge boundaries.
///
/// # Performance
///
/// - **Initialization**: O(1) - creates empty containers for all 100 wedges
/// - **Polygon distribution**: O(n×m) where n=polygons, m=average wedges per polygon
/// - **Hue lookup**: O(1) - HashMap-based position lookup
/// - **Classification**: O(k) where k=polygons in target wedge
///
/// # Examples
///
/// ```rust
/// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
///
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let system = MechanicalWedgeSystem::new();
///
/// // Check total wedge count
/// assert_eq!(system.wedge_count(), 100);
///
/// // Find wedge for specific hue
/// if let Some(wedge) = system.find_wedge_for_hue("5R") {
///     println!("5R is in wedge: {}", wedge);
/// }
/// # Ok(())
/// # }
/// ```
pub struct MechanicalWedgeSystem {
    /// Map of wedge identifiers to color polygon containers.
    ///
    /// Keys are formatted as "StartHue→EndHue" (e.g., "1R→2R", "10RP→1R").
    /// Values are vectors containing all ISCC-NBS color polygons that
    /// overlap with that wedge's hue range.
    wedge_containers: HashMap<String, Vec<ISCC_NBS_Color>>,
    
    /// Complete ordered sequence of Munsell hue references.
    ///
    /// Contains all 100 Munsell hues in canonical order:
    /// [1R, 2R, ..., 10R, 1YR, 2YR, ..., 10YR, 1Y, ..., 10RP]
    hue_sequence: Vec<String>,
    
    /// Fast lookup table mapping hue strings to sequence positions.
    ///
    /// Enables O(1) position lookup for hue range calculations
    /// without linear search through the hue sequence.
    hue_to_position: HashMap<String, usize>,
}

impl MechanicalWedgeSystem {
    /// Create a new mechanical wedge system with all 100 wedge containers.
    ///
    /// Initializes the complete wedge system by:
    /// 1. Creating the canonical 100-hue Munsell sequence
    /// 2. Building fast position lookup tables
    /// 3. Creating empty wedge containers for all hue ranges
    ///
    /// Uses the deterministic boundary rule: excludes starting boundary, includes ending boundary.
    ///
    /// # Returns
    /// Fully initialized wedge system ready for polygon distribution
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    ///
    /// let system = MechanicalWedgeSystem::new();
    /// assert_eq!(system.wedge_count(), 100);
    /// 
    /// // System includes all standard Munsell families
    /// let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    /// // Each family has 10 hue steps (1-10), totaling 100 unique hues
    /// ```
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
    
    /// Distribute a color polygon into appropriate wedge containers.
    ///
    /// Takes an ISCC-NBS color polygon and distributes copies into all wedge
    /// containers that overlap with the polygon's hue range. This enables
    /// efficient hue-based color classification.
    ///
    /// # Arguments
    /// * `polygon` - ISCC-NBS color with defined hue range and geometric polygon
    ///
    /// # Returns
    /// Result indicating success or failure of polygon distribution
    ///
    /// # Errors
    /// Returns [`MunsellError::ConversionError`] if:
    /// - Polygon hue range cannot be parsed
    /// - Hue values are not found in the standard Munsell sequence
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    /// // Note: ISCC_NBS_Color construction requires internal data
    /// // This example shows the conceptual usage
    /// 
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let mut system = MechanicalWedgeSystem::new();
    /// 
    /// // Polygon distribution happens internally during classifier initialization
    /// // Each polygon gets copied to all overlapping wedge containers
    /// assert_eq!(system.wedge_count(), 100);
    /// # Ok(())
    /// # }
    /// ```
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
    
    /// Find all ISCC-NBS colors that contain the given Munsell point.
    ///
    /// Searches for all color polygons that contain the specified (hue, value, chroma)
    /// coordinate. This is useful for detecting polygon overlaps or finding multiple
    /// valid color names for a single point.
    ///
    /// # Arguments
    /// * `hue` - Munsell hue string (e.g., "5R", "2.5YR")
    /// * `value` - Munsell value (0.0-10.0, lightness)
    /// * `chroma` - Munsell chroma (0.0+, saturation)
    ///
    /// # Returns
    /// Vector of ISCC-NBS color numbers that contain this point, sorted and deduplicated
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let system = MechanicalWedgeSystem::new();
    ///
    /// // Find all colors containing this point
    /// let colors = system.find_all_colors_at_point("5R", 5.0, 12.0);
    /// println!("Found {} overlapping colors", colors.len());
    ///
    /// // Multiple colors may contain the same point due to:
    /// // - Boundary overlaps between adjacent colors
    /// // - Colors with multiple disconnected regions
    /// # Ok(())
    /// # }
    /// ```
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
    
    /// Classify a Munsell color by finding the first matching ISCC-NBS color polygon.
    ///
    /// Performs efficient two-stage classification:
    /// 1. **Hue-based wedge selection**: O(1) lookup to find the correct wedge container
    /// 2. **Polygon containment testing**: O(k) search within the wedge's polygons
    ///
    /// Returns the first matching polygon, which is sufficient for most applications.
    /// For finding all overlapping colors, use [`find_all_colors_at_point`](Self::find_all_colors_at_point).
    ///
    /// # Arguments
    /// * `hue` - Munsell hue string (e.g., "5R", "2.5YR", "10GY")
    /// * `value` - Munsell value (0.0-10.0, lightness)
    /// * `chroma` - Munsell chroma (0.0+, saturation)
    ///
    /// # Returns
    /// Reference to the first ISCC-NBS color polygon containing this point, or `None`
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let system = MechanicalWedgeSystem::new();
    ///
    /// // Classify a specific Munsell color
    /// if let Some(color) = system.classify_color("5R", 5.0, 12.0) {
    ///     println!("Color number: {}", color.color_number);
    ///     println!("Hue range: {:?}", color.hue_range);
    /// } else {
    ///     println!("No ISCC-NBS color found for this point");
    /// }
    /// # Ok(())
    /// # }
    /// ```
    #[inline]
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
    #[inline]
    fn find_containing_wedge(&self, hue: &str) -> Option<String> {
        let (hue_number, hue_family) = self.parse_hue(hue).ok()?;
        
        // Optimized wedge number calculation - more efficient than chain of if-else
        let wedge_number = if hue_number <= 0.0 || hue_number > 10.0 {
            // Handle edge cases and wraparound
            let normalized = if hue_number <= 0.0 {
                (hue_number % 10.0 + 10.0) % 10.0
            } else {
                hue_number % 10.0
            };
            if normalized == 0.0 || normalized <= 1.0 { 1 } else { (normalized.ceil() as u8).min(10) }
        } else {
            // Normal case: direct ceiling calculation for (0, 10] range
            (hue_number.ceil() as u8).max(1).min(10)
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
    #[inline]
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
    
    /// Find which wedge contains a given hue.
    ///
    /// Determines the appropriate wedge container for a Munsell hue by parsing
    /// the hue notation and applying the mechanical wedge boundary rules.
    ///
    /// # Arguments
    /// * `hue` - Munsell hue string (e.g., "5R", "2.5YR", "10.3GY")
    ///
    /// # Returns
    /// Optional wedge key in format "StartHue→EndHue", or `None` if hue is invalid
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    ///
    /// let system = MechanicalWedgeSystem::new();
    ///
    /// // Find wedge for specific hues
    /// assert_eq!(system.find_wedge_for_hue("1.5R"), Some("1R→2R".to_string()));
    /// assert_eq!(system.find_wedge_for_hue("5R"), Some("5R→6R".to_string()));
    /// assert_eq!(system.find_wedge_for_hue("10RP"), Some("10RP→1R".to_string()));
    /// ```
    pub fn find_wedge_for_hue(&self, hue: &str) -> Option<String> {
        // Parse hue like "5.2R" or "10YR"
        let (hue_num, family) = self.parse_hue(hue).ok()?;
        
        // Determine which reference hues bracket this value
        let (start_ref, end_ref) = self.find_bracketing_hues(hue_num, &family)?;
        
        // Return the wedge key
        Some(format!("{}→{}", start_ref, end_ref))
    }
    
    /// Get all color polygons in a specific wedge container.
    ///
    /// Returns a reference to the vector of ISCC-NBS color polygons stored
    /// in the specified wedge container.
    ///
    /// # Arguments
    /// * `wedge_key` - Wedge identifier in format "StartHue→EndHue"
    ///
    /// # Returns
    /// Reference to vector of color polygons in the wedge, or `None` if wedge doesn't exist
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    ///
    /// let system = MechanicalWedgeSystem::new();
    ///
    /// // Get polygons from a specific wedge
    /// if let Some(polygons) = system.get_wedge_polygons("5R→6R") {
    ///     println!("Found {} polygons in 5R→6R wedge", polygons.len());
    /// }
    /// ```
    pub fn get_wedge_polygons(&self, wedge_key: &str) -> Option<&Vec<ISCC_NBS_Color>> {
        self.wedge_containers.get(wedge_key)
    }
    
    /// Get the total number of wedge containers.
    ///
    /// Returns the total count of wedge containers in the system.
    /// This should always be 100 for a complete Munsell hue system.
    ///
    /// # Returns
    /// Total number of wedge containers (always 100 for standard Munsell system)
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
    ///
    /// let system = MechanicalWedgeSystem::new();
    /// assert_eq!(system.wedge_count(), 100);
    /// ```
    pub fn wedge_count(&self) -> usize {
        self.wedge_containers.len()
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
    #[inline]
    fn get_next_family(&self, family: &str) -> Option<String> {
        // Use direct string matching for better performance than array search
        match family {
            "R" => Some("YR".to_string()),
            "YR" => Some("Y".to_string()),
            "Y" => Some("GY".to_string()),
            "GY" => Some("G".to_string()),
            "G" => Some("BG".to_string()),
            "BG" => Some("B".to_string()),
            "B" => Some("PB".to_string()),
            "PB" => Some("P".to_string()),
            "P" => Some("RP".to_string()),
            "RP" => Some("R".to_string()),
            _ => None,
        }
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
    #[inline]
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
    #[inline]
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