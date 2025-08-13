//! Reverse conversion pipeline: Munsell → Lab → sRGB/hex/HSL/HSV
//!
//! This module implements comprehensive reverse conversion from Munsell color
//! specifications to various color spaces and formats, using CIE Lab as an
//! intermediate color space for maximum accuracy and color science compliance.

use crate::mathematical::{MathematicalMunsellConverter, MunsellSpecification, CieXyY};
use crate::error::{MunsellError, Result};
use palette::{Srgb, Hsl, Hsv, Xyz, convert::IntoColor, white_point::D65};

/// CIE L*a*b* color space representation
#[derive(Debug, Clone, PartialEq)]
pub struct CieLab {
    pub l: f64,  // Lightness (0-100)
    pub a: f64,  // Green-Red axis (-128 to +127)
    pub b: f64,  // Blue-Yellow axis (-128 to +127)
}

/// HSL color space representation
#[derive(Debug, Clone, PartialEq)]
pub struct HslColor {
    pub h: f64,  // Hue (0-360 degrees)
    pub s: f64,  // Saturation (0-100%)
    pub l: f64,  // Lightness (0-100%)
}

/// HSV color space representation  
#[derive(Debug, Clone, PartialEq)]
pub struct HsvColor {
    pub h: f64,  // Hue (0-360 degrees)
    pub s: f64,  // Saturation (0-100%)
    pub v: f64,  // Value/Brightness (0-100%)
}

/// Comprehensive color representation with all formats
#[derive(Debug, Clone)]
pub struct ColorFormats {
    /// Original Munsell specification
    pub munsell: MunsellSpecification,
    /// CIE L*a*b* representation
    pub lab: CieLab,
    /// sRGB values [0-255]
    pub srgb: [u8; 3],
    /// Hexadecimal color string (e.g., "#FF0000")
    pub hex: String,
    /// HSL color representation
    pub hsl: HslColor,
    /// HSV color representation
    pub hsv: HsvColor,
}

/// Reverse conversion engine with Lab intermediate step
pub struct ReverseConverter {
    /// Mathematical converter for Munsell operations
    converter: MathematicalMunsellConverter,
}

impl ReverseConverter {
    /// Create a new reverse converter with default configuration
    pub fn new() -> Result<Self> {
        Ok(Self {
            converter: MathematicalMunsellConverter::new()?,
        })
    }
    
    /// Create reverse converter with custom mathematical converter
    pub fn with_converter(converter: MathematicalMunsellConverter) -> Self {
        Self { converter }
    }
    
    /// Convert Munsell specification to all color formats
    /// 
    /// This is the main entry point for comprehensive reverse conversion.
    /// It follows the scientifically accurate pipeline: Munsell → xyY → XYZ → Lab → sRGB/HSL/HSV
    ///
    /// # Arguments
    /// * `spec` - Munsell color specification
    ///
    /// # Returns
    /// * `ColorFormats` with all color representations
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::reverse_conversion::{ReverseConverter};
    /// use munsellspace::mathematical_v2::MunsellSpecification;
    ///
    /// let converter = ReverseConverter::new()?;
    /// let munsell = MunsellSpecification {
    ///     hue: 5.0,
    ///     family: "R".to_string(),
    ///     value: 4.0,
    ///     chroma: 14.0,
    /// };
    /// 
    /// let colors = converter.munsell_to_all_formats(&munsell)?;
    /// println!("Hex: {}", colors.hex);
    /// println!("HSL: H{:.1}° S{:.1}% L{:.1}%", colors.hsl.h, colors.hsl.s, colors.hsl.l);
    /// ```
    pub fn munsell_to_all_formats(&self, spec: &MunsellSpecification) -> Result<ColorFormats> {
        // Step 1: Munsell → xyY (via mathematical converter)
        let xyy = self.converter.munsell_specification_to_xyy(spec)?;
        
        // Step 2: xyY → XYZ
        let xyz = self.xyy_to_xyz(&xyy)?;
        
        // Step 3: XYZ → Lab (intermediate color space)
        let lab = self.xyz_to_lab(xyz)?;
        
        // Step 4: Lab → XYZ → sRGB (for display)
        let srgb = self.lab_to_srgb(&lab)?;
        
        // Step 5: sRGB → Hex string
        let hex = self.srgb_to_hex(srgb);
        
        // Step 6: sRGB → HSL
        let hsl = self.srgb_to_hsl(srgb)?;
        
        // Step 7: sRGB → HSV  
        let hsv = self.srgb_to_hsv(srgb)?;
        
        Ok(ColorFormats {
            munsell: spec.clone(),
            lab,
            srgb,
            hex,
            hsl,
            hsv,
        })
    }
    
