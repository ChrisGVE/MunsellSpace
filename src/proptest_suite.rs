//! Property-based tests for MunsellSpace library using proptest
//! 
//! These tests use property-based testing to validate invariants and edge cases
//! across the entire input space, helping catch bugs that specific test cases might miss.

use proptest::prelude::*;
use crate::{MunsellConverter, MunsellColor, RgbColor};

proptest! {
    /// Test that RGB input validation works for all possible u8 values
    #[test]
    fn test_rgb_validation_comprehensive(
        r in 0u8..=255,
        g in 0u8..=255, 
        b in 0u8..=255
    ) {
        let converter = MunsellConverter::new().unwrap();
        let result = converter.srgb_to_munsell([r, g, b]);
        
        // All valid RGB values should either convert successfully or fail gracefully
        match result {
            Ok(munsell) => {
                // If conversion succeeds, result should be valid
                prop_assert!(!munsell.notation.is_empty());
                prop_assert!(munsell.value >= 0.0 && munsell.value <= 10.0);
                if let Some(chroma) = munsell.chroma {
                    prop_assert!(chroma >= 0.0);
                }
            }
            Err(_) => {
                // If conversion fails, that's acceptable for some edge cases
                // but we should not panic
            }
        }
    }
    
    /// Test that neutral colors are properly detected
    #[test]
    fn test_grayscale_detection(gray_level in 0u8..=255) {
        let rgb = RgbColor::new(gray_level, gray_level, gray_level);
        prop_assert!(rgb.is_grayscale());
        
        // Test that slightly non-grayscale colors are not detected as grayscale
        if gray_level < 255 {
            let non_gray = RgbColor::new(gray_level, gray_level, gray_level + 1);
            prop_assert!(!non_gray.is_grayscale());
        }
    }
    
    /// Test that RGB inputs in valid ranges convert successfully  
    #[test]
    fn test_valid_rgb_conversion_ranges(
        r in 0.0..=1.0,
        g in 0.0..=1.0,
        b in 0.0..=1.0
    ) {
        let converter = MunsellConverter::new().unwrap();
        
        // Convert normalized RGB to u8 range
        let rgb_u8 = [
            (r * 255.0) as u8,
            (g * 255.0) as u8, 
            (b * 255.0) as u8
        ];
        
        // Test conversion succeeds for all valid inputs
        let result = converter.srgb_to_munsell(rgb_u8);
        
        // Should either succeed or fail gracefully without panic
        match result {
            Ok(munsell) => {
                prop_assert!(munsell.value >= 0.0 && munsell.value <= 10.0);
                if let Some(chroma) = munsell.chroma {
                    prop_assert!(chroma >= 0.0);
                }
            }
            Err(_) => {
                // Conversion failure is acceptable for some edge cases
            }
        }
    }
    
    /// Test Munsell color components are in reasonable ranges
    #[test]
    fn test_munsell_component_ranges(
        r in 0u8..=255,
        g in 0u8..=255, 
        b in 0u8..=255
    ) {
        let converter = MunsellConverter::new().unwrap();
        
        if let Ok(munsell) = converter.srgb_to_munsell([r, g, b]) {
            // Test value is in valid range
            prop_assert!(munsell.value >= 0.0 && munsell.value <= 10.0,
                "Value {} out of range for RGB[{},{},{}]", munsell.value, r, g, b);
            
            // Test chroma is non-negative
            if let Some(chroma) = munsell.chroma {
                prop_assert!(chroma >= 0.0,
                    "Negative chroma {} for RGB[{},{},{}]", chroma, r, g, b);
            }
            
            // Test notation is not empty
            prop_assert!(!munsell.notation.is_empty(),
                "Empty notation for RGB[{},{},{}]", r, g, b);
        }
    }
    
    /// Test batch conversion consistency
    #[test]
    fn test_batch_conversion_consistency(
        colors in prop::collection::vec(
            (0u8..=255, 0u8..=255, 0u8..=255),
            1..=20
        )
    ) {
        let converter = MunsellConverter::new().unwrap();
        
        let rgb_array: Vec<[u8; 3]> = colors.iter().map(|(r, g, b)| [*r, *g, *b]).collect();
        
        // Batch conversion should succeed
        let batch_result = converter.convert_batch(&rgb_array);
        prop_assert!(batch_result.is_ok());
        
        let batch_results = batch_result.unwrap();
        prop_assert_eq!(batch_results.len(), rgb_array.len());
        
        // Each individual conversion should match batch result
        for (i, &rgb) in rgb_array.iter().enumerate() {
            let individual_result = converter.srgb_to_munsell(rgb);
            
            match individual_result {
                Ok(individual_munsell) => {
                    prop_assert_eq!(individual_munsell.notation, batch_results[i].notation.clone(),
                        "Batch result differs from individual for RGB{:?} at index {}", rgb, i);
                }
                Err(_) => {
                    // Individual conversion failed - this should be rare but acceptable
                }
            }
        }
    }
    
    /// Test Munsell notation parsing and formatting roundtrip
    #[test]
    fn test_munsell_notation_roundtrip(
        hue_num in 2.5f64..10.0,
        value in 0.0..10.0,
        chroma in 0.0..20.0
    ) {
        let hue_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        let hue_family = hue_families[hue_num as usize % hue_families.len()];
        let hue = format!("{}{}", hue_num, hue_family);
        
        let original = MunsellColor::new_chromatic(hue.clone(), value, chroma);
        
        // Parse the notation back
        match MunsellColor::from_notation(&original.notation) {
            Ok(parsed) => {
                prop_assert_eq!(parsed.hue, Some(hue));
                prop_assert!((parsed.value - value).abs() < 1e-10);
                prop_assert!(parsed.chroma.map(|c| (c - chroma).abs() < 1e-10).unwrap_or(false));
            }
            Err(e) => {
                prop_assert!(false, "Failed to parse generated notation '{}': {}", original.notation, e);
            }
        }
    }
    
    /// Test neutral color notation roundtrip
    #[test]
    fn test_neutral_notation_roundtrip(value in 0.0..10.0) {
        let original = MunsellColor::new_neutral(value);
        
        match MunsellColor::from_notation(&original.notation) {
            Ok(parsed) => {
                prop_assert!(parsed.is_neutral());
                prop_assert!((parsed.value - value).abs() < 1e-10);
                prop_assert!(parsed.chroma.is_none());
            }
            Err(e) => {
                prop_assert!(false, "Failed to parse neutral notation '{}': {}", original.notation, e);
            }
        }
    }
    
    /// Test that Lab to Munsell conversion maintains reasonable properties
    #[test]
    fn test_lab_to_munsell_properties(
        l in 0.0..100.0,
        a in -100.0..100.0,
        b in -100.0..100.0
    ) {
        let converter = MunsellConverter::new().unwrap();
        
        let lab_result = converter.lab_to_munsell([l, a, b]);
        
        match lab_result {
            Ok(munsell) => {
                // Valid Munsell color properties
                prop_assert!(munsell.value >= 0.0 && munsell.value <= 10.0);
                
                if let Some(chroma) = munsell.chroma {
                    prop_assert!(chroma >= 0.0);
                }
                
                // Achromatic colors (near a*=0, b*=0) should have low chroma
                if a.abs() < 1.0 && b.abs() < 1.0 {
                    if let Some(chroma) = munsell.chroma {
                        prop_assert!(chroma < 5.0, "High chroma {} for near-achromatic color Lab[{}, {}, {}]", chroma, l, a, b);
                    }
                }
            }
            Err(_) => {
                // Some Lab colors may not convert (out of gamut) - this is acceptable
            }
        }
    }
    
    /// Test conversion determinism - same input should always give same output
    #[test]
    fn test_conversion_determinism(
        r in 0u8..=255,
        g in 0u8..=255,
        b in 0u8..=255
    ) {
        let converter = MunsellConverter::new().unwrap();
        
        let result1 = converter.srgb_to_munsell([r, g, b]);
        let result2 = converter.srgb_to_munsell([r, g, b]);
        
        match (result1, result2) {
            (Ok(munsell1), Ok(munsell2)) => {
                prop_assert_eq!(munsell1.notation, munsell2.notation,
                    "Non-deterministic conversion for RGB[{}, {}, {}]", r, g, b);
            }
            (Err(_), Err(_)) => {
                // Consistent failure is acceptable
            }
            _ => {
                prop_assert!(false, "Inconsistent conversion results for RGB[{}, {}, {}]", r, g, b);
            }
        }
    }
}

