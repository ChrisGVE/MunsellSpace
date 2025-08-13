//! General color space conversion utilities
//! 
//! This module provides convenience functions for converting between common color spaces
//! without needing to go through Munsell notation. These are useful for general color
//! processing tasks.

use crate::error::{MunsellError, Result};
use palette::{Srgb, Xyz, Lab, Hsl, Hsv, convert::IntoColor, white_point::D65};

/// Convert RGB [0-255] to hexadecimal color string
/// 
/// # Examples
/// ```rust
/// let hex = rgb_to_hex([255, 0, 0]);
/// assert_eq!(hex, "#FF0000");
/// ```
pub fn rgb_to_hex(rgb: [u8; 3]) -> String {
    format!("#{:02X}{:02X}{:02X}", rgb[0], rgb[1], rgb[2])
}

/// Convert hexadecimal color string to RGB [0-255]
/// 
/// Supports formats: #RGB, #RRGGBB, RGB, RRGGBB (case insensitive)
/// 
/// # Examples
/// ```rust
/// let rgb = hex_to_rgb("#FF0000")?;
/// assert_eq!(rgb, [255, 0, 0]);
/// ```
pub fn hex_to_rgb(hex: &str) -> Result<[u8; 3]> {
    crate::unified_cache::normalize_hex_to_rgb(hex)
}

/// Convert RGB [0-255] to CIE L*a*b* color space (D65 illuminant)
/// 
/// # Examples
/// ```rust
/// let lab = rgb_to_lab([255, 0, 0])?;
/// // Returns approximately L=53.23, a=80.11, b=67.22
/// ```
pub fn rgb_to_lab(rgb: [u8; 3]) -> Result<[f64; 3]> {
    // Convert to normalized sRGB
    let srgb = Srgb::new(
        rgb[0] as f64 / 255.0,
        rgb[1] as f64 / 255.0,
        rgb[2] as f64 / 255.0,
    );
    
    // Convert to Lab via XYZ
    let lab: Lab<D65, f64> = srgb.into_color();
    
    Ok([lab.l, lab.a, lab.b])
}

/// Convert CIE L*a*b* to RGB [0-255] (D65 illuminant)
/// 
/// # Examples
/// ```rust
/// let rgb = lab_to_rgb([53.23, 80.11, 67.22])?;
/// // Returns approximately [255, 0, 0]
/// ```
pub fn lab_to_rgb(lab: [f64; 3]) -> Result<[u8; 3]> {
    crate::unified_cache::lab_to_rgb(lab)
}

/// Convert RGB [0-255] to HSL color space
/// 
/// Returns H in degrees [0-360], S and L as percentages [0-100]
/// 
/// # Examples
/// ```rust
/// let hsl = rgb_to_hsl([255, 0, 0])?;
/// // Returns approximately H=0°, S=100%, L=50%
/// ```
pub fn rgb_to_hsl(rgb: [u8; 3]) -> Result<[f64; 3]> {
    let srgb = Srgb::new(
        rgb[0] as f64 / 255.0,
        rgb[1] as f64 / 255.0,
        rgb[2] as f64 / 255.0,
    );
    
    let hsl: Hsl<palette::encoding::Srgb, f64> = srgb.into_color();
    
    Ok([
        hsl.hue.into_positive_degrees(),
        hsl.saturation * 100.0,
        hsl.lightness * 100.0,
    ])
}

/// Convert HSL to RGB [0-255]
/// 
/// Expects H in degrees [0-360], S and L as percentages [0-100]
/// 
/// # Examples
/// ```rust
/// let rgb = hsl_to_rgb([0.0, 100.0, 50.0])?;
/// assert_eq!(rgb, [255, 0, 0]); // Pure red
/// ```
pub fn hsl_to_rgb(hsl: [f64; 3]) -> Result<[u8; 3]> {
    let hsl_color = Hsl::<palette::encoding::Srgb, f64>::new(
        hsl[0],
        hsl[1] / 100.0,
        hsl[2] / 100.0,
    );
    
    let srgb: Srgb<f64> = hsl_color.into_color();
    
    Ok([
        (srgb.red * 255.0).round().clamp(0.0, 255.0) as u8,
        (srgb.green * 255.0).round().clamp(0.0, 255.0) as u8,
        (srgb.blue * 255.0).round().clamp(0.0, 255.0) as u8,
    ])
}

