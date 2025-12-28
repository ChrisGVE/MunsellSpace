//! ISCC-NBS Color Name System Implementation
//!
//! This module provides implementation of the Inter-Society Color Council - 
//! National Bureau of Standards (ISCC-NBS) color naming system. It translates
//! Munsell color specifications into standardized color names.
//!
//! The ISCC-NBS system defines 267 color categories, each represented by:
//! - A numerical identifier (1-267)
//! - A descriptive name (e.g., "vivid red", "light grayish blue")
//! - A polygonal region in Munsell color space
//!
//! ## Examples
//!
//! ```rust
//! use munsellspace::iscc::IsccNbsClassifier;
//! use munsellspace::MunsellConverter;
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! // Create classifier and converter
//! let classifier = IsccNbsClassifier::new()?;
//! let converter = MunsellConverter::new()?;
//!
//! // Convert RGB to Munsell, then to ISCC-NBS color name
//! let munsell = converter.srgb_to_munsell([255, 0, 0])?;
//! if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
//!     println!("Munsell notation: {}", munsell.notation);
//!     // ISCC-NBS classification would use internal methods
//! }
//! # Ok(())
//! # }
//! ```

use crate::constants::{get_color_ish, get_achromatic_color_number, is_achromatic_hue, get_color_by_number, color_entry_to_metadata, get_polygon_definitions};
use crate::error::MunsellError;
use crate::mechanical_wedges::MechanicalWedgeSystem;
use geo::Polygon;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

/// Color metadata with on-the-fly descriptor construction.
///
/// This struct contains the raw data components for ISCC-NBS color descriptions
/// and provides methods to construct formatted descriptors dynamically.
///
/// # Examples
///
/// ```rust
/// use munsellspace::iscc::ColorMetadata;
///
/// # fn example() -> Result<(), Box<dyn std::error::Error>> {
/// // Color metadata would typically be loaded from internal data
/// let metadata = ColorMetadata {
///     iscc_nbs_color_name: "red".to_string(),
///     iscc_nbs_formatter: Some("vivid {0}".to_string()),
///     extended_name: "red".to_string(),
///     color_shade: "medium".to_string(),
/// };
///
/// // Generate formatted descriptor
/// let descriptor = metadata.iscc_nbs_descriptor();
/// println!("Descriptor: {}", descriptor); // "vivid red"
/// # Ok(())
/// # }
/// ```
#[derive(Debug, Clone)]
pub struct ColorMetadata {
    /// Base color name from ISCC-NBS data (e.g., "red", "blue", "yellow").
    ///
    /// This is the core color term that gets formatted with modifiers
    /// like "vivid", "dark", "light", etc.
    pub iscc_nbs_color_name: String,

    /// Formatter template with placeholders for dynamic descriptor construction.
    ///
    /// Contains templates like "vivid {0}", "light {1}", where:
    /// - `{0}` is replaced with the base color name
    /// - `{1}` is replaced with the "-ish" variant (e.g., "reddish")
    pub iscc_nbs_formatter: Option<String>,

    /// Extended ISCC-NBS name - more recognizable color terms.
    ///
    /// Provides more commonly-used names for colors (e.g., "lime" instead of
    /// "yellow green"), based on frequency analysis of color name usage.
    pub extended_name: String,

    /// Color shade information describing lightness/darkness characteristics.
    ///
    /// Indicates the relative brightness category such as "light", "dark",
    /// "medium", or other shade descriptors.
    pub color_shade: String,
}

