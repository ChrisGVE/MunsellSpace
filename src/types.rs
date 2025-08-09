//! Core types for Munsell color space representation.

use serde::{Deserialize, Serialize};
use std::fmt;
use crate::error::{MunsellError, Result};

/// Represents an RGB color with 8-bit components.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct RgbColor {
    /// Red component (0-255)
    pub r: u8,
    /// Green component (0-255)
    pub g: u8,
    /// Blue component (0-255)
    pub b: u8,
}

impl RgbColor {
    /// Create a new RGB color.
    ///
    /// # Arguments
    /// * `r` - Red component (0-255)
    /// * `g` - Green component (0-255)
    /// * `b` - Blue component (0-255)
    ///
    /// # Examples
    /// ```
    /// use munsellspace::RgbColor;
    /// 
    /// let red = RgbColor::new(255, 0, 0);
    /// let green = RgbColor::new(0, 255, 0);
    /// let blue = RgbColor::new(0, 0, 255);
    /// ```
    pub fn new(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b }
    }
    
    /// Create an RGB color from an array.
    ///
    /// # Arguments
    /// * `rgb` - Array of [R, G, B] values
    ///
    /// # Examples
    /// ```
    /// use munsellspace::RgbColor;
    /// 
    /// let color = RgbColor::from_array([255, 128, 64]);
    /// assert_eq!(color.r, 255);
    /// assert_eq!(color.g, 128);
    /// assert_eq!(color.b, 64);
    /// ```
    pub fn from_array(rgb: [u8; 3]) -> Self {
        Self {
            r: rgb[0],
            g: rgb[1],
            b: rgb[2],
        }
    }
    
    /// Convert to an array representation.
    ///
    /// # Returns
    /// Array of [R, G, B] values
    ///
    /// # Examples
    /// ```
    /// use munsellspace::RgbColor;
    /// 
    /// let color = RgbColor::new(255, 128, 64);
    /// let array = color.to_array();
    /// assert_eq!(array, [255, 128, 64]);
    /// ```
    pub fn to_array(self) -> [u8; 3] {
        [self.r, self.g, self.b]
    }
    
    /// Check if the color is grayscale (R == G == B).
    ///
    /// # Returns
    /// `true` if all components are equal, `false` otherwise
    ///
    /// # Examples
    /// ```
    /// use munsellspace::RgbColor;
    /// 
    /// let gray = RgbColor::new(128, 128, 128);
    /// assert!(gray.is_grayscale());
    /// 
    /// let red = RgbColor::new(255, 0, 0);
    /// assert!(!red.is_grayscale());
    /// ```
    pub fn is_grayscale(self) -> bool {
        self.r == self.g && self.g == self.b
    }
}

impl fmt::Display for RgbColor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "RGB({}, {}, {})", self.r, self.g, self.b)
    }
}

impl From<[u8; 3]> for RgbColor {
    fn from(rgb: [u8; 3]) -> Self {
        Self::from_array(rgb)
    }
}

impl From<RgbColor> for [u8; 3] {
    fn from(color: RgbColor) -> Self {
        color.to_array()
    }
}

/// Represents a color in the Munsell color system.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct MunsellColor {
    /// Complete Munsell notation string (e.g., "5R 4.0/14.0" or "N 5.6/")
    pub notation: String,
    /// Hue component (None for neutral colors)
    pub hue: Option<String>,
    /// Value (lightness) component (0.0 to 10.0)
    pub value: f64,
    /// Chroma (saturation) component (None for neutral colors)
    pub chroma: Option<f64>,
}

impl MunsellColor {
    /// Create a new chromatic Munsell color.
    ///
    /// # Arguments
    /// * `hue` - Hue component (e.g., "5R", "2.5YR")
    /// * `value` - Value component (0.0 to 10.0)
    /// * `chroma` - Chroma component (0.0+)
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    /// 
    /// let red = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
    /// assert_eq!(red.notation, "5R 4.0/14.0");
    /// assert!(!red.is_neutral());
    /// ```
    pub fn new_chromatic(hue: String, value: f64, chroma: f64) -> Self {
        let notation = format!("{} {:.1}/{:.1}", hue, value, chroma);
        Self {
            notation,
            hue: Some(hue),
            value,
            chroma: Some(chroma),
        }
    }
    
