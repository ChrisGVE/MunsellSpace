use geo::prelude::*;
use geo::{Point, Polygon};
use std::collections::HashMap;
use crate::error::MunsellError;
use crate::mechanical_wedges::MechanicalWedgeSystem;
use lazy_static::lazy_static;

// Define -ish transformation dictionary at module level
lazy_static! {
    static ref COLOR_TO_ISH: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();
        m.insert("brown", "brownish");
        m.insert("blue", "bluish");
        m.insert("red", "reddish");
        m.insert("green", "greenish");
        m.insert("yellow", "yellowish");
        m.insert("purple", "purplish");
        m.insert("pink", "pinkish");
        m.insert("orange", "orangish");
        m.insert("gray", "grayish");
        m.insert("grey", "greyish");
        m.insert("olive", "olive");  // Special case - stays as "olive"
        m.insert("white", "whitish");
        m.insert("black", "blackish");
        m
    };
}

/// Complete ISCC-NBS color classification result
#[derive(Debug, Clone)]
pub struct ISCC_NBS_Result {
    /// ISCC-NBS descriptor from CSV 'iscc-nbs-descriptor' column (e.g., "vivid")
    pub iscc_nbs_descriptor: String,
    /// ISCC-NBS color from CSV 'iscc-nbs-color' column (e.g., "red")
    pub iscc_nbs_color: String,
    /// ISCC-NBS formatter from CSV 'iscc-nbs-formatter' column (format string with placeholders)
    pub iscc_nbs_formatter: Option<String>,
    /// Revised color name from CSV 'revised-color' column
    pub revised_color: String,
    /// Revised descriptor constructed from revised_color + iscc_nbs_formatter
    pub revised_descriptor: String,
    /// Shade (last word of revised_color specifically)
    pub shade: String,
    /// ISCC-NBS color ID (renamed from color_number)
    pub iscc_nbs_color_id: u16,
}

impl ISCC_NBS_Result {
    /// Get the ISCC-NBS descriptor
    pub fn iscc_nbs_descriptor(&self) -> &str {
        &self.iscc_nbs_descriptor
    }
    
    /// Get the ISCC-NBS color
    pub fn iscc_nbs_color(&self) -> &str {
        &self.iscc_nbs_color
    }
    
    /// Get the ISCC-NBS formatter (if any)
    pub fn iscc_nbs_formatter(&self) -> Option<&str> {
        self.iscc_nbs_formatter.as_deref()
    }
    
    /// Get the revised color name
    pub fn revised_color(&self) -> &str {
        &self.revised_color
    }
    
    /// Get the revised descriptor (constructed from revised_color + iscc_nbs_formatter)
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
    
    /// Get the complete ISCC-NBS name (already complete descriptor, e.g., "vivid red")
    pub fn full_iscc_nbs_name(&self) -> String {
        // The descriptor field already contains the complete name (e.g., "vivid pink")
        // No need to combine with color field which would create "vivid pink pink"
        self.iscc_nbs_descriptor.clone()
    }
}

/// Color metadata stored separately from geometry for efficient memory usage
#[derive(Debug, Clone)]
pub struct ColorMetadata {
    /// ISCC-NBS color name from CSV 'iscc_nbs_color_name' column (e.g., "pink")
    pub iscc_nbs_color_name: String,
    /// ISCC-NBS formatter from CSV 'iscc_nbs_formatter' column (e.g., "vivid {0}")
    pub iscc_nbs_formatter: Option<String>,
    /// Alternative color name from CSV 'alt_color_name' column (e.g., "pink")
    pub alt_color_name: String,
}

/// Internal representation of an ISCC-NBS color category with its polygonal region
/// Metadata is stored separately to avoid duplication across wedges
#[derive(Debug, Clone)]
pub struct ISCC_NBS_Color {
    /// Color number from ISCC-NBS standard - used to lookup metadata
    pub color_number: u16,
    /// Polygon group number (for colors with multiple regions)
    pub polygon_group: u8,
    /// Hue range (e.g., "1R", "7R") - will be split into adjacent planes
    pub hue_range: (String, String),
    /// Polygon defining the color region in Munsell value-chroma space
    pub polygon: Polygon<f64>,
}

/// ISCC-NBS color naming engine with proper boundary disambiguation and caching
pub struct ISCC_NBS_Classifier {
    /// Mechanical wedge system for deterministic hue-based classification
    pub wedge_system: crate::mechanical_wedges::MechanicalWedgeSystem,
    /// Metadata lookup table - stores metadata once per color number instead of duplicating in each wedge
    color_metadata: HashMap<u16, ColorMetadata>,
    /// Small LRU cache for successive lookups without repeated searches
    cache: std::cell::RefCell<HashMap<(String, String, String), Option<ISCC_NBS_Result>>>, // (hue, value_str, chroma_str) -> result
    /// Maximum cache size
    cache_max_size: usize,
}

/// Embedded ISCC-NBS data - no external files needed
const ISCC_NBS_POLYGON_DATA: &str = include_str!("../assets/ISCC-NBS-Definitions.csv");
const ISCC_NBS_COLOR_DATA: &str = include_str!("../assets/ISCC-NBS-Colors.csv");

