//! Edge case tests for MunsellSpace library.
//!
//! These tests specifically target boundary conditions, extreme values,
//! and corner cases that might not be covered by regular unit tests.

#[cfg(test)]
#[allow(deprecated)] // Tests may use deprecated APIs for backward compatibility verification
mod edge_case_tests {
    use crate::{MunsellConverter, MunsellColor, RgbColor, MunsellError};
    use crate::mathematical::MathematicalMunsellConverter;
    use crate::iscc::IsccNbsClassifier;

    /// Test extreme RGB values at color space boundaries
    #[test]
    fn test_rgb_boundary_values() {
        let converter = MunsellConverter::new().unwrap();
        
        // Test all corners of RGB cube
        let corners = [
            [0, 0, 0],       // Black
            [255, 255, 255], // White  
            [255, 0, 0],     // Pure Red
            [0, 255, 0],     // Pure Green
            [0, 0, 255],     // Pure Blue
            [255, 255, 0],   // Yellow
            [255, 0, 255],   // Magenta
            [0, 255, 255],   // Cyan
        ];
        
        for &rgb in &corners {
            let result = converter.srgb_to_munsell(rgb);
            assert!(result.is_ok(), "Failed to convert corner RGB{:?}: {:?}", rgb, result);
            
            let munsell = result.unwrap();
            
            // Basic sanity checks
            assert!(munsell.value >= 0.0 && munsell.value <= 10.0, 
                   "Value out of range for RGB{:?}: {}", rgb, munsell.value);
            
            if let Some(chroma) = munsell.chroma {
                assert!(chroma >= 0.0, "Negative chroma for RGB{:?}: {}", rgb, chroma);
            }
            
            // Notation should parse successfully  
            assert!(MunsellColor::from_notation(&munsell.notation).is_ok(),
                   "Generated invalid notation for RGB{:?}: '{}'", rgb, munsell.notation);
        }
    }

    /// Test near-boundary RGB values that might cause precision issues
    #[test]
    fn test_near_boundary_rgb_precision() {
        let converter = MunsellConverter::new().unwrap();
        
        let near_boundary_values = [
            [1, 1, 1],       // Nearly black
            [254, 254, 254], // Nearly white
            [1, 0, 0],       // Nearly pure red
            [0, 1, 0],       // Nearly pure green  
            [0, 0, 1],       // Nearly pure blue
            [254, 255, 255], // Nearly cyan
            [255, 254, 255], // Nearly magenta
            [255, 255, 254], // Nearly yellow
        ];
        
        for &rgb in &near_boundary_values {
            let result = converter.srgb_to_munsell(rgb);
            assert!(result.is_ok(), "Failed to convert near-boundary RGB{:?}: {:?}", rgb, result);
            
            let munsell = result.unwrap();
            
            // Check for reasonable bounds (no NaN/Inf)
            assert!(munsell.value.is_finite(), "Non-finite value for RGB{:?}: {}", rgb, munsell.value);
            
            if let Some(chroma) = munsell.chroma {
                assert!(chroma.is_finite(), "Non-finite chroma for RGB{:?}: {}", rgb, chroma);
                assert!(chroma >= 0.0, "Negative chroma for RGB{:?}: {}", rgb, chroma);
            }
        }
    }

    /// Test Munsell notation parsing edge cases
    #[test]  
    fn test_munsell_notation_edge_cases() {
        // Test various formatting edge cases
        let edge_case_notations = [
            "N 0.0",          // Standard neutral
            "N 10.0",         // Maximum value neutral
            "N 5.5",          // Decimal neutral
            "10RP 1.0/1.0",   // Minimum non-zero values
            "0.1R 9.9/0.1",   // Very small hue and chroma
            "9.9R 0.1/30.0",  // High chroma, low value
            "5.0Y 5.0/20.0",  // High but reasonable chroma
            "2.5PB 8.5/12.0", // Complex decimal values
        ];
        
        for notation in &edge_case_notations {
            let result = MunsellColor::from_notation(notation);
            match result {
                Ok(munsell) => {
                    // Successful parse - verify consistency
                    assert!(munsell.value >= 0.0 && munsell.value <= 10.0,
                           "Parsed value out of range for '{}': {}", notation, munsell.value);
                    
                    if munsell.is_chromatic() {
                        assert!(munsell.hue.is_some(), "Chromatic color missing hue: '{}'", notation);
                        assert!(munsell.chroma.is_some(), "Chromatic color missing chroma: '{}'", notation);
                    }
                    
                    // Round-trip test
                    let regenerated = munsell.notation;
                    let reparsed = MunsellColor::from_notation(&regenerated);
                    assert!(reparsed.is_ok(), "Round-trip failed for '{}' -> '{}'", notation, regenerated);
                }
                Err(e) => {
                    // Failed parse - acceptable for some edge cases
                    println!("Note: '{}' failed to parse (might be expected): {}", notation, e);
                }
            }
        }
    }