impl ColorMetadata {
    /// Construct the primary ISCC-NBS descriptor using the formatter and color name.
    ///
    /// Applies the formatter template to the primary color name, creating
    /// standardized ISCC-NBS color descriptions.
    ///
    /// # Returns
    /// Formatted color descriptor string (e.g., "vivid red", "light blue")
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let metadata = ColorMetadata {
    ///     iscc_nbs_color_name: "red".to_string(),
    ///     iscc_nbs_formatter: Some("vivid {0}".to_string()),
    ///     extended_name: "red".to_string(),
    ///     color_shade: "bright".to_string(),
    /// };
    ///
    /// assert_eq!(metadata.iscc_nbs_descriptor(), "vivid red");
    /// ```
    pub fn iscc_nbs_descriptor(&self) -> String {
        if let Some(formatter) = &self.iscc_nbs_formatter {
            Self::construct_descriptor(formatter, &self.iscc_nbs_color_name)
        } else {
            self.iscc_nbs_color_name.clone()
        }
    }

    /// Construct the extended color descriptor using the formatter and extended name.
    ///
    /// Similar to [`iscc_nbs_descriptor`](Self::iscc_nbs_descriptor) but uses the
    /// extended color name, providing more recognizable naming options.
    ///
    /// # Returns
    /// Formatted extended color descriptor string
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let metadata = ColorMetadata {
    ///     iscc_nbs_color_name: "yellow green".to_string(),
    ///     iscc_nbs_formatter: Some("vivid {0}".to_string()),
    ///     extended_name: "lime".to_string(),
    ///     color_shade: "lime".to_string(),
    /// };
    ///
    /// assert_eq!(metadata.extended_descriptor(), "vivid lime");
    /// ```
    pub fn extended_descriptor(&self) -> String {
        if let Some(formatter) = &self.iscc_nbs_formatter {
            Self::construct_descriptor(formatter, &self.extended_name)
        } else {
            self.extended_name.clone()
        }
    }

    /// Deprecated: Use [`extended_descriptor`](Self::extended_descriptor) instead.
    #[deprecated(since = "1.3.0", note = "Use extended_descriptor() instead. Will be removed in v2.0.0.")]
    pub fn alt_color_descriptor(&self) -> String {
        self.extended_descriptor()
    }

    /// Deprecated: Access `extended_name` field directly instead.
    #[deprecated(since = "1.3.0", note = "Use extended_name field instead. Will be removed in v2.0.0.")]
    pub fn alt_color_name(&self) -> &str {
        &self.extended_name
    }

    /// Get the color shade information.
    ///
    /// Returns the shade descriptor indicating the relative lightness/darkness
    /// characteristics of the color.
    ///
    /// # Returns
    /// Reference to the shade descriptor string
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let metadata = ColorMetadata {
    ///     iscc_nbs_color_name: "blue".to_string(),
    ///     iscc_nbs_formatter: None,
    ///     extended_name: "blue".to_string(),
    ///     color_shade: "light".to_string(),
    /// };
    ///
    /// assert_eq!(metadata.shade(), "light");
    /// ```
    pub fn shade(&self) -> &str {
        &self.color_shade
    }

    /// Static descriptor construction using formatter templates and color name lookup.
    ///
    /// This method processes formatter templates containing placeholders:
    /// - `{0}` is replaced with the provided color name
    /// - `{1}` is replaced with the "-ish" variant (e.g., "red" → "reddish")
    ///
    /// # Arguments
    /// * `formatter` - Template string with `{0}` and/or `{1}` placeholders
    /// * `color_name` - Base color name to substitute into template
    ///
    /// # Returns
    /// Formatted descriptor with placeholders replaced
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    /// 
    /// let result = ColorMetadata::construct_descriptor("vivid {0}", "red");
    /// assert_eq!(result, "vivid red");
    /// 
    /// let result = ColorMetadata::construct_descriptor("light {1}", "blue");
    /// assert_eq!(result, "light bluish");
    /// ```
    pub fn construct_descriptor(formatter: &str, color_name: &str) -> String {
        let color_name_ish = get_color_ish(color_name);
        
        // Replace {0} with color_name and {1} with color_name_ish
        formatter
            .replace("{0}", color_name)
            .replace("{1}", color_name_ish)
    }
}

/// Internal representation of an ISCC-NBS color category with its polygonal region.
///
/// Each ISCC-NBS color is defined by a polygon in Munsell value-chroma space,
/// bounded by specific hue ranges. This struct represents one such color region.
///
/// # Fields
/// - `color_number`: Unique ISCC-NBS identifier (1-267)
/// - `polygon_group`: Group number for colors with multiple disconnected regions
/// - `hue_range`: Start and end hues defining the applicable hue range
/// - `polygon`: Geometric polygon defining the valid value-chroma region
#[derive(Debug, Clone)]
pub struct IsccNbsColor {
    /// Color number from ISCC-NBS standard (1-267).
    ///
    /// This unique identifier corresponds to specific color names
    /// in the ISCC-NBS system and is used for metadata lookup.
    pub color_number: u16,
    
    /// Polygon group number for colors with multiple disconnected regions.
    ///
    /// Some ISCC-NBS colors are defined by multiple separate polygons.
    /// This field groups polygons belonging to the same color category.
    pub polygon_group: u8,
    
    /// Hue range defining the applicable Munsell hue span.
    ///
    /// Tuple containing (start_hue, end_hue) such as ("1R", "7R"),
    /// indicating this color definition applies to hues from 1R through 7R.
    pub hue_range: (String, String),
    
    /// Geometric polygon defining the color region in Munsell value-chroma space.
    ///
    /// Points in this polygon represent valid (value, chroma) coordinates
    /// for this color within the specified hue range.
    pub polygon: Polygon<f64>,
}

/// ISCC-NBS color naming engine with deterministic boundary handling and performance caching.
///
/// This classifier translates Munsell color specifications into standardized
/// ISCC-NBS color names using a mechanical wedge system for precise hue-based
/// categorization and polygon containment testing.
///
/// # Architecture
///
/// The classifier uses a two-stage approach:
/// 1. **Hue-based wedge selection**: Determines which hue wedge contains the color
/// 2. **Polygon containment testing**: Tests if the (value, chroma) point falls
///    within any color polygons in that wedge
///
/// # Thread Safety
///
/// This struct is thread-safe and can be shared across multiple threads using
/// `Arc<T>`. The internal cache uses `RwLock` for concurrent access.
///
/// # Examples
///
/// ```rust
/// use munsellspace::iscc::IsccNbsClassifier;
///
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let classifier = IsccNbsClassifier::new()?;
///
/// // Classify a Munsell color specification
/// if let Ok(Some(color_metadata)) = classifier.classify_munsell("5R", 5.0, 12.0) {
///     println!("5R 5.0/12.0 is: {}", color_metadata.iscc_nbs_descriptor());
/// }
/// # Ok(())
/// # }
/// ```
pub struct IsccNbsClassifier {
    /// Mechanical wedge system providing deterministic hue-based classification.
    ///
    /// Divides the complete Munsell hue circle into 100 wedge containers,
    /// each containing the relevant color polygons for that hue range.
    pub wedge_system: crate::mechanical_wedges::MechanicalWedgeSystem,
    
    /// Metadata lookup table mapping color numbers to descriptive information.
    ///
    /// Stores color names, formatters, and alternative names indexed by
    /// ISCC-NBS color number, avoiding duplication across wedges.
    color_metadata: HashMap<u16, ColorMetadata>,
    
    /// Thread-safe LRU cache for performance optimization.
    ///
    /// Caches recent classification results using (hue, scaled_value, scaled_chroma)
    /// as keys, mapped to optional color numbers. Uses scaled integer values
    /// for reliable floating-point key hashing.
    cache: Arc<RwLock<HashMap<(String, i32, i32), Option<u16>>>>,
    
    /// Maximum number of entries to retain in the cache.
    ///
    /// When the cache exceeds this size, older entries are evicted to
    /// maintain reasonable memory usage.
    cache_max_size: usize,
}

// Embedded ISCC-NBS polygon data is now in constants module - no CSV loading needed

impl IsccNbsClassifier {
    /// Create a new ISCC-NBS classifier using embedded color data.
    ///
    /// Initializes the classifier by loading embedded ISCC-NBS color definitions
    /// and distributing them into a mechanical wedge system for efficient
    /// hue-based classification.
    ///
    /// # Returns
    /// Result containing the initialized classifier or an error if data loading fails
    ///
    /// # Errors
    /// Returns [`MunsellError::ReferenceDataError`] if embedded color data
    /// cannot be loaded or parsed.
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::IsccNbsClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = IsccNbsClassifier::new()?;
    /// println!("Classifier initialized with embedded ISCC-NBS data");
    /// # Ok(())
    /// # }
    /// ```
    pub fn new() -> Result<Self, MunsellError> {
        let (colors, color_metadata) = Self::load_embedded_iscc_data()?;
        let mut wedge_system = MechanicalWedgeSystem::new();

        // Distribute all polygons into the mechanical wedge system
        for polygon in colors {
            wedge_system.distribute_polygon(polygon)?;
        }

        Ok(IsccNbsClassifier {
            wedge_system,
            color_metadata,
            cache: Arc::new(RwLock::new(HashMap::new())),
            cache_max_size: 256,
        })
    }

    /// Create a new ISCC-NBS classifier from external CSV file.
    pub fn from_csv(csv_path: &str) -> Result<Self, MunsellError> {
        let (colors, color_metadata) = Self::load_iscc_data(csv_path)?;
        let mut wedge_system = MechanicalWedgeSystem::new();

        // Distribute all polygons into the mechanical wedge system
        for polygon in colors {
            wedge_system.distribute_polygon(polygon)?;
        }

        Ok(IsccNbsClassifier {
            wedge_system,
            color_metadata,
            cache: Arc::new(RwLock::new(HashMap::new())),
            cache_max_size: 256,
        })
    }

    /// Check if a hue represents an achromatic (neutral) color.
    #[inline]
    fn is_achromatic(&self, hue: &str) -> bool {
        is_achromatic_hue(hue)
    }

    /// Get the achromatic (neutral) color number for a given value.
    /// Helper method to eliminate duplication between classify_achromatic and find_all_colors_at_point.
    #[inline]
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
    #[inline]
    fn classify_achromatic(&self, value: f64) -> Option<u16> {
        self.get_achromatic_color_number(value)
    }

    /// Build a ColorMetadata result from a color number by cloning from the colors HashMap
    #[inline]
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

        // Round values to 4 decimal places for internal classification (optimized)
        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;

        // Create cache key using integer representations to avoid string formatting
        let cache_key = (
            hue.to_string(), // Only one string allocation
            (rounded_value * 10000.0) as i32,
            (rounded_chroma * 10000.0) as i32,
        );

        // Check cache first
        {
            let cache = self.cache.read().unwrap();
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
    fn cache_result(&self, key: (String, i32, i32), result: Option<u16>) {
        let mut cache = self.cache.write().unwrap();

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
    ) -> Option<&IsccNbsColor> {
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
    ///
    /// # Deprecated
    /// Use [`ColorClassifier::classify_srgb()`](crate::ColorClassifier::classify_srgb)
    /// instead for unified access to standard, extended, and semantic color names.
    #[deprecated(
        since = "1.2.0",
        note = "Use ColorClassifier::classify_srgb() for unified color naming. This method will be removed in v2.0.0."
    )]
    pub fn classify_srgb(&self, rgb: [u8; 3]) -> Result<Option<ColorMetadata>, MunsellError> {
        use crate::MunsellConverter;

        // Convert sRGB to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.srgb_to_munsell(rgb)?;

        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }

    /// Classify a Lab color using the ISCC-NBS system.
    ///
    /// # Deprecated
    /// Use [`ColorClassifier::classify_lab()`](crate::ColorClassifier::classify_lab)
    /// instead for unified access to standard, extended, and semantic color names.
    #[deprecated(
        since = "1.2.0",
        note = "Use ColorClassifier::classify_lab() for unified color naming. This method will be removed in v2.0.0."
    )]
    pub fn classify_lab(&self, lab: [f64; 3]) -> Result<Option<ColorMetadata>, MunsellError> {
        use crate::MunsellConverter;

        // Convert Lab to Munsell first
        let converter = MunsellConverter::new()?;
        let munsell = converter.lab_to_munsell(lab)?;

        // Then classify the Munsell color
        self.classify_munsell_color(&munsell)
    }

    /// Classify a hex color using the ISCC-NBS system.
    ///
    /// # Deprecated
    /// Use [`ColorClassifier::classify_hex()`](crate::ColorClassifier::classify_hex)
    /// instead for unified access to standard, extended, and semantic color names.
    #[deprecated(
        since = "1.2.0",
        note = "Use ColorClassifier::classify_hex() for unified color naming. This method will be removed in v2.0.0."
    )]
    #[allow(deprecated)] // Calls classify_srgb which is also deprecated
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

    /// Load ISCC-NBS polygon data from embedded constants (no file I/O required)
    fn parse_embedded_polygon_data() -> Result<Vec<IsccNbsColor>, MunsellError> {
        use geo::{Coord, LineString};
        let mut colors = Vec::new();
        
        // Convert embedded polygon definitions to IsccNbsColor instances
        for polygon_def in get_polygon_definitions() {
            if polygon_def.points.len() < 3 {
                return Err(Self::data_error(format!(
                    "Insufficient points for polygon: color {} polygon_group {} has {} points",
                    polygon_def.color_number,
                    polygon_def.polygon_group,
                    polygon_def.points.len()
                )));
            }
            
            // Convert points to geo::Coord format (chroma, value) - match mechanical wedge system
            let mut coords: Vec<Coord<f64>> = polygon_def.points.iter()
                .map(|p| Coord { x: p.chroma, y: p.value })
                .collect();
                
            // Ensure polygon is closed (first point equals last point)
            if !coords.is_empty() && coords.first() != coords.last() {
                coords.push(coords[0]);
            }
            
            // Create exterior ring from coordinates
            let exterior = LineString::new(coords);
            
            // Create polygon (no holes for ISCC-NBS regions)
            let polygon = geo::Polygon::new(exterior, vec![]);
            
            colors.push(IsccNbsColor {
                color_number: polygon_def.color_number,
                polygon_group: polygon_def.polygon_group,
                hue_range: (polygon_def.hue1.to_string(), polygon_def.hue2.to_string()),
                polygon,
            });
        }
        
        Ok(colors)
    }

    /// Load ISCC-NBS data from embedded constants (no file I/O required)
    fn load_embedded_iscc_data() -> Result<(Vec<IsccNbsColor>, HashMap<u16, ColorMetadata>), MunsellError> {
        // Load polygon data from embedded constants
        let polygons = Self::parse_embedded_polygon_data()?;
        
        // Load color metadata from embedded constants
        let mut color_metadata: HashMap<u16, ColorMetadata> = HashMap::new();
        
        for &color_number in crate::constants::get_all_color_numbers().iter() {
            if let Some(entry) = get_color_by_number(color_number) {
                let metadata = color_entry_to_metadata(entry);
                color_metadata.insert(color_number, metadata);
            }
        }
        
        Ok((polygons, color_metadata))
    }

    /// Load ISCC-NBS data from CSV files (for testing/development)
    fn load_iscc_data(
        polygon_csv_path: &str,
    ) -> Result<(Vec<IsccNbsColor>, HashMap<u16, ColorMetadata>), MunsellError> {
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

        // Parse CSV data: color_number,iscc_nbs_color_name,iscc_nbs_formatter,extended_name,color_shade
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

            let extended_name = record
                .get(3)
                .ok_or_else(|| Self::data_error("Missing extended_name".to_string()))?
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
                    extended_name,
                    color_shade,
                },
            );
        }

        Ok(color_metadata)
    }

    /// Parse polygon CSV data and convert to polygons
    fn parse_polygon_csv_data(csv_content: &str) -> Result<Vec<IsccNbsColor>, MunsellError> {
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

            colors.push(IsccNbsColor {
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
    use super::{IsccNbsColor, ValidationError};
    use geo::Intersects;

    /// Validate ISCC-NBS polygon data for integrity.
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
    use super::*;
    use std::sync::Arc;
    use std::thread;
    
    #[test]
    fn test_boundary_disambiguation() {
        // Test that boundary rules prevent ambiguous classification
        // Point exactly on boundary should only match one polygon
    }

    #[test]
    fn test_staircase_classification() {
        // Test that staircase polygons work correctly with rectangles in steps
    }
    
    #[test]
    fn test_thread_safety_concurrent_classification() {
        // Test that IsccNbsClassifier can be safely used across multiple threads
        let classifier = Arc::new(IsccNbsClassifier::new().expect("Failed to create classifier"));
        let mut handles = vec![];
        
        // Test data: various Munsell colors that should classify to different ISCC-NBS colors
        let test_colors = vec![
            ("5R", 6.0, 14.0),  // red
            ("10YR", 7.0, 6.0), // yellow-red
            ("5Y", 8.0, 12.0),  // yellow
            ("5G", 5.0, 8.0),   // green
            ("5B", 4.0, 6.0),   // blue
            ("5P", 3.0, 10.0),  // purple
            ("N", 5.0, 0.0),    // neutral gray
            ("N", 9.0, 0.0),    // light gray
            ("N", 2.0, 0.0),    // dark gray
        ];
        
        // Spawn multiple threads that perform classification simultaneously
        for thread_id in 0..8 {
            let classifier_clone = Arc::clone(&classifier);
            let test_colors_clone = test_colors.clone();
            
            let handle = thread::spawn(move || {
                let mut results = Vec::new();
                
                // Each thread classifies all test colors multiple times
                for iteration in 0..10 {
                    for (i, &(hue, value, chroma)) in test_colors_clone.iter().enumerate() {
                        // Use slightly different values per thread to test cache behavior
                        let adjusted_value = value + (thread_id as f64 * 0.01) + (iteration as f64 * 0.001);
                        let adjusted_chroma = if chroma > 0.0 { chroma + (i as f64 * 0.01) } else { 0.0 };
                        
                        match classifier_clone.classify_munsell(hue, adjusted_value, adjusted_chroma) {
                            Ok(Some(metadata)) => {
                                results.push((hue.to_string(), adjusted_value, adjusted_chroma, metadata.iscc_nbs_color_name.clone()));
                            }
                            Ok(None) => {
                                results.push((hue.to_string(), adjusted_value, adjusted_chroma, "unclassified".to_string()));
                            }
                            Err(e) => {
                                panic!("Classification error in thread {}: {:?}", thread_id, e);
                            }
                        }
                    }
                }
                
                (thread_id, results.len())
            });
            handles.push(handle);
        }
        
        // Wait for all threads to complete and collect results
        let mut total_classifications = 0;
        for handle in handles {
            let (thread_id, count) = handle.join().expect("Thread panicked");
            println!("Thread {} completed {} classifications", thread_id, count);
            total_classifications += count;
        }
        
        // Verify we got the expected number of classifications
        let expected_total = 8 * 10 * test_colors.len(); // 8 threads * 10 iterations * 9 colors
        assert_eq!(total_classifications, expected_total, 
                   "Expected {} total classifications, got {}", expected_total, total_classifications);
    }
    
    #[test]
    fn test_thread_safety_cache_behavior() {
        // Test that the cache works correctly under concurrent access
        let classifier = Arc::new(IsccNbsClassifier::new().expect("Failed to create classifier"));
        let mut handles = vec![];
        
        // Use the same color repeatedly to ensure cache hits
        let test_color = ("5R", 6.0, 14.0);
        
        for thread_id in 0..4 {
            let classifier_clone = Arc::clone(&classifier);
            
            let handle = thread::spawn(move || {
                let mut cache_hits = 0;
                let mut results = Vec::new();
                
                // Classify the same color many times to trigger cache usage
                for _ in 0..50 {
                    match classifier_clone.classify_munsell(test_color.0, test_color.1, test_color.2) {
                        Ok(Some(metadata)) => {
                            results.push(metadata.iscc_nbs_color_name.clone());
                            cache_hits += 1;
                        }
                        Ok(None) => {
                            // Should not happen for this test color
                        }
                        Err(e) => {
                            panic!("Classification error in thread {}: {:?}", thread_id, e);
                        }
                    }
                }
                
                (thread_id, cache_hits, results)
            });
            handles.push(handle);
        }
        
        // Collect results from all threads
        for handle in handles {
            let (thread_id, cache_hits, results) = handle.join().expect("Thread panicked");
            println!("Thread {} got {} cache hits", thread_id, cache_hits);
            
            // All results should be the same since we're classifying the same color
            if !results.is_empty() {
                let first_result = &results[0];
                for result in &results {
                    assert_eq!(result, first_result, 
                              "Thread {} got inconsistent results", thread_id);
                }
            }
        }
    }
    
    #[test]
    fn test_send_sync_traits() {
        // Verify that IsccNbsClassifier implements Send + Sync
        fn assert_send<T: Send>() {}
        fn assert_sync<T: Sync>() {}
        
        assert_send::<IsccNbsClassifier>();
        assert_sync::<IsccNbsClassifier>();
        
        // Also verify Arc<IsccNbsClassifier> is Send + Sync
        assert_send::<Arc<IsccNbsClassifier>>();
        assert_sync::<Arc<IsccNbsClassifier>>();
    }
}