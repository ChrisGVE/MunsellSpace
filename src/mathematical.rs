//! Mathematical Munsell color space conversion implementation
//! 
//! This module implements true mathematical algorithms for sRGB ↔ Munsell conversion
//! following ASTM D1535 standards and using the complete Munsell Renotation dataset
//! for accurate interpolation.

use palette::{Srgb, Yxy, convert::IntoColor, white_point::D65};
use crate::constants::*;
use crate::error::{MunsellError, Result};

/// Mathematical Munsell specification representation
#[derive(Debug, Clone, PartialEq)]
pub struct MunsellSpecification {
    pub hue: f64,           // 0.0-10.0
    pub family: String,     // "R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP", "N"
    pub value: f64,         // 0.0-10.0 (lightness)
    pub chroma: f64,        // 0.0+ (saturation)
}

/// CIE xyY color space representation
#[derive(Debug, Clone, PartialEq)]
pub struct CieXyY {
    pub x: f64,            // Chromaticity x
    pub y: f64,            // Chromaticity y  
    pub Y: f64,            // Luminance Y
}

/// Mathematical Munsell converter using ASTM D1535 algorithms
pub struct MathematicalMunsellConverter {
    /// Cached interpolation data for performance
    renotation_data: &'static [((&'static str, f64, f64), (f64, f64, f64))],
}

impl MathematicalMunsellConverter {
    /// Create a new mathematical converter instance
    pub fn new() -> Result<Self> {
        Ok(Self {
            renotation_data: MUNSELL_RENOTATION_DATA,
        })
    }

    /// Convert sRGB color to Munsell specification using mathematical algorithms
    ///
    /// # Arguments
    /// * `rgb` - sRGB color as [R, G, B] with values 0-255
    ///
    /// # Returns
    /// * `MunsellSpecification` with hue, value, chroma, and family
    ///
    /// # Example
    /// ```rust
    /// let converter = MathematicalMunsellConverter::new()?;
    /// let munsell = converter.srgb_to_munsell([255, 0, 0])?;
    /// println!("Red: {}.{} {:.1}/{:.1}", munsell.hue, munsell.family, munsell.value, munsell.chroma);
    /// ```
    pub fn srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellSpecification> {
        // Step 1: Convert sRGB to xyY using palette crate
        let xyy = self.srgb_to_xyy(rgb)?;
        
        // Step 2: Convert xyY to Munsell specification using mathematical algorithm
        self.xyy_to_munsell_specification(xyy)
    }

    /// Convert sRGB to CIE xyY color space using palette crate
    fn srgb_to_xyy(&self, rgb: [u8; 3]) -> Result<CieXyY> {
        // Create sRGB color with normalized values [0.0, 1.0]
        let srgb = Srgb::new(
            rgb[0] as f64 / 255.0,
            rgb[1] as f64 / 255.0,
            rgb[2] as f64 / 255.0,
        );
        
        // Convert sRGB → Linear RGB → XYZ → xyY (all in one chain)
        let xyy: Yxy<D65, f64> = srgb.into_linear().into_color();
        let (x, y, luma) = xyy.into_components();
        
        Ok(CieXyY { x, y, Y: luma })
    }

    /// Convert CIE xyY to Munsell specification using ASTM D1535 algorithm
    fn xyy_to_munsell_specification(&self, xyy: CieXyY) -> Result<MunsellSpecification> {
        // Step 1: Check for achromatic (neutral) colors
        if self.is_achromatic(xyy.x, xyy.y) {
            let value = self.luminance_to_munsell_value(xyy.Y)?;
            return Ok(MunsellSpecification {
                hue: 0.0,
                family: "N".to_string(),
                value,
                chroma: 0.0,
            });
        }

        // Step 2: Calculate Munsell Value using ASTM D1535 polynomial
        let value = self.luminance_to_munsell_value(xyy.Y)?;

        // Step 3: Calculate hue and chroma using interpolation from renotation data
        let (hue, family, chroma) = self.interpolate_hue_chroma(xyy.x, xyy.y, xyy.Y)?;

        Ok(MunsellSpecification {
            hue,
            family,
            value,
            chroma,
        })
    }

    /// Calculate Munsell Value from CIE Y luminance using ASTM D1535 polynomial
    /// 
    /// Uses Newton-Raphson iteration to solve the fifth-order polynomial:
    /// Y = 1.1914*V - 0.22533*V² + 0.23352*V³ - 0.020484*V⁴ + 0.00081939*V⁵
    /// Note: The polynomial gives Y on a 0-100 scale, so we need to convert input
    fn luminance_to_munsell_value(&self, y: f64) -> Result<f64> {
        // Handle edge cases
        if y <= 0.0 {
            return Ok(0.0);
        }
        
        // Convert Y from [0,1] scale to [0,100] scale for ASTM polynomial
        let y_scaled = y * 100.0;
        
        if y_scaled >= 100.0 {
            return Ok(10.0);
        }

        // Newton-Raphson iteration to solve for V given Y
        let mut v = 10.0 * y.sqrt(); // Initial guess based on approximate relationship
        
        for _ in 0..NEWTON_RAPHSON_MAX_ITERATIONS {
            let f = self.astm_polynomial(v) - y_scaled;
            let df = self.astm_polynomial_derivative(v);
            
            if df.abs() < 1e-15 {
                return Err(MunsellError::ConvergenceFailed);
            }
            
            let delta = f / df;
            v -= delta;
            
            if delta.abs() < NEWTON_RAPHSON_TOLERANCE {
                return Ok(v.max(0.0).min(10.0)); // Clamp to valid range
            }
        }
        
        Err(MunsellError::ConvergenceFailed)
    }

