//! Python-compatible Munsell converter
//! This module integrates the exact 1:1 Python ports for accurate conversion

use crate::error::{MunsellError, Result};
use crate::python_port::*;
use crate::python_port_helpers::*;
use crate::types::{MunsellColor, RgbColor};
use crate::mathematical::{MunsellSpecification, CieXyY};

/// Python-compatible Munsell converter using exact colour-science algorithms
pub struct PythonMunsellConverter;

impl PythonMunsellConverter {
    /// Create a new Python-compatible converter
    pub fn new() -> Self {
        Self
    }
    
    /// Convert sRGB to Munsell notation using Python-compatible algorithm
    pub fn srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellColor> {
        eprintln!("DEBUG: srgb_to_munsell called with RGB({}, {}, {})", rgb[0], rgb[1], rgb[2]);
        // Convert sRGB to linear RGB
        let rgb_linear = self.srgb_to_linear(rgb);
        eprintln!("DEBUG: Converted to linear RGB");
        
        // Convert to XYZ using D65
        let xyz = self.linear_rgb_to_xyz_d65(rgb_linear);
        
        // Convert to xyY
        let xyy = self.xyz_to_xyy(xyz);
        
        // Y is already in 0-1 range from sRGB conversion
        // Convert to Munsell specification using Python algorithm
        let spec = xyy_to_munsell_specification(xyy)?;
        
        // Convert specification to MunsellColor
        self.specification_to_munsell_color(spec)
    }
    
    /// Convert Munsell notation to sRGB using Python-compatible algorithm
    pub fn munsell_to_srgb(&self, munsell: &str) -> Result<RgbColor> {
        // Parse Munsell notation
        let spec = self.parse_munsell_notation(munsell)?;
        
        // Convert to xyY
        let xyy = munsell_specification_to_xyy(&spec)?;
        
        // Y is in 0-1 range, keep it that way
        // Convert to XYZ
        let xyz = self.xyy_to_xyz(xyy);
        
        // Convert to linear RGB
        let rgb_linear = self.xyz_to_linear_rgb_d65(xyz);
        
        // Convert to sRGB
        let rgb = self.linear_to_srgb(rgb_linear);
        
        Ok(RgbColor { r: rgb[0], g: rgb[1], b: rgb[2] })
    }
    
    // Helper functions for color space conversions
    
    fn srgb_to_linear(&self, rgb: [u8; 3]) -> [f64; 3] {
        let mut linear = [0.0; 3];
        for i in 0..3 {
            let c = rgb[i] as f64 / 255.0;
            linear[i] = if c <= 0.04045 {
                c / 12.92
            } else {
                ((c + 0.055) / 1.055).powf(2.4)
            };
        }
        linear
    }
    
    fn linear_to_srgb(&self, linear: [f64; 3]) -> [u8; 3] {
        let mut rgb = [0u8; 3];
        for i in 0..3 {
            let c = linear[i];
            let srgb = if c <= 0.0031308 {
                12.92 * c
            } else {
                1.055 * c.powf(1.0 / 2.4) - 0.055
            };
            rgb[i] = (srgb * 255.0).round().clamp(0.0, 255.0) as u8;
        }
        rgb
    }
    
    fn linear_rgb_to_xyz_d65(&self, rgb: [f64; 3]) -> [f64; 3] {
        // sRGB to XYZ matrix (D65 illuminant)
        let matrix = [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ];
        
        let xyz_unscaled = [
            matrix[0][0] * rgb[0] + matrix[0][1] * rgb[1] + matrix[0][2] * rgb[2],
            matrix[1][0] * rgb[0] + matrix[1][1] * rgb[1] + matrix[1][2] * rgb[2],
            matrix[2][0] * rgb[0] + matrix[2][1] * rgb[1] + matrix[2][2] * rgb[2],
        ];
        
        // Python's colour library scales XYZ so that white (RGB 255,255,255) has Y=1.0
        // The unscaled white Y is approximately 0.9505 (sum of Y row in matrix)
        // So we need to scale by 1/0.9505 ≈ 1.052
        // But the exact value from colour library testing is closer to 1.1115
        // This matches what we observed: Python Y=0.919160 vs Rust Y=0.826933
        // Ratio = 0.919160/0.826933 = 1.1115
        
        // After extensive testing, the colour library uses this scaling:
        // const XYZ_SCALING: f64 = 1.111528762434975;  // Exact ratio from test
        
        // Actually, the Python colour library does NOT scale XYZ values
        // It returns the raw XYZ values from the sRGB matrix
        xyz_unscaled
    }
    
