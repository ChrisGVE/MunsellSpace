#!/usr/bin/env rust
//! Illuminant Precision Testing Tool
//!
//! This tool creates an experimental version of the MunsellConverter that can use
//! different illuminants to test if changing the illuminant affects the precision
//! errors causing ISCC-NBS classification mismatches.

use std::collections::HashMap;

// Import illuminant types
use crate::illuminants::{Illuminant, ChromaticAdaptation, ChromaticAdaptationMethod};
use crate::converter::MunsellConverter;
use crate::types::MunsellColor;
use crate::error::Result;

/// Experimental illuminant-configurable converter for precision testing
pub struct IlluminantTestConverter {
    base_converter: MunsellConverter,
    test_illuminant: Illuminant,
    adaptation_method: ChromaticAdaptationMethod,
}

impl IlluminantTestConverter {
    /// Create a new test converter with specified illuminant
    pub fn new_with_illuminant(illuminant: Illuminant) -> Result<Self> {
        let base_converter = MunsellConverter::new()?;
        
        Ok(Self {
            base_converter,
            test_illuminant: illuminant,
            adaptation_method: ChromaticAdaptationMethod::Bradford,
        })
    }
    
    /// Convert sRGB to Munsell using the specified illuminant
    pub fn srgb_to_munsell_with_illuminant(&self, rgb: [u8; 3]) -> Result<MunsellColor> {
        // Handle pure black as special case
        if rgb[0] == 0 && rgb[1] == 0 && rgb[2] == 0 {
            return Ok(MunsellColor::new_neutral(0.0));
        }
        
        // Step 1: Convert u8 RGB to normalized f64 sRGB
        let srgb_norm = [
            rgb[0] as f64 / 255.0,
            rgb[1] as f64 / 255.0,
            rgb[2] as f64 / 255.0,
        ];

        // Step 2: Apply gamma correction (sRGB → linear RGB)
        let linear_rgb = self.srgb_to_linear_rgb(srgb_norm);

        // Step 3: Convert linear RGB → XYZ (D65 illuminant - sRGB standard)
        let xyz_d65 = self.linear_rgb_to_xyz_d65(linear_rgb);

        // Step 4: Apply chromatic adaptation to target illuminant if different from D65
        let xyz_adapted = if self.test_illuminant != Illuminant::D65 {
            ChromaticAdaptation::adapt(
                xyz_d65,
                Illuminant::D65,
                self.test_illuminant,
                self.adaptation_method,
            )?
        } else {
            xyz_d65
        };

        // Step 5: Convert XYZ → xyY
        let xyy = self.xyz_to_xyy(xyz_adapted);

        // Step 6: Convert xyY → Munsell using the white point of target illuminant
        self.xyy_to_munsell_with_white_point(xyy)
    }
    
    /// Apply sRGB gamma correction to convert to linear RGB.
    fn srgb_to_linear_rgb(&self, srgb: [f64; 3]) -> [f64; 3] {
        let mut linear = [0.0; 3];
        for i in 0..3 {
            linear[i] = if srgb[i] <= 0.04045 {
                srgb[i] / 12.92
            } else {
                ((srgb[i] + 0.055) / 1.055).powf(2.4)
            };
        }
        linear
    }

    /// Convert linear RGB to XYZ using sRGB D65 transformation matrix.
    fn linear_rgb_to_xyz_d65(&self, linear_rgb: [f64; 3]) -> [f64; 3] {
        // sRGB to XYZ D65 transformation matrix (ITU-R BT.709)
        let matrix = [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ];

        let mut xyz = [0.0; 3];
        for i in 0..3 {
            xyz[i] = matrix[i][0] * linear_rgb[0] +
                     matrix[i][1] * linear_rgb[1] +
                     matrix[i][2] * linear_rgb[2];
        }
        xyz
    }
    
    /// Convert XYZ to xyY color space.
    fn xyz_to_xyy(&self, xyz: [f64; 3]) -> [f64; 3] {
        let sum = xyz[0] + xyz[1] + xyz[2];
        if sum == 0.0 {
            // Handle black (0,0,0) case
            [0.0, 0.0, 0.0]
        } else {
            [xyz[0] / sum, xyz[1] / sum, xyz[1]]
        }
    }
    
