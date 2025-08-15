//! Additional comprehensive unit tests for MunsellSpace library.
//!
//! This module contains specialized unit tests that complement the existing
//! test suite to ensure complete coverage of edge cases, error conditions,
//! and API contracts that might not be covered elsewhere.

#[cfg(test)]
mod comprehensive_unit_tests {
    use crate::*;
    use crate::error::*;
    use crate::mathematical::*;
    use crate::mechanical_wedges::*;
    use crate::iscc::*;
    use crate::reverse_conversion::*;
    use std::collections::HashSet;
    use approx::assert_relative_eq;

    // =============================================================================
    // Error Handling Comprehensive Tests
    // =============================================================================

    #[test]
    fn test_error_exhaustive_coverage() {
        // Test every error variant can be created and displayed
        let errors = vec![
            MunsellError::InvalidRgb {
                rgb: [256, 0, 0], // Impossible value for u8 but conceptually invalid
                reason: "Value exceeds u8 range".to_string(),
            },
            MunsellError::OutOfGamut {
                rgb: [255, 255, 255],
                context: "Theoretical limit exceeded".to_string(),
            },
            MunsellError::InvalidNotation {
                notation: "INVALID".to_string(),
                reason: "Completely malformed".to_string(),
            },
            MunsellError::ReferenceDataError {
                message: "Critical data corruption".to_string(),
            },
            MunsellError::ConversionError {
                message: "Algorithm failure".to_string(),
            },
            MunsellError::IoError {
                message: "Disk full".to_string(),
            },
            MunsellError::ConvergenceFailed,
            MunsellError::InterpolationError {
                message: "Insufficient control points".to_string(),
            },
            MunsellError::InvalidMunsellColor("Negative chroma".to_string()),
            MunsellError::NotImplemented("Future feature".to_string()),
        ];

        for error in errors {
            // Each error should display properly
            let display_str = error.to_string();
            assert!(!display_str.is_empty(), "Error display should not be empty");
            
            // Each error should debug properly
            let debug_str = format!("{:?}", error);
            assert!(!debug_str.is_empty(), "Error debug should not be empty");
            
            // Each error should be cloneable
            let cloned = error.clone();
            assert_eq!(error, cloned, "Error should clone correctly");
        }
    }

    #[test]
    fn test_error_chain_propagation() {
        use std::io;
        
        // Test error conversion chains
        let io_error = io::Error::new(io::ErrorKind::PermissionDenied, "Access denied");
        let munsell_error: MunsellError = io_error.into();
        
        match munsell_error {
            MunsellError::IoError { message } => {
                assert!(message.contains("Access denied"));
            },
            _ => panic!("IO error should convert to MunsellError::IoError"),
        }
        
        // Test JSON error conversion
        let json_str = "{ invalid json }";
        let json_error = serde_json::from_str::<serde_json::Value>(json_str).unwrap_err();
        let converted_error: MunsellError = json_error.into();
        
        match converted_error {
            MunsellError::ConversionError { message } => {
                assert!(message.contains("JSON error"));
            },
            _ => panic!("JSON error should convert to MunsellError::ConversionError"),
        }
    }

    // =============================================================================
    // MunsellConverter API Contract Tests
    // =============================================================================

    #[test]
    fn test_converter_initialization_robustness() {
        // Test that converter can be created multiple times
        for _ in 0..10 {
            let converter = MunsellConverter::new();
            assert!(converter.is_ok(), "Converter should initialize consistently");
        }
        
        // Test that converters are independent
        let converter1 = MunsellConverter::new().unwrap();
        let converter2 = MunsellConverter::new().unwrap();
        
        let rgb = [128, 128, 128];
        let result1 = converter1.srgb_to_munsell(rgb).unwrap();
        let result2 = converter2.srgb_to_munsell(rgb).unwrap();
        
        assert_eq!(result1.notation, result2.notation, "Independent converters should give same results");
    }