    /// Create a new neutral (achromatic) Munsell color.
    ///
    /// # Arguments
    /// * `value` - Value component (0.0 to 10.0)
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    /// 
    /// let gray = MunsellColor::new_neutral(5.6);
    /// assert_eq!(gray.notation, "N 5.6/");
    /// assert!(gray.is_neutral());
    /// ```
    pub fn new_neutral(value: f64) -> Self {
        let notation = if value == 0.0 {
            "N 0.0".to_string()
        } else {
            format!("N {:.1}/", value)
        };
        Self {
            notation,
            hue: None,
            value,
            chroma: None,
        }
    }
    
    /// Parse a Munsell notation string into a MunsellColor.
    ///
    /// # Arguments
    /// * `notation` - Munsell notation string (e.g., "5R 4.0/14.0" or "N 5.6/")
    ///
    /// # Returns
    /// Result containing the parsed MunsellColor or an error
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    /// 
    /// let color = MunsellColor::from_notation("5R 4.0/14.0").unwrap();
    /// assert_eq!(color.hue, Some("5R".to_string()));
    /// assert_eq!(color.value, 4.0);
    /// assert_eq!(color.chroma, Some(14.0));
    /// 
    /// let gray = MunsellColor::from_notation("N 5.6/").unwrap();
    /// assert!(gray.is_neutral());
    /// ```
    pub fn from_notation(notation: &str) -> Result<Self> {
        let notation = notation.trim();
        
        // Handle neutral colors (e.g., "N 5.6/", "N 5.6", or "N 0.0")
        if notation.starts_with("N ") {
            let value_part = notation.strip_prefix("N ").unwrap().trim_end_matches('/');
            let value = value_part.parse::<f64>().map_err(|_| MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid value component in neutral color".to_string(),
            })?;
            
            if !(0.0..=10.0).contains(&value) {
                return Err(MunsellError::InvalidNotation {
                    notation: notation.to_string(),
                    reason: "Value must be between 0.0 and 10.0".to_string(),
                });
            }
            
            // Preserve original notation format
            return Ok(Self {
                notation: notation.to_string(),
                hue: None,
                value,
                chroma: None,
            });
        }
        