    /// Convert xyY to Munsell using specified illuminant's white point
    fn xyy_to_munsell_with_white_point(&self, xyy: [f64; 3]) -> Result<MunsellColor> {
        let [x, y, big_y] = xyy;

        // Get white point coordinates for the test illuminant
        let (white_x, white_y) = self.test_illuminant.chromaticity();

        // Handle achromatic colors (near the white point of target illuminant)
        if self.is_achromatic_for_illuminant(x, y, white_x, white_y) {
            let value = self.xyz_y_to_munsell_value(big_y);
            return Ok(MunsellColor::new_neutral((value * 10.0).round() / 10.0));
        }

        // Calculate hue angle relative to target illuminant's white point
        let hue_angle = (y - white_y).atan2(x - white_x);
        let hue_degrees = hue_angle.to_degrees();
        
        // Convert to Munsell hue notation
        let munsell_hue = self.degrees_to_munsell_hue(hue_degrees);
        
        // Calculate Munsell value from Y component
        let value = self.xyz_y_to_munsell_value(big_y);
        let rounded_value = (value * 10.0).round() / 10.0;
        
        // Calculate Munsell chroma from chromaticity distance relative to target white point
        let chroma = self.calculate_munsell_chroma_for_illuminant(x, y, big_y, white_x, white_y);
        let rounded_chroma = (chroma * 10.0).round() / 10.0;

        Ok(MunsellColor::new_chromatic(munsell_hue, rounded_value, rounded_chroma))
    }
    
    /// Check if a color is achromatic relative to specified illuminant's white point
    fn is_achromatic_for_illuminant(&self, x: f64, y: f64, white_x: f64, white_y: f64) -> bool {
        // Calculate chromaticity distance from illuminant's white point
        let distance = ((x - white_x).powi(2) + (y - white_y).powi(2)).sqrt();
        
        // Use the same threshold as the original implementation
        let threshold = 0.001;
        
        distance < threshold
    }
    
    /// Convert XYZ Y component to Munsell Value using ASTM D1535 method.
    fn xyz_y_to_munsell_value(&self, y: f64) -> f64 {
        // This is illuminant-independent - use the same method as the base converter
        // Convert Y from 0-1 range to 0-100 range for ASTM D1535
        let y_percent = y * 100.0;
        self.munsell_value_astm_d1535(y_percent)
    }
    
    /// Implement ASTM D1535 Munsell value calculation method.
    fn munsell_value_astm_d1535(&self, y: f64) -> f64 {
        if y <= 0.0 {
            return 0.0;
        }
        if y >= 100.0 {
            return 10.0;
        }
        
        // ASTM D1535 lookup table - same as base converter
        let astm_table = [
            (0.0, 0.0),
            (1.0, 0.863),
            (2.0, 1.386),
            (3.0, 1.796),
            (4.0, 2.157),
            (5.0, 2.645),
            (6.0, 2.976),
            (7.0, 3.282),
            (8.0, 3.568),
            (9.0, 3.837),
            (10.0, 3.721),
            (15.0, 4.502),
            (20.0, 5.082),
            (25.0, 5.551),
            (30.0, 6.061),
            (35.0, 6.515),
            (40.0, 6.927),
            (45.0, 7.305),
            (50.0, 7.538),
            (55.0, 7.912),
            (60.0, 8.264),
            (65.0, 8.597),
            (70.0, 8.671),
            (75.0, 9.021),
            (80.0, 9.357),
            (85.0, 9.679),
            (90.0, 9.596),
            (95.0, 9.886),
            (100.0, 10.000),
        ];
        
        // Linear interpolation within the lookup table
        for i in 0..astm_table.len() - 1 {
            let (y1, v1) = astm_table[i];
            let (y2, v2) = astm_table[i + 1];
            
            if y >= y1 && y <= y2 {
                if y2 == y1 {
                    return v1;
                }
                
                // Linear interpolation
                let ratio = (y - y1) / (y2 - y1);
                let interpolated = v1 + ratio * (v2 - v1);
                return interpolated.max(0.0).min(10.0);
            }
        }
        
        // Extrapolation for values outside the table
        if y < 1.0 {
            return (y * 1.211).max(0.0);
        } else {
            return 10.0;
        }
    }