    fn xyz_to_linear_rgb_d65(&self, xyz: [f64; 3]) -> [f64; 3] {
        // No scaling needed since we're not scaling in linear_rgb_to_xyz_d65 anymore
        // const XYZ_SCALING: f64 = 1.111528762434975;
        let xyz_unscaled = xyz;
        
        // XYZ to sRGB matrix (D65 illuminant)
        let matrix = [
            [ 3.2404542, -1.5371385, -0.4985314],
            [-0.9692660,  1.8760108,  0.0415560],
            [ 0.0556434, -0.2040259,  1.0572252],
        ];
        
        [
            matrix[0][0] * xyz_unscaled[0] + matrix[0][1] * xyz_unscaled[1] + matrix[0][2] * xyz_unscaled[2],
            matrix[1][0] * xyz_unscaled[0] + matrix[1][1] * xyz_unscaled[1] + matrix[1][2] * xyz_unscaled[2],
            matrix[2][0] * xyz_unscaled[0] + matrix[2][1] * xyz_unscaled[1] + matrix[2][2] * xyz_unscaled[2],
        ]
    }
    
    fn xyz_to_xyy(&self, xyz: [f64; 3]) -> [f64; 3] {
        let sum = xyz[0] + xyz[1] + xyz[2];
        if sum.abs() < 1e-10 {
            // Return D65 white point for black
            [0.31271, 0.32902, 0.0]
        } else {
            [xyz[0] / sum, xyz[1] / sum, xyz[1]]
        }
    }
    
    fn xyy_to_xyz(&self, xyy: [f64; 3]) -> [f64; 3] {
        let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
        if y.abs() < 1e-10 {
            [0.0, 0.0, 0.0]
        } else {
            let big_x = x * big_y / y;
            let big_z = (1.0 - x - y) * big_y / y;
            [big_x, big_y, big_z]
        }
    }
    
    fn specification_to_munsell_color(&self, spec: [f64; 4]) -> Result<MunsellColor> {
        let hue_num = spec[0];
        let value = spec[1];
        let chroma = spec[2];
        let code = spec[3] as u8;
        
        // Handle achromatic case
        if chroma < 1e-6 || hue_num.is_nan() {
            return Ok(MunsellColor::new_neutral(value));
        }
        
        // Convert code to family using Python's mapping
        let family = match code {
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
            _ => return Err(MunsellError::ConversionError {
                message: format!("Invalid hue code: {}", code)
            }),
        };
        
        // Format hue string with proper precision
        let hue_str = if hue_num == hue_num.floor() {
            format!("{}{}", hue_num as i32, family)
        } else {
            format!("{:.1}{}", hue_num, family)
        };
        
        Ok(MunsellColor::new_chromatic(hue_str, value, chroma))
    }
    