        // Handle chromatic colors (e.g., "5R 4.0/14.0")
        let parts: Vec<&str> = notation.split_whitespace().collect();
        if parts.len() != 2 {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Expected format: 'HUE VALUE/CHROMA' or 'N VALUE/'".to_string(),
            });
        }
        
        let hue = parts[0].to_string();
        
        // Validate hue format (should be number + valid hue family)
        if !is_valid_hue_format(&hue) {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid hue format. Expected format like '5R', '2.5YR', etc.".to_string(),
            });
        }
        
        let value_chroma = parts[1];
        
        if !value_chroma.contains('/') {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Missing '/' separator between value and chroma".to_string(),
            });
        }
        
        let value_chroma_parts: Vec<&str> = value_chroma.split('/').collect();
        if value_chroma_parts.len() != 2 {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid value/chroma format".to_string(),
            });
        }
        
        let value = value_chroma_parts[0].parse::<f64>().map_err(|_| MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Invalid value component".to_string(),
        })?;
        
        let chroma = value_chroma_parts[1].parse::<f64>().map_err(|_| MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Invalid chroma component".to_string(),
        })?;
        
        if !(0.0..=10.0).contains(&value) {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Value must be between 0.0 and 10.0".to_string(),
            });
        }
        
        if chroma < 0.0 {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Chroma must be non-negative".to_string(),
            });
        }
        
        Ok(Self::new_chromatic(hue, value, chroma))
    }
    
    /// Check if this is a neutral (achromatic) color.
    ///
    /// # Returns
    /// `true` if the color is neutral (no hue/chroma), `false` otherwise
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    /// 
    /// let gray = MunsellColor::new_neutral(5.6);
    /// assert!(gray.is_neutral());
    /// 
    /// let red = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
    /// assert!(!red.is_neutral());
    /// ```
    pub fn is_neutral(&self) -> bool {
        self.hue.is_none() || self.chroma.is_none()
    }
    
    /// Check if this is a chromatic color.
    ///
    /// # Returns
    /// `true` if the color has hue and chroma, `false` otherwise
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    /// 
    /// let red = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
    /// assert!(red.is_chromatic());
    /// 
    /// let gray = MunsellColor::new_neutral(5.6);
    /// assert!(!gray.is_chromatic());
    /// ```
    pub fn is_chromatic(&self) -> bool {
        !self.is_neutral()
    }
    
    /// Get the hue family (e.g., "R", "YR", "Y").
    ///
    /// # Returns
    /// Optional hue family string, None for neutral colors
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    /// 
    /// let red = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
    /// assert_eq!(red.hue_family(), Some("R".to_string()));
    /// 
    /// let yellow_red = MunsellColor::new_chromatic("2.5YR".to_string(), 6.0, 8.0);
    /// assert_eq!(yellow_red.hue_family(), Some("YR".to_string()));
    /// ```
    pub fn hue_family(&self) -> Option<String> {
        self.hue.as_ref().map(|h| {
            // Extract the alphabetic part (hue family)
            h.chars().filter(|c| c.is_alphabetic()).collect()
        })
    }
}

impl fmt::Display for MunsellColor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.notation)
    }
}

/// Represents an ISCC-NBS color name with all associated metadata.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct IsccNbsName {
    /// ISCC-NBS color number (1-267)
    pub color_number: u16,
    /// Full descriptor (e.g., "vivid pink")
    pub descriptor: String,
    /// Base color name (e.g., "pink")
    pub color_name: String,
    /// Optional modifier (e.g., "vivid", None for "black"/"white")
    pub modifier: Option<String>,
    /// Revised color name constructed from modifier rules
    pub revised_name: String,
    /// Shade (last word of revised name)
    pub shade: String,
}

impl IsccNbsName {
    /// Create a new ISCC-NBS color name.
    ///
    /// # Arguments
    /// * `color_number` - ISCC-NBS color number (1-267)
    /// * `descriptor` - Full ISCC-NBS descriptor
    /// * `color_name` - Base color name
    /// * `modifier` - Optional modifier string
    /// * `revised_color` - Revised color name from dataset
    ///
    /// # Examples
    /// ```
    /// use munsellspace::IsccNbsName;
    /// 
    /// let vivid_pink = IsccNbsName::new(
    ///     1,
    ///     "vivid pink".to_string(),
    ///     "pink".to_string(),
    ///     Some("vivid".to_string()),
    ///     "pink".to_string()
    /// );
    /// assert_eq!(vivid_pink.shade, "pink");
    /// ```
    pub fn new(
        color_number: u16,
        descriptor: String,
        color_name: String,
        modifier: Option<String>,
        revised_color: String,
    ) -> Self {
        // Apply ISCC-NBS naming transformation rules
        let revised_name = Self::apply_naming_rules(&color_name, &modifier, &revised_color);
        let shade = Self::extract_shade(&revised_name);
        
        Self {
            color_number,
            descriptor,
            color_name,
            modifier,
            revised_name,
            shade,
        }
    }
    