    /// Convert Munsell specification to CIE L*a*b*
    pub fn munsell_to_lab(&self, spec: &MunsellSpecification) -> Result<CieLab> {
        let xyy = self.converter.munsell_specification_to_xyy(spec)?;
        let xyz = self.xyy_to_xyz(&xyy)?;
        self.xyz_to_lab(xyz)
    }
    
    /// Convert Munsell specification to sRGB [0-255]
    pub fn munsell_to_srgb(&self, spec: &MunsellSpecification) -> Result<[u8; 3]> {
        // TODO: Implement reverse conversion with restored mathematical converter
        // self.converter.munsell_to_srgb(spec)
        Err(MunsellError::NotImplemented("Reverse conversion temporarily disabled during restoration".to_string()))
    }
    
    /// Convert Munsell specification to hexadecimal string
    pub fn munsell_to_hex(&self, spec: &MunsellSpecification) -> Result<String> {
        let srgb = self.munsell_to_srgb(spec)?;
        Ok(self.srgb_to_hex(srgb))
    }
    
    /// Convert Munsell specification to HSL
    pub fn munsell_to_hsl(&self, spec: &MunsellSpecification) -> Result<HslColor> {
        let srgb = self.munsell_to_srgb(spec)?;
        self.srgb_to_hsl(srgb)
    }
    
    /// Convert Munsell specification to HSV
    pub fn munsell_to_hsv(&self, spec: &MunsellSpecification) -> Result<HsvColor> {
        let srgb = self.munsell_to_srgb(spec)?;
        self.srgb_to_hsv(srgb)
    }
    
    // ===== PRIVATE CONVERSION METHODS =====
    
    /// Convert xyY to XYZ color space
    fn xyy_to_xyz(&self, xyy: &CieXyY) -> Result<[f64; 3]> {
        if xyy.y == 0.0 {
            // Handle black color
            Ok([0.0, 0.0, 0.0])
        } else {
            Ok([
                xyy.x * xyy.Y / xyy.y,                    // X
                xyy.Y,                                    // Y 
                (1.0 - xyy.x - xyy.y) * xyy.Y / xyy.y,   // Z
            ])
        }
    }
    
    /// Convert XYZ to CIE L*a*b* using D65 illuminant
    fn xyz_to_lab(&self, xyz: [f64; 3]) -> Result<CieLab> {
        // D65 illuminant white point
        const XN: f64 = 0.95047;
        const YN: f64 = 1.00000;
        const ZN: f64 = 1.08883;
        
        // Normalize by illuminant
        let xr = xyz[0] / XN;
        let yr = xyz[1] / YN;
        let zr = xyz[2] / ZN;
        
        // Apply Lab transformation function
        let fx = if xr > 0.008856 { xr.powf(1.0/3.0) } else { (7.787 * xr) + (16.0/116.0) };
        let fy = if yr > 0.008856 { yr.powf(1.0/3.0) } else { (7.787 * yr) + (16.0/116.0) };
        let fz = if zr > 0.008856 { zr.powf(1.0/3.0) } else { (7.787 * zr) + (16.0/116.0) };
        
        // Calculate L*a*b* values
        let l = 116.0 * fy - 16.0;
        let a = 500.0 * (fx - fy);
        let b = 200.0 * (fy - fz);
        
        Ok(CieLab { l, a, b })
    }
    
    /// Convert CIE L*a*b* to sRGB [0-255]
    fn lab_to_srgb(&self, lab: &CieLab) -> Result<[u8; 3]> {
        // Convert Lab to XYZ first
        let xyz = self.lab_to_xyz(lab)?;
        
        // Use palette crate for XYZ → sRGB conversion
        let xyz_color = Xyz::<D65, f64>::new(xyz[0], xyz[1], xyz[2]);
        let srgb: Srgb<f64> = xyz_color.into_color();
        
        // Convert to 8-bit values with clamping
        let r = (srgb.red * 255.0).round().clamp(0.0, 255.0) as u8;
        let g = (srgb.green * 255.0).round().clamp(0.0, 255.0) as u8;
        let b = (srgb.blue * 255.0).round().clamp(0.0, 255.0) as u8;
        
        Ok([r, g, b])
    }
    
