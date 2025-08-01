use geo::prelude::*;
use geo::{Point, Polygon};
use std::collections::HashMap;
use crate::error::MunsellError;

/// Complete ISCC-NBS color classification result
#[derive(Debug, Clone)]
pub struct IsccNbsResult {
    /// ISCC-NBS descriptor from CSV 'iscc-nbs-descriptor' column (e.g., "vivid")
    pub iscc_nbs_descriptor: String,
    /// ISCC-NBS color from CSV 'iscc-nbs-color' column (e.g., "red")
    pub iscc_nbs_color: String,
    /// ISCC-NBS modifier from CSV 'iscc-nbs-modifier' column (not just Black/White)
    pub iscc_nbs_modifier: Option<String>,
    /// Revised color name from CSV 'revised-color' column
    pub revised_color: String,
    /// Revised descriptor constructed from revised_color + iscc_nbs_modifier
    pub revised_descriptor: String,
    /// Shade (last word of revised_color specifically)
    pub shade: String,
    /// ISCC-NBS color ID (renamed from color_number)
    pub iscc_nbs_color_id: u16,
}

impl IsccNbsResult {
    /// Get the ISCC-NBS descriptor
    pub fn iscc_nbs_descriptor(&self) -> &str {
        &self.iscc_nbs_descriptor
    }
    
    /// Get the ISCC-NBS color
    pub fn iscc_nbs_color(&self) -> &str {
        &self.iscc_nbs_color
    }
    
    /// Get the ISCC-NBS modifier (if any)
    pub fn iscc_nbs_modifier(&self) -> Option<&str> {
        self.iscc_nbs_modifier.as_deref()
    }
    
    /// Get the revised color name
    pub fn revised_color(&self) -> &str {
        &self.revised_color
    }
    
    /// Get the revised descriptor (constructed from revised_color + iscc_nbs_modifier)
    pub fn revised_descriptor(&self) -> &str {
        &self.revised_descriptor
    }
    
    /// Get the shade (last word of revised_color)
    pub fn shade(&self) -> &str {
        &self.shade
    }
    
    /// Get the ISCC-NBS color ID
    pub fn iscc_nbs_color_id(&self) -> u16 {
        self.iscc_nbs_color_id
    }
}

/// Internal representation of an ISCC-NBS color category with its polygonal region
#[derive(Debug, Clone)]
struct IsccNbsColor {
    /// Color number from ISCC-NBS standard
    color_number: u16,
    /// Polygon group number (for colors with multiple regions)
    polygon_group: u8,
    /// ISCC-NBS descriptor (e.g., "vivid")
    descriptor: String,
    /// ISCC-NBS color name (e.g., "red")
    color_name: String,
    /// Optional modifier (e.g., "-ish")
    modifier: Option<String>,
    /// Revised color name
    revised_color: String,
    /// Hue range (e.g., "1R", "7R") - will be split into adjacent planes
    hue_range: (String, String),
    /// Polygon defining the color region in Munsell value-chroma space
    polygon: Polygon<f64>,
}

/// ISCC-NBS color naming engine with proper boundary disambiguation and caching
#[derive(Debug)]
pub struct IsccNbsClassifier {
    /// Organized by adjacent Munsell hue planes for efficient lookup (e.g., "1R-2R", "2R-3R")
    hue_planes: HashMap<String, Vec<IsccNbsColor>>,
    /// Small LRU cache for successive lookups without repeated searches
    cache: std::cell::RefCell<HashMap<(String, String, String), Option<IsccNbsResult>>>, // (hue, value_str, chroma_str) -> result
    /// Maximum cache size
    cache_max_size: usize,
}

/// Embedded ISCC-NBS data - no external files needed
const ISCC_NBS_DATA: &str = include_str!("../ISCC-NBS-Definitions.csv");