    /// Apply ISCC-NBS naming transformation rules.
    fn apply_naming_rules(color_name: &str, modifier: &Option<String>, revised_color: &str) -> String {
        match modifier.as_deref() {
            None => {
                // No modifier for white/black
                if color_name == "white" || color_name == "black" {
                    return color_name.to_string();
                }
                revised_color.to_string()
            }
            Some(mod_str) => {
                // Handle "-ish" transformation rules
                if mod_str == "-ish white" {
                    // "pink" + "-ish white" → "pinkish white"
                    format!("{}ish white", apply_ish_rules(color_name))
                } else if mod_str == "-ish gray" {
                    // "blue" + "-ish gray" → "bluish gray"
                    format!("{}ish gray", apply_ish_rules(color_name))
                } else if mod_str.starts_with("dark -ish") {
                    // "green" + "dark -ish gray" → "dark greenish gray"
                    let base_mod = mod_str.strip_prefix("dark -ish ").unwrap_or("");
                    format!("dark {}ish {}", apply_ish_rules(color_name), base_mod)
                } else {
                    // Standard modifier + color
                    format!("{} {}", mod_str, revised_color)
                }
            }
        }
    }
    
    /// Extract the shade (last word) from a revised color name.
    fn extract_shade(revised_name: &str) -> String {
        revised_name
            .split_whitespace()
            .last()
            .unwrap_or(revised_name)
            .to_string()
    }
}

/// Apply "-ish" transformation rules with special cases.
fn apply_ish_rules(color_name: &str) -> String {
    match color_name {
        "red" => "reddish".to_string(),  // Double 'd' exception
        "olive" => "olive".to_string(),  // No change exception
        other => format!("{}ish", other),
    }
}

impl fmt::Display for IsccNbsName {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.descriptor)
    }
}

/// Represents a point in Munsell color space for polygon definition.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct MunsellPoint {
    /// Starting hue boundary (e.g., "1R")
    pub hue1: String,
    /// Ending hue boundary (e.g., "4R")
    pub hue2: String,
    /// Chroma coordinate (can be >15 for open-ended regions)
    pub chroma: f64,
    /// Value coordinate (0-10)
    pub value: f64,
    /// Whether this represents an open-ended chroma region
    pub is_open_chroma: bool,
}

impl MunsellPoint {
    /// Create a new Munsell point.
    pub fn new(hue1: String, hue2: String, chroma: f64, value: f64, is_open_chroma: bool) -> Self {
        Self {
            hue1,
            hue2,
            chroma,
            value,
            is_open_chroma,
        }
    }
    
    /// Parse chroma value handling ">15" notation.
    pub fn parse_chroma(chroma_str: &str) -> (f64, bool) {
        if chroma_str.starts_with('>') {
            let value = chroma_str[1..].parse::<f64>().unwrap_or(15.0);
            (value, true)
        } else {
            let value = chroma_str.parse::<f64>().unwrap_or(0.0);
            (value, false)
        }
    }
}

/// Represents an ISCC-NBS color polygon in Munsell space.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct IsccNbsPolygon {
    /// ISCC-NBS color number (1-267)
    pub color_number: u16,
    /// ISCC-NBS descriptor
    pub descriptor: String,
    /// Base color name
    pub color_name: String,
    /// Optional modifier
    pub modifier: Option<String>,
    /// Revised color name
    pub revised_color: String,
    /// Polygon boundary points
    pub points: Vec<MunsellPoint>,
}

impl IsccNbsPolygon {
    /// Create a new ISCC-NBS polygon.
    pub fn new(
        color_number: u16,
        descriptor: String,
        color_name: String,
        modifier: Option<String>,
        revised_color: String,
        points: Vec<MunsellPoint>,
    ) -> Self {
        Self {
            color_number,
            descriptor,
            color_name,
            modifier,
            revised_color,
            points,
        }
    }
    
