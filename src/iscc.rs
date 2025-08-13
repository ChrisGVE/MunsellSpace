use crate::constants::{get_color_ish, get_achromatic_color_number, is_achromatic_hue};
use crate::error::MunsellError;
use crate::mechanical_wedges::MechanicalWedgeSystem;
use geo::Polygon;
use std::collections::HashMap;

/// Color metadata with on-the-fly descriptor construction
#[derive(Debug, Clone)]
pub struct ColorMetadata {
    /// ISCC-NBS color name from CSV 'iscc_nbs_color_name' column (e.g., "pink")
    pub iscc_nbs_color_name: String,
    /// ISCC-NBS formatter from CSV 'iscc_nbs_formatter' column (e.g., "vivid {0}")
    pub iscc_nbs_formatter: Option<String>,
    /// Alternative color name from CSV 'alt_color_name' column (e.g., "pink")
    pub alt_color_name: String,
    /// Color shade from CSV 'color_shade' column
    pub color_shade: String,
}

impl ColorMetadata {
    /// Construct the ISCC-NBS descriptor on the fly using the internal formatter
    pub fn iscc_nbs_descriptor(&self) -> String {
        if let Some(formatter) = &self.iscc_nbs_formatter {
            Self::construct_descriptor(formatter, &self.iscc_nbs_color_name)
        } else {
            self.iscc_nbs_color_name.clone()
        }
    }

    /// Construct the alternative color descriptor on the fly using the internal formatter
    pub fn alt_color_descriptor(&self) -> String {
        if let Some(formatter) = &self.iscc_nbs_formatter {
            Self::construct_descriptor(formatter, &self.alt_color_name)
        } else {
            self.alt_color_name.clone()
        }
    }

    /// Get the shade (loaded from CSV)
    pub fn shade(&self) -> &str {
        &self.color_shade
    }

    /// Static descriptor construction using CSV format strings and -ish dictionary lookup
    pub fn construct_descriptor(formatter: &str, color_name: &str) -> String {
        let color_name_ish = get_color_ish(color_name);
        
        // Replace {0} with color_name and {1} with color_name_ish
        formatter
            .replace("{0}", color_name)
            .replace("{1}", color_name_ish)
    }
}

/// Internal representation of an ISCC-NBS color category with its polygonal region
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
    cache: std::cell::RefCell<HashMap<(String, String, String), Option<u16>>>, // (hue, value_str, chroma_str) -> color_number
    /// Maximum cache size
    cache_max_size: usize,
}

/// Embedded ISCC-NBS data - no external files needed
const ISCC_NBS_POLYGON_DATA: &str = include_str!("../assets/ISCC-NBS-Definitions.csv");
const ISCC_NBS_COLOR_DATA: &str = include_str!("../assets/ISCC-NBS-Colors.csv");