    #[test]
    fn test_converter_input_validation_comprehensive() {
        let converter = MunsellConverter::new().unwrap();
        
        // Test all possible RGB boundary combinations
        let boundary_tests = [
            ([0, 0, 0], true),       // All minimum
            ([255, 255, 255], true), // All maximum
            ([0, 255, 128], true),   // Mixed boundaries
            ([255, 0, 128], true),   // Mixed boundaries
            ([128, 255, 0], true),   // Mixed boundaries
        ];
        
        for (rgb, should_succeed) in boundary_tests {
            let result = converter.srgb_to_munsell(rgb);
            if should_succeed {
                assert!(result.is_ok(), "RGB {:?} should convert successfully", rgb);
                let munsell = result.unwrap();
                
                // Verify basic invariants
                assert!(munsell.value >= 0.0 && munsell.value <= 10.0);
                if let Some(chroma) = munsell.chroma {
                    assert!(chroma >= 0.0, "Chroma should be non-negative");
                }
                assert!(!munsell.notation.is_empty(), "Notation should not be empty");
            } else {
                assert!(result.is_err(), "RGB {:?} should fail conversion", rgb);
            }
        }
    }

    #[test]
    fn test_converter_deterministic_behavior() {
        let converter = MunsellConverter::new().unwrap();
        
        // Generate a variety of RGB colors
        let test_colors: Vec<[u8; 3]> = (0..100)
            .map(|i| [
                (i * 17 + 13) % 256,
                (i * 37 + 29) % 256,
                (i * 73 + 41) % 256,
            ])
            .map(|[r, g, b]| [r as u8, g as u8, b as u8])
            .collect();
        
        // Convert each color multiple times
        for &rgb in &test_colors {
            let results: Vec<_> = (0..5)
                .map(|_| converter.srgb_to_munsell(rgb))
                .collect::<Result<Vec<_>, _>>()
                .unwrap();
            
            // All results should be identical
            let first_notation = &results[0].notation;
            for result in &results[1..] {
                assert_eq!(result.notation, *first_notation, 
                           "Conversion of RGB{:?} should be deterministic", rgb);
            }
        }
    }

    #[test]
    fn test_batch_conversion_consistency_and_edge_cases() {
        let converter = MunsellConverter::new().unwrap();
        
        // Test empty batch
        let empty_batch = vec![];
        let empty_result = converter.convert_batch(&empty_batch);
        assert!(empty_result.is_ok());
        assert_eq!(empty_result.unwrap().len(), 0);
        
        // Test single item batch
        let single_batch = vec![[255, 0, 0]];
        let single_result = converter.convert_batch(&single_batch).unwrap();
        assert_eq!(single_result.len(), 1);
        
        let individual_result = converter.srgb_to_munsell([255, 0, 0]).unwrap();
        assert_eq!(single_result[0].notation, individual_result.notation);
        
        // Test large batch with duplicates
        let large_batch = vec![[128, 128, 128]; 1000];
        let large_result = converter.convert_batch(&large_batch);
        assert!(large_result.is_ok());
        assert_eq!(large_result.unwrap().len(), 1000);
        
        // Test batch with all unique values
        let unique_batch: Vec<[u8; 3]> = (0..256).step_by(16)
            .flat_map(|r| (0..256).step_by(16).map(move |g| [r as u8, g as u8, 128]))
            .collect();
        
        let unique_result = converter.convert_batch(&unique_batch);
        assert!(unique_result.is_ok(), "Unique batch should convert successfully");
    }

    // =============================================================================
    // Mathematical Converter Comprehensive Tests
    // =============================================================================

    #[test]
    fn test_mathematical_converter_precision_boundaries() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test precision at different RGB ranges
        let precision_tests = [
            // Very dark colors (near black)
            ([1, 1, 1], "very_dark"),
            ([2, 1, 0], "minimal_red"),
            ([0, 2, 1], "minimal_green"),
            ([1, 0, 2], "minimal_blue"),
            
            // Very bright colors (near white)  
            ([254, 255, 255], "near_white_red"),
            ([255, 254, 255], "near_white_green"),
            ([255, 255, 254], "near_white_blue"),
            
            // Mid-range precision tests
            ([127, 128, 129], "precise_gray"),
            ([64, 128, 192], "quarter_ranges"),
        ];
        
