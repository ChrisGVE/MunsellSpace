//! Munsell color type with parsing, semantic overlay, and conversion methods.

use serde::{Deserialize, Serialize};
use std::fmt;
use crate::error::{MunsellError, Result};
use crate::semantic_overlay::{self, MunsellSpec};
use super::notation::{format_value, split_hue_from_value, is_valid_hue_format};

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

        // Handle neutral colors: accept "N 5.6", "N5.6", "n 5.6", "N 5.6/", "N 5.6/0"
        let upper = notation.to_uppercase();
        if upper.starts_with('N') {
            return Self::parse_neutral(notation, &upper);
        }

        // Handle chromatic colors (e.g., "5R 4.0/14.0", "5r 4/14", "5R4/14")
        Self::parse_chromatic(notation)
    }

    /// Parse a neutral Munsell notation.
    fn parse_neutral(notation: &str, upper: &str) -> Result<Self> {
        // Strip leading N (with or without space)
        let after_n = upper.strip_prefix('N').unwrap();
        let value_part = after_n.trim().trim_end_matches('/');
        // Also strip trailing /0 or /0.0 patterns
        let value_part = if let Some(idx) = value_part.find('/') {
            let after_slash = &value_part[idx + 1..];
            let trailing_zero = after_slash.trim().parse::<f64>().unwrap_or(1.0) == 0.0;
            if trailing_zero {
                &value_part[..idx]
            } else {
                return Err(MunsellError::InvalidNotation {
                    notation: notation.to_string(),
                    reason: "Neutral colors must have zero chroma".to_string(),
                });
            }
        } else {
            value_part
        };

        let value = value_part.trim().parse::<f64>().map_err(|_| {
            MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid value component in neutral color".to_string(),
            }
        })?;

        if !(0.0..=10.0).contains(&value) {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Value must be between 0.0 and 10.0".to_string(),
            });
        }

        // Always produce canonical form: "N {value}"
        let canonical = format!("N {}", format_value(value));
        Ok(Self {
            notation: canonical,
            hue: None,
            value,
            chroma: None,
        })
    }

    /// Parse a chromatic Munsell notation.
    fn parse_chromatic(notation: &str) -> Result<Self> {
        let parts: Vec<&str> = notation.split_whitespace().collect();

        let (hue_str, value_chroma) = match parts.len() {
            2 => (parts[0].to_string(), parts[1].to_string()),
            1 => {
                // No space — split at the boundary between hue family letters and value digits
                match split_hue_from_value(parts[0]) {
                    Some((h, vc)) => (h, vc),
                    None => {
                        return Err(MunsellError::InvalidNotation {
                            notation: notation.to_string(),
                            reason: "Expected format: 'HUE VALUE/CHROMA' or 'N VALUE/'"
                                .to_string(),
                        })
                    }
                }
            }
            _ => {
                return Err(MunsellError::InvalidNotation {
                    notation: notation.to_string(),
                    reason: "Expected format: 'HUE VALUE/CHROMA' or 'N VALUE/'".to_string(),
                })
            }
        };

        // Normalize hue to uppercase for case-insensitive matching
        let hue = hue_str.to_uppercase();

        // Validate hue format (should be number + valid hue family)
        if !is_valid_hue_format(&hue) {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid hue format. Expected format like '5R', '2.5YR', etc."
                    .to_string(),
            });
        }

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

        let value = value_chroma_parts[0].parse::<f64>().map_err(|_| {
            MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid value component".to_string(),
            }
        })?;

        let chroma = value_chroma_parts[1].parse::<f64>().map_err(|_| {
            MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid chroma component".to_string(),
            }
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

    /// Convert to MunsellSpec for semantic overlay operations.
    ///
    /// # Returns
    /// A MunsellSpec suitable for semantic overlay queries
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    ///
    /// let color = MunsellColor::new_chromatic("5BG".to_string(), 5.0, 8.0);
    /// let spec = color.to_munsell_spec();
    /// assert!(spec.is_some());
    /// ```
    pub fn to_munsell_spec(&self) -> Option<MunsellSpec> {
        if self.is_neutral() {
            // Neutral colors have no hue, chroma = 0
            Some(MunsellSpec::neutral(self.value))
        } else {
            let hue = self.hue.as_ref()?;
            let chroma = self.chroma?;
            let hue_number = semantic_overlay::parse_hue_to_number(hue)?;
            Some(MunsellSpec::new(hue_number, self.value, chroma))
        }
    }

    /// Get the best matching semantic overlay name for this color.
    ///
    /// Returns the non-basic color name (e.g., "aqua", "coral", "navy") that
    /// best matches this Munsell color based on Centore's convex polyhedra
    /// methodology. Returns None if the color doesn't match any semantic overlay.
    ///
    /// # Returns
    /// Optional color name string (e.g., "teal", "peach", "wine")
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    ///
    /// // A color in the teal region
    /// let teal = MunsellColor::new_chromatic("5BG".to_string(), 5.0, 8.0);
    /// if let Some(name) = teal.semantic_overlay() {
    ///     println!("This color is: {}", name);
    /// }
    /// ```
    pub fn semantic_overlay(&self) -> Option<&'static str> {
        let spec = self.to_munsell_spec()?;
        let registry = crate::semantic_overlay_data::get_registry();
        registry.best_match(&spec).map(|o| o.name)
    }

    /// Get all matching semantic overlay names for this color.
    ///
    /// A color may fall within multiple overlapping semantic regions.
    /// This method returns all matching names, ordered by sample count
    /// (most commonly agreed-upon names first).
    ///
    /// # Returns
    /// Vector of matching color names (may be empty)
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    ///
    /// let color = MunsellColor::new_chromatic("2.5P".to_string(), 3.0, 10.0);
    /// let matches = color.matching_overlays();
    /// for name in matches {
    ///     println!("Matches: {}", name);
    /// }
    /// ```
    pub fn matching_overlays(&self) -> Vec<&'static str> {
        match self.to_munsell_spec() {
            Some(spec) => {
                let registry = crate::semantic_overlay_data::get_registry();
                registry.matching_overlays(&spec)
                    .into_iter()
                    .map(|o| o.name)
                    .collect()
            }
            None => Vec::new(),
        }
    }

    /// Check if this color matches a specific semantic overlay.
    ///
    /// # Arguments
    /// * `overlay_name` - The overlay name to check (case-insensitive)
    ///
    /// # Returns
    /// `true` if the color falls within the specified overlay region
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    ///
    /// let color = MunsellColor::new_chromatic("5BG".to_string(), 5.0, 8.0);
    /// if color.matches_overlay("teal") {
    ///     println!("This is a teal color!");
    /// }
    /// ```
    pub fn matches_overlay(&self, overlay_name: &str) -> bool {
        match self.to_munsell_spec() {
            Some(spec) => {
                let registry = crate::semantic_overlay_data::get_registry();
                registry.matches(&spec, overlay_name)
            }
            None => false,
        }
    }

    /// Find the closest semantic overlay to this color.
    ///
    /// Unlike `semantic_overlay()` which requires the color to be inside
    /// the overlay region, this method finds the nearest overlay by
    /// Euclidean distance to the centroid, regardless of containment.
    ///
    /// # Returns
    /// Tuple of (overlay_name, distance) for the closest overlay,
    /// or None if conversion fails
    ///
    /// # Examples
    /// ```
    /// use munsellspace::MunsellColor;
    ///
    /// let color = MunsellColor::new_chromatic("5R".to_string(), 5.0, 10.0);
    /// if let Some((name, distance)) = color.closest_overlay() {
    ///     println!("Closest overlay: {} (distance: {:.2})", name, distance);
    /// }
    /// ```
    pub fn closest_overlay(&self) -> Option<(&'static str, f64)> {
        let spec = self.to_munsell_spec()?;
        let registry = crate::semantic_overlay_data::get_registry();
        registry.closest_overlay(&spec).map(|(o, d)| (o.name, d))
    }
}

