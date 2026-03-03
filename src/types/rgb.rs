//! RGB color type and conversions.

use serde::{Deserialize, Serialize};
use std::fmt;

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
    fn test_rgb_color_edge_cases() {
        let black = RgbColor::new(0, 0, 0);
        assert!(black.is_grayscale());
        assert_eq!(black.to_array(), [0, 0, 0]);

        let white = RgbColor::new(255, 255, 255);
        assert!(white.is_grayscale());
        assert_eq!(white.to_array(), [255, 255, 255]);

        for i in 0..=255 {
            let gray = RgbColor::new(i, i, i);
            assert!(gray.is_grayscale());
        }

        let red = RgbColor::new(255, 0, 0);
        assert!(!red.is_grayscale());

        let green = RgbColor::new(0, 255, 0);
        assert!(!green.is_grayscale());

        let blue = RgbColor::new(0, 0, 255);
        assert!(!blue.is_grayscale());
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
}