impl ISCC_NBS_Classifier {
    /// Simple descriptor construction using CSV format strings and -ish dictionary lookup
    /// 
    /// # Arguments
    /// * `formatter` - Format string from CSV (e.g., "{0} vivid", "-ish white")
    /// * `color_name` - Base color name (e.g., "pink", "red")
    /// 
    /// # Returns
    /// The properly formatted ISCC-NBS descriptor
    pub fn construct_descriptor(&self, formatter: &str, color_name: &str) -> String {
        if formatter.contains("{0}") {
            // Standard case: "{0} vivid" → "pink vivid"
            formatter.replace("{0}", color_name)
        } else if formatter.starts_with("-ish") {
            // Special -ish case: "-ish white" → "pinkish white"
            let color_name_ish = COLOR_TO_ISH.get(color_name)
                .copied() // Convert &&str to &str
                .unwrap_or_else(|| {
                    // For unknown colors not in dictionary, add "ish"
                    color_name // This will be handled below
                });
            
            let suffix = &formatter[4..]; // Remove "-ish" prefix
            if suffix.trim().is_empty() {
                // Just "-ish" → "pinkish"
                color_name_ish.to_string()
            } else {
                // "-ish white" → "pinkish white"
                format!("{}{}", color_name_ish, suffix)
            }
        } else {
            // Fallback - just return the formatter as-is
            formatter.to_string()
        }
    }
    
    /// Create a new ISCC-NBS classifier using embedded data.
    ///
    /// Creates a classifier loaded with the standard ISCC-NBS color definitions
    /// for converting Munsell colors to common color names.
    ///
    /// # Returns
    /// Result containing the classifier or an error if data loading fails
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::ISCC_NBS_Classifier;
    /// 
    /// let classifier = ISCC_NBS_Classifier::new().expect("Failed to create classifier");
    /// ```
    pub fn new() -> Result<Self, MunsellError> {
        let csv_path = concat!(env!("CARGO_MANIFEST_DIR"), "/assets/ISCC-NBS-Definitions.csv");
        Self::from_csv(csv_path)
    }
    
    /// Create a new ISCC-NBS classifier from external CSV file.
    ///
    /// Loads color definitions from an external CSV file for testing or development.
    /// The CSV should follow the same format as the embedded ISCC-NBS data.
    ///
    /// # Arguments
    /// * `csv_path` - Path to the CSV file containing ISCC-NBS definitions
    ///
    /// # Returns
    /// Result containing the classifier or an error if file loading fails
    ///
    /// # Examples
    /// ```rust,no_run
    /// use munsellspace::ISCC_NBS_Classifier;
    /// 
    /// let classifier = ISCC_NBS_Classifier::from_csv("custom_colors.csv")?;
    /// # Ok::<(), Box<dyn std::error::Error>>(())
    /// ```
    pub fn from_csv(csv_path: &str) -> Result<Self, MunsellError> {
        let (colors, color_metadata) = Self::load_iscc_data(csv_path)?;
        let mut wedge_system = MechanicalWedgeSystem::new();
        
        // Distribute all polygons into the mechanical wedge system
        for polygon in colors {
            wedge_system.distribute_polygon(polygon)?;
        }
        
        Ok(ISCC_NBS_Classifier { 
            wedge_system,
            color_metadata,
            cache: std::cell::RefCell::new(HashMap::new()),
            cache_max_size: 256,
        })
    }
    
    /// Check if a hue represents an achromatic (neutral) color.
    /// Achromatic colors have family "N" indicating no hue.
    ///
    /// # Arguments
    /// * `hue` - Munsell hue string (e.g., "N", "5R", "2.5YR")
    ///
    /// # Returns
    /// true if the color is achromatic (neutral), false otherwise
    fn is_achromatic(&self, hue: &str) -> bool {
        let hue = hue.trim().to_uppercase();
        // Check for various neutral notations:
        // - Just "N"
        // - Numeric prefix: "0N", "0.0N", etc.
        // - Just checking if it contains only digits/dots before "N"
        if hue == "N" {
            return true;
        }
        
        // Check if it ends with N and everything before it is numeric (digits or decimal point)
        if let Some(n_pos) = hue.rfind('N') {
            let prefix = &hue[..n_pos];
            // Allow empty prefix (just "N") or numeric prefix (like "0", "0.0", etc.)
            return prefix.is_empty() || prefix.chars().all(|c| c.is_ascii_digit() || c == '.');
        }
        
        false
    }
    
    /// Classify an achromatic (neutral) color based on its value.
    /// Maps value ranges to specific ISCC-NBS neutral color categories.
    ///
    /// # Arguments
    /// * `value` - Munsell value (lightness) from 0.0 to 10.0
    ///
    /// # Returns
    /// Result containing Some(ISCC_NBS_Result) for the appropriate neutral color
    fn classify_achromatic(&self, value: f64) -> Result<Option<ISCC_NBS_Result>, MunsellError> {
        let color_number = if value >= 0.0 && value <= 2.5 {
            267 // black
        } else if value > 2.5 && value <= 4.5 {
            266 // dark gray
        } else if value > 4.5 && value <= 6.5 {
            265 // medium gray
        } else if value > 6.5 && value <= 8.5 {
            264 // light gray
        } else if value > 8.5 && value <= 10.0 {
            263 // white
        } else {
            return Ok(None); // Value out of range
        };
        
        // Look up the metadata for this neutral color
        if let Some(metadata) = self.color_metadata.get(&color_number) {
            // Construct the full ISCC-NBS descriptor from formatter + color name
            let iscc_nbs_descriptor = if let Some(formatter) = &metadata.iscc_nbs_formatter {
                self.construct_descriptor(formatter, &metadata.iscc_nbs_color_name)
            } else {
                metadata.iscc_nbs_color_name.clone()
            };
            
            // Use alt_color_name as the revised color
            let revised_color = metadata.alt_color_name.clone();
            
            let result = ISCC_NBS_Result {
                iscc_nbs_descriptor,
                iscc_nbs_color: metadata.iscc_nbs_color_name.clone(),
                iscc_nbs_formatter: metadata.iscc_nbs_formatter.clone(),
                revised_color: revised_color.clone(),
                revised_descriptor: self.construct_revised_descriptor(&revised_color, &metadata.iscc_nbs_formatter),
                shade: self.extract_shade(&revised_color),
                iscc_nbs_color_id: color_number,
            };
            Ok(Some(result))
        } else {
            Ok(None)
        }
    }