/// Convert RGB [0-255] to HSV color space
/// 
/// Returns H in degrees [0-360], S and V as percentages [0-100]
/// 
/// # Examples
/// ```rust
/// let hsv = rgb_to_hsv([255, 0, 0])?;
/// // Returns approximately H=0°, S=100%, V=100%
/// ```
pub fn rgb_to_hsv(rgb: [u8; 3]) -> Result<[f64; 3]> {
    let srgb = Srgb::new(
        rgb[0] as f64 / 255.0,
        rgb[1] as f64 / 255.0,
        rgb[2] as f64 / 255.0,
    );
    
    let hsv: Hsv<palette::encoding::Srgb, f64> = srgb.into_color();
    
    Ok([
        hsv.hue.into_positive_degrees(),
        hsv.saturation * 100.0,
        hsv.value * 100.0,
    ])
}

/// Convert HSV to RGB [0-255]
/// 
/// Expects H in degrees [0-360], S and V as percentages [0-100]
/// 
/// # Examples
/// ```rust
/// let rgb = hsv_to_rgb([0.0, 100.0, 100.0])?;
/// assert_eq!(rgb, [255, 0, 0]); // Pure red
/// ```
pub fn hsv_to_rgb(hsv: [f64; 3]) -> Result<[u8; 3]> {
    let hsv_color = Hsv::<palette::encoding::Srgb, f64>::new(
        hsv[0],
        hsv[1] / 100.0,
        hsv[2] / 100.0,
    );
    
    let srgb: Srgb<f64> = hsv_color.into_color();
    
    Ok([
        (srgb.red * 255.0).round().clamp(0.0, 255.0) as u8,
        (srgb.green * 255.0).round().clamp(0.0, 255.0) as u8,
        (srgb.blue * 255.0).round().clamp(0.0, 255.0) as u8,
    ])
}

/// Convert hexadecimal to HSL
/// 
/// # Examples
/// ```rust
/// let hsl = hex_to_hsl("#FF0000")?;
/// // Returns approximately [0.0, 100.0, 50.0]
/// ```
pub fn hex_to_hsl(hex: &str) -> Result<[f64; 3]> {
    let rgb = hex_to_rgb(hex)?;
    rgb_to_hsl(rgb)
}

/// Convert HSL to hexadecimal
/// 
/// # Examples
/// ```rust
/// let hex = hsl_to_hex([0.0, 100.0, 50.0])?;
/// assert_eq!(hex, "#FF0000");
/// ```
pub fn hsl_to_hex(hsl: [f64; 3]) -> Result<String> {
    let rgb = hsl_to_rgb(hsl)?;
    Ok(rgb_to_hex(rgb))
}

/// Convert hexadecimal to HSV
/// 
/// # Examples
/// ```rust
/// let hsv = hex_to_hsv("#FF0000")?;
/// // Returns approximately [0.0, 100.0, 100.0]
/// ```
pub fn hex_to_hsv(hex: &str) -> Result<[f64; 3]> {
    let rgb = hex_to_rgb(hex)?;
    rgb_to_hsv(rgb)
}

/// Convert HSV to hexadecimal
/// 
/// # Examples
/// ```rust
/// let hex = hsv_to_hex([0.0, 100.0, 100.0])?;
/// assert_eq!(hex, "#FF0000");
/// ```
pub fn hsv_to_hex(hsv: [f64; 3]) -> Result<String> {
    let rgb = hsv_to_rgb(hsv)?;
    Ok(rgb_to_hex(rgb))
}

/// Convert Lab to HSL
/// 
/// # Examples
/// ```rust
/// let hsl = lab_to_hsl([53.23, 80.11, 67.22])?;
/// // Returns approximately [0.0, 100.0, 50.0] for red
/// ```
pub fn lab_to_hsl(lab: [f64; 3]) -> Result<[f64; 3]> {
    let rgb = lab_to_rgb(lab)?;
    rgb_to_hsl(rgb)
}

