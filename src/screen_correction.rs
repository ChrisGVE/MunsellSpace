//! Screen-to-Physical Color Correction
//!
//! This module provides correction factors to convert Munsell colors derived from
//! screen (RGB) sources to more accurate physical color references.
//!
//! ## Background
//!
//! When RGB colors displayed on computer monitors are converted to Munsell notation,
//! systematic biases exist compared to spectrophotometer-measured physical colors:
//!
//! - **Value bias**: Screen colors appear ~0.9 units lighter (self-luminous vs reflective)
//! - **Chroma bias**: Screen colors appear ~4.6 units more saturated (sRGB gamut effects)
//! - **Hue bias**: Non-uniform, varies by color region (cool colors shift cooler,
//!   warm colors shift warmer)
//!
//! ## Correction Model
//!
//! The hue correction uses a 4-harmonic Fourier series to capture the periodic,
//! non-uniform nature of hue bias. This model was trained on 29 color categories
//! from the XKCD color survey compared against Centore spectrophotometer references.
//!
//! ## Usage
//!
//! ```rust
//! use munsellspace::{MunsellConverter, MunsellColor};
//! use munsellspace::screen_correction::{correct_screen_color, ScreenCorrector};
//!
//! fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let converter = MunsellConverter::new()?;
//!
//!     // Convert an RGB color to Munsell (this gives screen-based color)
//!     let screen_munsell = converter.srgb_to_munsell([100, 200, 180])?;
//!     println!("Screen color: {}", screen_munsell);
//!
//!     // Apply correction for physical color reference
//!     let physical_munsell = correct_screen_color(&screen_munsell)?;
//!     println!("Physical color: {}", physical_munsell);
//!
//!     Ok(())
//! }
//! ```
//!
//! ## Accuracy
//!
//! The correction model achieves:
//! - Mean hue error: 5.1° (down from 17.6° with no correction)
//! - Weighted mean hue error: 7.2° (weighted by sample size)
//!
//! ## References
//!
//! Based on analysis of:
//! - XKCD Color Survey (175,844 color names from web users)
//! - Centore Polyhedron Data (30 spectrophotometer-measured color categories)

use crate::error::{MunsellError, Result};
use crate::semantic_overlay::parse_hue_to_number;
use crate::types::MunsellColor;

/// Correction constants derived from XKCD vs Centore comparison
///
/// Value correction: subtract from screen value to get physical value
pub const VALUE_CORRECTION: f64 = 0.898734;

/// Chroma correction: subtract from screen chroma to get physical chroma
pub const CHROMA_CORRECTION: f64 = 4.638094;

/// Fourier coefficients for hue correction
///
/// The hue correction is computed as:
/// ```text
/// correction = a0 + sum(a_k * cos(k * hue_rad) + b_k * sin(k * hue_rad))
/// ```
///
/// where hue_rad is the hue in radians (0-360° mapped to 0-2π)
const HUE_COEFFS: [f64; 9] = [
    -2.930815,   // a0 (constant term)
    6.500663,    // a1 (cos 1x)
    15.948564,   // b1 (sin 1x)
    -7.674857,   // a2 (cos 2x)
    6.927067,    // b2 (sin 2x)
    9.247554,    // a3 (cos 3x)
    -17.936596,  // b3 (sin 3x)
    -10.873069,  // a4 (cos 4x)
    7.078384,    // b4 (sin 4x)
];

/// Number of harmonics in the Fourier model
const N_HARMONICS: usize = 4;

/// Predict the hue correction to apply for a given screen hue.
///
/// # Arguments
/// * `hue_degrees` - Screen hue in degrees (0-360)
///
/// # Returns
/// The hue correction in degrees. Subtract this from the screen hue to get
/// the physical hue estimate.
///
/// # Example
/// ```
/// use munsellspace::screen_correction::predict_hue_correction;
///
/// // For teal region (~180°), expect large negative correction (screen is bluer)
/// let correction = predict_hue_correction(180.0);
/// assert!(correction < -30.0);
///
/// // For beige region (~90°), expect positive correction (screen is yellower)
/// let correction = predict_hue_correction(90.0);
/// assert!(correction > 20.0);
/// ```
pub fn predict_hue_correction(hue_degrees: f64) -> f64 {
    let hue_rad = hue_degrees.to_radians();

    let mut correction = HUE_COEFFS[0]; // constant term

    for k in 1..=N_HARMONICS {
        let idx = 2 * k - 1;
        correction += HUE_COEFFS[idx] * ((k as f64) * hue_rad).cos();
        correction += HUE_COEFFS[idx + 1] * ((k as f64) * hue_rad).sin();
    }

    correction
}

/// Convert hue number (0-40 Munsell scale) to degrees (0-360).
fn hue_number_to_degrees(hue_num: f64) -> f64 {
    hue_num * 9.0
}

/// Convert degrees (0-360) to hue number (0-40 Munsell scale).
fn degrees_to_hue_number(degrees: f64) -> f64 {
    // Normalize to 0-360
    let mut deg = degrees % 360.0;
    if deg < 0.0 {
        deg += 360.0;
    }
    deg / 9.0
}