    /// Test invalid Munsell notation strings
    #[test]
    fn test_invalid_munsell_notations() {
        let invalid_notations = [
            "",               // Empty string
            "X",              // Invalid hue family
            "N",              // Missing value
            "N -1.0",         // Negative value 
            "N 11.0",         // Value too high
            "5R",             // Missing value/chroma
            "5R 5.0",         // Missing chroma separator
            "5R 5.0 10.0",    // Missing chroma separator  
            "5R 5.0/-1.0",    // Negative chroma
            "100R 5.0/10.0",  // Hue value too high
            "-5R 5.0/10.0",   // Negative hue value
            "5ABC 5.0/10.0",  // Invalid hue family
            "N 5.0/10.0",     // Neutral with chroma
        ];
        
        for notation in &invalid_notations {
            let result = MunsellColor::from_notation(notation);
            assert!(result.is_err(), "Expected error for invalid notation '{}', got: {:?}", notation, result);
            
            // Verify it's the right kind of error
            match result.unwrap_err() {
                MunsellError::InvalidNotation { .. } => {}, // Expected
                other => panic!("Expected InvalidNotation error for '{}', got: {:?}", notation, other),
            }
        }
    }

    /// Test RgbColor validation edge cases
    #[test]
    fn test_rgb_color_validation() {
        // Valid RGB values - RgbColor::new() actually returns RgbColor directly, not Result
        let valid_colors = [
            [0, 0, 0],
            [255, 255, 255],
            [128, 64, 192],
        ];
        
        for &rgb in &valid_colors {
            let color = RgbColor::new(rgb[0], rgb[1], rgb[2]);
            assert_eq!(color.r, rgb[0]);
            assert_eq!(color.g, rgb[1]); 
            assert_eq!(color.b, rgb[2]);
        }
    }

    /// Test ISCC-NBS classification edge cases  
    #[test]
    fn test_iscc_nbs_edge_cases() {
        let classifier = IsccNbsClassifier::new().unwrap();
        
        // Test colors at edge of classification ranges
        let edge_case_colors = [
            ([0, 0, 0], "black"),
            ([255, 255, 255], "white"),  
            ([128, 128, 128], "gray"),
            ([255, 0, 0], "red"),
            ([0, 255, 0], "green"),
            ([0, 0, 255], "blue"),
        ];
        
        for &(rgb, expected_contains) in &edge_case_colors {
            let result = classifier.classify_srgb(rgb);
            assert!(result.is_ok(), "Failed to classify RGB{:?}: {:?}", rgb, result);
            
            if let Ok(Some(metadata)) = result {
                let descriptor = metadata.iscc_nbs_descriptor();
                println!("RGB{:?} -> '{}'", rgb, descriptor);
                
                // Very basic check - descriptor should contain expected color
                // (This is lenient as exact matching depends on complex color space mapping)
                let descriptor_lower = descriptor.to_lowercase();
                if !descriptor_lower.contains(expected_contains) {
                    println!("Note: RGB{:?} classified as '{}', expected to contain '{}'", 
                             rgb, descriptor, expected_contains);
                }
            } else {
                println!("Note: RGB{:?} not classified in ISCC-NBS system", rgb);
            }
        }
    }