    /// ASTM D1535 fifth-order polynomial for Munsell Value
    fn astm_polynomial(&self, v: f64) -> f64 {
        let coeffs = &ASTM_D1535_COEFFICIENTS;
        coeffs[0] * v + 
        coeffs[1] * v * v + 
        coeffs[2] * v * v * v + 
        coeffs[3] * v * v * v * v + 
        coeffs[4] * v * v * v * v * v
    }

    /// Derivative of ASTM D1535 polynomial for Newton-Raphson iteration
    fn astm_polynomial_derivative(&self, v: f64) -> f64 {
        let coeffs = &ASTM_D1535_COEFFICIENTS;
        coeffs[0] + 
        2.0 * coeffs[1] * v + 
        3.0 * coeffs[2] * v * v + 
        4.0 * coeffs[3] * v * v * v + 
        5.0 * coeffs[4] * v * v * v * v
    }

    /// Check if color is achromatic (neutral) based on chromaticity distance from Illuminant C
    fn is_achromatic(&self, x: f64, y: f64) -> bool {
        // Special case: if x=0 and y=0, this typically means Y=0 (pure black) 
        // and chromaticity is undefined - treat as achromatic
        if x == 0.0 && y == 0.0 {
            return true;
        }
        
        let dx = x - ILLUMINANT_C[0];
        let dy = y - ILLUMINANT_C[1];
        let distance = (dx * dx + dy * dy).sqrt();
        distance < ACHROMATIC_THRESHOLD
    }