    /// Check if a Munsell color point is contained within this polygon.
    ///
    /// # Arguments
    /// * `munsell` - The Munsell color to test
    ///
    /// # Returns
    /// `true` if the point is within the polygon boundaries
    pub fn contains_point(&self, munsell: &MunsellColor) -> bool {
        // Handle neutral colors
        if munsell.is_neutral() {
            return self.contains_neutral_point(munsell.value);
        }
        
        let hue = munsell.hue.as_ref().unwrap();
        let value = munsell.value;
        let chroma = munsell.chroma.unwrap_or(0.0);
        
        // Convert hue to degrees for comparison
        let hue_degrees = parse_hue_to_degrees(hue);
        
        // Check if point is within any of the polygon's hue-value-chroma regions
        self.is_point_in_polygon(hue_degrees, value, chroma)
    }
    
    /// Check if a neutral color point is within this polygon.
    fn contains_neutral_point(&self, value: f64) -> bool {
        // Neutral colors (N) typically map to gray categories or white/black
        // For simplicity, check if any polygon point has chroma close to 0
        self.points.iter().any(|point| {
            point.chroma <= 1.0 && (point.value - value).abs() <= 1.0
        })
    }
    
    /// Determine if a point is within the polygon using ray casting algorithm.
    fn is_point_in_polygon(&self, hue_degrees: f64, value: f64, chroma: f64) -> bool {
        // For each polygon region, check hue range and value-chroma boundaries
        let mut hue_ranges: Vec<(f64, f64)> = Vec::new();
        let mut vc_points: Vec<(f64, f64)> = Vec::new();
        
        // Extract hue ranges and value-chroma points
        for point in &self.points {
            let hue1_deg = parse_hue_to_degrees(&point.hue1);
            let hue2_deg = parse_hue_to_degrees(&point.hue2);
            hue_ranges.push((hue1_deg, hue2_deg));
            vc_points.push((point.value, point.chroma));
        }
        
        // Check if hue is within any of the hue ranges
        let hue_in_range = hue_ranges.iter().any(|(h1, h2)| {
            is_hue_in_circular_range(hue_degrees, *h1, *h2)
        });
        
        if !hue_in_range {
            return false;
        }
        
        // Use ray casting algorithm for value-chroma polygon
        ray_casting_point_in_polygon(value, chroma, &vc_points)
    }
}

/// Convert Munsell hue notation to degrees (0-360).
fn parse_hue_to_degrees(hue: &str) -> f64 {
    let hue_families = [
        ("R", 0.0), ("YR", 36.0), ("Y", 72.0), ("GY", 108.0), ("G", 144.0),
        ("BG", 180.0), ("B", 216.0), ("PB", 252.0), ("P", 288.0), ("RP", 324.0)
    ];
    
    // Extract family from end of hue string
    let family = hue_families
        .iter()
        .find(|(fam, _)| hue.ends_with(fam))
        .map(|(_, deg)| *deg)
        .unwrap_or(0.0);
    
    // Extract number from beginning
    let number_str = hue.chars()
        .take_while(|c| c.is_ascii_digit() || *c == '.')
        .collect::<String>();
    
    let number = number_str.parse::<f64>().unwrap_or(5.0);
    
    // Each step is 3.6 degrees (36/10), centered at 5
    family + (number - 5.0) * 3.6
}

/// Check if a hue angle is within a circular range.
fn is_hue_in_circular_range(hue: f64, start: f64, end: f64) -> bool {
    let normalized_hue = hue % 360.0;
    let normalized_start = start % 360.0;
    let normalized_end = end % 360.0;
    
    if normalized_start <= normalized_end {
        normalized_hue >= normalized_start && normalized_hue <= normalized_end
    } else {
        // Range crosses 0/360 boundary
        normalized_hue >= normalized_start || normalized_hue <= normalized_end
    }
}

/// Ray casting algorithm to determine if a point is inside a polygon.
fn ray_casting_point_in_polygon(test_x: f64, test_y: f64, vertices: &[(f64, f64)]) -> bool {
    let mut inside = false;
    let n = vertices.len();
    
    if n < 3 {
        return false;
    }
    
    let mut j = n - 1;
    for i in 0..n {
        let (xi, yi) = vertices[i];
        let (xj, yj) = vertices[j];
        
        if ((yi > test_y) != (yj > test_y)) &&
           (test_x < (xj - xi) * (test_y - yi) / (yj - yi) + xi) {
            inside = !inside;
        }
        j = i;
    }
    
    inside
}