impl ISCC_NBS_Classifier {
    /// Create a new ISCC-NBS classifier using embedded data.
    pub fn new() -> Result<Self, MunsellError> {
        let csv_path = concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/assets/ISCC-NBS-Definitions.csv"
        );
        Self::from_csv(csv_path)
    }

    /// Create a new ISCC-NBS classifier from external CSV file.
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
    fn is_achromatic(&self, hue: &str) -> bool {
        is_achromatic_hue(hue)
    }

    /// Get the achromatic (neutral) color number for a given value.
    /// Helper method to eliminate duplication between classify_achromatic and find_all_colors_at_point.
    fn get_achromatic_color_number(&self, value: f64) -> Option<u16> {
        let color_number = get_achromatic_color_number(value)?;

        // Verify the metadata exists before returning
        if self.color_metadata.contains_key(&color_number) {
            Some(color_number)
        } else {
            None
        }
    }

    /// Classify an achromatic (neutral) color based on its value.
    /// Returns just the color number for internal use.
    fn classify_achromatic(&self, value: f64) -> Option<u16> {
        self.get_achromatic_color_number(value)
    }

    /// Build a ColorMetadata result from a color number by cloning from the colors HashMap
    fn build_result(&self, color_number: u16) -> Option<ColorMetadata> {
        self.color_metadata.get(&color_number).cloned()
    }

    /// Classify a Munsell color using the ISCC-NBS system.
    pub fn classify_munsell(
        &self,
        hue: &str,
        value: f64,
        chroma: f64,
    ) -> Result<Option<ColorMetadata>, MunsellError> {
        // Check for achromatic colors first
        if self.is_achromatic(hue) {
            if let Some(color_number) = self.classify_achromatic(value) {
                return Ok(self.build_result(color_number));
            }
            return Ok(None);
        }

        // Round values to 4 decimal places for internal classification
        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;

        // Create cache key using 4-decimal precision
        let cache_key = (
            hue.to_string(),
            format!("{:.4}", rounded_value),
            format!("{:.4}", rounded_chroma),
        );

        // Check cache first
        {
            let cache = self.cache.borrow();
            if let Some(&cached_color_number) = cache.get(&cache_key) {
                return Ok(cached_color_number.and_then(|num| self.build_result(num)));
            }
        }

        // Use the mechanical wedge system for classification with rounded values
        if let Some(color) = self
            .wedge_system
            .classify_color(hue, rounded_value, rounded_chroma)
        {
            self.cache_result(cache_key, Some(color.color_number));
            return Ok(self.build_result(color.color_number));
        }

        self.cache_result(cache_key, None);
        Ok(None)
    }

    /// Find all ISCC-NBS colors that contain a given point.
    /// Returns just the color numbers.
    pub fn find_all_colors_at_point(
        &self,
        hue: &str,
        value: f64,
        chroma: f64,
    ) -> Result<Vec<u16>, MunsellError> {
        // Check for achromatic colors first
        if self.is_achromatic(hue) {
            if let Some(color_number) = self.get_achromatic_color_number(value) {
                return Ok(vec![color_number]);
            }
            return Ok(vec![]);
        }

        // Round values to 4 decimal places for internal consistency
        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;

        // Use the mechanical wedge system to find ALL colors at this point
        let colors = self
            .wedge_system
            .find_all_colors_at_point(hue, rounded_value, rounded_chroma);
        Ok(colors)
    }

    /// Classify a Munsell color using the ISCC-NBS system (convenience method).
    pub fn classify(
        &self,
        hue: &str,
        value: f64,
        chroma: f64,
    ) -> Option<ColorMetadata> {
        self.classify_munsell(hue, value, chroma).ok().flatten()
    }

    /// Classify a Munsell color with detailed error information.
    pub fn classify_with_details(
        &self,
        hue: &str,
        value: f64,
        chroma: f64,
    ) -> Option<(ColorMetadata, String)> {
        match self.classify_munsell(hue, value, chroma) {
            Ok(Some(metadata)) => {
                let details = format!("Classified Munsell {}:{}/{} successfully", hue, value, chroma);
                Some((metadata, details))
            }
            Ok(None) => None,
            Err(_) => None,
        }
    }

    /// Helper method to cache results with size management
    fn cache_result(&self, key: (String, String, String), result: Option<u16>) {
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
    pub fn get_polygon_in_wedge(
        &self,
        hue: &str,
        expected_descriptor: &str,
    ) -> Option<&ISCC_NBS_Color> {
        // Determine which wedge this hue belongs to
        let wedge_key = self.wedge_system.find_wedge_for_hue(hue)?;

        // Get polygons in this wedge and find matching descriptor
        self.wedge_system
            .get_wedge_polygons(&wedge_key)?
            .iter()
            .find(|polygon| {
                // Check if this polygon's full descriptor matches the expected one using metadata lookup
                if let Some(metadata) = self.color_metadata.get(&polygon.color_number) {
                    let constructed_descriptor = metadata.iscc_nbs_descriptor();
                    constructed_descriptor.to_lowercase() == expected_descriptor.to_lowercase()
                } else {
                    false
                }
            })
    }

    /// Classify a MunsellColor object using the ISCC-NBS system.
    pub fn classify_munsell_color(
        &self,
        munsell: &crate::types::MunsellColor,
    ) -> Result<Option<ColorMetadata>, MunsellError> {
        // Handle neutral colors (no hue/chroma)
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            self.classify_munsell(hue, munsell.value, chroma)
        } else {
            // Neutral color - handle separately or return None
            Ok(None)
        }
    }

    /// Classify an sRGB color using the ISCC-NBS system.
    pub fn classify_srgb(&self, rgb: [u8; 3]) -> Result<Option<ColorMetadata>, MunsellError> {
        use crate::MunsellConverter;

        // Convert sRGB to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.srgb_to_munsell(rgb)?;

        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }

    /// Classify a Lab color using the ISCC-NBS system.
    pub fn classify_lab(&self, lab: [f64; 3]) -> Result<Option<ColorMetadata>, MunsellError> {
        use crate::MunsellConverter;

        // Convert Lab to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.lab_to_munsell(lab)?;

        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }

    /// Classify a hex color using the ISCC-NBS system.
    pub fn classify_hex(&self, hex: &str) -> Result<Option<ColorMetadata>, MunsellError> {
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
            let r = u8::from_str_radix(&hex[0..1].repeat(2), 16).map_err(|_| {
                MunsellError::ConversionError {
                    message: format!("Invalid hex color format: {}", hex),
                }
            })?;
            let g = u8::from_str_radix(&hex[1..2].repeat(2), 16).map_err(|_| {
                MunsellError::ConversionError {
                    message: format!("Invalid hex color format: {}", hex),
                }
            })?;
            let b = u8::from_str_radix(&hex[2..3].repeat(2), 16).map_err(|_| {
                MunsellError::ConversionError {
                    message: format!("Invalid hex color format: {}", hex),
                }
            })?;
            [r, g, b]
        } else if hex.len() == 6 {
            // Long form: "ff0000"
            let r =
                u8::from_str_radix(&hex[0..2], 16).map_err(|_| MunsellError::ConversionError {
                    message: format!("Invalid hex color format: {}", hex),
                })?;
            let g =
                u8::from_str_radix(&hex[2..4], 16).map_err(|_| MunsellError::ConversionError {
                    message: format!("Invalid hex color format: {}", hex),
                })?;
            let b =
                u8::from_str_radix(&hex[4..6], 16).map_err(|_| MunsellError::ConversionError {
                    message: format!("Invalid hex color format: {}", hex),
                })?;
            [r, g, b]
        } else {
            return Err(MunsellError::ConversionError {
                message: format!(
                    "Invalid hex color length: {}. Expected 3 or 6 characters after #",
                    hex.len()
                ),
            });
        };

        Ok(rgb)
    }

    /// Helper function to create data error
    fn data_error<S: Into<String>>(msg: S) -> MunsellError {
        MunsellError::ReferenceDataError {
            message: msg.into(),
        }
    }

    /// Load ISCC-NBS data from CSV files (for testing/development)
    fn load_iscc_data(
        polygon_csv_path: &str,
    ) -> Result<(Vec<ISCC_NBS_Color>, HashMap<u16, ColorMetadata>), MunsellError> {
        use std::fs;
        use std::path::Path;

        // Read polygon data
        let polygon_csv_content =
            fs::read_to_string(polygon_csv_path).map_err(|e| MunsellError::ReferenceDataError {
                message: format!("Failed to read polygon CSV file: {}", e),
            })?;

        // Derive color metadata file path (same directory, different name)
        let polygon_path = Path::new(polygon_csv_path);
        let color_csv_path = polygon_path
            .parent()
            .unwrap_or(Path::new("."))
            .join("ISCC-NBS-Colors.csv");

        let color_csv_content =
            fs::read_to_string(&color_csv_path).map_err(|e| MunsellError::ReferenceDataError {
                message: format!(
                    "Failed to read color metadata CSV file {}: {}",
                    color_csv_path.display(),
                    e
                ),
            })?;

        let polygons = Self::parse_polygon_csv_data(&polygon_csv_content)?;
        let color_metadata = Self::parse_color_metadata_csv(&color_csv_content)?;
        Ok((polygons, color_metadata))
    }

    /// Parse color metadata CSV data into lookup table
    fn parse_color_metadata_csv(
        csv_content: &str,
    ) -> Result<HashMap<u16, ColorMetadata>, MunsellError> {
        use csv::Reader;

        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_metadata: HashMap<u16, ColorMetadata> = HashMap::new();

        // Parse CSV data: color_number,iscc_nbs_color_name,iscc_nbs_formatter,alt_color_name,color_shade
        for result in reader.records() {
            let record = result.map_err(|e| MunsellError::ReferenceDataError {
                message: format!("CSV parsing error: {}", e),
            })?;

            let color_number: u16 = record
                .get(0)
                .ok_or_else(|| Self::data_error("Missing color_number".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid color_number: {}", e)))?;

            let iscc_nbs_color_name = record
                .get(1)
                .ok_or_else(|| Self::data_error("Missing iscc_nbs_color_name".to_string()))?
                .to_string();

            let iscc_nbs_formatter = record
                .get(2)
                .filter(|s| !s.is_empty())
                .map(|s| s.to_string());

            let alt_color_name = record
                .get(3)
                .ok_or_else(|| Self::data_error("Missing alt_color_name".to_string()))?
                .to_string();

            let color_shade = record
                .get(4)
                .ok_or_else(|| Self::data_error("Missing color_shade".to_string()))?
                .to_string();

            color_metadata.insert(
                color_number,
                ColorMetadata {
                    iscc_nbs_color_name,
                    iscc_nbs_formatter,
                    alt_color_name,
                    color_shade,
                },
            );
        }

        Ok(color_metadata)
    }

    /// Parse polygon CSV data and convert to polygons
    fn parse_polygon_csv_data(csv_content: &str) -> Result<Vec<ISCC_NBS_Color>, MunsellError> {
        use csv::Reader;
        use geo::{Coord, LineString};

        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_groups: std::collections::HashMap<(u16, u8), Vec<(f64, f64)>> =
            std::collections::HashMap::new();
        let mut polygon_metadata: std::collections::HashMap<(u16, u8), (String, String)> =
            std::collections::HashMap::new();

        // Parse CSV data and group points by color_number and polygon_id
        for result in reader.records() {
            let record = result.map_err(|e| MunsellError::ReferenceDataError {
                message: format!("CSV parsing error: {}", e),
            })?;

            // Parse CSV columns: color_number,polygon_id,point_id,hue1,hue2,chroma,value
            let color_number: u16 = record
                .get(0)
                .ok_or_else(|| Self::data_error("Missing color_number".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid color_number: {}", e)))?;

            let polygon_id: u8 = record
                .get(1)
                .ok_or_else(|| Self::data_error("Missing polygon_id".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid polygon_id: {}", e)))?;

            let hue1 = record
                .get(3)
                .ok_or_else(|| Self::data_error("Missing hue1".to_string()))?
                .to_string();

            let hue2 = record
                .get(4)
                .ok_or_else(|| Self::data_error("Missing hue2".to_string()))?
                .to_string();

            let chroma: f64 = record
                .get(5)
                .ok_or_else(|| Self::data_error("Missing chroma".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid chroma: {}", e)))?;

            let value: f64 = record
                .get(6)
                .ok_or_else(|| Self::data_error("Missing value".to_string()))?
                .parse()
                .map_err(|e| Self::data_error(format!("Invalid value: {}", e)))?;

            // Store point in the appropriate group
            let key = (color_number, polygon_id);
            color_groups
                .entry(key)
                .or_insert_with(Vec::new)
                .push((value, chroma));

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
                    color_number,
                    polygon_id,
                    points.len()
                )));
            }

            let (hue1, hue2) = polygon_metadata
                .get(&(color_number, polygon_id))
                .ok_or_else(|| Self::data_error("Missing polygon metadata".to_string()))?
                .clone();

            // Create LineString from points (geo requires a closed ring)
            // NOTE: Using consistent coordinate system: x=chroma, y=value (matches mechanical wedge system)
            let mut coords: Vec<Coord<f64>> = points
                .into_iter()
                .map(|(value, chroma)| Coord {
                    x: chroma,
                    y: value,
                })
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
}

/// Validation functions using geo crate  
pub mod validation {
    use super::{ISCC_NBS_Color, ValidationError};
    use geo::Intersects;

    /// Validate ISCC-NBS polygon data for integrity.
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
        for i in 0..colors.len() {
            for j in (i + 1)..colors.len() {
                if colors[i].polygon.intersects(&colors[j].polygon) {
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
        for i in 1..coords.len() - 1 {
            let p1 = coords[i - 1];
            let p2 = coords[i];
            let p3 = coords[i + 1];

            // Calculate vectors
            let v1 = (p1.x - p2.x, p1.y - p2.y);
            let v2 = (p3.x - p2.x, p3.y - p2.y);

            // Calculate angle using dot product and cross product
            let dot = v1.0 * v2.0 + v1.1 * v2.1;
            let cross = v1.0 * v2.1 - v1.1 * v2.0;
            let angle = cross.atan2(dot).abs() * 180.0 / std::f64::consts::PI;

            // Check if angle is approximately 90° or 270° (allowing small tolerance)
            let tolerance = 1.0; // 1 degree tolerance
            let is_right_angle =
                (angle - 90.0).abs() < tolerance || (angle - 270.0).abs() < tolerance;

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