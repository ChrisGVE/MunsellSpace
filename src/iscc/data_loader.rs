//! Data loading, CSV parsing, and deprecated convenience methods for IsccNbsClassifier.

use crate::constants::{get_color_by_number, color_entry_to_metadata, get_polygon_definitions};
use crate::error::MunsellError;
use super::color::IsccNbsColor;
use super::classifier::IsccNbsClassifier;
use super::metadata::ColorMetadata;
use std::collections::HashMap;

impl IsccNbsClassifier {
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

        let converter = MunsellConverter::new()?;
        let munsell = converter.srgb_to_munsell(rgb)?;
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

        let converter = MunsellConverter::new()?;
        let munsell = converter.lab_to_munsell(lab)?;
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
    #[allow(deprecated)]
    pub fn classify_hex(&self, hex: &str) -> Result<Option<ColorMetadata>, MunsellError> {
        let rgb = self.parse_hex_to_rgb(hex)?;
        self.classify_srgb(rgb)
    }

    /// Parse hex color string to RGB array.
    pub(super) fn parse_hex_to_rgb(&self, hex: &str) -> Result<[u8; 3], MunsellError> {
        let hex = hex.trim_start_matches('#');

        let rgb = if hex.len() == 3 {
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

    /// Helper function to create data error.
    pub(super) fn data_error<S: Into<String>>(msg: S) -> MunsellError {
        MunsellError::ReferenceDataError {
            message: msg.into(),
        }
    }

    /// Load ISCC-NBS polygon data from embedded constants (no file I/O required).
    fn parse_embedded_polygon_data() -> Result<Vec<IsccNbsColor>, MunsellError> {
        use geo::{Coord, LineString};
        let mut colors = Vec::new();

        for polygon_def in get_polygon_definitions() {
            if polygon_def.points.len() < 3 {
                return Err(Self::data_error(format!(
                    "Insufficient points for polygon: color {} polygon_group {} has {} points",
                    polygon_def.color_number,
                    polygon_def.polygon_group,
                    polygon_def.points.len()
                )));
            }

            let mut coords: Vec<Coord<f64>> = polygon_def
                .points
                .iter()
                .map(|p| Coord {
                    x: p.chroma,
                    y: p.value,
                })
                .collect();

            if !coords.is_empty() && coords.first() != coords.last() {
                coords.push(coords[0]);
            }

            let exterior = LineString::new(coords);
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

    /// Load ISCC-NBS data from embedded constants (no file I/O required).
    pub(super) fn load_embedded_iscc_data(
    ) -> Result<(Vec<IsccNbsColor>, HashMap<u16, ColorMetadata>), MunsellError> {
        let polygons = Self::parse_embedded_polygon_data()?;

        let mut color_metadata: HashMap<u16, ColorMetadata> = HashMap::new();

        for &color_number in crate::constants::get_all_color_numbers().iter() {
            if let Some(entry) = get_color_by_number(color_number) {
                let metadata = color_entry_to_metadata(entry);
                color_metadata.insert(color_number, metadata);
            }
        }

        Ok((polygons, color_metadata))
    }

    /// Load ISCC-NBS data from CSV files (for testing/development).
    pub(super) fn load_iscc_data(
        polygon_csv_path: &str,
    ) -> Result<(Vec<IsccNbsColor>, HashMap<u16, ColorMetadata>), MunsellError> {
        use std::fs;
        use std::path::Path;

        let polygon_csv_content =
            fs::read_to_string(polygon_csv_path).map_err(|e| MunsellError::ReferenceDataError {
                message: format!("Failed to read polygon CSV file: {}", e),
            })?;

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

    /// Parse color metadata CSV data into lookup table.
    fn parse_color_metadata_csv(
        csv_content: &str,
    ) -> Result<HashMap<u16, ColorMetadata>, MunsellError> {
        use csv::Reader;

        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_metadata: HashMap<u16, ColorMetadata> = HashMap::new();

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

    /// Parse polygon CSV data and convert to polygons.
    fn parse_polygon_csv_data(csv_content: &str) -> Result<Vec<IsccNbsColor>, MunsellError> {
        use csv::Reader;
        use geo::{Coord, LineString};

        let mut reader = Reader::from_reader(csv_content.as_bytes());
        let mut color_groups: std::collections::HashMap<(u16, u8), Vec<(f64, f64)>> =
            std::collections::HashMap::new();
        let mut polygon_metadata: std::collections::HashMap<(u16, u8), (String, String)> =
            std::collections::HashMap::new();

        for result in reader.records() {
            let record = result.map_err(|e| MunsellError::ReferenceDataError {
                message: format!("CSV parsing error: {}", e),
            })?;

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

            let key = (color_number, polygon_id);
            color_groups
                .entry(key)
                .or_insert_with(Vec::new)
                .push((chroma, value));
            polygon_metadata
                .entry(key)
                .or_insert((hue1, hue2));
        }

        let mut colors = Vec::new();
        let mut sorted_keys: Vec<_> = color_groups.keys().cloned().collect();
        sorted_keys.sort();

        for key in sorted_keys {
            let points = &color_groups[&key];
            let (hue1, hue2) = &polygon_metadata[&key];

            if points.len() < 3 {
                return Err(Self::data_error(format!(
                    "Insufficient points for polygon: color {} polygon_id {}",
                    key.0, key.1
                )));
            }

            let mut coords: Vec<Coord<f64>> =
                points.iter().map(|&(c, v)| Coord { x: c, y: v }).collect();

            if coords.first() != coords.last() {
                coords.push(coords[0]);
            }

            let exterior = LineString::new(coords);
            let polygon = geo::Polygon::new(exterior, vec![]);

            colors.push(IsccNbsColor {
                color_number: key.0,
                polygon_group: key.1,
                hue_range: (hue1.clone(), hue2.clone()),
                polygon,
            });
        }

        Ok(colors)
    }
}
