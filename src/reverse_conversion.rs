//! Reverse conversion pipeline: Munsell → Lab → sRGB/hex/HSL/HSV
//!
//! This module implements comprehensive reverse conversion from Munsell color
//! specifications to various color spaces and formats, using CIE Lab as an
//! intermediate color space for maximum accuracy and color science compliance.

use crate::mathematical::{MathematicalMunsellConverter, MunsellSpecification, CieXyY};
use crate::munsell_converter_core::PythonMunsellConverter;
use crate::color_notation_parser::munsell_colour_to_munsell_specification;
use crate::munsell_color_science::munsell_specification_to_xyy;
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
    /// Python-compatible converter for accurate reverse conversion
    python_converter: PythonMunsellConverter,
}

impl ReverseConverter {
    /// Create a new reverse converter with default configuration
    pub fn new() -> Result<Self> {
        Ok(Self {
            converter: MathematicalMunsellConverter::new()?,
            python_converter: PythonMunsellConverter::new(),
        })
    }
    
    /// Create reverse converter with custom mathematical converter
    pub fn with_converter(converter: MathematicalMunsellConverter) -> Self {
        Self { 
            converter, 
            python_converter: PythonMunsellConverter::new(),
        }
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
    /// use munsellspace::mathematical::MunsellSpecification;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
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
    /// # Ok(())
    /// # }
    /// ```
    pub fn munsell_to_all_formats(&self, spec: &MunsellSpecification) -> Result<ColorFormats> {
        // Step 1: Munsell → xyY (via Python port for accuracy)
        let spec_array = self.munsell_spec_to_array(spec)?;
        let xyy_array = munsell_specification_to_xyy(&spec_array)?;
        let xyy = CieXyY { x: xyy_array[0], y: xyy_array[1], y_luminance: xyy_array[2] };
        
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
        let spec_array = self.munsell_spec_to_array(spec)?;
        let xyy_array = munsell_specification_to_xyy(&spec_array)?;
        let xyy = CieXyY { x: xyy_array[0], y: xyy_array[1], y_luminance: xyy_array[2] };
        let xyz = self.xyy_to_xyz(&xyy)?;
        self.xyz_to_lab(xyz)
    }
    
    /// Convert Munsell specification to sRGB [0-255]
    pub fn munsell_to_srgb(&self, spec: &MunsellSpecification) -> Result<[u8; 3]> {
        // Convert MunsellSpecification to notation string
        let notation = self.spec_to_notation_string(spec)?;
        
        // Use Python converter for accurate reverse conversion
        let rgb_color = self.python_converter.munsell_to_srgb(&notation)?;
        
        Ok([rgb_color.r, rgb_color.g, rgb_color.b])
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
    
    /// Convert MunsellSpecification to Python port format [hue, value, chroma, code]
    fn munsell_spec_to_array(&self, spec: &MunsellSpecification) -> Result<[f64; 4]> {
        // Handle neutral colors
        if spec.family == "N" {
            return Ok([f64::NAN, spec.value, 0.0, f64::NAN]);
        }
        
        // Convert family string to numeric code
        let code = match spec.family.as_str() {
            "B" => 1,
            "BG" => 2,
            "G" => 3,
            "GY" => 4,
            "Y" => 5,
            "YR" => 6,
            "R" => 7,
            "RP" => 8,
            "P" => 9,
            "PB" => 10,
            _ => return Err(MunsellError::InvalidNotation {
                notation: spec.family.clone(),
                reason: "Invalid family code".to_string(),
            }),
        };
        
        Ok([spec.hue, spec.value, spec.chroma, code as f64])
    }
    
    /// Convert MunsellSpecification to notation string (e.g., "5R 4/14" or "N 5")
    fn spec_to_notation_string(&self, spec: &MunsellSpecification) -> Result<String> {
        // Handle neutral colors
        if spec.family == "N" {
            return Ok(format!("N {}", spec.value));
        }
        
        // Handle chromatic colors
        let hue_str = if spec.hue == spec.hue.floor() {
            format!("{}", spec.hue as i32)
        } else {
            format!("{:.1}", spec.hue)
        };
        
        Ok(format!("{}{} {}/{}", hue_str, spec.family, spec.value, spec.chroma))
    }
    
    /// Convert array format [hue, value, chroma, code] back to MunsellSpecification
    fn array_to_munsell_spec(&self, spec_array: [f64; 4]) -> Result<MunsellSpecification> {
        // Handle neutral colors
        if spec_array[0].is_nan() && spec_array[2].is_nan() {
            return Ok(MunsellSpecification {
                hue: 0.0,
                family: "N".to_string(),
                value: spec_array[1],
                chroma: 0.0,
            });
        }
        
        // Convert numeric code back to family string
        let family = match spec_array[3] as u8 {
            1 => "B",
            2 => "BG",
            3 => "G",
            4 => "GY",
            5 => "Y",
            6 => "YR",
            7 => "R",
            8 => "RP",
            9 => "P",
            10 => "PB",
            code => return Err(MunsellError::InvalidNotation {
                notation: code.to_string(),
                reason: "Invalid family code".to_string(),
            }),
        };
        
        Ok(MunsellSpecification {
            hue: spec_array[0],
            family: family.to_string(),
            value: spec_array[1],
            chroma: spec_array[2],
        })
    }
    
    /// Convert xyY to XYZ color space
    fn xyy_to_xyz(&self, xyy: &CieXyY) -> Result<[f64; 3]> {
        if xyy.y == 0.0 {
            // Handle black color
            Ok([0.0, 0.0, 0.0])
        } else {
            Ok([
                xyy.x * xyy.y_luminance / xyy.y,                    // X
                xyy.y_luminance,                                    // Y 
                (1.0 - xyy.x - xyy.y) * xyy.y_luminance / xyy.y,   // Z
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
/// use munsellspace::munsell_to_hex_string;
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let hex = munsell_to_hex_string("5R 4/14")?;
/// println!("Hex: {}", hex); // e.g., "#C41E3A"
/// # Ok(())
/// # }
/// ```
pub fn munsell_to_hex_string(munsell_notation: &str) -> Result<String> {
    let spec = parse_munsell_notation(munsell_notation)?;
    let converter = ReverseConverter::new()?;
    converter.munsell_to_hex(&spec)
}

/// Parse Munsell notation string to MunsellSpecification using Python-ported parser
/// 
/// Supports formats like:
/// - "5R 4/14" (standard format)
/// - "N 5", "N5", "N5/", "N 5/", "N5/0", "N 5/0.0" (neutral colors)
/// - "2.5YR 6/8" (decimal hue)
pub fn parse_munsell_notation(notation: &str) -> Result<MunsellSpecification> {
    // Use Python-ported parser for consistency
    let spec_array = munsell_colour_to_munsell_specification(notation)?;
    
    // Create a dummy converter to use the helper method
    let converter = ReverseConverter::new()?;
    converter.array_to_munsell_spec(spec_array)
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
        
        // Test neutral color (Python format without space)
        let spec = parse_munsell_notation("N5").unwrap();
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
    
    #[test]
    fn test_comprehensive_reverse_conversion() {
        let converter = ReverseConverter::new().unwrap();
        
        // Test a red color
        let red_spec = MunsellSpecification {
            hue: 5.0,
            family: "R".to_string(),
            value: 4.0,
            chroma: 14.0,
        };
        
        // Test individual methods
        let srgb = converter.munsell_to_srgb(&red_spec).unwrap();
        let hex = converter.munsell_to_hex(&red_spec).unwrap();
        let lab = converter.munsell_to_lab(&red_spec).unwrap();
        let hsl = converter.munsell_to_hsl(&red_spec).unwrap();
        let hsv = converter.munsell_to_hsv(&red_spec).unwrap();
        
        // All methods should work without error
        assert!(srgb[0] > 0); // Red channel should be present
        assert!(hex.starts_with('#'));
        assert_eq!(hex.len(), 7); // Valid hex format
        assert!(lab.l > 0.0); // Positive lightness
        assert!(hsl.h >= 0.0 && hsl.h < 360.0); // Valid hue range
        assert!(hsv.v > 0.0); // Positive brightness
        
        // Test comprehensive method
        let colors = converter.munsell_to_all_formats(&red_spec).unwrap();
        
        // Results should be consistent
        assert_eq!(colors.srgb, srgb);
        assert_eq!(colors.hex, hex);
        assert_eq!(colors.lab.l, lab.l);
        assert_eq!(colors.hsl.h, hsl.h);
        assert_eq!(colors.hsv.v, hsv.v);
        
        // Verify the original spec is preserved
        assert_eq!(colors.munsell.hue, red_spec.hue);
        assert_eq!(colors.munsell.family, red_spec.family);
        assert_eq!(colors.munsell.value, red_spec.value);
        assert_eq!(colors.munsell.chroma, red_spec.chroma);
    }
}