    /// Convert CIE L*a*b* to XYZ
    fn lab_to_xyz(&self, lab: &CieLab) -> Result<[f64; 3]> {
        // D65 illuminant white point
        const XN: f64 = 0.95047;
        const YN: f64 = 1.00000;
        const ZN: f64 = 1.08883;
        
        let fy = (lab.l + 16.0) / 116.0;
        let fx = lab.a / 500.0 + fy;
        let fz = fy - lab.b / 200.0;
        
        let xr = if fx.powi(3) > 0.008856 { fx.powi(3) } else { (fx - 16.0/116.0) / 7.787 };
        let yr = if lab.l > (7.787 * 0.008856 + 16.0/116.0) * 116.0 { 
            fy.powi(3) 
        } else { 
            lab.l / (116.0 * 7.787) 
        };
        let zr = if fz.powi(3) > 0.008856 { fz.powi(3) } else { (fz - 16.0/116.0) / 7.787 };
        
        Ok([xr * XN, yr * YN, zr * ZN])
    }
    
    /// Convert sRGB [0-255] to hexadecimal string
    fn srgb_to_hex(&self, srgb: [u8; 3]) -> String {
        format!("#{:02X}{:02X}{:02X}", srgb[0], srgb[1], srgb[2])
    }
    
    /// Convert sRGB [0-255] to HSL
    fn srgb_to_hsl(&self, srgb: [u8; 3]) -> Result<HslColor> {
        // Use palette crate for accurate conversion
        let srgb_color = Srgb::new(
            srgb[0] as f64 / 255.0,
            srgb[1] as f64 / 255.0,
            srgb[2] as f64 / 255.0,
        );
        
        let hsl: Hsl<palette::encoding::Srgb, f64> = srgb_color.into_color();
        
        Ok(HslColor {
            h: hsl.hue.into_positive_degrees() as f64,
            s: hsl.saturation as f64 * 100.0,
            l: hsl.lightness as f64 * 100.0,
        })
    }
    
    /// Convert sRGB [0-255] to HSV
    fn srgb_to_hsv(&self, srgb: [u8; 3]) -> Result<HsvColor> {
        // Use palette crate for accurate conversion
        let srgb_color = Srgb::new(
            srgb[0] as f64 / 255.0,
            srgb[1] as f64 / 255.0,
            srgb[2] as f64 / 255.0,
        );
        
        let hsv: Hsv<palette::encoding::Srgb, f64> = srgb_color.into_color();
        
        Ok(HsvColor {
            h: hsv.hue.into_positive_degrees() as f64,
            s: hsv.saturation as f64 * 100.0,
            v: hsv.value as f64 * 100.0,
        })
    }
}

impl Default for ReverseConverter {
    fn default() -> Self {
        Self::new().expect("Failed to create default ReverseConverter")
    }
}

// ===== CONVENIENCE FUNCTIONS =====

/// Quick conversion from Munsell notation string to hex color
/// 
/// # Examples
/// ```rust
/// let hex = munsell_to_hex_string("5R 4/14")?;
/// println!("Hex: {}", hex); // e.g., "#C41E3A"
/// ```
pub fn munsell_to_hex_string(munsell_notation: &str) -> Result<String> {
    let spec = parse_munsell_notation(munsell_notation)?;
    let converter = ReverseConverter::new()?;
    converter.munsell_to_hex(&spec)
}