/// Validates that a hue string has the correct format (number + valid hue family).
fn is_valid_hue_format(hue: &str) -> bool {
    // Valid hue families
    let valid_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    
    // Check if hue ends with a valid family
    let has_valid_family = valid_families.iter().any(|&family| hue.ends_with(family));
    if !has_valid_family {
        return false;
    }
    
    // Find which family it ends with
    let family = valid_families.iter()
        .find(|&&family| hue.ends_with(family))
        .unwrap();
    
    // Extract the numeric part
    let numeric_part = hue.strip_suffix(family).unwrap_or("");
    
    // Check if numeric part is empty or invalid
    if numeric_part.is_empty() {
        return false;
    }
    
    // Parse numeric part - should be a valid float in range 0.0-10.0  
    match numeric_part.parse::<f64>() {
        Ok(num) => num > 0.0 && num <= 10.0,
        Err(_) => false,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rgb_color() {
        let color = RgbColor::new(255, 128, 64);
        assert_eq!(color.r, 255);
        assert_eq!(color.g, 128);
        assert_eq!(color.b, 64);
        assert!(!color.is_grayscale());
        
        let gray = RgbColor::new(128, 128, 128);
        assert!(gray.is_grayscale());
    }

    #[test]
    fn test_munsell_color_chromatic() {
        let color = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        assert_eq!(color.notation, "5R 4.0/14.0");
        assert!(!color.is_neutral());
        assert!(color.is_chromatic());
        assert_eq!(color.hue_family(), Some("R".to_string()));
    }

    #[test]
    fn test_munsell_color_neutral() {
        let color = MunsellColor::new_neutral(5.6);
        assert_eq!(color.notation, "N 5.6/");
        assert!(color.is_neutral());
        assert!(!color.is_chromatic());
        assert_eq!(color.hue_family(), None);
    }

    #[test]
    fn test_munsell_parsing() {
        let color = MunsellColor::from_notation("5R 4.0/14.0").unwrap();
        assert_eq!(color.hue, Some("5R".to_string()));
        assert_eq!(color.value, 4.0);
        assert_eq!(color.chroma, Some(14.0));

        let gray = MunsellColor::from_notation("N 5.6/").unwrap();
        assert!(gray.is_neutral());
        assert_eq!(gray.value, 5.6);
    }

    #[test]
    fn test_rgb_color_edge_cases() {
        // Test boundary values
        let black = RgbColor::new(0, 0, 0);
        assert!(black.is_grayscale());
        assert_eq!(black.to_array(), [0, 0, 0]);
        
        let white = RgbColor::new(255, 255, 255);
        assert!(white.is_grayscale());
        assert_eq!(white.to_array(), [255, 255, 255]);
        
        // Test various grayscale values
        for i in 0..=255 {
            let gray = RgbColor::new(i, i, i);
            assert!(gray.is_grayscale());
        }
        
        // Test non-grayscale combinations
        let red = RgbColor::new(255, 0, 0);
        assert!(!red.is_grayscale());
        
        let green = RgbColor::new(0, 255, 0);
        assert!(!green.is_grayscale());
        
        let blue = RgbColor::new(0, 0, 255);
        assert!(!blue.is_grayscale());
    }

    #[test]
    fn test_munsell_color_edge_cases() {
        // Test zero chroma
        let zero_chroma = MunsellColor::new_chromatic("5R".to_string(), 5.0, 0.0);
        assert_eq!(zero_chroma.notation, "5R 5.0/0.0");
        assert!(zero_chroma.is_chromatic());
        
        // Test high chroma
        let high_chroma = MunsellColor::new_chromatic("5R".to_string(), 5.0, 20.0);
        assert_eq!(high_chroma.notation, "5R 5.0/20.0");
        
        // Test boundary values
        let min_value = MunsellColor::new_chromatic("5R".to_string(), 0.0, 10.0);
        assert_eq!(min_value.value, 0.0);
        
        let max_value = MunsellColor::new_chromatic("5R".to_string(), 10.0, 10.0);
        assert_eq!(max_value.value, 10.0);
    }

    #[test]
    fn test_munsell_color_neutral_edge_cases() {
        // Test boundary neutral values
        let black_neutral = MunsellColor::new_neutral(0.0);
        assert_eq!(black_neutral.notation, "N 0.0");
        assert!(black_neutral.is_neutral());
        assert!(!black_neutral.is_chromatic());
        
        let white_neutral = MunsellColor::new_neutral(10.0);
        assert_eq!(white_neutral.notation, "N 10.0/");
        
        // Test fractional values
        let mid_neutral = MunsellColor::new_neutral(5.5);
        assert_eq!(mid_neutral.notation, "N 5.5/");
    }

    #[test]
    fn test_munsell_parsing_variants() {
        // Test different hue families
        let hue_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        for family in &hue_families {
            let notation = format!("5{} 5.0/10.0", family);
            let color = MunsellColor::from_notation(&notation).unwrap();
            assert_eq!(color.hue_family(), Some(family.to_string()));
            assert_eq!(color.value, 5.0);
            assert_eq!(color.chroma, Some(10.0));
        }
        
        // Test different hue numbers
        for hue_num in [2.5, 5.0, 7.5, 10.0] {
            let notation = format!("{}R 5.0/10.0", hue_num);
            let color = MunsellColor::from_notation(&notation).unwrap();
            assert!(color.hue.as_ref().unwrap().contains("R"));
        }
        
        // Test decimal values
        let precise = MunsellColor::from_notation("5.5R 6.25/12.75").unwrap();
        assert_eq!(precise.value, 6.25);
        assert_eq!(precise.chroma, Some(12.75));
    }

    #[test]
    fn test_munsell_parsing_invalid_cases() {
        // Test invalid notations
        assert!(MunsellColor::from_notation("").is_err());
        assert!(MunsellColor::from_notation("invalid").is_err());
        assert!(MunsellColor::from_notation("5X 5.0/10.0").is_err()); // Invalid hue family
        assert!(MunsellColor::from_notation("R 5.0/10.0").is_err()); // Missing hue number
        assert!(MunsellColor::from_notation("5R /10.0").is_err()); // Missing value
        assert!(MunsellColor::from_notation("5R 5.0/").is_err()); // Missing chroma for chromatic
        assert!(MunsellColor::from_notation("5R -1.0/10.0").is_err()); // Negative value
        assert!(MunsellColor::from_notation("5R 5.0/-1.0").is_err()); // Negative chroma
        assert!(MunsellColor::from_notation("N /").is_err()); // Missing value for neutral
        assert!(MunsellColor::from_notation("N 5.0/10.0").is_err()); // Chroma for neutral
    }

    #[test]
    fn test_munsell_color_display() {
        let chromatic = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        assert_eq!(format!("{}", chromatic), "5R 4.0/14.0");
        
        let neutral = MunsellColor::new_neutral(5.6);
        assert_eq!(format!("{}", neutral), "N 5.6/");
    }

    #[test]
    fn test_munsell_color_debug() {
        let color = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let debug_str = format!("{:?}", color);
        assert!(debug_str.contains("MunsellColor"));
        assert!(debug_str.contains("5R"));
        assert!(debug_str.contains("4"));
        assert!(debug_str.contains("14"));
    }

    #[test]
    fn test_munsell_color_clone() {
        let original = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let cloned = original.clone();
        assert_eq!(original.notation, cloned.notation);
        assert_eq!(original.hue, cloned.hue);
        assert_eq!(original.value, cloned.value);
        assert_eq!(original.chroma, cloned.chroma);
    }

    #[test]
    fn test_rgb_color_display() {
        let color = RgbColor::new(255, 128, 64);
        assert_eq!(format!("{}", color), "RGB(255, 128, 64)");
    }

    #[test]
    fn test_rgb_color_debug() {
        let color = RgbColor::new(255, 128, 64);
        let debug_str = format!("{:?}", color);
        assert!(debug_str.contains("RgbColor"));
        assert!(debug_str.contains("255"));
        assert!(debug_str.contains("128"));
        assert!(debug_str.contains("64"));
    }

    #[test]
    fn test_rgb_color_clone() {
        let original = RgbColor::new(255, 128, 64);
        let cloned = original.clone();
        assert_eq!(original.r, cloned.r);
        assert_eq!(original.g, cloned.g);
        assert_eq!(original.b, cloned.b);
    }

    #[test]
    fn test_rgb_color_equality() {
        let color1 = RgbColor::new(255, 128, 64);
        let color2 = RgbColor::new(255, 128, 64);
        let color3 = RgbColor::new(255, 128, 65);
        
        assert_eq!(color1, color2);
        assert_ne!(color1, color3);
    }

    #[test]
    fn test_munsell_color_equality() {
        let color1 = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let color2 = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let color3 = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.1);
        
        assert_eq!(color1, color2);
        assert_ne!(color1, color3);
    }

    #[test]
    fn test_munsell_point_functionality() {
        let point = MunsellPoint {
            hue1: "5R".to_string(),
            hue2: "7R".to_string(),
            value: 6.0,
            chroma: 12.0,
            is_open_chroma: false,
        };
        
        assert_eq!(point.hue1, "5R");
        assert_eq!(point.hue2, "7R");
        assert_eq!(point.value, 6.0);
        assert_eq!(point.chroma, 12.0);
        assert!(!point.is_open_chroma);
        
        // Test cloning
        let cloned = point.clone();
        assert_eq!(point.hue1, cloned.hue1);
        assert_eq!(point.hue2, cloned.hue2);
        assert_eq!(point.value, cloned.value);
        assert_eq!(point.chroma, cloned.chroma);
        assert_eq!(point.is_open_chroma, cloned.is_open_chroma);
    }

    #[test]
    fn test_iscc_nbs_name_functionality() {
        let name = IsccNbsName {
            color_number: 34,
            descriptor: "Strong".to_string(),
            color_name: "Red".to_string(),
            modifier: None,
            revised_name: "Strong Red".to_string(),
            shade: "Red".to_string(),
        };
        
        assert_eq!(name.color_number, 34);
        assert_eq!(name.color_name, "Red");
        assert_eq!(name.revised_name, "Strong Red");
        
        // Test cloning
        let cloned = name.clone();
        assert_eq!(name.color_number, cloned.color_number);
        assert_eq!(name.color_name, cloned.color_name);
        assert_eq!(name.revised_name, cloned.revised_name);
    }

    #[test]
    fn test_iscc_nbs_polygon_functionality() {
        let polygon = IsccNbsPolygon {
            color_number: 34,
            descriptor: "Strong".to_string(),
            color_name: "Red".to_string(),
            modifier: None,
            revised_color: "Strong Red".to_string(),
            points: vec![
                MunsellPoint {
                    hue1: "5R".to_string(),
                    hue2: "7R".to_string(),
                    value: 5.0,
                    chroma: 10.0,
                    is_open_chroma: false,
                }
            ],
        };
        
        assert_eq!(polygon.color_number, 34);
        assert_eq!(polygon.color_name, "Red");
        assert_eq!(polygon.revised_color, "Strong Red");
        assert_eq!(polygon.points.len(), 1);
        
        // Test cloning
        let cloned = polygon.clone();
        assert_eq!(polygon.color_number, cloned.color_number);
        assert_eq!(polygon.color_name, cloned.color_name);
        assert_eq!(polygon.revised_color, cloned.revised_color);
        assert_eq!(polygon.points.len(), cloned.points.len());
    }
}