/// Convert a hue number to a Munsell hue string.
fn hue_number_to_string(hue_num: f64) -> String {
    // Normalize to 0-40
    let mut hue = hue_num % 40.0;
    if hue < 0.0 {
        hue += 40.0;
    }

    // Map to hue family
    // 0-4: R, 4-8: YR, 8-12: Y, 12-16: GY, 16-20: G,
    // 20-24: BG, 24-28: B, 28-32: PB, 32-36: P, 36-40: RP
    let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    let family_idx = (hue / 4.0).floor() as usize % 10;
    let family = families[family_idx];

    // Get the number within the family (0-10, where 5 is the center)
    let num_in_family = (hue % 4.0) * 2.5;

    if num_in_family == 0.0 {
        // Use 10 from the previous family
        let prev_family = families[(family_idx + 9) % 10];
        format!("10{}", prev_family)
    } else {
        format!("{:.1}{}", num_in_family, family)
    }
}

/// Screen-to-physical color corrector.
///
/// This struct provides methods to correct Munsell colors derived from
/// screen (RGB) sources to more accurate physical color references.
#[derive(Debug, Clone, Copy)]
pub struct ScreenCorrector {
    /// Value correction factor
    pub value_correction: f64,
    /// Chroma correction factor
    pub chroma_correction: f64,
    /// Minimum chroma after correction (to avoid negative values)
    pub min_chroma: f64,
    /// Minimum value after correction
    pub min_value: f64,
    /// Maximum value after correction
    pub max_value: f64,
}

impl Default for ScreenCorrector {
    fn default() -> Self {
        Self::new()
    }
}

impl ScreenCorrector {
    /// Create a new screen corrector with default parameters.
    #[must_use]
    pub fn new() -> Self {
        Self {
            value_correction: VALUE_CORRECTION,
            chroma_correction: CHROMA_CORRECTION,
            min_chroma: 0.0,
            min_value: 0.0,
            max_value: 10.0,
        }
    }

    /// Create a screen corrector with custom correction factors.
    ///
    /// # Arguments
    /// * `value_correction` - Value correction (subtracted from screen value)
    /// * `chroma_correction` - Chroma correction (subtracted from screen chroma)
    #[must_use]
    pub fn with_custom(value_correction: f64, chroma_correction: f64) -> Self {
        Self {
            value_correction,
            chroma_correction,
            min_chroma: 0.0,
            min_value: 0.0,
            max_value: 10.0,
        }
    }

    /// Correct a screen-derived Munsell color to physical reference.
    ///
    /// # Arguments
    /// * `screen_color` - Munsell color derived from RGB screen color
    ///
    /// # Returns
    /// Corrected Munsell color approximating physical color reference
    ///
    /// # Errors
    /// Returns error if hue parsing fails for chromatic colors
    pub fn correct(&self, screen_color: &MunsellColor) -> Result<MunsellColor> {
        // Handle neutral colors (no hue correction needed)
        if screen_color.is_neutral() {
            let corrected_value = (screen_color.value - self.value_correction)
                .clamp(self.min_value, self.max_value);
            return Ok(MunsellColor::new_neutral(corrected_value));
        }

        // Get hue string and convert to degrees
        let hue_str = screen_color.hue.as_ref().ok_or_else(|| MunsellError::InvalidNotation {
            notation: screen_color.notation.clone(),
            reason: "Expected hue for chromatic color".to_string(),
        })?;

        let hue_num = parse_hue_to_number(hue_str).ok_or_else(|| MunsellError::InvalidNotation {
            notation: screen_color.notation.clone(),
            reason: format!("Failed to parse hue: {}", hue_str),
        })?;
        let hue_degrees = hue_number_to_degrees(hue_num);

        // Compute corrections
        let hue_correction = predict_hue_correction(hue_degrees);
        let corrected_hue_degrees = hue_degrees - hue_correction;
        let corrected_hue_num = degrees_to_hue_number(corrected_hue_degrees);
        let corrected_hue_str = hue_number_to_string(corrected_hue_num);

        let corrected_value = (screen_color.value - self.value_correction)
            .clamp(self.min_value, self.max_value);

        let screen_chroma = screen_color.chroma.unwrap_or(0.0);
        let corrected_chroma = (screen_chroma - self.chroma_correction).max(self.min_chroma);

        // If corrected chroma is essentially zero, return neutral
        if corrected_chroma < 0.1 {
            return Ok(MunsellColor::new_neutral(corrected_value));
        }

        Ok(MunsellColor::new_chromatic(
            corrected_hue_str,
            corrected_value,
            corrected_chroma,
        ))
    }

    /// Get the hue correction for a given screen hue in degrees.
    ///
    /// # Arguments
    /// * `hue_degrees` - Screen hue in degrees (0-360)
    ///
    /// # Returns
    /// Hue correction in degrees (subtract from screen hue)
    #[must_use]
    pub fn get_hue_correction(&self, hue_degrees: f64) -> f64 {
        predict_hue_correction(hue_degrees)
    }
}