impl IsccNbsClassifier {
    /// Create a new ISCC-NBS classifier using embedded data
    pub fn new() -> Result<Self, MunsellError> {
        let colors = Self::load_embedded_data()?;
        let hue_planes = Self::organize_by_adjacent_planes(colors);
        
        Ok(IsccNbsClassifier { 
            hue_planes,
            cache: std::cell::RefCell::new(HashMap::new()),
            cache_max_size: 256, // Small cache for performance
        })
    }
    
    /// Create a new ISCC-NBS classifier from external CSV file (for testing/development)
    pub fn from_csv(csv_path: &str) -> Result<Self, MunsellError> {
        let colors = Self::load_iscc_data(csv_path)?;
        let hue_planes = Self::organize_by_adjacent_planes(colors);
        
        Ok(IsccNbsClassifier { 
            hue_planes,
            cache: std::cell::RefCell::new(HashMap::new()),
            cache_max_size: 256,
        })
    }
    
    /// Classify a Munsell color using ISCC-NBS system with comprehensive result
    pub fn classify_munsell(&self, hue: &str, value: f64, chroma: f64) -> Result<Option<IsccNbsResult>, MunsellError> {
        // Create cache key
        let cache_key = (hue.to_string(), format!("{:.1}", value), format!("{:.1}", chroma));
        
        // Check cache first
        {
            let cache = self.cache.borrow();
            if let Some(cached_result) = cache.get(&cache_key) {
                return Ok(cached_result.clone());
            }
        }
        
        // Convert Munsell hue to adjacent plane
        let hue_plane = self.munsell_hue_to_adjacent_plane(hue)?;
        
        // Get polygons for this hue plane
        let Some(colors) = self.hue_planes.get(&hue_plane) else {
            let result = None;
            self.cache_result(cache_key, result.clone());
            return Ok(result);
        };
        
        let point = Point::new(value, chroma);
        
        // Check each polygon with ISCC boundary rules
        for color in colors {
            if self.point_in_iscc_polygon(&point, color)? {
                let result = Some(self.create_iscc_result(color));
                self.cache_result(cache_key, result.clone());
                return Ok(result);
            }
        }
        
        let result = None;
        self.cache_result(cache_key, result.clone());
        Ok(result)
    }
    
    /// Helper method to cache results with size management
    fn cache_result(&self, key: (String, String, String), result: Option<IsccNbsResult>) {
        let mut cache = self.cache.borrow_mut();
        
        // Simple cache size management - remove oldest entries if needed
        if cache.len() >= self.cache_max_size {
            // Remove first entry (simple FIFO, could be upgraded to LRU)
            if let Some(first_key) = cache.keys().next().cloned() {
                cache.remove(&first_key);
            }
        }
        
        cache.insert(key, result);
    }
    