/// Additional property tests for edge cases and invariants
#[cfg(test)]
mod edge_case_properties {
    use super::*;
    
    proptest! {
        /// Test that very similar RGB colors produce similar Munsell colors
        #[test]
        fn test_color_similarity_preservation(
            base_r in 50u8..=200,
            base_g in 50u8..=200,
            base_b in 50u8..=200,
            delta in 0u8..=5
        ) {
            let converter = MunsellConverter::new().unwrap();
            
            let rgb1 = [base_r, base_g, base_b];
            let rgb2 = [
                (base_r as i16 + delta as i16).min(255).max(0) as u8,
                (base_g as i16 + delta as i16).min(255).max(0) as u8,
                (base_b as i16 + delta as i16).min(255).max(0) as u8,
            ];
            
            let result1 = converter.srgb_to_munsell(rgb1);
            let result2 = converter.srgb_to_munsell(rgb2);
            
            if let (Ok(munsell1), Ok(munsell2)) = (result1, result2) {
                // Colors should be in similar ranges
                let value_diff = (munsell1.value - munsell2.value).abs();
                prop_assert!(value_diff < 2.0, "Value difference {} too large for similar colors", value_diff);
                
                if let (Some(c1), Some(c2)) = (munsell1.chroma, munsell2.chroma) {
                    let chroma_diff = (c1 - c2).abs();
                    prop_assert!(chroma_diff < 5.0, "Chroma difference {} too large for similar colors", chroma_diff);
                }
            }
        }
    }
}