    /// Classify a Munsell color using the ISCC-NBS system.
    ///
    /// Determines which ISCC-NBS color category (e.g., "vivid red") a Munsell color falls into
    /// by checking polygon containment in the standardized color regions.
    /// Handles achromatic (neutral) colors with special value-based mapping.
    ///
    /// # Arguments
    /// * `hue` - Munsell hue string (e.g., "5R", "2.5YR", "N" for neutral)
    /// * `value` - Munsell value (lightness) from 0.0 to 10.0
    /// * `chroma` - Munsell chroma (saturation) from 0.0 upwards
    ///
    /// # Returns
    /// Result containing Some(ISCC_NBS_Result) if classified, None if outside all regions
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::ISCC_NBS_Classifier;
    /// 
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ISCC_NBS_Classifier::new()?;
    /// 
    /// let result = classifier.classify_munsell("5R", 4.0, 14.0)?;
    /// if let Some(classification) = result {
    ///     println!("Color: {} {}", classification.iscc_nbs_descriptor, classification.iscc_nbs_color);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_munsell(&self, hue: &str, value: f64, chroma: f64) -> Result<Option<ISCC_NBS_Result>, MunsellError> {
        // Check for achromatic colors first
        if self.is_achromatic(hue) {
            return self.classify_achromatic(value);
        }
        
        // Round values to 4 decimal places for internal classification (reduces boundary collisions)
        // API output will still round to 1 decimal place for display
        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;
        
        // Create cache key using 4-decimal precision
        let cache_key = (hue.to_string(), format!("{:.4}", rounded_value), format!("{:.4}", rounded_chroma));
        
        // Check cache first
        {
            let cache = self.cache.borrow();
            if let Some(cached_result) = cache.get(&cache_key) {
                return Ok(cached_result.clone());
            }
        }
        
        // Use the mechanical wedge system for classification with rounded values
        if let Some(color) = self.wedge_system.classify_color(hue, rounded_value, rounded_chroma) {
            let result = Some(self.create_iscc_result(color));
            self.cache_result(cache_key, result.clone());
            return Ok(result);
        }
        
