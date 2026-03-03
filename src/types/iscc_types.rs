//! ISCC-NBS naming types and polygon geometry for color classification.

use serde::{Deserialize, Serialize};
use std::fmt;
use super::munsell::MunsellColor;

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
    fn apply_naming_rules(
        color_name: &str,
        modifier: &Option<String>,
        revised_color: &str,
    ) -> String {
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
                    format!("{}ish white", apply_ish_rules(color_name))
                } else if mod_str == "-ish gray" {
                    format!("{}ish gray", apply_ish_rules(color_name))
                } else if mod_str.starts_with("dark -ish") {
                    let base_mod = mod_str.strip_prefix("dark -ish ").unwrap_or("");
                    format!("dark {}ish {}", apply_ish_rules(color_name), base_mod)
                } else {
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
    /// Create a new Munsell point for polygon boundary definition.
    ///
    /// # Arguments
    /// * `hue1` - Starting hue boundary (e.g., "1R")
    /// * `hue2` - Ending hue boundary (e.g., "4R")
    /// * `chroma` - Chroma coordinate value
    /// * `value` - Value coordinate (0-10)
    /// * `is_open_chroma` - Whether this represents an open-ended chroma region
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellPoint;
    ///
    /// let point = MunsellPoint::new(
    ///     "5R".to_string(),
    ///     "10R".to_string(),
    ///     14.0,
    ///     6.0,
    ///     false
    /// );
    /// assert_eq!(point.chroma, 14.0);
    /// assert_eq!(point.value, 6.0);
    /// ```
    pub fn new(hue1: String, hue2: String, chroma: f64, value: f64, is_open_chroma: bool) -> Self {
        Self {
            hue1,
            hue2,
            chroma,
            value,
            is_open_chroma,
        }
    }

    /// Parse chroma value from string, handling ">15" open-ended notation.
    ///
    /// # Arguments
    /// * `chroma_str` - Chroma value as string (e.g., "12.0" or ">15")
    ///
    /// # Returns
    /// Tuple of (chroma_value, is_open_ended)
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellPoint;
    ///
    /// let (chroma, open) = MunsellPoint::parse_chroma("12.5");
    /// assert_eq!(chroma, 12.5);
    /// assert!(!open);
    ///
    /// let (chroma, open) = MunsellPoint::parse_chroma(">15");
    /// assert_eq!(chroma, 15.0);
    /// assert!(open);
    /// ```
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
    /// Create a new ISCC-NBS color polygon.
    ///
    /// # Arguments
    /// * `color_number` - ISCC-NBS color number (1-267)
    /// * `descriptor` - Full ISCC-NBS descriptor (e.g., "vivid pink")
    /// * `color_name` - Base color name (e.g., "pink")
    /// * `modifier` - Optional modifier string
    /// * `revised_color` - Revised color name from dataset
    /// * `points` - Vector of boundary points defining the polygon
    ///
    /// # Examples
    /// ```
    /// use munsellspace::{IsccNbsPolygon, MunsellPoint};
    ///
    /// let points = vec![
    ///     MunsellPoint::new("5R".to_string(), "10R".to_string(), 14.0, 4.0, false),
    ///     MunsellPoint::new("10R".to_string(), "5YR".to_string(), 16.0, 5.0, false),
    /// ];
    ///
    /// let polygon = IsccNbsPolygon::new(
    ///     1,
    ///     "vivid red".to_string(),
    ///     "red".to_string(),
    ///     Some("vivid".to_string()),
    ///     "red".to_string(),
    ///     points
    /// );
    /// assert_eq!(polygon.color_number, 1);
    /// ```
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
        self.points.iter().any(|point| {
            point.chroma <= 1.0 && (point.value - value).abs() <= 1.0
        })
    }

    /// Determine if a point is within the polygon using ray casting algorithm.
    fn is_point_in_polygon(&self, hue_degrees: f64, value: f64, chroma: f64) -> bool {
        let mut hue_ranges: Vec<(f64, f64)> = Vec::new();
        let mut vc_points: Vec<(f64, f64)> = Vec::new();

        for point in &self.points {
            let hue1_deg = parse_hue_to_degrees(&point.hue1);
            let hue2_deg = parse_hue_to_degrees(&point.hue2);
            hue_ranges.push((hue1_deg, hue2_deg));
            vc_points.push((point.value, point.chroma));
        }

        let hue_in_range = hue_ranges.iter().any(|(h1, h2)| {
            is_hue_in_circular_range(hue_degrees, *h1, *h2)
        });

        if !hue_in_range {
            return false;
        }

        ray_casting_point_in_polygon(value, chroma, &vc_points)
    }
}

// --- Geometry helpers ---

/// Convert Munsell hue notation to degrees (0-360).
pub(crate) fn parse_hue_to_degrees(hue: &str) -> f64 {
    let hue_families = [
        ("R", 0.0), ("YR", 36.0), ("Y", 72.0), ("GY", 108.0), ("G", 144.0),
        ("BG", 180.0), ("B", 216.0), ("PB", 252.0), ("P", 288.0), ("RP", 324.0),
    ];

    let family = hue_families
        .iter()
        .find(|(fam, _)| hue.ends_with(fam))
        .map(|(_, deg)| *deg)
        .unwrap_or(0.0);

    let number_str = hue.chars()
        .take_while(|c| c.is_ascii_digit() || *c == '.')
        .collect::<String>();

    let number = number_str.parse::<f64>().unwrap_or(5.0);

    // Each step is 3.6 degrees (36/10), centered at 5
    family + (number - 5.0) * 3.6
}

/// Check if a hue angle is within a circular range.
pub(crate) fn is_hue_in_circular_range(hue: f64, start: f64, end: f64) -> bool {
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
pub(crate) fn ray_casting_point_in_polygon(
    test_x: f64,
    test_y: f64,
    vertices: &[(f64, f64)],
) -> bool {
    let mut inside = false;
    let n = vertices.len();

    if n < 3 {
        return false;
    }

    let mut j = n - 1;
    for i in 0..n {
        let (xi, yi) = vertices[i];
        let (xj, yj) = vertices[j];

        if ((yi > test_y) != (yj > test_y))
            && (test_x < (xj - xi) * (test_y - yi) / (yj - yi) + xi)
        {
            inside = !inside;
        }
        j = i;
    }

    inside
}

#[cfg(test)]
mod tests {
    use super::*;

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

        let cloned = polygon.clone();
        assert_eq!(polygon.color_number, cloned.color_number);
        assert_eq!(polygon.color_name, cloned.color_name);
        assert_eq!(polygon.revised_color, cloned.revised_color);
        assert_eq!(polygon.points.len(), cloned.points.len());
    }
}