/// Parse Munsell notation string to MunsellSpecification
/// 
/// Supports formats like:
/// - "5R 4/14" (standard format)
/// - "N 5", "N5", "N5/", "N 5/", "N5/0", "N 5/0.0" (neutral colors)
/// - "2.5YR 6/8" (decimal hue)
pub fn parse_munsell_notation(notation: &str) -> Result<MunsellSpecification> {
    let notation = notation.trim();
    
    // Handle neutral colors (e.g., "N 5", "N5", "N5/", "N 5/", "N5/0", "N 5/0.0")
    if notation.starts_with('N') {
        let value_part = notation.strip_prefix('N').unwrap().trim();
        
        // Handle chroma part after slash (should be 0 or 0.0 for neutral colors)
        let value_str = if let Some(slash_pos) = value_part.find('/') {
            let (value_part, chroma_part) = value_part.split_at(slash_pos);
            let chroma_part = chroma_part.strip_prefix('/').unwrap().trim();
            
            // Verify chroma is 0 or 0.0 (or empty)
            if !chroma_part.is_empty() {
                let chroma: f64 = chroma_part.parse().map_err(|_| {
                    MunsellError::InvalidNotation {
                        notation: notation.to_string(),
                        reason: "Invalid neutral chroma".to_string(),
                    }
                })?;
                
                if chroma != 0.0 {
                    return Err(MunsellError::InvalidNotation {
                        notation: notation.to_string(),
                        reason: "Neutral colors must have zero chroma".to_string(),
                    });
                }
            }
            
            value_part.trim()
        } else {
            // Remove trailing slash if present (no chroma specified)
            value_part.strip_suffix('/').unwrap_or(value_part)
        };
        
        let value = value_str.parse::<f64>().map_err(|_| {
            MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid neutral value".to_string(),
            }
        })?;
        
        return Ok(MunsellSpecification {
            hue: 0.0,
            family: "N".to_string(),
            value,
            chroma: 0.0,
        });
    }
    
    // Handle chromatic colors (e.g., "5R 4/14")
    let parts: Vec<&str> = notation.split_whitespace().collect();
    if parts.len() != 2 {
        return Err(MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Expected format: 'HueFamily Value/Chroma' or 'N Value'".to_string(),
        });
    }
    
    // Parse hue and family from first part (e.g., "5R")
    let hue_part = parts[0];
    let mut hue_str = String::new();
    let mut family = String::new();
    
    for c in hue_part.chars() {
        if c.is_ascii_digit() || c == '.' {
            hue_str.push(c);
        } else {
            family.push_str(&hue_part[hue_str.len()..]);
            break;
        }
    }
    
    let hue = hue_str.parse::<f64>().map_err(|_| {
        MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Invalid hue number".to_string(),
        }
    })?;
    
    // Parse value and chroma from second part (e.g., "4/14")
    let value_chroma = parts[1];
    let vc_parts: Vec<&str> = value_chroma.split('/').collect();
    if vc_parts.len() != 2 {
        return Err(MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Value/Chroma must be separated by '/'".to_string(),
        });
    }
    
    let value = vc_parts[0].parse::<f64>().map_err(|_| {
        MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Invalid value number".to_string(),
        }
    })?;
    
    let chroma = vc_parts[1].parse::<f64>().map_err(|_| {
        MunsellError::InvalidNotation {
            notation: notation.to_string(),
            reason: "Invalid chroma number".to_string(),
        }
    })?;
    
    Ok(MunsellSpecification {
        hue,
        family,
        value,
        chroma,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_munsell_notation() {
        // Test chromatic color
        let spec = parse_munsell_notation("5R 4/14").unwrap();
        assert_eq!(spec.hue, 5.0);
        assert_eq!(spec.family, "R");
        assert_eq!(spec.value, 4.0);
        assert_eq!(spec.chroma, 14.0);
        
        // Test neutral color
        let spec = parse_munsell_notation("N 5").unwrap();
        assert_eq!(spec.hue, 0.0);
        assert_eq!(spec.family, "N");
        assert_eq!(spec.value, 5.0);
        assert_eq!(spec.chroma, 0.0);
        
        // Test decimal hue
        let spec = parse_munsell_notation("2.5YR 6/8").unwrap();
        assert_eq!(spec.hue, 2.5);
        assert_eq!(spec.family, "YR");
        assert_eq!(spec.value, 6.0);
        assert_eq!(spec.chroma, 8.0);
    }
    
    #[test]
    fn test_reverse_conversion_pipeline() {
        let converter = ReverseConverter::new().unwrap();
        
        // Test with a known red color
        let munsell = MunsellSpecification {
            hue: 5.0,
            family: "R".to_string(),
            value: 4.0,
            chroma: 14.0,
        };
        
        let colors = converter.munsell_to_all_formats(&munsell).unwrap();
        
        // Verify all formats are present
        assert_eq!(colors.munsell.family, "R");
        assert!(colors.lab.l > 0.0);
        assert!(colors.hex.starts_with('#'));
        assert_eq!(colors.hex.len(), 7);
        assert!(colors.hsl.h >= 0.0 && colors.hsl.h < 360.0);
        assert!(colors.hsv.v > 0.0);
    }
    
    #[test]
    fn test_srgb_to_hex() {
        let converter = ReverseConverter::new().unwrap();
        let hex = converter.srgb_to_hex([255, 0, 0]);
        assert_eq!(hex, "#FF0000");
        
        let hex = converter.srgb_to_hex([0, 255, 255]);
        assert_eq!(hex, "#00FFFF");
    }
    
    #[test]
    fn test_neutral_color_conversion() {
        let converter = ReverseConverter::new().unwrap();
        
        let neutral = MunsellSpecification {
            hue: 0.0,
            family: "N".to_string(),
            value: 5.0,
            chroma: 0.0,
        };
        
        let colors = converter.munsell_to_all_formats(&neutral).unwrap();
        
        // Neutral colors should have low chroma in HSL/HSV
        assert!(colors.hsl.s < 10.0); // Low saturation
        assert!(colors.hsv.s < 10.0); // Low saturation
        
        // Should be grayish
        let [r, g, b] = colors.srgb;
        let diff = ((r as i16 - g as i16).abs() + (g as i16 - b as i16).abs() + (b as i16 - r as i16).abs()) as f64;
        assert!(diff < 50.0); // Colors should be close (grayish)
    }
}