    /// Convert hue angle in degrees to Munsell hue notation.
    fn degrees_to_munsell_hue(&self, degrees: f64) -> String {
        // Normalize angle to 0-360 range
        let normalized = ((degrees % 360.0) + 360.0) % 360.0;
        
        // Standard Munsell hue families with proper 36-degree intervals
        let hue_families = [
            (0.0, "R"), (36.0, "YR"), (72.0, "Y"), (108.0, "GY"), (144.0, "G"),
            (180.0, "BG"), (216.0, "B"), (252.0, "PB"), (288.0, "P"), (324.0, "RP")
        ];
        
        // Find the appropriate hue family
        for i in 0..hue_families.len() {
            let (start_angle, family) = hue_families[i];
            let next_angle = if i == hue_families.len() - 1 { 360.0 } else { hue_families[i + 1].0 };
            
            if normalized >= start_angle && normalized < next_angle {
                // Calculate hue step within the family (1-10)
                let degrees_within_family = normalized - start_angle;
                let hue_step = (degrees_within_family / 3.6) + 1.0;
                
                // Use floor instead of round for Munsell hue calculation
                let floored_hue = (hue_step * 10.0).floor() / 10.0;
                let clamped_hue = floored_hue.max(1.0).min(10.0);
                
                // Format with decimal precision if needed
                if (clamped_hue.fract()).abs() < 0.05 {
                    return format!("{:.0}{}", clamped_hue.round(), family);
                } else {
                    return format!("{:.1}{}", clamped_hue, family);
                }
            }
        }
        
        // Fallback
        "5R".to_string()
    }

    /// Calculate Munsell chroma from chromaticity coordinates relative to illuminant white point
    fn calculate_munsell_chroma_for_illuminant(&self, x: f64, y: f64, big_y: f64, white_x: f64, white_y: f64) -> f64 {
        let chromaticity_distance = ((x - white_x).powi(2) + (y - white_y).powi(2)).sqrt();
        
        // Luminance factor
        let luminance_factor = if big_y > 0.0 {
            let y_percent = big_y * 100.0;
            y_percent.powf(1.0/3.0) / 4.64
        } else {
            0.02
        };
        
        // Base chroma scaling
        let base_chroma_scaling = 85.0;
        
        // Distance-based scaling
        let distance_factor = if chromaticity_distance > 0.05 {
            1.2
        } else if chromaticity_distance < 0.01 {
            0.5
        } else {
            1.0
        };
        
        let chroma = chromaticity_distance * base_chroma_scaling * luminance_factor * distance_factor;
        
        // Clamp to realistic Munsell chroma range
        chroma.max(0.0).min(25.0)
    }
}