/// Convenience function to correct a screen-derived Munsell color.
///
/// This is equivalent to `ScreenCorrector::new().correct(color)`.
///
/// # Arguments
/// * `screen_color` - Munsell color derived from RGB screen color
///
/// # Returns
/// Corrected Munsell color approximating physical color reference
///
/// # Errors
/// Returns error if hue parsing fails for chromatic colors
///
/// # Example
/// ```
/// use munsellspace::{MunsellColor, screen_correction::correct_screen_color};
///
/// let screen = MunsellColor::new_chromatic("5BG".to_string(), 7.0, 10.0);
/// let physical = correct_screen_color(&screen).unwrap();
///
/// // Value should be lower (screen colors appear lighter)
/// assert!(physical.value < screen.value);
///
/// // Chroma should be lower (screen colors appear more saturated)
/// assert!(physical.chroma.unwrap() < screen.chroma.unwrap());
/// ```
pub fn correct_screen_color(screen_color: &MunsellColor) -> Result<MunsellColor> {
    ScreenCorrector::new().correct(screen_color)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hue_correction_cool_colors() {
        // Teal region (~180°) should have negative correction (screen is bluer)
        let correction = predict_hue_correction(180.0);
        assert!(correction < -30.0, "Teal should shift toward cyan, got {}", correction);

        // Aqua/turquoise region
        let correction = predict_hue_correction(182.0);
        assert!(correction < -30.0, "Aqua should shift toward cyan, got {}", correction);
    }

    #[test]
    fn test_hue_correction_warm_colors() {
        // Beige/tan region (~90°) should have positive correction
        let correction = predict_hue_correction(90.0);
        assert!(correction > 20.0, "Beige region should shift toward yellow, got {}", correction);

        // Yellow region
        let correction = predict_hue_correction(110.0);
        assert!(correction > 20.0, "Yellow should shift toward yellow, got {}", correction);
    }

    #[test]
    fn test_hue_correction_primaries() {
        // Red (~20°) should have small correction
        let correction = predict_hue_correction(20.0);
        assert!(correction.abs() < 15.0, "Red should be stable, got {}", correction);

        // Blue (~245°) should have moderate negative correction
        let correction = predict_hue_correction(245.0);
        assert!(correction.abs() < 20.0, "Blue should be relatively stable, got {}", correction);
    }

    #[test]
    fn test_value_correction() {
        let corrector = ScreenCorrector::new();

        // Value should decrease
        let screen = MunsellColor::new_chromatic("5R".to_string(), 7.0, 10.0);
        let physical = corrector.correct(&screen).unwrap();
        assert!(physical.value < screen.value);
        assert!((physical.value - (7.0 - VALUE_CORRECTION)).abs() < 0.01);
    }

    #[test]
    fn test_chroma_correction() {
        let corrector = ScreenCorrector::new();

        // Chroma should decrease
        let screen = MunsellColor::new_chromatic("5R".to_string(), 5.0, 12.0);
        let physical = corrector.correct(&screen).unwrap();
        assert!(physical.chroma.unwrap() < screen.chroma.unwrap());
        assert!((physical.chroma.unwrap() - (12.0 - CHROMA_CORRECTION)).abs() < 0.01);
    }

    #[test]
    fn test_neutral_color() {
        let corrector = ScreenCorrector::new();

        let screen = MunsellColor::new_neutral(7.0);
        let physical = corrector.correct(&screen).unwrap();

        assert!(physical.is_neutral());
        assert!((physical.value - (7.0 - VALUE_CORRECTION)).abs() < 0.01);
    }

    #[test]
    fn test_low_chroma_becomes_neutral() {
        let corrector = ScreenCorrector::new();

        // If chroma is below correction, should become neutral
        let screen = MunsellColor::new_chromatic("5R".to_string(), 5.0, 4.0);
        let physical = corrector.correct(&screen).unwrap();

        // Chroma after correction would be negative, should be 0
        assert!(physical.chroma.unwrap_or(0.0) < 0.1);
    }

    #[test]
    fn test_hue_number_conversions() {
        // Test round-trip conversion
        let hue_num = 15.0; // 5GY
        let degrees = hue_number_to_degrees(hue_num);
        assert!((degrees - 135.0).abs() < 0.01);

        let back = degrees_to_hue_number(degrees);
        assert!((back - hue_num).abs() < 0.01);
    }

    #[test]
    fn test_hue_string_generation() {
        // Test hue number to string
        assert_eq!(hue_number_to_string(0.0), "10RP");
        assert_eq!(hue_number_to_string(2.0), "5.0R");
        assert_eq!(hue_number_to_string(4.0), "10R");
        assert_eq!(hue_number_to_string(6.0), "5.0YR");
        assert_eq!(hue_number_to_string(10.0), "5.0Y");
    }

    #[test]
    fn test_correct_screen_color_function() {
        let screen = MunsellColor::new_chromatic("5BG".to_string(), 7.0, 8.0);
        let physical = correct_screen_color(&screen).unwrap();

        assert!(physical.value < screen.value);
        assert!(physical.chroma.unwrap() < screen.chroma.unwrap());
    }
}