    /// Classify a MunsellColor object directly
    pub fn classify_munsell_color(&self, munsell: &crate::types::MunsellColor) -> Result<Option<IsccNbsResult>, MunsellError> {
        // Handle neutral colors (no hue/chroma)
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            self.classify_munsell(hue, munsell.value, chroma)
        } else {
            // Neutral color - handle separately or return None
            // For now, return None as neutrals may need special handling
            Ok(None)
        }
    }
    
    /// Classify an sRGB color directly (convenience method)
    pub fn classify_srgb(&self, rgb: [u8; 3]) -> Result<Option<IsccNbsResult>, MunsellError> {
        use crate::MunsellConverter;
        
        // Convert sRGB to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.srgb_to_munsell(rgb)?;
        
        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }
    
    /// Classify a Lab color directly (convenience method)
    pub fn classify_lab(&self, _lab: [f64; 3]) -> Result<Option<IsccNbsResult>, MunsellError> {
        // Convert Lab to sRGB first (if converter supports this), then to Munsell
        // For now, return error as Lab conversion may not be implemented
        Err(MunsellError::ConversionError { 
            message: "Lab to ISCC-NBS conversion not yet implemented".to_string() 
        })
    }
    
    /// Check if point is in polygon using ISCC-NBS boundary disambiguation rules
    fn point_in_iscc_polygon(&self, point: &Point<f64>, color: &IsccNbsColor) -> Result<bool, MunsellError> {
        // First check: standard geometric containment (fast rejection)
        if !color.polygon.contains(point) {
            return Ok(false);
        }
        
        // Second check: Apply ISCC boundary rules for disambiguation
        let bounds = self.get_polygon_bounds(&color.polygon);
        let (value, chroma) = (point.x(), point.y());
        
        // Value boundary rules
        let value_ok = if bounds.min_value == 0.0 {
            value >= bounds.min_value  // Include 0 boundary
        } else {
            value > bounds.min_value   // Exclude non-zero boundary
        };
        let value_ok = value_ok && value <= bounds.max_value;
        
        // Chroma boundary rules  
        let chroma_ok = if bounds.min_chroma == 0.0 {
            chroma >= bounds.min_chroma  // Include 0 boundary
        } else {
            chroma > bounds.min_chroma   // Exclude non-zero boundary
        };
        let chroma_ok = chroma_ok && chroma <= bounds.max_chroma;
        
        Ok(value_ok && chroma_ok)
    }
    
    /// Get bounding box of polygon for ISCC boundary rule application
    fn get_polygon_bounds(&self, polygon: &Polygon<f64>) -> PolygonBounds {
        let coords: Vec<_> = polygon.exterior().coords().collect();
        
        let values: Vec<f64> = coords.iter().map(|c| c.x).collect();
        let chromas: Vec<f64> = coords.iter().map(|c| c.y).collect();
        
        PolygonBounds {
            min_value: values.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
            max_value: values.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)),
            min_chroma: chromas.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
            max_chroma: chromas.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)),
        }
    }
    
    /// Convert Munsell hue notation to adjacent plane identifier
    fn munsell_hue_to_adjacent_plane(&self, hue: &str) -> Result<String, MunsellError> {
        // Parse Munsell hue (e.g., "5R", "2.5YR", "10PB")
        let hue = hue.trim();
        
        // Extract number and hue family
        let (hue_number, hue_family) = self.parse_munsell_hue(hue)?;
        
        // Convert to adjacent plane format
        // For hue "5R", we might map to plane "4R-6R" or find the specific plane it belongs to
        let plane_key = self.find_adjacent_plane_for_hue(hue_number, &hue_family)?;
        
        Ok(plane_key)
    }
    
    /// Create comprehensive ISCC-NBS result from color data
    fn create_iscc_result(&self, color: &IsccNbsColor) -> IsccNbsResult {
        // Extract shade from revised_color (last word specifically)
        let shade = self.extract_shade(&color.revised_color);
        
        // Construct revised descriptor from revised_color + iscc_nbs_modifier
        let revised_descriptor = self.construct_revised_descriptor(&color.revised_color, &color.modifier);
        
        IsccNbsResult {
            iscc_nbs_descriptor: color.descriptor.clone(),
            iscc_nbs_color: color.color_name.clone(),
            iscc_nbs_modifier: color.modifier.clone(),
            revised_color: color.revised_color.clone(),
            revised_descriptor,
            shade,
            iscc_nbs_color_id: color.color_number,
        }
    }
    
    /// Extract shade (last word of revised_color specifically)
    fn extract_shade(&self, revised_color: &str) -> String {
        revised_color.trim()
            .split_whitespace()
            .last()
            .unwrap_or("unknown")
            .to_string()
    }
    
    /// Construct revised descriptor from revised_color + iscc_nbs_modifier
    /// Following ISCC-NBS standardized rules for descriptor construction
    fn construct_revised_descriptor(&self, revised_color: &str, iscc_nbs_modifier: &Option<String>) -> String {
        match iscc_nbs_modifier {
            // Rule 2: No modifier case
            None => revised_color.trim().to_string(),
            
            // Rule 3: "-ish" transformation rules
            Some(modifier) if modifier.contains("-ish") => {
                self.construct_ish_descriptor(revised_color, modifier)
            },
            
            // Rule 1: Basic prefix rule
            Some(modifier) => {
                format!("{} {}", modifier.trim(), revised_color.trim())
            }
        }
    }
    
    /// Handle "-ish" modifier transformations with English grammar rules
    fn construct_ish_descriptor(&self, revised_color: &str, modifier: &str) -> String {
        // Parse modifier: split on "-ish" to extract prefix and suffix
        let parts: Vec<&str> = modifier.split("-ish").collect();
        let prefix = parts[0].trim();
        let suffix = if parts.len() > 1 { parts[1].trim() } else { "" };
        
        // Transform color (Rule 5: olive exception)
        let transformed_color = if revised_color.trim() == "olive" {
            revised_color.trim().to_string()
        } else {
            self.apply_ish_transformation(revised_color.trim())
        };
        
        // Combine parts: prefix + colorish + suffix
        let mut result = Vec::new();
        if !prefix.is_empty() { 
            result.push(prefix); 
        }
        result.push(&transformed_color);
        if !suffix.is_empty() { 
            result.push(suffix); 
        }
        
        result.join(" ")
    }
    
    /// Apply English grammar rules for "-ish" transformations
    fn apply_ish_transformation(&self, color: &str) -> String {
        match color {
            "brown" => "brownish".to_string(),
            "blue" => "bluish".to_string(), 
            "red" => "reddish".to_string(),
            "green" => "greenish".to_string(),
            "yellow" => "yellowish".to_string(), 
            "purple" => "purplish".to_string(),
            "pink" => "pinkish".to_string(),
            // Default fallback for any other colors
            _ => format!("{}ish", color),
        }
    }
    
    /// Format the complete ISCC-NBS color name
    fn format_color_name(&self, color: &IsccNbsColor) -> String {
        match &color.modifier {
            Some(modifier) => format!("{} {}{}", color.descriptor, color.color_name, modifier),
            None => format!("{} {}", color.descriptor, color.color_name),
        }
    }
    
    /// Helper function to create data error
    fn data_error<S: Into<String>>(msg: S) -> MunsellError {
        MunsellError::ReferenceDataError { message: msg.into() }
    }
    
    /// Load ISCC-NBS data from embedded CSV string
    fn load_embedded_data() -> Result<Vec<IsccNbsColor>, MunsellError> {
        Self::parse_csv_data(ISCC_NBS_DATA)
    }
    
    /// Load ISCC-NBS data from CSV file (for testing/development)
    fn load_iscc_data(csv_path: &str) -> Result<Vec<IsccNbsColor>, MunsellError> {
        use std::fs;
        let csv_content = fs::read_to_string(csv_path)
            .map_err(|e| MunsellError::ReferenceDataError { message: format!("Failed to read CSV file: {}", e) })?;
        Self::parse_csv_data(&csv_content)
    }
    
    /// Parse CSV data and convert to polygons
    fn parse_csv_data(csv_content: &str) -> Result<Vec<IsccNbsColor>, MunsellError> {
        use csv::Reader;
        use geo::{LineString, Coord};
        
        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_groups: std::collections::HashMap<(u16, u8), Vec<(f64, f64)>> = std::collections::HashMap::new();
        let mut color_metadata: std::collections::HashMap<(u16, u8), (String, String, Option<String>, String, String, String)> = std::collections::HashMap::new();
        
        // Parse CSV data and group points by color_number and polygon group
        for result in reader.records() {
            let record = result
                .map_err(|e| MunsellError::ReferenceDataError { message: format!("CSV parsing error: {}", e) })?;
            
            // Parse CSV columns: color_number,points,iscc-nbs-descriptor,iscc-nbs-color,iscc-nbs-modifier,revised-color,hue1,hue2,chroma,value
            let color_number: u16 = record.get(0)
                .ok_or_else(|| Self::data_error("Missing color_number".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid color_number: {}", e)))?;
                
            let point_id: String = record.get(1)
                .ok_or_else(|| Self::data_error("Missing point_id".to_string()))?
                .to_string();
                
            // Extract polygon group from point_id (e.g., "1.2" -> group 1)
            let polygon_group: u8 = point_id.split('.').next()
                .ok_or_else(|| Self::data_error("Invalid point_id format".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid polygon_group: {}", e)))?;
            
            let descriptor = record.get(2)
                .ok_or_else(|| Self::data_error("Missing descriptor".to_string()))?
                .to_string();
                
            let color_name = record.get(3)
                .ok_or_else(|| Self::data_error("Missing color_name".to_string()))?
                .to_string();
                
            let modifier = record.get(4).filter(|s| !s.is_empty()).map(|s| s.to_string());
            
            let revised_color = record.get(5)
                .ok_or_else(|| Self::data_error("Missing revised_color".to_string()))?
                .to_string();
                
            let hue1 = record.get(6)
                .ok_or_else(|| Self::data_error("Missing hue1".to_string()))?
                .to_string();
                
            let hue2 = record.get(7)
                .ok_or_else(|| Self::data_error("Missing hue2".to_string()))?
                .to_string();
                
            let chroma: f64 = record.get(8)
                .ok_or_else(|| Self::data_error("Missing chroma".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid chroma: {}", e)))?;
                
            let value: f64 = record.get(9)
                .ok_or_else(|| Self::data_error("Missing value".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid value: {}", e)))?;
            
            // Store point in the appropriate group
            let key = (color_number, polygon_group);
            color_groups.entry(key).or_insert_with(Vec::new).push((value, chroma));
            
            // Store metadata (same for all points in a group)
            if !color_metadata.contains_key(&key) {
                color_metadata.insert(key, (descriptor, color_name, modifier, revised_color, hue1, hue2));
            }
        }
        
        // Convert grouped points to Polygon objects
        let mut colors = Vec::new();
        for ((color_number, polygon_group), points) in color_groups {
            if points.len() < 3 {
                return Err(Self::data_error(format!(
                    "Insufficient points for polygon: color {} group {} has {} points", 
                    color_number, polygon_group, points.len()
                )));
            }
            
            let (descriptor, color_name, modifier, revised_color, hue1, hue2) = 
                color_metadata.get(&(color_number, polygon_group))
                    .ok_or_else(|| Self::data_error("Missing metadata".to_string()))?
                    .clone();
            
            // Create LineString from points (geo requires a closed ring)
            let mut coords: Vec<Coord<f64>> = points.into_iter()
                .map(|(value, chroma)| Coord { x: value, y: chroma })
                .collect();
            
            // Ensure polygon is closed
            if coords.first() != coords.last() {
                if let Some(first) = coords.first().cloned() {
                    coords.push(first);
                }
            }
            
            let exterior = LineString::from(coords);
            let polygon = Polygon::new(exterior, vec![]); // No holes in ISCC-NBS polygons
            
            colors.push(IsccNbsColor {
                color_number,
                polygon_group,
                descriptor,
                color_name,
                modifier,
                revised_color,
                hue_range: (hue1, hue2),
                polygon,
            });
        }
        
        Ok(colors)
    }
    
    /// Organize colors by adjacent Munsell planes for efficient lookup
    fn organize_by_adjacent_planes(colors: Vec<IsccNbsColor>) -> HashMap<String, Vec<IsccNbsColor>> {
        let mut plane_map: HashMap<String, Vec<IsccNbsColor>> = HashMap::new();
        
        for color in colors {
            // Split the color's hue range into adjacent planes
            let planes = Self::split_into_adjacent_planes(&color.hue_range.0, &color.hue_range.1);
            
            for plane in planes {
                // Clone the color for each plane it belongs to
                let mut color_copy = color.clone();
                // Update the hue range to reflect the specific plane
                color_copy.hue_range = Self::parse_plane_range(&plane);
                
                plane_map.entry(plane).or_insert_with(Vec::new).push(color_copy);
            }
        }
        
        plane_map
    }
    
    /// Split a hue range into adjacent plane identifiers
    fn split_into_adjacent_planes(hue1: &str, hue2: &str) -> Vec<String> {
        // Parse both hues
        if let (Ok((num1, family1)), Ok((num2, family2))) = (
            Self::parse_hue_static(hue1),
            Self::parse_hue_static(hue2)
        ) {
            // If same family, create planes within the family
            if family1 == family2 {
                Self::create_planes_within_family(num1, num2, &family1)
            } else {
                // Cross-family range, create planes across families
                Self::create_cross_family_planes(num1, &family1, num2, &family2)
            }
        } else {
            // Fallback: create a single plane from the range
            vec![format!("{}-{}", hue1, hue2)]
        }
    }
    
    /// Parse a plane range string back into (hue1, hue2) tuple
    fn parse_plane_range(plane: &str) -> (String, String) {
        let parts: Vec<&str> = plane.split('-').collect();
        if parts.len() == 2 {
            (parts[0].to_string(), parts[1].to_string())
        } else {
            (plane.to_string(), plane.to_string())
        }
    }
    
    /// Parse Munsell hue notation (e.g., "5R", "2.5YR", "10PB")
    fn parse_munsell_hue(&self, hue: &str) -> Result<(f64, String), MunsellError> {
        Self::parse_hue_static(hue)
    }
    
    /// Static version of hue parsing for use in static methods
    fn parse_hue_static(hue: &str) -> Result<(f64, String), MunsellError> {
        let hue = hue.trim();
        
        // Find where the number ends and hue family begins
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
    
    /// Find the adjacent plane that contains the given hue
    fn find_adjacent_plane_for_hue(&self, hue_number: f64, hue_family: &str) -> Result<String, MunsellError> {
        // Look through available hue planes to find the one containing this hue
        for plane_key in self.hue_planes.keys() {
            if self.hue_in_plane(hue_number, hue_family, plane_key) {
                return Ok(plane_key.clone());
            }
        }
        
        // If no exact plane match, create a best-fit plane
        let rounded_hue = (hue_number.round() as i32).max(1).min(10);
        Ok(format!("{}{}", rounded_hue, hue_family))
    }
    
    /// Check if a hue falls within a specific plane
    fn hue_in_plane(&self, hue_number: f64, hue_family: &str, plane_key: &str) -> bool {
        // Parse the plane key (e.g., "1R-2R" or "5YR")
        if plane_key.contains('-') {
            // Range format like "1R-2R"
            let parts: Vec<&str> = plane_key.split('-').collect();
            if parts.len() == 2 {
                if let (Ok((start_num, start_family)), Ok((end_num, end_family))) = (
                    Self::parse_hue_static(parts[0]),
                    Self::parse_hue_static(parts[1])
                ) {
                    return hue_family == start_family && 
                           hue_family == end_family &&
                           hue_number >= start_num && 
                           hue_number <= end_num;
                }
            }
        } else {
            // Single hue format like "5YR"
            if let Ok((plane_num, plane_family)) = Self::parse_hue_static(plane_key) {
                return hue_family == plane_family && 
                       (hue_number - plane_num).abs() < 1.0;
            }
        }
        
        false
    }
    
    /// Create planes within the same hue family
    fn create_planes_within_family(num1: f64, num2: f64, family: &str) -> Vec<String> {
        let start = num1.min(num2).floor() as i32;
        let end = num1.max(num2).ceil() as i32;
        
        let mut planes = Vec::new();
        for i in start..end {
            let next = i + 1;
            planes.push(format!("{}{}-{}{}", i, family, next, family));
        }
        
        // If no planes generated, create a single plane
        if planes.is_empty() {
            planes.push(format!("{}{}", ((num1 + num2) / 2.0).round() as i32, family));
        }
        
        planes
    }
    
    /// Create planes across different hue families
    fn create_cross_family_planes(num1: f64, family1: &str, num2: f64, family2: &str) -> Vec<String> {
        // For cross-family ranges, create individual planes
        // This is a simplified approach - could be enhanced with full hue circle logic
        vec![
            format!("{}{}", num1.round() as i32, family1),
            format!("{}{}", num2.round() as i32, family2),
        ]
    }
}

/// Validation functions using geo crate  
pub mod validation {
    use super::{IsccNbsColor, ValidationError};
    use geo::Intersects;
    
    /// Validate ISCC-NBS polygon data for integrity
    pub fn validate_polygons(colors: &[IsccNbsColor]) -> Vec<ValidationError> {
        let mut errors = Vec::new();
        
        // Check right angles using geo's geometric operations
        for color in colors {
            if let Err(mut angle_errors) = validate_right_angles(&color.polygon) {
                // Update color numbers in angle errors
                for error in &mut angle_errors {
                    if let ValidationError::InvalidAngle { color_number, .. } = error {
                        *color_number = color.color_number;
                    }
                }
                errors.extend(angle_errors);
            }
        }
        
        // Check for intersections using geo's robust intersection detection
        // For now, we'll use a simpler approach - true intersection check will be refined later
        for i in 0..colors.len() {
            for j in (i + 1)..colors.len() {
                if colors[i].polygon.intersects(&colors[j].polygon) {
                    // TODO: Add boundary vs interior intersection distinction
                    errors.push(ValidationError::Intersection {
                        color1: colors[i].color_number,
                        color2: colors[j].color_number,
                    });
                }
            }
        }
        
        errors
    }
    
    /// Validate that polygon has only right angles (90° and 270°) 
    fn validate_right_angles(polygon: &geo::Polygon<f64>) -> Result<(), Vec<ValidationError>> {
        
        let exterior = polygon.exterior();
        let coords: Vec<_> = exterior.coords().collect();
        
        if coords.len() < 4 {
            return Ok(()); // Too few points to validate angles
        }
        
        let mut errors = Vec::new();
        
        // Check each angle in the polygon
        for i in 1..coords.len()-1 {
            let p1 = coords[i-1];
            let p2 = coords[i];
            let p3 = coords[i+1];
            
            // Calculate vectors
            let v1 = (p1.x - p2.x, p1.y - p2.y);
            let v2 = (p3.x - p2.x, p3.y - p2.y);
            
            // Calculate angle using dot product and cross product
            let dot = v1.0 * v2.0 + v1.1 * v2.1;
            let cross = v1.0 * v2.1 - v1.1 * v2.0;
            let angle = cross.atan2(dot).abs() * 180.0 / std::f64::consts::PI;
            
            // Check if angle is approximately 90° or 270° (allowing small tolerance)
            let tolerance = 1.0; // 1 degree tolerance 
            let is_right_angle = (angle - 90.0).abs() < tolerance || (angle - 270.0).abs() < tolerance;
            
            if !is_right_angle {
                errors.push(ValidationError::InvalidAngle {
                    color_number: 0, // Would need to pass color number
                    point_index: i,
                    angle,
                });
            }
        }
        
        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }
}

/// Bounds of a polygon for ISCC boundary rule application
#[derive(Debug, Clone)]
struct PolygonBounds {
    min_value: f64,
    max_value: f64,
    min_chroma: f64,
    max_chroma: f64,
}

/// Validation error types
#[derive(Debug, Clone)]
pub enum ValidationError {
    InvalidAngle {
        color_number: u16,
        point_index: usize,
        angle: f64,
    },
    Intersection {
        color1: u16,
        color2: u16,
    },
    Gap {
        hue_slice: String,
        region: String,
    },
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_boundary_disambiguation() {
        // Test that boundary rules prevent ambiguous classification
        // Point exactly on boundary should only match one polygon
    }
    
    #[test]
    fn test_staircase_classification() {
        // Test that staircase polygons work correctly with rectangles in steps
    }
}