    fn parse_munsell_notation(&self, notation: &str) -> Result<[f64; 4]> {
        // Simple parser for Munsell notation like "5R 4/14"
        let notation = notation.trim();
        
        // Check for neutral
        if notation.starts_with('N') {
            let value_str = notation.trim_start_matches('N').trim();
            let value: f64 = value_str.parse()
                .map_err(|_| MunsellError::InvalidNotation {
                    notation: notation.to_string(),
                    reason: "Invalid neutral value".to_string(),
                })?;
            return Ok([f64::NAN, value, 0.0, f64::NAN]);
        }
        
        // Split by space
        let parts: Vec<&str> = notation.split_whitespace().collect();
        if parts.len() != 2 {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Expected format: 'HUE VALUE/CHROMA'".to_string(),
            });
        }
        
        // Parse hue
        let hue_part = parts[0];
        let (hue_num, family) = self.parse_hue_notation(hue_part)?;
        
        // Parse value/chroma
        let vc_parts: Vec<&str> = parts[1].split('/').collect();
        if vc_parts.len() != 2 {
            return Err(MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Expected VALUE/CHROMA format".to_string(),
            });
        }
        
        let value: f64 = vc_parts[0].parse()
            .map_err(|_| MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid value number".to_string(),
            })?;
            
        let chroma: f64 = vc_parts[1].parse()
            .map_err(|_| MunsellError::InvalidNotation {
                notation: notation.to_string(),
                reason: "Invalid chroma number".to_string(),
            })?;
        
        Ok([hue_num, value, chroma, family as f64])
    }
    
    fn parse_hue_notation(&self, hue_str: &str) -> Result<(f64, u8)> {
        // Find where the letters start
        let letter_pos = hue_str.find(|c: char| c.is_alphabetic())
            .ok_or_else(|| MunsellError::InvalidNotation {
                notation: hue_str.to_string(),
                reason: "No hue family found".to_string(),
            })?;
        
        let (num_part, family_part) = hue_str.split_at(letter_pos);
        
        // Parse hue number
        let hue_num: f64 = if num_part.is_empty() {
            5.0  // Default to 5 if no number
        } else {
            num_part.parse()
                .map_err(|_| MunsellError::InvalidNotation {
                    notation: hue_str.to_string(),
                    reason: "Invalid hue number".to_string(),
                })?
        };
        
        // Parse family
        let code = match family_part {
            "R" => 0,
            "YR" => 1,
            "Y" => 2,
            "GY" => 3,
            "G" => 4,
            "BG" => 5,
            "B" => 6,
            "PB" => 7,
            "P" => 8,
            "RP" => 9,
            _ => return Err(MunsellError::InvalidNotation {
                notation: hue_str.to_string(),
                reason: format!("Unknown hue family: {}", family_part),
            }),
        };
        
        Ok((hue_num, code))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_python_converter_basic() {
        let converter = PythonMunsellConverter::new();
        
        // Test black conversion
        println!("Testing black [0, 0, 0] (should be N 0.0)...");
        match converter.srgb_to_munsell([0, 0, 0]) {
            Ok(munsell) => {
                println!("Black: {}", munsell.notation);
                println!("  Expected: N 0.0");
            }
            Err(e) => {
                println!("Error converting black: {:?}", e);
            }
        }
        
        // Test red conversion
        println!("\nTesting red [255, 0, 0]...");
        match converter.srgb_to_munsell([255, 0, 0]) {
            Ok(munsell) => {
                println!("Red: {}", munsell.notation);
                println!("  Hue: {:?}, Value: {:.1}, Chroma: {:?}", 
                         munsell.hue, munsell.value, munsell.chroma);
            }
            Err(e) => {
                println!("Error converting red: {:?}", e);
                
                // Try to directly call the algorithm to see what spec it returns
                let rgb_linear = converter.srgb_to_linear([255, 0, 0]);
                let xyz = converter.linear_rgb_to_xyz_d65(rgb_linear);
                let xyy = converter.xyz_to_xyy(xyz);
                println!("  xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);
                
                // Call the algorithm directly with debug output
                println!("  Calling xyy_to_munsell_specification with xyY: [{:.6}, {:.6}, {:.6}]", 
                         xyy[0], xyy[1], xyy[2]);
                
                // First check what value we get
                let value = munsell_value_astmd1535(xyy[2] * 100.0);
                println!("  Munsell value from Y={:.6}: {:.6}", xyy[2], value);
                
                match xyy_to_munsell_specification(xyy) {
                    Ok(spec) => {
                        println!("  Raw spec from algorithm: hue={:.2}, value={:.2}, chroma={:.2}, code={}", 
                                 spec[0], spec[1], spec[2], spec[3] as u8);
                        
                        // Test if we can convert it back to xyY
                        println!("  Testing round-trip conversion...");
                        match munsell_specification_to_xyy(&spec) {
                            Ok(xyy_back) => {
                                println!("  Round-trip xyY: [{:.6}, {:.6}, {:.6}]", 
                                         xyy_back[0], xyy_back[1], xyy_back[2]);
                            }
                            Err(e) => {
                                println!("  Round-trip failed: {:?}", e);
                            }
                        }
                    }
                    Err(e) => {
                        println!("  Algorithm error: {:?}", e);
                    }
                }
            }
        }
        
        // First test some basic conversions
        println!("\nTesting basic conversions...");
        
        // Test grey conversion
        println!("Testing grey specification [NaN, 5.0, NaN, NaN]...");
        match munsell_specification_to_xyy(&[f64::NAN, 5.0, f64::NAN, f64::NAN]) {
            Ok(xyy) => {
                println!("  Grey at value 5.0 -> xyY: [{:.6}, {:.6}, {:.6}]", 
                         xyy[0], xyy[1], xyy[2]);
            }
            Err(e) => {
                println!("  Error: {:?}", e);
            }
        }
        
        // Test with a reference color from the dataset
        println!("\nTesting with reference color [0, 68, 119] (should be 2.9PB 2.8/7.0)...");
        match converter.srgb_to_munsell([0, 68, 119]) {
            Ok(munsell) => {
                println!("Result: {}", munsell.notation);
                println!("  Hue: {:?}, Value: {:.1}, Chroma: {:?}", 
                         munsell.hue, munsell.value, munsell.chroma);
                println!("  Expected: 2.9PB 2.8/7.0");
            }
            Err(e) => {
                println!("Error: {:?}", e);
                
                // Test the algorithm directly
                let rgb_linear = converter.srgb_to_linear([0, 68, 119]);
                let xyz = converter.linear_rgb_to_xyz_d65(rgb_linear);
                let xyy = converter.xyz_to_xyy(xyz);
                println!("  xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);
            }
        }
        
        // Test round trip with exact reference value
        println!("\nTesting round trip with 2.9PB 2.8/7.0...");
        match converter.munsell_to_srgb("2.9PB 2.8/7.0") {
            Ok(rgb) => {
                println!("2.9PB 2.8/7.0 -> RGB: [{}, {}, {}]", rgb.r, rgb.g, rgb.b);
                println!("  Expected: [0, 68, 119]");
            }
            Err(e) => {
                println!("Error: {:?}", e);
            }
        }
        
        // Test round trip with standard value
        println!("\nTesting round trip with 5R 5/10...");
        match converter.munsell_to_srgb("5R 5/10") {
            Ok(rgb) => {
                println!("5R 5/10 -> RGB: [{}, {}, {}]", rgb.r, rgb.g, rgb.b);
            }
            Err(e) => {
                println!("Error: {:?}", e);
            }
        }
    }
}