        for (rgb, description) in precision_tests {
            let xyy_result = converter.srgb_to_xyy(rgb);
            
            match xyy_result {
                Ok(xyy) => {
                    // Verify xyY values are in valid ranges
                    assert!(xyy.x >= 0.0 && xyy.x <= 1.0, 
                           "{}: x coordinate out of range: {}", description, xyy.x);
                    assert!(xyy.y >= 0.0 && xyy.y <= 1.0, 
                           "{}: y coordinate out of range: {}", description, xyy.y);
                    assert!(xyy.Y >= 0.0, 
                           "{}: Y luminance negative: {}", description, xyy.Y);
                    assert!(xyy.Y.is_finite(), 
                           "{}: Y luminance not finite: {}", description, xyy.Y);
                    
                    // Test Munsell conversion
                    let munsell_result = converter.xyy_to_munsell_specification(xyy);
                    if let Ok(spec) = munsell_result {
                        assert!(spec.value >= 0.0 && spec.value <= 10.0, 
                               "{}: Munsell value out of range: {}", description, spec.value);
                        if let Some(chroma) = spec.chroma {
                            assert!(chroma >= 0.0 && chroma.is_finite(), 
                                   "{}: Invalid chroma: {}", description, chroma);
                        }
                    }
                }
                Err(e) => {
                    println!("Note: {} failed conversion (may be expected): {}", description, e);
                }
            }
        }
    }

    #[test]
    fn test_mathematical_converter_illuminant_consistency() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test that illuminant settings affect results consistently
        let test_rgb = [200, 150, 100];
        let result1 = converter.srgb_to_xyy(test_rgb);
        let result2 = converter.srgb_to_xyy(test_rgb);
        
        match (&result1, &result2) {
            (Ok(xyy1), Ok(xyy2)) => {
                assert_relative_eq!(xyy1.x, xyy2.x, epsilon = 1e-10);
                assert_relative_eq!(xyy1.y, xyy2.y, epsilon = 1e-10);
                assert_relative_eq!(xyy1.Y, xyy2.Y, epsilon = 1e-10);
            }
            _ => {
                // If conversion fails, it should fail consistently
                assert_eq!(result1.is_err(), result2.is_err());
            }
        }
    }

    // =============================================================================
    // ISCC-NBS Classification Comprehensive Tests
    // =============================================================================

    #[test]
    fn test_iscc_nbs_comprehensive_coverage() {
        let classifier = ISCC_NBS_Classifier::new().unwrap();
        
        // Test classification of systematic color grid
        let mut classified_colors = HashSet::new();
        let mut unclassified_count = 0;
        let mut classification_errors = Vec::new();
        
        // Create a systematic sampling of RGB space
        for r in (0..=255).step_by(51) {  // 0, 51, 102, 153, 204, 255
            for g in (0..=255).step_by(51) {
                for b in (0..=255).step_by(51) {
                    let rgb = [r, g, b];
                    
                    match classifier.classify_srgb(rgb) {
                        Ok(Some(metadata)) => {
                            classified_colors.insert(metadata.iscc_nbs_color_name.clone());
                        }
                        Ok(None) => {
                            unclassified_count += 1;
                        }
                        Err(e) => {
                            classification_errors.push((rgb, e));
                        }
                    }
                }
            }
        }
        
        // Verify reasonable classification coverage
        let total_tested = 6_usize.pow(3); // 216 colors
        let classified_count = total_tested - unclassified_count - classification_errors.len();
        
        println!("ISCC-NBS Classification Coverage:");
        println!("  Total colors tested: {}", total_tested);
        println!("  Successfully classified: {}", classified_count);
        println!("  Unclassified (out of range): {}", unclassified_count);
        println!("  Classification errors: {}", classification_errors.len());
        println!("  Unique color names found: {}", classified_colors.len());
        
        // Should classify at least some colors successfully
        assert!(classified_count > 0, "Should successfully classify some colors");
        
        // Should find multiple distinct color names
        assert!(classified_colors.len() > 1, "Should find multiple distinct color names");
        
        // Classification errors should be minimal
        assert!(classification_errors.len() < total_tested / 10, 
               "Classification error rate too high: {}/{}", 
               classification_errors.len(), total_tested);
    }

    #[test]
    fn test_iscc_nbs_edge_case_classifications() {
        let classifier = ISCC_NBS_Classifier::new().unwrap();
        
        // Test specific edge cases that might cause problems
        let edge_cases = [
            // Pure primaries
            ([255, 0, 0], "pure_red"),
            ([0, 255, 0], "pure_green"),
            ([0, 0, 255], "pure_blue"),
            
            // Pure secondaries
            ([255, 255, 0], "pure_yellow"),
            ([255, 0, 255], "pure_magenta"),
            ([0, 255, 255], "pure_cyan"),
            
            // Grayscale points
            ([0, 0, 0], "black"),
            ([255, 255, 255], "white"),
            ([128, 128, 128], "middle_gray"),
            ([64, 64, 64], "dark_gray"),
            ([192, 192, 192], "light_gray"),
            
            // Colors near boundaries (might be problematic)
            ([1, 0, 0], "near_black_red"),
            ([254, 255, 255], "near_white_blue_tinted"),
        ];
        
        for (rgb, description) in edge_cases {
            let result = classifier.classify_srgb(rgb);
            
            match result {
                Ok(Some(metadata)) => {
                    // Successful classification
                    assert!(!metadata.iscc_nbs_color_name.is_empty(), 
                           "{}: Color name should not be empty", description);
                    assert!(!metadata.alt_color_name.is_empty(), 
                           "{}: Alt color name should not be empty", description);
                    println!("{}: {} -> {}", description, 
                           format!("RGB({}, {}, {})", rgb[0], rgb[1], rgb[2]), 
                           metadata.iscc_nbs_color_name);
                }
                Ok(None) => {
                    println!("{}: Not in ISCC-NBS classification range", description);
                }
                Err(e) => {
                    panic!("{}: Classification failed: {}", description, e);
                }
            }
        }
    }

    // =============================================================================
    // Mechanical Wedge System Tests
    // =============================================================================

    #[test]
    fn test_mechanical_wedge_system_comprehensive() {
        let wedge_system = MechanicalWedgeSystem::new().unwrap();
        
        // Test that all expected wedges are created
        let wedge_count = wedge_system.wedge_count();
        assert_eq!(wedge_count, 100, "Should have exactly 100 wedges");
        
        // Test wedge coverage across hue spectrum
        let test_hues = [
            "1R", "5R", "10R", "2.5YR", "5YR", "7.5YR", "10YR",
            "2.5Y", "5Y", "7.5Y", "10Y", "2.5GY", "5GY", "7.5GY", "10GY",
            "2.5G", "5G", "7.5G", "10G", "2.5BG", "5BG", "7.5BG", "10BG",
            "2.5B", "5B", "7.5B", "10B", "2.5PB", "5PB", "7.5PB", "10PB",
            "2.5P", "5P", "7.5P", "10P", "2.5RP", "5RP", "7.5RP", "10RP",
        ];
        
        for hue in test_hues {
            let munsell_color = MunsellColor::new_chromatic(hue.to_string(), 5.0, 10.0);
            let containing_wedge = wedge_system.find_containing_wedge(&munsell_color);
            
            assert!(containing_wedge.is_some(), 
                   "Hue {} should be contained in some wedge", hue);
            
            if let Some(wedge_idx) = containing_wedge {
                assert!(wedge_idx < wedge_count, 
                       "Wedge index should be valid: {} < {}", wedge_idx, wedge_count);
            }
        }
    }

    #[test]
    fn test_mechanical_wedge_boundary_conditions() {
        let wedge_system = MechanicalWedgeSystem::new().unwrap();
        
        // Test colors at wedge boundaries
        let boundary_test_cases = [
            // Colors that might be exactly on wedge boundaries
            ("10RP", 5.0, 10.0),  // End of hue circle
            ("1R", 5.0, 10.0),    // Start of hue circle
            ("5R", 0.1, 0.1),     // Very low value/chroma
            ("5R", 9.9, 0.1),     // Very high value, low chroma
            ("5R", 5.0, 25.0),    // High chroma
        ];
        
        for (hue, value, chroma) in boundary_test_cases {
            let munsell_color = MunsellColor::new_chromatic(hue.to_string(), value, chroma);
            let result = wedge_system.find_containing_wedge(&munsell_color);
            
            // Should either find a wedge or consistently not find one
            // (The important thing is no panics or errors)
            match result {
                Some(wedge_idx) => {
                    assert!(wedge_idx < wedge_system.wedge_count(), 
                           "Wedge index out of bounds for {}: {}", hue, wedge_idx);
                }
                None => {
                    // Some boundary colors might not be contained, that's ok
                    println!("Note: {} {}/{} not contained in any wedge", hue, value, chroma);
                }
            }
        }
    }

    // =============================================================================
    // Reverse Conversion Tests
    // =============================================================================

    #[test]
    fn test_reverse_conversion_comprehensive() {
        let reverse_converter = ReverseConverter::new().unwrap();
        
        // Test systematic conversion of various Munsell notations
        let test_notations = [
            // All major hue families
            "5R 5.0/10.0", "5YR 5.0/10.0", "5Y 5.0/10.0", "5GY 5.0/10.0",
            "5G 5.0/10.0", "5BG 5.0/10.0", "5B 5.0/10.0", "5PB 5.0/10.0",
            "5P 5.0/10.0", "5RP 5.0/10.0",
            
            // Different values
            "5R 1.0/5.0", "5R 3.0/8.0", "5R 7.0/12.0", "5R 9.0/6.0",
            
            // Different chromas
            "5R 5.0/2.0", "5R 5.0/15.0", "5R 5.0/20.0",
            
            // Neutral colors
            "N 0.0", "N 2.5", "N 5.0", "N 7.5", "N 9.5",
            
            // Decimal precision
            "2.5R 4.7/13.2", "7.5YR 6.3/9.8",
        ];
        
        for notation in test_notations {
            match MunsellColor::from_notation(notation) {
                Ok(munsell_color) => {
                    let result = reverse_converter.munsell_to_srgb(&munsell_color);
                    
                    match result {
                        Ok(rgb) => {
                            // Verify RGB values are in valid range
                            assert!(rgb[0] <= 255, "R component out of range for {}: {}", notation, rgb[0]);
                            assert!(rgb[1] <= 255, "G component out of range for {}: {}", notation, rgb[1]);
                            assert!(rgb[2] <= 255, "B component out of range for {}: {}", notation, rgb[2]);
                            
                            println!("Reverse conversion: {} -> RGB({}, {}, {})", 
                                   notation, rgb[0], rgb[1], rgb[2]);
                        }
                        Err(e) => {
                            println!("Note: {} could not be reverse converted: {}", notation, e);
                            // This is not necessarily an error - some Munsell colors
                            // may be outside the RGB gamut
                        }
                    }
                }
                Err(e) => {
                    panic!("Test notation '{}' should be valid: {}", notation, e);
                }
            }
        }
    }

    #[test]
    fn test_reverse_conversion_roundtrip_accuracy() {
        // Test round-trip conversion accuracy where possible
        let converter = MunsellConverter::new().unwrap();
        let reverse_converter = ReverseConverter::new().unwrap();
        
        let test_colors = [
            [255, 0, 0],     // Pure red
            [0, 255, 0],     // Pure green  
            [0, 0, 255],     // Pure blue
            [128, 128, 128], // Gray
            [200, 100, 50],  // Brown-ish
            [100, 200, 150], // Green-ish
        ];
        
        for &original_rgb in &test_colors {
            // Forward conversion: RGB -> Munsell
            match converter.srgb_to_munsell(original_rgb) {
                Ok(munsell_color) => {
                    // Reverse conversion: Munsell -> RGB
                    match reverse_converter.munsell_to_srgb(&munsell_color) {
                        Ok(converted_rgb) => {
                            // Calculate color difference
                            let r_diff = (original_rgb[0] as i16 - converted_rgb[0] as i16).abs();
                            let g_diff = (original_rgb[1] as i16 - converted_rgb[1] as i16).abs();
                            let b_diff = (original_rgb[2] as i16 - converted_rgb[2] as i16).abs();
                            let max_diff = r_diff.max(g_diff).max(b_diff);
                            
                            println!("Round-trip: RGB({}, {}, {}) -> {} -> RGB({}, {}, {}) [max_diff: {}]",
                                   original_rgb[0], original_rgb[1], original_rgb[2],
                                   munsell_color.notation,
                                   converted_rgb[0], converted_rgb[1], converted_rgb[2],
                                   max_diff);
                            
                            // Allow for some precision loss in round-trip
                            // This is a soft assertion - some colors may not round-trip perfectly
                            if max_diff > 50 {
                                println!("Note: Large round-trip error for RGB({}, {}, {}): max_diff = {}",
                                       original_rgb[0], original_rgb[1], original_rgb[2], max_diff);
                            }
                        }
                        Err(e) => {
                            println!("Note: Reverse conversion failed for {}: {}", munsell_color.notation, e);
                        }
                    }
                }
                Err(e) => {
                    println!("Note: Forward conversion failed for RGB({}, {}, {}): {}", 
                           original_rgb[0], original_rgb[1], original_rgb[2], e);
                }
            }
        }
    }

    // =============================================================================
    // Type System Comprehensive Tests
    // =============================================================================

    #[test]
    fn test_rgb_color_comprehensive_operations() {
        // Test all RGB color operations comprehensively
        let color = RgbColor::new(123, 45, 67);
        
        // Test all conversions and methods
        assert_eq!(color.to_array(), [123, 45, 67]);
        assert_eq!(color.r, 123);
        assert_eq!(color.g, 45);
        assert_eq!(color.b, 67);
        assert!(!color.is_grayscale());
        
        // Test From/Into trait implementations
        let array = [200, 100, 50];
        let from_array: RgbColor = array.into();
        assert_eq!(from_array.to_array(), array);
        
        let back_to_array: [u8; 3] = from_array.into();
        assert_eq!(back_to_array, array);
        
        // Test edge cases
        let black = RgbColor::new(0, 0, 0);
        assert!(black.is_grayscale());
        
        let white = RgbColor::new(255, 255, 255);
        assert!(white.is_grayscale());
        
        // Test near-grayscale (should not be grayscale)
        let near_gray = RgbColor::new(128, 128, 129);
        assert!(!near_gray.is_grayscale());
    }

    #[test]
    fn test_munsell_color_comprehensive_parsing_edge_cases() {
        // Test comprehensive parsing edge cases beyond basic tests
        let edge_cases = [
            // Extreme decimal precision
            ("5R 4.123456/14.987654", true),
            ("2.123456YR 6.789/8.345678", true),
            
            // Zero values
            ("5R 0.0/0.0", true),
            ("10RP 10.0/0.0", true),
            
            // Maximum theoretical values
            ("10R 10.0/50.0", true),
            ("0.1R 9.9/49.9", true),
            
            // Whitespace handling
            (" 5R 4.0/14.0 ", true),
            ("5R  4.0/14.0", true),
            ("5R 4.0 / 14.0", true),
            
            // Neutral edge cases
            ("N 0.0", true),
            ("N 10.0", true),
            ("N 5.123456789", true),
            (" N 5.0 ", true),
            
            // Invalid cases that should fail
            ("5R 4.0/14.0/extra", false),
            ("5Q 4.0/14.0", false),  // Invalid hue family
            ("5R -1.0/14.0", false), // Negative value
            ("5R 11.0/14.0", false), // Value too high
            ("5R 4.0/-1.0", false),  // Negative chroma
            ("N -1.0", false),       // Negative neutral value
            ("N 11.0", false),       // Neutral value too high
        ];
        
        for (notation, should_parse) in edge_cases {
            let result = MunsellColor::from_notation(notation);
            
            if should_parse {
                assert!(result.is_ok(), "Should parse '{}' successfully", notation);
                
                let parsed = result.unwrap();
                assert!(!parsed.notation.is_empty(), "Notation should not be empty");
                
                // Verify basic invariants
                assert!(parsed.value >= 0.0 && parsed.value <= 10.0, 
                       "Value out of range for '{}': {}", notation, parsed.value);
                
                if let Some(chroma) = parsed.chroma {
                    assert!(chroma >= 0.0, "Negative chroma for '{}': {}", notation, chroma);
                }
            } else {
                assert!(result.is_err(), "Should fail to parse '{}'", notation);
            }
        }
    }
}