/// Convert HSL to Lab
/// 
/// # Examples
/// ```rust
/// let lab = hsl_to_lab([0.0, 100.0, 50.0])?;
/// // Returns approximately [53.23, 80.11, 67.22] for red
/// ```
pub fn hsl_to_lab(hsl: [f64; 3]) -> Result<[f64; 3]> {
    let rgb = hsl_to_rgb(hsl)?;
    rgb_to_lab(rgb)
}

/// Convert Lab to HSV
/// 
/// # Examples
/// ```rust
/// let hsv = lab_to_hsv([53.23, 80.11, 67.22])?;
/// // Returns approximately [0.0, 100.0, 100.0] for red
/// ```
pub fn lab_to_hsv(lab: [f64; 3]) -> Result<[f64; 3]> {
    let rgb = lab_to_rgb(lab)?;
    rgb_to_hsv(rgb)
}

/// Convert HSV to Lab
/// 
/// # Examples
/// ```rust
/// let lab = hsv_to_lab([0.0, 100.0, 100.0])?;
/// // Returns approximately [53.23, 80.11, 67.22] for red
/// ```
pub fn hsv_to_lab(hsv: [f64; 3]) -> Result<[f64; 3]> {
    let rgb = hsv_to_rgb(hsv)?;
    rgb_to_lab(rgb)
}

/// Convert Lab to hexadecimal
/// 
/// # Examples
/// ```rust
/// let hex = lab_to_hex([53.23, 80.11, 67.22])?;
/// // Returns approximately "#FF0000"
/// ```
pub fn lab_to_hex(lab: [f64; 3]) -> Result<String> {
    let rgb = lab_to_rgb(lab)?;
    Ok(rgb_to_hex(rgb))
}

/// Convert hexadecimal to Lab
/// 
/// # Examples
/// ```rust
/// let lab = hex_to_lab("#FF0000")?;
/// // Returns approximately [53.23, 80.11, 67.22]
/// ```
pub fn hex_to_lab(hex: &str) -> Result<[f64; 3]> {
    let rgb = hex_to_rgb(hex)?;
    rgb_to_lab(rgb)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_rgb_hex_roundtrip() {
        let rgb = [255, 128, 64];
        let hex = rgb_to_hex(rgb);
        let rgb_back = hex_to_rgb(&hex).unwrap();
        assert_eq!(rgb, rgb_back);
    }
    
    #[test]
    fn test_rgb_hsl_roundtrip() {
        let rgb = [255, 0, 0];
        let hsl = rgb_to_hsl(rgb).unwrap();
        let rgb_back = hsl_to_rgb(hsl).unwrap();
        assert_eq!(rgb, rgb_back);
    }
    
    #[test]
    fn test_rgb_hsv_roundtrip() {
        let rgb = [0, 255, 0];
        let hsv = rgb_to_hsv(rgb).unwrap();
        let rgb_back = hsv_to_rgb(hsv).unwrap();
        assert_eq!(rgb, rgb_back);
    }
    
    #[test]
    fn test_rgb_lab_roundtrip() {
        let rgb = [128, 128, 128];
        let lab = rgb_to_lab(rgb).unwrap();
        let rgb_back = lab_to_rgb(lab).unwrap();
        // Lab conversion may have small rounding errors
        assert!((rgb[0] as i32 - rgb_back[0] as i32).abs() <= 2);
        assert!((rgb[1] as i32 - rgb_back[1] as i32).abs() <= 2);
        assert!((rgb[2] as i32 - rgb_back[2] as i32).abs() <= 2);
    }
    
    #[test]
    fn test_cross_conversions() {
        // Test hex -> hsl -> hsv -> lab -> hex
        let hex1 = "#FF8040";
        let hsl = hex_to_hsl(hex1).unwrap();
        let hsv = lab_to_hsv(hsl_to_lab(hsl).unwrap()).unwrap();
        let lab = hsv_to_lab(hsv).unwrap();
        let hex2 = lab_to_hex(lab).unwrap();
        
        // Should be close (allowing for rounding)
        let rgb1 = hex_to_rgb(hex1).unwrap();
        let rgb2 = hex_to_rgb(&hex2).unwrap();
        
        assert!((rgb1[0] as i32 - rgb2[0] as i32).abs() <= 3);
        assert!((rgb1[1] as i32 - rgb2[1] as i32).abs() <= 3);
        assert!((rgb1[2] as i32 - rgb2[2] as i32).abs() <= 3);
    }
}