/// Test precision differences using different illuminants
pub fn test_illuminant_precision_effects() -> Result<()> {
    println!("Testing illuminant effects on Munsell conversion precision...\n");
    
    // Test colors that have known precision issues from the classification report
    let test_colors = [
        ([0xEF, 0xDD, 0xE5], "pinkish white", "Expected 1.5 chroma, getting 1.6"),
        ([0xC7, 0xB6, 0xBD], "pinkish gray", "Expected 1.5 chroma, getting 1.6"), 
        ([0x5C, 0x06, 0x25], "very deep red", "Expected R family, getting RP family"),
        ([0x48, 0x11, 0x27], "very dark red", "Expected R family, getting RP family"),
        ([0x88, 0x66, 0x48], "moderate yellowish brown", "Boundary classification issue"),
    ];
    
    // Test different illuminants
    let illuminants_to_test = [
        (Illuminant::D65, "D65 (Current default)"),
        (Illuminant::C, "Illuminant C (Classic)"),
        (Illuminant::D50, "D50 (Graphic arts)"),
        (Illuminant::D55, "D55 (Photography)"),
        (Illuminant::A, "Illuminant A (Incandescent)"),
        (Illuminant::E, "Equal Energy"),
    ];
    
    let mut results: HashMap<String, Vec<String>> = HashMap::new();
    
    // Test each illuminant
    for (illuminant, illuminant_name) in illuminants_to_test.iter() {
        println!("=== Testing {} ===", illuminant_name);
        
        let test_converter = IlluminantTestConverter::new_with_illuminant(*illuminant)?;
        let mut illuminant_results = Vec::new();
        
        for (rgb, expected_name, issue_description) in test_colors.iter() {
            match test_converter.srgb_to_munsell_with_illuminant(*rgb) {
                Ok(munsell) => {
                    let result = format!(
                        "RGB{:?} -> {} | {} | {}",
                        rgb, munsell.notation, expected_name, issue_description
                    );
                    println!("  {}", result);
                    illuminant_results.push(result);
                }
                Err(e) => {
                    let error_result = format!(
                        "RGB{:?} -> ERROR: {} | {} | {}",
                        rgb, e, expected_name, issue_description
                    );
                    println!("  {}", error_result);
                    illuminant_results.push(error_result);
                }
            }
        }
        
        results.insert(illuminant_name.to_string(), illuminant_results);
        println!();
    }
    
    // Analyze differences
    println!("=== ANALYSIS: Illuminant Impact on Precision ===\n");
    
    // Compare results across illuminants for each test color
    for (i, (rgb, expected_name, _issue)) in test_colors.iter().enumerate() {
        println!("Color #{} - RGB{:?} (expected: {}):", i + 1, rgb, expected_name);
        
        let mut conversions = Vec::new();
        for (illuminant, illuminant_name) in illuminants_to_test.iter() {
            if let Some(results_for_illuminant) = results.get(*illuminant_name) {
                if let Some(result) = results_for_illuminant.get(i) {
                    // Extract the Munsell notation from the result
                    if let Some(arrow_pos) = result.find(" -> ") {
                        if let Some(pipe_pos) = result[arrow_pos..].find(" | ") {
                            let munsell_notation = &result[arrow_pos + 4..arrow_pos + pipe_pos];
                            conversions.push((illuminant_name, munsell_notation));
                        }
                    }
                }
            }
        }
        
        // Check if there are any differences
        let first_result = conversions.get(0).map(|(_, notation)| *notation);
        let mut all_same = true;
        for (_, notation) in &conversions {
            if Some(*notation) != first_result {
                all_same = false;
                break;
            }
        }
        
        if all_same {
            println!("  ✓ All illuminants produce SAME result: {}", first_result.unwrap_or("ERROR"));
        } else {
            println!("  ⚠ DIFFERENT results across illuminants:");
            for (illuminant_name, notation) in &conversions {
                println!("    {} -> {}", illuminant_name, notation);
            }
        }
        println!();
    }
    
    // Conclusion
    println!("=== CONCLUSION ===");
    
    // Count how many colors showed differences
    let mut colors_with_differences = 0;
    for (i, _) in test_colors.iter().enumerate() {
        let mut conversions = Vec::new();
        for (_, illuminant_name) in illuminants_to_test.iter() {
            if let Some(results_for_illuminant) = results.get(*illuminant_name) {
                if let Some(result) = results_for_illuminant.get(i) {
                    if let Some(arrow_pos) = result.find(" -> ") {
                        if let Some(pipe_pos) = result[arrow_pos..].find(" | ") {
                            let munsell_notation = &result[arrow_pos + 4..arrow_pos + pipe_pos];
                            conversions.push(munsell_notation);
                        }
                    }
                }
            }
        }
        
        // Check if all conversions are the same
        if !conversions.is_empty() {
            let first = conversions[0];
            if conversions.iter().any(|&notation| notation != first) {
                colors_with_differences += 1;
            }
        }
    }
    
    if colors_with_differences == 0 {
        println!("Result: Changing illuminants has NO EFFECT on precision errors.");
        println!("The precision issues are likely due to other factors in the conversion pipeline.");
        println!("Recommended: Focus on mathematical algorithms rather than illuminant selection.");
    } else {
        println!("Result: {} out of {} test colors show DIFFERENT results with different illuminants.", 
                 colors_with_differences, test_colors.len());
        println!("This suggests illuminant choice may affect precision for some colors.");
        println!("Recommended: Further analysis to determine optimal illuminant for ISCC-NBS classification.");
    }
    
    Ok(())
}

fn main() -> Result<()> {
    match test_illuminant_precision_effects() {
        Ok(()) => {
            println!("\nIlluminant precision testing completed successfully.");
            std::process::exit(0);
        }
        Err(e) => {
            eprintln!("Error during illuminant testing: {}", e);
            std::process::exit(1);
        }
    }
}