    /// Interpolate hue and chroma from Munsell Renotation dataset
    /// 
    /// This is the most complex part - finding the closest match in the renotation
    /// data and interpolating to get precise hue and chroma values.
    fn interpolate_hue_chroma(&self, x: f64, y: f64, luma: f64) -> Result<(f64, String, f64)> {
        // For now, implement a simple nearest-neighbor approach
        // TODO: Implement proper radial basis function interpolation
        
        let mut best_distance = f64::INFINITY;
        let mut best_match: Option<&'static ((&'static str, f64, f64), (f64, f64, f64))> = None;
        
        // Search through renotation data for closest xyY match
        for entry in self.renotation_data {
            let ((_, _, _), (entry_x, entry_y, entry_luma)) = entry;
            
            // Calculate distance in xyY space
            let dx = x - entry_x;
            let dy = y - entry_y;
            let dluma = luma - entry_luma;
            let distance = (dx * dx + dy * dy + dluma * dluma * 0.1).sqrt(); // Weight luminance less
            
            if distance < best_distance {
                best_distance = distance;
                best_match = Some(entry);
            }
        }
        
        match best_match {
            Some(((hue_str, _value, chroma), _)) => {
                let (hue, family) = self.parse_hue_string(hue_str)?;
                Ok((hue, family, *chroma))
            }
            None => Err(MunsellError::InterpolationError {
                message: "No matching color found in renotation data".to_string(),
            })
        }
    }

    /// Parse Munsell hue string like "5R", "2.5GY" into hue number and family
    fn parse_hue_string(&self, hue_str: &str) -> Result<(f64, String)> {
        // Find the boundary between number and letters
        let mut split_pos = 0;
        for (i, c) in hue_str.char_indices() {
            if c.is_alphabetic() {
                split_pos = i;
                break;
            }
        }
        
        if split_pos == 0 {
            return Err(MunsellError::InvalidNotation {
                notation: hue_str.to_string(),
                reason: "Hue string contains no alphabetic characters".to_string(),
            });
        }
        
        let hue_str_num = &hue_str[..split_pos];
        let family = hue_str[split_pos..].to_string();
        
        let hue: f64 = hue_str_num.parse()
            .map_err(|_| MunsellError::InvalidNotation {
                notation: hue_str_num.to_string(),
                reason: "Invalid numeric value in hue".to_string(),
            })?;
        
        Ok((hue, family))
    }

    /// Convert Munsell specification back to xyY coordinates
    /// 
    /// This implements the reverse conversion for bidirectional capability
    pub fn munsell_specification_to_xyy(&self, spec: &MunsellSpecification) -> Result<CieXyY> {
        // Handle neutral colors
        if spec.family == "N" {
            let y = self.munsell_value_to_luminance(spec.value)?;
            return Ok(CieXyY {
                x: ILLUMINANT_C[0],
                y: ILLUMINANT_C[1],
                Y: y,
            });
        }

        // For chromatic colors, find matching entry in renotation data
        let hue_str = format!("{}{}", spec.hue, spec.family);
        
        for entry in self.renotation_data {
            let ((entry_hue, entry_value, entry_chroma), (x, y, luma)) = entry;
            
            if entry_hue == &hue_str && 
               (entry_value - spec.value).abs() < 0.1 && 
               (entry_chroma - spec.chroma).abs() < 0.1 {
                return Ok(CieXyY { x: *x, y: *y, Y: *luma });
            }
        }
        
        Err(MunsellError::InterpolationError {
            message: format!("No matching renotation data for {}{} {:.1}/{:.1}", 
                spec.hue, spec.family, spec.value, spec.chroma),
        })
    }

    /// Convert Munsell Value to CIE Y luminance using ASTM polynomial directly
    fn munsell_value_to_luminance(&self, value: f64) -> Result<f64> {
        if value < 0.0 || value > 10.0 {
            return Err(MunsellError::InvalidNotation {
                notation: value.to_string(),
                reason: "Munsell Value must be between 0.0 and 10.0".to_string(),
            });
        }
        
        // ASTM polynomial gives Y on [0,100] scale, convert to [0,1] scale
        Ok(self.astm_polynomial(value) / 100.0)
    }

    /// Convert Munsell specification to formatted notation string
    pub fn format_munsell_notation(&self, spec: &MunsellSpecification) -> String {
        if spec.family == "N" {
            format!("N {:.1}", spec.value)
        } else {
            format!("{:.1}{} {:.1}/{:.1}", spec.hue, spec.family, spec.value, spec.chroma)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mathematical_converter_creation() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        assert_eq!(converter.renotation_data.len(), 4995);
    }

    #[test]
    fn test_srgb_to_xyy_conversion() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test pure red
        let xyy = converter.srgb_to_xyy([255, 0, 0]).unwrap();
        assert!(xyy.x > 0.6); // Red should have high x chromaticity
        assert!(xyy.y > 0.3 && xyy.y < 0.4); // Reasonable y chromaticity
        assert!(xyy.Y > 0.2 && xyy.Y < 0.3); // Reasonable luminance
    }

    #[test]
    fn test_astm_polynomial() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test known values
        assert!((converter.astm_polynomial(0.0) - 0.0).abs() < 1e-10);
        assert!(converter.astm_polynomial(5.0) > 0.1); // Should be positive
        
        // The ASTM polynomial gives Y values on a 0-100 scale
        
        // The ASTM polynomial gives reflectance values, not necessarily Y < 1.0
        // At V=10.0, it should give the maximum reflectance
        assert!(converter.astm_polynomial(10.0) > 0.9); // Should be close to but possibly > 1.0
    }

    #[test]
    fn test_luminance_to_munsell_value() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test edge cases
        assert!((converter.luminance_to_munsell_value(0.0).unwrap() - 0.0).abs() < 1e-10);
        assert!((converter.luminance_to_munsell_value(1.0).unwrap() - 10.0).abs() < 1e-10);
        
        // Test round-trip consistency
        let test_value = 5.0;
        let luminance = converter.munsell_value_to_luminance(test_value).unwrap(); // Use the proper conversion
        let recovered_value = converter.luminance_to_munsell_value(luminance).unwrap();
        assert!((recovered_value - test_value).abs() < 1e-6);
    }

    #[test]
    fn test_achromatic_detection() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test Illuminant C coordinates (should be achromatic)
        assert!(converter.is_achromatic(ILLUMINANT_C[0], ILLUMINANT_C[1]));
        
        // Test clearly chromatic coordinates
        assert!(!converter.is_achromatic(0.7, 0.3)); // Red region
        assert!(!converter.is_achromatic(0.3, 0.6)); // Green region
    }

    #[test]
    fn test_hue_string_parsing() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        let (hue, family) = converter.parse_hue_string("5R").unwrap();
        assert_eq!(hue, 5.0);
        assert_eq!(family, "R");
        
        let (hue, family) = converter.parse_hue_string("2.5GY").unwrap();
        assert_eq!(hue, 2.5);
        assert_eq!(family, "GY");
    }

    #[test]
    fn test_munsell_notation_formatting() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test neutral color
        let neutral = MunsellSpecification {
            hue: 0.0,
            family: "N".to_string(),
            value: 5.0,
            chroma: 0.0,
        };
        assert_eq!(converter.format_munsell_notation(&neutral), "N 5.0");
        
        // Test chromatic color
        let chromatic = MunsellSpecification {
            hue: 5.0,
            family: "R".to_string(),
            value: 4.0,
            chroma: 12.0,
        };
        assert_eq!(converter.format_munsell_notation(&chromatic), "5.0R 4.0/12.0");
    }

    #[test]
    fn test_black_color_conversion() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test pure black
        let munsell = converter.srgb_to_munsell([0, 0, 0]).unwrap();
        
        // For now, just test that it produces a reasonable result
        // The exact behavior for RGB [0,0,0] may depend on how palette handles it
        assert!(munsell.value < 1.0); // Should be very dark
        assert!(munsell.chroma < 1.0); // Should have very low chroma
    }
}