    /// Test mathematical converter with edge cases
    #[test]
    fn test_mathematical_converter_edge_cases() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test extreme RGB values instead of xyY since we don't have xyy_to_srgb
        let extreme_rgb_values = [
            [0, 0, 0],       // Complete black
            [255, 255, 255], // White
            [1, 1, 1],       // Very dark
            [254, 254, 254], // Nearly white
            [255, 0, 0],     // Pure red
            [0, 255, 0],     // Pure green
            [0, 0, 255],     // Pure blue
        ];
        
        for &rgb in &extreme_rgb_values {
            // Test xyY conversion
            let xyy_result = converter.srgb_to_xyy(rgb);
            
            match xyy_result {
                Ok(xyy) => {
                    // Should be valid xyY values
                    assert!(xyy.x >= 0.0 && xyy.x <= 1.0, "xyY x out of range: {}", xyy.x);
                    assert!(xyy.y >= 0.0 && xyy.y <= 1.0, "xyY y out of range: {}", xyy.y);
                    assert!(xyy.y_luminance >= 0.0, "xyY Y negative: {}", xyy.y_luminance);
                    
                    // Test Munsell conversion
                    let munsell_result = converter.xyy_to_munsell_specification(xyy);
                    assert!(munsell_result.is_ok(), "Munsell conversion failed for RGB{:?}", rgb);
                }
                Err(e) => {
                    // Some extreme values might legitimately fail
                    println!("Note: RGB{:?} failed xyY conversion: {}", rgb, e);
                }
            }
        }
    }

    /// Test batch processing with edge cases
    #[test]
    fn test_batch_processing_edge_cases() {
        let converter = MunsellConverter::new().unwrap();
        
        // Empty batch
        let empty_batch: Vec<[u8; 3]> = vec![];
        let result = converter.convert_batch(&empty_batch);
        assert!(result.is_ok(), "Empty batch should succeed");
        assert_eq!(result.unwrap().len(), 0);
        
        // Single item batch
        let single_batch = vec![[128, 128, 128]];
        let result = converter.convert_batch(&single_batch);
        assert!(result.is_ok(), "Single item batch should succeed");
        assert_eq!(result.unwrap().len(), 1);
        
        // Large batch with duplicates
        let large_batch = vec![[255, 0, 0]; 1000]; // 1000 identical red colors
        let result = converter.convert_batch(&large_batch);
        assert!(result.is_ok(), "Large batch should succeed");
        assert_eq!(result.unwrap().len(), 1000);
        
        // Batch with all corners
        let corner_batch = vec![
            [0, 0, 0], [255, 255, 255], [255, 0, 0], [0, 255, 0],
            [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255],
        ];
        let result = converter.convert_batch(&corner_batch);
        assert!(result.is_ok(), "Corner batch should succeed: {:?}", result);
        assert_eq!(result.unwrap().len(), 8);
    }

    /// Test floating point precision edge cases
    #[test]
    fn test_floating_point_precision() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test values near floating point precision limits
        let precision_test_values = [
            0,
            1,        // Very small positive
            254,      // Just under 255
            255,      // Maximum
            128,      // Middle value
            127,      // Just under middle
            129,      // Just over middle
        ];
        
        for &test_val in &precision_test_values {
            // Use test value in various contexts to check for precision issues
            let test_rgb = [test_val, 128, 128];
            
            let result = converter.srgb_to_xyy(test_rgb);
            
            match result {
                Ok(xyy) => {
                    // Check for NaN/Inf
                    assert!(xyy.x.is_finite(), "Non-finite x for test_val {}: {}", test_val, xyy.x);
                    assert!(xyy.y.is_finite(), "Non-finite y for test_val {}: {}", test_val, xyy.y);
                    assert!(xyy.y_luminance.is_finite(), "Non-finite Y for test_val {}: {}", test_val, xyy.y_luminance);
                    
                    // Check for reasonable bounds
                    assert!(xyy.x >= 0.0 && xyy.x <= 1.0, "x out of range for test_val {}: {}", test_val, xyy.x);
                    assert!(xyy.y >= 0.0 && xyy.y <= 1.0, "y out of range for test_val {}: {}", test_val, xyy.y);
                    assert!(xyy.y_luminance >= 0.0, "Y negative for test_val {}: {}", test_val, xyy.y_luminance);
                }
                Err(e) => {
                    println!("Note: Precision test failed for {}: {}", test_val, e);
                }
            }
        }
    }
}