impl fmt::Display for MunsellColor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.notation)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
    fn test_munsell_color_edge_cases() {
        let zero_chroma = MunsellColor::new_chromatic("5R".to_string(), 5.0, 0.0);
        assert_eq!(zero_chroma.notation, "5R 5.0/0.0");
        assert!(zero_chroma.is_chromatic());

        let high_chroma = MunsellColor::new_chromatic("5R".to_string(), 5.0, 20.0);
        assert_eq!(high_chroma.notation, "5R 5.0/20.0");

        let min_value = MunsellColor::new_chromatic("5R".to_string(), 0.0, 10.0);
        assert_eq!(min_value.value, 0.0);

        let max_value = MunsellColor::new_chromatic("5R".to_string(), 10.0, 10.0);
        assert_eq!(max_value.value, 10.0);
    }

    #[test]
    fn test_munsell_color_neutral_edge_cases() {
        let black_neutral = MunsellColor::new_neutral(0.0);
        assert_eq!(black_neutral.notation, "N 0.0");
        assert!(black_neutral.is_neutral());
        assert!(!black_neutral.is_chromatic());

        let white_neutral = MunsellColor::new_neutral(10.0);
        assert_eq!(white_neutral.notation, "N 10.0/");

        let mid_neutral = MunsellColor::new_neutral(5.5);
        assert_eq!(mid_neutral.notation, "N 5.5/");
    }

    #[test]
    fn test_munsell_parsing_variants() {
        let hue_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        for family in &hue_families {
            let notation = format!("5{} 5.0/10.0", family);
            let color = MunsellColor::from_notation(&notation).unwrap();
            assert_eq!(color.hue_family(), Some(family.to_string()));
            assert_eq!(color.value, 5.0);
            assert_eq!(color.chroma, Some(10.0));
        }

        for hue_num in [2.5, 5.0, 7.5, 10.0] {
            let notation = format!("{}R 5.0/10.0", hue_num);
            let color = MunsellColor::from_notation(&notation).unwrap();
            assert!(color.hue.as_ref().unwrap().contains("R"));
        }

        let precise = MunsellColor::from_notation("5.5R 6.25/12.75").unwrap();
        assert_eq!(precise.value, 6.25);
        assert_eq!(precise.chroma, Some(12.75));
    }

    #[test]
    fn test_munsell_parsing_invalid_cases() {
        assert!(MunsellColor::from_notation("").is_err());
        assert!(MunsellColor::from_notation("invalid").is_err());
        assert!(MunsellColor::from_notation("5X 5.0/10.0").is_err());
        assert!(MunsellColor::from_notation("R 5.0/10.0").is_err());
        assert!(MunsellColor::from_notation("5R /10.0").is_err());
        assert!(MunsellColor::from_notation("5R 5.0/").is_err());
        assert!(MunsellColor::from_notation("5R -1.0/10.0").is_err());
        assert!(MunsellColor::from_notation("5R 5.0/-1.0").is_err());
        assert!(MunsellColor::from_notation("N /").is_err());
        assert!(MunsellColor::from_notation("N 5.0/10.0").is_err());
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
    fn test_munsell_color_equality() {
        let color1 = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let color2 = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let color3 = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.1);

        assert_eq!(color1, color2);
        assert_ne!(color1, color3);
    }

    #[test]
    fn test_munsell_color_to_munsell_spec() {
        let chromatic = MunsellColor::new_chromatic("5R".to_string(), 4.0, 14.0);
        let spec = chromatic.to_munsell_spec();
        assert!(spec.is_some());
        let spec = spec.unwrap();
        assert_eq!(spec.value, 4.0);
        assert_eq!(spec.chroma, 14.0);
        assert!((spec.hue_number - 2.0).abs() < 0.01);

        let neutral = MunsellColor::new_neutral(5.0);
        let spec = neutral.to_munsell_spec();
        assert!(spec.is_some());
        let spec = spec.unwrap();
        assert_eq!(spec.value, 5.0);
        assert_eq!(spec.chroma, 0.0);
    }

    #[test]
    fn test_munsell_color_semantic_overlay() {
        let teal = MunsellColor::new_chromatic("5BG".to_string(), 5.0, 8.0);
        assert!(teal.to_munsell_spec().is_some());

        let closest = teal.closest_overlay();
        assert!(closest.is_some());
        let (name, _distance) = closest.unwrap();
        assert!(!name.is_empty());
    }

    #[test]
    fn test_munsell_color_matching_overlays() {
        let color = MunsellColor::new_chromatic("5R".to_string(), 5.0, 10.0);
        let matches = color.matching_overlays();
        let _ = matches.len();

        let neutral = MunsellColor::new_neutral(5.0);
        let matches = neutral.matching_overlays();
        assert!(matches.len() <= 2);
    }

    #[test]
    fn test_munsell_color_matches_overlay() {
        let color = MunsellColor::new_chromatic("5BG".to_string(), 5.0, 8.0);
        let _ = color.matches_overlay("teal");
        let _ = color.matches_overlay("TEAL");
        let _ = color.matches_overlay("Teal");
        assert!(!color.matches_overlay("nonexistent"));
    }

    #[test]
    fn test_munsell_color_closest_overlay() {
        let colors = [
            MunsellColor::new_chromatic("5R".to_string(), 5.0, 10.0),
            MunsellColor::new_chromatic("5Y".to_string(), 7.0, 6.0),
            MunsellColor::new_chromatic("5B".to_string(), 4.0, 8.0),
            MunsellColor::new_chromatic("5P".to_string(), 3.0, 10.0),
        ];

        for color in &colors {
            let result = color.closest_overlay();
            assert!(result.is_some(), "closest_overlay should return Some for {}", color);
            let (name, distance) = result.unwrap();
            assert!(!name.is_empty());
            assert!(distance >= 0.0);
        }

        let neutral = MunsellColor::new_neutral(5.0);
        let result = neutral.closest_overlay();
        assert!(result.is_some());
    }

    // === Notation parsing unification tests ===

    #[test]
    fn test_from_notation_neutral_no_space() {
        let c = MunsellColor::from_notation("N5.5").unwrap();
        assert!(c.is_neutral());
        assert_eq!(c.value, 5.5);
        assert_eq!(c.notation, "N 5.5");
    }

    #[test]
    fn test_from_notation_neutral_with_space() {
        let c = MunsellColor::from_notation("N 5.5").unwrap();
        assert!(c.is_neutral());
        assert_eq!(c.value, 5.5);
        assert_eq!(c.notation, "N 5.5");
    }

    #[test]
    fn test_from_notation_neutral_trailing_slash() {
        let c = MunsellColor::from_notation("N 5.6/").unwrap();
        assert!(c.is_neutral());
        assert_eq!(c.value, 5.6);
    }

    #[test]
    fn test_from_notation_neutral_trailing_slash_zero() {
        let c = MunsellColor::from_notation("N 5.0/0").unwrap();
        assert!(c.is_neutral());
        assert_eq!(c.value, 5.0);
    }

    #[test]
    fn test_from_notation_neutral_case_insensitive() {
        let c = MunsellColor::from_notation("n 5.0").unwrap();
        assert!(c.is_neutral());
        assert_eq!(c.notation, "N 5.0");
    }

    #[test]
    fn test_from_notation_chromatic_case_insensitive() {
        let c = MunsellColor::from_notation("5r 4.0/14.0").unwrap();
        assert!(c.is_chromatic());
        assert_eq!(c.hue, Some("5R".to_string()));
        assert_eq!(c.value, 4.0);
        assert_eq!(c.chroma, Some(14.0));
    }

    #[test]
    fn test_from_notation_chromatic_lowercase_compound_hue() {
        let c = MunsellColor::from_notation("2.5yr 6.5/8.0").unwrap();
        assert_eq!(c.hue, Some("2.5YR".to_string()));
    }

    #[test]
    fn test_from_notation_negative_chroma_rejected() {
        let result = MunsellColor::from_notation("5R 4.0/-2.0");
        assert!(result.is_err());
    }

    #[test]
    fn test_from_notation_compact_chromatic() {
        let c = MunsellColor::from_notation("5R4.0/14.0").unwrap();
        assert!(c.is_chromatic());
        assert_eq!(c.hue, Some("5R".to_string()));
        assert_eq!(c.value, 4.0);
        assert_eq!(c.chroma, Some(14.0));
    }

    #[test]
    fn test_from_notation_canonical_output_always_uppercase() {
        let c = MunsellColor::from_notation("5pb 3.0/8.0").unwrap();
        assert_eq!(c.hue, Some("5PB".to_string()));
        assert!(c.notation.contains("PB"));
    }
}