        let result = None;
        self.cache_result(cache_key, result.clone());
        Ok(result)
    }
    
    /// Find all ISCC-NBS colors that contain a given point.
    /// Unlike classify_munsell which returns the first match, this returns all overlapping colors.
    /// Useful for detecting overlapping polygon definitions.
    ///
    /// # Arguments
    /// * `hue` - Munsell hue string (e.g., "5R", "2.5YR", "N" for neutral)
    /// * `value` - Munsell value (lightness) from 0.0 to 10.0
    /// * `chroma` - Munsell chroma (saturation) from 0.0 upwards
    ///
    /// # Returns
    /// Vec of color numbers that contain this point
    pub fn find_all_colors_at_point(&self, hue: &str, value: f64, chroma: f64) -> Result<Vec<u16>, MunsellError> {
        // Check for achromatic colors first
        if self.is_achromatic(hue) {
            // For achromatic, use the value-based mapping
            let color_number = if value >= 0.0 && value <= 2.5 {
                267 // black
            } else if value > 2.5 && value <= 4.5 {
                266 // dark gray
            } else if value > 4.5 && value <= 6.5 {
                265 // medium gray
            } else if value > 6.5 && value <= 8.5 {
                264 // light gray
            } else if value > 8.5 && value <= 10.0 {
                263 // white
            } else {
                return Ok(vec![]); // Value out of range
            };
            
            // Verify the metadata exists
            if self.color_metadata.contains_key(&color_number) {
                return Ok(vec![color_number]);
            } else {
                return Ok(vec![]);
            }
        }
        
        // Round values to 4 decimal places for internal consistency
        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;
        
        // Use the mechanical wedge system to find ALL colors at this point
        let colors = self.wedge_system.find_all_colors_at_point(hue, rounded_value, rounded_chroma);
        Ok(colors)
    }
    
    /// Helper method to cache results with size management
    fn cache_result(&self, key: (String, String, String), result: Option<ISCC_NBS_Result>) {
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
    
    /// Get a polygon by its expected descriptor and hue wedge
    /// Returns the polygon if found in the specified wedge
    pub fn get_polygon_in_wedge(&self, hue: &str, expected_descriptor: &str) -> Option<&ISCC_NBS_Color> {
        // Determine which wedge this hue belongs to
        let wedge_key = self.wedge_system.find_wedge_for_hue(hue)?;
        
        // Get polygons in this wedge and find matching descriptor
        self.wedge_system.get_wedge_polygons(&wedge_key)?
            .iter()
            .find(|polygon| {
                // Check if this polygon's full descriptor matches the expected one using metadata lookup
                if let Some(metadata) = self.color_metadata.get(&polygon.color_number) {
                    // Construct the full ISCC-NBS descriptor from formatter + color name
                    let constructed_descriptor = if let Some(formatter) = &metadata.iscc_nbs_formatter {
                        self.construct_descriptor(formatter, &metadata.iscc_nbs_color_name)
                    } else {
                        metadata.iscc_nbs_color_name.clone()
                    };
                    constructed_descriptor.to_lowercase() == expected_descriptor.to_lowercase()
                } else {
                    false
                }
            })
    }
    
    /// Debug method to inspect wedge system state
    pub fn debug_wedge_lookup(&self, hue: &str, value: f64, chroma: f64) -> String {
        let wedge_stats = self.wedge_system.get_wedge_statistics();
        let mut debug_info = format!("=== WEDGE SYSTEM DEBUG ===\n");
        debug_info.push_str(&format!("Input: hue={}, value={}, chroma={}\n", hue, value, chroma));
        debug_info.push_str(&format!("Total wedges: {}\n", wedge_stats.total_wedges));
        debug_info.push_str(&format!("Total polygons: {}\n", wedge_stats.total_polygons));
        
        // Try to get the specific wedge for this hue
        if let Some(expected_wedge) = self.debug_find_expected_wedge(hue) {
            debug_info.push_str(&format!("Expected wedge for {}: {}\n", hue, expected_wedge));
            
            // Check if this wedge exists and has polygons
            if let Some(polygon_count) = wedge_stats.wedge_counts.get(&expected_wedge) {
                debug_info.push_str(&format!("Wedge {} exists with {} polygons\n", expected_wedge, polygon_count));
                
                // Look for color 43 specifically
                if let Some(color_43_info) = self.debug_find_color_43(&expected_wedge) {
                    debug_info.push_str(&format!("Color 43 found: {}\n", color_43_info));
                } else {
                    debug_info.push_str("Color 43 NOT found in this wedge\n");
                }
            } else {
                debug_info.push_str(&format!("❌ Wedge {} DOES NOT EXIST\n", expected_wedge));
            }
        } else {
            debug_info.push_str(&format!("❌ Could not determine expected wedge for hue {}\n", hue));
        }
        
        debug_info
    }
    
    /// Helper to determine expected wedge key
    fn debug_find_expected_wedge(&self, hue: &str) -> Option<String> {
        // Parse the hue to determine expected wedge
        if let Ok((hue_number, family)) = Self::parse_hue_static(hue) {
            let wedge_num = if hue_number > 9.0 && hue_number <= 10.0 {
                10
            } else {
                ((hue_number.ceil() as u8).max(1)).min(10)
            };
            
            let wedge_hue = format!("{}{}", wedge_num, family);
            
            // For 10R, next should be 1YR
            if wedge_hue == "10R" {
                Some("10R→1YR".to_string())
            } else {
                // This is simplified - need full logic for all wedge transitions
                Some(format!("{}→?", wedge_hue))
            }
        } else {
            None
        }
    }
    
    /// Helper to find color 43 in a specific wedge
    fn debug_find_color_43(&self, wedge_key: &str) -> Option<String> {
        // Check if color 43 exists in the specified wedge
        if let Some(contents) = self.wedge_system.debug_wedge_contents(wedge_key) {
            for content in &contents {
                if content.starts_with("Color 43:") {
                    return Some(content.clone());
                }
            }
            Some(format!("Color 43 NOT found in wedge {} (has {} colors)", wedge_key, contents.len()))
        } else {
            Some(format!("Wedge {} does not exist", wedge_key))
        }
    }
    
    /// Public debug methods for system inspection
    pub fn debug_find_all_color_43(&self) -> Vec<String> {
        self.wedge_system.debug_find_color(43)
    }
    
    pub fn debug_wedge_contents(&self, wedge_key: &str) -> Option<Vec<String>> {
        self.wedge_system.debug_wedge_contents(wedge_key)
    }
    
    pub fn debug_test_point(&self, wedge_key: &str, color_number: u16, value: f64, chroma: f64) -> Option<bool> {
        self.wedge_system.debug_point_test(wedge_key, color_number, value, chroma)
    }
    
    pub fn debug_test_point_detailed(&self, wedge_key: &str, color_number: u16, value: f64, chroma: f64) -> Option<String> {
        self.wedge_system.debug_point_test_detailed(wedge_key, color_number, value, chroma)
    }
    
    /// Classify a MunsellColor object using the ISCC-NBS system.
    ///
    /// Convenience method for classifying a MunsellColor struct directly.
    /// Handles both chromatic and neutral colors appropriately.
    ///
    /// # Arguments
    /// * `munsell` - MunsellColor object to classify
    ///
    /// # Returns
    /// Result containing Some(ISCC_NBS_Result) if classified, None if neutral or unclassifiable
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::{ISCC_NBS_Classifier, MunsellColor};
    /// 
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ISCC_NBS_Classifier::new()?;
    /// let munsell = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
    /// 
    /// let result = classifier.classify_munsell_color(&munsell)?;
    /// if let Some(classification) = result {
    ///     println!("Classification: {}", classification.revised_descriptor);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_munsell_color(&self, munsell: &crate::types::MunsellColor) -> Result<Option<ISCC_NBS_Result>, MunsellError> {
        // Handle neutral colors (no hue/chroma)
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            self.classify_munsell(hue, munsell.value, chroma)
        } else {
            // Neutral color - handle separately or return None
            // For now, return None as neutrals may need special handling
            Ok(None)
        }
    }
    
    /// Classify an sRGB color using the ISCC-NBS system.
    ///
    /// Convenience method that first converts sRGB to Munsell, then classifies
    /// using the ISCC-NBS color naming system.
    ///
    /// # Arguments
    /// * `rgb` - RGB color as [R, G, B] array with components 0-255
    ///
    /// # Returns
    /// Result containing Some(ISCC_NBS_Result) if classified, None if unclassifiable
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::ISCC_NBS_Classifier;
    /// 
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ISCC_NBS_Classifier::new()?;
    /// 
    /// let result = classifier.classify_srgb([255, 0, 0])?; // Pure red
    /// if let Some(classification) = result {
    ///     println!("Red RGB is: {} {}", classification.iscc_nbs_descriptor, classification.iscc_nbs_color);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_srgb(&self, rgb: [u8; 3]) -> Result<Option<ISCC_NBS_Result>, MunsellError> {
        use crate::MunsellConverter;
        
        // Convert sRGB to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.srgb_to_munsell(rgb)?;
        
        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }
    
    /// Classify a Lab color using the ISCC-NBS system.
    ///
    /// Convenience method that first converts Lab to Munsell, then classifies
    /// using the ISCC-NBS color naming system.
    ///
    /// # Arguments
    /// * `lab` - Lab color as [L*, a*, b*] array where L* is 0-100, a* and b* are typically -128 to +128
    ///
    /// # Returns
    /// Result containing Some(ISCC_NBS_Result) if classified, None if unclassifiable
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::ISCC_NBS_Classifier;
    /// 
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ISCC_NBS_Classifier::new()?;
    /// 
    /// let result = classifier.classify_lab([53.23, 80.11, 67.22])?; // Bright red
    /// if let Some(classification) = result {
    ///     println!("Lab color is: {} {}", classification.iscc_nbs_descriptor, classification.iscc_nbs_color);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_lab(&self, lab: [f64; 3]) -> Result<Option<ISCC_NBS_Result>, MunsellError> {
        use crate::MunsellConverter;
        
        // Convert Lab to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.lab_to_munsell(lab)?;
        
        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }
    
    /// Classify a hex color using the ISCC-NBS system.
    ///
    /// Convenience method that first converts hex to sRGB, then to Munsell, then classifies
    /// using the ISCC-NBS color naming system.
    ///
    /// # Arguments
    /// * `hex` - Hex color string (e.g., "#FF0000", "FF0000", "#f00", "f00")
    ///
    /// # Returns
    /// Result containing Some(ISCC_NBS_Result) if classified, None if unclassifiable
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::ISCC_NBS_Classifier;
    /// 
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ISCC_NBS_Classifier::new()?;
    /// 
    /// let result = classifier.classify_hex("#FF0000")?; // Red
    /// if let Some(classification) = result {
    ///     println!("Hex #FF0000 is: {} {}", classification.iscc_nbs_descriptor, classification.iscc_nbs_color);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_hex(&self, hex: &str) -> Result<Option<ISCC_NBS_Result>, MunsellError> {
        // Parse hex string to RGB
        let rgb = self.parse_hex_to_rgb(hex)?;
        
        // Then classify using existing sRGB method
        self.classify_srgb(rgb)
    }
    
    /// Parse hex color string to RGB array
    fn parse_hex_to_rgb(&self, hex: &str) -> Result<[u8; 3], MunsellError> {
        let hex = hex.trim_start_matches('#');
        
        let rgb = if hex.len() == 3 {
            // Short form: "f00" -> "ff0000"
            let r = u8::from_str_radix(&hex[0..1].repeat(2), 16)
                .map_err(|_| MunsellError::ConversionError { 
                    message: format!("Invalid hex color format: {}", hex) 
                })?;
            let g = u8::from_str_radix(&hex[1..2].repeat(2), 16)
                .map_err(|_| MunsellError::ConversionError { 
                    message: format!("Invalid hex color format: {}", hex) 
                })?;
            let b = u8::from_str_radix(&hex[2..3].repeat(2), 16)
                .map_err(|_| MunsellError::ConversionError { 
                    message: format!("Invalid hex color format: {}", hex) 
                })?;
            [r, g, b]
        } else if hex.len() == 6 {
            // Long form: "ff0000"
            let r = u8::from_str_radix(&hex[0..2], 16)
                .map_err(|_| MunsellError::ConversionError { 
                    message: format!("Invalid hex color format: {}", hex) 
                })?;
            let g = u8::from_str_radix(&hex[2..4], 16)
                .map_err(|_| MunsellError::ConversionError { 
                    message: format!("Invalid hex color format: {}", hex) 
                })?;
            let b = u8::from_str_radix(&hex[4..6], 16)
                .map_err(|_| MunsellError::ConversionError { 
                    message: format!("Invalid hex color format: {}", hex) 
                })?;
            [r, g, b]
        } else {
            return Err(MunsellError::ConversionError { 
                message: format!("Invalid hex color length: {}. Expected 3 or 6 characters after #", hex.len()) 
            });
        };
        
        Ok(rgb)
    }
    
    /// Check if point is in polygon using ISCC-NBS boundary disambiguation rules
    fn point_in_iscc_polygon(&self, point: &Point<f64>, color: &ISCC_NBS_Color) -> Result<bool, MunsellError> {
        // First check: standard geometric containment (fast rejection)
        if !color.polygon.contains(point) {
            return Ok(false);
        }
        
        // Second check: Apply ISCC boundary rules for disambiguation
        let bounds = self.get_polygon_bounds(&color.polygon);
        let (chroma, value) = (point.x(), point.y()); // x=chroma, y=value
        
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
        
        // x=chroma, y=value in our coordinate system
        let chromas: Vec<f64> = coords.iter().map(|c| c.x).collect();
        let values: Vec<f64> = coords.iter().map(|c| c.y).collect();
        
        PolygonBounds {
            min_value: values.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
            max_value: values.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)),
            min_chroma: chromas.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
            max_chroma: chromas.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)),
        }
    }
    
    // OBSOLETE METHOD - Replaced by MechanicalWedgeSystem
    // This method is no longer needed since the wedge system handles hue mapping directly
    
    /// Create comprehensive ISCC-NBS result from color data using metadata lookup
    fn create_iscc_result(&self, color: &ISCC_NBS_Color) -> ISCC_NBS_Result {
        // Look up metadata for this color number
        if let Some(metadata) = self.color_metadata.get(&color.color_number) {
            // Construct the full ISCC-NBS descriptor from formatter + color name
            let iscc_nbs_descriptor = if let Some(formatter) = &metadata.iscc_nbs_formatter {
                self.construct_descriptor(formatter, &metadata.iscc_nbs_color_name)
            } else {
                metadata.iscc_nbs_color_name.clone()
            };
            
            // Use alt_color_name as the revised color (they're the same in the new format)
            let revised_color = metadata.alt_color_name.clone();
            
            // Extract shade from alt_color_name (last word specifically)
            let shade = self.extract_shade(&metadata.alt_color_name);
            
            // Construct revised descriptor from alt_color_name + iscc_nbs_formatter
            let revised_descriptor = self.construct_revised_descriptor(&metadata.alt_color_name, &metadata.iscc_nbs_formatter);
            
            ISCC_NBS_Result {
                iscc_nbs_descriptor,
                iscc_nbs_color: metadata.iscc_nbs_color_name.clone(),
                iscc_nbs_formatter: metadata.iscc_nbs_formatter.clone(),
                revised_color,
                revised_descriptor,
                shade,
                iscc_nbs_color_id: color.color_number,
            }
        } else {
            // Fallback if metadata is missing (should not happen with valid data)
            ISCC_NBS_Result {
                iscc_nbs_descriptor: "unknown".to_string(),
                iscc_nbs_color: "unknown".to_string(),
                iscc_nbs_formatter: None,
                revised_color: "unknown".to_string(),
                revised_descriptor: "unknown".to_string(),
                shade: "unknown".to_string(),
                iscc_nbs_color_id: color.color_number,
            }
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
    
    /// Construct revised descriptor from revised_color + iscc_nbs_formatter
    /// Using simple format string replacement with dictionary lookup
    fn construct_revised_descriptor(&self, revised_color: &str, iscc_nbs_formatter: &Option<String>) -> String {
        match iscc_nbs_formatter {
            None => revised_color.trim().to_string(),
            Some(formatter) => self.construct_descriptor(formatter, revised_color),
        }
    }
    
    
    /// Helper function to create data error
    fn data_error<S: Into<String>>(msg: S) -> MunsellError {
        MunsellError::ReferenceDataError { message: msg.into() }
    }
    
    /// Load ISCC-NBS data from embedded CSV strings
    fn load_embedded_data() -> Result<(Vec<ISCC_NBS_Color>, HashMap<u16, ColorMetadata>), MunsellError> {
        let polygons = Self::parse_polygon_csv_data(ISCC_NBS_POLYGON_DATA)?;
        let color_metadata = Self::parse_color_metadata_csv(ISCC_NBS_COLOR_DATA)?;
        Ok((polygons, color_metadata))
    }
    
    /// Load ISCC-NBS data from CSV files (for testing/development)
    fn load_iscc_data(polygon_csv_path: &str) -> Result<(Vec<ISCC_NBS_Color>, HashMap<u16, ColorMetadata>), MunsellError> {
        use std::fs;
        use std::path::Path;
        
        // Read polygon data
        let polygon_csv_content = fs::read_to_string(polygon_csv_path)
            .map_err(|e| MunsellError::ReferenceDataError { message: format!("Failed to read polygon CSV file: {}", e) })?;
        
        // Derive color metadata file path (same directory, different name)
        let polygon_path = Path::new(polygon_csv_path);
        let color_csv_path = polygon_path.parent()
            .unwrap_or(Path::new("."))
            .join("ISCC-NBS-Colors.csv");
            
        let color_csv_content = fs::read_to_string(&color_csv_path)
            .map_err(|e| MunsellError::ReferenceDataError { 
                message: format!("Failed to read color metadata CSV file {}: {}", color_csv_path.display(), e) 
            })?;
        
        let polygons = Self::parse_polygon_csv_data(&polygon_csv_content)?;
        let color_metadata = Self::parse_color_metadata_csv(&color_csv_content)?;
        Ok((polygons, color_metadata))
    }
    
    /// Parse color metadata CSV data into lookup table
    fn parse_color_metadata_csv(csv_content: &str) -> Result<HashMap<u16, ColorMetadata>, MunsellError> {
        use csv::Reader;
        
        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_metadata: HashMap<u16, ColorMetadata> = HashMap::new();
        
        // Parse CSV data: color_number,iscc_nbs_color_name,iscc_nbs_formatter,alt_color_name
        for result in reader.records() {
            let record = result
                .map_err(|e| MunsellError::ReferenceDataError { message: format!("CSV parsing error: {}", e) })?;
            
            let color_number: u16 = record.get(0)
                .ok_or_else(|| Self::data_error("Missing color_number".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid color_number: {}", e)))?;
                
            let iscc_nbs_color_name = record.get(1)
                .ok_or_else(|| Self::data_error("Missing iscc_nbs_color_name".to_string()))?
                .to_string();
                
            let iscc_nbs_formatter = record.get(2)
                .filter(|s| !s.is_empty())
                .map(|s| s.to_string());
                
            let alt_color_name = record.get(3)
                .ok_or_else(|| Self::data_error("Missing alt_color_name".to_string()))?
                .to_string();
            
            color_metadata.insert(color_number, ColorMetadata {
                iscc_nbs_color_name,
                iscc_nbs_formatter,
                alt_color_name,
            });
        }
        
        Ok(color_metadata)
    }
    
    /// Parse polygon CSV data and convert to polygons
    fn parse_polygon_csv_data(csv_content: &str) -> Result<Vec<ISCC_NBS_Color>, MunsellError> {
        use csv::Reader;
        use geo::{LineString, Coord};
        
        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_groups: std::collections::HashMap<(u16, u8), Vec<(f64, f64)>> = std::collections::HashMap::new();
        let mut polygon_metadata: std::collections::HashMap<(u16, u8), (String, String)> = std::collections::HashMap::new();
        
        // Parse CSV data and group points by color_number and polygon_id
        for result in reader.records() {
            let record = result
                .map_err(|e| MunsellError::ReferenceDataError { message: format!("CSV parsing error: {}", e) })?;
            
            // Parse CSV columns: color_number,polygon_id,point_id,hue1,hue2,chroma,value
            let color_number: u16 = record.get(0)
                .ok_or_else(|| Self::data_error("Missing color_number".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid color_number: {}", e)))?;
                
            let polygon_id: u8 = record.get(1)
                .ok_or_else(|| Self::data_error("Missing polygon_id".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid polygon_id: {}", e)))?;
                
            // Skip point_id (column 2) - not needed for processing
            
            let hue1 = record.get(3)
                .ok_or_else(|| Self::data_error("Missing hue1".to_string()))?
                .to_string();
                
            let hue2 = record.get(4)
                .ok_or_else(|| Self::data_error("Missing hue2".to_string()))?
                .to_string();
                
            let chroma: f64 = record.get(5)
                .ok_or_else(|| Self::data_error("Missing chroma".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid chroma: {}", e)))?;
                
            let value: f64 = record.get(6)
                .ok_or_else(|| Self::data_error("Missing value".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid value: {}", e)))?;
            
            // Store point in the appropriate group
            let key = (color_number, polygon_id);
            color_groups.entry(key).or_insert_with(Vec::new).push((value, chroma));
            
            // Store polygon-specific metadata (hue range)
            if !polygon_metadata.contains_key(&key) {
                polygon_metadata.insert(key, (hue1, hue2));
            }
        }
        
        // Convert grouped points to Polygon objects
        let mut colors = Vec::new();
        for ((color_number, polygon_id), points) in color_groups {
            if points.len() < 3 {
                return Err(Self::data_error(format!(
                    "Insufficient points for polygon: color {} polygon_id {} has {} points", 
                    color_number, polygon_id, points.len()
                )));
            }
            
            let (hue1, hue2) = polygon_metadata.get(&(color_number, polygon_id))
                .ok_or_else(|| Self::data_error("Missing polygon metadata".to_string()))?
                .clone();
            
            // Create LineString from points (geo requires a closed ring)
            // NOTE: Using consistent coordinate system: x=chroma, y=value (matches mechanical wedge system)
            let mut coords: Vec<Coord<f64>> = points.into_iter()
                .map(|(value, chroma)| Coord { x: chroma, y: value })
                .collect();
            
            // Ensure polygon is closed
            if coords.first() != coords.last() {
                if let Some(first) = coords.first().cloned() {
                    coords.push(first);
                }
            }
            
            let exterior = LineString::from(coords);
            let polygon = Polygon::new(exterior, vec![]); // No holes in ISCC-NBS polygons
            
            colors.push(ISCC_NBS_Color {
                color_number,
                polygon_group: polygon_id,
                hue_range: (hue1, hue2),
                polygon,
            });
        }
        
        Ok(colors)
    }
    
    /// Organize colors by adjacent Munsell planes for efficient lookup
    fn organize_by_adjacent_planes(colors: Vec<ISCC_NBS_Color>) -> HashMap<String, Vec<ISCC_NBS_Color>> {
        let mut plane_map: HashMap<String, Vec<ISCC_NBS_Color>> = HashMap::new();
        
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
    
    /// Split a hue range into adjacent plane identifiers using mechanical wedge system
    fn split_into_adjacent_planes(hue1: &str, hue2: &str) -> Vec<String> {
        // Parse the hue range endpoints
        let (num1, family1) = Self::parse_hue_static(hue1).unwrap_or((1.0, "R".to_string()));
        let (num2, family2) = Self::parse_hue_static(hue2).unwrap_or((1.0, "R".to_string()));
        
        // If same family, create individual wedges within family
        if family1 == family2 {
            Self::create_comprehensive_family_coverage(num1, num2, &family1)
        } else {
            // Cross-family range - create comprehensive coverage
            Self::create_comprehensive_cross_family_coverage(num1, &family1, num2, &family2)
        }
    }
    
    /// Create comprehensive coverage for same-family ranges (e.g., 1R to 4R)
    fn create_comprehensive_family_coverage(num1: f64, num2: f64, family: &str) -> Vec<String> {
        let mut wedges = Vec::new();
        
        // Ensure proper ordering (num1 should be <= num2)
        let (start, end) = if num1 <= num2 { (num1, num2) } else { (num2, num1) };
        
        // Create individual hue planes for every integer in the range
        let start_int = start.floor() as i32;
        let end_int = end.ceil() as i32;
        
        for i in start_int..=end_int {
            // Ensure valid hue numbers (1-10) with wraparound
            let hue_num = if i < 1 { i + 10 } else if i > 10 { i - 10 } else { i };
            let next_num = if hue_num == 10 { 1 } else { hue_num + 1 };
            
            // Create wedge key: "4R-5R"
            wedges.push(format!("{}{}-{}{}", hue_num, family, next_num, family));
            
            // Also add individual hue keys for backward compatibility
            wedges.push(format!("{}{}", hue_num, family));
            
            // Add fractional support for boundary cases
            if (i as f64 - start).abs() < 0.1 || (i as f64 - end).abs() < 0.1 {
                wedges.push(format!("{}.5{}", hue_num, family));
            }
        }
        
        // Add original range key for direct lookup
        wedges.push(format!("{}{}-{}{}", start as i32, family, end as i32, family));
        
        wedges
    }
    
    /// Create comprehensive coverage for cross-family ranges (e.g., 9RP to 2R)
    fn create_comprehensive_cross_family_coverage(num1: f64, family1: &str, num2: f64, family2: &str) -> Vec<String> {
        let mut wedges = Vec::new();
        
        // Define circular hue family order: [R,YR,Y,GY,G,BG,B,PB,P,RP]
        let hue_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        
        // Find family indices
        let family1_idx = hue_families.iter().position(|&f| f == family1).unwrap_or(0);
        let family2_idx = hue_families.iter().position(|&f| f == family2).unwrap_or(0);
        
        // Handle wraparound case (e.g., 9RP to 2R crosses from RP back to R)
        if family1_idx > family2_idx || (family1_idx == family2_idx && num1 > num2) {
            // First part: family1 from num1 to 10
            wedges.extend(Self::create_comprehensive_family_coverage(num1, 10.0, family1));
            
            // Middle families (if any)
            let mut current_idx = (family1_idx + 1) % hue_families.len();
            while current_idx != family2_idx {
                let family = hue_families[current_idx];
                wedges.extend(Self::create_comprehensive_family_coverage(1.0, 10.0, family));
                current_idx = (current_idx + 1) % hue_families.len();
            }
            
            // Last part: family2 from 1 to num2
            wedges.extend(Self::create_comprehensive_family_coverage(1.0, num2, family2));
        } else {
            // Normal range within the circular sequence
            let mut current_idx = family1_idx;
            while current_idx <= family2_idx {
                let family = hue_families[current_idx];
                if current_idx == family1_idx && current_idx == family2_idx {
                    // Same family
                    wedges.extend(Self::create_comprehensive_family_coverage(num1, num2, family));
                } else if current_idx == family1_idx {
                    // First family
                    wedges.extend(Self::create_comprehensive_family_coverage(num1, 10.0, family));
                } else if current_idx == family2_idx {
                    // Last family
                    wedges.extend(Self::create_comprehensive_family_coverage(1.0, num2, family));
                } else {
                    // Middle family
                    wedges.extend(Self::create_comprehensive_family_coverage(1.0, 10.0, family));
                }
                current_idx += 1;
            }
        }
        
        wedges
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
    
    // OBSOLETE METHODS - Replaced by MechanicalWedgeSystem
    // These methods are no longer needed since the wedge system handles classification directly
    /*
    /// Find the adjacent plane that contains the given hue using mechanical wedge system
    fn find_adjacent_plane_for_hue(&self, hue_number: f64, hue_family: &str) -> Result<String, MunsellError> {
        // This functionality is now handled by MechanicalWedgeSystem
        Err(MunsellError::ConversionError {
            message: "Method obsolete - use MechanicalWedgeSystem directly".to_string()
        })
    }
    */
    
    
}

/// Validation functions using geo crate  
pub mod validation {
    use super::{ISCC_NBS_Color, ValidationError};
    use geo::Intersects;
    
    /// Validate ISCC-NBS polygon data for integrity.
    ///
    /// Performs geometric validation on ISCC-NBS color polygons to ensure
    /// proper angles, boundaries, and absence of invalid intersections.
    ///
    /// # Arguments
    /// * `colors` - Slice of ISCC-NBS color definitions to validate
    ///
    /// # Returns
    /// Vector of validation errors found, empty if all polygons are valid
    ///
    /// # Examples
    /// ```rust,ignore
    /// use munsellspace::iscc::validation::validate_polygons;
    /// 
    /// // Note: This requires internal ISCC_NBS_Color which is not public
    /// let errors = validate_polygons(&color_data);
    /// if errors.is_empty() {
    ///     println!("All polygons are valid!");
    /// }
    /// ```
    pub fn validate_polygons(colors: &[ISCC_NBS_Color]) -> Vec<ValidationError> {
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