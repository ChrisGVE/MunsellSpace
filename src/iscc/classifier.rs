//! ISCC-NBS color classifier with caching and classification logic.

use crate::constants::{get_achromatic_color_number, is_achromatic_hue};
use crate::error::MunsellError;
use crate::mechanical_wedges::MechanicalWedgeSystem;
use super::color::IsccNbsColor;
use super::metadata::ColorMetadata;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

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
    pub wedge_system: MechanicalWedgeSystem,

    /// Metadata lookup table mapping color numbers to descriptive information.
    pub(super) color_metadata: HashMap<u16, ColorMetadata>,

    /// Thread-safe FIFO cache for performance optimization.
    pub(super) cache: Arc<RwLock<HashMap<(String, i32, i32), Option<u16>>>>,

    /// FIFO insertion order for deterministic eviction.
    pub(super) cache_order: Arc<RwLock<std::collections::VecDeque<(String, i32, i32)>>>,

    /// Maximum number of entries to retain in the cache.
    pub(super) cache_max_size: usize,
}

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

        for polygon in colors {
            wedge_system.distribute_polygon(polygon)?;
        }

        Ok(IsccNbsClassifier {
            wedge_system,
            color_metadata,
            cache: Arc::new(RwLock::new(HashMap::new())),
            cache_order: Arc::new(RwLock::new(std::collections::VecDeque::new())),
            cache_max_size: 256,
        })
    }

    /// Create a new ISCC-NBS classifier from external CSV file.
    pub fn from_csv(csv_path: &str) -> Result<Self, MunsellError> {
        let (colors, color_metadata) = Self::load_iscc_data(csv_path)?;
        let mut wedge_system = MechanicalWedgeSystem::new();

        for polygon in colors {
            wedge_system.distribute_polygon(polygon)?;
        }

        Ok(IsccNbsClassifier {
            wedge_system,
            color_metadata,
            cache: Arc::new(RwLock::new(HashMap::new())),
            cache_order: Arc::new(RwLock::new(std::collections::VecDeque::new())),
            cache_max_size: 256,
        })
    }

    /// Check if a hue represents an achromatic (neutral) color.
    #[inline]
    fn is_achromatic(&self, hue: &str) -> bool {
        is_achromatic_hue(hue)
    }

    /// Get the achromatic (neutral) color number for a given value.
    #[inline]
    fn get_achromatic_color_number(&self, value: f64) -> Option<u16> {
        let color_number = get_achromatic_color_number(value)?;

        if self.color_metadata.contains_key(&color_number) {
            Some(color_number)
        } else {
            None
        }
    }

    /// Classify an achromatic (neutral) color based on its value.
    #[inline]
    fn classify_achromatic(&self, value: f64) -> Option<u16> {
        self.get_achromatic_color_number(value)
    }

    /// Build a ColorMetadata result from a color number.
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
        if self.is_achromatic(hue) {
            if let Some(color_number) = self.classify_achromatic(value) {
                return Ok(self.build_result(color_number));
            }
            return Ok(None);
        }

        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;

        let cache_key = (
            hue.to_string(),
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

        // Use the mechanical wedge system for classification
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
    pub fn find_all_colors_at_point(
        &self,
        hue: &str,
        value: f64,
        chroma: f64,
    ) -> Result<Vec<u16>, MunsellError> {
        if self.is_achromatic(hue) {
            if let Some(color_number) = self.get_achromatic_color_number(value) {
                return Ok(vec![color_number]);
            }
            return Ok(vec![]);
        }

        let rounded_value = (value * 10000.0).round() / 10000.0;
        let rounded_chroma = (chroma * 10000.0).round() / 10000.0;

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
                let details = format!(
                    "Classified Munsell {}:{}/{} successfully",
                    hue, value, chroma
                );
                Some((metadata, details))
            }
            Ok(None) => None,
            Err(_) => None,
        }
    }

    /// Cache a classification result with deterministic FIFO eviction.
    pub(super) fn cache_result(&self, key: (String, i32, i32), result: Option<u16>) {
        let mut cache = self.cache.write().unwrap();
        let mut order = self.cache_order.write().unwrap();

        if cache.len() >= self.cache_max_size {
            if let Some(oldest_key) = order.pop_front() {
                cache.remove(&oldest_key);
            }
        }

        cache.insert(key.clone(), result);
        order.push_back(key);
    }

    /// Get a polygon by its expected descriptor and hue wedge.
    pub fn get_polygon_in_wedge(
        &self,
        hue: &str,
        expected_descriptor: &str,
    ) -> Option<&IsccNbsColor> {
        let wedge_key = self.wedge_system.find_wedge_for_hue(hue)?;

        self.wedge_system
            .get_wedge_polygons(&wedge_key)?
            .iter()
            .find(|polygon| {
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
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            self.classify_munsell(hue, munsell.value, chroma)
        } else {
            Ok(None)
        }
    }
}
