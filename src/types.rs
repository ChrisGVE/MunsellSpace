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
}